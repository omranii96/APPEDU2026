/**
 * CHARMED PARIS — carrousel de coffrets (anneau photo). Anime le DOM rendu par le serveur
 * (vrais produits WooCommerce) ; sans JS, la liste reste une rangée défilante de fiches.
 * Ajout au panier : liens [data-cp-add] gérés par cart.js. ES2018.
 */
(function () {
	'use strict';

	var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	function init(root) {
		var stage = root.querySelector('.cp-cof__stage');
		var ring = root.querySelector('.cp-cof__ring');
		var items = Array.prototype.slice.call(ring.children);
		var N = items.length;
		if (N < 2) { return; }

		var text = root.querySelector('.cp-cof__text');
		var dots = root.querySelector('.cp-cof__dots');
		var hand = root.querySelector('.cp-cof__hand');
		var W = 1, H = 1, B = 360, Rx = 400;
		var c = 0, target = 0, dragging = false, sx = 0, st0 = 0, moved = false, front = -1, touched = false, visible = true, openTimer = 0, raf = 0;

		root.classList.add('is-ring');

		function idx(v) { return ((Math.round(v) % N) + N) % N; }
		function interact() { if (!touched) { touched = true; if (hand) { hand.style.opacity = '0'; } } }
		function goTo(k) {
			var cur = Math.round(target), d = ((k - idx(target)) % N + N) % N;
			if (d > N / 2) { d -= N; }
			target = cur + d; interact(); start();
		}

		items.forEach(function (e, k) {
			// Le panneau d'info porte le contenu accessible ; les coffrets sont décoratifs en mode anneau.
			e.setAttribute('aria-hidden', 'true');
			e.querySelectorAll('a,button').forEach(function (el) { el.tabIndex = -1; });
			e.addEventListener('click', function (ev) {
				ev.preventDefault();
				if (!moved) { goTo(k); }
			});
			var d = document.createElement('button');
			d.type = 'button';
			d.setAttribute('aria-label', (e.querySelector('.cp-cof__name') || e).textContent.trim());
			d.addEventListener('click', function () { goTo(k); });
			dots.appendChild(d);
		});

		function copy(sel, from) {
			var src = from.querySelector(sel), dst = text.querySelector(sel);
			if (src && dst) { dst.innerHTML = src.innerHTML; }
		}
		function setInfo(k) {
			var card = items[k].querySelector('.cp-cof__card');
			copy('.cp-cof__tag', card);
			copy('.cp-cof__name', card);
			copy('.cp-cof__line', card);
			copy('.cp-price', card);
			var src = card.querySelector('.cp-cof__add'), dst = text.querySelector('.cp-cof__add');
			if (src && dst) {
				var clone = src.cloneNode(true);
				clone.removeAttribute('tabindex');
				dst.parentNode.replaceChild(clone, dst);
			}
			text.querySelectorAll('a').forEach(function (a) { a.removeAttribute('tabindex'); });
			Array.prototype.forEach.call(dots.children, function (d, i) { d.setAttribute('aria-current', i === k ? 'true' : 'false'); });
		}

		root.querySelector('.cp-cof__prev').addEventListener('click', function () { target = Math.round(target) - 1; interact(); start(); });
		root.querySelector('.cp-cof__next').addEventListener('click', function () { target = Math.round(target) + 1; interact(); start(); });
		stage.addEventListener('keydown', function (e) {
			if (e.key === 'ArrowRight') { e.preventDefault(); target = Math.round(target) + 1; interact(); start(); }
			if (e.key === 'ArrowLeft') { e.preventDefault(); target = Math.round(target) - 1; interact(); start(); }
		});
		stage.addEventListener('pointerdown', function (e) {
			dragging = true; moved = false; sx = e.clientX; st0 = target;
			stage.classList.add('is-drag');
			try { stage.setPointerCapture(e.pointerId); } catch (_) { /* rien */ }
			start();
		});
		stage.addEventListener('pointermove', function (e) {
			if (!dragging) { return; }
			var dx = e.clientX - sx;
			if (Math.abs(dx) > 5) { moved = true; interact(); }
			target = st0 - dx / (Rx * 0.75);
		});
		function release() {
			if (!dragging) { return; }
			dragging = false; stage.classList.remove('is-drag');
			target = Math.round(target); start();
		}
		stage.addEventListener('pointerup', release);
		stage.addEventListener('pointercancel', release);
		var wt = 0;
		stage.addEventListener('wheel', function (e) {
			if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
				e.preventDefault(); target += e.deltaX / 350; interact(); start();
				clearTimeout(wt); wt = setTimeout(function () { target = Math.round(target); start(); }, 140);
			}
		}, { passive: false });

		function fit() {
			W = stage.clientWidth; H = stage.clientHeight;
			B = Math.round(Math.min(W * 0.46, H * 0.72, 420));
			Rx = Math.min(W * 0.44, 560);
			stage.style.setProperty('--B', B + 'px');
			start();
		}
		fit();
		window.addEventListener('resize', fit);
		if ('IntersectionObserver' in window) {
			new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) { start(); } }).observe(stage);
		}

		function start() { if (!raf && visible) { raf = requestAnimationFrame(tick); } }
		function tick() {
			raf = 0;
			c = reduce ? target : c + (target - c) * 0.1;
			var k0 = idx(c);
			if (k0 !== front) { front = k0; setInfo(k0); }
			items.forEach(function (e, k) {
				var th = (k - c) / N * Math.PI * 2, z = Math.cos(th), t = (z + 1) / 2;
				var sc = 0.3 + 0.7 * Math.pow(t, 2.2), x = Math.sin(th) * Rx, y = -(1 - t) * H * 0.22;
				e.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0) scale(' + sc.toFixed(3) + ')';
				var bl = (1 - t) * 3.2;
				e.style.filter = (bl > 0.2 ? 'blur(' + bl.toFixed(1) + 'px) ' : '') + 'brightness(' + (0.55 + 0.45 * t).toFixed(2) + ')';
				e.style.zIndex = String(Math.round(t * 100));
				e.style.opacity = (0.35 + 0.65 * t).toFixed(2);
			});
			var settled = !dragging && Math.abs(target - c) < 0.02 && target === Math.round(target);
			items.forEach(function (e, k) {
				if (e.classList.contains('is-open') && !(settled && k === idx(target))) { e.classList.remove('is-open'); }
			});
			if (settled && !items[idx(target)].classList.contains('is-open') && !openTimer) {
				openTimer = setTimeout(function () {
					openTimer = 0;
					if (!dragging && Math.abs(target - c) < 0.02) { items[idx(target)].classList.add('is-open'); }
				}, 150);
			}
			if (!settled || Math.abs(target - c) > 0.0005) { start(); } else { c = target; }
		}
		setInfo(0);
		start();
	}

	document.querySelectorAll('.cp-cof').forEach(init);
})();
