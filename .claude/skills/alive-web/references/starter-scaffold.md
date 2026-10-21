# Starter Scaffold — known-good runnable baseline (Preset A)

Purpose: **do not start from a blank file.** Copy these three files verbatim, serve them, confirm the physics hero works, and only then extend chapter by chapter. Every version below is pinned and the loading strategy is deliberately boring (UMD globals for GSAP/Lenis, import map only for Three/Rapier) because it works first-try — ES-module CDN interop for GSAP plugins is flaky and not worth debugging.

This scaffold delivers: the STUDIO shell (paper/ink/cobalt tokens, two-scale typography, registration marks, pill buttons), a panel-framed canvas, Rapier physics jacks that fall in under gravity and are shoved by the cursor, the Lenis+ScrollTrigger bridge, a masked SplitText headline reveal, and magnetic buttons. Extend it using the other reference files.

Serve with `python -m http.server 3001` (never `file://`).

## index.html

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Studio</title>
<link rel="stylesheet" href="styles.css">
<!-- GSAP + plugins as UMD globals (all plugins free since gsap 3.13).
     SRI hashes verified against these exact pinned files — do not change a version
     without recomputing its hash (curl the file, openssl dgst -sha384 -binary | openssl base64 -A) -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"
        integrity="sha384-HOvlOYPIs/zjoIkWUGXkVmXsjr8GuZLV+Q+rcPwmJOVZVpvTSXQChiN4t9Euv9Vc" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js"
        integrity="sha384-P8VzCVnT9NBUkMrpcIZrJbA7EBjJvh/fJS6PmP+4nLIM284DtsImIv8D0fFjIkeh" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/SplitText.min.js"
        integrity="sha384-xb96EMJeax+NLXMC88ZBa1xAeAW+kn+horHh/zFlbMLG2UPWhMJJSlv7fi57hS+Q" crossorigin="anonymous"></script>
<!-- Lenis as UMD global -->
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.14/dist/lenis.min.js"
        integrity="sha384-O55L/6rhHr9CFvrxqv5luxOCcmVaBmETbZbJDP+Do8T0pztTACsFBD/IXCNkj7DV" crossorigin="anonymous"></script>
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/",
    "@dimforge/rapier3d-compat": "https://cdn.jsdelivr.net/npm/@dimforge/rapier3d-compat@0.14.0/+esm"
  }
}
</script>
</head>
<body>
  <header class="nav">
    <a class="wordmark" href="#">STUDIO</a>
    <p class="nav-statement">We create 3D visual storytelling and interactive web experiences that help brands stand out</p>
    <div class="nav-actions">
      <button class="pill" data-magnetic>LET'S TALK <span class="dot">·</span></button>
      <button class="pill" data-magnetic>MENU <span class="dot">··</span></button>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="hero-panel">
        <canvas id="hero-canvas"></canvas>
        <span class="mark tl">+</span><span class="mark tr">+</span>
        <span class="mark bl">+</span><span class="mark br">+</span>
      </div>
      <p class="scroll-cue">SCROLL TO EXPLORE</p>
    </section>

    <section class="work">
      <div class="section-head">
        <h2 class="display" data-split>Featured Work</h2>
        <p class="annotation">A SELECTION OF IMMERSIVE DIGITAL EXPERIENCES CREATED FOR AMBITIOUS BRANDS AND FORWARD THINKING TEAMS.</p>
      </div>
      <div class="card-grid">
        <article class="card"><div class="card-media"></div><h3>Project One</h3><p class="annotation">INTERACTIVE 3D · 2026</p></article>
        <article class="card"><div class="card-media"></div><h3>Project Two</h3><p class="annotation">WEBGL EXPERIENCE · 2026</p></article>
      </div>
    </section>

    <footer class="footer">
      <h2 class="display" data-split>Let's build something alive</h2>
      <button class="pill" data-magnetic>START A PROJECT <span class="dot">·</span></button>
    </footer>
  </main>

  <script type="module" src="app.js"></script>
</body>
</html>
```

## styles.css

```css
:root {
  --paper:  oklch(95% 0.01 285);
  --ink:    oklch(18% 0.012 280);
  --panel:  oklch(14% 0.012 265);
  --accent: oklch(50% 0.28 265);
  --radius-panel: 24px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { background: var(--paper); }
body {
  font-family: Inter, 'Neue Montreal', Archivo, system-ui, sans-serif;
  color: var(--ink); background: var(--paper);
  -webkit-font-smoothing: antialiased;
}

/* two-scale typography: huge sentence-case display vs tiny caps utility */
.display { font-size: clamp(48px, 9vw, 130px); font-weight: 400; line-height: 1.02; letter-spacing: -0.02em; }
.annotation, .scroll-cue, .pill { font-size: 11px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; }
.annotation { max-width: 26ch; opacity: 0.75; line-height: 1.6; }

.nav { display: flex; align-items: flex-start; justify-content: space-between; gap: 24px; padding: 28px 44px; }
.wordmark { font-size: 20px; font-weight: 500; letter-spacing: 0.28em; color: var(--ink); text-decoration: none; }
.nav-statement { font-size: clamp(18px, 2vw, 26px); font-weight: 400; max-width: 34ch; line-height: 1.3; }
.nav-actions { display: flex; gap: 10px; }
.pill {
  background: var(--ink); color: var(--paper); border: 0; cursor: pointer;
  padding: 14px 22px; border-radius: 999px; display: inline-flex; gap: 8px; align-items: center;
}
.pill .dot { color: var(--accent); }

.hero { padding: 8px 44px 0; }
.hero-panel {
  position: relative; height: calc(100vh - 160px); min-height: 480px;
  background: var(--panel); border-radius: var(--radius-panel); overflow: hidden;
}
#hero-canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
.mark { position: absolute; font-size: 13px; opacity: 0.55; color: var(--ink); }
.hero-panel .mark { color: var(--paper); z-index: 2; }
.mark.tl { top: 10px; left: 12px; } .mark.tr { top: 10px; right: 12px; }
.mark.bl { bottom: 8px; left: 12px; } .mark.br { bottom: 8px; right: 12px; }
.scroll-cue { text-align: center; padding: 18px 0 8px; opacity: 0.6; }

.work { padding: 26vh 44px 10vh; }
.section-head { display: flex; justify-content: space-between; align-items: flex-end; gap: 32px; margin-bottom: 8vh; }
.card-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 28px; }
.card-media { height: 52vh; background: var(--panel); border-radius: var(--radius-panel); margin-bottom: 16px; }
.card h3 { font-size: 22px; font-weight: 400; margin-bottom: 6px; }

.footer { padding: 24vh 44px 16vh; display: grid; gap: 40px; justify-items: start; }

/* SplitText mask — lines rise out of overflow-hidden wrappers */
.split-line { overflow: hidden; }
@media (max-width: 760px) {
  .nav-statement { display: none; }
  .card-grid { grid-template-columns: 1fr; }
}
```

## app.js

```javascript
import * as THREE from 'three'
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js'
import RAPIER from '@dimforge/rapier3d-compat'

/* gsap, ScrollTrigger, SplitText, Lenis are UMD globals from index.html */
gsap.registerPlugin(ScrollTrigger, SplitText)

/* ---------- 1. smooth scroll bridge (mandatory, exactly this) ---------- */
const lenis = new Lenis({ lerp: 0.1, smoothWheel: true })
lenis.on('scroll', ScrollTrigger.update)
gsap.ticker.add(t => lenis.raf(t * 1000))
gsap.ticker.lagSmoothing(0)
let scrollVel = 0
lenis.on('scroll', e => { scrollVel = e.velocity })

/* ---------- 2. renderer inside the panel ---------- */
const panel = document.querySelector('.hero-panel')
const canvas = document.getElementById('hero-canvas')
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true })
renderer.setPixelRatio(Math.min(devicePixelRatio, 2))
renderer.toneMapping = THREE.ACESFilmicToneMapping
const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 60)
camera.position.z = 10

function resize() {
  const w = panel.clientWidth, h = panel.clientHeight
  renderer.setSize(w, h)
  camera.aspect = w / h
  camera.updateProjectionMatrix()
}
new ResizeObserver(resize).observe(panel)
resize()

/* soft studio environment (cool key light) — no external HDR file */
;(function env() {
  const W = 256, H = 128, data = new Float32Array(W * H * 4)
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = (y * W + x) * 4, fy = y / H, fx = (x / W) * Math.PI * 2
    let r = 0.08, g = 0.10, b = 0.15
    const kl = Math.max(0, -Math.sin(fx - 2.2) * (1 - fy * 1.5))
    r += kl * 4.0; g += kl * 4.2; b += kl * 5.0
    const top = Math.max(0, 1 - fy * 2.5)
    r += top * 0.6; g += top * 0.7; b += top * 1.0
    data[i] = r; data[i+1] = g; data[i+2] = b; data[i+3] = 1
  }
  const tex = new THREE.DataTexture(data, W, H, THREE.RGBAFormat, THREE.FloatType)
  tex.mapping = THREE.EquirectangularReflectionMapping
  tex.needsUpdate = true
  const pmrem = new THREE.PMREMGenerator(renderer)
  scene.environment = pmrem.fromEquirectangular(tex).texture
  tex.dispose(); pmrem.dispose()
})()

/* ---------- 3. physics hero: jacks fall in, cursor shoves them ---------- */
const jacks = []
let world = null, mouseBody = null
const COLORS = [0xffffff, 0x141519, 0x2430e8]  // white / ink / cobalt ONLY

function jackMesh(color) {
  const g = new THREE.Group()
  const geo = new RoundedBoxGeometry(1.7, 0.5, 0.5, 4, 0.16)
  const mat = new THREE.MeshPhysicalMaterial({
    color, metalness: 0, roughness: 0.22, clearcoat: 1, clearcoatRoughness: 0.06, envMapIntensity: 1.4,
  })
  const a = new THREE.Mesh(geo, mat)
  const b = new THREE.Mesh(geo, mat); b.rotation.z = Math.PI / 2
  const c = new THREE.Mesh(geo, mat); c.rotation.y = Math.PI / 2
  g.add(a, b, c)
  return g
}

RAPIER.init().then(() => {
  world = new RAPIER.World({ x: 0, y: -3.5, z: 0 })

  // container walls sized from the camera frustum at z=0
  const halfH = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * camera.position.z
  const halfW = halfH * camera.aspect
  const wall = (hx, hy, hz, x, y, z) =>
    world.createCollider(RAPIER.ColliderDesc.cuboid(hx, hy, hz).setTranslation(x, y, z))
  wall(halfW, 0.5, 3,  0, -halfH - 0.5, 0)
  // lid must clear the ENTIRE spawn stack (max spawn y = halfH + 1.5 + 11*1.6 = halfH + 19.1).
  // At halfH + 0.5 it caps the box below the spawn points and the jacks pile up ON it —
  // symptom: an empty panel with one stone peeking in at the top edge, no console error.
  wall(halfW, 0.5, 3,  0,  halfH + 22, 0)
  wall(0.5, halfH, 3, -halfW - 0.5, 0, 0)
  wall(0.5, halfH, 3,  halfW + 0.5, 0, 0)
  wall(halfW, halfH, 0.5, 0, 0, -1.8)
  wall(halfW, halfH, 0.5, 0, 0,  1.8)

  // spawn ABOVE the frustum — gravity is the entrance animation
  for (let i = 0; i < 12; i++) {
    const mesh = jackMesh(COLORS[i % 3])
    scene.add(mesh)
    const body = world.createRigidBody(
      RAPIER.RigidBodyDesc.dynamic()
        .setTranslation((Math.random() - 0.5) * halfW * 1.4, halfH + 1.5 + i * 1.6, (Math.random() - 0.5) * 1.5)
        .setRotation(new THREE.Quaternion().random())
        .setLinearDamping(0.5).setAngularDamping(0.7)
    )
    const arm = (rx, ry, rz) => {
      const q = new THREE.Quaternion().setFromEuler(new THREE.Euler(rx, ry, rz))
      world.createCollider(
        RAPIER.ColliderDesc.roundCuboid(0.69, 0.09, 0.09, 0.16)
          .setRotation({ x: q.x, y: q.y, z: q.z, w: q.w })
          .setRestitution(0.35).setFriction(0.8),
        body)
    }
    arm(0, 0, 0); arm(0, 0, Math.PI / 2); arm(0, Math.PI / 2, 0)
    jacks.push({ mesh, body })
  }

  // the cursor is a physical object in the world
  mouseBody = world.createRigidBody(RAPIER.RigidBodyDesc.kinematicPositionBased())
  world.createCollider(RAPIER.ColliderDesc.ball(0.7), mouseBody)
})

/* pointer → panel-relative NDC → world point on the z=0 plane */
const ndc = new THREE.Vector2(-9, -9)
const ray = new THREE.Raycaster()
const planeZ0 = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0)
const mouseWorld = new THREE.Vector3(9999, 9999, 0)
window.addEventListener('pointermove', e => {
  const r = panel.getBoundingClientRect()
  ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1)
})

/* ---------- 4. render loop ---------- */
const clock = new THREE.Clock()
renderer.setAnimationLoop(() => {
  const dt = Math.min(clock.getDelta(), 1 / 30)
  if (world) {
    ray.setFromCamera(ndc, camera)
    if (ray.ray.intersectPlane(planeZ0, mouseWorld) && mouseBody)
      mouseBody.setNextKinematicTranslation({ x: mouseWorld.x, y: mouseWorld.y, z: 0 })
    // scroll physically stirs the pile
    if (Math.abs(scrollVel) > 2)
      for (const { body } of jacks)
        body.applyImpulse({ x: 0, y: -scrollVel * 0.002, z: 0 }, true)
    world.timestep = dt
    world.step()
    for (const { mesh, body } of jacks) {
      mesh.position.copy(body.translation())
      mesh.quaternion.copy(body.rotation())
    }
  }
  renderer.render(scene, camera)
})

/* ---------- 5. masked headline reveals ---------- */
document.querySelectorAll('[data-split]').forEach(el => {
  const split = new SplitText(el, { type: 'lines', linesClass: 'split-line-inner' })
  split.lines.forEach(line => {
    const wrap = document.createElement('div')
    wrap.className = 'split-line'
    line.parentNode.insertBefore(wrap, line)
    wrap.appendChild(line)
  })
  gsap.from(split.lines, {
    yPercent: 110, duration: 0.9, ease: 'power4.out', stagger: 0.08,
    scrollTrigger: { trigger: el, start: 'top 82%' },
  })
})

/* ---------- 6. magnetic buttons ---------- */
document.querySelectorAll('[data-magnetic]').forEach(el => {
  el.addEventListener('pointermove', e => {
    const r = el.getBoundingClientRect()
    const dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2)
    gsap.to(el, { x: dx * 0.3, y: dy * 0.3, duration: 0.3, ease: 'power2.out' })
  })
  el.addEventListener('pointerleave', () =>
    gsap.to(el, { x: 0, y: 0, duration: 0.6, ease: 'power4.out' }))
})
```

## Acceptance test before extending

Serve and check, in order:
1. Page is pale lavender with a dark rounded hero panel and `+` marks — not a dark page.
2. Within ~2s, 12 glossy jacks (white/black/cobalt) fall into the panel, collide, and settle. Verify with numbers, not just the screenshot: all 12 body `y` values should end below `halfH`. If they park just above it, the lid is too low (see the ceiling comment).
3. Moving the cursor through the pile shoves objects; fast flicks send them flying.
4. Fast scroll visibly stirs the pile.
5. Headlines rise out of a mask when scrolled into view; pill buttons stick to the cursor.

If any check fails, fix it before adding anything (consult `pitfalls.md`). All five passing = the baseline is award-grade; now extend: replace card-media placeholders with real media, add chapters per `flow-choreography.md`, add a scrubbed camera or second scene per `motion-recipes.md`.

## Adapting the scaffold

- **Preset B (product story)**: keep app.js structure but swap the shell (warm void tokens, full-bleed fixed canvas instead of a panel), replace the jacks with one GLTF hero (`webgl-recipes.md` §8), and drive chapters from the map in `flow-choreography.md` §1. The Lenis bridge, env, resize, and pointer plumbing transfer unchanged.
- **React/Next**: same logic inside one `useEffect` with the cleanup pattern from `pitfalls.md`; or keep it vanilla in a route-level component. The physics/render loop code is framework-agnostic by design (plain objects, no state).
- **npm instead of CDN**: `npm i three@0.170.0 gsap@3.13.0 lenis@1.1.14 @dimforge/rapier3d-compat@0.14.0` — the three/rapier imports keep the same specifiers; delete the UMD `<script>` tags and the import map, and instead import the globals at the top of app.js: `import gsap from 'gsap'`, `import { ScrollTrigger } from 'gsap/ScrollTrigger'`, `import { SplitText } from 'gsap/SplitText'`, `import Lenis from 'lenis'`.
