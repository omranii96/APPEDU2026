/* =====================================================================
   CHARMED PARIS · prototype · site.js (toutes les pages, chargé en defer)
   i18n FR/EN · panier partagé (localStorage) · tiroir « Ton écrin » ·
   recherche · grilles + filtres · fiche produit · panier · paiement ·
   rétractation · cookies · newsletter. ES2017, sans dépendance.
   Données produits : assets/js/catalogue.js (window.CP), généré par _build/build.py.
   ===================================================================== */
(function () {
  'use strict';
  var CP = window.CP || { products: [], univers: {} };
  var $ = function (id) { return document.getElementById(id); };
  var qa = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var html = document.documentElement;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Stockage sûr (navigation privée, stockage bloqué) ---------- */
  function sget(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } }
  function sset(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* stockage indisponible */ } }

  /* ---------- Date « du jour » (surchargeable pour tester : ?today=2026-12-10) ---------- */
  var TODAY = new Date();
  (function () {
    var m = /[?&]today=(\d{4}-\d{2}-\d{2})/.exec(location.search);
    if (m) { TODAY = new Date(m[1] + 'T10:00:00'); }
  })();
  var XMAS_DEADLINE = new Date('2026-12-04T23:59:59');
  var WRAP_END = new Date('2026-12-24T23:59:59');
  function period() { return TODAY <= XMAS_DEADLINE ? 'avant' : (TODAY <= WRAP_END ? 'apres' : 'hors'); }

  /* =====================================================================
     i18n
     ===================================================================== */
  var LANG = html.classList.contains('lang-en') ? 'en' : 'fr';
  var langHooks = [];
  function T(fr, en) { return LANG === 'en' ? en : fr; }
  function L(o) { return o ? (o[LANG] || o.fr) : ''; }
  function onLang(fn) { langHooks.push(fn); }
  var ATTRS = ['aria-label', 'alt', 'placeholder', 'title', 'content', 'value', 'href'];
  function applyLang() {
    html.lang = LANG;
    html.classList.toggle('lang-en', LANG === 'en');
    qa('[data-en]').forEach(function (el) {
      if (el.dataset.fr === undefined) { el.dataset.fr = el.textContent; }
      el.textContent = LANG === 'en' ? el.dataset.en : el.dataset.fr;
    });
    qa('[data-en-html]').forEach(function (el) {
      if (el.dataset.frHtml === undefined) { el.dataset.frHtml = el.innerHTML; }
      el.innerHTML = LANG === 'en' ? el.dataset.enHtml : el.dataset.frHtml;
    });
    ATTRS.forEach(function (a) {
      qa('[data-en-' + a + ']').forEach(function (el) {
        var k = 'fr-' + a;
        if (!el.hasAttribute('data-' + k)) { el.setAttribute('data-' + k, el.getAttribute(a) || ''); }
        el.setAttribute(a, LANG === 'en' ? el.getAttribute('data-en-' + a) : el.getAttribute('data-' + k));
      });
    });
    // JSON-LD : on active la version de la langue courante
    var fr = $('ld-fr'), en = $('ld-en');
    if (fr && en) { fr.type = LANG === 'fr' ? 'application/ld+json' : 'application/x-ld-inactive'; en.type = LANG === 'en' ? 'application/ld+json' : 'application/x-ld-inactive'; }
    qa('.lang button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.lang === LANG)); });
    qa('.lang-mini').forEach(function (b) {
      b.textContent = LANG === 'en' ? 'FR' : 'EN';
      b.setAttribute('aria-label', LANG === 'en' ? 'Passer le site en français' : 'Switch the site to English');
      b.setAttribute('lang', LANG === 'en' ? 'fr' : 'en');
    });
    langHooks.forEach(function (f) { try { f(); } catch (e) { if (window.console) { console.warn(e); } } });
  }
  function setLang(l) {
    if (l !== 'fr' && l !== 'en') { return; }
    LANG = l; sset('cp-lang', l); applyLang();
    toast(T('Site affiché en français.', 'The site is now in English.'));
  }

  /* ---------- Formats ---------- */
  function round2(v) { return Math.round(v * 100) / 100; }
  function eur(v, short) {
    v = round2(v);
    var whole = Math.abs(v - Math.round(v)) < 0.001;
    var s = (short && whole) ? String(Math.round(v)) : v.toFixed(2);
    return LANG === 'en' ? '€' + s : s.replace('.', ',') + ' €';
  }
  function addBiz(d, n) { d = new Date(d); while (n > 0) { d.setDate(d.getDate() + 1); var w = d.getDay(); if (w !== 0 && w !== 6) { n--; } } return d; }
  function fdate(d, long) {
    return d.toLocaleDateString(LANG === 'en' ? 'en-GB' : 'fr-FR', long ? { weekday: 'long', day: 'numeric', month: 'long' } : { weekday: 'short', day: 'numeric', month: 'short' });
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  /* =====================================================================
     Catalogue
     ===================================================================== */
  var BY = {};
  CP.products.forEach(function (p) { BY[p.sku] = p; });
  function parseKey(k) { var a = String(k).split('~'); return { p: BY[a[0]], v: a[1] || '' }; }
  function variantOf(p, v) { if (!p || !p.variants) { return null; } for (var i = 0; i < p.variants.length; i++) { if (p.variants[i].id === v) { return p.variants[i]; } } return null; }
  function uName(p) { var u = CP.univers[p.u]; return u ? L(u.name) : ''; }

  /* =====================================================================
     Panier (localStorage « cp-cart » = { clé: quantité })
     Règles : 2e parure −15 % sur la moins chère (dès 2 parures, une fois par commande),
     livraison 4,90 € sous 50 € (seuil calculé après remise), offerte dès 50 €.
     ===================================================================== */
  var CART_KEY = 'cp-cart', MAXQ = 10;
  var cart = {};
  function loadCart() {
    try { cart = JSON.parse(sget(CART_KEY, '{}')) || {}; } catch (e) { cart = {}; }
    Object.keys(cart).forEach(function (k) { if (!parseKey(k).p || !(cart[k] > 0)) { delete cart[k]; } });
  }
  loadCart();
  function saveCart() { sset(CART_KEY, JSON.stringify(cart)); }
  function count() { var n = 0; for (var k in cart) { n += cart[k]; } return n; }
  function getCode() { try { return sessionStorage.getItem('cp-code') || ''; } catch (e) { return ''; } }
  function setCode(c) { try { if (c) { sessionStorage.setItem('cp-code', c); } else { sessionStorage.removeItem('cp-code'); } } catch (e) { /* */ } }
  function calc() {
    var prices = [], sub = 0, n = 0;
    Object.keys(cart).forEach(function (k) { var p = parseKey(k).p, q = cart[k]; n += q; sub += q * p.price; for (var i = 0; i < q; i++) { prices.push(p.price); } });
    prices.sort(function (a, b) { return a - b; });
    var bundle = n >= 2 ? round2(prices[0] * 0.15) : 0;
    var code = getCode(), codeDisc = code === 'CERCLE10' && n ? round2(sub * 0.10) : 0;
    var useCode = codeDisc > bundle;
    var disc = useCode ? codeDisc : bundle;
    var after = round2(sub - disc);
    var free = after >= 50, ship = n ? (free ? 0 : 4.9) : 0;
    return { n: n, sub: round2(sub), bundle: bundle, codeDisc: codeDisc, useCode: useCode, disc: disc, after: after, free: free, ship: ship, total: round2(after + ship), code: code };
  }
  var cartHooks = [];
  function onCart(fn) { cartHooks.push(fn); }
  function renderCart() { cartHooks.forEach(function (f) { f(); }); }
  function setQty(k, q) { if (q <= 0) { delete cart[k]; } else { cart[k] = Math.min(q, MAXQ); } saveCart(); renderCart(); }
  function add(k, q, opts) {
    opts = opts || {};
    var r = parseKey(k); if (!r.p) { return; }
    cart[k] = Math.min((cart[k] || 0) + (q || 1), MAXQ); saveCart(); renderCart();
    var v = variantOf(r.p, r.v);
    var nm = L(r.p.name) + (v ? ' (' + L(v) + ')' : '');
    announce(T(nm + ' ajoutée à ton écrin.', nm + ' added to your box.'));
    if (!opts.stay) { openDrawer(); }
  }
  window.addEventListener('storage', function (e) { if (e.key === CART_KEY) { loadCart(); renderCart(); } if (e.key === 'cp-lang' && e.newValue && e.newValue !== LANG) { LANG = e.newValue; applyLang(); } });

  function shipText(c) {
    if (!c.n) { return T('Livraison offerte dès 50 €. 2e parure −15 %.', 'Free delivery from €50. 15% off your second set.'); }
    if (c.free) { return T('La livraison est offerte.', 'Delivery is on us.'); }
    if (c.n === 1 && 50 - c.after < 60) { return T('Plus que ' + eur(50 - c.after) + ' pour la livraison offerte. Une 2e parure et c\'est fait, avec −15 % sur la moins chère.', eur(50 - c.after) + ' away from free delivery. Add a second set and you\'re there, with 15% off the cheaper one.'); }
    return T('Plus que ' + eur(50 - c.after) + ' pour la livraison offerte.', eur(50 - c.after) + ' away from free delivery.');
  }
  function paintShipbar(el, c) {
    if (!el) { return; }
    el.classList.toggle('done', c.free && c.n > 0);
    var t = el.querySelector('.txt'), b = el.querySelector('.bar i');
    if (t) { t.textContent = (c.free && c.n ? '✓ ' : '') + shipText(c); }
    if (b) { b.style.width = Math.min(100, (c.after / 50) * 100) + '%'; }
  }
  function thumb(p, v) {
    var img = (v && v.img) || p.img;
    return '<img src="' + img + '" alt="" width="400" height="400" loading="lazy">';
  }
  function lineHTML(k, big) {
    var r = parseKey(k), p = r.p, v = variantOf(p, r.v), q = cart[k];
    var pcs = L(p.pcs).join(' + ');
    return '<div class="line" data-k="' + esc(k) + '"><div class="th">' + thumb(p, v) + '</div><div><b><a href="' + p.url + '">' + esc(L(p.name)) + '</a></b>' +
      '<small>' + esc(pcs) + (v ? ' · ' + esc(L(v)) : '') + '</small>' +
      '<div class="qty" role="group" aria-label="' + esc(T('Quantité de ', 'Quantity of ') + L(p.name)) + '"><button type="button" data-d="-1" aria-label="' + esc(T('Retirer une parure', 'One less')) + '">−</button><span aria-live="polite">' + q + '</span><button type="button" data-d="1" aria-label="' + esc(T('Ajouter une parure', 'One more')) + '"' + (q >= MAXQ ? ' disabled' : '') + '>+</button></div>' +
      (big ? ' <button type="button" class="rm" data-rm="1">' + T('Retirer', 'Remove') + '</button>' : '') +
      '</div><span class="lp">' + eur(q * p.price) + '</span></div>';
  }
  function bindLines(root) {
    qa('.line', root).forEach(function (l) {
      var k = l.dataset.k;
      qa('.qty button', l).forEach(function (b) { b.addEventListener('click', function () { setQty(k, (cart[k] || 0) + Number(b.dataset.d)); focusAfterRender(root, k, b.dataset.d); }); });
      var rm = l.querySelector('[data-rm]'); if (rm) { rm.addEventListener('click', function () { setQty(k, 0); announce(T('Parure retirée.', 'Set removed.')); }); }
    });
  }
  function focusAfterRender(root, k, d) {
    setTimeout(function () {
      var l = root.querySelector('.line[data-k="' + k.replace(/"/g, '') + '"]');
      var b = l && l.querySelector('.qty button[data-d="' + d + '"]');
      if (b && !b.disabled) { b.focus(); } else if (root.closest && root.closest('.drawer')) { var c = $('drawerClose'); if (c) { c.focus(); } }
    }, 0);
  }
  function sumHTML(c, opts) {
    opts = opts || {};
    var s = '<div class="row"><span>' + T('Sous-total', 'Subtotal') + '</span><span>' + eur(c.sub) + '</span></div>';
    if (c.disc) { s += '<div class="row disc"><span>' + (c.useCode ? T('Code CERCLE10 −10 %', 'Code CERCLE10 −10%') : T('2e parure −15 %', 'Second set −15%')) + '</span><span>− ' + eur(c.disc) + '</span></div>'; }
    s += '<div class="row"><span>' + T('Livraison suivie', 'Tracked delivery') + '</span><span>' + (!c.n ? '—' : (c.free ? T('Offerte', 'Free') : eur(c.ship))) + '</span></div>';
    s += '<div class="row tot"><span>' + T('Total TTC', 'Total (VAT incl.)') + '</span><span>' + eur(c.total) + '</span></div>';
    s += '<p class="note">' + T('Prix TTC, TVA incluse. Droits de douane déjà payés.', 'Prices include VAT. Duties already paid.') + '</p>';
    if (c.useCode && c.bundle) { s += '<p class="note">' + T('Ce code ne se cumule pas avec la remise 2e parure. On a gardé la plus avantageuse pour toi.', 'This code can\'t be combined with the second-set discount. We kept the better one for you.') + '</p>'; }
    return s;
  }
  function offerNote(c) {
    if (c.n === 1) { return '<p class="offer-note">' + T('Ajoute une 2e parure : −15 % sur la moins chère des deux.', 'Add a second set: 15% off the cheaper of the two.') + '</p>'; }
    if (c.n >= 2) { return '<p class="offer-note">' + T('−15 % sur ta 2e parure, déjà appliqué. Tes parures arrivent dans un seul colis : une dans la boîte-tiroir, les autres dans leur sachet scellé. Pour deux cadeaux à deux adresses, passe deux commandes.', '15% off your second set, already applied. Your sets travel in one parcel: one in the drawer box, the others in sealed bags. For two gifts to two addresses, place two orders.') + '</p>'; }
    return '';
  }
  function suggestions(nb) {
    var inCart = {}; Object.keys(cart).forEach(function (k) { inCart[parseKey(k).p.sku] = 1; });
    var first = Object.keys(cart)[0], u = first ? parseKey(first).p.u : 'eclat';
    var pool = CP.products.filter(function (p) { return !inCart[p.sku] && p.u === u; });
    var rest = CP.products.filter(function (p) { return !inCart[p.sku] && p.u !== u && p.price < 100; });
    return pool.concat(rest).slice(0, nb || 3);
  }
  function upsellHTML(list) {
    return '<div class="upsell"><h3>' + T('La 2e à −15 %', 'Your second at −15%') + '</h3><ul>' + list.map(function (p) {
      return '<li><img src="' + p.img + '" alt="" width="48" height="48" loading="lazy"><span><a href="' + p.url + '">' + esc(L(p.name)) + '</a><small>' +
        T(eur(p.price) + ' · −15 % dans ton écrin : ' + eur(round2(p.price * 0.85)), eur(p.price) + ' · −15% in your box: ' + eur(round2(p.price * 0.85))) +
        '</small></span><button type="button" data-add="' + p.sku + '" aria-label="' + esc(T('Ajouter ', 'Add ') + L(p.name)) + '">' + T('Ajouter', 'Add') + '</button></li>';
    }).join('') + '</ul><p class="note small muted">' + T('−15 % sur la parure la moins chère dès 2 parures dans la même commande. Non cumulable avec le code de bienvenue.', '15% off the cheaper set from 2 sets in one order. Not combinable with the welcome code.') + '</p></div>';
  }
  function bindAdds(root, stay) {
    qa('[data-add]', root).forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); add(b.dataset.add, 1, { stay: stay }); }); });
  }

  /* ---------- Tiroir « Ton écrin » ---------- */
  var lastFocus = null;
  function openDrawer() {
    var d = $('drawer'); if (!d) { return; }
    lastFocus = document.activeElement;
    d.classList.add('on'); d.setAttribute('aria-hidden', 'false'); d.removeAttribute('inert');
    $('scrim').classList.add('on');
    qa('[data-open-cart]').forEach(function (b) { b.setAttribute('aria-expanded', 'true'); });
    setTimeout(function () { $('drawerClose').focus(); }, 60);
  }
  function closeDrawer() {
    var d = $('drawer'); if (!d || !d.classList.contains('on')) { return; }
    d.classList.remove('on'); d.setAttribute('aria-hidden', 'true'); d.setAttribute('inert', '');
    $('scrim').classList.remove('on');
    qa('[data-open-cart]').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
    if (lastFocus && lastFocus.focus) { lastFocus.focus(); }
  }
  function renderDrawer() {
    var c = calc();
    qa('[data-count]').forEach(function (el) { el.textContent = c.n; el.hidden = !c.n; });
    qa('[data-open-cart]').forEach(function (b) { b.setAttribute('aria-label', T('Ouvrir ton écrin (panier), ' + c.n + (c.n > 1 ? ' parures' : ' parure'), 'Open your box (cart), ' + c.n + (c.n > 1 ? ' sets' : ' set'))); });
    var d = $('drawer'); if (!d) { return; }
    $('drawerTitle').textContent = T('Ton écrin', 'Your box') + (c.n ? ' (' + c.n + ')' : '');
    paintShipbar($('drawerShip'), c);
    var lines = $('drawerLines');
    if (!c.n) {
      lines.innerHTML = '<div class="empty"><span>' + T('Ton écrin est vide.', 'Your box is empty.') + '</span><a class="btn ghost" href="parures.html">' + T('Voir les parures', 'See the sets') + '</a></div>';
    } else {
      lines.innerHTML = Object.keys(cart).map(function (k) { return lineHTML(k, true); }).join('') + offerNote(c) + upsellHTML(suggestions(c.n === 1 ? 3 : 2));
      bindLines(lines); bindAdds(lines, true);
    }
    $('drawerSum').innerHTML = sumHTML(c);
    var go = $('drawerGo'); go.setAttribute('aria-disabled', String(!c.n)); go.tabIndex = c.n ? 0 : -1;
  }
  onCart(renderDrawer);
  onLang(renderDrawer);

  /* ---------- Annonces (lecteur d'écran) et toast ---------- */
  var tt;
  function toast(msg) {
    var t = $('toast'); if (!t) { return; }
    t.textContent = msg; t.classList.add('on');
    clearTimeout(tt); tt = setTimeout(function () { t.classList.remove('on'); }, 3200);
  }
  function announce(msg) { toast(msg); }

  /* =====================================================================
     En-tête : menu mobile, sous-menu Univers, recherche
     ===================================================================== */
  function initHeader() {
    var mb = $('menuBtn'), mn = $('mnav');
    if (mb && mn) {
      mb.addEventListener('click', function () {
        var o = mb.getAttribute('aria-expanded') !== 'true';
        mb.setAttribute('aria-expanded', String(o)); mn.hidden = !o;
        var hdr = $('hdr'); mn.style.setProperty('--mnav-top', (hdr.getBoundingClientRect().bottom) + 'px');
        document.body.style.overflow = o ? 'hidden' : '';
        if (o) { var a = mn.querySelector('a'); if (a) { a.focus(); } }
      });
    }
    qa('.navbtn').forEach(function (b) {
      var sub = $(b.getAttribute('aria-controls'));
      function close() { b.setAttribute('aria-expanded', 'false'); sub.hidden = true; }
      b.addEventListener('click', function () { var o = b.getAttribute('aria-expanded') !== 'true'; b.setAttribute('aria-expanded', String(o)); sub.hidden = !o; });
      b.parentNode.addEventListener('focusout', function (e) { if (!b.parentNode.contains(e.relatedTarget)) { close(); } });
      b.parentNode.addEventListener('keydown', function (e) { if (e.key === 'Escape') { close(); b.focus(); } });
    });
    var sb = $('searchBtn'), sp = $('searchPanel'), si = $('searchInput'), sr = $('searchRes');
    if (sb && sp) {
      sb.addEventListener('click', function () {
        var o = sp.hidden; sp.hidden = !o; sb.setAttribute('aria-expanded', String(o));
        if (o) { si.focus(); }
      });
      sp.addEventListener('keydown', function (e) { if (e.key === 'Escape') { sp.hidden = true; sb.setAttribute('aria-expanded', 'false'); sb.focus(); } });
      var paint = function () {
        var q = si.value.trim();
        if (q.length < 2) { sr.innerHTML = ''; $('searchStatus').textContent = ''; return; }
        var res = search(q);
        $('searchStatus').textContent = T(res.length + ' résultat' + (res.length > 1 ? 's' : ''), res.length + ' result' + (res.length > 1 ? 's' : ''));
        sr.innerHTML = res.slice(0, 6).map(function (p) {
          return '<li><a href="' + p.url + '"><img src="' + p.img + '" alt="" width="48" height="48" loading="lazy"><span>' + esc(L(p.name)) + '<small>' + esc(uName(p)) + ' · ' + esc(L(p.pcs).join(' + ')) + '</small></span><span class="pr">' + eur(p.price, 1) + '</span></a></li>';
        }).join('');
      };
      si.addEventListener('input', paint);
      onLang(paint);
    }
    qa('.lang button').forEach(function (b) { b.addEventListener('click', function () { setLang(b.dataset.lang); }); });
    qa('.lang-mini').forEach(function (b) { b.addEventListener('click', function () { setLang(LANG === 'en' ? 'fr' : 'en'); }); });
    qa('[data-open-cart]').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); openDrawer(); }); });
    var sc = $('scrim'); if (sc) { sc.addEventListener('click', closeDrawer); }
    var dc = $('drawerClose'); if (dc) { dc.addEventListener('click', closeDrawer); }
    document.addEventListener('keydown', function (e) {
      var d = $('drawer');
      if (!d || !d.classList.contains('on')) { return; }
      if (e.key === 'Escape') { closeDrawer(); }
      if (e.key === 'Tab') { // piège de focus dans le tiroir
        var f = qa('a[href],button:not([disabled]),input,select,[tabindex="0"]', d).filter(function (x) { return x.offsetParent !== null; });
        if (!f.length) { return; }
        if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
      }
    });
  }
  function norm(s) { return String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function search(q) {
    var words = norm(q).split(/\s+/).filter(Boolean);
    return CP.products.filter(function (p) {
      var hay = norm([p.name.fr, p.name.en, p.mat.fr, p.mat.en, p.pcs.fr.join(' '), p.pcs.en.join(' '), uName(p), (CP.univers[p.u] || {}).name ? CP.univers[p.u].name.en : '', p.tags || ''].join(' '));
      return words.every(function (w) { return hay.indexOf(w) > -1; });
    });
  }

  /* ---------- Bandeau d'annonce selon la date ---------- */
  function initAnnonce() {
    var per = period();
    qa('[data-period]').forEach(function (el) { el.hidden = el.dataset.period !== per; });
    qa('[data-xmas]').forEach(function (el) { el.hidden = (el.dataset.xmas === 'avant' && per !== 'avant') || (el.dataset.xmas === 'apres' && per !== 'apres') || (el.dataset.xmas === 'noel' && per === 'hors'); });
  }

  /* ---------- Accordéons ---------- */
  function initAcc(root) {
    qa('.acc-btn', root).forEach(function (b) {
      if (b.dataset.bound) { return; } b.dataset.bound = '1';
      var p = $(b.getAttribute('aria-controls'));
      var sync = function () { var o = b.getAttribute('aria-expanded') === 'true'; if (o) { p.removeAttribute('inert'); } else { p.setAttribute('inert', ''); } };
      sync();
      b.addEventListener('click', function () { b.setAttribute('aria-expanded', String(b.getAttribute('aria-expanded') !== 'true')); sync(); });
    });
  }

  /* ---------- Cookies (dialogue « Gérer mes cookies ») ---------- */
  function initCookies() {
    var d = $('cookieDlg'); if (!d) { return; }
    qa('[data-cookies]').forEach(function (b) { b.addEventListener('click', function () { if (d.showModal) { d.showModal(); } else { d.setAttribute('open', ''); } }); });
    qa('[data-consent]', d).forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.dataset.consent;
        if (v === 'custom') { var c = $('cookieCustom'); c.hidden = !c.hidden; return; }
        sset('cp-consent', JSON.stringify({ choix: v, date: new Date().toISOString() }));
        d.close ? d.close() : d.removeAttribute('open');
        toast(T('Ton choix est enregistré pour 6 mois.', 'Your choice is saved for 6 months.'));
      });
    });
  }

  /* ---------- Newsletter ---------- */
  function initNews() {
    qa('form[data-news]').forEach(function (f) {
      var input = f.querySelector('input[type=email]'), err = f.parentNode.querySelector('.err'), ok = f.parentNode.querySelector('.ok');
      f.addEventListener('submit', function (e) {
        e.preventDefault();
        var v = input.value.trim();
        if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) {
          input.setAttribute('aria-invalid', 'true');
          err.hidden = false; err.textContent = T('Cette adresse ne semble pas complète. Vérifie l\'arobase et le point.', 'That email doesn\'t look complete. Check the @ and the dot.');
          input.focus(); return;
        }
        input.removeAttribute('aria-invalid'); err.hidden = true; ok.hidden = false; f.reset();
      });
    });
  }

  /* =====================================================================
     Cartes produit et grilles
     ===================================================================== */
  var PLUS = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>';
  function card(p) {
    var tag = p.u === 'j925' ? '<span class="tag t925">' + T('Joaillerie 925', '925 Silver') + '</span>' : (p.isNew ? '<span class="tag">' + T('Nouveau', 'New') + '</span>' : '');
    var alt = p.cut ? '<img class="alt" src="' + p.cut + '" alt="" width="700" height="700" loading="lazy">' : '';
    var addBtn = p.variants ? '<a class="quick" href="' + p.url + '" aria-label="' + esc(T('Choisir la finition de ', 'Choose the finish of ') + L(p.name)) + '">' + PLUS + '</a>'
      : '<button class="quick" type="button" data-add="' + p.sku + '" aria-label="' + esc(T('Ajouter à l\'écrin : ', 'Add to my box: ') + L(p.name)) + '">' + PLUS + '</button>';
    return '<article class="card">' +
      '<div class="visual">' + '<img src="' + p.img + '" alt="' + esc(L(p.alt)) + '" width="400" height="400" loading="lazy">' + alt + tag + '</div>' +
      addBtn +
      '<h3><a href="' + p.url + '">' + esc(L(p.name)) + '</a></h3>' +
      '<div class="meta"><span class="pcs">' + esc(L(p.pcs).join(' + ')) + '</span><span class="price">' + eur(p.price, 1) + '</span></div>' +
      '<div class="pcs">' + esc(L(p.mat)) + '</div></article>';
  }
  function promoTile() {
    return '<aside class="promo-tile"><span class="wm" aria-hidden="true"><span class="br l"></span><span class="br r"></span></span><div><h3>' + T('2e parure −15 %', '15% off your second set') + '</h3><p>' +
      T('Dès deux parures dans ta commande, la moins chère est à −15 %, appliqué automatiquement. Une pour toi, une à offrir.', 'From two sets in one order, the cheaper one is 15% off, applied automatically. One for you, one to give.') +
      '</p></div><a class="btn gold" href="cadeaux.html">' + T('Idées cadeaux', 'Gift ideas') + '</a></aside>';
  }

  /* Grilles statiques simples : <div data-grid data-skus="A,B"> ou data-u="eclat" */
  function initStaticGrids() {
    qa('[data-grid]:not([data-filterable])').forEach(function (g) {
      var list;
      if (g.dataset.skus) { list = g.dataset.skus.split(',').map(function (s) { return BY[s.trim()]; }).filter(Boolean); }
      else if (g.dataset.u) { list = CP.products.filter(function (p) { return p.u === g.dataset.u; }); }
      else { list = CP.products.slice(); }
      if (g.dataset.exclude) { list = list.filter(function (p) { return p.sku !== g.dataset.exclude; }); }
      if (g.dataset.limit) { list = list.slice(0, Number(g.dataset.limit)); }
      var promoAt = Number(g.dataset.promo || 0);
      var paint = function () {
        g.innerHTML = list.map(function (p, i) { return card(p) + (promoAt && i === promoAt - 1 && list.length > promoAt ? promoTile() : ''); }).join('');
        bindAdds(g);
      };
      paint(); onLang(paint);
    });
  }

  /* Page « Toutes les parures » : filtres (univers, budget, métal, pièces) + tri + « Voir plus » */
  function initShop() {
    var g = document.querySelector('[data-grid][data-filterable]'); if (!g) { return; }
    var state = { u: [], b: [], m: [], r: false, sort: 'choix', shown: 12, q: '' };
    var mq = /[?&]q=([^&]+)/.exec(location.search); if (mq) { state.q = decodeURIComponent(mq[1].replace(/\+/g, ' ')); }
    var mu = /[?&]u=([a-z0-9]+)/.exec(location.search); if (mu) { state.u = [mu[1]]; }
    var BUD = { b50: function (p) { return p.price < 50; }, b100: function (p) { return p.price >= 50 && p.price < 100; }, b100p: function (p) { return p.price >= 100; } };
    var MET = { dore: function (p) { return p.metal === 'dore' || p.metal === 'bicolore' || p.metal === 'dore-argent'; }, argente: function (p) { return p.metal === 'argente' || p.metal === 'rose' || p.metal === 'bicolore' || p.metal === 'dore-argent'; }, a925: function (p) { return p.metal === '925'; } };
    function match(p, skip) {
      if (state.q && search(state.q).indexOf(p) < 0) { return false; }
      if (skip !== 'u' && state.u.length && state.u.indexOf(p.u) < 0) { return false; }
      if (skip !== 'b' && state.b.length && !state.b.some(function (k) { return BUD[k](p); })) { return false; }
      if (skip !== 'm' && state.m.length && !state.m.some(function (k) { return MET[k](p); })) { return false; }
      if (skip !== 'r' && state.r && !p.ring) { return false; }
      return true;
    }
    function sorted(list) {
      var l = list.slice();
      if (state.sort === 'asc') { l.sort(function (a, b) { return a.price - b.price; }); }
      if (state.sort === 'desc') { l.sort(function (a, b) { return b.price - a.price; }); }
      return l;
    }
    function paint() {
      var list = sorted(CP.products.filter(function (p) { return match(p); }));
      var vis = list.slice(0, state.shown);
      g.innerHTML = vis.length ? vis.map(function (p, i) { return card(p) + (i === 5 && vis.length > 6 ? promoTile() : ''); }).join('')
        : '<p class="empty" style="grid-column:1/-1">' + T('Aucune parure ne correspond à ces filtres.', 'No set matches these filters.') + ' <button type="button" class="linkbtn" data-clear>' + T('Effacer les filtres', 'Clear filters') + '</button></p>';
      bindAdds(g);
      var clr = g.querySelector('[data-clear]'); if (clr) { clr.addEventListener('click', clearAll); }
      $('shopCount').textContent = T(list.length + (list.length > 1 ? ' parures' : ' parure'), list.length + (list.length > 1 ? ' sets' : ' set'));
      var more = $('shopMore');
      more.hidden = list.length <= state.shown;
      $('shopShown').textContent = T(Math.min(state.shown, list.length) + ' sur ' + list.length, Math.min(state.shown, list.length) + ' of ' + list.length);
      // compteurs + chips sans résultat désactivés
      qa('.chip[data-f]').forEach(function (c) {
        var f = c.dataset.f, v = c.dataset.v, on;
        if (f === 'r') { on = state.r; } else { on = state[f].indexOf(v) > -1; }
        c.setAttribute('aria-pressed', String(on));
        var n = CP.products.filter(function (p) {
          if (!match(p, f)) { return false; }
          if (f === 'u') { return p.u === v; } if (f === 'b') { return BUD[v](p); } if (f === 'm') { return MET[v](p); } return p.ring;
        }).length;
        var s = c.querySelector('small'); if (s) { s.textContent = n; }
        c.disabled = !on && n === 0;
      });
      var qi = $('shopQ'); if (qi) { qi.hidden = !state.q; qi.querySelector('b').textContent = '« ' + state.q + ' »'; }
    }
    function clearAll() { state.u = []; state.b = []; state.m = []; state.r = false; state.q = ''; state.shown = 12; paint(); }
    qa('.chip[data-f]').forEach(function (c) {
      c.addEventListener('click', function () {
        var f = c.dataset.f, v = c.dataset.v;
        if (f === 'r') { state.r = !state.r; } else { var i = state[f].indexOf(v); if (i > -1) { state[f].splice(i, 1); } else { state[f].push(v); } }
        state.shown = 12; paint();
      });
    });
    qa('[data-clear-all]').forEach(function (b) { b.addEventListener('click', clearAll); });
    $('shopSort').addEventListener('change', function (e) { state.sort = e.target.value; paint(); });
    $('shopMoreBtn').addEventListener('click', function () {
      var before = state.shown; state.shown += 12; paint();
      var cards = qa('.card', g); var t = cards[before]; if (t) { var a = t.querySelector('h3 a'); if (a) { a.focus(); } }
    });
    paint(); onLang(paint);
  }

  /* =====================================================================
     Fiche produit
     ===================================================================== */
  function etaText() {
    var a = addBiz(TODAY, 4), b = addBiz(TODAY, 9);
    return T('Commandée aujourd\'hui, livrée en France entre le <b>' + fdate(a) + '</b> et le <b>' + fdate(b) + '</b> (9 colis sur 10). Préparée en 1 à 2 jours ouvrés.',
      'Order today, delivered to France between <b>' + fdate(a) + '</b> and <b>' + fdate(b) + '</b> (9 parcels in 10). Prepared in 1 to 2 business days.');
  }
  function initProduct() {
    var root = document.querySelector('[data-pdp]'); if (!root) { return; }
    var P = BY[root.dataset.pdp]; if (!P) { return; }
    sset('cp-last-list', (CP.univers[P.u] || {}).url || 'parures.html');
    var qty = 1, variant = P.variants ? P.variants[0].id : '';
    // Galerie
    var track = $('gTrack'), slides = qa('.g-slide', track), thumbs = qa('#gThumbs button'), dots = $('gDots'), cur = 0, N = slides.length;
    for (var i = 0; i < N; i++) {
      (function (i) {
        var b = document.createElement('button'); b.type = 'button';
        b.setAttribute('aria-label', 'Photo ' + (i + 1) + ' / ' + N); b.addEventListener('click', function () { go(i); }); dots.appendChild(b);
        if (thumbs[i]) { thumbs[i].addEventListener('click', function () { go(i); }); }
      })(i);
    }
    function go(i) { i = Math.max(0, Math.min(N - 1, i)); track.scrollTo({ left: i * track.clientWidth, behavior: reduceMotion ? 'auto' : 'smooth' }); }
    function mark() {
      cur = Math.round(track.scrollLeft / Math.max(1, track.clientWidth));
      $('gCount').textContent = (cur + 1) + ' / ' + N;
      thumbs.forEach(function (t, k) { t.setAttribute('aria-current', String(k === cur)); });
      qa('button', dots).forEach(function (t, k) { t.setAttribute('aria-current', String(k === cur)); });
      $('gPrev').disabled = cur === 0; $('gNext').disabled = cur === N - 1;
    }
    var raf; track.addEventListener('scroll', function () { cancelAnimationFrame(raf); raf = requestAnimationFrame(mark); }, { passive: true });
    $('gPrev').addEventListener('click', function () { go(cur - 1); });
    $('gNext').addEventListener('click', function () { go(cur + 1); });
    track.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); go(cur + 1); } if (e.key === 'ArrowLeft') { e.preventDefault(); go(cur - 1); } });
    window.addEventListener('resize', function () { track.scrollLeft = cur * track.clientWidth; });
    mark();
    // Finition (variantes)
    qa('input[name="finition"]').forEach(function (r) {
      r.addEventListener('change', function () {
        variant = r.value; var v = variantOf(P, variant);
        $('finLabel').textContent = L(v);
        if (v.slide !== undefined) { go(v.slide); }
      });
    });
    function prices() {
      $('atcPrice').textContent = eur(P.price * qty);
      $('qVal').textContent = qty; $('qMinus').disabled = qty <= 1; $('qPlus').disabled = qty >= MAXQ;
      var c = calc(), after = c.after + P.price * qty;
      paintShipbar($('pShip'), { n: c.n + qty, after: after, free: after >= 50 });
    }
    $('qMinus').addEventListener('click', function () { if (qty > 1) { qty--; prices(); } });
    $('qPlus').addEventListener('click', function () { if (qty < MAXQ) { qty++; prices(); } });
    function doAdd() {
      add(P.sku + (variant ? '~' + variant : ''), qty);
      var b = $('atc'), s = b.querySelector('[data-label]');
      s.textContent = T('Ajoutée à l\'écrin', 'Added to your box');
      setTimeout(function () { s.textContent = T('Ajouter à l\'écrin', 'Add to my box'); }, 2000);
      qty = 1; prices();
    }
    $('atc').addEventListener('click', doAdd);
    var sa = $('satc'); if (sa) { sa.addEventListener('click', doAdd); }
    var bar = $('stickyAtc');
    if (bar && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { var vis = es[0].isIntersecting; bar.classList.toggle('on', !vis && es[0].boundingClientRect.top < 0); bar.setAttribute('aria-hidden', String(vis)); if (vis) { bar.setAttribute('inert', ''); } else { bar.removeAttribute('inert'); } }).observe($('atcRow'));
    }
    var paintEta = function () { $('eta').innerHTML = etaText(); prices(); $('satcPrice').textContent = eur(P.price); };
    paintEta(); onLang(paintEta); onCart(prices);
  }

  /* =====================================================================
     Page panier
     ===================================================================== */
  function initCartPage() {
    var root = $('cartPage'); if (!root) { return; }
    var back = sget('cp-last-list', 'parures.html');
    qa('[data-back]').forEach(function (a) { a.href = back; });
    function paint() {
      var c = calc(), lines = $('cartLines');
      $('cartCount').textContent = c.n ? T('(' + c.n + (c.n > 1 ? ' parures)' : ' parure)'), '(' + c.n + (c.n > 1 ? ' sets)' : ' set)')) : '';
      if (!c.n) {
        lines.innerHTML = '<div class="empty"><span>' + T('Ton écrin est vide.', 'Your box is empty.') + '</span><a class="btn" href="parures.html">' + T('Voir les parures', 'See the sets') + '</a></div>';
      } else {
        lines.innerHTML = Object.keys(cart).map(function (k) { return lineHTML(k, true); }).join('') + offerNote(c);
        bindLines(lines);
      }
      paintShipbar($('cartShip'), c);
      $('cartSum').innerHTML = sumHTML(c);
      var go = $('cartGo'); go.setAttribute('aria-disabled', String(!c.n)); if (!c.n) { go.removeAttribute('href'); } else { go.href = 'paiement.html'; }
      var up = $('cartUpsell'); up.innerHTML = c.n ? upsellHTML(suggestions(3)) : ''; bindAdds(up, true);
      $('cartEta').innerHTML = etaText();
    }
    paint(); onCart(paint); onLang(paint);
  }

  /* =====================================================================
     Paiement (maquette : aucune donnée n'est envoyée, aucun paiement)
     ===================================================================== */
  var ETA = { FR: [4, 9], BE: [4, 9], LU: [4, 9], DE: [4, 9], ES: [4, 9], IT: [3, 10], NL: [4, 6], IE: [5, 11], PT: [4, 12], AT: [4, 12] };
  function initCheckout() {
    var form = $('coForm'); if (!form) { return; }
    function paintSum() {
      var c = calc();
      $('coLines').innerHTML = c.n ? Object.keys(cart).map(function (k) { var r = parseKey(k), v = variantOf(r.p, r.v); return '<div class="line"><div class="th">' + thumb(r.p, v) + '</div><div><b>' + esc(L(r.p.name)) + '</b><small>' + cart[k] + ' × ' + eur(r.p.price) + (v ? ' · ' + esc(L(v)) : '') + '</small></div><span class="lp">' + eur(cart[k] * r.p.price) + '</span></div>'; }).join('')
        : '<div class="empty"><span>' + T('Ton écrin est vide.', 'Your box is empty.') + '</span><a class="btn ghost" href="parures.html">' + T('Voir les parures', 'See the sets') + '</a></div>';
      $('coSum').innerHTML = sumHTML(c);
      $('coToggleTotal').textContent = eur(c.total);
      $('coShipPrice').textContent = c.free ? T('offerte', 'free') : eur(4.9) + T(' (offerte dès 50 €)', ' (free from €50)');
      paintShipbar($('coShip'), c);
      var co = $('country').value, e = ETA[co] || [4, 12];
      $('coEta').textContent = T('Livraison suivie DHL · ' + e[0] + ' à ' + e[1] + ' jours ouvrés', 'DHL tracked delivery · ' + e[0] + '–' + e[1] + ' business days');
      $('coEtaDates').textContent = T('Estimation : entre le ' + fdate(addBiz(TODAY, e[0])) + ' et le ' + fdate(addBiz(TODAY, e[1])) + ' (9 colis sur 10).', 'Estimate: between ' + fdate(addBiz(TODAY, e[0])) + ' and ' + fdate(addBiz(TODAY, e[1])) + ' (9 parcels in 10).');
      $('coSubmit').disabled = !c.n;
      var cm = $('codeMsg'); if (cm && c.code) { cm.textContent = c.useCode ? T('Code CERCLE10 appliqué.', 'Code CERCLE10 applied.') : T('Ce code ne se cumule pas avec la remise 2e parure. On a gardé la plus avantageuse pour toi.', 'This code can\'t be combined with the second-set discount. We kept the better one for you.'); }
    }
    $('country').addEventListener('change', paintSum);
    $('coToggle').addEventListener('click', function () { var b = $('coToggle'), o = b.getAttribute('aria-expanded') !== 'true'; b.setAttribute('aria-expanded', String(o)); $('coRecap').classList.toggle('open-m', o); });
    qa('[data-reveal]').forEach(function (b) { b.addEventListener('click', function () { var t = $(b.dataset.reveal); t.hidden = false; b.hidden = true; var i = t.querySelector('input,select,textarea'); if (i) { i.focus(); } }); });
    $('shipElse').addEventListener('change', function (e) { $('shipElseBox').hidden = !e.target.checked; });
    $('codeApply').addEventListener('click', function () {
      var v = $('code').value.trim().toUpperCase(), m = $('codeMsg');
      if (v === 'CERCLE10') { setCode(v); paintSum(); }
      else { setCode(''); m.textContent = T('Ce code ne fonctionne pas. Vérifie l\'orthographe ou sa date de validité.', 'That code doesn\'t work. Check the spelling or its expiry date.'); paintSum(); }
    });
    qa('input[name="pay"]').forEach(function (r) { r.addEventListener('change', function () { qa('[data-pay]').forEach(function (p) { p.hidden = p.dataset.pay !== r.value; }); }); });
    qa('.xpay').forEach(function (b) { b.addEventListener('click', function () { toast(T('Maquette : le paiement express sera fourni par la passerelle (Stripe, PayPal).', 'Mock-up: express checkout will come from the payment gateway (Stripe, PayPal).')); }); });

    var MSG = {
      req: ['Il nous manque cette information pour t\'envoyer ta parure.', 'We need this to send your set.'],
      email: ['Cette adresse ne semble pas complète. Vérifie l\'arobase et le point.', 'That email doesn\'t look complete. Check the @ and the dot.'],
      phone: ['Ajoute ton numéro : le transporteur peut en avoir besoin pour te livrer.', 'Add your number: the carrier may need it to deliver.'],
      zip: ['Le code postal ne correspond pas au pays choisi.', 'The postcode doesn\'t match the country.'],
      cgv: ['Coche la case pour accepter les conditions générales de vente.', 'Tick the box to accept the terms and conditions.']
    };
    function setErr(input, key) {
      var f = input.closest('.field') || input.closest('.check-wrap');
      var e = f && f.querySelector('.err');
      if (key) { input.setAttribute('aria-invalid', 'true'); if (e) { e.hidden = false; e.textContent = T(MSG[key][0], MSG[key][1]); } }
      else { input.removeAttribute('aria-invalid'); if (e) { e.hidden = true; } }
      return key;
    }
    function validate(input) {
      var v = (input.type === 'checkbox') ? input.checked : input.value.trim();
      if (input.offsetParent === null && input.type !== 'checkbox') { return setErr(input, null); }
      if (input.required && !v) { return setErr(input, input.type === 'checkbox' ? 'cgv' : (input.type === 'tel' ? 'phone' : 'req')); }
      if (input.type === 'email' && v && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) { return setErr(input, 'email'); }
      if (input.id === 'zip' && v && $('country').value === 'FR' && !/^\d{5}$/.test(v)) { return setErr(input, 'zip'); }
      return setErr(input, null);
    }
    qa('input,select', form).forEach(function (i) { i.addEventListener('blur', function () { if (i.value || i.getAttribute('aria-invalid')) { validate(i); } }); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = [];
      qa('[required]', form).forEach(function (i) { var k = validate(i); if (k) { bad.push({ i: i, k: k }); } });
      var sumBox = $('errSummary');
      if (bad.length) {
        sumBox.hidden = false;
        sumBox.querySelector('ul').innerHTML = bad.map(function (b) { var lab = form.querySelector('label[for="' + b.i.id + '"]'); return '<li><a href="#' + b.i.id + '">' + esc(lab ? lab.textContent.replace(/\s*\(.*\)$/, '') : b.i.id) + ' : ' + esc(T(MSG[b.k][0], MSG[b.k][1])) + '</a></li>'; }).join('');
        sumBox.focus(); return;
      }
      sumBox.hidden = true;
      var c = calc(); if (!c.n) { return; }
      var no = 'CP-' + String(Math.floor(1000 + Math.random() * 9000));
      var co = $('country').value, eta = ETA[co] || [4, 12];
      $('cfName').textContent = $('fname').value.trim();
      $('cfNo').textContent = no;
      $('cfTotal').textContent = eur(c.total);
      $('cfPrep').textContent = fdate(addBiz(TODAY, 2), true);
      $('cfDel').textContent = T('entre le ' + fdate(addBiz(TODAY, eta[0]), true) + ' et le ' + fdate(addBiz(TODAY, eta[1]), true), 'between ' + fdate(addBiz(TODAY, eta[0]), true) + ' and ' + fdate(addBiz(TODAY, eta[1]), true));
      sset('cp-last-order', JSON.stringify({ no: no, email: $('email').value.trim(), date: TODAY.toISOString(), items: Object.keys(cart).map(function (k) { return L(parseKey(k).p.name) + ' × ' + cart[k]; }) }));
      cart = {}; saveCart(); setCode(''); renderCart();
      $('coWrap').hidden = true; $('coDone').hidden = false;
      $('coDone').focus(); window.scrollTo(0, 0);
    });
    paintSum(); onCart(paintSum); onLang(paintSum);
  }

  /* =====================================================================
     Rétractation en ligne (L. 221-21) : formulaire → vérification → confirmation → accusé de réception
     ===================================================================== */
  function initWithdrawal() {
    var f = $('wdForm'); if (!f) { return; }
    try { var last = JSON.parse(sget('cp-last-order', 'null')); if (last) { $('wdOrder').value = last.no; $('wdEmail').value = last.email; $('wdItems').value = last.items.join('\n'); } } catch (e) { /* */ }
    var step1 = $('wdStep1'), step2 = $('wdStep2'), step3 = $('wdStep3');
    function fieldErr(i, msg) { var e = i.closest('.field').querySelector('.err'); if (msg) { i.setAttribute('aria-invalid', 'true'); e.hidden = false; e.textContent = msg; } else { i.removeAttribute('aria-invalid'); e.hidden = true; } return !!msg; }
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = false, first = null;
      qa('[required]', f).forEach(function (i) {
        var v = i.value.trim(), m = '';
        if (!v) { m = T('Il nous manque cette information pour traiter ta demande.', 'We need this to process your request.'); }
        else if (i.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) { m = T('Cette adresse ne semble pas complète. Vérifie l\'arobase et le point.', 'That email doesn\'t look complete. Check the @ and the dot.'); }
        if (fieldErr(i, m)) { bad = true; first = first || i; }
      });
      if (bad) { first.focus(); return; }
      $('wdRecap').innerHTML = [['wdName', T('Nom', 'Name')], ['wdEmail', T('E-mail', 'Email')], ['wdOrder', T('Commande n°', 'Order no.')], ['wdDate', T('Reçue le', 'Received on')], ['wdItems', T('Parures concernées', 'Sets concerned')], ['wdReason', T('Motif (facultatif)', 'Reason (optional)')]].map(function (r) {
        var v = $(r[0]).value.trim(); return v ? '<dt>' + r[1] + '</dt><dd>' + esc(v).replace(/\n/g, '<br>') + '</dd>' : '';
      }).join('');
      step1.hidden = true; step2.hidden = false; $('wdStep2Title').focus();
    });
    $('wdBack').addEventListener('click', function () { step2.hidden = true; step1.hidden = false; $('wdName').focus(); });
    $('wdConfirm').addEventListener('click', function () {
      var now = new Date();
      $('wdWhen').textContent = now.toLocaleString(LANG === 'en' ? 'en-GB' : 'fr-FR', { dateStyle: 'full', timeStyle: 'short' });
      $('wdMail').textContent = $('wdEmail').value.trim();
      $('wdRef').textContent = 'RET-' + now.getTime().toString(36).toUpperCase().slice(-6);
      var log = []; try { log = JSON.parse(sget('cp-withdrawals', '[]')) || []; } catch (e) { log = []; }
      log.push({ ref: $('wdRef').textContent, order: $('wdOrder').value.trim(), date: now.toISOString() }); sset('cp-withdrawals', JSON.stringify(log));
      step2.hidden = true; step3.hidden = false; $('wdStep3Title').focus();
    });
  }

  /* =====================================================================
     Démarrage
     ===================================================================== */
  window.CPsite = { T: T, L: L, eur: eur, add: add, onLang: onLang, onCart: onCart, lang: function () { return LANG; }, byId: BY, esc: esc, period: period, today: function () { return TODAY; }, reduceMotion: reduceMotion };
  function boot() {
    initHeader(); initAnnonce(); initAcc(document); initCookies(); initNews();
    initStaticGrids(); initShop(); initProduct(); initCartPage(); initCheckout(); initWithdrawal();
    applyLang(); renderCart();
    var u = document.body.dataset.list; if (u) { sset('cp-last-list', u); }
    document.dispatchEvent(new CustomEvent('cp:ready'));
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
})();
