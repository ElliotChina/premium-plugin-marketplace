# Use the following style guide in the current design task

## Name of the styleguide: `mobile-02-swissexpressive_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Swiss Expressive Mobile Dashboard — Style Guide

---

## Style Summary

### Description

Dramatic dark-canvas mobile interface commanding attention through typographic boldness. Sora at bold 700 weight delivers punchy, confident headlines with tight negative letter-spacing while Inter handles crisp functional communication. The design embraces deep black (#0C0C0C) as primary background with elevated dark surfaces (#1A1A1A) creating subtle layered depth. Signature red accent (#FF3B30) provides electric emphasis for active states and section markers. Horizontal red accent lines (24x2px) precede uppercase labels for systematic visual rhythm. Square-ish corners (4–12px) maintain geometric precision. Progress bars use rectangular forms with sharp edges. Suited for fitness apps, productivity tools, and technical dashboards targeting users who appreciate bold confidence and dark-mode functionality.

### Key Aesthetics

- **Swiss Systematization:** Uppercase labels with wide letter-spacing, horizontal accent lines, structured hierarchy.
- **Typographic Power:** Sora bold 700 for commanding headlines with tight negative letter-spacing (-1.5 to -2px).
- **Dark Confidence:** Deep black layering (#0C0C0C → #1A1A1A → #242424) creates depth without shadows.
- **Electric Red Accent:** #FF3B30 for striking emphasis—accent lines, active states, and CTAs.
- **Geometric Clarity:** Restrained 4–12px corner radii, square-ish checkboxes (4px), rectangular progress bars.
- **Dual-Font System:** Sora for commanding display layer, Inter for crisp functional text.

### Tags

`mobile` · `dark-mode` · `swiss` · `bold` · `expressive` · `geometric` · `technical` · `high-contrast` · `typographic` · `modern`

---

## Color System

Color creates dramatic contrast on the dark canvas. Deep black backgrounds provide visual rest. Layered surfaces create subtle depth hierarchy. Red accent delivers electric, energetic emphasis. White text commands attention.

### Core Backgrounds

- #0C0C0C — Page Background (deep black)
- #1A1A1A — Card Surface
- #242424 — Elevated Surface

### Text Colors

- #FFFFFF — Text Primary (white)
- #8A8A8A — Text Secondary (descriptions)
- #525252 — Text Muted (labels, meta)

### Border Colors

- #2A2A2A — Border Default; card boundaries, dividers
- #3A3A3A — Border Strong; form controls, emphasis

### Accent Colors

- #FF3B30 — Red Primary; active states, accent lines, CTAs
- #FF3B3020 — Soft Red (20% opacity tint)
- #32D74B — Status Positive; success states
- #FF453A — Status Negative; error states

---

## Typography

The dual-font system creates deliberate contrast—Sora handles the commanding display layer (headlines, large values, program titles), Inter handles the precise functional layer (body text, labels, navigation). Bold 700 on Sora provides impact; various weights on Inter create hierarchy.

### Font Families

- **Sora** — Headlines, metric values, card titles, program titles, schedule times (geometric sans-serif)
- **Inter** — Body text, labels, badges, navigation, descriptions (neo-grotesque sans-serif)

### Type Scale

- **38px** — Large Title. Sora, bold 700, letterSpacing: -1.5, lineHeight: 1.0
- **36px** — Metric Value. Sora, bold 700, letterSpacing: -2
- **24px** — Featured Stat. Sora, bold 700
- **22px** — Card Title. Sora, bold 700, letterSpacing: -0.5
- **16px** — Schedule Time. Sora, bold 700
- **14px** — Headline, Body. Inter, medium 500 / normal
- **13px** — Callout, Segment Label. Inter, medium 500 / semibold 600
- **12px** — Subhead, Action. Inter, medium 500
- **11px** — Section Label. Inter, bold 700, letterSpacing: 2, UPPERCASE
- **10px** — Tab Label. Inter, medium 500–600
- **9px** — Micro Label, Badge. Inter, bold 700, letterSpacing: 1, UPPERCASE

### Font Weights

- **700** — Bold. Sora headlines, section labels
- **600** — Semibold. Active states, buttons
- **500** — Medium. Labels, emphasis
- **400** — Normal. Body text, descriptions

### Letter Spacing

- **-1.5px to -2px** — Large display titles
- **-0.5px** — Card titles, program headers
- **+1–2px** — Uppercase section labels (THIS WEEK, HABITS)
- **0** — Default; body text

### Line Height

- **1.0** — Tight; large display headlines
- **1.1** — Comfortable; program card titles
- **auto** — Default; most elements

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section gaps
- **20px** — Program card internal
- **16px** — Standard; section header to content, card padding
- **14px** — Row content spacing
- **12px** — Section header accent line to label
- **8px** — Week chart bars, small groups
- **6px** — Icon + label pairs
- **4px** — Label pairs, status indicators
- **2px** — Tight stacks (title + description)

### Padding Scale

- **[0, 24]** — Content wrapper (horizontal)
- **[32, 32]** — Empty state card
- **[20, 20]** — Metric cards, program cards
- **[16, 16]** — Habit rows, card padding
- **[16, 0, 34, 0]** — Tab bar (includes safe area)
- **[8, 12]** — Action buttons
- **[6, 10]** — Progress badges
- **[4, 8]** — Small badges

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **24px** — Content Padding (horizontal)
- **32px** — Section Gap (vertical, generous)
- **12px** — Card Gap (within sections)
- **180px** — Program Card Width (fixed)

---

## Corner Radius

Corner radius is deliberately restrained for geometric precision. 12px for cards maintains modern softness while 4px checkboxes and chart bars preserve Swiss sharpness.

- **12px** — Cards, major containers
- **8px** — Search bar, segmented control container, notification button
- **6px** — Action buttons
- **4px** — Checkboxes, badges, chart bars, segmented control items
- **2px** — Accent bars (schedule cards)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, check-square, bar-chart, user (with labels)
- **Actions:** search, bell, plus, chevron-down, chevron-right

### Icon Sizes

- **22px** — Navigation (tab bar), empty state
- **18px** — Notification, search, chevrons
- **14px** — Action buttons
- **12px** — Checkmarks

### Icon Color States

- #FF3B30 — Active navigation (red)
- #525252 — Inactive navigation (muted)
- #32D74B — Positive status (green)
- #FFFFFF — On accent backgrounds, default on dark