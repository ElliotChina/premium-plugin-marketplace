# Use the following style guide in the current design task

## Name of the styleguide: `mobile-01-swissexpressive_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Swiss Expressive Mobile Dashboard — Style Guide

---

## Style Summary

### Description

A high-contrast light canvas mobile interface that harmonizes Swiss design precision with expressive typography. Outfit at extra-bold 800 weight delivers commanding headlines with tight letter-spacing while JetBrains Mono provides technical precision for labels and data. The design embraces sharp black borders (2px), square checkboxes, and rectangular day indicators that reject softness in favor of confident geometry. Primary blue (#0066FF) serves as the action color, complemented by signal red (#FF3300) and success green (#00AA55). White cards pop against a cool off-white foundation (#FAFAFA) with bold black strokes creating structural definition. Section headers use uppercase monospace labels with decorative horizontal lines. A floating pill tab bar provides playful contrast to the angular content. Suited for productivity apps, fitness trackers, and task management tools targeting users who appreciate bold confidence and systematic organization.

### Key Aesthetics

- **Swiss Rationalism:** Grid-based thinking with systematic organization; uppercase monospace labels (+3px tracking) with decorative horizontal rules.
- **Bold Expression:** Outfit at extra-bold 800 weight for commanding headlines with tight negative letter-spacing.
- **Technical Precision:** JetBrains Mono monospace for all labels, meta text, and data—systematic credibility.
- **Black Border Structure:** 2px black strokes define all cards, containers, and controls—no shadows needed.
- **Sharp Geometry:** Zero corner radii on all content elements. Square checkboxes, rectangular day indicators.
- **Floating Pill Contrast:** The rounded tab bar (200px radius) provides playful tension against angular content. Icons only, no labels.

### Tags

`mobile` · `light-mode` · `swiss` · `bold` · `high-contrast` · `geometric` · `monospace` · `expressive` · `precise` · `floating-nav`

---

## Color System

Color creates impact through high contrast and restraint. Black borders define all structural elements. Blue indicates active/in-progress states. Red provides urgent emphasis. Green signals completion. Most UI remains in stark black/white contrast.

### Core Backgrounds

- #FAFAFA — Page Background (cool off-white)
- #FFFFFF — Card Surface (white)
- #F5F5F5 — Elevated Surface (light gray for tab bar)

### Text Colors

- #0A0A0A — Text Primary (near-black)
- #666666 — Text Secondary (descriptions)
- #888888 — Text Tertiary (labels, meta)
- #AAAAAA — Text Muted (inactive states)
- #CCCCCC — Text Disabled (empty states)

### Border Colors

- #0A0A0A — Border Primary; 2px black strokes on cards and controls
- #E5E5E5 — Border Subtle; dividers, list separators, tab bar stroke
- #E0E0E0 — Border Inactive; empty day indicator strokes

### Accent Colors

- #0066FF — Primary Blue; actions, in-progress, links
- #FF3300 — Signal Red; warnings, negative metrics
- #00AA55 — Success Green; completed states, positive metrics
- #8A8A8A — Tab Inactive (muted gray)
- #FFFFFF — Text On Dark (white on black/blue/green backgrounds)

---

## Typography

The dual-font system creates the Swiss x Expressive tension—Outfit handles the commanding display layer (headlines, titles, body), JetBrains Mono handles the systematic technical layer (labels, meta, data). Extra-bold weight and tight negative spacing on headlines create confident impact.

### Font Families

- **Outfit** — Headlines, page titles, body text, program titles, accordion content (geometric sans-serif)
- **JetBrains Mono** — Section labels, meta text, badges, status text, schedule times/meta, buttons (monospace)

### Type Scale

- **44px** — Metric Value. Outfit, extra-bold 800, letterSpacing: -2
- **42px** — Large Title. Outfit, extra-bold 800, letterSpacing: -2, lineHeight: 0.95
- **32px** — Title 1. Outfit, extra-bold 800, letterSpacing: -1.5
- **22px** — Program Title. Outfit, extra-bold 800, letterSpacing: -1, lineHeight: 1.0
- **18px** — Subsection. Outfit, bold 700, letterSpacing: -0.5
- **15px** — Headline, Body. Outfit, semibold 600 / normal
- **14px** — Callout, Segment Label, Accordion Content. Outfit, medium 500 / normal, lineHeight: 1.5
- **13px** — Subhead. Outfit, normal
- **14px** — Schedule Time. JetBrains Mono, bold 700
- **12px** — Status Text. JetBrains Mono, semibold 600
- **11px** — Section Label, Meta, Button. JetBrains Mono, semibold 600, letterSpacing: 3 / +0.3px / +1px, uppercase
- **10px** — Badge, Schedule Meta. JetBrains Mono, semibold 600 / medium 500, letterSpacing: 2 / +1px, uppercase

### Font Weights

- **800** — Extra Bold. Display headlines, metric values (Outfit)
- **700** — Bold. Subsections, schedule times
- **600** — Semibold. List titles, mono labels, status text
- **500** — Medium. Callouts, inactive segments, schedule meta
- **400** — Normal. Body text, descriptions

### Letter Spacing

- **-2px** — Large titles, metric values (very tight)
- **-1.5px** — Title 1
- **-1px** — Program titles
- **+3px** — Section labels (wide, uppercase)
- **+2px** — Badges (wide, uppercase)
- **+1px** — Schedule meta, buttons
- **+0.3px** — Mono descriptions (slightly wide)
- **0** — Default; body text

### Line Height

- **1.5** — Readable; paragraph content, accordion answers
- **1.0** — Tight; multi-line program titles
- **0.95** — Compact; display headlines
- **auto** — Default; most elements

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section gaps
- **20px** — Large; search to content
- **16px** — Standard; section header to content, row content gaps
- **12px** — Medium; cards within sections, program internal
- **8px** — Standard; day label to indicator
- **6px** — Small; status icon to text
- **2px** — Minimal; title + description stacks

### Padding Scale

- **[20, 20]** — Content wrapper, program cards
- **[20, 16]** — Metric cards
- **[16, 16]** — List rows, schedule content, accordion
- **[8, 12]** — Add button
- **[4, 4]** — Tab bar pill internal
- **[12, 21, 21, 21]** — Tab bar container

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **20px** — Content Padding (all around)
- **32px** — Section Gap (vertical)
- **12px** — Card Gap (within sections)
- **200px** — Program Card Width (fixed)

---

## Corner Radius

Sharp corners are the signature of this design system. The geometric precision of square/rectangular shapes creates a systematic, confident visual language. The only exception is the floating pill tab bar, which provides playful contrast.

- **0px** — ALL content (cards, checkboxes, day indicators, segments, accordions)
- **200px** — Tab bar pill (fully rounded, contrast element)
- **100px** — Tab item active state (circular background)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, search, calendar, bar-chart, user (icons only in pill tab bar)
- **Actions:** bell, search, plus, chevron-down, chevron-right

### Icon Sizes

- **22px** — Navigation (tab bar icons)
- **20px** — Notification, Chevrons
- **18px** — Search, Checkmarks
- **14px** — Action buttons, trend indicators

### Icon Color States

- #FFFFFF — Active navigation (on black circular background)
- #8A8A8A — Inactive navigation (muted gray)
- #0A0A0A — Search, chevrons (primary black)
- #FFFFFF — On dark/blue/green backgrounds (white)
