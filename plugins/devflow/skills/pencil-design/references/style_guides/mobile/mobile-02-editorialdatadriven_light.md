# Use the following style guide in the current design task

## Name of the styleguide: `mobile-02-editorialdatadriven_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Editorial Data-Driven Mobile Dashboard — Style Guide

---

## Style Summary

### Description

Refined white-canvas mobile interface channeling editorial print design. Lora serif at medium 500 weight delivers sophisticated headlines while Inter handles crisp data communication. The design embraces pure white (#FFFFFF) as primary background with clean gray borders (#E5E5E5) creating sharp, frameless card structures. Blue accent (#0066CC) provides confident emphasis for progress and actions. Rectangular forms with zero border radius maintain editorial sharpness. Numbered lists (01, 02, 03) add magazine indexing feel. Data-forward typography pairs large serif metrics with uppercase labels. Yellow highlight (#FFF3CD) marks active/in-progress states. Suited for productivity apps, analytics dashboards, and professional tools targeting users who appreciate information clarity and editorial sophistication.

### Key Aesthetics

- **Print Heritage:** Magazine-inspired layouts with numbered indices (01, 02, 03) and serif headlines.
- **Editorial Sharpness:** Zero border radius throughout for clean, newspaper-like frames.
- **Dual-Font System:** Lora serif for aspirational display layer, Inter sans-serif for functional data layer.
- **Border-Defined Structure:** 1px strokes (#E5E5E5) define all card boundaries—no shadows needed.
- **Data-Forward Layout:** Large serif metrics paired with uppercase labels and small-caps categories.
- **Yellow Highlight:** #FFF3CD marks active/in-progress items for immediate visual priority.

### Tags

`mobile` · `light-mode` · `editorial` · `magazine` · `data-driven` · `serif` · `professional` · `sharp` · `minimal` · `informational`

---

## Color System

Color is used sparingly for maximum impact. White background maintains editorial cleanliness. Blue accent provides confident, professional emphasis. Yellow highlight draws attention to active items. Borders define structure without shadow complexity.

### Core Backgrounds

- #FFFFFF — Page Background (pure white)
- #F8F8F8 — Card Surface (subtle warm gray)
- #FAF9F7 — Surface Warm (slightly warm white)
- #FFF3CD — Highlight (yellow for active states)

### Text Colors

- #111111 — Text Primary (headlines, values)
- #555555 — Text Secondary (descriptions)
- #999999 — Text Muted (labels, meta, placeholders)

### Border Colors

- #E5E5E5 — Border Default; card strokes, dividers, tab bar top
- #CCCCCC — Border Strong; form controls, emphasis

### Accent Colors

- #0066CC — Primary Blue; active states, links, progress
- #0066CC12 — Soft Blue (12% opacity tint)
- #1A8754 — Status Positive; success states
- #C41E3A — Status Negative; error states

---

## Typography

The dual-font system creates deliberate emotional separation—Lora handles the aspirational layer (headlines, metrics, section titles), Inter handles the functional layer (body text, labels, UI elements). Medium weight on Lora maintains refined appearance; various weights on Inter create interface hierarchy.

### Font Families

- **Lora** — Headlines, section headers, metric values, program titles (elegant serif)
- **Inter** — Body text, labels, badges, navigation, descriptions (neo-grotesque sans-serif)

### Type Scale

- **40px** — Large Title. Lora, medium 500, letterSpacing: -0.5, lineHeight: 1.0
- **34px** — Metric Value. Lora, medium 500, letterSpacing: -1
- **24px** — Featured Stat. Lora, medium 500
- **16px** — Section Header. Lora, medium 500
- **14px** — Headline, Body. Inter, normal
- **12px** — Callout, Action. Inter, medium 500
- **11px** — Footnote. Inter, normal
- **10px** — Caption, Label. Inter, semibold 600, letterSpacing: 1–2px, UPPERCASE
- **9px** — Micro Stats. Inter, medium 500

### Font Weights

- **700** — Bold. Active tab labels
- **600** — Semibold. Uppercase labels, active states
- **500** — Medium. Lora headlines, emphasized labels
- **400** — Normal. Body text, descriptions

### Letter Spacing

- **-0.5px to -1px** — Large display values (tight)
- **+1–2px** — Uppercase labels (STEPS, HABITS)
- **0** — Default; body text, section headers

### Line Height

- **1.0** — Tight; large display headlines
- **1.15** — Standard; program card titles
- **auto** — Default; most elements

---

## Spacing System

### Gap Scale (between elements)

- **24px** — Major; section gaps
- **16px** — Standard; content rows, schedule cards
- **14px** — Section; header to content
- **12px** — Medium; cards within sections, horizontal scroll
- **8px** — Section titles with line markers
- **6px** — Status indicators
- **4px** — Label groups (caption + label)
- **2px** — Tight stacks (within content rows)

### Padding Scale

- **[0, 24]** — Content wrapper (horizontal)
- **[20, 16]** — Metric cards
- **[20, 12]** — Week chart
- **[16, 14]** — Program cards
- **[14, 14]** — Habit rows, accordion items
- **[16, 0, 34, 0]** — Tab bar (includes safe area)

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **24px** — Content Padding (horizontal)
- **24px** — Section Gap (vertical)
- **12px** — Card Gap (within sections)
- **160px** — Program Card Width (fixed)

---

## Corner Radius

Zero border radius is a core design decision. Sharp corners evoke print design, newspaper columns, and editorial layouts. This creates a sophisticated, professional aesthetic that prioritizes information density and clean geometric structure.

- **0px** — ALL elements (cards, containers, buttons, inputs, checkboxes, tab bar)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, check-square, bar-chart, user (with labels)
- **Actions:** bell, search, plus, chevron-down, chevron-right

### Icon Sizes

- **22px** — Navigation (tab bar)
- **18px** — Notification, search
- **16px** — Chevrons
- **14px** — Trend indicators
- **12px** — Checkmarks, small icons

### Icon Color States

- #111111 — Active navigation (black)
- #999999 — Inactive navigation, search, chevrons (muted)
- #1A8754 — Positive status (green)
- #C41E3A — Negative status (red)
- #FFFFFF — On accent backgrounds
