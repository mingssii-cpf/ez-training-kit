"""Episode scenes. Mechanics (photo/sticky/pop/typewriter/cursor/spot/sfx/page-turn/assembly) live in eplib.
Run: python <skill>/scripts/align.py . && python tools/build.py && npx --yes hyperframes@0.8.143 check
Copy patterns from the reference episode: copilot-hr-series/s1e1-end-of-day/tools/build.py
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, "__SKILL_SCRIPTS__")
from eplib import *  # noqa: E402,F401,F403

init(ROOT, kick="หนึ่งวันกับ EZ · HH:MM <ชื่อตอน>")
SC = {}

# ---------- s1 hook ----------
s = "s1-hook"
SC[s] = f"""
  <div class="h1" id="s1-h" style="left:150px;top:600px"><span class="hl" id="s1-hl"></span><span class="t">ข้อความ hook</span></div>
"""
rise("#s1-h", L(s, 0))
sweep("#s1-hl", L(s, 0) + 0.5)

# ---------- s2 EZ ----------
s = "s2-ez"
SC[s] = f"""
  <img class="ez" id="s2-ezimg" src="public/ez-4.webp" alt="" style="left:1180px;top:170px;width:600px">
  <div class="bubble" id="s2-bub" style="left:1010px;top:200px">EZ พามารู้จัก Copilot</div>
"""
ft("#s2-ezimg", '{opacity:0, y:220, scale:0.8}', '{opacity:1, y:0, scale:1, duration:0.8, ease:"back.out(1.6)"}', S(s) + 0.1)
sfx("sparkle", S(s) + 0.3, 0.3)
pop("#s2-bub", L(s, 0) + 0.3, 3)

# Every scene id in script.json needs an SC entry. Screens: ph, m = photo(...); add_scrib/add_spot/add_cursor; drop(); cursor_click(); punch().
write_page(SC)
