#!/usr/bin/env python3
"""Génère le site prototype CHARMED PARIS (v2, refonte du 23/11/2026).

Sources : site/_build/catalogue-source.json (30 parures), woocommerce/contenus/produits-woocommerce.csv
(textes), woocommerce/legal/*.md (pages légales). Sortie : site/*.html + site/assets/js/data.js.
Lancer : python3 site/_build/build.py
"""
import csv, html, json, re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
W = ROOT / 'woocommerce'
BASE_URL = 'https://charmedparis.fr/'

def e(s): return html.escape(str(s), quote=True)

# ---------------------------------------------------------------- offre (une seule source de vérité, reprise par app.js)
OFFER = {
    'freeShipFrom': 50, 'shipFee': 4.90,
    'd2': 0.30, 'd3': 0.50,  # 2 parures : la 2e à −30 % ; 3 parures : la 3e à −50 % (rentable même au scénario pessimiste, voir woocommerce/conversion/offre-bundles.md)
    'gift': None,
    'xmasCutoff': '2026-12-04', 'xmasWrapUntil': '2026-12-24',
}

# ---------------------------------------------------------------- données produits
src = json.loads((SITE / '_build/catalogue-source.json').read_text())
CSV = {r['SKU']: r for r in csv.DictReader(open(W / 'contenus/produits-woocommerce.csv', encoding='utf-8'))}
UNIV = {
    'sculpture': dict(name='Sculpture', line='Métal doré qui a l’air d’avoir fondu', file='collection.html#sculpture'),
    'eclat': dict(name='Éclat', line='Doré et oxydes de zirconium', file='collection.html#eclat'),
    'couleur': dict(name='Couleur précieuse', line='Une pierre de couleur en écho', file='collection.html#couleur'),
    'j925': dict(name='Joaillerie 925', line='Argent 925 et moissanite synthétique', file='collection.html#j925'),
    'mixte': dict(name='Mixte', line='Sur cordon, à partager', file='collection.html#mixte'),
}
HD = {  # visuels haute définition disponibles (photo d'origine retouchée ou générée à partir de la photo produit)
    'JS63WT': ['assets/img/cascade/01-parure-or.webp', 'assets/img/cascade/02-parure-or-pose.webp', 'assets/img/cascade/05-portee.webp', 'assets/img/cascade/03-boucles-or.webp'],
    'JS1AQ5': ['assets/img/ia/I9-solar-sphere-packshot.webp', 'assets/img/ia/I5-post-solar-sphere-cafe.webp', 'assets/img/ia/I1-banniere-solar-sphere.webp'],
    'JSJB3S': ['assets/img/ia/I7-golden-luxe-packshot.webp', 'assets/img/ia/I3-post-golden-luxe-portee.webp', 'assets/img/ia/I10-story-golden-luxe-paris.webp'],
    'JSGRQR': ['assets/img/ia/I8-molten-art-packshot.webp', 'assets/img/ia/I4-post-molten-art-profil.webp', 'assets/img/ia/I2-banniere-noel-molten-art.webp'],
}

def sect(desc, title):
    m = re.search(r'<p><strong>' + re.escape(title) + r'[^<]*</strong>(?:<br>)?(.*?)</p>(<ul>.*?</ul>)?', desc, re.S)
    if not m: return ''
    return (m.group(1) or '').strip(), (m.group(2) or '')

# Photos portées (mannequin) : survol des cartes + 2e photo de la galerie. Source : photos Branvas (droits inclus avec l'abonnement).
PORTE = {f.stem: f'assets/img/portes/{f.name}' for f in (SITE / 'assets/img/portes').glob('*.webp')}
PORTE.setdefault('JSJB3S', 'assets/img/ia/I3-post-golden-luxe-portee.webp')

PRODUCTS = []
for p in src['products']:
    r = CSV.get(p['sku'], {})
    d = r.get('Description', '')
    intro = re.match(r'<p>(.*?)</p>', d, re.S)
    inside = sect(d, 'Dans la parure') or ('', '')
    mats = sect(d, 'Matières') or ('', '')
    gift = sect(d, "Pour l'offrir") or ('', '')
    slug = p['url'].replace('.html', '')
    PRODUCTS.append(dict(
        sku=p['sku'], model=p['model'], name=p['model'], price=p['price'], u=p['u'], pcs=p['pcs']['fr'],
        mat=p['mat']['fr'], metal=p['metal'], img=(HD.get(p['sku']) or [p['img']])[0], thumb=p['img'], cut=p['cut'],
        line=p['line']['fr'], url=p['url'], slug=slug, alt=p['alt']['fr'], tags=p['tags'],
        intro=intro.group(1) if intro else p['line']['fr'], inside=inside[1], mats=mats[1], giftfor=gift[0],
        gallery=list(dict.fromkeys(((HD.get(p['sku']) or [p['img']])[:1]) + ([PORTE[p['sku']]] if p['sku'] in PORTE else []) + (HD.get(p['sku']) or [])[1:] + [p['img']] + ([p['cut']] if p['cut'] else []))),
        porte=PORTE.get(p['sku']),
        eligible=p['u'] != 'j925',
    ))
BY = {p['sku']: p for p in PRODUCTS}

PIECES = [  # pièces seules (prix proposés, à valider dans Branvas)
    dict(sku='JNEJ8J', name='Collier Golden Arc', price=39, img='assets/img/pieces/golden-arc-necklace-JNEJ8J.webp', line='Cinq pierres en arc sur une chaîne fine. Doré à l’or 14 carats, oxydes de zirconium.'),
    dict(sku='JNEXV0', name='Collier Clé du cœur', price=39, img='assets/img/pieces/secret-heart-key-necklace-JNEXV0.webp', line='Une petite clé dorée à l’anneau en cœur, pavée de pierres.'),
    dict(sku='JNDEG4', name='Collier Courbe', price=109, img='assets/img/pieces/curve-statement-necklace-JNDEG4.webp', line='Une courbe dorée sculptée sur une chaîne serpent. Argent 925 doré.'),
    dict(sku='JNQXAH', name='Collier Croissant trois rangs', price=39, img='assets/img/pieces/golden-crescent-layer-set-JNQXAH.webp', line='Maille serpent, pastilles et croissant de lune. Acier doré.'),
    dict(sku='JNPCC0', name='Collier Pierre verte', price=79, img='assets/img/pieces/emerald-dreams-necklace-JNPCC0.webp', line='Une pierre verte coussin entourée de pavé. Argent 925 doré.'),
    dict(sku='JNYA6X', name='Pendentif Goutte de lumière', price=339, img='assets/img/pieces/teardrop-brilliance-necklace-JNYA6X.webp', line='Argent 925 et moissanite synthétique. Livré dans son écrin en velours bleu avec certificat.'),
]

# Onglets d'angle sur chaque palier : un avatar, une raison d'acheter, vraie et vérifiable.
def tiers_for(p):
    gf = p['giftfor'].rstrip('.') if p['giftfor'] else 'ta sœur, ta mère ou ta meilleure amie'
    return [
        dict(n=1, tab='Pour toi', title='1 parure', note='Le collier et les boucles, déjà assortis. Rien à chercher.'),
        dict(n=2, tab='Une pour toi, une à offrir', title='2 parures', badge='La 2e à −30 %', note=f'Une pour toi, une pour {gf}. Même colis, même livraison.'),
        dict(n=3, tab='Tous tes cadeaux de Noël', title='3 parures', badge='La 3e à −50 %', note='Trois cadeaux réglés d’un coup, la 3e parure à moitié prix.'),
    ]

# ---------------------------------------------------------------- briques HTML
ICONS = {
    'bag': '<path d="M6 8h12l-1 12H7L6 8Z"/><path d="M9 8a3 3 0 0 1 6 0"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'close': '<path d="M6 6l12 12M18 6 6 18"/>',
    'truck': '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17.5" cy="17.5" r="1.6"/>',
    'shield': '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6l7-3Z"/><path d="m9 12 2 2 4-4"/>',
    'return': '<path d="M9 7 5 11l4 4"/><path d="M5 11h9a5 5 0 0 1 0 10h-3"/>',
    'gift': '<path d="M4 10h16v10H4zM3 7h18v3H3zM12 7v13"/><path d="M12 7c-2-3-5-3-5-1s3 1 5 1c2 0 5 1 5-1s-3-2-5 1Z"/>',
    'lock': '<rect x="5" y="11" width="14" height="9" rx="1.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    'chev': '<path d="m6 9 6 6 6-6"/>',
    'check': '<path d="m5 12 5 5 9-10"/>',
    'box': '<path d="M3 8l9-4 9 4-9 4-9-4Z"/><path d="M3 8v8l9 4 9-4V8"/><path d="M12 12v8"/>',
}
def icon(n, cls='ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[n]}</svg>'

LOGO = (W / 'identite/logos/principal/charmed-paris-principal-encre.svg').read_text()
LOGO = re.sub(r'<\?xml[^>]*>|<!--.*?-->', '', LOGO, flags=re.S)
LOGO = re.sub(r'<svg ', '<svg class="logo" aria-hidden="true" focusable="false" ', LOGO, count=1)
LOGO = re.sub(r'(<svg[^>]*?)\s(width|height)="[^"]*"', r'\1', LOGO)
LOGO = re.sub(r'(<svg[^>]*?)\s(width|height)="[^"]*"', r'\1', LOGO)
LOGO = re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="currentColor"', LOGO)

def fmt(x):
    s = f'{x:,.2f}'.replace(',', ' ').replace('.', ',')
    return s.replace(',00', '') + ' €' if s.endswith(',00') else s + ' €'

NAV = [('collection.html', 'Toutes les parures'), ('collection.html#eclat', 'Éclat'), ('collection.html#sculpture', 'Sculpture'),
       ('collection.html#couleur', 'Couleur précieuse'), ('collection.html#j925', 'Joaillerie 925'), ('pieces-seules.html', 'Pièces seules'),
       ('cadeaux.html', 'Idées cadeaux')]

ANN = ('<span>2 parures : la 2e à −30 %</span><span>3 parures : la 3e à moitié prix</span>'
       '<span data-xmas>Noël en Europe : commande avant le vendredi 4 décembre</span><span>Livraison offerte dès 50 €</span>')
def annonce():
    return ('<div class="annonce" role="region" aria-label="Offres en cours"><div class="annonce-track">' + ANN + ANN.replace('<span', '<span aria-hidden="true"', 1).replace('<span>', '<span aria-hidden="true">').replace('<span data-xmas>', '<span data-xmas aria-hidden="true">') + '</div></div>')

def header():
    links = ''.join(f'<li><a href="{h}">{e(t)}</a></li>' for h, t in NAV)
    return f'''<header class="hdr" id="hdr">
  <div class="hdr-in wrap">
    <button class="ibtn menu-btn" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu" data-menu>{icon('menu')}</button>
    <nav class="nav-d" aria-label="Navigation principale"><ul>{links}</ul></nav>
    <a class="brand" href="index.html" aria-label="CHARMED PARIS, accueil">{LOGO}</a>
    <div class="tools">
      <a class="ibtn" href="panier.html" data-cart-open aria-label="Panier">{icon('bag')}<span class="cnt" data-count hidden>0</span></a>
    </div>
  </div>
</header>
<div class="menu" id="menu" hidden>
  <div class="menu-panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="menu-top"><span class="menu-t">Menu</span><button class="ibtn" type="button" aria-label="Fermer le menu" data-menu-close>{icon('close')}</button></div>
    <ul class="menu-l">{links}<li><a href="livraison-retours.html">Livraison et retours</a></li><li><a href="faq.html">Questions fréquentes</a></li><li><a href="a-propos.html">Notre histoire</a></li></ul>
    <p class="menu-foot">Livraison offerte dès 50 € · Droits de douane payés · 14 jours pour changer d’avis</p>
  </div>
</div>'''

def drawer():
    return f'''<div class="drawer" id="drawer" hidden>
  <div class="drawer-bg" data-cart-close></div>
  <aside class="drawer-p" role="dialog" aria-modal="true" aria-labelledby="drawerT">
    <div class="drawer-h"><h2 id="drawerT">Ton panier <span data-count-label></span></h2><button class="ibtn" type="button" aria-label="Fermer le panier" data-cart-close>{icon('close')}</button></div>
    <div class="drawer-b" data-cart-body></div>
    <div class="drawer-f" data-cart-foot></div>
  </aside>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>'''

def footer():
    return f'''<footer class="foot">
  <div class="wrap foot-proof">
    <div>{icon('truck')}<p><b>Livrée en 4 à 9 jours ouvrés</b><span>Suivi DHL, droits de douane payés</span></p></div>
    <div>{icon('return')}<p><b>14 jours pour changer d’avis</b><span>Retour gratuit, remboursement sous 14 jours</span></p></div>
    <div>{icon('gift')}<p><b>Prête à offrir</b><span>Boîte cadeau CHARMED PARIS, aucun prix dans le colis</span></p></div>
    <div>{icon('lock')}<p><b>Paiement sécurisé</b><span>Carte bancaire, Apple Pay, Google Pay</span></p></div>
  </div>
  <div class="wrap foot-cols">
    <div class="foot-brand"><a href="index.html" aria-label="CHARMED PARIS, accueil">{LOGO}</a><p>Ouvre. Laisse-toi charmer.</p></div>
    <div><h2>Boutique</h2><ul><li><a href="collection.html">Toutes les parures</a></li><li><a href="pieces-seules.html">Pièces seules</a></li><li><a href="cadeaux.html">Idées cadeaux</a></li></ul></div>
    <div><h2>Aide</h2><ul><li><a href="livraison-retours.html">Livraison et retours</a></li><li><a href="faq.html">Questions fréquentes</a></li><li><a href="matieres-entretien.html">Matières et entretien</a></li><li><a href="a-propos.html#contact">Contact</a></li><li><a href="retractation.html">Me rétracter</a></li></ul></div>
    <div><h2>Légal</h2><ul><li><a href="cgv.html">Conditions générales de vente</a></li><li><a href="mentions-legales.html">Mentions légales</a></li><li><a href="confidentialite.html">Confidentialité</a></li><li><a href="cookies.html">Cookies</a></li></ul></div>
  </div>
  <div class="wrap foot-legal"><p>© 2026 CHARMED PARIS · Prix TTC en euros. Nos bijoux dorés sont en laiton doré : ce n’est pas de l’or massif. À garder au sec.</p></div>
</footer>'''

def page(file, title, desc, body, *, canonical=None, ld=None, cls='', robots='index,follow'):
    url = BASE_URL + ('' if file == 'index.html' else file)
    ldj = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    full = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical or url}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE_URL}assets/img/pack/pack-noel-f-600.webp">
<meta name="theme-color" content="#F5EFE6">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml"><link rel="icon" href="assets/img/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="assets/img/apple-touch-icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/app.css">
<link rel="stylesheet" href="assets/css/editorial.css">
{ldj}
</head>
<body class="{cls}">
<a class="skip" href="#main">Aller au contenu</a>
{annonce()}
{header()}
<main id="main">
{body}
</main>
{footer()}
{drawer()}
<script src="assets/js/data.js"></script>
<script src="assets/js/app.js" defer></script>
</body>
</html>
'''
    (SITE / file).write_text(full)

def card(p, cls=''):
    pcs = ' + '.join(p['pcs'])
    return f'''<article class="card {cls}" data-sku="{p['sku']}" data-u="{p['u']}">
  <a class="card-img" href="{p['url']}"><img src="{p['thumb']}" alt="{e(p['alt'])}" loading="lazy" width="400" height="400">{f'<img class="card-alt" src="{p["porte"]}" alt="" loading="lazy" width="480" height="480">' if p.get('porte') else ''}</a>
  <div class="card-b">
    <h3><a href="{p['url']}">{e(p['name'])}</a></h3>
    <p class="card-pcs">{e(pcs)}</p>
    <p class="card-price">{fmt(p['price'])}</p>
  </div>
  <button class="card-add" type="button" data-add="{p['sku']}" aria-label="Ajouter {e(p['name'])} au panier">+</button>
</article>'''

def offer_band(title='Plus tu en prends, moins chaque parure coûte'):
    return f'''<section class="offer-band" id="offre" aria-labelledby="offreT">
  <div class="wrap">
    <p class="kicker">L’offre CHARMED PARIS</p>
    <h2 id="offreT">{title}</h2>
    <div class="ob-grid">
      <div class="ob"><span class="ob-tab">Pour toi</span><p class="ob-n">1 parure</p><p class="ob-d">Livraison offerte dès 50 €</p></div>
      <div class="ob is-hl"><span class="ob-tab">Une pour toi, une à offrir</span><p class="ob-n">2 parures</p><p class="ob-d"><b>La 2e à −30 %</b></p></div>
      <div class="ob"><span class="ob-tab">Tous tes cadeaux de Noël</span><p class="ob-n">3 parures</p><p class="ob-d"><b>La 3e à −50 %</b>, à moitié prix</p></div>
    </div>
    <p class="ob-fine">Remise appliquée automatiquement au panier sur la parure la moins chère. Mélange les modèles comme tu veux. Hors Joaillerie 925.</p>
  </div>
</section>'''

# ---------------------------------------------------------------- pages
def build_home():
    essentials = ''.join(card(BY[s]) for s in ['JS1AQ5', 'JSGRQR', 'JSJB3S', 'JS63WT'])
    moment = ''.join(card(BY[s]) for s in ['JS4P8D', 'JS0DGC', 'JS4EXR', 'JS8445'])
    body = f'''
<section class="ed-hero" aria-labelledby="heroT">
  <div class="ed-hero-img"><img src="assets/img/ia/I4-post-molten-art-profil.webp" alt="Portrait de profil, boucles d’oreilles et collier de la parure Molten Art" width="1024" height="1280" fetchpriority="high"></div>
  <div class="ed-hero-in">
    <p class="kicker">CHARMED PARIS · Noël 2026</p>
    <h1 id="heroT">La parure<br><em>comme signature.</em></h1>
    <p class="sub">Le collier et les boucles, déjà assortis, livrés dans leur boîte cadeau. Commande avant le 4 décembre pour Noël.</p>
    <div class="ed-hero-cta"><a class="btn" href="collection.html">Choisir ma parure</a><a class="ed-link light" href="#offre">2 parures : la 2e à −30 %</a></div>
  </div>
  <span class="ed-hero-idx">01 / CHARMED PARIS</span>
</section>
<div class="sticky" data-hero-sticky hidden><div class="sticky-in"><span class="sticky-t"><b>La 2e parure à −30 %</b><small>la 3e à −50 %</small></span><a class="btn" href="collection.html">Choisir ma parure</a></div></div>
<div class="proof wrap" aria-label="Nos engagements">
  <p>{icon('truck')}Livrée en 4 à 9 jours ouvrés</p><p>{icon('shield')}Droits de douane payés</p><p>{icon('return')}14 jours pour changer d’avis</p>
</div>
<section class="ed-intro wrap" aria-labelledby="introT">
  <p class="kicker">L’univers CHARMED</p>
  <h2 id="introT">Une allure. <em>Mille expressions.</em></h2>
  <p class="txt">Un bijou n’est jamais un simple détail. Il accompagne un geste, souligne une silhouette et raconte quelque chose de toi. Chez nous, le collier et les boucles arrivent ensemble, déjà assortis.</p>
</section>
<section class="ed-cats wrap" aria-label="Explorer les univers">
  <a class="ed-cat" href="collection.html#sculpture"><img src="assets/img/cascade/05-portee.webp" alt="La parure Liquid Gold Cascade portée" loading="lazy" width="900" height="1125"><div><span>01 / Métal sculpté</span><h3>Sculpture</h3></div></a>
  <a class="ed-cat" href="collection.html#eclat"><img src="assets/img/ia/I3-post-golden-luxe-portee.webp" alt="La parure Golden Luxe portée" loading="lazy" width="900" height="1125"><div><span>02 / Doré et pierres</span><h3>Éclat</h3></div></a>
</section>
<section class="ed-prod wrap" aria-labelledby="essT">
  <div class="ed-head"><div><p class="kicker">Pièces choisies</p><h2 id="essT">Nos essentiels.</h2></div><a class="ed-link" href="collection.html">Voir les 30 parures</a></div>
  <div class="grid">{essentials}</div>
</section>
{offer_band()}
<section class="ed-story" aria-labelledby="storyT">
  <img src="assets/img/ia/I6-trio-flatlay.webp" alt="Trois parures CHARMED PARIS posées sur du lin" loading="lazy" width="1024" height="1024">
  <div class="ed-story-c">
    <p class="kicker">L’art du détail</p>
    <h2 id="storyT">Des pièces qui<br><em>ne passent pas inaperçues.</em></h2>
    <p class="txt">Formes fluides, éclats subtils, métal qui a l’air d’avoir fondu. Chaque parure se porte complète, ou pièce par pièce avec ce que tu as déjà.</p>
    <a class="ed-link" href="a-propos.html">Notre histoire</a>
  </div>
</section>
<section class="ed-prod wrap" aria-labelledby="momT">
  <div class="ed-head"><div><p class="kicker">Les pièces du moment</p><h2 id="momT">À découvrir.</h2></div><a class="ed-link" href="cadeaux.html">Idées cadeaux</a></div>
  <div class="grid">{moment}</div>
</section>
<section class="unbox" aria-labelledby="unboxT" style="margin-top:100px">
  <div class="wrap unbox-in">
    <div class="unbox-img"><img src="assets/img/pack/pack-f.webp" alt="Le colis CHARMED PARIS ouvert : carton blanc au logo, papier nid d’abeille, boîte cadeau au ruban à cœurs, carte de remerciement" loading="lazy" width="800" height="800"></div>
    <div class="unbox-c">
      <p class="kicker">Ce que tu reçois</p>
      <h2 id="unboxT">Un colis qu’on a envie d’ouvrir</h2>
      <ul class="checks">
        <li>{icon('check')}Le carton CHARMED PARIS, logo à l’intérieur du couvercle</li>
        <li>{icon('check')}La boîte cadeau blanche, nouée du ruban à petits cœurs dorés</li>
        <li>{icon('check')}La pochette en velours et la chamoisine pour l’entretien</li>
        <li>{icon('check')}Aucun prix dans le colis : tu peux l’envoyer directement</li>
        <li>{icon('check')}Jusqu’au 24 décembre, l’emballage de Noël est offert</li>
      </ul>
      <p class="fine">Une boîte cadeau par commande : avec plusieurs parures, les autres voyagent dans leur pochette scellée, dans le même colis.</p>
    </div>
  </div>
</section>
<section class="ed-end wrap" aria-labelledby="endT">
  <p class="kicker">Le style n’a pas de règles</p>
  <h2 id="endT">À porter. À associer.<br><em>À faire tienne.</em></h2>
  <a class="btn" href="collection.html">Choisir ma parure</a>
</section>
{faq_block(short=True)}
'''
    ld = [{'@context': 'https://schema.org', '@type': 'Organization', 'name': 'CHARMED PARIS', 'url': BASE_URL, 'logo': BASE_URL + 'assets/img/favicon-32.png'},
          {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'CHARMED PARIS', 'url': BASE_URL}]
    page('index.html', 'CHARMED PARIS · Parures de bijoux assorties, prêtes à offrir',
         'Parures collier + boucles d’oreilles, livrées dans leur boîte cadeau. 2 parures : la 2e à −30 %. 3 parures : la 3e à −50 %. Livraison offerte dès 50 €.', body, ld=ld, cls='home')

FAQ = [
    ('Quand vais-je recevoir ma commande ?', 'Ta commande est préparée en 1 à 2 jours ouvrés, puis livrée par DHL en 4 à 9 jours ouvrés en France (9 colis sur 10). Pour Noël en Europe, commande avant le vendredi 4 décembre.'),
    ('Comment fonctionne l’offre sur plusieurs parures ?', 'Dès 2 parures, la moins chère est à −30 %. Dès 3 parures, la moins chère est à −50 %. Au-delà, la règle se répète par groupe de 3. La remise s’applique toute seule dans le panier. Les parures de la Joaillerie 925 ne sont pas concernées.'),
    ('Est-ce que je vais payer des frais de douane ?', 'Non. Les droits et taxes d’importation sont déjà payés : rien à régler au livreur.'),
    ('Et si la parure ne me plaît pas ?', 'Tu as 14 jours après réception pour changer d’avis. Le retour est à nos frais et tu es remboursée sous 14 jours.'),
    ('Les bijoux craignent-ils l’eau ?', 'Oui : nos bijoux dorés sont en laiton doré. Retire-les avant la douche, la piscine et le sport, et mets ton parfum avant tes bijoux. Rangés dans leur pochette, ils gardent leur éclat plus longtemps.'),
    ('Puis-je l’envoyer directement à la personne ?', 'Oui. Le colis arrive dans sa boîte cadeau et ne contient aucun prix. Il n’est pas possible d’ajouter un message manuscrit.'),
]
def faq_block(short=False):
    items = FAQ[:4] if short else FAQ
    qs = ''.join(f'<details class="qa"><summary>{e(q)}{icon("chev")}</summary><p>{e(a)}</p></details>' for q, a in items)
    more = '<p><a class="lnk" href="faq.html">Toutes les questions</a></p>' if short else ''
    return f'<section class="sec wrap faq" aria-labelledby="faqT"><div class="sec-h"><div><p class="kicker">Questions fréquentes</p><h2 id="faqT">Avant de commander</h2></div></div><div class="qas">{qs}</div>{more}</section>'

def faq_ld():
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}

def build_collection():
    chips = '<button type="button" class="chip is-on" data-filter="all" aria-pressed="true">Toutes</button>' + ''.join(
        f'<button type="button" class="chip" data-filter="{k}" aria-pressed="false">{e(u["name"])}</button>' for k, u in UNIV.items())
    grid = ''.join(card(p) for p in PRODUCTS)
    body = f'''<section class="wrap page-h"><nav class="crumbs" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span>/</span><span aria-current="page">Toutes les parures</span></nav>
<h1>Toutes les parures</h1><p class="lead">30 parures assorties, collier et boucles d’oreilles. 2 parures : la 2e à −30 %. 3 parures : la 3e à −50 %.</p></section>
<section class="wrap coll">
  <div class="coll-bar"><div class="chips" role="group" aria-label="Filtrer par univers">{chips}</div>
  <label class="sort"><span>Trier</span><select data-sort><option value="">Sélection</option><option value="asc">Prix croissant</option><option value="desc">Prix décroissant</option></select></label></div>
  <p class="coll-n" data-count-res role="status">30 parures</p>
  <div class="grid" data-grid>{grid}</div>
</section>
{offer_band('Mélange les modèles, la remise suit')}'''
    ld = [{'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': BASE_URL + p['url'], 'name': p['name']} for i, p in enumerate(PRODUCTS)]}]
    page('collection.html', 'Toutes les parures de bijoux · CHARMED PARIS', 'Les 30 parures CHARMED PARIS : collier et boucles assortis, doré, argent 925, pierres de couleur. Livraison offerte dès 50 €.', body, ld=ld)

def build_product(p):
    gal = ''.join(f'<li><img src="{g}" alt="{e(p["alt"]) if i == 0 else ""}" width="800" height="800" {"fetchpriority=\"high\"" if i == 0 else "loading=\"lazy\""}></li>' for i, g in enumerate(p['gallery']))
    dots = ''.join(f'<button type="button" class="gdot{" is-on" if i == 0 else ""}" aria-label="Photo {i + 1}" data-g="{i}"></button>' for i in range(len(p['gallery'])))
    thumbs = ''.join(f'<button type="button" class="gth{" is-on" if i == 0 else ""}" data-g="{i}" aria-label="Voir la photo {i + 1}"><img src="{g}" alt="" loading="lazy" width="80" height="80"></button>' for i, g in enumerate(p['gallery']))
    pcs = ' + '.join(p['pcs'])
    u = UNIV[p['u']]
    if p['eligible']:
        tiers = ''
        for t in tiers_for(p):
            badge = f'<span class="tier-badge">{t["badge"]}</span>' if t.get('badge') else ''
            gift = f'<span class="tier-gift">{icon("gift")}+ Collier Golden Arc offert</span>' if t.get('gift') else ''
            tiers += f'''<label class="tier{" is-on" if t['n'] == 1 else ""}" data-tier="{t['n']}">
  <span class="tier-tab">{e(t['tab'])}</span>
  <input type="radio" name="tier" value="{t['n']}"{" checked" if t['n'] == 1 else ""}>
  <span class="tier-row"><span class="tier-radio" aria-hidden="true"></span><span class="tier-t">{t['title']}{badge}</span><span class="tier-p"><b data-tier-total="{t['n']}"></b><small data-tier-save="{t['n']}"></small></span></span>
  <span class="tier-note">{e(t['note'])}</span>{gift}
</label>'''
        buy = f'''<fieldset class="tiers" data-offer><legend class="tiers-l">Choisis ton offre</legend>{tiers}</fieldset>
<div class="slots" data-slots hidden><p class="slots-l">Choisis tes autres parures</p><div data-slot-list></div></div>'''
    else:
        buy = '<p class="note-925">Argent 925 et moissanite synthétique : ces parures sont livrées dans leur écrin en velours bleu, avec certificat GRA dès 0,1 carat. Elles ne sont pas concernées par l’offre sur plusieurs parures.</p>'
    acc = [
        ('Dans la parure', f'<p>{p["intro"]}</p>{p["inside"]}'),
        ('Matières et entretien', f'{p["mats"]}<p>À garder au sec : retire ta parure avant la douche, la piscine et le sport. Parfum et crème d’abord, bijoux ensuite. Range-la dans sa pochette en velours et essuie-la avec la chamoisine.</p>'),
        ('Livraison et retours', '<p>Préparée en 1 à 2 jours ouvrés, livrée par DHL en 4 à 9 jours ouvrés en France (9 colis sur 10), avec suivi. Expédiée depuis les entrepôts de notre partenaire hors Union européenne : les droits de douane sont déjà payés, rien à régler à la livraison.</p><p>Livraison offerte dès 50 €, sinon 4,90 €. Tu as 14 jours après réception pour changer d’avis : retour à nos frais, remboursement sous 14 jours.</p><p><a href="livraison-retours.html">Tout savoir sur la livraison et les retours</a></p>'),
        ('Ce que contient le colis', '<p>Le carton CHARMED PARIS, la boîte cadeau nouée du ruban à cœurs, la pochette en velours, la chamoisine et une carte de remerciement. Aucun prix dans le colis. Une boîte cadeau par commande : les autres parures voyagent dans leur pochette scellée, dans le même colis.</p><img src="assets/img/pack/pack-f-600.webp" alt="Le colis CHARMED PARIS ouvert" loading="lazy" width="600" height="600">'),
    ]
    accs = ''.join(f'<details class="acc"{" open" if i == 0 else ""}><summary>{t}{icon("chev")}</summary><div class="acc-b">{b}</div></details>' for i, (t, b) in enumerate(acc))
    same = [x for x in PRODUCTS if x['u'] == p['u'] and x['sku'] != p['sku']][:4]
    if len(same) < 4: same += [x for x in PRODUCTS if x['sku'] != p['sku'] and x not in same][:4 - len(same)]
    rel = ''.join(card(x) for x in same)
    ia = ' <span class="gal-note">Visuels réalisés à partir de la photo du produit.</span>' if p['sku'] in HD and p['sku'] != 'JS63WT' else ''
    body = f'''<div class="wrap pdp" data-pdp="{p['sku']}">
  <nav class="crumbs" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span>/</span><a href="{u['file']}">{e(u['name'])}</a><span>/</span><span aria-current="page">{e(p['name'])}</span></nav>
  <div class="pdp-grid">
    <div class="gal">
      <ul class="gal-main" data-gal tabindex="0" aria-label="Photos de la parure">{gal}</ul>
      <div class="gal-dots">{dots}</div>
      <div class="gal-th">{thumbs}</div>{ia}
    </div>
    <div class="buy">
      <p class="kicker">{e(u['name'])} · Parure {len(p['pcs'])} pièces</p>
      <h1>{e(p['name'])}</h1>
      <p class="buy-pcs">{e(pcs)} · {e(p['mat'])}</p>
      <p class="buy-price"><span data-unit>{fmt(p['price'])}</span><small>TTC</small></p>
      <p class="buy-line">{e(p['line'])}</p>
      {buy}
      <button class="btn btn-buy" type="button" data-buy="{p['sku']}">Ajouter au panier<span data-buy-total></span></button>
      <p class="eta" data-eta>{icon('truck')}<span>Livrée entre le <b data-eta-a>…</b> et le <b data-eta-b>…</b></span></p>
      <p class="xmas" data-xmas-note>{icon('gift')}<span>Pour Noël en Europe, commande avant le <b>vendredi 4 décembre</b>. Emballage de Noël offert.</span></p>
      <ul class="buy-proof"><li>{icon('shield')}Droits de douane payés</li><li>{icon('return')}14 jours pour changer d’avis, retour gratuit</li><li>{icon('box')}Livrée dans sa boîte cadeau, sans prix</li></ul>
      <div class="accs">{accs}</div>
    </div>
  </div>
</div>
<section class="sec wrap" aria-labelledby="relT"><div class="sec-h"><div><p class="kicker">À associer</p><h2 id="relT">Pour compléter ton offre</h2></div></div><div class="grid">{rel}</div></section>
<div class="sticky" data-sticky hidden><div class="sticky-in"><span class="sticky-t"><b>{e(p['name'])}</b><small data-sticky-p>{fmt(p['price'])}</small></span><button class="btn" type="button" data-sticky-buy>Ajouter au panier</button></div></div>'''
    ld = [{'@context': 'https://schema.org', '@type': 'Product', 'name': 'Parure ' + p['name'], 'sku': p['sku'], 'brand': {'@type': 'Brand', 'name': 'CHARMED PARIS'},
           'description': p['line'], 'image': [BASE_URL + g for g in p['gallery']], 'material': p['mat'],
           'offers': {'@type': 'Offer', 'price': f"{p['price']:.2f}", 'priceCurrency': 'EUR', 'availability': 'https://schema.org/InStock', 'url': BASE_URL + p['url'],
                      'shippingDetails': {'@type': 'OfferShippingDetails', 'shippingDestination': {'@type': 'DefinedRegion', 'addressCountry': 'FR'},
                                          'deliveryTime': {'@type': 'ShippingDeliveryTime', 'handlingTime': {'@type': 'QuantitativeValue', 'minValue': 1, 'maxValue': 2, 'unitCode': 'DAY'},
                                                           'transitTime': {'@type': 'QuantitativeValue', 'minValue': 3, 'maxValue': 7, 'unitCode': 'DAY'}}},
                      'hasMerchantReturnPolicy': {'@type': 'MerchantReturnPolicy', 'applicableCountry': 'FR', 'returnPolicyCategory': 'https://schema.org/MerchantReturnFiniteReturnWindow', 'merchantReturnDays': 14, 'returnFees': 'https://schema.org/FreeReturn'}}},
          {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
              {'@type': 'ListItem', 'position': 1, 'name': 'Accueil', 'item': BASE_URL},
              {'@type': 'ListItem', 'position': 2, 'name': u['name'], 'item': BASE_URL + 'collection.html'},
              {'@type': 'ListItem', 'position': 3, 'name': p['name'], 'item': BASE_URL + p['url']}]}]
    page(p['url'], f'Parure {p["name"]} · {pcs} · CHARMED PARIS', f'Parure {p["name"]} : {pcs.lower()}, {p["mat"].lower()}. {p["line"]} Livrée dans sa boîte cadeau.', body, ld=ld, cls='is-pdp')

def build_pieces():
    cards = ''.join(f'''<article class="card" data-sku="{x['sku']}"><div class="card-img"><img src="{x['img']}" alt="{e(x['name'])}" loading="lazy" width="400" height="400">{f'<img class="card-alt" src="{PORTE[x["sku"]]}" alt="" loading="lazy" width="480" height="480">' if x['sku'] in PORTE else ''}</div>
<div class="card-b"><h3>{e(x['name'])}</h3><p class="card-pcs">{e(x['line'])}</p><p class="card-price">{fmt(x['price'])}</p></div>
<button class="card-add" type="button" data-add="{x['sku']}" aria-label="Ajouter {e(x['name'])} au panier">+</button></article>''' for x in PIECES)
    body = f'''<section class="wrap page-h"><nav class="crumbs" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span>/</span><span aria-current="page">Pièces seules</span></nav>
<h1>Pièces seules</h1><p class="lead">Un collier à porter seul ou avec ta parure. Livraison offerte dès 50 €.</p></section>
<section class="wrap"><div class="grid">{cards}</div></section>'''
    page('pieces-seules.html', 'Colliers et pendentifs · Pièces seules · CHARMED PARIS', 'Colliers et pendentifs CHARMED PARIS à porter seuls ou avec une parure. Livraison offerte dès 50 €.', body)

def build_gifts():
    groups = [
        ('maman', 'Pour ta mère', 'Des pierres de couleur et des lignes nettes.', ['JS0DGC', 'JSX3G6', 'JS3GGZ', 'JSJB3S']),
        ('soeur', 'Pour ta sœur', 'Du doré sculpté, qui se porte avec un tee-shirt.', ['JSGRQR', 'JS63WT', 'JSG813', 'JS411P']),
        ('amie', 'Pour ta meilleure amie', 'Prenez-en une chacune : la 2e est à −30 %.', ['JS1AQ5', 'JS63VP', 'JS4EXR', 'JSB541']),
        ('moins-60', 'Moins de 60 €', 'Des parures complètes dès 49 €.', [p['sku'] for p in sorted(PRODUCTS, key=lambda x: x['price']) if p['price'] < 60][:4]),
    ]
    sec = ''.join(f'<section class="sec wrap" id="{i}" aria-labelledby="{i}T"><div class="sec-h"><div><h2 id="{i}T">{t}</h2><p class="lead">{d}</p></div></div><div class="grid">{"".join(card(BY[s]) for s in skus)}</div></section>' for i, t, d, skus in groups)
    body = f'''<section class="wrap page-h"><nav class="crumbs" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span>/</span><span aria-current="page">Idées cadeaux</span></nav>
<h1>Idées cadeaux</h1><p class="lead">Une parure arrive dans sa boîte cadeau, sans aucun prix dans le colis. Pour Noël en Europe, commande avant le vendredi 4 décembre.</p></section>{sec}{offer_band()}'''
    page('cadeaux.html', 'Idées cadeaux bijoux pour Noël · CHARMED PARIS', 'Idées cadeaux : parures de bijoux pour ta mère, ta sœur, ta meilleure amie, et à moins de 50 €. Livrées dans leur boîte cadeau.', body)

def build_cart():
    body = f'''<section class="wrap page-h"><nav class="crumbs" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span>/</span><span aria-current="page">Panier</span></nav><h1>Ton panier</h1></section>
<section class="wrap cart-page"><div class="cart-main" data-cart-body></div><aside class="cart-side" data-cart-foot></aside></section>'''
    page('panier.html', 'Panier · CHARMED PARIS', 'Ton panier CHARMED PARIS.', body, robots='noindex,follow', cls='is-cart')

def build_checkout():
    body = f'''<section class="wrap page-h"><h1>Commande</h1><p class="lead">Livraison offerte dès 50 € · droits de douane payés · 14 jours pour changer d’avis.</p></section>
<section class="wrap co">
  <form class="co-form" data-checkout novalidate>
    <fieldset><legend>1. Contact</legend>
      <label class="f"><span>E-mail</span><input type="email" name="email" autocomplete="email" required></label>
      <label class="chk"><input type="checkbox" name="news"><span>Je veux recevoir les nouveautés par e-mail (désinscription en un clic).</span></label>
    </fieldset>
    <fieldset><legend>2. Livraison</legend>
      <div class="f2"><label class="f"><span>Prénom</span><input name="fn" autocomplete="given-name" required></label><label class="f"><span>Nom</span><input name="ln" autocomplete="family-name" required></label></div>
      <label class="f"><span>Adresse</span><input name="ad" autocomplete="address-line1" required></label>
      <label class="f"><span>Complément d’adresse <small>(facultatif)</small></span><input name="ad2" autocomplete="address-line2"></label>
      <div class="f2"><label class="f"><span>Code postal</span><input name="zip" autocomplete="postal-code" inputmode="numeric" required></label><label class="f"><span>Ville</span><input name="city" autocomplete="address-level2" required></label></div>
      <label class="f"><span>Pays</span><select name="country" autocomplete="country"><option>France</option><option>Belgique</option><option>Suisse</option><option>Luxembourg</option><option>Allemagne</option><option>Espagne</option><option>Italie</option><option>Pays-Bas</option></select></label>
      <label class="f"><span>Téléphone <small>(pour le livreur DHL)</small></span><input type="tel" name="tel" autocomplete="tel" required></label>
      <div class="ship-opt">{icon('truck')}<span><b>Livraison suivie DHL</b><small>4 à 9 jours ouvrés · droits de douane payés</small></span><b data-co-ship></b></div>
    </fieldset>
    <fieldset><legend>3. Paiement</legend>
      <div class="pay-opts"><label class="pay"><input type="radio" name="pay" checked><span>Carte bancaire</span></label><label class="pay"><input type="radio" name="pay"><span>Apple Pay</span></label><label class="pay"><input type="radio" name="pay"><span>Google Pay</span></label></div>
      <p class="fine">{icon('lock')}Paiement chiffré, traité par notre prestataire de paiement. Nous ne voyons jamais ton numéro de carte.</p>
    </fieldset>
    <label class="chk"><input type="checkbox" name="cgv" required><span>J’ai lu et j’accepte les <a href="cgv.html" target="_blank">conditions générales de vente</a>.</span></label>
    <button class="btn btn-buy" type="submit">Commander avec obligation de paiement<span data-co-total></span></button>
    <p class="fine" data-co-msg role="status"></p>
  </form>
  <aside class="cart-side co-side" data-cart-foot data-mode="checkout"></aside>
</section>'''
    page('commande.html', 'Commande · CHARMED PARIS', 'Finalise ta commande CHARMED PARIS.', body, robots='noindex,nofollow', cls='is-checkout')

# ---------------------------------------------------------------- pages éditoriales et légales
def md(text):
    out, lst = [], None
    def inline(s):
        s = e(s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
        s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
        return s
    for line in text.splitlines():
        if re.match(r'^\s*[-*] ', line):
            if lst is None: out.append('<ul>'); lst = True
            out.append('<li>' + inline(re.sub(r'^\s*[-*] ', '', line)) + '</li>'); continue
        if lst: out.append('</ul>'); lst = None
        m = re.match(r'^(#{1,4}) (.*)', line)
        if m:
            lvl = min(len(m.group(1)) + 1, 4)
            if len(m.group(1)) == 1: continue
            out.append(f'<h{lvl}>{inline(m.group(2))}</h{lvl}>')
        elif line.strip().startswith('>'):
            out.append('<p class="fine">' + inline(line.strip('> ')) + '</p>')
        elif line.strip() and not line.startswith('|') and line.strip() != '---':
            out.append('<p>' + inline(line.strip()) + '</p>')
    if lst: out.append('</ul>')
    return '\n'.join(out)

def text_page(file, title, desc, h1, html_body, robots='index,follow', ld=None):
    body = f'''<section class="wrap page-h"><nav class="crumbs" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span>/</span><span aria-current="page">{e(h1)}</span></nav><h1>{e(h1)}</h1></section>
<article class="wrap prose">{html_body}</article>'''
    page(file, title, desc, body, robots=robots, ld=ld)

def build_texts():
    for f, src, h1 in [('cgv.html', 'cgv.md', 'Conditions générales de vente'), ('mentions-legales.html', 'mentions-legales.md', 'Mentions légales'),
                       ('confidentialite.html', 'politique-confidentialite.md', 'Politique de confidentialité'), ('cookies.html', 'politique-cookies.md', 'Cookies'),
                       ('retractation.html', 'retours-et-retractation.md', 'Retours et rétractation')]:
        txt = (W / 'legal' / src).read_text()
        text_page(f, f'{h1} · CHARMED PARIS', f'{h1} de la boutique CHARMED PARIS.', h1, md(txt), robots='index,follow')
    text_page('livraison-retours.html', 'Livraison et retours · CHARMED PARIS', 'Délais de livraison, droits de douane, retours sous 14 jours.', 'Livraison et retours', f'''
<h2>Délais</h2><p>Ta commande est préparée en 1 à 2 jours ouvrés, puis livrée par DHL avec suivi. En France, compte 4 à 9 jours ouvrés entre ta commande et la livraison (9 colis sur 10). Belgique, Allemagne, Espagne : 4 à 9 jours ouvrés. Pays-Bas : 4 à 6. Italie : 3 à 10.</p>
<h2>Noël</h2><p>Pour une livraison avant Noël en Europe, commande avant le <b>vendredi 4 décembre 2026</b>. Jusqu’au 24 décembre, ton colis part dans son emballage de Noël, sans supplément.</p>
<h2>Frais</h2><p>Livraison offerte dès 50 €, sinon 4,90 €. Un seul mode de livraison, sans option express. Les droits de douane et taxes d’importation sont déjà payés : rien à régler au livreur.</p>
<h2>D’où part ton colis</h2><p>Nos bijoux sont expédiés depuis les entrepôts de notre partenaire, aux États-Unis ou en Chine. Plusieurs articles arrivent dans un seul colis.</p>
<h2>Changer d’avis</h2><p>Tu as 14 jours après réception pour te rétracter, sans avoir à te justifier. Le retour est à nos frais et tu es remboursée sous 14 jours après réception du retour. <a href="retractation.html">Me rétracter en ligne</a>.</p>
<h2>Un souci avec ta parure ?</h2><p>Colis abîmé, bijou défectueux ou erreur de modèle : écris-nous avec une photo dans les 10 jours qui suivent la livraison, nous te renvoyons la bonne parure. La garantie légale de conformité de 2 ans s’applique dans tous les cas.</p>''')
    text_page('faq.html', 'Questions fréquentes · CHARMED PARIS', 'Livraison, offre sur plusieurs parures, douane, retours, entretien : les réponses.', 'Questions fréquentes',
              ''.join(f'<h2>{e(q)}</h2><p>{e(a)}</p>' for q, a in FAQ), ld=[faq_ld()])
    text_page('matieres-entretien.html', 'Matières et entretien · CHARMED PARIS', 'Laiton doré, oxydes de zirconium, argent 925, moissanite synthétique : nos matières et comment les entretenir.', 'Matières et entretien', '''
<h2>Laiton doré</h2><p>La plupart de nos parures sont en laiton doré par électrolyse, avec un revêtement anti-ternissement. Ce n’est pas de l’or massif.</p>
<h2>Oxydes de zirconium</h2><p>Les pierres claires et de couleur de nos parures Éclat et Couleur précieuse sont des oxydes de zirconium.</p>
<h2>Argent 925 et moissanite synthétique</h2><p>La Joaillerie 925 est en argent 925 estampillé, sertie de moissanite synthétique. Certificat GRA fourni dès 0,1 carat.</p>
<h2>Entretien</h2><ul><li>Retire ta parure avant la douche, la piscine et le sport : l’eau, le savon et le chlore usent la dorure.</li><li>Parfum et crème d’abord, bijoux ensuite.</li><li>Range-la dans sa pochette en velours et essuie-la avec la chamoisine fournie.</li></ul>''')
    text_page('a-propos.html', 'Notre histoire · CHARMED PARIS', 'CHARMED PARIS : des parures assorties, livrées prêtes à offrir.', 'Notre histoire', '''
<p>CHARMED PARIS est né d’un agacement simple : trouver des boucles d’oreilles qui vont vraiment avec un collier prend des heures. Alors on ne vend que des parures, déjà assorties.</p>
<p>Chaque parure arrive dans notre boîte cadeau, avec sa pochette en velours et sa chamoisine. Aucun prix dans le colis : tu peux l’envoyer directement à la personne.</p>
<h2 id="contact">Nous écrire</h2><p>Une question avant de commander, un souci avec ta parure : écris-nous à <a href="mailto:bonjour@charmedparis.fr">bonjour@charmedparis.fr</a>. Nous répondons du lundi au vendredi.</p>''')

def build_404():
    page('404.html', 'Page introuvable · CHARMED PARIS', 'Cette page n’existe pas.', '<section class="wrap page-h"><h1>Cette page n’existe pas</h1><p class="lead">Elle a peut-être changé d’adresse.</p><p><a class="btn" href="collection.html">Voir les parures</a></p></section>', robots='noindex')

def write_data():
    data = {'offer': OFFER, 'univers': {k: v['name'] for k, v in UNIV.items()},
            'products': [{k: p[k] for k in ('sku', 'name', 'price', 'u', 'pcs', 'thumb', 'url', 'eligible')} for p in PRODUCTS],
            'pieces': [{'sku': x['sku'], 'name': x['name'], 'price': x['price'], 'thumb': x['img'], 'url': 'pieces-seules.html', 'pcs': ['Collier'], 'eligible': False, 'u': 'piece'} for x in PIECES]}
    (SITE / 'assets/js/data.js').write_text('/* Généré par site/_build/build.py. Ne pas modifier à la main. */\nwindow.CP=' + json.dumps(data, ensure_ascii=False) + ';\n')

def write_sitemap():
    files = ['index.html', 'collection.html', 'pieces-seules.html', 'cadeaux.html', 'livraison-retours.html', 'faq.html', 'matieres-entretien.html', 'a-propos.html', 'cgv.html', 'mentions-legales.html', 'confidentialite.html', 'cookies.html', 'retractation.html'] + [p['url'] for p in PRODUCTS]
    today = datetime.date.today().isoformat()
    (SITE / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{BASE_URL}{"" if f == "index.html" else f}</loc><lastmod>{today}</lastmod></url>\n' for f in files) + '</urlset>\n')
    (SITE / 'robots.txt').write_text(f'User-agent: *\nDisallow: /panier.html\nDisallow: /commande.html\nSitemap: {BASE_URL}sitemap.xml\n')

if __name__ == '__main__':
    write_data(); build_home(); build_collection(); build_pieces(); build_gifts(); build_cart(); build_checkout(); build_texts(); build_404()
    for p in PRODUCTS: build_product(p)
    write_sitemap()
    print('ok', len(PRODUCTS), 'parures')
