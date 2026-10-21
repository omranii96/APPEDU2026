# Agent — Structured data & social

Paste as a subagent prompt. Read `references/dimensions.md` (section 3) first.

**Target:** {{url}}
**fetch-audit output (JSON-LD blocks & types, OG/Twitter):** {{fetch_audit_json}}

Judge correctness, not just presence:

- **Valid & parseable** — the JSON-LD blocks parse. Flag syntax errors.
- **Right type for the page** — Article/BlogPosting on an article, Product + Offer on a product, FAQPage only if the FAQ is genuinely on the page, BreadcrumbList for breadcrumbs, LocalBusiness for a physical location, Organization/WebSite on the home page. Flag the wrong type, and flag marking up content that is not visible on the page (a Google guidelines violation that can cause a manual action).
- **Rich-result eligibility** — required properties are present for the type (Product: name, image, offers/price, availability; Article: headline, image, datePublished/Modified; FAQ: question + answer pairs). List what is missing.
- **Social** — `og:title`, `og:description`, `og:image` (right dimensions), and a Twitter card, so shares and link unfurls render well. fetch-audit flags what is absent.

Where useful, note that the fix should be validated with Google's Rich Results Test / Schema.org validator after implementation.

**Output:** `{ issue, severity, impact, fix }`, giving the concrete JSON-LD change or the missing property for each finding.
