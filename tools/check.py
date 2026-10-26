"""Offline checks for the general notebook kit: python tools/check.py."""
import ast
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import wave

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/explainer-notebook"
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")


def run(*args, ok=True):
    result = subprocess.run([sys.executable, *map(str, args)], env=ENV,
                            capture_output=True, text=True, encoding="utf-8")
    assert (result.returncode == 0) == ok, result.stdout + result.stderr
    return result


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.assets = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if "src" in attrs:
            self.assets.append(attrs["src"])


def check_pages(ep):
    for name in ("index.html", "preview.html"):
        text = (ep / name).read_text(encoding="utf-8")
        page = Page()
        page.feed(text)
        assert len(page.ids) == len(set(page.ids)), f"Duplicate IDs in {name}"
        assets = page.assets + re.findall(r'url\("([^"]+)"\)', text)
        for asset in assets:
            if not asset.startswith(("https://", "http://")):
                assert (ep / html.unescape(asset)).is_file(), f"Missing asset: {asset}"
    return (ep / "index.html").read_text(encoding="utf-8")


for path in SKILL.rglob("*.py"):
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
for path in SKILL.rglob("*.json"):
    json.loads(path.read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "SOURCE-MANIFEST.json").read_text(encoding="utf-8"))
for path, checksum in manifest["sha256"].items():
    if path.startswith("assets/fonts/") or (path.startswith("assets/sfx/") and path.endswith(".mp3")):
        assert hashlib.sha256((SKILL / path).read_bytes()).hexdigest() == checksum

with tempfile.TemporaryDirectory(prefix="notebook-check-") as tmp:
    temp = Path(tmp)
    series = temp / "episodes"
    create = SKILL / "scripts/new_episode.py"
    run(create, series, "plain", "--preview")
    plain = series / "plain"
    page = check_pages(plain)
    assert not list((plain / "public").iterdir()), "Default output contains branding assets"
    assert not any(text in page for text in ("EZ", "CPF", "Copilot", "cpf-logo", "ez-4"))
    assert "ONE IDEA AT A TIME" in page
    assert 'data-width="1920"' in page and 'data-height="1080"' in page
    before = (plain / "script.json").read_bytes()
    run(create, series, "plain", ok=False)
    assert before == (plain / "script.json").read_bytes()

    image = temp / "own-character.svg"
    image.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="10" y="10" width="80" height="80" rx="20" fill="#0f8f83"/></svg>', encoding="utf-8")
    for name, flags, logo, mascot in (
        ("logo-only", ["--logo", image], True, False),
        ("mascot-only", ["--mascot", image], False, True),
        ("custom", ["--brand", '<b>Our team</b> & Co', "--title", 'A <B> & C', "--logo", image, "--mascot", image], True, True),
        ("ez", ["--preset", "ez"], True, True),
        ("override", ["--preset", "ez", "--logo", image, "--mascot", image], True, True),
        ("long-title", ["--title", "W" * 60], False, False),
    ):
        run(create, series, name, *flags, "--preview")
        ep = series / name
        text = check_pages(ep)
        brand = json.loads((ep / "brand.json").read_text(encoding="utf-8"))
        assert bool(brand["logo"]) == logo and bool(brand["mascot"]) == mascot
        assert ('class="logo"' in text) == logo
        assert ('class="mascot"' in text) == mascot
        if name == "custom":
            assert "<b>Our team</b>" not in text and "&lt;b&gt;Our team&lt;/b&gt; &amp; Co" in text
            assert "A &lt;B&gt; &amp; C" in text
        if name == "override":
            assert "public/logo.svg" in text and "public/mascot.svg" in text and "cpf-logo.svg" not in text
        if name in ("custom", "mascot-only"):
            assert not any(path.name.startswith(("ez-", "cpf-")) for path in (ep / "public").iterdir())

    for slug in ("../escape", "/absolute", "con", "nul", "a/b", "."):
        run(create, temp / "invalid", slug, ok=False)
    run(create, temp / "invalid", "bad-image", "--mascot", temp / "missing.png", ok=False)
    run(create, temp / "invalid", "long", "--title", "X" * 61, ok=False)
    assert not (temp / "invalid").exists(), "Invalid input created output directories"

    moved = temp / "moved episode"
    shutil.move(str(series / "custom"), moved)
    run(moved / "tools/build.py")
    check_pages(moved)
    brand = json.loads((moved / "brand.json").read_text(encoding="utf-8"))
    brand["logo"] = brand["mascot"] = None
    (moved / "brand.json").write_text(json.dumps(brand), encoding="utf-8")
    run(moved / "tools/build.py")
    text = check_pages(moved)
    assert 'class="logo"' not in text and 'class="mascot"' not in text

    # Exercise the voiced HTML contract with synthetic WAVs, without requiring a TTS service.
    script = json.loads((plain / "script.json").read_text(encoding="utf-8"))
    timing = {}
    for i, scene in enumerate(script["scenes"]):
        sid = scene["id"]
        audio = f"audio/voice/{sid}.wav"
        with wave.open(str(plain / audio), "wb") as wav:
            wav.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
            wav.writeframes(b"\0\0" * 16000 * 4)
        timing[sid] = dict(audio=audio, audio_s=4, start=i * 6, dur=6,
                           subs=[dict(t=.35 + n, d=.8, text=line)
                                 for n, line in enumerate(scene["lines"])])
    timing["_total"] = len(script["scenes"]) * 6
    (plain / "timing.json").write_text(json.dumps(timing), encoding="utf-8")
    run(plain / "tools/build.py")
    assert 'id="vo-s1-hook"' in check_pages(plain)

print("PASS: generic default; independent logo/mascot; custom brand; EZ opt-in/override; safe input; no overwrite; portable build; voiced HTML; unique IDs; asset integrity")
print("Scope: offline synthetic checks, not real TTS, alignment, rendered-video or visual approval")
