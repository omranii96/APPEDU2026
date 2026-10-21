---
name: ui-component-sourcing
description: "Use when building UI: pick free copy-paste components."
version: 1.0.0
author: unfoldingdimensions (unfoldingdimensions), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [UI, Components, Licensing, Copy-Paste, Tailwind, React, Animations]
    category: creative
    related_skills: [popular-web-designs, software-product-research, claude-design, shadcn-app-frontend]
---

# UI Component & Animation Sourcing

When building an app/website UI and you need ready-made components, animations, landing blocks, or icons: which source to pull from, whether it is legally free for commercial use, and how to consume it (copy-paste vs CLI vs npm). Verified audit data lives in `references/free-ui-libraries-audit.md` (audited 2026-08). Also encodes the full design-angle build workflow (layout, type, color, motion, icons, states) and a measured QA loop — `references/components.md`, `references/motion.md`, `references/design-qa.md`, `references/icons.md`.

## When to Use

- Building UI for an app/website and need components, animated effects, sections, or icon sets without writing them from scratch.
- User names a UI source (aceternity, reactbits, motion-primitives, watermelon, etc.) and asks "is it free?" / "can we use it commercially?"
- Deciding whether to copy a component from a demo site or reimplement it in the project's own style.

## The short version (audit date 2026-08 — re-verify prices/free tiers, they move)

- **Safely copy-paste (MIT):** Watermelon UI, Fancy Components, Number Flow (npm package), Motion Primitives core (CLI), Shadcn Studio open-source repo.
- **Free tier, custom site terms:** Aceternity UI — free tier usable in unlimited personal/commercial projects; only restriction is reselling/redistributing the components as a competing product. Not OSI-licensed; terms live in the site FAQ.
- **Restricted but usable:** React Bits — MIT + Commons Clause: fine inside your app/product, but you may NOT sell/redistribute the components themselves and must keep the copyright notice.
- **Freemium — paid tiers optional:** Aceternity All-Access, Motion Primitives Pro ($149 lifetime), Shadcn Studio ($149–899 one-time), UI Layouts Pro ($169–549 one-time). The free tiers are genuinely usable without paying.
- **Reference-only (no code to copy):** component.gallery (design-system component taxonomy), happyhues.co (color palettes shown in context), checklist.design (110 UX/UI checklists + Figma plugin), noahelhadedy/free-icon-resources (157 icon-source links, list is CC0).
- **Round-2 (2026-08-09):** Uiverse (MIT, 500k+ CSS/Tailwind elements) joins the copy-safe tier; Great UI (MIT claimed, LICENSE file missing — verify before heavy use); Beautiful UI (free copy-paste AI-native components, no formal license — reimplement patterns); 60fps.design + Refero Styles (reference galleries — motion + DESIGN.md token files); Appllama (paid iOS research, $144/yr — paywall/onboarding benchmarks); Paper MCP (agent access to Paper design files); ui.sh (invite-gated workflow inspiration → `references/workflows.md`).
- **Round-3 (2026-08, free Motion code):** Magic UI (⭐ MIT, 22k★, the flagship animated-component source), Cult UI + SmoothUI + Origin UI (all MIT, all shadcn-compatible) join the copy-safe tier; Animate UI (MIT + Commons Clause AND ~8 months dormant — reimplement patterns); HeroUI (Apache-2.0 npm library — permissive but a runtime dependency, not owned files); 21st.dev (per-item-license marketplace + Magic MCP for agents); ⚠️ originui.com now serves coss ui which is **AGPL-3.0 — never paste into closed-source apps**.

## Consumption patterns

- **Copy-paste registry sites** (Aceternity, Watermelon, Fancy, React Bits): component code is shown on the site — paste into the project and adapt (typical deps: Tailwind, motion/framer-motion, clsx/tailwind-merge).
- **CLI registries:** `npx motion-primitives@latest add <component>`; shadcn-style `npx shadcn@latest add ...`.
- **npm packages:** `number-flow` / `@number-flow/react` (MIT, dependency-free, accessible — animated numbers for React/Vue/Svelte/TS).
- **Reference galleries:** use for decisions — component taxonomy, palette choices, checklist QA, icon selection — never as copy source.

## Building with these sources (design angles)

When constructing a page/section with components from the tiers above, work through every design angle in order — a complete UI needs all of them, not just the components:

1. **Inventory.** List pages/sections and every component each needs; cross-check `references/components.md` so nothing is forgotten (tables, empty states, forms, nav, feedback). For agent products, also check the **AI-native / agent-interface category** there.
2. **Base layer = shadcn/ui** (`npx shadcn@latest add ...`). Never reimplement base components from a copy-paste library — that adds churn, not value.
3. **Flair from the tiers.** Tier A: copy/adapt freely, keep copyright notices. Tier B: reimplement the *pattern* in the project's own style (don't paste wholesale). Never copy Tier C. For transform/refactor/adapt tasks (screenshot→markup, Tailwind cleanup, dark-mode images, responsive pass, design directions, component refactor), follow the procedures in `references/workflows.md`.
4. **Layout & grid.** 4px/8px spacing scale, 12-col grid, `max-w-6xl/7xl` containers, section padding `py-16/24`, card grids equal-height per row with no dead space (measured, not eyeballed).
5. **Typography.** 1.2–1.25 modular scale; display/heading/body/caption hierarchy; 40–60ch measure for prose; `clamp()` for display sizes. Default: clean warm-minimal aesthetic (Notion-like); serif display acceptable on landing pages. Match the product's existing design language when one exists.
6. **Color as variables, never raw hex in components.** Define roles (`bg, surface, border, text, text-muted, accent, danger, success`) per theme; theming = variable swap. Check WCAG contrast: 4.5:1 body, 3:1 large/UI.
7. **Motion** per `references/motion.md` (timings, easing, reduced-motion) — purposeful, not decorative.
8. **Icons** per `references/icons.md` — MIT sets first (Lucide/Heroicons/Phosphor/Tabler), bundle SVGs, never hotlink, never unattributed Flaticon/Freepik/Vecteezy.
9. **States on every interactive component**: default, hover, active, focus-visible, disabled, loading, empty, error. Happy-path-only is incomplete.
10. **QA gates** (each is a gate, not a suggestion): measured geometry via `browser_console` `getBoundingClientRect` (equal card heights, grid alignment, no dead space) → theme flip (computed styles of toggles/pills/inputs in BOTH themes) → `references/design-qa.md` checklists → `browser_vision` slop check → keyboard/a11y spot check (focus-visible rings, tab order).

## Auditing a new UI source ("is it really free?")

1. GitHub API discovery + metadata (`api.github.com/search/repositories?q=<name>` unauthenticated; search engines get CAPTCHA'd). Note `license`, `stargazers_count`, `created_at`, `pushed_at`. Hype signal: huge stars + brand-new repo → verify marketing claims.
2. **License gotcha:** API `license: NOASSERTION` (or null) → fetch `LICENSE`, `LICENSE.md`, `LICENCE` from the resolved default branch before concluding unlicensed. GitHub only auto-detects the exact filename `LICENSE`.
3. Mine the site FAQ: most Next.js sites embed schema.org FAQ JSON-LD in the static HTML — `grep -oP '"text":"[^"]{0,300}"' page.html` surfaces free/commercial/resell language without clicking through.
4. Freemium check: grep the page for `"price"`, `discount_price`, plan names; read what the free tier actually includes (e.g. "57 blocks, theme generator, no credit card, no time limit").
5. Verdict format: separate "free software" from "conditionally free (tier)" from "reference-only"; date the numbers.

## Pitfalls

- **"Free" ≠ OSI open-source.** React Bits is MIT+Commons Clause; Aceternity is custom site terms. Both are fine for building your apps, but the components cannot be shipped/sold as a product themselves.
- **Attribution requirements hide in icon/asset sources**, not component libraries — Flaticon, Freepik, Vecteezy need attribution; Reshot, Iconduck, Lucide, Tabler don't.
- **Marketing counts are unverified for brand-new projects** (Watermelon UI claims 600+ components but its repo is months old with ~180 stars). MIT makes it safe regardless; just don't trust the headline numbers.
- **The common permissive line** across Aceternity / Shadcn Studio / UI Layouts is: "unlimited projects, client work OK, no reselling as competing product" — quote that wording when reporting commercial use.
- **Reference galleries often carry no license on their repos** (component.gallery) — treat strictly as inspiration.
- **Bot-protected sites** (motion-primitives.com returns 429 to curl): use the browser, not curl.
- **framer-motion → motion.** The library was renamed; current imports are `motion/react`. Old samples (most React Bits / Aceternity code) import `framer-motion` — adapt.
- **SSR hydration.** Animation libs + Next.js SSR can mismatch on first paint; gate client-only animations behind a mounted flag.
- **Never paste Tier C.** A component behind a paywall → rebuild the interaction from the demo; the *pattern* isn't copyrightable, the code is.

## References

- `references/free-ui-libraries-audit.md` — full 12-source audit (2026-08): per-site license, pricing, stars, commercial verdicts, consumption method, plus the audit recipes that worked. Round-2 additions (2026-08-09): Uiverse, Great UI, Beautiful UI, 60fps, Refero Styles, Appllama, Paper MCP, ui.sh.
- `references/components.md` — canonical component taxonomy (what a complete UI contains) + required state sets per component, incl. the AI-native / agent-interface category.
- `references/motion.md` — motion spec: durations, easing curves, stagger, reduced-motion rules (+ 60fps.design as the reference gallery).
- `references/design-qa.md` — QA checklists distilled from checklist.design: website, web app, mobile, design system, flows.
- `references/icons.md` — icon strategy: MIT sets vs attribution-required sets, from the free-icon-resources audit.
- `references/workflows.md` — transformation workflows (ui.sh-inspired): markup-from-image, canonicalize Tailwind, dark-mode image, make-responsive, design directions, brand direction, refactor-to-components, senior-designer build posture.
- `references/playbook.md` — production build playbook: which design skill to load per phase (taste → craft → verify) + how to obtain the skills (bundled, hub, manual install).
