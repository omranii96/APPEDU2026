# Free UI Component / Animation Source Audit (2026-08-09)

Research question: "which copy-paste UI libraries/components are truly free to use in commercial apps?" All facts verified from the GitHub API and site pages on the audit date. Prices and free tiers move — re-verify before acting. Raw page captures from the audit session live in the project's `research_tmp/` (not part of the skill).

## Copy-paste component libraries

### Aceternity UI — ui.aceternity.com
- 200+ React/Tailwind/Motion copy-paste components; free tier ~100+; paid "All-Access Pass" adds premium blocks + full-page templates.
- License: **custom site terms** (FAQ-embedded; no OSI license). FAQ wording: free tier for "personal and commercial projects"; "only restriction: you cannot resell or redistribute the components themselves as a competing product." No attribution requirement mentioned.
- No public repo for the components (the `aceternity` GitHub org only hosts boilerplates).

### Watermelon UI — ui.watermelon.sh
- "600+ free, open-source UI components", 100+ animations, templates; CSS-variable theming. "OPEN SOURCE — FREE FOREVER... free for commercial and personal use. No strings attached."
- Repo: `WatermelonCorp/watermelon-platform` — **MIT**, created 2026-02, ~180★ (brand-new; "600+" count is marketing, unverified).
- Consumption: copy-paste. Site is JS-rendered (4KB curl shell) — use the browser.

### Shadcn Studio — shadcnstudio.com
- 1000+ shadcn/ui components, 800+ blocks/templates, live theme generator, AI tools.
- Repo `shadcnstudio/shadcn-studio`: **MIT** — but the file is `LICENSE.md`, so the GitHub API reports NOASSERTION (see software-product-research pitfall).
- Site freemium: free forever plan = 57 blocks + theme generator + free components, "no credit card, no time limit". Paid one-time: Basic $149, Pro $249, Team $499, Enterprise $899 — lifetime updates.
- Commercial: yes, unlimited projects (client work, SaaS, internal); reselling source files as a competing product not permitted.

### React Bits — reactbits.dev
- 45k★ animated/interactive React components, `DavidHDev/react-bits`, actively maintained (pushed 2026-08).
- License: **MIT + Commons Clause v1.0** (`LICENSE.md`, so API shows NOASSERTION). Free to use in an app/website/product, including commercial; MAY NOT sell/sublicense/redistribute the components themselves (alone, bundled, or ported); the copyright notice must be included in copies. Not OSI-approved.
- Consumption: copy-paste. Site is JS-rendered — use the browser.

### Motion Primitives — motion-primitives.com
- Core components: **MIT** repo (`ibelick/motion-primitives`, ~5.9k★) + CLI `npx motion-primitives@latest add <component>` (also shadcn-compatible). Free.
- Pro (pro.motion-primitives.com): one-time **$149** (list $299; code `MP10` = 10% off), perpetual, commercial use, lifetime updates; 50+ handcrafted motion sections/components + landing template; Stripe checkout (`buy.stripe.com/...`).
- Site is Vercel-bot-protected (curl → 429 Security Checkpoint) — use the browser.

### Fancy Components — fancycomponents.dev
- "Free & Open Source" — repo `danielpetho/fancy`, **MIT**, ~3k★, actively maintained. Copy-paste fancy React components (site author: Daniel Petho).

### UI Layouts Pro — pro.ui-layouts.com
- Premium React/Tailwind blocks + templates + drag-drop Template Studio builder.
- Freemium: limited free access to 150+ premium blocks. Paid one-time: Pro Creator $169, Forever Builder $198 (list $249; unlimited 150+ blocks, builder, commercial license unlimited projects, lifetime updates), Team Forge $449 (list $549; 15 seats, shared workspace, dedicated support).

## npm / focused libraries

- **Number Flow** — number-flow.barvian.me → `barvian/number-flow`, **MIT**, ~7.6k★, pushed 2026-07. Animated number component for React/Vue/Svelte/TS; dependency-free, accessible, customizable. npm: `number-flow` / `@number-flow/react`.

## Reference-only (no code to copy)

- **component.gallery** — curated index of components from real design systems (Astro + Airtable; repo `inbn/component-gallery`, **no license** — treat as inspiration only). Entries tagged e.g. "Open source", "Accessibility", "Code examples". Use for component taxonomy; each referenced design system has its own license.
- **happyhues.co** — Mackenzie Child; color palette inspiration shown live in context on an example site (click palettes → whole site recolors). Free.
- **checklist.design** — George Hatzis, sponsored by Mobbin; 110 free UX/UI checklists across Website / Web App / Mobile / Design System / Flows + a Figma plugin with AI-powered design review. Free, no login.
- **noahelhadedy/free-icon-resources** (GitHub) — curated list of 157 free icon resources, 14 categories: open-source icon sets, brand/logos, animated icons, 3D icons, emoji, flags, search engines, SVG/favicon/AI generators, Figma plugins, inspiration. The list itself is **CC0**. Highlights: MIT sets Lucide/Heroicons/Tabler/Phosphor; attribution needed on Flaticon/Freepik/Vecteezy; no attribution on Reshot/Iconduck.

## Round-2 sources (audited 2026-08-09)

### Uiverse — uiverse.io — Tier A (MIT)
- Largest community library of open-source UI elements (500k+ buttons, loaders, cards, inputs) in pure CSS or Tailwind. "Free to copy and use", commercial OK, **MIT per element**.
- Consumption: copy-paste (HTML/CSS or Tailwind) — great for CSS-only flourishes that don't need React; adapt into JSX + Tailwind classes for app use.

### Great UI — great-ui.com — Tier A-pending (claims MIT, verify)
- Copy-paste animated React components (TypeScript, Tailwind, Motion). Repo `Saurabh-2607/GreatUI` — README badge claims **MIT** but the **LICENSE file is missing**; repo brand-new (2026-07, ~56★). Verify the license appears before heavy use; small catalog.

### Beautiful UI — beautiful-ui-five.vercel.app — Tier B (free copy-paste, no formal license)
- "Crafted primitives for AI-native interfaces" — copy-paste components for chat agents, thinking states, human-in-the-loop approvals. Author: **Shane Levine** (Cal.com byline). No repo, no LICENSE file → use in apps, reimplement patterns, credit the author, don't redistribute.
- Catalog (the AI-native reference): streaming text, thinking states (pixel-grid loader + elapsed timer, reduced-motion aware), tool-call chips, approval cards, agent task rows (running/failed/completed), confidence-meter suggestions, HITL questions, tabbed chat panel, paged insights, live status chips.

### 60fps.design — Tier D (freemium reference)
- Curated UI/UX animation & interaction inspiration from top iOS/web apps (video clips). Framer site; free browsing, pro unlocks more. **No code** — the "what good looks like" gallery for motion work; pairs with `references/motion.md`.

### Refero Styles — styles.refero.design — Tier D (free)
- Curated **DESIGN.md library for AI agents**: colors, typography, spacing, components, design rules from leading product websites; formatted for Cursor, Claude Code, Codex, v0, Lovable. Content is embedded in the page (free to view/copy). Pairs with the `design-md` skill (authoring format) and `popular-web-designs` (visual languages) — pull a product's DESIGN.md when the user says "make it look like X".

### Appllama — appllama.io — Tier C (paid reference)
- iOS design research: 29,400+ screens + live videos from 720+ **top-earning iOS apps**; onboarding / paywall / flow focus; filter by revenue, downloads, recency. Free tier sliver; **Pro $144/yr** (save $48), Team $192/seat/yr, Studio Pro 4K watermark-free exports. No code — use when designing paid mobile apps (paywall/onboarding benchmarks).

### Paper MCP — paper.design/docs/mcp — integration (freemium tool)
- MCP server for **Paper**, a DOM-based design tool ("design, share, ship"): agents read/write design files from Cursor (`/add-plugin paper-desktop`), Claude Code (`claude mcp add paper --transport http http://127.0.0.1:29979/mcp --scope user`), Claude Desktop. Paper is freemium — free collaboration + free viewer seats, paid editor seats on Pro.
- Use when a workflow involves Paper design files: wire the MCP so the agent can read the file as context instead of guessing from screenshots.

### ui.sh — "Agent skills for interface builders" — Tier D (invite-gated inspiration)
- By **Adam Wathan & Steve Schoger** (Tailwind CSS + Refactoring UI). Task-oriented prompts/workflows for building UIs: build-new-UI (senior-designer expertise), design-directions (generate + compare multiple), brand-direction, refactor-components, canonicalize-tailwind, dark-mode, dark-mode-image, make-responsive, markup-from-image. **Invite-gated** ("Request an invite").
- Use the *concepts* — encoded as procedures in `references/workflows.md`. Don't copy their skill text; implement the workflows ourselves.

## Round-3 sources — free Motion/framer-motion code (audited 2026-08)

### Magic UI — magicui.design — Tier A (MIT) ⭐ flagship animation source
- THE free animated-component library: 50+ animated components & effects (backgrounds, text animations, marquees, dot patterns) built with Tailwind CSS + Motion; copy-paste; shadcn-compatible.
- Repo `magicuidesign/magicui`: **MIT**, ~22k★, actively maintained (pushed 2026-08). The biggest omission from rounds 1–2, now corrected.

### Cult UI — cult-ui.com — Tier A (MIT)
- Components crafted for design engineers; Tailwind-styled, shadcn-compatible, copy-paste.
- Repo `nolly-studio/cult-ui`: **MIT**, ~6k★, active (pushed 2026-07).

### SmoothUI — smoothui.io — Tier A (MIT)
- Beautifully designed components with smooth animations (React, Tailwind, shadcn/ui, Motion).
- Repo `educlopez/smoothui`: **MIT**, active.

### Origin UI — origin-space — Tier A (MIT)
- Large copy-paste component collection + layouts/experiments built with shadcn/ui (many with subtle motion).
- Repos under `origin-space` org (`origin-space/origin-ui` etc.): **MIT**, active.

### Animate UI — animate-ui.com — Tier B (MIT + Commons Clause) ⚠️ dormant
- Fully-animated shadcn-style distribution, `npx`-installable components.
- Repo `imskyleen/animate-ui`: LICENSE.md is **MIT + Commons Clause v1.0** (same restriction family as React Bits — usable in apps, may not sell/redistribute the components themselves); ~4.2k★ but **no push since Dec 2025 (~8 months dormant)**. Reimplement patterns; don't build on it as infrastructure.

### HeroUI (ex-NextUI) — heroui.com — different model (npm dependency)
- Modern animated React **library** consumed via npm — you don't own the files (unlike every Tier A source above).
- Repo `heroui-inc/heroui`: **Apache-2.0**, ~30k★, very active. Fine to use (Apache is permissive), but it's a runtime dependency, not copy-paste ownership — fits projects that accept a component-library dependency.

### 21st.dev — hybrid marketplace (+ agent MCP)
- Community catalog of UI by design engineers: React/Tailwind components and full templates. Free community catalog; premium/paid items exist — **license is per-item**, each listing states its terms before purchase.
- **Magic MCP** (`21st-dev/magic-mcp`, Apache-2.0): lets coding agents search 10k+ components and pull them into the editor. Agent-native sourcing pairs with the Paper MCP note above.

### ⚠️ coss ui — AGPL warning
- `originui.com` now fronts **coss ui** — "the official design system of Cal.com" (`cosscom/coss`, ~10k★, **AGPL-3.0**). AGPL is viral copyleft: do NOT paste those components into closed-source/commercial apps. Origin UI's own MIT repos under `origin-space` remain the safe route. Lesson repeated: check the license of what a domain currently serves, not what it served last year.

## Audit recipes that worked this session

- GitHub API search (`api.github.com/search/repositories?q=<name>`) works unauthenticated; web search engines get CAPTCHA'd.
- Resolve `default_branch` first, then fetch LICENSE → LICENSE.md → LICENCE from `raw.githubusercontent.com` (API auto-detects only the exact filename `LICENSE`).
- Next.js sites embed FAQ + pricing as schema.org JSON-LD in static HTML: `grep -oP '"name":"[^"]{0,80}"|"text":"[^"]{0,300}"|"price":"[^"]*"' page.html` recovers free/commercial/resell terms and plan prices without clicking.
- RSC payloads (pro.ui-layouts.com) bury pricing in escaped JSON — grep for `variantId|discount_price|\\$[0-9]+` with 100-char context.
- Windows git-bash: `curl -o /tmp/...` silently writes nothing (HTTP 200, 0 bytes) — use cwd-relative paths. Session `cd` persists across terminal calls — check the `cwd` field of prior results before using relative paths.
- JS-rendered sites (Watermelon, React Bits, Motion Primitives): curl returns a 2-5KB shell — use the browser.
