"""
Original vector character art (cute "kawaii" dinosaurs + props), built from
shapely primitives. One model -> three renderings:
  * line art (coloring pages): painter's algorithm, white fills + black outlines
  * colour art (covers): same parts, palette fills
  * silhouette / outline (shadow-match, dot-to-dot): union of parts
All art is 100% original geometry produced in code - no third-party images,
so there is no copyright / AI-disclosure ambiguity for the line art.
"""
import math

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

from .kdpkit import draw_geom, hex_color
from reportlab.lib.colors import black, white


# --------------------------------------------------------------------------- primitives
def ell(cx, cy, rx, ry, rot=0):
    g = affinity.scale(Point(cx, cy).buffer(1, 64), rx, ry)
    return affinity.rotate(g, rot, origin=(cx, cy)) if rot else g


def circ(cx, cy, r):
    return Point(cx, cy).buffer(r, 64)


def hull2(p0, r0, p1, r1):
    return unary_union([circ(*p0, r0), circ(*p1, r1)]).convex_hull


def chain(pts, r0, r1):
    """Tapered tube through points (tails, necks)."""
    n = len(pts)
    rs = [r0 + (r1 - r0) * i / (n - 1) for i in range(n)]
    parts = [hull2(pts[i], rs[i], pts[i + 1], rs[i + 1]) for i in range(n - 1)]
    return unary_union(parts)


def bez(p0, p1, p2, n=16):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in [i / n for i in range(n + 1)]]


def tri(a, b, c_, rnd=1.2):
    return Polygon([a, b, c_]).buffer(rnd, join_style=1)


def arc_line(cx, cy, r, a0, a1, n=20, ry=None):
    ry = ry or r
    return LineString([(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                        cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)])


# --------------------------------------------------------------------------- model
class Model:
    """parts: list of (role, geom) back-to-front; lines: list of (geom) details;
    eyes: list of (x, y, r); cheeks: list of (x, y, r)."""

    def __init__(self, name, parts, lines=(), eyes=(), cheeks=(), solids=()):
        self.name = name
        self.parts = parts
        self.lines = list(lines)
        self.eyes = list(eyes)
        self.cheeks = list(cheeks)
        self.solids = list(solids)  # always-black filled details (nostrils)

    def union(self):
        return unary_union([g for _, g in self.parts]).buffer(0)

    def bounds(self):
        return self.union().bounds


PALETTES = {
    "green": {"body": "#7cc96a", "belly": "#f4e3a1", "accent": "#f08a4b", "dark": "#4f9a43"},
    "orange": {"body": "#ffb04c", "belly": "#ffe7b0", "accent": "#e2574c", "dark": "#e08a2a"},
    "blue": {"body": "#6fb6e8", "belly": "#dff1fb", "accent": "#ffd23f", "dark": "#3f86bd"},
    "purple": {"body": "#a98be0", "belly": "#efe4ff", "accent": "#ffcf4a", "dark": "#7a5bc0"},
    "teal": {"body": "#52c4b5", "belly": "#e3fbf6", "accent": "#ff8fab", "dark": "#2c9486"},
    "red": {"body": "#f2766b", "belly": "#ffe0d8", "accent": "#ffd23f", "dark": "#c94c42"},
    "yellow": {"body": "#ffd95a", "belly": "#fff4c9", "accent": "#7cc96a", "dark": "#d9ab22"},
}


def render(c, model, x, y, scale, mode="line", palette="green", lw=2.2, flip=False):
    """Draw model with its local origin at (x, y). mode: line | color | silhouette."""
    pal = {k: hex_color(v) for k, v in PALETTES[palette].items()}
    outline = hex_color("#2a2320") if mode == "color" else black

    def T(g):
        if flip:
            g = affinity.scale(g, -1, 1, origin=(0, 0))
        g = affinity.scale(g, scale, scale, origin=(0, 0))
        return affinity.translate(g, x, y)

    if mode == "silhouette":
        draw_geom(c, T(model.union()), fill=hex_color("#2b2b2b"), stroke=None)
        return
    if mode == "outline":
        draw_geom(c, T(model.union()), fill=None, stroke=black, lw=lw)
        return
    for role, g in model.parts:
        fill = white if mode == "line" else pal.get(role, pal["body"]) if role != "white" else white
        draw_geom(c, T(g), fill=fill, stroke=outline, lw=lw)
    for g in model.lines:
        draw_geom(c, T(g), fill=None, stroke=outline, lw=lw * 0.85)
    for (ex, ey, er) in model.eyes:
        draw_geom(c, T(circ(ex, ey, er)), fill=outline, stroke=None)
        draw_geom(c, T(circ(ex + er * 0.35 * (-1 if flip else 1), ey + er * 0.35, er * 0.38)), fill=white, stroke=None)
    for (sx, sy, sr) in model.solids:
        draw_geom(c, T(circ(sx, sy, sr)), fill=outline, stroke=None)
    if mode == "color":
        for (cx_, cy_, cr) in model.cheeks:
            g = T(ell(cx_, cy_, cr, cr * 0.65))
            c.saveState()
            draw_geom(c, g, fill=hex_color("#ff8fa3", 0.55), stroke=None)
            c.restoreState()


def fit(model, box_w, box_h, pad=0.0):
    x0, y0, x1, y1 = model.bounds()
    s = min((box_w - 2 * pad) / (x1 - x0), (box_h - 2 * pad) / (y1 - y0))
    return s, x0, y0, x1, y1


def place(c, model, bx, by, bw, bh, mode="line", palette="green", lw=2.2, flip=False, pad=0):
    """Fit model centred in a box."""
    s, x0, y0, x1, y1 = fit(model, bw, bh, pad)
    w, h = (x1 - x0) * s, (y1 - y0) * s
    if flip:
        ox = bx + (bw + w) / 2 + x0 * s
    else:
        ox = bx + (bw - w) / 2 - x0 * s
    oy = by + (bh - h) / 2 - y0 * s
    render(c, model, ox, oy, s, mode, palette, lw, flip)
    return s


def placement(model, bx, by, bw, bh, pad=0, flip=False):
    """(scale, origin_x, origin_y) that centres a model in a box - same maths as place()."""
    s, x0, y0, x1, y1 = fit(model, bw, bh, pad)
    w, h = (x1 - x0) * s, (y1 - y0) * s
    ox = bx + (bw + w) / 2 + x0 * s if flip else bx + (bw - w) / 2 - x0 * s
    oy = by + (bh - h) / 2 - y0 * s
    return s, ox, oy


def transformed_union(model, bx, by, bw, bh, pad=0, flip=False):
    s, x0, y0, x1, y1 = fit(model, bw, bh, pad)
    w, h = (x1 - x0) * s, (y1 - y0) * s
    g = model.union()
    if flip:
        g = affinity.scale(g, -1, 1, origin=(0, 0))
        ox = bx + (bw + w) / 2 + x0 * s
    else:
        ox = bx + (bw - w) / 2 - x0 * s
    oy = by + (bh - h) / 2 - y0 * s
    g = affinity.scale(g, s, s, origin=(0, 0))
    return affinity.translate(g, ox, oy)


# --------------------------------------------------------------------------- dinosaurs
def smile(cx, cy, w, depth=None):
    depth = depth or w * 0.55
    return LineString(bez((cx - w, cy), (cx, cy - depth * 2), (cx + w, cy)))


def trex():
    tail = chain([(40, 40), (24, 34), (8, 28), (-6, 26)], 15, 2.5)
    leg_back = ell(46, 22, 9, 14, -8)
    foot_back = hull2((40, 7), 4.5, (52, 7), 4.5)
    body = ell(58, 44, 27, 25, 25)
    belly = ell(66, 40, 14, 17, 25)
    leg = ell(56, 26, 11, 15, 10)
    foot = hull2((52, 8), 5.5, (68, 8), 5.5)
    head = ell(88, 78, 23, 17, 8)
    jaw = ell(92, 66, 18, 8, 5)
    arm = hull2((80, 46), 3.4, (88, 42), 2.6)
    parts = [("body", tail), ("dark", leg_back), ("dark", foot_back), ("body", body), ("belly", belly),
             ("body", leg), ("body", foot), ("body", jaw), ("body", head), ("body", arm)]
    lines = [smile(95, 70, 9, 3), LineString([(56, 3.8), (56, 9)]), LineString([(62, 3.8), (62, 9)]),
             LineString(bez((60, 30), (66, 35), (72, 31))),
             LineString([(63, 54), (69, 54)]), LineString([(63, 46), (71, 47)])]
    spots = [("accent", ell(38, 58, 4, 3, 30)), ("accent", ell(48, 64, 3.2, 2.5, 30)), ("accent", ell(28, 46, 3, 2.3, 20))]
    parts[4:4] = []
    parts += []
    m = Model("T-Rex", parts + spots, lines, eyes=[(93, 82, 3.6)], cheeks=[(99, 74, 4)], solids=[(108, 82, 1.2)])
    return m


def triceratops():
    tail = chain([(28, 40), (14, 34), (2, 30)], 11, 2.5)
    frill = unary_union([ell(84, 58, 15, 21)] + [circ(84 + 16 * math.cos(math.radians(a)), 58 + 21 * math.sin(math.radians(a)), 3.8)
                                                for a in range(-30, 211, 30)])
    legs_back = [hull2((34, 26), 6.5, (34, 9), 6), hull2((70, 26), 6.5, (72, 9), 6)]
    body = ell(52, 40, 32, 22, 5)
    legs_front = [hull2((42, 24), 7, (42, 8), 6.5), hull2((62, 24), 7, (64, 8), 6.5)]
    head = ell(94, 46, 17, 14, -10)
    beak = hull2((104, 40), 7, (112, 36), 3.5)
    horn1 = hull2((92, 58), 3.6, (110, 70), 0.9)
    horn2 = hull2((100, 56), 3.4, (118, 64), 0.9)
    nose = hull2((108, 45), 2.6, (114, 51), 0.7)
    belly = ell(52, 30, 20, 9)
    parts = [("body", tail), ("accent", frill), ("dark", legs_back[0]), ("dark", legs_back[1]), ("body", body),
             ("belly", belly), ("body", legs_front[0]), ("body", legs_front[1]), ("belly", horn1), ("belly", horn2),
             ("body", head), ("belly", nose), ("body", beak)]
    lines = [smile(100, 40, 6, 2.2)] + [LineString([(x, 3.0), (x, 7)]) for x in (40, 44, 62, 66)]
    spots = [("accent", ell(40, 52, 4, 3)), ("accent", ell(54, 56, 4.5, 3.2)), ("accent", ell(68, 50, 3.5, 2.6))]
    return Model("Triceratops", parts + spots, lines, eyes=[(95, 50, 3.3)], cheeks=[(90, 42, 3.6)])


def stegosaurus():
    plates = []
    for i, (px, py, h) in enumerate([(26, 52, 9), (36, 60, 12), (48, 64, 14), (60, 64, 14), (72, 59, 12), (82, 50, 9)]):
        ang = math.atan2(py - 38, px - 54)
        tipx, tipy = px + h * math.cos(ang), py + h * math.sin(ang)
        nx, ny = -math.sin(ang) * 6.5, math.cos(ang) * 6.5
        plates.append(("accent", tri((px - nx, py - ny), (px + nx, py + ny), (tipx, tipy), 2.6)))
    tail = chain([(26, 38), (12, 34), (0, 36)], 10, 3)
    spikes = [("belly", hull2((4, 38), 2.2, (-2, 47), 0.6)), ("belly", hull2((8, 38), 2.2, (6, 48), 0.6))]
    legs_back = [hull2((32, 24), 6, (32, 8), 5.5), hull2((72, 24), 5.5, (74, 8), 5)]
    body = ell(54, 38, 31, 21, 0)
    belly = ell(54, 29, 20, 8)
    legs_front = [hull2((42, 22), 6.5, (42, 7), 6), hull2((64, 22), 6, (65, 7), 5.5)]
    neck = chain([(80, 36), (90, 32), (98, 30)], 9, 7)
    head = ell(102, 30, 11, 8, -5)
    parts = spikes + [("body", tail)] + plates + [("dark", legs_back[0]), ("dark", legs_back[1]), ("body", body),
                                                  ("belly", belly), ("body", legs_front[0]), ("body", legs_front[1]),
                                                  ("body", neck), ("body", head)]
    lines = [smile(106, 27, 4.5, 1.6)] + [LineString([(x, 2.0), (x, 6)]) for x in (40, 44, 63, 67)]
    return Model("Stegosaurus", parts, lines, eyes=[(104, 33, 2.4)], cheeks=[(100, 27, 2.6)])


def longneck():
    tail = chain([(22, 40), (8, 30), (-6, 22), (-14, 20)], 12, 2.2)
    legs_back = [hull2((28, 24), 7, (28, 7), 6.5), hull2((60, 24), 7, (61, 7), 6.5)]
    body = ell(44, 38, 28, 21)
    belly = ell(44, 28, 17, 8)
    legs_front = [hull2((36, 22), 7.5, (36, 6), 7), hull2((54, 22), 7.5, (55, 6), 7)]
    neck = chain([(60, 48), (70, 66), (76, 84), (80, 98)], 10.5, 6.5)
    head = ell(87, 101, 12, 8.5, 8)
    parts = [("body", tail), ("dark", legs_back[0]), ("dark", legs_back[1]), ("body", body), ("belly", belly),
             ("body", legs_front[0]), ("body", legs_front[1]), ("body", neck), ("body", head)]
    spots = [("accent", ell(36, 48, 4, 3)), ("accent", ell(50, 52, 3.4, 2.5)), ("accent", ell(70, 70, 2.6, 2.0, 60)),
             ("accent", ell(75, 84, 2.2, 1.8, 70))]
    lines = [smile(92, 97, 5, 1.8)] + [LineString([(x, 1.0), (x, 5)]) for x in (34, 38, 53, 57)]
    return Model("Brachiosaurus", parts + spots, lines, eyes=[(89, 104, 2.6)], cheeks=[(85, 98, 2.8)])


def ptero():
    wing_l = Polygon(bez((48, 52), (20, 80), (0, 62)) + bez((0, 62), (18, 56), (22, 44)) + [(44, 44)]).buffer(1.5)
    wing_r = Polygon(bez((58, 52), (86, 82), (108, 66)) + bez((108, 66), (90, 58), (86, 46)) + [(62, 44)]).buffer(1.5)
    body = ell(53, 46, 10, 15)
    belly = ell(53, 42, 6, 9)
    head = ell(56, 66, 10, 9)
    crest = hull2((50, 70), 3.5, (38, 80), 1.2)
    beak = Polygon([(62, 68), (82, 62), (63, 60)]).buffer(1.4)
    feet = [hull2((49, 31), 2.4, (47, 26), 2.2), hull2((57, 31), 2.4, (59, 26), 2.2)]
    parts = [("accent", crest), ("dark", wing_l), ("dark", wing_r), ("body", feet[0]), ("body", feet[1]), ("body", body),
             ("belly", belly), ("belly", beak), ("body", head)]
    lines = [LineString(bez((24, 70), (30, 60), (34, 49))), LineString(bez((84, 72), (80, 62), (76, 50)))]
    return Model("Pterodactyl", parts, lines, eyes=[(58, 69, 2.6)], cheeks=[(54, 63, 2.6)])


def ankylo():
    club = unary_union([circ(-4, 26, 7), circ(2, 30, 5)])
    tail = chain([(24, 28), (10, 26), (0, 27)], 9, 4)
    legs_back = [hull2((30, 18), 6, (30, 6), 5.5), hull2((70, 18), 6, (71, 6), 5.5)]
    shell = Polygon(bez((14, 24), (50, 74), (88, 24))).buffer(2)
    shell = unary_union([shell] + [circ(14 + i * 9.5, 24 + 0.5, 0.1) for i in range(9)])
    belly = ell(51, 21, 30, 6)
    legs_front = [hull2((40, 16), 6.5, (40, 5), 6), hull2((62, 16), 6.5, (63, 5), 6)]
    head = ell(94, 26, 12, 9.5)
    knobs = [("belly", circ(30 + i * 11, 30 + 14 * math.sin(math.pi * (i + 0.6) / 5.2), 3.2)) for i in range(5)]
    parts = [("accent", club), ("body", tail), ("dark", legs_back[0]), ("dark", legs_back[1]), ("belly", belly),
             ("body", shell)] + knobs + [("body", legs_front[0]), ("body", legs_front[1]), ("body", head)]
    lines = [smile(99, 23, 5, 1.7), LineString(bez((26, 34), (50, 52), (76, 34)))]
    return Model("Ankylosaurus", parts, lines, eyes=[(96, 29, 2.6)], cheeks=[(92, 24, 2.8)])


def baby_egg():
    head = ell(50, 62, 20, 17)
    body = ell(50, 42, 17, 15)
    shell_pts = [(22, 46)]
    for i in range(9):
        shell_pts.append((22 + (i + 0.5) * 56 / 9, 46 + (6 if i % 2 == 0 else -2)))
    shell_pts += [(78, 46)]
    shell_bottom = Polygon(shell_pts + [(78, 46)] + bez((78, 46), (80, 4), (50, 2))[1:] + bez((50, 2), (20, 4), (22, 46))[1:]).buffer(0.8)
    shell_top = Polygon([(36, 82), (42, 92), (47, 86), (53, 93), (58, 86), (64, 92), (68, 82)]
                        + bez((68, 82), (52, 106), (36, 82))[1:]).buffer(0.8)
    arms = [hull2((33, 48), 3.6, (28, 52), 3.2), hull2((67, 48), 3.6, (72, 52), 3.2)]
    parts = [("body", body), ("body", arms[0]), ("body", arms[1]), ("white", shell_bottom), ("body", head), ("belly", shell_top)]
    lines = [smile(50, 56, 6, 2.6), LineString([(30, 30), (36, 24)]), LineString([(64, 20), (70, 26)])]
    return Model("Baby Dino", parts, lines, eyes=[(42, 65, 3.2), (58, 65, 3.2)], cheeks=[(37, 58, 3.4), (63, 58, 3.4)])


def spino():
    sail = unary_union([Polygon(bez((28, 48), (50, 96), (80, 50))).buffer(2)])
    tail = chain([(28, 38), (12, 30), (-4, 26)], 11, 2.4)
    legs_back = [hull2((40, 24), 7, (38, 8), 5.5)]
    body = ell(54, 40, 27, 18, 15)
    belly = ell(58, 35, 15, 9, 15)
    leg = hull2((54, 26), 8, (55, 8), 6)
    foot = hull2((50, 6), 4.8, (64, 6), 4.8)
    head = unary_union([ell(88, 58, 12, 9, 10), hull2((92, 56), 6, (110, 52), 4)])
    arm = hull2((74, 42), 3, (80, 36), 2.4)
    parts = [("accent", sail), ("body", tail), ("dark", legs_back[0]), ("body", body), ("belly", belly),
             ("body", leg), ("body", foot), ("body", head), ("body", arm)]
    ridges = [LineString([(40 + i * 8, 54 + 18 * math.sin(math.pi * (i + 0.6) / 5)), (40 + i * 8 + (i - 2) * 1.2, 60 + 22 * math.sin(math.pi * (i + 0.6) / 5))]) for i in range(5)]
    lines = ridges + [smile(102, 52, 5, 1.6)]
    return Model("Spinosaurus", parts, lines, eyes=[(90, 62, 2.7)], cheeks=[(86, 55, 2.8)], solids=[(108, 56, 0.9)])


DINOS = {"trex": trex, "triceratops": triceratops, "stegosaurus": stegosaurus, "longneck": longneck,
         "ptero": ptero, "ankylo": ankylo, "baby": baby_egg, "spino": spino}


# --------------------------------------------------------------------------- props
def egg():
    pts = bez((0, 20), (0, 0), (14, 0)) + bez((14, 0), (28, 0), (28, 20))[1:] + bez((28, 20), (26, 46), (14, 46))[1:] + bez((14, 46), (2, 46), (0, 20))[1:]
    g = Polygon(pts)
    spots = [("accent", ell(9, 30, 3, 2.2)), ("accent", ell(19, 18, 3.6, 2.6)), ("accent", ell(10, 10, 2.4, 1.8))]
    return Model("Egg", [("belly", g)] + spots)


def bone():
    shaft = hull2((8, 10), 4, (40, 10), 4)
    ends = [circ(5, 14, 5), circ(5, 6, 5), circ(43, 14, 5), circ(43, 6, 5)]
    return Model("Bone", [("white", unary_union([shaft] + ends))])


def volcano():
    mountain = Polygon([(0, 0), (34, 56), (52, 56), (86, 0)]).buffer(1.5)
    lava = Polygon([(34, 56), (38, 44), (42, 50), (46, 40), (50, 50), (52, 56)]).buffer(1)
    smoke = unary_union([circ(40, 66, 7), circ(50, 72, 8), circ(44, 80, 6), circ(58, 82, 7)])
    return Model("Volcano", [("white", smoke), ("dark", mountain), ("accent", lava)],
                 [LineString([(20, 10), (28, 26)]), LineString([(64, 12), (58, 30)])])


def palm():
    trunk = Polygon(bez((24, 0), (20, 30), (30, 58)) + bez((36, 58), (28, 30), (32, 0))).buffer(0.8)
    leaves = []
    for ang, ln in [(150, 30), (120, 26), (60, 26), (30, 30), (95, 22)]:
        a = math.radians(ang)
        tip = (33 + ln * math.cos(a), 60 + ln * math.sin(a) - 8)
        mid = (33 + ln * 0.5 * math.cos(a) - 4 * math.sin(a), 60 + ln * 0.5 * math.sin(a) + 6)
        leaves.append(("body", Polygon(bez((33, 60), mid, tip) + bez(tip, (mid[0], mid[1] - 10), (33, 58))).buffer(1)))
    return Model("Palm", [("dark", trunk)] + leaves + [("accent", circ(30, 56, 3.4)), ("accent", circ(37, 56, 3.4))],
                 [LineString([(25, 12), (31, 13)]), LineString([(24, 26), (30, 27)]), LineString([(26, 40), (32, 41)])])


def footprint():
    pad = ell(20, 18, 12, 14)
    toes = [ell(8, 40, 4.5, 7.5, 20), ell(20, 44, 4.5, 8), ell(32, 40, 4.5, 7.5, -20)]
    return Model("Footprint", [("dark", pad)] + [("dark", t) for t in toes])


def fern():
    stem = LineString(bez((20, 0), (18, 30), (30, 60)))
    leafs = []
    for i in range(1, 8):
        t = i / 8
        px, py = stem.interpolate(t, normalized=True).coords[0]
        for side in (-1, 1):
            leafs.append(("body", ell(px + side * 7, py + 2, 7 * (1 - t * 0.5), 2.6, side * 25)))
    return Model("Fern", leafs, [stem])


def sun():
    rays = [("accent", tri((20 + 15 * math.cos(math.radians(a - 12)), 20 + 15 * math.sin(math.radians(a - 12))),
                           (20 + 15 * math.cos(math.radians(a + 12)), 20 + 15 * math.sin(math.radians(a + 12))),
                           (20 + 24 * math.cos(math.radians(a)), 20 + 24 * math.sin(math.radians(a))), 1)) for a in range(0, 360, 30)]
    return Model("Sun", rays + [("belly", circ(20, 20, 14))], [smile(20, 17, 5, 2)], eyes=[(15, 23, 1.8), (25, 23, 1.8)],
                 cheeks=[(12, 17, 2), (28, 17, 2)])


def cloud():
    return Model("Cloud", [("white", unary_union([circ(14, 10, 10), circ(28, 16, 13), circ(42, 10, 10), hull2((10, 4), 6, (46, 4), 6)]))])


def rock():
    return Model("Rock", [("dark", Polygon([(0, 0), (4, 12), (14, 18), (26, 14), (32, 0)]).buffer(2))])


PROPS = {"egg": egg, "bone": bone, "volcano": volcano, "palm": palm, "footprint": footprint, "fern": fern,
         "sun": sun, "cloud": cloud, "rock": rock}
