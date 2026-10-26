"""Raw captures -> <episode>/assets/shots/<name>.jpg with private regions blurred.

Config <episode>/redact.json (boxes in capture px, x0,y0,x1,y1):
{"raw_dir": "C:/.../tool-results", "presets": {"inbox": [50,180,585,740], "avatar": [1440,0,1490,48]},
 "shots": {"c01-pane": {"src": "*1791731516491*", "boxes": ["inbox", "avatar", [640,585,1440,625]]}}}
Raw files never enter the episode folder. Writes _contact.jpg for one-look review.
Run: python redact.py <episode-dir>
"""
import json, pathlib, sys
from PIL import Image, ImageFilter

ep = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
cfg = json.loads((ep / "redact.json").read_text(encoding="utf-8"))
raw = pathlib.Path(cfg["raw_dir"])
presets = cfg.get("presets", {})
out = ep / "assets" / "shots"
out.mkdir(parents=True, exist_ok=True)
thumbs = []
for name, spec in cfg["shots"].items():
    src = next(raw.glob(spec["src"]))
    im = Image.open(src).convert("RGB")
    for b in spec.get("boxes", []):
        box = tuple(presets[b] if isinstance(b, str) else b)
        im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(14)), box)
    im.save(out / f"{name}.jpg", quality=92)
    thumbs.append(im.resize((im.width // 2, im.height // 2)))
    print("wrote", name, im.size)
if thumbs:
    w, h = thumbs[0].size
    sheet = Image.new("RGB", (w * 2, h * ((len(thumbs) + 1) // 2)), "white")
    for i, t in enumerate(thumbs):
        sheet.paste(t.resize((w, h)), ((i % 2) * w, (i // 2) * h))
    sheet.save(out / "_contact.jpg", quality=85)
    print("contact sheet:", out / "_contact.jpg")
