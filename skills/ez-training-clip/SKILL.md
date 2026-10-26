---
name: ez-training-clip
description: "Produce one episode of the CPF internal training series hosted by EZ (\"หนึ่งวันกับ EZ\" / Copilot Chat training) — Thai motion-graphic clip, style C notebook, real Copilot screen captures (redacted), Gemini TTS voice Fenrir, SFX + music bed, HyperFrames render. Use when asked to make/continue/re-voice/re-render an EZ series episode (ทำตอนต่อไป, ทำคลิป EZ ตอนใหม่, S1E2…). Not for a new visual style or a different brand — use motion-director/hyperframes for that."
metadata:
  version: "1.0.0"
  reference_episode: "training-pilot/videos/copilot-hr-series/s1e1-end-of-day"
---

# EZ training clip

The look, voice, sound and pipeline are **approved and locked** (S1E1 v2, 2026-10-12). Don't re-interview style, voice or music. Only the episode's content needs deciding.

## Fixed decisions
- Style C notebook: `references/frame.md` + `assets/style.css`. EZ poses: `public/ez-1..5.webp`. Logo top-right, no DRAFT tag.
- Voice: Gemini 3.8 Flash TTS · **Fenrir** + the `style_prompt` in `assets/templates/script.json` (EZ guideline 8.3). EZ speaks in first person and ends with ครับ.
- Sound: bundled SFX (`assets/sfx`, Pixabay licence) placed through `eplib.sfx`. Music bed: `<series>/shared/bgm/source-*.mp3`, fitted per episode, `bgm_vol` 0.12.
- 1920×1080, 30 fps, captions burned in and timed from the real voice. Target 1.5–2.5 min.
- Facts: teach only what the series capability matrix marks ✅ for **Copilot Chat (Basic)**.

## Pipeline (one episode)
1. **Scaffold:** `python scripts/new_episode.py <series> <slug>`
2. **Script:** fill `script.json`: 8–10 scenes, hook → EZ → steps (real screen) → check/limits → try-it. Split each scene into `lines` at natural breath pauses. Owner OKs the script before voicing.
3. **Voice:** AI Studio in Chrome, one scene at a time, then `python scripts/grab_tts.py <ep> <scene-id>`. Steps: `references/workflow.md#voice`.
4. **Time:** `python scripts/align.py <ep>`. If a boundary has no pause, merge those two `lines`. Never estimate times.
5. **Capture:** Copilot in Outlook (Chrome, zoom 175%, light theme), `save_to_disk`. Steps: `references/workflow.md#capture`.
6. **Redact:** write `redact.json`, run `python scripts/redact.py <ep>`, read `_contact.jpg` once.
7. **Music:** `python scripts/fit_bgm.py <ep> <series>/shared/bgm/source-*.mp3`
8. **Build:** write scenes in `tools/build.py` using eplib (API: `references/eplib.md`), then `npx --yes hyperframes@0.8.143 check 2>&1 | grep -E "✗|Check"`. Fix every ✗.
9. **Inspect:** `npx --yes hyperframes@0.8.143 snapshot --at <t1,t2,…>` at the effect moments, then read the contact sheet once.
10. **Render:** `npx --yes hyperframes@0.8.143 render --fps 30 --quality standard --workers 2 --output renders/<slug>.mp4` (≈6 min; run it in the background).
11. **QA:** `python scripts/qa.py <ep> renders/<slug>.mp4`. Then send the MP4 with SendUserFile and update the series status doc.

## Stop and ask
- Before uploading a file to Copilot, downloading anything new, or a step that sends mail or changes settings. Never send email.
- A capture shows data the redaction presets don't cover (salary, ID, health, disability, termination).
- A capability the episode needs isn't ✅ in the matrix. Test it first and record the result.

## Token budget (chat)
Read `references/token-rules.md` once per session. In short:
- Batch browser steps and use refs instead of screenshots.
- Screenshots at `scale` 0.5–0.6. Full resolution only with `save_to_disk` for captures.
- Grep tool output; one contact sheet instead of individual frames.
- Never paste base64, email bodies or long Copilot answers into chat.
- Reports: short Thai, a table plus the decisions needed.
