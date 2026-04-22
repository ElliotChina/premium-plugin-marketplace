# Use the following style guide in the current design task

## Name of the styleguide: `mobile-03-bauhausdigital_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Bauhaus Digital Mobile — Style Guide

---

## Style Summary

### Description

Pure white canvas mobile interface that speaks in decisive geometric statements. DM Sans at bold 700 weight delivers confident authority while 2px black strokes replace shadows entirely, creating stark graphic definition. Bauhaus red (#E53935) serves as a singular powerful accent against a pure black-and-white foundation. White surfaces are framed by bold black outlines, eliminating softness in favor of architectural precision. Cards feature sharp corners with no rounded edges, while circular elements (status indicators, pills) provide controlled geometric contrast. Metric values use massive display sizes (40–64px) for maximum visual impact. Suited for productivity apps, fitness trackers, and goal-oriented tools targeting users who appreciate bold modernism and functional clarity.

### Key Aesthetics

- **Bauhaus Heritage:** Primary colors, geometric purity, form follows function—sharp rectangles for structure, circles for accent.
- **Stroke-Based Definition:** 2px black outlines replace shadows entirely; all depth comes from strokes, never blur or offset.
- **High Contrast:** Pure black (#000000) on pure white (#FFFFFF) with no gray compromises or warm tints on backgrounds.
- **Singular Red Accent:** Bauhaus red (#E53935) used sparingly for CTAs, active states, and emphasis—maximum impact through restraint.
- **Bold Typography:** DM Sans at 700 weight for all headlines and metrics; massive display sizes (40–64px) for data emphasis.
- **Zero Decoration:** No shadows, no gradients, no rounded corners on cards—pure architectural precision. Pill-shaped tab bar and circular status indicators provide controlled geometric contrast.

### Tags

`mobile` · `light-mode` · `bauhaus` · `bold` · `graphic` · `high-contrast` · `geometric` · `black-stroke` · `red-accent` · `minimal`

---

## Color System

The design achieves maximum contrast through a strict black-and-white foundation with a singular red accent. Pure white (#FFFFFF) and pure black (#000000) are used without warm tints or gray compromises. Red (#E53935) is THE accent color—used sparingly for maximum impact. Filled cards use solid color (red or black) without strokes; stroked cards use white fill with 2px black outlines.

### Core Backgrounds

- #FFFFFF — Page Background, Card Surface (pure white)
- #F5F5F5 — Muted Surface; secondary elements, search bar, inactive segments, tab bar

### Text Colors

- #000000 — Text Primary; headlines, primary content (pure black)
- #757575 — Text Secondary; body text, descriptions, inactive navigation
- #BDBDBD — Text Tertiary; labels, placeholders, meta info

### Border Colors

- #000000 — Border Primary; card strokes, dividers (2px)
- #E53935 — Border Accent; active state borders (2–2.5px)
- #BDBDBD — Border Muted; inactive/subtle borders (2px)

### Accent Colors

- #E53935 — Red Primary; active states, CTAs, emphasis, completed status
- #000000 — Black Accent; secondary metric cards, filled states, segmented control active
- #FFFFFF — On Accent; white text/icons on red or black surfaces
- #BDBDBD — Inactive; pending states, future indicators

---

## Typography

DM Sans—a geometric sans-serif—serves as the sole typeface, creating unity across all hierarchy levels. Bold 700 weight dominates headlines and metrics for commanding presence, while lighter weights (400–500) handle body text and labels. The system relies on dramatic size contrast (11px captions to 64px hero metrics) rather than font variety to establish hierarchy.

### Font Families

- **DM Sans** — All text: headlines, metrics, body, labels, navigation

### Type Scale

- **64px** — Metric Hero. DM Sans, bold 700, lineHeight: 1.0
- **40px** — Metric Large. DM Sans, bold 700, lineHeight: 1.0
- **34px** — Large Title. DM Sans, bold 700, letterSpacing: -0.5, lineHeight: 1.05
- **28px** — Title 1. DM Sans, bold 700, letterSpacing: -0.3
- **24px** — Title 2, Metric Medium. DM Sans, bold 700
- **18px** — Title 3, Metric Small. DM Sans, bold 700
- **15px** — Headline, Body. DM Sans, semibold 600 / normal 400
- **14px** — Callout. DM Sans, medium 500 / semibold 600
- **13px** — Subhead. DM Sans, medium 500
- **12px** — Footnote, Caption 2. DM Sans, semibold 600
- **11px** — Caption 1 (tab labels). DM Sans, semibold 600 / bold 700

### Font Weights

- **700** — Bold. All titles, headlines, metrics
- **600** — Semibold. Subheads, caption emphasis, footnotes
- **500** — Medium. Labels, secondary emphasis
- **400** — Normal. Body text, descriptions

### Letter Spacing

- **-0.5px** — Display headlines (Large Title, tight for impact)
- **+2px** — Uppercase section labels (wide tracking)
- **0** — Default; all other text

### Line Height

- **1.0** — Metric values (compact)
- **1.05** — Large titles (display)
- **1.4** — Descriptions, meta text (standard)
- **1.5** — Expanded content, help text (readable)

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section spacing
- **16px** — Standard; component spacing, section header to content, metric card grid gap
- **14px** — Row; list item content spacing
- **8px** — Small; element groups, card content, day column gaps
- **6px** — Tight; day indicator internals
- **4px** — Minimal; icon to label, status pairs

### Padding Scale

- **[0, 24, 24, 24]** — Content wrapper (top, horizontal, bottom)
- **24px** — Metric cards (uniform)
- **[18, 0]** — List item rows (vertical, horizontal)
- **[0, 18]** — Search bar (horizontal)
- **16px** — Card rows, schedule items, program card content
- **[12, 21, 21, 21]** — Tab bar section (top, sides, bottom for safe area)
- **[8, 16]** — Tab bar items (vertical, horizontal)
- **4px** — Small pills, tight badges

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **874px** — Minimum Screen Height
- **24px** — Content Padding (horizontal)
- **32px** — Section Gap (vertical)
- **16px** — Component Gap (standard)
- **2 columns** — Metric Card Grid, equal width, 16px gap
- **180px** — Program Card Width (horizontal scroll)

---

## Corner Radius

Sharp corners are essential to this design language. Cards and containers reject softness in favor of architectural precision—a direct Bauhaus influence. Circular elements exist as controlled geometric contrast, not decoration.

- **0px** — Cards, containers, search bar, segmented controls, accent bars (sharp corners throughout)
- **14px** — Circular stroke indicators (fixed size elements)
- **24px** — Notification button (softened circle)
- **100px** — Pills, tab bar, circular status indicators (full round)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, bar-chart, compass, user (tab bar)
- **Actions:** search, bell, plus, chevron-right, chevron-up, chevron-down
- **Status:** trending-up, trending-down, check (on colored cards)

### Icon Sizes

- **24px** — Navigation (tab bar icons)
- **22px** — Notification bell, action buttons
- **20px** — Search, chevrons/arrows
- **13px** — Trend indicators (on metric cards)

### Icon Color States

- #E53935 — Active (tab bar, navigation)
- #757575 — Inactive (tab bar, search placeholder, chevrons)
- #FFFFFF — On Dark Surfaces (metric cards, expanded accordion)
- #000000 — Default (header icons on white background)
