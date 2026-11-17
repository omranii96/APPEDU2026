"""Puzzle generators: mazes (with solver), word search (with solution), dot-to-dot."""
import math
import random
from collections import deque

from shapely.geometry import Polygon


# --------------------------------------------------------------------------- maze
def make_maze(cols, rows, seed):
    rnd = random.Random(seed)
    # walls[(c, r)] = set of open directions
    opened = {(c, r): set() for c in range(cols) for r in range(rows)}
    stack = [(0, 0)]
    seen = {(0, 0)}
    D = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
    OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}
    while stack:
        c, r = stack[-1]
        nbrs = [(d, (c + dx, r + dy)) for d, (dx, dy) in D.items()
                if 0 <= c + dx < cols and 0 <= r + dy < rows and (c + dx, r + dy) not in seen]
        if not nbrs:
            stack.pop()
            continue
        d, n = rnd.choice(nbrs)
        opened[(c, r)].add(d)
        opened[n].add(OPP[d])
        seen.add(n)
        stack.append(n)
    return opened


def solve_maze(opened, start, goal):
    D = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
    prev = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == goal:
            break
        for d in opened[cur]:
            dx, dy = D[d]
            n = (cur[0] + dx, cur[1] + dy)
            if n not in prev:
                prev[n] = cur
                q.append(n)
    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return path[::-1]


def draw_maze(c, opened, cols, rows, x, y, cell, lw=2.2, solution=None, sol_color=None):
    """Entrance: bottom-left cell's West wall. Exit: top-right cell's East wall."""
    c.saveState()
    c.setLineCap(1)
    c.setLineWidth(lw)
    p = c.beginPath()
    for (ci, ri), dirs in opened.items():
        x0, y0 = x + ci * cell, y + ri * cell
        if "N" not in dirs:
            p.moveTo(x0, y0 + cell); p.lineTo(x0 + cell, y0 + cell)
        if "E" not in dirs and not (ci == cols - 1 and ri == rows - 1):
            p.moveTo(x0 + cell, y0); p.lineTo(x0 + cell, y0 + cell)
        if ri == 0:
            p.moveTo(x0, y0); p.lineTo(x0 + cell, y0)
        if ci == 0 and ri != 0:
            p.moveTo(x0, y0); p.lineTo(x0, y0 + cell)
    c.drawPath(p, stroke=1, fill=0)
    if solution:
        c.setStrokeColor(sol_color)
        c.setLineWidth(max(1.5, cell * 0.28))
        c.setLineJoin(1)
        sp = c.beginPath()
        sp.moveTo(x - cell * 0.5, y + cell * 0.5)
        for (ci, ri) in solution:
            sp.lineTo(x + (ci + 0.5) * cell, y + (ri + 0.5) * cell)
        sp.lineTo(x + (cols + 0.5) * cell, y + (rows - 0.5) * cell)
        c.drawPath(sp, stroke=1, fill=0)
    c.restoreState()


# --------------------------------------------------------------------------- word search
DIRS_EASY = [(1, 0), (0, -1)]
DIRS_MED = DIRS_EASY + [(1, -1)]
DIRS_HARD = DIRS_MED + [(-1, 0), (0, 1), (1, 1)]


def make_wordsearch(words, n, dirs, seed, alphabet="ABCDEFGHIJKLMNOPRSTUVWY"):
    rnd = random.Random(seed)
    for attempt in range(400):
        grid = [[None] * n for _ in range(n)]
        placed = []
        ok = True
        for w in sorted(words, key=len, reverse=True):
            cands = []
            for (dx, dy) in dirs:
                for r in range(n):
                    for cc in range(n):
                        er, ec = r + dy * (len(w) - 1), cc + dx * (len(w) - 1)
                        if not (0 <= er < n and 0 <= ec < n):
                            continue
                        good, overlap = True, 0
                        for i, ch in enumerate(w):
                            g = grid[r + dy * i][cc + dx * i]
                            if g is not None and g != ch:
                                good = False
                                break
                            overlap += g == ch
                        if good:
                            cands.append((overlap, r, cc, dx, dy))
            if not cands:
                ok = False
                break
            rnd.shuffle(cands)
            cands.sort(key=lambda t: -t[0] if rnd.random() < 0.3 else 0)
            _, r, cc, dx, dy = cands[0]
            for i, ch in enumerate(w):
                grid[r + dy * i][cc + dx * i] = ch
            placed.append((w, r, cc, dx, dy))
        if ok:
            for r in range(n):
                for cc in range(n):
                    if grid[r][cc] is None:
                        grid[r][cc] = rnd.choice(alphabet)
            return grid, placed
        seed += 7919
        rnd = random.Random(seed)
    raise RuntimeError("could not place words")


# --------------------------------------------------------------------------- dot to dot
def dots_from_outline(geom, n, start_angle=90):
    """Evenly spaced points along the outer ring of the biggest polygon."""
    if geom.geom_type == "MultiPolygon":
        geom = max(geom.geoms, key=lambda g: g.area)
    ring = Polygon(geom.exterior).simplify(0.6).exterior
    L = ring.length
    cx, cy = geom.centroid.x, geom.centroid.y
    # start at the point closest to the requested angle from the centroid
    best, best_d = 0, 1e9
    k = 720
    for i in range(k):
        px, py = ring.interpolate(L * i / k).coords[0]
        a = math.degrees(math.atan2(py - cy, px - cx))
        d = abs((a - start_angle + 180) % 360 - 180)
        if d < best_d:
            best, best_d = i, d
    off = L * best / k
    pts = [ring.interpolate((off + L * i / n) % L).coords[0] for i in range(n)]
    # orientation: go clockwise visually (screen y up -> clockwise means negative area)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    if area > 0:
        pts = [pts[0]] + pts[1:][::-1]
    return pts, (cx, cy)
