# Agent — On-page & content

Paste as a subagent prompt. Read `references/dimensions.md` (section 2) first.

**Target:** {{url}}   **Goal:** {{goal}}   **Primary keyword:** {{primary_keyword}}
**fetch-audit output:** {{fetch_audit_json}}

Judge what the signals cannot:

- **Title & meta** — beyond the length flags from fetch-audit: does the title match search intent, lead with the keyword naturally, and read like a promise? Does the meta description earn the click? Rewrite weak ones.
- **Heading structure** — one `<h1>` that states the topic, logical H2/H3 nesting (fetch-audit gives the outline), headings that describe their sections.
- **Content quality** — does the page answer the query better than what currently ranks? Judge originality, specifics, evidence, and freshness. Call out thin or padded sections, and say what is missing.
- **Keyword relevance** — the topic and natural variations are present without stuffing. Flag both extremes: exact-match repetition, or the target barely mentioned.
- **Internal linking** — descriptive anchors to and from relevant pages; flag orphaned or dead-end pages.

**Output:** `{ issue, severity, impact, fix }`, with concrete rewrites for the title, meta, and any weak headings, and a short note on the biggest content gap versus the top results.
