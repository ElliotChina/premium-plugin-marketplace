# Use the following style guide in the current design task

## Name of the styleguide: `mobile-01-japaneseswiss_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Japanese Swiss Mobile Dashboard — Style Guide

---

## Style Summary

### Description

An ultra-refined mobile interface that breathes through deliberate emptiness. Inter at light 300 weight for headlines creates an almost whispered elegance, while the monochromatic palette of pure black, grays, and white eliminates distraction. Section labels employ wide letter-spacing (+2px) and uppercase treatment reminiscent of Swiss editorial design. Cards float on a subtle gray canvas (#F5F5F5) without corner radii—sharp edges create sophisticated tension. Status indicators are reduced to minimal 8px dots, bar charts use hairline 4px bars. The design achieves presence through absence. Suited for mindfulness apps, productivity tools, and premium lifestyle products targeting design-conscious users who appreciate quiet sophistication.

### Key Aesthetics

- **Japanese Ma (間):** Conscious use of negative space as an active design element—generous padding (28px) and section gaps (32px).
- **Swiss Precision:** Typographic hierarchy with mathematical letter-spacing; wide-tracked uppercase section labels (+2px).
- **Monochromatic Discipline:** Pure black/white with intentional gray tones only. Color appears solely for semantic meaning (green/red).
- **Light Typography:** Inter at weight "300" for headlines and metrics—whispered elegance, not bold authority.
- **Sharp Geometry:** Zero corner radii, no shadows. Flat editorial aesthetic aligned with print design principles.
- **Hairline Elements:** Minimal indicators—8px status dots, 4px chart bars, 2px accent lines, 1px borders.

### Tags

`mobile` · `light-mode` · `minimal` · `japanese` · `swiss` · `editorial` · `monochrome` · `refined` · `quiet` · `typographic`

---

## Color System

Color is used with extreme restraint. Black and white dominate the interface. Gray tones create subtle hierarchy. Positive/negative states use standard semantic colors. No decorative color—every hue has purpose.

### Core Backgrounds

- #F5F5F5 — Page Background (subtle warm gray)
- #FFFFFF — Card Surface (pure white)

### Text Colors

- #000000 — Text Primary (pure black)
- #999999 — Text Secondary (descriptions, timestamps)
- #C4C4C4 — Text Tertiary (inactive, placeholders)
- #E5E5E5 — Text Disabled (lowest contrast)

### Border Colors

- #F5F5F5 — Border Subtle; internal dividers, row separators
- #E5E5E5 — Border Default; card strokes, form controls
- #000000 — Border Strong; active states, emphasis (2px)

### Accent Colors

- #000000 — Primary Black; active states, filled indicators
- #34A853 — Positive Green; positive metrics, success
- #D93025 — Negative Red; negative metrics, warnings

---

## Typography

A single-font system using Inter at varying weights to create all hierarchy. Light weight (300) is the signature—used for headlines and large metrics to create refined elegance. Medium weight (500) handles labels and emphasis. No serif, no decorative type—pure geometric precision.

### Font Families

- **Inter** — All text (geometric sans-serif; neutral, precise, contemporary)

### Type Scale

- **32px** — Large Title, Large Metric. Inter, light 300, letterSpacing: -1 / -2px
- **28px** — Title 1. Inter, light 300, letterSpacing: -0.5
- **22px** — Title 2. Inter, normal 400, letterSpacing: -0.3
- **18px** — Title 3, Card Title. Inter, medium 500
- **15px** — Headline, Body. Inter, normal 400
- **14px** — Callout. Inter, normal 400
- **13px** — Subhead. Inter, medium 500
- **12px** — Footnote, Segment Label. Inter, normal 400 / medium 500
- **11px** — Section Label, Meta, Delta. Inter, medium 500, letterSpacing: 2, uppercase
- **10px** — Tab Label, Day Label, Duration. Inter, medium 500, letterSpacing: 1

### Font Weights

- **300** — Light. Headlines, large metrics (signature weight)
- **400** — Normal. Body text, descriptions
- **500** — Medium. Labels, emphasis, section headers

### Letter Spacing

- **-2px** — Large metric numbers (condensed impact)
- **-1px** — Large title (subtle tightening)
- **+2px** — Section labels, uppercase (Swiss editorial style)
- **+1px** — Duration badges, small uppercase
- **0** — Default; body text

### Line Height

- **1.4** — Standard; descriptions, meta text
- **1.2** — Tight; multi-line card titles
- **auto** — Default; single-line elements

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section gaps
- **28px** — Content; wrapper padding
- **24px** — Section; metric card gaps, internal spacing
- **20px** — Large; card internal padding, schedule card gaps
- **16px** — Standard; content within rows, card gaps
- **12px** — Medium; day column spacing
- **8px** — Small; internal header content
- **4px** — Tight; icon to label
- **2px** — Minimal; title + meta stacks

### Padding Scale

- **[28, 28]** — Content wrapper (uniform)
- **[24, 20]** — Program cards
- **[24, 24]** — Week chart card
- **[20, 20]** — Card rows, accordion items, schedule cards
- **[14, 14]** — Search bar (uniform)
- **[12, 20]** — Segmented control items
- **[16, 0, 36, 0]** — Tab bar (top, sides, bottom safe area)

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **28px** — Content Padding (uniform)
- **32px** — Section Gap (vertical)
- **16px** — Card Gap (within sections)
- **200px** — Program Card Width (fixed)

---

## Corner Radius

Sharp corners are fundamental to this design language. The absence of rounded corners creates sophisticated tension and precise geometric forms aligned with Swiss design principles and Japanese architectural aesthetics. Circular elements (dots, ellipses) exist only where semantically appropriate.

- **0px** — ALL elements (cards, inputs, buttons, bar charts, containers)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, check-square, bar-chart, user (tab bar)
- **Actions:** bell, search, plus, chevron-right, chevron-down

### Icon Sizes

- **22px** — Navigation (tab bar)
- **20px** — Notification (header bell)
- **18px** — Search
- **16px** — Chevrons/Arrows
- **14px** — Action buttons

### Icon Color States

- #000000 — Active (pure black)
- #C4C4C4 — Inactive, placeholder, chevrons (gray)