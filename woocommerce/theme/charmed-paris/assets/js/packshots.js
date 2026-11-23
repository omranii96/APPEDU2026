/**
 * CHARMED PARIS — sélecteur de packagings (Femme / Homme / Noël) et léger zoom au scroll.
 * Sans JS : la première photo reste affichée, les boutons sont masqués.
 */
(function () {
	'use strict';
	document.querySelectorAll('.cp-pack').forEach(function (root) {
		var shot = root.querySelector('.cp-pack__shot');
		var tag = root.querySelector('.cp-pack__tag');
		var buttons = root.querySelectorAll('.cp-pack__switch button');
		root.classList.add('is-ready');

		function set(key) {
			shot.querySelectorAll('img').forEach(function (img) {
				var on = img.getAttribute('data-pack') === key;
				if (on && img.loading === 'lazy') { img.loading = 'eager'; }
				img.classList.toggle('is-on', on);
			});
			buttons.forEach(function (b) {
				var on = b.getAttribute('data-pack') === key;
				b.setAttribute('aria-pressed', on ? 'true' : 'false');
				if (on && tag) { tag.textContent = b.textContent; }
			});
		}
		buttons.forEach(function (b) {
			b.addEventListener('click', function () { set(b.getAttribute('data-pack')); });
		});

		var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		if (reduce || !('IntersectionObserver' in window)) { return; }
		var visible = false;
		var ticking = false;
		function zoom() {
			ticking = false;
			var r = shot.getBoundingClientRect();
			var vh = window.innerHeight;
			var t = Math.min(1, Math.max(0, (vh - r.top) / (vh * 0.9)));
			var e = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
			shot.style.setProperty('--z', (0.12 * (1 - e)).toFixed(3));
		}
		new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; if (visible) { zoom(); } }).observe(shot);
		window.addEventListener('scroll', function () {
			if (visible && !ticking) { ticking = true; requestAnimationFrame(zoom); }
		}, { passive: true });
	});
})();
