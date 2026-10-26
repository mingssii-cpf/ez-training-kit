"""Caption timing from real voice files (audio/voice/<id>.wav), regardless of TTS provider.

Each scene was synthesised as one take, so line boundaries come from the take's own pauses:
silencedetect finds the gaps, and each boundary between script.json "lines" is snapped to the
gap nearest its character-proportional estimate. A boundary with no gap within MAX_DEV_S is
reported and the run fails, instead of silently falling back to an estimate.

Run: python align.py <episode-dir>
Writes timing.json in the same contract eplib reads:
  {scene_id: {"audio", "audio_s", "start", "dur", "subs": [{"t", "d", "text"}]}, "_total": s}
"""
import json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()  # episode folder
script = json.loads((ROOT / "script.json").read_text(encoding="utf-8"))
LEAD, TAIL = script["lead_s"], script["tail_s"]
NOISE, MIN_GAP, MAX_DEV_S = "-38dB", 0.08, 1.2
MIN_RATE, MAX_RATE = 6.0, 20.0  # Thai chars (spaces excluded) per second of speech


def silences(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
                          f"silencedetect=n={NOISE}:d={MIN_GAP}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).group(3)) + \
        60 * int(re.search(r"Duration: (\d+):(\d+)", err).group(2))
    if len(ends) < len(starts):
        ends.append(dur)
    return list(zip(starts, ends)), dur


def align(sid, lines):
    path = ROOT / "audio" / "voice" / f"{sid}.wav"
    gaps, dur = silences(path)
    head = gaps[0][1] if gaps and gaps[0][0] < 0.05 else 0.0
    tail = gaps[-1][0] if gaps and gaps[-1][1] >= dur - 0.05 else dur
    inner = [g for g in gaps if g[0] > head + 0.2 and g[1] < tail - 0.2]
    chars = [len(l.replace(" ", "")) for l in lines]
    total, cum, bounds, problems = sum(chars), 0, [], []
    for i in range(len(lines) - 1):
        cum += chars[i]
        est = head + (tail - head) * cum / total
        lo = bounds[-1][1] if bounds else head
        cands = [g for g in inner if g[0] > lo + 0.3]
        best = min(cands, key=lambda g: abs((g[0] + g[1]) / 2 - est), default=None)
        if best is None or abs((best[0] + best[1]) / 2 - est) > MAX_DEV_S:
            problems.append(f"{sid}: no pause near line {i + 1}/{i + 2} boundary (est {est:.2f}s)")
            best = (est, est)
        bounds.append(best)
    edges = [head] + [b for g in bounds for b in g] + [tail]
    spans = [(edges[2 * k], edges[2 * k + 1]) for k in range(len(lines))]
    for (a, b), n, txt in zip(spans, chars, lines):  # a snap onto a mid-word gap shows up as an absurd rate
        if not MIN_RATE <= n / max(b - a, 0.01) <= MAX_RATE:
            problems.append(f"{sid}: implausible rate {n / max(b - a, 0.01):.1f} chars/s for line '{txt}'")
    return dur, spans, problems


def main():
    out, t, problems = {}, 0.0, []
    for sc in script["scenes"]:
        sid, lines = sc["id"], sc["lines"]
        dur, spans, probs = align(sid, lines)
        problems += probs
        d = round(LEAD + dur + TAIL, 3)
        out[sid] = {"audio": f"audio/voice/{sid}.wav", "audio_s": round(dur, 3), "start": round(t, 3), "dur": d,
                    "subs": [{"t": round(LEAD + a, 3), "d": round(b - a, 3), "text": txt}
                             for (a, b), txt in zip(spans, lines)]}
        print(f"{sid:16s} {dur:6.2f}s  " + "  ".join(f"{a:5.2f}-{b:5.2f}" for a, b in spans))
        t += d
    out["_total"] = round(t, 3)
    print("total", out["_total"])
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    (ROOT / "timing.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


main()
