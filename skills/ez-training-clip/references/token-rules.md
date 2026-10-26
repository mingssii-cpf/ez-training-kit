# Token rules (measured costs in the S1E1 session)

Biggest waste seen: full-size screenshots for navigation, `get_page_text` on long Copilot answers / mailbox,
full `hyperframes check` output, one-frame-at-a-time inspection, a base64 dump of a file, and re-asking settled choices.

## Browser
- Plan 3–10 steps and send them as **one `browser_batch`** (click → type → key → waits → find/screenshot).
- Navigate with `find` (refs) instead of screenshots. Screenshot only to verify a visual, at `scale: 0.5–0.6`.
- Full-resolution screenshots only for shots that go into the video, with `save_to_disk: true`. Don't re-view them in chat;
  review the redacted `_contact.jpg` once.
- Never `get_page_text` on Outlook/Copilot answers with private data; use `zoom` on the region you need.
- To read the end of a long answer use `javascript_tool` returning `innerText.slice(-N)` with a small N. Never dump the whole page.
- File uploads: `file_upload` (Chrome) by path. Never base64 a file into a tool call.

## Shell / tools
- Filter output: `check 2>&1 | grep -E "✗|Check"`; render `| tail -2`; ffmpeg `-v error`; ffprobe single fields.
- Inspect visuals as **one contact sheet** (`snapshot --at t1,t2,…` → `contact-sheet.jpg`, `qa.py` → `qa/frames.jpg`).
- Edit with small targeted Python/sed replacements and verify with a count (`grep -c`). Don't rewrite or re-read big files.
- Run long renders with `run_in_background` and keep working (or wait for the notification). Don't poll.

## Conversation
- Locked decisions (style, voice, music, SFX, pipeline) are in SKILL.md. Don't reopen them unless the owner asks.
- Ask only content questions (topic, prompt wording, which test result to show). Batch them, at most 3.
- Status updates: one line. Final report: a short table (what changed / what to review / next).
