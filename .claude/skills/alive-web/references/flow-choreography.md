# Flow Choreography — one continuous experience across 3D and 2D chapters

Read this at Step 3. This is the other half of what wins awards: oryzo.ai is not "a 3D site" — it is a sequence of chapters that move between full 3D (camera orbiting the coaster), hybrid (giant 2D text sliding behind the 3D object), pure 2D (horizontal card carousel, spec tables), vector (the object dissolving into its dashed blueprint), and back into 3D — and you can never point at the seam. The craft is in the handoffs.

## Contents
1. Architecture: one canvas, one timeline, a chapter map
2. Match cuts — the film rule that makes handoffs invisible
3. 3D → 2D handoff (object becomes a DOM/SVG element)
4. 2D → 3D handoff (DOM element becomes the object)
5. The blueprint dissolve (Oryzo's signature transition)
6. Background bridging
7. Chapter-type playbook (the Oryzo sequence, generalized)
8. Persistent UI anchors
9. Don'ts

---

## 1. Architecture: one canvas, one timeline, a chapter map

**One persistent canvas for the whole page.** Never mount/unmount canvases per section — WebGL context churn causes visible pops and stalls. The canvas stays fixed and full-viewport; chapters change what it renders and how much of it is visible (scene swaps, camera moves, exposure/opacity tweens).

**One source of truth for progress.** A single ScrollTrigger spanning the page drives a master `progress` (0–1). Chapters are ranges of that progress:

```javascript
// `local: 0` on every entry is MANDATORY — onUpdate hasn't fired on the first
// rendered frame, and an undefined local poisons the camera with NaN (pitfalls.md
// "Chapter map / render loop"): the page renders nothing with zero console errors.
const chapters = [
  { name: 'hero',      range: [0.00, 0.14], mode: '3d',     local: 0 },
  { name: 'portable',  range: [0.14, 0.30], mode: 'hybrid', local: 0 }, // text behind object
  { name: 'blueprint', range: [0.30, 0.38], mode: 'vector', local: 0 }, // dissolve transition
  { name: 'carousel',  range: [0.38, 0.58], mode: '2d',     local: 0 },
  { name: 'variants',  range: [0.58, 0.72], mode: '2d',     local: 0 },
  { name: 'finale',    range: [0.72, 1.00], mode: '3d',     local: 0 },
]

ScrollTrigger.create({
  trigger: '#page', start: 'top top', end: 'bottom bottom', scrub: true,
  onUpdate(self) {
    for (const c of chapters) {
      const [s, e] = c.range
      c.local = THREE.MathUtils.clamp((self.progress - s) / (e - s), 0, 1)
    }
  }
})
```

Each chapter reads its own normalized `local` progress (0 before it, 0→1 through it, 1 after). Camera paths, text slides, dissolves, and carousel offsets are all functions of a chapter's `local` — which means adjusting one chapter's scroll length never breaks the others. DOM sections still exist for semantics/pinning, but *motion* is driven from the map.

**Derive the ranges, don't hardcode them.** Hand-tuned fractions rot the moment a chapter is added or a scroll length changes — every number after the edit point shifts. Instead, give the page one `.spacer` element per chapter (`<section class="spacer" style="height:200vh">`), same order as the chapter array, and build the ranges from their live heights at init (and on resize):

```javascript
function buildRanges() {
  const spacers = [...document.querySelectorAll('#page .spacer')]
  const total = spacers.reduce((s, el) => s + el.offsetHeight, 0)
  let acc = 0
  chapters.forEach((c, i) => {
    c.range = [acc / total, (acc + spacers[i].offsetHeight) / total]
    acc += spacers[i].offsetHeight
  })
}
```

Now inserting a chapter = add one spacer + one array entry; every other chapter keeps its tuning because each still owns its own untouched spacer. This is what turned "add three more interactive sections" into an hour instead of a re-choreography on a real build. Two footguns: any "which chapter am I in" lookup (`p >= s && p < e`) misses `p === 1` exactly — fall back to the last chapter; and keyframe per-chapter background colors at chapter *midpoints computed from these same ranges*, so backgrounds move when chapters do.

Give the page real scroll length: 10–20 viewport-heights total for a product story. Each chapter needs room to breathe (nothing under ~1.5 viewport-heights).

## 2. Match cuts — the film rule that makes handoffs invisible

Every chapter boundary is a *cut*, and film editing solved this a century ago: a cut is invisible when the outgoing and incoming frames share an anchor — same shape, same screen position, same scale, continuous background. Apply it mechanically:

> **At every chapter boundary, name the anchor.** "The coaster's circle (center screen, 40vh wide) becomes the dashed blueprint circle." "The blueprint circle becomes the first carousel card's rounded mask." If you cannot name the shared element, the transition will feel like two stapled-together pages — redesign the boundary.

The three continuity channels, strongest first:
1. **Shape/position** — an element at the same place and size across the cut (the anchor).
2. **Background** — one continuous color/gradient tween spanning the boundary (§6).
3. **Motion** — velocity carries through: if things were drifting left before the cut, the new chapter enters drifting left.

You need at least two of the three at every boundary.

## 3. 3D → 2D handoff (object becomes a DOM/SVG element)

Project the 3D anchor's screen position/size, place the DOM successor exactly there, crossfade over a short scroll window (~6–10% of the page), then the DOM element carries the narrative.

```javascript
// screen-space center + radius of a 3D object
const wp = new THREE.Vector3(), edge = new THREE.Vector3()
function screenCircle(mesh, worldRadius) {
  mesh.getWorldPosition(wp)
  const c = wp.clone().project(camera)
  edge.copy(wp).add(new THREE.Vector3(worldRadius, 0, 0))
  const e = edge.project(camera)
  return {
    x: (c.x * 0.5 + 0.5) * innerWidth,
    y: (-c.y * 0.5 + 0.5) * innerHeight,
    r: Math.abs(e.x - c.x) * 0.5 * innerWidth,
  }
}

// during the handoff window (chapter.local of the transition chapter):
const t = chapters[2].local          // 0→1 across the boundary
const { x, y, r } = screenCircle(hero, 1.0)
gsap.set('#successor', { left: x, top: y, width: r * 2, height: r * 2, xPercent: -50, yPercent: -50 })
gsap.set('#successor', { opacity: THREE.MathUtils.smoothstep(t, 0.15, 0.5) })
heroMaterial.opacity = 1 - THREE.MathUtils.smoothstep(t, 0.3, 0.7)   // overlap, don't swap
```

Key details:
- **Overlap the fades** (successor in by t=0.5, object out by t=0.7) — a gap reads as a glitch, a hard swap reads as a cut.
- Track the projection *every frame* during the window, not once — the camera may still be moving.
- The successor keeps the object's rounded silhouette (border-radius or SVG circle), so the eye never loses the anchor.

## 4. 2D → 3D handoff (DOM element becomes the object)

The reverse: measure the DOM anchor's rect, compute the world scale/position that makes the 3D object's projection match it, then fade the object in as the DOM fades out.

```javascript
// world units per CSS pixel at depth `dist` from a perspective camera
function worldPerPixel(camera, dist) {
  const h = 2 * dist * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2))
  return h / innerHeight
}

const rect = successor.getBoundingClientRect()
const dist = camera.position.z            // object plane
const wpp = worldPerPixel(camera, dist)
hero.scale.setScalar((rect.width * wpp) / heroNativeDiameter)
hero.position.x = (rect.left + rect.width / 2 - innerWidth / 2) * wpp
hero.position.y = -(rect.top + rect.height / 2 - innerHeight / 2) * wpp
```

Snap the object to the rect at the start of the window, then let the chapter's camera path take over — the first camera move *away* from the matched position is what sells "the picture came alive".

## 5. The blueprint dissolve (Oryzo's signature transition)

The photoreal object dissolves into its technical drawing between chapters — simultaneously a transition, a brand moment, and a breather. The version below is the refined recipe from the Sunder build, where the registration is exact rather than approximate:

1. **Derive the drawing from the model — don't hand-draw it.** At load, pose the model exactly as the drawing will show it, measure the anchor features in world space (`Box3.setFromObject().getCenter()/getSize()` per part group), and write the SVG's circle centers/radii and path `d` attributes from those measurements. Hand-drawn SVGs never quite fit; measured ones fit by construction and survive model swaps. Keep dashed outlines, small accent squares at control points, faint crosshair guides; `pointer-events: none`.
2. **Fit per-frame with a two-anchor projection**: store two anchor offsets in pivot-local space at load (e.g. both cup-face centers — pose-independent), then each frame `updateMatrixWorld(true)` → `pivot.localToWorld(offset).project(camera)` for both → scale the SVG so its two reference points land on the two projections. The drawing stays glued through camera moves, cursor nudges, and resizes.
3. **Pose the object for the drawing, visibly.** If the drawing shows the object face-on (full circles) but the object is edge-on, rotate the relevant parts into the diagram pose as the drawing draws — a cup swiveling open so its cushion's full circle matches the drawn circle reads as deliberate mechanical choreography. Spin parts *in place* (measure and compensate the pivot swing — pitfalls.md "Rig / pose interpolation") so silhouettes stay natural; parts flared away from the body read as broken, not exploded.
4. **Scrubbed sequence with strict ordering** (one chapter of ~8–10% page progress): dashes draw in (`stroke-dashoffset` scrub) + parts swivel to the diagram pose → *only after the drawing completes*, the object fades out under it → hold on pure blueprint. Reverse to re-enter 3D: drawing appears alone → object fades in inside it (matching exactly, because of 1–3) → dashes retract → parts fold back to the display pose. Every fade in this sequence is a pure function of chapter-local progress (never time-smoothed — see pitfalls.md), so drawing and object can never drift out of sync.
5. Hold the camera still through both handoffs; start camera moves only after the fold-back completes.

Works with any product: the blueprint is just the object's silhouette + guides. This pattern generalizes: any "the thing becomes a diagram of itself" handoff (map → route line, UI card → wireframe) reads as intentional design.

## 6. Background bridging

One continuous background tween across every boundary, owned globally — never per-chapter backgrounds that switch at edges:

```javascript
const bg = { color: '#16100A' }   // start = the hero chapter's background
const bgTl = gsap.timeline({ scrollTrigger: { trigger: '#page', start: 'top top', end: 'bottom bottom', scrub: 1 } })
bgTl.to(bg, { color: '#1A0F08', duration: 0.2 }, 0.10)   // positions on master progress
    .to(bg, { color: '#0E0C0A', duration: 0.2 }, 0.34)
// apply to BOTH worlds every frame so canvas and DOM can never diverge:
scene.background?.set(bg.color); document.body.style.backgroundColor = bg.color
renderer.setClearColor(bg.color)  // when using alpha canvas over DOM bg, skip this
```

Because the background is shared, a 3D chapter can hand off to a 2D chapter with *zero* visible boundary even before the anchor work — the world just keeps flowing.

## 7. Chapter-type playbook (the Oryzo sequence, generalized)

Sequence these to get the "flows between 3D and 2D" feel. Interactivity requirement per type comes from interaction-recipes.md §1.

| Chapter type | What happens | Interactive element |
|---|---|---|
| **3D establish** | Camera orbits/approaches the hero; kickers fade through | Pointer parallax, cursor force |
| **Hybrid text-behind** | Object pinned; enormous display text slides behind it (motion-recipes.md §3); kicker + body swap per beat | Parallax + text drifts with pointer |
| **Vector dissolve** | Blueprint transition (§5) — doubles as the 3D→2D cut | Dash-draw scrubs with scroll direction |
| **2D horizontal carousel** | Pinned section, track slides sideways (motion-recipes.md §4), full-height media cards | Draggable with inertia; hover tilt on cards |
| **2D spec/variants** | Comparison columns, mock-technical tables, testimonials | Velocity skew, magnetic CTAs, hover reveals |
| **3D re-entry finale** | Reverse dissolve or 2D→3D match cut (§4); camera pulls back for the closing statement + CTA | Full physics playground or grab-and-throw |

Rhythm rules: never two heavy 3D chapters back-to-back without a 2D breather; never end on 2D — the finale returns to the object; the carousel/spec chapters are where actual information lives (the 3D chapters carry feeling, the 2D chapters carry facts).

## 8. Persistent UI anchors

Continuity is also carried by what *doesn't* change: fixed nav (tiny caps links, dotted-underline active state that updates per chapter), the scroll cue pill, a progress indicator (thin bar or chapter dots), the vertical edge tab label. These live above every mode and are the user's handrail through the cuts. Update the nav's active state from the chapter map — not from separate IntersectionObservers that can disagree with it.

## 9. Don'ts

- Don't mount/unmount canvases or renderers per section — one persistent canvas, always.
- Don't hard-swap at a boundary with no named anchor — every cut needs its match (§2).
- Don't fade to black/white between chapters — that's a scene *break*, the opposite of flow. Bridge the background instead.
- Don't let a 2D chapter go inert (no hover, no skew, no drag) — the mode switch becomes obvious precisely because the aliveness dropped.
- Don't run separate uncoordinated ScrollTriggers for camera, text, and background over the same region — drive them from the chapter map so their timing is provably aligned.
- Don't scroll-jack (hijacking wheel to step between slides). Everything is scrubbed; the user always owns the scroll position. The cinematic hold (motion-recipes.md §8) is the only sanctioned pause, and it's ≤ 1.2s, forward-only.
