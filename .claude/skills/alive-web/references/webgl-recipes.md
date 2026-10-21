# WebGL Recipes — renderer, materials, particles, post, assets

Read this at Step 2 (building the 3D scene). Everything here is palette-agnostic: colors always come from the art-direction preset chosen in SKILL.md Step 0.

## Contents
1. Renderer + canvas/scroll sync
2. Programmatic HDR environment (no external files)
3. PBR materials that feel precious
4. Shader displacement — living surfaces
5. GPGPU particles (only when the scene calls for them)
6. Particle field placement
7. Post-processing — one merged pass
8. Real GLTF assets (loading + normalization)
9. Pre-computed simulations (Houdini pattern)
10. Gems and refractive heroes (real dispersion, no path tracer)
11. CPU caustics from the same BVH

---

## 1. Renderer + canvas/scroll sync

```javascript
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true })
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
renderer.setSize(width, height)
renderer.toneMapping = THREE.ACESFilmicToneMapping
renderer.toneMappingExposure = 1.0
```

**Canvas positioning — pick ONE pattern:**

- `position: fixed` + **no transform** — canvas always fills the viewport (Preset B full-bleed stage, or a full-page background layer).
- `position: absolute` (full page height) + `translateY(scrollY)` re-applied each rAF — canvas tracks DOM elements exactly (Lusion's scroll-sync trick; use when 3D objects must stay glued to specific DOM sections). Add ~25% vertical padding to the render area to hide clipping during fast swipes.

```javascript
// absolute-canvas variant only:
function onRaf() {
  canvas.style.transform = `translateY(${window.scrollY}px)`
  renderScene()
  requestAnimationFrame(onRaf)
}
```

Never combine `position: fixed` with `translateY(scrollY)` — that pushes the canvas off-screen as the user scrolls (see pitfalls.md).

**Preset A panel canvases**: the canvas can simply be sized to its rounded panel (`position: absolute` inside the panel, `border-radius` inherited via `overflow: hidden` on the panel). One renderer per panel is fine for 1–2 panels; use a single fixed canvas + scissor rects if there are many.

## 2. Programmatic HDR environment

No external `.hdr`/`.exr` files — they add latency and 404 risk. Build the studio lighting in code. (`RoomEnvironment` is not importable in Three.js r151+; this replaces it.)

```javascript
function setupEnv(renderer, scene, { keyPhase = 2.2, warm = false } = {}) {
  const W = 512, H = 256
  const data = new Float32Array(W * H * 4)
  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const i = (y * W + x) * 4
      const fy = y / H
      const fx = (x / W) * Math.PI * 2
      // dark ambient base — tint warm for Preset B, cool for Preset A
      let r = warm ? 0.12 : 0.08, g = 0.10, b = warm ? 0.07 : 0.15
      // key light (position set by phase offset; 2.2 ≈ 10 o'clock)
      const kl = Math.max(0, -Math.sin(fx - keyPhase) * (1 - fy * 1.5))
      r += kl * 4.0; g += kl * 4.2; b += kl * (warm ? 3.2 : 5.0)
      // soft fill opposite
      const fl = Math.max(0, Math.sin(fx - 1.0) * (1 - fy * 2))
      r += fl * 1.8; g += fl * 1.4; b += fl * 0.8
      // top dome
      const top = Math.max(0, 1 - fy * 2.5)
      r += top * 0.6; g += top * 0.7; b += top * (warm ? 0.5 : 1.0)
      data[i] = r; data[i+1] = g; data[i+2] = b; data[i+3] = 1
    }
  }
  const tex = new THREE.DataTexture(data, W, H, THREE.RGBAFormat, THREE.FloatType)
  tex.mapping = THREE.EquirectangularReflectionMapping
  tex.needsUpdate = true
  const pmrem = new THREE.PMREMGenerator(renderer)
  pmrem.compileEquirectangularShader()
  scene.environment = pmrem.fromEquirectangular(tex).texture
  tex.dispose(); pmrem.dispose()
}
```

**Lighting discipline**: ONE key light. For precious-object visualization (product, gem, bottle) a single tight source gives one clean specular and controlled refractions; multiple sources give muddy randomness. Cool white (R×0.86 G×0.92 B×1.0) reads studio-professional; warm amber on metal/glass reads cheap — reserve warm light for Preset B's cork/wood/fabric world.

## 3. PBR materials that feel precious

```javascript
// Preset A glossy plastic (toy-like, lusion.co objects)
new THREE.MeshPhysicalMaterial({
  color: accentOrWhiteOrBlack,   // ONLY the preset's three colors
  metalness: 0, roughness: 0.22,
  clearcoat: 1, clearcoatRoughness: 0.06,
  envMapIntensity: 1.4,
})

// Glass / translucent hero object
new THREE.MeshPhysicalMaterial({
  color: 0xffffff, metalness: 0, roughness: 0.03,
  transmission: 0.92, thickness: 1.5, ior: 1.5,
  clearcoat: 1, clearcoatRoughness: 0, envMapIntensity: 3,
})
```

The luxury difference is material + environment + tone mapping, not effects. If the object looks flat, fix the env map and roughness before reaching for bloom (don't reach for bloom).

## 4. Shader displacement — living surfaces

```glsl
// vertex shader — needs high-poly geometry (SphereGeometry(1, 128, 128))
// Self-contained value noise — no external snoise include needed:
vec3 hash3(vec3 p) {
  p = vec3(dot(p, vec3(127.1, 311.7, 74.7)),
           dot(p, vec3(269.5, 183.3, 246.1)),
           dot(p, vec3(113.5, 271.9, 124.6)));
  return fract(sin(p) * 43758.5453);
}
float noise3(vec3 p) {
  vec3 i = floor(p), f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  float n = mix(
    mix(mix(hash3(i).x,               hash3(i + vec3(1,0,0)).x, f.x),
        mix(hash3(i + vec3(0,1,0)).x, hash3(i + vec3(1,1,0)).x, f.x), f.y),
    mix(mix(hash3(i + vec3(0,0,1)).x, hash3(i + vec3(1,0,1)).x, f.x),
        mix(hash3(i + vec3(0,1,1)).x, hash3(i + vec3(1,1,1)).x, f.x), f.y), f.z);
  return n * 2.0 - 1.0;
}

uniform float uTime;
uniform float uDisplacement;
varying vec3 vNormal;
void main() {
  vNormal = normal;
  float n = noise3(position * 1.5 + uTime * 0.3);
  vec3 displaced = position + normal * n * uDisplacement;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(displaced, 1.0);
}
```

Drive `uDisplacement` from a scrubbed ScrollTrigger for surfaces that "wake up" as sections enter. Keep amplitude subtle (0.1–0.4): breathing, not boiling.

**Scroll-velocity UV warp** (fast scroll bends the scene):
```glsl
uniform float uScrollVelocity;
vec2 distorted = vUv;
distorted.y += sin(vUv.x * 10.0) * clamp(uScrollVelocity, 0.0, 60.0) * 0.002;
```
Velocity tracking + decay lives in motion-recipes.md §6.

## 5. GPGPU particles

Only for scenes that are *about* particles (abstract R&D pages, data-cloud moments). Never as default garnish. CPU caps at ~8k particles; for 16k+ use `GPUComputationRenderer`:

```javascript
import { GPUComputationRenderer } from 'three/addons/misc/GPUComputationRenderer.js'
const WIDTH = 128 // 128×128 = 16k particles
const gpu = new GPUComputationRenderer(WIDTH, WIDTH, renderer)

// Three textures: position, velocity, and a STATIC copy of home positions
const dtPos = gpu.createTexture(), dtVel = gpu.createTexture(), dtHome = gpu.createTexture()
fillWithStartPositions(dtPos); fillWithStartPositions(dtHome)  // same data (see §6 for distribution)

const posVar = gpu.addVariable('texturePosition', posFrag, dtPos)
const velVar = gpu.addVariable('textureVelocity', velFrag, dtVel)
gpu.setVariableDependencies(posVar, [posVar, velVar])
gpu.setVariableDependencies(velVar, [posVar, velVar])
// home texture is a plain uniform on the velocity pass (it never changes):
velVar.material.uniforms.textureHome = { value: dtHome }
velVar.material.uniforms.uMouse = { value: new THREE.Vector3(9999, 9999, 9999) }
velVar.material.uniforms.uMouseSpeed = { value: 0 }
gpu.init()
// per frame:
gpu.compute()
particleMat.uniforms.texturePosition.value = gpu.getCurrentRenderTarget(posVar).texture
```

Position shader (`posFrag`) — integrate velocity:
```glsl
void main() {
  vec2 uv = gl_FragCoord.xy / resolution.xy;
  vec4 pos = texture2D(texturePosition, uv);
  vec4 vel = texture2D(textureVelocity, uv);
  pos.xyz += vel.xyz;
  gl_FragColor = pos;
}
```

Velocity shader (`velFrag`) — damping + spring-home + mouse repulsion:
```glsl
uniform sampler2D textureHome;
uniform vec3 uMouse;
uniform float uMouseSpeed;
void main() {
  vec2 uv = gl_FragCoord.xy / resolution.xy;
  vec4 vel = texture2D(textureVelocity, uv);
  vec4 pos = texture2D(texturePosition, uv);
  vec4 home = texture2D(textureHome, uv);
  vel.xyz *= 0.97;                              // damping
  vel.xyz -= (pos.xyz - home.xyz) * 0.003;      // spring back to home
  float d = distance(pos.xyz, uMouse);
  if (d < 2.0) vel.xyz += normalize(pos.xyz - uMouse) * (1.0 - d / 2.0) * 0.004 * uMouseSpeed;
  gl_FragColor = vel;
}
```

Render with velocity-driven alpha, `AdditiveBlending`, `depthWrite: false`. Keep alpha ≤ 0.3 and color the particles in the preset palette (cream/orange for B; ink/accent for A — NOT white-on-black starfield).

## 6. Particle field placement

| Radius (relative to hero object at ~2 units) | Reads as |
|---|---|
| 2–3 units | A shell wrapping the hero — wrong, snow-globe effect |
| 6–8 units | Background atmosphere the hero floats in front of — correct |
| 12+ units | Disconnected from the scene |

Fibonacci-sphere distribution avoids pole clumping:
```javascript
const N = 8000, PHI = Math.PI * (3 - Math.sqrt(5))
for (let i = 0; i < N; i++) {
  const y = 1 - (i / (N - 1)) * 2
  const r = Math.sqrt(1 - y * y)
  const R = 6.5 + (Math.random() - 0.5) * 2.5
  pos[i*3] = Math.cos(PHI * i) * r * R
  pos[i*3+1] = y * R
  pos[i*3+2] = Math.sin(PHI * i) * r * R
}
```

## 7. Post-processing — one merged pass

Merge grain + vignette + aberration into ONE ShaderPass (three separate passes = 3× texture reads). Values below are intentionally at the threshold of perception; that is the point — felt, not seen.

```javascript
const cinematicShader = {
  uniforms: {
    tDiffuse: { value: null }, uTime: { value: 0 },
    uAberration: { value: 0.0015 }, uGrain: { value: 0.018 }, uVignette: { value: 0.28 },
  },
  vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
  fragmentShader: /* glsl */`
    uniform sampler2D tDiffuse; uniform float uTime,uAberration,uGrain,uVignette;
    varying vec2 vUv;
    float rand(vec2 co){ return fract(sin(dot(co,vec2(12.9898,78.233)))*43758.5453); }
    void main(){
      vec2 dir = vUv - 0.5;
      vec4 cr = texture2D(tDiffuse, vUv + dir*uAberration);
      vec4 cg = texture2D(tDiffuse, vUv);
      vec4 cb = texture2D(tDiffuse, vUv - dir*uAberration);
      vec4 color = vec4(cr.r, cg.g, cb.b, 1.0);
      color.rgb += (rand(vUv + uTime*0.01) - 0.5) * uGrain;
      color.rgb *= 1.0 - dot(dir,dir) * uVignette * 2.0;
      gl_FragColor = color;
    }`
}
```

`UnrealBloomPass` is allowed ONLY on abstract particle scenes (strength ≤ 0.8, threshold ≥ 0.2). Never on products, never on Preset A panels — bloom on a product looks like a broken TV, not luxury.

## 8. Real GLTF assets

Use real GLTF/GLB models for any recognizable object (product, gem, shoe, bottle); procedural geometry only for abstract forms. Procedural lacks the topology and micro-detail that makes something read as real — a viewer spots it in under a second.

**Preferred source — generate the object in Claude Design.** claude.ai/design has a **"3D object"** template in its template picker (verified in the Beta UI, 2026-09) that generates a 3D object from a prompt and exports it as `.glb` or `.obj`. Prefer this over stock assets: you get exactly the object the brief describes, in the brand's own material world, with no license attribution and no hunting through search results for something that is nearly right.

This is a **browser step the user performs** — Claude Code cannot invoke it. The `design` skill bundled with Claude Code is an early preview of the *canvas editor* only (2D `.dc.html` artboards, PNG/PDF export); 3D generation lives in the claude.ai/design backend, which that preview does not expose, and `DesignSync` only moves design-system HTML. So do not call a tool for this. Instead, at Step 2, ask:

> "I need the hero object as a model. Generate it at claude.ai/design — prompt it for *‹the object, in ‹material›, ‹finish››* — export **.glb**, and drop it in `models/`. I'll normalize and light it."

Then keep building everything that doesn't depend on the file (shell, chapter map, scroll rig, a stand-in primitive at the hero's transform) so the model drops into a scene that already works.

- **Ask for `.glb`, not `.obj`.** OBJ carries no PBR materials, no embedded textures, and no scene graph — you would be re-authoring the material by hand and would lose the per-part groups the assembled/exploded interactions in `flow-choreography.md` depend on. Take `.obj` only if `.glb` isn't offered, and expect to assign a `MeshPhysicalMaterial` yourself.
- **Preset A (stylized) barely cares.** Its objects get overridden to a palette `MeshPhysicalMaterial` anyway, so a generated mesh's own materials are discarded — only the silhouette and topology matter. **Preset B (photoreal product) cares a lot**: it renders the real material, so `.glb` with its textures intact is the only sensible input.
- Inspect before committing, exactly as with a downloaded asset: traverse the scene graph and check the part groups against world-space bounds (`pitfalls.md` § GLTF asset traps applies to any model, generated or stock).

**Fallbacks, in order**, when the user can't or won't generate one: Sketchfab (use a `sketchfab-search` skill or helper script if your environment has one — check your available skills/tools; otherwise browse sketchfab.com and download a glTF manually, filtering to downloadable + CC licenses), Poly Haven (CC0), Khronos glTF-Sample-Assets. CC-BY needs a footer credit.

Load + normalize (center, fit to known size, re-material):
```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
const hero = new THREE.Group()
hero.scale.setScalar(0)          // hidden until the intro timeline reveals it
scene.add(hero)
new GLTFLoader().load('./models/scene.gltf', (gltf) => {
  const model = gltf.scene
  const box = new THREE.Box3().setFromObject(model)
  model.position.sub(box.getCenter(new THREE.Vector3()))
  const size = box.getSize(new THREE.Vector3())
  model.scale.setScalar(2.0 / Math.max(size.x, size.y, size.z))
  // keep original textures for photoreal products (Preset B);
  // override with a preset-palette MeshPhysicalMaterial for stylized scenes (Preset A):
  // model.traverse(c => { if (c.isMesh) c.material = presetMaterial })
  hero.add(model)
})
```

## 9. Pre-computed simulations (Houdini pattern)
10. Gems and refractive heroes (real dispersion, no path tracer)
11. CPU caustics from the same BVH

Lusion's core philosophy: *"You don't need to do everything real-time. Pre-calculate the complex, display the result."* For cloth, fluid, destruction: simulate offline (Houdini/C4D/Blender), export per-frame vertex positions, compress to 16-bit, pack into PNG textures, sample in the vertex shader:

```glsl
uniform sampler2D uPositions; uniform float uFrame, uFrameCount;
void main() {
  vec2 frameUV = vec2(uv.x, uFrame / uFrameCount);
  vec3 pos = texture2D(uPositions, frameUV).xyz * uDivider; // decompress
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

Drive `uFrame` from a scrubbed ScrollTrigger — scroll becomes the simulation's timeline. The same texture-sampling trick works for pre-rendered lighting (bake in Blender Cycles, sample frames by scroll index).


---

## 10. Gems and refractive heroes (real dispersion, no path tracer)

For a hero that is *made of* light behaviour - a gem, a lens, a crystal, thick glass - a PBR `transmission` material is not enough and a path tracer is the wrong instrument. Verified on a diamond build.

**Do not reach for a path tracer.** `three-gpu-pathtracer` works and looks extraordinary, but its cost is pixels x samples, so there is ALWAYS a resolve wait; on anything short of a high-end discrete GPU that wait is seconds. Any hero the user handles continuously is structurally incompatible with an accumulating renderer. (It remains excellent as an *offline* tool - see §11.)

**Do this instead: raycast inside the mesh, in the fragment shader, against a BVH.**

```js
import { MeshBVH, MeshBVHUniformStruct, BVHShaderGLSL } from 'three-mesh-bvh'

const bvh = new MeshBVH( geometry )
const bvhUniform = new MeshBVHUniformStruct()
bvhUniform.updateFrom( bvh )
// fragment shader:
//   ${BVHShaderGLSL.common_functions}
//   ${BVHShaderGLSL.bvh_struct_definitions}
//   ${BVHShaderGLSL.bvh_ray_functions}
//   #define BVH_STACK_DEPTH 40
//   #define INFINITY 1e20
//   uniform BVH bvh;
//   bvhIntersectFirstHit( bvh, origin, dir, faceIndices, faceNormal, barycoord, side, dist )
```

Per pixel: refract in at the surface, then bounce internally against the real geometry (2-4 bounces), refracting out or reflecting on total internal reflection, and sample a cubemap on escape. The brilliance then comes from the object's actual facets rather than from a matcap. Measured cost on a 112-triangle stone, 7 wavelengths x 4 bounces: under the 6 ms vsync interval even at 24 megapixels. drei's `MeshRefractionMaterial` is this technique packaged for React; porting it to vanilla needs the shader defines, the BVH setup, and per-frame camera matrices.

**Non-obvious requirements:**

- **Trace in the geometry's LOCAL space** (the space the BVH is built in) and transform only the final exit direction to world. Sync `modelMatrixInverse` every frame the object moves, or it silently refracts against last frame's orientation.
- **`modelMatrix` is injected into the VERTEX prefix only.** The fragment prefix carries `viewMatrix` and `cameraPosition` but not `modelMatrix` - declare it yourself and the renderer populates it.
- **Face the hit normal against the ray** (`n * (dot(n,dir) > 0 ? -1 : 1)`). Getting this wrong inverts every internal refraction, and the result still looks plausible, which makes it expensive to find.
- **Do not clamp a still-trapped ray to black.** Diamond's critical angle is ~24.4 degrees, so total internal reflection is the common case; a ray that runs out of bounces should return its current direction, or you drain exactly the light that makes the cut bright.
- **`pow(base, 2.0)` with a negative base is undefined in GLSL.** Schlick's f0 for ior > 1 has a negative base (about -0.415 for diamond) - square it directly.

**Real dispersion, cheaply.** Do not use a hand-tuned RGB channel offset. Build a wavelength table from the material's real Cauchy curve and the CIE colour matching functions, normalise the weights so they sum to (1,1,1) (or a white environment comes back tinted), and either trace one path per wavelength (top tier) or trace one path and split the spectrum at the exit interface (everything else). The exit-split costs N cubemap samples instead of N BVH traversals and still reads as real, because the separation comes from the true indices.

**The lighting rule that decides whether any of this looks like anything.** A raster shader point-samples the environment ONCE per wavelength, so it almost always MISSES small sources. This is the exact opposite of a path tracer, which integrates hundreds of samples and therefore loves near-point lights in a black void. Hand a raster refraction shader a path tracer's rig and it renders an almost entirely black object with a few rainbow slivers. Build a real light box instead:

- a **broad front field** centred on the camera direction, falling off with angle - a brilliant cut is engineered to return light that entered the crown back out of the crown, so light must arrive from the VIEWER's side. With sources only overhead, the object reads as a dark star face-on, which is the opposite of what the cut exists to do.
- **bright bands with deliberate dark gaps** for the facet mosaic (see pitfalls.md, design failures).
- **a handful of near-point hot spots** for the fire, small enough not to overlap their own spectrum (dispersion separates diamond's wavelengths by roughly 2 degrees, so a 20-degree source averages back to white).
- **a base that is dark but not black.** The ratio of base to field IS the object's dynamic range: too low and the unlit facets read as holes punched in the object; too high and everything clips. Measured sweet spot on the diamond build was base/field ~= 0.07.

---

## 11. CPU caustics from the same BVH

A refractive hero throwing a real pool of light onto a surface beneath it is most of what sells it as a physical object, and it does not need a bake.

`MeshBVH` is queryable from JavaScript (`bvh.raycastFirst( ray, THREE.DoubleSide )`), so the same BVH the shader uses can be photon-traced on the CPU: fire rays from the lamp, refract in, bounce internally, intersect the receiving plane, accumulate where they land, blur, normalise, upload as a `DataTexture` on an additively-blended plane.

- **Slice it across frames.** 90k photons measured ~500 ms in one call, which lands as a stall at exactly the worst moment: the instant the user releases the object. An incremental tracer stepping ~1400 photons per frame held the worst frame at 6.4 ms.
- **Retrace only when the pose settles**, debounced (~24 still frames), and only if the pose actually changed.
- **Expect ~4% of photons to reach the plane** and do not treat it as a bug - a brilliant cut sends most light back up to the viewer.
- **Normalise on a high percentile (~0.997), not the max**, or one lucky texel scales the whole pattern into invisibility.
- **Resolution trades against coherence**: the photon count is fixed by the frame budget, so lowering the texture size is the free way to get more photons per texel. 128 with three blur passes read as a caustic; 192 read as speckle.
- Three wavelengths is enough for the colour at the fringes; the pattern is low-frequency.
- Directions rotate but do not translate - transform them with a `Matrix3` normal matrix, not the full inverse matrix, or any translation corrupts the light direction.
