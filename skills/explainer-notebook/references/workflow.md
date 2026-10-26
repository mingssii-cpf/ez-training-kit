# From theme to a real episode

1. Scaffold with optional --brand, --logo and --mascot. Use --preview to inspect three silent starter scenes before producing audio.
2. Edit script.json and tools/build.py. Keep titles short (the starter accepts up to 60 characters). The prompt and three step labels are sample content; replace them for the topic.
3. Choose narration and a voice for this project. Put one real WAV per scene at audio/voice/<scene-id>.wav. Any recording or TTS provider can supply those files.
4. Run python <skill>/scripts/align.py <episode>. This replaces synthetic preview timing with measurements from the voice. Review line boundaries and captions.
5. For screenshots, capture the actual application. In redact.json set raw_dir to the actual capture folder and remeasure privacy rectangles for that viewport. Run scripts/redact.py, then visually inspect the contact sheet.
6. Optional background music: provide an appropriately licensed track and use scripts/fit_bgm.py. scripts/compose_bgm.py is an optional NumPy-based alternative. The kit does not require music.
7. Run python <episode>/tools/build.py. Within the episode folder run npm run check, then npm run render -- --fps 30 --quality standard --workers 2 --output renders/<slug>.mp4.
8. Run python <skill>/scripts/qa.py <episode> <mp4>. Inspect typography, character proportions, captions, redaction, transitions and audio in the actual render.

Requirements: Python 3 for scaffold/build; Node.js/npm for HyperFrames; FFmpeg/ffprobe for voice alignment and video/audio QA. Pillow is needed only for redact.py; NumPy only for compose_bgm.py. The existing HyperFrames 0.8.143 pin is retained for reproducibility.

Do not use preview timing for a voiced final. Nothing in this kit grants permission to upload private files, use someone else's branding or send messages. Account sign-in and browser tooling depend on the user's host.
