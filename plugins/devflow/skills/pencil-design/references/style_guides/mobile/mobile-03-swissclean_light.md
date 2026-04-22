# Use the following style guide in the current design task

## Name of the styleguide: `mobile-03-swissclean_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Swiss Clean Mobile — Style Guide

---

## Style Summary

### Description

Pure white canvas mobile interface that embodies Swiss design clarity and rationalism. Inter typeface delivers neutral, highly readable text across all sizes while stroke-based containers (#E4E4E7, 1.5px) create clean boundaries without visual weight. The design embraces a single blue accent (#2563EB) for all interactive and active states, creating instant recognition and clear hierarchy. Cards and containers are defined by their borders rather than fills or shadows, achieving maximum lightness and visual breathing room. Circular day indicators and rounded status badges provide friendly geometry without compromising the systematic approach. Suited for productivity apps, task managers, analytics tools, and business applications targeting users who appreciate precision, clarity, and functional minimalism.

### Key Aesthetics

- **Swiss Rationalism:** Grid-based thinking, neutral Inter typography, and functional elegance—every element serves information hierarchy.
- **Stroke Definition:** All containers defined by 1.5px borders (#E4E4E7), not fills or shadows—maximum visual lightness.
- **Single Blue Accent:** #2563EB handles all interactive/active states; no secondary accent colors for absolute clarity.
- **No Shadows:** Depth achieved through stroke borders, color shifts (#EFF6FF for active states), and divider lines—never shadows.
- **Circular Week View:** Round indicators (32px circles) for day-of-week progress display.
- **Uppercase Labels:** Letter-spaced category labels (12px, +1px tracking) create systematic editorial rhythm.

### Tags

`mobile` · `light-mode` · `swiss` · `clean` · `minimal` · `stroke-based` · `blue-accent` · `neutral` · `professional` · `rational`

---

## Color System

Color is used sparingly for maximum impact. Blue indicates ALL interactive and active states. Stroke-defined containers eliminate need for fill colors. Gray scale creates sufficient hierarchy. No secondary accent colors. Expanded/active accordion uses light blue background.

### Core Backgrounds

- #FFFFFF — Page Background (pure white)
- transparent — Card Surface; cards have no fill, defined by stroke
- #EFF6FF — Highlight Surface; expanded/active states (blue-50)

### Text Colors

- #18181B — Text Primary; headlines, primary content (zinc-900)
- #71717A — Text Secondary; body text, descriptions (zinc-500)
- #A1A1AA — Text Tertiary; labels, placeholders, inactive (zinc-400)
- #D4D4D8 — Text Muted; disabled, scheduled items (zinc-300)
- #FFFFFF — Text On-Accent; text on blue backgrounds

### Border Colors

- #E4E4E7 — Border Default; card strokes (1.5px), dividers (1px) (zinc-200)

### Accent Colors

- #2563EB — Blue Primary; all active/interactive states (blue-600)
- #EFF6FF — Blue Light; expanded state backgrounds (blue-50)

---

## Typography

Inter serves as the sole typeface—a neutral sans-serif that ensures universal readability. The design relies on weight variation (400–700) and size contrast for hierarchy, maintaining systematic consistency across all text.

### Font Families

- **Inter** — All text: headlines, metrics, body, labels, navigation

### Type Scale

- **36px** — Large Metric. Inter, bold 700, lineHeight: 1.0
- **28px** — Screen Title. Inter, semibold 600, letterSpacing: -0.5
- **20px** — Section Header. Inter, semibold 600
- **16px** — Card Title, Program Name. Inter, semibold 600
- **15px** — List Item Title, Body. Inter, medium 500 / normal 400
- **14px** — Button, Subhead. Inter, semibold 600 / medium 500
- **13px** — Description, Meta. Inter, normal 400
- **12px** — Section Label, Day Letter. Inter, semibold 600, letterSpacing: 1 (uppercase labels)
- **11px** — Tab Label. Inter, medium 500 / semibold 600

### Font Weights

- **700** — Bold. Large metrics only
- **600** — Semibold. Headlines, buttons, active states
- **500** — Medium. Labels, subheads, inactive tabs
- **400** — Normal. Body text, descriptions

### Letter Spacing

- **-0.5px** — Screen titles (slightly tight)
- **+1px** — Uppercase section labels (expanded)
- **0** — Default; all other text

### Line Height

- **1.0** — Large metrics (compact)
- **1.4** — Card descriptions
- **1.5** — Expanded content, paragraphs

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section vertical gaps
- **16px** — Standard; section header to content, card internal
- **14px** — Row; habit row content spacing
- **12px** — Medium; cards within sections, program cards
- **8px** — Small; day columns, content blocks
- **4px** — Tight; icon to label, status rows
- **2px** — Minimal; title + meta within list items

### Padding Scale

- **[0, 24, 24, 24]** — Content wrapper (top, horizontal, bottom)
- **20px** — Metric card padding
- **16px** — Card padding (rows, smaller cards)
- **[12, 21, 21, 21]** — Tab bar section (top, sides, bottom)
- **[8, 16]** — Button padding
- **[8, 14]** — Tab item padding
- **[6, 10]** — Badge padding
- **4px** — Segmented control internal, tab bar internal

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

Corner radii are restrained and systematic. Most containers use either 12px or 16px for consistency. The pill tab bar (100px) is the only fully rounded element. Stroke-based containers benefit from moderate radii that prevent harsh corners without becoming overly soft.

- **2px** — Accent bars
- **6px** — Status indicators (squared-off rounded)
- **8px** — Segment items, badges
- **12px** — Search bar, help cards, schedule cards
- **16px** — Metric cards, habit cards, week cards, program cards, day circles
- **22px** — Notification button
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

- **22px** — Navigation (tab bar)
- **20px** — Notification bell, chevrons
- **18px** — Search
- **16px** — Day checkmarks, add button
- **14px** — Status checks, trend indicators

### Icon Color States

- #2563EB — Active (navigation, expanded chevron, blue)
- #A1A1AA — Inactive (navigation, search placeholder, zinc-400)
- #FFFFFF — On Accent Backgrounds (white)
