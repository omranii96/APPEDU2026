/**
 * CHARMED PARIS — en-tête : transparent sur l'intro de l'accueil, plein dès qu'on la quitte.
 * Sans JS ou sans intro : en-tête plein (CSS par défaut).
 */
(function () {
	'use strict';
	var header = document.querySelector('.cp-header');
	var intro = document.querySelector('.cp-intro');
	if (!header) { return; }
	if (!intro) { header.classList.add('is-solid'); return; }

	var ticking = false;
	function update() {
		ticking = false;
		header.classList.toggle('is-solid', intro.getBoundingClientRect().bottom < 70);
	}
	window.addEventListener('scroll', function () {
		if (!ticking) { ticking = true; requestAnimationFrame(update); }
	}, { passive: true });
	update();
})();
