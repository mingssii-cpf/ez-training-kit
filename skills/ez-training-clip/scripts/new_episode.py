"""Scaffold a new episode folder from the skill assets (fonts, EZ, logo, SFX, style, HyperFrames config).

Run: python new_episode.py <series-dir> <slug>  e.g.  python new_episode.py D:/.../copilot-hr-series s1e2-follow-up
Creates <series>/<slug>/ with: script.json (template), tools/build.py (template), tools/style.css, fonts/, public/,
assets/sfx/, assets/bgm/ (fill with fit_bgm.py after align), hyperframes.json,
package.json, meta.json, redact.json (template). Refuses to overwrite an existing folder.
"""
import json, pathlib, shutil, sys

SKILL = pathlib.Path(__file__).resolve().parent.parent
series, slug = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2]
ep = series / slug
if ep.exists():
    sys.exit(f"exists: {ep}")
A = SKILL / "assets"
shutil.copytree(A / "fonts", ep / "fonts")
shutil.copytree(A / "public", ep / "public")
shutil.copytree(A / "sfx", ep / "assets" / "sfx")
(ep / "tools").mkdir()
(ep / "audio" / "gemini").mkdir(parents=True)
(ep / "assets" / "bgm").mkdir(parents=True)
shutil.copy(A / "style.css", ep / "tools" / "style.css")
shutil.copy(A / "hyperframes.json", ep / "hyperframes.json")
(ep / "package.json").write_text(json.dumps({"name": slug, "private": True, "type": "module", "scripts": {
    "check": "npx --yes hyperframes@0.8.143 check", "render": "npx --yes hyperframes@0.8.143 render"}}, indent=1), encoding="utf-8")
(ep / "meta.json").write_text(json.dumps({"id": slug, "name": slug}), encoding="utf-8")
shutil.copy(SKILL / "assets" / "templates" / "script.json", ep / "script.json")
shutil.copy(SKILL / "assets" / "templates" / "redact.json", ep / "redact.json")
tpl = (SKILL / "assets" / "templates" / "build.py").read_text(encoding="utf-8")
(ep / "tools" / "build.py").write_text(tpl.replace("__SKILL_SCRIPTS__", str(SKILL / "scripts").replace("\\", "/")), encoding="utf-8")
print("scaffolded", ep)
