"""Code-composed music bed for the series (fully owned, no licence question).

Soft lo-fi corporate bed: 92 BPM, I–vi–IV–V in C (C, Am, F, G), warm electric-piano chords, round bass,
gentle pluck melody on off-beats, quiet shaker. Deterministic (fixed seed). Length = composition length
with 1.5 s fade-in and 3 s fade-out, so it never ends early.
Run: python tools/compose_bgm.py <seconds> <out.wav>
"""
import sys, wave
import numpy as np

SR = 44100
BPM = 92
BEAT = 60 / BPM
dur = float(sys.argv[1])
out = sys.argv[2]
n = int(dur * SR)
mix = np.zeros(n)
rng = np.random.default_rng(7)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def note(t0, length, midi, amp, kind):
    i0 = int(t0 * SR)
    if i0 >= n:
        return
    m = min(int(length * SR), n - i0)
    t = np.arange(m) / SR
    f = hz(midi)
    if kind == "ep":      # electric piano: sine + soft 2nd/3rd partials, bell-ish decay
        w = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 3) + 0.12 * np.sin(6 * np.pi * f * t) * np.exp(-t * 5)
        env = np.minimum(t / 0.01, 1) * np.exp(-t * 1.1)
    elif kind == "bass":  # round sine bass
        w = np.sin(2 * np.pi * f * t) + 0.2 * np.sin(4 * np.pi * f * t)
        env = np.minimum(t / 0.015, 1) * np.exp(-t * 1.6)
    else:                 # pluck
        w = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) * np.exp(-t * 8)
        env = np.minimum(t / 0.004, 1) * np.exp(-t * 4.5)
    mix[i0:i0 + m] += amp * w * env


CHORDS = [  # (bass midi, chord midis, melody pool)
    (36, [60, 64, 67, 71], [72, 76, 79]),   # Cmaj7
    (33, [57, 60, 64, 67], [72, 76, 69]),   # Am7
    (29, [57, 60, 65, 69], [72, 77, 69]),   # Fmaj7
    (31, [59, 62, 67, 71], [74, 79, 71]),   # G (add 7)
]
bar = 4 * BEAT
t, k = 0.0, 0
while t < dur:
    bass, chord, pool = CHORDS[k % 4]
    for b in range(4):                                   # chords on beats 1 and 3 (soft), bass on 1 and 3
        if b in (0, 2):
            for j, mn in enumerate(chord):
                note(t + b * BEAT + j * 0.012, bar / 2 + 0.6, mn, 0.055, "ep")
            note(t + b * BEAT, bar / 2, bass, 0.16, "bass")
    for b in range(8):                                   # sparse pluck melody on some off-beats
        if rng.random() < 0.45:
            note(t + b * BEAT / 2 + BEAT / 4, 0.8, int(rng.choice(pool)), 0.05, "pluck")
    for b in range(8):                                   # shaker: filtered noise ticks on eighths
        i0 = int((t + b * BEAT / 2) * SR)
        m = min(int(0.06 * SR), n - i0)
        if m > 0:
            nz = rng.standard_normal(m)
            nz = np.diff(np.concatenate([[0], nz]))     # crude high-pass
            mix[i0:i0 + m] += (0.012 if b % 2 else 0.007) * nz * np.exp(-np.arange(m) / SR * 60)
    t += bar
    k += 1

# gentle low-pass smoothing + fades + normalise to -3 dBFS
kernel = np.ones(3) / 3
mix = np.convolve(mix, kernel, mode="same")
fi, fo = int(1.5 * SR), int(3.0 * SR)
mix[:fi] *= np.linspace(0, 1, fi)
mix[-fo:] *= np.linspace(1, 0, fo)
mix /= np.max(np.abs(mix)) / 0.7
pcm = (mix * 32767).astype(np.int16)
with wave.open(out, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", out, f"{dur:.1f}s")
