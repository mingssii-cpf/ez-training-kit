"""Three editable notebook scenes; brand.json controls optional logo and character."""
import html
import json
from pathlib import Path
from eplib import *

ROOT = Path(__file__).resolve().parent.parent
script = json.loads((ROOT / "script.json").read_text(encoding="utf-8"))
brand = json.loads((ROOT / "brand.json").read_text(encoding="utf-8"))
scenes = {scene["id"]: scene for scene in script["scenes"]}
esc = html.escape
init(ROOT, kick=brand["name"] or "Explainer Notebook")
SC = {}
title_class = " long" if len(script["title"]) > 40 else ""

s = "s1-hook"
SC[s] = f'''
<div class="eyebrow" style="left:150px;top:220px">LEARN · TRY · APPLY</div>
<div class="h1 notebook-title{title_class}" id="hook-title" style="left:150px;top:300px;width:1000px">{esc(script['title'])}</div>
<div class="sticky chipnote" id="hook-note" style="left:150px;top:760px;--rot:-1deg">เปลี่ยนความเข้าใจ ให้เป็นสิ่งที่ลงมือทำได้</div>
'''
if brand.get("mascot"):
    SC[s] += f'<img class="mascot" id="hook-art" src="{esc(brand["mascot"], quote=True)}" alt="Character" style="left:1220px;top:240px;width:500px;height:500px;object-fit:contain">'
else:
    SC[s] += '''<div class="sticky" id="hook-art" style="left:1280px;top:300px;width:430px;--rot:3deg">
<div class="lab">ONE IDEA AT A TIME</div><div style="font-size:120px;font-weight:700;line-height:1.1">01</div>
<div style="margin-top:30px">เริ่มจากเรื่องเดียว<br>ที่อยากทำให้ดีขึ้น</div></div>'''
rise("#hook-title", S(s) + 0.2)
pop("#hook-note", S(s) + 0.8, -1)
pop("#hook-art", S(s) + 0.5, 3 if not brand.get("mascot") else 0)

s = "s2-prompt"
SC[s] = f'''
<div class="eyebrow" style="left:150px;top:180px">GIVE IT A CLEAR START</div>
<div class="h2" id="prompt-title" style="left:150px;top:250px">เริ่มจากคำถามที่ชัด</div>
<div class="sticky" id="prompt-card" style="left:180px;top:390px;width:1010px;--rot:-1deg">
<div class="lab">PROMPT</div><div style="white-space:pre-wrap;font-size:42px">{esc(scenes[s]['prompt'])}</div>
<div class="foot">ปรับข้อความให้เข้ากับงานของคุณ</div></div>
<div class="sticky chipnote" id="prompt-tip" style="left:1320px;top:430px;width:390px;--rot:2deg;white-space:normal">ข้อมูลครบ<br>คำตอบก็ชัดขึ้น</div>
'''
rise("#prompt-title", S(s) + 0.1)
pop("#prompt-card", S(s) + 0.4, -1)
pop("#prompt-tip", S(s) + 1.0, 2)

s = "s3-steps"
SC[s] = '''<div class="eyebrow" style="left:150px;top:200px">YOUR NEXT MOVE</div>
<div class="h2" id="steps-title" style="left:150px;top:280px">ลองทำตาม 3 ขั้นตอน</div>'''
rise("#steps-title", S(s) + 0.1)
for i, label in enumerate(scenes[s]["steps"]):
    SC[s] += f'''<div class="sticky chipnote" id="step-{i}" style="left:{150 + i * 550}px;top:460px;width:470px;min-height:220px;--rot:0deg">
<div class="lab">0{i + 1}</div><div style="font-size:42px;line-height:1.4">{esc(label)}</div></div>'''
    pop(f"#step-{i}", S(s) + 0.4 + i * 0.4, 0)
write_page(SC)
