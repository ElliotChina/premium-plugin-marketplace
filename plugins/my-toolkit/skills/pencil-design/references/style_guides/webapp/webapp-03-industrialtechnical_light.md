# Use the following style guide in the current design task

## Name of the styleguide: `webapp-03-industrialtechnical_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Industrial Technical Dashboard — Style Guide

---

## Style Summary

### Description

A high-tech dark dashboard combining near-black backgrounds with vibrant neon green accents. The design embraces industrial terminal aesthetics—monospace typography (JetBrains Mono) dominates throughout, uppercase labels, code-like syntax patterns, and bracket-wrapped status indicators. Space Grotesk provides geometric authority for large metrics and headlines. Sharp corners, hairline borders in dark gray, and a matrix-inspired color palette create a sophisticated command center feel ideal for developer tools, monitoring dashboards, fintech platforms, and data-intensive SaaS applications.

### Key Aesthetics

- **Dark Foundation:** Near-black backgrounds (#0C0C0C, #080808, #0A0A0A) create depth, reduce eye strain, and establish an immersive command center environment.
- **Neon Green Accent:** Vibrant green (#00FF88) signals activity, success, and interactivity across the entire interface.
- **Monospace Dominance:** JetBrains Mono is used for 95% of text, reinforcing immediate technical credibility and developer-native feel.
- **Uppercase Convention:** Labels, navigation, buttons, and badges all use CAPS for industrial authority and terminal heritage.
- **Code Syntax Patterns:** Bracket status indicators [ACTIVE], comment prefixes (// SYSTEM), and underscore naming (CUSTOMER_ID) throughout.
- **Zero Decoration:** No shadows, no gradients, no rounded corners — pure terminal precision with hairline borders defining all structure.

### Tags

`industrial` · `technical` · `dark-mode` · `terminal` · `monospace` · `neon-green` · `developer` · `data-dashboard` · `matrix` · `command-center`

---

## Color System

The palette operates entirely within a dark environment — all backgrounds are variations of near-black (#080808 to #0C0C0C to #0A0A0A), with color differentiation happening through accent colors rather than background contrast. Neon green (#00FF88) signals interactivity and success, orange (#FF8800) is reserved exclusively for warnings, and hairline borders (#2f2f2f) create structure within the dark space.

### Core Backgrounds

- #0C0C0C — Page Background (main canvas, deepest dark)
- #080808 — Sidebar Background (slightly darker for depth separation)
- #0A0A0A — Card Background (component surfaces)
- #141414 — Surface Elevated (slightly lighter for nested elements)
- #1A1A1A — Surface Subtle (avatar backgrounds, image placeholders)

### Text Colors

- #FFFFFF — Text Primary (primary text on dark backgrounds)
- #8a8a8a — Text Secondary (labels, metadata, descriptions)
- #6a6a6a — Text Muted (placeholders, close icons)
- #0C0C0C — Text on Accent (text on green buttons and backgrounds)

### Accent Colors

- #00FF88 — Green Primary; active states, CTAs, success, accent bars
- #00FF8820 — Green Tint 20%; badge backgrounds, subtle highlights
- #00FF8810 — Green Tint 10%; active navigation background tint
- #00FF8840 — Green Tint 40%; promotional border accents
- #FF8800 — Orange Primary; alert labels, warning indicators
- #FF880020 — Orange Tint 20%; warning badge backgrounds
- #FF880040 — Orange Tint 40%; warning border accents
- #FF4444 — Red Error; negative values, error states, decline indicators
- #2f2f2f — Border Gray; all component borders, dividers, strokes
- #3f3f3f — Border Light; subtle borders on elevated surfaces

---

## Typography

The monospace-first approach establishes immediate technical credibility — JetBrains Mono is the workhorse covering 95% of text, while Space Grotesk is reserved for impact moments with large numbers and headlines. The uppercase convention reinforces command-line and terminal heritage throughout the interface.

### Font Families

- **JetBrains Mono** — Navigation, labels, metadata, body text, buttons, tables, badges (monospace, developer-native, industrial)
- **Space Grotesk** — Page titles, metric values, section headers (geometric, modern, authoritative)

### Type Scale

- **42px** — Page Title. Space Grotesk, bold 700, letterSpacing: -1
- **32px** — Metric Value. Space Grotesk, bold 700, letterSpacing: -1
- **18px** — Section Title. Space Grotesk, semibold 600
- **16px** — Logo Text. JetBrains Mono, semibold 600, letterSpacing: 1
- **14px** — Page Subtitle. JetBrains Mono, normal 400
- **13px** — Body, List Items, Table Cells. JetBrains Mono, medium 500
- **12px** — Navigation, Meta, Timestamps. JetBrains Mono, semibold 600 active / medium 500 inactive
- **11px** — Labels, Table Headers, Badges, Chart Labels. JetBrains Mono, medium 500 to bold 700, letterSpacing: 0.5
- **9px** — Alert Labels. JetBrains Mono, bold 700

### Font Weights

- **700** — Bold. Page titles, metric values, active navigation, button labels, badges
- **600** — Semibold. Section headers, logo, status amounts, table values
- **500** — Medium. Body text, labels, inactive navigation, meta info
- **400** — Normal. Descriptions, secondary text, timestamps

### Letter Spacing

- **-1px** — Large headings and metric values (tightened for display)
- **0.5px** — Labels, table headers, navigation text (subtle tracking)
- **1px** — Logo text (wider tracking for brand emphasis)

### Line Height

- **1.5** — Body text; comfortable reading
- **1.0** — Headlines and labels; single line

---

## Spacing System

### Gap Scale

- **32px** — Major section gaps, content padding
- **24px** — Chart section padding, content area vertical gaps
- **20px** — Metric cards gap, table row actions
- **16px** — Card internal vertical, list items padding, user section gaps
- **12px** — Logo elements gap, nav icon to text, list item icon to content, section gaps
- **10px** — Search icon to placeholder, system info rows
- **8px** — Action buttons gap, title row to subtitle, bar to label
- **6px** — Label stacks (title to meta), change indicators
- **4px** — Gallery navigation buttons, inline elements
- **2px** — Navigation item vertical stacking (tight list)

### Padding Scale

- [32, 40] — Content area main padding
- [24, 24] — Chart section
- [20, 20] — Metric cards, system info
- [16, 20] — List items, upgrade box, user section
- [16, 16] — Table rows, gallery content
- [12, 20] — Navigation items
- [12, 16] — Banner
- [10, 16] — Primary/secondary buttons
- [10, 14] — Search box, action buttons
- [8, 12] — Secondary button actions
- [4, 8] — Small badges, tiny labels

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **240px** — Sidebar Width (fixed)
- **fill_container** — Content Area (flexible)
- **32px / 40px** — Content Padding (vertical / horizontal)
- **32px** — Section Gap between major sections
- **12px** — Card Grid Gap

---

## Corner Radius

This design system uses **zero corner radius** throughout, creating terminal/command-line aesthetic alignment, industrial precision and mechanical feel, clear differentiation from friendly consumer interfaces, and an aggressive, technical, professional appearance.

- **0px** — All elements (no rounded corners)

---

## Icons

### Icon Style

- **Lucide** — Thin stroke icons matching terminal aesthetic

### Icons Used

- **Navigation:** layout-dashboard, activity, users, settings, archive, folder
- **Actions:** search, download, plus, zap
- **Status:** trending-up, trending-down, credit-card
- **Content:** image (placeholder)

### Icon Sizes

- **28px** — Placeholder images
- **16px** — Navigation icons
- **14px** — Button icons
- **12px** — Status indicators

### Icon Color States

- #00FF88 — Active, Accent (active states, positive indicators)
- #0C0C0C — Primary on Green (text/icons on green backgrounds)
- #8a8a8a — Inactive (standard muted icons)
- #6a6a6a — Muted (secondary muted elements)
- #1A1A1A — Placeholder (image placeholders)
