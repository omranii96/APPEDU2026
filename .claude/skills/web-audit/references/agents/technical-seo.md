# Agent — Technical SEO & crawlability

Paste as a subagent prompt. Read `references/dimensions.md` (section 1) first.

**Target:** {{url}}
**fetch-audit output:** {{fetch_audit_json}}
**link-check output:** {{link_check_output}}

Judge and confirm:

- **Indexability** — can this page be indexed and ranked? Check the robots meta (a `noindex` on a page that should rank is critical), `robots.txt` (fetch `/robots.txt`), and any `X-Robots-Tag`. This is the first thing to rule out.
- **Canonical** — present, self-referencing (or a correct cross-canonical), and pointing at the live URL. Flag missing or wrong canonicals.
- **Status & redirects** — the page returns 200; redirects are single-hop; no loops or soft-404s. Use the link-check results for internal breakage.
- **Broken links** — report the exact internal 4xx/5xx URLs from link-check as fixes.
- **HTTPS & mixed content** — HTTPS with zero insecure sub-resources (fetch-audit counts these).
- **URL & architecture** — readable, stable URLs; check for an XML sitemap (`/sitemap.xml`) that lists the page; for multilingual sites, reciprocal `hreflang`.

**Output:** `{ issue, severity (critical/important/minor), impact, fix }` per finding. Only report broken links and tags that came from the scripts; state anything needing a full crawl as "needs a crawl tool".
