# Workflow details (proven in S1E1, 2026-10-11/12)

## voice
Chrome tab (Claude in Chrome), owner's Google account is already signed in at aistudio.google.com.
1. `navigate https://aistudio.google.com/generate-speech` → `find "Create new dialog"` → click.
2. Voice: click `Speaker 1 - …` → in the panel click the **"Search 2,000+ voices" box by coordinate** (the ref
   sometimes doesn't take typing) → type `Fenrir` → click the Fenrir row → close the panel (`find "Close panel"`).
3. Style: click `Style` → click the "Describe the voice style" box → type the `style_prompt` → Return → Escape.
   The chip then reads "Friendly, appro…".
4. Per scene, **one batch**: click the text block → `ctrl+a` → type the narration → click Run (bottom right) →
   wait 10+10+8 s → click Download (`find "Download audio button"` once; the ref stays the same) → wait 4 s.
   Then `python scripts/grab_tts.py <ep> <scene-id>`. The Download ref changes per take: click it by coordinate
   (bottom player, left of the thumbs) after the first `find`. It warns if the take length repeats (stale download).
5. Pace ≈ 12 Thai chars/s. A ~110-char scene takes about 9 s. A paid key is linked: regenerate only scenes that changed.

## capture
- Outlook: `https://outlook.cloud.microsoft/mail/` → Copilot pane: `find "แชทกับ Copilot"` (ribbon right; the app-bar icon
  doesn't open the pane). Settings already done: Copilot theme Light. **Chrome zoom 175%** (the owner presses Ctrl + once).
- Prompt box: click the placeholder text first (clicking the box edge doesn't focus it), then type. Screenshot **before**
  sending (the prompt shot), then send → wait 30–40 s → screenshot the top of the answer + the source chips → scroll the pane
  (scroll inside the pane at x≈1040) → further shots. Use `save_to_disk:true` for shots that go into the video.
- If the pane freezes while typing, the previous answer is still streaming: wait 5 s and retype.
- Run "วันนี้" prompts on a weekday after 17:00 so the screen matches the narration.
- Raw files land in `C:/Users/User/.claude/projects/D--ai-clip/<session>/tool-results/*<id>*.jpg`; reference them
  from `redact.json` by the id suffix. Don't copy raw files into the project.
- The Copilot file preview (xlsx/pptx) can hang the tab: navigate to a fresh chat URL or open a new tab.
- Zoom without the owner (S1E2): `javascript_tool` → `document.documentElement.style.zoom='1.75'` (lost on reload). Wide
  answer tables: set `'1.3'` for those shots. Save shots with `screenshot save_to_disk` at scale 1 (scaled shots save small).
- Keep the MCP Chrome window visible: when minimised, tabs report `hidden` and screenshots/JS time out. Fix: close all
  group tabs → `tabs_context_mcp createIfEmpty` opens a fresh, visible window. Use one tab and navigate it (background
  tabs freeze too).
- Never click inside the answer area to focus: table cells/links open files. Click the composer placeholder only.

## redact presets (Outlook at 1490×740 capture, 100% zoom; re-measure at 175%)
- 175% (1568×757): inbox list `[383,260,680,761]` · avatar `[1500,8,1562,64]` · account line `[85,440,365,482]`
- 130% (1568×761): inbox `[285,190,636,761]` · avatar `[1518,4,1566,50]` · account `[62,322,282,362]` (see s1e2 redact.json)
- inbox list with the pane open: `[50,180,585,740]` · without the pane: `[263,180,600,740]` · avatar: `[1440,0,1490,48]`
- Also blur: colleague names in answers, file names, sensitive HR topics, and the owner's full name on file cards.

## build patterns (see the reference episode tools/build.py)
- Real-screen scene: `ph, m = photo(pid, shot, crop, width, x, y, rot)` → focus points via `m(px,py)` (capture px) →
  `add_scrib(ellipse)`, `add_spot`, `add_cursor` → `drop`, then `cursor_click` / `spot_on` + `punch` / `draw`, keyed to `L(s,i)`.
- Prompt scene: `typed(SEG)` with `.mk` ids → `type_on(".ty", n, at, dur)` → `mark_on` per heading after typing ends.
- Ids must be unique across the page (a scene id and an element id clashed once: `s2-ez`).
- The sticky class `chipnote` is a white card. Don't name classes `tag`, `sub` or `clip` (they collide with chrome/caption CSS).
- Avoid rotated boxes sitting tight together: rotated bounding boxes trip `content_overlap`. Give a label 20 px margin.

## QA expectations
`check` passes (warnings about sub-compositions/track density are expected). The motion audit flags "cadence" and "spikes"
on mostly-still explainers; confirm by reading consecutive frames, not by changing the motion. `qa.py`: about -16 LUFS,
voice window about -18 dB, end hold about -44 dB with the bed.
