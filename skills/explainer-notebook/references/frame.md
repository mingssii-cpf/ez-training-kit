# Explainer Notebook — visual contract

Warm grid paper, dark ink, a restrained teal accent and marker-yellow emphasis. The style belongs to the layout and materials; it works with any character or with none.

## Palette and typography

| Token | Value | Use |
|---|---|---|
| bg | #fbf7ee | Paper canvas |
| grid | rgba(31,42,68,0.06) | 48 px grid |
| ink | #1f2a44 | Text, borders and offset shadows |
| muted | #666c7a | Supporting text |
| accent | #0f8f83 | Focus, numbers and progress |
| accent-ink | #0d7a70 | Small labels on paper |
| marker | #ffe066 | Short highlighted phrase or tape |
| sticky | #fff1a8 | Prompt notes |
| pink | #ffd9d2 | Occasional secondary note |

Default canvas: 1920×1080 at 30 fps. IBM Plex Sans Thai 400/500/600/700 supports Thai and Latin; Space Grotesk supports Latin labels and numbers. Use 64–84 px titles, 38–42 px body, 22–32 px labels. Keep the bottom caption band clear.

Change the CSS variables in the episode's tools/style.css to change colors. Check text contrast and the rendered layout after any palette or font change.

## Components

- Paper cards: slight rotation, ink borders and a small hard offset shadow.
- Prompt stickies: warm yellow, a small PROMPT label, readable text and enough hold time.
- Real screenshots: white photo border, two tape strips and a subtle tilt. Crop around the demonstrated area.
- Focus: hand-drawn ellipse or a restrained spotlight. Keep annotations outside important UI text.
- Step cards: one short action per card, numbered in reading order.
- Optional mascot: an image placed beside the lesson. Scale with object-fit:contain; do not stretch it or make the whole scene depend on it.
- Optional logo: top right, within a 300×52 px box. Omit the element when absent.

## Motion

Short card pops, a small settling rotation, marker sweeps, gentle screenshot punch-ins and page-like scene transitions. Keep motion tied to the explanation; avoid decorative looping, neon and glow. Reuse the shipped eplib helpers.

The static preview shows final positions, not motion. Check entry/exit frames and a real render when producing a video. Brand identity, subject, narrator, music and mascot are project choices, not requirements of this theme.
