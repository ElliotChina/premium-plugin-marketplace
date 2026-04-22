# Use the following style guide in the current design task

## Name of the styleguide: `mobile-03-editorialdata_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Editorial Data Mobile — Style Guide

---

## Style Summary

### Description

A refined light-mode mobile interface that channels the editorial authority of premium publications combined with the technical precision of data visualization. The design pairs Newsreader's literary serif elegance at medium weight with JetBrains Mono's monospaced technical utility for labels and metrics—creating a "newspaper meets dashboard" aesthetic. Clean #FAFAFA canvas provides a calm paper-like foundation while subtle #E5E5E5 borders and teal (#0D6E6E) accents bring measured sophistication. The pill-shaped floating tab bar with soft shadow creates a modern, friendly navigation anchor. Generous whitespace and systematic section labeling with uppercase monospaced headers establish clear information hierarchy without visual noise. Suited for productivity apps, habit trackers, finance dashboards, and professional tools targeting users who appreciate intellectual depth and refined aesthetics.

### Key Aesthetics

- **Editorial Authority:** Newsreader serif for headlines and key content evokes trusted publications; JetBrains Mono for metrics, labels, and section headers brings data credibility; Inter for readable body text.
- **Uppercase Monospace Headers:** Section labels use JetBrains Mono at 11px with 2px letter-spacing in uppercase, creating systematic editorial rhythm throughout.
- **Clean Minimalism:** Restrained grayscale palette lets content breathe; most UI remains neutral with teal and orange as the only accent colors.
- **Bordered Cards:** 1px subtle strokes (#E5E5E5) define surfaces instead of shadows. Cards rely on borders for definition, creating a flatter, more editorial aesthetic.
- **Floating Pill Tab Bar:** 32px radius pill with subtle shadow (8% opacity) provides a modern navigation anchor with gradient fade from content.
- **Measured Spacing:** Generous 32px section gaps and systematic organization create clear information hierarchy without visual noise.

### Tags

`mobile` · `light-mode` · `editorial` · `data-driven` · `serif` · `monospace` · `clean` · `sophisticated` · `professional` · `minimal`

---

## Color System

The design achieves hierarchy through restraint and precision. Primary teal indicates active, completed, or positive states. Orange provides urgency contrast for in-progress items. Most UI remains in grayscale to let content breathe. Borders are extremely subtle, defining without dominating.

### Core Backgrounds

- #FAFAFA — Page Background (near-white canvas)
- #FFFFFF — Card Surface (pure white, elevated)
- #F8F8F8 — Muted Surface; expanded accordion states
- #F0F0F0 — Control Background; segmented controls, empty states

### Text Colors

- #1A1A1A — Text Primary; headlines, primary content
- #666666 — Text Secondary; body text, descriptions
- #888888 — Text Tertiary; labels, meta info, section headers
- #AAAAAA — Text Muted; inactive tabs, placeholders, disabled
- #BBBBBB — Text Disabled; inactive content
- #CCCCCC — Text Subtle; future/pending items, chevrons

### Border Colors

- #E5E5E5 — Border Primary; card strokes (1px), tab bar
- #F0F0F0 — Divider; list item dividers, internal separators
- #DDDDDD — Border Muted; pending state indicators

### Accent Colors

- #0D6E6E — Teal Primary; active states, CTAs, positive metrics, completed
- #E07B54 — Orange Secondary; in-progress states, warnings

### Shadows

- 0 2px 12px #00000008 — Tab Bar; floating pill shadow (8% opacity)
- 0 1px 2px #00000010 — Active Segment; segmented control shadow (10% opacity)

---

## Typography

The three-font system creates deliberate emotional separation—Newsreader handles the aspirational layer (literary elegance for headlines and titles), JetBrains Mono handles the data layer (metrics, section labels, timestamps), and Inter handles the functional layer (body text and UI elements). This "newspaper meets dashboard" typographic voice is the defining characteristic.

### Font Families

- **Newsreader** — Headlines, screen titles, card titles, list item titles, accordion questions
- **JetBrains Mono** — Metric values, section labels (uppercase), schedule times, badges, meta text
- **Inter** — Body text, descriptions, UI labels, navigation, buttons

### Type Scale

- **40px** — Screen Title. Newsreader, medium 500, lineHeight: 1.05
- **32px** — Large Metric. JetBrains Mono, bold 700, lineHeight: 0.85
- **28px** — Percentage Value. JetBrains Mono, bold 700
- **18px** — Card Title, Program Name. Newsreader, medium 500
- **16px** — List Item Title. Newsreader, medium 500
- **15px** — Accordion Title. Newsreader, medium 500
- **14px** — Schedule Time. JetBrains Mono, semibold 600
- **13px** — Description, Link. Inter, normal 400 / medium 500, lineHeight: 1.4–1.5
- **12px** — Metric Label, Body Content. Inter, medium 500
- **11px** — Section Header. JetBrains Mono, semibold 600, letterSpacing: 2, uppercase
- **10px** — Tab Label, Badge. Inter / JetBrains Mono, medium 500 / bold 700
- **9px** — Time Period. JetBrains Mono, medium 500 / bold 700

### Font Weights

- **700** — Bold. Large metrics, percentage values, badges
- **600** — Semibold. Section headers (mono), tab labels, time values
- **500** — Medium. Newsreader headlines, labels, interactive text
- **400** — Normal. Body text, descriptions

### Letter Spacing

- **+2px** — Section headers (uppercase monospace labels)
- **+0.5px** — Small badge text
- **-0.3px** — Large display values (optional, tight)
- **0** — Default; all other text

### Line Height

- **0.85** — Large metric numbers (tight)
- **1.05** — Display titles (headlines)
- **1.4** — Card descriptions (standard)
- **1.5** — Expanded content, help text (readable)

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section vertical gaps
- **20px** — Section; header to content gap
- **16px** — Standard; metrics row, programs scroll, schedule section
- **14px** — Row; habit row horizontal gap
- **12px** — Medium; metric card internal, accordion internal, schedule cards
- **8px** — Small; program card content, progress indicator internal
- **4px** — Tight; tab item internal (icon to label)
- **2px** — Minimal; title + meta within rows

### Padding Scale

- **[0, 24, 24, 24]** — Content wrapper (top, horizontal, bottom)
- **20px** — Metric cards, week card (uniform)
- **16px** — Row padding (habits, accordion, schedule), program card content
- **21px** — Tab bar horizontal, bottom safe area
- **12px** — Add button horizontal, tab item padding
- **8px** — Badge horizontal, add button vertical
- **4px** — Segmented control internal, badge vertical

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **874px** — Minimum Screen Height
- **24px** — Content Padding (horizontal)
- **32px** — Section Gap (vertical)
- **16–20px** — Internal Section Gap
- **12–16px** — Card Gap (within sections)
- **200px** — Program Card Width (horizontal scroll)

---

## Corner Radius

Corner radii maintain geometric precision while adding approachability. The design uses a restrained radius scale that emphasizes clean edges with soft corners. The standout exception is the 32px tab bar radius, which creates a distinctive floating pill.

- **2px** — Sparkline bars, progress bar fills
- **4px** — Badges, bar chart bars
- **6px** — Segmented control items, small buttons
- **8px** — Search bar, notification button, segmented control container, add button
- **10px** — Status indicators (habit circles)
- **12px** — Cards, schedule cards, program cards
- **32px** — Tab bar pill (full pill shape)

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
- **14px** — Add button icon
- **12px** — Checkmarks

### Icon Color States

- #0D6E6E — Active (navigation, expanded chevron)
- #AAAAAA — Inactive (navigation, search placeholder)
- #CCCCCC — Subtle (collapsed chevron)
- #FFFFFF — On Accent Backgrounds