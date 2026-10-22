"""Builds the voice track from ONE external take of the whole script (ElevenLabs, Higgsfield...).

The take is cut only in its silences: every pause becomes a candidate cut, each chunk is transcribed by Whisper, and a
dynamic programme groups consecutive chunks into the 12 sentences of the script (best total text match). The sentences
are then placed with the silences the storyboard needs (gag, pivot, end), exactly like build_voice.py.

usage: build_voice_take.py <project_dir> <take.wav|mp3>
A fast reader leaves short pauses: TAKE_MIN_PAUSE (s, default 0.12) and TAKE_FLOOR_DB (default -38) cut finer.
"""
import difflib
import os
import subprocess
import sys
import numpy as np
from scipy.signal import resample_poly
from build_voice import SCRIPT, assemble, distribute, groups_of, norm, word_times
from tts_lib import asr, transcribe

SR = 48000


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def chunks(a, win=0.01, min_pause=0.12, floor_db=-38):
    """Voiced chunks (start, end) in samples, split at every pause of min_pause s or more."""
    n = int(SR * win)
    m = len(a) // n
    e = 20 * np.log10(np.sqrt(np.mean(a[: m * n].reshape(m, n) ** 2, axis=1) + 1e-12))
    idx = np.where(e > np.max(e) + floor_db)[0]
    if len(idx) == 0:
        return []
    segs, s0, prev = [], idx[0], idx[0]
    for f in idx[1:]:
        if (f - prev - 1) * win >= min_pause:
            segs.append((s0, prev + 1))
            s0 = f
        prev = f
    segs.append((s0, prev + 1))
    # a fragment (breath, the tail of a word) joins the neighbour it is closest to
    merged = True
    while merged and len(segs) > 1:
        merged = False
        for i, (s0, s1) in enumerate(segs):
            if (s1 - s0) * win >= 0.4:
                continue
            gap_before = s0 - segs[i - 1][1] if i > 0 else 10 ** 9
            gap_after = segs[i + 1][0] - s1 if i + 1 < len(segs) else 10 ** 9
            if gap_before <= gap_after:
                segs[i - 1] = (segs[i - 1][0], s1)
            else:
                segs[i + 1] = (s0, segs[i + 1][1])
            del segs[i]
            merged = True
            break
    pad = 3
    return [(max(0, s - pad) * n, min(m, t + pad) * n) for s, t in segs]


def align(texts, targets):
    """Splits the consecutive texts into len(targets) runs that best match the targets (dynamic programme).
    Returns [(first, last_exclusive), ...]."""
    n, k = len(texts), len(targets)
    best = np.full((n + 1, k + 1), -1e9)
    back = np.zeros((n + 1, k + 1), dtype=int)
    best[0][0] = 0
    for j in range(1, k + 1):
        for i in range(j, n - (k - j) + 1):
            for p in range(j - 1, i):
                if best[p][j - 1] < -1e8:
                    continue
                text = norm(" ".join(texts[p:i]))
                sc = difflib.SequenceMatcher(None, text, targets[j - 1]).ratio() * max(len(targets[j - 1]), 1)
                if best[p][j - 1] + sc > best[i][j]:
                    best[i][j] = best[p][j - 1] + sc
                    back[i][j] = p
    runs, i = [], n
    for j in range(k, 0, -1):
        p = back[i][j]
        runs.append((p, i))
        i = p
    return runs[::-1]


def sentence_words(a, s, sub, texts, shown):
    """Word cues of one sentence, relative to its start s (samples), from its chunks: a chunk that holds one comma
    group gives that group exact bounds; a chunk that holds several is split at its own pauses."""
    groups = groups_of(shown)
    gt = [norm(" ".join(g)) for g in groups]
    if len(sub) >= len(groups):
        runs = align(texts, gt)  # several chunks per group
        spans = [(sub[r0][0], sub[r1 - 1][1], [g]) for (r0, r1), g in zip(runs, groups)]
    else:
        runs = align(gt, [norm(x) for x in texts])  # several groups per chunk
        spans = [(c0, c1, groups[r0:r1]) for (r0, r1), (c0, c1) in zip(runs, sub)]
    words = []
    for c0, c1, gs in spans:
        t0, t1 = (c0 - s) / SR, (c1 - s) / SR
        if len(gs) == 1:
            words += distribute(gs[0], t0, t1)
        else:
            words += word_times(a[c0:c1], SR, " ".join(" ".join(g) for g in gs), t0)
    return words


def main():
    project, take = sys.argv[1], sys.argv[2]
    a = load(take)
    a = a / (np.max(np.abs(a)) + 1e-9)
    ch = chunks(a, min_pause=float(os.environ.get("TAKE_MIN_PAUSE", 0.12)),
                floor_db=float(os.environ.get("TAKE_FLOOR_DB", -38)))
    rec = asr()
    heard = [transcribe(rec, resample_poly(a[s:e], 16000, SR).astype(np.float32), 16000) for s, e in ch]
    for (s, e), h in zip(ch, heard):
        print(f"  chunk {s / SR:6.2f} -> {e / SR:6.2f}  {h}")
    targets = [norm(shown) for shown, _, _, _ in SCRIPT]
    n, k = len(ch), len(targets)
    if n < k:
        sys.exit(f"only {n} chunks for {k} sentences: the take has fewer pauses than sentences")
    cuts = align(heard, targets)
    parts = []
    for (p, i), (shown, _, gap, tag) in zip(cuts, SCRIPT):
        s, e = ch[p][0], ch[i - 1][1]
        seg = a[s:e].copy()
        fade = int(0.005 * SR)
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
        ratio = difflib.SequenceMatcher(None, norm(" ".join(heard[p:i])), norm(shown)).ratio()
        print(f"{tag:>4} {ratio:.2f}  {' '.join(heard[p:i])}")
        parts.append((seg, SR, shown, gap, tag, sentence_words(a, s, ch[p:i], heard[p:i], shown)))
    sentences = assemble(project, parts)
    for s in sentences:
        print(f"{s['id']:>4} {s['start']:6.2f} -> {s['end']:6.2f}  {s['text']}")


if __name__ == "__main__":
    main()
