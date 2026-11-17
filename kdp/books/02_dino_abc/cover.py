"""Book 2 full-wrap cover (8.5x11, 82 pp, black ink/white paper) + front JPG. Same series look as Book 1."""
import os
import sys

from reportlab.lib.colors import white
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from shapely.geometry import Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
KDP = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, KDP)

from lib import art as A  # noqa: E402
from lib import kdpkit as K  # noqa: E402
from lib import strokes as S  # noqa: E402
from lib.coverkit import INK, ORANGE, YELLOW, badge, hills, scene  # noqa: E402

PAGES = 82
TRIM_W, TRIM_H = 8.5 * inch, 11 * inch
SAFE = 0.5 * inch

CTX = {
    "en": {
        "series": "DINO QUEST", "kind": "ABC LETTER TRACING", "ages": "for Preschoolers Ages 3-5",
        "badge": ["A-Z", "LETTERS", "+ 0-10"],
        "bar": "Stroke-order arrows • Trace • Write • Color • Numbers 0-10",
        "back_h": "Learn to write the right way!",
        "back_p": "Most tracing books only show dotted letters. Dino Quest ABC shows little hands exactly WHERE "
                  "to start and WHICH WAY to go - with numbered strokes and arrows, just like a teacher would.",
        "bullets": ["8 warm-up pages: lines, curves, circles, zigzags & loops",
                    "26 letter spreads: uppercase + lowercase, step by step",
                    "A picture to color + a word to trace for every letter",
                    "“Find the letter” games build letter recognition",
                    "Numbers 0-10 with counting & number words",
                    "ABC review, matching, ABC dot-to-dot & name practice",
                    "Star chart + Super Writer certificate"],
        "foot": "Big 8.5 x 11 pages, made for little hands.",
        "spine": "DINO QUEST ABC  •  Letter Tracing Ages 3-5",
        "pub": "Dino Quest Kids Press",
    },
    "fr": {
        "series": "DINO QUEST", "kind": "J'APPRENDS À ÉCRIRE", "ages": "les lettres et les chiffres • dès 3 ans",
        "badge": ["A-Z", "LETTRES", "+ 0-10"],
        "bar": "Flèches & ordre des traits • Je repasse • J'écris • Je colorie",
        "back_h": "Bien écrire dès le début !",
        "back_p": "La plupart des cahiers ne montrent que des pointillés. Dino Quest ABC montre aux petites "
                  "mains OÙ commencer et DANS QUEL SENS tracer, avec des traits numérotés et des flèches, "
                  "comme le ferait la maîtresse.",
        "bullets": ["8 pages d'échauffement : traits, ponts, ronds, zigzags, boucles",
                    "26 doubles pages : majuscules + minuscules, pas à pas",
                    "Un dessin à colorier + un mot à écrire par lettre",
                    "Jeux « trouve la lettre » pour bien les reconnaître",
                    "Les nombres de 0 à 10, à compter et à écrire",
                    "Révisions, relier majuscules/minuscules, points ABC",
                    "Tableau d'étoiles + diplôme de Super Écrivain"],
        "foot": "Grand format 21,6 x 27,9 cm, pensé pour les petites mains.",
        "spine": "DINO QUEST ABC  •  J'apprends à écrire",
        "pub": "Dino Quest Kids Press",
    },
}


def pencil(c, x, y, length, width, angle):
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    w2 = width / 2
    c.setLineWidth(3)
    c.setStrokeColor(INK)
    c.setFillColor(K.hex_color("#ffd23f"))
    c.rect(0, -w2, length * 0.78, width, stroke=1, fill=1)
    c.setFillColor(K.hex_color("#ff8fab"))
    c.roundRect(-length * 0.1, -w2, length * 0.12, width, width * 0.25, stroke=1, fill=1)
    c.setFillColor(K.hex_color("#b9b9b9"))
    c.rect(0, -w2, length * 0.05, width, stroke=1, fill=1)
    K.poly(c, [(length * 0.78, -w2), (length, 0), (length * 0.78, w2)], fill=K.hex_color("#f4d7a8"), stroke=INK, lw=3)
    K.poly(c, [(length * 0.93, -w2 * 0.32), (length, 0), (length * 0.93, w2 * 0.32)], fill=INK, stroke=INK, lw=1)
    c.setLineWidth(2)
    c.line(0, -w2 / 3, length * 0.78, -w2 / 3)
    c.line(0, w2 / 3, length * 0.78, w2 / 3)
    c.restoreState()


def block(c, x, y, s, letter, color, rot=0):
    c.saveState()
    c.translate(x + s / 2, y + s / 2)
    c.rotate(rot)
    c.setFillColor(K.hex_color(color))
    c.setStrokeColor(INK)
    c.setLineWidth(3.5)
    c.roundRect(-s / 2, -s / 2, s, s, s * 0.14, stroke=1, fill=1)
    c.setLineWidth(2)
    c.roundRect(-s / 2 + s * 0.08, -s / 2 + s * 0.08, s * 0.84, s * 0.84, s * 0.1, stroke=1, fill=0)
    K.outlined_text(c, letter, 0, -s * 0.27, "Title", s * 0.72, white, INK, 5)
    K.outlined_text(c, letter, 0, -s * 0.27, "Title", s * 0.72, white, white, 0.1)
    c.restoreState()


def front(c, x, y, w, h, t):
    bx, by, bw, bh = x - K.BLEED, y - K.BLEED, w + K.BLEED, h + 2 * K.BLEED
    scene(c, bx, by, bw, bh)
    c.saveState()
    p = c.beginPath()
    p.rect(bx, by, bw, bh)
    c.clipPath(p, stroke=0, fill=0)
    A.place(c, A.cloud(), x + w * 0.05, y + h * 0.56, w * 0.22, w * 0.1, mode="color", lw=2)
    A.place(c, A.sun(), x + w * 0.76, y + h * 0.55, w * 0.16, w * 0.16, mode="color", palette="orange", lw=2.2)
    hills(c, bx, by, bw, bh)
    block(c, x + w * 0.08, y + h * 0.13, w * 0.24, "A", "#e2574c", -6)
    block(c, x + w * 0.37, y + h * 0.11, w * 0.22, "B", "#2f7fd8", 4)
    block(c, x + w * 0.25, y + h * 0.3, w * 0.19, "C", "#5cbf4f", -3)
    pencil(c, x + w * 0.4, y + h * 0.47, w * 0.4, w * 0.065, 12)
    A.place(c, A.trex(), x + w * 0.52, y + h * 0.12, w * 0.46, h * 0.36, mode="color", palette="green", lw=3.2, flip=True)
    A.place(c, A.baby_egg(), x + w * 0.62, y + h * 0.06, w * 0.18, h * 0.13, mode="color", palette="yellow", lw=2.4)
    c.restoreState()
    # writing demo: the letter "a" with numbered strokes on guide lines (the USP, shown on the cover)
    gx, gy, u = x + w * 0.05, y + h * 0.47, 0.42 * inch
    c.setFillColor(K.hex_color("#ffffff", 0.9))
    c.setStrokeColor(INK)
    c.setLineWidth(2.5)
    c.roundRect(gx, gy - 0.25 * inch, 2.2 * inch, 1.15 * inch, 0.15 * inch, stroke=1, fill=1)
    K.guide_lines(c, gx + 0.1 * inch, gx + 2.1 * inch, gy + 0.05 * inch, u * 0.9, descender=False)
    old = K.ARROW_COLOR
    K.ARROW_COLOR = K.hex_color("#e0472b")
    K.draw_strokes(c, S.layout("A")[0][2], gx + 0.25 * inch, gy + 0.05 * inch, u * 0.9, "solid",
                   lw=4, numbered=True, arrows=True)
    K.draw_strokes(c, S.layout("a")[0][2], gx + 1.35 * inch, gy + 0.05 * inch, u * 0.9, "solid", lw=4, numbered=True, arrows=True)
    K.ARROW_COLOR = old
    cx = x + w / 2
    tsize = K.fit_size(t["series"], "Title", w - 2 * SAFE - 0.3 * inch, 118)
    ty = y + h - SAFE - tsize * 0.85
    K.outlined_text(c, t["series"], cx, ty, "Title", tsize, white, INK, 16)
    K.outlined_text(c, t["series"], cx, ty, "Title", tsize, ORANGE, white, 6)
    K.outlined_text(c, t["series"], cx, ty, "Title", tsize, ORANGE, ORANGE, 0.1)
    ry = ty - 0.95 * inch
    rw = w - 2 * SAFE
    c.setFillColor(K.hex_color("#e2574c"))
    c.setStrokeColor(INK)
    c.setLineWidth(3)
    c.roundRect(x + SAFE, ry, rw, 0.78 * inch, 0.39 * inch, stroke=1, fill=1)
    ks = K.fit_size(t["kind"], "Title", rw - 0.5 * inch, 46)
    K.outlined_text(c, t["kind"], cx, ry + 0.2 * inch, "Title", ks, white, INK, 5)
    K.outlined_text(c, t["kind"], cx, ry + 0.2 * inch, "Title", ks, white, white, 0.1)
    asz = K.fit_size(t["ages"], "RoundBold", rw, 30)
    K.outlined_text(c, t["ages"], cx, ry - 0.48 * inch, "RoundBold", asz, INK, white, 7)
    K.outlined_text(c, t["ages"], cx, ry - 0.48 * inch, "RoundBold", asz, INK, INK, 0.1)
    badge(c, x + w - SAFE - 0.85 * inch, ry - 1.4 * inch, 0.85 * inch, t["badge"])
    c.setFillColor(K.hex_color("#ffffff", 0.92))
    c.setStrokeColor(INK)
    c.setLineWidth(2.5)
    c.roundRect(x + SAFE - 0.15 * inch, y + SAFE - 0.1 * inch, w - 2 * SAFE + 0.3 * inch, 0.62 * inch, 0.3 * inch, stroke=1, fill=1)
    K.text_center(c, t["bar"], cx, y + SAFE + 0.1 * inch, "RoundBold", 17, w - 2 * SAFE - 0.2 * inch, INK)


def back(c, x, y, w, h, t, thumbs):
    bx, by, bw, bh = x - K.BLEED, y - K.BLEED, w + K.BLEED, h + 2 * K.BLEED
    c.setFillColor(K.hex_color("#fff6d6"))
    c.rect(bx, by, bw, bh, stroke=0, fill=1)
    c.saveState()
    p = c.beginPath()
    p.rect(bx, by, bw, bh)
    c.clipPath(p, stroke=0, fill=0)
    hills(c, bx, by, bw, bh * 0.55)
    c.restoreState()
    L, R = x + SAFE, x + w - SAFE
    K.text_center(c, t["back_h"], (L + R) / 2, y + h - SAFE - 0.45 * inch, "Title", 38, R - L, INK)
    yy = K.paragraph(c, t["back_p"], L, y + h - SAFE - 0.75 * inch, "BodyBold", 13.5, R - L, 1.35, INK, align="center")
    tw = (R - L - 0.3 * inch) / 4
    th = tw * 11 / 8.5
    ty = yy - th - 0.2 * inch
    for i, img in enumerate(thumbs):
        tx = L + i * (tw + 0.1 * inch)
        c.saveState()
        c.translate(tx + tw / 2, ty + th / 2)
        c.rotate([-3, 2, -2, 3][i])
        c.drawImage(ImageReader(img), -tw / 2, -th / 2, tw, th)
        c.setStrokeColor(INK)
        c.setLineWidth(2)
        c.rect(-tw / 2, -th / 2, tw, th, stroke=1, fill=0)
        c.restoreState()
    yy = ty - 0.42 * inch
    for b in t["bullets"]:
        A.place(c, A.footprint(), L + 0.2 * inch, yy - 0.24 * inch, 0.3 * inch, 0.3 * inch, mode="color", palette="orange", lw=1.2)
        c.setFillColor(INK)
        c.setFont("BodyBold", K.fit_size(b, "BodyBold", R - L - 0.8 * inch, 15))
        c.drawString(L + 0.65 * inch, yy - 0.17 * inch, b)
        yy -= 0.36 * inch
    zx, zy, zw, zh = K.barcode_zone(x, y, w)
    A.place(c, A.stegosaurus(), L, y + SAFE + 0.4 * inch, 2.2 * inch, 1.2 * inch, mode="color", palette="blue", lw=2.2)
    K.paragraph(c, t["foot"], L + 2.35 * inch, y + SAFE + 1.35 * inch, "Title", 16, zx - (L + 2.35 * inch) - 0.2 * inch, 1.15, INK)
    c.setFont("RoundBold", 11)
    c.setFillColor(INK)
    c.drawString(L, y + SAFE, t["pub"])
    c.setFillColor(white)
    c.rect(zx, zy, zw, zh, stroke=0, fill=1)


def spine(c, x, y, w, h, t):
    c.setFillColor(K.hex_color("#e2574c"))
    c.rect(x - 0.01 * inch, y - K.BLEED, w + 0.02 * inch, h + 2 * K.BLEED, stroke=0, fill=1)
    if PAGES >= K.SPINE_TEXT_MIN_PAGES:
        size = min(w * 0.5, 8)
        c.saveState()
        c.translate(x + w / 2, y + h / 2)
        c.rotate(-90)
        c.setFillColor(white)
        c.setFont("RoundBold", size)
        c.drawCentredString(0, -size * 0.35, t["spine"])
        c.restoreState()


def build(lang):
    t = CTX[lang]
    out = os.path.join(KDP, "out", "02_dino_abc", lang)
    interior = os.path.join(out, f"DinoQuestABC_{lang.upper()}_Interior_8.5x11.pdf")
    tmp = os.path.join(out, "_thumbs")
    thumbs = K.render_pages(interior, tmp, scale=1.3, pages=[11, 12, 3, 66], prefix="t", fmt="jpg")
    path = os.path.join(out, f"DinoQuestABC_{lang.upper()}_Cover_Paperback.pdf")
    geo = K.build_cover(path, TRIM_W, TRIM_H, PAGES, "bw_white",
                        lambda c, *a: back(c, *a, t, thumbs), lambda c, *a: spine(c, *a, t),
                        lambda c, *a: front(c, *a, t), title="Dino Quest ABC", author=t["pub"])
    import pypdfium2 as pdfium
    pg = pdfium.PdfDocument(path)[0]
    sc = 300 / 72
    img = pg.render(scale=sc).to_pil().convert("RGB")
    fx, fy = int((K.BLEED + TRIM_W + geo["spine_in"] * inch) * sc), int(K.BLEED * sc)
    img.crop((fx, fy, fx + int(TRIM_W * sc), fy + int(TRIM_H * sc))).save(
        os.path.join(out, f"DinoQuestABC_{lang.upper()}_Front_Cover.jpg"), quality=93, dpi=(300, 300))
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    return path, geo


if __name__ == "__main__":
    for lang in sys.argv[1:] or ["en", "fr"]:
        p, g = build(lang)
        print(lang, p, {k: round(v, 4) for k, v in g.items() if k.endswith("_in")})
