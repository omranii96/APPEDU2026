"""Genere les logos CHARMED PARIS en SVG (lettres vectorisees depuis Bodoni Moda / Jost, OFL)."""
# Usage : pip install fonttools ; python3 generer-logos.py ..   (regenere tous les SVG dans logos/)
# Polices : Bodoni Moda et Jost, SIL OFL 1.1 (voir fonts/OFL.txt). Les SVG produits ne contiennent que des contours.
import json, os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'fonts')
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

_cache = {}
def font(fn, loc):
    k = (fn, tuple(sorted(loc.items())))
    if k not in _cache:
        _cache[k] = instancer.instantiateVariableFont(TTFont(os.path.join(FONTS, fn)), loc)
    return _cache[k]

def fmt(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith('.0') else s

class RoundPen(SVGPathPen):
    def __init__(self, gs):
        super().__init__(gs, ntos=fmt)

def text_paths(f, text, size, x0, baseline, tracking_em):
    """Return (d, ink_bounds, advance_end). size = em size in logo units; y-down coordinates."""
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    s = size / upm
    x = x0; ds = []; bx = [1e9, 1e9, -1e9, -1e9]
    for i, ch in enumerate(text):
        g = cmap[ord(ch)]
        pen = RoundPen(gs)
        tp = TransformPen(pen, (s, 0, 0, -s, x, baseline))
        gs[g].draw(tp)
        ds.append(pen.getCommands())
        bp = BoundsPen(gs); gs[g].draw(bp)
        if bp.bounds:
            a, b, c, d = bp.bounds
            bx = [min(bx[0], x + a*s), min(bx[1], baseline - d*s), max(bx[2], x + c*s), max(bx[3], baseline - b*s)]
        x += gs[g].width * s
        if i < len(text) - 1:
            x += tracking_em * size
    return ' '.join(ds), bx, x

def glyph_lsb_rsb(f, ch, size):
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    g = cmap[ord(ch)]; bp = BoundsPen(gs); gs[g].draw(bp)
    return bp.bounds[0]*size/upm, (gs[g].width - bp.bounds[2])*size/upm

def bracket(x, y, w, h, T, t, side):
    """Parenthese-ecrin : epais a l'exterieur (T), fin en haut/bas (t), ouvert vers l'interieur.
    side='l' -> ouverture a droite (le C). side='r' -> miroir (le D)."""
    r = min(h/2, w*0.92)
    rx, ry = r - T, r - t
    if side == 'l':
        X = lambda u: x + u
    else:
        X = lambda u: x + w - u
    sweep_o = 0 if side == 'l' else 1
    sweep_i = 1 if side == 'l' else 0
    p = [f"M{fmt(X(w))} {fmt(y)}", f"H{fmt(X(r))}",
         f"A{fmt(r)} {fmt(r)} 0 0 {sweep_o} {fmt(X(0))} {fmt(y+r)}",
         f"V{fmt(y+h-r)}",
         f"A{fmt(r)} {fmt(r)} 0 0 {sweep_o} {fmt(X(r))} {fmt(y+h)}",
         f"H{fmt(X(w))}", f"V{fmt(y+h-t)}", f"H{fmt(X(r))}",
         f"A{fmt(rx)} {fmt(ry)} 0 0 {sweep_i} {fmt(X(T))} {fmt(y+h-r)}",
         f"V{fmt(y+r)}",
         f"A{fmt(rx)} {fmt(ry)} 0 0 {sweep_i} {fmt(X(r))} {fmt(y+t)}",
         f"H{fmt(X(w))}Z"]
    return ''.join(p)

def gem(cx, cy, w, h):
    return f"M{fmt(cx)} {fmt(cy-h/2)}L{fmt(cx+w/2)} {fmt(cy)}L{fmt(cx)} {fmt(cy+h/2)}L{fmt(cx-w/2)} {fmt(cy)}Z"

MASTERS = {
    # principal : ecran et impression couleur >= 40 mm
    'principal': dict(opsz=18, wght=500, jost=500, T=225, t=44),
    # impression : dorure a chaud Branvas, petites tailles, tampons
    'impression': dict(opsz=6, wght=600, jost=600, T=262, t=80),
}
CAP = 1500  # hauteur de capitale Bodoni Moda pour une taille d'em de 2000
EM = 2000

def wordmark(m):
    M = MASTERS[m]
    bf = font('BodoniModa[opsz,wght].ttf', {'opsz': M['opsz'], 'wght': M['wght']})
    over = 34
    bh = CAP + 2*over; bw = 1000
    gap = 300  # pointe de la parenthese -> encre de la lettre
    lsbH, _ = glyph_lsb_rsb(bf, 'H', EM)
    _, rsbE = glyph_lsb_rsb(bf, 'E', EM)
    x_letters = bw + gap - lsbH
    d_letters, bx, xend = text_paths(bf, 'HARME', EM, x_letters, CAP, 0.16)
    xr = bx[2] + gap
    parts = [
        ('brackets', bracket(0, -over, bw, bh, M['T'], M['t'], 'l')),
        ('letters', d_letters),
        ('brackets', bracket(xr, -over, bw, bh, M['T'], M['t'], 'r')),
    ]
    width = xr + bw
    return parts, dict(width=width, top=-over, bottom=CAP+over, inner=(bx[0], bx[2]))

def paris(m, cap_h, tracking):
    M = MASTERS[m]
    jf = font('Jost[wght].ttf', {'wght': M['jost']})
    size = cap_h / 0.7
    d, bx, _ = text_paths(jf, 'PARIS', size, 0, 0, tracking)
    return d, bx

def translate_d(d, dx, dy):
    # re-render instead of parsing: helper wraps in group transform
    return d

def lockup_stacked(m):
    parts, g = wordmark(m)
    capP = CAP * (0.30 if m == 'principal' else 0.34)
    d, bx = paris(m, capP, 0.80 if m == 'principal' else 0.62)
    pw = bx[2] - bx[0]
    cx = (g['inner'][0] + g['inner'][1]) / 2
    dx = cx - pw/2 - bx[0]
    top = g['bottom'] + (CAP * 0.36)
    dy = top + capP
    groups = [(r, p, None) for r, p in parts] + [('paris', d, (dx, dy))]
    box = (0, g['top'], g['width'], dy)
    return groups, box

def lockup_horizontal(m):
    parts, g = wordmark(m)
    M = MASTERS[m]
    capP = CAP * (0.36 if m == 'principal' else 0.40)
    d, bx = paris(m, capP, 0.55 if m == 'principal' else 0.45)
    pw = bx[2] - bx[0]
    gap = 520
    rule_x = g['width'] + gap
    rule_w = max(M['t'], 44) * 1.0
    rule_h = CAP * 0.9
    rule_y = (CAP - rule_h) / 2
    rule = f"M{fmt(rule_x)} {fmt(rule_y)}h{fmt(rule_w)}v{fmt(rule_h)}h{fmt(-rule_w)}Z"
    px = rule_x + rule_w + gap
    dx = px - bx[0]
    dy = CAP/2 + capP/2
    groups = [(r, p, None) for r, p in parts] + [('rule', rule, None), ('paris', d, (dx, dy))]
    box = (0, g['top'], px + pw, g['bottom'])
    return groups, box

def monogram(m):
    M = MASTERS[m]
    s = 1000
    bh = 1000; bw = 560
    T = 150 if m == 'principal' else 170
    t = 34 if m == 'principal' else 60
    inner_gap = 360
    total = 2*bw + inner_gap
    x0 = (s - total)/2 + 0
    groups = [
        ('brackets', bracket(0, 0, bw, bh, T, t, 'l'), None),
        ('gem', gem(bw + inner_gap/2, bh/2, 210, 300), None),
        ('brackets', bracket(bw + inner_gap, 0, bw, bh, T, t, 'r'), None),
    ]
    return groups, (0, 0, total, bh)

def favicon_groups():
    # icone app : carre velours, ecrin or epaissi pour 16-32 px
    s = 512
    bw, bh = 150, 300
    gapc = 92
    total = 2*bw + gapc
    x0 = (s - total)/2; y0 = (s - bh)/2
    return [
        ('bg', f"M0 0H{s}V{s}H0Z", None),
        ('brackets', bracket(x0, y0, bw, bh, 58, 22, 'l'), None),
        ('gem', gem(s/2, s/2, 66, 96), None),
        ('brackets', bracket(x0 + bw + gapc, y0, bw, bh, 58, 22, 'r'), None),
    ], (0, 0, s, s)

PAL = dict(velours='#1A1015', encre='#1A1015', grenat='#7A1F3A', or_='#A9813F', or_clair='#E9CB8F',
           porcelaine='#F4F2F5', clair='#F2E9EC', blanc='#FFFFFF', noir='#000000')

def colors(variant):
    if variant == 'encre':
        return dict(letters=PAL['encre'], brackets=PAL['encre'], paris=PAL['encre'], gem=PAL['encre'], rule=PAL['encre'])
    if variant == 'grenat':
        return dict(letters=PAL['encre'], brackets=PAL['grenat'], paris=PAL['grenat'], gem=PAL['grenat'], rule=PAL['grenat'])
    if variant == 'or':
        return dict(letters=PAL['or_clair'], brackets=PAL['or_clair'], paris=PAL['or_clair'], gem=PAL['or_clair'], rule=PAL['or_clair'])
    if variant == 'bicolore':
        return dict(letters=PAL['clair'], brackets=PAL['or_clair'], paris=PAL['or_clair'], gem=PAL['or_clair'], rule=PAL['or_clair'])
    if variant == 'blanc':
        return dict(letters=PAL['blanc'], brackets=PAL['blanc'], paris=PAL['blanc'], gem=PAL['blanc'], rule=PAL['blanc'])
    if variant == 'noir':
        return dict(letters=PAL['noir'], brackets=PAL['noir'], paris=PAL['noir'], gem=PAL['noir'], rule=PAL['noir'])
    if variant == 'current':
        return None
    raise ValueError(variant)

def svg(groups, box, variant, title, bg=None, pad=0):
    x0, y0, x1, y1 = box
    x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    w, h = x1 - x0, y1 - y0
    col = colors(variant)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fmt(x0)} {fmt(y0)} {fmt(w)} {fmt(h)}" role="img" aria-label="{title}">',
           f'<title>{title}</title>']
    if bg:
        out.append(f'<rect x="{fmt(x0)}" y="{fmt(y0)}" width="{fmt(w)}" height="{fmt(h)}" fill="{bg}"/>')
    # regroupe par couleur
    for role, d, tr in groups:
        if role == 'bg':
            out.append(f'<path fill="{PAL["velours"]}" d="{d}"/>'); continue
        fill = col[role] if col else 'currentColor'
        attr = f' transform="translate({fmt(tr[0])} {fmt(tr[1])})"' if tr else ''
        out.append(f'<path fill="{fill}"{attr} d="{d}"/>')
    out.append('</svg>')
    return '\n'.join(out) + '\n'

def symbol(groups, box, sid, two_tone=True):
    x0, y0, x1, y1 = box
    out = [f'<symbol id="{sid}" viewBox="{fmt(x0)} {fmt(y0)} {fmt(x1-x0)} {fmt(y1-y0)}">']
    for role, d, tr in groups:
        if role == 'bg': continue
        fill = 'var(--lg-accent, currentColor)' if role in ('brackets', 'gem') and two_tone else 'currentColor'
        if role in ('paris', 'rule') and two_tone: fill = 'var(--lg-sub, currentColor)'
        attr = f' transform="translate({fmt(tr[0])} {fmt(tr[1])})"' if tr else ''
        out.append(f'<path style="fill:{fill}"{attr} d="{d}"/>')
    out.append('</symbol>')
    return ''.join(out)

L = 'CHARMED PARIS'
files = {}
st, stb = lockup_stacked('principal')
hz, hzb = lockup_horizontal('principal')
mo, mob = monogram('principal')
st_i, stb_i = lockup_stacked('impression')
hz_i, hzb_i = lockup_horizontal('impression')
mo_i, mob_i = monogram('impression')
wm, wmg = wordmark('principal'); wmb = (0, wmg['top'], wmg['width'], wmg['bottom'])
wm = [(r, p, None) for r, p in wm]

for v in ['encre', 'grenat', 'or', 'bicolore', 'blanc']:
    files[f'principal/charmed-paris-principal-{v}.svg'] = svg(st, stb, v, L)
    files[f'horizontal/charmed-paris-horizontal-{v}.svg'] = svg(hz, hzb, v, L)
    files[f'monogramme/charmed-monogramme-{v}.svg'] = svg(mo, mob, v, 'CHARMED PARIS monogramme')
files['principal/charmed-paris-principal-or-sur-velours.svg'] = svg(st, stb, 'or', L, bg=PAL['velours'], pad=700)
files['monogramme/charmed-monogramme-or-sur-velours.svg'] = svg(mo, (-360, -600, 1840, 1600), 'or', 'CHARMED PARIS monogramme', bg=PAL['velours'])
files['principal/charmed-wordmark-seul-encre.svg'] = svg(wm, wmb, 'encre', 'CHARMED')
# impression 1 couleur (noir pur) : master renforce
files['impression/charmed-paris-principal-noir-impression.svg'] = svg(st_i, stb_i, 'noir', L)
files['impression/charmed-paris-horizontal-noir-impression.svg'] = svg(hz_i, hzb_i, 'noir', L)
files['impression/charmed-monogramme-noir-impression.svg'] = svg(mo_i, mob_i, 'noir', 'CHARMED PARIS monogramme')
files['impression/charmed-paris-principal-blanc-impression.svg'] = svg(st_i, stb_i, 'blanc', L)
fg, fgb = favicon_groups()
fav = svg(fg, fgb, 'or', 'CHARMED PARIS')
files['favicon/favicon.svg'] = fav

for k, v in files.items():
    p = os.path.join(OUT, k); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(v)

sprite = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
          + symbol(st, stb, 'lg-stack') + symbol(hz, hzb, 'lg-horiz') + symbol(mo, mob, 'lg-mono')
          + symbol(st_i, stb_i, 'lg-stack-print', False) + symbol(wm, wmb, 'lg-wm') + '</svg>')
open(os.path.join(HERE, 'sprite.svg'), 'w').write(sprite)

# metriques pour la charte (tailles minimales)
def thin(m):
    M = MASTERS[m]
    hair = {18: 26, 6: 74}[M['opsz']]
    return min(hair, M['t'])
info = {}
for name, box, m in [('principal', stb, 'principal'), ('horizontal', hzb, 'principal'),
                     ('principal-impression', stb_i, 'impression'), ('horizontal-impression', hzb_i, 'impression')]:
    w = box[2]-box[0]; h = box[3]-box[1]
    info[name] = dict(w=round(w), h=round(h), ratio=round(w/h, 3), thinnest=thin(m),
                      min_width_mm_for_0_3mm=round(0.3*w/thin(m), 1), cap=CAP)
info['monogramme'] = dict(w=round(mob[2]), h=round(mob[3]))
info['monogramme-impression'] = dict(w=round(mob_i[2]), h=round(mob_i[3]), thinnest=60, min_width_mm_for_0_3mm=round(0.3*mob_i[2]/60, 1))
json.dump(info, open(os.path.join(HERE, 'metrics.json'), 'w'), indent=1)
print(json.dumps(info, indent=1))
print('\n'.join(sorted(files)))

# logo decompose pour l'animation de la charte
x0,y0,x1,y1 = stb
hero = [f'<svg class="hero-logo" viewBox="{fmt(x0)} {fmt(y0)} {fmt(x1-x0)} {fmt(y1-y0)}" role="img" aria-label="CHARMED PARIS">']
for role, d, tr in st:
    cls = {'brackets':'bk','letters':'mid','paris':'paris'}[role]
    if role == 'brackets':
        cls += ' bl' if 'bl-done' not in globals() else ' br'
        globals()['bl-done'] = True
    attr = f' transform="translate({fmt(tr[0])} {fmt(tr[1])})"' if tr else ''
    hero.append(f'<g class="{cls}"><path{attr} d="{d}"/></g>')
hero.append('</svg>')
open(os.path.join(HERE, 'hero.svg'), 'w').write(''.join(hero))
