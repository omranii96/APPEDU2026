---
name: alive-web
description: Use when building cinematic, immersive, award-worthy web experiences in the style of Lusion studio (lusion.co) or their product-story sites (oryzo.ai) — physics-driven hero objects that react to the cursor, scroll-driven WebGL storytelling that flows seamlessly between 3D and 2D chapters, interactive product showcases, premium studio portfolios, GPU particles, magnetic cursors. Use whenever the user says "like Lusion", "like Oryzo", "Awwwards", "award-winning", "immersive", "cinematic scroll", "interactive 3D", or wants a site that feels alive instead of static.
---

# Alive Web: award-grade immersive sites

## Read this first — why attempts at this style usually fail

Lusion is a **design studio** that happens to use WebGL, not a WebGL demo shop. On every site they ship, graphic design carries 70% of the impression: the paper color, the type, the spacing, the tiny utility labels. The 3D scene is a precious object *framed* by that design. Attempts fail when they invert this — leading with effects (particles, bloom, glow) on a generic dark layout.

The single most common failure: **defaulting to a dark navy page with neon/cyan accents, a starfield, and bloom.** Nothing Lusion ships looks like that. lusion.co is a *light* site. oryzo.ai is warm black + cream, not cool black + neon. If you build the shell right, even a plain spinning cube will read as premium; if you build the shell wrong, no shader can save it.

So the order of work is fixed: **art direction → HTML/CSS shell → 3D scene → scroll choreography → micro-interactions → polish.** Do not open Three.js until the shell alone looks like a studio site.

## What actually wins the award — two behaviors, not a look

The shell gets you to "credible". Two behaviors get you to "site of the day", and both are mandatory, not garnish:

1. **Everything is alive.** lusion.co's hero objects aren't animated — they're *simulated*: real gravity, real collisions, and your cursor is a physical object that shoves them. The user plays with the site within the first second, before reading a word. Every chapter of the page, 3D or 2D, must respond to input (the "never inert" rule — `references/interaction-recipes.md`).
2. **Everything flows.** oryzo.ai moves from a 3D camera orbit, to giant 2D text sliding behind the pinned object, to the object dissolving into its dashed blueprint, to a 2D horizontal carousel, and back into 3D — and you cannot point at a seam. Every chapter boundary is a *match cut*: a named shared anchor (shape at the same screen position), a bridged background, carried momentum (`references/flow-choreography.md`).

If the build has a beautiful shell but a static hero and hard section breaks, it is not done.

### The instrument structure — when the brief wants agency instead of a narrative

Both mandatory behaviors are about *aliveness and continuity*, not about scrolling. A scroll story is the default way to deliver them, not the only way, and there is a second structure worth reaching for deliberately:

**Make the page an instrument the visitor operates.** The camera never moves; they turn the *object* and move the *light*. There are no chapters, so there are no boundaries to match-cut — the flow requirement is satisfied trivially because nothing ever cuts. In place of chapters, the content is a set of **findings the visitor discovers by examining**, revealed as they put the instrument in the right state.

Reach for it when the brief is about a single object whose *properties* are the story (a gem, an instrument, a material sample, a mechanism), when the copy voice is technical and disclosure-driven, or when the brand's claim is something the visitor should be able to *check* rather than be told. It is also the answer when a scroll build would read as a sibling of the last three scroll builds: the 2026 award field is saturated with WebGL-first scroll sites, so scrolling harder is not differentiation, and real agency over a real object is the uncopied lane.

What it still owes you, and these are not optional:

- **Routing by what is under the cursor**, not a mode switch or a control panel: drag the object to turn it, drag the field to move the light. Both discoverable, no UI.
- **Direct 1:1 tracking, with inertia recorded separately.** Apply rotation on each pointer move and keep the velocity for the glide afterwards. Integrating velocity only in the frame loop makes 300 px of drag turn the object 7 degrees, which feels broken. Quaternions, never Euler angles — the object gimbal locks the instant it passes vertical, and an instrument is meant to be handled freely.
- **Every readout computed from live state.** Read the tilt back out of the object's quaternion each frame rather than tracking a parallel number, and the numbers can never disagree with the image.
- **The wiggle test still applies**, and a drag-only build fails it: hovering without pressing must move something. A lerped light sweep driven by pointer position is enough.
- **Gate the findings on engagement**, or the resting pose awards one on page load and cheapens the whole mechanic.
- **Derive the framing**, do not eyeball it: visible height is `2*d*tan(fov/2)`, so solve for the object occupying ~55-60% of the frame. Filling 89% of it reads as cropped and airless.

Verification is *easier* than for a scroll build, not harder: expose a debug handle that can pose the object and read the state back, then assert that every finding is actually reachable. A finding that can never fire is a dead feature, and only a numeric probe will tell you.

## Execution contract

Follow this linear path. Each gate is pass/fail — do not proceed past a failing gate. When the brief leaves a choice open, take the stated default instead of inventing.

1. **Pick art direction** (Step 0). *Default: Preset A for a studio/portfolio brief, Preset B for a single-product brief. Never invent a dark-neon third option.*
2. **Start from the scaffold** — copy `references/starter-scaffold.md`'s three files verbatim and run its 5-point acceptance test. *Gate: all 5 pass (physics jacks fall in, cursor shoves them, scroll stirs, headlines mask-reveal, buttons magnetize).* Starting from a blank file instead of the scaffold is only justified when the brief demands a fundamentally different structure.
3. **Build the full shell** (Step 1). *Gate: a screenshot of the shell alone, canvas hidden, reads as a premium studio site.*
4. **Build the scene and chapters** (Steps 2–3), reading the reference files as directed. *Gate: scrub every chapter boundary — no visible seam without a named match-cut anchor.*
5. **Interactivity pass** (Step 4). *Gate: the wiggle test passes at every scroll position.*
6. **Polish and verify** (Step 5): screenshots at 4–6 scroll positions AND the interaction checks, against the Hard bans list.

Budget honestly: steps 3–4 are ~70% of the work. If time is short, cut chapter count, never the physics hero or the match cuts.

---

## Step 0 — Commit to an art direction

Pick ONE of the two verified directions below (or derive your own under the same constraints). Never blend them, and never fall back to "dark + neon".

**Scope note — presets vs. real brands.** The presets below are faithful studies of the reference sites, furniture and all. Using them *verbatim* (their fonts-as-standins, their scroll pill, their edge tab) is right only when the user explicitly asks for "like lusion.co / like oryzo.ai" or for a quick exploration. For a real named brand, the presets supply the *structure and mechanics*, but the surface identity must go through "Deriving your own direction" below — especially step 9 (borrow mechanics, never costumes).

| | **A. STUDIO** (lusion.co) | **B. PRODUCT STORY** (oryzo.ai) |
|---|---|---|
| Use for | Studio/agency portfolios, creative landing pages, "we make things" sites | Single product launches, pinned-object storytelling, spec-sheet narratives |
| Canvas | Light. 3D lives inside dark rounded panels | Dark warm. 3D IS the page, full-bleed, object pinned center |
| Mood | Playful, glossy, toy-like physics | Deadpan, technical, obsessive product worship |

### Preset A — STUDIO (verified against lusion.co)

```css
:root {
  --paper:  oklch(95% 0.01 285);   /* #EEEFF6 pale lavender-white page */
  --ink:    oklch(18% 0.012 280);  /* #16171D near-black text */
  --panel:  oklch(14% 0.012 265);  /* #0E0F15 dark panel the WebGL sits in */
  --accent: oklch(50% 0.28 265);   /* #2430E8 cobalt blue — the ONLY color */
  --radius-panel: 24px;
  --radius-pill: 999px;
}
```

- **Type**: ONE grotesque family, weights 400 + 500 only. Aeonik is the real face; use `Inter` (tight tracking, `font-feature-settings: "ss01"`) or `Neue Montreal`/`Archivo` as stand-ins. Headlines are **sentence case**, large and calm: hero statement ~26–38px, section titles enormous (~9vw, e.g. "Featured Work"). Never uppercase headlines, never bold-900, never letterspaced headlines.
- **Utility layer**: tiny 10–12px UPPERCASE labels with `letter-spacing: 0.08em` for microcopy ("SCROLL TO EXPLORE", "A SELECTION OF IMMERSIVE DIGITAL EXPERIENCES…"). This two-scale contrast (huge sentence-case display vs. tiny caps utility) is the core typographic signature of the studio preset.
- **The panel pattern**: the WebGL canvas sits inside an inset rounded-corner dark panel (`border-radius: 24px`, ~40–60px margin from page edges), like a framed screen. Small `+` registration marks sit at the panel's corners outside it. Video reels get the same treatment.
- **Buttons**: dark pill buttons (`--ink` bg, paper text), tiny uppercase 13–14px label, with a small dot or glyph after the text ("LET'S TALK ·", "MENU ··").
- **Section rhythm**: giant display heading left-aligned + tiny uppercase annotation right-aligned on the same row; work shown as large rounded-corner media cards in an asymmetric 2-col grid.
- **3D look**: glossy soft-plastic objects (think toy jacks, blobs, ribbons) in ONLY white, black, and `--accent` blue. Soft studio lighting, gentle physics (float, collide, react to cursor). Playful, tactile, never sci-fi.

### Preset B — PRODUCT STORY (verified against oryzo.ai)

```css
:root {
  --void:   oklch(16% 0.02 60);    /* #16100A warm near-black, brown undertone */
  --cream:  oklch(93% 0.03 80);    /* #F6E8D2 display type + logo */
  --accent: oklch(58% 0.19 40);    /* #DC5000 burnt orange — glow, markers, packaging */
  --grid:   oklch(40% 0.02 60 / 0.35); /* faint measurement-grid lines */
}
```

- **Type**: condensed-ish grotesque (`Archivo`, `Halyard`-like, or `Inter` tightened). Display type is **enormous cream headline fragments** (15–25vw) that slide *behind* the pinned 3D object. Kickers are small UPPERCASE ("SO PORTABLE,", "24/7 UPTIME. NO POWER REQUIRED.").
- **The pinned object**: one photoreal hero object stays center-viewport for the entire page while the world changes around it — camera orbits, environments swap, giant text passes behind it. Scroll length is HUGE: 10–20 viewport-heights per chapter, `scrub` everywhere.
- **Blueprint motif**: dashed-line technical frames, circle guides with small orange square control-points (like a design-tool selection), faint measurement grids and rulers. The object periodically "dissolves" into its blueprint between chapters.
- **Copy voice**: deadpan mock-technical marketing. Spec tables, thermal diagrams, grip coefficients, absurd claims delivered straight. Sentence fragments as chapter titles.
- **Chapter variety**: at least one horizontal-scroll card carousel (full-height media cards sliding sideways while the page scrolls), one spec/variants comparison (e.g. Standard / Pro / Pro Max), one testimonial or grid section.
- **Nav**: tiny uppercase links top-right with dotted underline on the active item; vertical tab label on the viewport edge ("ORYZO-1 MODEL" style); "SCROLL TO CONTINUE" pill bottom-center.

### Deriving your own direction (when no palette is given)

When the brief names no colors, do NOT default to a preset or to dark-navy-plus-neon. Derive a direction from the brand itself — this procedure produced a direction rated "near perfect" on a real brief, and every step exists because skipping it produces template-looking output:

1. **Brand name → three mood words → a material world.** Interrogate the name and product before touching color. "Sunder" (= to split apart) + headphones → *machined, precise, torn-open* → the material world of an audio lab: graphite, forged aluminum, CAD drawings, foam. Colors get *picked from the material world*, never from a palette generator — that's why they cohere.
2. **Temperature is the first fork.** Warm undertones (cream/amber/brown — analog, comfort, hospitality, food, craft) or cold (blue-grey — engineering, precision, instruments, labs). Commit to one for the page. Never neutral-neutral: pure untinted greys read as unfinished.
3. **Neutrals are tinted, never pure.** Near-black at `oklch(11–16% 0.008–0.02 <hue>)` with the hue angle matching your temperature (Sunder: `oklch(15% 0.008 260)` — a breath of cold blue keeps graphite from going dead). "White" is never `#fff`: tint it. And a taste move worth stealing: warm the type-white even on a cold page (`oklch(94% 0.01 90)` bone) — text then reads as *printed on paper* rather than emitted by an LED, and the human-warm type against machine-cold ground is itself a designed contrast.
4. **The single accent needs a semantic alibi.** Name what the accent *is* in the product's world before using it: Oryzo's burnt orange is toasted cork and heat; Sunder's signal red-orange (`oklch(58% 0.24 30)`) is laser markers, safety flags, and the red control-point squares in CAD software. If you cannot say what the accent is, it's arbitrary, and arbitrary reads as templated.
5. **Accent budget: under ~2% of any viewport.** Kickers, pill dots, thin progress bar, blueprint squares, one drawn line. The accent is punctuation, not paint. The moment it fills a card or a section background, the page stops looking expensive.
6. **Choose the copy voice with the palette** — they are one decision. Cold precision → deadpan mock-technical ("Charge it in March. Again in May." / "TOLERANCE ±0.05 MM"); warm → droll and sensory. Numbers are designed objects in either voice.
7. **Let the name generate the signature interaction.** "Sunder" → the product physically splits apart on scroll and reassembles. When name, palette, copy voice, and hero behavior all express the same idea, the site reads as *conceived*, not assembled — this unity is most of what juries reward.
8. **Position against the presets deliberately.** Differ from both on at least the temperature or lightness axis (Sunder: cold where Oryzo is warm) so the result is a sibling of the references, not a re-skin.
9. **Borrow mechanics, never costumes — at most 1–2 recognizable moves per reference.** The references license *behaviors* (text-behind-object, the dissolve-to-drawing match cut, pinned-object storytelling); their surface identity is off-limits: never their typeface or a lookalike, never their annotation language, never their glyph vocabulary. Re-skin every borrowed mechanic in the brand's own material world. Sunder kept Oryzo's giant-text-behind and blueprint-dissolve *mechanics* but recostumed the drawing as an acoustic calibration target ("CAL TARGET · 94 DB SPL @ 1 KHZ", "0 DB = 20 µPA" — not CAD-sheet language like "DO NOT SCALE DRAWING"), swapped the design-tool selection squares for instrument tick marks, replaced the scroll pill with an animated VU level meter, and set the utility layer in a monospace so labels read as measurement printouts. Test: if a viewer who knows the reference could name it from a single cropped screenshot of your UI furniture, you copied the homework.

Invariants that keep any derived direction reading as award-grade: max 3 colors (one paper/void, one ink, ONE accent); one type family at two weights — OR a display grotesque paired with a monospace that owns the entire utility layer, when the material world justifies instrument language (Sunder: Space Grotesk display + IBM Plex Mono utility; mono runs wide, so cut caps tracking to ~0.04em). Never the reference's own typeface or a recognizable stand-in for it. Plus: the two-scale typography signature; either light-with-dark-panels or a committed warm/cold dark — never generic cool dark with neon; utility microcopy layer; rounded geometry everywhere (panels, pills, cards).

Worked example — the full Sunder token block with each choice's reason:

```css
:root {
  --void:   oklch(15% 0.008 260);  /* graphite: cold hue tint, never pure grey */
  --void-2: oklch(11% 0.008 255);  /* deeper layer for 2D-chapter cards */
  --bone:   oklch(94% 0.01 90);    /* type-white warmed toward paper, not #fff */
  --signal: oklch(58% 0.24 30);    /* laser/CAD-marker red-orange; punctuation only */
}
```

---

## Step 1 — Build the shell (no WebGL yet)

Start from `references/starter-scaffold.md` (a complete, tested baseline with pinned dependencies — shell + physics hero + scroll bridge already working) and extend it. Build out the full page in HTML/CSS: nav, hero copy, every section, footer, real copy, with a **solid placeholder div** where each additional canvas/scene will go (use `--panel` or `--void` color).

**Checkpoint before proceeding**: screenshot the shell. It must already look like a premium studio site — correct paper color, huge calm type, tiny caps labels, registration marks, pill buttons. If a section looks like a generic template (three equal feature cards, centered everything), fix it now. This checkpoint is where the "looks nothing like the reference" problem is won or lost.

Shell details that sell it:
- `+` registration marks at panel corners and section boundaries (absolutely-positioned pseudo-elements, 10px, `--ink` at 60%).
- A scroll cue: "SCROLL TO EXPLORE" (A) or a "⌄ SCROLL TO CONTINUE" pill (B), fixed bottom-center, tiny caps.
- Numbers as design elements: section indices ("01", "02"), coordinates, dimensions in the utility layer. On cards, repeat the index as a ghost numeral (~180px, type color at 4–6% opacity, bleeding off the card corner) — depth for free.
- Generous air: hero copy occupies < 40% of the viewport; sections breathe with 20–30vh gaps.
- The footer earns a personality beat: three tiny-caps fragments, and the last one is dry wit in the brand's voice ("BUILT LOUD IN A QUIET ROOM") — the only joke on the page, placed where only people who scrolled everything will find it.

## Step 2 — The 3D scene

One strong idea per scene, executed with material discipline:

- **One material family per scene.** Preset A: glossy plastic (`MeshPhysicalMaterial`, `roughness 0.15–0.3`, `clearcoat 1`) in white/black/accent only. Preset B: the real product material (cork, metal, fabric) rendered photoreal, plus cream/orange props.
- **Soft studio lighting**: programmatic HDR environment (no external .hdr files — see `references/webgl-recipes.md` §Environment), ACES tone mapping, one key light. Never colored point-light soup.
- **Physicality over spectacle**: objects have mass. For hero scenes, that means a real physics engine (Rapier): objects fall in under gravity on load, collide, settle, and the cursor is a kinematic collider that shoves them — see `references/interaction-recipes.md` §2–3. Where full physics is overkill, use spring integration or pointer parallax (§4–5), but a completely input-deaf 3D scene is never acceptable. A few chunky simulated objects beat 100k particles.
- **Real GLTF models** for any recognizable object; procedural geometry only for abstract blobs/ribbons. Preferred source is **generating the object in claude.ai/design** (`.glb` export) rather than stock — it gives you the exact object the brief describes, in the brand's material world, with no license credit. It is a browser step the user performs, not a tool you can call, so ask for it early and keep building against a stand-in primitive meanwhile. Sketchfab/Poly Haven are the fallbacks. See `references/webgl-recipes.md` §8.
- Particles are a *garnish*, not the scene — and only in the scene's own palette.

Full recipes (renderer setup, GPGPU particles, post pipeline, baked sims, GLTF normalization): **`references/webgl-recipes.md`**.

## Step 3 — Scroll choreography and chapter flow

*(If you chose the instrument structure above, this step is replaced by the findings model: no chapters, no boundaries, no match cuts. Skip to Step 4, which still applies in full.)*

The scroll IS the narrative, and the page is a sequence of *chapters* that move between 3D, hybrid, and 2D modes. Storyboard first — one line per chapter plus, critically, **one line per boundary** naming the match-cut anchor ("coaster's circle becomes the blueprint circle"). If a boundary has no nameable shared element, redesign it before coding.

Architecture (full detail in `references/flow-choreography.md`): one persistent canvas for the whole page, one master scroll progress, a chapter map with normalized local progress per chapter, a globally-bridged background that both the DOM and the scene read from. Chapter types to sequence: 3D establish → hybrid text-behind-object → vector dissolve → 2D carousel/spec chapters → 3D re-entry finale.

The individual motion moves live in `references/motion-recipes.md`:
- Lenis + GSAP bridge, camera path scrubbed through timeline segments (`scrub: 1–2`)
- Text-behind-object layering (canvas z-index between two DOM text layers)
- Pinned chapters and horizontal carousels (`pin: true, end: '+=150%'`)
- Scroll-velocity feeding shader distortion and object tilt
- Section-enter scroll pause (cinematic hold) — Preset B especially
- Camera/object screen-position vs. DOM text: keep text left-anchored, object right (or object center with text passing behind)

## Step 4 — Interactivity pass (the "never inert" rule)

Walk the finished page top to bottom and verify: at every scroll position, wiggling the mouse moves *something*. 3D chapters get cursor forces or pointer parallax; 2D chapters get velocity skew, draggable tracks, hover tilts, magnetic buttons; headings get SplitText reveals; spec callouts get world-space projected label chips. Recipes in `references/interaction-recipes.md` §7 and `references/motion-recipes.md`. Any chapter that fails the wiggle test gets one interactive element added before you move on.

## Step 5 — Polish and verify

- **Motion rules**: ease out with `power3.out`/`power4.out`/`expo.out` only. No bounce, no elastic. Scrubbed animations use `ease: 'none'` inside the timeline. Nothing snaps; everything has weight (`scrub ≥ 1`, lerped cursor/tilt).
- **Post-processing is seasoning**: at most ONE merged pass (grain 0.02 + vignette 0.28 + aberration 0.0015 — barely perceptible). Bloom only for abstract particle scenes, never on products or Preset A panels.
- **Verify by looking — mandatory.** Serve locally (`python -m http.server 3001`), then use whatever browser automation exists in your environment (Playwright MCP, claude-in-chrome, gstack, a headless-browser script — check your available tools) to screenshot at 4–6 scroll positions. If no browser tooling is available, write a short Playwright script (`npx playwright screenshot` works zero-config) or, as a last resort, ask the user to open the page and describe/screenshot it. Compare against the preset's checklist: paper color right? two-scale typography present? registration marks? object framed or pinned correctly? If a screenshot could be described as "dark site with glowing particles", you have failed the brief — return to Step 0.
- **Verify by interacting — equally mandatory.** Screenshots can't see behavior. Expose a debug handle from app code (`window.__dbg = { state: () => ({ progress, poseValues… }) }`) so interaction claims become numbers: drag, then read the rotation back; hold, read the held state, release, read again. Then in the browser: move the pointer through the hero (do objects react?), scroll fast then stop (does the world carry momentum and settle?), scrub across every chapter boundary slowly (can you point at a seam? — if yes, fix the match cut), hover buttons and cards, drag the carousel. Static screenshots passing while the page is inert is the failure mode this step exists to catch.
- **Distrust your own probes before distrusting the code.** Automation browsers throttle `requestAnimationFrame` (state looks frozen when the loop is merely starved — pump frames before reading), synthetic events must be dispatched on the element owning the listener, and threshold-gated interactions correctly ignore input fired at the wrong scroll position. Every "the drag is broken" verdict needs the checklist in pitfalls.md § Automation-browser verification traps run first — four false diagnoses on real builds came from skipping it.
- **Sweep the rendered copy against the Hard bans before shipping.** Run one pass over every visible string looking for ban-list artifacts — em dashes especially survive even careful builds because attention is on mechanics while copy is written (`grep -n "—" *.html` catches it in seconds). Bans apply to body copy, annotations, and microcopy alike.
- **Beware stale cache when verifying edits.** Dev servers send no cache headers; browsers keep executing the old module while the server serves the new one — code that "mysteriously doesn't work" with zero console errors is almost always this. Navigate with a fresh query per test run (`index.html?bust=<n>`), version-query your own script tags (`app.js?v=2`, bump on change), and settle any doubt in one probe: fetch the file with `{cache:'reload'}` and check for a marker string from your newest edit (pitfalls.md § Dev-server cache traps).
- Cap `devicePixelRatio` at 2; mobile gets reduced particle counts or a video fallback.

---

## Hard bans (each one instantly reads as AI-generated)

- Dark navy/black page + neon cyan/mint/purple accent (the #1 tell)
- Starfield particle background behind everything
- Bloom on product/panel scenes; stacked glow effects
- Gradient text (`background-clip: text`), glassmorphism cards
- Three identical feature cards in a row; centered-everything layouts
- `elastic`/`bounce` easing; spinning objects at constant velocity
- Sci-fi fonts (Orbitron, Audiowide), letterspaced uppercase headlines
- Em dashes in copy; "Elevate your…" marketing filler
- Purple-to-blue gradients on anything
- A hero that ignores the cursor (a rotating showpiece you can't touch is a screensaver, not a living site)
- Hard section breaks — background jumps or content swaps at a boundary with no shared anchor
- Scroll-jacking (wheel hijacked into discrete slides); everything is scrubbed, the user owns the scroll

## Reference files — read when you reach that step

- **`references/starter-scaffold.md`** — complete runnable baseline (Preset A shell + Rapier physics hero + Lenis bridge + SplitText + magnetic buttons) with pinned, SRI-hashed dependencies and a 5-point acceptance test. START HERE for any from-scratch build; adaptation notes for Preset B, React, and npm included.
- **`references/webgl-recipes.md`** — renderer/canvas-scroll sync, programmatic HDR environment, PBR materials, GPGPU particles, merged post pass, GLTF loading + normalization, baked-simulation playback, particle placement radii. Read at Step 2.
- **`references/interaction-recipes.md`** — the "never inert" rule, Rapier physics hero (gravity, collisions, cursor-as-collider, grab-and-throw, scroll shake), cheap spring physics, pointer parallax, the 2D interactivity kit, physics performance budget. Read at Step 2 for the hero and again at Step 4.
- **`references/flow-choreography.md`** — chapter-map architecture, match cuts, 3D→2D and 2D→3D handoffs with projection math, the blueprint dissolve, background bridging, the chapter-type playbook, persistent UI anchors. Read at Step 3.
- **`references/motion-recipes.md`** — Lenis+GSAP bridge, camera scrub timelines, text-behind-object, pinning + horizontal carousel, scroll velocity, cinematic hold, magnetic cursor, SplitText, 3D→screen label projection, object tilt, Barba page transitions. Read at Step 3.
- **`references/pitfalls.md`** — hard-won failure list: canvas positioning bugs, Lenis import rename, React/R3F hook traps, Three.js r151+ deprecations, ignorable console warnings, dev-server gotchas. Skim before Step 2; return when something misbehaves.
- **`references/inspiration.md`** — award-tier reference index across the whole interaction spectrum: scroll-driven product stories (bike, console, monolith, WebGPU microsite), hover-scrubbed personality sites, world-as-interface experiences (tiny-planet game, drivable portfolio), a studio/agency roster filed by signature mechanic (Active Theory, Unseen, 14islands, Darkroom, Immersive Garden, Obys…), and no-3D lanes (kinetic type, editorial grids) — each with steal-this mechanics, art-direction positioning notes, and an explicit confidence tier (visually reviewed vs corroborated). Read at Step 0 when the brief needs more reference range than the two presets, or when choosing which mechanics to borrow (never costumes — derivation step 9).

Related skills: `gsap` (deep GSAP API), `impeccable` (final design pass), `three-js-scroll` (lighter-weight scroll-3D without the full art direction).
