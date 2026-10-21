# Interaction Recipes — physics heroes, cursor forces, the "never inert" rule

Read this whenever the scene should *react* to the user. This is half of what makes a site feel alive: on lusion.co the hero objects tumble under real gravity, collide, and get shoved around by your cursor. That is not an animation — it is a simulation the user participates in.

## Contents
1. The "never inert" rule
2. Real-physics hero (Rapier) — the lusion.co jacks
3. Cursor as a force field (physics version)
4. Cheap spring physics (no engine, < 20 objects)
5. Pointer parallax — the whole scene leans
6. Grab-and-throw (drag a 3D object)
7. 2D interactivity kit (for 2D chapters)
8. Performance budget

---

## 1. The "never inert" rule

At every scroll position, at least one thing on screen must respond to input. This is the invariant that separates award sites from scroll videos. Audit your page chapter by chapter:

- 3D chapters: cursor force field or pointer parallax, minimum.
- 2D text/carousel chapters: velocity skew, magnetic buttons, hover reveals, draggable track.
- Even loading/idle states: the hero keeps floating, breathing, or reacting.

If the user stops scrolling and wiggles the mouse and *nothing* moves, the chapter fails.

## 2. Real-physics hero (Rapier) — the lusion.co jacks

Use a real physics engine for the hero when objects should have weight: falling on load, colliding, settling, reacting to cursor and scroll. Rapier is the current standard (fast WASM, actively maintained). `npm i @dimforge/rapier3d-compat` or import map from esm.sh.

```javascript
import RAPIER from '@dimforge/rapier3d-compat'
await RAPIER.init()

// Toy gravity — softer than Earth so objects feel like light glossy plastic
const world = new RAPIER.World({ x: 0, y: -3.5, z: 0 })
```

**Plus/jack-shaped bodies** (lusion's hero objects) — one dynamic body, three rounded-box colliders crossed on the axes:

```javascript
function spawnJack(pos, mesh) {
  const body = world.createRigidBody(
    RAPIER.RigidBodyDesc.dynamic()
      .setTranslation(pos.x, pos.y, pos.z)
      .setLinearDamping(0.5)      // air resistance — settles instead of bouncing forever
      .setAngularDamping(0.7)
      .setCanSleep(true)
  )
  const arm = (rx, ry, rz) => {
    const q = new THREE.Quaternion().setFromEuler(new THREE.Euler(rx, ry, rz))
    world.createCollider(
      RAPIER.ColliderDesc.roundCuboid(0.42, 0.13, 0.13, 0.1)  // rounded = soft toy contact
        .setRotation({ x: q.x, y: q.y, z: q.z, w: q.w })
        .setRestitution(0.35).setFriction(0.8).setDensity(1),
      body)
  }
  arm(0, 0, 0); arm(0, 0, Math.PI / 2); arm(0, Math.PI / 2, 0)
  return { body, mesh }
}
```

**Invisible container** so objects stay inside the visible panel — size walls from the camera frustum at the objects' depth plane:

```javascript
const dist = camera.position.z            // objects live near z = 0
const halfH = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * dist
const halfW = halfH * camera.aspect
const wall = (hx, hy, hz, x, y, z) =>
  world.createCollider(RAPIER.ColliderDesc.cuboid(hx, hy, hz).setTranslation(x, y, z))
wall(halfW, 0.5, 2,  0, -halfH - 0.5, 0)   // floor
wall(halfW, 0.5, 2,  0,  halfH + 0.5, 0)   // ceiling (keeps cursor-flung objects in)
wall(0.5, halfH, 2, -halfW - 0.5, 0, 0)    // left
wall(0.5, halfH, 2,  halfW + 0.5, 0, 0)    // right
wall(halfW, halfH, 0.5, 0, 0, -1.6)        // back
wall(halfW, halfH, 0.5, 0, 0,  1.6)        // front glass
```

**Sync loop** — fixed timestep, then copy transforms to meshes:

```javascript
const clock = new THREE.Clock()
function tick() {
  world.timestep = Math.min(clock.getDelta(), 1 / 30)  // clamp: tab-switch spike protection
  world.step()
  for (const { body, mesh } of jacks) {
    mesh.position.copy(body.translation())
    mesh.quaternion.copy(body.rotation())
  }
  renderer.render(scene, camera)
  requestAnimationFrame(tick)
}
```

**Entrance**: spawn bodies above the frustum (`y = halfH + i * 1.2`) with slight random rotation and let them *fall in* on load — gravity is the entrance animation. Far better than tweening opacity.

**Scroll shake**: feed scroll velocity in as impulses so scrolling physically stirs the pile:

```javascript
// in the render loop, vel = smoothed scroll velocity (motion-recipes.md §6)
if (Math.abs(vel) > 2) {
  for (const { body } of jacks)
    body.applyImpulse({ x: 0, y: -vel * 0.004 * body.mass(), z: 0 }, true)
}
```

## 3. Cursor as a force field (physics version)

The cursor becomes an invisible kinematic ball inside the simulation — it *pushes* bodies on contact, exactly like lusion.co:

```javascript
const mouseBody = world.createRigidBody(RAPIER.RigidBodyDesc.kinematicPositionBased())
world.createCollider(RAPIER.ColliderDesc.ball(0.55), mouseBody)

const ndc = new THREE.Vector2(), ray = new THREE.Raycaster()
const planeZ0 = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0)
const pt = new THREE.Vector3()
window.addEventListener('pointermove', e => {
  ndc.set((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1)
})
// per frame, BEFORE world.step():
ray.setFromCamera(ndc, camera)
ray.ray.intersectPlane(planeZ0, pt)
mouseBody.setNextKinematicTranslation({ x: pt.x, y: pt.y, z: 0 })
```

Kinematic bodies transfer velocity through contacts, so fast mouse flicks send objects flying and slow movement nudges them — the interaction feels analog for free.

**Click burst** (optional): on `pointerdown`, apply a radial impulse from the click point:

```javascript
for (const { body } of jacks) {
  const d = new THREE.Vector3().copy(body.translation()).sub(pt)
  const dist = Math.max(d.length(), 0.4)
  if (dist < 3) body.applyImpulse(d.normalize().multiplyScalar(1.8 / dist), true)
}
```

## 4. Cheap spring physics (no engine, < 20 objects)

When you only need float + cursor repulsion (no collisions), skip the engine — per-object spring integration in plain JS:

```javascript
// each object: { mesh, home: Vector3, vel: Vector3 }
const toMouse = new THREE.Vector3()
function step(o, dt) {
  o.vel.addScaledVector(o.home.clone().sub(o.mesh.position), 2.0 * dt)  // spring home
  toMouse.copy(o.mesh.position).sub(mouseWorld)
  const d = toMouse.length()
  if (d < 1.6) o.vel.addScaledVector(toMouse.normalize(), (1 - d / 1.6) * 8 * dt) // repel
  o.vel.multiplyScalar(1 - 2.5 * dt)                                    // damping
  o.mesh.position.addScaledVector(o.vel, dt)
}
```

Add per-object idle drift (`home.y + sin(t * speed + phase) * 0.1`) so the field breathes when the cursor is away.

## 5. Pointer parallax — the whole scene leans

The minimum-viable 3D interactivity; costs nothing, apply to every 3D chapter:

```javascript
const lean = { x: 0, y: 0 }
window.addEventListener('pointermove', e => {
  lean.x = (e.clientX / innerWidth - 0.5)
  lean.y = (e.clientY / innerHeight - 0.5)
})
// render loop — lerped so it trails the cursor with weight
sceneGroup.rotation.y += (lean.x * 0.14 - sceneGroup.rotation.y) * 0.05
sceneGroup.rotation.x += (lean.y * 0.10 - sceneGroup.rotation.x) * 0.05
```

Rotate a wrapper group (or offset the camera), never the hero's own rotation — scroll choreography owns that.

## 6. Grab-and-throw (drag a 3D object)

For "play with the product" moments. Raycast on pointerdown, then drive the body kinematically while held; restore dynamic on release — release velocity gives a natural throw:

```javascript
let held = null, prev = new THREE.Vector3()
canvas.addEventListener('pointerdown', () => {
  ray.setFromCamera(ndc, camera)
  const hit = ray.intersectObjects(jackMeshes)[0]
  if (hit) {
    held = bodiesByMesh.get(hit.object)
    held.setBodyType(RAPIER.RigidBodyType.KinematicPositionBased, true)
  }
})
// per frame while held: (pt from the z-plane raycast in §3)
if (held) {
  held.setNextKinematicTranslation({ x: pt.x, y: pt.y, z: 0 })
}
canvas.addEventListener('pointerup', () => {
  if (!held) return
  held.setBodyType(RAPIER.RigidBodyType.Dynamic, true)
  const v = pt.clone().sub(prev).multiplyScalar(30)      // frame delta → throw velocity
  held.setLinvel({ x: v.x, y: v.y, z: 0 }, true)
  held = null
})
// end of frame: prev.copy(pt)
```

Set `cursor: grab / grabbing` and disable Lenis while dragging (`lenis.stop()` on grab, `start()` on release) so drag and scroll never fight.

## 7. 2D interactivity kit (for 2D chapters)

2D chapters must stay as alive as the 3D ones. Pick 2–3 per chapter:

- **Velocity skew** — cards/text shear with scroll speed: `gsap.set(els, { skewY: clamp(vel * 0.06, -6, 6) })` in the ticker, lerped back to 0. Instantly makes a plain list feel physical.
- **Magnetic buttons** — motion-recipes.md §9.
- **Draggable carousel** — the horizontal track from motion-recipes.md §4, plus pointer drag with inertia (GSAP `Draggable` + `InertiaPlugin`, or manual: track `dx`, apply as `xOffset`, decay by 0.95/frame). Scroll and drag write to the same offset value.
- **Hover tilt cards** — perspective tilt from pointer position: `rotateX/rotateY` up to 6°, `transform-style: preserve-3d`, lerped, with a `translateZ(20px)` child layer for depth.
- **Image reveal on hover** — media inside `overflow: hidden` rounded mask scales 1 → 1.06; a `clip-path: inset()` wipe on enter.
- **Text scramble / char stagger on hover** — nav links and buttons; SplitText chars `yPercent: -100` roll-over (duplicate line below rolls in).
- **Cursor image trail** — portfolio index rows spawn trailing thumbnails at the pointer (cap at ~6 live elements, fade+scale out).

## 8. Performance budget

- Rapier WASM is ~1.5MB — `RAPIER.init()` once, lazily, and only on pages that use it. Show the shell immediately; let physics arrive a beat later (objects falling in covers the wait).
- ≤ 40 dynamic bodies desktop, ≤ 15 mobile. Enable sleeping (default) — a settled pile costs almost nothing.
- One `world.step()` per frame with clamped timestep; never step in event handlers.
- Reuse `Vector3`/`Quaternion` temp objects in loops — zero allocations per frame.
- Touch devices: no cursor → substitute device-orientation tilt as the force input, or drive the force ball along a slow autonomous path so the pile still lives.
