# Use the following style guide in the current design task

## Name of the styleguide: `mobile-02-brutalistluxury_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Brutalist Luxury Mobile Dashboard — Style Guide

---

## Style Summary

### Description

Unapologetically bold dark-canvas mobile interface demanding attention through typographic weight and precious metal accents. Space Grotesk at bold 700 weight delivers commanding ALL-CAPS headlines with tight letter-spacing while maintaining geometric precision throughout. The design embraces deep charcoal (#111111) as primary background with elevated dark surfaces (#1C1C1C) creating subtle depth. Signature gold accent (#D4AF37) provides luxurious emphasis for section markers, active states, and progress indicators. Vertical gold accent bars (3x14px) precede every section label. Zero corner radius maintains brutalist sharpness across all cards and containers. Square checkboxes reinforce the geometric vocabulary. The iOS 18-style pill tab bar features UPPERCASE labels. Suited for premium fitness apps, luxury lifestyle products, and high-end productivity tools targeting users who appreciate bold confidence and sophisticated restraint.

### Key Aesthetics

- **Brutalist Geometry:** Zero corner radius, sharp rectangular forms across all cards, containers, and controls.
- **Gold Luxury Restraint:** #D4AF37 used sparingly for maximum impact—active states, accent bars, CTAs.
- **Typographic Power:** Space Grotesk bold 700, ALL-CAPS throughout with generous letter-spacing.
- **Vertical Accent Markers:** 3x14px gold rectangles before every section label create systematic visual rhythm.
- **Dark Surface Layering:** Depth through #111111 → #1C1C1C → #282828 color stepping, no shadows.
- **Pill Tab Bar:** iOS 18-style floating pill with UPPERCASE labels and gold active state.

### Tags

`mobile` · `dark-mode` · `brutalist` · `luxury` · `gold` · `geometric` · `bold` · `uppercase` · `premium` · `high-end`

---

## Color System

Color creates hierarchy through dramatic restraint. Gold is the only accent color. Multiple dark values create subtle depth. White text commands attention on dark backgrounds. Accent bars create systematic visual rhythm.

### Core Backgrounds

- #111111 — Page Background (deep charcoal)
- #1C1C1C — Card Surface
- #282828 — Elevated Surface (subtle elevation)

### Text Colors

- #FFFFFF — Text Primary (white)
- #A0A0A0 — Text Secondary (descriptions)
- #666666 — Text Muted (labels, meta)

### Border Colors

- #2A2A2A — Border Default; card boundaries, dividers
- #3A3A3A — Border Strong; form controls, emphasis

### Accent Colors

- #D4AF37 — Gold Primary; active states, accent bars, CTAs
- #D4AF3720 — Soft Gold (20% opacity tint)
- #4CAF50 — Status Positive; success states
- #F44336 — Status Negative; error states

---

## Typography

Single-font system using Space Grotesk throughout. Bold 700 for headlines and values, medium 500 for labels and content, normal 400 for body. ALL-CAPS is the dominant text treatment for labels, navigation, and actions.

### Font Families

- **Space Grotesk** — All text: headlines, labels, body, navigation, badges (geometric grotesque sans-serif)

### Type Scale

- **42px** — Large Title. Space Grotesk, bold 700, letterSpacing: -1, lineHeight: 0.95, UPPERCASE
- **36px** — Metric Value. Space Grotesk, bold 700, letterSpacing: -2
- **28px** — Featured Stat. Space Grotesk, bold 700
- **18px** — Card Title. Space Grotesk, bold 700, lineHeight: 1.1, UPPERCASE
- **13px** — Headline, Body. Space Grotesk, medium 500
- **12px** — Callout. Space Grotesk, normal
- **11px** — Section Label. Space Grotesk, semibold 600, letterSpacing: 1–2px, UPPERCASE
- **10px** — Card Label. Space Grotesk, medium 500, letterSpacing: 1–1.5px, UPPERCASE
- **9px** — Tab Label. Space Grotesk, medium 500–600, letterSpacing: 0.5, UPPERCASE

### Font Weights

- **700** — Bold. Headlines, metric values, emphasis
- **600** — Semibold. Section labels
- **500** — Medium. Labels, content, tab labels
- **400** — Normal. Descriptions, body text

### Letter Spacing

- **-1px to -2px** — Display headlines, large metric values
- **+1–2px** — Section labels, UPPERCASE markers
- **+1–1.5px** — Card labels (STEPS, SLEEP)
- **+0.5px** — Tab bar labels
- **0** — Default; body text

### Line Height

- **0.95** — Tight; large display headlines
- **1.1** — Comfortable; program card titles
- **auto** — Default; most elements

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section gaps
- **18px** — Large; row internal, schedule cards
- **16px** — Standard; section header to content
- **14px** — Empty state internal
- **12px** — Medium; accent bar to label, cards within sections
- **10px** — Day column internal
- **8px** — Week chart bars, small groups
- **6px** — Status indicators
- **4px** — Label pairs, icon + label
- **2px** — Tight stacks (stat parts)

### Padding Scale

- **[0, 28]** — Content wrapper (horizontal)
- **[32, 24]** — Empty state card
- **[24, 20]** — Metric cards
- **[24, 18]** — Program cards
- **[24, 16]** — Week chart
- **[18, 18]** — Habit rows, accordion items, schedule cards
- **[12, 21, 21, 21]** — Tab bar container
- **[4, 5]** — Tab bar pill internal

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **28px** — Content Padding (horizontal, generous)
- **32px** — Section Gap (vertical, dramatic)
- **12px** — Card Gap (within sections)
- **165px** — Program Card Width (fixed)

---

## Corner Radius

Zero corner radius is the core brutalist principle. Sharp corners create architectural, uncompromising forms. The only exception is the floating pill tab bar, which uses generous radius to float distinctly from the sharp-edged content.

- **0px** — ALL content (cards, containers, inputs, checkboxes, chart bars, segments)
- **36px** — Tab bar container (full pill)
- **26px** — Tab bar items (rounded pill)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, check-square, bar-chart, user (tab bar, with UPPERCASE labels)
- **Actions:** search, bell, plus, chevron-down, chevron-right

### Icon Sizes

- **18px** — Navigation (tab bar), notification, search
- **14px** — Add button
- **12px** — Checkmarks
- **22px** — Empty state

### Icon Color States

- #111111 — Active navigation (dark on gold)
- #666666 — Inactive navigation (muted)
- #FFFFFF — Notification bell (white), on dark backgrounds
- #000000 — On gold backgrounds
