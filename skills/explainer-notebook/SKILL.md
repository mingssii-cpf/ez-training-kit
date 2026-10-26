---
name: explainer-notebook
description: Create or adapt Thai or English explainer and training-video visuals in a warm grid-paper notebook style, with taped screenshots, sticky prompts, marker highlights and numbered cards. Branding, mascot, subject and voice are optional project choices.
metadata:
  version: "2.0.0"
---

# Explainer Notebook

Reuse the visual language, not the original EZ identity. Default to no logo and no mascot. Do not assume CPF, HR, Copilot, a TTS provider, a signed-in account or an approved voice.

Read [frame.md](references/frame.md) for the design contract. The code in assets/style.css is its reusable implementation. Use [workflow.md](references/workflow.md) only for production, and [eplib.md](references/eplib.md) when composing new scenes.

## Start

Run from this skill folder, replacing paths and content for the project:

```text
python scripts/new_episode.py <output-folder> <slug> --title "Clearer team meetings" --preview
python scripts/new_episode.py <output-folder> <slug> --brand "Your team" --logo <logo.png> --mascot <character.webp> --preview
```

All branding flags are optional. Custom files are copied into the episode. The starter includes a title scene, prompt sticky and three numbered cards; adapt their content in script.json and layout in tools/build.py.

Open the generated preview.html for an offline static gallery. Its timing is synthetic, and it has no narration. index.html is the timed HyperFrames composition, not a standalone player. Once generated, the episode's build files and assets are self-contained and can move together.

## Adapt

- brand.json controls optional logo and character paths plus the header name. Set logo/mascot to null to remove them; rebuild afterward.
- script.json controls the title, narration and starter card content. New scene IDs require matching scene code in tools/build.py.
- tools/style.css controls palette and typography. Keep the notebook hierarchy when changing brand colors.
- Choose voice, music and topic per project. For real narration place per-scene WAVs in audio/voice/, then run scripts/align.py. Never present preview timing as timing measured from speech.
- Capture actual UI when teaching an application. Inspect every redacted shot; preset rectangles depend on the captured viewport.

## Optional EZ preset

Add --preset ez only when the user wants EZ/CPF branding. Custom --logo and --mascot flags override that preset. Those assets live in assets/presets/ez/public/ and are not copied into the default output.

Keep the user's approved direction. Adapt existing components before adding a new visual system. Before delivery run the repository's tools/check.py, then the actual episode's check/render/QA as applicable; static proof does not establish rendered-video quality.
