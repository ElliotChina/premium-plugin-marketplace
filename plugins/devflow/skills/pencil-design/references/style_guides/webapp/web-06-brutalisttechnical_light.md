# Use the following style guide in the current design task

## Name of the styleguide: `web-06-brutalisttechnical_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Brutalist Technical Landing Page - Style Guide

---

## Style Summary

### Description

A high-contrast, brutalist landing page built as a single-column vertical stack where all sections sit flush edge-to-edge with zero gaps between them—structure is communicated entirely through selective black border strokes rather than spacing, shadows, or background variations. The color palette is reduced to just three values: black, white, and a single electric neon green used exclusively as a large hero background block. Typography pairs a heavy condensed display face for all headings with a clean sans-serif for all utility text, relying on extreme size contrast and tight line-heights to create hierarchy. Sections and cards share edges in a grid-table pattern, with per-edge borders creating incised dividing lines across the page surface. The overall tone is technical and developer-oriented—uppercase labels, wide letter-spacing, status badges, and form controls evoke creative-coding tools and industrial control panels.

### Key Aesthetics

- **Flush Edge-to-Edge Composition:** Every section and card sits flush against its neighbors with no gaps or margins. The page reads as a single connected surface divided by incised black lines, not as floating cards.
- **Dual Typeface System:** One heavy condensed display face for all headings, one clean sans-serif for all utility text. Hierarchy comes from extreme size jumps between the two.
- **Single Accent, Maximum Impact:** The only color beyond black and white is a neon electric green, used once as a massive hero background fill. Its rarity and scale make it the visual anchor.
- **Structure Through Borders:** Selective per-edge black strokes define all card boundaries, section dividers, and form elements. No shadows, no elevation, no background color shifts.
- **Tight Display Typography:** Headings use compressed line-heights (0.9–1.0) so multi-line titles feel like stacked slabs of text, giving the page a printed-poster quality.
- **Technical Developer Tone:** Uppercase labels, wide letter-spacing, status badges with live data readouts, and minimal functional icons borrow the visual language of terminal UIs and spec sheets.

### Tags

`light-mode` · `brutalist` · `technical` · `developer` · `neon-green` · `flush-layout` · `condensed-type` · `monochrome` · `industrial`

---

## Color System

An extremely reduced palette with no gradients, no shadows, and no opacity variations. Every element is solid black, solid white, or solid green. The accent color appears only once but at massive scale, creating a dramatic focal point atop an otherwise monochrome page.

### Core Backgrounds

- #FFFFFF — Page background; card fills, secondary badge fills, form field backgrounds
- #00FF00 — Hero accent fill; electric neon green used as a single large block for the hero section only (never used elsewhere)

### Text Colors

- #000000 — Primary text; all headings, body text, labels, badge text, icons
- #FFFFFF — Inverted text; used only inside dark (black-fill) badges

### Stroke Color

- #000000 — All borders, dividers, form outlines, badge outlines

---

## Typography

### Font Families

- **Anton** — used for all display text (hero headline, card numbers, card section labels, marquee text)
- **Inter** — used for all utility text (body descriptions, badge labels, form labels, form values, subtitles)

### Type Scale

- **96px** — Hero Headline; black weight, lineHeight: 1.0
- **64px** — Card Number; black weight, lineHeight: 0.9
- **22px** — Card Section Label / Marquee; black weight, letterSpacing: 1, lineHeight: 1.0
- **13px** — Body / Description; regular weight, lineHeight: 1.5
- **13px** — Form Label; bold, uppercase, letterSpacing: 1.5
- **13px** — Form Value / Subtitle; regular or bold, lineHeight: 1.5
- **11px** — Badge Text; bold, letterSpacing: 0.5

### Font Weights

- **900** — Black. All Anton display text (headlines, numbers, labels, marquee)
- **700** — Bold. Form labels, badge text, subtitle taglines
- **400** — Regular. Body descriptions, form values

### Line Height

- **1.5** — Body text; comfortable reading for descriptions and form values
- **1.0** — Display headings and section labels; tight stacking for poster-like density
- **0.9** — Card numbers; ultra-tight so large numerals sit as compact blocks

### Letter Spacing

- **+1.5px** — Uppercase form labels and subtitle taglines
- **+1px** — Card section labels and marquee text
- **+0.5px** — Badge text
- **0** — Default; body text, hero headlines, card numbers

---

## Spacing System

### Gap Scale (between elements)

- **24px** — Large; hero text group internal spacing
- **20px** — Standard; between elements inside feature cards (number → label → description → form fields)
- **8px** — Small; between inline badges

### Padding Scale

All sections use **24px uniform padding** on all sides. This consistent inner padding creates alignment across the hero, cards, and marquee bar.

- **24px** — All sides; hero section, feature cards
- **16px vertical / 24px horizontal** — Marquee bar
- **0 vertical / 12px horizontal** — Form select fields
- **6px vertical / 12px horizontal** — Badges

### Layout Pattern (Flush Grid)

Because all sections sit flush with zero gaps, cards share edges and borders serve as the only visual separators. Selective per-edge borders (right, bottom, or both) create a technical grid-table aesthetic where incised lines divide the surface.

- **1440px** — Screen Width; standard desktop
- **Full-width** — All sections span the complete page width
- **4 equal columns** — Feature card row; each card fills one quarter of the page width
- **0px** — Gap between all sections and cards; flush edge-to-edge composition
- **Top-left / bottom-left** — Hero content alignment; large negative space on the right is intentional and dramatic

---

## Borders & Strokes

Borders are the primary structural device in this design, replacing shadows, gaps, and background variations entirely. They are always black and applied selectively per edge.

### Scale

- **2px** — Heavy; section dividers (marquee top/bottom borders), card outer boundaries (right and bottom edges)
- **1.5px** — Standard; form input outlines, badge outlines

### Application Pattern

- Feature cards use selective right + bottom borders so adjacent cards share a single dividing line rather than doubling up
- The last card in a row omits the right border, using only a bottom border
- The marquee bar uses top + bottom borders to read as a horizontal divider band
- Form select fields and outlined badges use uniform 1.5px borders on all edges

---

## Corner Radius

Essentially zero throughout the design. Sharp corners reinforce the brutalist, industrial character and allow flush sections to share clean edge-to-edge boundaries.

### Scale

- **4px** — Badges only; a minimal softening on small status indicator pills
- **0px** — Everything else; cards, sections, form fields, hero area
