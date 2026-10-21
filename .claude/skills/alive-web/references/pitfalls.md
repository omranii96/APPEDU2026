# Pitfalls — failures that actually happened on builds from this skill

Skim before starting Step 2; return here when something misbehaves. Every entry below cost a real debugging session.

## Canvas + scroll

- **Never apply `translateY(scrollY)` to a `position: fixed` canvas.** Fixed is already viewport-locked; adding the offset pushes the canvas off-screen within a few pixels of scrolling and the whole scene "disappears". Valid combos: `fixed` + no transform, or `absolute` (full page height) + `translateY(scrollY)` each rAF. Pick one, never mix.
- Serve over HTTP (`python -m http.server 3001`) — `file://` blocks ES-module imports and GLTF/texture fetches. Avoid port 3000 on Windows (frequently occupied).
- **Serve from the common root, not the site folder.** If shared assets live *above* the page's folder (`models/` beside `site/`, referenced as `../models/...`), serving from inside `site/` makes every `../` URL 404 — symptom: "the 3D model isn't showing", static shell renders fine, or the browser shows a bare directory listing. Serve the parent and open `http://localhost:PORT/site/`. This exact mistake resurfaced when relaunching a working build for the user.

## Lenis / GSAP

- Install `lenis`, not `@studio-freight/lenis` (deprecated rename; the old package silently drifts out of date).
- Always run the full bridge: `lenis.on('scroll', ScrollTrigger.update)` + `gsap.ticker.add(t => lenis.raf(t * 1000))` + `gsap.ticker.lagSmoothing(0)`. A bare scroll listener calling `ScrollTrigger.update` makes Lenis and ScrollTrigger fight over scroll position (visible jitter).
- After Barba page transitions, kill and re-create ScrollTriggers (`ScrollTrigger.getAll().forEach(t => t.kill())`) — stale triggers point at removed DOM.

## Three.js version traps

- `RoomEnvironment` is not importable as a standalone module in r151+. Use the programmatic `DataTexture` + `PMREMGenerator.fromEquirectangular()` environment (webgl-recipes.md §2).
- Import loaders from `three/addons/...` (r150+ path), not `three/examples/jsm/...` when using import maps with current builds.

## React / R3F

- Store all animated values in module-level plain objects (`const cam = { x: 0, y: 0, z: 8 }`); GSAP tweens them, `useFrame` reads them. Zero re-renders. Never `useState` for per-frame values.
- Never place a conditional early return before hooks (`useRef`, `useEffect`) — Rules of Hooks violation that crashes at runtime, not build time. Put conditions in a hook-free wrapper component.
- Don't cast a plain `{ x, z }` object with `as unknown as React.MutableRefObject<T>` — it has no `.current`, so consumers read `undefined` and the effect silently does nothing. Wrap it: `{ current: plainObj }`.
- Split `EffectComposer` creation from resizing: one `useEffect` keyed on `[gl, scene, camera]` builds it once; a separate `useEffect` keyed on `[size]` calls `composer.setSize()`. Putting `size` in the creation deps rebuilds the whole pipeline every resize.
- `useGLTF` from `@react-three/drei`, with `useGLTF.preload('/path')` at module level.

## Events / DOM

- Capture `querySelectorAll` results into an array once and reuse the same array in cleanup — re-querying in cleanup can miss elements if the DOM changed, leaking listeners.

## Chapter map / render loop (from the Sunder build)

- **Initialize every chapter's `local` to 0 at creation.** ScrollTrigger's `onUpdate` hasn't fired on the first rendered frame, so `chapter.local` is `undefined` → `Math.sin(undefined)` → NaN camera position, and `camera.position.lerp(NaN)` poisons the camera permanently. The page renders nothing with zero console errors.
- **Per-frame smoothing must be dt-based** (`v += (target - v) * Math.min(1, dt * k)`), never a bare per-frame factor (`v += (target - v) * 0.07`). Frame-factor lerps converge 6× slower at 10fps (weak GPUs, headless test browsers), so fades that look instant on your machine visibly lag elsewhere. Snap when within ~0.02 of the target.
- **Anything that must stay synchronized with a scrubbed animation must itself be scrubbed.** If the wireframe draw is a function of scroll but the model's crossfade is time-smoothed, they drift apart at low framerates and the match cut visibly breaks. Rule: fades that participate in a match cut are pure functions of chapter-local progress; time-smoothing is only for cursor-follow and physics-feel, never for handoff opacity.
- **Idle auto-rotation accumulates without bound** — any chapter whose 2D overlay assumes a fixed object orientation (blueprint, exploded diagram, projection-matched successor) needs a spring back to the nearest full turn (`Math.round(y / (2π)) * 2π`) while that chapter is active, or the match cut breaks after the user has idled.
- **Drag-to-spin: accumulate pointer dx in the event handler, consume it in the render loop.** Applying per-event deltas scaled by a per-frame velocity mixes event rate with frame rate — the same gesture spins 5× less on a slow device.
- **Hold interactions** (press = state A while held, release = spring back): `gsap.killTweensOf(state)` then tween toward the held value on `pointerdown`; tween back on `pointerup` AND `pointercancel` AND `window blur` — missing the last two leaves the state stuck when the pointer leaves the window or the tab switches.

## Rig / pose interpolation (from the Sunder build)

- **Rotating a part about an offset pivot swings its center.** A cup pivoted at the yoke tip that rotates 180° ends up far from where it started — the "flared out" look. For spin-in-place poses: at load, measure the part's world center in pose A and pose B (`Box3.setFromObject().getCenter()` after `updateMatrixWorld(true)`), and store a compensating position offset so the center stays fixed while the orientation changes. Convert the world offset into pivot-parent space with two `worldToLocal` calls (a base point and base+offset), not `transformDirection` (which ignores scale).
- **Never assume which face of a part is showing.** "Home" orientation showed the cups' outer plates when the design needed cushions — indistinguishable in code, obvious in a zoomed screenshot (`clip:` region screenshot of just the part). A/B the rotation sign/angle empirically before wiring it into choreography; orientation semantics (front/back, inside/outside) are only verifiable by looking.
- Distinct poses deserve distinct stored quaternions per part (`homeQ` flat-pack, `targetQ` assembled, `diagramQ` display) composed at load — do not try to express a third pose as a scalar along the home↔target slerp; the shortest-arc path will not pass through it.

## Overlay ↔ 3D registration (the match-cut upgrade that made the blueprint exact)

- **Derive overlay geometry from the model, don't hand-draw it.** At load, pose the rig in the exact pose the overlay must match, measure the real anchor features in world space (cup centers, radii, band bounds), and write the SVG's circle positions/radii/path `d` from those measurements. Registration is then exact *by construction* and survives model swaps.
- **Fit the overlay per-frame by projecting two anchor points** (e.g. both cup-face centers) and mapping the overlay's corresponding reference points onto them — scale = projected distance / reference distance. Store anchor offsets in *pivot-local* space at load (pose-independent); per frame `pivot.localToWorld(offset).project(camera)` after a fresh `updateMatrixWorld(true)`.
- Sequence the handoff so the object is only hidden while the drawing fully represents it: outbound = draw completes → THEN model fades; inbound = model fades in → THEN drawing retracts. A gap where neither is fully present reads as a glitch.

## Dev-server cache traps (cost a full debugging detour)

- **`python -m http.server` sends no cache headers; browsers heuristically cache both HTML and ES modules.** Your edits can be served correctly (curl shows the new file) while the browser keeps executing the old module — new code appears to "not work" with zero errors. Version-query local assets (`app.js?v=5`, bump on change) and hard-refresh (Ctrl+Shift+R) after edits.
- Playwright's `page.goto`/`page.reload` do NOT bypass this cache, and CDP `Network.setCacheDisabled` is not always enough for the top-level document — navigate to `index.html?bust=' + Date.now()` in tests to guarantee freshness.
- Diagnostic that settles it in one step: `fetch('app.js', {cache:'reload'}).then(r => r.text())` and check for a marker string from your newest edit — if the fetch has it and the page behavior doesn't, you are running stale cache, not broken code.

## Automation-browser verification traps (cost four false diagnoses across two sessions)

When Step 5 says "verify by interacting", the probe itself becomes a component that can fail. Every entry here produced a confident, wrong "the code is broken" verdict on code that was fine.

- **Headless/backgrounded tabs throttle `requestAnimationFrame` to ~1 frame per 200ms** (Playwright MCP, any non-foreground tab). Anything driven by `setAnimationLoop`/rAF — physics stepping, drag-accumulator consumption, scrubbed poses — barely advances, so state read right after an interaction looks frozen: "accumulator never consumed", "object stuck at spawn height", "drag does nothing". Pump frames manually around every interaction and state read:
  ```js
  const pump = async n => { for (let i = 0; i < n; i++) await new Promise(r => requestAnimationFrame(r)) }
  await pump(10)          // before reading any per-frame state
  ```
  Screenshots paint on demand and are unaffected — a page can screenshot perfectly while its loop is starved. Diagnostic that settles it in one step: read a frame counter twice with a wait between; if it advanced ~5 frames in a second, you're throttled, not broken.
- **Dispatch synthetic events on the element that owns the listener.** Listeners registered on a container (`stage.addEventListener('pointermove', …)`) never see events dispatched on `window` or `document` — events propagate up, not down. A drag simulated as `window.dispatchEvent(pointermove)` silently does nothing and reads as "drag is broken".
- **Read the state gates before judging an interaction dead.** Interactions guarded by thresholds (`physics.blend < 0.5`, `drawProgress > 0.98`) will correctly ignore input when the gate is closed — a probe fired at the wrong scroll position reports failure against working code. Read the gate values in the same probe that dispatches the events.
- **`setPointerCapture` throws `NotFoundError` on synthetic pointerIds** (no active pointer). Harmless for real users; in tests either use the automation tool's real mouse, or expect and ignore this error.
- **Expose a debug handle and make claims numeric** (`window.__dbg = { state: () => ({...}) }`). "The cursor shoves the hero" should be "heroPos.x moved 0.02 → 1.19". Numeric before/after pairs are also what catches the throttle trap: an unchanged number prompts "is the loop ticking?" where a vague look at a screenshot doesn't.
- **The automation browser's GPU process degrades after ~15 WebGL context creations, and then reports ~1 fps for everything.** (Playwright MCP, Chromium, RTX 5080 host.) A build that measured 165 fps read 1.1 fps an hour later, and a shader was nearly rewritten to chase it. The diagnostic that settles it in one step: **hide the subject and re-measure.** If an empty scene is also 1 fps, it is the browser, not your code — close the page and relaunch. Every page reload that constructs a renderer, a PMREM generator or a path-tracer target leaks toward this, so a long verification session will hit it.
- **Check the shape of your assertion before believing a `false`.** `el.style.backgroundImage.startsWith('url(data:image/png')` reports false for a correctly applied image, because browsers normalise the property to `url("data:image/png...")` with quotes. Two minutes were spent on working code. Assert with `includes()` on a distinctive substring, or print the value before judging it.
- **`gl.finish()` does not drain the pipeline under ANGLE/D3D11.** A synchronous timing probe built on it reported **0.3 ms** for a full-resolution path-traced sample. It happened to classify a fast GPU correctly and would have waved a slow one straight through — which defeats the entire point of a capability gate. Time *observed throughput over real rAF frames* instead (samples or frames per second across ~700 ms); wall-clock throughput cannot be fooled this way.
- **`preserveDrawingBuffer: true` is not a free way to enable `readPixels`.** It took a render loop from 95 rAF/s to **1 rAF/s** at 2560x1249, because it forces a full-framebuffer copy every frame. The measurement instrument destroyed the thing it measured. Read pixels inside the same rAF callback as the draw instead, where the buffer is still intact, and leave the flag off.
- Verdict discipline: a failing probe is evidence about *either* the page or the probe. Before editing app code, confirm (1) the render loop is actually ticking and (2) the event actually reached the handler (one `console.log` or counter). Two frontier-model sessions each burned two false diagnoses by skipping exactly this.

## Render-loop JS traps (from the Veredmor build)

- **A `let` declared after `frame()` is called throws on every single frame.** The loop is started as soon as it is defined, so any `let`/`const` the loop body closes over must be declared *above* the `frame()` call — function declarations hoist, bindings do not. The symptom is a flood of identical `ReferenceError: Cannot access 'x' before initialization`, one per frame, with the page otherwise rendering. Bit the same build twice, in two different files.
- **Backticks inside a GLSL comment terminate the JS template literal holding the shader.** `// \`frame\` is a parameter...` inside a `` /* glsl */`...` `` string closed the string and produced `SyntaxError: Unexpected identifier 'frame'` far from the real cause. Never use backticks in shader comments; put a "no backticks in this block" note at the top of any injected GLSL.
- **`THREE.Sphere` has `.center` and `.radius`, not `getCenter()`.** (`Box3` has `getCenter()`, `Sphere` does not.) Trivial, but it throws at runtime inside a per-frame path where it is annoying to spot.
- **Uniforms added to a `ShaderMaterial` after construction still bind**, provided the shader declares them and you set `needsUpdate`. Useful for patching a third-party material: you can inject GLSL into `material.fragmentShader` as a string and add matching uniforms, without forking the library. Verify the patch actually matched — a string replace that silently hit nothing looks exactly like a working build with the feature switched off, so make the patch *throw* when an anchor is missing.

## GLTF asset traps (from the Sunder build)

- **Three's GLTFLoader sanitizes node names** (spaces, dots, colons stripped: `nc mic.001_4` → `ncmic001_4`). Never match loaded nodes by their original GLTF names — match by a stable suffix pattern (`/_(\d+)$/`) or traverse indices.
- **"Assembled-looking" Sketchfab scenes are often flat-packed multi-copy part layouts** (product-viz models especially). Inspect the scene graph and render each part-group before committing to an asset — and before hand-rigging an assembly, check whether the "exploded" layout is itself usable as a pose (assembled↔exploded interpolation made Sunder's signature interaction).
- When node-name groups and spatial clusters disagree, trust world-space bounds (`getBounds` in @gltf-transform, or `Box3.setFromObject` after `updateMatrixWorld(true)`); baked leaf `matrix` transforms make accessor min/max alone meaningless.
- `gltf-transform optimize` runs `join`/`flatten`, which merges the per-part meshes a rig needs. Use individual `weld` + `quantize` + `resize` + `webp` commands instead — all natively decodable by three (KHR_mesh_quantization, EXT_texture_webp), no decoder setup.

## Console warnings that are NOT bugs (do not chase these)

| Warning | Source | Action |
|---|---|---|
| `THREE.Clock: This module has been deprecated` | R3F internals on Three 0.184+ | Ignore |
| `THREE.WebGLProgram: Program Info Log: X4122` | ANGLE/HLSL precision on Windows | Ignore |
| `Texture is not power of two` | GLTF textures, WebGL2 handles it | Ignore |

Rule: if the build passes and the visual is correct, warnings from Three.js/R3F internals are not actionable. Only fix warnings originating in application-authored shaders/components.

## Testing

- Playwright `webServer` on Windows: use port 3001+, not 3000.
- Add `exclude: ['**/e2e/**']` to `vitest.config.ts` or Vitest picks up Playwright's `test.describe` and fails.

## Design failures (the expensive kind)

These don't error — they just make the result look AI-generated. All are hard bans in SKILL.md; repeated here because they recur:

- Dark page + neon accent when the brief said "like Lusion" (lusion.co is light; oryzo.ai is warm dark, not cool dark).
- Bloom or particle clouds added to a product scene "for atmosphere" — snow-globe effect, broken-TV glow.
- Multiple light sources on a glossy/refractive object — muddy speculars. One key light.
- Warm amber light on platinum/glass/white plastic — reads as wrong material, not mood.
- Particle radius 2–3 units around a ~2-unit hero — wraps it like a shell. Use 6–8.
- Procedural geometry for a recognizable real-world object — spotted as fake in under a second. Use a real GLTF.
- 50/50 text/object grid — collisions as the camera moves. Fixed text rail, or center-pinned object with text behind.
- Elastic/bounce easing, gradient text, glassmorphism-everywhere, em dashes in copy, three identical feature cards.
- **Building the dark-page version of a brief whose own design doc specified a light page.** On the Veredmor build the art direction was already written down ("a light page with a dark viewing box, not a dark page") and the first full implementation was dark everywhere with a cool blue accent - the #1 hard ban - because the 3D chapter had been built first and the shell inherited the canvas's background. Re-read the project's own design doc before styling the shell, and if the brief has a `DESIGN.md`, treat it as more authoritative than the preset.
- **Overexposure erases hue, so "make it brighter" and "make it more colourful" are opposing controls.** A clipped channel cannot carry a colour. On a dispersive object this is brutal: raising the environment exposure from 0.12 to 1.0 took clipping from 0.1% to 15% and cut the strongly-coloured pixels from 2.2% to 0.2%. Whenever a scene has a colour that comes from physics rather than from a texture, sweep exposure against *both* a clipping count and a saturation count before choosing - the visually "brightest" setting is usually several stops past the most beautiful one.
- **A smooth bright environment makes a faceted object read as grey mush.** Sparkle is extreme LOCAL contrast - a mosaic of near-black and near-white facets side by side - so the environment needs structure and real darkness, not more light. Bright bands with deliberate dark gaps between them took the coloured-pixel share of one build from 1.78% to 6.13% before exposure was touched at all, and lifted the luma standard deviation to ~60. Extra sources cost nothing: it is the same single texture lookup.
