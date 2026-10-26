"""eplib — shared builder for EZ training-clip episodes (style C "Explainer Notebook", HyperFrames).

An episode's tools/build.py does:
    import sys; sys.path.insert(0, r"<skill>/scripts"); from eplib import *
    init(ROOT, kick="หนึ่งวันกับ EZ · <ตอน>")
    SC = {}
    s = "s1-hook"; SC[s] = "...html..."; pop("#id", L(s, 0)); ...
    write_page(SC)
Every cue is keyed to caption lines: L(sid, i) = absolute start of line i of scene sid (from timing.json),
S(sid) = scene start, D(sid) = scene duration. Re-voicing re-times picture and sound.
"""
import html, json, pathlib

SW, SH = 1490, 740            # default capture size (override in init if captures differ)
XF = 0.5                      # page-turn overlap between scenes
SFX_LEN = {"sparkle": 1.8, "typing": 1.5, "whoosh-short": 0.57, "pop": 0.72, "click": 0.37, "click-soft": 0.37,
           "chime": 2.5, "ping": 1.32, "notification": 2.46}
THAI_MARKS = set("ำัิีึืฺุู็่้๊๋์ํ๎")
CHECK = '<svg class="ckv" viewBox="0 0 40 32" width="40" height="32"><path class="ck" d="M4 17 L15 27 L36 5"/></svg>'


class _E:
    root = None; T = None; IDS = None; A = None; SFX = None
    end_hold = 2.5; total = 0.0; kick = ""; bgm = None; bgm_vol = 0.12


E = _E()


def init(root, kick, end_hold=2.5, bgm_vol=0.12, capture=(1490, 740)):
    global SW, SH
    SW, SH = capture
    E.root = pathlib.Path(root)
    E.T = json.loads((E.root / "timing.json").read_text(encoding="utf-8"))
    E.IDS = [k for k in E.T if not k.startswith("_")]
    E.A, E.SFX = [], []
    E.end_hold = end_hold
    E.total = round(E.T["_total"] + end_hold, 3)
    E.kick = kick
    bdir = E.root / "assets" / "bgm"
    E.bgm = next((p for p in sorted(bdir.glob("track.*"))), None) if bdir.exists() else None
    E.bgm_vol = bgm_vol


def L(sid, i):
    return E.T[sid]["start"] + E.T[sid]["subs"][i]["t"]


def S(sid):
    return E.T[sid]["start"]


def D(sid):
    return E.T[sid]["dur"]


# ---------- timeline primitives ----------
def sfx(name, at, vol=0.3):
    E.SFX.append((name, round(at, 3), vol))


def ft(sel, frm, to_, at):
    E.A.append(f'  tl.fromTo({json.dumps(sel)}, {frm}, {to_}, {at:.3f});')


def to(sel, props, at):
    E.A.append(f'  tl.to({json.dumps(sel)}, {props}, {at:.3f});')


def raw(js):
    """Append a raw timeline line (stagger tweens, counters)."""
    E.A.append(js)


def pop(sel, at, rot=0, d=0.45, sound=True):
    ft(sel, f'{{opacity:0, scale:0.6, rotation:{rot - 6}}}', f'{{opacity:1, scale:1, rotation:{rot}, duration:{d}, ease:"back.out(2.2)"}}', at)
    if sound:
        sfx("pop", at, 0.22)


def rise(sel, at, d=0.5):
    ft(sel, '{opacity:0, y:30}', f'{{opacity:1, y:0, duration:{d}, ease:"power3.out"}}', at)


def drop(sel, at, rot=-1.2):
    ft(sel, '{opacity:0, y:-140, rotation:-7}', f'{{opacity:1, y:0, rotation:{rot}, duration:0.7, ease:"back.out(1.4)"}}', at)


def draw(sel, at, d=0.6):
    to(sel, f'{{strokeDashoffset:0, duration:{d}, ease:"power2.inOut"}}', at)


def sweep(sel, at):
    ft(sel, '{scaleX:0}', '{scaleX:1, duration:0.5, ease:"power2.out"}', at)


def stagger_in(sel, at, step=0.25, frm="{opacity:0, x:-20}", d=0.3):
    E.A.append(f'  tl.fromTo("{sel}", {frm}, {{opacity:1, x:0, duration:{d}, stagger:{step}, ease:"power2.out"}}, {at:.3f});')


# ---------- Thai-safe typewriter ----------
def clusters(text):
    """Typing units: a base character plus its combining marks (sara am stays with its consonant)."""
    out = []
    for ch in text:
        if out and ch in THAI_MARKS:
            out[-1] += ch
        else:
            out.append(ch)
    return out


def typed(segments, cls="ty"):
    """segments: [(text, mark_id or None)] -> html, one span per cluster (class cls); mark_id wraps a .mk highlight."""
    parts = []
    for text, mid in segments:
        inner = "".join(f'<span class="{cls}">{html.escape(c)}</span>' for c in clusters(text))
        parts.append(f'<b class="mk" id="{mid}">{inner}</b>' if mid else inner)
    return "".join(parts)


def type_on(sel, n_clusters, at, dur, sound=True, vol=0.22):
    """Reveal the typed spans of `sel` over `dur` seconds; typing SFX every 1.5 s."""
    E.A.append(f'  tl.fromTo("{sel}", {{opacity:0}}, {{opacity:1, duration:0.01, stagger:{dur / n_clusters:.4f}, ease:"none"}}, {at:.3f});')
    if sound:
        t = 0.0
        while t < dur - 0.3:
            sfx("typing", at + t, vol)
            t += 1.5


def mark_on(sel, at):
    ft(sel, '{backgroundSize:"0% 100%"}', '{backgroundSize:"100% 100%", duration:0.4, ease:"power2.out"}', at)


# ---------- taped photos of real captures ----------
def photo(pid, img, crop, width, x, y, rot=-1.2):
    """Taped photo of a crop (x0,y0,x1,y1 in capture px). Returns (html, mapper(px,py)->frame-local coords)."""
    x0, y0, x1, y1 = crop
    k = width / (x1 - x0)
    h = (y1 - y0) * k
    inner = (f'<img src="assets/shots/{img}.jpg" alt="" style="width:{SW * k:.1f}px;height:{SH * k:.1f}px;'
             f'left:{-x0 * k:.1f}px;top:{-y0 * k:.1f}px">')
    html_ = (f'<div class="photo" id="{pid}" style="left:{x}px;top:{y}px;width:{width}px;height:{h:.1f}px;--rot:{rot}deg">'
             f'<div class="tape t1"></div><div class="tape t2"></div><div class="clipbox">{inner}<!--spot--></div>'
             f'<svg class="scrib" viewBox="0 0 {width} {h:.1f}" width="{width}" height="{h:.1f}"></svg><!--extra--></div>')
    return html_, (lambda px, py: ((px - x0) * k, (py - y0) * k))


def ellipse(cls, cx, cy, rx, ry):
    return f'<ellipse class="ring {cls}" cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry}"/>'


def add_scrib(photo_html, shapes):
    return photo_html.replace("</svg><!--extra-->", "".join(shapes) + "</svg><!--extra-->")


def add_spot(photo_html, sid, cx, cy, w, h):
    return photo_html.replace("<!--spot-->", f'<div class="spot" id="{sid}" style="left:{cx - w / 2:.1f}px;top:{cy - h / 2:.1f}px;width:{w}px;height:{h}px"></div>')


def add_cursor(photo_html, cid, cx, cy):
    # +12: the scribble/cursor layer sits outside the 12px photo border
    return photo_html.replace("<!--extra-->", f'<div class="cursor" id="{cid}" style="left:{cx + 12:.1f}px;top:{cy + 12:.1f}px">'
                              f'<svg viewBox="0 0 28 36" width="34" height="44"><path d="M2 2 L2 30 L10 23 L15 34 L20 32 L15 21 L26 21 Z"/></svg>'
                              f'<i class="ripple"></i></div><!--extra-->')


def cursor_click(cid, at, dx=240, dy=150):
    ft(f"#{cid}", f'{{opacity:0, x:{dx}, y:{dy}}}', '{opacity:1, x:0, y:0, duration:0.7, ease:"power2.inOut"}', at)
    ft(f"#{cid} .ripple", '{opacity:0.9, scale:0}', '{opacity:0, scale:1.8, duration:0.5, ease:"power2.out"}', at + 0.72)
    sfx("click", at + 0.72, 0.45)


def punch(sel, at, cx, cy, scale=1.18, d=0.9):
    ft(sel, '{scale:1}', f'{{scale:{scale}, transformOrigin:"{cx:.0f}px {cy:.0f}px", duration:{d}, ease:"power2.inOut", immediateRender:false}}', at)


def spot_on(sel, at):
    ft(sel, '{opacity:0}', '{opacity:1, duration:0.4, ease:"power1.out"}', at)


# ---------- notebook pieces ----------
def sticky(sid, label, body, x, y, w, rot=2, cls=""):
    """cls: "" (yellow) | small | chipnote (white card, hard shadow) | pink."""
    return (f'<div class="sticky {cls}" id="{sid}" style="left:{x}px;top:{y}px;width:{w}px;--rot:{rot}deg">'
            f'<div class="lab">{label}</div>{body}</div>')


def counter(ids_targets, at, d=0.8):
    """Count numbers up: ids_targets = [("elem-id", 8), ...] (elements start at 0)."""
    keys = "abcdefgh"[:len(ids_targets)]
    init_ = ", ".join(f"{k}:0" for k in keys)
    tgt = ", ".join(f"{k}:{v}" for k, (_, v) in zip(keys, ids_targets))
    upd = " ".join(f'document.getElementById("{i}").textContent = Math.round(c.{k});' for k, (i, _) in zip(keys, ids_targets))
    E.A.append(f'  {{ const c = {{{init_}}}; tl.to(c, {{{tgt}, duration:{d}, ease:"power1.out", onUpdate:() => {{ {upd} }}}}, {at:.3f}); }}')


def _confetti_pieces(n, seed):
    conf = []
    for i in range(n):
        seed = (seed * 1103515245 + 12345) % 2147483648
        dx = (seed % 900) - 450
        seed = (seed * 1103515245 + 12345) % 2147483648
        up = 180 + seed % 260
        seed = (seed * 1103515245 + 12345) % 2147483648
        conf.append((dx, up, 300 + seed % 400, (seed // 7) % 3, (seed % 720) - 360))
    return conf


def confetti_html(wrap_id, prefix="cf", n=30, seed=7, x=None, y=None):
    """Deterministic confetti pieces (default origin 1480,380 via CSS .confetti). Pair with confetti_burst()."""
    style = f' style="left:{x}px;top:{y}px"' if x is not None else ""
    return (f'<div class="confetti" id="{wrap_id}"{style}>'
            + "".join(f'<i class="cf c{c}" id="{prefix}{i}"></i>' for i, (_, _, _, c, _) in enumerate(_confetti_pieces(n, seed))) + "</div>")


def confetti_burst(at, prefix="cf", n=30, seed=7, sound=True):
    for i, (dx, up, fall, _, rot) in enumerate(_confetti_pieces(n, seed)):
        to(f"#{prefix}{i}", f'{{keyframes:[{{opacity:1, duration:0.01}}, {{x:{dx * 0.6:.0f}, y:{-up}, rotation:{rot / 2:.0f}, duration:0.45, ease:"power2.out"}}, '
           f'{{x:{dx}, y:{fall}, rotation:{rot}, opacity:0, duration:1.2, ease:"power2.in"}}]}}', at + (i % 5) * 0.02)
    if sound:
        sfx("chime", at, 0.22)


# ---------- assemble ----------
def write_page(SC, css_path=None):
    T, IDS = E.T, E.IDS
    parts, subs, audio = [], [], []
    for i, sid in enumerate(IDS):
        st, du = T[sid]["start"], T[sid]["dur"]
        last = i == len(IDS) - 1
        d = du + (E.end_hold if last else XF)
        parts.append(f'  <section id="{sid}" class="clip scene" data-start="{st:.3f}" data-duration="{d:.3f}" data-track-index="1">{SC[sid]}</section>')
        if i:  # page turn: outgoing slides left, incoming slides in from the right
            prev = IDS[i - 1]
            ft(f"#{prev}", '{opacity:1, x:0}', f'{{opacity:0, x:-160, duration:{XF}, ease:"power2.in", immediateRender:false}}', st)
            ft(f"#{sid}", '{opacity:0, x:160}', f'{{opacity:1, x:0, duration:{XF}, ease:"power3.out"}}', st + 0.05)
            sfx("whoosh-short", st, 0.18)
        audio.append(f'<audio id="vo-{sid}" src="{T[sid]["audio"]}" data-start="{st + 0.35:.3f}" data-duration="{T[sid]["audio_s"]:.3f}" data-track-index="5" data-volume="1"></audio>')
        for k, sb in enumerate(T[sid]["subs"]):
            subs.append(f'<div id="sub-{sid}-{k}" class="clip sub" data-start="{st + sb["t"]:.3f}" data-duration="{sb["d"] + 0.15:.3f}" data-track-index="3"><span>{html.escape(sb["text"])}</span></div>')
    for n, (name, at, vol) in enumerate(sorted(E.SFX, key=lambda x: x[1])):
        dd = min(SFX_LEN[name], E.total - at)
        audio.append(f'<audio id="fx{n}" src="assets/sfx/{name}.mp3" data-start="{at:.3f}" data-duration="{dd:.3f}" data-track-index="{6 + n % 4}" data-volume="{vol}"></audio>')
    if E.bgm:
        audio.append(f'<audio id="bgm" src="assets/bgm/{E.bgm.name}" data-start="0" data-duration="{E.total}" data-track-index="10" data-volume="{E.bgm_vol}"></audio>')
    css = pathlib.Path(css_path or (E.root / "tools" / "style.css")).read_text(encoding="utf-8")
    TOTAL = E.total
    page = f"""<!doctype html>
<html lang="th">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
{css}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
  <div id="ground" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="0"></div>
{chr(10).join(parts)}
  <div id="chrome" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="2">
    <div class="kick">{E.kick}</div>
    <img class="logo" src="public/cpf-logo.svg" alt="">
    <div class="progress"><div id="bar"></div></div>
  </div>
  {''.join(subs)}
  {''.join(audio)}
</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  document.querySelectorAll(".ring, .ck").forEach(p => {{ const Ln = p.getTotalLength(); p.style.strokeDasharray = Ln; p.style.strokeDashoffset = Ln; }});
{chr(10).join(E.A)}
  tl.fromTo("#bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {TOTAL}, ease: "none" }}, 0);
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
    (E.root / "index.html").write_text(page, encoding="utf-8")
    print("wrote index.html", TOTAL, "s,", len(E.A), "tweens,", len(E.SFX), "sfx, bgm:", E.bgm.name if E.bgm else "none")
