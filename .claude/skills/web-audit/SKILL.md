---
name: web-audit
description: Run a structured audit of a web page or site across technical SEO, on-page content, structured data, performance, and UX, and return a prioritised fix list. Use when asked to audit a website, do a sitecheck, review SEO/technical health, or find why a page underperforms. Combines two dependency-free scanners (on-page signals + broken links) with agent judgement per dimension.
license: See LICENSE.md
---

# Website Audit

A repeatable, multi-dimension audit that a single "review my site" prompt cannot match. Each dimension is checked by an agent that fetches the real page, uses the bundled scanners for the objective signals, and reports issues ranked by impact, so you get a punch list, not a vibe.

The two scripts do the mechanical work (extracting on-page signals, proving which links are broken); the agents do the judgement (is the content actually good, is the structured data right for this page, will this hurt Core Web Vitals). The report says which is which.

## When to use

Trigger for any "audit this website / sitecheck / why is this page not ranking / technical SEO review" request. For a single quick signal dump, run `scripts/fetch-audit.mjs <url>` on its own.

## Inputs

- **target** — a URL (required). For a multi-page audit, a list of URLs or the key templates (home, category, product, article).
- **goal** — optional: what the page is for (rank for X, convert, inform). Sharpens the content and UX judgement.
- **primary keyword** — optional, for the on-page relevance check.

## Run order

**1. Machine baseline (do this first).**

- `node scripts/fetch-audit.mjs <url>` — title/meta lengths, canonical, robots, viewport, headings, images (alt + dimensions), Open Graph, JSON-LD types, insecure references, word count, with severity flags. Add `--json` to feed the agents.
- `node scripts/link-check.mjs <url>` — every link's HTTP status; broken (4xx/5xx) and redirects are proven, not guessed. Use `--internal-only` to focus.

**2. Dimension passes (agents, or sequential in one context).** Work through `references/dimensions.md`. Split across agents, one per dimension, then synthesise:

- **Technical SEO & crawlability** (`references/agents/technical-seo.md`) — indexability (noindex, robots.txt, canonical), redirects and status codes, https and mixed content, sitemap/hreflang where relevant, URL structure, and the broken-link results.
- **On-page & content** (`references/agents/onpage-content.md`) — title/meta quality and intent match, heading structure, content depth and usefulness, keyword relevance without stuffing, internal linking.
- **Structured data & social** (`references/agents/structured-data.md`) — is the JSON-LD present, valid, and the *right type* for the page? rich-result eligibility, and Open Graph / Twitter cards for sharing.
- **Performance & UX** (`references/agents/performance-ux.md`) — signals that predict Core Web Vitals (image weight/format/dimensions, render-blocking, layout-shift risk), mobile-friendliness, and obvious UX friction. Recommend a lab run (Lighthouse / PageSpeed Insights) for real field metrics.

For a deep accessibility pass, hand off to the dedicated **accessibility-audit** skill; this audit only flags obvious a11y issues in passing.

**3. Synthesis.** Merge everything into one report per `references/report-format.md`, ranked by impact × effort.

## Principles

- **Prove the objective, judge the rest.** Never report a broken link or a missing tag you did not get from a script run. Never pass off "content looks fine" as a real content review.
- **Impact over inventory.** A noindex on a key page or a broken checkout link outranks fifty missing image dimensions. Rank by what it costs the site's goal.
- **Every finding ships a fix and a reason.** Say what to change, and why it matters (ranking, conversion, sharing, speed).
- **Name the limits.** On-page signals are not field performance. Where only a lab tool or crawl can confirm something, say so and recommend it rather than bluffing.

## Output

One report (`references/report-format.md`): a verdict, a prioritised issue table (dimension, severity, impact, fix), quick wins vs bigger projects, and an appendix with the raw script output. For a multi-page audit, group findings that repeat across templates.

## What this skill will not do

- It will not report field Core Web Vitals or a crawl of the whole site from on-page signals alone; it flags risks and points you to the right lab/crawl tool.
- It will not invent a metric (traffic, ranking position) it cannot see. It audits what is on the page and what the scripts prove.
