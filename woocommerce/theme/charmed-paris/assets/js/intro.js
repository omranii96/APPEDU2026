/**
 * CHARMED PARIS — intro « écrin » pilotée au scroll (accueil uniquement, chargé en defer).
 *
 *  - Ne fait rien si prefers-reduced-motion, trafic publicitaire (classe cp-ad) ou pas de mode film :
 *    le héros statique rendu par le serveur reste affiché.
 *  - Anime d'abord le DOM (parenthèses du logo, textes) avec un anneau CSS de repli.
 *  - Télécharge Three.js r128 (auto-hébergé) seulement à la première interaction ou sur temps mort,
 *    jamais si Save-Data, mémoire < 2 Go ou WebGL indisponible ; version allégée sur mobile.
 *  - Boucle d'animation arrêtée quand l'intro est hors écran ou l'onglet caché.
 * ES2018, sans dépendance.
 */
(function () {
	'use strict';

	var root = document.querySelector('.cp-intro[data-film]');
	var html = document.documentElement;
	if (!root || !html.classList.contains('cp-motion') || html.classList.contains('cp-ad')) { return; }

	var q = function (sel) { return root.querySelector(sel); };
	var stage = q('.cp-intro__stage');
	var logo = q('.cp-intro__logo');
	var brL = q('.cp-intro__logo .cp-br--l');
	var brR = q('.cp-intro__logo .cp-br--r');
	var mid = q('.cp-intro__mid');
	var paris = q('.cp-intro__paris');
	var glow = q('.cp-intro__glow');
	var tOpen = q('.cp-intro__open');
	var t1 = q('.cp-intro__t1');
	var t2 = q('.cp-intro__t2');
	var fin = q('.cp-intro__final');
	var hint = q('.cp-intro__hint');
	var prog = q('.cp-intro__prog i');
	var ring = q('.cp-intro__ring');
	var poster = q('.cp-intro__poster');
	var canvas = q('.cp-intro__gl');

	root.classList.add('is-film');

	var small = window.innerWidth < 700 || (window.matchMedia && window.matchMedia('(pointer: coarse)').matches);
	var FOV = 35;
	var TAN = Math.tan(FOV / 2 * Math.PI / 180);

	function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }
	function seg(p, a, b) { return clamp((p - a) / (b - a), 0, 1); }
	function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
	function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
	function lerp(a, b, t) { return a + (b - a) * t; }
	function band(p, a, b, c, d) { return seg(p, a, b) * (1 - seg(p, c, d)); }

	/* ---------- Three.js (chargé à la demande) ---------- */
	var G = null;

	function canUseGL() {
		var conn = navigator.connection || {};
		if (conn.saveData) { return false; }
		if (navigator.deviceMemory && navigator.deviceMemory < 2) { return false; }
		try {
			var c = document.createElement('canvas');
			return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl')));
		} catch (e) { return false; }
	}

	function makeEnv(THREE, renderer) {
		var w = small ? 512 : 1024;
		var h = w / 2;
		var c = document.createElement('canvas');
		c.width = w; c.height = h;
		var x = c.getContext('2d');
		var g = x.createLinearGradient(0, 0, 0, h);
		g.addColorStop(0, '#8a7a80'); g.addColorStop(0.45, '#2a2026'); g.addColorStop(1, '#0a0708');
		x.fillStyle = g; x.fillRect(0, 0, w, h);
		x.filter = 'blur(' + (small ? 7 : 14) + 'px)';
		var k = w / 1024;
		[[0, 0, 1024, 40, '#ffffff'], [260, 60, 340, 130, '#ffffff'], [660, 120, 260, 90, '#ffe6b8'], [60, 180, 160, 220, '#f8e4ea'], [840, 220, 150, 180, '#ffffff'], [420, 300, 300, 60, '#c9a6b0']].forEach(function (r) {
			x.fillStyle = r[4]; x.fillRect(r[0] * k, r[1] * k, r[2] * k, r[3] * k);
		});
		x.filter = 'none';
		var t = new THREE.CanvasTexture(c);
		t.mapping = THREE.EquirectangularReflectionMapping;
		t.encoding = THREE.sRGBEncoding;
		var pm = new THREE.PMREMGenerator(renderer);
		var env = pm.fromEquirectangular(t).texture;
		t.dispose(); pm.dispose();
		return env;
	}

	function spriteTex(THREE, kind) {
		var s = 128;
		var c = document.createElement('canvas');
		c.width = c.height = s;
		var x = c.getContext('2d');
		var g = x.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2);
		g.addColorStop(0, 'rgba(255,255,255,1)');
		g.addColorStop(kind === 'star' ? 0.08 : 0.25, 'rgba(255,240,210,.7)');
		g.addColorStop(1, 'rgba(255,240,210,0)');
		x.fillStyle = g; x.fillRect(0, 0, s, s);
		if (kind === 'star') {
			x.globalCompositeOperation = 'lighter';
			[[s, 3], [3, s]].forEach(function (d) {
				var horiz = d[0] === s;
				var lg = x.createLinearGradient(horiz ? 0 : s / 2, horiz ? s / 2 : 0, horiz ? s : s / 2, horiz ? s / 2 : s);
				lg.addColorStop(0, 'rgba(255,255,255,0)'); lg.addColorStop(0.5, 'rgba(255,255,255,1)'); lg.addColorStop(1, 'rgba(255,255,255,0)');
				x.fillStyle = lg; x.fillRect((s - d[0]) / 2, (s - d[1]) / 2, d[0], d[1]);
			});
		}
		return new THREE.CanvasTexture(c);
	}

	function setupGL(THREE) {
		var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: !small, alpha: true, powerPreference: small ? 'low-power' : 'high-performance' });
		if (!renderer.getContext()) { throw new Error('no gl'); }
		renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, small ? 1.5 : 2));
		renderer.outputEncoding = THREE.sRGBEncoding;
		renderer.toneMapping = THREE.ACESFilmicToneMapping;
		renderer.toneMappingExposure = 1.15;
		var scene = new THREE.Scene();
		scene.environment = makeEnv(THREE, renderer);
		var camera = new THREE.PerspectiveCamera(FOV, 1, 0.1, 100);
		camera.position.set(0, 0, 10);
		var gold = new THREE.MeshStandardMaterial({ color: 0xE8C27A, metalness: 1, roughness: 0.15 });
		var band3 = new THREE.Group();
		band3.add(new THREE.Mesh(new THREE.TorusGeometry(1, 0.11, small ? 24 : 48, small ? 120 : 220), gold));
		var head = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.09, 0.22, 32), gold);
		head.position.y = 1.16; band3.add(head);
		var prof = [[0, -0.36], [0.34, -0.02], [0.34, 0.03], [0.21, 0.15], [0, 0.15]].map(function (a) { return new THREE.Vector2(a[0], a[1]); });
		var gemMat = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 1, roughness: 0, flatShading: true, envMapIntensity: 4.5, emissive: 0x2b2530 });
		var gem = new THREE.Mesh(new THREE.LatheGeometry(prof, 16), gemMat);
		gem.position.y = 1.47; band3.add(gem);
		for (var i = 0; i < 4; i++) {
			var an = i * Math.PI / 2 + Math.PI / 4;
			var pr = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.022, 0.32, 8), gold);
			pr.position.set(Math.cos(an) * 0.27, 1.42, Math.sin(an) * 0.27);
			pr.rotation.z = -Math.cos(an) * 0.4; pr.rotation.x = Math.sin(an) * 0.4;
			band3.add(pr);
		}
		var starMat = new THREE.SpriteMaterial({ map: spriteTex(THREE, 'star'), color: 0xfff1d0, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0 });
		var star = new THREE.Sprite(starMat);
		star.scale.set(1.1, 1.1, 1); star.position.set(0.1, 1.56, 0.25); band3.add(star);
		var pivot = new THREE.Group();
		pivot.add(band3); band3.position.y = -0.25; scene.add(pivot);
		var dl = new THREE.DirectionalLight(0xfff3e0, 1.1);
		dl.position.set(3, 5, 4); scene.add(dl);
		var N = small ? 300 : 900;
		var pos = new Float32Array(N * 3);
		for (var k = 0; k < N; k++) {
			var r = 1.8 + Math.random() * 7, th = Math.random() * Math.PI * 2, ph = Math.acos(2 * Math.random() - 1);
			pos[k * 3] = r * Math.sin(ph) * Math.cos(th);
			pos[k * 3 + 1] = r * Math.cos(ph) * 0.8;
			pos[k * 3 + 2] = r * Math.sin(ph) * Math.sin(th) * 0.6;
		}
		var dg = new THREE.BufferGeometry();
		dg.setAttribute('position', new THREE.BufferAttribute(pos, 3));
		var dustMat = new THREE.PointsMaterial({ size: 0.06, map: spriteTex(THREE, 'dot'), color: 0xE9CB8F, transparent: true, opacity: 0.4, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true });
		var dust = new THREE.Points(dg, dustMat);
		scene.add(dust);
		return { renderer: renderer, scene: scene, camera: camera, pivot: pivot, starMat: starMat, dust: dust, dustMat: dustMat };
	}

	var loading = false;
	function loadThree() {
		if (loading || G || !root.dataset.three || !canUseGL()) { return; }
		loading = true;
		var done = function () {
			try {
				G = setupGL(window.THREE);
				root.classList.add('has-gl');
				measure();
				start();
			} catch (e) { G = null; }
		};
		if (window.THREE) { done(); return; }
		var s = document.createElement('script');
		s.src = root.dataset.three;
		s.async = true;
		s.onload = done;
		document.head.appendChild(s);
	}

	// Chargement après interaction ou temps mort (jamais pendant le rendu initial : LCP préservé).
	var triggers = ['scroll', 'wheel', 'pointerdown', 'touchstart', 'keydown'];
	function onFirst() {
		triggers.forEach(function (t) { window.removeEventListener(t, onFirst); });
		loadThree();
	}
	triggers.forEach(function (t) { window.addEventListener(t, onFirst, { passive: true, once: true }); });
	window.addEventListener('load', function () {
		var idle = window.requestIdleCallback || function (cb) { return setTimeout(cb, 2500); };
		idle(onFirst, { timeout: 4000 });
	});

	/* ---------- Mesures ---------- */
	var W = 1, H = 1, F = 100, midW = 300, zf = 1;
	function measure() {
		W = stage.clientWidth; H = stage.clientHeight;
		F = parseFloat(getComputedStyle(logo).fontSize) || 100;
		var ls = mid.style.letterSpacing, pl = mid.style.paddingLeft;
		mid.style.letterSpacing = '.08em'; mid.style.paddingLeft = '.08em';
		midW = mid.offsetWidth;
		mid.style.letterSpacing = ls; mid.style.paddingLeft = pl;
		var asp = W / H;
		zf = asp < 1 ? Math.min(1.9, 1.15 / asp) : 1;
		if (G) {
			G.renderer.setSize(W, H, false);
			G.camera.aspect = asp;
			G.camera.updateProjectionMatrix();
		}
	}
	measure();
	window.addEventListener('resize', function () { measure(); readScroll(); });

	/* ---------- Scroll et pointeur ---------- */
	var target = 0, sp = 0, px = 0, py = 0, mx = 0, my = 0;
	function readScroll() {
		var r = root.getBoundingClientRect();
		var total = root.offsetHeight - stage.offsetHeight;
		target = total > 0 ? clamp(-r.top / total, 0, 1) : 1;
	}
	window.addEventListener('scroll', function () { readScroll(); start(); }, { passive: true });
	readScroll();
	if (!small) {
		window.addEventListener('pointermove', function (e) {
			mx = (e.clientX / window.innerWidth) * 2 - 1;
			my = (e.clientY / window.innerHeight) * 2 - 1;
		}, { passive: true });
	}

	/* ---------- Boucle ---------- */
	var visible = true, raf = 0, t0 = performance.now();
	function start() { if (!raf && visible && !document.hidden) { raf = requestAnimationFrame(frame); } }
	function stop() { if (raf) { cancelAnimationFrame(raf); raf = 0; } }
	if ('IntersectionObserver' in window) {
		new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) { start(); } else { stop(); } }).observe(root);
	}
	document.addEventListener('visibilitychange', function () { if (document.hidden) { stop(); } else { start(); } });

	function frame(now) {
		raf = 0;
		var time = (now - t0) / 1000;
		sp += (target - sp) * 0.085;
		px += (mx - px) * 0.05; py += (my - py) * 0.05;
		var p = sp;
		var o = ease(seg(p, 0.10, 0.40)), c = ease(seg(p, 0.78, 0.95));
		var zEnd = 12 * zf, ringPx = 1.45 / (2 * zEnd * TAN) * H;
		logo.style.top = (46 - 9 * c) + '%';
		var fScale = clamp((2.1 * ringPx) / (0.7 * F), 0.6, 2.6);
		var closedX = midW / 2 + 0.32 * F, farX = W / 2 + 0.8 * F * 1.6, finalX = ringPx * 0.9 + 0.25 * F * fScale + 8;
		var x, a, s;
		if (c > 0) { x = lerp(farX, finalX, c); a = lerp(82, 0, c); s = lerp(1.6, fScale, c); }
		else { x = lerp(closedX, farX, o); a = lerp(0, 82, o); s = lerp(1, 1.6, o); }
		var breathe = (1 - o) * Math.sin(time * 1.6) * 0.012 * F + (1 - seg(p, 0, 0.04)) * Math.pow(Math.max(0, Math.sin(time * 1.3)), 10) * 0.22 * F;
		brL.style.transform = 'translate(-50%,-50%) translateX(' + (-x - breathe) + 'px) rotateY(' + (-a) + 'deg) scale(' + s + ')';
		brR.style.transform = 'translate(-50%,-50%) translateX(' + (x + breathe) + 'px) rotateY(' + a + 'deg) scale(' + s + ')';
		var ls = lerp(0.08, 0.95, o);
		mid.style.letterSpacing = ls + 'em'; mid.style.paddingLeft = ls + 'em';
		mid.style.opacity = String(1 - seg(p, 0.14, 0.34));
		mid.style.filter = 'blur(' + (o * 10).toFixed(2) + 'px)';
		if (paris) { paris.style.opacity = String(1 - seg(p, 0.06, 0.18)); }
		glow.style.opacity = String(clamp(seg(p, 0.12, 0.38) * (1 - 0.6 * seg(p, 0.62, 0.8)) + 0.45 * c, 0, 1));
		glow.style.transform = 'scale(' + (1 + 0.25 * o - 0.15 * c) + ')';
		tOpen.style.opacity = String(1 - seg(p, 0.03, 0.12));
		var b1 = band(p, 0.45, 0.51, 0.59, 0.64), b2 = band(p, 0.61, 0.66, 0.73, 0.78);
		t1.style.opacity = String(b1); t1.style.transform = 'translateX(-50%) translateY(' + ((1 - b1) * 18) + 'px)';
		t2.style.opacity = String(b2); t2.style.transform = 'translateX(-50%) translateY(' + ((1 - b2) * -18) + 'px)';
		var bf = seg(p, 0.88, 0.97);
		fin.style.opacity = String(bf);
		fin.style.transform = 'translateX(-50%) translateY(' + ((1 - bf) * 16) + 'px)';
		fin.style.pointerEvents = bf > 0.5 ? 'auto' : 'none';
		fin.style.visibility = bf > 0.01 ? 'visible' : 'hidden';
		if (hint) { hint.style.opacity = String(1 - seg(p, 0, 0.05)); }
		if (prog) { prog.style.transform = 'scaleX(' + p + ')'; }
		var r = easeOut(seg(p, 0.24, 0.50));
		if (poster) { poster.style.opacity = String(G ? 0 : r); }
		if (G) {
			var macro = band(p, 0.44, 0.60, 0.66, 0.84);
			var z = p < 0.64 ? lerp(10, 3.2, ease(seg(p, 0.30, 0.62))) : lerp(3.2, 12, ease(seg(p, 0.66, 0.86)));
			var zz = z * zf, off = c * 0.09 * 2 * zz * TAN;
			G.camera.position.set(px * 0.25 * (1 - macro), 1.25 * macro + (-py) * 0.15 - off, zz);
			G.camera.lookAt(0, 1.05 * macro - off, 0);
			G.pivot.position.y = lerp(-4.4, 0, r);
			G.pivot.scale.setScalar(lerp(0.6, 1, r));
			G.pivot.rotation.y = time * 0.22 + p * Math.PI * 2.4 + px * 0.35;
			G.pivot.rotation.x = py * 0.18 + 0.32 * macro;
			G.starMat.opacity = seg(p, 0.40, 0.55) * (0.25 + 0.75 * Math.pow(Math.max(0, Math.sin(time * 2.1)), 10));
			G.starMat.rotation = time * 0.4;
			G.dust.rotation.y = time * 0.025 + p * 0.7;
			G.dust.scale.setScalar(1 + 1.3 * easeOut(seg(p, 0.18, 0.5)));
			G.dustMat.opacity = 0.3 + 0.55 * seg(p, 0.12, 0.4);
			G.renderer.toneMappingExposure = 1.1 + 0.35 * band(p, 0.2, 0.35, 0.45, 0.6);
			G.renderer.render(G.scene, G.camera);
		} else if (ring) {
			ring.style.opacity = String(r);
			ring.style.transform = 'translate(-50%,-50%) scale(' + lerp(0.5, 1, r) * (1 + 0.4 * band(p, 0.44, 0.6, 0.66, 0.84)) + ')';
		}
		// Sans WebGL et une fois la scène immobile, on arrête la boucle (rien ne bouge plus).
		var settled = Math.abs(target - sp) < 0.0005;
		if (G || !settled || p < 0.04) { start(); }
	}
	start();
})();
