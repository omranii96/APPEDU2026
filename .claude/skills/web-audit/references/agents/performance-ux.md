# Agent — Performance & UX

Paste as a subagent prompt. Read `references/dimensions.md` (section 4) first.

**Target:** {{url}}
**fetch-audit output (images, viewport, insecure refs):** {{fetch_audit_json}}

Judge the signals that predict real-world performance and note where a lab tool is needed:

- **Images** — usually the biggest win. Check for modern formats (WebP/AVIF), explicit `width`/`height` (fetch-audit counts those missing, they cause layout shift / CLS), `loading="lazy"` below the fold, and sensibly sized files. Give specific fixes.
- **Layout-shift risk** — images, ads, or embeds without reserved space; late-injected content. Map to the missing-dimensions count.
- **Render-blocking** — large synchronous CSS/JS in the head, heavy third-party scripts (analytics, chat, tag managers). Judge from the markup; recommend deferring/async.
- **Mobile-friendly** — a viewport meta (fetch-audit flags its absence), responsive layout, tap targets not cramped.
- **UX friction** — intrusive interstitials, unclear primary action, key text at risk on contrast (hand contrast off to the accessibility-audit skill for the real check).

Always add: on-page signals predict but do not measure Core Web Vitals. Recommend a **Lighthouse** or **PageSpeed Insights** run for real LCP / INP / CLS numbers, and treat those as the source of truth for field performance.

**Output:** `{ issue, severity, impact, fix }` per finding, plus the one-line recommendation to run a lab test for measured metrics.
