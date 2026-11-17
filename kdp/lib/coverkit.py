"""Shared cover-art helpers for the Dino Quest series (consistent series branding)."""
from reportlab.lib.units import inch  # noqa: F401

from . import kdpkit as K

INK = K.hex_color("#2a2320")
ORANGE = K.hex_color("#ff8a2a")
YELLOW = K.hex_color("#ffd23f")
GREEN = K.hex_color("#5cbf4f")
SKY1, SKY2 = K.hex_color("#7fd3ff"), K.hex_color("#fff1b8")


def scene(c, x, y, w, h):
    """Sky + hills background painted over a whole panel (incl. bleed)."""
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.linearGradient(x, y + h, x, y, (SKY1, SKY2), extend=True)
    c.restoreState()


def hills(c, x, y, w, h):
    for col, base, amp, ph in [("#9ad86f", 0.30, 0.06, 0.0), ("#5cbf4f", 0.20, 0.05, 1.3)]:
        c.setFillColor(K.hex_color(col))
        p = c.beginPath()
        p.moveTo(x, y)
        p.lineTo(x, y + h * base)
        p.curveTo(x + w * 0.3, y + h * (base + amp), x + w * 0.6, y + h * (base - amp), x + w, y + h * (base + amp * 0.5))
        p.lineTo(x + w, y)
        p.close()
        c.drawPath(p, fill=1, stroke=0)


def badge(c, cx, cy, r, lines):
    K.poly(c, K.star_points(cx, cy, r, r * 0.8, n=16), fill=K.hex_color("#e2574c"), stroke=INK, lw=3)
    c.setFillColor(YELLOW)
    c.circle(cx, cy, r * 0.7, stroke=0, fill=1)
    sizes = [r * 0.62, r * 0.27, r * 0.22]
    ys = [cy + r * 0.02, cy - r * 0.28, cy + r * 0.38]
    order = [1, 2, 0]  # big number in middle, word under, word above
    for (txt, s_, yy) in [(lines[0], sizes[0], cy - r * 0.12), (lines[1], sizes[2], cy + r * 0.4), (lines[2], sizes[2], cy - r * 0.48)]:
        s_ = K.fit_size(txt, "Title", r * 1.25, s_)
        c.setFillColor(INK)
        c.setFont("Title", s_)
        c.drawCentredString(cx, yy, txt)


