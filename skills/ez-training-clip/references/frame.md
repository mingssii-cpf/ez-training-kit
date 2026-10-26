---
version: 1.0
name: Explainer Notebook — Copilot HR series
description: >
  Locked by owner 2026-10-09 (style gate, chose C). Warm grid-paper canvas, deep-ink type, one teal accent
  taken from the EZ mascot, marker-yellow for emphasis only. Real screenshots sit as taped photos; prompts sit
  on sticky notes; flows are hand-placed cards with hard offset shadows. Reference build:
  ../style-gate/tools/build.py (theme "c-notebook"), renders in ../style-gate/review/.
unit: 1920x1080 primary
principle: atoms are fixed · composition is free · every claim comes from capability-matrix.md

colors:
  bg: "#fbf7ee"            # paper
  grid: "rgba(31,42,68,0.06)"  # 2px lines, 48px cell
  ink: "#1f2a44"           # headings, borders, wires, card shadows
  muted: "#666c7a"         # sub lines, footnotes
  accent: "#0f8f83"        # EZ teal — focus rings, end node, progress bar, numbered dots
  accent-ink: "#0d7a70"    # eyebrow, labels on paper
  marker: "#ffe066"        # highlighter behind 1 phrase per frame max; tape
  sticky: "#fff1a8"        # prompt cards, decision nodes
  white: "#ffffff"         # photo border, nodes, callouts
  brand-logo-only: "#01a451 / #2c358d / #b1955a"  # CPF logo file only; not UI colours (no official CI guide yet)

typography:
  family: "IBM Plex Sans Thai (400/500/600/700, OFL) · Space Grotesk for Latin labels/numbers"
  h1:      { px: 104, weight: 700, lineHeight: 1.22 }
  h2:      { px: 64,  weight: 700 }
  eyebrow: { px: 30,  weight: 600, color: accent-ink }
  body:    { px: 38,  weight: 500, lineHeight: 1.5 }   # prompt text
  sub:     { px: 32-40, weight: 500, color: muted }
  label:   { px: 22, family: Space Grotesk, weight: 700, tracking: 0.14em }  # PROMPT, STEP
  node:    { px: 30, weight: 600 }

components:
  photo-screenshot: "white 14px border, radius 6, rotate ≈ -1.2deg, 2 tape strips (marker @75%), soft shadow 0 18 30 -14 ink@35%"
  sticky-prompt:    "sticky bg, radius 4, rotate 2deg, label PROMPT + verbatim prompt + foot 'คัดลอกได้จากการ์ดท้ายตอน'"
  step-pill:        "ink bg, paper text, rotate -1.5deg, top-left"
  callout:          "white, 3px ink border, numbered teal dot, rotate -1deg"
  focus:            "hand-drawn teal ellipse (stroke 6) drawn on with dashoffset — never a fake cursor or fake UI"
  flow-node:        "white card, 3px ink border, radius 10, hard shadow 6px 6px 0 ink@90%, alternate ±1deg"
  decision:         "rotated sticky square, ink border"
  end-node:         "teal fill, white text"
  ez:               "public/ez-1..5.webp (alpha). Speech bubble = white pill, 3px ink border. Line 'EZ พามารู้จัก Copilot' once per EP; EZ never sits inside a Copilot screenshot"

motion:
  feel: "playful but quick — back.out(2–2.4) pops ≤0.5s, slight rotation on entry, settle to resting tilt"
  text: "lines pop with -3..2deg rotation; marker sweeps scaleX left→right 0.5s after the line lands"
  screenshot: "drop in from above with rotation (-7→-1.2deg), tapes pop after; slow punch-in ≤1.07 toward the focus area"
  prompt: "sticky slaps in (scale 1.25→1, rot 9→2), text reveals left→right; hold ≥4s readable"
  flow: "nodes pop in reading order, each wire draws (dashoffset 0.4s) after its source node, arrowhead appears at wire end"
  scene-change: "0.3s crossfade overlap"
  bans: "no neon/glow, no fake Copilot UI, on-screen text ≤ short phrases (don't repeat narration verbatim)"

guardrails:
  - "DRAFT tag bottom-right until EZ owner approval (plan Q2)"
  - "Executive tone check: if a frame reads too playful for leadership, reduce rotations first, keep palette"
---
