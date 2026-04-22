# Use the following style guide in the current design task

## Name of the styleguide: `mobile-03-minimalvibrant_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Minimal Vibrant Mobile — Style Guide

---

## Style Summary

### Description

Bright white canvas mobile interface radiating friendly energy and modern playfulness. Plus Jakarta Sans at extrabold 800 weight delivers confident, rounded headlines while Inter provides clean readability throughout. The design embraces pure white (#FFFFFF) as its foundation with soft gray cards (#F4F4F5) and a vibrant purple accent (#8B5CF6) that brings joyful energy without overwhelming. Generous 24px corner radii create a distinctly soft, approachable aesthetic—everything feels pillowy and touchable. Teal (#14B8A6) and pink (#F472B6) secondary accents add playful variety. Circular day indicators, pill-shaped progress badges, and rounded buttons create cohesive geometric rhythm. Suited for wellness apps, habit trackers, and lifestyle products targeting users who appreciate bright positivity, modern softness, and interfaces that feel optimistic and approachable.

### Key Aesthetics

- **Joyful Minimalism:** Pure white canvas radiates positivity; soft gray cards (#F4F4F5) float without borders or shadows.
- **Extrabold Impact:** Plus Jakarta Sans 800 for hero metrics and confident headlines; Inter for all body text and labels.
- **Pillowy Corners:** 24px standard radius creates soft, touchable forms throughout cards, buttons, and search bars.
- **Purple Energy:** Vibrant purple (#8B5CF6) dominates as primary accent for CTAs, active states, and feature elements.
- **Colorful Variety:** Teal (#14B8A6) for positive metrics, pink (#F472B6) for highlights and schedule accents—three-color accent system.
- **Borderless Cards:** Clean separation through background color differentiation alone; no strokes on card surfaces.

### Tags

`mobile` · `light-mode` · `minimal` · `vibrant` · `playful` · `modern` · `rounded` · `purple` · `bright` · `soft`

---

## Color System

Color brings energy and joy. Purple dominates as the primary accent, appearing in CTAs, active states, and feature elements. Teal appears for positive metrics and success states. Pink adds playful highlights for schedule and special moments. Most UI remains white and soft gray for breathing room.

### Core Backgrounds

- #FFFFFF — Page Background (pure white)
- #F4F4F5 — Card Surface (soft gray)
- #E4E4E7 — Elevated Surface; expanded states, empty indicators

### Text Colors

- #18181B — Text Primary; headlines, primary content (near-black)
- #71717A — Text Secondary; meta text, descriptions
- #A1A1AA — Text Tertiary; placeholders, inactive labels
- #D4D4D8 — Text Muted; disabled states, empty day labels
- #52525B — Text Subtle; expanded content text

### Border Colors

- #D4D4D8 — Border Standard; subtle dividers
- #8B5CF6 — Border Active; active state borders (purple)
- #F472B6 — Border Accent; highlight borders (pink)

### Accent Colors

- #8B5CF6 — Purple Primary; main accent, CTAs, active states
- #8B5CF620 — Purple Soft; transparent badge backgrounds (12.5% opacity)
- #14B8A6 — Teal Success; positive metrics, success states
- #F472B6 — Pink Highlight; schedule accents, special states

### Shadows

- 0 2px 8px #00000010 — Active Segment; segmented control (6% opacity)

---

## Typography

Plus Jakarta Sans serves as the display typeface—rounded geometric with confident weight. Inter handles all body text and UI labels. The design relies on extreme weight contrast (400–800) and size variation for hierarchy. No monospace or serif fonts.

### Font Families

- **Plus Jakarta Sans** — Headlines, metrics, section titles, card titles
- **Inter** — Body text, labels, descriptions, navigation, buttons

### Type Scale

- **34px** — Screen Title / Large Metric. Plus Jakarta Sans, bold 700 / extrabold 800, lineHeight: 0.9–1.1
- **28px** — Major Section Head. Plus Jakarta Sans, bold 700
- **20px** — Section Header. Plus Jakarta Sans, bold 700
- **18px** — Medium Metric. Plus Jakarta Sans, bold 700
- **17px** — Card Title. Plus Jakarta Sans, bold 700
- **16px** — List Item Title. Inter, semibold 600
- **15px** — Body, Search Placeholder. Inter, normal 400
- **14px** — Card Label, Metric Small. Inter, semibold 600
- **13px** — Supporting Text, Progress Badge. Inter, normal 400 / semibold 600
- **12px** — Day Label, Badge. Inter, medium 500 / semibold 600
- **11px** — Tab Label. Inter, medium 500 / semibold 600

### Font Weights

- **800** — Extrabold. Large metric display values
- **700** — Bold. Headlines, section titles, time values
- **600** — Semibold. List titles, active labels, buttons
- **500** — Medium. Secondary labels, inactive tabs
- **400** — Normal. Body text, descriptions

### Letter Spacing

- **0** — Default; all text maintains natural spacing

### Line Height

- **0.9** — Large metrics (compact density)
- **1.1** — Large titles
- **1.4** — Card descriptions
- **1.5** — Expanded help content

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section vertical gaps
- **20px** — Section; header to content
- **16px** — Standard; metric cards gap, program cards gap
- **14px** — Row; status indicator to content, search bar internal
- **12px** — Medium; help content gap, schedule cards gap
- **8px** — Small; day indicator to label
- **6px** — Tight; program card content gap
- **4px** — Micro; tab item icon to label, metric bottom stack
- **2px** — Minimal; title + description within rows

### Padding Scale

- **[0, 24, 24, 24]** — Content wrapper (top, horizontal, bottom)
- **24px** — Metric cards, week card (uniform)
- **[18, 20]** — Habit rows (vertical, horizontal)
- **18px** — Help items, schedule card content
- **[20, 0, 8, 0]** — Program card content
- **[12, 21, 21, 21]** — Tab bar section (top, sides, bottom)
- **[10, 18]** — Action button
- **[8, 14]** — Tab item, program badge
- **[6, 12]** — Progress badges
- **4px** — Segmented control internal, tab bar internal

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **874px** — Minimum Screen Height
- **24px** — Content Padding (horizontal)
- **32px** — Section Gap (vertical)
- **20px** — Header-to-Content Gap
- **16px** — Card Gap (within sections)
- **200px** — Program Card Width (horizontal scroll)

---

## Corner Radius

Generous corner radii define this design language. The consistent use of 24px creates a pillowy, soft aesthetic that feels modern and approachable. Elements appear to float and breathe, never sharp or aggressive. The pill-shaped tab bar (100px) and circular day indicators provide playful contrast.

- **14px** — Status indicators, small badges
- **18px** — Day circles, schedule accent corner
- **20px** — Schedule cards, segmented items, progress badges
- **24px** — Standard cards, metric cards, buttons, search bar
- **26px** — Search bar (extra soft)
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
- **22px** — Notification bell
- **20px** — Search, chevrons
- **16–18px** — Status checks
- **16px** — Action button icons

### Icon Color States

- #8B5CF6 — Active (navigation, expanded chevron, purple)
- #A1A1AA — Inactive (navigation, search placeholder)
- #FFFFFF — On Purple Backgrounds (white)
