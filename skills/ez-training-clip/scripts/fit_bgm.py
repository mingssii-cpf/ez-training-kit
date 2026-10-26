"""Fit the series music bed to an episode: <episode>/assets/bgm/track.wav = source trimmed (or crossfade-looped)
to timing total + end hold, loudness-normalised (-20 LUFS), 1.5 s fade-in, 3 s fade-out. eplib plays it at
bgm_vol 0.12 (≈ -26 dB under the voice; accepted in S1E1 v2).

Run after align.py:  python fit_bgm.py <episode-dir> <source-audio> [end_hold=2.5]
"""
import json, pathlib, subprocess, sys

ep, src = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
hold = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
T = json.loads((ep / "timing.json").read_text(encoding="utf-8"))
need = T["_total"] + hold + 0.5
have = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                            capture_output=True, text=True).stdout)
out = ep / "assets" / "bgm" / "track.wav"
out.parent.mkdir(parents=True, exist_ok=True)
post = f"loudnorm=I=-20:TP=-2:LRA=11,afade=t=in:d=1.5,afade=t=out:st={need - 3:.2f}:d=3"
if have >= need:
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-t", f"{need:.2f}", "-af", post, "-ar", "44100", "-ac", "2", str(out)]
else:  # loop with a 4 s crossfade until long enough
    reps = int(need // (have - 4)) + 1
    ins = sum([["-i", str(src)] for _ in range(reps)], [])
    chain, last = [], "[0:a]"
    for i in range(1, reps):
        chain.append(f"{last}[{i}:a]acrossfade=d=4[x{i}]")
        last = f"[x{i}]"
    cmd = ["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(chain) + f";{last}atrim=0:{need:.2f},{post}[o]",
           "-map", "[o]", "-ar", "44100", "-ac", "2", str(out)]
subprocess.run(cmd, check=True)
print(f"bgm fitted: {need:.1f}s from {src.name} ({have:.0f}s) -> {out}")
