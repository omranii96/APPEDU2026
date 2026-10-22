"""Music, sound effects and final mix of the film, all locked on onsets.json (the same cues as index.html).

The music is original and synthesized here (no generated-music model, no downloaded track): a ticking tension bed
up to the pivot, cut by a low impact, then a warm major "élan" at 100 BPM whose first downbeat lands on "L'ITSM".
Sound effects come from HyperFrames' media-use library (Pixabay Content License).

usage: build_audio.py <project_dir> <sfx_dir>
writes <project>/assets/audio/{voix.wav, music.wav, sfx.wav, mix.wav} and sfx-events.json
"""
import json
import os
import subprocess
import sys
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

PROJECT, SFX_DIR = sys.argv[1], sys.argv[2]
SR = 48000
D = json.load(open(os.path.join(PROJECT, "onsets.json")))
S = {s["id"]: s for s in D["sentences"]}
TOTAL = D["film"]
N = int(TOTAL * SR)
rng = np.random.default_rng(7)


def cue(sid, i):
    return S[sid]["words"][i]["start"]


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def place(buf, clip, t, gain=1.0):
    i = int(round(t * SR))
    if i < 0:
        clip, i = clip[-i:], 0
    j = min(len(buf), i + len(clip))
    if j > i:
        buf[i:j] += clip[: j - i] * gain


def db(x):
    return 10 ** (x / 20)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x, axis=0)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x, axis=0)


def env(n, a, d_rel, sustain=1.0, hold=None):
    """attack a s, then exponential decay with time constant d_rel s"""
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-4), np.exp(-(t - a) / d_rel) * sustain + (1 - sustain) * 0)
    return e


def stereo(m, pan=0.0):
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    return np.stack([m * l, m * r], axis=1) * 1.414


def saw(f, n, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for k in range(1, 18):
        if f * k > 9000:
            break
        out += np.sin(2 * np.pi * f * (1 + detune) * k * t) / k
    return out * 0.6


def note(f, dur, kind="pad", vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    if kind == "pad":
        x = (saw(f, n, 0.0) + saw(f, n, 0.004) + saw(f, n, -0.004)) / 3
        x = lp(x, 1600)
        a, r = 0.35, 0.5
        e = np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (dur - t) / r))
        return x * e * vel
    if kind == "pluck":
        x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
        return x * np.exp(-t / 0.22) * np.minimum(1, t / 0.003) * vel
    if kind == "bell":
        x = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.4)
        return x * np.exp(-t / 1.4) * np.minimum(1, t / 0.004) * vel
    if kind == "bass":
        x = lp(saw(f, n), 320) + 0.6 * np.sin(2 * np.pi * f * t)
        e = np.minimum(1, t / 0.01) * np.exp(-t / 0.35)
        return x * e * vel
    raise ValueError(kind)


def hz(name):
    names = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    p, o = name[:-1], int(name[-1])
    return 440 * 2 ** ((names[p] + (o - 4) * 12) / 12)


def tick(freq, vel=1.0):
    n = int(0.06 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.012) + 0.5 * rng.standard_normal(n) * np.exp(-t / 0.004)
    return hp(x, 900) * vel


def kick(vel=1.0):
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    f = 50 + 70 * np.exp(-t / 0.03)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.12) * vel


def hat(vel=1.0):
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7000) * np.exp(-t / 0.012) * vel


def reverb(x, secs=2.2, mix=0.22):
    n = int(secs * SR)
    t = np.arange(n) / SR
    ir = np.stack([rng.standard_normal(n), rng.standard_normal(n)], axis=1) * np.exp(-t / (secs / 5))[:, None]
    ir = lp(ir, 5000)
    ir /= np.sqrt(np.sum(ir ** 2, axis=0))
    wet = np.stack([fftconvolve(x[:, c], ir[:, c])[: len(x)] for c in range(2)], axis=1)
    return x * (1 - mix) + wet * mix * 1.6


# ---------------------------------------------------------------- music
G0, G1 = S["s3"]["end"], S["s4"]["start"]   # the silent gag
GL = G1 - G0
T_OUT = S["s6"]["end"] + 0.08                # lights out, door after door
T_FLASH = S["s8"]["start"] - 0.34            # the door floods the frame with light
T_IMPACT = T_OUT + 0.35                      # cut to black
T_DROP = cue("s8", 0)     # "L'ITSM": first downbeat of the élan
BAR = 2.4                 # 100 BPM, 4/4
T_IMP = S["s11"]["end"] + 0.18
T_END = T_IMP + 0.42

tension = np.zeros((N, 2))
# tick-tock at 120 BPM, accelerating during the silent gag (the clock that spins)
t = 0.3
k = 0
while t < T_IMPACT - 0.05:
    in_gag = G0 + 0.14 <= t < G1 - 0.46
    place(tension, stereo(tick(1900 if k % 2 == 0 else 1350, 0.5), -0.25 if k % 2 == 0 else 0.25), t)
    if in_gag:
        p = (t - G0 - 0.14) / (GL - 0.6)
        t += 0.24 * (1 - p) + 0.05 * p
    else:
        t += 0.5
    k += 1
# low pulse on A, filter opening with the build
for i in range(int((T_IMPACT - 0.3) / 0.25)):
    tt = 0.3 + i * 0.25
    if G0 + 0.09 <= tt < G1 - 0.36:
        continue
    vel = 0.55 if i % 2 == 0 else 0.32
    x = note(hz("A1"), 0.3, "bass", vel)
    cutoff = 220 + 900 * max(0, (tt - 8) / (T_IMPACT - 8))
    place(tension, stereo(lp(x, cutoff)), tt)
# dark pad (A minor add9), slowly swelling
for ch, (a, b) in enumerate([(0.0, G1), (G1, T_IMPACT)]):
    for f, v in [("A2", 0.5), ("E3", 0.4), ("C4", 0.32), ("B3", 0.22)]:
        x = note(hz(f), b - a + 0.6, "pad", v * (0.8 if ch == 0 else 0.95))
        place(tension, stereo(x, 0.0), a)
# riser into the cut
riser = load(os.path.join(SFX_DIR, "riser.mp3"))
pk = np.argmax(np.abs(riser).sum(axis=1)) / SR
place(tension, riser, T_IMPACT - pk, 0.55)
# hard stop at the impact
cut = int(T_IMPACT * SR)
fade = np.linspace(1, 0, int(0.02 * SR))[:, None]
tension[cut: cut + len(fade)] *= fade
tension[cut + len(fade):] = 0
tension = reverb(tension, 1.6, 0.18)

# pivot air: two quiet high sines
pivot = np.zeros((N, 2))
for f in ("E5", "B5"):
    x = note(hz(f), T_FLASH - T_OUT - 0.65, "pad", 0.08)
    place(pivot, stereo(lp(x, 3000), 0.2 if f == "E5" else -0.2), T_OUT + 0.65)

# élan: D major, I-V-vi-IV
elan = np.zeros((N, 2))
CH = {"D": ["D3", "F#3", "A3", "D4"], "A": ["A2", "E3", "A3", "C#4"], "Bm": ["B2", "F#3", "B3", "D4"], "G": ["G2", "D3", "G3", "B3"]}
ROOT = {"D": "D2", "A": "A1", "Bm": "B1", "G": "G1"}
# as many bars as the solution lasts, ending on the dominant before the final D of the end card
nb = max(2, int(np.ceil((T_END - T_DROP) / BAR)))
prog = [["D", "A", "Bm", "G"][i % 4] for i in range(nb - 1)] + ["A"]
for b, c in enumerate(prog):
    t0 = T_DROP + b * BAR
    for f in CH[c]:
        place(elan, stereo(note(hz(f), BAR + 0.3, "pad", 0.22), 0.0), t0)
    for beat in range(4):
        place(elan, stereo(note(hz(ROOT[c]), 0.55, "bass", 0.55 if beat % 2 == 0 else 0.4)), t0 + beat * 0.6)
        place(elan, stereo(kick(0.55 if beat % 2 == 0 else 0.38)), t0 + beat * 0.6)
        if b >= 1:
            place(elan, stereo(hat(0.22), 0.3), t0 + beat * 0.6 + 0.3)
    arp = [CH[c][i] for i in (1, 2, 3, 2)] * 2
    for i, f in enumerate(arp):
        o = int(f[-1]) + 1
        place(elan, stereo(note(hz(f[:-1] + str(o)), 0.5, "pluck", 0.2), -0.3 if i % 2 else 0.3), t0 + i * 0.3)
# the implosion breathes in, the end card resolves on D with a bell
T_FINAL = T_DROP + len(prog) * BAR
for f in CH["D"] + ["F#4", "A4"]:
    place(elan, stereo(note(hz(f), 5.5, "pad", 0.2)), T_END)
place(elan, stereo(note(hz("D2"), 2.0, "bass", 0.6)), T_END)
for i, f in enumerate(["D5", "A5", "F#5", "D6"]):
    place(elan, stereo(note(hz(f), 2.5, "bell", 0.14), -0.2 + 0.13 * i), T_END + 0.05 + i * 0.12)
# keep the groove only up to the implosion, a short dip before the end card
g = np.ones(N)
a, b = int(T_IMP * SR), int(T_END * SR)
groove_end = np.ones(N)
elan_main = elan.copy()
elan_main[a:b] *= np.linspace(1, 0.25, b - a)[:, None]
fin = int((TOTAL - 3.0) * SR)
elan_main[fin:] *= np.linspace(1, 0, N - fin)[:, None] ** 1.5
elan = reverb(elan_main, 2.2, 0.2)
elan[: int((T_DROP - 0.02) * SR)] = 0

# ---------------------------------------------------------------- sound effects (locked on the picture)
EV = []


def sfx(name, t, gain_db=-6.0):
    EV.append({"t": round(t, 3), "name": name, "gain_db": gain_db})


T_IT, T_RH, T_FI = cue("s4", 0), cue("s4", 3), cue("s5", 4)
sfx("pop", 0.18, -12); sfx("pop", cue("s1", 2) - 0.1, -14)
sfx("whoosh-short", cue("s2", 0) - 0.14, -16); sfx("click", cue("s2", 0) + 0.04, -10)
sfx("whoosh-short", cue("s3", 0) - 0.24, -16); sfx("pop", cue("s3", 0) - 0.14, -11)
for tt in (cue("s3", 1) + 0.2, cue("s3", 4) + 0.05, cue("s3", 6) + 0.06):
    sfx("click", tt, -8)
sfx("whoosh-short", G0 + 0.07, -16)
for tt in (G0 + 0.285 * GL, G0 + 0.515 * GL, G0 + 0.746 * GL):
    sfx("click-soft", tt, -16)
sfx("pop", G1 - 0.44, -14); sfx("whoosh", G1 - 0.36, -9); sfx("click-soft", G1 + 0.02, -12)
sfx("pop", cue("s4", 1) - 0.05, -11); sfx("whoosh-short", T_RH - 0.15, -15); sfx("whoosh", T_RH, -12)
sfx("pop", cue("s5", 2) - 0.05, -11); sfx("whoosh-short", T_FI - 0.15, -15); sfx("whoosh", T_FI, -12)
sfx("pop", T_FI + 0.55, -12)
sfx("whoosh", cue("s6", 1) - 0.08, -14)
for tt in (cue("s6", 2), cue("s6", 3) + 0.1, cue("s6", 4)):
    sfx("click-soft", tt, -15)
for tt in (cue("s6", 6) - 0.12, cue("s6", 7) - 0.12, cue("s6", 8) - 0.12):
    sfx("pop", tt, -11)
for tt in (T_OUT, T_OUT + 0.2):
    sfx("click", tt, -12)
sfx("impact-bass-1", T_IMPACT, -14)
sfx("sparkle", cue("s7", 5) - 0.05, -18)
wc = load(os.path.join(SFX_DIR, "whoosh-cinematic.mp3"))
wc_pk = np.argmax(np.abs(wc).sum(axis=1)) / SR
sfx("whoosh-cinematic", T_FLASH + 0.02 - wc_pk, -15)
sfx("sparkle", T_FLASH + 0.02, -12)
sfx("click-soft", cue("s8", 0) - 0.066, -14); sfx("click-soft", cue("s8", 1), -17)
sfx("whoosh-short", cue("s8", 5) - 0.1, -16)
sfx("pop", cue("s8", 6) - 0.1, -14); sfx("pop", cue("s8", 6) + 0.1, -16)
TCLICK = cue("s8", 8) - 0.04
sfx("click", TCLICK, -6); sfx("whoosh-short", TCLICK + 0.1, -16); sfx("pop", TCLICK + 0.16, -12)
for tt in (cue("s8", 9) + 0.05, cue("s8", 10) + 0.05, cue("s8", 12), cue("s8", 13) + 0.1):
    sfx("click-soft", tt, -12)
sfx("pop", cue("s8", 11) - 0.2, -14); sfx("ping", cue("s8", 13) + 0.05, -16)
T_ESM = cue("s9", 0)
sfx("whoosh", T_ESM - 0.2, -11); sfx("click-soft", T_ESM - 0.066, -12); sfx("pop", T_ESM + 0.3, -15)
for tt in (cue("s9", 1), cue("s9", 3), cue("s9", 4), cue("s9", 6)):
    sfx("whoosh-short", tt - 0.12, -17); sfx("pop", tt + 0.05, -13)
T_ONE = cue("s10", 0)
sfx("whoosh", T_ONE - 0.15, -13); sfx("pop", T_ONE - 0.02, -12)
T_SEND = cue("s10", 3) + 0.02
sfx("click", T_SEND, -5); sfx("pop", T_SEND + 0.24, -14)
sfx("whoosh-short", cue("s10", 4) - 0.05, -15); sfx("pop", cue("s10", 4) + 0.02, -12)
for tt in (cue("s10", 6), cue("s10", 8), cue("s10", 10)):
    sfx("click", tt + 0.02, -9)
sfx("click", cue("s10", 12) + 0.02, -9); sfx("notification", cue("s10", 12) + 0.04, -9)
sfx("whoosh", cue("s11", 0) - 0.12, -12); sfx("pop", cue("s11", 0) + 0.02, -12)
sfx("click-soft", cue("s11", 3) - 0.1, -16); sfx("error", cue("s11", 7) - 0.05, -18); sfx("pop", cue("s11", 7) + 0.05, -13)
sfx("whoosh-cinematic", T_IMP - 0.2, -20)
sfx("impact-bass-2", T_END, -19); sfx("sparkle", T_END + 0.05, -12)
T_BTN = S["s12"]["end"] + 0.1
T_CL = T_BTN + 0.85
sfx("pop", T_BTN, -12); sfx("whoosh-short", T_CL - 0.55, -18); sfx("click", T_CL, -5); sfx("chime", T_CL + 0.04, -10)

sfx_buf = np.zeros((N, 2))
cache = {}
for e in EV:
    if e["name"] not in cache:
        cache[e["name"]] = load(os.path.join(SFX_DIR, e["name"] + ".mp3"))
    place(sfx_buf, cache[e["name"]], e["t"], db(e["gain_db"]))

# ---------------------------------------------------------------- voice processing
v, vsr = sf.read(os.path.join(PROJECT, "assets", "audio", "voix-raw.wav"), dtype="float64")
assert vsr == SR
v = hp(v, 85)
# gentle presence and warmth
pres = sosfilt(butter(2, [2500, 5000], "band", fs=SR, output="sos"), v)
warm = sosfilt(butter(2, [150, 300], "band", fs=SR, output="sos"), v)
v = v + 0.35 * pres + 0.15 * warm
voice = np.zeros((N, 2))
voice[: min(N, len(v))] = stereo(v[:N], 0.0)[: min(N, len(v))] * 0.707
voice = reverb(voice, 0.7, 0.07)

# ---------------------------------------------------------------- mix: music ducked under the voice
venv = np.sqrt(np.maximum(lp(np.mean(voice ** 2, axis=1), 6), 0))
venv = venv / (venv.max() + 1e-9)
speaking = np.clip((venv - 0.02) / 0.06, 0, 1)
# attack 40 ms, release 300 ms
duck = np.zeros(N)
a_c, r_c = np.exp(-1 / (0.04 * SR)), np.exp(-1 / (0.3 * SR))
acc = 0.0
for i in range(0, N, 48):
    target = speaking[i]
    c = a_c ** 48 if target > acc else r_c ** 48
    acc = target + (acc - target) * c
    duck[i: i + 48] = acc
music_gain = db(-8.0) ** duck  # -8 dB under the voice

tension_gain, elan_gain = db(-17.0), db(-13.5)
music = (tension * tension_gain + pivot * db(-14) + elan * elan_gain) * music_gain[:, None]
mix = voice * db(-2.0) + music + sfx_buf
audio_dir = os.path.join(PROJECT, "assets", "audio")
sf.write(os.path.join(audio_dir, "music.wav"), music.astype(np.float32), SR, subtype="FLOAT")
sf.write(os.path.join(audio_dir, "sfx.wav"), sfx_buf.astype(np.float32), SR, subtype="FLOAT")
sf.write(os.path.join(audio_dir, "voix.wav"), voice.astype(np.float32), SR, subtype="FLOAT")
sf.write(os.path.join(audio_dir, "mix-pre.wav"), mix.astype(np.float32), SR, subtype="FLOAT")
json.dump(EV, open(os.path.join(audio_dir, "sfx-events.json"), "w"), indent=1)


def lufs(path, start, end):
    out = subprocess.run(["ffmpeg", "-v", "info", "-ss", str(start), "-to", str(end), "-i", path, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    for line in out.splitlines()[::-1]:
        if "I:" in line and "LUFS" in line:
            return float(line.split("I:")[1].split("LUFS")[0])


raw_music = (tension * tension_gain + elan * elan_gain)
sf.write(os.path.join(audio_dir, "_music-unducked.wav"), raw_music.astype(np.float32), SR, subtype="FLOAT")
print(f"tension {lufs(os.path.join(audio_dir, "_music-unducked.wav"), 8, 15.5):.1f} LUFS, élan {lufs(os.path.join(audio_dir, "_music-unducked.wav"), 20, 40):.1f} LUFS (target: tension 2 to 3 dB under)")
print(f"{len(EV)} sound effects placed")
