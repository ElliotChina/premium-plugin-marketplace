# Use the following style guide in the current design task

## Name of the styleguide: `mobile-03-terminalminimal_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Terminal Minimal Mobile — Style Guide

---

## Style Summary

### Description

Dark terminal-inspired mobile interface where JetBrains Mono monospace typography meets refined minimalism. The design embraces a deep navy canvas (#0A0F1C) with slate blue card surfaces (#1E293B), creating a sophisticated developer aesthetic. Electric cyan (#22D3EE) serves as the singular accent color, marking active states, progress, and interactive elements with bright clarity against the darkness. Uppercase labels with generous letter-spacing evoke command-line headers, while Inter provides clean readability for content. Status indicators use terminal characters (✓ ◐ ○) rather than graphical icons, reinforcing the code-editor feel. Horizontal progress bars visualize week data with minimal height. The floating pill tab bar anchors navigation with full-width presence. Suited for productivity apps, developer tools, and habit trackers targeting users who appreciate technical aesthetics and focused dark environments.

### Key Aesthetics

- **Terminal Heritage:** Monospace JetBrains Mono for values and status, terminal characters (✓ ◐ ○) instead of graphical icons, command-line style uppercase labels.
- **Deep Slate Canvas:** #0A0F1C background with #1E293B card surfaces creates focused dark environment; depth through layered fills, never shadows.
- **Singular Cyan Accent:** #22D3EE marks everything active, positive, or interactive—no semantic color variations, just intensity control.
- **Compact Radii:** 6–12px for a technical, precise feel; 100px reserved exclusively for the floating pill tab bar.
- **Horizontal Progress Bars:** Week progress visualized as minimal-height horizontal bars, not circles or vertical columns.
- **Inverted Expanded States:** Accordion expanded items use solid cyan fills with inverted dark text for dramatic moments.

### Tags

`mobile` · `dark-mode` · `terminal` · `monospace` · `minimal` · `developer` · `tech` · `cyan-accent` · `slate` · `modern`

---

## Color System

This design uses a single accent color (cyan) for all emphasis. Deep slate backgrounds create depth without complexity. White text on slate provides excellent dark-mode readability. No semantic colors (red/green)—all status communicated through cyan intensity and typography.

### Core Backgrounds

- #0A0F1C — Page Background (deep navy/slate)
- #1E293B — Card Surface (slate 800, elevated containers)
- #0F172A — Inset Surface (slate 900, nested/darker elements)
- #22D3EE — Accent Surface; highlighted cards/expanded states (cyan)

### Text Colors

- #FFFFFF — Text Primary; headlines, primary content (pure white)
- #94A3B8 — Text Secondary; descriptions, notification icons (slate 400)
- #64748B — Text Tertiary; labels, section headers (slate 500)
- #475569 — Text Muted; placeholders, inactive (slate 600)
- #0A0F1C — Text Inverted; dark text on cyan backgrounds

### Border Colors

- #0F172A — Divider; subtle separators (slate 900)

### Accent Colors

- #22D3EE — Cyan; all active states, progress, CTAs, interactive elements (cyan 400)

---

## Typography

JetBrains Mono serves as the data/display typeface—a monospace font that brings technical precision to metrics, values, and status text. Inter handles all readable content and titles with neutral professionalism. The design relies on font-family contrast (monospace vs sans-serif) and weight variation for hierarchy.

### Font Families

- **JetBrains Mono** — Hero metrics, data values, day labels, schedule times, badges, tab labels, status characters, meta info
- **Inter** — Screen titles, section labels, card titles, habit titles, body text, descriptions, help content

### Type Scale

- **32px** — Hero Metric. JetBrains Mono, bold 700
- **24px** — Screen Header, Large Metric. Inter semibold 600 / JetBrains Mono bold 700
- **20px** — Section Percentage. JetBrains Mono, bold 700
- **15px** — Card Title. Inter, semibold 600
- **14px** — List Title, Schedule Time. Inter medium 500 / JetBrains Mono semibold 600
- **13px** — Search Placeholder, Help Content. Inter normal 400 / JetBrains Mono normal 400
- **12px** — Meta Text, Links, Changes. JetBrains Mono, medium 500 / Inter normal 400, lineHeight: 1.4
- **11px** — Section Label, Day Label, Badge. Inter semibold 600 / JetBrains Mono semibold 600–bold 700
- **10px** — Tab Label. JetBrains Mono, medium 500 / semibold 600

### Font Weights

- **700** — Bold. Hero metrics, active values, badges
- **600** — Semibold. Section headers, times, active tabs
- **500** — Medium. Labels, supporting text, inactive tabs
- **400** — Normal. Body text, meta info, descriptions

### Letter Spacing

- **+2px** — Uppercase section labels ("STREAK", "HABITS", "SCHEDULE")
- **+1.5px** — Alternate labels ("POINTS", "COMPLETION")
- **0** — Default; all other text

### Line Height

- **1.4** — Card descriptions, meta text
- **1.5** — Expanded help content

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section vertical gaps
- **16px** — Standard; schedule card internal gaps
- **12px** — Medium; section header to content, day row gaps, list gaps
- **8px** — Small; metric card internal, schedule card gaps
- **6px** — Tight; card title to description
- **4px** — Micro; icon to label (tab bar), segment gaps
- **2px** — Minimal; title + meta within habit rows

### Padding Scale

- **[0, 24, 24, 24]** — Content wrapper (top, horizontal, bottom)
- **[20, 20]** — Metric cards
- **[16, 16]** — Schedule cards, help items, week card, program content
- **[14, 16]** — Habit rows
- **[12, 21, 21, 21]** — Tab bar section (includes gradient fade)
- **[12, 16]** — Program card headers
- **[8, 16]** — Tab bar items
- **[8, 12]** — Add button
- **4px** — Segmented control container, tab bar pill, habits list container

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **874px** — Minimum Screen Height
- **24px** — Content Padding (horizontal)
- **32px** — Section Gap (vertical)
- **12px** — Header-to-Content Gap, Card Gap (within sections)
- **180px** — Program Card Width (horizontal scroll)

---

## Corner Radius

Corner radii are deliberately compact to maintain a technical, precise aesthetic. Most UI elements use 8–12px for a clean but not overly soft appearance. The largest radius (100px) is reserved for the floating tab bar pill, creating clear distinction between navigation and content.

- **3px** — Progress bars, day bars (technical precision)
- **4px** — Hero progress bar
- **6px** — Segmented items, small buttons
- **8px** — Habit rows, search bar, notification button, segmented control container
- **12px** — Cards, containers, help section
- **100px** — Tab bar pill

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, bar-chart, compass, user (tab bar)
- **Actions:** search, bell, plus, chevron-right, chevron-down
- **Status:** Terminal characters ✓ (complete), ◐ (in progress), ○ (pending)

### Icon Sizes

- **22px** — Navigation (tab bar)
- **18px** — Notification bell, search, chevrons
- **16px** — Program icons
- **14px** — Add button icon

### Icon Color States

- #22D3EE — Active (navigation, cyan)
- #475569 — Inactive (navigation, search placeholder, slate 600)
- #94A3B8 — Notification (slate 400)
- #0A0F1C — On Cyan Backgrounds (page background dark)
