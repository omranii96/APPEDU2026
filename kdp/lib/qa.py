"""
KDP preflight for every deliverable - measured, not eyeballed.

Checks per PDF:
  * page count / page size match the KDP spec for that file
  * every font embedded (KDP rejects non-embedded fonts)
  * every text character's bounding box keeps the required distance from the trim edges
    (interior: KDP minimum 0.25in outside/top/bottom, 0.375in gutter for 24-150 pages;
     cover: our stricter 0.5in from each panel's trim edges, spine excluded)
  * nothing printed inside the barcode zone on the back cover
"""
import json
import os
import sys

import pypdfium2 as pdfium

from . import kdpkit as K

IN = 72.0


def _chars(page):
    tp = page.get_textpage()
    n = tp.count_chars()
    out = []
    for i in range(n):
        ch = tp.get_text_range(i, 1)
        if not ch.strip():
            continue
        l_, b_, r_, t_ = tp.get_charbox(i)
        out.append((ch, l_, b_, r_, t_))
    return out


def check_interior(path, trim_w, trim_h, bleed, expect_pages, gutter_min=0.375, edge_min=0.25):
    pdf = pdfium.PdfDocument(path)
    issues = []
    if len(pdf) != expect_pages:
        issues.append(f"page count {len(pdf)} != {expect_pages}")
    exp_w = trim_w + (bleed if bleed else 0)
    exp_h = trim_h + (2 * bleed if bleed else 0)
    worst = 99.0
    for i in range(len(pdf)):
        pg = pdf[i]
        w, h = pg.get_width() / IN, pg.get_height() / IN
        if abs(w - exp_w) > 0.01 or abs(h - exp_h) > 0.01:
            issues.append(f"p{i + 1} size {w:.3f}x{h:.3f} != {exp_w}x{exp_h}")
        right = (i % 2 == 0)  # page 1 is a right-hand page
        tx0 = 0 if (right or not bleed) else bleed
        ty0 = bleed if bleed else 0
        for ch, l_, b_, r_, t_ in _chars(pg):
            l_, b_, r_, t_ = l_ / IN - tx0, b_ / IN - ty0, r_ / IN - tx0, t_ / IN - ty0
            inner = l_ if right else trim_w - r_
            outer = trim_w - r_ if right else l_
            d = min(inner - gutter_min + edge_min, outer, b_, trim_h - t_)
            worst = min(worst, d)
            if inner < gutter_min or outer < edge_min or b_ < edge_min or trim_h - t_ < edge_min:
                issues.append(f"p{i + 1} char {ch!r} too close to edge (in={inner:.2f} out={outer:.2f} "
                              f"bot={b_:.2f} top={trim_h - t_:.2f})")
                break
    return issues, worst


def check_cover(path, trim_w, trim_h, pages, paper, safe=0.5):
    pdf = pdfium.PdfDocument(path)
    pg = pdf[0]
    W_, H_, sp = K.cover_dims(trim_w * IN, trim_h * IN, pages, paper)
    issues = []
    w, h = pg.get_width(), pg.get_height()
    if abs(w - W_) > 0.5 or abs(h - H_) > 0.5:
        issues.append(f"cover size {w / IN:.3f}x{h / IN:.3f} != {W_ / IN:.3f}x{H_ / IN:.3f}")
    b = K.BLEED / IN
    spi = sp / IN
    back = (b, b, b + trim_w, b + trim_h)
    front = (b + trim_w + spi, b, b + 2 * trim_w + spi, b + trim_h)
    zx, zy, zw, zh = [v / IN for v in K.barcode_zone(b * IN, b * IN, trim_w * IN)]
    worst = 99.0
    for ch, l_, b_, r_, t_ in _chars(pg):
        l_, b_, r_, t_ = l_ / IN, b_ / IN, r_ / IN, t_ / IN
        cx = (l_ + r_) / 2
        if back[0] <= cx <= back[2]:
            panel = back
        elif front[0] <= cx <= front[2]:
            panel = front
        else:
            continue  # spine text has its own rule (0.0625in), handled by construction
        d = min(l_ - panel[0], panel[2] - r_, b_ - panel[1], panel[3] - t_)
        worst = min(worst, d)
        if d < safe:
            issues.append(f"char {ch!r} only {d:.3f}in from trim (need {safe})")
            break
        if panel is back and l_ < zx + zw and r_ > zx and b_ < zy + zh and t_ > zy:
            issues.append(f"char {ch!r} inside barcode zone")
            break
    return issues, worst


def run(out_root):
    specs = [
        ("01_dino_quest", "DinoQuest", 8.5, 11, 0, 108, "bw_white"),
        ("02_dino_abc", "DinoQuestABC", 8.5, 11, 0, 82, "bw_white"),
        ("03_nova", "Nova", 8.5, 8.5, 0.125, 32, "color_white"),
    ]
    report = {}
    ok = True
    for folder, stem, tw, th, bl, pages, paper in specs:
        for lang in ("en", "fr"):
            d = os.path.join(out_root, folder, lang)
            files = os.listdir(d)
            inter = [f for f in files if "Interior" in f][0]
            cover = [f for f in files if f.endswith("Cover_Paperback.pdf")][0]
            i_issues, i_worst = check_interior(os.path.join(d, inter), tw, th, bl, pages)
            c_issues, c_worst = check_cover(os.path.join(d, cover), tw, th, pages, paper)
            meta_i = K.pdf_report(os.path.join(d, inter))
            meta_c = K.pdf_report(os.path.join(d, cover))
            if meta_i["unembedded"] or meta_c["unembedded"]:
                i_issues.append(f"unembedded fonts: {meta_i['unembedded'] + meta_c['unembedded']}")
            key = f"{folder}/{lang}"
            report[key] = {
                "interior": inter, "interior_pages": meta_i["pages"], "interior_issues": i_issues,
                "closest_text_margin_interior_in": round(i_worst, 3),
                "cover": cover, "cover_issues": c_issues, "closest_text_margin_cover_in": round(c_worst, 3),
                "spine_in": round(K.spine_width(pages, paper) / IN, 4),
            }
            ok &= not i_issues and not c_issues
    return ok, report


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(K.ROOT, "out")
    ok, rep = run(root)
    print(json.dumps(rep, indent=1, ensure_ascii=False))
    print("PREFLIGHT", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
