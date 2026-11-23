/* CHARMED PARIS · prototype v2 · panier, offre en paliers, fiche produit */
(() => {
  'use strict';
  const CP = window.CP, O = CP.offer;
  const ALL = [...CP.products, ...CP.pieces];
  const BY = Object.fromEntries(ALL.map(p => [p.sku, p]));
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const eur = x => (Math.round(x * 100) / 100).toLocaleString('fr-FR', { minimumFractionDigits: x % 1 ? 2 : 0, maximumFractionDigits: 2 }) + ' €';
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const KEY = 'cp_cart_v2';
  const pc = x => '−' + Math.round(x * 100) + ' %';

  /* ------------------------------------------------ stockage */
  let mem = [];
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return mem; } };
  const save = c => { mem = c; try { localStorage.setItem(KEY, JSON.stringify(c)); } catch { /* navigation privée */ } render(); };
  const add = (sku, qty = 1) => { const c = load(); const l = c.find(x => x.sku === sku); l ? l.qty += qty : c.push({ sku, qty }); save(c); };
  const setQty = (sku, q) => { let c = load(); const l = c.find(x => x.sku === sku); if (!l) return; l.qty = q; c = c.filter(x => x.qty > 0); save(c); };

  /* ------------------------------------------------ calcul de l'offre
     Parures éligibles triées par prix décroissant, par groupes de 3 : la moins chère de chaque groupe complet est remisée de d3 (−50 %).
     S'il reste 2 parures hors groupe, la moins chère des deux est remisée de d2 (−30 %). Cadeau optionnel (O.gift) dès 3 parures. */
  function compute(cart) {
    const lines = cart.map(l => ({ ...l, p: BY[l.sku] })).filter(l => l.p && l.qty > 0);
    const units = [];
    lines.forEach(l => { if (l.p.eligible) for (let i = 0; i < l.qty; i++) units.push({ sku: l.sku, price: l.p.price }); });
    units.sort((a, b) => b.price - a.price);
    const disc = {}, tags = {};
    const tag = (u, amount, label) => { disc[u.sku] = (disc[u.sku] || 0) + amount; (tags[u.sku] = tags[u.sku] || []).push(label); };
    const n = units.length;
    for (let g = 0; g + 3 <= n; g += 3) tag(units[g + 2], units[g + 2].price * O.d3, pc(O.d3));
    if (n % 3 === 2) tag(units[n - 1], units[n - 1].price * O.d2, pc(O.d2));
    const sub = lines.reduce((s, l) => s + l.p.price * l.qty, 0);
    const discount = Object.values(disc).reduce((a, b) => a + b, 0);
    const after = sub - discount;
    const ship = !lines.length || after >= O.freeShipFrom ? 0 : O.shipFee;
    const gift = !!O.gift && n >= 3;
    let next = '';
    if (n === 0 && lines.length) next = `Ajoute une parure : dès 2, la 2e est à ${pc(O.d2)}.`;
    else if (n % 3 === 1) next = `Ajoute 1 parure : <b>elle est à ${pc(O.d2)}</b>.`;
    else if (n % 3 === 2) next = `Ajoute 1 parure : <b>elle est à ${pc(O.d3)}</b>.`;
    else if (n >= 3) next = `<b>Offre débloquée</b> : ta 3e parure est à ${pc(O.d3)}.`;
    return { lines, n, sub, discount, after, ship, total: after + ship, gift, disc, tags, next };
  }

  /* ------------------------------------------------ rendu panier (tiroir + page + commande) */
  function lineHTML(l, r) {
    const p = l.p, full = p.price * l.qty, d = r.disc[l.sku] || 0;
    const t = (r.tags[l.sku] || []).map(x => `<span class="line-tag">${l.qty > 1 ? 'Dont 1 à ' + x : x}</span>`).join(' ');
    return `<div class="line"><img src="${p.thumb}" alt="" width="76" height="76">
<div><h3><a href="${p.url}">${esc(p.name)}</a></h3><p class="line-pcs">${esc(p.pcs.join(' + '))}</p>${t}
<div><button class="rm" type="button" data-rm="${l.sku}">Retirer</button></div></div>
<div class="line-r"><p class="line-price">${d ? `<s>${eur(full)}</s>` : ''}${eur(full - d)}</p>
<div class="qty" role="group" aria-label="Quantité de ${esc(p.name)}"><button type="button" data-q="${l.sku}" data-d="-1" aria-label="Retirer une">−</button><span>${l.qty}</span><button type="button" data-q="${l.sku}" data-d="1" aria-label="Ajouter une">+</button></div></div></div>`;
  }
  function giftHTML() {
    return `<div class="line"><img src="${O.gift.img}" alt="" width="76" height="76"><div><h3>${O.gift.name}</h3><p class="line-pcs">Collier · ajouté avec ta 3e parure</p><span class="line-tag gift">Cadeau</span></div><div class="line-r"><p class="line-price"><s>${eur(O.gift.value)}</s>Offert</p></div></div>`;
  }
  function progHTML(r) {
    if (!r.lines.length) return '';
    const k = r.n === 0 ? 0 : r.n % 3 === 0 ? 3 : r.n % 3;
    const bars = [1, 2, 3].map(i => `<i class="${i <= k ? 'on' : ''}"></i>`).join('');
    return `<div class="prog"><p>${r.next}</p><div class="prog-bar">${bars}</div><div class="prog-steps"><span>1 parure</span><span>2e à −30 %</span><span>3e à −50 %</span></div></div>`;
  }
  function upsellHTML(r) {
    if (!r.lines.length || r.n % 3 === 0) return '';
    const inCart = new Set(r.lines.map(l => l.sku));
    const ref = r.lines.find(l => l.p.eligible)?.p;
    const pool = CP.products.filter(p => p.eligible && !inCart.has(p.sku));
    const pick = [...pool.filter(p => ref && p.u === ref.u), ...pool.filter(p => !ref || p.u !== ref.u)].slice(0, 2);
    const lbl = r.n % 3 === 2 ? 'à −' + Math.round(O.d3 * 100) + ' %' : 'à −' + Math.round(O.d2 * 100) + ' %';
    return `<div class="upsell"><h3>Ta prochaine parure ${lbl}</h3>${pick.map(p => `<div class="ups"><img src="${p.thumb}" alt="" width="56" height="56"><span><b>${esc(p.name)}</b><small>${eur(p.price)}</small></span><button type="button" data-add="${p.sku}">Ajouter</button></div>`).join('')}</div>`;
  }
  function totalsHTML(r, mode) {
    const cta = mode === 'checkout' ? '' : `<a class="btn" href="commande.html">Passer commande · ${eur(r.total)}</a>`;
    return `<div class="tot"><div><span>Sous-total</span><span>${eur(r.sub)}</span></div>
${r.discount ? `<div class="disc"><span>Offre parures</span><span>−${eur(r.discount)}</span></div>` : ''}
${r.gift ? `<div class="disc"><span>${O.gift.name}</span><span>Offert</span></div>` : ''}
<div><span>Livraison suivie DHL</span><span>${r.ship ? eur(r.ship) : 'Offerte'}</span></div>
<div class="grand"><span>Total<small>TTC, droits de douane payés</small></span><span>${eur(r.total)}</span></div></div>
${r.ship ? `<p class="foot-note">Plus que ${eur(O.freeShipFrom - r.after)} pour la livraison offerte.</p>` : ''}
${cta}<p class="foot-note">Livrée entre le ${eta()[0]} et le ${eta()[1]} · 14 jours pour changer d’avis</p>`;
  }
  function render() {
    const r = compute(load());
    const count = r.lines.reduce((s, l) => s + l.qty, 0);
    $$('[data-count]').forEach(x => { x.textContent = count; x.hidden = !count; });
    $$('[data-count-label]').forEach(x => x.textContent = count ? `(${count})` : '');
    const body = r.lines.length
      ? progHTML(r) + r.lines.map(l => lineHTML(l, r)).join('') + (r.gift ? giftHTML() : '') + upsellHTML(r)
      : `<div class="empty"><p>Ton panier est vide.</p><a class="btn" href="collection.html">Voir les parures</a></div>`;
    $$('[data-cart-body]').forEach(x => x.innerHTML = body);
    $$('[data-cart-foot]').forEach(x => {
      const mode = x.dataset.mode;
      if (!r.lines.length) { x.innerHTML = mode === 'checkout' ? '<p>Ton panier est vide. <a href="collection.html">Voir les parures</a></p>' : ''; x.hidden = !mode && x.closest('.drawer') ? true : false; return; }
      x.hidden = false;
      x.innerHTML = (mode === 'checkout' ? '<h2 class="co-sum">Récapitulatif</h2>' + r.lines.map(l => lineHTML(l, r)).join('') + (r.gift ? giftHTML() : '') : '') + totalsHTML(r, mode);
    });
    $$('[data-co-ship]').forEach(x => x.textContent = r.ship ? eur(r.ship) : 'Offerte');
    $$('[data-co-total]').forEach(x => x.textContent = r.lines.length ? eur(r.total) : '');
  }

  /* ------------------------------------------------ dates de livraison (jours ouvrés) */
  function addBiz(d, n) { const x = new Date(d); while (n > 0) { x.setDate(x.getDate() + 1); const w = x.getDay(); if (w && w !== 6) n--; } return x; }
  const fd = d => d.toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' });
  function eta() { const t = new Date(); return [fd(addBiz(t, 4)), fd(addBiz(t, 9))]; }

  /* ------------------------------------------------ tiroir, menu, toast */
  const drawer = $('#drawer');
  let lastFocus;
  function openCart() { if (!drawer) return; lastFocus = document.activeElement; drawer.hidden = false; document.body.style.overflow = 'hidden'; $('.drawer-p .ibtn', drawer)?.focus(); }
  function closeCart() { if (!drawer || drawer.hidden) return; drawer.hidden = true; document.body.style.overflow = ''; lastFocus?.focus(); }
  const menu = $('#menu');
  function openMenu() { menu.hidden = false; document.body.style.overflow = 'hidden'; $('[data-menu]').setAttribute('aria-expanded', 'true'); $('[data-menu-close]').focus(); }
  function closeMenu() { if (menu.hidden) return; menu.hidden = true; document.body.style.overflow = ''; $('[data-menu]').setAttribute('aria-expanded', 'false'); $('[data-menu]').focus(); }
  let toastT;
  function toast(msg) { const t = $('#toast'); t.innerHTML = msg; t.classList.add('is-on'); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('is-on'), 2600); }
  function trap(e, root) {
    if (e.key !== 'Tab') return;
    const f = $$('a[href],button:not([disabled]),select,input', root).filter(x => x.offsetParent);
    if (!f.length) return; const a = f[0], z = f[f.length - 1];
    if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
  }

  document.addEventListener('click', e => {
    const t = e.target.closest('[data-add],[data-rm],[data-q],[data-cart-open],[data-cart-close],[data-menu],[data-menu-close]');
    if (!t) { if (e.target === menu) closeMenu(); return; }
    if (t.dataset.add) { add(t.dataset.add); const p = BY[t.dataset.add]; if (document.body.classList.contains('is-cart') || !drawer) toast(`${esc(p.name)} ajoutée`); else openCart(); }
    else if (t.dataset.rm) setQty(t.dataset.rm, 0);
    else if (t.dataset.q) { const l = load().find(x => x.sku === t.dataset.q); if (l) setQty(t.dataset.q, l.qty + +t.dataset.d); }
    else if ('cartOpen' in t.dataset) { if (!document.body.classList.contains('is-cart') && drawer) { e.preventDefault(); openCart(); } }
    else if ('cartClose' in t.dataset) closeCart();
    else if ('menu' in t.dataset) openMenu();
    else if ('menuClose' in t.dataset) closeMenu();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeCart(); if (menu && !menu.hidden) closeMenu(); }
    if (drawer && !drawer.hidden) trap(e, drawer); else if (menu && !menu.hidden) trap(e, menu);
  });
  window.addEventListener('storage', e => { if (e.key === KEY) render(); });

  /* ------------------------------------------------ fiche produit */
  const pdp = $('[data-pdp]');
  if (pdp) {
    const me = BY[pdp.dataset.pdp];
    const offer = $('[data-offer]', pdp), slotsBox = $('[data-slots]', pdp), slotList = $('[data-slot-list]', pdp);
    const buyBtn = $('[data-buy]', pdp), buyTotal = $('[data-buy-total]', pdp);
    const elig = CP.products.filter(p => p.eligible);
    let tier = 1, picks = [me.sku, me.sku, me.sku];
    const opts = sel => Object.entries(CP.univers).filter(([k]) => k !== 'j925').map(([k, name]) =>
      `<optgroup label="${esc(name)}">${elig.filter(p => p.u === k).map(p => `<option value="${p.sku}"${p.sku === sel ? ' selected' : ''}>${esc(p.name)} · ${eur(p.price)}</option>`).join('')}</optgroup>`).join('');
    const cartOf = list => { const m = {}; list.forEach(s => m[s] = (m[s] || 0) + 1); return Object.entries(m).map(([sku, qty]) => ({ sku, qty })); };
    function drawSlots() {
      if (!slotsBox) return;
      slotsBox.hidden = tier === 1;
      if (tier === 1) return;
      let h = `<div class="slot"><img src="${me.thumb}" alt=""><span class="slot-fixed">1. ${esc(me.name)}</span></div>`;
      for (let i = 1; i < tier; i++) {
        const p = BY[picks[i]];
        h += `<div class="slot"><img src="${p.thumb}" alt="" data-slot-img="${i}"><label>${i + 1}e parure<select data-slot="${i}">${opts(picks[i])}</select></label></div>`;
      }
      slotList.innerHTML = h;
    }
    function refresh() {
      if (offer) {
        [1, 2, 3].forEach(n => {
          const r = compute(cartOf(picks.slice(0, n)));
          const tot = $(`[data-tier-total="${n}"]`, offer), sv = $(`[data-tier-save="${n}"]`, offer);
          if (tot) tot.textContent = eur(r.total);
          if (sv) sv.textContent = r.discount ? `Tu économises ${eur(r.discount + (r.gift ? O.gift.value : 0))}` : (r.ship ? '' : 'Livraison offerte');
        });
        $$('.tier', offer).forEach(t => t.classList.toggle('is-on', +t.dataset.tier === tier));
      }
      const r = compute(cartOf(picks.slice(0, tier)));
      buyTotal.textContent = eur(r.after);
      const sp = $('[data-sticky-p]'); if (sp) sp.textContent = eur(r.after) + (tier > 1 ? ` · ${tier} parures` : '');
    }
    offer?.addEventListener('change', e => {
      if (e.target.name === 'tier') { tier = +e.target.value; drawSlots(); refresh(); }
    });
    slotList?.addEventListener('change', e => {
      const i = e.target.dataset.slot; if (i === undefined) return;
      picks[+i] = e.target.value; const img = $(`[data-slot-img="${i}"]`, slotList); if (img) img.src = BY[e.target.value].thumb; refresh();
    });
    const doBuy = () => {
      const list = picks.slice(0, tier);
      const c = load(); list.forEach(s => { const l = c.find(x => x.sku === s); l ? l.qty++ : c.push({ sku: s, qty: 1 }); }); save(c);
      openCart();
    };
    buyBtn.addEventListener('click', doBuy);
    $('[data-sticky-buy]')?.addEventListener('click', doBuy);
    drawSlots(); refresh();

    // galerie
    const gal = $('[data-gal]', pdp);
    const setOn = i => { $$('.gdot,.gth', pdp).forEach(b => b.classList.toggle('is-on', +b.dataset.g === i)); };
    gal.addEventListener('scroll', () => setOn(Math.round(gal.scrollLeft / gal.clientWidth)), { passive: true });
    $$('.gdot,.gth', pdp).forEach(b => b.addEventListener('click', () => { gal.scrollTo({ left: +b.dataset.g * gal.clientWidth, behavior: 'smooth' }); setOn(+b.dataset.g); }));
    gal.addEventListener('keydown', e => { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); gal.scrollBy({ left: (e.key === 'ArrowRight' ? 1 : -1) * gal.clientWidth, behavior: 'smooth' }); } });

    // barre fixe : visible quand le bouton d'achat sort de l'écran
    const sticky = $('[data-sticky]');
    if (sticky && 'IntersectionObserver' in window) {
      sticky.hidden = false;
      new IntersectionObserver(([en]) => sticky.classList.toggle('is-on', !en.isIntersecting), { threshold: 0 }).observe(buyBtn);
    }
    const [a, b] = eta(); const ea = $('[data-eta-a]', pdp), eb = $('[data-eta-b]', pdp); if (ea) { ea.textContent = a; eb.textContent = b; }
  }

  /* ------------------------------------------------ Noël : masquer après la date limite */
  if (new Date() > new Date(O.xmasCutoff + 'T23:59:59')) $$('[data-xmas],[data-xmas-note]').forEach(x => x.remove());

  /* ------------------------------------------------ collection : filtres et tri */
  const grid = $('[data-grid]');
  if (grid) {
    const chips = $$('.chip'), sel = $('[data-sort]'), res = $('[data-count-res]');
    const cards = $$('.card', grid), order = cards.slice();
    function apply(f) {
      chips.forEach(c => { const on = c.dataset.filter === f; c.classList.toggle('is-on', on); c.setAttribute('aria-pressed', on); });
      let n = 0; cards.forEach(c => { const show = f === 'all' || c.dataset.u === f; c.hidden = !show; if (show) n++; });
      res.textContent = `${n} parure${n > 1 ? 's' : ''}`;
    }
    chips.forEach(c => c.addEventListener('click', () => { apply(c.dataset.filter); history.replaceState(null, '', c.dataset.filter === 'all' ? location.pathname : '#' + c.dataset.filter); }));
    sel.addEventListener('change', () => {
      const v = sel.value, price = c => BY[c.dataset.sku].price;
      const list = v ? order.slice().sort((x, y) => v === 'asc' ? price(x) - price(y) : price(y) - price(x)) : order;
      list.forEach(c => grid.appendChild(c));
    });
    const h = location.hash.slice(1); apply(CP.univers[h] ? h : 'all');
    window.addEventListener('hashchange', () => { const k = location.hash.slice(1); if (CP.univers[k]) apply(k); });
  }

  /* ------------------------------------------------ commande (prototype : aucun paiement) */
  const co = $('[data-checkout]');
  if (co) co.addEventListener('submit', e => {
    e.preventDefault();
    let ok = true;
    $$('input[required]', co).forEach(i => { const bad = i.type === 'checkbox' ? !i.checked : !i.value.trim() || (i.type === 'email' && !/^\S+@\S+\.\S+$/.test(i.value)); i.setAttribute('aria-invalid', bad); if (bad && ok) { i.focus(); ok = false; } });
    const msg = $('[data-co-msg]', co);
    if (!compute(load()).lines.length) { msg.textContent = 'Ton panier est vide.'; return; }
    msg.textContent = ok ? 'Prototype : la commande et le paiement seront branchés sur WooCommerce. Aucun paiement n’a été effectué.' : 'Vérifie les champs en rouge.';
  });

  render();
})();
