"""Book 1 full-wrap paperback cover (8.5x11, 108 pp, black ink/white paper) + front JPG."""
import os
import sys

from reportlab.lib.colors import white
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

HERE = os.path.dirname(os.path.abspath(__file__))
KDP = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, KDP)
sys.path.insert(0, HERE)

from lib import art as A  # noqa: E402
from lib import kdpkit as K  # noqa: E402
from lib.coverkit import badge, hills, scene  # noqa: E402,F401

PAGES = 108
TRIM_W, TRIM_H = 8.5 * inch, 11 * inch
SAFE = 0.5 * inch  # stricter than KDP's 0.25in: every text item >= 0.5in from trim
INK = K.hex_color("#2a2320")
ORANGE = K.hex_color("#ff8a2a")
YELLOW = K.hex_color("#ffd23f")
GREEN = K.hex_color("#5cbf4f")
SKY1, SKY2 = K.hex_color("#7fd3ff"), K.hex_color("#fff1b8")

CTX = {
    "en": {
        "series": "DINO QUEST", "kind": "ACTIVITY BOOK", "ages": "for Kids Ages 4-8",
        "badge": ["86", "FUN", "ACTIVITIES"],
        "bar": "Mazes • Dot-to-Dot • Word Search • Coloring • Counting • Tracing",
        "back_h": "Roar into learning!",
        "back_lines": [
            "Join Rex, Trixie, Bitsy and the whole Dino Quest crew on a 108-page prehistoric adventure "
            "that keeps little explorers busy, happy and learning - without a screen.",
        ],
        "bullets": ["14 mazes from easy to tricky", "12 dot-to-dots counting up to 50",
                    "8 word searches + tracing pages", "Counting, adding, shadows & odd-one-out",
                    "Color-by-number & spot the difference", "10 single-sided coloring pages",
                    "Quest Map, answer key & certificate"],
        "foot": "Perfect gift for birthdays, road trips & rainy days!",
        "spine": "DINO QUEST  •  Activity Book for Kids Ages 4-8",
        "pub": "Dino Quest Kids Press",
    },
    "fr": {
        "series": "DINO QUEST", "kind": "CAHIER D'ACTIVITÉS", "ages": "pour les enfants de 4 à 8 ans",
        "badge": ["86", "ACTIVITÉS", "FUN"],
        "bar": "Labyrinthes • Points à relier • Mots mêlés • Coloriages • Calcul • Graphisme",
        "back_h": "En route pour l'aventure !",
        "back_lines": [
            "Rex, Trixie, Bitsy et toute l'équipe Dino Quest emmènent les petits explorateurs dans une "
            "aventure préhistorique de 108 pages : on s'amuse, on apprend, et sans écran !",
        ],
        "bullets": ["14 labyrinthes du plus facile au plus malin", "12 points à relier jusqu'à 50",
                    "8 mots mêlés + pages de graphisme", "Dénombrement, additions, ombres, intrus",
                    "Coloriages magiques & 5 différences", "10 coloriages imprimés au recto seul",
                    "Carte de la Quête, solutions & diplôme"],
        "foot": "L'idée cadeau parfaite : anniversaires, voyages, jours de pluie !",
        "spine": "DINO QUEST  •  Cahier d'activités 4-8 ans",
        "pub": "Dino Quest Kids Press",
    },
}


def front(c, x, y, w, h, t):
    # bleed-extended art region
    bx, by, bw, bh = x - K.BLEED, y - K.BLEED, w + K.BLEED, h + 2 * K.BLEED
    scene(c, bx, by, bw, bh)
    c.saveState()
    p = c.beginPath()
    p.rect(bx, by, bw, bh)
    c.clipPath(p, stroke=0, fill=0)
    A.place(c, A.volcano(), x + w * 0.58, y + h * 0.22, w * 0.42, h * 0.3, mode="color", palette="purple", lw=2.5)
    A.place(c, A.sun(), x + w * 0.74, y + h * 0.6, w * 0.17, w * 0.17, mode="color", palette="orange", lw=2.2)
    A.place(c, A.cloud(), x + w * 0.3, y + h * 0.6, w * 0.2, w * 0.09, mode="color", lw=2)
    hills(c, bx, by, bw, bh)
    A.place(c, A.palm(), x + w * 0.0, y + h * 0.17, w * 0.24, h * 0.38, mode="color", palette="teal", lw=2.5)
    A.place(c, A.longneck(), x + w * 0.5, y + h * 0.14, w * 0.48, h * 0.5, mode="color", palette="purple", lw=3)
    A.place(c, A.ptero(), x + w * 0.42, y + h * 0.5, w * 0.26, h * 0.09, mode="color", palette="teal", lw=2.2)
    A.place(c, A.trex(), x + w * 0.08, y + h * 0.13, w * 0.58, h * 0.44, mode="color", palette="green", lw=3.4)
    A.place(c, A.triceratops(), x + w * 0.56, y + h * 0.1, w * 0.4, h * 0.19, mode="color", palette="orange", lw=3)
    A.place(c, A.baby_egg(), x + w * 0.02, y + h * 0.1, w * 0.22, h * 0.17, mode="color", palette="yellow", lw=2.6)
    c.restoreState()
    # title block
    cx = x + w / 2
    tsize = K.fit_size(t["series"], "Title", w - 2 * SAFE - 0.3 * inch, 118)
    K.outlined_text(c, t["series"], cx, y + h - SAFE - tsize * 0.85, "Title", tsize, white, INK, 16)
    K.outlined_text(c, t["series"], cx, y + h - SAFE - tsize * 0.85, "Title", tsize, ORANGE, white, 6)
    K.outlined_text(c, t["series"], cx, y + h - SAFE - tsize * 0.85, "Title", tsize, ORANGE, ORANGE, 0.1)
    # ribbon
    ry = y + h - SAFE - tsize * 0.85 - 0.95 * inch
    rw = w - 2 * SAFE
    c.setFillColor(K.hex_color("#2f7fd8"))
    c.setStrokeColor(INK)
    c.setLineWidth(3)
    c.roundRect(x + SAFE, ry, rw, 0.78 * inch, 0.39 * inch, stroke=1, fill=1)
    ks = K.fit_size(t["kind"], "Title", rw - 0.5 * inch, 46)
    K.outlined_text(c, t["kind"], cx, ry + 0.2 * inch, "Title", ks, white, INK, 5)
    K.outlined_text(c, t["kind"], cx, ry + 0.2 * inch, "Title", ks, white, white, 0.1)
    asz = K.fit_size(t["ages"], "RoundBold", rw, 30)
    K.outlined_text(c, t["ages"], cx, ry - 0.48 * inch, "RoundBold", asz, INK, white, 7)
    K.outlined_text(c, t["ages"], cx, ry - 0.48 * inch, "RoundBold", asz, INK, INK, 0.1)
    badge(c, x + SAFE + 0.85 * inch, ry - 1.3 * inch, 0.85 * inch, t["badge"])
    # bottom bar
    bh_ = 0.62 * inch
    c.setFillColor(K.hex_color("#ffffff", 0.92))
    c.setStrokeColor(INK)
    c.setLineWidth(2.5)
    c.roundRect(x + SAFE - 0.15 * inch, y + SAFE - 0.1 * inch, w - 2 * SAFE + 0.3 * inch, bh_, 0.3 * inch, stroke=1, fill=1)
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
    K.text_center(c, t["back_h"], (L + R) / 2, y + h - SAFE - 0.45 * inch, "Title", 40, R - L, INK)
    yy = y + h - SAFE - 0.75 * inch
    for para in t["back_lines"]:
        yy = K.paragraph(c, para, L, yy, "BodyBold", 13.5, R - L, 1.35, INK, align="center") - 0.12 * inch
    # thumbnails of real interior pages
    tw = (R - L - 0.3 * inch) / 4
    th = tw * 11 / 8.5
    ty = yy - th - 0.1 * inch
    for i, img in enumerate(thumbs):
        tx = L + i * (tw + 0.1 * inch)
        c.setFillColor(white)
        c.setStrokeColor(INK)
        c.setLineWidth(2)
        c.saveState()
        c.translate(tx + tw / 2, ty + th / 2)
        c.rotate([-3, 2, -2, 3][i])
        c.drawImage(ImageReader(img), -tw / 2, -th / 2, tw, th)
        c.rect(-tw / 2, -th / 2, tw, th, stroke=1, fill=0)
        c.restoreState()
    # bullets
    yy = ty - 0.42 * inch
    for b in t["bullets"]:
        A.place(c, A.footprint(), L + 0.2 * inch, yy - 0.24 * inch, 0.3 * inch, 0.3 * inch, mode="color", palette="green", lw=1.2)
        c.setFillColor(INK)
        c.setFont("BodyBold", K.fit_size(b, "BodyBold", R - L - 0.8 * inch, 16))
        c.drawString(L + 0.65 * inch, yy - 0.17 * inch, b)
        yy -= 0.38 * inch
    A.place(c, A.stegosaurus(), x + w * 0.42, y + SAFE + 1.45 * inch, w * 0.3, h * 0.13, mode="color", palette="blue", lw=2.4)
    A.place(c, A.ankylo(), x + w * 0.72, y + SAFE + 1.45 * inch, w * 0.24, h * 0.1, mode="color", palette="red", lw=2.2, flip=True)
    # mascot + footer, keeping the KDP barcode zone (bottom-right) clear
    zx, zy, zw, zh = K.barcode_zone(x, y, w)
    A.place(c, A.baby_egg(), L, y + SAFE + 0.45 * inch, 1.5 * inch, 1.3 * inch, mode="color", palette="yellow", lw=2.4)
    K.paragraph(c, t["foot"], L + 1.65 * inch, y + SAFE + 1.45 * inch, "Title", 17, zx - (L + 1.65 * inch) - 0.25 * inch, 1.15, INK)
    c.setFont("RoundBold", 11)
    c.setFillColor(INK)
    c.drawString(L, y + SAFE, t["pub"])
    c.setFillColor(white)
    c.rect(zx, zy, zw, zh, stroke=0, fill=1)  # clean white field for KDP's barcode


def spine(c, x, y, w, h, t):
    c.setFillColor(K.hex_color("#2f7fd8"))
    c.rect(x - 0.01 * inch, y - K.BLEED, w + 0.02 * inch, h + 2 * K.BLEED, stroke=0, fill=1)
    if PAGES >= K.SPINE_TEXT_MIN_PAGES:
        size = min(w * 0.5, 9)  # leaves >= 0.0625in each side
        c.saveState()
        c.translate(x + w / 2, y + h / 2)
        c.rotate(-90)
        c.setFillColor(white)
        c.setFont("RoundBold", size)
        c.drawCentredString(0, -size * 0.35, t["spine"])
        c.restoreState()


def build(lang):
    t = CTX[lang]
    out = os.path.join(KDP, "out", "01_dino_quest", lang)
    interior = os.path.join(out, f"DinoQuest_{lang.upper()}_Interior_8.5x11.pdf")
    thumbs = K.render_pages(interior, os.path.join(out, "_thumbs"), scale=1.3, pages=[22, 8, 18, 28], prefix="t", fmt="jpg")
    path = os.path.join(out, f"DinoQuest_{lang.upper()}_Cover_Paperback.pdf")
    geo = K.build_cover(path, TRIM_W, TRIM_H, PAGES, "bw_white",
                        lambda c, *a: back(c, *a, t, thumbs), lambda c, *a: spine(c, *a, t),
                        lambda c, *a: front(c, *a, t), title="Dino Quest", author=t["pub"])
    # front-cover JPG (marketing, A+ content, social) from the vector PDF
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(path)
    pg = pdf[0]
    scale = 300 / 72
    img = pg.render(scale=scale).to_pil().convert("RGB")
    fx = int((K.BLEED + TRIM_W + geo["spine_in"] * inch) * scale)
    fy = int(K.BLEED * scale)
    front_img = img.crop((fx, fy, fx + int(TRIM_W * scale), fy + int(TRIM_H * scale)))
    front_img.save(os.path.join(out, f"DinoQuest_{lang.upper()}_Front_Cover.jpg"), quality=93, dpi=(300, 300))
    for f in os.listdir(os.path.join(out, "_thumbs")):
        os.remove(os.path.join(out, "_thumbs", f))
    os.rmdir(os.path.join(out, "_thumbs"))
    return path, geo


if __name__ == "__main__":
    for lang in sys.argv[1:] or ["en", "fr"]:
        p, g = build(lang)
        print(lang, p, {k: round(v, 4) for k, v in g.items() if k.endswith("_in")})
