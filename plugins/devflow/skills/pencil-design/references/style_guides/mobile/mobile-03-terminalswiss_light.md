# Use the following style guide in the current design task

## Name of the styleguide: `mobile-03-terminalswiss_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Terminal Swiss Mobile — Style Guide

---

## Style Summary

### Description

Pure black canvas mobile interface that channels the raw energy of terminal interfaces and NYC subway signage. The design employs a dual-typeface system: Inter for clean geometric headers at bold weights paired with Space Mono for data and metrics, creating a striking contrast between humanist and mechanical. A singular red accent (#FF0000) slices through the monochromatic darkness with urgent intensity. Sharp-cornered cards with thin gray borders (#333333) create structured containment while all-caps letter-spaced labels reference Swiss International style. Massive display numbers (132px) dominate hero sections with tight tracking (-8px) for maximum visual impact. The aesthetic is unapologetically technical, designed for users who value information density over decoration. Suited for productivity apps, fitness trackers, and data-heavy applications targeting users who appreciate raw functionality and brutalist clarity.

### Key Aesthetics

- **Massive Display Numbers:** 132px hero metrics at extrabold 800 with -8px letter-spacing create commanding visual impact.
- **Dual Typography System:** Inter for geometric structure and headers, Space Mono for all data, metrics, and meta—mechanical vs humanist tension.
- **Signal Red Accent:** #FF0000 pure red is the singular accent—cuts through pure black with urgent clarity for active/completed states.
- **Sharp Zero Radius:** All elements use 0px corners except the pill tab bar (100px)—razor-sharp brutalist geometry throughout.
- **Border-Defined Cards:** Thin 1px #333333 strokes define all containers; no fills on cards—borders do the work, not shadows or fills.
- **All-Caps Swiss Labels:** Section headers in 10px uppercase with 2–3px letter-spacing reference Swiss International style.

### Tags

`mobile` · `dark-mode` · `terminal` · `swiss` · `brutalist` · `monospace` · `high-contrast` · `data-driven` · `technical` · `minimal`

---

## Color System

Color is weaponized for maximum impact. Only one accent color (red) to maintain stark clarity. Red signals completion, action, and importance. Gray (#666666) handles all secondary information. Borders define space, not fills. Contrast is absolute: white on black. No gradients except for the tab bar fade effect.

### Core Backgrounds

- #0C0C0C — Page Background (near-black primary surface)
- #0C0C0C — Card Surface (same as background; borders define cards)
- #1A1A1A — Elevated Surface; dividers/separators
- #333333 — Active Surface; expanded/selected state backgrounds

### Text Colors

- #FFFFFF — Text Primary; headlines, metrics, primary content (pure white)
- #666666 — Text Secondary; labels, descriptions, meta info, placeholders, inactive tabs

### Border Colors

- #333333 — Border Primary; card strokes, dividers, controls (1px)
- #1A1A1A — Border Divider; internal separators within cards (1px)

### Accent Colors

- #FF0000 — Signal Red; active states, CTAs, completed items, emphasis

---

## Typography

Inter serves as the primary structural typeface—geometric sans-serif that delivers clean, modern authority for headers and UI. Space Mono handles all data display: metrics, timestamps, statuses, and meta information with mechanical precision. The design relies on extreme size contrast (10px labels to 132px metrics) and the humanist/mechanical font tension.

### Font Families

- **Inter** — Screen headers, card titles, list titles, section labels, buttons, tab labels, UI elements
- **Space Mono** — Metrics, data values, schedule times, meta info, badges, day labels

### Type Scale

- **132px** — Hero Metric. Inter, extrabold 800, letterSpacing: -8, lineHeight: 0.85
- **48px** — Percent Symbol. Inter, extrabold 800
- **36px** — Secondary Metric. Space Mono, bold 700
- **28px** — Screen Header. Inter, bold 700, letterSpacing: -0.5
- **24px** — Large Value. Space Mono, bold 700
- **16px** — Card Title. Inter, semibold 600
- **15px** — List Item Title. Inter, medium 500
- **14px** — Schedule Time, Button. Space Mono bold 700 / Inter normal 400
- **13px** — Description, Segmented Label. Inter, normal 400 / semibold 600, lineHeight: 1.4
- **12px** — Link, Badge. Inter, medium 500 / Space Mono normal 400
- **11px** — Meta Info. Space Mono, normal 400 / bold 700
- **10px** — Section Label, Tab Label. Inter, semibold 600 / medium 500, letterSpacing: 2–3px, all-caps

### Font Weights

- **800** — Extrabold. Hero display numbers
- **700** — Bold. Screen headers, data values
- **600** — Semibold. Section labels, card titles, active tabs
- **500** — Medium. List titles, links
- **400** — Normal. Body text, descriptions

### Letter Spacing

- **-8px** — Hero metrics (132px, extreme tight)
- **-0.5px** — Screen headers (slightly tight)
- **+2px to +3px** — Uppercase section labels (expanded)
- **0** — Default; body text and descriptions

### Line Height

- **0.85** — Hero display numbers (compact)
- **1.2** — Single-line elements
- **1.4** — Descriptions, card content
- **1.5** — Expanded help text, paragraphs

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section vertical gaps
- **24px** — Hero; hero section internal gaps
- **16px** — Standard; row internal gaps, component spacing, card gaps
- **12px** — Medium; expanded content gaps, hero number to percent
- **8px** — Small; internal card content, day columns
- **4px** — Tight; icon to label (navigation), content within rows
- **2px** — Minimal; title + meta within rows

### Padding Scale

- **[0, 24, 24, 24]** — Content wrapper (top, horizontal, bottom)
- **24px** — Metric cards (uniform)
- **16px** — List rows, schedule cards (uniform)
- **[12, 21, 21, 21]** — Tab bar section (with safe area)
- **[12, 16]** — Program card badges
- **[10, 16]** — Small buttons, badges
- **[8, 16]** — Tab items

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **874px** — Minimum Screen Height
- **24px** — Content Padding (horizontal)
- **32px** — Section Gap (vertical)
- **16px** — Component Gap (header to content, between cards)
- **180px** — Program Card Width (horizontal scroll)

---

## Corner Radius

Sharp corners define the entire design language. This brutalist approach creates tension and technical precision. The singular exception—the pill-shaped tab bar—provides striking contrast and signals its special navigation function. Every other element maintains razor-sharp geometry.

- **0px** — All elements (cards, buttons, search bars, segmented controls, status indicators, day squares, program cards)
- **100px** — Tab bar pill (only rounded element)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, bar-chart, compass, user (tab bar)
- **Actions:** search, bell, plus, chevron-right, chevron-down
- **Status:** Square indicators (16px filled/outlined rectangles)

### Icon Sizes

- **22px** — Navigation (tab bar)
- **18px** — Notification bell, search, chevrons
- **14px** — Add button icon

### Icon Color States

- #FF0000 — Active (navigation, signal red)
- #666666 — Inactive (navigation, search placeholder, gray)
- #FFFFFF — On Dark Backgrounds (white)
