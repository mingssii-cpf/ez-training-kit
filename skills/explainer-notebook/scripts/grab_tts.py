"""Optional AI Studio helper: move "Generated Audio*.wav" to <episode>/audio/voice/<scene-id>.wav.

Run right after clicking Download for a scene:  python grab_tts.py <episode-dir> <scene-id>
Prints duration; refuses if the newest file is older than 120 s (stale/no download) or the duration repeats
the previous take (AI Studio re-downloaded the old audio).
"""
import pathlib, shutil, subprocess, sys, time

ep, sid = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2]
dl = pathlib.Path.home() / "Downloads"
files = sorted(dl.glob("Generated Audio*.wav"), key=lambda p: p.stat().st_mtime)
if not files or time.time() - files[-1].stat().st_mtime > 120:
    sys.exit("no fresh AI Studio download")
dst = ep / "audio" / "voice" / f"{sid}.wav"
dst.parent.mkdir(parents=True, exist_ok=True)
shutil.move(str(files[-1]), dst)  # works across drives (Downloads on C:, project on D:)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(dst)],
                           capture_output=True, text=True).stdout)
others = [p for p in dst.parent.glob("*.wav") if p != dst]
same = [p.name for p in others if abs(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout or 0) - dur) < 0.005]
print(f"{sid} {dur:.2f}s" + (f"  WARNING same length as {same} — check it is a new take" if same else ""))
