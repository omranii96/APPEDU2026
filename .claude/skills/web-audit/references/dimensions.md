# Audit dimensions

What each dimension checks and the common failures. Items marked *[auto]* come from `scripts/fetch-audit.mjs` or `scripts/link-check.mjs`; the rest need judgement.

## 1. Technical SEO & crawlability

- **Indexability** *[auto: robots meta]* — is the page indexable? Check `<meta robots>` (noindex is a red flag on pages you want ranked), `X-Robots-Tag`, and `robots.txt`. A stray noindex is the single most damaging finding.
- **Canonical** *[auto]* — one self-referencing (or correct cross-) canonical. Failure: missing, or pointing to the wrong URL.
- **Status & redirects** *[auto: link-check]* — 200 for live pages; redirect chains kept to one hop; no soft-404s. Fix redirect chains and loops.
- **HTTPS & mixed content** *[auto: insecure refs]* — served over HTTPS with no http:// sub-resources.
- **Broken links** *[auto: link-check]* — no internal 4xx/5xx. External breakage matters less but still ages a page.
- **URL structure** — readable, lowercase, hyphenated, stable. Avoid deep nesting and parameter soup.
- **Sitemap & hreflang** — an XML sitemap exists and lists this page; multilingual pages have correct reciprocal `hreflang`.

## 2. On-page & content

- **Title** *[auto: length]* — unique, ~15-65 chars, primary keyword near the front, reads like a promise.
- **Meta description** *[auto: length]* — ~70-165 chars, active, gives a reason to click. Not a keyword dump.
- **Heading structure** *[auto: h1 count / outline]* — exactly one `<h1>`, logical H2/H3 nesting, no level jumps. Headings describe content.
- **Content depth & quality** — does the page actually answer the query better than what ranks now? Judgement: originality, specifics, evidence, freshness. Flag thin or padded content.
- **Keyword relevance** — the topic and its natural variations are present without stuffing. Failure: exact-match repetition, or the target term barely appears.
- **Internal linking** — links to and from relevant pages with descriptive anchors; no orphan pages.

## 3. Structured data & social

- **JSON-LD present & valid** *[auto: blocks/types]* — structured data exists and parses.
- **Right type for the page** — Article on an article, Product + Offer on a product, FAQPage only if the FAQ is really on the page, BreadcrumbList for breadcrumbs, LocalBusiness for a location. Failure: wrong type, or marking up content that is not visible (a guidelines violation).
- **Rich-result eligibility** — required properties present (e.g. Product needs name, offers, price; Article needs headline, image, dates).
- **Open Graph & Twitter** *[auto]* — `og:title`, `og:description`, `og:image` (and a Twitter card) so shares render well.

## 4. Performance & UX

- **Images** *[auto: alt, dimensions]* — modern format (WebP/AVIF), explicit width/height (prevents layout shift → CLS), lazy-loaded below the fold, appropriately sized. This is usually the biggest, easiest performance win.
- **Layout shift risk** *[auto: missing dimensions]* — images/embeds without reserved space, late-injected banners.
- **Render-blocking** — heavy synchronous CSS/JS in the head; large third-party scripts. Judgement from the markup.
- **Mobile-friendly** *[auto: viewport]* — a viewport meta, responsive layout, tap targets not cramped.
- **UX friction** — obvious issues: intrusive interstitials, unreadable contrast on key text (hand to accessibility-audit for the real check), unclear primary action.
- **Field metrics** — on-page signals predict but do not measure Core Web Vitals. Recommend a Lighthouse / PageSpeed Insights run for real LCP/INP/CLS numbers.

## Cross-reference

For anything beyond a light accessibility glance (keyboard, screen reader, full WCAG), use the **accessibility-audit** skill. This audit only flags the obvious in passing.
