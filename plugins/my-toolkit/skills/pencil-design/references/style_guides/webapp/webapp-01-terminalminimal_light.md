# Use the following style guide in the current design task

## Name of the styleguide: `webapp-01-terminalminimal_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Terminal Minimal Dashboard — Style Guide

---

## Style Summary

### Description

A sleek, dark-mode dashboard that fully embraces terminal aesthetics through exclusive use of monospace typography (JetBrains Mono), command-line visual metaphors, and a vibrant green accent (#22C55E). The design features an all-lowercase approach with snake_case naming conventions, comment-style descriptions (// prefixed), and terminal prompt indicators (~ and >) for navigation. The near-black canvas (#0C0C0C) paired with subtle gray surface cards (#171717) creates depth without distraction. Suited for developer tools, analytics dashboards, DevOps platforms, and any application targeting technical users.

### Key Aesthetics

- **Pure Terminal:** JetBrains Mono used exclusively for all text, reinforcing the code editor feel. Weight variations alone create hierarchy.
- **Total Darkness:** Near-black backgrounds (#0C0C0C page, #171717 cards) create an immersive, focused environment.
- **Green Energy:** Bright terminal green (#22C55E) as the sole accent color for CTAs, active states, and data visualization.
- **Terminal Metaphors:** Prompt symbols (~ for logo, > for active nav) and comment syntax (// subtitles) create authentic CLI atmosphere.
- **Code Conventions:** All-lowercase text, snake_case labels (total_revenue, active_users), hash IDs (#4892).
- **Minimal Structure:** Ultra-thin borders (#1F1F1F, #252525) for structure. Status as colored text only—no background chips or pills.

### Tags

`terminal` · `monospace` · `dark-mode` · `developer` · `minimal` · `green-accent` · `command-line` · `lowercase` · `snake_case` · `devtools`

---

## Color System

The design operates on a controlled gray scale from #0C0C0C to #E5E5E5, with color used sparingly and purposefully. Green dominates as the primary accent, with amber, blue, and red reserved strictly for semantic states. Surface elevation (#171717 over #0C0C0C) provides depth without shadows.

### Core Backgrounds

- #0C0C0C — Page Background (near-black canvas)
- #171717 — Surface/Card (elevated content)
- #1A1A1A — Input/Highlight (active nav, input fields)
- #1F1F1F — Border Primary (structure)
- #252525 — Border Secondary (table rows, lists)

### Text Colors

- #E5E5E5 — Text Primary (headlines, values)
- #A3A3A3 — Text Secondary (body, descriptions)
- #737373 — Text Tertiary (labels, metadata, inactive nav)
- #525252 — Text Muted (placeholders, disabled, inactive icons)

### Accent Colors

- #22C55E — Green Primary; CTAs, active states, charts, positive indicators, prompt symbol
- #F59E0B — Warning; pending status, upgrade prompts
- #3B82F6 — Info; new badges, informational links
- #EF4444 — Error; negative indicators, failed status
- #525252 — Neutral; unchanged metrics, disabled

---

## Typography

The single-font approach creates absolute consistency and reinforces the terminal aesthetic. Weight variations (400–600) provide hierarchy without introducing visual complexity from mixed typefaces. All text uses lowercase with snake_case conventions.

### Font Families

- **JetBrains Mono** — All text: headlines, body, labels, data, navigation, buttons

### Type Scale

- **32px** — Page Title. Semibold 600
- **28px** — Metric Value. Semibold 600
- **14-16px** — Section Title. Medium 500
- **13px** — Navigation. Medium 500 (active) / normal 400 (inactive)
- **12-13px** — Body, Table Cell. Normal/medium
- **11-12px** — Meta, Badge, Timestamp. Normal/medium

### Font Weights

- **600** — Semibold. Page titles, metric values, emphasis
- **500** — Medium. Section titles, buttons, active nav, badges
- **400** — Normal. Body text, labels, inactive navigation, metadata

### Letter Spacing

- **0** — Default; all text

### Line Height

- **1.6** — Descriptions; multi-line readability
- **1.3-1.4** — Default; inherits from font

---

## Spacing System

### Gap Scale (between elements)

- **40px** — Content side; content area horizontal padding
- **32px** — Major; sidebar top sections gap, main content sections gap
- **24px** — Section; sidebar bottom sections gap
- **20px** — Large; chart/table section internal
- **16px** — Card; cards grid gap, metric cards internal, gallery items gap, chart header gap
- **12px** — Medium; nav item internal, upgrade box internal, activity items gap
- **10px** — Small; card content stacking
- **8px** — Standard; logo components, action buttons row
- **6px** — Tight; change indicator components
- **4px** — Minimal; navigation items vertical gap, pagination buttons gap

### Padding Scale

- **[32, 40]** — Main content area (top/bottom, left/right)
- **[32, 20]** — Sidebar (vertical, horizontal)
- **[20, 20]** — Metric cards, chart section, activity section, table section
- **[16, 16]** — Gallery card content, upgrade box internal
- **[12, 16]** — Banner
- **[8, 16]** — CTA buttons with icons
- **[8, 12]** — Small buttons, nav items, search field
- **[6, 12]** — Compact buttons (export)

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **240px** — Sidebar Width (fixed, #0C0C0C, right border 1px #1F1F1F)
- **fill_container** — Content Area (flexible, #0C0C0C)
- **32px / 40px** — Content Padding (vertical / horizontal)
- **32px** — Section Gap between major sections
- **4 columns** — Metric Card Grid, equal width, 16px gap
- **3 columns** — Gallery Card Grid, equal width, 16px gap
- **360px** — Activity Feed fixed width

---

## Corner Radius

This design system uses **near-zero corner radius** throughout, maintaining sharp, technical edges. Small radius on interactive elements provides subtle interaction affordance.

- **0px** — Page container, sidebar, table cells
- **2px** — Chart bars, small elements
- **4px** — Buttons, input fields, nav item highlights, avatar

---

## Icons

### Icon Style

- **Lucide** — Icon font, consistent stroke weight

### Icons Used

- **Actions:** search, calendar, plus, download, x
- **Arrows:** chevron-down, chevron-left, chevron-right

### Icon Sizes

- **14-16px** — Button icons, chevrons, dismiss/close
- **12-14px** — Compact actions

### Icon Color States

- #22C55E — Active (prompt symbol, active states)
- #737373 — Secondary (active icons on dark)
- #525252 — Muted/Inactive (placeholders, disabled)
- #0C0C0C — On Green (buttons with green background)

### Arrow Indicators

- **Positive:** "↑" text character, #22C55E
- **Negative:** "↓" text character, #EF4444
- **Neutral:** "—" text character, #525252
