/**
 * CHARMED PARIS — ajout au vrai panier WooCommerce (Store API), sans rechargement.
 *
 * Amélioration progressive : chaque bouton est un lien natif « ?add-to-cart=ID » qui fonctionne
 * sans JS. Avec JS : POST /wc/store/v1/cart/add-item, puis événement « wc-blocks_added_to_cart »
 * (le bloc Mini-panier se met à jour et s'ouvre), et message de confirmation.
 * En cas d'échec (stock, nonce, réseau) : on suit le lien natif, WooCommerce affiche la raison.
 * ES2018, sans dépendance.
 */
(function () {
	'use strict';

	var cfg = window.charmedCart || {};
	var i18n = cfg.i18n || {};
	var nonce = cfg.nonce || '';
	var toastEl = null;
	var toastTimer = 0;

	function toast(message) {
		if (!toastEl) {
			toastEl = document.createElement('div');
			toastEl.className = 'cp-toast';
			toastEl.setAttribute('role', 'status');
			toastEl.setAttribute('aria-live', 'polite');
			document.body.appendChild(toastEl);
		}
		toastEl.textContent = message;
		if (cfg.cartUrl) {
			var link = document.createElement('a');
			link.href = cfg.cartUrl;
			link.textContent = i18n.viewCart || 'Panier';
			toastEl.appendChild(document.createTextNode(' '));
			toastEl.appendChild(link);
		}
		toastEl.classList.add('is-on');
		clearTimeout(toastTimer);
		toastTimer = setTimeout(function () { toastEl.classList.remove('is-on'); }, 3200);
	}

	function keepNonce(res) {
		var n = res.headers.get('Nonce');
		if (n) { nonce = n; }
		return res;
	}

	// GET /cart ne demande pas de nonce et en renvoie un frais : utile quand la page vient du cache.
	function refreshNonce() {
		return fetch(cfg.api + 'cart', { credentials: 'same-origin' }).then(keepNonce);
	}

	function post(path, body, retried) {
		return fetch(cfg.api + path, {
			method: 'POST',
			credentials: 'same-origin',
			headers: { 'Content-Type': 'application/json', 'Nonce': nonce },
			body: JSON.stringify(body)
		}).then(keepNonce).then(function (res) {
			if ((res.status === 401 || res.status === 403) && !retried) {
				return refreshNonce().then(function () { return post(path, body, true); });
			}
			if (!res.ok) { throw new Error('store-api-' + res.status); }
			return res.json();
		});
	}

	function addToCart(id, quantity) {
		return post('cart/add-item', { id: id, quantity: quantity || 1 });
	}

	function notify(cart) {
		document.body.dispatchEvent(new CustomEvent('wc-blocks_added_to_cart', {
			bubbles: true,
			cancelable: true,
			detail: { preserveCartData: false }
		}));
		// Thèmes/widgets classiques éventuels : rafraîchissement sûr des fragments.
		if (window.jQuery) { window.jQuery(document.body).trigger('wc_fragment_refresh'); }
		if (cart && typeof cart.items_count === 'number') {
			document.querySelectorAll('[data-cp-cart-count]').forEach(function (el) {
				el.textContent = String(cart.items_count);
			});
		}
	}

	document.addEventListener('click', function (e) {
		var a = e.target && e.target.closest ? e.target.closest('a[data-cp-add]') : null;
		if (!a || !cfg.api || !window.fetch) { return; }
		if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) { return; }
		e.preventDefault();
		if (a.getAttribute('aria-busy') === 'true') { return; }

		var id = parseInt(a.getAttribute('data-cp-add'), 10);
		var name = a.getAttribute('data-cp-name') || '';
		var label = a.textContent;
		a.setAttribute('aria-busy', 'true');
		a.textContent = i18n.adding || '…';

		addToCart(id, 1).then(function (cart) {
			a.removeAttribute('aria-busy');
			a.textContent = label;
			notify(cart);
			toast((i18n.added || '%s').replace('%s', name));
		}).catch(function () {
			window.location.href = a.href; // Repli natif : WooCommerce ajoute ou explique le refus.
		});
	});

	window.charmedAddToCart = addToCart;
})();
