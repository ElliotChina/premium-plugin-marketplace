# Use the following style guide in the current design task

## Name of the styleguide: `mobile-03-nordicbrutalist_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Nordic Brutalist Mobile — Style Guide

---

## Style Summary

### Description

Warm stone canvas mobile interface that feels both cozy and commanding. Manrope at extrabold 800 weight delivers confident brutalist authority while soft rounded corners and earthy stone tones create Nordic warmth. The design embraces burnt orange (#C2410C) as a singular powerful accent against a foundation of charcoal (#2D2D2D) and warm cream (#FAF9F7). Stone gray surfaces (#E7E5E4) provide gentle contrast without coldness. Metric values use massive display sizes (40–56px) with extrabold weight for maximum visual impact. Status indicators use rounded squares (8px radius) rather than circles—a signature element. Suited for productivity apps, habit trackers, and goal-oriented tools targeting users who appreciate warm sophistication and functional confidence.

### Key Aesthetics

- **Nordic Warmth:** Warm cream canvas (#FAF9F7), stone gray cards (#E7E5E4), and charcoal (#2D2D2D) dark elements—no pure black or pure white.
- **Brutalist Typography:** Manrope extrabold 800 for commanding headlines and metrics; Inter for clean body text.
- **Burnt Orange Accent:** #C2410C as the singular earthy accent—used sparingly for active states, CTAs, and emphasis.
- **Rounded Square Signature:** 8px radius status indicators are the hallmark element—softer than sharp corners but more grounded than circles.
- **Generous Card Radii:** 14–16px on cards provides Nordic softness to counterbalance the typographic weight.
- **Fill-Based Depth:** Surfaces defined by warm fills (cream, stone, charcoal), not shadows. Charcoal cards for emphasis, stone cards for standard surfaces.

### Tags

`mobile` · `light-mode` · `nordic` · `brutalist` · `warm` · `earthy` · `stone` · `orange-accent` · `rounded` · `bold-type`

---

## Color System

Color creates warmth and grounded confidence. Burnt orange is THE accent—earthy and powerful. Stone gray is the primary card surface. Charcoal anchors dark elements and metrics. Cream background provides warmth. No pure black or pure white—always warm-tinted.

### Core Backgrounds

- #FAF9F7 — Page Background (warm cream)
- #E7E5E4 — Card Surface (stone gray)
- #2D2D2D — Dark Surface; charcoal emphasis/dark cards
- #D6D3D1 — Muted Surface; dividers, light stone
- #44403C — Dark Muted; image placeholders

### Text Colors

- #2D2D2D — Text Primary; headlines, primary content (charcoal)
- #78716C — Text Secondary; labels, descriptions (warm gray)
- #A8A29E — Text Tertiary; meta info, placeholders (light stone)
- #FAF9F7 — Text On Dark; text on dark surfaces (cream)

### Border Colors

- #D6D3D1 — Border Subtle; dividers, inactive strokes (1px)
- #C2410C — Border Active; active state borders (2–2.5px)

### Accent Colors

- #C2410C — Burnt Orange; active states, CTAs, emphasis

---

## Typography

Manrope delivers confident brutalist authority with its geometric character. Inter provides clean, readable support for body text. The design relies on extrabold 800 weight for commanding headlines and metrics, with no light weights.

### Font Families

- **Manrope** — Headlines, screen titles, section headers, metrics, day indicators, tab labels
- **Inter** — Body text, descriptions, labels, meta info

### Type Scale

- **56px** — Hero Metric. Manrope, extrabold 800, lineHeight: 1.0
- **40px** — Large Metric. Manrope, extrabold 800, lineHeight: 1.0
- **32px** — Screen Title. Manrope, extrabold 800, letterSpacing: -0.5, lineHeight: 1.1
- **26px** — Screen Header. Manrope, extrabold 800, letterSpacing: -0.3
- **22px** — Section Title. Manrope, bold 700
- **16px** — Subsection, Metric Medium. Manrope, bold 700
- **15px** — List Item Title, Body. Manrope, medium 500 / Inter, normal 400
- **14px** — Label, Callout. Inter, medium 500 / semibold 600
- **13px** — Subhead, Day Indicator. Manrope, bold 700 / Inter, normal 400
- **12px** — Section Label, Footnote. Manrope, bold 700, letterSpacing: 2, uppercase
- **11px** — Tab Label, Caption. Manrope, semibold 600 / bold 700

### Font Weights

- **800** — Extrabold. Headlines, metrics (KEY WEIGHT)
- **700** — Bold. Section titles, labels
- **600** — Semibold. Subheads, inactive tabs
- **500** — Medium. Labels, descriptions (Inter)
- **400** — Normal. Body text (Inter)

### Letter Spacing

- **-0.5px** — Screen titles (tight for impact)
- **+2px** — Uppercase section labels (wide tracking)
- **0** — Default; body text and labels

### Line Height

- **1.0** — Metric values (compact)
- **1.1** — Large titles
- **1.4** — Descriptions, meta text
- **1.5** — Help content, paragraphs

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section vertical gaps
- **16px** — Standard; section header to content, component spacing
- **14px** — Row; list item content spacing
- **12px** — Medium; metric card internal, program scroll
- **10px** — Schedule; schedule card spacing
- **8px** — Small; program card content
- **6px** — Day; day grid spacing
- **4px** — Tight; icon to label, day indicator internals

### Padding Scale

- **[0, 24, 24, 24]** — Content wrapper (top, horizontal, bottom)
- **20px** — Metric cards (uniform)
- **18px** — List item rows
- **16px** — Card rows, help items, program card content
- **[12, 21, 21, 21]** — Tab bar section (top, sides, bottom)
- **[8, 16]** — Tab bar items
- **4px** — Segmented control container, tab bar container

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **874px** — Minimum Screen Height
- **24px** — Content Padding (horizontal)
- **32px** — Section Gap (vertical)
- **16px** — Header-to-Content Gap
- **12–16px** — Card Gap (within sections)
- **180px** — Program Card Width (horizontal scroll)

---

## Corner Radius

Rounded corners are essential to this design language, providing Nordic softness to counterbalance brutalist typography weight. The 8px rounded square for status indicators is a signature element. Cards use generous 14–16px radii for approachable warmth. The pill-shaped tab bar provides playful contrast.

- **2px** — Accent bar detail
- **8px** — Status indicators (rounded square signature)
- **10px** — Day pills, week grid items
- **12px** — Notification button, segmented control
- **14px** — Search bar, schedule cards, help cards
- **16px** — Metric cards, habit cards, program cards
- **100px** — Tab bar pill

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, bar-chart, compass, user (tab bar)
- **Actions:** search, bell, plus, chevron-right, chevron-down
- **Status:** check (completion indicator)

### Icon Sizes

- **24px** — Navigation (tab bar)
- **22px** — Notification bell, action buttons
- **20px** — Search, chevrons
- **16px** — Checkmarks
- **13px** — Trend indicators

### Icon Color States

- #C2410C — Active (navigation, burnt orange)
- #78716C — Inactive (navigation, search placeholder, warm gray)
- #FAF9F7 — On Dark Surfaces (cream)