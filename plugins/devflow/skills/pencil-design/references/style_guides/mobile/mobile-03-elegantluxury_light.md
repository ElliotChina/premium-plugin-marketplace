# Use the following style guide in the current design task

## Name of the styleguide: `mobile-03-elegantluxury_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Elegant Luxury Mobile — Style Guide

---

## Style Summary

### Description

A sumptuous dark-mode mobile interface that evokes the refined atmosphere of a private members' club. The design pairs Cormorant Garamond's elegant light-weight serif at 52px for display metrics with Inter's clean precision for supporting text—creating a "haute couture meets digital" aesthetic. Deep charcoal canvas (#1A1A1C) provides a rich, velvety foundation while burnished gold accents (#C9A962) and muted sage green (#6E9E6E) bring measured luxury without ostentation. Generously rounded cards (20px radius) with subtle border strokes create soft containers that feel tailored rather than technical. The pill-shaped floating tab bar with delicate gold accent echoes jewelry-like craftsmanship. Suited for premium lifestyle apps, high-end habit trackers, luxury wellness platforms, and executive productivity tools targeting users who appreciate understated elegance and refined aesthetics.

### Key Aesthetics

- **Quiet Luxury:** Cormorant Garamond light (300) for large metrics and medium (500) for titles delivers timeless sophistication; Inter provides clean functional support for all body text and UI.
- **Dark Sophistication:** Deep charcoal foundation (#1A1A1C) with lighter charcoal surfaces (#242426) creates intimate, premium atmosphere through color layering rather than shadows.
- **Burnished Gold Accent:** Muted gold (#C9A962) used with the restraint of fine jewelry—only for active states, CTAs, and featured gradient elements.
- **Generous Radii:** 20px standard on main cards, up to 34px for the tab bar pill, creating soft, luxurious forms that feel tailored rather than technical.
- **Zero Shadows:** Depth achieved through subtle 1px border strokes (#3A3A3C), color layering, and gradient backgrounds on premium elements—never through drop shadows.
- **Warm Text:** Cream off-white (#F5F5F0) instead of pure white, creating inviting contrast that feels softer and more refined.

### Tags

`mobile` · `dark-mode` · `luxury` · `elegant` · `serif` · `gold` · `premium` · `sophisticated` · `refined` · `minimal`

---

## Color System

The design achieves luxury through restraint and precision. Gold accent used sparingly—only for active states and primary actions. Most UI remains in rich charcoal tones. Warm off-white text (#F5F5F0) feels softer than pure white. Borders are extremely subtle, defining without dominating. Gradients reserved for premium featured elements only.

### Core Backgrounds

- #1A1A1C — Page Background (deep charcoal)
- #242426 — Card Surface (lighter charcoal, elevated)
- #2A2A2C — Expanded Surface; interactions, dividers

### Text Colors

- #F5F5F0 — Text Primary; headlines, primary content (warm off-white)
- #6E6E70 — Text Secondary; labels, meta info, descriptions
- #4A4A4C — Text Tertiary; muted text, inactive items
- #3A3A3C — Text Disabled; disabled states, pending items

### Border Colors

- #3A3A3C — Border Primary; card borders, notification button, tab bar
- #2A2A2C — Border Divider; internal card dividers
- #C9A962 — Border Accent; gold accents on active/featured elements

### Accent Colors

- #C9A962 — Gold Primary; active states, CTAs, badges, primary accent
- #8B7845 — Gold Deep; gradient end for featured cards
- #6E9E6E — Sage Green; positive metrics, secondary success states

### Gradients

- #C9A962 → #8B7845 — Gold Feature; premium program card gradient (135°)
- #3A3A3C → #2A2A2C — Neutral Feature; standard program card gradient (135°)
- #1A1A1C00 → #1A1A1C — Fade; tab bar gradient overlay (0°, vertical)

---

## Typography

The dual-font system creates deliberate emotional separation—Cormorant Garamond handles the aspirational layer (elegant serif for display and titles), Inter handles the functional layer (clean sans-serif for body text and UI). Light weight (300) on Cormorant for large metrics maintains refined appearance; medium (500) for titles. No bold weights on display text—luxury whispers rather than shouts.

### Font Families

- **Cormorant Garamond** — Display metrics, screen titles, card titles, list item titles, schedule times, accordion questions
- **Inter** — Body text, labels, navigation, buttons, section headers, meta info

### Type Scale

- **52px** — Large Metric. Cormorant Garamond, light 300, lineHeight: 0.85
- **42px** — Screen Title. Cormorant Garamond, normal 400, lineHeight: 1.0
- **20px** — Card Title, Program Name, Time. Cormorant Garamond, medium 500
- **18px** — List Item Title. Cormorant Garamond, medium 500
- **16px** — Accordion Title. Cormorant Garamond, medium 500
- **14px** — Section Label, Body. Inter, medium 500
- **13px** — Expanded Content, Segment Text. Inter, normal 400 / medium 500, lineHeight: 1.5–1.6
- **12px** — Description, Card Content. Inter, normal 400, lineHeight: 1.5
- **11px** — Section Header (spaced), Footnote, Meta. Inter, medium 500, letterSpacing: 3 (headers)
- **10px** — Tab Label, Badge. Inter, medium 500
- **9px** — Time Period Label. Inter, medium 500, letterSpacing: 1

### Font Weights

- **600** — Semibold. Active tab labels, current day indicators
- **500** — Medium. Titles, labels, emphasis (Cormorant + Inter)
- **400** — Normal. Body text, descriptions, display titles (Cormorant)
- **300** — Light. Large metric values (Cormorant Garamond only)

### Letter Spacing

- **+3px** — Uppercase section labels (Schedule, Help)
- **+1px** — AM/PM time period labels
- **0** — Default; all other text

### Line Height

- **0.85** — Large metric values (display, tight)
- **1.0** — Screen headlines (display titles)
- **1.5** — Card descriptions (standard)
- **1.6** — Expanded content, help text (readable)

---

## Spacing System

### Gap Scale (between elements)

- **40px** — Major; section vertical gaps
- **20px** — Section; header to content, schedule card content, program content padding
- **16px** — Standard; metric card gap, habit row horizontal, metrics row
- **14px** — Accordion; expanded content gap
- **12px** — Cards; schedule cards gap
- **10px** — Week; day column internal gap
- **8px** — Small; program card content gap
- **4px** — Tight; tab item internal (icon to label), content title/meta gap

### Padding Scale

- **[0, 28, 28, 28]** — Content wrapper (top, horizontal, bottom)
- **28px** — Week card internal padding
- **24px** — Metric cards (uniform)
- **[20, 24]** — Habit rows (vertical, horizontal)
- **[18, 24]** — Accordion items
- **[18, 20]** — Schedule card content
- **20px** — Program card content
- **[8, 16]** — Tab items, add button
- **[6, 12]** — Badge padding
- **4px** — Segmented control internal, tab bar internal

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **874px** — Minimum Screen Height
- **28px** — Content Padding (horizontal)
- **40px** — Section Gap (vertical)
- **20px** — Internal Section Gap
- **12–16px** — Card Gap (within sections)
- **200px** — Program Card Width (horizontal scroll)

---

## Corner Radius

Corner radii are generous throughout, creating soft, luxurious forms. The consistent use of 20px on main containers establishes a harmonious rhythm. The standout 34px tab bar radius creates a jewelry-like pill that anchors the navigation with distinctive elegance.

- **12px** — Status indicators (nearly circular at 24x24)
- **16px** — Schedule cards
- **18px** — Week day circles (fully circular at 36x36)
- **20px** — Main cards, program cards, segmented control items, badges, add button
- **22px** — Notification button (nearly circular)
- **24px** — Segmented control container
- **26px** — Search bar (large pill)
- **34px** — Tab bar pill

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, bar-chart, compass, user (tab bar)
- **Actions:** search, bell, plus, chevron-right, chevron-down
- **Status:** check (completion indicator)

### Icon Sizes

- **22px** — Navigation (tab bar)
- **20px** — Notification bell
- **18px** — Search, chevrons
- **14–16px** — Checkmarks
- **14px** — Add button icon

### Icon Color States

- #C9A962 — Active (navigation, expanded chevron, gold)
- #6E6E70 — Inactive (navigation, search placeholder)
- #4A4A4C — Tertiary (collapsed chevron)
- #1A1A1C — On Gold Backgrounds (dark)
