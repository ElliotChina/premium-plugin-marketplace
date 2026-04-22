# Use the following style guide in the current design task

## Name of the styleguide: `webapp-01-japaneseswiss_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Japanese Swiss Web Dashboard — Style Guide

---

## Style Summary

### Description

A light-mode minimalist dashboard fusing Japanese zen restraint with Swiss typographic precision. An ultra-narrow icon-only black sidebar (64px) maximizes content space on a warm off-white (#FAFAFA) canvas. The dual-font system pairs Sora's geometric modernity for UI elements with IBM Plex Mono's technical precision for data. Vertical color indicators, metric dividers, and a single vivid red accent (#DC2626) create visual rhythm without clutter. Suited for analytics dashboards, SaaS platforms, and professional business tools.

### Key Aesthetics

- **Japanese-Swiss Fusion:** Zen restraint meets Swiss mathematical clarity. No shadows, gradients, or rounded corners—pure functional form.
- **Typography:** Dual-font system—Sora (UI/headings) with tight negative letter-spacing (-1 to -2px) and IBM Plex Mono (data/metrics). Creates cognitive separation between the emotional and rational layers.
- **Structure:** Metric dividers (right-stroke borders between KPI cards), vertical color indicators (3-4px bars for status), and thin horizontal rules. Icon-only 64px black sidebar.
- **Color:** Warm off-white (#FAFAFA) canvas with precise gray scale. Single vivid red (#DC2626) reserved for CTAs, alerts, accent bars, and chart elements.
- **Interactive elements:** Red-filled primary buttons with icon + label. Outlined secondary buttons with 1px #E5E5E5 borders.

### Tags

`japanese` · `swiss` · `minimal` · `zen` · `webapp` · `dashboard` · `geometric` · `monospace` · `icon-sidebar` · `off-white` · `red-accent` · `data-focused`

---

## Color System

The design uses a warm off-white base (#FAFAFA instead of pure white) to reduce eye strain and create a welcoming atmosphere within strict minimalism. The pure black sidebar provides dramatic contrast, while a single red accent maintains disciplined visual hierarchy.

### Core Backgrounds

- #FAFAFA — Page Background (warm off-white)
- #000000 — Sidebar Background
- #F5F5F5 — Surface Tint (table headers, hover states)
- transparent — Card Background (inherits page background)

### Text Colors

- #000000 — Text Primary
- #5E5E5E — Text Secondary (descriptions, muted content)
- #666666 — Text Tertiary (inactive nav icons)
- #999999 — Text Placeholder (metadata, muted icons)
- #FAFAFA — Text On Dark (sidebar icons, button labels on dark/red)

### Accent Colors

- #DC2626 — Red Primary (CTAs, active states, alerts, accent bars, chart bars)
- #22C55E — Success (positive indicators, completed status)
- #3B82F6 — Info (information highlights, new items)

### Border

- #E5E5E5 — All borders, dividers, strokes

---

## Typography

The dual-font system creates clear cognitive separation. Sora with negative letter-spacing handles the emotional layer—what you feel and navigate. IBM Plex Mono handles the rational layer—what you measure and analyze. The tight letter-spacing on headlines is the Swiss signature—it creates visual sophistication and density that elevates the entire interface.

### Font Families

- **Sora** — Headlines, page titles, section headers, buttons, navigation, card titles
- **IBM Plex Mono** — Metrics, labels, metadata, table content, timestamps, badges

### Type Scale

- **48px** — Page Title. Sora, semibold 600, letterSpacing: -2
- **40px** — Metric Value. Sora, semibold 600, letterSpacing: -2
- **24px** — Section Title. Sora, semibold 600, letterSpacing: -1
- **16px** — Logo Mark. Sora, bold 700
- **14px** — Card Title. Sora, semibold 600
- **13-14px** — Body. Sora, normal 400 / medium 500
- **12px** — Button Label. Sora, medium 500 / semibold 600
- **12px** — Metric Label. IBM Plex Mono, medium 500
- **12px** — Table Header. IBM Plex Mono, semibold 600, letterSpacing: 1
- **13px** — Table Cell. IBM Plex Mono, normal/medium
- **12px** — Meta/Timestamp. IBM Plex Mono, normal 400
- **11-13px** — Badge/Status. IBM Plex Mono, medium 500
- **10px** — Avatar Text. Sora, semibold 600

### Font Weights

- **700** — Bold. Logo mark only
- **600** — Semibold. Page titles, section titles, metric values, table headers
- **500** — Medium. Buttons, labels, active navigation, badges
- **400** — Normal. Body text, descriptions, metadata, inactive elements

### Letter Spacing

- **-2px** — Page titles, metric values (creates visual density)
- **-1px** — Section titles (subtle tightening)
- **+1px** — Table headers (all-caps feel without uppercase)
- **0px** — All other text

---

## Spacing System

Structured whitespace is central to the zen aesthetic. Generous padding and gaps allow content to breathe, while the 64px icon-only sidebar maximizes content real estate. Major sections are separated by 52px vertical gaps, and the content area uses 48px/64px padding (vertical/horizontal).

### Gap Scale (between elements)

- **64px** — Content Side (content area horizontal padding)
- **52px** — Section Divider (vertical gap between main content sections)
- **48px** — Content (main row gap, content area top/bottom padding)
- **32px** — Major (sidebar top section gap, activity section gap)
- **24px** — Section (sidebar bottom gaps, banner padding, gallery gap)
- **20px** — Large (list item padding, table cell padding)
- **16px** — Medium (metric card internal, list item gaps)
- **12px** — Standard (header title/subtitle, action button gaps)
- **8px** — Small (button icon gaps, gallery nav gap)
- **6px** — Tight (status change indicator gap, pagination gap)
- **4px** — Minimal (navigation icon vertical gaps)

### Padding Scale

- **[48, 64]** — Content area (top/bottom, left/right)
- **[32, 0]** — Sidebar vertical padding
- **[20, 24]** — Banner
- **[16, 20]** — Table cells, table header row
- **[12, 16]** — Primary buttons (search, date picker, new report)
- **[10, 16]** — Secondary buttons (export)

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **64px** — Sidebar Width (fixed, icon-only, #000000)
- **fill_container** — Content Area (flexible, #FAFAFA)
- **48px / 64px** — Content Padding (vertical / horizontal)
- **52px** — Section Gap (vertical between major sections)
- **48px** — Main Row Gap (chart + activity side-by-side)
- **24px** — Card Grid Gap (3-up gallery)
- **360px** — Activity Feed Width (fixed)

---

## Corner Radius

This design system uses **zero corner radius** throughout—sharp edges like shoji screens, reinforcing Japanese architectural precision and Swiss mathematical authority.

- **0px** — ALL elements (no rounded corners whatsoever)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight

### Icons Used

- **Navigation:** layout-grid, trending-up, users, file-text, settings
- **Actions:** search, calendar, plus, download, x
- **Arrows:** arrow-up-right, arrow-down-right, arrow-left, arrow-right, chevron-right
- **Status:** minus, zap

### Icon Sizes

- **18px** — Sidebar Navigation
- **14-16px** — Buttons, Actions, Gallery Nav

### Icon Color States

- #FAFAFA — Active/Primary (on dark backgrounds)
- #666666, #999999 — Inactive/Muted
- #000000 — On Light (primary actions)
- #22C55E, #DC2626 — Semantic (success, alert/accent)