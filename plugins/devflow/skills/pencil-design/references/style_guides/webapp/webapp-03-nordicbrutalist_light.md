# Use the following style guide in the current design task

## Name of the styleguide: `webapp-03-nordicbrutalist_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Nordic Brutalist Dashboard — Style Guide

---

## Style Summary

### Description

A bold dashboard aesthetic combining Scandinavian warmth with brutalist design principles. The warm cream background (#F5F2ED) evokes natural paper, while terracotta accents (#C45A3B) and muted olive greens (#6B8E5E) bring organic earthiness. Space Grotesk provides architectural, commanding typography with tight negative letter-spacing for headlines and positive letter-spacing for labels. Heavy border weights (2-4px) create bold structural divisions. The result is a sophisticated, confident interface ideal for data-rich business applications, analytics platforms, and professional SaaS products.

### Key Aesthetics

- **Warm Foundation:** Cream/paper background (#F5F2ED) creates an inviting, natural Scandinavian canvas. Warm gray scale throughout replaces cold standard grays.
- **Architectural Typography:** Space Grotesk with negative letter-spacing (-1 to -2px) on headlines commands attention. Uppercase labels with positive letter-spacing (1-3px) provides structured clarity.
- **Bold Structural Lines:** 2-4px border weights create decisive section breaks. No shadows—borders and fills create all visual separation.
- **Earthy Palette:** Terracotta (#C45A3B) for primary actions and alerts, olive green (#6B8E5E) for positive values. Organic accent colors against warm neutrals.
- **Dark Inversions:** Strategic use of #1A1A1A fills for emphasis areas—header, featured metric card, table heads, badges.
- **Geometric Purity:** Sharp corners (0px default, 8px active nav only) maintain architectural precision aligned with brutalist principles.

### Tags

`brutalist` · `nordic` · `scandinavian` · `webapp` · `architectural` · `warm` · `earthy` · `geometric` · `bold-type` · `dashboard`

---

## Color System

The design uses strategic dark inversions for visual hierarchy. The header, featured metric card, table headers, primary buttons, and completed badges all use dark fills (#1A1A1A) to create emphasis. The warm cream foundation (#F5F2ED) provides Scandinavian comfort while earthy accents bring organic warmth.

### Core Backgrounds

- #F5F2ED — Page Background (warm cream/paper tone, Scandinavian warmth)
- #1A1A1A — Header Background (charcoal black for primary navigation)
- #1A1A1A — Card Featured (dark fill for emphasized metric cards)
- #1A1A1A — Table Header (dark header rows for data tables)
- #E8E4DD — Surface Muted (slightly darker cream for image placeholders)

### Text Colors

- #1A1A1A — Primary Text (headlines, important content, structural fills)
- #888888 — Secondary Text (inactive navigation, icons)
- #999999 — Muted Text (tertiary labels)
- #C8C4BD — Placeholder Icons (on muted surfaces)
- #F5F2ED — Text On Dark (cream text on dark backgrounds, avatar text on light)

### Accent Colors

- #C45A3B — Terracotta Primary (active states, CTAs, primary accent, chart bars, alerts, negative/decrease indicator)
- #6B8E5E — Olive Green (muted olive for gains, success, positive growth)

### Borders

- #1A1A1A — Standard borders (1px element separation)
- #1A1A1A — Heavy section dividers (2-4px for major breaks)

---

## Typography

The typography system creates a strict hierarchy through size and spacing contrast. Space Grotesk handles all structural elements—its geometric character reinforces the brutalist aesthetic. Inter provides neutral readability for supporting content without competing with headlines. Compressed headlines command attention while open labels provide clarity.

### Font Families

- **Space Grotesk** — Page titles, section titles, metric values, navigation, buttons, labels, badges (geometric, architectural, bold, modern)
- **Inter** — Body text, descriptions, metadata, timestamps, change indicators (humanist, neutral, highly legible)

### Type Scale

- **64px** — Page Title. Space Grotesk, bold 700, letterSpacing: -2
- **44px** — Metric Value. Space Grotesk, bold 700, letterSpacing: -1
- **28px** — Upgrade Title. Space Grotesk, bold 700, letterSpacing: 1
- **24px** — Section Title. Space Grotesk, bold 700, letterSpacing: 1
- **18px** — Chart Title. Space Grotesk, bold 700, letterSpacing: 1
- **16px** — Item Title / Logo. Space Grotesk, semibold 600 / bold 700, letterSpacing: 3 (logo)
- **14px** — Navigation / Table Data. Space Grotesk, medium 500 / semibold 600
- **13-14px** — Body. Inter, normal 400
- **12-13px** — Button/Action. Space Grotesk, semibold 600, letterSpacing: 1
- **11px** — Label/Meta. Space Grotesk, semibold 600, letterSpacing: 1
- **10-11px** — Badge. Space Grotesk, semibold 600, letterSpacing: 1

### Font Weights

- **700** — Bold. Page titles, metric values, section titles, logo
- **600** — Semibold. Item titles, buttons, labels, badges, table data
- **500** — Medium. Inactive navigation
- **400** — Normal. Body text, descriptions, metadata (Inter)

### Letter Spacing

- **-2px** — Page title headlines (creates bold, impactful presence)
- **-1px** — Metric values (condensed for cohesion)
- **+1px** — Labels, buttons, badges (creates open, structured feel)
- **+2px** — CTA label accents
- **+3px** — Logo text (widest tracking)
- **0** — Default; body text, descriptions

### Line Height

- **1.0** — Headlines, labels; single line
- **Default** — Body text, descriptions

---

## Spacing System

### Gap Scale

- **64px** — Page horizontal padding
- **48px** — Section gap (major content sections)
- **32px** — Major (metric card padding, chart padding, gallery items top padding)
- **28px** — List item vertical padding
- **24px** — Section (list item icon to info, gallery content padding)
- **20px** — Large (metric card content gap, right actions gap)
- **16px** — Medium (bar to label in charts)
- **14px** — Logo gap (mark to text)
- **12px** — Standard (button gap, gallery nav gap, upgrade content stack)
- **10px** — Button icon gap
- **8px** — Small (badge content stack, info text stack, gallery content stack)

### Padding Scale

- **[42, 64]** — Content area (vertical, horizontal)
- **[40, 48]** — Upgrade CTA section
- **[32, 32]** — Metric cards
- **[24, 32]** — Chart header
- **[20, 64]** — Header
- **[20, 28]** — Banner
- **[20, 16]** — Table cells
- **[16, 32]** — CTA buttons
- **[14, 28]** — Standard buttons (primary/secondary)
- **[12, 24]** — Navigation items
- **[10, 18]** — Small action buttons (export)
- **[8, 16]** — Period/date chips
- **[6, 14]** — Standard badges (list badges)
- **[4, 12]** — Small badges (table badges)

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **42px / 64px** — Content Padding (vertical / horizontal)
- **48px** — Section Gap (vertical between major sections)
- **76px** — Header Height (approximate)

---

## Corner Radius

This design system uses **near-zero corner radius** throughout, creating architectural, structural visual weight and bold geometric presence aligned with brutalist principles. Clear differentiation from softer, consumer-friendly interfaces.

- **0px** — Default (most elements: cards, buttons, badges, inputs, charts, tables)
- **8px** — Active navigation state (subtle rounding for interactive feedback; single exception)

---

## Icons

### Icon Style

- **Lucide** — Regular stroke weight

### Icon Sizes

- **36px** — Large (gallery placeholders)
- **24px** — Medium (list item icons)
- **20px** — Navigation (gallery nav arrows)
- **18px** — Standard (header icons, close buttons)
- **16px** — Small (button icons)
- **14px** — Tiny (small action buttons)

### Icon Color States

- #1A1A1A — Primary (on light background)
- #888888 — Secondary (on light background)
- #F5F2ED — On Dark Background
- #C8C4BD — Placeholder