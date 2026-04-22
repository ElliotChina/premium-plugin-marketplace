# Use the following style guide in the current design task

## Name of the styleguide: `webapp-03-terminaltechnicalcrisp_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Terminal Technical Crisp Dashboard — Style Guide

---

## Style Summary

### Description

A pure terminal-native dashboard embracing command-line culture throughout. The design uses JetBrains Mono exclusively — every single element speaks in monospace. A bright green accent (#00D084) evokes terminal success states against a clean light gray canvas with white section cards. Code conventions permeate the UI: bracket-wrapped status badges [ACTIVE], comment-style descriptions "// features", terminal commands "$ export --csv", ISO timestamps, and underscore_case labels. The horizontal black header bar anchors the interface, while zero corner radius throughout maintains the sharp, technical precision of a code editor.

### Key Aesthetics

- **Monospace Purity:** JetBrains Mono is the only typeface, creating total code-editor immersion across every UI element.
- **Terminal Vocabulary:** UI speaks in code conventions — bracket badges [OK], comment syntax // descriptions, shell commands $ export, underscore_case labels.
- **Green Signal Color:** #00D084 accent evokes classic terminal "success" green; the single accent carries all emphasis in the grayscale foundation.
- **Horizontal Authority:** Black top navigation bar (#000000) anchors the hierarchy with prompt symbol logo (">") in green.
- **Clinical Clarity:** Light gray background (#F5F5F5) with white cards for maximum readability and clean content separation.
- **Zero Decoration:** No shadows, no rounded corners, no gradients, no icon fonts — pure functional geometry with text-based characters.

### Tags

`terminal` · `monospace` · `developer` · `webapp` · `technical` · `green-accent` · `code-native` · `command-line` · `flat` · `crisp`

---

## Color System

The design operates with a disciplined grayscale foundation where the single accent color (green) carries all emphasis. Green means "go", "success", "active" — just as it does in command-line environments. Semantic colors extend the terminal metaphor with red for errors and yellow for warnings.

### Core Backgrounds

- #F5F5F5 — Page Background (light gray canvas for content separation)
- #FFFFFF — Card/Section Fill (white for primary content areas)
- #000000 — Header Background (pure black top navigation bar)

### Text Colors

- #000000 — Text Primary (headers, buttons, primary text, active pagination)
- #777777 — Text Secondary (navigation inactive, metric labels, secondary text)
- #888888 — Text Tertiary (descriptions, timestamps, metadata, table headers)
- #CCCCCC — Placeholder (disabled content)

### Accent Colors

- #00D084 — Green Primary; logo prompt, active states, positive indicators, chart bars
- #00AF6F — Green Success; positive change values, success badges
- #FF4444 — Negative/Error; decline, warning, error states
- #FFB800 — Warning/Alert; system alerts, caution states
- #F0F0F0 — Border Light; row dividers, list separators
- #E0E0E0 — Border Medium; card borders, gallery outlines, pagination inactive

---

## Typography

The single-font system creates complete code-editor immersion. Every piece of text feels like it could be typed at a command prompt. This radical simplicity differentiates sharply from consumer interfaces while resonating deeply with developer audiences.

### Font Families

- **JetBrains Mono** — Everything: logos, navigation, headings, body, data, labels (monospace, developer-familiar, highly technical)

### Type Scale

- **42px** — Page Title. JetBrains Mono, bold 700
- **36px** — Metric Value. JetBrains Mono, bold 700
- **20px** — Upgrade Title. JetBrains Mono, semibold 600
- **16px** — Logo/Brand. JetBrains Mono, bold 700 / medium 500
- **14px** — Section Title. JetBrains Mono, semibold 600
- **13px** — Body/Content. JetBrains Mono, medium 500
- **12px** — Navigation, Meta/Labels. JetBrains Mono, medium 500 active / normal 400 inactive
- **11px** — Badge/Small. JetBrains Mono, varies

### Font Weights

- **700** — Bold. Page titles, metric values, logo prompt symbol
- **600** — Semibold. Section titles, status badges, upgrade headers
- **500** — Medium. Buttons, active nav, table cells, content titles
- **400** — Normal. Descriptions, labels, metadata, inactive navigation

### Letter Spacing

- **0** — Default; all text (monospace naturally provides even spacing)

### Line Height

- **1.5** — Body text, descriptions

---

## Spacing System

### Gap Scale

- **40px** — Major; content area padding, section gaps
- **32px** — Navigation gap (horizontal nav items)
- **24px** — Section; card padding internal, metrics row gap
- **20px** — Large; list items gap, gallery cards gap, table header padding
- **16px** — Medium; metric card internal, bar chart bars gap, pagination
- **12px** — Standard; logo components, banner internal, upgrade header content
- **8px** — Small; gallery content internal, navigation dots to text
- **4px** — Tight stacks; name + timestamp in list items

### Padding Scale

- **[40, 40]** — Content area (all sides)
- **[32, 40]** — Upgrade section (promotional)
- **[24, 24]** — Metric cards, chart sections, list sections, table sections
- **[20, 20]** — Gallery card content
- **[16, 40]** — Header bar
- **[16, 0]** — List items, table rows
- **[14, 20]** — Banner/alerts
- **[12, 24]** — CTA buttons
- **[12, 0]** — Table header row
- **[10, 20]** — Buttons (primary and secondary)

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **Horizontal** — Navigation (full-width black top header bar)
- **fill_container** — Content Area (flexible)
- **40px** — Content Padding (all sides)
- **40px** — Section Gap between major sections
- **24px** — Metric Card Grid Gap (4 columns, equal width)
- **20px** — Gallery Gap (3 columns, equal width)

---

## Corner Radius

This design system enforces zero corner radius universally, creating a pure terminal/code editor aesthetic with sharp, technical precision in every element. The absence of rounding clearly differentiates from consumer "friendly" interfaces and maintains an authoritative, professional appearance.

- **0px** — All elements (no rounded corners whatsoever)

---

## Icons

### Icon Style

- **Text-based characters** using JetBrains Mono (no icon fonts or SVG icons)

### Icons Used

- **Navigation Arrows:** 14px characters (left arrow, right arrow)
- **Close/Dismiss:** [x] in monospace
- **Terminal Prompt:** > (logo symbol)
- **Command Prefix:** $ (shell commands)
- **Comment Prefix:** // (descriptions)
- **Separator:** :: (change indicators)

### Icon Sizes

- **14px** — Navigation arrows, text-based characters
- **12px** — Small characters, close dismiss
- **11px** — Badge-level characters

### Icon Color States

- #000000 — Active, on light background
- #FFFFFF — Active, on dark background
- #00D084 — Accent (terminal green)
- #888888 — Inactive, muted
