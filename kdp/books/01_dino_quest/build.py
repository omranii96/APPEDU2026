"""
Book 1 - DINO QUEST Activity Book for Kids Ages 4-8 (EN + FR editions)
KDP paperback, 8.5 x 11 in, black ink on white paper, no bleed, 108 pages.

    python3 -m books.01_dino_quest.build   (run from kdp/)  ->  out/01_dino_quest/<lang>/
"""
import math
import os
import random
import sys

from reportlab.lib.colors import black, white
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from shapely import affinity
from shapely.geometry import box as sbox
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
KDP = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, KDP)

from lib import art as A  # noqa: E402
from lib import kdpkit as K  # noqa: E402
from lib import puzzles as P  # noqa: E402
from lib import strokes as S  # noqa: E402
from text import TEXT  # noqa: E402

W, H = 8.5 * inch, 11 * inch
GUTTER, OUTER, TOP, BOTTOM = 0.75 * inch, 0.55 * inch, 0.55 * inch, 0.6 * inch
TARGET_PAGES = 108
K.ARROW_COLOR = K.hex_color("#3a3a3a")  # black-ink interior: no colour anywhere
GREY = K.hex_color("#6b6b6b")
SOFT = K.hex_color("#e9e9e9")
MID = K.hex_color("#bdbdbd")
DINO_KEYS = ["trex", "triceratops", "stegosaurus", "longneck", "ptero", "ankylo", "spino", "baby"]
SEC_ICON = {"maze": "footprint", "dots": "egg", "ws": "bone", "trace": "fern", "count": "egg", "add": "egg",
            "shadow": "sun", "odd": "footprint", "half": "fern", "cbn": "sun", "spot": "volcano", "color": "palm",
            "answers": "bone"}


def model(key):
    return (A.DINOS.get(key) or A.PROPS.get(key))()


class Book:
    def __init__(self, lang, out_dir):
        self.lang = lang
        self.t = TEXT[lang]
        self.path = os.path.join(out_dir, f"DinoQuest_{lang.upper()}_Interior_8.5x11.pdf")
        self.c = K.new_canvas(self.path, W, H, self.t["full_title"], self.t["author"])
        self.page = 0
        self.answers = []  # (kind, page, payload)
        self.rnd = random.Random(2026)
        self.page_open = False

    # ------------------------------------------------------------------ frame
    def box(self):
        """Live area for the current page (mirrors gutter on left/right pages)."""
        right_page = (self.page % 2 == 1)
        x0 = GUTTER if right_page else OUTER
        x1 = W - (OUTER if right_page else GUTTER)
        return x0, BOTTOM, x1, H - TOP

    def new_page(self, sec=None, instruction=None, level=None, header=True, number=True):
        if self.page_open:
            self.c.showPage()
        self.page += 1
        self.page_open = True
        x0, y0, x1, y1 = self.box()
        c = self.c
        top = y1
        if sec and header:
            bh = 0.62 * inch
            c.setFillColor(SOFT)
            c.setStrokeColor(black)
            c.setLineWidth(1.6)
            c.roundRect(x0, y1 - bh, x1 - x0, bh, 0.22 * inch, stroke=1, fill=1)
            A.place(c, model(SEC_ICON.get(sec, "egg")), x0 + 0.1 * inch, y1 - bh + 0.08 * inch, 0.48 * inch, bh - 0.16 * inch, lw=1.0)
            title = self.t["sec"][sec]
            c.setFillColor(black)
            c.setFont("Title", 25)
            c.drawString(x0 + 0.68 * inch, y1 - bh + 0.18 * inch, title)
            if level:
                lab = self.t["levels"][level]
                stars = {"easy": 1, "medium": 2, "hard": 3}[level]
                c.setFont("Round", 12)
                lw_ = stringWidth(lab, "Round", 12)
                rx = x1 - 0.18 * inch - stars * 0.27 * inch
                c.drawRightString(rx - 0.06 * inch, y1 - bh + 0.24 * inch, lab)
                for i in range(stars):
                    K.poly(c, K.star_points(rx + (i + 0.5) * 0.27 * inch, y1 - bh / 2, 0.12 * inch, 0.055 * inch),
                           fill=black, stroke=None)
            top = y1 - bh - 0.12 * inch
            if instruction:
                size = K.fit_size(instruction, "Round", x1 - x0, 15)
                c.setFont("Round", size)
                c.setFillColor(black)
                c.drawCentredString((x0 + x1) / 2, top - 0.2 * inch, instruction)
                top -= 0.36 * inch
        if number:
            cx = (x0 + x1) / 2
            c.setFillColor(black)
            c.circle(cx, 0.36 * inch, 0.15 * inch, stroke=0, fill=1)
            c.setFillColor(white)
            c.setFont("RoundBold", 10)
            c.drawCentredString(cx, 0.32 * inch, str(self.page))
        c.setFillColor(black)
        c.setStrokeColor(black)
        return x0, y0 + 0.15 * inch, x1, top

    def finish(self):
        if self.page_open:
            self.c.showPage()
        self.c.save()

    # ------------------------------------------------------------------ front matter
    def belongs_page(self):
        x0, y0, x1, y1 = self.new_page(number=False)
        c = self.c
        cx = (x0 + x1) / 2
        A.place(c, model("trex"), x0 + 0.3 * inch, y1 - 4.6 * inch, x1 - x0 - 0.6 * inch, 4.2 * inch, lw=3)
        K.text_center(c, self.t["belongs"], cx, y1 - 5.4 * inch, "Title", 34, x1 - x0)
        c.setLineWidth(2)
        c.setDash(2, 5)
        c.line(x0 + 0.6 * inch, y1 - 6.5 * inch, x1 - 0.6 * inch, y1 - 6.5 * inch)
        c.setDash()
        K.text_center(c, self.t["belongs_sub"], cx, y1 - 7.2 * inch, "Round", 20, x1 - x0)
        for i, k in enumerate(["egg", "footprint", "bone", "fern", "egg"]):
            A.place(c, model(k), x0 + i * (x1 - x0) / 5 + 0.25 * inch, y0 + 0.1 * inch, (x1 - x0) / 5 - 0.5 * inch, 1.1 * inch, lw=1.4)

    def copyright_page(self):
        x0, y0, x1, y1 = self.new_page(number=False)
        c = self.c
        c.setFont("Title", 26)
        c.setFillColor(black)
        c.drawString(x0, y1 - 0.4 * inch, self.t["grownups_title"])
        y = y1 - 0.75 * inch
        for ptxt in self.t["grownups"]:
            y = K.paragraph(c, "•  " + ptxt, x0, y, "Body", 12.5, x1 - x0, 1.4) - 0.14 * inch
        A.place(c, model("stegosaurus"), x0 + 1.2 * inch, y - 3.2 * inch, x1 - x0 - 2.4 * inch, 2.9 * inch, lw=2)
        yy = y0 + 1.25 * inch
        for line in self.t["copyright"]:
            c.setFont("Body", 9)
            c.setFillColor(GREY)
            c.drawCentredString((x0 + x1) / 2, yy, line)
            yy -= 0.19 * inch

    def map_page(self):
        x0, y0, x1, y1 = self.new_page(number=True)
        c = self.c
        cx = (x0 + x1) / 2
        K.text_center(c, self.t["map_title"], cx, y1 - 0.45 * inch, "Title", 34, x1 - x0)
        K.text_center(c, self.t["map_sub"], cx, y1 - 0.85 * inch, "Round", 14, x1 - x0)
        # winding trail of 22 footprints (one per ~5 pages)
        pts = []
        rows = 5
        top, bot = y1 - 1.6 * inch, y0 + 1.55 * inch
        for r in range(rows):
            yy = top - r * (top - bot) / (rows - 1)
            xs = [x0 + 0.75 * inch + i * (x1 - x0 - 1.5 * inch) / 4 for i in range(5)]
            if r % 2:
                xs = xs[::-1]
            for xx in (xs if r < rows - 1 else xs[:3]):
                pts.append((xx, yy))
        c.setStrokeColor(MID)
        c.setLineWidth(10)
        c.setLineCap(1)
        c.setLineJoin(1)
        p = c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, stroke=1, fill=0)
        fp = model("footprint")
        for i, (px, py) in enumerate(pts):
            A.place(c, fp, px - 0.32 * inch, py - 0.32 * inch, 0.64 * inch, 0.64 * inch, lw=1.6)
            c.setFont("RoundBold", 9)
            c.setFillColor(black)
            c.drawCentredString(px, py - 0.5 * inch, str(i + 1))
        A.place(c, model("volcano"), x1 - 1.9 * inch, y0 + 0.05 * inch, 1.5 * inch, 1.3 * inch, lw=1.6)
        A.place(c, model("baby"), x0 + 0.1 * inch, y0 + 0.05 * inch, 1.2 * inch, 1.3 * inch, lw=1.6)
        c.setFont("Title", 16)
        c.drawCentredString(pts[0][0], pts[0][1] + 0.42 * inch, self.t["map_start"])
        c.drawCentredString(pts[-1][0], pts[-1][1] + 0.42 * inch, self.t["map_end"])

    def meet_page(self):
        x0, y0, x1, y1 = self.new_page()
        c = self.c
        K.text_center(c, self.t["meet"], (x0 + x1) / 2, y1 - 0.45 * inch, "Title", 30, x1 - x0)
        cw, ch = (x1 - x0) / 2, (y1 - 0.75 * inch - y0) / 4
        for i, k in enumerate(DINO_KEYS):
            col, row = i % 2, i // 2
            bx, by = x0 + col * cw, y1 - 0.75 * inch - (row + 1) * ch
            c.setLineWidth(1.4)
            c.setStrokeColor(black)
            c.roundRect(bx + 0.06 * inch, by + 0.06 * inch, cw - 0.12 * inch, ch - 0.12 * inch, 0.16 * inch)
            A.place(c, model(k), bx + 0.15 * inch, by + 0.2 * inch, 1.45 * inch, ch - 0.4 * inch, lw=1.3)
            tx = bx + 1.7 * inch
            tw = cw - 1.85 * inch
            c.setFillColor(black)
            c.setFont("Title", 18)
            c.drawString(tx, by + ch - 0.45 * inch, self.t["names"][k])
            c.setFont("Round", 10.5)
            c.drawString(tx, by + ch - 0.66 * inch, self.t["species"][k])
            K.paragraph(c, self.t["facts"][k], tx, by + ch - 0.78 * inch, "Body", 10, tw, 1.25)

    # ------------------------------------------------------------------ activities
    def maze(self, level, idx):
        dims = {"easy": (7, 8), "medium": (11, 13), "hard": (15, 18)}[level]
        k = DINO_KEYS[idx % 7]
        name = self.t["names"][k]
        x0, y0, x1, y1 = self.new_page("maze", self.t["ins"]["maze"].format(name=name), level)
        cols, rows = dims
        avail_w, avail_h = x1 - x0 - 2.0 * inch, y1 - y0 - 0.4 * inch
        cell = min(avail_w / cols, avail_h / rows)
        mw, mh = cols * cell, rows * cell
        mx = x0 + (x1 - x0 - mw) / 2
        my = y0 + (y1 - y0 - mh) / 2
        opened = P.make_maze(cols, rows, seed=1000 + idx * 31 + len(level))
        P.draw_maze(self.c, opened, cols, rows, mx, my, cell, lw=2.6 if level == "easy" else 2.0)
        A.place(self.c, model(k), mx - 1.0 * inch, my - 0.05 * inch, 0.95 * inch, 1.0 * inch, lw=1.4)
        A.place(self.c, model("egg"), mx + mw + 0.12 * inch, my + mh - 0.95 * inch, 0.8 * inch, 0.9 * inch, lw=1.4)
        sol = P.solve_maze(opened, (0, 0), (cols - 1, rows - 1))
        self.answers.append(("maze", self.page, (opened, cols, rows, sol)))

    def dots(self, idx, n):
        k = ["trex", "triceratops", "stegosaurus", "longneck", "ankylo", "spino", "ptero", "baby",
             "volcano", "palm", "egg", "bone"][idx % 12]
        x0, y0, x1, y1 = self.new_page("dots", self.t["ins"]["dots"].format(n=n),
                                       "easy" if n <= 25 else "medium" if n <= 40 else "hard")
        m = model(k)
        flip = (idx % 2 == 1)
        bx, by, bw, bh = x0 + 0.35 * inch, y0 + 0.3 * inch, x1 - x0 - 0.7 * inch, y1 - y0 - 0.6 * inch
        g = A.transformed_union(m, bx, by, bw, bh, flip=flip)
        c = self.c
        # inner details are pre-drawn (eyes, belly, legs...) - only the outer contour is dots,
        # so the child sees the dino "appear" and stays motivated.
        sc, ox, oy = A.placement(m, bx, by, bw, bh, flip=flip)
        inner = g.buffer(-0.07 * inch)
        c.saveState()
        c.clipPath(K.geom_path(c, inner), stroke=0, fill=0)
        A.render(c, m, ox, oy, sc, mode="line", lw=1.8, flip=flip)
        c.restoreState()
        pts, (cx, cy) = P.dots_from_outline(g, n)
        fs = 13 if n <= 25 else 11.5 if n <= 40 else 10.5
        for i, (px, py) in enumerate(pts):
            c.setFillColor(black)
            c.circle(px, py, 3.0 if i else 4.6, stroke=0, fill=1)
            ang = math.atan2(py - cy, px - cx)
            lx, ly = px + math.cos(ang) * 0.2 * inch, py + math.sin(ang) * 0.2 * inch - fs * 0.35
            c.setFont("RoundBold", fs)
            c.drawCentredString(lx, ly, str(i + 1))

    def wordsearch(self, idx):
        words = self.t["ws_lists"][idx]
        level = "easy" if idx < 2 else "medium" if idx < 5 else "hard"
        n = {"easy": 8, "medium": 10, "hard": 12}[level]
        dirs = {"easy": P.DIRS_EASY, "medium": P.DIRS_MED, "hard": P.DIRS_HARD}[level]
        x0, y0, x1, y1 = self.new_page("ws", self.t["ins"]["ws"], level)
        c = self.c
        K.text_center(c, self.t["ws_titles"][idx], (x0 + x1) / 2, y1 - 0.35 * inch, "Title", 24, x1 - x0)
        grid, placed = P.make_wordsearch(words, n, dirs, seed=77 + idx * 13)
        gw = min(x1 - x0 - 0.6 * inch, 5.6 * inch)
        cell = gw / n
        gx = x0 + (x1 - x0 - gw) / 2
        gy = y1 - 0.65 * inch - gw
        self._ws_grid(grid, gx, gy, cell, n, placed=None)
        # word list with check boxes
        cols = 2 if len(words) > 4 else 1
        ly = gy - 0.45 * inch
        colw = (x1 - x0) / cols
        for i, w in enumerate(words):
            col, row = i % cols, i // cols
            tx = x0 + col * colw + colw / 2 - 1.2 * inch
            ty = ly - row * 0.42 * inch
            c.setLineWidth(1.4)
            c.rect(tx, ty - 0.04 * inch, 0.22 * inch, 0.22 * inch)
            c.setFont("RoundBold", 17)
            c.setFillColor(black)
            c.drawString(tx + 0.35 * inch, ty, w)
        self.answers.append(("ws", self.page, (grid, placed, n)))

    def _ws_grid(self, grid, gx, gy, cell, n, placed=None, font_scale=0.56):
        c = self.c
        c.setLineWidth(1.6)
        c.setStrokeColor(black)
        c.roundRect(gx - 0.08 * inch, gy - 0.08 * inch, n * cell + 0.16 * inch, n * cell + 0.16 * inch, 0.12 * inch)
        if placed:
            c.saveState()
            c.setStrokeColor(MID)
            c.setLineCap(1)
            c.setLineWidth(cell * 0.72)
            for (w, r, cc, dx, dy) in placed:
                sx, sy = gx + (cc + 0.5) * cell, gy + (n - r - 0.5) * cell
                ex = gx + (cc + dx * (len(w) - 1) + 0.5) * cell
                ey = gy + (n - (r + dy * (len(w) - 1)) - 0.5) * cell
                c.line(sx, sy, ex, ey)
            c.restoreState()
        c.setFillColor(black)
        c.setFont("RoundBold", cell * font_scale)
        for r in range(n):
            for cc in range(n):
                c.drawCentredString(gx + (cc + 0.5) * cell, gy + (n - r - 0.5) * cell - cell * font_scale * 0.36, grid[r][cc])

    def trace_paths(self, idx):
        x0, y0, x1, y1 = self.new_page("trace", self.t["ins"]["trace_path"], "easy")
        c = self.c
        rows = 4
        rh = (y1 - y0) / rows
        kinds = [["line", "zigzag", "wave", "loops"], ["mountain", "castle", "wave", "spiral"],
                 ["zigzag", "loops", "castle", "wave"], ["line", "mountain", "spiral", "loops"]][idx % 4]
        for r, kind in enumerate(kinds):
            cy = y1 - (r + 0.5) * rh
            dk = DINO_KEYS[(idx * 4 + r) % 8]
            A.place(c, model(dk), x0, cy - 0.55 * inch, 1.15 * inch, 1.1 * inch, lw=1.3)
            A.place(c, model("egg"), x1 - 0.75 * inch, cy - 0.45 * inch, 0.7 * inch, 0.9 * inch, lw=1.3)
            sx, ex = x0 + 1.3 * inch, x1 - 0.9 * inch
            amp = rh * 0.28
            pts = []
            N = 240
            for i in range(N + 1):
                t = i / N
                xx = sx + (ex - sx) * t
                if kind == "line":
                    yy = cy
                elif kind == "zigzag":
                    ph = (t * 5) % 1
                    yy = cy + amp * (4 * abs(ph - 0.5) - 1)
                elif kind == "wave":
                    yy = cy + amp * math.sin(t * 2 * math.pi * 3)
                elif kind == "mountain":
                    ph = (t * 3) % 1
                    yy = cy - amp + 2 * amp * (1 - abs(2 * ph - 1)) ** 1.0
                elif kind == "castle":
                    ph = (t * 5) % 1
                    yy = cy + (amp if ph < 0.5 else -amp)
                    if pts and abs(pts[-1][1] - yy) > 1:
                        pts.append((xx, pts[-1][1]))
                elif kind == "loops":
                    a = t * 2 * math.pi * 5
                    xx = sx + (ex - sx) * t - amp * 0.55 * math.sin(a)
                    yy = cy + amp * 0.8 * math.cos(a) * -1
                elif kind == "spiral":
                    a = t * 2 * math.pi * 4
                    xx = sx + (ex - sx) * t + amp * 0.5 * math.sin(a)
                    yy = cy + amp * 0.75 * math.cos(a) * (0.4 + 0.6 * abs(math.sin(math.pi * t)))
                pts.append((xx, yy))
            c.saveState()
            c.setLineCap(1)
            c.setLineJoin(1)
            c.setLineWidth(3.2)
            c.setStrokeColor(K.GRAY)
            c.setDash(5, 6)
            p = c.beginPath()
            p.moveTo(*pts[0])
            for q in pts[1:]:
                p.lineTo(*q)
            c.drawPath(p, stroke=1, fill=0)
            c.setDash()
            c.setFillColor(black)
            c.circle(pts[0][0], pts[0][1], 5, stroke=0, fill=1)
            c.restoreState()

    def trace_names(self, idx):
        x0, y0, x1, y1 = self.new_page("trace", self.t["ins"]["trace_name"], "medium")
        c = self.c
        words = self.t["trace_words"][idx * 2: idx * 2 + 2]
        bh = (y1 - y0) / 2
        for i, w in enumerate(words):
            by = y1 - (i + 1) * bh
            A.place(c, model(DINO_KEYS[(idx * 2 + i) % 8]), x0, by + bh - 1.55 * inch, 1.6 * inch, 1.45 * inch, lw=1.5)
            unit = 0.36 * inch if w.isupper() else 0.4 * inch
            # big model word with numbered strokes
            mx = x0 + 1.9 * inch
            K.guide_lines(c, mx - 0.1 * inch, x1, by + bh - 1.25 * inch, unit, descender=False)
            K.draw_text_strokes(c, w, mx, by + bh - 1.25 * inch, unit, style="solid", numbered=True, arrows=True,
                                lw=unit * 0.14)
            # tracing rows
            for r in range(3):
                base = by + bh - 2.3 * inch - r * 0.98 * inch
                K.guide_lines(c, x0, x1, base, unit * 0.82)
                if r < 2:
                    xx = x0 + 0.15 * inch
                    ww = S.text_width(w) * unit * 0.82
                    while xx + ww < x1 - 0.1 * inch:
                        K.draw_text_strokes(c, w, xx, base, unit * 0.82, style="dashed", lw=unit * 0.1)
                        xx += ww + 0.55 * inch

    def scatter(self, item, n, bx, by, bw, bh, size, seed):
        rnd = random.Random(seed)
        placed = []
        tries = 0
        while len(placed) < n and tries < 5000:
            tries += 1
            px = bx + rnd.uniform(0, bw - size)
            py = by + rnd.uniform(0, bh - size)
            if all(abs(px - qx) > size * 1.02 or abs(py - qy) > size * 1.02 for qx, qy in placed):
                placed.append((px, py))
        for (px, py) in placed:
            A.place(self.c, model(item), px, py, size, size, lw=1.3, flip=rnd.random() < 0.5)
        return len(placed)

    def count_page(self, idx):
        x0, y0, x1, y1 = self.new_page("count", self.t["ins"]["count"], "easy" if idx < 4 else "medium")
        c = self.c
        items = ["egg", "bone", "footprint", "fern"]
        cw, ch = (x1 - x0) / 2, (y1 - y0) / 2
        res = []
        for i in range(4):
            col, row = i % 2, i // 2
            bx, by = x0 + col * cw, y1 - (row + 1) * ch
            c.setLineWidth(1.6)
            c.roundRect(bx + 0.08 * inch, by + 0.08 * inch, cw - 0.16 * inch, ch - 0.16 * inch, 0.18 * inch)
            item = items[(i + idx) % 4]
            n = random.Random(idx * 10 + i).randint(3 if idx < 4 else 6, 7 if idx < 4 else 12)
            got = self.scatter(item, n, bx + 0.25 * inch, by + 1.0 * inch, cw - 0.5 * inch, ch - 1.25 * inch,
                               0.62 * inch if idx < 4 else 0.52 * inch, seed=idx * 100 + i)
            res.append(got)
            c.setFont("Round", 13)
            c.drawString(bx + 0.3 * inch, by + 0.45 * inch, self.t["count_items"][item] + " :")
            c.setLineWidth(2)
            c.roundRect(bx + cw - 1.25 * inch, by + 0.28 * inch, 0.85 * inch, 0.6 * inch, 0.1 * inch)
        self.answers.append(("count", self.page, res))

    def add_page(self, idx):
        x0, y0, x1, y1 = self.new_page("add", self.t["ins"]["add"], "medium")
        c = self.c
        rows = 4
        rh = (y1 - y0) / rows
        rnd = random.Random(500 + idx)
        res = []
        item = ["egg", "bone", "footprint", "fern"][idx % 4]
        for r in range(rows):
            a, b = rnd.randint(1, 5), rnd.randint(1, 4)
            res.append(a + b)
            cy = y1 - (r + 0.5) * rh
            sz = 0.6 * inch
            xx = x0
            for grp, n in enumerate((a, b)):
                gw = 3 * sz
                rows_n = 1 if n <= 3 else 2
                for k in range(n):
                    gx = xx + (k % 3) * sz
                    gy = cy - sz / 2 + (0 if rows_n == 1 else (sz * 0.55 if k < 3 else -sz * 0.55))
                    A.place(c, model(item), gx + sz * 0.05, gy, sz * 0.9, sz * 0.9, lw=1.3)
                c.setFillColor(black)
                c.setFont("RoundBold", 15)
                c.drawCentredString(xx + gw / 2, cy - rh / 2 + 0.12 * inch, str(n))
                xx += gw + 0.1 * inch
                if grp == 0:
                    c.setFont("Title", 38)
                    c.drawCentredString(xx + 0.22 * inch, cy - 0.17 * inch, "+")
                    xx += 0.55 * inch
            c.setFont("Title", 38)
            c.drawCentredString(xx + 0.2 * inch, cy - 0.17 * inch, "=")
            c.setLineWidth(2)
            c.roundRect(xx + 0.6 * inch, cy - 0.45 * inch, 0.95 * inch, 0.9 * inch, 0.12 * inch)
            if r < rows - 1:
                c.setStrokeColor(MID)
                c.setDash(2, 4)
                c.line(x0, cy - rh / 2, x1, cy - rh / 2)
                c.setDash()
                c.setStrokeColor(black)
        self.answers.append(("add", self.page, res))

    def shadow_page(self, idx):
        x0, y0, x1, y1 = self.new_page("shadow", self.t["ins"]["shadow"], "easy")
        c = self.c
        keys = DINO_KEYS[idx * 2 % 8:] + DINO_KEYS[:idx * 2 % 8]
        keys = keys[:4]
        order = list(range(4))
        random.Random(idx + 3).shuffle(order)
        if order == list(range(4)):
            order = order[::-1]
        rh = (y1 - y0) / 4
        for i, k in enumerate(keys):
            cy = y1 - (i + 1) * rh
            A.place(c, model(k), x0 + 0.1 * inch, cy + 0.1 * inch, 2.4 * inch, rh - 0.2 * inch, lw=1.6)
            c.circle(x0 + 2.75 * inch, cy + rh / 2, 5, stroke=0, fill=1)
        for j, i in enumerate(order):
            cy = y1 - (j + 1) * rh
            A.place(c, model(keys[i]), x1 - 2.5 * inch, cy + 0.1 * inch, 2.4 * inch, rh - 0.2 * inch, mode="silhouette")
            c.circle(x1 - 2.75 * inch, cy + rh / 2, 5, stroke=0, fill=1)
        self.answers.append(("shadow", self.page, [(i + 1, order.index(i) + 1) for i in range(4)]))

    def odd_page(self, idx):
        x0, y0, x1, y1 = self.new_page("odd", self.t["ins"]["odd"], "easy" if idx < 2 else "medium")
        c = self.c
        rh = (y1 - y0) / 4
        res = []
        for r in range(4):
            k = (DINO_KEYS + ["volcano", "palm", "sun"])[(idx * 4 + r) % 11]
            odd = random.Random(idx * 7 + r).randint(0, 3)
            cy = y1 - (r + 1) * rh
            cw = (x1 - x0) / 4
            for i in range(4):
                m = model(k)
                if i == odd:
                    if idx % 2 == 0 or not m.eyes:
                        A.place(c, m, x0 + i * cw + 0.1 * inch, cy + 0.15 * inch, cw - 0.2 * inch, rh - 0.3 * inch, lw=1.4, flip=True)
                    else:  # subtle: missing details
                        m.lines = m.lines[1:]
                        m.eyes = []
                        A.place(c, m, x0 + i * cw + 0.1 * inch, cy + 0.15 * inch, cw - 0.2 * inch, rh - 0.3 * inch, lw=1.4)
                else:
                    A.place(c, m, x0 + i * cw + 0.1 * inch, cy + 0.15 * inch, cw - 0.2 * inch, rh - 0.3 * inch, lw=1.4)
            res.append(odd + 1)
        self.answers.append(("odd", self.page, res))

    def half_page(self, idx):
        k = ["baby", "sun", "egg", "volcano"][idx % 4]
        x0, y0, x1, y1 = self.new_page("half", self.t["ins"]["half"], "hard")
        c = self.c
        K.text_center(c, self.t["half_names"][k], (x0 + x1) / 2, y1 - 0.4 * inch, "Title", 24)
        n = 8
        size = min(x1 - x0 - 0.4 * inch, y1 - y0 - 0.8 * inch)
        cell = size / n
        gx, gy = x0 + (x1 - x0 - size) / 2, y0 + (y1 - 0.6 * inch - y0 - size) / 2
        c.saveState()
        p = c.beginPath()
        p.rect(gx, gy, size / 2, size)
        c.clipPath(p, stroke=0, fill=0)
        A.place(c, model(k), gx + 0.3 * inch, gy + 0.3 * inch, size - 0.6 * inch, size - 0.6 * inch, lw=2.6)
        c.restoreState()
        c.setStrokeColor(MID)
        c.setLineWidth(0.9)
        for i in range(n + 1):
            c.line(gx + i * cell, gy, gx + i * cell, gy + size)
            c.line(gx, gy + i * cell, gx + size, gy + i * cell)
        c.setStrokeColor(black)
        c.setLineWidth(2.2)
        c.setDash(6, 4)
        c.line(gx + size / 2, gy - 0.1 * inch, gx + size / 2, gy + size + 0.1 * inch)
        c.setDash()
        c.rect(gx, gy, size, size)

    def cbn_page(self, idx):
        k = ["trex", "triceratops", "stegosaurus", "longneck", "spino", "ankylo"][idx % 6]
        x0, y0, x1, y1 = self.new_page("cbn", self.t["ins"]["cbn"], "medium")
        c = self.c
        m = model(k)
        bx, by, bw, bh = x0 + 0.2 * inch, y0 + 1.25 * inch, x1 - x0 - 0.4 * inch, y1 - y0 - 1.4 * inch
        s, mx0, my0, mx1, my1 = A.fit(m, bw, bh)
        w_, h_ = (mx1 - mx0) * s, (my1 - my0) * s
        ox, oy = bx + (bw - w_) / 2 - mx0 * s, by + (bh - h_) / 2 - my0 * s
        A.render(c, m, ox, oy, s, mode="line", lw=2.2)
        # number each visible region at its pole of inaccessibility
        roles = ["body", "belly", "accent", "dark"]
        tr = [affinity.translate(affinity.scale(g, s, s, origin=(0, 0)), ox, oy) for _, g in m.parts]
        for i, (role, _) in enumerate(m.parts):
            vis = tr[i].difference(unary_union(tr[i + 1:])) if i + 1 < len(tr) else tr[i]
            if vis.is_empty:
                continue
            geoms = vis.geoms if vis.geom_type == "MultiPolygon" else [vis]
            for gpart in geoms:
                if gpart.area < (0.18 * inch) ** 2:
                    continue
                from shapely.ops import polylabel
                try:
                    pt = polylabel(gpart.buffer(0), tolerance=1)
                except Exception:
                    pt = gpart.representative_point()
                num = str(roles.index(role if role in roles else "body") + 1)
                c.setFillColor(black)
                c.setFont("RoundBold", 12 if gpart.area > (0.5 * inch) ** 2 else 9)
                c.drawCentredString(pt.x, pt.y - 4, num)
        # colour key
        kw = (x1 - x0) / 4
        for i, role in enumerate(roles):
            kx = x0 + i * kw
            c.setLineWidth(1.6)
            c.circle(kx + 0.35 * inch, y0 + 0.5 * inch, 0.24 * inch)
            c.setFont("Title", 18)
            c.drawCentredString(kx + 0.35 * inch, y0 + 0.43 * inch, str(i + 1))
            c.setFont("Round", 14)
            c.drawString(kx + 0.7 * inch, y0 + 0.44 * inch, self.t["colors"][role])

    def spot_page(self, idx):
        x0, y0, x1, y1 = self.new_page("spot", self.t["ins"]["spot"], "hard")
        c = self.c
        rnd = random.Random(900 + idx)
        hero = ["trex", "triceratops", "longneck", "stegosaurus"][idx % 4]
        items = [("cloud", 0.05, 0.72, 0.28, 0.2), ("sun", 0.74, 0.7, 0.22, 0.26), ("volcano", 0.62, 0.3, 0.36, 0.38),
                 ("palm", 0.02, 0.2, 0.22, 0.5), (hero, 0.22, 0.05, 0.48, 0.55), ("egg", 0.75, 0.04, 0.09, 0.15),
                 ("egg", 0.86, 0.04, 0.09, 0.15), ("fern", 0.04, 0.02, 0.15, 0.25), ("rock", 0.6, 0.02, 0.12, 0.1),
                 ("bone", 0.42, 0.62, 0.14, 0.08)]
        changes = rnd.sample(range(len(items)), 5)
        ph = (y1 - y0 - 0.3 * inch) / 2
        diffs = []
        for panel in range(2):
            px, py, pw = x0, y1 - (panel + 1) * ph - panel * 0.3 * inch, x1 - x0
            c.setLineWidth(2)
            c.roundRect(px, py, pw, ph, 0.15 * inch)
            c.saveState()
            p = c.beginPath()
            p.roundRect(px, py, pw, ph, 0.15 * inch)
            c.clipPath(p, stroke=0, fill=0)
            c.setLineWidth(1.5)
            c.line(px, py + ph * 0.12, px + pw, py + ph * 0.12)
            for j, (key, fx, fy, fw, fh) in enumerate(items):
                flip = False
                if panel == 1 and j in changes:
                    mode = changes.index(j) % 3
                    if mode == 0:
                        diffs.append((fx + fw / 2, fy + fh / 2))
                        continue  # removed
                    elif mode == 1:
                        flip = True
                    else:
                        fy = fy + 0.08
                    diffs.append((fx + fw / 2, fy + fh / 2))
                A.place(c, model(key), px + fx * pw, py + fy * ph, fw * pw, fh * ph, lw=1.5, flip=flip)
            c.restoreState()
        self.answers.append(("spot", self.page, diffs))

    # ------------------------------------------------------------------ coloring (single sided)
    def coloring(self, idx):
        k = DINO_KEYS[idx % 8]
        name, sp = self.t["names"][k], self.t["species"][k]
        if idx >= 8:
            k = ["longneck", "trex"][idx % 2]
            name, sp = self.t["names"][k], self.t["species"][k]
        x0, y0, x1, y1 = self.new_page("color", self.t["ins"]["color"].format(name=name, species=sp))
        c = self.c
        rnd = random.Random(idx)
        bw, bh = x1 - x0, y1 - y0 - 0.75 * inch
        by = y0 + 0.75 * inch
        c.setLineWidth(2.4)
        c.roundRect(x0, by, bw, bh, 0.2 * inch)
        c.saveState()
        p = c.beginPath()
        p.roundRect(x0, by, bw, bh, 0.2 * inch)
        c.clipPath(p, stroke=0, fill=0)
        ground = by + bh * 0.16
        c.setLineWidth(2.2)
        hp = c.beginPath()
        hp.moveTo(x0, ground + 0.4 * inch)
        hp.curveTo(x0 + bw * 0.3, ground + 0.9 * inch, x0 + bw * 0.6, ground - 0.1 * inch, x1, ground + 0.5 * inch)
        c.drawPath(hp, stroke=1, fill=0)
        A.place(c, model("cloud"), x0 + 0.3 * inch, by + bh - 1.4 * inch, 1.9 * inch, 1.0 * inch, lw=2.2)
        A.place(c, model("sun" if idx % 2 == 0 else "cloud"), x1 - 2.0 * inch, by + bh - 1.8 * inch, 1.6 * inch, 1.5 * inch, lw=2.2)
        A.place(c, model("volcano" if idx % 3 else "palm"), x1 - 2.6 * inch, ground + 0.2 * inch, 2.4 * inch, 2.7 * inch, lw=2.4)
        A.place(c, model("palm" if idx % 3 else "fern"), x0 + 0.1 * inch, ground + 0.1 * inch, 1.8 * inch, 3.4 * inch, lw=2.4)
        if idx < 8:
            A.place(c, model(k), x0 + 0.9 * inch, ground - 0.35 * inch, bw - 1.8 * inch, bh * 0.66, lw=3.2)
        else:  # family scenes: a big dino with a friend
            big, small = [("longneck", "triceratops"), ("trex", "baby")][idx % 2]
            A.place(c, model(big), x0 + 0.5 * inch, ground - 0.3 * inch, bw * 0.62, bh * 0.68, lw=3.0)
            A.place(c, model(small), x0 + bw * 0.58, ground - 0.4 * inch, bw * 0.38, bh * 0.32, lw=2.8, flip=True)
        for j in range(3):
            A.place(c, model(["egg", "rock", "fern"][j]), x0 + 0.3 * inch + j * 0.9 * inch + rnd.uniform(0, 0.3) * inch,
                    by + 0.15 * inch, 0.7 * inch, 0.75 * inch, lw=2)
        c.restoreState()
        K.paragraph(c, self.t["facts"][k], x0, y0 + 0.62 * inch, "Round", 13, bw, align="center")
        # blank back (single-sided printing for markers)
        self.new_page(number=False)
        bx0, by0, bx1, by1 = self.box()
        c.setFont("Round", 11)
        c.setFillColor(GREY)
        c.drawCentredString((bx0 + bx1) / 2, by0 + 0.2 * inch, self.t["blank_note"])

    # ------------------------------------------------------------------ answers
    def answer_pages(self):
        c = self.c
        groups = [("maze", 6, 2), ("ws", 4, 2), ("other", 12, 3)]
        mazes = [a for a in self.answers if a[0] == "maze"]
        wss = [a for a in self.answers if a[0] == "ws"]
        others = [a for a in self.answers if a[0] not in ("maze", "ws")]
        for chunk in [mazes[i:i + 6] for i in range(0, len(mazes), 6)]:
            x0, y0, x1, y1 = self.new_page("answers")
            cw, ch = (x1 - x0) / 2, (y1 - y0) / 3
            for i, (_, pg, (op, cols, rows, sol)) in enumerate(chunk):
                bx, by = x0 + (i % 2) * cw, y1 - (i // 2 + 1) * ch
                cell = min((cw - 0.5 * inch) / cols, (ch - 0.6 * inch) / rows)
                mx = bx + (cw - cols * cell) / 2
                my = by + 0.15 * inch
                P.draw_maze(c, op, cols, rows, mx, my, cell, lw=1.1, solution=sol, sol_color=MID)
                P.draw_maze(c, op, cols, rows, mx, my, cell, lw=1.1)
                c.setFont("RoundBold", 11)
                c.setFillColor(black)
                c.drawCentredString(bx + cw / 2, by + ch - 0.32 * inch, f"{self.t['sec']['maze']} - {self.t['answer_page']} {pg}")
        for chunk in [wss[i:i + 4] for i in range(0, len(wss), 4)]:
            x0, y0, x1, y1 = self.new_page("answers")
            cw, ch = (x1 - x0) / 2, (y1 - y0) / 2
            for i, (_, pg, (grid, placed, n)) in enumerate(chunk):
                bx, by = x0 + (i % 2) * cw, y1 - (i // 2 + 1) * ch
                cell = min(cw - 0.5 * inch, ch - 0.8 * inch) / n
                gx = bx + (cw - n * cell) / 2
                self._ws_grid(grid, gx, by + 0.3 * inch, cell, n, placed=placed, font_scale=0.6)
                c.setFont("RoundBold", 11)
                c.drawCentredString(bx + cw / 2, by + ch - 0.32 * inch, f"{self.t['sec']['ws']} - {self.t['answer_page']} {pg}")
        x0, y0, x1, y1 = self.new_page("answers")
        y = y1 - 0.2 * inch
        col = 0
        colw = (x1 - x0) / 2
        for kind, pg, data in others:
            if kind == "spot":
                txt = None
            elif kind == "shadow":
                txt = ", ".join(f"{a}→{b}" for a, b in data)
            else:
                txt = "  ".join(f"{chr(97 + i) if kind != 'odd' else i + 1}) {v}" for i, v in enumerate(data))
            if kind == "spot":
                continue
            c.setFont("RoundBold", 12)
            c.setFillColor(black)
            c.drawString(x0 + col * colw, y, f"{self.t['sec'][kind]} - p.{pg}")
            c.setFont("Body", 11.5)
            c.drawString(x0 + col * colw, y - 0.22 * inch, txt)
            y -= 0.62 * inch
            if y < y0 + 2.2 * inch:
                y = y1 - 0.2 * inch
                col += 1
        # spot the difference answers: mini maps with circles, bottom of the same page
        spots = [a for a in self.answers if a[0] == "spot"]
        if spots:
            cw = (x1 - x0) / len(spots)
            ph_ = 1.25 * inch
            for i, (_, pg, diffs) in enumerate(spots):
                px, pw = x0 + i * cw + 0.08 * inch, cw - 0.16 * inch
                by = y0 + 0.1 * inch
                c.setLineWidth(1.2)
                c.setStrokeColor(black)
                c.roundRect(px, by, pw, ph_, 0.06 * inch)
                c.setFont("RoundBold", 10)
                c.setFillColor(black)
                c.drawCentredString(px + pw / 2, by + ph_ + 0.1 * inch, f"{self.t['sec']['spot']} p.{pg}")
                for (fx, fy) in diffs:
                    c.setLineWidth(1.8)
                    c.circle(px + fx * pw, by + fy * ph_, 0.1 * inch)

    def certificate(self):
        x0, y0, x1, y1 = self.new_page(number=False)
        c = self.c
        cx = (x0 + x1) / 2
        c.setLineWidth(4)
        c.roundRect(x0, y0, x1 - x0, y1 - y0, 0.3 * inch)
        c.setLineWidth(1.5)
        c.roundRect(x0 + 0.15 * inch, y0 + 0.15 * inch, x1 - x0 - 0.3 * inch, y1 - y0 - 0.3 * inch, 0.25 * inch)
        K.text_center(c, self.t["certificate"], cx, y1 - 1.1 * inch, "Title", 54, x1 - x0 - 1 * inch)
        K.text_center(c, self.t["cert_sub"], cx, y1 - 1.65 * inch, "Round", 24, x1 - x0 - 1 * inch)
        A.place(c, model("trex"), x0 + 1.0 * inch, y1 - 5.3 * inch, x1 - x0 - 2.0 * inch, 3.4 * inch, lw=2.6)
        c.setLineWidth(1.6)
        c.line(x0 + 1.0 * inch, y1 - 6.3 * inch, x1 - 1.0 * inch, y1 - 6.3 * inch)
        c.setFont("Round", 12)
        c.drawCentredString(cx, y1 - 6.55 * inch, self.t["cert_name"])
        K.paragraph(c, self.t["cert_text"], x0 + 0.8 * inch, y1 - 6.9 * inch, "Round", 15, x1 - x0 - 1.6 * inch, align="center")
        K.text_center(c, self.t["cert_role"], cx, y1 - 7.75 * inch, "Title", 28, x1 - x0 - 1 * inch)
        c.line(x0 + 1.0 * inch, y0 + 1.0 * inch, cx - 0.3 * inch, y0 + 1.0 * inch)
        c.drawCentredString((x0 + 1.0 * inch + cx - 0.3 * inch) / 2, y0 + 0.75 * inch, self.t["cert_date"])
        K.poly(c, K.star_points(x1 - 1.7 * inch, y0 + 1.0 * inch, 0.62 * inch, 0.4 * inch, n=12), fill=None, stroke=black, lw=2)
        A.place(c, model("footprint"), x1 - 2.0 * inch, y0 + 0.7 * inch, 0.6 * inch, 0.6 * inch, lw=1.5)

    def thanks_page(self):
        x0, y0, x1, y1 = self.new_page(number=False)
        c = self.c
        K.text_center(c, self.t["thanks_title"], (x0 + x1) / 2, y1 - 0.8 * inch, "Title", 38, x1 - x0)
        A.place(c, model("baby"), x0 + 2 * inch, y1 - 4.4 * inch, x1 - x0 - 4 * inch, 3.2 * inch, lw=2.4)
        y = y1 - 4.8 * inch
        for ptxt in self.t["thanks"]:
            y = K.paragraph(c, ptxt, x0 + 0.4 * inch, y, "Body", 14, x1 - x0 - 0.8 * inch, 1.4, align="center") - 0.2 * inch
        for i in range(5):
            K.poly(c, K.star_points((x0 + x1) / 2 + (i - 2) * 0.7 * inch, y0 + 1.0 * inch, 0.28 * inch, 0.12 * inch),
                   fill=None, stroke=black, lw=2)


def build(lang, out_root):
    out_dir = os.path.join(out_root, lang)
    b = Book(lang, out_dir)
    b.belongs_page()
    b.copyright_page()
    b.map_page()
    b.meet_page()
    # progressive, interleaved playlist (76 activity pages)
    plan = []
    mz = iter(["easy"] * 5 + ["medium"] * 5 + ["hard"] * 4)
    dots_n = iter([15, 20, 20, 25, 25, 30, 30, 35, 40, 40, 45, 50])
    counters = {k: 0 for k in ["maze", "dots", "ws", "tp", "tn", "count", "add", "shadow", "odd", "half", "cbn", "spot"]}
    pattern = ["maze", "dots", "tp", "count", "shadow", "ws", "maze", "cbn", "dots", "odd", "tn", "maze", "add",
               "dots", "ws", "half", "count", "maze", "spot", "dots", "cbn"]
    limits = {"maze": 14, "dots": 12, "ws": 8, "tp": 4, "tn": 4, "count": 8, "add": 4, "shadow": 4, "odd": 4,
              "half": 4, "cbn": 6, "spot": 4}
    while len(plan) < sum(limits.values()):
        for kind in pattern:
            if counters[kind] < limits[kind]:
                plan.append((kind, counters[kind]))
                counters[kind] += 1
    for kind, i in plan:
        if kind == "maze":
            b.maze(next(mz), i)
        elif kind == "dots":
            b.dots(i, next(dots_n))
        elif kind == "ws":
            b.wordsearch(i)
        elif kind == "tp":
            b.trace_paths(i)
        elif kind == "tn":
            b.trace_names(i)
        elif kind == "count":
            b.count_page(i)
        elif kind == "add":
            b.add_page(i)
        elif kind == "shadow":
            b.shadow_page(i)
        elif kind == "odd":
            b.odd_page(i)
        elif kind == "half":
            b.half_page(i)
        elif kind == "cbn":
            b.cbn_page(i)
        elif kind == "spot":
            b.spot_page(i)
    # coloring section must start on a right-hand (odd) page so each picture faces its blank back correctly
    if b.page % 2 == 1:
        b.new_page(number=False)
    for i in range(10):
        b.coloring(i)
    b.answer_pages()
    b.certificate()
    b.thanks_page()
    while b.page < TARGET_PAGES:
        b.new_page(number=False)
    b.finish()
    return b.path, b.page


if __name__ == "__main__":
    out_root = os.path.join(KDP, "out", "01_dino_quest")
    langs = sys.argv[1:] or ["en", "fr"]
    for lang in langs:
        path, pages = build(lang, out_root)
        print(lang, pages, "pages ->", path)
