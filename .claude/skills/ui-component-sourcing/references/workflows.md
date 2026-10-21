# UI Transformation Workflows

Task-oriented procedures for the recurring UI jobs an agent is asked to do. Concepts inspired by
ui.sh ("Agent skills for interface builders" — Adam Wathan & Steve Schoger, invite-gated); these
are our own implementations, not their skill text. Each workflow ends with a checkable
completion criterion. Run the QA gates from SKILL.md after any workflow that produces UI.

## 1. Markup From Image

Turn a screenshot, mockup, or wireframe into semantic markup.

1. Load the image (`vision_analyze`); describe layout: sections, order, alignment, spacing rhythm, typography roles, colors.
2. Draft the semantic skeleton first: landmarks (`header/main/section/footer`), one `h1`, sequential headings, lists for repeated items — no styling yet.
3. Fill content from the image; use real copy where visible, sensible placeholder otherwise (never lorem).
4. Apply the project's design language (see `popular-web-designs` / Refero Styles if matching a brand) — Tailwind classes, tokens.
5. Verify: re-render and compare `getBoundingClientRect` geometry against the source image (section order, approximate ratios); `browser_vision` diff.

## 2. Canonicalize Tailwind

Sort, normalize, dedupe, and resolve conflicting Tailwind classes in existing markup.

1. `search_files` the target file; list every element with 4+ utility classes.
2. Reorder per Tailwind convention: layout (display/position/flex/grid) → spacing (margin/padding) → size → typography → background/border → effects → transitions/interactivity; group variants consistently (`hover:`/`dark:` last).
3. Remove duplicates and contradictory pairs (`p-4` + `p-8` — keep the last / the intended one); move repeated clusters to a shared class, `@apply` component, or a local `cn()` helper.
4. Verify: `grep` the diff — no class appears twice in one element, no contradictory spacing/size pairs remain, and the rendered page is visually unchanged (`browser_vision` before/after).

## 3. Dark Mode Image

Adapt light-mode raster images so they sit well in dark themes.

1. Identify images that look wrong in dark mode (bright white backgrounds, harsh contrast).
2. Non-destructive first: CSS filters (`invert` + `hue-rotate(180deg)` works for simple icons/diagrams; wrap in a `.dark img.invertible` rule) — keep the original asset untouched.
3. For photos: blend with `mix-blend-mode` / opacity; for product screenshots: keep them in a light card so the dark page doesn't fight them.
4. SVG/diagrams: restyle fills/strokes via CSS variables (`currentColor`, theme tokens) instead of filters.
5. Verify: flip theme, `browser_console` computed styles — no element below contrast, no blinding-white blocks.

## 4. Make Responsive

Adapt an existing design across mobile, tablet, and desktop breakpoints.

1. Establish the current state: load at 375px, 768px, 1280px; note overflow, squished grids, broken nav.
2. Mobile-first pass: single-column stack, hamburger nav (aria-expanded), touch targets ≥44px, no horizontal scroll.
3. Tablet: 2-col grids, constrained max-width, keep sidebars optional.
4. Desktop: 12-col grid, `max-w-6xl/7xl`, card grids equal-height per row.
5. Verify: `browser_console` at all three widths — `document.documentElement.scrollWidth <= clientWidth`, no dead space in grids, nav usable.

## 5. Design Directions

Generate and compare multiple design directions before committing.

1. Produce **2–3 distinct directions** (not variations): e.g. (a) editorial/typographic, (b) playful/colorful, (c) minimal/technical — each as a small HTML sketch with its own palette, type pairing, and layout.
2. Present them side by side with the reasoning (who each serves, what it signals); ask the user to pick or mix.
3. On pick, carry the chosen direction's tokens forward — never blend directions mid-build.

## 6. Brand Direction

Generate a visual brand direction for a new product idea.

1. Extract the product's essence: audience, tone, one-line promise (from the user or the brief).
2. Produce a mini brand kit: 2–3 words of design character, 5-role color palette (with contrast-checked pairings), type pairing (display + body), spacing/radius tokens, one signature visual motif.
3. Show it applied to a hero section mock; iterate on feedback; lock tokens into CSS variables.

## 7. Refactor To Components

Turn large chunks of UI code into organized, reusable components.

1. `search_files` for repetition: identical JSX blocks, copy-pasted class strings, inline data.
2. Extract by pattern: repeated markup → component with props; repeated logic → hook; repeated data shapes → types; repeated class clusters → `cn()` constants or shadcn-style variants.
3. Keep the default behavior identical — refactor is not redesign: no visual changes, no prop API churn beyond what the extraction needs.
4. Verify: page renders byte-identical to before (`browser_vision` diff), build/lint passes, and the repeated-block count in the source drops (grep counts before/after).

## 8. Build New UI (senior-designer standard)

The default posture for any new interface build — the framing that the other workflows assume.

1. Think like a senior designer before writing code: name the job of the page, the user's next action, and the hierarchy of information.
2. Use the design-angle order from SKILL.md (inventory → base layer → flair → layout → type → color → motion → icons → states → QA gates).
3. Never ship happy-path-only; never ship a layout that only looks right in one theme or one width.
