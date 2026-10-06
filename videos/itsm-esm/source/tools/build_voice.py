"""Builds the voice track of the film and its word timings (the single source of truth for every cue).

Each sentence is synthesized whole (natural prosody), trimmed, then placed on the timeline with the silence written in
the script after it. Word times inside a sentence come from the pauses the voice makes at its commas (exact) and, inside
each comma group, from the length of each word (close enough: cues are shown 2 frames early).

usage: build_voice.py <project_dir>
"""
import difflib
import hashlib
import json
import os
import re
import sys
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from tts_lib import tts, say, asr, transcribe

PROJECT = sys.argv[1]
OUT_SR = 48000
LEAD = 0.30  # silence before the first word
SPEED = {"s8": 0.9, "s9": 0.92, "s10": 0.94}  # per-sentence speed (default 0.96)

# (shown text, spoken text, silence after in s, tag)
SCRIPT = [
    ("Un nouvel arrivant.", "Un nouvel arrivant.", 0.30, "s1"),
    ("Premier jour.", "Premier jour.", 0.32, "s2"),
    ("Pas d'ordinateur, pas de badge, pas d'accès.", "Pas d'ordinateur, pas de badge, pas d'accès.", 2.60, "s3"),
    ("L'informatique attend les RH.", "L'informatique attend les RH.", 0.28, "s4"),
    ("Les RH attendent la finance.", "Les RH attendent la finance.", 0.28, "s5"),
    ("Et chacun suit sa demande dans son propre tableau.", "Et chacun suit sa demande dans son propre tableau.", 0.95, "s6"),
    ("Et si tout passait par une seule porte ?", "Et si tout passait par une seule porte ?", 1.05, "s7"),
    ("L'ITSM organise le service informatique : un catalogue clair, des tickets suivis, des délais tenus.",
     "L'i té esse aime organise le service informatique. Un catalogue clair. Des tickets suivis. Des délais tenus.",
     0.45, "s8"),
    ("L'ESM applique la même méthode à toute l'entreprise.", "L'eu esse aime applique la même méthode à toute l'entreprise.", 0.40, "s9"),
    ("Une seule demande déclenche tout : le poste, le badge, les accès, le contrat.",
     "Une seule demande déclenche tout. Le poste. Le badge. Les accès. Le contrat.", 0.45, "s10"),
    ("Et la direction voit enfin où se perd le temps.", "Et la direction voit enfin où se perd le temps.", 0.85, "s11"),
    ("Une seule porte pour tous vos services.", "Une seule porte pour tous vos services.", 3.40, "s12"),
]


TAKES = 8


def norm(text):
    t = text.lower().replace("rh", "éraches").replace("itsm", "i t s m").replace("esm", "e s m").replace("usm", "e s m")
    return re.sub(r"[^a-zà-ÿ ]", "", t)


def frames(a, sr, win=0.01):
    n = int(sr * win)
    m = len(a) // n
    e = np.sqrt(np.mean(a[: m * n].reshape(m, n) ** 2, axis=1) + 1e-12)
    return 20 * np.log10(e), win


def trim(a, sr, thr_db=-42):
    db, win = frames(a, sr)
    idx = np.where(db > thr_db)[0]
    s = max(0, idx[0] - 1) * int(sr * win)
    e = min(len(a), (idx[-1] + 2) * int(sr * win))
    return a[s:e]


def pauses(a, sr, thr_db=-38, min_len=0.09):
    """Internal silences (start, end) in s, longest first."""
    db, win = frames(a, sr)
    quiet = db < thr_db
    out, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if i > 0 and j < len(quiet) and (j - i) * win >= min_len:
                out.append((i * win, j * win))
            i = j
        else:
            i += 1
    return out


def weight(word):
    w = re.sub(r"[^\wÀ-ÿ]", "", word)
    return max(len(w), 1) + 1.5  # a floor for short words (the voice never says them in no time)


def distribute(words, t0, t1):
    tot = sum(weight(w) for w in words)
    out, t = [], t0
    for w in words:
        d = (t1 - t0) * weight(w) / tot
        out.append({"word": w, "start": round(t, 3), "end": round(t + d, 3)})
        t += d
    return out


def main():
    engine = tts("tom")
    rec = asr()
    track = [np.zeros(int(LEAD * OUT_SR), dtype=np.float32)]
    t = LEAD
    sentences = []
    report = []
    for shown, spoken, gap, tag in SCRIPT:
        # several takes, keep the one Whisper understands best (the method's "2 or 3 takes")
        key = hashlib.sha1(f"{spoken}|{SPEED.get(tag, 0.96)}".encode()).hexdigest()[:10]
        cache = os.path.join(PROJECT, "assets", "audio", "takes", f"{tag}-{key}.wav")
        best = None
        if os.path.exists(cache):
            a, sr = sf.read(cache, dtype="float32")
            best = (1.0, a, sr, "(cached take)", "cache")
        for take in range(0 if best else TAKES):
            a, sr = say(engine, spoken, sid=0, speed=SPEED.get(tag, 0.96))
            a = trim(a, sr)
            heard = transcribe(rec, resample_poly(a, 16000, sr).astype(np.float32), 16000)
            score = difflib.SequenceMatcher(None, norm(heard), norm(shown)).ratio()
            if best is None or score > best[0]:
                best = (score, a, sr, heard, take)
        score, a, sr, heard, take = best
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        sf.write(cache, a, sr, subtype="FLOAT")
        report.append(f"{tag}: take {take} score {score:.2f}: {heard}")
        a48 = resample_poly(a, OUT_SR, sr).astype(np.float32)
        dur = len(a48) / OUT_SR
        # comma groups of the shown text; a lone ":" or "?" (French spacing) sticks to the word before it
        groups = []
        for g in re.split(r"(?<=[,:])\s+", shown):
            ws = []
            for w in g.split():
                if re.fullmatch(r"[:;?!]", w) and ws:
                    ws[-1] += "\u00a0" + w
                else:
                    ws.append(w)
            if ws:
                groups.append(ws)
        # each comma boundary snaps to the detected pause nearest to where the word lengths put it
        tot = sum(weight(w) for g in groups for w in g)
        expected, acc = [], 0.0
        for g in groups[:-1]:
            acc += sum(weight(w) for w in g) / tot * dur
            expected.append(acc)
        found = pauses(a, sr)
        bounds = [0.0]
        for x in expected:
            near = min(found, key=lambda p: abs((p[0] + p[1]) / 2 - x)) if found else None
            if near and abs((near[0] + near[1]) / 2 - x) < 0.6:
                found.remove(near)
                bounds += [near[0], near[1]]
            else:
                bounds += [x, x]
        bounds.append(dur)
        words = []
        for gi, g in enumerate(groups):
            words += distribute(g, t + bounds[2 * gi], t + bounds[2 * gi + 1])
        sentences.append({"id": tag, "text": shown, "start": round(t, 3), "end": round(t + dur, 3),
                          "gap_after": gap, "words": words})
        track.append(a48)
        track.append(np.zeros(int(gap * OUT_SR), dtype=np.float32))
        t += dur + gap
    voice = np.concatenate(track)
    voice = voice / (np.max(np.abs(voice)) + 1e-9) * 0.89
    os.makedirs(os.path.join(PROJECT, "assets", "audio"), exist_ok=True)
    sf.write(os.path.join(PROJECT, "assets", "audio", "voix-raw.wav"), voice, OUT_SR, subtype="PCM_24")
    total = round(len(voice) / OUT_SR, 3)
    with open(os.path.join(PROJECT, "onsets.json"), "w") as f:
        json.dump({"total": total, "sentences": sentences}, f, ensure_ascii=False, indent=1)
    print("\n".join(report))
    print(f"total {total} s")
    for s in sentences:
        print(f"{s['id']:>4} {s['start']:6.2f} -> {s['end']:6.2f}  {s['text']}")


main()
