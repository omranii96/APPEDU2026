"""
kdpkit - shared production engine for the KDP children's book line.

* Fonts (SIL OFL, embedded + subset by reportlab -> KDP compliant)
* KDP print geometry: trim, bleed, spine width, safe zones, barcode zone
* Vector helpers: shapely geometry -> PDF paths, text fitting
* Stroke-alphabet renderer (solid / dashed tracing / numbered arrows)
* Full-wrap cover builder + PDF rasteriser for previews and Kindle covers
"""
import math
import os

from reportlab.lib.colors import Color, black, white
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

from . import strokes as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "fonts")

FONTS = {
    "Title": "LilitaOne-Regular.ttf",
    "Round": "Fredoka-600.ttf",
    "RoundBold": "Fredoka-700.ttf",
    "RoundReg": "Fredoka-400.ttf",
    "Read": "Andika-Regular.ttf",
    "ReadBold": "Andika-Bold.ttf",
    "Body": "Nunito-400.ttf",
    "BodyBold": "Nunito-700.ttf",
    "BodyBlack": "Nunito-900.ttf",
    "Hand": "PatrickHand-Regular.ttf",
    "Baloo": "Baloo2-800.ttf",
    "Sniglet": "Sniglet-ExtraBold.ttf",
}
_registered = False


def register_fonts():
    global _registered
    if _registered:
        return
    for name, fn in FONTS.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fn)))
    _registered = True


# --------------------------------------------------------------------------- KDP geometry
BLEED = 0.125 * inch
# Spine width per page (inches) - KDP paperback submission guidelines.
SPINE_PER_PAGE = {
    "bw_white": 0.002252,
    "bw_cream": 0.0025,
    "color_white": 0.002347,  # standard & premium colour
}
SPINE_TEXT_MIN_PAGES = 80  # KDP: spine text only from 79-80+ pages


def spine_width(pages, paper):
    return pages * SPINE_PER_PAGE[paper] * inch


def hex_color(h, a=1.0):
    h = h.lstrip("#")
    return Color(int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, alpha=a)


def new_canvas(path, w, h, title, author):
    register_fonts()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c = rl_canvas.Canvas(path, pagesize=(w, h), pageCompression=1, initialFontName="Body", initialFontSize=12)
    c.setTitle(title)
    c.setAuthor(author)
    c.setCreator("kdpkit")
    c.setProducer("kdpkit")
    return c


# --------------------------------------------------------------------------- text helpers
def fit_size(text, font, max_w, start, min_size=6):
    size = start
    while size > min_size and pdfmetrics.stringWidth(text, font, size) > max_w:
        size -= 0.5
    return size


def text_center(c, text, x, y, font, size, max_w=None, color=black):
    if max_w:
        size = fit_size(text, font, max_w, size)
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawCentredString(x, y, text)
    return size


def outlined_text(c, text, x, y, font, size, fill, outline, ow, center=True):
    """Bold sticker-style title text: thick outline under a fill."""
    w = pdfmetrics.stringWidth(text, font, size)
    x0 = x - w / 2 if center else x
    t = c.beginText(x0, y)
    t.setFont(font, size)
    c.saveState()
    c.setLineJoin(1)
    c.setLineWidth(ow)
    c.setStrokeColor(outline)
    c.setFillColor(outline)
    t.setTextRenderMode(2)
    t.textOut(text)
    c.drawText(t)
    t2 = c.beginText(x0, y)
    t2.setFont(font, size)
    t2.setTextRenderMode(0)
    c.setFillColor(fill)
    t2.textOut(text)
    c.drawText(t2)
    c.restoreState()
    return w


def wrap(text, font, size, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def paragraph(c, text, x, y, font, size, max_w, leading=1.3, color=black, align="left"):
    """Draw wrapped text with top at y. Returns y after last line."""
    c.setFillColor(color)
    c.setFont(font, size)
    yy = y - size
    for para in text.split("\n"):
        for line in wrap(para, font, size, max_w) or [""]:
            if align == "center":
                c.drawCentredString(x + max_w / 2, yy, line)
            else:
                c.drawString(x, yy, line)
            yy -= size * leading
    return yy + size * leading - size * 0.3


# --------------------------------------------------------------------------- geometry
def geom_path(c, geom):
    """shapely (Multi)Polygon / LineString -> reportlab path."""
    p = c.beginPath()

    def ring(coords, close=True):
        coords = list(coords)
        p.moveTo(*coords[0])
        for q in coords[1:]:
            p.lineTo(*q)
        if close:
            p.close()

    gt = geom.geom_type
    if gt == "Polygon":
        ring(geom.exterior.coords)
        for i in geom.interiors:
            ring(i.coords)
    elif gt in ("MultiPolygon", "GeometryCollection"):
        for g in geom.geoms:
            if g.geom_type == "Polygon":
                ring(g.exterior.coords)
                for i in g.interiors:
                    ring(i.coords)
    elif gt == "LineString":
        ring(geom.coords, close=False)
    elif gt == "MultiLineString":
        for g in geom.geoms:
            ring(g.coords, close=False)
    return p


def draw_geom(c, geom, fill=None, stroke=black, lw=2.0):
    if geom.is_empty:
        return
    c.saveState()
    c.setLineJoin(1)
    c.setLineCap(1)
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.drawPath(geom_path(c, geom), fill=1 if fill is not None else 0,
               stroke=1 if stroke is not None else 0, fillMode=0)
    c.restoreState()


def star_points(cx, cy, r_out, r_in, n=5, rot=90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def poly(c, pts, fill=None, stroke=None, lw=1, close=True):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.drawPath(p, fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0)


# --------------------------------------------------------------------------- tracing renderer
GRAY = hex_color("#9a9a9a")
LIGHT = hex_color("#c9c9c9")
GUIDE_BLUE = hex_color("#7f7f7f")
# Direction-arrow colour: red for colour interiors, dark grey for black-ink interiors
ARROW_COLOR = hex_color("#e0472b")


def guide_lines(c, x0, x1, baseline, unit, descender=True, lw=0.9):
    """Classic 3/4-line handwriting guide (top, dashed midline, baseline, descender)."""
    c.saveState()
    c.setStrokeColor(hex_color("#555555"))
    c.setLineWidth(lw * 1.2)
    c.line(x0, baseline + 2 * unit, x1, baseline + 2 * unit)
    c.line(x0, baseline, x1, baseline)
    c.setLineWidth(lw)
    c.setDash(4, 4)
    c.setStrokeColor(hex_color("#8a8a8a"))
    c.line(x0, baseline + unit, x1, baseline + unit)
    if descender:
        c.setDash(1, 3)
        c.setStrokeColor(hex_color("#b5b5b5"))
        c.line(x0, baseline - unit, x1, baseline - unit)
    c.restoreState()


def _stroke_path(c, pts, x, y, unit):
    p = c.beginPath()
    p.moveTo(x + pts[0][0] * unit, y + pts[0][1] * unit)
    for q in pts[1:]:
        p.lineTo(x + q[0] * unit, y + q[1] * unit)
    return p


def draw_strokes(c, strokes, x, y, unit, style="solid", lw=None, color=black,
                 numbered=False, arrows=False, num_font="RoundBold"):
    """Render one glyph's strokes. style: solid | dashed | dotted | ghost."""
    lw = lw or max(1.2, unit * 0.16)
    c.saveState()
    c.setLineCap(1)
    c.setLineJoin(1)
    for i, s in enumerate(strokes):
        if len(s) == 1:  # a dot
            px, py = x + s[0][0] * unit, y + s[0][1] * unit
            r = lw * 0.75 if style != "solid" else lw * 0.7
            c.setFillColor(color if style == "solid" else GRAY)
            if style in ("dashed", "dotted"):
                c.setStrokeColor(GRAY)
                c.setLineWidth(lw * 0.35)
                c.circle(px, py, r * 1.2, stroke=1, fill=0)
            else:
                c.circle(px, py, r, stroke=0, fill=1)
            continue
        c.setStrokeColor(color)
        c.setLineWidth(lw)
        if style == "dashed":
            c.setStrokeColor(GRAY)
            c.setDash(lw * 1.5, lw * 1.6)
        elif style == "dotted":
            c.setStrokeColor(GRAY)
            c.setDash(0.1, lw * 2.0)
        elif style == "ghost":
            c.setStrokeColor(LIGHT)
            c.setDash()
        else:
            c.setDash()
        c.drawPath(_stroke_path(c, s, x, y, unit), stroke=1, fill=0)
        c.setDash()
        if arrows:
            _arrow_along(c, s, x, y, unit, lw)
    if numbered:
        placed = []
        r = max(5, unit * 0.2)
        for i, s in enumerate(strokes):
            sx, sy = x + s[0][0] * unit, y + s[0][1] * unit
            # several strokes starting at the same point: fan the badges out
            k = 0
            while any(math.dist((sx, sy), q) < 2.05 * r for q in placed) and k < 6:
                if len(s) > 1:
                    dx, dy = s[1][0] - s[0][0], s[1][1] - s[0][1]
                    d = math.hypot(dx, dy) or 1
                    # slide the badge forward along its own stroke direction
                    sx, sy = sx + dx / d * 2.1 * r, sy + dy / d * 2.1 * r
                else:
                    sx += 2.1 * r
                k += 1
            placed.append((sx, sy))
            c.setFillColor(hex_color("#111111"))
            c.circle(sx, sy, r, stroke=0, fill=1)
            c.setFillColor(white)
            c.setFont(num_font, r * 1.35)
            c.drawCentredString(sx, sy - r * 0.47, str(i + 1))
    c.restoreState()


def _arrow_along(c, pts, x, y, unit, lw):
    """Small direction arrow ~40% along a stroke, offset to the side."""
    if len(pts) < 2:
        return
    seg = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    lens = [math.dist(a, b) for a, b in seg]
    tot = sum(lens)
    if tot * unit < 22:
        return
    target = tot * 0.45
    acc = 0
    for (a, b), ln in zip(seg, lens):
        if acc + ln >= target and ln > 0:
            t = (target - acc) / ln
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            dx, dy = (b[0] - a[0]) / ln, (b[1] - a[1]) / ln
            break
        acc += ln
    else:
        return
    off = 0.32
    nx, ny = -dy, dx  # left normal
    cx, cy = x + (px + nx * off) * unit, y + (py + ny * off) * unit
    L = unit * 0.38
    c.saveState()
    c.setStrokeColor(ARROW_COLOR)
    c.setFillColor(ARROW_COLOR)
    c.setLineWidth(max(1.0, lw * 0.4))
    c.setDash()
    tx, ty = cx + dx * L / 2, cy + dy * L / 2
    c.line(cx - dx * L / 2, cy - dy * L / 2, tx, ty)
    h = L * 0.45
    p = c.beginPath()
    p.moveTo(tx + dx * h * 0.3, ty + dy * h * 0.3)
    p.lineTo(tx - dx * h + nx * h * 0.55, ty - dy * h + ny * h * 0.55)
    p.lineTo(tx - dx * h - nx * h * 0.55, ty - dy * h - ny * h * 0.55)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def draw_text_strokes(c, text, x, baseline, unit, style="dashed", lw=None, color=black,
                      numbered=False, arrows=False, gap=S.ADVANCE_GAP):
    for ch, off, g in S.layout(text, gap):
        draw_strokes(c, g, x + off * unit, baseline, unit, style, lw, color, numbered, arrows)
    return S.text_width(text, gap) * unit


# --------------------------------------------------------------------------- covers
def cover_dims(trim_w, trim_h, pages, paper):
    sp = spine_width(pages, paper)
    W = 2 * BLEED + 2 * trim_w + sp
    H = trim_h + 2 * BLEED
    return W, H, sp


def build_cover(path, trim_w, trim_h, pages, paper, draw_back, draw_spine, draw_front,
                title, author, background=None):
    """Full-wrap paperback cover. Callbacks get (c, x, y, w, h) of their TRIM area;
    art should extend BLEED beyond outer edges (callbacks may paint the full sheet
    via `background`)."""
    W, H, sp = cover_dims(trim_w, trim_h, pages, paper)
    c = new_canvas(path, W, H, title, author)
    if background:
        background(c, W, H)
    back = (BLEED, BLEED, trim_w, trim_h)
    spine = (BLEED + trim_w, BLEED, sp, trim_h)
    front = (BLEED + trim_w + sp, BLEED, trim_w, trim_h)
    draw_back(c, *back)
    draw_spine(c, *spine)
    draw_front(c, *front)
    c.showPage()
    c.save()
    return {"width_in": W / inch, "height_in": H / inch, "spine_in": sp / inch,
            "front": front, "back": back, "spine": spine}


BARCODE_W, BARCODE_H = 2.0 * inch, 1.2 * inch


def barcode_zone(back_x, back_y, back_w):
    """KDP auto-places its barcode bottom-right of the back cover (2" x 1.2",
    ~0.25" from the spine & bottom trim). Keep this area free of content."""
    return (back_x + back_w - 0.25 * inch - BARCODE_W, back_y + 0.25 * inch, BARCODE_W, BARCODE_H)


# --------------------------------------------------------------------------- rendering / QA
def render_pages(pdf_path, out_dir, scale=1.0, pages=None, prefix="p", fmt="png"):
    import pypdfium2 as pdfium
    os.makedirs(out_dir, exist_ok=True)
    pdf = pdfium.PdfDocument(pdf_path)
    idx = range(len(pdf)) if pages is None else pages
    paths = []
    for i in idx:
        img = pdf[i].render(scale=scale).to_pil().convert("RGB")
        p = os.path.join(out_dir, f"{prefix}{i + 1:03d}.{fmt}")
        img.save(p, quality=92)
        paths.append(p)
    return paths


def contact_sheet(pdf_path, out_png, cols=8, thumb_w=220, pages=None, label=True):
    import pypdfium2 as pdfium
    from PIL import Image, ImageDraw
    pdf = pdfium.PdfDocument(pdf_path)
    idx = list(range(len(pdf))) if pages is None else list(pages)
    thumbs = []
    for i in idx:
        pg = pdf[i]
        sc = thumb_w / pg.get_width()
        im = pg.render(scale=sc).to_pil().convert("RGB")
        thumbs.append((i, im))
    th = max(t.height for _, t in thumbs)
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * (thumb_w + 10) + 10, rows * (th + 26) + 10), (90, 90, 90))
    d = ImageDraw.Draw(sheet)
    for k, (i, t) in enumerate(thumbs):
        x = 10 + (k % cols) * (thumb_w + 10)
        y = 10 + (k // cols) * (th + 26)
        sheet.paste(t, (x, y))
        if label:
            d.text((x + 2, y + th + 4), f"p{i + 1}", fill=(255, 255, 255))
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    sheet.save(out_png)
    return out_png


def pdf_report(pdf_path):
    """Basic KDP preflight: page count, page sizes, fonts embedded."""
    from pypdf import PdfReader
    r = PdfReader(pdf_path)
    sizes = {(round(float(p.mediabox.width) / 72, 3), round(float(p.mediabox.height) / 72, 3)) for p in r.pages}
    fonts, unembedded = set(), set()
    for p in r.pages:
        res = p.get("/Resources") or {}
        fd = res.get("/Font") or {}
        for _, f in fd.items():
            f = f.get_object()
            name = f.get("/BaseFont")
            fonts.add(str(name))
            desc = f.get("/FontDescriptor")
            if f.get("/Subtype") == "/Type0":
                desc = f["/DescendantFonts"][0].get_object().get("/FontDescriptor")
            if desc is None or not any(k in desc.get_object() for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                unembedded.add(str(name))
    return {"pages": len(r.pages), "sizes_in": sorted(sizes), "fonts": sorted(fonts),
            "unembedded": sorted(unembedded), "bytes": os.path.getsize(pdf_path)}
