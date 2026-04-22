# Use the following style guide in the current design task

## Name of the styleguide: `webapp-02-swisselegant_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Swiss Elegant Dashboard v2 — Style Guide

---

## Style Summary

### Description

An editorial, magazine-inspired dashboard combining a minimalist dark icon-only sidebar (#0A0A0A) with an expansive white content area. The design marries Swiss modernist principles—systematic spacing, clean hierarchy, restrained color—with sophisticated typography: Cormorant Garamond serif for display elements and metrics, paired with Outfit geometric sans-serif for UI text. A distinctive muted burgundy accent (#6B2D3C) provides warmth without distraction. Suited for creative agencies, editorial platforms, portfolio tools, and premium SaaS applications.

### Key Aesthetics

- **Editorial Swiss:** Cormorant Garamond serif brings editorial gravitas to headlines and metrics; Outfit handles all functional interface elements with geometric clarity.
- **Restrained Minimalism:** Near-black sidebar (#0A0A0A) against pure white (#FFFFFF) content creates elegant contrast without harshness.
- **Muted Burgundy Accent:** #6B2D3C appears sparingly for featured items and review states—sophisticated warmth, never demanding.
- **Icon-First Navigation:** Compact 72px sidebar with 8px radius nav icons maximizes content space.
- **Structure:** 1px borders (#E5E5E5) throughout. Metric cards separated by background strips rather than borders. #FAFAFA and #F5F5F5 subtle surface tints.
- **Generous Whitespace:** Ample padding (40px vertical, 48px horizontal) and section gaps create breathing room. Numbered lists (01, 02, 03) add editorial sequencing.

### Tags

`swiss` · `elegant` · `editorial` · `serif` · `sophisticated` · `minimal` · `burgundy-accent` · `icon-sidebar` · `webapp` · `premium`

---

## Color System

The palette operates on a principle of restraint—primary work is done by black (#0A0A0A) and white (#FFFFFF), the gray spectrum handles secondary information, and the muted burgundy accent appears sparingly for maximum impact. No bright or competing colors.

### Core Backgrounds

- #FFFFFF — Page Background (pure white canvas)
- #0A0A0A — Sidebar Background (near-black)
- #282828 — Sidebar Active (active nav icon background)
- #FAFAFA — Surface Tint Light (table headers, cards)
- #F5F5F5 — Surface Tint Medium (search fields, subtle fills)
- #E5E5E5 — Metrics Strip (divider between metric cards)

### Text Colors

- #0A0A0A — Text Primary (near-black)
- #777777 — Text Secondary (labels, subtitles)
- #999999 — Text Tertiary (metadata, inactive states)
- #FFFFFF — Text On Dark (sidebar, filled buttons)

### Accent Colors

- #6B2D3C — Burgundy Primary; featured cards, review states, status indicators
- #B89999 — Burgundy Light; secondary text on burgundy backgrounds
- #9A1033 — Negative; decline indicators, negative change
- #E5E5E5 — Border Gray; all borders, dividers, strokes

---

## Typography

The dual-font system creates editorial sophistication—Cormorant Garamond handles display and data (commanding attention with serif elegance), Outfit handles the interface (clean, geometric, highly legible for functional elements). Tight negative letter-spacing on display text creates refined headlines.

### Font Families

- **Cormorant Garamond** — Metric values, page titles, gallery card titles, logo
- **Outfit** — Labels, buttons, body text, metadata, navigation, section labels

### Type Scale

- **56px** — Metric Value. Cormorant Garamond, medium 500, letterSpacing: -2
- **48px** — Page Title. Cormorant Garamond, medium 500, letterSpacing: -1
- **22px** — Logo. Cormorant Garamond, semibold 600
- **18px** — Gallery Title. Cormorant Garamond, medium 500
- **15px** — Page Subtitle. Outfit, normal 400, letterSpacing: 0.2
- **14px** — List Title. Outfit, medium 500
- **13px** — Body, Button. Outfit, normal/medium
- **12px** — Label, Table Header, Badge. Outfit, semibold 600
- **11px** — Section Label, Meta. Outfit, medium/semibold 500-600, letterSpacing: 1-1.5px

### Font Weights

- **600** — Semibold. Labels, logo, emphasized labels
- **500** — Medium. Metric values, page titles, buttons, list titles
- **400** — Normal. Body text, subtitles, metadata

### Letter Spacing

- **-2px** — Large metric values (tighter display feel)
- **-1px** — Page titles (refined headline spacing)
- **+1.5px** — Section labels (uppercase-style emphasis)
- **+1px** — Metric labels (moderate tracking)
- **+0.5px** — Table headers, category tags (slight tracking)
- **+0.2px** — Page subtitles (subtle openness)
- **0** — Default; all other text

### Line Height

- **1.5** — Body, descriptions; comfortable reading
- **1.0** — Headlines, labels; single line

---

## Spacing System

### Gap Scale (between elements)

- **48px** — Content horizontal; content area horizontal padding
- **40px** — Major; content padding vertical, section gaps
- **32px** — Large; logo to navigation gap
- **24px** — Section; chart area internal, chart header to chart area
- **20px** — Card; metric card internal, list item content, gallery section header
- **16px** — Medium; table cell gaps
- **12px** — Standard; actions row, banner content, gallery card content
- **8px** — Small; nav icons, title to subtitle, button icon to label
- **6px** — Tight; change indicator icon to text
- **4px** — Minimal; gallery nav buttons, pagination items, list content stacks

### Padding Scale

- **[40, 48]** — Main content area (vertical, horizontal)
- **[32, 24]** — Metric cards (vertical, horizontal)
- **[32]** — Chart section padding
- **[24]** — Gallery cards, sidebar vertical padding
- **[20, 24]** — List items, list header
- **[16, 24]** — Table body rows, pagination
- **[14, 24]** — Table header row
- **[14, 20]** — Banner
- **[12, 20]** — Secondary buttons
- **[4, 10]** — Badges

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **72px** — Sidebar Width (fixed, icon-only, #0A0A0A)
- **fill_container** — Content Area (flexible, #FFFFFF)
- **40px / 48px** — Content Padding (vertical / horizontal)
- **40px** — Section Gap between major sections
- **4 columns** — Metric Cards, separated by #E5E5E5 background strips
- **4 columns** — Gallery Carousel, 8px gap, 180px height

---

## Corner Radius

This design system uses **sharp corners by default** with selective softness for sidebar navigation elements only.

- **0px** — Most elements (cards, buttons, inputs, charts)
- **8px** — Navigation icon containers, logo mark, sidebar avatar
- **20px** — Avatar frame (circular feel at 40px size)

---

## Icons

### Icon Style

- **Lucide** — Icon font, consistent stroke weight

### Icons Used

- **Navigation:** Icon-only sidebar (layout-grid, trending-up, users, file-text, settings)
- **Actions:** search, calendar, plus, download, x
- **Arrows:** trending-up, trending-down, chevron-left, chevron-right

### Icon Sizes

- **20px** — Navigation (sidebar icons)
- **16px** — Button icons (primary/secondary buttons)
- **14px** — Metric arrows (trending up/down), action icons

### Icon Color States

- #FFFFFF — Active on dark (sidebar active)
- #777777 — Inactive on dark (sidebar inactive)
- #0A0A0A — Active on light (content area)
- #999999 — Muted (secondary actions)
- #9A1033 — Negative state
