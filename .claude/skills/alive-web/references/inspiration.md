# Inspiration Index — award-tier references

Sites and studios that deliver the scroll-driven, object-held, cinematic-web feel. Two confidence tiers apply throughout: **visually reviewed** (screenshots taken in a real browser, July 2026) and **corroborated** (from research/write-ups/award pages, not personally screenshotted). Sites die and campaigns get retired: re-verify a URL before citing it to a user. Use everything here as a menu of *mechanics* to steal and art directions to position against — never copy any site's surface identity (SKILL.md derivation step 9).

## Tier 1 — visually verified, study these

### LOOK 795 Blade RS — `795bladers.lookcycle.com/en`
Racing bicycle. The closest verified sibling to oryzo.ai: one pinned 3D bike inside a dark "garage" environment with practical fluorescent light strips, ~27 viewport-heights of scrub. Camera cuts from clean side profile to dramatic low three-quarter angles as captions swap beneath ("Exceptional lightness… just 7 kg").
**Steal**: the *environment* as a character — the object never moves scenes, the lighting and camera do all the storytelling; staged caption swaps under a held object; scroll-driven part reveal.
**Position against**: 2-color cold clinical (near-black/near-white), sport-technical type. Occupies the "cold monochrome" slot — differ on accent or temperature.

### Analogue Pocket — `analogue.co/pocket`
Retro handheld console. Proof the feel does NOT require WebGL: ~33vh of scroll built from staged photography, exploded/multi-angle accessory views (Side/Back/Top/Front), and a numbered horizontal carousel embedded mid-scroll. Reverent, scholarly copy ("reference level database") — the closest *voice* match to Oryzo's deadpan found anywhere.
**Steal**: photography-staged exploded views when a 3D budget doesn't exist; horizontal chapter inside vertical scroll; the museum-plaque copy register.
**Position against**: black + high-contrast product photography. Its restraint is typographic, not chromatic.

### Hubtown — `hubtown.co.in` (Unseen Studio; Awwwards SOTD June 2026)
Real-estate brand story. Hero verified: a glowing blue 3D monolith floats over a dark reflective ocean between terrain banks, glitch-interrupted display type ("WE BUILD THE FUTUR OF REAL ES AT"), sound toggle, mono UI labels. Structurally the Oryzo formula (one hero object + text behind + scroll narrative) applied to a non-product — proof WebGL can make a "boring" B2B brand feel premium. Corroborated detail: a mouse-reveal interaction uncovers geometry/lighting detail.
**Steal**: the object-as-monument staging; glitch typography as a *sparing* texture; ambient sound as an opt-in layer; cursor as a flashlight over hidden detail.
**Caution**: it wheel-hijacks (virtual scroll, page height = 1 viewport) — admire the staging, keep our scrubbed-native-scroll rule. Also single-accent glow on dark = adjacent to the banned neon-on-dark look; it survives only because the glow IS the product object, not UI chrome.

### Lando Norris — `landonorris.com` (OFF+BRAND; Awwwards Site of the Year + Users' Choice)
F1 driver's personal platform — a *personality* site, not a product story, but its mechanics transfer. Visually verified including the signature move caught mid-transition: a racing helmet materializes over the driver's headshot in liquid horizontal slices that follow cursor position — identity (face ↔ helmet) as a hover scrub. ~16vh of scroll; deeper sections become a scattered photo journal (mixed sizes, mono location-date captions: "BARCELONA, 2024") with a live "NEXT RACE · SPA GP" data card, and pull quotes set in a personality serif against the grotesque nav.
**Steal**: cursor-position-dependent reveal of a second identity layer (works for any product with an "inside" — X-ray, cutaway, thermal view); scattered-journal photo grids with instrument captions; live data as a design element; mixing one serif voice into a grotesque system for *spoken* copy only.
**Position against**: light warm paper + faint topographic contour doodles + ONE acid chartreuse accent. Occupies the "light + acid" slot — and proves award-tier doesn't require a dark page.

## Beyond scroll — world-as-interface (the far pole)

When the brief says "playable", "explorable", or the product IS a world, scroll chapters stop being the frame.

### Messenger — `messenger.abeto.co` (Vicente Lucendo / Abeto) — visually verified
A complete miniature planet you walk around delivering mail — the hand-drawn-outline world floats in a flat teal sky, whole villages readable from orbit distance. Techniques (from the developers' write-ups): sphere built as an "unwrapped cube" to minimize distortion, custom outline rendering for the hand-drawn look, aggressive LOD swapping, 3D UI drawn inside the canvas, spatial audio, WASM font rendering.
**Steal**: the world-as-interface ceiling — navigation replaces scrolling entirely; the single-environment commitment taken to its logical end; outline shading as an art direction that makes low-poly read as *crafted* instead of cheap.

### Bruno Simon — `bruno-simon.com` (recently rebuilt) — loader-only in my headless review; details corroborated
The benchmark portfolio: a fully drivable 3D car world (Rapier physics) as the navigation metaphor, rebuilt on the WebGPU renderer with TSL shaders, now with real-time multiplayer "whispers" and a live leaderboard. **URL note**: use the hyphenated `bruno-simon.com` — `brunosimon.com` is a parked domain.
**Steal**: physics as the primary input (the same instinct as our Rapier hero, taken to full-world scale); audio as a spatial layer, not a soundtrack; live multiplayer presence as a reason to return.

## Studios & agencies — corroborated; study their signature mechanics

Research-sourced (award pages, write-ups, July 2026), not personally screenshotted. Each line is a mechanic worth stealing, filed under who does it best.

- **Active Theory** (LA/Amsterdam; Google, Spotify, Hennessy) — real-time particle systems networked across live visitors (multiplayer cursor trails); fully immersive 3D environments on their custom "Hydra" framework; AI-guided site navigation layered over WebGL scenes.
- **Resn** (Wellington) — playful, character-driven WebGL: a revolving crystalline 3D centerpiece as the homepage hub; interactive experiments/easter eggs threaded throughout.
- **Unseen Studio** (Awwwards "Design Studio of the Year") — drag-to-explore "World" page navigation; type-led motion pacing with impeccable restraint. (Also built Hubtown, above.)
- **14islands** (Stockholm/Reykjavík; open-sourced `r3f-scroll-rig`) — WebGL shader interactions layered onto ordinary React components; a scroll-rig that keeps DOM layout and the Three.js/R3F canvas in sync. The library to reach for when the brief is "React site with WebGL accents" rather than "one big canvas".
- **Darkroom Engineering** (formerly Studio Freight; maintainers of Lenis) — built Lenis, Satus (Next.js/R3F starter), Hamo, Tempus. Engineering-first performance discipline: motion that holds up under load. Their repos are the reference implementation for our own Lenis bridge.
- **Immersive Garden** (Paris; Cartier, Louis Vuitton, Dior) — six-room scrollable 3D "alcove" format, one scene per product; cinematic camera choreography for product reveals (Three.js, GLSL, GSAP, Lenis, Web Audio). The structure to study when a brief has a *collection* instead of one hero object.
- **Obys Agency** (editorial art-direction benchmark) — full-bleed video grid with continuous horizontal/vertical scroll modes; typographic motion where static frames already read as posters. The bar for "every scroll position is a screenshot".
- **Uncommon Studio** (Awwwards SOTD + Developer Award) — GSAP "camera move" transitions between sections; full-bleed video reel with scrubbing.

## Product / brand sites — corroborated additions

- **IVRESS** — Japanese brand-story microsite (Utsubo; FWA Site of the Month, May 2026): WebGPURenderer with automatic WebGL fallback, shaders authored in TSL; chaptered scroll narrative (9 chapters) with tap-to-interact beats; a *budgeted* scene graph — deliberate motion over brute-force effects. The forward-compatibility reference: how to adopt WebGPU today without stranding WebGL users.
- **by-kin** (Manchester interior-design studio) — weighted smooth-scroll with GSAP timeline choreography; continuous-surface transitions that never call attention to themselves. Study for the "quiet luxury" register where the craft is invisible.
- **Explore Primland — `explore.ownprimland.com`** (Auberge Resorts; Awwwards SOTD Feb 2026): cinematic aerial 3D terrain flythrough with atmospheric fog; scroll-driven camera gliding over rendered landscape; ambient audio synced to scroll progress; a "seasons" toggle that relights the whole environment mid-scroll — the technique to study for material/colorway switchers. Loader never finished in my headless browser; verify in a real one.
- **Sleep Well Creatives — `sleep-well-creatives.com`** (Awwwards SOTD Jan 2026): hand-illustrated 3D world sequenced entirely by scroll position; audio-reactive chapter transitions; editorial pacing (entrance/hold/exit per section) for long-form content; deep blue + cream two-tone. Sits behind an "Enter Site" gate (couldn't screenshot content headless). Useful when the product has no single heroic silhouette — the *environment* is the hero.
- **Apple AirPods Pro — `apple.com/airpods-pro`**: staged scroll-triggered image sequences build an exploded internals view ("Take a closer look"); AR view as end-of-scroll payoff. The mainstream ceiling of the no-WebGL approach. Clinical white/airy — the "light mode" counterexample to all the dark references.

## Personal portfolios — corroborated

- **Mat Voyce** (kinetic-type designer: FT, Nike, Pepsi; GSAP Site of the Year nominee) — timeline-driven kinetic typography: letters stretch, snap, and recombine on scroll, with motion reveals tuned so animation never blocks readability. The reference for a *type-only* signature interaction when there's no 3D object at all.
- **Minh Pham** (product/visual designer: Fantasy, Ford, UFC) — GSAP motion layered over Three.js without overwhelming content; an interactive 3D client-logo "planet" as centerpiece. Study for balancing showcase spectacle against portfolio legibility.
- **Cuberto** (runner-up) — mouse-follower interactions, video-heavy case studies. Verified live; a solid reference for cursor craft specifically.

## Dead/retired (do not cite)

- Opal Tadpole's award-winning scroll site — `opal.camera` now redirects to a minimal teaser; the awarded experience is gone.
- Cartier Watches & Wonders (Immersive Garden) — campaign microsite retired into the main e-commerce catalog.

## What the full set teaches, distilled

1. The pinned-object formula generalizes far beyond gadgets (bike, monolith, terrain, a person's face) — what's constant is *one subject, held, while everything else changes*.
2. There are two budgets for the same feel: full WebGL (LOOK, Hubtown) and staged photography with scroll triggers (Analogue, Apple, Lando). Choose by asset availability, not ambition — Analogue proves the cheap route can still feel reverent.
3. Every strong example commits to ONE environment idea (garage, ocean, tunnel, studio-white, paper-with-contours, teal sky) rather than swapping backdrops per section — reinforcing the background-bridging rule in flow-choreography.md.
4. The copy voice does heavy lifting in all of them; none use generic marketing speak.
5. The interaction spectrum runs: scrubbed scroll story (Oryzo, LOOK, IVRESS) → hover-scrubbed identity layers (Lando, Hubtown's mouse-reveal) → drag-to-explore navigation (Unseen's World page) → fully navigable world (Messenger, Bruno Simon). Pick the point that matches the brief's appetite — going further right costs exponentially more and abandons the scroll-owns-time contract, so it needs explicit user buy-in.
6. Light pages win awards too (Lando's paper + acid, Apple's clinical white) — the dark-page default is a habit, not a requirement.
7. There is a no-3D lane at every tier: kinetic type alone (Mat Voyce), editorial grids where every frame is a poster (Obys), staged photography (Analogue). A brief with no model budget still has an award-tier path.
8. The platform is moving: WebGPU + TSL with automatic WebGL fallback is shipping on award winners now (IVRESS, Bruno Simon). Adopt via renderer fallback, never as a hard requirement.
9. Engineering discipline IS an aesthetic (Darkroom, 14islands): motion that holds 60fps under load reads as premium; the same motion janking reads as broken. Budget the scene graph deliberately (IVRESS) instead of stacking effects.

## Validated additions — September 2026 (existence re-checked by fetching each evidence page)

Added because builds kept reaching for the same six references above. "Verified" = the award page or article was fetched and the listed detail is stated there. Mechanics beyond that line are NOT verified; do not embellish them.

### Cursor reveals and image transitions
- **Lando Norris hero, how it is built** — three.js forum thread `discourse.threejs.org/t/.../87857` ("liquid blob masking cursor effect"): replies point to a WebGL fluid simulation used as a mask, texture UVs in screen space; "This is not trivial". Recreation repo: `github.com/zeinaboud/landonorris-task` (not reviewed).
- **Dual-Scene Fluid X-Ray Reveal** — Codrops, Cullen Webber, 2026-03-23 (verified). Pipeline: 2D canvas cursor mask -> ping-pong fluid sim with FBM displacement -> two scenes rendered to targets -> composite by fluid mask. The closest published recipe to Lando's reveal, for 3D subjects.
- **Mouse-Following Square Lens** — Codrops, Tomoyuki Nakata, 2026-08-25 (verified). Grayscale image + colour image inside a cursor-following square, CC-Lens bulge distortion, radial RGB shift toward the square's edges.
- **Efecto: ASCII and dithering shaders** — Codrops, 2026-01-04 (corroborated by agent fetch). Floyd-Steinberg on CPU, procedural 5x7 ASCII glyphs in shader.
- **WebGPU scanning effect with depth maps** — Codrops, 2025-03-31 (corroborated). TSL; depth map drives UV displacement and a scan-line reveal of a dot grid.

### Scroll and layout mechanics that are not pin + scrub
- **Scroll-driven dual-wave text** — Codrops, Valentin Descombes, 2026-01-15 (verified). Two columns of text offset horizontally by a sine phase of scroll progress and index; the item nearest centre drives a synced image.
- **Infinite Canvas, pan-anywhere image space** — Codrops, Edoardo Lunardi, 2026-01-07 (verified). Seeded chunk streaming around the camera (3x3x3), distance fade and culling, inertial pan on mouse/touch/keys.
- **SVG mask transitions on scroll** — Codrops, Hiroki Watanabe, 2026-03-11 (corroborated). Blinds/grid/column-wave masks; overlap 0.01-0.1 to kill subpixel seams; `shape-rendering: crispEdges`.
- **Infinite GSAP scroll gallery with Flip** — Codrops, 2026-07-30 (corroborated). Paused timeline as scroll controller; parallax offset zeroed at the wrap point to hide the loop seam.
- **Scroll-reactive 3D gallery, velocity-driven mood** — Codrops, 2026-03-09 (corroborated). Scroll velocity drives brightness, tilt and palette interpolation rather than position.
- **Cross-document View Transitions** — css-tricks "Cross-Document View Transitions part 2" and Chrome's "View transitions in 2025" (corroborated): `view-transition-name`, `match-element`, nested transition groups (Chrome 140).

### Award sites, luxury / object lane (award page verified)
- **OCCUPY** (`occupied.unadsgn.tw`, Una Huang) — Awwwards SOTD 2026-01-27. Bespoke jewellery; award page lists a "tear-open strip" scroll interaction, loading sequence, mouse interaction.
- **The Watch / FS 60P** (`thewatch.60fps.fr`, 60fps) — Awwwards SOTD 2026-08-17. "A real-time WebGL piece that interacts with the content around it."
- **MIU MIU, A House That We Shaped** (`immersivebags.miumiu.com`, Merci Michel) — Awwwards SOTD 2026-08-25. Explore a house and handle objects; listed interactions include a Viewmaster and Matelassé interaction and colour selection.
- **Cartier Watches & Wonders 2025** (60fps) — Awwwards SOTD 2025-08-18. 3D "universes", product interactions, gestures. (The earlier Immersive Garden Cartier microsite above is retired; this is a different year.)
- **OceanX 2025** (`2025.oceanx.org`, Unseen + PROPAGANDE) — Awwwards SOTD 2026-02-23. WebGL timeline, WebGL intro transition, horizontal layout.
- Corroborated only (agent-reported, not re-checked): Floema Jewelry (WebGL brand experience), Art Here 2025 / Richard Mille (SOTD 2026-02-23, light-and-shadow theme), Vero New-York (SOTD 2026-08-08, WebGL in nav), Unseen Studio 2025 Wrapped (ASCII liquid sim), Utsubo 2024 (WebGPU boids flock), Shopify Live Globe 2025 (live data globe + pinball).

### Lessons from validating agent research
Haiku research agents reliably found real URLs but padded "mechanics" with plausible guesses ("likely clip-path", invented water physics) and one unsourced statistic. Always re-fetch the evidence page and keep only what it states.
