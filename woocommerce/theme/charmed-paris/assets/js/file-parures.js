/**
 * CHARMED PARIS — « La file des parures » : vues Une / La file / Toutes, étiquette (ticket).
 * Anime le DOM rendu par le serveur (vrais produits) ; sans JS : grille de fiches avec liens
 * et boutons d'ajout natifs. Ajout au panier : liens [data-cp-add] gérés par cart.js. ES2018.
 */
(function () {
	'use strict';

	var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	function init(root) {
		var stage = root.querySelector('.cp-file__stage');
		var host = root.querySelector('.cp-file__items');
		var els = Array.prototype.slice.call(host.children);
		var N = els.length;
		if (!N) { return; }

		var rail = root.querySelector('.cp-file__rail');
		var big = root.querySelector('.cp-file__big');
		var meta = root.querySelector('.cp-file__meta');
		var hint = root.querySelector('.cp-file__hint');
		var tag = root.querySelector('.cp-ticket');
		var T = function (k) { return tag.querySelector('[data-t="' + k + '"]'); };
		var rowsEl = T('rows');
		var extraRow = rowsEl ? rowsEl.querySelector('.cp-ticket__extra') : null;
		var included = rowsEl ? rowsEl.getAttribute('data-included') : '';
		var hintDefault = hint ? hint.textContent : '';

		var view = 'focus', target = 0, S = 360, W = 1, H = 1, visible = true, shown = -1, raf = 0, c = 0;
		var st = els.map(function () { return { x: 0, y: 0, z: -3000, s: 1, b: 10, o: 0 }; });
		var drag = false, sx = 0, st0 = 0, moved = false;

		root.classList.add('is-live');

		function idx() { return ((Math.round(target) % N) + N) % N; }
		function jump(k) {
			var cur = Math.round(target), d = ((k - idx()) % N + N) % N;
			if (d > N / 2) { d -= N; }
			target = cur + d; start();
		}
		function setView(v) {
			view = v;
			root.classList.toggle('is-focus', v === 'focus');
			root.classList.toggle('is-grid', v === 'grid');
			root.querySelectorAll('.cp-file__views button').forEach(function (b) {
				b.setAttribute('aria-pressed', b.getAttribute('data-v') === v ? 'true' : 'false');
			});
			if (hint) { hint.textContent = v === 'grid' ? hint.getAttribute('data-grid') : hintDefault; }
			if (v === 'focus') { scanNow(); }
			start();
		}
		root.querySelectorAll('.cp-file__views button').forEach(function (b) {
			b.addEventListener('click', function () { setView(b.getAttribute('data-v')); });
		});

		function scanNow() {
			var e = els[idx()];
			e.classList.remove('is-scanning');
			void e.offsetWidth;
			e.classList.add('is-scanning');
		}

		els.forEach(function (e, k) {
			e.querySelectorAll('.cp-file__fb a').forEach(function (a) { a.tabIndex = -1; });
			e.addEventListener('click', function (ev) {
				ev.preventDefault();
				if (moved) { return; }
				if (view === 'focus' && k === idx()) { return; }
				if (view === 'grid') { jump(k); setView('focus'); } else if (k === idx()) { setView('focus'); } else { jump(k); }
			});
			var r = document.createElement('button');
			r.type = 'button';
			r.textContent = e.getAttribute('data-no');
			r.setAttribute('aria-label', e.getAttribute('data-short'));
			r.addEventListener('click', function () { jump(k); });
			rail.appendChild(r);
		});

		function showInfo(k) {
			var e = els[k];
			var no = e.getAttribute('data-no');
			var short = e.getAttribute('data-short');
			big.classList.add('is-out');
			setTimeout(function () {
				big.textContent = short;
				meta.textContent = no + ' · ' + (e.getAttribute('data-univers') || '');
				big.classList.remove('is-out');
			}, reduce ? 0 : 180);

			T('no').textContent = no;
			T('code').textContent = e.getAttribute('data-code');
			T('name').textContent = short;
			if (rowsEl) {
				Array.prototype.slice.call(rowsEl.children).forEach(function (li) { if (li !== extraRow) { rowsEl.removeChild(li); } });
				var pieces = [];
				try { pieces = JSON.parse(e.getAttribute('data-pieces') || '[]'); } catch (_) { pieces = []; }
				pieces.forEach(function (p) {
					var li = document.createElement('li');
					var a = document.createElement('span'); a.textContent = p;
					var b = document.createElement('span'); b.textContent = included;
					li.appendChild(a); li.appendChild(b);
					rowsEl.insertBefore(li, extraRow);
				});
			}
			var price = e.querySelector('.cp-file__fb .cp-price');
			T('price').innerHTML = price ? price.innerHTML : '';
			var sku = e.getAttribute('data-sku');
			T('sku').textContent = (sku ? sku + ' · ' : '') + 'CHARMED PARIS';
			var src = e.querySelector('.cp-file__fb .cp-btn');
			var slot = T('add');
			if (src && slot) {
				var clone = src.cloneNode(true);
				clone.className = 'cp-ticket__add';
				clone.removeAttribute('tabindex');
				slot.innerHTML = '';
				slot.appendChild(clone);
			}
			tag.classList.remove('is-swap'); void tag.offsetWidth; tag.classList.add('is-swap');
			Array.prototype.forEach.call(rail.children, function (x, i) { x.setAttribute('aria-current', i === k ? 'true' : 'false'); });
			if (view === 'focus') { scanNow(); }
		}

		stage.addEventListener('pointerdown', function (e) {
			if (e.target.closest('.cp-ticket,.cp-file__views,.cp-file__rail')) { return; }
			drag = true; moved = false; sx = e.clientX; st0 = target;
			stage.classList.add('is-drag');
			try { stage.setPointerCapture(e.pointerId); } catch (_) { /* rien */ }
		});
		stage.addEventListener('pointermove', function (e) {
			if (!drag) { return; }
			var dx = e.clientX - sx;
			if (Math.abs(dx) > 6) { moved = true; }
			if (view !== 'grid') { target = st0 - dx / (S * 0.9); start(); }
		});
		function up() {
			if (!drag) { return; }
			drag = false; stage.classList.remove('is-drag');
			target = Math.round(target); start();
			setTimeout(function () { moved = false; }, 0);
		}
		stage.addEventListener('pointerup', up);
		stage.addEventListener('pointercancel', up);
		stage.addEventListener('keydown', function (e) {
			if (e.target.closest('.cp-ticket')) { return; }
			if (e.key === 'ArrowRight') { e.preventDefault(); target = Math.round(target) + 1; start(); }
			if (e.key === 'ArrowLeft') { e.preventDefault(); target = Math.round(target) - 1; start(); }
			if (e.key === 'Enter' && e.target === stage) { setView('focus'); }
		});
		var wt = 0;
		stage.addEventListener('wheel', function (e) {
			if (view !== 'grid' && Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
				e.preventDefault(); target += e.deltaX / 400; start();
				clearTimeout(wt); wt = setTimeout(function () { target = Math.round(target); start(); }, 140);
			}
		}, { passive: false });

		function fit() {
			W = stage.clientWidth; H = stage.clientHeight;
			S = Math.round(Math.min(W * 0.62, H * 0.56, 440));
			stage.style.setProperty('--S', S + 'px');
			start();
		}
		fit();
		window.addEventListener('resize', fit);
		if ('IntersectionObserver' in window) {
			new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) { start(); } }).observe(stage);
		}

		var SX = [0, -0.62, 0.62, -1.18, 1.18, -0.32, 0.32, -0.9, 0.9], SR = [0, 1, 1, 2, 2, 3, 3, 4, 4];
		function one(n) {
			var r = SR[n] || 4;
			return { x: (SX[n] || 0) * S * 0.95, y: -r * S * 0.06, z: -r * S * 0.95, s: 1, b: r * 2.2, o: Math.max(0, 1 - r * 0.13) };
		}
		function slot(d) {
			if (d < 0) { var t = -d; return { x: 0, y: S * 0.1 * t, z: S * 1.3 * t, s: 1, b: 5 * t, o: 1 - t }; }
			var a = Math.floor(d), f = d - a, b2 = Math.min(a + 1, N - 1);
			var p = one(a), q = one(b2);
			return { x: p.x + (q.x - p.x) * f, y: p.y + (q.y - p.y) * f, z: p.z + (q.z - p.z) * f, s: 1, b: p.b + (q.b - p.b) * f, o: p.o + (q.o - p.o) * f };
		}

		function start() { if (!raf && visible) { raf = requestAnimationFrame(frame); } }
		function frame() {
			raf = 0;
			c = reduce ? target : c + (target - c) * 0.12;
			var k0 = idx();
			if (k0 !== shown && !drag) { shown = k0; showInfo(k0); }
			var narrow = W < 760, moving = Math.abs(target - c) > 0.001;
			els.forEach(function (e, k) {
				var g;
				if (view === 'grid') {
					var col = k % 3, row = Math.floor(k / 3), gs = narrow ? 0.42 : 0.5;
					g = { x: (col - 1) * S * (narrow ? 0.5 : 0.82), y: (row - 1) * S * (narrow ? 0.62 : 0.6) + S * 0.02, z: 0, s: gs, b: 0, o: 1 };
				} else {
					var d = ((k - c) % N + N) % N;
					if (d > N - 1) { d -= N; }
					g = slot(d);
					if (view === 'focus') {
						if (k === ((Math.round(c) % N) + N) % N && Math.abs(d) < 0.5) {
							g = { x: narrow ? 0 : -S * 0.18, y: narrow ? -S * 0.12 : 0, z: 0, s: narrow ? 1.02 : 1.18, b: d * d * 8, o: 1 - Math.abs(d) };
						} else { g.z -= S * 2.5; g.o = 0; }
					}
				}
				var o = st[k], lf = reduce ? 1 : 0.11;
				['x', 'y', 'z', 's', 'b', 'o'].forEach(function (p) {
					var delta = g[p] - o[p];
					if (Math.abs(delta) > 0.01) { moving = true; }
					o[p] += delta * lf;
				});
				e.style.transform = 'translate3d(' + o.x.toFixed(1) + 'px,' + o.y.toFixed(1) + 'px,' + o.z.toFixed(1) + 'px) scale(' + o.s.toFixed(3) + ')';
				e.style.filter = o.b > 0.15 ? 'blur(' + o.b.toFixed(1) + 'px)' : 'none';
				e.style.opacity = Math.max(0, Math.min(1, o.o)).toFixed(3);
				e.style.zIndex = String(1000 + Math.round(o.z));
				e.style.pointerEvents = o.o > 0.3 ? 'auto' : 'none';
			});
			if (moving || drag) { start(); }
		}
		start();
	}

	document.querySelectorAll('.cp-file').forEach(init);
})();
