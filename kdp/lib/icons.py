"""
Alphabet picture icons (original vector art). Most icons were chosen so the SAME
picture works in English and French (Ball/Ballon, Cat/Chat, Robot, Pizza, Lion...),
which lets one artwork set serve both editions.
"""
import math

from shapely import affinity
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union

from .art import Model, arc_line, bez, chain, circ, ell, hull2, smile, tri


def rbox(x0, y0, x1, y1, r):
    return box(x0 + r, y0 + r, x1 - r, y1 - r).buffer(r, join_style=1)


def face(cx, cy, s=1.0, eye_dx=6, eye_y=3):
    return dict(eyes=[(cx - eye_dx * s, cy + eye_y * s, 2.4 * s), (cx + eye_dx * s, cy + eye_y * s, 2.4 * s)],
                cheeks=[(cx - 10 * s, cy - 2 * s, 2.6 * s), (cx + 10 * s, cy - 2 * s, 2.6 * s)])


def avocado():
    outer = Polygon(bez((30, 0), (0, 2), (6, 40)) + bez((6, 40), (12, 66), (30, 70))[1:] +
                    bez((30, 70), (48, 66), (54, 40))[1:] + bez((54, 40), (60, 2), (30, 0))[1:])
    inner = affinity.scale(outer, 0.8, 0.82, origin=(30, 30))
    pit = circ(30, 22, 11)
    f = face(30, 44, 0.8)
    return Model("avocado", [("dark", outer), ("belly", inner), ("accent", pit)], [smile(30, 39, 4, 1.6)], **f)


def ball():
    b = circ(30, 30, 28)
    lines = [arc_line(30, 30, 28, 0, 360), LineString(bez((2, 30), (30, 44), (58, 30))),
             LineString(bez((30, 2), (16, 30), (30, 58))), LineString(bez((30, 2), (44, 30), (30, 58)))]
    return Model("ball", [("accent", b)], lines[1:])


def cat():
    body = ell(30, 18, 18, 16)
    tail = chain([(46, 10), (58, 16), (60, 30)], 3.5, 2.5)
    head = ell(30, 46, 19, 16)
    ears = [tri((14, 52), (16, 70), (28, 58), 1.5), tri((46, 52), (44, 70), (32, 58), 1.5)]
    f = face(30, 47, 1.0)
    whisk = [LineString([(4, 46), (16, 44)]), LineString([(4, 40), (16, 41)]), LineString([(56, 46), (44, 44)]),
             LineString([(56, 40), (44, 41)]), smile(27, 42, 3, 1.4), smile(33, 42, 3, 1.4)]
    return Model("cat", [("body", tail), ("body", body), ("body", ears[0]), ("body", ears[1]), ("body", head)], whisk,
                 **f, solids=[(30, 43.5, 1.6)])


def dice():
    top = Polygon([(10, 44), (34, 56), (58, 44), (34, 32)]).buffer(2, join_style=1)
    left = Polygon([(10, 44), (34, 32), (34, 2), (10, 14)]).buffer(2, join_style=1)
    right = Polygon([(34, 32), (58, 44), (58, 14), (34, 2)]).buffer(2, join_style=1)
    pips = [(34, 44), (22, 30), (16, 20), (22, 10)][:1] + [(28, 23)] + [(46, 30), (52, 21), (40, 12)]
    return Model("dice", [("white", left), ("belly", right), ("white", top)], [],
                 solids=[(34, 44, 2.8), (22, 32, 2.6), (16, 16, 2.6), (28, 22, 2.6), (40, 26, 2.6), (46, 18, 2.6), (52, 10, 2.6)])


def elephant():
    body = ell(40, 24, 21, 16)
    legs = [rbox(26, 0, 35, 16, 3), rbox(46, 0, 55, 16, 3)]
    tail = chain([(60, 28), (66, 22)], 1.5, 1.2)
    ear = ell(34, 40, 13, 15, -10)
    head = ell(22, 40, 15, 14)
    trunk = chain([(12, 34), (6, 24), (6, 14), (11, 9)], 5.2, 3.2)
    return Model("elephant", [("dark", tail), ("dark", legs[1]), ("body", body), ("body", legs[0]), ("accent", ear),
                              ("body", trunk), ("body", head)], [smile(22, 33, 3.4, 1.2)],
                 eyes=[(17, 43, 2.4), (27, 43, 2.4)], cheeks=[(14, 36, 2.6), (30, 36, 2.6)])


def flower():
    stem = rbox(28, 0, 32, 34, 1.8)
    leaves = [ell(20, 14, 9, 4, 30), ell(40, 18, 9, 4, -30)]
    petals = [("accent", ell(30 + 13 * math.cos(math.radians(a)), 44 + 13 * math.sin(math.radians(a)), 9, 7, a)) for a in range(0, 360, 60)]
    center = circ(30, 44, 9)
    return Model("flower", [("body", stem), ("body", leaves[0]), ("body", leaves[1])] + petals + [("belly", center)],
                 [smile(30, 41, 3.4, 1.4)], eyes=[(26.5, 46, 1.5), (33.5, 46, 1.5)])


def guitar():
    body = unary_union([circ(22, 18, 17), circ(22, 40, 12)])
    neck = rbox(19, 46, 25, 78, 1.5)
    head = rbox(16, 76, 28, 88, 3)
    hole = circ(22, 24, 6)
    bridge = rbox(15, 9, 29, 13, 1.5)
    lines = [LineString([(20.5, 12), (20.5, 80)]), LineString([(23.5, 12), (23.5, 80)])]
    return Model("guitar", [("accent", body), ("dark", neck), ("dark", head), ("white", hole), ("dark", bridge)], lines,
                 solids=[(14.5, 80, 1.5), (14.5, 85, 1.5), (29.5, 80, 1.5), (29.5, 85, 1.5)])


def hamster():
    body = ell(30, 26, 26, 24)
    ears = [circ(12, 46, 7), circ(48, 46, 7)]
    belly = ell(30, 18, 15, 12)
    paws = [ell(22, 26, 4, 3), ell(38, 26, 4, 3)]
    feet = [ell(18, 4, 6, 3.5), ell(42, 4, 6, 3.5)]
    f = face(30, 36, 1.0)
    return Model("hamster", [("accent", ears[0]), ("accent", ears[1]), ("body", feet[0]), ("body", feet[1]), ("body", body),
                             ("belly", belly), ("body", paws[0]), ("body", paws[1])],
                 [smile(27.5, 32, 2.6, 1.2), smile(32.5, 32, 2.6, 1.2)], **f, solids=[(30, 34, 1.5)])


def igloo():
    dome = Polygon(bez((0, 0), (0, 54), (40, 54)) + bez((40, 54), (80, 54), (80, 0))[1:]).buffer(1)
    door = Polygon(bez((28, 0), (28, 26), (40, 26)) + bez((40, 26), (52, 26), (52, 0))[1:])
    lines = [LineString([(4, 14), (76, 14)]), LineString([(10, 28), (70, 28)]), LineString([(22, 41), (58, 41)]),
             LineString([(16, 0), (16, 14)]), LineString([(62, 0), (62, 14)]), LineString([(26, 14), (26, 28)]),
             LineString([(56, 14), (56, 28)]), LineString([(40, 28), (40, 41)]), LineString([(30, 41), (32, 51)]),
             LineString([(50, 41), (48, 51)])]
    return Model("igloo", [("white", dome), ("dark", door)], lines)


def juice():
    glass = Polygon([(8, 60), (12, 0), (40, 0), (44, 60)]).buffer(1.5, join_style=1)
    liquid = Polygon([(10, 44), (13, 4), (39, 4), (42, 44)]).buffer(1, join_style=1)
    straw = Polygon([(28, 40), (34, 40), (44, 78), (38, 78)])
    slice_ = Polygon(bez((38, 58), (50, 74), (60, 58)) + [(49, 58)])
    f = face(26, 24, 0.8)
    return Model("juice", [("accent", straw), ("white", glass), ("belly", liquid), ("accent", slice_)],
                 [smile(26, 19, 3.4, 1.4)], **f)


def kiwi():
    outer = ell(30, 30, 28, 26)
    flesh = ell(30, 30, 23, 21)
    core = ell(30, 30, 8, 7)
    seeds = [(30 + 14 * math.cos(math.radians(a)), 30 + 13 * math.sin(math.radians(a)), 1.4) for a in range(0, 360, 30)]
    return Model("kiwi", [("dark", outer), ("body", flesh), ("belly", core)], [], solids=seeds)


def lion():
    mane = unary_union([circ(30 + 22 * math.cos(math.radians(a)), 34 + 22 * math.sin(math.radians(a)), 9) for a in range(0, 360, 30)] + [circ(30, 34, 22)])
    head = circ(30, 34, 18)
    ears = [circ(16, 48, 5), circ(44, 48, 5)]
    muzzle = ell(30, 27, 9, 6.5)
    f = face(30, 36, 1.0, eye_dx=7, eye_y=4)
    return Model("lion", [("accent", mane), ("body", ears[0]), ("body", ears[1]), ("body", head), ("belly", muzzle)],
                 [smile(27, 26, 3, 1.3), smile(33, 26, 3, 1.3)], **f, solids=[(30, 29.5, 2.2)])


def muffin():
    cup = Polygon([(6, 30), (12, 0), (48, 0), (54, 30)]).buffer(1.5, join_style=1)
    top = unary_union([circ(14, 34, 10), circ(30, 40, 14), circ(46, 34, 10), box(6, 28, 54, 34)])
    cherry = circ(30, 58, 5)
    lines = [LineString([(18, 2), (16, 28)]), LineString([(30, 2), (30, 28)]), LineString([(42, 2), (44, 28)]),
             LineString(bez((31, 62), (34, 70), (40, 72)))]
    sprinkles = [(20, 38, 1.5), (38, 44, 1.5), (44, 34, 1.5), (26, 46, 1.5), (14, 32, 1.5)]
    return Model("muffin", [("dark", cup), ("belly", top), ("accent", cherry)], lines, solids=sprinkles)


def nest():
    eggs = [ell(18, 26, 8, 11, 10), ell(30, 28, 8, 11), ell(42, 26, 8, 11, -10)]
    bowl = Polygon(bez((0, 26), (4, 0), (30, 0)) + bez((30, 0), (56, 0), (60, 26))[1:] + [(0, 26)]).buffer(1.5)
    lines = [LineString(bez((4, 20), (30, 12), (56, 20))), LineString(bez((8, 10), (30, 4), (52, 10))),
             LineString([(14, 24), (22, 14)]), LineString([(36, 22), (46, 12)])]
    return Model("nest", [("belly", g) for g in eggs] + [("dark", bowl)], lines)


def orange():
    o = circ(30, 28, 27)
    leaf = ell(40, 58, 9, 4.5, 25)
    stem = rbox(28, 53, 32, 60, 1.5)
    f = face(30, 28, 1.0)
    return Model("orange", [("dark", stem), ("body", leaf), ("accent", o)], [smile(30, 22, 4, 1.8)], **f,
                 solids=[(18, 40, 0.8), (40, 12, 0.8), (46, 34, 0.8)])


def pizza():
    slice_ = Polygon([(30, 0), (0, 56), (60, 56)]).buffer(2, join_style=1)
    crust = rbox(-2, 52, 62, 62, 5)
    pep = [circ(30, 36, 5), circ(20, 46, 4.5), circ(40, 46, 4.5), circ(30, 18, 4)]
    return Model("pizza", [("belly", slice_)] + [("accent", p) for p in pep] + [("dark", crust)], [])


def queen():
    head = circ(30, 28, 20)
    crown = Polygon([(10, 44), (10, 64), (20, 54), (30, 68), (40, 54), (50, 64), (50, 44)]).buffer(1.2)
    hair = [ell(10, 26, 6, 14), ell(50, 26, 6, 14)]
    f = face(30, 28, 1.0)
    return Model("queen", [("dark", hair[0]), ("dark", hair[1]), ("belly", head), ("accent", crown)],
                 [smile(30, 22, 4, 1.8)], **f, solids=[(20, 50, 1.6), (30, 52, 1.6), (40, 50, 1.6)])


def quille():
    pin = Polygon(bez((14, 0), (2, 30), (12, 44)) + bez((12, 44), (8, 58), (18, 64))[1:] +
                  bez((18, 64), (22, 72), (26, 64))[1:] + bez((26, 64), (36, 58), (32, 44))[1:] +
                  bez((32, 44), (42, 30), (30, 0))[1:])
    stripes = [Polygon([(10.5, 46), (33.5, 46), (32.6, 50), (11.4, 50)])]
    return Model("quille", [("white", pin)] + [("accent", s) for s in stripes], [])


def robot():
    body = rbox(10, 0, 50, 30, 4)
    head = rbox(14, 34, 46, 58, 5)
    neck = rbox(26, 28, 34, 36, 1)
    ant = rbox(29, 58, 31, 68, 0.8)
    bulb = circ(30, 70, 3.5)
    arms = [rbox(0, 6, 10, 24, 3), rbox(50, 6, 60, 24, 3)]
    panel = rbox(20, 8, 40, 22, 2)
    f = dict(eyes=[(23, 48, 3.2), (37, 48, 3.2)], cheeks=[(19, 42, 2.4), (41, 42, 2.4)])
    return Model("robot", [("dark", arms[0]), ("dark", arms[1]), ("body", body), ("belly", panel), ("dark", neck),
                           ("body", head), ("dark", ant), ("accent", bulb)], [smile(30, 41, 4, 1.4)], **f,
                 solids=[(25, 15, 1.8), (30, 15, 1.8), (35, 15, 1.8)])


def train():
    cab = rbox(30, 14, 58, 52, 3)
    roof = rbox(26, 50, 62, 56, 2)
    boiler = rbox(0, 14, 34, 36, 4)
    chimney = Polygon([(6, 36), (16, 36), (18, 50), (4, 50)]).buffer(1)
    window = rbox(36, 32, 52, 46, 2)
    wheels = [circ(10, 10, 8), circ(26, 10, 8), circ(48, 10, 9)]
    smoke = unary_union([circ(10, 58, 5), circ(16, 66, 6)])
    return Model("train", [("white", smoke), ("accent", chimney), ("body", boiler), ("dark", cab), ("accent", roof),
                           ("white", window)] + [("belly", w) for w in wheels], [],
                 solids=[(10, 10, 2.2), (26, 10, 2.2), (48, 10, 2.4)])


def ukulele():
    g = guitar()
    g = Model("ukulele", [(r, affinity.scale(geom, 0.9, 0.82, origin=(22, 0))) for r, geom in g.parts],
              [affinity.scale(l, 0.9, 0.82, origin=(22, 0)) for l in g.lines],
              solids=[(x * 0.9 + 22 * 0.1, y * 0.82, r) for x, y, r in g.solids])
    g.parts[0] = ("body", g.parts[0][1])
    return g


def volcano_icon():
    from .art import volcano
    return volcano()


def wagon():
    tub = Polygon([(4, 16), (8, 38), (52, 38), (56, 16)]).buffer(1.5, join_style=1)
    handle = chain([(56, 30), (66, 46), (70, 54)], 1.8, 1.8)
    grip = rbox(64, 52, 76, 58, 2.5)
    wheels = [circ(16, 10, 9), circ(44, 10, 9)]
    lines = [LineString([(12, 30), (48, 30)])]
    return Model("wagon", [("dark", handle), ("dark", grip), ("accent", tub)] + [("belly", w) for w in wheels], lines,
                 solids=[(16, 10, 2.4), (44, 10, 2.4)])


def xylophone():
    frame = Polygon([(0, 8), (70, 18), (70, 12), (0, 2)]).buffer(1)
    bars = [("accent" if i % 2 else "body", rbox(4 + i * 11, 6 + i * 1.6, 12 + i * 11, 40 - i * 2.5 + i * 1.6, 2)) for i in range(6)]
    sticks = [chain([(30, 52), (50, 70)], 1.4, 1.4), chain([(44, 50), (64, 64)], 1.4, 1.4)]
    heads = [circ(30, 52, 4), circ(44, 50, 4)]
    return Model("xylophone", bars + [("dark", frame), ("dark", sticks[0]), ("dark", sticks[1]), ("belly", heads[0]),
                                      ("belly", heads[1])], [], solids=[(8 + i * 11, 10 + i * 1.6, 1.2) for i in range(6)])


def yoyo():
    disc = circ(30, 24, 22)
    inner = circ(30, 24, 13)
    string = LineString(bez((30, 46), (34, 64), (28, 80)))
    ring = arc_line(28, 84, 4, 0, 360)
    f = face(30, 24, 0.7)
    return Model("yoyo", [("accent", disc), ("belly", inner)], [string, ring, smile(30, 20.5, 3, 1.3)], **f)


def zebra():
    head = Polygon(bez((16, 58), (2, 30), (14, 8)) + bez((14, 8), (30, -4), (46, 8))[1:] + bez((46, 8), (58, 30), (44, 58))[1:] +
                   bez((44, 58), (30, 66), (16, 58))[1:]).buffer(0.5)
    muzzle = ell(30, 14, 15, 11)
    ears = [tri((16, 56), (8, 76), (24, 62), 1.5), tri((44, 56), (52, 76), (36, 62), 1.5)]
    mane = unary_union([circ(30, 62 + i * 0.1, 5) for i in range(1)] + [circ(24, 64, 4.5), circ(36, 64, 4.5)])
    stripes = [Polygon([(9, 40), (22, 44), (22, 40), (8, 34)]), Polygon([(51, 40), (38, 44), (38, 40), (52, 34)]),
               Polygon([(12, 26), (20, 28), (20, 24), (12, 21)]), Polygon([(48, 26), (40, 28), (40, 24), (48, 21)]),
               Polygon([(26, 56), (30, 46), (34, 56)])]
    f = dict(eyes=[(22, 34, 2.6), (38, 34, 2.6)], cheeks=[(16, 26, 2.6), (44, 26, 2.6)])
    return Model("zebra", [("white", ears[0]), ("white", ears[1]), ("dark", mane), ("white", head)] +
                 [("dark", s) for s in stripes] + [("belly", muzzle)], [smile(30, 10, 4, 1.6)], **f,
                 solids=[(25, 16, 1.6), (35, 16, 1.6)])


ICONS = {f.__name__.replace("_icon", ""): f for f in
         [avocado, ball, cat, dice, elephant, flower, guitar, hamster, igloo, juice, kiwi, lion, muffin, nest, orange,
          pizza, queen, quille, robot, train, ukulele, volcano_icon, wagon, xylophone, yoyo, zebra]}


def sun_icon():
    from .art import sun
    return sun()


ICONS["sun"] = sun_icon

# letter -> (icon, english word, french icon, french word)
ALPHABET = [
    ("A", "avocado", "avocado", "avocado", "avocat"), ("B", "ball", "ball", "ball", "ballon"),
    ("C", "cat", "cat", "cat", "chat"), ("D", "dice", "dice", "dice", "dé"),
    ("E", "elephant", "elephant", "elephant", "éléphant"), ("F", "flower", "flower", "flower", "fleur"),
    ("G", "guitar", "guitar", "guitar", "guitare"), ("H", "hamster", "hamster", "hamster", "hamster"),
    ("I", "igloo", "igloo", "igloo", "igloo"), ("J", "juice", "juice", "juice", "jus"),
    ("K", "kiwi", "kiwi", "kiwi", "kiwi"), ("L", "lion", "lion", "lion", "lion"),
    ("M", "muffin", "muffin", "muffin", "muffin"), ("N", "nest", "nest", "nest", "nid"),
    ("O", "orange", "orange", "orange", "orange"), ("P", "pizza", "pizza", "pizza", "pizza"),
    ("Q", "queen", "queen", "quille", "quille"), ("R", "robot", "robot", "robot", "robot"),
    ("S", "sun", "sun", "sun", "soleil"), ("T", "train", "train", "train", "train"),
    ("U", "ukulele", "ukulele", "ukulele", "ukulélé"), ("V", "volcano", "volcano", "volcano", "volcan"),
    ("W", "wagon", "wagon", "wagon", "wagon"), ("X", "xylophone", "xylophone", "xylophone", "xylophone"),
    ("Y", "yoyo", "yo-yo", "yoyo", "yoyo"), ("Z", "zebra", "zebra", "zebra", "zèbre"),
]
