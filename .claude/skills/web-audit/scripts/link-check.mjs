#!/usr/bin/env node
// Website Audit — broken link checker. Zero dependencies, Node 18+.
//
// Fetches a page, extracts its links, and checks each one's HTTP status so you
// know exactly which are broken (4xx/5xx), which redirect, and which error out.
// Broken links are a concrete, provable defect, hence a script, not a guess.
//
// Usage:
//   node link-check.mjs https://example.com          # check links found on the page
//   node link-check.mjs urls.txt                      # check a list (one URL per line)
//   node link-check.mjs https://example.com --internal-only
//
// Exit code 1 if any link is broken.

import { readFileSync } from 'node:fs'

const args = process.argv.slice(2)
const src = args.find(a => !a.startsWith('--'))
const internalOnly = args.includes('--internal-only')
const CONCURRENCY = 8
const CAP = 200
const TIMEOUT = 12000
if (!src) { console.error('Usage: node link-check.mjs <https://url | urls.txt> [--internal-only]'); process.exit(2) }

// ── build the list of URLs to check ──────────────────────────────────────────
let links = [], base = null
if (/^https?:\/\//i.test(src)) {
  base = new URL(src)
  let page
  try { page = await fetch(src, { headers: { 'user-agent': 'CreativeDeals-web-audit/1.0' } }).then(r => r.text()) }
  catch (e) { console.error('fetch page failed:', e.message); process.exit(2) }
  const hrefs = [...page.matchAll(/<a\b[^>]*\bhref\s*=\s*("([^"]*)"|'([^']*)')/gi)].map(m => m[2] ?? m[3])
  const seen = new Set()
  for (const h of hrefs) {
    if (!h || /^(mailto:|tel:|javascript:|#)/i.test(h)) continue
    let u
    try { u = new URL(h, base) } catch { continue }
    if (!/^https?:$/.test(u.protocol)) continue
    u.hash = ''
    const key = u.href
    if (seen.has(key)) continue
    seen.add(key)
    const internal = u.host === base.host
    if (internalOnly && !internal) continue
    links.push({ url: key, internal })
  }
} else {
  links = readFileSync(src, 'utf8').split('\n').map(s => s.trim()).filter(Boolean)
    .filter(u => /^https?:\/\//i.test(u)).map(u => ({ url: u, internal: true }))
}

let capped = false
if (links.length > CAP) { links = links.slice(0, CAP); capped = true }
if (!links.length) { console.log('No links found to check.'); process.exit(0) }
console.log(`Checking ${links.length} link(s)${base ? ` from ${base.href}` : ''}${capped ? ` (capped at ${CAP})` : ''}...\n`)

// ── check one URL (HEAD, fall back to GET) ───────────────────────────────────
async function check(link) {
  const withTimeout = (method) => {
    const ac = new AbortController()
    const t = setTimeout(() => ac.abort(), TIMEOUT)
    return fetch(link.url, { method, redirect: 'manual', signal: ac.signal, headers: { 'user-agent': 'CreativeDeals-web-audit/1.0' } })
      .finally(() => clearTimeout(t))
  }
  try {
    let res = await withTimeout('HEAD')
    if (res.status === 405 || res.status === 501 || res.status === 403) res = await withTimeout('GET')
    const loc = res.headers.get('location')
    return { ...link, status: res.status, redirect: res.status >= 300 && res.status < 400 ? loc : null }
  } catch (e) {
    return { ...link, status: 0, error: e.name === 'AbortError' ? 'timeout' : e.message }
  }
}

// ── run with a small concurrency pool ────────────────────────────────────────
const results = []
let i = 0
async function worker() { while (i < links.length) { const idx = i++; results[idx] = await check(links[idx]) } }
await Promise.all(Array.from({ length: Math.min(CONCURRENCY, links.length) }, worker))

// ── report ───────────────────────────────────────────────────────────────────
const broken = results.filter(r => r.status === 0 || r.status >= 400)
const redirects = results.filter(r => r.redirect)
const ok = results.length - broken.length - redirects.length

for (const r of broken) console.log(`  BROKEN  ${r.status || 'ERR'}  ${r.url}${r.error ? `  (${r.error})` : ''}`)
if (redirects.length) { console.log(''); for (const r of redirects) console.log(`  ${r.status} -> ${r.redirect || '?'}  ${r.url}`) }

console.log(`\n${ok} ok, ${redirects.length} redirect(s), ${broken.length} broken, of ${results.length} checked.`)
// Set exitCode and let the event loop drain instead of forcing process.exit(),
// which can race with closing fetch/abort handles and crash libuv on Windows.
process.exitCode = broken.length ? 1 : 0

