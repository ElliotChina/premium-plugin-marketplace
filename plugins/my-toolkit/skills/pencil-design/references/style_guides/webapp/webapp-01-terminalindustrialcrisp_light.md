# Use the following style guide in the current design task

## Name of the styleguide: `webapp-01-terminalindustrialcrisp_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Terminal Industrial Crisp Dashboard — Style Guide

---

## Style Summary

### Description

A bold, industrial dark-mode dashboard that commands attention through its electric lime accent (#BFFF00) against a pure black canvas (#000000). The design employs a dual-font strategy—Inter for headlines and metric values delivering clarity and authority, paired with JetBrains Mono for labels, navigation, and data creating technical credibility. Active states are marked by crisp 2px left border indicators, while status dots appear as small rounded squares rather than circles. Title case text, spaced-out logo treatment, and generous padding create a premium, polished feel suited for enterprise SaaS platforms, fintech dashboards, analytics tools, and professional B2B applications.

### Key Aesthetics

- **Industrial Premium:** Inter headlines bring clean authority; JetBrains Mono handles all data, labels, and navigation with technical precision.
- **Pure Black Canvas:** #000000 base creates maximum contrast for the electric lime accent.
- **Electric Lime Accent:** #BFFF00 for CTAs, active states, charts, and positive indicators—high-energy, never subtle.
- **Crisp Indicators:** 2px left border marks active navigation states with geometric clarity. Rounded status squares (6x6, 3px radius) replace circles.
- **Structure:** 1px borders (#1A1A1A) for cards and dividers. Surface cards (#111111) lift content from the black base without shadows.
- **Title Case Convention:** Proper capitalization throughout headlines and navigation. Letter-spaced logo (3px tracking) for industrial character.

### Tags

`industrial` · `dark-mode` · `lime-accent` · `neon` · `enterprise` · `crisp` · `professional` · `dual-font` · `bold` · `fintech`

---

## Color System

The design achieves impact through extreme contrast—electric lime (#BFFF00) against pure black (#000000). This isn't a subtle accent system; it demands attention and signals action. Surface elevation (#111111 over #000000) provides depth, while the extended gray text hierarchy (#FFFFFF → #999999 → #6e6e6e → #404040) creates layered readability.

### Core Backgrounds

- #000000 — Page Background (pure black canvas)
- #111111 — Surface/Card (elevated content)
- #1A1A1A — Border, Input, Highlight

### Text Colors

- #FFFFFF — Text Primary (headlines, values)
- #999999 — Text Secondary (body, dates)
- #6e6e6e — Text Tertiary (labels, descriptions, inactive nav)
- #404040 — Text Muted (icons, placeholders, disabled)

### Accent Colors

- #BFFF00 — Lime Primary; CTAs, active states, chart bars, positive indicators
- #3B82F6 — Info; new badges, informational status
- #F59E0B — Warning; pending status, warnings
- #FF4444 — Error; negative indicators, failed status
- #404040 — Neutral; unchanged metrics

---

## Typography

The dual-font system creates clear visual separation—Inter commands attention on headlines and key metrics (what matters most), JetBrains Mono provides technical credibility for data and navigation (what users interact with). Title case text throughout maintains a polished, professional appearance.

### Font Families

- **Inter** — Page titles, section headers, metric values, card titles, logo text
- **JetBrains Mono** — Navigation, buttons, labels, metadata, table content, badges

### Type Scale

- **32px** — Page Title, Metric Value. Inter, semibold 600
- **16-18px** — Section Title. Inter, semibold 600
- **15px** — Card Title, Logo. Inter, semibold 600; logo uses letterSpacing: 3
- **13px** — Navigation. JetBrains Mono, medium 500 (active) / normal 400 (inactive)
- **12-13px** — Body, Table Cell. JetBrains Mono, normal/medium
- **10-12px** — Meta, Chart Labels. JetBrains Mono, normal
- **9px** — Tag. JetBrains Mono, bold 700

### Font Weights

- **700** — Bold. Banner tags
- **600** — Semibold. Headlines, metric values, section titles, buttons, amounts
- **500** — Medium. Active navigation, status badges, labels
- **400** — Normal. Body text, inactive navigation, descriptions, dates

### Letter Spacing

- **+3px** — Logo text (spaced-out industrial style)
- **0** — Default; all other text

### Line Height

- **1.6** — Descriptions; multi-line readability
- **1.3-1.4** — Default; inherits from font

---

## Spacing System

### Gap Scale (between elements)

- **48px** — Content side; content area horizontal padding
- **40px** — Major; sidebar top sections gap, main content sections gap
- **24px** — Section; chart/activity internal, sidebar bottom sections gap
- **20px** — Large; table section gap, gallery section gap
- **16px** — Card; cards grid gap, metric cards internal, banner internal
- **14px** — Activity; item internal (dot to content)
- **12px** — Medium; nav item internal, upgrade box internal, gallery card content
- **10px** — Small; bar chart internal, search button internal
- **8px** — Standard; action buttons row, date button internal
- **6px** — Tight; change indicator, upgrade label
- **4px** — Minimal; pagination buttons, gallery navigation
- **2px** — Micro; navigation items vertical gap

### Padding Scale

- **[32, 48]** — Main content area (top/bottom, left/right)
- **[32, 24]** — Sidebar (vertical, horizontal)
- **[24, 24]** — Metric cards, chart section, activity section, table section
- **[20, 20]** — Gallery card content
- **[14, 20]** — Banner
- **[10, 18]** — Primary CTA buttons
- **[10, 14]** — Navigation items, secondary buttons
- **[8, 14]** — Export button
- **[8, 12]** — Small table search button
- **[4, 10]** — Banner tag
- **[4, 8]** — Gallery card tag

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **240px** — Sidebar Width (fixed, #000000, right border 1px #1A1A1A)
- **fill_container** — Content Area (flexible, #000000)
- **32px / 48px** — Content Padding (vertical / horizontal)
- **40px** — Section Gap between major sections
- **4 columns** — Metric Card Grid, equal width, 16px gap
- **3 columns** — Gallery Card Grid, equal width, 16px gap
- **360px** — Activity Feed fixed width

---

## Corner Radius

This design system uses **zero corner radius** for virtually all elements, maintaining sharp, industrial edges. The only exception is small status indicator dots.

- **0px** — All elements (cards, buttons, page container, sidebar)
- **3px** — Status indicator dots (small rounded squares, 6x6)

---

## Icons

### Icon Style

- **Lucide** — Icon font, consistent stroke weight

### Icons Used

- **Navigation:** layout-dashboard, trending-up, users, file-text, settings
- **Actions:** search, calendar, plus, download, x
- **Arrows:** chevron-down, chevron-left, chevron-right

### Icon Sizes

- **16px** — Navigation (sidebar icons)
- **14-16px** — Chevrons, dismiss/close
- **12-14px** — Button/Action (buttons, indicators)

### Icon Color States

- #BFFF00 — Active (active nav icons)
- #6e6e6e — Secondary (inactive icons, labels)
- #404040 — Muted/Inactive (placeholders, disabled)
- #000000 — On Lime (buttons with lime background)

### Arrow Indicators

- **Positive:** "↑" text character, #BFFF00
- **Negative:** "↓" text character, #FF4444
- **Neutral:** "—" text character, #404040