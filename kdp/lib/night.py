"""
Night-meadow illustration kit for "Luma's Little Light" (full-colour picture book).
Everything is drawn directly on the PDF canvas as vectors: gradients, glows built
from stacked translucent discs, silhouettes, and the cast:
Luma (firefly), Flick (her little brother), Grandma Owl, Frog, Bunny, Snail, the Moon.
"""
import math
import random

from reportlab.lib.colors import Color

from .kdpkit import hex_color as HX

NAVY = HX("#141a3a")
INK = HX("#1d1733")
CREAM = HX("#fff6dc")
GOLD = HX("#ffd25e")
FEEL = {"calm": "#ffd25e", "worried": "#5aa9ff", "grumpy": "#ff5b4a", "excited": "#fff04a", "sleepy": "#ffc96b"}


def C(h, a=1.0):
    return HX(h, a)


# --------------------------------------------------------------------------- primitives
def path_poly(c, pts, fill=None, stroke=None, lw=2, close=True):
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
    c.drawPath(p, fill=fill is not None, stroke=stroke is not None)


def ellipse(c, cx, cy, rx, ry, fill=None, stroke=None, lw=2, rot=0):
    c.saveState()
    c.translate(cx, cy)
    if rot:
        c.rotate(rot)
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.ellipse(-rx, -ry, rx, ry, fill=fill is not None, stroke=stroke is not None)
    c.restoreState()


def glow(c, x, y, r, color_hex, strength=1.0, steps=22):
    """Soft light: many translucent discs, larger ones fainter."""
    c.saveState()
    for i in range(steps, 0, -1):
        rr = r * i / steps
        a = 0.045 * strength * (1.15 - i / steps)
        c.setFillColor(C(color_hex, min(a, 1)))
        c.circle(x, y, rr, stroke=0, fill=1)
    c.restoreState()


def sky(c, x, y, w, h, top="#0e1233", bottom="#3b2f6b"):
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.linearGradient(x, y + h, x, y, (C(top), C(bottom)), extend=True)
    c.restoreState()


def stars(c, x, y, w, h, n=60, seed=1, color="#fff6dc"):
    rnd = random.Random(seed)
    for _ in range(n):
        sx, sy = x + rnd.random() * w, y + rnd.random() * h
        r = rnd.choice([0.7, 0.9, 1.1, 1.4, 2.0])
        c.setFillColor(C(color, rnd.uniform(0.5, 1)))
        c.circle(sx, sy, r, stroke=0, fill=1)
        if r >= 1.4:
            glow(c, sx, sy, r * 5, color, 0.6, steps=8)


def sparkle(c, x, y, r, color="#fff6dc"):
    pts = []
    for i in range(8):
        a = math.radians(i * 45)
        rr = r if i % 2 == 0 else r * 0.28
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    path_poly(c, pts, fill=C(color))


def hill(c, x0, x1, base, peaks, color, y_floor):
    """Smooth silhouette through (x, y) peaks, filled down to y_floor."""
    p = c.beginPath()
    p.moveTo(x0, y_floor)
    p.lineTo(x0, peaks[0][1])
    prev = (x0, peaks[0][1])
    for (px, py) in peaks:
        mx = (prev[0] + px) / 2
        p.curveTo(mx, prev[1], mx, py, px, py)
        prev = (px, py)
    p.curveTo((prev[0] + x1) / 2, prev[1], (prev[0] + x1) / 2, base, x1, base)
    p.lineTo(x1, y_floor)
    p.close()
    c.setFillColor(C(color))
    c.drawPath(p, fill=1, stroke=0)


def grass(c, x0, x1, y, h, color, seed=3, density=0.09):
    rnd = random.Random(seed)
    c.setFillColor(C(color))
    x = x0
    while x < x1:
        bw = rnd.uniform(3, 7)
        bh = h * rnd.uniform(0.45, 1.0)
        lean = rnd.uniform(-bh * 0.35, bh * 0.35)
        p = c.beginPath()
        p.moveTo(x, y)
        p.curveTo(x + bw * 0.2, y + bh * 0.5, x + lean * 0.6, y + bh * 0.8, x + lean + bw / 2, y + bh)
        p.curveTo(x + lean * 0.6 + bw, y + bh * 0.7, x + bw * 0.9, y + bh * 0.4, x + bw, y)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        x += bw * rnd.uniform(0.6, 1.4) / density * 0.09
    c.rect(x0, y - 40, x1 - x0, 40.5, stroke=0, fill=1)


def flower(c, x, y, s, petal="#f4c1e0", center="#ffd25e", stem="#2a5a4a"):
    c.setStrokeColor(C(stem))
    c.setLineWidth(s * 0.12)
    c.line(x, y - s * 2.2, x, y)
    for k in range(6):
        a = math.radians(k * 60)
        ellipse(c, x + math.cos(a) * s * 0.55, y + math.sin(a) * s * 0.55, s * 0.5, s * 0.3, fill=C(petal), rot=k * 60)
    c.setFillColor(C(center))
    c.circle(x, y, s * 0.35, stroke=0, fill=1)


def tree(c, x, ground, h, color="#1c2a4a"):
    c.setFillColor(C(color))
    p = c.beginPath()
    p.moveTo(x - h * 0.07, ground)
    p.curveTo(x - h * 0.05, ground + h * 0.3, x - h * 0.06, ground + h * 0.45, x - h * 0.03, ground + h * 0.58)
    p.lineTo(x + h * 0.03, ground + h * 0.58)
    p.curveTo(x + h * 0.06, ground + h * 0.45, x + h * 0.05, ground + h * 0.3, x + h * 0.08, ground)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    for (dx, dy, r) in [(0, 0.72, 0.24), (-0.2, 0.62, 0.18), (0.2, 0.63, 0.19), (-0.12, 0.84, 0.17), (0.13, 0.85, 0.16),
                        (0, 0.95, 0.12), (-0.28, 0.52, 0.12), (0.29, 0.53, 0.12)]:
        c.circle(x + dx * h, ground + dy * h, r * h, stroke=0, fill=1)
    # the branch Grandma Owl sits on
    path_poly(c, [(x + h * 0.02, ground + h * 0.55), (x + h * 0.36, ground + h * 0.6), (x + h * 0.36, ground + h * 0.625),
                  (x + h * 0.02, ground + h * 0.59)], fill=C(color))


def moon(c, x, y, r, face=True, sleepy=False):
    glow(c, x, y, r * 2.6, "#fff3c4", 1.2)
    c.setFillColor(C("#fff3c4"))
    c.circle(x, y, r, stroke=0, fill=1)
    for (dx, dy, rr) in [(-0.35, 0.35, 0.16), (0.4, -0.3, 0.12), (0.25, 0.5, 0.08)]:
        c.setFillColor(C("#f0e1a6"))
        c.circle(x + dx * r, y + dy * r, rr * r, stroke=0, fill=1)
    if face:
        c.setStrokeColor(C("#8a6d3b"))
        c.setLineWidth(r * 0.05)
        c.setLineCap(1)
        for ex in (-0.3, 0.3):
            p = c.beginPath()
            p.arc(x + ex * r - r * 0.12, y + r * 0.02, x + ex * r + r * 0.12, y + r * 0.22, 200 if sleepy else 20, 140)
            c.drawPath(p, stroke=1, fill=0)
        p = c.beginPath()
        p.arc(x - r * 0.22, y - r * 0.42, x + r * 0.22, y - r * 0.08, 200, 140)
        c.drawPath(p, stroke=1, fill=0)
        c.setFillColor(C("#ffb3a7", 0.7))
        c.circle(x - r * 0.5, y - r * 0.18, r * 0.11, stroke=0, fill=1)
        c.circle(x + r * 0.5, y - r * 0.18, r * 0.11, stroke=0, fill=1)


def storm_cloud(c, x, y, s, bolt=True):
    if bolt:
        path_poly(c, [(x + s * 0.1, y - s * 0.2), (x - s * 0.1, y - s * 0.75), (x + s * 0.05, y - s * 0.7),
                      (x - s * 0.08, y - s * 1.2), (x + s * 0.3, y - s * 0.55), (x + s * 0.12, y - s * 0.6),
                      (x + s * 0.3, y - s * 0.2)], fill=C("#ffe680"))
    c.setFillColor(C("#4a4f7a"))
    for (dx, dy, r) in [(-0.6, 0, 0.35), (-0.2, 0.2, 0.45), (0.3, 0.15, 0.4), (0.7, -0.02, 0.3)]:
        c.circle(x + dx * s, y + dy * s, r * s, stroke=0, fill=1)
    c.roundRect(x - 0.9 * s, y - 0.3 * s, 1.85 * s, 0.4 * s, 0.2 * s, stroke=0, fill=1)


# --------------------------------------------------------------------------- characters
def _eye(c, x, y, r, mood, look=(0, 0)):
    if mood in ("sleepy", "calm_closed"):
        c.setStrokeColor(INK)
        c.setLineWidth(r * 0.35)
        c.setLineCap(1)
        p = c.beginPath()
        p.arc(x - r, y - r * 0.6, x + r, y + r * 0.9, 200, 140)
        c.drawPath(p, stroke=1, fill=0)
        return
    c.setFillColor(INK)
    c.ellipse(x - r * 0.8, y - r, x + r * 0.8, y + r, stroke=0, fill=1)
    c.setFillColor(C("#ffffff"))
    c.circle(x - r * 0.25 + look[0], y + r * 0.35 + look[1], r * 0.32, stroke=0, fill=1)
    c.circle(x + r * 0.3 + look[0], y - r * 0.35 + look[1], r * 0.13, stroke=0, fill=1)


def _brows(c, x, y, r, mood, side):
    if mood not in ("worried", "grumpy"):
        return
    c.setStrokeColor(INK)
    c.setLineWidth(r * 0.3)
    c.setLineCap(1)
    inner_up = mood == "worried"
    dx = r * 1.0
    if side < 0:
        a, b = (x - dx, y + r * (1.45 if inner_up else 1.75)), (x + dx * 0.6, y + r * (1.85 if inner_up else 1.3))
    else:
        a, b = (x - dx * 0.6, y + r * (1.85 if inner_up else 1.3)), (x + dx, y + r * (1.45 if inner_up else 1.75))
    c.line(a[0], a[1], b[0], b[1])


def _mouth(c, x, y, r, mood):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.setLineWidth(r * 0.08)
    c.setLineCap(1)
    if mood == "excited":
        p = c.beginPath()
        p.moveTo(x - r * 0.3, y)
        p.curveTo(x - r * 0.25, y - r * 0.35, x + r * 0.25, y - r * 0.35, x + r * 0.3, y)
        p.close()
        c.drawPath(p, fill=1, stroke=1)
        c.setFillColor(C("#ff8fa3"))
        c.circle(x, y - r * 0.16, r * 0.09, stroke=0, fill=1)
    elif mood == "grumpy":
        p = c.beginPath()
        p.arc(x - r * 0.2, y - r * 0.2, x + r * 0.2, y + r * 0.08, 20, 140)
        c.drawPath(p, stroke=1, fill=0)
    elif mood == "worried":
        p = c.beginPath()
        p.moveTo(x - r * 0.2, y - r * 0.05)
        p.curveTo(x - r * 0.1, y + r * 0.05, x - r * 0.05, y - r * 0.12, x, y - r * 0.05)
        p.curveTo(x + r * 0.05, y + r * 0.05, x + r * 0.1, y - r * 0.12, x + r * 0.2, y - r * 0.05)
        c.drawPath(p, stroke=1, fill=0)
    elif mood == "surprised":
        c.setFillColor(INK)
        c.ellipse(x - r * 0.09, y - r * 0.2, x + r * 0.09, y + r * 0.02, stroke=0, fill=1)
    else:
        p = c.beginPath()
        p.arc(x - r * 0.18, y - r * 0.15, x + r * 0.18, y + r * 0.12, 200, 140)
        c.drawPath(p, stroke=1, fill=0)


def firefly(c, x, y, s, mood="calm", glow_color=None, flip=False, wings_up=True, small=False, strength=1.0, tilt=0):
    """Luma / Flick. (x, y) = centre of the head. s = head radius."""
    gc = glow_color or FEEL.get(mood, FEEL["calm"])
    c.saveState()
    c.translate(x, y)
    if tilt:
        c.rotate(tilt)
    if flip:
        c.scale(-1, 1)
    lx, ly = -s * 0.95, -s * 1.55  # lantern (glowing tail)
    glow(c, lx, ly, s * 4.2, gc, 1.3 * strength)
    # wings
    for (dx, rot, rx) in [(-0.55, 35, 1.05), (0.35, -20, 0.95)]:
        ellipse(c, dx * s - s * 0.4, s * 0.45, rx * s, s * 0.48, fill=C("#dff4ff", 0.55), stroke=C("#ffffff", 0.8), lw=s * 0.05,
                rot=rot + (10 if wings_up else -30))
    # body + lantern
    ellipse(c, -s * 0.55, -s * 0.85, s * 0.62, s * 0.55, fill=C("#6b4fa0"), rot=35)
    ellipse(c, lx, ly, s * 0.66, s * 0.6, fill=C(gc), rot=35)
    glow(c, lx, ly, s * 1.1, "#ffffff", 0.9 * strength, steps=10)
    # legs
    c.setStrokeColor(C("#3a2a5c"))
    c.setLineWidth(s * 0.09)
    c.setLineCap(1)
    for k in range(3):
        bx = -s * (0.25 + k * 0.28)
        c.line(bx, -s * 1.05, bx + s * 0.08, -s * 1.45)
    # antennae
    c.setLineWidth(s * 0.08)
    for side in (-1, 1):
        p = c.beginPath()
        p.moveTo(side * s * 0.3, s * 0.8)
        p.curveTo(side * s * 0.45, s * 1.4, side * s * 0.9, s * 1.6, side * s * 1.0, s * 1.35)
        c.drawPath(p, stroke=1, fill=0)
        c.setFillColor(C(gc))
        c.circle(side * s * 1.0, s * 1.35, s * 0.14, stroke=0, fill=1)
    # head
    c.setFillColor(C("#8c6cc8" if not small else "#6fb0d8"))
    c.circle(0, 0, s, stroke=0, fill=1)
    c.setFillColor(C("#ffffff", 0.18))
    c.circle(-s * 0.35, s * 0.4, s * 0.35, stroke=0, fill=1)
    em = "sleepy" if mood == "sleepy" else mood
    for side in (-1, 1):
        _eye(c, side * s * 0.38, s * 0.08, s * 0.2, em)
        _brows(c, side * s * 0.38, s * 0.08, s * 0.2, mood, side)
    c.setFillColor(C("#ff8fa3", 0.75))
    c.circle(-s * 0.62, -s * 0.28, s * 0.16, stroke=0, fill=1)
    c.circle(s * 0.62, -s * 0.28, s * 0.16, stroke=0, fill=1)
    _mouth(c, 0, -s * 0.38, s, mood)
    if mood == "sleepy" or small:
        pass
    c.restoreState()


def owl(c, x, y, s, eyes_closed=False):
    """Grandma Owl. (x, y) = feet on branch; s = body height."""
    w = s * 0.42
    ellipse(c, x, y + s * 0.45, w, s * 0.5, fill=C("#8b5e3c"))
    ellipse(c, x, y + s * 0.36, w * 0.68, s * 0.33, fill=C("#e9c99a"))
    c.setStrokeColor(C("#b98b5a"))
    c.setLineWidth(s * 0.012)
    for row in range(3):
        for k in range(3 - (row == 2)):
            cx_ = x - w * 0.35 + k * w * 0.35 + (w * 0.17 if row == 2 else 0)
            cy_ = y + s * (0.5 - row * 0.12)
            p = c.beginPath()
            p.arc(cx_ - w * 0.12, cy_ - s * 0.05, cx_ + w * 0.12, cy_ + s * 0.03, 200, 140)
            c.drawPath(p, stroke=1, fill=0)
    for side in (-1, 1):
        ellipse(c, x + side * w * 0.92, y + s * 0.42, w * 0.28, s * 0.32, fill=C("#6e4528"), rot=side * -12)
        path_poly(c, [(x + side * w * 0.45, y + s * 0.86), (x + side * w * 0.9, y + s * 1.08), (x + side * w * 0.8, y + s * 0.78)],
                  fill=C("#6e4528"))
    for side in (-1, 1):
        c.setFillColor(C("#fff6dc"))
        c.circle(x + side * w * 0.38, y + s * 0.72, w * 0.33, stroke=0, fill=1)
        if eyes_closed:
            c.setStrokeColor(INK)
            c.setLineWidth(s * 0.025)
            p = c.beginPath()
            p.arc(x + side * w * 0.38 - w * 0.15, y + s * 0.66, x + side * w * 0.38 + w * 0.15, y + s * 0.78, 200, 140)
            c.drawPath(p, stroke=1, fill=0)
        else:
            _eye(c, x + side * w * 0.38, y + s * 0.72, w * 0.15, "calm")
        c.setStrokeColor(C("#c79a2e"))
        c.setLineWidth(s * 0.02)
        c.circle(x + side * w * 0.38, y + s * 0.72, w * 0.36, stroke=1, fill=0)
    c.line(x - w * 0.02, y + s * 0.74, x + w * 0.02, y + s * 0.74)
    path_poly(c, [(x - w * 0.1, y + s * 0.62), (x + w * 0.1, y + s * 0.62), (x, y + s * 0.52)], fill=C("#f2a03d"))
    for side in (-1, 1):
        for k in range(3):
            c.setStrokeColor(C("#f2a03d"))
            c.setLineWidth(s * 0.03)
            c.line(x + side * w * 0.3, y + s * 0.02, x + side * w * (0.18 + k * 0.12), y - s * 0.04)


def frog(c, x, y, s, mood="calm", squeeze=False):
    """(x, y) = centre of lily pad; s = frog size."""
    pad_w = s * 1.3
    p = c.beginPath()
    p.moveTo(x, y)
    p.arc(x - pad_w, y - pad_w * 0.32, x + pad_w, y + pad_w * 0.32, 105, 330)
    p.close()
    c.setFillColor(C("#2f8f6b"))
    c.drawPath(p, fill=1, stroke=0)
    sq = 0.82 if squeeze else 1.0
    ellipse(c, x, y + s * 0.42 * sq, s * 0.75 / sq ** 0.5, s * 0.5 * sq, fill=C("#7ccf5e"))
    ellipse(c, x, y + s * 0.3 * sq, s * 0.45, s * 0.28 * sq, fill=C("#d9f2a6"))
    for side in (-1, 1):
        ellipse(c, x + side * s * 0.7, y + s * 0.12, s * 0.3, s * 0.13, fill=C("#5fb547"))
        c.setFillColor(C("#7ccf5e"))
        c.circle(x + side * s * 0.36, y + s * 0.88 * sq, s * 0.24, stroke=0, fill=1)
        if squeeze:
            c.setStrokeColor(INK)
            c.setLineWidth(s * 0.05)
            c.line(x + side * s * 0.46, y + s * 0.84 * sq, x + side * s * 0.26, y + s * 0.92 * sq)
        else:
            c.setFillColor(C("#ffffff"))
            c.circle(x + side * s * 0.36, y + s * 0.9, s * 0.16, stroke=0, fill=1)
            _eye(c, x + side * s * 0.36, y + s * 0.9, s * 0.09, "calm")
    c.setStrokeColor(INK)
    c.setLineWidth(s * 0.04)
    p = c.beginPath()
    p.arc(x - s * 0.3, y + s * 0.42 * sq, x + s * 0.3, y + s * 0.68 * sq, 200, 140)
    c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(C("#ff8fa3", 0.7))
    c.circle(x - s * 0.5, y + s * 0.5 * sq, s * 0.08, stroke=0, fill=1)
    c.circle(x + s * 0.5, y + s * 0.5 * sq, s * 0.08, stroke=0, fill=1)


def bunny(c, x, y, s, mood="worried"):
    """(x, y) = bottom centre."""
    for side in (-1, 1):
        ellipse(c, x + side * s * 0.18, y + s * 1.25, s * 0.12, s * 0.38, fill=C("#d9d6e8"), rot=side * -10)
        ellipse(c, x + side * s * 0.18, y + s * 1.25, s * 0.06, s * 0.28, fill=C("#ffb3c6"), rot=side * -10)
    ellipse(c, x, y + s * 0.32, s * 0.42, s * 0.34, fill=C("#d9d6e8"))
    c.setFillColor(C("#e8e6f3"))
    c.circle(x, y + s * 0.8, s * 0.32, stroke=0, fill=1)
    for side in (-1, 1):
        _eye(c, x + side * s * 0.12, y + s * 0.84, s * 0.055, "calm" if mood != "sleepy" else "sleepy")
        _brows(c, x + side * s * 0.12, y + s * 0.84, s * 0.055, mood, side)
    c.setFillColor(C("#ff8fa3"))
    c.circle(x, y + s * 0.74, s * 0.035, stroke=0, fill=1)
    _mouth(c, x, y + s * 0.68, s * 0.3, mood if mood != "sleepy" else "calm")
    ellipse(c, x - s * 0.22, y + s * 0.03, s * 0.14, s * 0.07, fill=C("#e8e6f3"))
    ellipse(c, x + s * 0.22, y + s * 0.03, s * 0.14, s * 0.07, fill=C("#e8e6f3"))


def snail(c, x, y, s, sleepy=False):
    p = c.beginPath()
    p.moveTo(x - s * 0.7, y)
    p.curveTo(x - s * 0.2, y - s * 0.05, x + s * 0.4, y - s * 0.05, x + s * 0.7, y + s * 0.05)
    p.curveTo(x + s * 0.8, y + s * 0.3, x + s * 0.6, y + s * 0.45, x + s * 0.45, y + s * 0.2)
    p.lineTo(x - s * 0.7, y + s * 0.12)
    p.close()
    c.setFillColor(C("#f1c38b"))
    c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(C("#f1c38b"))
    c.setLineWidth(s * 0.05)
    for dx in (0.55, 0.68):
        c.line(x + s * dx, y + s * 0.35, x + s * (dx + 0.05), y + s * 0.6)
        c.setFillColor(C("#f1c38b"))
        c.circle(x + s * (dx + 0.05), y + s * 0.6, s * 0.05, stroke=0, fill=1)
    _eye(c, x + s * 0.62, y + s * 0.28, s * 0.04, "sleepy" if sleepy else "calm")
    for i, (r, col) in enumerate([(0.45, "#c0627a"), (0.32, "#e07d96"), (0.2, "#c0627a"), (0.09, "#e07d96")]):
        c.setFillColor(C(col))
        c.circle(x - s * 0.1 + i * s * 0.03, y + s * 0.45 - i * s * 0.02, r * s, stroke=0, fill=1)
