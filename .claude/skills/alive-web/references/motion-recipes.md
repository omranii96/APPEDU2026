# Motion Recipes — scroll, camera, cursor, text, transitions

Read this at Step 3 (scroll choreography). Motion character everywhere: weighted and intentional. `scrub ≥ 1`, exponential ease-outs, lerped followers. Nothing snaps.

## Contents
1. Lenis + GSAP bridge (the foundation)
2. Camera as storyteller (scrubbed timeline)
3. Text-behind-object layering (Oryzo signature)
4. Pinned chapters
5. Camera position vs. text layout
6. Scroll velocity → shader/tilt
7. Scroll-driven object tilt
8. Cinematic hold (section scroll pause)
9. Magnetic cursor
10. Typography that moves (SplitText)
11. 3D → screen label projection
12. Layered zoom / depth reveal
13. Page transitions (Barba + Flip)

---

## 1. Lenis + GSAP bridge

Without smooth scroll every scrubbed animation feels mechanical. Wire this first.

```javascript
import Lenis from 'lenis'   // NOT '@studio-freight/lenis' — deprecated alias
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
gsap.registerPlugin(ScrollTrigger)

const lenis = new Lenis({ lerp: 0.1, smoothWheel: true })  // 0.05 floaty · 0.15 snappy
lenis.on('scroll', ScrollTrigger.update)
gsap.ticker.add((t) => lenis.raf(t * 1000))
gsap.ticker.lagSmoothing(0)
```

(GSAP Club alternative: `ScrollSmoother.create({ smooth: 4, effects: true })` enables `data-speed`/`data-lag` parallax attributes in plain HTML.)

## 2. Camera as storyteller

Map the camera path to scroll progress via a mutable plain object (works identically in vanilla and R3F — no React re-renders):

```javascript
const cam = { x: 0, y: 0, z: 8 }
const look = { x: 0, y: 0, z: 0 }

gsap.timeline({
  scrollTrigger: { trigger: '#page', start: 'top top', end: 'bottom bottom', scrub: 1.5 }
})
.to(cam, { z: 3, y: 1.5, duration: 1, ease: 'none' })
.to(cam, { x: -1.8, z: 5, duration: 2, ease: 'none' })
.to(cam, { x: 0, y: 0, z: 8, duration: 1, ease: 'none' })

// render loop
camera.position.set(cam.x, cam.y, cam.z)
camera.lookAt(look.x, look.y, look.z)
```

Inside a scrubbed timeline use `ease: 'none'` — the scrub lag IS the easing. Segment `duration`s are relative weights (a duration-2 segment spans twice the scroll distance of a duration-1).

## 3. Text-behind-object layering (Oryzo signature)

Giant display text slides behind the pinned 3D object. Three stacked layers:

```
z-index 1: .display-text-back   (the giant cream headline, position: fixed)
z-index 2: #webgl-canvas        (transparent background, alpha: true)
z-index 3: .kickers-and-ui      (small caps labels, nav, scroll cue)
```

Translate the back-layer text horizontally with a scrubbed tween so headline fragments drift through as chapters change. Because the canvas is transparent, the object naturally occludes the text — no masking needed. Keep back-layer text `pointer-events: none`.

## 4. Pinned chapters

```javascript
gsap.timeline({
  scrollTrigger: { trigger: '#chapter-2', pin: true, start: 'top top', end: '+=150%', scrub: 1 }
})
.to(cam, { z: 2, ease: 'none' })
.fromTo('#chapter-2 .headline', { yPercent: 120 }, { yPercent: -120, ease: 'none' }, 0)
```

Preset B pages are mostly pinned chapters back-to-back — total scroll length 10–20× viewport height. Horizontal card carousel = pinned section + `x` tween on a wide flex track:

```javascript
gsap.to('.track', {
  x: () => -(track.scrollWidth - window.innerWidth),
  ease: 'none',
  scrollTrigger: { trigger: '#carousel', pin: true, start: 'top top', end: '+=250%', scrub: 1 }
})
```

## 5. Camera position vs. text layout

A perspective camera shifts apparent object position *opposite* to its own movement: `cam.x` negative → object appears RIGHT of viewport center. Decide the eye-space split before writing the camera path:

- Text rail fixed to the left 40–45vw (`max-width: 45vw; padding-left: 8vw`), object held in the right half (`cam.x` stays negative through content sections), **or**
- Object pinned dead-center with text passing behind/around it (Preset B).

Never a 50/50 grid where text and object compete for the same space — they will collide as the camera moves.

## 6. Scroll velocity → shader / motion

```javascript
let lastY = 0, vel = 0
// in the render loop, not a scroll listener:
vel += ((window.scrollY - lastY) - vel) * 0.1   // smooth in
lastY = window.scrollY
vel *= 0.85                                      // decay
material.uniforms.uScrollVelocity.value = vel
```

Feed it to the UV-warp shader (webgl-recipes.md §4), particle turbulence, or object lean. Velocity-reactive motion is what makes fast scrolling feel like dragging a physical world.

## 7. Scroll-driven object tilt

Tilt attitudes per chapter via a scrubbed timeline, applied with a lerp so it lands softly:

```javascript
const dTilt = { x: 0, z: 0 }
gsap.timeline({ scrollTrigger: { trigger: '#page', start: 'top top', end: 'bottom bottom', scrub: 2 } })
  .to(dTilt, { x: 0.35, z: 0.12, duration: 0.15, ease: 'none' }, 0.0)
  .to(dTilt, { x: -0.28, z: -0.18, duration: 0.15, ease: 'none' }, 0.2)
  .to(dTilt, { x: 0, z: 0, duration: 0.2, ease: 'none' }, 0.8)

gsap.ticker.add(() => {
  hero.rotation.x += (dTilt.x - hero.rotation.x) * 0.08
  hero.rotation.z += (dTilt.z - hero.rotation.z) * 0.08
})
// idle Y-rotation stays in the render loop: hero.rotation.y += 0.003
```

Keep tilts under ±0.5 rad — beyond that reads as tumbling.

## 8. Cinematic hold (section scroll pause)

Pause scroll ~1s when a chapter enters so its entrance animation lands — the film-cut breathing room. Scroll-down only; pausing on scroll-up breaks the user's mental model.

```javascript
let lock = false
function hold(ms = 1000) {
  if (lock) return
  lock = true
  lenis.stop()
  setTimeout(() => { lenis.start(); lock = false }, ms)
}
sections.forEach(id => ScrollTrigger.create({
  trigger: id, start: 'top 8%',
  onEnter: () => { hold(1000); playEntranceTimeline(id) },  // no onEnterBack
}))
```

800ms subtle · 1000ms standard · 1200ms only for hero→first-chapter. Use sparingly (Preset B chapters, major reveals) — every section pausing gets annoying.

## 9. Magnetic cursor

```javascript
const xTo = gsap.quickTo('.cursor', 'x', { duration: 0.4, ease: 'power3' })
const yTo = gsap.quickTo('.cursor', 'y', { duration: 0.4, ease: 'power3' })
window.addEventListener('mousemove', e => { xTo(e.clientX); yTo(e.clientY) })

function addMagnetic(el) {
  el.addEventListener('mousemove', e => {
    const r = el.getBoundingClientRect()
    const dx = e.clientX - (r.left + r.width / 2)
    const dy = e.clientY - (r.top + r.height / 2)
    const t = Math.max(r.width, r.height) * 0.7
    const dist = Math.hypot(dx, dy)
    if (dist < t) {
      const f = (1 - dist / t) * 0.4
      gsap.to(el, { x: dx * f, y: dy * f, duration: 0.3, ease: 'power2.out' })
    }
  })
  el.addEventListener('mouseleave', () =>
    gsap.to(el, { x: 0, y: 0, duration: 0.6, ease: 'power4.out' }))
}
```

Apply to pill buttons and nav links only — not to every element. Hide the custom cursor on touch devices.

## 10. Typography that moves

```javascript
import { SplitText } from 'gsap/SplitText'
const split = new SplitText(heading, { type: 'chars,words' })
gsap.from(split.chars, {
  yPercent: 110, opacity: 0,
  stagger: { amount: 0.4 }, ease: 'power4.out', duration: 0.8,
  scrollTrigger: { trigger: heading, start: 'top 80%' },
})
```

Wrap lines in `overflow: hidden` containers so characters rise from a mask — the reveal reads as print-quality, not "fade in". Big display headlines in Preset B also parallax at `data-speed`-style rates slightly different from body copy, giving the page depth without 3D.

## 11. 3D → screen label projection

Floating annotation chips that track a 3D object (Preset B spec callouts):

```javascript
const wp = new THREE.Vector3()
function updateLabel(mesh, el, ox = 100, oy = -50) {
  mesh.getWorldPosition(wp)
  const s = wp.clone().project(camera)
  el.style.left = ((s.x * 0.5 + 0.5) * innerWidth + ox) + 'px'
  el.style.top  = ((-s.y * 0.5 + 0.5) * innerHeight + oy) + 'px'
}
// call in the render loop AFTER camera position is applied
```

Style chips in the utility layer: 10px caps, 1px accent border, pill radius, `background: color-mix(in oklch, var(--void) 75%, transparent)`, `backdrop-filter: blur(8px)`, `pointer-events: none`. Toggle opacity per chapter with ScrollTrigger `onEnter`/`onLeave`.

## 12. Layered zoom / depth reveal

Stacked copies at different scales rush forward on scroll — cheap Z-depth without WebGL:

```javascript
gsap.timeline({ scrollTrigger: { trigger: sec, start: 'top top', end: 'bottom top', scrub: true, pin: true } })
  .to(layers, { scale: 1, ease: 'none', stagger: { amount: 0.4, from: 'end' } }, 0)
  .to(layers, { filter: 'blur(0px)', ease: 'none', stagger: { amount: 0.3, from: 'end' } }, 0.1)
```

## 13. Page transitions (Barba + Flip)

```javascript
import barba from '@barba/core'
import { Flip } from 'gsap/Flip'
let flipState
barba.init({ transitions: [{
  async leave({ current }) {
    flipState = Flip.getState('.hero-media')
    await gsap.to(current.container, { opacity: 0, y: -30, duration: 0.4, ease: 'power2.in' })
  },
  enter({ next }) {
    Flip.from(flipState, { targets: '.hero-media', duration: 0.8, ease: 'power3.inOut' })
    return gsap.from(next.container, { opacity: 0, y: 30, duration: 0.6, ease: 'power2.out' })
  },
}]})
```

The shared element (work-card media → project hero) morphing across the navigation is what makes a multi-page site feel like one continuous experience. Re-init Lenis + ScrollTrigger after each Barba enter.
