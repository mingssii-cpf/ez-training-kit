"""Run the kit's offline packaging smoke check: python tools/check.py."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import wave

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "ez-training-clip"
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")


def run(*args, ok=True):
    result = subprocess.run([sys.executable, *map(str, args)], env=ENV,
                            capture_output=True, text=True, encoding="utf-8")
    assert (result.returncode == 0) == ok, result.stdout + result.stderr
    return result


manifest = json.loads((ROOT / "SOURCE-MANIFEST.json").read_text(encoding="utf-8"))
actual = {p.relative_to(SKILL).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in SKILL.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
assert actual == manifest["sha256"], "Skill differs from the frozen source manifest"
for path in ROOT.rglob("*.py"):
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
for path in ROOT.rglob("*.json"):
    json.loads(path.read_text(encoding="utf-8"))

with tempfile.TemporaryDirectory(prefix="ez-kit-check-") as tmp:
    series = Path(tmp) / "series"
    ep = series / "smoke"
    run(SKILL / "scripts/new_episode.py", series, "smoke")
    before = (ep / "script.json").read_bytes()
    refused = run(SKILL / "scripts/new_episode.py", series, "smoke", ok=False)
    assert "exists:" in refused.stderr + refused.stdout
    assert (ep / "script.json").read_bytes() == before
    build = (ep / "tools/build.py").read_text(encoding="utf-8")
    assert "__SKILL_SCRIPTS__" not in build
    assert (SKILL / "scripts").as_posix() in build
    script = json.loads(before)
    timing = {}
    for i, scene in enumerate(script["scenes"]):
        sid = scene["id"]
        audio = f"audio/gemini/{sid}.wav"
        with wave.open(str(ep / audio), "wb") as wav:
            wav.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
            wav.writeframes(b"\0\0" * 16000 * 4)
        timing[sid] = dict(audio=audio, audio_s=4, start=i * 6, dur=6,
                           subs=[dict(t=0.35 + n, d=0.8, text=line)
                                 for n, line in enumerate(scene["lines"])])
    timing["_total"] = len(script["scenes"]) * 6
    (ep / "timing.json").write_text(json.dumps(timing), encoding="utf-8")
    run(ep / "tools/build.py")
    page = (ep / "index.html").read_text(encoding="utf-8")
    assert 'data-width="1920"' in page and 'data-height="1080"' in page
    assert 'window.__timelines["main"]' in page
    for sid in timing:
        if not sid.startswith("_"):
            assert f'id="{sid}"' in page
    for asset in re.findall(r'(?:src="|url\(")([^"\)]+)', page):
        if not asset.startswith(("https://", "http://")):
            assert (ep / asset).is_file(), f"Missing generated asset: {asset}"

print(f"PASS: {len(actual)} source files match; Python/JSON parse; scaffold; overwrite refusal; HTML build; local assets")
print("Scope: offline synthetic packaging check; no TTS, browser capture, HyperFrames render or visual QA")
