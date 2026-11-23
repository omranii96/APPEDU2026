#!/usr/bin/env python3
"""
CHARMED PARIS · générateur du prototype statique (site/).

Lit les sources du dépôt (contenus, SEO, légal, logos) et écrit les pages HTML
autonomes de site/ + assets/js/catalogue.js. Les pages partagent le même en-tête,
le même pied de page et le même tiroir panier (fonctions chrome()).

Usage :  python3 site/_build/build.py      (depuis la racine du dépôt ou ailleurs)
Dépendance : markdown (pip install markdown) pour les pages légales.
"""
import csv, html, json, re, unicodedata
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
W = ROOT / 'woocommerce'
DOMAIN = 'https://charmedparis.com'

# ------------------------------------------------------------------ utilitaires
def a(s):  # attribut
    return html.escape(str(s), quote=True)

def e(s):  # texte
    return html.escape(str(s), quote=False)

def el(tag, fr, en, cls='', **attrs):
    """Élément court bilingue : texte FR dans le DOM, EN dans data-en."""
    at = ''.join(f' {k.replace("_", "-")}="{a(v)}"' for k, v in attrs.items())
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c}{at} data-en="{a(en)}">{e(fr)}</{tag}>'

def elh(tag, fr, en, cls='', **attrs):
    """Élément bilingue avec HTML interne (data-en-html)."""
    at = ''.join(f' {k.replace("_", "-")}="{a(v)}"' for k, v in attrs.items())
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c}{at} data-en-html="{a(en)}">{fr}</{tag}>'

def bi(fr, en):
    """Bloc long bilingue : deux versions, l'une masquée en CSS selon html.lang-en."""
    return f'<div data-lang="fr" lang="fr">{fr}</div><div data-lang="en" lang="en">{en}</div>'

def slugify(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)

RENAMES = {'Emerald Dreams': 'Green Dreams', 'Emerald Square': 'Green Square', 'Royal Sapphire': 'Royal Blue Halo'}
def renamed(s):
    for k, v in RENAMES.items():
        s = s.replace(k, v)
    return s

def fix_fr(s):
    """Vocabulaire légal : « oxyde de zirconium » plutôt que « zircone » ; coquilles des sources."""
    for k, v in [('de zircones', "d'oxydes de zirconium"), ('zircones colorées', 'oxydes de zirconium colorés'), ('Zircones', 'Oxydes de zirconium'),
                 ('zircones', 'oxydes de zirconium'), ('en zircone', 'en oxyde de zirconium'), ('zircone', 'oxyde de zirconium'),
                 ('Le oxyde de zirconium, ou oxyde de zirconium,', "L'oxyde de zirconium"), ('oxydes de zirconium (oxydes de zirconium)', 'oxydes de zirconium'),
                 ('**Oxydes de zirconium.** Oxydes de zirconium, des pierres', '**Oxydes de zirconium.** Des pierres')]:
        s = s.replace(k, v)
    return s

TODO_RE = re.compile(r'\[(À COMPLÉTER|À VÉRIFIER|À DÉCIDER|À CONFIRMER|TO COMPLETE|TO CHECK|TO DECIDE)([^\]]*)\]')
def todo(s):
    return TODO_RE.sub(lambda m: f'<mark class="todo">[{m.group(1)}{m.group(2)}]</mark>', s)

NOTE_START = re.compile(r'^\s*(\*\*)?(Note interne|Internal note|À confirmer|Note :|Note:|Faits packaging|Délais|Corrections|Titre modifié|To confirm)', re.I)
def md(text):
    """Markdown → HTML ; les blockquotes « note interne / à confirmer » deviennent des notes de maquette."""
    out, buf, lines = [], [], text.split('\n')
    i = 0
    while i < len(lines):
        if lines[i].startswith('>'):
            grp = []
            while i < len(lines) and lines[i].startswith('>'):
                grp.append(re.sub(r'^>\s?', '', lines[i])); i += 1
            if NOTE_START.match(grp[0]):
                inner = markdown.markdown('\n'.join(grp), extensions=['tables', 'sane_lists'])
                out.append(markdown.markdown('\n'.join(buf), extensions=['tables', 'sane_lists'])); buf = []
                out.append(f'<aside class="mock-note"><b>Note interne (maquette)</b>{todo(inner)}</aside>')
            else:
                buf.extend('> ' + g for g in grp)
            continue
        buf.append(lines[i]); i += 1
    out.append(markdown.markdown('\n'.join(buf), extensions=['tables', 'sane_lists']))
    return todo(''.join(out))

def read(p):
    return Path(p).read_text(encoding='utf-8')

# ------------------------------------------------------------------ sources
PAGES_FR = fix_fr(renamed(read(W / 'contenus/pages.md')))
PAGES_EN = renamed(read(W / 'contenus/pages-en.md'))

def section(src, start_pat, stop_pat=r'\n(## |---)'):
    m = re.search(start_pat, src)
    if not m:
        raise KeyError(start_pat)
    rest = src[m.end():]
    s = re.search(stop_pat, rest)
    return rest[:s.start()] if s else rest

def seo_rows(path):
    raw = read(path).lstrip('﻿')
    return list(csv.DictReader(raw.splitlines(), delimiter=';'))
SEO_FR, SEO_EN = seo_rows(W / 'seo/mots-cles-par-page.csv'), seo_rows(W / 'seo/mots-cles-par-page-en.csv')
def seo(fr_page, en_page):
    f = next(r for r in SEO_FR if r['page'] == fr_page)
    g = next(r for r in SEO_EN if r['page'] == en_page)
    return {'title': fix_fr(f['title']), 'title_en': g['title'], 'desc': fix_fr(f['meta_description']), 'desc_en': g['meta_description'],
            'h1': fix_fr(f['h1']), 'h1_en': g['h1'], 'url': f['url'], 'url_en': g['url']}

# ------------------------------------------------------------------ logos (SVG vectorisés de la charte)
def logo(kind, cls):
    src = read(W / f'identite/logos/{kind}')
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    body = ''
    for attrs in re.findall(r'<path ([^>]*?)/>', src):
        fill = re.search(r'fill="([^"]+)"', attrs).group(1)
        c = 'lg-tx' if fill.upper() in ('#1A1015',) else 'lg-br'
        body += f'<path class="{c}" ' + re.sub(r'fill="[^"]+"\s*', '', attrs) + '/>'
    return f'<svg class="logo-svg {cls}" viewBox="{vb}" aria-hidden="true" focusable="false">{body}</svg>'
LOGO_H = logo('horizontal/charmed-paris-horizontal-grenat.svg', 'logo-h')
LOGO_P = logo('principal/charmed-paris-principal-grenat.svg', 'logo-p')
LOGO_FOOT = logo('principal/charmed-paris-principal-grenat.svg', 'logo-f')

# ------------------------------------------------------------------ univers
UNIVERS = {
    'sculpture': dict(fr='Sculpture', en='Sculpture', file='univers-sculpture.html', seo=('Univers Sculpture', 'Collection Sculpture'), md='2.1 Sculpture', mden='2.1 Sculpture',
                      line_fr='7 parures · métal doré et argenté', line_en='7 sets · gold and silver tones', hook_fr='Des formes fondues, comme des pièces de galerie.', hook_en='Molten shapes, like pieces from a gallery.',
                      facts_fr='Laiton doré ou finition argentée · perles de culture · à garder au sec', facts_en='Gold-plated brass or silver tone · cultured pearls · keep dry',
                      img='assets/img/cascade/01-parure-or.webp'),
    'eclat': dict(fr='Éclat', en='Sparkle', file='univers-eclat.html', seo=('Univers Éclat', 'Collection Sparkle (Éclat)'), md='2.2 Éclat', mden='2.2 Sparkle',
                  line_fr='11 parures · doré et oxydes de zirconium', line_en='11 sets · gold and cubic zirconia', hook_fr='La lumière, du collier aux oreilles.', hook_en='Light, from neckline to earlobe.',
                  facts_fr='Laiton doré et oxydes de zirconium · à garder au sec', facts_en='Gold-plated brass and cubic zirconia · keep dry', img='assets/img/produits/JS63VP.webp'),
    'couleur': dict(fr='Couleur précieuse', en='Precious Colour', file='univers-couleur-precieuse.html', seo=('Univers Couleur précieuse', 'Collection Colored Stones'), md='2.3 Couleur précieuse', mden='2.3 Precious Colour',
                    line_fr='7 parures · vert, bleu, rose', line_en='7 sets · green, blue, pink', hook_fr='Une pierre de couleur, en écho.', hook_en='One coloured stone, repeated.',
                    facts_fr='Oxydes de zirconium de couleur · doré, argenté ou rosé · à garder au sec', facts_en='Coloured cubic zirconia · gold, silver or rose tone · keep dry', img='assets/img/produits/JSX3G6.webp'),
    'j925': dict(fr='Joaillerie 925', en='925 Silver', file='univers-joaillerie-925.html', seo=('Univers Joaillerie 925', 'Collection Sterling Silver 925'), md='2.4 Joaillerie 925', mden='2.4 925 Silver',
                 line_fr='3 parures · argent 925', line_en='3 sets · sterling silver', hook_fr='Argent 925 et moissanites synthétiques.', hook_en='Sterling silver and lab-grown moissanite.',
                 facts_fr='Argent 925 estampillé · moissanite synthétique · certificat GRA dès 0,1 ct', facts_en='Stamped 925 sterling silver · lab-grown moissanite · GRA certificate from 0.1 ct', img='assets/img/produits/JSDQA1.webp'),
    'mixte': dict(fr='Mixte', en='Unisex', file='univers-mixte.html', seo=('Univers Mixte', 'Collection Unisex'), md='2.5 Mixte', mden='2.5 Unisex',
                  line_fr='2 parures · sur cordon', line_en='2 sets · on cord', hook_fr='À porter à deux, ou à partager.', hook_en='To wear together, or to share.',
                  facts_fr='Laiton doré sur cordon noir réglable · à garder au sec', facts_en='Gold-plated brass on adjustable black cord · keep dry', img='assets/img/produits/JSVKMZ.webp'),
}
CAT2U = {'Sculpture': 'sculpture', 'Éclat': 'eclat', 'Couleur précieuse': 'couleur', 'Joaillerie 925': 'j925', 'Mixte': 'mixte'}
for k, u in UNIVERS.items():
    blk_fr = section(PAGES_FR, r'### ' + re.escape(u['md']) + r'\n', r'\n(### |## |---)')
    blk_en = section(PAGES_EN, r'### ' + re.escape(u['mden']) + r'\n', r'\n(### |## |---)')
    u['intro_fr'] = re.search(r'\*\*Intro\*\*\n(.+?)\n\n', blk_fr, re.S).group(1).strip()
    u['seo_fr'] = re.search(r'\*\*Texte SEO bas de page\*\*\n(.+?)(\n\n|$)', blk_fr, re.S).group(1).strip()
    u['intro_en'] = re.search(r'\*\*Intro\*\*\n(.+?)\n\n', blk_en, re.S).group(1).strip()
    u['seo_en'] = re.search(r'\*\*SEO text \(bottom of page\)\*\*\n(.+?)(\n\n|$)', blk_en, re.S).group(1).strip()
    u['meta'] = seo(*u['seo'])

# ------------------------------------------------------------------ produits (30 parures)
def rows(p):
    return {r['SKU']: r for r in csv.DictReader(open(p, encoding='utf-8-sig'))}
PFR, PEN = rows(W / 'contenus/produits-woocommerce.csv'), rows(W / 'contenus/produits-woocommerce-en.csv')
CUTS = {p.stem for p in (SITE / 'assets/img/detoures').glob('*.webp')}

def first_p(h):
    m = re.search(r'<p>(.*?)</p>', h, re.S)
    return strip_tags(m.group(1)) if m else ''

PRODUCTS, codes = [], set()
for sku, f in PFR.items():
    g = PEN[sku]
    name_fr, name_en = renamed(f['Name']), renamed(g['Name'])
    model = name_fr.replace('Parure ', '')
    u = CAT2U[f['Categories'].split(',')[0].split('>')[1].strip()]
    mat_fr, mat_en = f['Attribute 2 value(s)'], g['Attribute 2 value(s)']
    pcs_fr = [x.strip() for x in f['Attribute 1 value(s)'].split(',')]
    pcs_en = [x.strip() for x in g['Attribute 1 value(s)'].split(',')]
    metal = '925' if 'Argent 925' in mat_fr else 'rose' if 'rosée' in mat_fr else 'argente' if 'argentée' in mat_fr else 'bicolore' if 'bicolore' in mat_fr else 'dore'
    words = re.sub(r'[^A-Za-z ]', '', model).split()
    code = (words[0][:2] + words[1][0]).upper() if len(words) > 1 else words[0][:3].upper()
    while code in codes:
        code = code[:2] + chr(ord(code[2]) + 1)
    codes.add(code)
    p = dict(sku=sku, model=model, slug=slugify(model), name={'fr': name_fr, 'en': name_en}, price=int(float(f['Regular price'])), u=u,
             pcs={'fr': pcs_fr, 'en': pcs_en}, mat={'fr': mat_fr, 'en': mat_en}, metal=metal, ring='Bague' in pcs_fr, code=code,
             img=f'assets/img/produits/{sku}.webp', cut=f'assets/img/detoures/{sku}.webp' if sku in CUTS else None,
             line={'fr': renamed(first_p(f['Short description'])), 'en': renamed(first_p(g['Short description']))},
             short_fr=renamed(f['Short description']), short_en=renamed(g['Short description']),
             desc_fr=fix_fr(renamed(f['Description'])), desc_en=renamed(g['Description']), tags=f['Tags'] + ', ' + g['Tags'],
             todo=f['Meta: _charmed_a_confirmer'])
    p['url'] = f'parure-{p["slug"]}.html'
    p['alt'] = {'fr': f'{name_fr} : {" + ".join(pcs_fr).lower()}, {mat_fr.lower()}', 'en': f'{name_en}: {" + ".join(pcs_en).lower()}, {mat_en.lower()}'}
    row = next(r for r in SEO_FR if f'({sku})' in r['page'])
    row_en = next(r for r in SEO_EN if f'({sku})' in r['page'])
    p['meta'] = {'title': fix_fr(row['title']), 'title_en': row_en['title'], 'desc': fix_fr(row['meta_description']), 'desc_en': row_en['meta_description'],
                 'h1': fix_fr(row['h1']), 'h1_en': row_en['h1'], 'url': row['url'], 'url_en': row_en['url']}
    PRODUCTS.append(p)

# Liquid Gold Cascade : nouvelles photos HD (or + argent), finition au choix, photo portée générée par IA
CASC = next(p for p in PRODUCTS if p['sku'] == 'JS63WT')
CASC.update(img='assets/img/cascade/01-parure-or.webp', cut='assets/img/cascade/01-parure-or-detoure.webp', metal='dore-argent',
            mat={'fr': 'Laiton doré ou finition argentée', 'en': 'Gold-plated brass or silver tone'},
            variants=[{'id': 'or', 'fr': 'Dorée', 'en': 'Gold-plated', 'slide': 0},
                      {'id': 'argent', 'fr': 'Argentée', 'en': 'Silver tone', 'slide': 3, 'img': 'assets/img/cascade/04-or-et-argent.webp'}])
CASC['alt'] = {'fr': 'Parure Liquid Gold Cascade : collier pendentif en lames dorées et boucles en franges, dorés', 'en': 'Liquid Gold Cascade set: gold blade pendant necklace and fringe earrings'}
BY = {p['sku']: p for p in PRODUCTS}
U_ORDER = ['sculpture', 'eclat', 'couleur', 'j925', 'mixte']
PRODUCTS.sort(key=lambda p: (U_ORDER.index(p['u']), p['price']))
for k, u in UNIVERS.items():
    u['count'] = sum(1 for p in PRODUCTS if p['u'] == k)

# Pièces seules (décision du 23/11/2026, woocommerce/source/pieces-seules.md) : prix à confirmer, pas encore en vente
PIECES = [
    dict(id='JNEXV0', img='secret-heart-key-necklace-JNEXV0.webp', fr='Collier Clé et cœur', en='Key & Heart necklace', mat_fr='Doré, pavé de petites pierres claires (carat de la dorure à relever)', mat_en='Gold-plated, paved with small clear stones (plating karat to confirm)', ref='JNEXV0'),
    dict(id='JNEJ8J', img='golden-arc-necklace-JNEJ8J.webp', fr='Collier Arc', en='Arc necklace', mat_fr="Doré à l'or 14 carats, cinq oxydes de zirconium en arc", mat_en='14K gold-plated, five cubic zirconia in an arc', ref='JNEJ8J'),
    dict(id='JNQXAH', img='golden-crescent-layer-set-JNQXAH.webp', fr='Collier Croissant à rangs', en='Layered Crescent necklace', mat_fr='Acier 304, finition PVD dorée (3 ou 4 rangs : à vérifier)', mat_en='304 steel, gold PVD finish (3 or 4 layers: to check)', ref='JNQXAH'),
    dict(id='JNPCC0', img='emerald-dreams-necklace-JNPCC0.webp', fr='Collier Pierre verte', en='Green Stone necklace', mat_fr='Argent 925 doré, pierre verte taille coussin (oxyde de zirconium vert, à confirmer)', mat_en='Gold-plated 925 silver, green cushion-cut stone (green cubic zirconia, to confirm)', ref='JNPCC0'),
    dict(id='JNDEG4', img='curve-statement-necklace-JNDEG4.webp', fr='Collier Courbe', en='Curve necklace', mat_fr='Argent 925 doré, pendentif courbe sculpturale', mat_en='Gold-plated 925 silver, sculptural curve pendant', ref='JNDEG4'),
    dict(id='MOISS', img='teardrop-brilliance-necklace-JNYA6X.webp', fr='Pendentif Goutte moissanite', en='Moissanite Drop pendant', mat_fr='Argent 925, moissanite synthétique ; écrin en velours bleu, certificat GRA dès 0,1 ct', mat_en='925 sterling silver, lab-grown moissanite; blue velvet case, GRA certificate from 0.1 ct', ref='à confirmer (photo indicative : JNYA6X)', ref_en='to confirm (indicative photo: JNYA6X)'),
]
PIECE_MEN = dict(id='PLUME', fr='Pendentif Plume', en='Feather pendant', mat_fr='Argenté avec accent doré (matière exacte à confirmer)', mat_en='Silver tone with a gold accent (exact material to confirm)', ref='à confirmer dans le compte', ref_en='to confirm in the supplier account')

# ------------------------------------------------------------------ catalogue.js
def write_catalogue():
    keep = ['sku', 'model', 'name', 'price', 'u', 'pcs', 'mat', 'metal', 'ring', 'code', 'img', 'cut', 'line', 'url', 'alt', 'variants']
    data = {'products': [{k: p[k] for k in keep if k in p} | {'tags': p['tags']} for p in PRODUCTS],
            'univers': {k: {'name': {'fr': u['fr'], 'en': u['en']}, 'url': u['file']} for k, u in UNIVERS.items()}}
    js = '/* Généré par site/_build/build.py depuis woocommerce/contenus/produits-woocommerce(.csv|-en.csv). Ne pas modifier à la main. */\nwindow.CP = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'
    (SITE / 'assets/js/catalogue.js').write_text(js, encoding='utf-8')

# ------------------------------------------------------------------ icônes (trait 1,5 px, Lucide-like)
IC = {
    'truck': '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17" cy="17.5" r="1.6"/>',
    'shield': '<path d="M12 3l7 3v6c0 4-3 7-7 9-4-2-7-5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    'return': '<path d="M9 14L4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 0 12h-3"/>',
    'gift': '<path d="M4 10h16v10H4zM3 7h18v3H3zM12 7v13M12 7c-2-4-6-3-5 0M12 7c2-4 6-3 5 0"/>',
    'lock': '<rect x="5" y="11" width="14" height="9"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    'clock': '<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>',
    'globe': '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.6 2.5 14.4 0 17M12 3.5c-2.5 2.6-2.5 14.4 0 17"/>',
    'star': '<path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9"/>',
    'drop': '<path d="M12 3c4 5 6 8 6 11a6 6 0 0 1-12 0c0-3 2-6 6-11z"/>',
    'search': '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
    'bag': '<path d="M5 8h14l-1 12H6z"/><path d="M9 8a3 3 0 0 1 6 0"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'close': '<path d="M6 6l12 12M18 6L6 18"/>',
}
def icon(n):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{IC[n]}</svg>'

# ------------------------------------------------------------------ chrome commun
NAV = [('parures.html', 'Parures', 'Sets'), ('univers', 'Univers', 'Collections'), ('pieces-seules.html', 'Pièces seules', 'Single pieces'), ('cadeaux.html', 'Cadeaux', 'Gifts')]

def annonce():
    def p(per, fr, en, hidden=False):
        return f'<p data-period="{per}" style="margin:0"{" hidden" if hidden else ""} data-en-html="{a(en)}">{fr}</p>'
    s = '<span class="sep" aria-hidden="true">·</span>'
    return ('<div class="annonce" role="region" aria-label="Informations commande" data-en-aria-label="Order information">'
            + p('avant', f"Noël en Europe : commande avant le vendredi 4/12 {s} Emballage de Noël offert jusqu'au 24/12 {s} Livraison offerte dès 50 € {s} 2e parure −15 %",
                f"Christmas in Europe: order by Friday 4/12 {s} Free Christmas wrapping until 24/12 {s} Free delivery from €50 {s} 15% off your second set")
            + p('apres', f"Emballage de Noël offert jusqu'au 24/12 {s} Livraison avant Noël non garantie {s} Livraison offerte dès 50 € {s} 2e parure −15 %",
                f"Free Christmas wrapping until 24/12 {s} Christmas delivery no longer guaranteed {s} Free delivery from €50 {s} 15% off your second set", True)
            + p('hors', f"Livraison offerte dès 50 € {s} Droits de douane déjà payés {s} 2e parure −15 %", f"Free delivery from €50 {s} Duties already paid {s} 15% off your second set", True)
            + '</div>')

def header(cur):
    items = ''
    for href, fr, en in NAV:
        if href == 'univers':
            sub = ''.join(f'<li><a href="{u["file"]}"{" aria-current=\"page\"" if cur == u["file"] else ""}><span data-en="{a(u["en"])}">{e(u["fr"])}</span><small>{u["count"]}</small></a></li>' for u in UNIVERS.values())
            items += (f'<li class="has-sub"><button class="navbtn" type="button" aria-expanded="false" aria-controls="subUnivers" data-en="{a(en)}">{e(fr)}</button>'
                      f'<ul class="subnav" id="subUnivers" hidden>{sub}</ul></li>')
        else:
            items += f'<li><a href="{href}"{" aria-current=\"page\"" if cur == href else ""} data-en="{a(en)}">{e(fr)}</a></li>'
    mitems = ''.join(f'<li><a href="{h}" data-en="{a(en)}">{e(fr)}</a></li>' for h, fr, en in NAV if h != 'univers')
    msub = ''.join(f'<li class="sub"><a href="{u["file"]}"><span data-en="{a(u["en"])}">{e(u["fr"])}</span><small class="muted">{u["count"]}</small></a></li>' for u in UNIVERS.values())
    return f'''<header class="hdr" id="hdr">
  <div class="wrap bar">
    <div class="left">
      <button class="icon-btn menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu" data-en-aria-label="Menu">{icon('menu')}</button>
      <nav class="mainnav" aria-label="Navigation principale" data-en-aria-label="Main navigation"><ul>{items}</ul></nav>
    </div>
    <a class="brand" href="index.html" aria-label="CHARMED PARIS, accueil" data-en-aria-label="CHARMED PARIS, home">{LOGO_H}{LOGO_P}</a>
    <div class="tools">
      <div class="lang lang-full" role="group" aria-label="Langue" data-en-aria-label="Language"><button type="button" data-lang="fr" lang="fr" aria-pressed="true" aria-label="Français">FR</button><span class="sl" aria-hidden="true">|</span><button type="button" data-lang="en" lang="en" aria-pressed="false" aria-label="English">EN</button></div>
      <button class="icon-btn lang-mini" type="button" lang="en" aria-label="Switch the site to English">EN</button>
      <button class="icon-btn" id="searchBtn" type="button" aria-expanded="false" aria-controls="searchPanel" aria-label="Rechercher une parure" data-en-aria-label="Search for a set">{icon('search')}</button>
      <a class="icon-btn" href="panier.html" data-open-cart aria-expanded="false" aria-controls="drawer">{icon('bag')}<span class="lbl" data-en="Cart">Panier</span><span class="count" data-count hidden>0</span></a>
    </div>
  </div>
  <div class="search-panel" id="searchPanel" hidden>
    <div class="wrap">
      <form role="search" action="parures.html" method="get" aria-label="Recherche" data-en-aria-label="Search">
        <label class="sr-only" for="searchInput" data-en="Search for a set">Rechercher une parure</label>
        <input id="searchInput" name="q" type="search" autocomplete="off" placeholder="Une parure, une pierre, une couleur…" data-en-placeholder="A set, a stone, a colour…">
        <button class="btn" type="submit" data-en="Search">Chercher</button>
      </form>
      <p class="sr-only" id="searchStatus" role="status"></p>
      <ul class="search-res" id="searchRes"></ul>
    </div>
  </div>
</header>
<nav class="mnav" id="mnav" hidden aria-label="Navigation mobile" data-en-aria-label="Mobile navigation">
  <ul>{mitems.replace('<li><a href="pieces-seules.html"', msub + '<li><a href="pieces-seules.html"', 1)}<li><a href="a-propos.html" data-en="Our story">Notre histoire</a></li><li><a href="faq.html" data-en="FAQ">FAQ</a></li></ul>
  <div class="mnav-foot"><span data-en="Language">Langue</span><div class="lang" role="group" aria-label="Langue" data-en-aria-label="Language"><button type="button" data-lang="fr" lang="fr" aria-pressed="true">Français</button><button type="button" data-lang="en" lang="en" aria-pressed="false">English</button></div>
  <span data-en="Free delivery from €50 · Duties paid · 14 days to change your mind">Livraison offerte dès 50 € · Droits payés · 14 jours pour changer d'avis</span></div>
</nav>'''

def footer():
    U = UNIVERS
    return f'''<footer class="site-foot">
  <div class="wrap cols">
    <div class="brandcol">
      <a href="index.html" aria-label="CHARMED PARIS, accueil" data-en-aria-label="CHARMED PARIS, home" style="display:inline-block">{LOGO_FOOT}</a>
      <p class="tagline" data-en="Open. Be charmed.">Ouvre. Laisse-toi charmer.</p>
      <p data-en="Matching jewellery sets, boxed and ready to give.">Des parures assorties, livrées prêtes à offrir.</p>
      <div class="lang" role="group" aria-label="Langue" data-en-aria-label="Language"><button type="button" data-lang="fr" lang="fr" aria-pressed="true">Français</button><span class="sl" aria-hidden="true">|</span><button type="button" data-lang="en" lang="en" aria-pressed="false">English</button></div>
    </div>
    <div><h2 data-en="Shop">Boutique</h2><ul>
      <li><a href="parures.html" data-en="All sets">Toutes les parures</a></li>
      <li><a href="{U['eclat']['file']}" data-en="Sparkle">Éclat</a></li>
      <li><a href="{U['j925']['file']}" data-en="925 Silver">Joaillerie 925</a></li>
      <li><a href="pieces-seules.html" data-en="Single pieces">Pièces seules</a></li>
      <li><a href="pieces-seules.html#homme" data-en="For him">Pour lui</a></li>
      <li><a href="cadeaux.html" data-en="Gift ideas">Idées cadeaux</a></li></ul></div>
    <div><h2 data-en="Help">Aide</h2><ul>
      <li><a href="livraison-retours.html" data-en="Shipping &amp; returns">Livraison et retours</a></li>
      <li><a href="matieres-entretien.html" data-en="Materials &amp; care">Matières et entretien</a></li>
      <li><a href="faq.html" data-en="FAQ">FAQ</a></li>
      <li><a href="a-propos.html#contact" data-en="Contact">Contact</a></li>
      <li><a class="retract" href="retractation.html" data-en="Withdraw from my order">Me rétracter</a></li></ul></div>
    <div><h2 data-en="Legal">Légal</h2><ul>
      <li><a href="cgv.html" data-en="Terms of sale">CGV</a></li>
      <li><a href="mentions-legales.html" data-en="Legal notice">Mentions légales</a></li>
      <li><a href="confidentialite.html" data-en="Privacy">Confidentialité</a></li>
      <li><a href="cookies.html" data-en="Cookies">Cookies</a></li>
      <li><button type="button" data-cookies data-en="Manage my cookies">Gérer mes cookies</button></li></ul></div>
    <div><h2 data-en="Follow">Suivre</h2><ul>
      <li><span class="soon">Instagram <small data-en="soon">bientôt</small></span></li>
      <li><span class="soon">TikTok <small data-en="soon">bientôt</small></span></li>
      <li><span class="soon">Pinterest <small data-en="soon">bientôt</small></span></li></ul>
      <p class="small" data-en="Accounts to open: @charmedparis to check.">Comptes à ouvrir : @charmedparis à vérifier.</p></div>
  </div>
  <div class="wrap legal">
    <span data-en="© 2026 CHARMED PARIS · Prices in euros incl. VAT · Duties paid · Card, Apple Pay, Google Pay, PayPal (gateway to confirm)">© 2026 CHARMED PARIS · Prix TTC en euros · Droits de douane payés · Carte, Apple Pay, Google Pay, PayPal (passerelle à confirmer)</span>
    <span data-en="Our gold-tone jewellery is gold-plated brass: not solid gold. Keep it dry.">Nos bijoux dorés sont en laiton doré : ce n'est pas de l'or massif. À garder au sec.</span>
    <span data-en="Reference prototype for the WooCommerce site: no real order or payment.">Prototype de référence du site WooCommerce : aucune commande ni aucun paiement réels.</span>
  </div>
</footer>'''

def drawer():
    return f'''<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" role="dialog" aria-modal="true" aria-labelledby="drawerTitle" aria-hidden="true" inert>
  <header><h2 id="drawerTitle">Ton écrin</h2><button class="icon-btn" type="button" id="drawerClose" aria-label="Fermer ton écrin" data-en-aria-label="Close your box">{icon('close')}</button></header>
  <div class="shipbar" id="drawerShip"><span class="txt"></span><div class="bar"><i></i></div></div>
  <div class="lines" id="drawerLines"></div>
  <div class="totals">
    <div class="sum" id="drawerSum"></div>
    <a class="btn block big" id="drawerGo" href="paiement.html" style="margin-top:12px" data-en="Checkout">Commander</a>
    <a class="linkbtn" href="panier.html" style="display:block;text-align:center" data-en="View my box">Voir mon écrin</a>
    <p class="note small muted" style="text-align:center" data-en="Secure payment · 14-day returns · Duties paid">Paiement sécurisé · Retours 14 j · Droits payés</p>
  </div>
</aside>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<dialog class="cp-dialog" id="cookieDlg" aria-labelledby="cookieTitle">
  <div class="in">
    <h2 id="cookieTitle" data-en="Your cookies">Tes cookies</h2>
    <p data-en="This prototype uses no tracker or advertising cookie. Only your cart and your language are kept in your browser (local storage, needed for the service). On the live site, a consent tool will list measurement and advertising tools here, each one off by default.">Ce prototype n'utilise aucun traceur ni cookie publicitaire. Seuls ton panier et ta langue sont gardés dans ton navigateur (stockage local, nécessaire au service). Sur le site réel, l'outil de consentement listera ici la mesure d'audience et la publicité, chacune désactivée par défaut.</p>
    <div id="cookieCustom" hidden>
      <label class="check"><input type="checkbox" checked disabled> <span data-en="Necessary (cart, language): always on">Nécessaires (panier, langue) : toujours actifs</span></label>
      <label class="check"><input type="checkbox"> <span data-en="Audience measurement (none in the prototype)">Mesure d'audience (aucune dans le prototype)</span></label>
      <label class="check"><input type="checkbox"> <span data-en="Advertising and social networks (none in the prototype)">Publicité et réseaux sociaux (aucun dans le prototype)</span></label>
    </div>
    <div class="btns">
      <button class="btn" type="button" data-consent="refuse" data-en="Refuse all">Tout refuser</button>
      <button class="btn" type="button" data-consent="accept" data-en="Accept all">Tout accepter</button>
      <button class="btn ghost" type="button" data-consent="custom" data-en="Customise">Personnaliser</button>
    </div>
    <p class="small muted" style="margin-top:12px"><a href="cookies.html" data-en="Our cookie policy">Notre politique cookies</a></p>
  </div>
</dialog>'''

HEAD_JS = ("(function(d){var h=d.documentElement;try{if(localStorage.getItem('cp-lang')==='en'){h.lang='en';h.classList.add('lang-en');}}catch(e){}"
           "var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;"
           "var ad=/[?&](utm_[a-z]+|gclid|fbclid|ttclid|epik)=/.test(location.search);"
           "if(!rm&&!ad){h.classList.add('cp-motion');}h.classList.add('js');})(document);")

def crumbs(items):
    """items = [(href|None, fr, en)] ; le dernier est la page courante."""
    lis = ''
    for i, (href, fr, en) in enumerate(items):
        if href and i < len(items) - 1:
            lis += f'<li><a href="{href}" data-en="{a(en)}">{e(fr)}</a></li>'
        else:
            lis += f'<li><span aria-current="page" data-en="{a(en)}">{e(fr)}</span></li>'
    return f'<div class="wrap"><nav class="crumbs" aria-label="Fil d\'Ariane" data-en-aria-label="Breadcrumb"><ol>{lis}</ol></nav></div>'

def ld_breadcrumb(items, lang):
    lst = []
    for i, (href, fr, en) in enumerate(items):
        it = {'@type': 'ListItem', 'position': i + 1, 'name': fr if lang == 'fr' else en}
        if href:
            it['item'] = f'{DOMAIN}/{href}'
        lst.append(it)
    return {'@type': 'BreadcrumbList', 'itemListElement': lst}

ORG = {'@type': 'Organization', '@id': f'{DOMAIN}/#organization', 'name': 'CHARMED PARIS', 'url': f'{DOMAIN}/', 'logo': f'{DOMAIN}/assets/img/apple-touch-icon-180.png',
       'slogan': 'Ouvre. Laisse-toi charmer.', 'email': 'bonjour@charmedparis.com',
       'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer service', 'email': 'bonjour@charmedparis.com', 'availableLanguage': ['French', 'English']}}

def jsonld(graph):
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1).replace('</', '<\\/')

def page(file, *, title, title_en, desc, desc_en, body, url, url_en, ld_fr, ld_en, cur=None, index=True, home=False, data_list=None, og_img='assets/img/pack/pack-noel-f-600.webp'):
    robots = 'index,follow' if index else 'noindex,follow'
    canon = DOMAIN + url
    scripts = '<script src="assets/js/catalogue.js" defer></script>\n<script src="assets/js/site.js" defer></script>'
    if home:
        scripts += '\n<script src="assets/js/home.js" defer></script>'
    dl = f' data-list="{a(data_list)}"' if data_list else ''
    doc = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title data-en="{a(title_en)}">{e(title)}</title>
<meta name="description" content="{a(desc)}" data-en-content="{a(desc_en)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{a(canon)}">
<link rel="alternate" hreflang="fr" href="{a(canon)}">
<link rel="alternate" hreflang="en" href="{a(DOMAIN + url_en)}">
<link rel="alternate" hreflang="x-default" href="{a(canon)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CHARMED PARIS">
<meta property="og:title" content="{a(title)}" data-en-content="{a(title_en)}">
<meta property="og:description" content="{a(desc)}" data-en-content="{a(desc_en)}">
<meta property="og:image" content="{a(og_img)}">
<meta property="og:locale" content="fr_FR">
<meta name="theme-color" content="#1A1015">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon-180.png">
<link rel="preload" href="assets/fonts/jost-latin-wght.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/bodoni-moda-latin-wght.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css">
<script>{HEAD_JS}</script>
<script type="application/ld+json" id="ld-fr">{jsonld(ld_fr)}</script>
<script type="application/x-ld-inactive" id="ld-en">{jsonld(ld_en)}</script>
{scripts}
</head>
<body class="{'home' if home else 'pg'}"{dl}>
<a class="skip" href="#main" data-en="Skip to content">Aller au contenu</a>
{annonce()}
{header(cur or file)}
<main id="main">
{body}
</main>
{footer()}
{drawer()}
</body>
</html>
'''
    (SITE / file).write_text(doc, encoding='utf-8')
    PAGES_WRITTEN.append(file)

PAGES_WRITTEN = []

def webpage_ld(name, desc, url, crumbs_items, lang, typ='WebPage', extra=None):
    g = [{'@type': typ, '@id': DOMAIN + url, 'url': DOMAIN + url, 'name': name, 'description': desc, 'inLanguage': 'fr-FR' if lang == 'fr' else 'en', 'isPartOf': {'@id': f'{DOMAIN}/#website'}},
         ld_breadcrumb(crumbs_items, lang)]
    if extra:
        g[0].update(extra)
    return g

# ------------------------------------------------------------------ blocs réutilisables
def reass():
    items = [('truck', 'Livraison 4 à 9 jours ouvrés', 'Offerte dès 50 €, droits payés', 'Delivered in 4–9 business days', 'Free from €50, duties paid'),
             ('globe', 'Expédiée hors UE', 'États-Unis ou Chine, rien à régler à la livraison', 'Ships from outside the EU', 'US or China, nothing to pay on arrival'),
             ('return', "14 jours pour changer d'avis", 'Retour à nos frais', '14 days to change your mind', 'Returns on us'),
             ('gift', 'Coffret inclus', 'Sur chaque commande, bordereau sans prix', 'Box included', 'With every order, no prices on the slip')]
    lis = ''.join(f'<li>{icon(i)}<div>{el("b", b1, b2)}{el("span", s1, s2)}</div></li>' for i, b1, s1, b2, s2 in items)
    return f'<section class="reass" aria-label="Nos engagements" data-en-aria-label="Our promises"><div class="wrap"><ul>{lis}</ul></div></section>'

def reviews_slot(scope_fr='cette parure', scope_en='this set'):
    return f'''<section class="band" aria-labelledby="rv-t"><div class="wrap"><div class="reviews-slot">
  {el('h2', 'Avis clientes vérifiées', 'Verified customer reviews', id='rv-t')}
  {el('span', '( à venir )', '( coming soon )', 'tag')}
  {el('p', f"Seules les clientes qui ont acheté {scope_fr} pourront laisser un avis : on le leur demande par e-mail après la livraison. Rien ne s'affiche avant les premiers vrais avis, et nous n'en publions aucun d'inventé.", f"Only customers who bought {scope_en} can leave a review: we ask them by email after delivery. Nothing shows until the first real reviews arrive, and we never publish made-up ones.")}
</div></div></section>'''

def grid(skus=None, u=None, promo=0, limit=0, exclude='', cls=''):
    at = ''
    if skus: at += f' data-skus="{",".join(skus)}"'
    if u: at += f' data-u="{u}"'
    if promo: at += f' data-promo="{promo}"'
    if limit: at += f' data-limit="{limit}"'
    if exclude: at += f' data-exclude="{exclude}"'
    # Rendu serveur de secours (sans JS) : liens vers les fiches
    lst = [BY[s] for s in skus] if skus else [p for p in PRODUCTS if (not u or p['u'] == u) and p['sku'] != exclude]
    if limit: lst = lst[:limit]
    noscript = ''.join(f'<li><a href="{p["url"]}">{e(p["name"]["fr"])}</a> · {p["price"]} €</li>' for p in lst)
    return f'<div class="grid {cls}" data-grid{at}><noscript><ul>{noscript}</ul></noscript></div>'

def newsletter():
    return f'''<section class="band velours news" id="news" aria-labelledby="news-t"><div class="wrap">
  {el('p', 'Le cercle Charmed', 'The Charmed circle', 'eyebrow')}
  {el('h2', '−10 % sur ta première commande', '10% off your first order', id='news-t')}
  <form class="news-form" data-news novalidate><span class="br l" aria-hidden="true"></span><div class="inner">
    <label class="sr-only" for="news-mail" data-en="Your email">Ton e-mail</label>
    <input id="news-mail" type="email" autocomplete="email" placeholder="ton e-mail" data-en-placeholder="your email" aria-describedby="news-fine">
    <button class="btn gold" type="submit" data-en="Sign me up">Je m'inscris</button></div><span class="br r" aria-hidden="true"></span></form>
  <p class="err" hidden role="alert"></p>
  <p class="ok" hidden role="status" data-en="Welcome to the circle. Your code is on its way (mock-up: CERCLE10).">Bienvenue dans le cercle. Ton code arrive par e-mail (maquette : CERCLE10).</p>
  {elh('p', 'Un e-mail quand une parure arrive ou qu\'une date compte. Désinscription en un clic. <a class="link" href="confidentialite.html">Confidentialité</a>', 'One email when a new set arrives or a date matters. Unsubscribe in one click. <a class="link" href="confidentialite.html">Privacy</a>', 'fine', id='news-fine')}
</div></section>'''

def noel_box(compact=False):
    return (f'<div class="noel" data-xmas="avant">{icon("star")}' + elh('span', "<b>Noël :</b> commande avant le vendredi 4 décembre pour une livraison avant Noël en Europe. L'emballage de Noël est offert jusqu'au 24 décembre.",
            '<b>Christmas:</b> order by Friday 4 December for delivery before Christmas in Europe. Christmas wrapping is free until 24 December.') + '</div>'
            + f'<div class="noel" data-xmas="apres" hidden>{icon("star")}' + elh('span', "<b>Noël :</b> emballage de Noël offert jusqu'au 24 décembre. Livraison avant Noël non garantie.",
            '<b>Christmas:</b> free Christmas wrapping until 24 December. Delivery before Christmas can no longer be guaranteed.') + '</div>')

# =====================================================================
# PAGES
# =====================================================================
def build_home():
    m = seo('Accueil', 'Home')
    cof = ['JSGRQR', 'JS1AQ5', 'JS3GGZ', 'JSG813', 'JS63WT', 'JSJB3S', 'JSX3G6', 'JSSFYS', 'JS63VP']
    lu = ['JSGRQR', 'JS63WT', 'JS1AQ5', 'JS3GGZ', 'JSG813', 'JSJB3S', 'JSX3G6', 'JSSFYS', 'JS4EXR']
    uni = ''
    for k in U_ORDER:
        u = UNIVERS[k]
        img = u['img']; ai = ''
        if k == 'sculpture':
            img = 'assets/img/cascade/05-portee.webp'
            ai = el('span', 'Image générée par IA', 'AI-generated image', 'ai')
        frm = min(p['price'] for p in PRODUCTS if p['u'] == k)
        uni += (f'<a class="uni" href="{u["file"]}"><img src="{img}" alt="" width="535" height="536" loading="lazy">{ai}'
                f'{el("span", u["line_fr"] + f" · dès {frm} €", u["line_en"] + f" · from €{frm}", "u-meta")}{el("h3", u["fr"], u["en"])}{el("p", u["hook_fr"], u["hook_en"])}</a>')
    packs = ''.join(f'<img src="assets/img/pack/pack-{k}-600.webp" srcset="assets/img/pack/pack-{k}-600.webp 600w, assets/img/pack/pack-{k}.webp {w}w" sizes="(min-width:900px) 560px, 100vw" width="{w}" height="{w}" data-pack="{k}" alt="{a(fr)}" data-en-alt="{a(en)}" loading="lazy">'
                    for k, w, fr, en in [('noel-f', 1000, 'Emballage de Noël CHARMED PARIS : boîte blanche, ruban vert, pochette en velours, carte de Noël', 'CHARMED PARIS Christmas wrapping: white box, green ribbon, velvet pouch, Christmas card'),
                                         ('f', 800, "Colis CHARMED PARIS ouvert : carton à notre logo, papier, boîte cadeau au ruban, pochette en velours", 'Open CHARMED PARIS parcel: logo mailer, paper, ribboned gift box, velvet pouch'),
                                         ('h', 800, 'Packaging homme CHARMED PARIS : papier noir, écrins noirs, pochette noire', 'CHARMED PARIS men\'s packaging: black paper, black cases, black pouch'),
                                         ('noel-h', 1000, 'Emballage de Noël homme CHARMED PARIS : papier rouge, pochette noire, écrin au ruban rouge', "CHARMED PARIS men's Christmas wrapping: red paper, black pouch, case with red ribbon")])
    molten, solar = BY['JSGRQR'], BY['JS1AQ5']
    body = f'''
<section class="intro" id="intro" data-three="assets/js/vendor/three-r128.min.js" aria-labelledby="h1">
  <div class="stage">
    <div class="glow" aria-hidden="true"></div>
    <canvas class="gl" aria-hidden="true"></canvas>
    <div class="ring" aria-hidden="true"></div>
    <div class="i-logo" aria-hidden="true"><span class="br l"></span><span class="mid">HARME</span><span class="br r"></span><span class="paris">PARIS</span></div>
    {el('p', 'Ouvre.', 'Open.', 'it it-open', aria_hidden='true')}
    {el('p', "Le bijou qu'on offre.", 'The jewellery you give.', 'it it-1', aria_hidden='true')}
    {el('p', "Et celui qu'on s'offre.", 'And the jewellery you keep.', 'it it-2', aria_hidden='true')}
    <div class="i-final">
      <span class="fw" aria-hidden="true">CHARMED</span><span class="fs" aria-hidden="true">PARIS</span>
      {el('h1', m['h1'], m['h1_en'], id='h1')}
      {el('p', 'Parures de bijoux assorties, prêtes à offrir. Dès 49 €, livraison offerte dès 50 €.', 'Matching jewellery sets, ready to give. From €49, free delivery from €50.', 'sub')}
    </div>
    <a class="i-skip" id="skipIntro" href="#coffrets" data-en="Skip intro">Passer l'intro</a>
    <div class="i-cta">
      <p class="i-hint" aria-hidden="true"><span class="desk" data-en="Scroll down to open the box">Descends pour ouvrir l'écrin</span><span class="touch" data-en="Swipe up to open the box">Glisse vers le haut pour ouvrir l'écrin</span><span class="chev"></span></p>
      <div class="row"><a class="btn gold" href="parures.html" data-en="See the sets">Voir les parures</a><a class="btn ghost" href="cadeaux.html" data-en="Gift ideas">Idées cadeaux</a></div>
    </div>
    <div class="prog" aria-hidden="true"><i></i></div>
  </div>
</section>

<section class="coffrets" id="coffrets" aria-labelledby="cof-h">
  <div class="wrap cof-head">
    {el('p', f'{len(cof)} parures · {len(cof)} coffrets CHARMED PARIS', f'{len(cof)} sets · {len(cof)} CHARMED PARIS boxes', 'eyebrow')}
    {el('h2', 'Choisis ton coffret', 'Choose your box', id='cof-h')}
    {el('p', 'Fais tourner les coffrets. Celui qui arrive devant toi s\'ouvre sur sa parure.', 'Turn the boxes. The one that comes to the front opens on its set.')}
  </div>
  <div class="cof-stage" id="cofStage" tabindex="0" role="group" aria-roledescription="carrousel" aria-label="Coffrets : flèches gauche et droite pour tourner" data-en-aria-label="Boxes: left and right arrow keys to turn" data-skus="{','.join(cof)}">
    <div id="cofRing"></div>
    <div class="cof-hand" id="cofHand" aria-hidden="true" data-en="← Turn →">← Fais tourner →</div>
  </div>
  <div class="wrap cof-info">
    <button class="cof-arrow" id="cofPrev" type="button" aria-label="Coffret précédent" data-en-aria-label="Previous box">←</button>
    <div class="cof-text"><span class="eyebrow" id="cofTag"></span><h3 id="cofName"></h3><p id="cofDesc"></p>
      <div class="cof-buy"><b id="cofPrice"></b><button class="btn gold" id="cofAdd" type="button" data-en="Add to my box">Ajouter à l'écrin</button></div></div>
    <button class="cof-arrow" id="cofNext" type="button" aria-label="Coffret suivant" data-en-aria-label="Next box">→</button>
  </div>
  <p class="sr-only" id="cofLive" aria-live="polite"></p>
  <div class="cof-dots" id="cofDots" role="group" aria-label="Choisir un coffret" data-en-aria-label="Choose a box"></div>
  {el('p', 'Mise en scène : une seule boîte à bijoux par commande. Une 2e parure voyage dans son sachet scellé, dans le même colis.', 'Staging: one jewellery box per order. A second set travels in its sealed bag, in the same parcel.', 'cof-note wrap')}
</section>

<div class="marquee" aria-hidden="true"><div class="track">{''.join(f'<span data-en="{en}">{fr}</span>' for fr, en in [('Ouvre', 'Open'), ('Offre', 'Give'), ('Garde', 'Keep'), ('Laisse-toi charmer', 'Be charmed'), ('CHARMED PARIS', 'CHARMED PARIS')] * 2)}</div></div>

<section class="lineup focus" id="pieces" aria-labelledby="lu-h">
  {el('h2', 'La file des parures', 'The line-up', 'sr-only', id='lu-h')}
  <div class="lu-stage" id="luStage" tabindex="0" aria-label="Parures : flèches gauche et droite pour passer à la suivante, Entrée pour ouvrir la fiche" data-en-aria-label="Sets: left and right arrow keys to move, Enter to open the page" data-skus="{','.join(lu)}">
    <div class="lu-top">
      <div class="lu-title" aria-hidden="true"><b>CHARMED PARIS</b><br><span data-en="The line-up · {len(lu)} boxes">La file des parures · {len(lu)} écrins</span></div>
      <div class="lu-views" role="group" aria-label="Affichage" data-en-aria-label="View">
        <button type="button" data-v="focus" aria-pressed="true" data-en="One">Une</button><button type="button" data-v="queue" aria-pressed="false" data-en="The line">La file</button><button type="button" data-v="grid" aria-pressed="false" data-en="All">Toutes</button>
      </div>
    </div>
    <div id="luItems"></div>
    <div class="lu-name"><small id="luMeta"></small><h3 id="luName"></h3></div>
    <div class="lu-hint" id="luHint" aria-hidden="true"></div>
    <aside class="ticket" id="luTag" aria-label="Étiquette de la parure" data-en-aria-label="Set tag">
      <div class="tt-head"><span class="tt-brand"><span class="wm"><span class="br l"></span><span class="mid">HARME</span><span class="br r"></span></span><span>Paris</span></span><span id="ttNo"></span></div>
      <div class="tt-code"><b id="ttCode"></b><span id="ttName"></span></div>
      {el('h3', 'Dans ton colis', 'In your parcel')}
      <ul class="tt-rows" id="ttRows"></ul>
      <div class="tt-total"><span data-en="Set total">Total parure</span><b id="ttPrice"></b></div>
      <button class="tt-add" type="button" id="ttAdd"><span>Ajouter à l'écrin</span><span aria-hidden="true">→</span></button>
      <div class="tt-bar" aria-hidden="true"></div>
      <div class="tt-sku" id="ttSku"></div>
      <div class="tt-foot"><span data-xmas="noel" data-en="Christmas wrapping free">Emballage de Noël offert</span><span>Paris</span></div>
    </aside>
    <p class="sr-only" id="luLive" aria-live="polite"></p>
  </div>
  <div class="lu-foot"><a class="btn ghost" href="parures.html" data-en="See all {len(PRODUCTS)} sets">Voir les {len(PRODUCTS)} parures</a></div>
</section>

<section class="band" id="univers" aria-labelledby="uni-h"><div class="wrap">
  <div class="head-row"><div>{el('p', 'Les univers', 'Collections', 'eyebrow')}{el('h2', 'Choisis ton éclat', 'Choose your shine', 'h2', id='uni-h')}</div><a class="btn ghost" href="parures.html" data-en="See all">Tout voir</a></div>
  <div class="uni-rail">{uni}</div>
</div></section>

<section class="band velours duo-band" id="parure" aria-labelledby="duo-h"><div class="wrap">
  <div style="display:flex;flex-direction:column;gap:16px;align-items:flex-start">
    {el('p', 'La parure Charmed', 'The Charmed set', 'eyebrow')}
    {el('h2', 'Les pièces assorties, dans un seul écrin.', 'Pieces that match, in one box.', id='duo-h')}
    {el('p', 'Chaque parure est pensée comme un ensemble : rien à assortir, tout arrive prêt à offrir. Et la 2e parure est à −15 %, sur la moins chère.', 'Every set is designed as a whole: nothing to match, everything arrives ready to give. And your second set is 15% off, on the cheaper one.', 'lead')}
    {el('p', 'Exemple : Molten Art 49 € + Solar Sphere 69 € − 7,35 € = 110,65 €, livraison offerte.', 'Example: Molten Art €49 + Solar Sphere €69 − €7.35 = €110.65, free delivery.', 'duo-math')}
    <a class="btn ghost" href="parures.html" data-en="See the sets">Voir les parures</a>
  </div>
  <div class="duo" aria-hidden="true"><span class="br l"></span><span class="pieces"><img src="{molten['img']}" alt="" width="400" height="400" loading="lazy"><span class="plus">+</span><img src="{solar['img']}" alt="" width="400" height="400" loading="lazy"></span><span class="br r"></span></div>
</div></section>

<section class="band" id="cadeaux" aria-labelledby="gift-h"><div class="wrap">
  <div class="head-row"><div>{el('p', 'Idées cadeaux', 'Gift ideas', 'eyebrow')}{el('h2', 'Offrir, selon ton budget', 'Gifts by budget', 'h2', id='gift-h')}</div><a class="btn ghost" href="cadeaux.html" data-en="All gift ideas">Toutes les idées</a></div>
  <div class="budgets">
    <a class="budget" href="cadeaux.html#moins-50">{el('span', 'Moins de', 'Under')}<b data-en="€50">50 €</b>{el('span', 'Sculpture et Mixte · 5 parures à 49 €', 'Sculpture and Unisex · 5 sets at €49')}</a>
    <a class="budget" href="cadeaux.html#moins-100">{el('span', 'Moins de', 'Under')}<b data-en="€100">100 €</b>{el('span', 'Éclat, Couleur précieuse, Sculpture', 'Sparkle, Precious Colour, Sculpture')}</a>
    <a class="budget" href="cadeaux.html#plus-100">{el('span', 'Plus de', 'Over')}<b data-en="€100">100 €</b>{el('span', 'Argent 925 et moissanite synthétique', 'Sterling silver and lab-grown moissanite')}</a>
  </div>
  <div class="occasions">{''.join(f'<a class="chip" href="{h}" data-en="{a(en)}">{e(fr)}</a>' for h, fr, en in [('cadeaux.html#noel', 'Noël', 'Christmas'), ('cadeaux.html#anniversaire', 'Anniversaire', 'Birthday'), ('cadeaux.html#fete-des-meres', 'Fête des mères', "Mother's Day"), ('parures.html', 'Pour soi', 'For yourself'), ('pieces-seules.html#homme', 'Pour lui', 'For him')])}</div>
</div></section>

<section class="band offrir" id="offrir" aria-labelledby="off-h" style="padding-top:0"><div class="wrap">
  <div>
    <figure class="packshot" id="packshot">{packs}<span class="pk-tag" id="pkTag"></span></figure>
    <div class="pack-switch" role="group" aria-label="Choisir le packaging" data-en-aria-label="Choose the packaging">
      {''.join(f'<button class="chip" type="button" data-pack="{k}" aria-pressed="false" data-en="{a(en)}">{e(fr)}</button>' for k, fr, en in [('f', 'Femme', 'Her'), ('h', 'Homme', 'Him'), ('noel-f', 'Noël Femme', 'Christmas Her'), ('noel-h', 'Noël Homme', 'Christmas Him')])}
    </div>
    {el('p', 'Photos réelles de packagings, avec notre logo. Couleur de la boîte et emplacement de la dorure à confirmer sur échantillon.', 'Real photos of our packaging, with our logo. Box colour and foil placement to be confirmed on a sample.', 'pack-note')}
  </div>
  <div>
    {el('p', "L'écrin Charmed", 'The Charmed box', 'eyebrow')}
    {el('h2', 'Chaque commande arrive prête à offrir', 'Every order arrives ready to give', 'h2', id='off-h')}
    <ol>
      {el('li', 'Une boîte-tiroir beige métallisé à notre logo, nouée d\'un ruban, dans un carton d\'envoi à notre logo. Une boîte par commande : une 2e parure voyage dans son sachet scellé, dans le même colis.', 'A metallic beige drawer box with our logo, tied with ribbon, inside a shipping box with our logo. One box per order: a second set travels in its sealed bag, in the same parcel.')}
      {el('li', 'Une pochette en velours et une chamoisine pour l\'entretien.', 'A velvet pouch and a polishing cloth.')}
      {el('li', 'Une carte avec les conseils d\'entretien. Le bordereau n\'affiche aucun prix : tu peux faire livrer directement chez la personne.', 'A care card. The packing slip shows no prices, so you can send it straight to them.')}
      {el('li', 'Jusqu\'au 24 décembre : emballage de Noël offert, avec papier cadeau, ruban et carte de Noël.', 'Until 24 December: free Christmas wrapping, with festive paper, ribbon and a Christmas card.')}
      {el('li', 'Pas de message cadeau ni de gravure : le colis arrive prêt à offrir, tel quel.', 'No gift message and no engraving: the parcel arrives ready to give, as it is.')}
    </ol>
    {el('p', 'Les parures en argent 925 arrivent dans un écrin en velours bleu, glissé dans notre carton d\'envoi.', 'Our sterling silver sets arrive in a blue velvet jewellery box, inside our shipping box.', 'muted small')}
  </div>
</div></section>

{reass()}
{reviews_slot('une parure', 'a set')}
{newsletter()}
'''
    ld = lambda lang: [ORG, {'@type': 'WebSite', '@id': f'{DOMAIN}/#website', 'url': f'{DOMAIN}/', 'name': 'CHARMED PARIS', 'inLanguage': ['fr-FR', 'en'], 'publisher': {'@id': f'{DOMAIN}/#organization'},
                         'potentialAction': {'@type': 'SearchAction', 'target': f'{DOMAIN}/?s={{search_term_string}}&post_type=product', 'query-input': 'required name=search_term_string'}},
                       {'@type': 'WebPage', '@id': f'{DOMAIN}/', 'name': m['title'] if lang == 'fr' else m['title_en'], 'description': m['desc'] if lang == 'fr' else m['desc_en'], 'isPartOf': {'@id': f'{DOMAIN}/#website'}}]
    page('index.html', title=m['title'], title_en=m['title_en'], desc=m['desc'], desc_en=m['desc_en'], body=body, url='/', url_en='/en/', ld_fr=ld('fr'), ld_en=ld('en'), home=True)

def itemlist(prods, lang):
    return {'@type': 'ItemList', 'numberOfItems': len(prods), 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': DOMAIN + p['meta']['url' if lang == 'fr' else 'url_en'], 'name': p['name'][lang]} for i, p in enumerate(prods)]}

def build_shop():
    m = seo('Boutique', 'Shop')
    cr = [('index.html', 'Accueil', 'Home'), (None, 'Toutes les parures', 'All sets')]
    chips = lambda f, opts: ''.join(f'<button class="chip" type="button" data-f="{f}" data-v="{v}" aria-pressed="false"><span data-en="{a(en)}">{e(fr)}</span> <small></small></button>' for v, fr, en in opts)
    body = f'''{crumbs(cr)}
<div class="wrap">
  <header class="page-head">
    {el('h1', m['h1'], m['h1_en'])}
    {el('p', f"{len(PRODUCTS)} parures, collier et boucles assortis (parfois une bague ou un bracelet), livrées dans leur boîte à bijoux. Dorées, colorées ou en argent 925.", f"{len(PRODUCTS)} sets, necklace and matching earrings (sometimes a ring or bracelet), delivered in their jewellery box. Gold-plated, colourful or 925 silver.", 'lead')}
    {el('p', 'Livraison offerte dès 50 € · Droits payés · Retours 14 jours', 'Free delivery from €50 · Duties paid · 14-day returns', 'facts-line')}
  </header>
  <p id="shopQ" hidden class="small"><span data-en="Search results for">Résultats pour</span> <b></b> · <button type="button" class="linkbtn" data-clear-all data-en="Clear">Effacer</button></p>
  <div class="filters" role="group" aria-label="Filtrer les parures" data-en-aria-label="Filter the sets">
    <div class="chip-group">{el('span', 'Univers', 'Collection')}<div class="chip-row">{chips('u', [(k, UNIVERS[k]['fr'], UNIVERS[k]['en']) for k in U_ORDER])}</div></div>
    <div class="chip-group">{el('span', 'Budget', 'Budget')}<div class="chip-row">{chips('b', [('b50', 'Moins de 50 €', 'Under €50'), ('b100', '50 à 100 €', '€50 to €100'), ('b100p', 'Plus de 100 €', 'Over €100')])}</div></div>
    <div class="chip-group">{el('span', 'Métal et pièces', 'Metal and pieces')}<div class="chip-row">{chips('m', [('dore', 'Doré', 'Gold-plated'), ('argente', 'Argenté ou rosé', 'Silver or rose tone'), ('a925', 'Argent 925', '925 silver')])}{chips('r', [('1', 'Avec bague', 'With a ring')])}</div></div>
  </div>
  <div class="toolbar"><p id="shopCount" role="status" style="margin:0"></p>
    <label><span data-en="Sort">Trier</span> <select id="shopSort"><option value="choix" data-en="Our picks">Nos choix</option><option value="asc" data-en="Price, low to high">Prix croissant</option><option value="desc" data-en="Price, high to low">Prix décroissant</option></select></label></div>
  <div class="grid g4" data-grid data-filterable></div>
  <div class="more-row" id="shopMore"><span id="shopShown"></span><button class="btn ghost" type="button" id="shopMoreBtn" data-en="Show more sets">Voir plus de parures</button></div>
  <p class="small muted" style="margin-top:28px;text-align:center">{elh('span', 'Envie d\'une seule pièce ? <a class="link" href="pieces-seules.html">Découvre les pièces seules</a>.', 'Fancy a single piece? <a class="link" href="pieces-seules.html">See the single pieces</a>.')}</p>
</div>
<div class="band" style="padding-block:40px 0"></div>
{reass()}'''
    ld = lambda l: webpage_ld(m['title'] if l == 'fr' else m['title_en'], m['desc'] if l == 'fr' else m['desc_en'], m['url'] if l == 'fr' else m['url_en'], cr, l, 'CollectionPage', {'mainEntity': itemlist(PRODUCTS, l)})
    page('parures.html', title=m['title'], title_en=m['title_en'], desc=m['desc'], desc_en=m['desc_en'], body=body, url=m['url'], url_en=m['url_en'], ld_fr=ld('fr'), ld_en=ld('en'), data_list='parures.html')

def split_h1(h):
    parts = re.split(r'\s+—\s+', h, maxsplit=1)
    return parts if len(parts) == 2 else [h, '']

def build_univers():
    for k in U_ORDER:
        u = UNIVERS[k]; m = u['meta']
        cr = [('index.html', 'Accueil', 'Home'), ('parures.html', 'Parures', 'Sets'), (None, u['fr'], u['en'])]
        n1, s1 = split_h1(m['h1']); n2, s2 = split_h1(m['h1_en'])
        h1 = f'<h1><span class="h1-name" data-en="{a(n2)}">{e(n1)}</span><span class="h1-sub" data-en="{a(s2)}">{e(s1)}</span></h1>'
        fig = f'<figure><img src="{u["img"]}" alt="" width="532" height="534"></figure>'
        if k == 'sculpture':
            fig = (f'<figure><img src="assets/img/cascade/05-portee.webp" width="535" height="536" alt="Parure Liquid Gold Cascade portée : collier en lames dorées et boucles en franges" data-en-alt="Liquid Gold Cascade set worn: gold blade necklace and fringe earrings">'
                   f'<figcaption class="ai-cap">{el("span", "Parure Liquid Gold Cascade, portée · image générée par IA", "Liquid Gold Cascade set, worn · AI-generated image")}</figcaption></figure>')
        others = ''.join(f'<a class="chip" href="{UNIVERS[o]["file"]}" data-en="{a(UNIVERS[o]["en"])}">{e(UNIVERS[o]["fr"])}</a>' for o in U_ORDER if o != k)
        prods = [p for p in PRODUCTS if p['u'] == k]
        body = f'''{crumbs(cr)}
<div class="wrap">
  <header class="page-head uni-hero">
    <div>{el('p', u['line_fr'], u['line_en'], 'eyebrow')}{h1}
      {bi(f'<p class="lead">{e(u["intro_fr"])}</p>', f'<p class="lead">{e(u["intro_en"])}</p>')}
      {el('p', u['facts_fr'], u['facts_en'], 'facts-line')}
    </div>
    {fig}
  </header>
  <nav class="occasions" aria-label="Autres univers" data-en-aria-label="Other collections" style="margin:0 0 26px">{others}<a class="chip" href="parures.html" data-en="All sets">Toutes les parures</a></nav>
  {grid(u=k, promo=6 if len(prods) > 6 else 0, cls='g4')}
  <section class="seo-text" aria-labelledby="seo-t">
    {el('h2', f"L'univers {u['fr']}", f"The {u['en']} collection", id='seo-t')}
    {bi(f'<p>{e(u["seo_fr"])}</p>', f'<p>{e(u["seo_en"])}</p>')}
  </section>
</div>
<div class="band" style="padding-block:32px 0"></div>
{reass()}'''
        ld = lambda l: webpage_ld(m['title'] if l == 'fr' else m['title_en'], m['desc'] if l == 'fr' else m['desc_en'], m['url'] if l == 'fr' else m['url_en'], cr, l, 'CollectionPage', {'mainEntity': itemlist(prods, l)})
        page(u['file'], title=m['title'], title_en=m['title_en'], desc=m['desc'], desc_en=m['desc_en'], body=body, url=m['url'], url_en=m['url_en'], ld_fr=ld('fr'), ld_en=ld('en'), cur=u['file'], data_list=u['file'])

def gallery(p):
    sl = []  # (classe, html interne, légende fr, légende en, vignette, classe vignette)
    nm_fr, nm_en = p['name']['fr'], p['name']['en']
    if p['sku'] == 'JS63WT':
        c = 'assets/img/cascade/'
        sl += [('photo', f'<img src="{c}01-parure-or.webp" width="532" height="534" alt="{a(p["alt"]["fr"])}" data-en-alt="{a(p["alt"]["en"])}">', 'La parure, dorée', 'The set, gold-plated', c + '01-parure-or.webp', ''),
               ('photo', f'<img src="{c}02-parure-or-pose.webp" width="532" height="530" loading="lazy" alt="Collier à chaîne réglable et boucles en franges dorées, posés à plat" data-en-alt="Adjustable chain necklace and gold fringe earrings, laid flat">', 'Collier réglable', 'Adjustable necklace', c + '02-parure-or-pose.webp', ''),
               ('photo', f'<img src="{c}03-boucles-or.webp" width="534" height="533" loading="lazy" alt="Gros plan des boucles d\'oreilles en franges dorées" data-en-alt="Close-up of the gold fringe earrings">', 'Les boucles', 'The earrings', c + '03-boucles-or.webp', ''),
               ('photo', f'<img src="{c}04-or-et-argent.webp" width="532" height="531" loading="lazy" alt="La parure en finition dorée et en finition argentée, côte à côte" data-en-alt="The set in gold-plated and silver-tone finishes, side by side">', 'Dorée ou argentée', 'Gold or silver tone', c + '04-or-et-argent.webp', ''),
               ('photo', f'<img src="{c}05-portee.webp" width="535" height="536" loading="lazy" alt="La parure portée : collier en lames dorées et boucles en franges" data-en-alt="The set worn: gold blade necklace and fringe earrings">', 'Portée', 'Worn', c + '05-portee.webp', 'ai')]
    else:
        sl.append(('photo', f'<img src="{p["img"]}" width="400" height="400" alt="{a(p["alt"]["fr"])}" data-en-alt="{a(p["alt"]["en"])}">', 'La parure', 'The set', p['img'], ''))
    if p['cut']:
        sl.append(('velours', f'<img src="{p["cut"]}" width="700" height="700" loading="lazy" alt="{a(nm_fr)} détourée sur fond velours" data-en-alt="{a(nm_en)} cut out on velvet">', 'Sur velours', 'On velvet', p['cut'], 'v'))
        if p['u'] != 'j925':
            sl.append(('coffret', f'<img class="box" src="assets/img/box-open.webp" width="720" height="720" loading="lazy" alt=""><img class="jw" src="{p["cut"]}" width="700" height="700" loading="lazy" alt="{a(nm_fr)} posée dans sa boîte à bijoux ouverte" data-en-alt="{a(nm_en)} in its open jewellery box">', 'Dans sa boîte (montage maquette)', 'In its box (mock-up composite)', 'assets/img/box-open.webp', 'c'))
    if p['u'] != 'j925':
        sl.append(('photo-pack', '<img src="assets/img/pack/pack-f-600.webp" width="600" height="600" loading="lazy" alt="Colis CHARMED PARIS ouvert : carton à notre logo, boîte cadeau au ruban, pochette en velours" data-en-alt="Open CHARMED PARIS parcel: logo mailer, ribboned gift box, velvet pouch">', 'Ton colis', 'Your parcel', 'assets/img/pack/pack-f-600.webp', ''))
    slides = ''.join(f'<figure class="g-slide {c}">{inner}<figcaption><span data-en="{a(en)}">{e(fr)}</span>{el("span", "Image générée par IA", "AI-generated image", "ai") if ai == "ai" else ""}</figcaption></figure>' for c, inner, fr, en, th, ai in sl)
    thumbs = ''.join(f'<button type="button" class="{"v" if tc == "v" else ""}" aria-label="Photo {i + 1} : {a(fr)}" data-en-aria-label="Photo {i + 1}: {a(en)}"><img src="{th}" alt="" width="72" height="72" loading="lazy"></button>' for i, (c, inner, fr, en, th, tc) in enumerate(sl))
    return f'''<section class="gallery" aria-label="Photos de la parure" data-en-aria-label="Photos of the set">
  <div class="g-main">
    <div class="g-track" id="gTrack" tabindex="0" aria-label="Galerie : glisse ou utilise les flèches" data-en-aria-label="Gallery: swipe or use the arrow keys">{slides}</div>
    <button class="g-nav prev" type="button" id="gPrev" aria-label="Photo précédente" data-en-aria-label="Previous photo">←</button>
    <button class="g-nav next" type="button" id="gNext" aria-label="Photo suivante" data-en-aria-label="Next photo">→</button>
    <span class="g-count" id="gCount" aria-hidden="true">1 / {len(sl)}</span>
  </div>
  <div class="g-thumbs" id="gThumbs">{thumbs}</div>
  <div class="g-dots" id="gDots"></div>
  {el('p', 'Photos du fournisseur (400 px) en attendant les originaux haute définition.', 'Supplier photos (400 px) until we get the high-definition originals.', 'ai-cap') if p['sku'] != 'JS63WT' else ''}
</section>'''

def build_product(p):
    m = p['meta']; U = UNIVERS[p['u']]
    cr = [('index.html', 'Accueil', 'Home'), ('parures.html', 'Parures', 'Sets'), (U['file'], U['fr'], U['en']), (None, p['name']['fr'], p['name']['en'])]
    _, s1 = split_h1(m['h1']); _, s2 = split_h1(m['h1_en'])
    n = len(p['pcs']['fr'])
    is925 = p['u'] == 'j925'
    box_fr = 'Écrin en velours bleu, certificat GRA dès 0,1 ct' if is925 else 'Boîte-tiroir à notre logo, nouée d\'un ruban'
    box_en = 'Blue velvet case, GRA certificate from 0.1 ct' if is925 else 'Drawer box with our logo, tied with ribbon'
    rows = ''.join(f'<li class="tt-row"><span data-en="{a(en)}">{e(fr)}</span><span data-en="included">inclus</span></li>' for fr, en in zip(p['pcs']['fr'], p['pcs']['en']))
    rows += f'<li class="tt-row"><span data-en="{a(box_en)}">{e(box_fr)}</span><span data-en="1 per order">1 / commande</span></li>'
    rows += '<li class="tt-row"><span data-en="Velvet pouch, polishing cloth, care card">Pochette en velours, chamoisine, carte d\'entretien</span><span data-en="included">inclus</span></li>'
    rows += '<li class="tt-row"><span data-en="Packing slip without prices">Bordereau sans aucun prix</span><span data-en="ready to give">prêt à offrir</span></li>'
    rows += '<li class="tt-row" data-xmas="noel"><span data-en="Christmas wrapping">Emballage de Noël</span><span data-en="free to 24/12">offert → 24/12</span></li>'
    variants = ''
    if p.get('variants'):
        opts = ''.join(f'<label class="opt"><input type="radio" name="finition" value="{v["id"]}"{" checked" if i == 0 else ""}><span><i class="{"arg" if v["id"] == "argent" else ""}" aria-hidden="true"></i><span data-en="{a(v["en"])}">{e(v["fr"])}</span></span></label>' for i, v in enumerate(p['variants']))
        variants = f'<fieldset><legend style="font-family:var(--body);font-size:15px;font-weight:500"><span data-en="Finish">Finition</span> : <b id="finLabel" data-en="Gold-plated">Dorée</b></legend><div class="opts">{opts}</div></fieldset>'
    mat_extra = ''
    if is925:
        mat_extra = el('p', 'Argent 925 estampillé sur chaque pièce. Moissanite synthétique, créée en laboratoire ; certificat GRA pour les pierres de 0,1 carat et plus (poids en équivalent diamant). L\'argent se ternit naturellement : la chamoisine lui rend son éclat.', 'Every piece is stamped 925. Lab-grown moissanite; GRA certificate for stones of 0.1 ct and above (weight in diamond equivalent). Silver darkens naturally: the polishing cloth brings the shine back.')
    else:
        mat_extra = el('p', 'Laiton doré par électrolyse, revêtement anti-ternissement. Ce n\'est pas de l\'or massif. À garder au sec : retire ta parure avant la douche, la baignade et le sport.', 'Brass plated in real gold by electroplating, with an anti-tarnish coating. It isn\'t solid gold. Keep it dry: take it off before showering, swimming and sport.')
    gpsr_fr = f'Opérateur économique responsable dans l\'UE : CHARMED PARIS, <mark class="todo">[À COMPLÉTER : raison sociale et adresse]</mark>, bonjour@charmedparis.com. Référence du produit : {p["sku"]}. Bijou pour adulte ; contient de petites pièces : à tenir hors de portée des jeunes enfants. À retirer avant le sport et le sommeil.'
    gpsr_en = f'EU responsible economic operator: CHARMED PARIS, <mark class="todo">[TO COMPLETE: company name and address]</mark>, bonjour@charmedparis.com. Product reference: {p["sku"]}. Adult jewellery; contains small parts: keep away from young children. Remove before sport and sleep.'
    acc = [('Description', 'Description', bi(todo(p['desc_fr']), todo(p['desc_en'])), True),
           ('Matières et entretien', 'Materials & care', f'<dl><dt data-en="Pieces">Pièces</dt><dd data-en="{a(", ".join(p["pcs"]["en"]))}">{e(", ".join(p["pcs"]["fr"]))}</dd><dt data-en="Materials">Matières</dt><dd data-en="{a(p["mat"]["en"])}">{e(p["mat"]["fr"])}</dd><dt data-en="Reference">Référence</dt><dd>{p["sku"]}</dd></dl>{mat_extra}'
            + f'<aside class="mock-note"><b>Note interne (maquette)</b>{e(p["todo"])}</aside>', False),
           ('Livraison et retours', 'Shipping & returns', '<ul>' + ''.join(el('li', fr, en) for fr, en in [
               ('Préparée en 1 à 2 jours ouvrés, livrée en France en 4 à 9 jours ouvrés (9 colis sur 10), avec suivi DHL.', 'Prepared in 1–2 business days, delivered to France in 4–9 business days (9 parcels in 10), with DHL tracking.'),
               ('Expédiée depuis les entrepôts de notre partenaire hors Union européenne (États-Unis ou Chine). Droits de douane déjà payés : rien à régler à la livraison.', 'Ships from our partner\'s warehouses outside the EU (United States or China). Duties already paid: nothing to pay on arrival.'),
               ('Un seul mode de livraison, sans option express ni date garantie.', 'One delivery method, no express option, no guaranteed date.'),
               ('Offerte dès 50 €, sinon 4,90 €. Un colis et une boîte à bijoux par commande : les parures suivantes voyagent en sachets scellés.', 'Free from €50, otherwise €4.90. One parcel and one jewellery box per order: further sets travel in sealed bags.'),
               ("14 jours après réception pour changer d'avis, retour à nos frais. Garantie légale de conformité de 2 ans.", '14 days from delivery to change your mind, returns on us. 2-year legal guarantee of conformity.')]) + '</ul>'
            + elh('p', '<a class="link" href="livraison-retours.html">Tout sur la livraison et les retours</a> · <a class="link" href="retractation.html">Me rétracter</a>', '<a class="link" href="livraison-retours.html">All about shipping and returns</a> · <a class="link" href="retractation.html">Withdraw from my order</a>'), False),
           ('Sécurité produit', 'Product safety', elh('p', gpsr_fr, gpsr_en), False),
           ('Questions fréquentes', 'Questions', ''.join(f'<p><b data-en="{a(q2)}">{e(q1)}</b><br><span data-en="{a(r2)}">{e(r1)}</span></p>' for q1, r1, q2, r2 in [
               ('Je peux la porter sous la douche ?', 'Non. Comme tous nos bijoux, garde-la au sec : retire-la avant la douche, la baignade et le sport.', 'Can I wear it in the shower?', 'No. Like all our jewellery, keep it dry: take it off before showering, swimming and sport.'),
               ('Elle arrive prête à offrir ?', 'Oui : boîte à bijoux avec ruban, pochette en velours, chamoisine, carte d\'entretien et bordereau sans prix. Une boîte par commande.', 'Does it arrive ready to give?', 'Yes: ribboned jewellery box, velvet pouch, polishing cloth, care card and a packing slip with no prices. One box per order.'),
               ('Peut-on la graver, ou joindre un message ?', 'Non : nos parures ne se gravent pas et ne se personnalisent pas, et nous ne pouvons pas joindre de message cadeau.', 'Can it be engraved, or come with a message?', 'No: our sets can\'t be engraved or personalised, and we can\'t add a gift message.')]), False)]
    acc_html = ''
    for i, (t1, t2, content, open_) in enumerate(acc):
        acc_html += (f'<div class="acc-item"><h3><button class="acc-btn" type="button" aria-expanded="{"true" if open_ else "false"}" aria-controls="ac{i}" id="ac{i}b"><span data-en="{a(t2)}">{e(t1)}</span><i aria-hidden="true"></i></button></h3>'
                     f'<div class="acc-panel" id="ac{i}" role="region" aria-labelledby="ac{i}b"><div><div class="acc-body">{content}</div></div></div></div>')
    eyebrow_fr = f'{U["fr"]} · Parure {n} pièces'; eyebrow_en = f'{U["en"]} · {n}-piece set'
    body = f'''{crumbs(cr)}
<div class="wrap pdp" data-pdp="{p['sku']}">
  {gallery(p)}
  <section class="buy" aria-labelledby="pname">
    {el('p', eyebrow_fr, eyebrow_en, 'eyebrow')}
    <h1 id="pname"><span class="h1-name" data-en="{a(p['name']['en'])}">{e(p['name']['fr'])}</span><span class="h1-sub" data-en="{a(s2)}">{e(s1)}</span></h1>
    {bi(p['short_fr'].replace('<p>', '<p class="lead">', 1), p['short_en'].replace('<p>', '<p class="lead">', 1))}
    <div class="price-row"><span class="pr" data-en="€{p['price']}.00">{p['price']},00 €</span><small data-en="incl. VAT">TTC</small></div>
    {el('p', 'Coffret inclus · Livraison offerte dès 50 € · Droits de douane payés', 'Box included · Free delivery from €50 · Duties paid', 'under-price')}
    <ul class="facts"><li>{icon('clock')}<span id="eta"></span></li>
      <li>{icon('globe')}<span data-en="Ships from our partner warehouses outside the EU (United States or China), by DHL. No express option.">Expédiée par DHL depuis les entrepôts de notre partenaire hors UE (États-Unis ou Chine). Pas d'option express.</span></li></ul>
    {noel_box()}
    {variants}
    <div class="atc-row" id="atcRow">
      <div class="qty" role="group" aria-label="Quantité" data-en-aria-label="Quantity"><button type="button" id="qMinus" aria-label="Une de moins" data-en-aria-label="One less">−</button><output id="qVal" aria-live="polite">1</output><button type="button" id="qPlus" aria-label="Une de plus" data-en-aria-label="One more">+</button></div>
      <button class="btn big" type="button" id="atc"><span data-label data-en="Add to my box">Ajouter à l'écrin</span><span aria-hidden="true">·</span><span id="atcPrice">{p['price']},00 €</span></button>
    </div>
    {el('p', 'Arrive prête à offrir : boîte à bijoux à ruban, bordereau sans prix. Pas de gravure ni de message cadeau.', 'Arrives ready to give: ribboned jewellery box, packing slip without prices. No engraving or gift message.', 'ready')}
    <div class="shipbar" id="pShip"><span class="txt"></span><div class="bar"><i></i></div></div>
    <aside class="ticket" aria-labelledby="tt-title">
      <div class="tt-head"><span class="tt-brand"><span class="wm"><span class="br l"></span><span class="mid">HARME</span><span class="br r"></span></span><span>Paris</span></span><span data-en="Box no. {PRODUCTS.index(p) + 1:02d}">Écrin n°{PRODUCTS.index(p) + 1:02d}</span></div>
      <div class="tt-code"><b>{p['code']}</b><span>{e(p['model'])}</span></div>
      {el('h2', 'Dans ton colis', 'In your parcel', id='tt-title')}
      <ul class="tt-rows">{rows}</ul>
      <div class="tt-total"><span data-en="Set total">Total parure</span><b data-en="€{p['price']}.00">{p['price']},00 €</b></div>
      <div class="tt-bar" aria-hidden="true"></div><div class="tt-sku">{p['sku']} · CHARMED PARIS</div>
      <div class="tt-foot"><span data-en="14 days to change your mind">14 jours pour changer d'avis</span><span>Paris</span></div>
    </aside>
    <ul class="reass-list" aria-label="Nos engagements" data-en-aria-label="Our promises">
      <li>{icon('shield')}<div>{el('b', 'Droits payés', 'Duties paid')}{el('span', 'Rien à régler à la livraison', 'Nothing to pay on delivery')}</div></li>
      <li>{icon('return')}<div>{el('b', "14 jours pour changer d'avis", '14 days to change your mind')}{el('span', 'Retour à nos frais, rétractation en ligne', 'Returns on us, online withdrawal')}</div></li>
      <li>{icon('lock')}<div>{el('b', 'Paiement sécurisé', 'Secure payment')}{el('span', 'Carte, Apple Pay, Google Pay, PayPal (à confirmer)', 'Card, Apple Pay, Google Pay, PayPal (to confirm)')}</div></li>
    </ul>
  </section>
</div>
<section class="band" aria-labelledby="xs-t" style="padding-top:24px"><div class="wrap">
  <div class="head-row"><div>{el('p', '2e parure −15 %', '15% off your second set', 'eyebrow')}{el('h2', 'Une pour toi, une à offrir', 'One for you, one to give', 'h2', id='xs-t')}
    {el('p', 'Dès deux parures, la moins chère est à −15 %, appliqué automatiquement dans ton écrin. Elles voyagent dans le même colis : une boîte à bijoux par commande, la 2e parure en sachet scellé.', 'From two sets, the cheaper one is 15% off, applied automatically in your box. They travel in the same parcel: one jewellery box per order, the second set in a sealed bag.', 'muted')}</div>
    <a class="btn ghost" href="{U['file']}" data-en="All {a(U['en'])} sets">Toutes les parures {e(U['fr'])}</a></div>
  {grid(u=p['u'] if UNIVERS[p['u']]['count'] > 3 else None, exclude=p['sku'], limit=4, cls='g4')}
</div></section>
<section class="band" aria-labelledby="det-t" style="padding-top:0"><div class="wrap details">
  <div>{el('p', 'Les détails', 'Details', 'eyebrow')}{el('h2', f"Tout sur {p['model']}", f"Everything about {p['model']}", 'h2', id='det-t')}{el('p', 'Matières, entretien, livraison : les réponses franches, avant que tu les demandes.', 'Materials, care, delivery: the straight answers, before you ask.', 'muted')}</div>
  <div class="acc">{acc_html}</div>
</div></section>
{reviews_slot()}
<div class="sticky-atc" id="stickyAtc" aria-hidden="true" inert><div class="n"><b>{e(p['model'])}</b><span id="satcPrice">{p['price']},00 €</span></div><button class="btn" type="button" id="satc" data-en="Add">Ajouter</button></div>'''

    def ld(l):
        prod = {'@type': 'Product', '@id': DOMAIN + m['url' if l == 'fr' else 'url_en'] + '#product', 'name': p['name'][l], 'sku': p['sku'], 'mpn': p['sku'],
                'brand': {'@type': 'Brand', 'name': 'CHARMED PARIS'}, 'image': [p['img']] + ([p['cut']] if p['cut'] else []),
                'description': (m['desc'] if l == 'fr' else m['desc_en']), 'category': f"Bijoux > Parures > {U['fr']}" if l == 'fr' else f"Jewellery > Sets > {U['en']}",
                'material': p['mat'][l], 'url': DOMAIN + m['url' if l == 'fr' else 'url_en'],
                'offers': {'@type': 'Offer', 'priceCurrency': 'EUR', 'price': f"{p['price']}.00", 'availability': 'https://schema.org/InStock', 'itemCondition': 'https://schema.org/NewCondition',
                           'seller': {'@id': f'{DOMAIN}/#organization'},
                           'shippingDetails': {'@type': 'OfferShippingDetails', 'shippingRate': {'@type': 'MonetaryAmount', 'value': '0.00' if p['price'] >= 50 else '4.90', 'currency': 'EUR'},
                                               'shippingDestination': {'@type': 'DefinedRegion', 'addressCountry': 'FR'},
                                               'deliveryTime': {'@type': 'ShippingDeliveryTime', 'handlingTime': {'@type': 'QuantitativeValue', 'minValue': 1, 'maxValue': 2, 'unitCode': 'DAY'},
                                                                'transitTime': {'@type': 'QuantitativeValue', 'minValue': 3, 'maxValue': 7, 'unitCode': 'DAY'}}},
                           'hasMerchantReturnPolicy': {'@type': 'MerchantReturnPolicy', 'applicableCountry': 'FR', 'returnPolicyCategory': 'https://schema.org/MerchantReturnFiniteReturnWindow',
                                                       'merchantReturnDays': 14, 'returnMethod': 'https://schema.org/ReturnByMail', 'returnFees': 'https://schema.org/FreeReturn'}}}
        if p.get('variants'):
            prod['color'] = 'Doré ou argenté' if l == 'fr' else 'Gold-plated or silver tone'
        return [prod, ld_breadcrumb(cr, l)]
    page(p['url'], title=m['title'], title_en=m['title_en'], desc=m['desc'], desc_en=m['desc_en'], body=body, url=m['url'], url_en=m['url_en'], ld_fr=ld('fr'), ld_en=ld('en'), cur=U['file'], og_img=p['img'])

def build_cadeaux():
    m = seo('Hub Idées cadeaux', 'Gift ideas hub')
    cr = [('index.html', 'Accueil', 'Home'), (None, 'Idées cadeaux', 'Gift ideas')]
    def gift_txt(num_fr, num_en):
        f = section(PAGES_FR, r'### ' + re.escape(num_fr) + r'\n', r'\n(### |## |---)')
        g = section(PAGES_EN, r'### ' + re.escape(num_en) + r'\n', r'\n(### |## |---)')
        clean = lambda s: '\n'.join(l for l in s.split('\n') if not re.match(r'^\*\*H1|^(Sélection|Selection)\s?:', l))
        return md(clean(f)), md(clean(g))
    secs = [('noel', '3.4 Noël', '3.4 Christmas', 'Cadeaux de Noël', 'Christmas gifts', ['JSJB3S', 'JSC940', 'JSDYG2', 'JSCT1F', 'JS1AQ5', 'JSDQA1']),
            ('moins-50', '3.1 Cadeaux à moins de 50 €', '3.1 Gifts under €50', 'Idées cadeaux à moins de 50 €', 'Gift ideas under €50', ['JSGRQR', 'JSM1BZ', 'JS8445', 'JSVKMZ', 'JSCT1F']),
            ('moins-100', '3.2 Cadeaux à moins de 100 €', '3.2 Gifts under €100', 'Idées cadeaux à moins de 100 €', 'Gift ideas under €100', ['JS63WT', 'JSG813', 'JS1AQ5', 'JS4AH6', 'JS63VP', 'JSX3G6', 'JSB541', 'JSDYG2']),
            ('plus-100', '3.3 Cadeaux à plus de 100 €', '3.3 Gifts over €100', 'Idées cadeaux à plus de 100 €', 'Gift ideas over €100', ['JS1PPS', 'JSSFYS', 'JSDQA1']),
            ('fete-des-meres', '3.5 Fête des mères', "3.5 Mother's Day", 'Cadeaux pour la fête des mères', "Mother's Day gifts", ['JS4P8D', 'JSX3G6', 'JSG813', 'JSDQA1']),
            ('anniversaire', '3.6 Anniversaire', '3.6 Birthdays', "Cadeaux d'anniversaire", 'Birthday gifts', ['JSB541', 'JS8445', 'JS4AH6', 'JSJB3S', 'JSSFYS'])]
    toc = ''.join(f'<a class="chip" href="#{k}" data-en="{a(h2e)}">{e(h2f)}</a>' for k, _, _, h2f, h2e, _ in secs) + '<a class="chip" href="#pour-lui" data-en="For him">Pour lui</a>'
    html_secs = ''
    for k, nf, ne, h2f, h2e, skus in secs:
        tf, te = gift_txt(nf, ne)
        extra = ''
        if k == 'noel':
            extra = f'<p class="deadline" data-xmas="avant">{icon("star")}<span data-en="Order by Friday 4 December 2026 for delivery before Christmas in Europe">Commande avant le vendredi 4 décembre 2026 pour une livraison avant Noël en Europe</span></p>'
        html_secs += f'''<section class="gift-sec" id="{k}" aria-labelledby="{k}-t">
  <div class="head-row"><div>{el('h2', h2f, h2e, 'h2', id=k + '-t')}{extra}<div class="lead" style="margin-top:14px">{bi(tf, te)}</div></div></div>
  {grid(skus=skus, cls='g4')}
</section>'''
    html_secs += f'''<section class="gift-sec" id="pour-lui" aria-labelledby="pl-t">
  <div class="head-row"><div>{el('h2', 'Pour lui', 'For him', 'h2', id='pl-t')}{el('p', 'Deux parures sur cordon noir, à porter seul ou à partager, et bientôt une petite ligne homme dans les pièces seules.', 'Two sets on black cord, to wear alone or to share, and soon a small men\'s line among the single pieces.', 'lead')}</div><a class="btn ghost" href="pieces-seules.html#homme" data-en="Men's single pieces">Pièces seules homme</a></div>
  {grid(skus=['JSVKMZ', 'JSCT1F'], cls='g4')}
</section>'''
    body = f'''{crumbs(cr)}
<div class="wrap">
  <header class="page-head">
    {el('h1', m['h1'], m['h1_en'])}
    {el('p', 'Une parure arrive dans sa boîte à bijoux nouée d\'un ruban, sans aucun prix dans le colis : tu peux la faire livrer directement chez la personne. Choisis par budget ou par occasion.', 'A set arrives in its ribboned jewellery box, with no prices in the parcel: you can send it straight to them. Choose by budget or by occasion.', 'lead')}
    {el('p', 'Pas de message cadeau ni de gravure · Une boîte par commande · 2e parure −15 %', 'No gift message or engraving · One box per order · 15% off your second set', 'facts-line')}
  </header>
  <div class="budgets">
    <a class="budget" href="#moins-50">{el('span', 'Moins de', 'Under')}<b data-en="€50">50 €</b>{el('span', '5 parures à 49 €', '5 sets at €49')}</a>
    <a class="budget" href="#moins-100">{el('span', 'Moins de', 'Under')}<b data-en="€100">100 €</b>{el('span', 'La plupart de nos parures', 'Most of our sets')}</a>
    <a class="budget" href="#plus-100">{el('span', 'Plus de', 'Over')}<b data-en="€100">100 €</b>{el('span', 'Argent 925 et moissanite synthétique', 'Sterling silver and lab-grown moissanite')}</a>
  </div>
  <nav class="toc" aria-label="Occasions" data-en-aria-label="Occasions" style="margin-top:22px">{toc}</nav>
  {html_secs}
</div>
{reass()}'''
    all_skus = []
    for s in secs:
        all_skus += [x for x in s[5] if x not in all_skus]
    ld = lambda l: webpage_ld(m['title'] if l == 'fr' else m['title_en'], m['desc'] if l == 'fr' else m['desc_en'], m['url'] if l == 'fr' else m['url_en'], cr, l, 'CollectionPage', {'mainEntity': itemlist([BY[s] for s in all_skus], l)})
    page('cadeaux.html', title=m['title'], title_en=m['title_en'], desc=m['desc'], desc_en=m['desc_en'], body=body, url=m['url'], url_en=m['url_en'], ld_fr=ld('fr'), ld_en=ld('en'), data_list='cadeaux.html', og_img='assets/img/pack/pack-noel-f-600.webp')

def build_pieces():
    cr = [('index.html', 'Accueil', 'Home'), (None, 'Pièces seules', 'Single pieces')]
    title, title_en = 'Pièces seules : colliers et pendentifs | CHARMED PARIS', 'Single Pieces: Necklaces & Pendants | CHARMED PARIS'
    desc = 'Les parures restent notre cœur ; voici quelques pièces seules choisies avec le même soin, et une petite ligne homme. Prix et références à confirmer.'
    desc_en = 'Sets remain at our heart; here are a few single pieces chosen with the same care, and a small men\'s line. Prices and references to confirm.'
    cards = ''
    for pc in PIECES:
        cards += f'''<article class="card">
  <div class="visual"><img src="assets/img/pieces/{pc['img']}" alt="{a(pc['fr'] + ' : ' + pc['mat_fr'])}" data-en-alt="{a(pc['en'] + ': ' + pc['mat_en'])}" width="400" height="400" loading="lazy"><span class="tag" data-en="Soon">Bientôt</span></div>
  <h3 data-en="{a(pc['en'])}">{e(pc['fr'])}</h3>
  <div class="meta"><span class="pcs" data-en="{a(pc['mat_en'])}">{e(pc['mat_fr'])}</span></div>
  <div class="meta"><span data-en="Price to confirm">Prix à confirmer</span><span class="small" data-en="{a('Ref. ' + pc.get('ref_en', pc['ref']))}">{e('Réf. ' + pc['ref'])}</span></div>
</article>'''
    men = PIECE_MEN
    body = f'''{crumbs(cr)}
<div class="wrap">
  <header class="page-head">
    {el('p', 'Nouvelle rubrique', 'New', 'eyebrow')}
    {el('h1', 'Pièces seules', 'Single pieces')}
    {el('p', 'Les parures restent notre cœur. Pour commencer petit, compléter une parure ou offrir un détail, voici quelques pièces seules choisies avec le même soin, et une petite ligne homme.', 'Sets remain at our heart. To start small, complete a set or give a little something, here are a few single pieces chosen with the same care, and a small men\'s line.', 'lead')}
    {el('p', 'Prix à confirmer, entre 29 et 59 € · Disponibles bientôt', 'Prices to confirm, between €29 and €59 · Available soon', 'facts-line')}
  </header>
  <aside class="mock-note"><b>Note interne (maquette)</b>{bi('<p>Décision du 23/11/2026 (woocommerce/source/pieces-seules.md). À faire avant la mise en vente : relever coût, carat et dimensions dans le compte fournisseur, fixer les prix (29–59 € à valider ; la moissanite sera probablement au-dessus), confirmer les références du pendentif moissanite et du pendentif plume, décider si les pièces seules comptent pour la livraison offerte dès 50 € et pour la remise 2e parure. Tant que ce n\'est pas fait : pas de bouton d\'achat.</p>', '<p>Decision of 23/11/2026 (woocommerce/source/pieces-seules.md). Before selling: record cost, karat and dimensions in the supplier account, set prices (€29–59 to validate; the moissanite will likely be above), confirm the moissanite and feather pendant references, decide whether single pieces count towards free delivery from €50 and the second-set discount. Until then: no buy button.</p>')}</aside>
  <section class="gift-sec" aria-labelledby="pf-t" style="border-top:0;padding-top:8px">
    {el('h2', 'Pour elle', 'For her', 'h2 sr-only', id='pf-t')}
    <div class="grid g4">{cards}</div>
  </section>
</div>
<section class="band velours" id="homme" aria-labelledby="homme-t"><div class="wrap">
  <div class="head-row"><div>{el('p', 'Petite ligne homme', "Small men's line", 'eyebrow')}{el('h2', 'Pour lui', 'For him', 'h2', id='homme-t')}
    {el('p', 'Peu de pièces, sobres, à porter tous les jours. Le packaging homme est noir, avec une pochette noire.', 'A few understated pieces to wear every day. The men\'s packaging is black, with a black pouch.', 'lead')}</div></div>
  <div class="grid g4">
    <article class="card"><div class="visual" style="background:var(--velours-2);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 1480 1000" width="120" aria-hidden="true" style="position:relative;fill:var(--or-clair)"><path d="M560 0H500A500 500 0 0 0 0 500V500A500 500 0 0 0 500 1000H560V966H500A350 466 0 0 1 150 500V500A350 466 0 0 1 500 34H560Z"/><path d="M740 350L845 500L740 650L635 500Z"/><path d="M920 0H980A500 500 0 0 1 1480 500V500A500 500 0 0 1 980 1000H920V966H980A350 466 0 0 0 1330 500V500A350 466 0 0 0 980 34H920Z"/></svg><span class="tag" data-en="Photo to come">Photo à venir</span></div>
      <h3 data-en="{a(men['en'])}">{e(men['fr'])}</h3><div class="meta"><span class="pcs" style="color:var(--velours-muted)" data-en="{a(men['mat_en'])}">{e(men['mat_fr'])}</span></div>
      <div class="meta" style="color:var(--velours-muted)"><span data-en="Price to confirm">Prix à confirmer</span><span class="small" data-en="{a('Ref. ' + men['ref_en'])}">{e('Réf. ' + men['ref'])}</span></div></article>
  </div>
  <div class="head-row" style="margin-top:44px"><div>{el('h3', 'Et en parure : la ligne Mixte', 'And as a set: the Unisex line', '', style='font-size:26px')}{el('p', 'Deux parures sur cordon noir réglable, à 49 €, disponibles dès maintenant.', 'Two sets on adjustable black cord, €49, available now.', 'muted')}</div><a class="btn gold" href="univers-mixte.html" data-en="See the Unisex sets">Voir les parures Mixte</a></div>
  {grid(skus=['JSVKMZ', 'JSCT1F'], cls='g4')}
</div></section>
{reass()}'''
    ld = lambda l: webpage_ld(title if l == 'fr' else title_en, desc if l == 'fr' else desc_en, '/pieces-seules/' if l == 'fr' else '/en/single-pieces/', cr, l, 'CollectionPage')
    page('pieces-seules.html', title=title, title_en=title_en, desc=desc, desc_en=desc_en, body=body, url='/pieces-seules/', url_en='/en/single-pieces/', ld_fr=ld('fr'), ld_en=ld('en'), index=False)

def content_page(file, seo_key, sec_fr, sec_en, cr_fr, cr_en, url=None, url_en=None, typ='WebPage', extra_body='', mainentity=None, title_override=None):
    if seo_key:
        m = seo(*seo_key)
    else:
        m = title_override
    cr = [('index.html', 'Accueil', 'Home'), (None, cr_fr, cr_en)]
    body = f'''{crumbs(cr)}
<div class="wrap">
  <header class="page-head">{el('h1', m['h1'], m['h1_en'])}</header>
  <div class="prose">{bi(sec_fr, sec_en)}</div>
  {extra_body}
</div>
<div class="band" style="padding-block:28px 0"></div>
{reass()}'''
    ld = lambda l: webpage_ld(m['title'] if l == 'fr' else m['title_en'], m['desc'] if l == 'fr' else m['desc_en'], (url or m['url']) if l == 'fr' else (url_en or m['url_en']), cr, l, typ, mainentity(l) if mainentity else None)
    page(file, title=m['title'], title_en=m['title_en'], desc=m['desc'], desc_en=m['desc_en'], body=body, url=url or m['url'], url_en=url_en or m['url_en'], ld_fr=ld('fr'), ld_en=ld('en'), index=m.get('index', True))

def pages_section(src, num_title):
    s = section(src, r'## ' + re.escape(num_title) + r'\n', r'\n---')
    return '\n'.join(l for l in s.split('\n') if not l.startswith('**H1'))

def build_static_pages():
    # À propos
    fr = pages_section(PAGES_FR, '4. À propos').replace('[À COMPLÉTER : e-mail de contact]', 'bonjour@charmedparis.com [À CONFIRMER]')
    en = pages_section(PAGES_EN, '4. About').replace('[TO COMPLETE: contact email]', 'bonjour@charmedparis.com [TO CONFIRM]')
    contact = f'''<section id="contact" class="panel" style="max-width:760px;margin-top:32px" aria-labelledby="ct-t">{el('h2', 'Nous écrire', 'Write to us', id='ct-t')}
      {elh('p', 'Une question sur une parure, une commande ou un cadeau : <a class="link" href="mailto:bonjour@charmedparis.com">bonjour@charmedparis.com</a> <mark class="todo">[adresse à confirmer]</mark>. Une personne de l\'équipe te répond, en français ou en anglais.', 'A question about a set, an order or a gift: <a class="link" href="mailto:bonjour@charmedparis.com">bonjour@charmedparis.com</a> <mark class="todo">[address to confirm]</mark>. A real person on the team replies, in French or English.')}
      {elh('p', 'Allergie ou peau sensible ? Écris-nous avant de commander : on te transmet la composition détaillée. Pour changer d\'avis : <a class="link" href="retractation.html">formulaire de rétractation en ligne</a>.', 'Allergy or sensitive skin? Write to us before ordering and we\'ll send the detailed composition. To change your mind: <a class="link" href="retractation.html">online withdrawal form</a>.')}</section>'''
    content_page('a-propos.html', ('Notre histoire', 'Our story'), md(fr), md(en), 'Notre histoire', 'Our story', typ='AboutPage', extra_body=contact)
    # Livraison & retours
    fr = pages_section(PAGES_FR, '5. Livraison & retours').replace('utilise le formulaire de rétractation en bas de page', 'utilise le [formulaire de rétractation en ligne](retractation.html)')
    en = pages_section(PAGES_EN, '5. Shipping & returns').replace('use the withdrawal form at the bottom of this page', 'use the [online withdrawal form](retractation.html)')
    cta = f'<p style="margin-top:28px"><a class="btn" href="retractation.html" data-en="Withdraw from my order">Me rétracter</a></p>'
    content_page('livraison-retours.html', ('Livraison et retours', 'Shipping & returns'), md(fr) + noel_box(), md(en), 'Livraison et retours', 'Shipping & returns', extra_body=cta)
    # Matières & entretien
    content_page('matieres-entretien.html', ('Matières & entretien', 'Materials & care'), md(pages_section(PAGES_FR, '6. Matières & entretien')), md(pages_section(PAGES_EN, '6. Materials & care')), 'Matières et entretien', 'Materials & care')
    # FAQ (accordéon + FAQPage)
    def faq_items(src, title):
        s = pages_section(src, title)
        return [(q.strip(), r.strip()) for q, r in re.findall(r'\*\*\d+\.\s*(.+?)\*\*\n(.+?)(?=\n\n|\n>|$)', s, re.S)]
    qf, qe = faq_items(PAGES_FR, '7. FAQ'), faq_items(PAGES_EN, '7. FAQ')
    acc = ''
    for i, ((q1, r1), (q2, r2)) in enumerate(zip(qf, qe)):
        acc += (f'<div class="acc-item"><h3><button class="acc-btn q" type="button" aria-expanded="false" aria-controls="fq{i}" id="fq{i}b"><span data-en="{a(q2)}">{e(q1)}</span><i aria-hidden="true"></i></button></h3>'
                f'<div class="acc-panel" id="fq{i}" role="region" aria-labelledby="fq{i}b"><div><div class="acc-body"><p data-en="{a(r2)}">{e(r1)}</p></div></div></div></div>')
    m = seo('FAQ', 'FAQ')
    cr = [('index.html', 'Accueil', 'Home'), (None, 'Questions fréquentes', 'FAQ')]
    body = f'''{crumbs(cr)}
<div class="wrap">
  <header class="page-head">{el('h1', m['h1'], m['h1_en'])}{el('p', 'Matières, entretien, livraison, douane, retours, cadeau : les réponses franches, avant que tu les demandes.', 'Materials, care, shipping, customs, returns, gifting: straight answers, before you ask.', 'lead')}</header>
  <div class="acc narrow">{acc}</div>
  {elh('p', 'Pas trouvé ? <a class="link" href="a-propos.html#contact">Écris-nous</a>.', 'Not here? <a class="link" href="a-propos.html#contact">Write to us</a>.', 'muted', style='margin-top:24px')}
</div>
<div class="band" style="padding-block:28px 0"></div>
{reass()}'''
    faq_ld = lambda items: {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': r}} for q, r in items]}
    ld = lambda l: [faq_ld(qf if l == 'fr' else qe), ld_breadcrumb(cr, l)]
    page('faq.html', title=m['title'], title_en=m['title_en'], desc=m['desc'], desc_en=m['desc_en'], body=body, url=m['url'], url_en=m['url_en'], ld_fr=ld('fr'), ld_en=ld('en'))

def legal_md(name):
    s = read(W / f'legal/{name}')
    s = re.sub(r'^# .+\n', '', s, count=1)
    return md(fix_fr(s) if not name.endswith('-en.md') else s)

def build_legal():
    defs = [('cgv.html', 'cgv', ('CGV', 'Terms'), None, 'CGV', 'Terms of sale', True),
            ('mentions-legales.html', 'mentions-legales', None, dict(title='Mentions légales | CHARMED PARIS', title_en='Legal Notice | CHARMED PARIS', desc='Mentions légales de CHARMED PARIS : éditeur, hébergeur, vente en ligne, médiation, propriété intellectuelle.', desc_en='CHARMED PARIS legal notice: publisher, host, online sales, mediation, intellectual property.', h1='Mentions légales', h1_en='Legal notice', url='/mentions-legales/', url_en='/en/legal-notice/', index=False), 'Mentions légales', 'Legal notice', False),
            ('confidentialite.html', 'politique-confidentialite', None, dict(title='Politique de confidentialité | CHARMED PARIS', title_en='Privacy Policy | CHARMED PARIS', desc='Comment CHARMED PARIS traite tes données personnelles : finalités, bases légales, durées, destinataires, transferts et tes droits.', desc_en='How CHARMED PARIS handles your personal data: purposes, legal bases, retention, recipients, transfers and your rights.', h1='Politique de confidentialité', h1_en='Privacy policy', url='/politique-de-confidentialite/', url_en='/en/privacy-policy/', index=False), 'Confidentialité', 'Privacy', False),
            ('cookies.html', 'politique-cookies', None, dict(title='Politique cookies | CHARMED PARIS', title_en='Cookie Policy | CHARMED PARIS', desc='Les cookies et traceurs utilisés par CHARMED PARIS, leurs finalités, leurs durées et comment changer ton choix à tout moment.', desc_en='The cookies and trackers CHARMED PARIS uses, why, for how long, and how to change your choice at any time.', h1='Politique cookies', h1_en='Cookie policy', url='/cookies/', url_en='/en/cookies/', index=False), 'Cookies', 'Cookies', False)]
    for file, src, seo_key, over, crf, cre, idx in defs:
        extra = ''
        if file == 'cookies.html':
            extra = '<p style="margin-top:24px"><button class="btn" type="button" data-cookies data-en="Manage my cookies">Gérer mes cookies</button></p>'
        content_page(file, seo_key, legal_md(src + '.md'), legal_md(src + '-en.md'), crf, cre, extra_body=extra, title_override=over)

def build_retract():
    title, title_en = 'Me rétracter : rétractation en ligne | CHARMED PARIS', 'Withdraw From My Order Online | CHARMED PARIS'
    desc = 'Rétracte-toi en ligne dans les 14 jours suivant la réception de ta commande : formulaire, confirmation et accusé de réception immédiat.'
    desc_en = 'Withdraw online within 14 days of receiving your order: form, confirmation and an immediate acknowledgement of receipt.'
    cr = [('index.html', 'Accueil', 'Home'), ('livraison-retours.html', 'Livraison et retours', 'Shipping & returns'), (None, 'Me rétracter', 'Withdraw from my order')]
    form_fr = section(read(W / 'legal/retours-et-retractation.md'), r'## Formulaire de rétractation\n', r'\n---')
    form_en = section(read(W / 'legal/retours-et-retractation-en.md'), r'## Withdrawal form\n', r'\n---')
    def f(id_, lab_fr, lab_en, typ='text', req=True, help_fr='', help_en='', ac='', area=False):
        opt = '' if req else ' <span class="opt" data-en="(optional)">(facultatif)</span>'
        hp = f'<span class="help" id="{id_}H" data-en="{a(help_en)}">{e(help_fr)}</span>' if help_fr else ''
        desc_ = f' aria-describedby="{id_}H"' if help_fr else ''
        ctrl = (f'<textarea id="{id_}" name="{id_}"{" required" if req else ""}{desc_}></textarea>' if area else
                f'<input id="{id_}" name="{id_}" type="{typ}"{" required" if req else ""}{f" autocomplete={chr(34)}{ac}{chr(34)}" if ac else ""}{desc_}>')
        return f'<div class="field"><label for="{id_}"><span data-en="{a(lab_en)}">{e(lab_fr)}</span>{opt}</label>{hp}{ctrl}<p class="err" hidden></p></div>'
    body = f'''{crumbs(cr)}
<div class="wrap">
  <header class="page-head">{el('h1', 'Me rétracter', 'Withdraw from my order')}
    {el('p', "Tu as 14 jours à compter de la réception de ta commande pour changer d'avis, sans avoir à te justifier. Remplis ce formulaire : tu reçois aussitôt un accusé de réception par e-mail. Les frais de retour sont à notre charge.", 'You have 14 days from receiving your order to change your mind, no reason needed. Fill in this form: you\'ll get an acknowledgement by email straight away. Return costs are on us.', 'lead')}</header>
  <aside class="mock-note"><b>Note interne (maquette)</b>{bi('<p>Fonctionnalité de rétractation en ligne obligatoire depuis le 19/06/2026 (L. 221-21, ordonnance 2026-2). Libellé exact du bouton selon le décret 2026-3 : <mark class="todo">[À VÉRIFIER]</mark>. Ici, rien n\'est envoyé : la demande est seulement gardée dans ton navigateur pour la démonstration. En production : accessible sans compte, accusé de réception sur support durable (e-mail) avec date et heure.</p>', '<p>Online withdrawal function required since 19/06/2026 (French Consumer Code L. 221-21, ordonnance 2026-2). Exact button wording per décret 2026-3: <mark class="todo">[TO CHECK]</mark>. Here nothing is sent: the request is only kept in your browser for the demo. In production: available without an account, acknowledgement on a durable medium (email) with date and time.</p>')}</aside>
  <div class="cart-page" style="padding-bottom:0">
    <section aria-labelledby="wd-t">
      <div id="wdStep1">
        {el('h2', '1. Ta demande', '1. Your request', 'h2', id='wd-t', style='font-size:28px;margin-bottom:16px')}
        <form id="wdForm" novalidate>
          <div class="row2">{f('wdName', 'Nom et prénom', 'Full name', ac='name')}{f('wdEmail', 'E-mail utilisé pour la commande', 'Email used for the order', 'email', ac='email', help_fr='Tu recevras l\'accusé de réception à cette adresse.', help_en='Your acknowledgement goes to this address.')}</div>
          <div class="row2">{f('wdOrder', 'Numéro de commande', 'Order number', help_fr='Il figure dans ton e-mail de confirmation (ex. CP-1234).', help_en='It\'s in your confirmation email (e.g. CP-1234).')}{f('wdDate', 'Date de réception', 'Date received', 'date', req=False)}</div>
          {f('wdItems', 'Parure(s) concernée(s)', 'Set(s) concerned', area=True, help_fr='Une par ligne. Toute la commande si tu laisses « toute la commande ».', help_en='One per line. Write “whole order” for everything.')}
          {f('wdReason', 'Motif', 'Reason', area=True, req=False, help_fr='Tu n\'as pas à te justifier. Ça nous aide seulement à progresser.', help_en='You don\'t need to give a reason. It just helps us improve.')}
          <button class="btn big" type="submit" data-en="Check my request">Vérifier ma demande</button>
        </form>
      </div>
      <div id="wdStep2" hidden>
        <h2 id="wdStep2Title" tabindex="-1" style="font-size:28px;margin-bottom:12px" data-en="2. Check and confirm">2. Vérifie et confirme</h2>
        <dl id="wdRecap" class="panel" style="display:grid;grid-template-columns:auto 1fr;gap:6px 16px;margin:0 0 18px"></dl>
        <div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn ghost" type="button" id="wdBack" data-en="Edit">Modifier</button><button class="btn big" type="button" id="wdConfirm" data-en="Confirm the withdrawal">Confirmer la rétractation</button></div>
      </div>
      <div id="wdStep3" hidden class="confirm">
        <h2 id="wdStep3Title" tabindex="-1" data-en="It's recorded">C'est enregistré</h2>
        <p>{el('span', 'Ta déclaration de rétractation a été reçue le', 'Your withdrawal notice was received on')} <b id="wdWhen"></b>. {el('span', 'Référence', 'Reference')} <b id="wdRef"></b>.</p>
        <p>{el('span', 'Un accusé de réception est envoyé à', 'An acknowledgement is sent to')} <b id="wdMail"></b> {el('span', '(simulé dans la maquette).', '(simulated in the mock-up).')}</p>
        <ol class="timeline">
          <li><i>1</i>{elh('span', 'Renvoie la parure complète, dans son coffret, sous 14 jours, à : <mark class="todo">[À COMPLÉTER : adresse de retour en France]</mark>. Les frais de retour sont à notre charge.', 'Send the set back complete, in its box, within 14 days, to: <mark class="todo">[TO COMPLETE: return address in France]</mark>. Return costs are on us.')}</li>
          <li><i>2</i>{el('span', 'Nous te remboursons sous 14 jours après ta demande, par le même moyen de paiement (nous pouvons attendre la réception de la parure ou la preuve de son envoi).', 'We refund you within 14 days of your request, to your original payment method (we may wait for the set or proof that you\'ve sent it).')}</li>
        </ol>
        <a class="btn ghost" href="index.html" data-en="Back to the shop">Retour à la boutique</a>
      </div>
    </section>
    <aside><div class="panel">{el('h2', 'Bon à savoir', 'Good to know')}
      <ul class="reass-list">
        <li>{icon('clock')}<div>{el('b', '14 jours', '14 days')}{el('span', 'À compter de la réception de ta commande', 'From the day you receive your order')}</div></li>
        <li>{icon('return')}<div>{el('b', 'Retour à nos frais', 'Returns on us')}{el('span', 'Parure complète, dans son coffret', 'Complete set, in its box')}</div></li>
        <li>{icon('shield')}<div>{el('b', 'Garantie légale 2 ans', '2-year legal guarantee')}{elh('span', 'Parure abîmée ou erreur ? <a class="link" href="livraison-retours.html">Voir la procédure</a>', 'Damaged or wrong set? <a class="link" href="livraison-retours.html">See the procedure</a>')}</div></li>
      </ul></div></aside>
  </div>
  <section class="prose" style="margin-top:56px" aria-labelledby="ft-t">
    {el('h2', 'Formulaire type de rétractation', 'Model withdrawal form', id='ft-t')}
    {el('p', "Tu peux aussi l'imprimer ou le recopier et nous l'envoyer par courrier ou par e-mail. Son utilisation n'est pas obligatoire.", 'You can also print or copy it and send it to us by post or email. Using it is optional.', 'muted')}
    {bi(md(form_fr), md(form_en))}
  </section>
</div>
<div class="band" style="padding-block:28px 0"></div>'''
    ld = lambda l: webpage_ld(title if l == 'fr' else title_en, desc if l == 'fr' else desc_en, '/retractation/' if l == 'fr' else '/en/cancellation-form/', cr, l)
    page('retractation.html', title=title, title_en=title_en, desc=desc, desc_en=desc_en, body=body, url='/retractation/', url_en='/en/cancellation-form/', ld_fr=ld('fr'), ld_en=ld('en'), index=False)

def build_cart():
    cr = [('index.html', 'Accueil', 'Home'), (None, 'Ton écrin', 'Your box')]
    title, title_en = 'Ton écrin (panier) | CHARMED PARIS', 'Your Box (Cart) | CHARMED PARIS'
    desc, desc_en = 'Ton panier CHARMED PARIS : parures, remise 2e parure −15 %, livraison offerte dès 50 €.', 'Your CHARMED PARIS cart: sets, 15% off your second set, free delivery from €50.'
    body = f'''{crumbs(cr)}
<div class="wrap">
  <header class="page-head"><h1><span data-en="Your box">Ton écrin</span> <span id="cartCount" class="muted" style="font-size:.5em"></span></h1></header>
  <div class="cart-page" id="cartPage">
    <section aria-label="Parures dans ton écrin" data-en-aria-label="Sets in your box">
      <div class="shipbar" id="cartShip" style="margin-bottom:8px"><span class="txt"></span><div class="bar"><i></i></div></div>
      <div class="cart-lines" id="cartLines"></div>
      <div id="cartUpsell"></div>
      <p style="margin-top:18px"><a class="link" data-back href="parures.html" data-en="Keep browsing">Continuer à regarder</a></p>
    </section>
    <aside><div class="panel">
      {el('h2', 'Récapitulatif', 'Summary')}
      <div class="sum" id="cartSum"></div>
      <a class="btn block big" id="cartGo" href="paiement.html" style="margin-top:14px" data-en="Checkout">Commander</a>
      <p class="small muted" id="cartEta" style="margin-top:14px"></p>
      {noel_box()}
      <ul class="reass-list" style="margin-top:16px">
        <li>{icon('lock')}<div>{el('b', 'Paiement sécurisé', 'Secure payment')}{el('span', 'Carte, Apple Pay, Google Pay, PayPal (à confirmer)', 'Card, Apple Pay, Google Pay, PayPal (to confirm)')}</div></li>
        <li>{icon('return')}<div>{el('b', "14 jours pour changer d'avis", '14 days to change your mind')}{el('span', 'Retour à nos frais', 'Returns on us')}</div></li>
        <li>{icon('gift')}<div>{el('b', "C'est un cadeau ?", 'Is it a gift?')}{el('span', "Aucun prix dans le colis. Mets l'adresse de la personne en livraison. Pas de message cadeau possible.", 'No prices in the parcel. Use their address for delivery. No gift message possible.')}</div></li>
      </ul>
    </div></aside>
  </div>
</div>'''
    ld = lambda l: webpage_ld(title if l == 'fr' else title_en, desc if l == 'fr' else desc_en, '/panier/' if l == 'fr' else '/en/cart/', cr, l)
    page('panier.html', title=title, title_en=title_en, desc=desc, desc_en=desc_en, body=body, url='/panier/', url_en='/en/cart/', ld_fr=ld('fr'), ld_en=ld('en'), index=False)

def build_checkout():
    cr = [('index.html', 'Accueil', 'Home'), ('panier.html', 'Ton écrin', 'Your box'), (None, 'Commande', 'Checkout')]
    title, title_en = 'Commande | CHARMED PARIS', 'Checkout | CHARMED PARIS'
    desc, desc_en = 'Finalise ta commande CHARMED PARIS : livraison suivie DHL, droits payés, paiement sécurisé.', 'Complete your CHARMED PARIS order: DHL tracked delivery, duties paid, secure payment.'
    countries = [('FR', 'France', 'France'), ('BE', 'Belgique', 'Belgium'), ('LU', 'Luxembourg', 'Luxembourg'), ('DE', 'Allemagne', 'Germany'), ('ES', 'Espagne', 'Spain'), ('IT', 'Italie', 'Italy'), ('NL', 'Pays-Bas', 'Netherlands'), ('IE', 'Irlande', 'Ireland'), ('PT', 'Portugal', 'Portugal'), ('AT', 'Autriche', 'Austria')]
    def f(id_, lab_fr, lab_en, typ='text', req=True, ac='', help_fr='', help_en='', extra=''):
        opt = '' if req else ' <span class="opt" data-en="(optional)">(facultatif)</span>'
        hp = f'<span class="help" id="{id_}H" data-en="{a(help_en)}">{e(help_fr)}</span>' if help_fr else ''
        dsc = f' aria-describedby="{id_}H"' if help_fr else ''
        return (f'<div class="field"><label for="{id_}"><span data-en="{a(lab_en)}">{e(lab_fr)}</span>{opt}</label>{hp}'
                f'<input id="{id_}" name="{id_}" type="{typ}"{" required" if req else ""}{f" autocomplete={chr(34)}{ac}{chr(34)}" if ac else ""}{dsc}{extra}><p class="err" hidden></p></div>')
    opts = ''.join(f'<option value="{c}" data-en="{a(en)}">{e(fr)}</option>' for c, fr, en in countries)
    body = f'''{crumbs(cr)}
<div class="wrap" id="coWrap">
  <header class="page-head" style="padding-bottom:12px">{el('h1', 'Commande', 'Checkout')}</header>
  <div class="cart-page co">
    <form id="coForm" novalidate>
      <div class="err-summary" id="errSummary" tabindex="-1" hidden role="alert"><h2 data-en="A few details are missing">Il manque quelques informations</h2><ul></ul></div>
      <ol class="co-steps"><li data-en="Details">Coordonnées</li><li data-en="Delivery">Livraison</li><li data-en="Payment">Paiement</li></ol>
      <section aria-label="Paiement express" data-en-aria-label="Express checkout">
        <div class="xpay-row"><button class="xpay" type="button" aria-label="Payer avec Apple Pay" data-en-aria-label="Pay with Apple Pay"> Pay</button><button class="xpay gpay" type="button" aria-label="Payer avec Google Pay" data-en-aria-label="Pay with Google Pay">G Pay</button><button class="xpay pp" type="button" aria-label="Payer avec PayPal" data-en-aria-label="Pay with PayPal">PayPal</button></div>
        <p class="or-sep" data-en="or">ou</p>
      </section>
      <fieldset><legend data-en="Your details">Coordonnées</legend>
        {f('email', 'E-mail', 'Email', 'email', ac='email', help_fr='Pour ta confirmation et ton suivi.', help_en='For your confirmation and tracking.')}
        <label class="check"><input type="checkbox" id="optin"> <span data-en="Email me about new sets and dates that matter.">Je veux recevoir les nouvelles parures et les dates importantes par e-mail.</span></label>
      </fieldset>
      <fieldset><legend data-en="Delivery">Livraison</legend>
        <div class="field"><label for="country" data-en="Country">Pays</label><select id="country" name="country" autocomplete="country">{opts}</select>{el('span', 'Autres pays : bientôt. Royaume-Uni non ouvert pour l\'instant.', 'Other countries: soon. UK not open yet.', 'help')}</div>
        <div class="row2">{f('fname', 'Prénom', 'First name', ac='given-name')}{f('lname', 'Nom', 'Last name', ac='family-name')}</div>
        {f('address', 'Adresse', 'Address', ac='address-line1', help_fr='Vérifie le numéro de rue : une adresse incomplète bloque l\'envoi.', help_en='Check your street number: an incomplete address holds up the order.')}
        <button type="button" class="linkbtn" data-reveal="addr2Box" data-en="+ Add flat, floor or door code">+ Ajouter un complément (bâtiment, étage, code)</button>
        <div id="addr2Box" hidden>{f('address2', 'Complément', 'Flat, floor, door code', req=False, ac='address-line2')}</div>
        <div class="row2">{f('zip', 'Code postal', 'Postcode', ac='postal-code', extra=' inputmode="numeric"')}{f('city', 'Ville', 'Town or city', ac='address-level2')}</div>
        {f('phone', 'Téléphone', 'Phone', 'tel', ac='tel', help_fr='Uniquement pour le livreur DHL, qui peut en avoir besoin pour te livrer.', help_en='Only for the DHL driver, who may need it to deliver.')}
        <label class="check"><input type="checkbox" id="gift"> <span><b data-en="This is a gift">C'est un cadeau</b><br><span class="muted" data-en="No prices in the parcel. The set arrives in its ribboned drawer box. We can't add a note: you can send your message yourself on the delivery day.">Aucun prix dans le colis. La parure arrive dans sa boîte-tiroir nouée d'un ruban. On ne peut pas glisser de mot : tu peux envoyer ton message toi-même le jour de la livraison.</span></span></label>
        <label class="check"><input type="checkbox" id="shipElse"> <span data-en="Deliver to a different address (for a gift, say)">Livrer à une autre adresse (pour un cadeau, par exemple)</span></label>
        <div id="shipElseBox" hidden class="panel" style="margin-bottom:16px"><div class="row2">{f('s_name', 'Nom de la personne', 'Recipient name', req=False)}{f('s_address', 'Son adresse', 'Their address', req=False)}</div></div>
        <div class="ship-method"><span class="dot" aria-hidden="true"></span><div><b id="coEta"></b><span data-en="Ships from outside the EU (United States or China), duties already paid. No express option.">Expédiée hors UE (États-Unis ou Chine), droits de douane déjà payés. Pas d'option express.</span><br><span id="coEtaDates"></span><br><span data-en="Price:">Tarif :</span> <span id="coShipPrice"></span></div></div>
        <p class="small" data-xmas="avant" style="margin-top:10px" data-en="Ordered today, your set should arrive before Christmas in Europe (order by Friday 4 December).">Commandée aujourd'hui, ta parure devrait arriver avant Noël en Europe (commande avant le vendredi 4 décembre).</p>
        <p class="small" data-xmas="apres" hidden style="margin-top:10px" data-en="From today, delivery before Christmas can't be guaranteed.">Livraison avant Noël non garantie à partir d'aujourd'hui.</p>
      </fieldset>
      <fieldset style="margin-top:18px"><legend data-en="Payment">Paiement</legend>
        <label class="check"><input type="radio" name="pay" value="card" checked> <span data-en="Bank card">Carte bancaire</span></label>
        <div class="pay-ph" data-pay="card" data-en="Mock-up: the gateway's secure card fields (Stripe or WooPayments) go here. No card data is collected in this prototype.">Maquette : ici, les champs carte sécurisés de la passerelle (Stripe ou WooPayments). Aucune donnée de carte n'est collectée dans ce prototype.</div>
        <label class="check" style="margin-top:12px"><input type="radio" name="pay" value="paypal"> <span>PayPal</span></label>
        <div class="pay-ph" data-pay="paypal" hidden data-en="Mock-up: you'll be redirected to PayPal to pay.">Maquette : tu serais redirigée vers PayPal pour payer.</div>
        <button type="button" class="linkbtn" data-reveal="codeBox" data-en="Got a code?">Un code ?</button>
        <div id="codeBox" hidden><div class="field"><label for="code" data-en="Promo code">Code promo</label><div style="display:flex;gap:8px"><input id="code" type="text" autocomplete="off"><button class="btn ghost" type="button" id="codeApply" data-en="Apply">Appliquer</button></div><p class="help" id="codeMsg" aria-live="polite"></p></div></div>
      </fieldset>
      <div class="check-wrap" style="margin-top:12px"><label class="check" for="cgv"><input type="checkbox" id="cgv" required> <span>{elh('span', "J'ai lu et j'accepte les <a class=\"link\" href=\"cgv.html\">conditions générales de vente</a>.", 'I have read and accept the <a class="link" href="cgv.html">terms and conditions of sale</a>.')}</span></label><p class="err" hidden></p></div>
      <p class="final-legal" style="margin-bottom:12px" data-en="You have 14 days from delivery to withdraw.">Tu disposes de 14 jours pour te rétracter après réception.</p>
      <button type="submit" class="btn block big" id="coSubmit" data-en="Place order with obligation to pay">Commander avec obligation de paiement</button>
      {elh('p', 'En commandant, tu t\'engages à payer. Tu as 14 jours après réception pour changer d\'avis : <a class="link" href="retractation.html">Me rétracter</a>.', 'By ordering, you agree to pay. You have 14 days from delivery to change your mind: <a class="link" href="retractation.html">Withdraw from my order</a>.', 'final-legal')}
      <p class="mock-note"><b data-en="Mock-up">Maquette</b><span data-en="No data is sent and no payment is taken. The order is simulated in your browser.">Aucune donnée n'est envoyée et aucun paiement n'est effectué. La commande est simulée dans ton navigateur.</span></p>
    </form>
    <aside id="coRecap"><div class="panel">
      <button type="button" class="co-toggle" id="coToggle" aria-expanded="false" aria-controls="coRecapBody"><span data-en="Show the summary">Afficher le récapitulatif</span> · <b id="coToggleTotal"></b></button>
      <div id="coRecapBody">
        {el('h2', 'Ton écrin', 'Your box', 'co-h')}
        <div class="shipbar" id="coShip" style="margin-bottom:6px"><span class="txt"></span><div class="bar"><i></i></div></div>
        <div id="coLines"></div>
        <div class="sum" id="coSum" style="margin-top:12px"></div>
        <p style="margin-top:12px"><a class="link" href="panier.html" data-en="Edit my box">Modifier mon écrin</a></p>
      </div>
    </div></aside>
  </div>
</div>
<section class="wrap" id="coDone" hidden tabindex="-1" aria-labelledby="cf-t" style="padding-bottom:56px">
  <div class="confirm">
    {el('p', 'Commande confirmée (maquette)', 'Order confirmed (mock-up)', 'eyebrow')}
    <h2 id="cf-t"><span data-en="Thank you">Merci</span> <span id="cfName"></span>.</h2>
    <p><span data-en="Order no.">Ta commande n°</span> <b id="cfNo"></b> <span data-en="is confirmed. Total:">est confirmée. Total :</span> <b id="cfTotal"></b>.</p>
    {el('p', 'Tu reçois un e-mail dans quelques minutes, puis un autre avec ton suivi DHL dès l\'expédition (simulé).', 'You\'ll get an email in a few minutes, then another with your DHL tracking once it ships (simulated).', 'muted')}
    <ol class="timeline">
      <li><i>1</i><span><b data-en="Prepared">Préparée</b> · <span data-en="by">d'ici le</span> <span id="cfPrep"></span></span></li>
      <li><i>2</i><span><b data-en="Shipped">Expédiée</b> · <span data-en="email with DHL tracking">e-mail avec le suivi DHL</span></span></li>
      <li><i>3</i><span><b data-en="Delivered">Livrée</b> <span id="cfDel"></span></span></li>
    </ol>
    {el('p', 'Une erreur dans l\'adresse ? Réponds à l\'e-mail de confirmation tout de suite : on peut la corriger tant que la commande n\'est pas partie en préparation.', 'Wrong address? Reply to the confirmation email straight away: we can fix it until the order goes into preparation.', 'small')}
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px"><a class="btn" href="parures.html" data-en="Keep browsing">Continuer à regarder</a><a class="btn ghost" href="retractation.html" data-en="Withdraw from my order">Me rétracter</a></div>
  </div>
</section>'''
    ld = lambda l: webpage_ld(title if l == 'fr' else title_en, desc if l == 'fr' else desc_en, '/commande/' if l == 'fr' else '/en/checkout/', cr, l, 'CheckoutPage')
    page('paiement.html', title=title, title_en=title_en, desc=desc, desc_en=desc_en, body=body, url='/commande/', url_en='/en/checkout/', ld_fr=ld('fr'), ld_en=ld('en'), index=False)

def build_404():
    cr = [('index.html', 'Accueil', 'Home'), (None, 'Page introuvable', 'Page not found')]
    title, title_en = 'Page introuvable | CHARMED PARIS', 'Page Not Found | CHARMED PARIS'
    desc, desc_en = "Cette page n'existe pas, ou plus. Retrouve nos parures et nos idées cadeaux.", "This page doesn't exist, or no longer does. Find our sets and gift ideas."
    body = f'''{crumbs(cr)}
<div class="wrap" style="padding-block:24px 64px;text-align:center">
  <p class="wm" aria-hidden="true" style="font-size:clamp(60px,12vw,120px);color:var(--grenat);justify-content:center;display:flex;margin:0 0 18px"><span class="br l"></span><span class="mid" style="font-size:.5em">404</span><span class="br r"></span></p>
  {el('h1', "Cette page n'existe pas, ou plus.", "This page doesn't exist, or no longer does.", '', style='font-size:clamp(30px,4.6vw,48px);margin-inline:auto')}
  {el('p', "L'écrin est vide ici. Les parures, elles, t'attendent.", 'This box is empty. The sets are waiting for you.', 'lead', style='margin:16px auto 26px')}
  <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap"><a class="btn" href="parures.html" data-en="See the sets">Voir les parures</a><a class="btn ghost" href="cadeaux.html" data-en="Gift ideas">Idées cadeaux</a></div>
</div>
<section class="band" style="padding-top:0" aria-labelledby="p404"><div class="wrap">{el('h2', 'Quelques parures', 'A few sets', 'h2', id='p404', style='margin-bottom:22px')}{grid(skus=['JS1AQ5', 'JS63WT', 'JSX3G6', 'JSSFYS'], cls='g4')}</div></section>'''
    ld = lambda l: webpage_ld(title if l == 'fr' else title_en, desc if l == 'fr' else desc_en, '/404/', cr, l)
    page('404.html', title=title, title_en=title_en, desc=desc, desc_en=desc_en, body=body, url='/404/', url_en='/en/404/', ld_fr=ld('fr'), ld_en=ld('en'), index=False)

# ------------------------------------------------------------------ main
if __name__ == '__main__':
    import shutil
    (SITE / 'assets/img/pieces').mkdir(parents=True, exist_ok=True)
    for pc in PIECES:
        src = next(ROOT.glob(f'branvas-photos/*/{pc["img"]}'))
        shutil.copy(src, SITE / 'assets/img/pieces' / pc['img'])
    write_catalogue()
    build_home(); build_shop(); build_univers()
    for p in PRODUCTS:
        build_product(p)
    build_cadeaux(); build_pieces(); build_static_pages(); build_legal(); build_retract(); build_cart(); build_checkout(); build_404()
    print(f'{len(PAGES_WRITTEN)} pages :', ', '.join(PAGES_WRITTEN))
