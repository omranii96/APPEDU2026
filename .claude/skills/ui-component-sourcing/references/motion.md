# Motion Spec

Concrete numbers for the animation patterns seen across Motion Primitives, React Bits, Watermelon
UI, and Aceternity — encoded so builds are consistent instead of improvised. Use `motion/react`
(renamed from framer-motion; old samples import `framer-motion` — adapt).

Reference gallery for "what good motion looks like": **60fps.design** (curated UI/UX animation
clips from top iOS/web apps) — watch relevant clips before building an animated section, then
encode the feel with the numbers below.

Copy-paste code sources for the patterns themselves (all MIT, shadcn-compatible): **Magic UI**
(the flagship animated-component library — backgrounds, text animations, marquees),
**Cult UI**, **SmoothUI**, **Origin UI**. See `free-ui-libraries-audit.md` round 3 for licenses
and caveats (Animate UI is Commons Clause + dormant; coss ui is AGPL — avoid in closed source).

## Durations

| Use | Duration |
|---|---|
| Micro-interaction (hover, press, focus, toggle) | 100–200ms |
| Component transition (modal, drawer, accordion) | 200–400ms |
| Element reveal on scroll / page enter | 400–700ms (staggered) |
| Hero / headline entrance | 600–900ms with overshoot ease |

## Easing

- Standard UI: `cubic-bezier(0.4, 0, 0.2, 1)` (or `easeOutCubic` in motion).
- Entrances: ease-out / decelerate (`[0.22, 1, 0.36, 1]` — the "easeOutExpo-ish" everyone uses).
- Exits: ease-in / accelerate (`[0.4, 0, 1, 1]`).
- Spring only for playful/physical elements (cards, buttons); `stiffness ≈ 260, damping ≈ 20–25`.

## Stagger & orchestration

- Enter animations: 40–80ms between items, max ~6 staggered items — beyond that, group.
- Reveal on scroll: `whileInView` with `viewport={{ once: true, margin: "-80px" }}` (don't re-trigger).
- Respect existing page rhythm: hero → section headers → cards; don't animate everything at once.

## Rules

- **Purpose rule:** animate to direct attention (reveal, focus, state change) or give feedback
  (hover, press, toast). Never decorative looping; never animate loading screens beyond a skeleton.
- **prefers-reduced-motion:** disable transform/translate animations, keep opacity fades and
  smooth scrolling; check with `matchMedia('(prefers-reduced-motion: reduce)')` or Tailwind
  `motion-reduce:` variants.
- **No element animates longer than 3s** without a stop control (WCAG 2.2.2).
- **Layout stability:** animate `transform`/`opacity` only — never `top/left/width/height/margin`
  (causes reflow). Reserve space or use skeletons so reveals don't shift layout.
- **Entrance animations must not hide content:** if JS/motion fails to load, content must still
  be visible (start visible, animate from hidden only when the lib is ready; gate behind a
  mounted flag on SSR).
- No parallax on body text; no infinite marquee for primary content; text reveals per
  word/char are for hero/headline only.

## Verification

- `prefers-reduced-motion: reduce` emulation in devtools shows content without transforms.
- No layout shift when animations trigger (before/after `getBoundingClientRect` on the section).
- With JS disabled, all content is visible and readable.
