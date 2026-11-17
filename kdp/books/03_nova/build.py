"""
Book 3 - NOVA'S CALM GLOW, full-colour picture book (EN + FR)
KDP paperback: 8.5 x 8.5 in, PREMIUM COLOR ink, white paper, FULL BLEED, 32 pages.
Also builds an ebook PDF (trim size, no bleed) for Kindle Kids' Book Creator.

    python3 build.py [en|fr]   -> out/03_nova/<lang>/
"""
import math
import os
import random
import sys

from reportlab.lib.units import inch

HERE = os.path.dirname(os.path.abspath(__file__))
KDP = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, KDP)
sys.path.insert(0, HERE)

from lib import kdpkit as K  # noqa: E402
from lib import night as N  # noqa: E402
from lib.night import C  # noqa: E402
from story import BACK, META, STORY  # noqa: E402

S = 8.5 * inch
B = K.BLEED
PAGES = 32
SAFE = 0.6 * inch           # text safe margin from trim (KDP min 0.375in incl. gutter)
PARCH = "#fff4dc"


# ------------------------------------------------------------------ helpers
def meadow(c, X, Y, seed=1, top="#0e1233", bottom="#3b2f6b", moon=None, tree=False, stars_n=70, hill_cols=None,
           grass_h=0.13, flowers=True, pond=False):
    N.sky(c, X - B, Y - B, S + 2 * B, S + 2 * B, top, bottom)
    N.stars(c, X - B, Y + S * 0.35, S + 2 * B, S * 0.7, stars_n, seed)
    if moon:
        N.moon(c, X + moon[0] * S, Y + moon[1] * S, moon[2] * S, face=True, sleepy=moon[3] if len(moon) > 3 else False)
    hc = hill_cols or ["#2b2f68", "#1f3f5c", "#173a3f"]
    N.hill(c, X - B, X + S + B, Y + S * 0.3, [(X + S * 0.2, Y + S * 0.36), (X + S * 0.55, Y + S * 0.29), (X + S * 0.85, Y + S * 0.38)],
           hc[0], Y - B)
    if tree:
        N.tree(c, X + tree[0] * S, Y + S * 0.18, tree[1] * S)
    N.hill(c, X - B, X + S + B, Y + S * 0.2, [(X + S * 0.3, Y + S * 0.25), (X + S * 0.7, Y + S * 0.21)], hc[1], Y - B)
    if pond:
        N.ellipse(c, X + S * 0.55, Y + S * 0.12, S * 0.42, S * 0.09, fill=C("#24507a"))
        N.ellipse(c, X + S * 0.5, Y + S * 0.14, S * 0.18, S * 0.02, fill=C("#ffffff", 0.12))
    N.grass(c, X - B, X + S + B, Y + S * 0.06, S * grass_h, hc[2], seed=seed + 4)
    if flowers:
        rnd = random.Random(seed)
        for _ in range(5):
            N.flower(c, X + rnd.uniform(0.05, 0.95) * S, Y + rnd.uniform(0.08, 0.15) * S, S * 0.012,
                     petal=rnd.choice(["#f4c1e0", "#c9b8ff", "#ffe3a3"]))


def text_panel(c, text, X, Y, where="top", size=22, maxw=None, color=None):
    w = maxw or (S - 2 * SAFE)
    font = "ReadBold"
    while True:
        lines = []
        for para in text.split("\n"):
            lines += K.wrap(para, font, size, w - 0.5 * inch)
        lead = size * 1.32
        h = len(lines) * lead + 0.36 * inch
        if h < S * 0.34 or size <= 13:
            break
        size -= 0.5
    x = X + (S - w) / 2
    y = Y + S - SAFE - h if where == "top" else Y + SAFE
    if where == "mid":
        y = Y + (S - h) / 2
    c.saveState()
    c.setFillColor(C("#0b0f2a", 0.55))
    c.roundRect(x, y, w, h, 0.22 * inch, stroke=0, fill=1)
    c.setFillColor(color or N.CREAM)
    c.setFont(font, size)
    ty = y + h - 0.18 * inch - size
    for ln in lines:
        c.drawCentredString(x + w / 2, ty, ln)
        ty -= lead
    c.restoreState()
    return y, h


def candle(c, x, y, s):
    c.setFillColor(C("#ff9ec4"))
    c.roundRect(x - s * 0.18, y, s * 0.36, s * 1.1, s * 0.06, stroke=0, fill=1)
    c.setFillColor(C("#ffffff", 0.5))
    for k in range(4):
        c.rect(x - s * 0.18, y + s * (0.15 + k * 0.25), s * 0.36, s * 0.07, stroke=0, fill=1)
    N.glow(c, x, y + s * 1.38, s * 0.7, "#ffd25e", 1.4)
    p = c.beginPath()
    p.moveTo(x, y + s * 1.16)
    p.curveTo(x - s * 0.16, y + s * 1.25, x - s * 0.05, y + s * 1.45, x, y + s * 1.62)
    p.curveTo(x + s * 0.05, y + s * 1.45, x + s * 0.16, y + s * 1.25, x, y + s * 1.16)
    c.setFillColor(C("#ffb02e"))
    c.drawPath(p, fill=1, stroke=0)


def dots_row(c, x, y, n, label, gap, col="#fff6dc"):
    c.setFont("RoundBold", 16)
    c.setFillColor(C(col))
    for i in range(n):
        c.circle(x + i * gap, y, 9, stroke=0, fill=1)
        c.setFillColor(C("#1d1733"))
        c.drawCentredString(x + i * gap, y - 5.5, str(i + 1))
        c.setFillColor(C(col))
    c.setFont("ReadBold", 15)
    c.drawString(x + n * gap, y - 5, label)


def leaf(c, x, y, s, rot=0):
    c.saveState()
    c.translate(x, y)
    c.rotate(rot)
    p = c.beginPath()
    p.moveTo(-s, 0)
    p.curveTo(-s * 0.4, s * 0.55, s * 0.5, s * 0.5, s, 0)
    p.curveTo(s * 0.5, -s * 0.45, -s * 0.4, -s * 0.5, -s, 0)
    c.setFillColor(C("#3f9a62"))
    c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(C("#2b7449"))
    c.setLineWidth(s * 0.03)
    c.line(-s * 0.95, 0, s * 0.9, 0)
    for k in range(4):
        xx = -s * 0.6 + k * s * 0.38
        c.line(xx, 0, xx + s * 0.18, s * 0.22)
        c.line(xx, 0, xx + s * 0.18, -s * 0.22)
    c.restoreState()


def zzz(c, x, y, s):
    c.setFillColor(N.CREAM)
    for i in range(3):
        c.setFont("Title", s * (0.6 + i * 0.25))
        c.drawString(x + i * s * 0.5, y + i * s * 0.6, "z")


def trail(c, pts, color):
    for i, (px, py) in enumerate(pts):
        N.glow(c, px, py, 9 + i * 0.4, color, 0.6, steps=6)
        c.setFillColor(C(color, 0.8))
        c.circle(px, py, 1.6, stroke=0, fill=1)


def star5(c, cx, cy, r, fill, num=None):
    N.glow(c, cx, cy, r * 2.2, "#fff3c4", 0.9)
    K.poly(c, K.star_points(cx, cy, r, r * 0.45), fill=C(fill), stroke=None)
    if num:
        c.setFillColor(C("#1d1733"))
        c.setFont("Title", r * 0.75)
        c.drawCentredString(cx, cy - r * 0.27, str(num))


# ------------------------------------------------------------------ pages
def p_title(c, X, Y, L):
    m = META[L]
    meadow(c, X, Y, seed=11, moon=(0.8, 0.6, 0.06), tree=(0.1, 0.55))
    N.firefly(c, X + S * 0.55, Y + S * 0.42, S * 0.07, "calm")
    trail(c, [(X + S * (0.2 + i * 0.03), Y + S * (0.3 + 0.06 * math.sin(i * 0.6))) for i in range(10)], "#ffd25e")
    sz = K.fit_size(m["title"], "Title", S - 2 * SAFE, 52)
    K.outlined_text(c, m["title"], X + S / 2, Y + S - SAFE - sz, "Title", sz, C("#ffd25e"), C("#1d1733"), 6)
    K.outlined_text(c, m["title"], X + S / 2, Y + S - SAFE - sz, "Title", sz, C("#ffd25e"), C("#ffd25e"), 0.1)
    c.setFillColor(N.CREAM)
    c.setFont("ReadBold", K.fit_size(m["subtitle"], "ReadBold", S - 2 * SAFE, 18))
    c.drawCentredString(X + S / 2, Y + S - SAFE - sz - 0.45 * inch, m["subtitle"])
    c.setFont("Round", 13)
    c.drawCentredString(X + S / 2, Y + SAFE, m["author"])


def p_copyright(c, X, Y, L):
    m = META[L]
    c.setFillColor(C(PARCH))
    c.rect(X - B, Y - B, S + 2 * B, S + 2 * B, stroke=0, fill=1)
    N.firefly(c, X + S / 2, Y + S * 0.72, S * 0.045, "sleepy")
    c.setFillColor(C("#3b2f6b"))
    yy = Y + S * 0.55
    for ln in m["dedication"].split("\n"):
        c.setFont("ReadBold", 20)
        c.drawCentredString(X + S / 2, yy, ln)
        yy -= 28
    yy = Y + SAFE + 0.7 * inch
    for ln in m["copyright"]:
        c.setFont("Body", 9.5)
        c.setFillColor(C("#5a5470"))
        c.drawCentredString(X + S / 2, yy, ln)
        yy -= 14


def story_page(n):
    def draw(c, X, Y, L):
        txt = STORY[n][0 if L == "en" else 1]
        u = S
        where = "top"
        if n == 3:
            meadow(c, X, Y, seed=3, moon=(0.85, 0.62, 0.06), tree=(0.12, 0.62))
            N.firefly(c, X + u * 0.6, Y + u * 0.32, u * 0.04, "calm")
            trail(c, [(X + u * (0.35 + i * 0.022), Y + u * (0.24 + 0.03 * math.sin(i))) for i in range(10)], "#ffd25e")
        elif n == 4:
            meadow(c, X, Y, seed=4, top="#16163f", bottom="#4b3a7a", stars_n=50)
            N.firefly(c, X + u * 0.5, Y + u * 0.36, u * 0.12, "calm")
            for (sx, sy) in [(0.25, 0.48), (0.75, 0.3), (0.72, 0.52)]:
                N.sparkle(c, X + u * sx, Y + u * sy, 9, "#ffe9a8")
        elif n == 5:
            meadow(c, X, Y, seed=5, moon=(0.8, 0.55, 0.07))
            N.bunny(c, X + u * 0.2, Y + u * 0.1, u * 0.15, "calm")
            N.snail(c, X + u * 0.38, Y + u * 0.1, u * 0.07)
            N.firefly(c, X + u * 0.62, Y + u * 0.35, u * 0.045, "calm")
        elif n == 6:
            meadow(c, X, Y, seed=6, top="#0b1030", bottom="#28335f", stars_n=40)
            N.storm_cloud(c, X + u * 0.78, Y + u * 0.5, u * 0.07)
            N.firefly(c, X + u * 0.42, Y + u * 0.34, u * 0.1, "worried", tilt=-4)
        elif n == 7:
            meadow(c, X, Y, seed=7, top="#170f2e", bottom="#4a2a52")
            N.firefly(c, X + u * 0.38, Y + u * 0.34, u * 0.1, "grumpy")
            N.firefly(c, X + u * 0.75, Y + u * 0.45, u * 0.05, "excited", small=True, flip=True, glow_color="#7fe0ff", tilt=10)
            c.setStrokeColor(C("#ffffff", 0.5))
            c.setLineWidth(2.2)
            c.setLineCap(1)
            for k in range(3):
                c.line(X + u * 0.84, Y + u * (0.43 + k * 0.025), X + u * 0.96, Y + u * (0.44 + k * 0.025))
        elif n == 8:
            meadow(c, X, Y, seed=8, top="#1a1440", bottom="#5a3b7a")
            zz = [(X + u * (0.12 + i * 0.05), Y + u * (0.33 + (0.06 if i % 2 else -0.04))) for i in range(9)]
            trail(c, zz, "#fff04a")
            N.firefly(c, X + u * 0.66, Y + u * 0.36, u * 0.1, "excited", wings_up=True, tilt=8)
            for (sx, sy) in [(0.5, 0.52), (0.85, 0.5), (0.8, 0.22)]:
                N.sparkle(c, X + u * sx, Y + u * sy, 11, "#fff04a")
        elif n == 9:
            meadow(c, X, Y, seed=9)
            for (gx, gy, col) in [(0.3, 0.42, "#5aa9ff"), (0.7, 0.42, "#ff5b4a"), (0.5, 0.2, "#fff04a")]:
                N.glow(c, X + u * gx, Y + u * gy, u * 0.2, col, 1.5)
            N.firefly(c, X + u * 0.5, Y + u * 0.35, u * 0.1, "worried", glow_color="#ffffff")
        elif n == 10:
            meadow(c, X, Y, seed=10, tree=(0.2, 0.46), moon=(0.86, 0.5, 0.045))
            N.owl(c, X + u * (0.2 + 0.46 * 0.27), Y + u * (0.18 + 0.46 * 0.6), u * 0.14)
            N.firefly(c, X + u * 0.7, Y + u * 0.26, u * 0.07, "worried", flip=True)
            where = "top"
        elif n == 11:
            meadow(c, X, Y, seed=12, top="#151a45", bottom="#40336f", flowers=False)
            N.flower(c, X + u * 0.27, Y + u * 0.36, u * 0.07, petal="#f4c1e0")
            candle(c, X + u * 0.73, Y + u * 0.2, u * 0.12)
            N.firefly(c, X + u * 0.5, Y + u * 0.2, u * 0.05, "calm")
            dots_row(c, X + u * 0.1, Y + u * 0.55, 4, "", 26)
            dots_row(c, X + u * 0.58, Y + u * 0.55, 5, "", 26)
        elif n == 12:
            meadow(c, X, Y, seed=13, tree=(0.85, 0.7))
            N.firefly(c, X + u * 0.45, Y + u * 0.36, u * 0.1, "sleepy", glow_color="#ffd25e")
            c.setStrokeColor(C("#bfe6ff", 0.6))
            c.setLineWidth(2.5)
            for k in range(3):
                p = c.beginPath()
                p.arc(X + u * (0.6 + k * 0.04) - 20, Y + u * 0.35 - 20 - k * 10, X + u * (0.6 + k * 0.04) + 20,
                      Y + u * 0.35 + 20 + k * 10, -60, 120)
                c.drawPath(p, stroke=1, fill=0)
        elif n in (13, 14, 15):
            meadow(c, X, Y, seed=14, pond=True, top="#0f1a3d", bottom="#2c4a6b")
            N.frog(c, X + u * 0.55, Y + u * 0.1, u * 0.14, squeeze=(n == 14))
            mood = {13: "calm", 14: "grumpy", 15: "sleepy"}[n]
            gc = {13: "#ffe58a", 14: "#ffd25e", 15: "#ffb44d"}[n]
            N.firefly(c, X + u * 0.25, Y + u * 0.36, u * 0.08, mood if n != 14 else "worried", glow_color=gc)
        elif n == 16:
            meadow(c, X, Y, seed=16, top="#0d1435", bottom="#33306a")
            N.moon(c, X + u * 0.66, Y + u * 0.48, u * 0.13)
            c.setFillColor(C("#5b5f92"))
            for (dx, dy, r) in [(-0.1, -0.08, 0.07), (0.0, -0.1, 0.08), (0.1, -0.09, 0.06), (0.17, -0.1, 0.05)]:
                c.circle(X + u * (0.66 + dx), Y + u * (0.48 + dy), u * r, stroke=0, fill=1)
            N.firefly(c, X + u * 0.25, Y + u * 0.3, u * 0.07, "calm")
        elif n == 17:
            meadow(c, X, Y, seed=17, stars_n=30)
            for i, (sx, sy) in enumerate([(0.15, 0.45), (0.32, 0.55), (0.5, 0.47), (0.68, 0.56), (0.85, 0.46)]):
                star5(c, X + u * sx, Y + u * sy, u * 0.05, "#ffe9a8", i + 1)
            N.firefly(c, X + u * 0.5, Y + u * 0.25, u * 0.06, "calm")
        elif n == 18:
            meadow(c, X, Y, seed=18, top="#141a45", bottom="#4a3d7f")
            N.firefly(c, X + u * 0.5, Y + u * 0.35, u * 0.13, "calm", strength=1.4)
            for (sx, sy) in [(0.2, 0.5), (0.8, 0.5), (0.25, 0.2), (0.78, 0.22)]:
                N.sparkle(c, X + u * sx, Y + u * sy, 12, "#ffe9a8")
        elif n == 19:
            meadow(c, X, Y, seed=19, tree=(0.12, 0.56))
            N.owl(c, X + u * (0.12 + 0.56 * 0.27), Y + u * (0.18 + 0.56 * 0.6), u * 0.14)
            N.firefly(c, X + u * 0.6, Y + u * 0.34, u * 0.09, "excited", glow_color="#ffd25e")
            N.firefly(c, X + u * 0.83, Y + u * 0.27, u * 0.045, "calm", small=True, flip=True, glow_color="#7fe0ff")
        elif n == 20:
            meadow(c, X, Y, seed=20, top="#0b1030", bottom="#28335f")
            N.storm_cloud(c, X + u * 0.18, Y + u * 0.52, u * 0.05)
            N.bunny(c, X + u * 0.38, Y + u * 0.08, u * 0.24, "worried")
            N.firefly(c, X + u * 0.72, Y + u * 0.35, u * 0.07, "calm", flip=True)
        elif n == 21:
            meadow(c, X, Y, seed=21)
            N.bunny(c, X + u * 0.22, Y + u * 0.08, u * 0.2, "calm")
            N.snail(c, X + u * 0.45, Y + u * 0.09, u * 0.09, sleepy=True)
            N.firefly(c, X + u * 0.65, Y + u * 0.33, u * 0.07, "sleepy")
            N.firefly(c, X + u * 0.85, Y + u * 0.25, u * 0.04, "sleepy", small=True, flip=True, glow_color="#7fe0ff")
        elif n == 22:
            meadow(c, X, Y, seed=22, moon=(0.85, 0.6, 0.06), tree=(0.1, 0.6))
            rnd = random.Random(22)
            for _ in range(70):
                gx, gy = X + rnd.uniform(0.03, 0.97) * u, Y + rnd.uniform(0.08, 0.5) * u
                N.glow(c, gx, gy, rnd.uniform(8, 22), rnd.choice(["#ffd25e", "#ffe58a", "#ffc46b"]), 1.0, steps=8)
                c.setFillColor(C("#fff6dc"))
                c.circle(gx, gy, 1.8, stroke=0, fill=1)
            N.firefly(c, X + u * 0.5, Y + u * 0.32, u * 0.06, "calm")
        elif n == 23:
            meadow(c, X, Y, seed=23, top="#0a0f2b", bottom="#2a2a5a", flowers=False)
            leaf(c, X + u * 0.5, Y + u * 0.22, u * 0.3, rot=-6)
            N.firefly(c, X + u * 0.52, Y + u * 0.3, u * 0.09, "sleepy", wings_up=False, glow_color="#ffc46b")
        elif n == 24:
            meadow(c, X, Y, seed=24, top="#070b22", bottom="#1d1f4a", moon=(0.78, 0.55, 0.08, True), flowers=False)
            leaf(c, X + u * 0.4, Y + u * 0.2, u * 0.26, rot=4)
            N.firefly(c, X + u * 0.42, Y + u * 0.27, u * 0.08, "sleepy", wings_up=False, glow_color="#ffb44d", strength=0.7)
            zzz(c, X + u * 0.52, Y + u * 0.36, 18)
        text_panel(c, txt, X, Y, where)
    return draw


def p_star(c, X, Y, L):
    t = BACK[L]
    meadow(c, X, Y, seed=25, stars_n=40, flowers=False)
    cx, cy, r = X + S / 2, Y + S * 0.4, S * 0.26
    pts = K.star_points(cx, cy, r, r * 0.45)
    pts.append(pts[0])
    c.saveState()
    c.setStrokeColor(C("#ffd25e"))
    c.setLineWidth(9)
    c.setLineCap(1)
    c.setLineJoin(1)
    c.setDash(1, 16)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()
    for i in range(10):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        mx, my = (ax + bx) / 2, (ay + by) / 2
        lab = t["in"] if by > ay else t["out"]
        dx, dy = mx - cx, my - cy
        d = math.hypot(dx, dy)
        c.setFillColor(C("#bfe6ff" if by > ay else "#ffd2a8"))
        c.setFont("RoundBold", 15)
        c.drawCentredString(mx + dx / d * 26, my + dy / d * 26 - 5, lab)
    N.firefly(c, pts[0][0], pts[0][1] + 22, S * 0.03, "calm")
    tp_y, _ = text_panel(c, t["star_t"] + "\n" + t["star_i"], X, Y, "top", size=17)


def p_hill(c, X, Y, L):
    t = BACK[L]
    meadow(c, X, Y, seed=26, flowers=False, stars_n=40)
    pts = []
    for i in range(121):
        xx = X + SAFE + (S - 2 * SAFE) * i / 120
        yy = Y + S * 0.32 + S * 0.09 * math.sin(i / 120 * 2 * math.pi * 3 - math.pi / 2)
        pts.append((xx, yy))
    c.saveState()
    c.setStrokeColor(C("#ffd25e"))
    c.setLineWidth(9)
    c.setLineCap(1)
    c.setDash(1, 16)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()
    for k in range(3):
        up = pts[k * 40 + 10]
        dn = pts[k * 40 + 30]
        c.setFont("RoundBold", 16)
        c.setFillColor(C("#bfe6ff"))
        c.drawCentredString(up[0] - 10, up[1] + 18, t["in"])
        c.setFillColor(C("#ffd2a8"))
        c.drawCentredString(dn[0] + 10, dn[1] + 18, t["out"])
    N.firefly(c, pts[0][0] + 6, pts[0][1] + 24, S * 0.03, "calm")
    text_panel(c, t["hill_t"] + "\n" + t["hill_i"], X, Y, "top", size=17)


def p_feel(c, X, Y, L):
    t = BACK[L]
    meadow(c, X, Y, seed=27, flowers=False, stars_n=40)
    for i, (mood, name) in enumerate(t["feels"]):
        col, row = i % 3, i // 3
        cx = X + S * (0.2 + col * 0.3) + (S * 0.15 if row == 1 else 0)
        cy = Y + S * (0.5 - row * 0.28)
        N.firefly(c, cx, cy, S * 0.045, mood)
        c.setFillColor(C(N.FEEL[mood]))
        c.setFont("Title", 20)
        c.drawCentredString(cx - S * 0.02, cy - S * 0.13, name)
    text_panel(c, t["feel_t"] + "\n" + t["feel_i"], X, Y, "top", size=18)


def p_tools(c, X, Y, L):
    t = BACK[L]
    meadow(c, X, Y, seed=28, flowers=False, stars_n=40)
    ty, th = text_panel(c, t["tool_t"], X, Y, "top", size=24)
    cw = S - 2 * SAFE
    chh = (ty - Y - SAFE - 0.3 * inch) / 3
    for i, (name, desc) in enumerate(t["tools"]):
        cy = ty - 0.15 * inch - (i + 1) * chh - i * 0.05 * inch
        c.setFillColor(C("#fff4dc", 0.95))
        c.roundRect(X + SAFE, cy, cw, chh, 0.2 * inch, stroke=0, fill=1)
        ix = X + SAFE + 0.75 * inch
        icy = cy + chh / 2
        if i == 0:
            N.flower(c, ix - 0.3 * inch, icy + 0.12 * inch, 16, petal="#f4a6cf")
            candle(c, ix + 0.34 * inch, icy - 0.5 * inch, 0.55 * inch)
        elif i == 1:
            N.frog(c, ix, icy - 0.38 * inch, 0.75 * inch, squeeze=True)
        else:
            for k in range(5):
                K.poly(c, K.star_points(ix - 0.42 * inch + k * 0.21 * inch, icy + (0.12 if k % 2 else -0.08) * inch,
                                        0.12 * inch, 0.055 * inch), fill=C("#f2b632"), stroke=None)
        c.setFillColor(C("#3b2f6b"))
        c.setFont("Title", 23)
        c.drawString(X + SAFE + 1.6 * inch, cy + chh - 0.5 * inch, name)
        K.paragraph(c, desc, X + SAFE + 1.6 * inch, cy + chh - 0.62 * inch, "ReadBold", 16, cw - 1.8 * inch, 1.25, C("#3b2f6b"))


def p_draw(c, X, Y, L):
    t = BACK[L]
    c.setFillColor(C(PARCH))
    c.rect(X - B, Y - B, S + 2 * B, S + 2 * B, stroke=0, fill=1)
    c.setFillColor(C("#3b2f6b"))
    c.setFont("Title", 30)
    c.drawCentredString(X + S / 2, Y + S - SAFE - 0.35 * inch, t["draw_t"])
    K.paragraph(c, t["draw_i"], X + SAFE, Y + S - SAFE - 0.55 * inch, "ReadBold", 15, S - 2 * SAFE, 1.3, C("#3b2f6b"), align="center")
    jx, jy, jw, jh = X + S * 0.27, Y + SAFE + 0.2 * inch, S * 0.46, S * 0.58
    c.setStrokeColor(C("#3b2f6b"))
    c.setLineWidth(4)
    c.roundRect(jx, jy, jw, jh, 0.5 * inch, stroke=1, fill=0)
    c.roundRect(jx + jw * 0.12, jy + jh, jw * 0.76, 0.35 * inch, 0.08 * inch, stroke=1, fill=0)
    c.setLineWidth(2)
    c.line(jx + jw * 0.15, jy + jh * 0.85, jx + jw * 0.15, jy + jh * 0.55)
    N.firefly(c, X + S * 0.83, Y + S * 0.3, S * 0.04, "calm")


def p_grown(c, X, Y, L):
    t = BACK[L]
    c.setFillColor(C(PARCH))
    c.rect(X - B, Y - B, S + 2 * B, S + 2 * B, stroke=0, fill=1)
    c.setFillColor(C("#3b2f6b"))
    c.setFont("Title", 30)
    c.drawString(X + SAFE, Y + S - SAFE - 0.35 * inch, t["grown_t"])
    yy = Y + S - SAFE - 0.6 * inch
    for para in t["grown"]:
        yy = K.paragraph(c, para, X + SAFE, yy, "Body", 15, S - 2 * SAFE, 1.42, C("#3b2f6b")) - 0.16 * inch
    N.firefly(c, X + S - SAFE - 0.4 * inch, Y + SAFE + 0.35 * inch, S * 0.03, "calm")


def p_thanks(c, X, Y, L):
    t = BACK[L]
    meadow(c, X, Y, seed=31, moon=(0.8, 0.62, 0.06))
    N.firefly(c, X + S * 0.5, Y + S * 0.3, S * 0.06, "excited", glow_color="#ffd25e")
    text_panel(c, t["thanks_t"] + "\n" + "\n".join(t["thanks"]), X, Y, "top", size=17)


def p_end(c, X, Y, L):
    t = BACK[L]
    meadow(c, X, Y, seed=32, top="#060a1f", bottom="#1a1c44", moon=(0.5, 0.62, 0.1, True), flowers=False)
    leaf(c, X + S * 0.5, Y + S * 0.2, S * 0.2)
    N.firefly(c, X + S * 0.52, Y + S * 0.26, S * 0.06, "sleepy", wings_up=False, glow_color="#ffb44d", strength=0.7)
    c.setFillColor(N.CREAM)
    c.setFont("Title", 34)
    c.drawCentredString(X + S / 2, Y + SAFE + 0.05 * inch, t["sweet"])


PAGE_FUNCS = {1: p_title, 2: p_copyright, 25: p_star, 26: p_hill, 27: p_feel, 28: p_tools, 29: p_draw, 30: p_grown,
              31: p_thanks, 32: p_end}
for _n in range(3, 25):
    PAGE_FUNCS[_n] = story_page(_n)


def build(lang, mode="print"):
    out = os.path.join(KDP, "out", "03_nova", lang)
    tag = "Interior_8.5x8.5_bleed" if mode == "print" else "eBook_KKBC"
    path = os.path.join(out, f"Nova_{lang.upper()}_{tag}.pdf")
    pw, ph = (S + B, S + 2 * B) if mode == "print" else (S, S)
    c = K.new_canvas(path, pw, ph, META[lang]["title"], META[lang]["author"])
    for n in range(1, PAGES + 1):
        if mode == "print":
            X = 0 if n % 2 == 1 else B   # right pages: bleed on the right; left pages: bleed on the left
            Y = B
        else:
            X, Y = 0, 0
        c.saveState()
        p = c.beginPath()
        p.rect(0, 0, pw, ph)
        c.clipPath(p, stroke=0, fill=0)
        PAGE_FUNCS[n](c, X, Y, lang)
        c.restoreState()
        c.showPage()
    c.save()
    return path


if __name__ == "__main__":
    for lang in sys.argv[1:] or ["en", "fr"]:
        for mode in ("print", "ebook"):
            print(lang, mode, build(lang, mode))
