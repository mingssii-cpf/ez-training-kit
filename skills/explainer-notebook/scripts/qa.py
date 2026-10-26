"""Compact QA for a rendered episode — prints ~10 lines, writes qa/frames.jpg (one frame per scene).

Run: python qa.py <episode-dir> <render.mp4>
Checks: streams/duration vs timing, integrated loudness, voice level vs a voice window, music bed present
(level in the end hold), one mid-scene frame per scene in a contact sheet for a single visual read.
"""
import json, pathlib, re, subprocess, sys

ep, mp4 = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
T = json.loads((ep / "timing.json").read_text(encoding="utf-8"))
ids = [k for k in T if not k.startswith("_")]


def ff(args):
    return subprocess.run(["ffmpeg", "-hide_banner", *args], capture_output=True, text=True).stderr


def mean(ss, t):
    m = re.search(r"mean_volume: (-?[\d.]+)", ff(["-ss", str(ss), "-t", str(t), "-i", str(mp4), "-af", "volumedetect", "-vn", "-f", "null", "-"]))
    return float(m.group(1)) if m else None


probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration", "-of", "json", str(mp4)],
                       capture_output=True, text=True).stdout
pj = json.loads(probe)
dur = float(pj["format"]["duration"])
kinds = [s["codec_type"] for s in pj["streams"]]
I = re.findall(r"I:\s+(-?[\d.]+) LUFS", ff(["-i", str(mp4), "-af", "ebur128", "-f", "null", "-"]))
s1 = ids[min(2, len(ids) - 1)]
print(f"duration {dur:.2f}s (timing {T['_total']:.2f}s + end hold) | streams {kinds}")
print(f"integrated loudness {I[-1] if I else '?'} LUFS (internal target about -16 to -18)")
print(f"voice window ({s1}) mean {mean(T[s1]['start'] + 1, 5)} dB | end-hold mean {mean(dur - 2.0, 1.6)} dB (music bed ≈ -40..-46 if present)")
out = ep / "qa"
out.mkdir(exist_ok=True)
sel = "+".join(f"eq(n\\,{int((T[k]['start'] + T[k]['dur'] * 0.75) * 30)})" for k in ids)
cols = 3
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf", f"select='{sel}',scale=640:-1,tile={cols}x{(len(ids) + cols - 1) // cols}",
                "-frames:v", "1", str(out / "frames.jpg")], check=True)
print("frames:", out / "frames.jpg", "(read once at scale; check text, redaction, layout)")
