"""Create a notebook episode, optionally with custom branding and a silent style preview."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

SKILL = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("series", type=Path)
parser.add_argument("slug", help="Lowercase folder name: letters, digits, hyphens")
parser.add_argument("--title", default="เข้าใจง่าย ลงมือทำได้")
parser.add_argument("--brand", default=None, help="Optional brand or series name")
parser.add_argument("--logo", type=Path, help="Your PNG, JPEG, WebP or SVG logo")
parser.add_argument("--mascot", type=Path, help="Your character image; transparent PNG/WebP works well")
parser.add_argument("--preset", choices=("notebook", "ez"), default="notebook")
parser.add_argument("--preview", action="store_true", help="Build a silent style sample using synthetic timing")
args = parser.parse_args()

if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", args.slug) or re.fullmatch(r"con|prn|aux|nul|com[1-9]|lpt[1-9]", args.slug):
    parser.error("slug must be a safe lowercase folder name, not a path or device name")
if not args.title.strip() or len(args.title) > 60:
    parser.error("title must contain 1–60 characters; use a short title for the sample layout")
if args.brand is not None and len(args.brand) > 60:
    parser.error("brand must be at most 60 characters")

brand = {"name": args.brand if args.brand is not None else ("หนึ่งวันกับ EZ" if args.preset == "ez" else ""),
         "title": args.title, "preset": args.preset, "logo": None, "mascot": None}
images = {}
for key in ("logo", "mascot"):
    source = getattr(args, key)
    if source is not None:
        source = source.resolve()
        if not source.is_file() or source.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp", ".svg"):
            parser.error(f"{key} must be an existing PNG, JPEG, WebP or SVG image")
        images[key] = source

ep = args.series.resolve() / args.slug
if ep.exists():
    parser.exit(1, f"exists: {ep}\n")
# ponytail: fixed notebook components plus optional images; add another preset only for a real recurring brand.
ep.mkdir(parents=True)
assets = SKILL / "assets"
shutil.copytree(assets / "fonts", ep / "fonts")
shutil.copytree(assets / "sfx", ep / "assets/sfx")
for folder in ("tools", "public", "audio/voice", "assets/bgm"):
    (ep / folder).mkdir(parents=True, exist_ok=True)
if args.preset == "ez":
    shutil.copytree(assets / "presets/ez/public", ep / "public", dirs_exist_ok=True)
    brand.update(logo="public/cpf-logo.svg", mascot="public/ez-4.webp")
for key, source in images.items():
    target = ep / "public" / f"{key}{source.suffix.lower()}"
    shutil.copyfile(source, target)
    brand[key] = target.relative_to(ep).as_posix()

for source, target in ((assets / "style.css", "tools/style.css"),
                       (assets / "hyperframes.json", "hyperframes.json"),
                       (assets / "templates/build.py", "tools/build.py"),
                       (SKILL / "scripts/eplib.py", "tools/eplib.py"),
                       (assets / "templates/redact.json", "redact.json")):
    shutil.copyfile(source, ep / target)
script = json.loads((assets / "templates/script.json").read_text(encoding="utf-8"))
script["title"] = args.title
script["scenes"][0]["lines"] = [args.title]
script["scenes"][0]["narration"] = args.title
for name, data in (("brand.json", brand), ("script.json", script),
                   ("meta.json", {"id": args.slug, "name": args.title}),
                   ("package.json", {"name": args.slug, "private": True, "type": "module", "scripts": {
                       "check": "npx --yes hyperframes@0.8.143 check",
                       "render": "npx --yes hyperframes@0.8.143 render"}})):
    (ep / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if args.preview:
    timing = {}
    for i, scene in enumerate(script["scenes"]):
        timing[scene["id"]] = {"start": i * 8, "dur": 8, "subs": []}
    timing.update(_total=len(script["scenes"]) * 8, _preview=True)
    (ep / "timing.json").write_text(json.dumps(timing), encoding="utf-8")
    subprocess.run([sys.executable, str(ep / "tools/build.py")], check=True)
    print("Silent style preview (synthetic timing):", ep / "preview.html")
print("scaffolded", ep)
