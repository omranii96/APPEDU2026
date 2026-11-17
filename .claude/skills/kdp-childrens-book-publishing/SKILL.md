---
name: "kdp-childrens-book-publishing"
description: "Prepares a complete, ready-to-upload Amazon KDP publishing package for an illustrated children's picture book from a manuscript .docx — print interior DOCX, full-wrap paperback cover PDF, Kindle eBook cover image, fixed-layout EPUB, KDP metadata & best-seller strategy doc, and step-by-step publishing guide. Use this whenever the user mentions KDP, Kindle Direct Publishing, publishing a children's/picture book on Amazon, a paperback cover, a book \"interior,\" a book series for kids, or uploads a children's book manuscript and wants it publish-ready — even if they don't name every deliverable explicitly. Also trigger for follow-up requests on a book already in this pipeline, like \"check the resolution,\" \"the page count is short,\" \"fix the cover so it doesn't block the art,\" or \"add this to the series.\""
---

# KDP Children's Picture Book Publishing Pipeline

Turns an illustrated children's-book manuscript (.docx, usually with inline AI-generated
illustrations) into a complete, ready-to-upload Amazon KDP package: print interior DOCX,
full-wrap paperback cover PDF, Kindle eBook cover JPG, fixed-layout EPUB, a KDP metadata
& best-seller strategy Word doc, and a step-by-step publishing guide Word doc.

This skill was developed across a real multi-book series ("Chip's AI Adventures," ages
8-10) and encodes the specs, bugs, and fixes discovered along the way, cross-checked
against Amazon's official Paperback Submission Guidelines
(https://kdp.amazon.com/en_US/help/topic/G201857950 — re-fetch this if it's been a
while, KDP does update these specs). Apply this skill to any similar square-trim
illustrated children's book, not just that series — generalize the specifics (title,
characters, page count) to whatever manuscript you're given.

## Standing project default: Premium Color ink

For the "Chip's AI Adventures" series specifically (and as a sensible default for any
other full-color picture book project under this skill unless told otherwise), assume
**Premium Color ink** on KDP. This is a confirmed, standing decision — don't re-ask about
ink option for books in this series. It matters because it's what makes a 24-page count
valid at 8.5x8.5in trim (Standard Color would require 72 pages minimum at that trim size —
see the page-count table below). Say so explicitly in each book's metadata/guide docs so
the user doesn't accidentally pick Standard Color on upload.

## Standing project requirement: 0.5in cover text safety margin

KDP's own official minimum is text ≥0.25in from the outer trim edge (≈0.375in from the
raw full-bleed PDF edge, once you account for the 0.125in bleed strip). For this project,
the user has asked for an *extra* safety buffer beyond that: **every piece of cover text
must stay at least 0.5in from every edge of the cover PDF** (front, back, top, bottom —
not just the official minimum). Treat 0.5in as the real requirement for this project, not
0.375in — it's stricter than KDP requires, which is exactly the point (extra insurance
against trimming variance during printing). Verify programmatically (see below), not by
eye — this project has twice shipped covers where a copy-pasted layout constant looked
fine visually but measured under the required margin.

## Standing project requirement: paperback interior deliverable is DOCX, not PDF

**The `<Title> - Interior Print>` deliverable must be a `.docx` file, not a `.pdf`.** This
is a deliberate project choice, not the pipeline's original default (earlier books in this
series shipped a hand-built PDF interior) — going forward, build and deliver the interior
as a Word document instead.

- This is workable within KDP's own rules because this pipeline's interiors are "No
  Bleed" (illustrations are inset with a margin, not bled to the trim edge) — KDP accepts
  DOC/DOCX/RTF/HTML/TXT for no-bleed interiors and auto-converts on upload. (KDP still
  requires PDF for interiors that use bleed — if a future book's interior design needs
  bleed, flag that trade-off to the user before assuming DOCX will still work.)
- Building the interior as DOCX trades away some of the pixel-precise layout control a
  hand-built PDF gives you (exact image placement, custom fonts/positioning, decorative
  elements). Use the `docx` skill/library to build page-by-page: one Word section per
  story page (or a page break between pages), each with the illustration inserted at a
  size/position matching the original print layout as closely as Word's layout model
  allows, and the story text formatted at a clearly legible size (never below the 7pt
  floor — see the legibility-check section below; body text this size should realistically
  be much larger than 7pt for a children's book, more like 14-18pt+, matching the visual
  weight of the original PDF design).
- If a story page has a lot of dialogue/text, scale the illustration down a bit on that
  page (rather than keeping one fixed image size for every page) so the text still fits
  on a single page without spilling onto a near-blank overflow page. Check the rendered
  page count against expectations after building — a page with only a stray page number
  and nothing else is a sign some earlier page overflowed.
- After building, render the DOCX to PDF (e.g. via `soffice --headless --convert-to pdf`)
  purely as a **visual QA step** — check pages, images, and text layout look right, and
  confirm no page is unexpectedly near-blank — but the file you actually deliver and tell
  the user to upload to KDP is the `.docx`, not that QA-rendered PDF.
- The full-wrap **Cover Print stays a PDF** — this requirement is about the interior only.
  A wraparound cover has bleed and spine geometry that only a hand-built PDF can express;
  KDP does not accept a DOCX for the cover.
- Update the deliverables checklist, the metadata doc, and the guide doc's upload
  instructions accordingly (see below) so nothing still says "PDF" for the interior.

## Standing project requirement: no placeholder text in the interior

Do not include bracketed/placeholder text in the delivered interior — e.g. don't print
`ISBN: [add your KDP-assigned or self-purchased ISBN here]` on the copyright page, and
don't print `[Add a sentence or two here about you — this is a placeholder.]` on the About
the Author page. These used to appear in every book's interior; the project's standing
preference is to leave the interior clean instead:

- Copyright page: just omit the ISBN line entirely. KDP assigns a free ISBN during setup
  (or the author can supply their own there) — the interior file itself doesn't need to
  say anything about it.
- About the Author page: keep only the one real, general sentence already written for the
  author (no bracketed placeholder sentence appended after it). If the user wants a fuller
  bio, that's their call to add — don't insert a visible "placeholder" prompting them to.
- If it's useful to remind the user to add a real ISBN or expand their bio later, put that
  as a bullet in the KDP Metadata & Strategy doc (see its structure below) instead of
  printing it inside the book itself — keep the delivered interior clean of any text that
  isn't meant to be permanent, printed content.
- This is a general pattern worth extending: don't put ANY visible "fill this in" style
  text inside a deliverable meant to be printed/published as-is. Reserve that kind of
  guidance for the metadata/guide docs, which are explicitly instructional documents.
- This applies equally to the fixed-layout EPUB, not just the print interior — e.g. an
  About the Author page inside the EPUB should reuse the same real bio sentence as the
  print interior, with no bracketed placeholder appended.

## Standing project requirement: Kindle version fonts must be clearly readable

Every font used in the Kindle eBook deliverables (the fixed-layout EPUB's body/heading
text, and any text baked into the Kindle Cover JPG) must be clearly legible at normal
on-device reading size — not just "technically renders."

- Fixed-layout EPUBs mimic the print page at a fixed pixel canvas, which is an easy way to
  accidentally ship text sized for an 8.5x8.5in physical page and too small once that same
  canvas is shown on a 6-7in device screen. Size body text generously — treat this as a
  distinct, stricter bar than the print minimum (see the 7pt print floor below); on a
  fixed-layout EPUB page sized to match an 8.5x8.5in canvas, body text should read
  comfortably at typical tablet/e-reader zoom, not just barely pass a font-size number.
  Concretely: set an explicit base `font-size` on `html`/`body` (don't leave it undefined
  and rely on em units cascading from the reader's own default — that makes the actual
  rendered size unpredictable and, in practice, ended up far too small) sized proportional
  to the fixed-layout canvas (e.g. ~2% of the canvas width), and give body story text its
  own explicit size clearly larger than incidental caption/label text.
- Use high-contrast, clean sans-serif or well-hinted fonts for any text rendered small;
  avoid thin/light font weights for body copy — they degrade further on e-ink and
  lower-DPI phone screens.
- After building the EPUB, actually open/render representative pages (e.g. render the
  page XHTML in a headless browser or convert to an image at the fixed-layout's native
  resolution) and visually confirm every line of text is crisp and easy to read at that
  resolution — don't just trust the CSS font-size number in isolation, since embedded-font
  fallback failures or an unexpectedly small computed size can still slip through.
- This applies to the Kindle Cover JPG too: title/subtitle/author text on that cover must
  be sharp and readable at the thumbnail sizes Kindle actually displays (store thumbnail,
  library grid) — check it doesn't disappear or blur out when scaled down, not just at
  full size. Also check title text actually **fits within the canvas** at whatever fixed
  font size the layout code uses — a title/subtitle string that's longer than whatever
  book it was originally tuned for can silently run off the edge. Auto-fit long titles
  (measure text width and shrink the font size until it fits within a safe max width)
  rather than assuming a fixed font-size percentage will always fit every book's title.

## Manuscript & interior text/image legibility check (run on every book, before final delivery)

Before calling any book's interior or cover final, explicitly check all body text *and*
any text embedded inside illustrations (e.g. signage, labels drawn as part of the artwork)
against these common failure modes:

1. **Font size** — every text element is at least 7pt (KDP's hard minimum); in practice,
   children's-book body text should be well above that floor for actual readability (this
   pipeline's existing books use body copy in roughly the 11-17pt range depending on the
   element — treat 7pt as an absolute floor, not a target).
2. **No cutoff or overlap** — no text is clipped by the page/image edge, a decorative
   band, an illustration, or another text block; no two text elements overlap each other.
   Check this the same way the cover-margin check works: render the page and inspect
   actual bounding boxes, not just the source layout code, since library/font-substitution
   quirks can shift real rendered position from what the code intended.
3. **Text-to-background contrast** — text color must not blend into whatever is behind
   it (a background photo/illustration, a colored band, etc.). Spot-check every distinct
   text-on-background combination used in the book; if a color pairing is even borderline,
   increase contrast (darker/lighter text, add a subtle background plate behind the text,
   or use a stroke/shadow) rather than leaving it marginal.
4. **Image clarity** — illustrations must not be blurry, pixelated, jagged (visible
   stair-stepping/aliasing at edges), or faded/washed out, and must meet the existing
   300 DPI minimum (see the DPI verification section below — that check confirms
   resolution, but still visually inspect for jagged upscale artifacts or faded color,
   which a DPI number alone won't catch). **Also check for compositing/seam defects** —
   see the dedicated "Verifying illustration assets aren't corrupted" section below for a
   real bug this project shipped (a visible white seam plus a mismatched second image
   bleeding into the bottom of four story-page illustrations) and how to scan for it
   programmatically rather than relying on catching it by eye.

Do this as an explicit pass late in the workflow: render final pages (interior and cover)
at or near their actual output resolution and visually review them page-by-page against
these four checks, in addition to (not instead of) the automated DPI and text-margin
checks elsewhere in this skill. Report to the user that this pass was done, and flag
anything borderline rather than silently "fixing" it in a way that changes the art/design
without their input.

## Verifying illustration assets aren't corrupted (a seam/compositing check, not just a layout check)

A real bug on this project (Book 4, "Chip and the Mystery Library") turned out to be
neither a layout bug nor a resolution problem: four consecutive story-page illustration
JPEGs (page08-page11) each had a visible defect **baked into the image file itself** — a
bright white horizontal seam band around 92-95% down the image, with a mismatched,
unrelated second image bleeding in below the seam. Reported by the user as "some pics on
some pages are split into two." Because the fixed-layout EPUB's `.frame img { width:100%;
height:100%; object-fit:cover; }` just displays whatever the source JPEG contains, none of
this project's existing checks caught it — the wrap-aware text-fit math, the "does every
page fit" verification log, and the flexbox/margin fixes are all about *text* layout and
have nothing to say about a corrupted *image* asset. The defect had been sitting in the
source images since an earlier asset-recovery/upscale step and shipped undetected through
several rounds of EPUB fixes because nobody had visually reviewed the actual pixel content
of every embedded illustration, only the text card layered on top of it.

**Where this kind of defect comes from on this project:** most likely an artifact of the
image-recovery workflow documented elsewhere in this skill (extracting page art from a
previously-delivered `.epub`/`.docx`/cover PDF when the scratch directory was lost, or an
upscale/tiling step that pastes processed tiles back together). A botched crop/paste in
either of those steps can leave a stray strip of a *different* image glued onto the bottom
of the intended one. It is not something the layout/CSS code can cause on its own, since
each frame only ever references one `<img>` tag pointing at one source file.

**Detect this with an automated scan across every embedded page image, not just a visual
skim** — a seam like this is subtle at thumbnail size and easy to miss by eye, especially
across a whole series. For each image, look for a horizontal band of near-white,
low-variance rows that isn't at the very top/bottom edge of a legitimately white-background
illustration:

```python
from PIL import Image
import numpy as np
import os

def scan_for_seams(img_dir):
    """Flags any page image with a suspicious near-white, low-variance
    horizontal band away from the edges -- a sign of a stitched-together
    or corrupted source asset, not a layout bug."""
    flagged = {}
    for fn in sorted(os.listdir(img_dir)):
        if not (fn.startswith("page") or fn == "remember.jpg"):
            continue
        im = np.array(Image.open(f"{img_dir}/{fn}").convert("L"))
        h, w = im.shape
        row_means = im.mean(axis=1)
        row_stds = im.std(axis=1)
        seam_rows = [
            y for y in range(int(h * 0.03), int(h * 0.99))
            if row_means[y] > 244 and row_stds[y] < 8
        ]
        if not seam_rows:
            continue
        groups, start, prev = [], seam_rows[0], seam_rows[0]
        for y in seam_rows[1:]:
            if y - prev > 3:
                groups.append((start, prev))
                start = y
            prev = y
        groups.append((start, prev))
        thick = [g for g in groups if g[1] - g[0] >= 4]
        if thick:
            flagged[fn] = thick
    return flagged
```

Run this on every book's embedded image set (extract straight from the built `.epub` via
`zipfile`, or from the scratch `epub_images`/`print_images` directory) as a standard part
of the pre-delivery QA pass — not just when a user reports a problem. If any image is
flagged, open it directly (don't trust the thumbnail-scale contact sheet alone) and
confirm by eye whether it's a real defect or a legitimate design element (e.g. an
intentionally white background near an edge) before deciding it needs a fix.

**The fix, once a genuine seam is confirmed:** crop the image just above where the seam
begins, then center-crop the width to match so the result is still square (matching the
frame's aspect ratio), then resize back up to the original pixel dimensions so it still
matches the rest of the book's resolution:

```python
def fix_seam(path, seam_start_row, target_size):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    crop_row = max(0, seam_start_row - 6)  # small safety buffer above the seam
    cropped = im.crop((0, 0, w, crop_row))
    new_h = cropped.height
    if w > new_h:
        left = (w - new_h) // 2
        cropped = cropped.crop((left, 0, left + new_h, new_h))
    cropped.resize((target_size, target_size), Image.LANCZOS).save(path, quality=95)
```

After patching the affected images, rebuild that book's EPUB (`build_epubN.py`), then
re-run `scan_for_seams()` against the freshly-extracted images from the rebuilt `.epub` to
confirm the fix actually took (don't just trust that patching the source file was enough —
confirm it made it into the rebuilt archive), and do one direct visual spot-check of the
previously-flagged pages.

**Check the print interior for the same defect, and flag it separately rather than fixing
it unprompted.** If a source image is corrupted, whatever else in the pipeline uses that
same image (or a same-named file processed from the same recovery step) may carry the
identical defect — but the print interior and the EPUB do not necessarily draw from
identical files (this project's `epub_images` and `print_images` directories held
different, non-identical copies for the same book, and in at least one case the
print-side image for a given page number turned out to be visually different content
altogether, suggesting a page-to-image mapping mismatch worth its own investigation later).
Don't assume fixing the EPUB image also fixed the print asset — check it independently,
and don't rebuild/reship the print interior without the user's go-ahead, since that's a
bigger, more disruptive rebuild than patching an EPUB image.

## Before you start: gather these from the user (or the manuscript itself)

1. The manuscript .docx (story text + inline illustrations).
2. Is this book part of a series? If so: series name, this book's number, and the titles
   of prior books (needed for cross-promotion text and the KDP series-linking step).
3. Any established visual/character design system from prior books in the series — e.g.
   "the robot is named X, the boy is named Y." If the manuscript's text doesn't match its
   own artwork (this happens with AI-generated content), or contradicts an established
   series convention, stop and ask the user which is correct rather than guessing. Don't
   silently rename characters or retitle the book without confirming — that's a big
   change to make unilaterally. If you DO make an edit like this, grep every build script
   for the old name/title afterward — it's easy to fix the story data file and miss a
   hardcoded reference in the cover, ebook-cover, or EPUB script (each of these projects
   had 2-3 places a character name was hardcoded outside the main data file).
4. Target trim size — default to 8.5x8.5in (square) unless told otherwise, matching most
   children's picture books.
5. Which interior ink option they'll select on KDP. For this project, that's Premium
   Color by standing default (see above) — only ask if the user is starting a different
   project or explicitly says otherwise, since it changes the minimum legal page count.

## Deliverables checklist (all six, every time)

Use this naming convention (swap in the real title):

- `<Title> - Interior Print.docx` — print-ready interior manuscript, formatted to trim
  size, "No Bleed." **DOCX, not PDF** (see standing requirement above). No placeholder/
  bracketed text anywhere in it (see standing requirement above).
- `<Title> - Cover Print.pdf` — full wrap (back + spine + front) PDF, sized to exact page
  count. Stays PDF (bleed/spine geometry requires it).
- `<Title> - Kindle Cover.jpg` — portrait eBook cover
- `<Title>.epub` — fixed-layout EPUB (bonus/alternative to Kindle Create)
- `KDP Metadata and Strategy - <Book N>.docx` — copy-paste-ready listing content
- `KDP Publishing Guide - <Book N>.docx` — step-by-step upload walkthrough

## Print specs (official KDP Paperback Submission Guidelines)

These are Amazon's actual current requirements, not approximations — pull exact numbers
from here rather than estimating. (Note: this project's own text-margin bar and interior
file-format choice are stricter/different from KDP's official minimum — see the standing
requirements above.)

### Page count — minimum depends on ink + trim size, not a flat 24

The blanket "24-page minimum" people quote is only true for **Black ink** and **Premium
Color ink**. **Standard Color ink at 8.5x8.5in trim requires a 72-page minimum** — nearly
3x higher. Before finalizing a page count, confirm which ink option the book will use
(for this project: Premium Color, per the standing default above).

| Trim size | Black ink, white paper | Black ink, cream paper | Standard color ink | Premium color ink |
|---|---|---|---|---|
| 8.5" x 8.5" | 24 - 590 | 24 - 550 | **72 - 600** | 24 - 590 |
| 8.5" x 11" | 24 - 590 | 24 - 550 | **72 - 600** | 24 - 590 |
| 6" x 9" | 24 - 828 | 24 - 776 | **72 - 600** | 24 - 828 |

(Full table at the source URL above if the trim size isn't listed here.)

If short of the minimum, do not pad with blank pages — add purposeful, on-theme back
matter: a "Try It Yourself" activity page and a "Words to Know" glossary work well for
concept-driven kids' books and reinforce the lesson rather than diluting it.

### Trim, bleed, and margins

- Trim size: 8.5 x 8.5in unless the user specifies otherwise.
- Cover bleed: 0.125in (3.2mm) required on all sides. Bottom bleed cannot exceed 0.125in.
  KDP's own minimum keeps content ≥0.25in (6.4mm) from the outer trim edge, but **this
  project requires ≥0.5in from every raw PDF edge** — the stricter standing requirement
  above supersedes KDP's official minimum for all text placement decisions.
- Interior "No Bleed": page size = exact trim size. This project's interiors are always
  "No Bleed," which is what makes the DOCX interior format (see standing requirement
  above) workable. Interior "Full Bleed" (images running to the edge) is not used by this
  project — if a future book needs full-bleed interior art, flag to the user that this
  would force the interior back to PDF.
- Interior margins depend on page count:

  | Page count | Inside (gutter) margin | Outside margin, no bleed | Outside margin, with bleed |
  |---|---|---|---|
  | 24-150 pages | 0.375in | ≥0.25in | ≥0.375in |
  | 151-300 pages | 0.5in | ≥0.25in | ≥0.375in |

  (Higher page counts need a wider gutter still — see source for the full table.)

### Spine width — formula depends on paper AND ink, not one universal number

Compute this from the *final* interior page count, and build the cover only after the
interior is finalized. There is no flat offset added — it's page count times a
coefficient, full stop:

- Black ink, white paper: `pages x 0.002252"`
- Black ink, cream paper: `pages x 0.0025"`
- Black ink, groundwood paper: `pages x 0.00235"`
- **Color ink (Standard or Premium), white paper: `pages x 0.002347"`** — use this one
  for a full-color illustrated picture book, not the black-ink coefficient.

Spine text is only printed if the book exceeds 79 pages — most picture books this size
have a blank spine, which is normal and expected, not a bug.

### File and format requirements

- Cover: PDF, or build with KDP's Cover Creator (which accepts JPG/PNG/GIF). A hand-built
  full-wrap PDF (what this pipeline produces) is the standard path.
- Interior: **this project delivers DOCX** (see standing requirement above), which KDP
  accepts and auto-converts for no-bleed interiors. (KDP's general rule: PDF is required
  if the interior has any bleed; DOC/DOCX/RTF/HTML/TXT are accepted only for no-bleed
  interiors.)
- Max file size 650MB. Embed all fonts where the format supports it, flatten
  transparency/layers in any embedded images, minimum font size 7pt.
- **Do not leave crop marks, trim marks, bookmarks, comments, invisible objects,
  annotations, placeholder text, or file metadata in the submitted files** — these are
  listed by Amazon as common causes of file rejection, and this project additionally
  treats any visible "fill this in" placeholder text as something to avoid even where
  KDP itself wouldn't reject it (see the no-placeholder-text standing requirement above).
  Sanity-check generated files for this before calling them final, especially if any step
  round-tripped through another tool (e.g. Word/LibreOffice export).
- Minimum image resolution 300 DPI (both cover and interior). Amazon also recommends
  *capping* resolution around 600 DPI — excessively high-res images can cause processing
  timeouts or manufacturing delays without adding visible print quality. If upscaling,
  don't wildly overshoot 300 DPI; targeting roughly 400-500 DPI (as this pipeline's
  scale factors do) is a reasonable, safe margin without over-inflating file size.
- Barcode: optional to supply your own; if omitted, KDP stamps one onto the back cover
  automatically. **Don't print visible placeholder text like "barcode area" directly on
  the back cover art** — it's real printed content, not just a design guide, and it will
  still be visible even after KDP's real barcode is placed nearby. Leave the safe area
  visually blank (a subtle box outline is fine internally, but strip any instructional
  text before the file is truly final) or omit the mockup box entirely and just leave
  that corner clear.
- Reading direction: left-to-right only, except Hebrew, Yiddish, and Japanese.

## Kindle eBook cover spec

Portrait, ~1.6:1 ratio, 1600x2560px, RGB, JPEG. Build this as its own flow-based layout
(not a crop of the print cover) — it doesn't have the same overlap risks as the print
cover because there's no spine/back-cover geometry to manage. All text on this cover must
meet the Kindle font-clarity requirement above (sharp and readable at thumbnail scale, and
auto-fit so long titles never run off the canvas edge).

## Front-cover design: pick based on the actual artwork, don't assume one layout

Look at the cover illustration before deciding:

- **If there's a genuinely clear, uncluttered zone** (e.g. open ground/sky at the bottom
  or top with no characters/objects touching it), a full-bleed cover with an opaque title
  band placed over that clear zone works well and looks bold.
- **If characters or objects touch most/all edges of the art** (typical of many
  AI-illustrated covers), use a "framed illustration" design instead: inset the full
  image (never cropped) inside a bordered mat, and put ALL title text in a dedicated band
  entirely outside/below the image. This guarantees zero overlap regardless of what's in
  the art.

This project's standing visual identity across the whole series is the **framed
illustration** design: cream background, a series banner ("SERIES NAME • Book N") above
the image, the framed square illustration with a gold border, and a title band below with
title/subtitle/author. Keep every book in this series visually consistent with this
pattern (front and back cover layout, fonts, colors) — if an earlier book in the series
used a different one-off layout (e.g. a full-bleed design), treat that as a bug to bring
into line with the rest of the series rather than an intentional variation, unless the
user says otherwise. When you need the square cover illustration for a book whose
original source image isn't available anymore, it can be extracted straight out of that
book's already-delivered Cover Print PDF (via `pikepdf`'s `PdfImage.extract_to`) — the
front-cover artwork embedded in that PDF is the same art, just previously composited
differently.

Either way, verify your choice empirically: render a strip of the bottom (or top) ~30%
of the cover art and look at it before committing to a layout, rather than assuming
there's a clear zone.

**Known bug to avoid in the framed-illustration layout:** when computing the image's
available height, make sure you subtract the bottom margin below the title band as well
as the band's own height — not just the top gap and band height. The wrong formula
(`avail_h = H - top_gap - band_h`) silently overlaps the image's bottom edge into the
band's territory by the size of that missing margin, which shows up as text poking
through the image border. The correct formula:

```python
band_y0 = 0.28*IN  # bottom margin below the band
avail_h = H - top_gap - band_h - band_y0
img_y = band_y0 + band_h
```

After building the cover, render it and visually confirm the title doesn't touch the art,
for both this layout and the full-bleed layout.

## Text-safety-margin verification (always run this, don't eyeball it)

This applies to the Cover Print PDF (the interior is DOCX now — see the legibility-check
section above for that file's own QA approach). This project has needed this margin fix
twice already (once to meet KDP's 0.375in minimum, once again to meet the project's
stricter 0.5in standing requirement) because the same layout constants get copy-pasted
from book to book. Always verify programmatically with `pdfplumber`, against whatever the
current required threshold is (0.5in / 36pt for this project):

```python
import pdfplumber

THRESH = 0.5 * 72  # points; this project's standing requirement

def check(pdf_path, label):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        W, H = page.width, page.height
        flagged = []
        for w in page.extract_words():
            x0, x1, top, bottom = w['x0'], w['x1'], w['top'], w['bottom']
            margin = min(x0, W - x1, top, H - bottom)
            if margin < THRESH:
                flagged.append((w['text'], round(margin / 72, 3)))
        print(label, 'words:', len(page.extract_words()), 'flagged:', len(flagged))
        if flagged:
            print('  ', flagged[:12])

check("cover_wrap.pdf", "Cover")
```

If anything is flagged, don't just nudge the flagged element — figure out *why* it's
close (usually a baseline that ignores font ascent/descent) and add a real buffer, not
just enough to clear the threshold by a hair. Concretely, for this pipeline's recurring
elements:

- **Front-cover series banner** (top of front cover, e.g. "CHIP'S AI ADVENTURES • Book
  N"): its baseline needs to sit *below* `H - 0.5in - ascent`, not just `H - 0.5in` — text
  is measured from the top of the glyph bounding box, which sits above the baseline by
  roughly 65% of the font size. A baseline of `H - 0.63*IN` (for a ~10.5pt font) gives a
  safe ~0.535in top margin with buffer to spare.
- **"by AUTHOR" lines** (front cover bottom, back cover bottom): baseline needs to sit
  *above* `0.5in + descent` from the bottom edge — descenders (the tail on "y", "g", etc.)
  extend below the baseline by roughly 20% of the font size. Padding the baseline offset
  by an extra ~8pt beyond the raw 0.5in target (e.g. `band_y + 26` instead of `band_y +
  18`, or `0.6*IN` instead of `0.5*IN`) reliably clears the margin with buffer.

When a margin bug or threshold change is found, check *every* book's cover in the series
for the same latent issue (copy-pasted layout code) — don't just fix the one file the
user reported. Rebuild and re-verify all of them in the same pass.

## Fixed-layout EPUB (bonus deliverable)

Hand-build a small EPUB3 from scratch rather than relying on a WYSIWYG tool:
`mimetype`, `META-INF/container.xml`, `OEBPS/content.opf` with
`rendition:layout=pre-paginated`, `nav.xhtml`, and one xhtml file per page using CSS
absolute positioning to match the print layout. Validate with `zipfile.testzip()` and
confirm the XML is well-formed before calling it done. Apply the Kindle font-clarity
requirement above to every page's text — including setting an explicit base font-size on
`html`/`body` so em-based sizes don't silently inherit an undefined/tiny default. Mention
in the metadata doc that Kindle Create (Amazon's own tool, built from the Interior Print
file) is the recommended path, and the EPUB is a bonus for advanced/direct upload.

**Build this as ONE shared, parameterized module (e.g. `epub_common.py` with a
`build_epub(cfg)` function) used by every book's thin per-book runner script, not as
independently copy-pasted layout code in each book's `build_epubN.py`.** This project
shipped the same layout bug to multiple books at once several times specifically because
each book's script started as a copy of another book's script. A shared module means a
fix made once (a font-fit function, a page's geometry) is a fix for every book
simultaneously, and there's exactly one place left to introduce a new bug. Each book's
runner script should contain only that book's data (title, pages, remember cards, rhyme,
note text, bio, image paths, output path, UID) and a call into the shared builder.

## Fixed-layout EPUB story-page design: consistent framed illustration + text card

Don't position the illustration and the story text independently with two unrelated
guessed values (e.g. a fixed-percentage image size plus a fixed `top:` percentage for the
text) — on any page where the image renders taller than expected, the text you "guessed"
would be below it instead overlaps it. Computing the text's top position purely from where
the image happens to end (`img_top + img_height + gap`) technically prevents overlap, but
produces a different image size and text position on every single page depending on that
page's line count, which reads as inconsistent and unpolished when the pages are turned in
sequence — a bug fix that stopped short of being a good design. Do it properly:

- Give every story page the **exact same illustration size and position** — a fixed square
  "frame" (white mat padding + gold border + rounded corners + soft shadow, mirroring this
  series' print-cover framed-illustration treatment) that never moves or resizes page to
  page. Consistency across page turns matters more than maximizing image size on any single
  page.
- Put a thin gold divider rule below the frame, then the story text inside its own
  **fixed-size rounded white "card"** underneath — also identical position/size on every
  page.
- **Top-align the text inside the card; don't vertically center it.** The only thing that
  changes per page is the font size *inside* the card, computed to be the largest size
  that fits that page's (wrap-aware, see below) line count within the card's fixed inner
  height. Short pages simply leave more empty space at the bottom of the card; that reads
  fine and is far safer than centering.
- Compute the per-page font size to be **wrap-aware**, not line-count-aware. Don't assume
  each authored sentence renders as exactly one line — estimate wrapped-line count from
  actual character width at each candidate font size (a real renderer's fallback font can
  be wider than whatever font you tested with), and subtract an explicit safety-margin
  buffer (e.g. 20-30px) from the available height budget so real-device font-metric
  variance can't push text past the card. **This safety-margin trick only protects a card
  whose displayed size is a large, FIXED box unrelated to the content — see the dedicated
  section below on auto-sizing cards for a case where that protection silently evaporates.**

```python
import re, math

def plain_len(s):
    return len(re.sub(r"<[^>]+>", "", s))

def wrapped_lines(text_len, font_size, width_px, char_w=0.58):
    cpl = max(1, int(width_px / (font_size * char_w)))
    return max(1, math.ceil(text_len / cpl))

def fit_lines(lines, inner_w, inner_h, max_size, min_size, line_height, safety=24):
    """For content with ZERO space between lines. Do not add any inline
    margin/gap to the HTML this sizes -- see the gap-count section below
    for why that mismatch is a silent-overflow bug."""
    lens = [plain_len(l) for l in lines]
    size = max_size
    while size > min_size:
        total = sum(wrapped_lines(l, size, inner_w) for l in lens)
        if total * size * line_height <= inner_h - safety:
            break
        size -= 1
    total = sum(wrapped_lines(l, size, inner_w) for l in lens)
    return size, total * size * line_height, total
```

- For any page with a heading/caption (e.g. a book's opening "Meet <Character>!" label),
  reserve a fixed eyebrow zone *above* the frame for it rather than letting its presence or
  absence shift the frame position — pages without a heading just leave that zone blank, so
  the frame position stays identical either way.
- Apply the same fixed-frame + card treatment, wrap-aware fit, and top-alignment to any
  other image+text page in the same book (e.g. a "Remember This!" recap page — see the
  dedicated section below for that page's specific content format) for visual consistency
  across the whole EPUB, not just the story pages.
- **This wrap-tolerant card component is the single most reliable text-layout primitive in
  this whole file — prefer reusing it over inventing a new, more "precise" layout for any
  new page type, even when the new content (e.g. short labeled keywords) seems like it
  wants its own bespoke treatment.** See the dedicated Remember-page section below for why
  a more "precise" single-line-fit alternative was tried and abandoned in favor of just
  reusing this card.
- **Every free-flowing prose block (not just the story card) needs an explicit paragraph
  margin reset and the same wrap-aware auto-fit** — don't leave any `<p>` relying on a
  renderer's undefined default margin. A page like "A Note for Grown-Ups" (several full
  sentences, meant to wrap across multiple lines, unlike the short one-sentence-per-line
  story cards) is exactly the case this bites: with no margin reset, the renderer's default
  ~1em top/bottom paragraph margin stacked with genuinely long wrapped sentences pushed the
  total block height past the fixed canvas and visibly cut off the last paragraph(s). Fix
  by giving every paragraph an explicit `margin` (zero, or a deliberate small
  `margin-bottom`) and running the same wrap-aware fit function (generalized to sum
  estimated wrapped lines across multiple prose paragraphs, not just single "lines") before
  choosing a font size, so the block height is always a known, verified quantity — never an
  assumption. **If that deliberate `margin-bottom` is non-zero, see the dedicated section
  below on keeping the fit function's gap math and the actual generated margins in sync —
  this is a distinct bug from the "no margin at all" case and bit this project again later
  even after this fix.**
- Center the whole content block vertically on the canvas rather than anchoring it to the
  top for pages with naturally short, fixed content (e.g. the Remember page, the About the
  Author page, or "A Note for Grown-Ups" once its actual block height is known after
  fitting) — a heading + image + short content block anchored at `top` leaves a visibly
  lopsided empty zone at the bottom of the page; compute total content height and offset
  everything down by `(canvas_h - content_h) / 2` so top/bottom whitespace stays balanced.
  This is a separate, page-level centering decision from the per-story-card text alignment
  above (which should stay top-aligned, not centered) — don't conflate the two.
- Since there's no HTML rendering engine in most sandboxed environments, verify with FOUR
  layers, not just one: (1) a pure math check that every page's computed block height fits
  its available height (log `block_h` vs `avail_h` for literally every page in the book and
  assert none overflow — not just a sample), (2) a PIL-based mock render using the exact
  same computed pixel values as the real CSS for at least the most-lines page, the
  fewest-lines page, and any page with unusual content (heading, long prose, Remember
  page), (3) make sure step (2)'s mock render actually reproduces the SAME CSS logic
  as production, including things like flex-centering-plus-offset combinations or a
  single-line-only fit function — a mock render that "looks fine" while quietly using
  different math than the real CSS is how bugs below shipped undetected the first time,
  and (4) a pixel-level scan of the actual embedded illustration *images themselves* (not
  just the text layered on top) for compositing/seam defects — see the dedicated section
  above on verifying illustration assets aren't corrupted, which is a category of bug none
  of the first three layers can catch since they're all about text layout, not image
  content. **For any page whose height check keeps reporting "fits" using the SAME
  character-width estimate that built it (layer 1), that's a self-consistency check, not
  independent verification — see the dedicated section below on auto-sizing cards for why
  an independent, real-font-metric re-check caught a class of risk that layer 1 alone
  could not.**
- If the user says a layout fix "still looks terrible" even after you've mathematically
  verified there's no overlap, that's a signal the bug is fixed but the design isn't good
  — don't just re-verify the same math again. Go back to the series' established visual
  language (what does the print cover/interior already look like?) and reuse it, rather
  than inventing a new one-off treatment for just this file. But also don't assume a
  "looks bad" report and a "text is literally outside the box / cut off / wrapping (or not
  wrapping) when it shouldn't" report are the same kind of problem — the latter are
  correctness bugs that no amount of redesign taste fixes; get the math right first, then
  worry about polish. And don't assume every "something looks wrong with a page" report is
  a text-layout bug at all — "pictures split into two" turned out to be a corrupted image
  asset, not a CSS problem; read what the user is describing literally before reaching for
  the layout-math toolbox.

## Fixed-layout EPUB: avoid CSS flexbox entirely -- use plain block layout with precomputed positions

This project shipped **two separate real bugs from the same root mechanism**: using CSS
flexbox (`display:flex`) for centering inside a fixed-layout EPUB, in a way that the
reading system rendered inconsistently with what a normal desktop browser (or a from-scratch
PIL mock render, which doesn't automatically replicate CSS layout bugs it doesn't know
about) would show:

1. A text card used `.card { display:flex; align-items:center; }` for vertical centering,
   AND ALSO had a manually-computed `margin-top` offset applied on top of it (meant to be
   an alternative way of centering). The two centering mechanisms stacked instead of one
   overriding the other, doubling the downward shift — on pages with a short text block (a
   large computed offset), the doubled shift pushed the text past the card's own bottom
   edge. Reported by the user as "text outside the placemat."
2. A title/copyright/rhyme/about-page wrapper used `.center { display:flex;
   align-items:center; }` around a `<p style="max-width:70%">`. Percentage `max-width` on
   a flex item's cross-axis is a known inconsistently-implemented CSS3 interaction, and it
   silently failed to constrain/wrap the paragraph correctly, cutting text off. Reported by
   the user as the About the Author page being cut off.

**The fix in both cases, and the standing rule going forward: don't use flexbox at all in
a fixed-layout Kindle EPUB.** Replace every centering/alignment need with plain block CSS
and positions computed in Python:

- Vertical centering of a content block → compute the block's actual height (via the
  wrap-aware fit functions above), then set an absolute `top` position equal to
  `(canvas_h - content_h) / 2`. No `display:flex`, no `align-items`, no `transform`.
- Horizontal centering of text → `text-align:center` on a plain block element (universally,
  boringly well-supported — this is NOT the risky part; flexbox is).
- A row of N equal-width cards → compute each card's `left%` and `width%` explicitly in
  Python and position each one with `position:absolute`, rather than `display:flex;
  justify-content:space-between`. (This project has since moved away from a multi-card row
  for the Remember page specifically — see below — but the "no flexbox, precompute
  positions" rule still applies to anything laid out as a grid/row.)
- A block element that needs a max content width → give it an explicit `width` (not
  `max-width` inside a flex parent) — a plain block element's `width` property is reliably
  respected by every rendering engine tested so far, in a way percentage `max-width` inside
  a flex item was not.

The broader lesson: a fixed-layout EPUB's target rendering engines (Kindle firmware,
Kindle Previewer, various e-reader apps) are often simplified or older WebKit forks with
incomplete/buggy CSS3 support. Prefer the boring, maximally-compatible subset of CSS
(absolute positioning with precomputed pixel/percent values, block-level elements,
`text-align`, explicit `width`/`height`) over newer layout modules (flexbox, grid,
transforms) even when the newer module would be more convenient to write — convenience for
the script author is not worth an unpredictable render on the actual target device.

## Fixed-layout EPUB "Remember This!" recap page: one big wrap-tolerant card, not many small single-line cards

This page recaps a book's key terms (2 to 5 short label+explanation pairs, varies by
book). Two earlier approaches to laying these out both failed in ways worth understanding,
because the *reason* they failed generalizes:

- **v1 — a single flex row of N bordered cards, one per keyword**, with wrap-tolerant text
  sized to a fixed card height. Result: on books with more cards, the cards got narrow
  enough that text visibly wrapped inside them, which read as cramped and inconsistent.
- **v2 — the same N small cards, but redesigned to SOLVE for a single-line font size**
  (using an average-character-width estimate) so text would never wrap, switching to a
  multi-row grid when there were more than 3 cards. This eliminated the *wrapping*, but a
  character-width estimate is still only an estimate — on the real device, some words
  rendered wider than predicted and spilled past their narrow card's edge. Reported by the
  user as "words outside of the text box." A single-line box has zero margin for that kind
  of estimation error; there's nowhere for a slightly-too-wide word to go.

**v3, the standing design: stop trying to precisely predict single-line text width in a
tight box. Put every keyword in ONE big card instead** — the same fixed-size, top-aligned,
WRAP-TOLERANT card component already used (and already verified reliable) on every story
page — formatted as one line per keyword: `<b>NAME:</b> explanation`. Because this card
allows wrapping, a slightly-off width estimate just means a line wraps a little
differently — never that a word renders outside the box. This is the general lesson: when
a "more precise" layout keeps needing tighter and tighter estimation to avoid visibly
breaking, that's a sign to make the container more forgiving (allow wrap, give it more
room) rather than to keep refining the estimate. Concretely:

- Build the keyword lines as `[f"<b>{name}:</b> {explanation}" for name, explanation in
  cards]` and run them through `fit_paragraphs()` (not `fit_lines()` — see the dedicated
  section below on why: this page needs visible spacing between keyword lines, and only
  `fit_paragraphs()` accounts for that spacing in its height math). Bold tags are stripped
  by `plain_len()`'s regex before measuring, so they don't skew the width estimate.
- Reuse the same `.card` CSS (top-aligned, `overflow:hidden` as a backstop, explicit
  paragraph margins) — set `text-align:left` on this card's inner wrapper specifically
  (list-style content reads better left-aligned than centered, unlike the narrative story
  text).
- Compute the card's real height from `fit_paragraphs()`'s returned block height (not a
  fixed guess), then re-center the whole content block (heading + illustration frame +
  this card) vertically on the canvas using that real height — same pattern as the
  note/about pages. **Do not size the card to hug that returned height exactly — see the
  dedicated section below on why an auto-sizing card needs an explicit cushion added on
  top of the computed height, not just the computed height itself.**
- This scales cleanly from 2 keywords to 5+ without any card-count-dependent layout logic
  (no row-splitting, no per-row centering, no shared-width-across-rows math) — more or
  fewer lines just changes the auto-fit font size and the card's height, nothing else
  about the layout changes.

## Fixed-layout EPUB: an inline margin on every line must match the fit function's gap-count assumption exactly

A fourth EPUB bug (Book 4, "Chip and the Mystery Library," Remember page) came from a
different failure mode than the wrap-estimation bugs above — not imprecise text-width
estimation, but a **mismatch between the CSS actually rendered and the math used to size
the box for it**:

- The v3 Remember-page HTML generation gave every `<p>` line (including the *last* one) an
  inline `margin-bottom:0.4em` for visible spacing between keyword lines. But the card's
  height was originally computed with `fit_lines()`, whose formula
  (`total_lines * size * line_height`) has **no margin/gap term at all** — it assumes
  lines stack with zero space between them.
- Result: the real rendered block was taller than the computed/allocated card by
  `n_lines * 0.4 * font_size` px (56px on this book's 5-keyword card) — enough to push the
  last keyword line past the card's bottom edge. Because `.card { overflow:hidden; }` is
  used everywhere as a safety backstop, the overflow didn't reflow or visibly break the
  page layout — it just silently clipped the last line, which is exactly why this shipped
  as a passing "does every page fit" math check the first time (that check was validating
  `fit_lines()`'s own, internally-consistent-but-wrong number, not the actual rendered
  DOM). Reported by the user as "text being cut off... on the remember this page."
- The general bug class: **any place inline styling adds spacing between elements, and a
  separate function computes the box height that content needs to fit in, is a place
  those two things can silently drift apart.** It doesn't matter how good the
  wrap-estimation is if the height formula and the actual generated markup are answering
  different questions about how much vertical space the content occupies.
- **The same latent pattern was found (proactively, by auditing every page using this
  fit-function-plus-inline-margin combination, not just the one reported) on the
  copyright page and the rhyme page** — both had generous-enough height budgets that the
  mismatch hadn't yet been pushed past the visible-clipping threshold, but the underlying
  math was identically wrong. Fixed both preemptively rather than waiting for a future
  report.

**The fix, and the standing rule:** use `fit_paragraphs()` (not `fit_lines()`) for any
block where the HTML generation adds inter-line/inter-paragraph spacing, and always
generate that spacing so it matches an `n-1` gap count exactly — explicitly omit the
margin on the last item in the generation loop, rather than relying on CSS `:last-child`
(inline `style=` attributes written per-item in a Python loop don't get the benefit of a
stylesheet's `:last-child` selector the way a shared CSS class does):

```python
def fit_paragraphs(paragraphs, inner_w, inner_h, max_size, min_size, line_height,
                    gap_em, safety=24):
    """For content where the generated HTML puts real margin/gap spacing
    BETWEEN items (n-1 gaps, matching a last-item-has-no-margin generation
    loop). Do not use fit_lines() for this content -- its height formula
    has no gap term and will under-allocate the box."""
    paragraphs = [p for p in paragraphs if plain_len(p) > 0]
    lens = [plain_len(p) for p in paragraphs]
    size = max_size
    while size > min_size:
        total_lines = sum(wrapped_lines(l, size, inner_w) for l in lens)
        gap_px = max(0, len(paragraphs) - 1) * gap_em * size
        if total_lines * size * line_height + gap_px <= inner_h - safety:
            break
        size -= 1
    total_lines = sum(wrapped_lines(l, size, inner_w) for l in lens)
    gap_px = max(0, len(paragraphs) - 1) * gap_em * size
    return size, total_lines * size * line_height + gap_px

# HTML generation MUST mirror the exact same n-1 gap count used above --
# margin on every item except the last, nothing more clever than that:
GAP_EM = 0.4
html = "".join(
    f"<p style='font-size:{size}px;line-height:{line_height};"
    f"margin-bottom:{0 if i == len(paragraphs) - 1 else GAP_EM}em;'>{p}</p>"
    for i, p in enumerate(paragraphs)
)
```

Use `fit_lines()` only for content with genuinely zero space between lines — and don't add
any inline margin to that content's HTML either, or the same mismatch reappears in the
opposite direction. Use `fit_paragraphs()` any time the HTML adds real spacing between
items (Remember-page keyword lines, copyright-page lines, rhyme-page lines, "A Note for
Grown-Ups" paragraphs), and always audit the generated `<p>` loop itself for the same n-1
pattern when reviewing or debugging this kind of page — don't just check that a
`fit_paragraphs()` call exists, confirm the HTML generation actually matches its
assumption.

**This bug pattern doesn't announce itself in a "did every page fit" math check, because
that check re-runs the same (in this case wrong) formula that produced the box allocation
in the first place — it will report a clean pass right up until the box is genuinely too
small for what's really being rendered.** The only way this specific bug was actually
found was by extracting and reading the real generated XHTML out of the already-built
`.epub` (`zipfile` + `.read()` on `OEBPS/remember.xhtml`) and checking the literal
`margin-bottom` value written on the last `<p>` tag, rather than re-trusting the Python-side
numbers a second time. **When a user reports text cut off on a page that a math check
already called "fits," read the actual built markup before concluding the report must be
about a stale file or re-running the same check** — and while in there, audit every other
page using the same fit-function-plus-inline-margin pattern, since this project's
copyright and rhyme pages had the identical latent bug sitting unreported.

## Fixed-layout EPUB: an auto-sized card must carry its own safety cushion, not just borrow the fit function's

A fifth Remember-page bug (still Book 4-and-5-shaped, but this time affecting all 5 books
identically) surfaced after the margin/gap fix above: the user reported "remember this
page has text cut off" a second time, without naming a book. Direct investigation this
time found **no overflow** by re-running the same estimate that built the page (of course
not — re-running the identical formula just reproduces the identical, self-consistent
answer). A genuinely independent check — an actual PIL font-metrics simulation using real
`.ttf` glyph widths (bold and regular separately, not one flat `CHAR_W` average) instead of
the character-count estimate — also came back clean for the current keyword text in all 5
books. But it surfaced something the estimate alone couldn't: **every one of the 5 books'
Remember cards had exactly 0px of margin between the card's actual height and the
estimated content height.**

The reason: unlike every fixed-size card elsewhere in the book (story cards, note page,
etc.), the Remember card **auto-sizes to hug the estimated content height** —
`rem_card_h_actual = rem_block_h + 2*REM_CARD_PAD_V`, with no cushion term. The `SAFETY`
constant subtracted during font-size selection only guarantees the chosen font fits within
a much bigger, unrelated *fixed budget* (`REM_CARD_INNER_H_BUDGET`, based on the full page
height) — it says nothing about the *final displayed card*, which is sized to the estimate
with surgical precision. A fixed-size card has real slack: being some pixels under a big,
constant box is genuine tolerance. An auto-sized card sized to the exact estimate has
**no** tolerance at all — if the real device (a specific Kindle firmware/app's default
sans-serif, not the DejaVu Sans stand-in used for verification, and not the flat `CHAR_W`
average used for layout) renders even slightly wider than assumed, there is zero room to
absorb that difference before `.card { overflow:hidden; }` clips it.

**The fix:** add an explicit, unconditional buffer to the auto-sized card's final height —
not to the font-selection budget (already has one), to the *card itself*:

```python
REM_CARD_SAFETY_BUFFER = 30  # px of real, unconditional cushion in the final card
rem_card_h_actual = rem_block_h + 2 * REM_CARD_PAD_V + REM_CARD_SAFETY_BUFFER
```

Apply this any time a card/box is sized by adding a fixed padding to a *computed* content
height (auto-sizing), as opposed to being a large constant box the computed content just
needs to fit inside (fixed-sizing). The two need different protection: a fixed box's
protection comes from the gap between a generous constant and the (smaller) real content;
an auto-sized box has no such gap by construction, so its protection has to be added
explicitly as its own line in the formula, every time.

**When re-verifying a "should already be fixed" report, prefer an independent method over
re-running the same formula.** The character-count `wrapped_lines()` estimate can't ever
disagree with itself; a second, independently-implemented check (a real font-metrics
render, even with a stand-in font, or literally opening the file and looking) is what
actually tells you whether the original estimate was trustworthy in the first place, and
in this case revealed the *design* was fragile (zero margin everywhere) even though the
specific numbers happened not to be over budget for the current text.

## Verifying resolution (always do this explicitly, never just assert it)

Don't estimate DPI from source-image dimensions alone — verify what actually ends up in
the delivered files, since an image may be scaled up or down when placed. For the cover
PDF (and for any interim/QA-rendered PDF of the DOCX interior), use `pikepdf` to read each
page's content stream, extract the `cm` (transformation matrix) operands for each drawn
image, and cross-reference against the embedded XObject's actual pixel dimensions:

```python
import pikepdf

def check(pdf_path, label):
    pdf = pikepdf.open(pdf_path)
    print(f"\n=== {label} ({pdf_path}) - {len(pdf.pages)} page(s) ===")
    for pno, page in enumerate(pdf.pages):
        content = pikepdf.parse_content_stream(page)
        xobjs = page.get("/Resources", {}).get("/XObject", {})
        cur_cm = None
        for operands, operator in content:
            if str(operator) == "cm":
                cur_cm = [float(x) for x in operands]
            if str(operator) == "Do" and cur_cm:
                name = str(operands[0])
                if name in xobjs:
                    xobj = xobjs[name]
                    try:
                        px_w, px_h = int(xobj.Width), int(xobj.Height)
                    except Exception:
                        continue
                    a, b, c_, d, e, f = cur_cm
                    draw_w_pt, draw_h_pt = abs(a), abs(d)
                    if draw_w_pt > 0 and draw_h_pt > 0:
                        dpi_w = px_w / (draw_w_pt / 72.0)
                        dpi_h = px_h / (draw_h_pt / 72.0)
                        print(f"  page {pno+1} {name}: {px_w}x{px_h}px drawn "
                              f"{draw_w_pt/72:.2f}x{draw_h_pt/72:.2f}in -> "
                              f"{dpi_w:.0f} x {dpi_h:.0f} DPI")

check("interior_qa_render.pdf", "Interior (QA render of the delivered DOCX)")
check("cover_wrap.pdf", "Cover")
```

For the DOCX interior itself, cross-check embedded image resolution directly (e.g. via
`python-docx` to pull each embedded image and check its native pixel dimensions against
its displayed size in the document) in addition to the QA-render check above. Confirm
every value is at or above 300 DPI (and not wildly over ~600 DPI per the file-size
guidance above), and report the actual numbers to the user. Also confirm the Kindle cover
JPG is exactly 1600x2560 RGB via PIL.

## KDP Metadata & Best-Seller Strategy doc — structure

A Word doc the user copy-pastes from directly into the KDP listing form. Sections, in
order:

1. **Book Details** — title, subtitle, series name + number, author, language, age/grade
   range, and the interior ink option to select (Premium Color, per the standing default
   — call this out explicitly given how it affects the minimum page count).
2. **Series setup** — if book 2+: instructions to add this book to the existing KDP
   series (not recreate it). If book 1: instructions to create the series fresh.
3. **Product Description** — 3-4 short paragraphs, KDP-description-field-ready: a hook,
   what the character learns, what makes this book/series distinct, and a closing line
   that names the other books in the series by title for cross-promotion.
4. **7 Keywords** — concrete, specific search phrases a parent or gift-buyer would type
   (age range, subject/skill taught, "picture book," gift/nonfiction angle, series name).
   Avoid generic single words.
5. **Categories** — up to 3 KDP browse categories. Keep these consistent across every book
   in the same series so they reinforce each other in Amazon's category rankings.
6. **Pricing table** — paperback and eBook price ranges, matching prior books in the
   series for consistency (typically $12.99-$14.99 paperback, $3.99-$4.99 eBook for a
   ~24-32pg color picture book; adjust to genre/market norms if different).
7. **Best-seller launch tactics** — series-aware tactics: box-set bundling once 3+ books
   exist, using an interior activity page as shareable social-proof, cross-linking
   descriptions, and asking prior-book reviewers directly for launch-week reviews on the
   new book (review velocity in week one matters most for ranking).
8. **Optional additions** — mention that the interior's copyright page doesn't print an
   ISBN (KDP assigns a free one during setup, or the user can supply their own there), and
   that the About the Author page currently has one general sentence which the user is
   welcome to expand into a fuller bio before final upload. Frame these as optional
   reminders in this doc, not as literal placeholder text sitting inside the book itself
   (see the no-placeholder-text standing requirement above — the interior itself should
   stay clean).

## KDP Publishing Guide doc — structure

A second Word doc that's a literal step-by-step walkthrough, written for someone who has
never used KDP before:

- A "Your Files" table mapping each deliverable filename to what it's used for — note
  next to the Interior Print entry that it's a `.docx` and KDP will auto-convert it on
  upload (no bleed setting to worry about, since this project's interiors are always "No
  Bleed").
- If book 2+ in a series: a "Part A0 — link the series" step first.
- Part A — Publish the Paperback: create title, fill in details (pointing back at the
  metadata doc), upload interior (DOCX file; trim size and no-bleed setting; ink =
  Premium Color per the standing default), upload cover (PDF), preview/price/publish.
- Part B — Publish the Kindle eBook: Option 1 (recommended) Kindle Create from the
  Interior Print DOCX; Option 2 (advanced) direct EPUB upload.
- Troubleshooting — reiterate the exact trim settings and ink option the files were built
  for, and any book-specific notes (e.g. thin-spine books have blank/no spine text —
  that's normal under 80 pages).

## Workflow order

1. Read the manuscript, confirm character/series consistency with the user if anything
   looks off (see "gather" step above).
2. Confirm the ink option (Premium Color by standing default for this project) and check
   the resulting minimum page count for the chosen trim size before finalizing story
   length.
3. Finalize story text and page count; add on-theme back matter if under the minimum.
4. Upscale/verify illustration resolution (target ~400-500 DPI, don't overshoot ~600).
5. Build the interior as a DOCX (see standing requirement above), with no placeholder
   text anywhere in it (see standing requirement above). Get the final page count from it,
   and confirm no page came out unexpectedly near-blank (a sign of text/image overflow).
6. Build the cover PDF using that exact page count and the ink-appropriate spine formula
   above, and the series' established framed-illustration layout. Render and visually
   check for overlap, and check the barcode-safe-area doesn't have printed placeholder
   text on it.
7. Build the Kindle eBook cover JPG, with title/subtitle auto-fit so long text can't run
   off the canvas edge.
8. Build the fixed-layout EPUB via the shared `epub_common.py` module (see dedicated
   sections above) — explicit base font-size, consistent framed-illustration + top-aligned
   text-card design with wrap-aware font fitting reused on every text page (including
   Remember This — one big card, not many small ones, with its own explicit safety-buffer
   cushion since it auto-sizes to content), NO flexbox anywhere (plain block layout with
   precomputed absolute positions only), and any page whose HTML adds real inter-line/
   paragraph margin sized with `fit_paragraphs()` (not `fit_lines()`) so the fit math and
   the generated markup agree on the exact same gap count.
9. Write the metadata doc and guide doc.
10. Convert the metadata/guide Word docs (and the interior DOCX, for QA purposes only) to
    PDF and render page 1+ of each as a quick visual QA check before calling anything done
    (catches docx-library formatting mistakes cheaply).
11. Run the DPI verification pass on the cover PDF and the interior's embedded images, the
    text-safety-margin verification pass (0.5in threshold) on the cover PDF, and the
    manuscript/interior legibility check (font size, cutoff/overlap, contrast, image
    clarity) on every page — report actual numbers and findings to the user. For the EPUB
    specifically, also run the wrap-aware block-height-vs-available-height check on every
    single page of every book (not a sample) and report a clean "ALL PAGES FIT" result per
    book. Additionally, for any page whose card/box uses `overflow:hidden` as a backstop,
    directly extract and read that page's real generated XHTML out of the built `.epub`
    (`zipfile` + `.read()`) at least once and confirm the literal margin values match the
    fit function's gap assumption — the math check alone can't catch this class of bug
    (see the dedicated section above). Also run the seam/compositing scan (see the
    dedicated "Verifying illustration assets aren't corrupted" section above) across every
    book's embedded page images, since neither the text-fit checks nor a quick visual skim
    reliably catch a defect baked into the image file itself. For any auto-sized card
    (height computed from content rather than a fixed constant), confirm it carries its
    own explicit safety buffer beyond the computed content height — a passing fit check
    alone doesn't prove that, since the check and the box are built from the same estimate
    (see the dedicated section above).
12. Deliver all six files per book using the naming convention above (interior as `.docx`,
    cover as `.pdf`), and summarize: page count, ink option assumed, resolution
    verification results, text-margin verification results, legibility-check results, and
    any content/character-consistency decisions made along the way.

## Practical gotchas from experience

- reportlab's `roundRect()` does not accept `strokeColor` as a keyword argument — call
  `c.setStrokeColor(...)` before `roundRect()` instead, or it throws a TypeError.
- If working in a sandboxed environment with a separate "outputs" folder that can't have
  files deleted or renamed once written: do all iterative/preview work in a scratch temp
  directory, and only copy (not write-then-delete) into the outputs folder once a file is
  truly final. Overwriting an existing outputs file via copy is fine; deleting is often
  not. If a title or protagonist name changes mid-project, the new deliverables will have
  different filenames than the old ones — the old, now-stale files will still be sitting
  in the outputs folder since they can't be deleted; explicitly tell the user which
  filenames are current and which are stale leftovers to ignore.
- The scratch/temp working directory (e.g. `/tmp/...`) is NOT guaranteed to persist across
  sessions, even though the outputs folder does. If you come back to a project and the
  scratch directory with source images/build scripts is gone, you can usually reconstruct
  what you need from what's already been delivered: extract embedded images straight out
  of a previously-delivered Cover Print PDF (`pikepdf`), Interior Print DOCX (read
  `word/media/*` out of the docx zip directly with Python's `zipfile`), or — for EPUB page
  art specifically — straight out of a previously-delivered `.epub` (it's also just a zip;
  `unzip` it and pull `OEBPS/images/*` directly, which is simpler than going through the
  PDF/DOCX route when an EPUB was already shipped) rather than re-generating art from
  scratch. Match media files back to their page order carefully (e.g. by filename, or by
  the order they were inserted in the build script) before renaming them. Some scratch
  files (e.g. a per-book `book_data.py` with all story text/metadata, or a shared
  `epub_common.py` layout module) may still be sitting in a *different* persistent location
  (e.g. an outputs/build folder) even after `/tmp` resets — check there before
  regenerating story data or layout code from scratch. **A recovery/extraction step like
  this is also a plausible source of a corrupted image asset (a botched crop pasting a
  fragment of the wrong page into another page's image) — see the dedicated "Verifying
  illustration assets aren't corrupted" section above for a real case of this on Book 4.**
- When a cover-overlap or layout bug is found and fixed, check whether earlier books in
  the same series share the same latent bug (copy-pasted layout code) — fix and rebuild
  those too rather than leaving an inconsistency. This has happened repeatedly on this
  project: the 0.375in margin fix, the later tightening to 0.5in, a Kindle-cover
  title-overflow bug, and the EPUB story-page overlap/overflow/flexbox/wrapping bugs all
  turned out to affect multiple books at once because the same layout constants (or, in
  the EPUB's case, entire copy-pasted per-book scripts) were duplicated book to book —
  check every sibling book, not just the one that was reported. Extracting shared logic
  into one module (like `epub_common.py`) is the structural fix for this whole class of
  problem — prefer that over continuing to patch N copies in parallel. When a *design* fix
  (not just a bug fix) is made after user pushback like "still looks terrible," don't
  propagate it to sibling books automatically — confirm the redesign is approved first,
  then ask whether to roll it out series-wide (a direct "redo all of the ebook contents"
  or "update all EPUBs"-type request is explicit permission to do so). Note that a
  corrupted-image-asset bug (see above) is NOT automatically a copy-paste bug across
  books — it can be isolated to just the specific files that went through a bad
  recovery/upscale step, so run the seam scan across every book to check rather than
  assuming it's series-wide OR assuming it's isolated. A margin/tolerance-design bug (like
  the auto-sizing-card cushion fix above), by contrast, WAS identical across all 5 books
  since they all share `epub_common.py` — fix it once there and rebuild every book.
- If a user reports "cover text too close to the edge" and you've already fixed this
  exact issue before, don't assume the newly uploaded file is stale before checking — the
  requirement itself may have changed (e.g. from 0.375in to 0.5in). Always re-measure the
  actual uploaded file against the *current* threshold before concluding it's a duplicate
  report of an old, already-fixed file.
- If asked to make one book's cover match "the rest of the series," don't assume the
  older book just needs new title/author text swapped into its existing one-off layout —
  check whether it's using the same underlying design (framed illustration, series
  banner, etc.) as its siblings at all. An early book in a series is a likely place for a
  leftover pre-series-convention layout to still be lurking.
- When a character name or title changes, grep *every* build script (interior, cover,
  ebook-cover, EPUB) for the old name — it's commonly hardcoded in 2-4 places outside the
  central story-data file (page headings like "X's Memory Rhyme," blurb text, EPUB UID
  strings, output filenames), and missing even one makes the deliverables inconsistent
  with each other in a way that's easy for the user to spot and hard for them to trust.
- Before telling a user a rebuild is unnecessary because the source file "hasn't
  changed" (verified by hash), double check whether *your own* output actually matches
  the source text verbatim. A file can be byte-identical to what you processed before
  while your generated content still diverges from it, if an earlier step in the
  conversation deliberately rewrote story content. Compare your delivered text to the
  manuscript's actual wording before asserting nothing is wrong — don't just compare
  file hashes and assume that settles it.
- Don't re-ask about the ink option for this project — Premium Color is the confirmed
  standing default (see top of this file). Only raise it if the user brings up a
  different trim size, paper type, or explicitly changes the ink choice.
- The cover text-safety margin for this project is 0.5in (see standing requirement
  above), stricter than KDP's official 0.375in minimum — use 0.5in as the real target for
  all future books and cover edits in this series, not the official minimum.
- The interior deliverable is DOCX, not PDF (see standing requirement above) — this is a
  project-specific choice, not a KDP requirement, so don't silently "improve" it back to
  PDF; if a future book's design genuinely needs interior bleed (which would force PDF),
  flag that trade-off to the user rather than deciding unilaterally.
- The interior should never contain visible bracketed placeholder text (no ISBN
  placeholder, no author-bio placeholder — see standing requirement above); if you find
  yourself writing something like `[Add ... here]` into a deliverable meant to be
  published as-is, that's a sign it belongs in the metadata/guide doc instead.
- Existing already-shipped books built before these requirements (0.5in cover margin,
  DOCX interior, no placeholder text, explicit legibility check) were updated retroactively
  where the user asked for it, but format/content changes like DOCX-vs-PDF are NOT applied
  automatically to already-shipped books just because the skill changed — treat "add this
  to the skill" requests as applying to future work by default, and confirm with the user
  before assuming they also want every already-shipped book changed to match.
- A fixed-layout EPUB story page that technically has zero text/image overlap (verified
  mathematically) can still be rejected by the user as bad *design* — "no overlap" is the
  floor, not the goal. Use the series' own established framed-illustration + card pattern
  (see dedicated EPUB section above) as the actual design target, not just gap-based
  positioning that happens to avoid collisions.
- **Never use CSS flexbox in a fixed-layout Kindle EPUB** (see the dedicated section
  above) — this project shipped two separate real bugs from it: a `.card`
  `display:flex;align-items:center` combined with a manual `margin-top` offset that
  double-shifted text past the card's bottom edge ("text outside the placemat"), and a
  `.center` `display:flex` wrapper around a `<p style="max-width:70%">` that let the About
  the Author text get cut off (percentage `max-width` inside a flex item's cross-axis is
  inconsistently implemented across rendering engines). Use plain block layout with
  Python-precomputed absolute positions/widths for everything — centering, multi-card
  rows, max-width constraints — instead. A from-scratch PIL mock render of a page's layout
  is only a valid sanity check if its Python math actually reproduces the same logic as
  the real CSS; it won't automatically surface a CSS-specific bug it doesn't know exists,
  which is exactly how both of these shipped undetected the first time.
- A block-height auto-fit function that assumes one authored "line" of text = one
  rendered line is only safe if you're also confident the renderer's actual font metrics
  won't wrap it — don't assume this silently. Use a wrap-aware estimate (character count
  ÷ estimated chars-per-line at the candidate font size) even for short, pre-authored
  "one sentence per line" content, and always run it for genuinely long free-flowing prose
  (like an author's note) where wrapping is expected and load-bearing for the layout math.
- **When a layout keeps needing a more precise width/wrap estimate to avoid visibly
  breaking (text wrapping when it shouldn't, or overflowing a box), that's a signal to
  make the container more forgiving instead of refining the estimate further.** The
  Remember page went through exactly this progression: allow-wrap-in-a-tight-box (looked
  cramped) → solve-for-single-line-in-a-tight-box (estimation errors put words outside the
  box on the real device) → one big allow-wrap card (robust, because a wrap-tolerant
  container has nowhere for an estimation error to cause visible breakage) → **that big
  card, itself auto-sized with zero cushion, still needed an explicit safety buffer added
  to its own final height** (see the dedicated section above) — making a container
  wrap-tolerant removes width-estimation risk, but doesn't automatically remove
  height-estimation risk if the container's height is *also* derived from the same
  estimate with no added slack. Both dimensions need their own margin for error.
- Any `<p>` tag written into fixed-layout EPUB XHTML needs an explicit `margin` — don't
  assume `margin:0` from a sibling CSS class covers every paragraph in the book. The "A
  Note for Grown-Ups" page's cutoff bug traced back to exactly this: every other page's
  paragraphs had margin reset via a shared class, but this one page's paragraphs used raw
  inline styles with no margin property, silently inheriting the renderer's default
  paragraph spacing and pushing the block past the canvas.
- When the user says "redo all of the ebook contents" / "update all EPUBs" (or similar)
  after a fix has been validated on one book, that's explicit permission to roll the fix
  out series-wide — don't just fix the reported book and mention the others exist. Check
  whether the other books' EPUB scripts still contain the pre-fix design and bring them up
  to the same shared, fixed implementation in the same pass, recovering any missing
  scratch assets (source images, book data) from already-delivered files rather than
  asking the user to re-provide them.
- Recap-card counts vary by book in this series (2 keywords in Book 2, 3 in Books 1 and 3,
  5 in Books 4 and 5) — the Remember page's one-big-card design handles this naturally
  (more keywords just means more lines and a taller/smaller-font card, no structural
  change needed), which is part of why it's preferable to the old per-card grid approach
  that needed genuinely different layout logic (row-splitting, shared card width) at
  different card counts.
- **An auto-fit function and the HTML it sizes for must agree on *exactly* how many gaps
  exist between lines/paragraphs** — `fit_lines()` assumes zero, `fit_paragraphs()`
  assumes `n-1` (matching a last-item-has-no-margin generation pattern). Giving every
  `<p>` (including the last) an inline `margin-bottom` while sizing the box with
  `fit_lines()` is a silent-overflow bug: `.card { overflow:hidden; }` clips the excess
  without any visible layout break, so the standard "does every page fit" math check keeps
  reporting a clean pass even though the real render doesn't fit. This shipped on the
  Remember page (Book 4, "Chip and the Mystery Library") and was latent-but-not-yet-visible
  on the copyright and rhyme pages (fixed proactively once the pattern was recognized).
  When one of these is reported as cut off despite a passing fit check, verify by reading
  the actual built XHTML out of the delivered `.epub`, not by re-running the same
  fit-function math a second time — see the dedicated section above for the full fix.
- **Not every "something's wrong with this page" report is a text-layout bug.** A user
  report of "some pics on some pages are split into two" turned out to be a corrupted
  source *image* file (a white seam plus a mismatched second image bled into the bottom of
  four Book 4 story illustrations), not a CSS/layout issue at all — none of this project's
  text-fit or flexbox checks could have caught it, because they only ever look at the text
  layered on top of an image, never the image's own pixel content. When a report doesn't
  obviously map to text overlap/cutoff/wrapping, consider that the defect might be baked
  into the illustration asset itself, and run the seam/compositing scan (see the dedicated
  section above) across the actual embedded images before assuming it's another layout-math
  bug. This class of defect can also be present in the print interior's copy of the same
  artwork (or, confusingly, not — this project's print and EPUB image sets turned out not
  to be identical files) — check the print interior independently and flag it to the user
  rather than assuming a fix in one deliverable covers the other, or rebuilding the print
  interior unprompted.
- **A "fits" verdict is only as trustworthy as how independent the check was from the
  estimate that built the thing being checked.** The Remember page's card height, the
  math-based "does it fit" verification log, and the PIL mock render can all agree the
  page is fine while all three are quietly built on the exact same `CHAR_W` average —
  which tells you the code is internally consistent, not that it matches the real device.
  When a bug is reported a second time after a fix that mathematically checked out, reach
  for a genuinely independent verification method (e.g. real font-metric rendering with an
  actual `.ttf`, not a character-count estimate) rather than re-running the same formula
  and reporting the same "no overflow found" result. See the dedicated
  "auto-sized card must carry its own safety cushion" section above for exactly this
  situation and its fix.
- **Don't overwrite a saved skill with placeholder/stub content, even temporarily, as a
  two-step "clear then rewrite" approach.** `save_skill` replaces the entire skill body in
  one call — there is no intermediate "draft" state, so a call made with placeholder text
  "to be filled in next" actually deletes the real content immediately and is visible to
  the user as a broken skill until the next call succeeds. Always assemble the complete,
  final skill body in memory first, and make exactly one `save_skill` call with the real
  content already in place.
