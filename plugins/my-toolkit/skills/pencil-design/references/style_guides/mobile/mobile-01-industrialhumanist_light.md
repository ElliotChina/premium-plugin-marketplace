# Use the following style guide in the current design task

## Name of the styleguide: `mobile-01-industrialhumanist_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Industrial Humanist Mobile Dashboard — Style Guide

---

## Style Summary

### Description

A warm stone canvas mobile interface that balances condensed industrial typography with warm serif elegance. Barlow Semi Condensed at bold weight delivers efficient, all-caps labels with wide tracking while Source Serif 4 provides warm, humanist body content. The design embraces an earthy color palette—forest green (#3D7A5A) for completion, burnt orange (#C45C26) for progress—against a natural taupe foundation (#F4F3F1). White cards float with subtle shadows creating gentle depth. Square status indicators and vertical bar charts reinforce industrial geometry while warm colors and serifs add humanity. Suited for wellness apps, journaling tools, and productivity applications targeting users who appreciate crafted, tactile design with professional refinement.

### Key Aesthetics

- **Industrial Efficiency:** Barlow Semi Condensed all-caps labels with wide letter-spacing (+3px) for systematic section headers.
- **Humanist Warmth:** Source Serif 4 for headlines and body content brings editorial elegance and readability.
- **Earthy Palette:** Forest green (#3D7A5A) and burnt orange (#C45C26) against warm stone (#F4F3F1) create organic warmth.
- **Tactile Depth:** White cards with subtle shadows (0 1px 6px #0000000D) feel like quality paper.
- **Sharp Geometry:** Zero corner radii throughout—hard edges contrast with the warm color palette.
- **Industrial Details:** Square status indicators, 4px accent bars on schedule cards, vertical bar charts with warm backgrounds.

### Tags

`mobile` · `light-mode` · `industrial` · `humanist` · `warm` · `serif` · `condensed` · `earthy` · `organic` · `shadowed`

---

## Color System

Color creates warmth through an earthy, organic palette. Forest green signals completion. Burnt orange indicates progress and draws attention. Warm stone backgrounds feel like quality paper. Dark charcoal (#2B2B2B) replaces pure black for warmth throughout.

### Core Backgrounds

- #F4F3F1 — Page Background (warm stone/paper)
- #FFFFFF — Card Surface (white)
- #EEECE9 — Bar Background (warm beige for chart backgrounds)

### Text Colors

- #1C1C1C — Text Primary (warm black)
- #5C5C5C — Text Secondary (descriptions, labels)
- #8C8A87 — Text Muted (inactive nav, meta)
- #B5B3B0 — Text Disabled

### Border Colors

- #D9D7D4 — Border Subtle; button strokes, segment dividers

### Accent Colors

- #3D7A5A — Forest Green; success, completion
- #C45C26 — Burnt Orange; progress, active navigation, warmth
- #2B2B2B — Dark Charcoal; buttons, active segments, dark program cards
- #FFFFFF — Text On Green / On Charcoal (white)

### Shadow System

- **Card Shadow:** (0, 1px) blur 6px #0000000D — subtle outer shadow on white cards
- **Navigation Shadow:** (0, -1px) blur 6px #0000000D — upward shadow on bottom nav

---

## Typography

The dual-font system creates the Industrial x Humanist tension—Barlow Semi Condensed handles the systematic layer (labels, meta, navigation), Source Serif 4 handles the editorial layer (headlines, body, descriptions). Italic Source Serif 4 adds visual variety for placeholders and program descriptions.

### Font Families

- **Barlow Semi Condensed** — Section labels, meta text, badges, buttons, navigation, timestamps, day labels (all-caps, tracked)
- **Source Serif 4** — Headlines, body text, list titles, accordion titles, program titles, descriptions

### Type Scale

- **36px** — Metric Value. Source Serif 4, semibold 600, letterSpacing: -1
- **32px** — Large Title. Source Serif 4, semibold 600, letterSpacing: -0.5
- **18px** — Program Title, Schedule Time. Source Serif 4, semibold 600 / Barlow SC, bold 700
- **15px** — Body, List Title. Source Serif 4, semibold 600
- **14px** — Callout, Accordion Content. Source Serif 4, normal / italic, lineHeight: 1.6
- **12px** — Section Label, Segment Label, Subhead. Barlow SC, bold 700, letterSpacing: 3 / +2px, uppercase
- **11px** — Meta, Badge, Button, Progress, Day Label. Barlow SC, medium 500 / semibold 600, letterSpacing: 0.5–1px, uppercase
- **10px** — Tab Label, Metric Label, Time Suffix. Barlow SC, bold 700 / medium 500, letterSpacing: 1–2px, uppercase

### Font Weights

- **700** — Bold. Barlow SC section labels, active tab labels, schedule times
- **600** — Semibold. Source Serif 4 body/titles, Barlow SC badges/buttons
- **500** — Medium. Barlow SC meta text, inactive labels
- **400** — Normal. Source Serif 4 italic descriptions

### Letter Spacing

- **+3px** — Section labels (very wide, industrial)
- **+2px** — Segment labels, metric labels, AM/PM
- **+1px** — Badge text, button labels, tab labels
- **+0.5px** — Meta text
- **-0.5px** — Headlines (slightly tight)
- **-1px** — Large metric numbers
- **0** — Default; body text

### Line Height

- **1.6** — Readable; paragraph content, accordion answers
- **1.2** — Tight; multi-line program titles
- **auto** — Default; most elements

---

## Spacing System

### Gap Scale (between elements)

- **24px** — Major; section gaps
- **20px** — Large; search padding, schedule content
- **16px** — Standard; section gap, row padding
- **12px** — Medium; card internal, row content
- **8px** — Standard; day chart gaps, small groups
- **6px** — Small; add button internal
- **4px** — Tight; title + description pairs, schedule info
- **2px** — Minimal; time stack (hours + AM/PM)

### Padding Scale

- **[20, 20]** — Content wrapper, program cards
- **[16, 16]** — Habit rows, metric cards, accordion, week grid
- **[16, 0]** — Search section padding
- **[12, 20, 28, 20]** — Bottom navigation
- **[8, 12]** — Add button
- **[4, 8]** — Badge containers

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **20px** — Content Padding (all around)
- **24px** — Section Gap (vertical)
- **12px** — Card Gap (within sections)
- **180px** — Program Card Width (fixed)

---

## Corner Radius

This design system uses **zero corner radius** throughout. Sharp corners maintain the industrial quality while warm colors and serifs add humanity—the contrast between hard edges and soft palette creates the Industrial x Humanist tension.

- **0px** — ALL elements (cards, buttons, checkboxes, bars, segments, navigation)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, check-square, bar-chart, user (bottom nav)
- **Actions:** bell, search, plus, chevron-down, chevron-right

### Icon Sizes

- **22px** — Navigation (bottom nav icons)
- **18px** — Notification, Search, Chevrons
- **14px** — Checkmarks, action buttons

### Icon Color States

- #C45C26 — Active navigation (burnt orange)
- #8C8A87 — Inactive navigation (warm gray)
- #5C5C5C — Search, chevrons (secondary)
- #2B2B2B — Notification bell (dark charcoal)
- #FFFFFF — On green backgrounds (white)