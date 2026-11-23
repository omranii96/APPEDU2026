/* =====================================================================
   CHARMED PARIS · prototype · home.js (accueil uniquement, defer, après site.js)
   1. Intro « l'écrin s'ouvre » pilotée au scroll (260vh bureau / 170vh mobile)
      - inactive si prefers-reduced-motion, trafic pub (utm_, gclid, fbclid…) ou sans JS : état final statique
      - Three.js r128 (auto-hébergé) chargé seulement après une interaction ou un temps mort
   2. Carrousel des coffrets (photos réelles boîte fermée / ouverte + parures détourées)
   3. « La file des parures » (Une / La file / Toutes) avec étiquette ticket
   4. Packagings réels (sélecteur) · en-tête velours pendant l'intro
   ===================================================================== */
(function () {
  'use strict';
  var S = window.CPsite, CP = window.CP;
  if (!S || !CP) { return; }
  var T = S.T, L = S.L, eur = S.eur, esc = S.esc;
  var $ = function (id) { return document.getElementById(id); };
  var html = document.documentElement;
  var reduce = S.reduceMotion;
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }
  function seg(p, a, b) { return clamp((p - a) / (b - a), 0, 1); }
  function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function band(p, a, b, c, d) { return seg(p, a, b) * (1 - seg(p, c, d)); }

  /* ---------- En-tête velours tant que l'intro est à l'écran ---------- */
  var hdr = $('hdr'), intro = $('intro'), ann = document.querySelector('.annonce');
  function annH() { if (ann) { html.style.setProperty('--ann', ann.offsetHeight + 'px'); } }
  annH(); window.addEventListener('resize', annH);
  function hdrTone() { if (!intro) { return; } var r = intro.getBoundingClientRect(); hdr.classList.toggle('dark', r.bottom > 64); }
  window.addEventListener('scroll', hdrTone, { passive: true }); hdrTone();

  /* ---------- « Passer l'intro » ---------- */
  var skip = $('skipIntro');
  if (skip) {
    skip.addEventListener('click', function (e) {
      var t = $('coffrets'); if (!t) { return; }
      e.preventDefault();
      t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      t.setAttribute('tabindex', '-1'); t.focus({ preventScroll: true });
    });
  }

  /* =====================================================================
     1. Intro
     ===================================================================== */
  (function () {
    if (!intro || !html.classList.contains('cp-motion')) { return; }
    var q = function (s) { return intro.querySelector(s); };
    var stage = q('.stage'), logo = q('.i-logo'), brL = q('.i-logo .br.l'), brR = q('.i-logo .br.r'), mid = q('.i-logo .mid'), paris = q('.i-logo .paris');
    var glow = q('.glow'), tOpen = q('.it-open'), t1 = q('.it-1'), t2 = q('.it-2'), fin = q('.i-final'), hint = q('.i-hint'), prog = q('.prog i'), ring = q('.ring'), canvas = q('.gl');
    intro.classList.add('is-film');
    logo.style.opacity = '1';
    var small = window.innerWidth < 700 || (window.matchMedia && window.matchMedia('(pointer: coarse)').matches);
    var FOV = 35, TAN = Math.tan(FOV / 2 * Math.PI / 180);
    var G = null, loading = false;

    function canUseGL() {
      var conn = navigator.connection || {};
      if (conn.saveData) { return false; }
      if (navigator.deviceMemory && navigator.deviceMemory < 2) { return false; }
      try { var c = document.createElement('canvas'); return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl'))); } catch (e) { return false; }
    }
    function makeEnv(THREE, renderer) {
      var w = small ? 512 : 1024, h = w / 2, c = document.createElement('canvas'); c.width = w; c.height = h;
      var x = c.getContext('2d'), g = x.createLinearGradient(0, 0, 0, h);
      g.addColorStop(0, '#8a7a80'); g.addColorStop(0.45, '#2a2026'); g.addColorStop(1, '#0a0708');
      x.fillStyle = g; x.fillRect(0, 0, w, h); x.filter = 'blur(' + (small ? 7 : 14) + 'px)';
      var k = w / 1024;
      [[0, 0, 1024, 40, '#ffffff'], [260, 60, 340, 130, '#ffffff'], [660, 120, 260, 90, '#ffe6b8'], [60, 180, 160, 220, '#f8e4ea'], [840, 220, 150, 180, '#ffffff'], [420, 300, 300, 60, '#c9a6b0']].forEach(function (r) { x.fillStyle = r[4]; x.fillRect(r[0] * k, r[1] * k, r[2] * k, r[3] * k); });
      x.filter = 'none';
      var t = new THREE.CanvasTexture(c); t.mapping = THREE.EquirectangularReflectionMapping; t.encoding = THREE.sRGBEncoding;
      var pm = new THREE.PMREMGenerator(renderer), env = pm.fromEquirectangular(t).texture; t.dispose(); pm.dispose(); return env;
    }
    function spriteTex(THREE, kind) {
      var s = 128, c = document.createElement('canvas'); c.width = c.height = s;
      var x = c.getContext('2d'), g = x.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2);
      g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(kind === 'star' ? 0.08 : 0.25, 'rgba(255,240,210,.7)'); g.addColorStop(1, 'rgba(255,240,210,0)');
      x.fillStyle = g; x.fillRect(0, 0, s, s);
      if (kind === 'star') {
        x.globalCompositeOperation = 'lighter';
        [[s, 3], [3, s]].forEach(function (d) { var hz = d[0] === s, lg = x.createLinearGradient(hz ? 0 : s / 2, hz ? s / 2 : 0, hz ? s : s / 2, hz ? s / 2 : s); lg.addColorStop(0, 'rgba(255,255,255,0)'); lg.addColorStop(0.5, 'rgba(255,255,255,1)'); lg.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = lg; x.fillRect((s - d[0]) / 2, (s - d[1]) / 2, d[0], d[1]); });
      }
      return new THREE.CanvasTexture(c);
    }
    function setupGL(THREE) {
      var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: !small, alpha: true, powerPreference: small ? 'low-power' : 'high-performance' });
      if (!renderer.getContext()) { throw new Error('no gl'); }
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, small ? 1.5 : 2));
      renderer.outputEncoding = THREE.sRGBEncoding; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.15;
      var scene = new THREE.Scene(); scene.environment = makeEnv(THREE, renderer);
      var camera = new THREE.PerspectiveCamera(FOV, 1, 0.1, 100); camera.position.set(0, 0, 10);
      var gold = new THREE.MeshStandardMaterial({ color: 0xE8C27A, metalness: 1, roughness: 0.15 });
      var bandG = new THREE.Group();
      bandG.add(new THREE.Mesh(new THREE.TorusGeometry(1, 0.11, small ? 24 : 48, small ? 120 : 220), gold));
      var head = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.09, 0.22, 32), gold); head.position.y = 1.16; bandG.add(head);
      var prof = [[0, -0.36], [0.34, -0.02], [0.34, 0.03], [0.21, 0.15], [0, 0.15]].map(function (a) { return new THREE.Vector2(a[0], a[1]); });
      var gem = new THREE.Mesh(new THREE.LatheGeometry(prof, 16), new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 1, roughness: 0, flatShading: true, envMapIntensity: 4.5, emissive: 0x2b2530 }));
      gem.position.y = 1.47; bandG.add(gem);
      for (var i = 0; i < 4; i++) { var an = i * Math.PI / 2 + Math.PI / 4, pr = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.022, 0.32, 8), gold); pr.position.set(Math.cos(an) * 0.27, 1.42, Math.sin(an) * 0.27); pr.rotation.z = -Math.cos(an) * 0.4; pr.rotation.x = Math.sin(an) * 0.4; bandG.add(pr); }
      var starMat = new THREE.SpriteMaterial({ map: spriteTex(THREE, 'star'), color: 0xfff1d0, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0 });
      var star = new THREE.Sprite(starMat); star.scale.set(1.1, 1.1, 1); star.position.set(0.1, 1.56, 0.25); bandG.add(star);
      var pivot = new THREE.Group(); pivot.add(bandG); bandG.position.y = -0.25; scene.add(pivot);
      var dl = new THREE.DirectionalLight(0xfff3e0, 1.1); dl.position.set(3, 5, 4); scene.add(dl);
      var N = small ? 300 : 900, pos = new Float32Array(N * 3);
      for (var k = 0; k < N; k++) { var r = 1.8 + Math.random() * 7, th = Math.random() * Math.PI * 2, ph = Math.acos(2 * Math.random() - 1); pos[k * 3] = r * Math.sin(ph) * Math.cos(th); pos[k * 3 + 1] = r * Math.cos(ph) * 0.8; pos[k * 3 + 2] = r * Math.sin(ph) * Math.sin(th) * 0.6; }
      var dg = new THREE.BufferGeometry(); dg.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      var dustMat = new THREE.PointsMaterial({ size: 0.06, map: spriteTex(THREE, 'dot'), color: 0xE9CB8F, transparent: true, opacity: 0.4, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true });
      var dust = new THREE.Points(dg, dustMat); scene.add(dust);
      return { renderer: renderer, scene: scene, camera: camera, pivot: pivot, starMat: starMat, dust: dust, dustMat: dustMat };
    }
    function loadThree() {
      if (loading || G || !intro.dataset.three || !canUseGL()) { return; }
      loading = true;
      var done = function () { try { G = setupGL(window.THREE); intro.classList.add('has-gl'); measure(); start(); } catch (e) { G = null; } };
      if (window.THREE) { done(); return; }
      var s = document.createElement('script'); s.src = intro.dataset.three; s.async = true; s.onload = done; document.head.appendChild(s);
    }
    var triggers = ['scroll', 'wheel', 'pointerdown', 'touchstart', 'keydown'];
    function onFirst() { triggers.forEach(function (t) { window.removeEventListener(t, onFirst); }); loadThree(); }
    triggers.forEach(function (t) { window.addEventListener(t, onFirst, { passive: true, once: true }); });
    window.addEventListener('load', function () { var idle = window.requestIdleCallback || function (cb) { return setTimeout(cb, 2500); }; idle(onFirst, { timeout: 4000 }); });

    var W = 1, H = 1, F = 100, midW = 300, zf = 1;
    function measure() {
      W = stage.clientWidth; H = stage.clientHeight;
      F = parseFloat(getComputedStyle(logo).fontSize) || 100;
      var ls = mid.style.letterSpacing, pl = mid.style.paddingLeft;
      mid.style.letterSpacing = '.08em'; mid.style.paddingLeft = '.08em'; midW = mid.offsetWidth;
      mid.style.letterSpacing = ls; mid.style.paddingLeft = pl;
      var asp = W / H; zf = asp < 1 ? Math.min(1.9, 1.15 / asp) : 1;
      if (G) { G.renderer.setSize(W, H, false); G.camera.aspect = asp; G.camera.updateProjectionMatrix(); }
    }
    measure();
    window.addEventListener('resize', function () { measure(); readScroll(); start(); });
    var target = 0, sp = 0, px = 0, py = 0, mx = 0, my = 0;
    function readScroll() { var r = intro.getBoundingClientRect(), total = intro.offsetHeight - stage.offsetHeight; target = total > 0 ? clamp(-r.top / total, 0, 1) : 1; }
    window.addEventListener('scroll', function () { readScroll(); start(); }, { passive: true });
    readScroll();
    if (!small) { window.addEventListener('pointermove', function (e) { mx = (e.clientX / window.innerWidth) * 2 - 1; my = (e.clientY / window.innerHeight) * 2 - 1; }, { passive: true }); }
    var visible = true, raf = 0, t0 = performance.now();
    function start() { if (!raf && visible && !document.hidden) { raf = requestAnimationFrame(frame); } }
    function stop() { if (raf) { cancelAnimationFrame(raf); raf = 0; } }
    if ('IntersectionObserver' in window) { new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) { start(); } else { stop(); } }).observe(intro); }
    document.addEventListener('visibilitychange', function () { if (document.hidden) { stop(); } else { start(); } });
    var mileStones = {};
    function frame(now) {
      raf = 0;
      var time = (now - t0) / 1000;
      sp += (target - sp) * 0.09; px += (mx - px) * 0.05; py += (my - py) * 0.05;
      var p = sp;
      [25, 50, 75, 100].forEach(function (m) { if (!mileStones[m] && p * 100 >= m - 0.5) { mileStones[m] = 1; (window.dataLayer = window.dataLayer || []).push({ event: 'intro_progression', pct: m }); } });
      var o = ease(seg(p, 0.08, 0.38)), c = ease(seg(p, 0.74, 0.92));
      var zEnd = 12 * zf, ringPx = 1.45 / (2 * zEnd * TAN) * H;
      logo.style.top = (44 - 12 * c) + '%';
      var fScale = clamp((2.1 * ringPx) / (0.7 * F), 0.6, 2.6);
      var closedX = midW / 2 + 0.32 * F, farX = W / 2 + 0.8 * F * 1.6, finalX = ringPx * 0.9 + 0.25 * F * fScale + 8;
      var x, a, s;
      if (c > 0) { x = lerp(farX, finalX, c); a = lerp(82, 0, c); s = lerp(1.6, fScale, c); }
      else { x = lerp(closedX, farX, o); a = lerp(0, 82, o); s = lerp(1, 1.6, o); }
      var breathe = (1 - o) * Math.sin(time * 1.6) * 0.012 * F;
      brL.style.transform = 'translate(-50%,-50%) translateX(' + (-x - breathe) + 'px) rotateY(' + (-a) + 'deg) scale(' + s + ')';
      brR.style.transform = 'translate(-50%,-50%) translateX(' + (x + breathe) + 'px) rotateY(' + a + 'deg) scale(' + s + ')';
      var ls = lerp(0.08, 0.95, o);
      mid.style.letterSpacing = ls + 'em'; mid.style.paddingLeft = ls + 'em';
      mid.style.opacity = String(1 - seg(p, 0.12, 0.32));
      mid.style.filter = 'blur(' + (o * 10).toFixed(2) + 'px)';
      if (paris) { paris.style.opacity = String(1 - seg(p, 0.05, 0.16)); }
      glow.style.opacity = String(clamp(0.35 + seg(p, 0.1, 0.36) * 0.65 * (1 - 0.6 * seg(p, 0.6, 0.78)) + 0.45 * c, 0, 1));
      tOpen.style.opacity = String(1 - seg(p, 0.03, 0.12));
      var b1 = band(p, 0.40, 0.46, 0.54, 0.59), b2 = band(p, 0.56, 0.61, 0.68, 0.73);
      t1.style.opacity = String(b1); t1.style.transform = 'translateX(-50%) translateY(' + ((1 - b1) * 18) + 'px)';
      t2.style.opacity = String(b2); t2.style.transform = 'translateX(-50%) translateY(' + ((1 - b2) * -18) + 'px)';
      var bf = seg(p, 0.84, 0.96);
      fin.style.opacity = String(bf); fin.style.transform = 'translateX(-50%) translateY(' + ((1 - bf) * 16) + 'px)';
      fin.style.visibility = bf > 0.01 ? 'visible' : 'hidden';
      if (hint) { hint.style.opacity = String(1 - seg(p, 0, 0.06)); }
      if (prog) { prog.style.transform = 'scaleX(' + p + ')'; }
      var r = easeOut(seg(p, 0.2, 0.46));
      if (G) {
        var macro = band(p, 0.40, 0.56, 0.62, 0.80);
        var z = p < 0.6 ? lerp(10, 3.2, ease(seg(p, 0.26, 0.58))) : lerp(3.2, 12, ease(seg(p, 0.62, 0.84)));
        var zz = z * zf, off = c * 0.09 * 2 * zz * TAN;
        G.camera.position.set(px * 0.25 * (1 - macro), 1.25 * macro + (-py) * 0.15 - off, zz);
        G.camera.lookAt(0, 1.05 * macro - off, 0);
        G.pivot.position.y = lerp(-4.4, 0, r); G.pivot.scale.setScalar(lerp(0.6, 1, r));
        G.pivot.rotation.y = time * 0.22 + p * Math.PI * 2.4 + px * 0.35; G.pivot.rotation.x = py * 0.18 + 0.32 * macro;
        G.starMat.opacity = seg(p, 0.36, 0.5) * (0.25 + 0.75 * Math.pow(Math.max(0, Math.sin(time * 2.1)), 10)); G.starMat.rotation = time * 0.4;
        G.dust.rotation.y = time * 0.025 + p * 0.7; G.dust.scale.setScalar(1 + 1.3 * easeOut(seg(p, 0.16, 0.46)));
        G.dustMat.opacity = 0.3 + 0.55 * seg(p, 0.1, 0.36);
        G.renderer.toneMappingExposure = 1.1 + 0.35 * band(p, 0.18, 0.32, 0.42, 0.56);
        G.renderer.render(G.scene, G.camera);
      } else if (ring) {
        ring.style.opacity = String(0.25 + 0.75 * r);
        ring.style.transform = 'translate(-50%,-50%) scale(' + lerp(0.6, 1, r) * (1 + 0.3 * band(p, 0.4, 0.56, 0.62, 0.8)) + ')';
      }
      var settled = Math.abs(target - sp) < 0.0005;
      if (G || !settled) { start(); }
    }
    start();
  })();

  /* =====================================================================
     2. Carrousel des coffrets
     ===================================================================== */
  (function () {
    var stage = $('cofStage'); if (!stage) { return; }
    var C = stage.dataset.skus.split(',').map(function (s) { return S.byId[s]; }).filter(Boolean);
    var N = C.length, ring = $('cofRing'), dots = $('cofDots'), hand = $('cofHand');
    var items = [], W = 1, H = 1, B = 300, Rx = 400;
    C.forEach(function (p, k) {
      var e = document.createElement('div'); e.className = 'citem'; e.setAttribute('aria-hidden', 'true');
      e.innerHTML = '<div class="sh"></div><img class="closed" src="assets/img/box-closed.webp" alt="" width="720" height="720" loading="lazy"><img class="open" src="assets/img/box-open.webp" alt="" width="720" height="720" loading="lazy"><div class="glow2"></div><img class="jw" alt="" width="700" height="700" loading="lazy">';
      e.querySelector('.jw').src = p.cut;
      e.addEventListener('click', function () { if (!moved) { goTo(k); } });
      ring.appendChild(e); items.push(e);
      var d = document.createElement('button'); d.type = 'button';
      d.addEventListener('click', function () { goTo(k); }); dots.appendChild(d);
    });
    var c = 0, target = 0, dragging = false, sx = 0, st0 = 0, moved = false, front = -1, touched = false, visible = true, openTimer = null;
    function idx(v) { return ((Math.round(v) % N) + N) % N; }
    function interact() { if (!touched) { touched = true; hand.style.opacity = '0'; } }
    function goTo(k) { var cur = Math.round(target), d = ((k - idx(target)) % N + N) % N; if (d > N / 2) { d -= N; } target = cur + d; interact(); kick(); }
    function setInfo(k) {
      var p = C[k];
      $('cofTag').textContent = L(CP.univers[p.u].name) + ' · ' + T('Parure ' + p.pcs.fr.length + ' pièces', p.pcs.en.length + '-piece set');
      $('cofName').innerHTML = '<a href="' + p.url + '">' + esc(L(p.name)) + '</a>';
      $('cofDesc').textContent = L(p.line);
      $('cofPrice').textContent = eur(p.price, 1);
      $('cofLive').textContent = T('Coffret ' + (k + 1) + ' sur ' + N + ' : ' + L(p.name) + ', ' + eur(p.price, 1), 'Box ' + (k + 1) + ' of ' + N + ': ' + L(p.name) + ', ' + eur(p.price, 1));
      Array.prototype.forEach.call(dots.children, function (d, i) { d.setAttribute('aria-current', String(i === k)); d.setAttribute('aria-label', L(C[i].name)); });
    }
    $('cofAdd').addEventListener('click', function () { var p = C[idx(target)]; S.add(p.sku); });
    $('cofPrev').addEventListener('click', function () { target = Math.round(target) - 1; interact(); kick(); });
    $('cofNext').addEventListener('click', function () { target = Math.round(target) + 1; interact(); kick(); });
    stage.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); $('cofNext').click(); } if (e.key === 'ArrowLeft') { e.preventDefault(); $('cofPrev').click(); } });
    stage.addEventListener('pointerdown', function (e) { dragging = true; moved = false; sx = e.clientX; st0 = target; stage.classList.add('drag'); try { stage.setPointerCapture(e.pointerId); } catch (_) { /* */ } kick(); });
    stage.addEventListener('pointermove', function (e) { if (!dragging) { return; } var dx = e.clientX - sx; if (Math.abs(dx) > 5) { moved = true; interact(); } target = st0 - dx / (Rx * 0.75); kick(); });
    function release() { if (!dragging) { return; } dragging = false; stage.classList.remove('drag'); target = Math.round(target); kick(); }
    stage.addEventListener('pointerup', release); stage.addEventListener('pointercancel', release);
    function fit() { W = stage.clientWidth; H = stage.clientHeight; B = Math.round(Math.min(W * 0.5, H * 0.72, 420)); Rx = Math.min(W * 0.42, 560); stage.style.setProperty('--B', B + 'px'); kick(); }
    fit(); window.addEventListener('resize', fit);
    var raf = 0;
    function kick() { if (!raf && visible) { raf = requestAnimationFrame(tick); } }
    if ('IntersectionObserver' in window) { new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) { kick(); } }).observe(stage); }
    function tick() {
      raf = 0;
      c = reduce ? target : c + (target - c) * 0.12;
      var k0 = idx(c); if (k0 !== front) { front = k0; setInfo(k0); }
      items.forEach(function (e, k) {
        var th = (k - c) / N * Math.PI * 2, z = Math.cos(th), t = (z + 1) / 2;
        var sc = 0.3 + 0.7 * Math.pow(t, 2.2), x = Math.sin(th) * Rx, y = -(1 - t) * H * 0.22;
        e.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0) scale(' + sc.toFixed(3) + ')';
        var bl = (1 - t) * 3; e.style.filter = (bl > 0.2 ? 'blur(' + bl.toFixed(1) + 'px) ' : '') + 'brightness(' + (0.55 + 0.45 * t).toFixed(2) + ')';
        e.style.zIndex = String(Math.round(t * 100)); e.style.opacity = (0.35 + 0.65 * t).toFixed(2);
      });
      var settled = !dragging && Math.abs(target - c) < 0.02 && target === Math.round(target);
      items.forEach(function (e, k) { if (e.classList.contains('isopen') && !(settled && k === idx(target))) { e.classList.remove('isopen'); } });
      if (settled && !items[idx(target)].classList.contains('isopen') && !openTimer) {
        openTimer = setTimeout(function () { openTimer = null; if (!dragging && Math.abs(target - c) < 0.02) { items[idx(target)].classList.add('isopen'); } }, 150);
      }
      if (!settled || dragging) { kick(); }
    }
    S.onLang(function () { setInfo(idx(target)); });
    setInfo(0); kick();
  })();

  /* =====================================================================
     3. La file des parures
     ===================================================================== */
  (function () {
    var root = $('pieces'); if (!root) { return; }
    var stage = $('luStage'), host = $('luItems');
    var Lst = stage.dataset.skus.split(',').map(function (s) { return S.byId[s]; }).filter(Boolean);
    var N = Lst.length, view = 'focus', target = 0, els = [], st = [], Sz = 320, W = 1, H = 1, visible = true;
    Lst.forEach(function (p, k) {
      var e = document.createElement('div'); e.className = 'lu-item'; e.setAttribute('aria-hidden', 'true');
      e.innerHTML = '<img alt="" width="700" height="700" loading="lazy"><div class="lbl"></div>';
      e.querySelector('img').src = p.cut;
      e.addEventListener('click', function () { if (moved) { return; } if (view === 'grid') { jump(k); setView('focus'); } else if (k !== idx()) { jump(k); } });
      host.appendChild(e); els.push(e); st.push({ x: 0, y: 0, z: -3000, s: 1, b: 10, o: 0 });
    });
    function labels() { els.forEach(function (e, k) { e.querySelector('.lbl').textContent = String(k + 1).padStart(2, '0') + ' ' + Lst[k].model.toUpperCase() + ' · ' + eur(Lst[k].price, 1); }); }
    function idx() { return ((Math.round(target) % N) + N) % N; }
    function jump(k) { var c0 = Math.round(target), d = ((k - idx()) % N + N) % N; if (d > N / 2) { d -= N; } target = c0 + d; kick(); }
    function setView(v) {
      view = v; root.classList.toggle('focus', v === 'focus'); root.classList.toggle('grid', v === 'grid');
      root.querySelectorAll('.lu-views button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.v === v)); });
      $('luHint').textContent = v === 'grid' ? T('Touche une parure pour l\'ouvrir', 'Tap a set to open it') : T('Glisse, ou utilise les flèches ← →', 'Swipe, or use the ← → keys');
      kick();
    }
    root.querySelectorAll('.lu-views button').forEach(function (b) { b.addEventListener('click', function () { setView(b.dataset.v); }); });
    var shown = -1;
    function showInfo(k) {
      var p = Lst[k], h = $('luName');
      h.classList.add('out');
      setTimeout(function () { h.innerHTML = '<a href="' + p.url + '">' + esc(p.model) + '</a>'; $('luMeta').textContent = T('Parure n°', 'Set no. ') + String(k + 1).padStart(2, '0') + ' · ' + L(CP.univers[p.u].name); h.classList.remove('out'); }, reduce ? 0 : 160);
      $('ttNo').textContent = T('Écrin n°', 'Box no. ') + String(k + 1).padStart(2, '0');
      $('ttCode').textContent = p.code; $('ttName').textContent = p.model;
      var rows = L(p.pcs).map(function (x) { return '<li class="tt-row"><span>' + esc(x) + '</span><span>' + T('inclus', 'included') + '</span></li>'; }).join('');
      rows += '<li class="tt-row"><span>' + (p.u === 'j925' ? T('Écrin velours, pochette, chamoisine', 'Velvet case, pouch, cloth') : T('Boîte à bijoux, pochette, chamoisine', 'Jewellery box, pouch, cloth')) + '</span><span>' + T('incluses', 'included') + '</span></li>';
      $('ttRows').innerHTML = rows;
      $('ttPrice').textContent = eur(p.price); $('ttSku').textContent = p.sku + ' · CHARMED PARIS';
      $('luLive').textContent = T('Parure ' + (k + 1) + ' sur ' + N + ' : ' + L(p.name) + ', ' + eur(p.price, 1), 'Set ' + (k + 1) + ' of ' + N + ': ' + L(p.name) + ', ' + eur(p.price, 1));
      var t = $('luTag'); t.classList.remove('swap'); void t.offsetWidth; if (!reduce) { t.classList.add('swap'); }
      var add = $('ttAdd'); add.firstChild.textContent = T('Ajouter à l\'écrin', 'Add to my box');
      add.setAttribute('aria-label', T('Ajouter à l\'écrin : ', 'Add to my box: ') + L(p.name));
    }
    $('ttAdd').addEventListener('click', function () { var p = Lst[idx()]; if (p.variants) { location.href = p.url; } else { S.add(p.sku); } });
    var drag = false, sx = 0, st0 = 0, moved = false;
    stage.addEventListener('pointerdown', function (e) { if (e.target.closest('.ticket,.lu-views,a,button')) { return; } drag = true; moved = false; sx = e.clientX; st0 = target; stage.classList.add('drag'); try { stage.setPointerCapture(e.pointerId); } catch (_) { /* */ } });
    stage.addEventListener('pointermove', function (e) { if (!drag) { return; } var dx = e.clientX - sx; if (Math.abs(dx) > 6) { moved = true; } if (view !== 'grid') { target = st0 - dx / (Sz * 0.9); kick(); } });
    function up() { if (!drag) { return; } drag = false; stage.classList.remove('drag'); target = Math.round(target); kick(); }
    stage.addEventListener('pointerup', up); stage.addEventListener('pointercancel', up);
    stage.addEventListener('keydown', function (e) {
      if (e.target !== stage) { return; }
      if (e.key === 'ArrowRight') { e.preventDefault(); target = Math.round(target) + 1; kick(); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); target = Math.round(target) - 1; kick(); }
      if (e.key === 'Enter') { location.href = Lst[idx()].url; }
    });
    function fit() { W = stage.clientWidth; H = stage.clientHeight; Sz = Math.round(Math.min(W * 0.62, H * 0.54, 430)); stage.style.setProperty('--S', Sz + 'px'); kick(); }
    fit(); window.addEventListener('resize', fit);
    if ('IntersectionObserver' in window) { new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) { kick(); } }).observe(stage); }
    var SX = [0, -0.62, 0.62, -1.18, 1.18, -0.32, 0.32, -0.9, 0.9], SR = [0, 1, 1, 2, 2, 3, 3, 4, 4];
    function slot(d) {
      if (d < 0) { var t = -d; return { x: 0, y: Sz * 0.1 * t, z: Sz * 1.3 * t, s: 1, b: 5 * t, o: 1 - t }; }
      var a = Math.floor(d), f = d - a, b2 = Math.min(a + 1, N - 1);
      function one(n) { var r = SR[n] || 4; return { x: (SX[n] || 0) * Sz * 0.95, y: -r * Sz * 0.06, z: -r * Sz * 0.95, s: 1, b: r * 2.2, o: Math.max(0, 1 - r * 0.13) }; }
      var p = one(a), q = one(b2); return { x: p.x + (q.x - p.x) * f, y: p.y + (q.y - p.y) * f, z: p.z + (q.z - p.z) * f, s: 1, b: p.b + (q.b - p.b) * f, o: p.o + (q.o - p.o) * f };
    }
    var c = 0, raf = 0;
    function kick() { if (!raf && visible) { raf = requestAnimationFrame(frame); } }
    function frame() {
      raf = 0;
      c = reduce ? target : c + (target - c) * 0.12;
      var k0 = idx(); if (k0 !== shown && !drag) { shown = k0; showInfo(k0); }
      var narrow = W < 760, still = true;
      els.forEach(function (e, k) {
        var g;
        if (view === 'grid') { var col = k % 3, row = Math.floor(k / 3), gs = narrow ? 0.42 : 0.5; g = { x: (col - 1) * Sz * (narrow ? 0.5 : 0.82), y: (row - 1) * Sz * (narrow ? 0.62 : 0.6) + Sz * 0.02, z: 0, s: gs, b: 0, o: 1 }; }
        else {
          var d = ((k - c) % N + N) % N; if (d > N - 1) { d -= N; }
          g = slot(d);
          if (view === 'focus') {
            if (k === (((Math.round(c) % N) + N) % N) && Math.abs(d) < 0.5) { g = { x: narrow ? 0 : -Sz * 0.18, y: narrow ? -Sz * 0.14 : 0, z: 0, s: narrow ? 1 : 1.15, b: d * d * 8, o: 1 - Math.abs(d) }; }
            else { g.z -= Sz * 2.5; g.o = 0; }
          }
        }
        var o = st[k], lf = reduce ? 1 : 0.12;
        ['x', 'y', 'z', 's', 'b', 'o'].forEach(function (key) { var dv = g[key] - o[key]; o[key] += dv * lf; if (Math.abs(dv) > 0.01) { still = false; } });
        e.style.transform = 'translate3d(' + o.x.toFixed(1) + 'px,' + o.y.toFixed(1) + 'px,' + o.z.toFixed(1) + 'px) scale(' + o.s.toFixed(3) + ')';
        e.style.filter = o.b > 0.15 ? 'blur(' + o.b.toFixed(1) + 'px)' : 'none';
        e.style.opacity = clamp(o.o, 0, 1).toFixed(3);
        e.style.zIndex = String(1000 + Math.round(o.z));
        e.style.pointerEvents = o.o > 0.3 ? 'auto' : 'none';
      });
      if (!still || Math.abs(target - c) > 0.001 || drag) { kick(); }
    }
    if (window.innerWidth < 760) { setView('grid'); } else { setView('focus'); }
    labels(); S.onLang(function () { labels(); shown = -1; setView(view); });
    kick();
  })();

  /* =====================================================================
     4. Packagings réels
     ===================================================================== */
  (function () {
    var scene = $('packshot'); if (!scene) { return; }
    var LBL = { f: ['Femme', 'For her'], h: ['Homme', 'For him'], 'noel-f': ['Noël · Femme', 'Christmas · Her'], 'noel-h': ['Noël · Homme', 'Christmas · Him'] };
    var cur = S.period() === 'hors' ? 'f' : 'noel-f';
    function setPack(v) {
      cur = v;
      scene.querySelectorAll('img').forEach(function (im) { im.classList.toggle('on', im.dataset.pack === v); });
      $('pkTag').textContent = T(LBL[v][0], LBL[v][1]);
      document.querySelectorAll('.pack-switch .chip').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.pack === v)); });
    }
    document.querySelectorAll('.pack-switch .chip').forEach(function (b) { b.addEventListener('click', function () { setPack(b.dataset.pack); }); });
    S.onLang(function () { setPack(cur); });
    setPack(cur);
  })();
})();
