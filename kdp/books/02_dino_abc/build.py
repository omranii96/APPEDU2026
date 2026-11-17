"""
Book 2 - DINO QUEST ABC: Letter Tracing Workbook for Preschoolers (Ages 3-5), EN + FR.
KDP paperback 8.5 x 11 in, black ink, white paper, no bleed, 82 pages.

Unique selling point: every letter and digit is drawn from a pedagogical stroke model,
so each model letter shows NUMBERED STROKES + DIRECTION ARROWS (how teachers teach it),
followed by graded practice: trace -> trace -> start-dots only -> free writing.
"""
import os
import random
import sys

from reportlab.lib.colors import black, white
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth

HERE = os.path.dirname(os.path.abspath(__file__))
KDP = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, KDP)

from lib import art as A  # noqa: E402
from lib import icons as I  # noqa: E402
from lib import kdpkit as K  # noqa: E402
from lib import strokes as S  # noqa: E402

K.ARROW_COLOR = K.hex_color("#3a3a3a")
W, H = 8.5 * inch, 11 * inch
GUTTER, OUTER, TOP, BOTTOM = 0.75 * inch, 0.55 * inch, 0.55 * inch, 0.6 * inch
SOFT = K.hex_color("#ececec")
MID = K.hex_color("#bdbdbd")
GREY = K.hex_color("#6b6b6b")
MASCOTS = ["trex", "triceratops", "stegosaurus", "longneck", "ptero", "ankylo", "spino", "baby"]

TEXT = {
    "en": {
        "title": "Dino Quest ABC", "sub": "Letter Tracing Workbook for Preschoolers",
        "author": "Dino Quest Kids Press",
        "belongs": "This book belongs to", "belongs_sub": "Super Writer in training",
        "grown": "For Grown-Ups",
        "grown_pts": [
            "Little and often wins: 10 minutes a day is better than one long session. Stop while it's still fun!",
            "Watch the grip: a relaxed “pinch” near the pencil tip. Chunky triangular pencils or crayons help little hands.",
            "Follow the numbers: every model letter shows WHERE to start (numbered dot) and WHICH WAY to go "
            "(arrows). Good habits now make writing faster and neater later.",
            "Each letter has 4 steps: trace the model, trace the dotted rows, start from the dots alone, "
            "then write it on your own. Then the facing page connects the letter to a word and a picture to color.",
            "Celebrate! Color a star on the Star Chart after every letter and finish with the certificate.",
        ],
        "copyright": ["Dino Quest ABC - Letter Tracing Workbook for Preschoolers",
                      "Copyright © 2026 Dino Quest Kids Press. All rights reserved.",
                      "Pages may be copied for use within your own home or classroom. Original artwork."],
        "chart": "My Star Chart", "chart_sub": "Color a star each time you finish a page!",
        "warm": "Warm-Up", "warm_ins": ["Trace the lines from top to bottom.", "Trace the lines from left to right.",
                                        "Trace the slanted lines.", "Trace the curves.", "Trace the circles - go around!",
                                        "Trace the zigzags.", "Trace the waves.", "Trace the loops."],
        "letter": "Letter", "is_for": "{L} is for {w}",
        "watch": "Watch how to write it - follow the numbers and arrows!",
        "trace": "Trace", "dots": "Start at the dot", "own": "Now write the word on your own!",
        "find": "Circle every {U} and {l} !",
        "color": "Color me!",
        "number": "Number", "count_color": "Color {n} eggs!", "count_one": "Color 1 egg!", "count_zero": "Zero means none - leave all the eggs white!",
        "num_words": ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
        "review_u": "ABC Review - Uppercase", "review_l": "abc Review - Lowercase",
        "review_ins": "Trace the whole alphabet!",
        "match": "Match It!", "match_ins": "Draw a line from each big letter to its little letter.",
        "abc_dots": "ABC Dot-to-Dot", "abc_dots_ins": "Connect the letters from A to Z to see who is hiding!",
        "name": "I Can Write My Name!", "name_ins": "Ask a grown-up to write your name on the first line, then copy it!",
        "cert": "CERTIFICATE", "cert_sub": "Super Writer Award",
        "cert_txt": "can trace and write every letter from A to Z and every number from 0 to 10!",
        "cert_name": "Name", "cert_date": "Date",
        "thanks_t": "Amazing job!",
        "thanks": ["Thank you for writing with Dino Quest! We are a small independent publisher and every page is "
                   "made with care.",
                   "If this book helped your child, an honest review on Amazon helps other families find it - "
                   "and tells us which adventure to make next.",
                   "Look for Dino Quest Activity Book for Kids Ages 4-8 - mazes, dot-to-dots, word searches and more!"],
    },
    "fr": {
        "title": "Dino Quest ABC", "sub": "Mon cahier pour apprendre à écrire les lettres",
        "author": "Dino Quest Kids Press",
        "belongs": "Ce cahier appartient à", "belongs_sub": "Super écrivain en herbe",
        "grown": "Pour les grands",
        "grown_pts": [
            "Peu mais souvent : 10 minutes par jour valent mieux qu'une longue séance. Arrêtez tant que c'est encore un plaisir !",
            "La tenue du crayon : une « pince » détendue près de la pointe. Les crayons triangulaires aident les petites mains.",
            "Suivre les numéros : chaque lettre modèle montre OÙ commencer (point numéroté) et DANS QUEL SENS "
            "tracer (flèches). Les bonnes habitudes d'aujourd'hui rendent l'écriture plus rapide et plus jolie demain.",
            "Chaque lettre suit 4 étapes : repasser le modèle, repasser les pointillés, partir des points seuls, "
            "puis écrire tout seul. La page d'en face relie la lettre à un mot et à un dessin à colorier.",
            "Les lettres sont en écriture script (lettres bâton et minuscules d'imprimerie), idéale pour la "
            "petite et la moyenne section et pour la lecture.",
            "Félicitez ! Coloriez une étoile sur le tableau après chaque lettre et terminez par le diplôme.",
        ],
        "copyright": ["Dino Quest ABC - Mon cahier pour apprendre à écrire les lettres",
                      "Copyright © 2026 Dino Quest Kids Press. Tous droits réservés.",
                      "Photocopie autorisée pour un usage familial ou en classe. Illustrations originales."],
        "chart": "Mon tableau d'étoiles", "chart_sub": "Colorie une étoile chaque fois que tu termines une page !",
        "warm": "Échauffement", "warm_ins": ["Repasse les traits de haut en bas.", "Repasse les traits de gauche à droite.",
                                                  "Repasse les traits penchés.", "Repasse les ponts.", "Repasse les ronds : fais le tour !",
                                                  "Repasse les zigzags.", "Repasse les vagues.", "Repasse les boucles."],
        "letter": "La lettre", "is_for": "{L} comme {w}",
        "watch": "Regarde comment on l'écrit : suis les numéros et les flèches !",
        "trace": "Je repasse", "dots": "Je pars du point", "own": "À toi d'écrire le mot tout seul !",
        "find": "Entoure tous les {U} et les {l} !",
        "color": "Colorie-moi !",
        "number": "Le nombre", "count_color": "Colorie {n} œufs !", "count_one": "Colorie 1 œuf !", "count_zero": "Zéro, c'est rien : laisse tous les œufs en blanc !",
        "num_words": ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix"],
        "review_u": "Révision ABC - Majuscules", "review_l": "Révision abc - Minuscules",
        "review_ins": "Repasse tout l'alphabet !",
        "match": "Relie !", "match_ins": "Relie chaque majuscule à sa minuscule.",
        "abc_dots": "Points ABC", "abc_dots_ins": "Relie les lettres de A à Z pour découvrir qui se cache !",
        "name": "J'écris mon prénom !", "name_ins": "Demande à un grand d'écrire ton prénom sur la première ligne, puis recopie-le !",
        "cert": "DIPLÔME", "cert_sub": "Super Écrivain",
        "cert_txt": "sait tracer et écrire toutes les lettres de A à Z et tous les nombres de 0 à 10 !",
        "cert_name": "Prénom", "cert_date": "Date",
        "thanks_t": "Bravo, quel travail !",
        "thanks": ["Merci d'avoir écrit avec Dino Quest ! Nous sommes une petite maison d'édition indépendante "
                   "et chaque page est faite avec soin.",
                   "Si ce cahier a aidé votre enfant, un avis sincère sur Amazon aide d'autres familles à le trouver, "
                   "et nous indique quelle aventure créer ensuite.",
                   "Découvrez aussi Dino Quest - Cahier d'activités Dinosaures 4-8 ans : labyrinthes, points à relier, mots mêlés..."],
    },
}


def model(key):
    return (I.ICONS.get(key) or A.DINOS.get(key) or A.PROPS.get(key))()


class Book:
    def __init__(self, lang, out_dir):
        self.lang, self.t = lang, TEXT[lang]
        self.path = os.path.join(out_dir, f"DinoQuestABC_{lang.upper()}_Interior_8.5x11.pdf")
        self.c = K.new_canvas(self.path, W, H, f"{self.t['title']} - {self.t['sub']}", self.t["author"])
        self.page = 0
        self.open = False

    def box(self):
        right = self.page % 2 == 1
        return (GUTTER if right else OUTER), BOTTOM, W - (OUTER if right else GUTTER), H - TOP

    def new_page(self, title=None, sub=None, icon=None, number=True, big_label=None):
        if self.open:
            self.c.showPage()
        self.page += 1
        self.open = True
        c = self.c
        x0, y0, x1, y1 = self.box()
        top = y1
        if title:
            bh = 0.72 * inch
            c.setFillColor(SOFT)
            c.setStrokeColor(black)
            c.setLineWidth(1.8)
            c.roundRect(x0, y1 - bh, x1 - x0, bh, 0.25 * inch, stroke=1, fill=1)
            tx = x0 + 0.25 * inch
            if big_label:
                c.setFillColor(black)
                c.circle(x0 + bh / 2, y1 - bh / 2, bh / 2 - 0.06 * inch, stroke=0, fill=1)
                c.setFillColor(white)
                c.setFont("Title", K.fit_size(big_label, "Title", bh * 0.75, 30))
                c.drawCentredString(x0 + bh / 2, y1 - bh / 2 - 10, big_label)
                tx = x0 + bh + 0.15 * inch
            c.setFillColor(black)
            c.setFont("Title", K.fit_size(title, "Title", x1 - tx - 1.2 * inch, 28))
            c.drawString(tx, y1 - bh / 2 - 9, title)
            if icon:
                A.place(c, model(icon), x1 - 1.05 * inch, y1 - bh + 0.06 * inch, 0.95 * inch, bh - 0.12 * inch, lw=1.1)
            top = y1 - bh - 0.1 * inch
            if sub:
                c.setFont("Round", K.fit_size(sub, "Round", x1 - x0, 14))
                c.drawCentredString((x0 + x1) / 2, top - 0.2 * inch, sub)
                top -= 0.34 * inch
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
        if self.open:
            self.c.showPage()
        self.c.save()

    # -------------------------------------------------------------- practice rows
    def practice_row(self, text, x0, x1, base, unit, mode, desc=True):
        """mode: trace (all dashed) | dots (first dashed, then start dots only) | model (solid+numbers)"""
        c = self.c
        K.guide_lines(c, x0, x1, base, unit, descender=desc)
        w = S.text_width(text) * unit
        gap = max(0.45 * inch, unit * 1.2)
        xx = x0 + 0.18 * inch
        i = 0
        while xx + w < x1 - 0.05 * inch:
            if mode == "trace" or (mode == "dots" and i == 0):
                K.draw_text_strokes(c, text, xx, base, unit, style="dashed", lw=max(1.6, unit * 0.11))
            elif mode == "dots":
                for ch, off, g in S.layout(text):
                    for st in g[:1]:
                        c.setFillColor(GREY)
                        c.circle(xx + (off + st[0][0]) * unit, base + st[0][1] * unit, max(2.2, unit * 0.09), stroke=0, fill=1)
            xx += w + gap
            i += 1

    # -------------------------------------------------------------- front matter
    def belongs(self):
        x0, y0, x1, y1 = self.new_page(number=False)
        c = self.c
        cx = (x0 + x1) / 2
        K.text_center(c, "A B C", cx, y1 - 1.4 * inch, "Title", 96, x1 - x0)
        A.place(c, model("trex"), x0 + 1.3 * inch, y1 - 5.6 * inch, x1 - x0 - 2.6 * inch, 3.8 * inch, lw=3)
        K.text_center(c, self.t["belongs"], cx, y1 - 6.4 * inch, "Title", 32, x1 - x0)
        c.setDash(2, 5)
        c.setLineWidth(2)
        c.line(x0 + 0.6 * inch, y1 - 7.5 * inch, x1 - 0.6 * inch, y1 - 7.5 * inch)
        c.setDash()
        K.text_center(c, self.t["belongs_sub"], cx, y1 - 8.1 * inch, "Round", 20, x1 - x0)

    def grownups(self):
        x0, y0, x1, y1 = self.new_page(number=False)
        c = self.c
        c.setFont("Title", 28)
        c.drawString(x0, y1 - 0.45 * inch, self.t["grown"])
        y = y1 - 0.8 * inch
        for p in self.t["grown_pts"]:
            y = K.paragraph(c, "•  " + p, x0, y, "Body", 12.5, x1 - x0, 1.38) - 0.13 * inch
        # mini legend: how to read a model letter
        unit = 0.8 * inch
        base = y - 2.3 * inch
        K.guide_lines(c, x0 + 0.5 * inch, x0 + 2.6 * inch, base, unit, descender=False)
        K.draw_strokes(c, S.layout("A")[0][2], x0 + 0.9 * inch, base, unit, "solid", numbered=True, arrows=True)
        K.paragraph(c, {"en": "1, 2, 3 = stroke order\nArrows = direction\nDotted = trace\nDot alone = start here",
                        "fr": "1, 2, 3 = ordre des traits\nFlèches = sens du tracé\nPointillés = repasser\nPoint seul = départ"}[self.lang],
                    x0 + 3.2 * inch, base + 1.6 * inch, "RoundBold", 15, x1 - x0 - 3.0 * inch, 1.45)
        yy = y0 + 0.75 * inch
        for line in self.t["copyright"]:
            c.setFont("Body", 9)
            c.setFillColor(GREY)
            c.drawCentredString((x0 + x1) / 2, yy, line)
            yy -= 0.19 * inch

    def star_chart(self):
        x0, y0, x1, y1 = self.new_page(self.t["chart"], self.t["chart_sub"], icon="sun")
        c = self.c
        labels = [chr(65 + i) for i in range(26)] + [str(i) for i in range(11)]
        cols = 6
        cw = (x1 - x0) / cols
        rows = (len(labels) + cols - 1) // cols
        ch = (y1 - y0) / rows
        for i, lab in enumerate(labels):
            cx = x0 + (i % cols + 0.5) * cw
            cy = y1 - (i // cols + 0.5) * ch
            r = min(cw, ch) * 0.44
            K.poly(c, K.star_points(cx, cy, r, r * 0.5), fill=None, stroke=black, lw=2)
            c.setFillColor(black)
            c.setFont("Title", r * 0.62)
            c.drawCentredString(cx, cy - r * 0.25, lab)

    # -------------------------------------------------------------- warm-up
    def warmup(self, i):
        import math
        x0, y0, x1, y1 = self.new_page(f"{self.t['warm']} {i + 1}", self.t["warm_ins"][i], icon=MASCOTS[i % 8])
        c = self.c
        c.saveState()
        c.setLineCap(1)
        c.setLineJoin(1)
        c.setLineWidth(3.2)

        def dashed(pts):
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

        if i == 0:  # vertical rain lines from clouds
            n = 7
            for k in range(n):
                xx = x0 + (k + 0.5) * (x1 - x0) / n
                A.place(c, model("cloud"), xx - 0.42 * inch, y1 - 0.85 * inch, 0.84 * inch, 0.6 * inch, lw=1.4)
                dashed([(xx, y1 - 1.0 * inch), (xx, y0 + 1.2 * inch)])
                A.place(c, model("flower"), xx - 0.32 * inch, y0 + 0.1 * inch, 0.64 * inch, 0.95 * inch, lw=1.3)
        elif i == 1:
            rows = 6
            for r in range(rows):
                yy = y1 - (r + 0.5) * (y1 - y0) / rows
                A.place(c, model(MASCOTS[r % 8]), x0, yy - 0.42 * inch, 0.9 * inch, 0.85 * inch, lw=1.2)
                dashed([(x0 + 1.05 * inch, yy), (x1 - 0.85 * inch, yy)])
                A.place(c, model("egg"), x1 - 0.65 * inch, yy - 0.38 * inch, 0.6 * inch, 0.76 * inch, lw=1.2)
        elif i == 2:
            rows = 2
            for r in range(rows):
                ytop = y1 - r * (y1 - y0) / rows - 0.2 * inch
                ybot = ytop - (y1 - y0) / rows + 0.6 * inch
                for k in range(6):
                    xs = x0 + 0.3 * inch + k * (x1 - x0 - 0.6 * inch) / 6
                    if r == 0:
                        dashed([(xs, ytop), (xs + 0.9 * inch, ybot)])
                    else:
                        dashed([(xs + 0.9 * inch, ytop), (xs, ybot)])
        elif i == 3:  # bridges / rainbows
            rows = 4
            for r in range(rows):
                yy = y1 - (r + 1) * (y1 - y0) / rows + 0.25 * inch
                n = 3 + r
                wseg = (x1 - x0 - 0.4 * inch) / n
                for k in range(n):
                    sx = x0 + 0.2 * inch + k * wseg
                    pts = [(sx + wseg * t / 30, yy + math.sin(math.pi * t / 30) * wseg * 0.55) for t in range(31)]
                    dashed(pts)
        elif i == 4:  # circles
            rows, cols = 4, 4
            for r in range(rows):
                for k in range(cols):
                    cx = x0 + (k + 0.5) * (x1 - x0) / cols
                    cy = y1 - (r + 0.5) * (y1 - y0) / rows
                    rad = min((x1 - x0) / cols, (y1 - y0) / rows) * (0.38 - 0.05 * (r % 2))
                    pts = [(cx + rad * math.cos(math.radians(90 + a)), cy + rad * math.sin(math.radians(90 + a))) for a in range(0, 361, 8)]
                    dashed(pts)
        else:
            rows = 5
            for r in range(rows):
                cy = y1 - (r + 0.5) * (y1 - y0) / rows
                amp = (y1 - y0) / rows * 0.3
                sx, ex = x0 + 0.2 * inch, x1 - 0.2 * inch
                pts = []
                for k in range(241):
                    t = k / 240
                    xx = sx + (ex - sx) * t
                    if i == 5:
                        ph = (t * (4 + r)) % 1
                        yy = cy + amp * (4 * abs(ph - 0.5) - 1)
                    elif i == 6:
                        yy = cy + amp * math.sin(t * 2 * math.pi * (2 + r * 0.5))
                    else:
                        a = t * 2 * math.pi * (4 + r)
                        xx = xx - amp * 0.5 * math.sin(a)
                        yy = cy - amp * 0.85 * math.cos(a)
                    pts.append((xx, yy))
                dashed(pts)
        c.restoreState()

    # -------------------------------------------------------------- letter spreads
    def letter_page(self, idx):
        L, icon_en, w_en, icon_fr, w_fr = I.ALPHABET[idx]
        l = L.lower()
        x0, y0, x1, y1 = self.new_page(f"{self.t['letter']} {L}", self.t["watch"], icon=MASCOTS[idx % 8], big_label=L + l)
        c = self.c
        # model box with big numbered letters
        unit = 0.7 * inch
        mh = 3 * unit + 0.3 * inch
        c.setLineWidth(1.6)
        c.roundRect(x0, y1 - mh, x1 - x0, mh, 0.2 * inch)
        base = y1 - mh + unit + 0.15 * inch
        K.guide_lines(c, x0 + 0.15 * inch, x1 - 0.15 * inch, base, unit)
        wu, wl = S.glyph_width(L) * unit, S.glyph_width(l) * unit
        gap = 1.0 * inch
        sx = (x0 + x1) / 2 - (wu + gap + wl) / 2
        K.draw_strokes(c, S.layout(L)[0][2], sx, base, unit, "solid", lw=unit * 0.14, numbered=True, arrows=True)
        K.draw_strokes(c, S.layout(l)[0][2], sx + wu + gap, base, unit, "solid", lw=unit * 0.14, numbered=True, arrows=True)
        # practice rows
        ru = 0.34 * inch
        rows = [(L, "trace"), (L, "dots"), (l, "trace"), (l, "dots")]
        avail = (y1 - mh - 0.25 * inch) - y0
        step = avail / len(rows)
        for r, (ch, mode) in enumerate(rows):
            b = y1 - mh - 0.25 * inch - r * step - 2.15 * ru
            lab = self.t["trace"] if mode == "trace" else self.t["dots"]
            c.setFont("Round", 9.5)
            c.setFillColor(GREY)
            c.drawString(x0, b + 2 * ru + 0.08 * inch, lab)
            self.practice_row(ch, x0, x1, b, ru, mode)

    def word_page(self, idx):
        L, icon_en, w_en, icon_fr, w_fr = I.ALPHABET[idx]
        icon, word = (icon_en, w_en) if self.lang == "en" else (icon_fr, w_fr)
        l = L.lower()
        title = self.t["is_for"].format(L=L, w=word)
        x0, y0, x1, y1 = self.new_page(title, None, big_label=L + l)
        c = self.c
        # picture to color
        ph = 3.0 * inch
        c.setLineWidth(2)
        c.roundRect(x0, y1 - ph, (x1 - x0) * 0.55, ph, 0.2 * inch)
        A.place(c, model(icon), x0 + 0.25 * inch, y1 - ph + 0.25 * inch, (x1 - x0) * 0.55 - 0.5 * inch, ph - 0.5 * inch, lw=2.6)
        rx = x0 + (x1 - x0) * 0.55 + 0.2 * inch
        c.setFont("Round", 15)
        c.drawString(rx, y1 - 0.45 * inch, self.t["color"])
        # big hollow word for colouring / reading
        ws = K.fit_size(word, "Title", x1 - rx, 60)
        K.outlined_text(c, word, (rx + x1) / 2, y1 - 1.6 * inch, "Title", ws, white, black, 2.2)
        K.outlined_text(c, word, (rx + x1) / 2, y1 - 1.6 * inch, "Title", ws, white, white, 0.1)
        # stroke-model word (small, solid)
        mu = min(0.3 * inch, (x1 - rx - 0.1 * inch) / max(S.text_width(word), 0.1))
        K.guide_lines(c, rx, x1, y1 - 2.65 * inch, mu)
        K.draw_text_strokes(c, word, rx + 0.05 * inch, y1 - 2.65 * inch, mu, style="solid", lw=mu * 0.14)
        # trace the word
        ru = min(0.36 * inch, (x1 - x0 - 0.5 * inch) / (S.text_width(word) * 1.0 + 0.1))
        yy = y1 - ph - 0.35 * inch
        c.setFont("Round", 9.5)
        c.setFillColor(GREY)
        c.drawString(x0, yy, self.t["trace"])
        for r in range(2):
            b = yy - 0.1 * inch - 2 * ru - r * 3.1 * ru
            self.practice_row(word, x0, x1, b, ru, "trace")
        # find the letter game (anchored from the bottom so nothing can collide)
        own_base = y0 + 0.3 * inch
        row2 = own_base + 1.35 * inch
        row1 = row2 + 0.72 * inch
        fy = row1 + 0.62 * inch
        c.setFillColor(black)
        c.setFont("RoundBold", 14)
        c.drawString(x0, fy, self.t["find"].format(U=L, l=l))
        rnd = random.Random(idx * 17 + (1 if self.lang == "fr" else 0))
        pool = [ch for ch in "ABCDEFGHIJKLMNOPRSTUVWXYZabcdefghijkmnoprstuvwxyz" if ch.lower() != l]
        cells = [L, l, L, l, L, l] + rnd.sample(pool, 12)
        rnd.shuffle(cells)
        cols = 9
        cw = (x1 - x0) / cols
        for k, ch in enumerate(cells):
            cx = x0 + (k % cols + 0.5) * cw
            cy = (row1, row2)[k // cols]
            c.setLineWidth(1.2)
            c.setStrokeColor(MID)
            c.circle(cx, cy + 0.12 * inch, 0.3 * inch)
            c.setFillColor(black)
            c.setFont(["Title", "RoundBold", "BodyBlack"][k % 3], 26)
            c.drawCentredString(cx, cy, ch)
        # write it yourself
        c.setFont("Round", 9.5)
        c.setFillColor(GREY)
        c.drawString(x0, own_base + 2 * 0.34 * inch + 0.08 * inch, self.t["own"])
        K.guide_lines(c, x0, x1, own_base + 0.1 * inch, 0.34 * inch)

    # -------------------------------------------------------------- numbers
    def number_page(self, n):
        x0, y0, x1, y1 = self.new_page(f"{self.t['number']} {n} - {self.t['num_words'][n]}", None,
                                       icon=MASCOTS[n % 8], big_label=str(n))
        c = self.c
        unit = 0.62 * inch
        digits = str(n)
        mh = 2 * unit + 0.55 * inch
        c.setLineWidth(1.6)
        c.roundRect(x0, y1 - mh, (x1 - x0) * 0.45, mh, 0.2 * inch)
        base = y1 - mh + 0.28 * inch
        wd = S.text_width(digits, 0.6) * unit
        sx = x0 + ((x1 - x0) * 0.45 - wd) / 2
        for ch, off, g in S.layout(digits, 0.6):
            K.draw_strokes(c, g, sx + off * unit, base, unit, "solid", lw=unit * 0.14, numbered=True, arrows=True)
        # count & colour eggs
        bx = x0 + (x1 - x0) * 0.45 + 0.2 * inch
        bw = x1 - bx
        c.setFont("RoundBold", 14)
        msg = self.t["count_color"].format(n=n) if n else self.t["count_zero"]
        if n == 1:
            msg = self.t["count_one"]
        K.paragraph(c, msg, bx, y1 - 0.05 * inch, "RoundBold", 14, bw, 1.2)
        es = bw / 5
        for k in range(10):
            A.place(c, model("egg"), bx + (k % 5) * es + es * 0.12, y1 - mh + 0.1 * inch + (1 - k // 5) * (mh - 0.75 * inch) / 2,
                    es * 0.76, (mh - 0.75 * inch) / 2 - 0.05 * inch, lw=1.3)
        # trace rows: digit x2, word x1, free
        ru = 0.36 * inch
        yy = y1 - mh - 0.3 * inch
        rows = [(digits, "trace"), (digits, "dots"), (self.t["num_words"][n], "trace"), (self.t["num_words"][n], "trace")]
        step = (yy - y0 - 0.9 * inch) / len(rows)
        for r, (txt, mode) in enumerate(rows):
            b = yy - r * step - 2.1 * ru
            c.setFont("Round", 9.5)
            c.setFillColor(GREY)
            c.drawString(x0, b + 2 * ru + 0.08 * inch, self.t["trace"] if mode == "trace" else self.t["dots"])
            self.practice_row(txt, x0, x1, b, ru, mode)
        K.guide_lines(c, x0, x1, y0 + 0.35 * inch, ru)

    # -------------------------------------------------------------- review & extras
    def review(self, upper):
        x0, y0, x1, y1 = self.new_page(self.t["review_u"] if upper else self.t["review_l"], self.t["review_ins"],
                                       icon="baby")
        c = self.c
        letters = [chr(65 + i) for i in range(26)]
        if not upper:
            letters = [x.lower() for x in letters]
        groups = [letters[i:i + 6] for i in range(0, 26, 6)]
        ru = 0.36 * inch
        step = (y1 - y0) / len(groups)
        for r, g in enumerate(groups):
            b = y1 - r * step - 2.2 * ru
            K.guide_lines(c, x0, x1, b, ru)
            xx = x0 + 0.2 * inch
            for ch in g:
                K.draw_text_strokes(c, ch, xx, b, ru, style="dashed", lw=1.8)
                xx += (x1 - x0 - 0.4 * inch) / 6

    def match(self):
        x0, y0, x1, y1 = self.new_page(self.t["match"], self.t["match_ins"], icon="triceratops")
        c = self.c
        rnd = random.Random(42)
        sets = [list("BDGMQR"), list("AEHNPT")]
        cw = (x1 - x0) / 2
        for s_i, letters in enumerate(sets):
            lows = [x.lower() for x in letters]
            rnd.shuffle(lows)
            bx = x0 + s_i * cw
            rh = (y1 - y0) / 6
            for k in range(6):
                cy = y1 - (k + 0.5) * rh
                c.setFont("Title", 40)
                c.drawCentredString(bx + 0.55 * inch, cy - 14, letters[k])
                c.circle(bx + 1.05 * inch, cy, 4.5, stroke=0, fill=1)
                c.circle(bx + cw - 1.15 * inch, cy, 4.5, stroke=0, fill=1)
                c.setFont("BodyBlack", 40)
                c.drawCentredString(bx + cw - 0.6 * inch, cy - 14, lows[k])

    def abc_dots(self):
        import math
        from lib import puzzles as P
        x0, y0, x1, y1 = self.new_page(self.t["abc_dots"], self.t["abc_dots_ins"], icon="egg")
        c = self.c
        m = A.longneck()
        bx, by, bw, bh = x0 + 0.4 * inch, y0 + 0.3 * inch, x1 - x0 - 0.8 * inch, y1 - y0 - 0.6 * inch
        g = A.transformed_union(m, bx, by, bw, bh)
        sc, ox, oy = A.placement(m, bx, by, bw, bh)
        c.saveState()
        c.clipPath(K.geom_path(c, g.buffer(-0.07 * inch)), stroke=0, fill=0)
        A.render(c, m, ox, oy, sc, mode="line", lw=1.8)
        c.restoreState()
        pts, (cx, cy) = P.dots_from_outline(g, 26, start_angle=100)
        for i, (px, py) in enumerate(pts):
            c.setFillColor(black)
            c.circle(px, py, 3.2, stroke=0, fill=1)
            ang = math.atan2(py - cy, px - cx)
            c.setFont("RoundBold", 15)
            c.drawCentredString(px + math.cos(ang) * 0.22 * inch, py + math.sin(ang) * 0.22 * inch - 5, chr(65 + i))

    def name_page(self):
        x0, y0, x1, y1 = self.new_page(self.t["name"], self.t["name_ins"], icon="ptero")
        ru = 0.45 * inch
        step = (y1 - y0) / 6
        for r in range(6):
            K.guide_lines(self.c, x0, x1, y1 - r * step - 2.3 * ru, ru)

    def certificate(self):
        x0, y0, x1, y1 = self.new_page(number=False)
        c = self.c
        cx = (x0 + x1) / 2
        c.setLineWidth(4)
        c.roundRect(x0, y0, x1 - x0, y1 - y0, 0.3 * inch)
        c.setLineWidth(1.5)
        c.roundRect(x0 + 0.15 * inch, y0 + 0.15 * inch, x1 - x0 - 0.3 * inch, y1 - y0 - 0.3 * inch, 0.25 * inch)
        K.text_center(c, self.t["cert"], cx, y1 - 1.1 * inch, "Title", 54, x1 - x0 - inch)
        K.text_center(c, self.t["cert_sub"], cx, y1 - 1.65 * inch, "Round", 24, x1 - x0 - inch)
        A.place(c, model("baby"), x0 + 2.0 * inch, y1 - 5.0 * inch, x1 - x0 - 4.0 * inch, 3.0 * inch, lw=2.6)
        c.line(x0 + inch, y1 - 6.1 * inch, x1 - inch, y1 - 6.1 * inch)
        c.setFont("Round", 12)
        c.drawCentredString(cx, y1 - 6.35 * inch, self.t["cert_name"])
        K.paragraph(c, self.t["cert_txt"], x0 + 0.9 * inch, y1 - 6.75 * inch, "Round", 16, x1 - x0 - 1.8 * inch, align="center")
        K.draw_text_strokes(c, "ABC 123", cx - S.text_width("ABC 123") * 0.32 * inch / 2, y1 - 8.3 * inch, 0.32 * inch, "solid", lw=4)
        c.line(x0 + inch, y0 + inch, cx - 0.3 * inch, y0 + inch)
        c.drawCentredString((x0 + inch + cx - 0.3 * inch) / 2, y0 + 0.75 * inch, self.t["cert_date"])
        K.poly(c, K.star_points(x1 - 1.7 * inch, y0 + 1.0 * inch, 0.62 * inch, 0.4 * inch, n=12), fill=None, stroke=black, lw=2)

    def thanks(self):
        x0, y0, x1, y1 = self.new_page(number=False)
        c = self.c
        K.text_center(c, self.t["thanks_t"], (x0 + x1) / 2, y1 - 0.8 * inch, "Title", 38, x1 - x0)
        A.place(c, model("stegosaurus"), x0 + 1.5 * inch, y1 - 4.2 * inch, x1 - x0 - 3 * inch, 3 * inch, lw=2.4)
        y = y1 - 4.7 * inch
        for p in self.t["thanks"]:
            y = K.paragraph(c, p, x0 + 0.4 * inch, y, "Body", 14, x1 - x0 - 0.8 * inch, 1.4, align="center") - 0.2 * inch


def build(lang, out_root):
    b = Book(lang, os.path.join(out_root, lang))
    b.belongs()
    b.grownups()
    b.star_chart()
    for i in range(8):
        b.warmup(i)
    assert b.page % 2 == 1  # next letter page will be an even (left) page -> spreads face each other
    for i in range(26):
        b.letter_page(i)
        b.word_page(i)
    for n in range(11):
        b.number_page(n)
    b.review(True)
    b.review(False)
    b.match()
    b.abc_dots()
    b.name_page()
    b.certificate()
    b.thanks()
    while b.page % 2:
        b.new_page(number=False)
    b.finish()
    return b.path, b.page


if __name__ == "__main__":
    out_root = os.path.join(KDP, "out", "02_dino_abc")
    for lang in sys.argv[1:] or ["en", "fr"]:
        p, n = build(lang, out_root)
        print(lang, n, "pages ->", p)
