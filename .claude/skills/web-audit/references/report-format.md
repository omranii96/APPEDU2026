# Report format

One report per audit. Lead with the verdict and the highest-impact fixes. Every finding is actionable and explains why it matters.

## Structure

```markdown
# Website audit — <url>

**Audited:** <page or template>   **Date:** <date>
**Method:** automated (fetch-audit + link-check) + agent judgement per dimension

## Verdict
One paragraph: overall health, the count of critical vs minor issues, and the single highest-impact fix.

## Critical (fix first)
Issues that cost rankings, conversions, or block indexing.

| # | Issue | Dimension | Impact | Fix |
|---|-------|-----------|--------|-----|
| 1 | Page has `<meta robots=noindex>` | Technical SEO | Page cannot rank at all | Remove the noindex on production |
| 2 | 3 internal links 404 | Technical SEO | Wastes crawl budget, dead ends for users | Fix or redirect the 3 URLs (listed in appendix) |

## Important
Real issues with a smaller or slower impact (title/meta quality, thin content, missing schema, image weight).

## Quick wins
High-value, low-effort (add image dimensions, tighten a meta description, add OG image).

## Bigger projects
Worth doing but larger (content rewrite, structured-data rollout, performance work).

## Verified vs needs a tool
- **Proven by script:** broken links, on-page tags, insecure refs, heading/image signals.
- **Judged this audit:** content quality, keyword intent, schema correctness, layout-shift risk.
- **Needs a lab/crawl tool:** field Core Web Vitals (Lighthouse / PageSpeed Insights), full-site crawl, log analysis.

## Appendix — raw script output
The fetch-audit and link-check output, verbatim, including the exact broken URLs.
```

## Severity rule

Rank by **cost to the site's goal**, not by count:

- **Critical** — blocks indexing/ranking or a core task (noindex, broken checkout, canonical to the wrong page, site-wide mixed content).
- **Important** — measurably hurts performance/rankings/conversions (weak titles, thin content, missing/incorrect schema, heavy unoptimised images).
- **Minor / quick win** — small polish (one missing image dimension, a slightly long meta).

## Writing the fixes

- Give the concrete change (the tag, the code, the exact URLs), not "improve SEO".
- Explain the why in a few words: ranking, crawl, conversion, sharing, or speed.
- Never list a broken link or missing tag that did not come from an actual script run. Never present an on-page guess as a measured metric.
