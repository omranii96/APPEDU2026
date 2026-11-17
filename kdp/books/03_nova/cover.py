"""Book 3 full-wrap cover (8.5x8.5, 32 pp, premium colour) + Kindle eBook cover (2560x2560 JPG)."""
import os
import sys

from reportlab.lib.units import inch

HERE = os.path.dirname(os.path.abspath(__file__))
KDP = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, KDP)
sys.path.insert(0, HERE)

from lib import kdpkit as K  # noqa: E402
from lib import night as N  # noqa: E402
from lib.night import C  # noqa: E402
from build import S, leaf, meadow, trail  # noqa: E402,F401

PAGES = 32
SAFE = 0.5 * inch

CTX = {
    "en": {
        "t1": "Nova's", "t2": "Calm Glow",
        "sub": "A Bedtime Story About Big Feelings",
        "ages": "Ages 3-6",
        "pub": "Dino Quest Kids Press",
        "back_h": "Some nights, little lights feel BIG feelings.",
        "back": [
            "When thunder grumbles, her brother bumps her wing and tomorrow's Moonlight Picnic feels SO exciting, "
            "Nova the firefly's light flashes worried blue, cross red and fizzy yellow. How will she ever fall asleep?",
            "With help from wise Grandma Owl, a jumpy little Frog and the kind Moon, Nova learns three simple ways "
            "to calm her glow - and then shares them with her friends.",
        ],
        "bullets": ["A gentle read-aloud for a calmer bedtime", "Names feelings with colors kids understand",
                    "3 easy calming tools: breathing, squeeze & let go, counting stars",
                    "Bonus: star breathing & hill breathing pages, feelings chart, parent tips"],
    },
    "fr": {
        "t1": "La lumière douce", "t2": "de Nova",
        "sub": "Une histoire du soir pour apprivoiser les émotions",
        "ages": "Dès 3 ans",
        "pub": "Dino Quest Kids Press",
        "back_h": "Certains soirs, les petites lumières ressentent de GRANDES émotions.",
        "back": [
            "Quand l'orage gronde, que son petit frère lui cogne l'aile et que le pique-nique de demain la rend "
            "SI impatiente, la lumière de Nova la luciole clignote en bleu inquiet, en rouge fâché et en jaune "
            "pétillant. Comment va-t-elle réussir à dormir ?",
            "Avec Mamie Chouette, Grenouille et la gentille Lune, Nova découvre trois façons simples de calmer "
            "sa lumière... puis les partage avec ses amis.",
        ],
        "bullets": ["Une lecture douce pour un coucher plus serein", "Des couleurs pour nommer les émotions",
                    "3 outils faciles : respirer, serrer-relâcher, compter les étoiles",
                    "Bonus : respiration de l'étoile, roue des émotions, conseils parents"],
    },
}


def front(c, x, y, w, h, t, ebook=False):
    meadow(c, x, y, seed=41, moon=(0.87, 0.41, 0.045), tree=(0.08, 0.5))
    N.owl(c, x + w * (0.08 + 0.5 * 0.27), y + w * (0.18 + 0.5 * 0.6), w * 0.13)
    N.frog(c, x + w * 0.8, y + w * 0.09, w * 0.1)
    N.bunny(c, x + w * 0.16, y + w * 0.07, w * 0.13, "calm")
    trail(c, [(x + w * (0.25 + i * 0.025), y + w * (0.22 + 0.04 * (i % 3))) for i in range(9)], "#ffd25e")
    N.firefly(c, x + w * 0.56, y + w * 0.33, w * 0.13, "calm", strength=1.3)
    for (sx, sy) in [(0.3, 0.45), (0.85, 0.32), (0.72, 0.55)]:
        N.sparkle(c, x + w * sx, y + w * sy, 11, "#ffe9a8")
    cx = x + w / 2
    s1 = K.fit_size(t["t1"], "Title", w - 2 * SAFE, 60)
    s2 = K.fit_size(t["t2"], "Title", w - 2 * SAFE, 78)
    s = min(s1 * 1.0, s2)
    y1 = y + h - SAFE - s1 * 0.95
    y2 = y1 - s2 * 1.0
    for txt, yy, sz in [(t["t1"], y1, s1 if len(t["t1"]) > 10 else s1), (t["t2"], y2, s2)]:
        K.outlined_text(c, txt, cx, yy, "Title", sz, C("#ffd25e"), C("#1d1733"), 9)
        K.outlined_text(c, txt, cx, yy, "Title", sz, C("#ffd25e"), C("#ffd25e"), 0.1)
    c.setFillColor(N.CREAM)
    sub_sz = K.fit_size(t["sub"], "ReadBold", w - 2 * SAFE, 20)
    c.setFont("ReadBold", sub_sz)
    c.drawCentredString(cx, y2 - 0.42 * inch, t["sub"])
    # age badge + publisher
    bx, by = x + w - SAFE - 0.55 * inch, y2 - 1.15 * inch
    N.glow(c, bx, by, 0.9 * inch, "#ffd25e", 1.0)
    c.setFillColor(C("#ffd25e"))
    c.circle(bx, by, 0.5 * inch, stroke=0, fill=1)
    c.setFillColor(C("#1d1733"))
    c.setFont("Title", K.fit_size(t["ages"], "Title", 0.85 * inch, 17))
    c.drawCentredString(bx, by - 6, t["ages"])
    c.setFillColor(N.CREAM)
    c.setFont("RoundBold", 12)
    c.drawCentredString(cx, y + SAFE + 0.08 * inch, t["pub"])


def back(c, x, y, w, h, t):
    N.sky(c, x - K.BLEED, y - K.BLEED, w + 2 * K.BLEED, h + 2 * K.BLEED, "#10153a", "#3b2f6b")
    N.stars(c, x - K.BLEED, y, w + 2 * K.BLEED, h, 60, 7)
    L, R = x + SAFE, x + w - SAFE
    yy = K.paragraph(c, t["back_h"], L, y + h - SAFE, "Title", 27, R - L, 1.12, C("#ffd25e"), align="center") - 0.16 * inch
    for p in t["back"]:
        yy = K.paragraph(c, p, L, yy, "ReadBold", 15, R - L, 1.35, N.CREAM, align="center") - 0.14 * inch
    for b in t["bullets"]:
        N.glow(c, L + 0.12 * inch, yy - 0.12 * inch, 12, "#ffd25e", 1.2, steps=8)
        c.setFillColor(C("#ffd25e"))
        c.circle(L + 0.12 * inch, yy - 0.12 * inch, 4, stroke=0, fill=1)
        yy = K.paragraph(c, b, L + 0.35 * inch, yy, "RoundBold", 14, R - L - 0.35 * inch, 1.25, N.CREAM) - 0.08 * inch
    # feelings row
    zx, zy, zw, zh = K.barcode_zone(x, y, w)
    for i, mood in enumerate(["worried", "grumpy", "excited", "calm"]):
        N.firefly(c, L + 0.4 * inch + i * 1.0 * inch, y + SAFE + 0.75 * inch, 0.26 * inch, mood)
    c.setFillColor(C("#ffffff"))
    c.rect(zx, zy, zw, zh, stroke=0, fill=1)


def spine(c, x, y, w, h, t):
    N.sky(c, x - 1, y - K.BLEED, w + 2, h + 2 * K.BLEED, "#10153a", "#3b2f6b")


def build(lang):
    t = CTX[lang]
    out = os.path.join(KDP, "out", "03_nova", lang)
    path = os.path.join(out, f"Nova_{lang.upper()}_Cover_Paperback.pdf")
    geo = K.build_cover(path, S, S, PAGES, "color_white",
                        lambda c, *a: back(c, *a, t), lambda c, *a: spine(c, *a, t),
                        lambda c, *a: front(c, *a, t), title=t["t1"] + " " + t["t2"], author=t["pub"])
    # Kindle eBook cover: square 2560 px rendered from a dedicated vector front (no spine/bleed)
    epdf = os.path.join(out, "_ebook_cover.pdf")
    c = K.new_canvas(epdf, S, S, t["t1"], t["pub"])
    front(c, 0, 0, S, S, t, ebook=True)
    c.showPage()
    c.save()
    import pypdfium2 as pdfium
    img = pdfium.PdfDocument(epdf)[0].render(scale=2560 / S).to_pil().convert("RGB")
    img.save(os.path.join(out, f"Nova_{lang.upper()}_Kindle_Cover_2560.jpg"), quality=92)
    os.remove(epdf)
    return path, geo


if __name__ == "__main__":
    for lang in sys.argv[1:] or ["en", "fr"]:
        p, g = build(lang)
        print(lang, p, {k: round(v, 4) for k, v in g.items() if k.endswith("_in")})
