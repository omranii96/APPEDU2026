#!/usr/bin/env node
// Website Audit — on-page signal extractor. Zero dependencies, Node 18+.
//
// Fetches a URL (or reads a local HTML file) and extracts the objective on-page
// SEO / technical signals a script can check reliably: title & meta lengths,
// canonical, robots, viewport, headings, images, Open Graph, structured data,
// insecure references, and more. Feeds the audit agents so they interpret real
// data instead of guessing, and gives you a fast machine baseline on its own.
//
// Usage:
//   node fetch-audit.mjs https://example.com
//   node fetch-audit.mjs page.html
//   node fetch-audit.mjs https://example.com --json     # raw JSON only
//
// Exit code 1 if any high-severity flag fires (missing title, no h1, noindex...).

import { readFileSync } from 'node:fs'

const arg = process.argv[2]
const jsonOnly = process.argv.includes('--json')
if (!arg) { console.error('Usage: node fetch-audit.mjs <https://url | file.html> [--json]'); process.exit(2) }

const isURL = /^https?:\/\//i.test(arg)
let html, finalUrl = arg, status = null
if (isURL) {
  try {
    const res = await fetch(arg, { redirect: 'follow', headers: { 'user-agent': 'CreativeDeals-web-audit/1.0' } })
    status = res.status
    finalUrl = res.url
    html = await res.text()
  } catch (e) { console.error('fetch failed:', e.message); process.exit(2) }
} else {
  html = readFileSync(arg, 'utf8')
}

// ── helpers ──────────────────────────────────────────────────────────────────
const first = (re) => { const m = html.match(re); return m ? (m[1] ?? m[0]).trim() : null }
const metaContent = (name, attr = 'name') => {
  const re = new RegExp(`<meta[^>]*\\b${attr}\\s*=\\s*["']${name}["'][^>]*>`, 'i')
  const tag = html.match(re)
  if (!tag) return null
  const c = tag[0].match(/\bcontent\s*=\s*("([^"]*)"|'([^']*)')/i)
  return c ? (c[2] ?? c[3]).trim() : null
}
const count = (re) => (html.match(re) || []).length
const len = (s) => (s ? [...s].length : 0)

// ── extract ──────────────────────────────────────────────────────────────────
const title = first(/<title[^>]*>([\s\S]*?)<\/title>/i)
const desc = metaContent('description')
const robots = metaContent('robots')
const canonical = (html.match(/<link[^>]*\brel\s*=\s*["']canonical["'][^>]*>/i)?.[0].match(/\bhref\s*=\s*("([^"]*)"|'([^']*)')/i)) || null
const canonicalUrl = canonical ? (canonical[2] ?? canonical[3]) : null
const viewport = metaContent('viewport')
const charset = !!html.match(/<meta[^>]*\bcharset\b/i)
const lang = first(/<html[^>]*\blang\s*=\s*["']([^"']+)["']/i)
const h1 = count(/<h1\b/gi)
const headings = [...html.matchAll(/<h([1-6])\b/gi)].map(m => Number(m[1]))
const imgs = html.match(/<img\b[^>]*>/gi) || []
const imgNoAlt = imgs.filter(t => !/\balt\s*=/i.test(t)).length
const imgNoDims = imgs.filter(t => !/\bwidth\s*=/i.test(t) || !/\bheight\s*=/i.test(t)).length
const og = { title: !!metaContent('og:title', 'property'), description: !!metaContent('og:description', 'property'), image: !!metaContent('og:image', 'property') }
const twitter = !!metaContent('twitter:card')
const jsonld = [...html.matchAll(/<script[^>]*type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)]
const jsonldTypes = []
for (const m of jsonld) { const t = m[1].match(/"@type"\s*:\s*"([^"]+)"/g); if (t) jsonldTypes.push(...t.map(x => x.match(/"([^"]+)"$/)[1])) }
const bodyText = html.replace(/<script[\s\S]*?<\/script>/gi, '').replace(/<style[\s\S]*?<\/style>/gi, '').replace(/<[^>]+>/g, ' ')
const words = (bodyText.match(/\p{L}+/gu) || []).length
const insecure = isURL && /^https:/i.test(finalUrl)
  ? [...html.matchAll(/\b(?:src|href)\s*=\s*["'](http:\/\/[^"']+)/gi)].map(m => m[1]).length
  : 0

// ── flags (severity) ─────────────────────────────────────────────────────────
const flags = []
const flag = (sev, msg) => flags.push({ sev, msg })
if (status && status >= 400) flag('high', `HTTP ${status}`)
if (!title) flag('high', 'Missing <title>')
else if (len(title) < 15 || len(title) > 65) flag('med', `Title length ${len(title)} (aim 15-65)`)
if (!desc) flag('med', 'Missing meta description')
else if (len(desc) < 70 || len(desc) > 165) flag('low', `Meta description length ${len(desc)} (aim 70-165)`)
if (robots && /noindex/i.test(robots)) flag('high', `robots contains noindex (${robots})`)
if (!canonicalUrl) flag('low', 'No canonical link')
if (!viewport) flag('high', 'No viewport meta (not mobile-friendly)')
if (!lang) flag('med', 'No lang attribute on <html>')
if (h1 === 0) flag('high', 'No <h1>')
else if (h1 > 1) flag('med', `${h1} <h1> elements (expected 1)`)
let prev = 0, jumps = 0
for (const l of headings) { if (prev && l > prev + 1) jumps++; prev = l }
if (jumps) flag('low', `${jumps} heading-level jump(s)`)
if (imgNoAlt) flag('med', `${imgNoAlt}/${imgs.length} images without alt`)
if (imgNoDims) flag('low', `${imgNoDims}/${imgs.length} images without width/height (layout shift)`)
if (!og.title || !og.image) flag('low', 'Incomplete Open Graph tags (poor social preview)')
if (jsonldTypes.length === 0) flag('low', 'No JSON-LD structured data')
if (insecure) flag('high', `${insecure} insecure http:// reference(s) on an https page (mixed content)`)
if (words < 250 && !isURL === false) flag('low', `Thin content (~${words} words)`)

const result = {
  url: finalUrl, status,
  title, titleLength: len(title),
  metaDescription: desc, metaDescriptionLength: len(desc),
  robots, canonical: canonicalUrl, viewport, charset, lang,
  h1Count: h1, headingOutline: headings,
  images: { total: imgs.length, missingAlt: imgNoAlt, missingDimensions: imgNoDims },
  openGraph: og, twitterCard: twitter,
  structuredData: { blocks: jsonld.length, types: [...new Set(jsonldTypes)] },
  wordCount: words, insecureRefs: insecure,
  flags,
}

// ── output ───────────────────────────────────────────────────────────────────
if (jsonOnly) { console.log(JSON.stringify(result, null, 2)); process.exit(flags.some(f => f.sev === 'high') ? 1 : 0) }

console.log(`On-page audit — ${finalUrl}${status ? `  (HTTP ${status})` : ''}\n`)
console.log(`  title        ${title ? `"${title}" (${len(title)})` : '— MISSING'}`)
console.log(`  description  ${desc ? `(${len(desc)} chars)` : '— MISSING'}`)
console.log(`  canonical    ${canonicalUrl || '—'}`)
console.log(`  robots       ${robots || '—'}    lang ${lang || '—'}    viewport ${viewport ? 'yes' : 'NO'}`)
console.log(`  headings     h1×${h1}   outline ${headings.join('') || '—'}`)
console.log(`  images       ${imgs.length} (no-alt ${imgNoAlt}, no-dims ${imgNoDims})`)
console.log(`  social       OG ${og.title && og.image ? 'ok' : 'partial'}   twitter ${twitter ? 'yes' : 'no'}`)
console.log(`  schema       ${result.structuredData.blocks} block(s) ${result.structuredData.types.join(', ')}`)
console.log(`  content      ~${words} words   insecure refs ${insecure}`)
console.log('')
if (!flags.length) { console.log('No high/medium flags. Still run the audit dimensions for the judgement checks.') }
else {
  const order = { high: 0, med: 1, low: 2 }
  for (const f of flags.sort((a, b) => order[a.sev] - order[b.sev])) console.log(`  [${f.sev.toUpperCase().padEnd(4)}] ${f.msg}`)
}
process.exit(flags.some(f => f.sev === 'high') ? 1 : 0)
