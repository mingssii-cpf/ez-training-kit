# eplib API (scripts/eplib.py)

`init(ROOT, kick, end_hold=2.5, bgm_vol=0.12, capture=(1490,740))` — load timing.json; `capture` = raw shot size.
Time: `L(sid,i)` line start · `S(sid)` scene start · `D(sid)` scene duration.

| Need | Call |
|---|---|
| Pop in (with pop SFX) | `pop(sel, at, rot=0, d=0.45, sound=True)` |
| Rise / drop photo | `rise(sel, at)` · `drop(sel, at, rot)` |
| Draw SVG ring/check | `draw(sel, at, d=0.6)` (`.ring` / `.ck` auto-dashed) |
| Marker sweep under a headline | `sweep("#..-hl", at)` (`<span class="hl">` inside `.h1`) |
| List items one by one | `stagger_in("#id li", at, step)` |
| Typewriter (Thai-safe) | `typed([(text, mark_id|None)…], cls)` + `type_on(".cls", n_clusters, at, dur, vol)`; `clusters(text)` |
| Highlight a typed heading | `mark_on("#mark_id", at)` |
| Real screen | `photo(pid, shot, (x0,y0,x1,y1), width, x, y, rot)` → `(html, m)` |
| Annotate the screen | `add_scrib(ph,[ellipse(cls,cx,cy,rx,ry)])` · `add_spot(ph,id,cx,cy,w,h)` + `spot_on(sel,at)` · `add_cursor(ph,id,cx,cy)` + `cursor_click(id,at,dx,dy)` |
| Camera punch-in | `punch(sel, at, cx+12, cy+12, scale=1.18)` (≤1.25 keeps the notes visible) |
| Notes | `sticky(id, label, body_html, x, y, w, rot, cls="" \| small \| chipnote \| pink)` · `CHECK` svg |
| Count up | `counter([("id",8),("id2",1)], at)` |
| Confetti | `confetti_html(wrap_id)` in the scene + `confetti_burst(at)` |
| Sound accent | `sfx(name, at, vol)`: pop, click, click-soft, typing, whoosh-short, ping, chime, sparkle, notification |
| Raw GSAP | `ft(sel, from, to, at)` · `to(sel, props, at)` · `raw("  tl...;")` |
| Write page | `write_page(SC)` — page-turn transitions + whoosh, VO, captions, SFX, bed, chrome (kick + logo + progress) |

Layout safe zone: captions sit at bottom 56 px; keep content above y≈900. EZ images ≈ 300–600 px wide.
CSS building blocks (assets/style.css): `.h1 .xl .h2 .eyebrow .sub .bubble(.big) .chip .clock .mails .steps .next .note .ez .spark`.
