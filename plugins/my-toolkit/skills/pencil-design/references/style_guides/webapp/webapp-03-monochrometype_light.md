# Use the following style guide in the current design task

## Name of the styleguide: `webapp-03-monochrometype_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Monochrome Type Dashboard — Style Guide

---

## Style Summary

### Description

An elegant editorial dashboard combining magazine aesthetics with functional clarity. Playfair Display—a refined serif typeface in italic—brings literary sophistication to headlines and metrics, while Inter handles UI elements with quiet professionalism. The strictly monochromatic palette (black, white, and carefully calibrated grays) creates a timeless, premium feel. Very light borders (#E0E0E0) provide subtle structure without visual weight. The result is a sophisticated, understated interface ideal for luxury brands, editorial platforms, publishing tools, and premium SaaS applications.

### Key Aesthetics

- **Literary Typography:** Playfair Display italic creates an editorial, magazine-like presence. Reserved for display elements at dramatic sizes (84px titles, 48px metrics).
- **Pure Monochrome:** Strictly black, white, and gray—no color accents whatsoever. Every visual distinction achieved through typography, gray scale, borders, and spatial relationships.
- **Whisper Borders:** Ultra-light #E0E0E0 lines provide structure without visual noise. A single border color used throughout.
- **Text-Based Navigation:** Arrow characters and text (arrows, slashes) instead of icon libraries reinforce the typographic aesthetic.
- **Generous Whitespace:** 64px section gaps and 56px horizontal padding create premium breathing room and luxury feel.
- **Italic-Only Display:** All Playfair Display usage is italic throughout—no upright usage—reinforcing the editorial identity consistently.

### Tags

`editorial` · `monochrome` · `serif` · `webapp` · `magazine` · `typography` · `elegant` · `minimal` · `luxury` · `dashboard`

---

## Color System

This design uses zero color accents. Every visual distinction is achieved through typography (weight, style, size), gray scale values, border presence/absence, and spatial relationships. This constraint creates a timeless, sophisticated aesthetic that won't date.

### Core Backgrounds

- #FFFFFF — Page Background (pure white canvas)
- #F5F5F5 — Surface Muted (very light gray for image placeholders)
- #000000 — Banner/CTA Background (black for emphasis sections)

### Text Colors

- #000000 — Primary Text (headlines, important content, active states)
- #666666 — Muted Text (hero subtitle, softer descriptions)
- #888888 — Secondary Text (labels, inactive navigation, metadata)
- #DDDDDD — Disabled/Placeholder (gallery placeholder numbers)
- #CCCCCC — Separator (pagination separators)

### Accent Colors

- None — Zero color accents; pure monochrome system

### Borders

- #E0E0E0 — All borders, dividers, strokes (universal border color)
- #000000 — Strong borders (button outlines on primary actions)

---

## Typography

The dual-font system creates sophisticated contrast. Playfair Display Italic is reserved for display elements—its literary character elevates dashboards to editorial quality. Inter handles all functional UI—its neutrality doesn't compete with the display type. The italic-only approach for Playfair creates visual consistency.

### Font Families

- **Playfair Display** — Page titles, section titles, metric values, logo, gallery numbers, upgrade titles (elegant serif, literary, refined; always italic)
- **Inter** — Navigation, buttons, body text, labels, metadata, table content (clean, neutral, highly legible)

### Type Scale

- **84px** — Page Title. Playfair Display, italic, normal 400, letterSpacing: -3
- **48px** — Metric Value / Gallery Number. Playfair Display, italic, normal 400, letterSpacing: -2
- **36px** — Upgrade Title. Playfair Display, italic, normal 400
- **28px** — Section Title. Playfair Display, italic, normal 400
- **24px** — Logo. Playfair Display, italic, bold 700
- **16px** — Body / Pagination Active. Inter, normal 400 / Playfair Display, italic, semibold 600
- **14px** — Navigation / Table Header / Table Data. Inter, semibold 600 active / normal 400 inactive / medium 500
- **13px** — Link/Action / Meta. Inter, medium 500 / normal 400
- **12px** — Badge (unused in pagination). Inter, medium 500

### Font Weights

- **700** — Bold. Logo only
- **600** — Semibold. Active navigation, pagination active
- **500** — Medium. Actions, badges, table headers, buttons
- **400** — Normal. Everything else (most common weight)
- **300** — Light. Pagination separators

### Letter Spacing

- **-3px** — Page title (84px); tight for dramatic impact
- **-2px** — Metric values (48px); condensed for cohesion
- **0** — Default; all other text

### Line Height

- **1.6** — Hero subtitle, descriptions; comfortable reading
- **1.0** — Headlines, labels; single line

---

## Spacing System

### Gap Scale

- **64px** — Section gap (between major content blocks)
- **56px** — Page horizontal padding, banner horizontal padding
- **40px** — Major (metric card padding, chart header to content gap)
- **32px** — Large (list item columns, gallery cards gap)
- **24px** — Standard (navigation items gap, section header to content, gallery items internal, pagination gap)
- **16px** — Medium (bar to label in charts, nav arrows gap, upgrade content stack, button gap)
- **8px** — Small (title/description stacks, list item info stack, gallery content stack)

### Padding Scale

- **[48, 56]** — Upgrade CTA section
- **[42, 56, 56, 56]** — Hero section
- **[0, 56, 56, 56]** — Content area
- **[24, 56]** — Header
- **[24, 24]** — Gallery content area
- **[24, 0]** — List items vertical
- **[18, 0]** — Table body rows
- **[16, 56]** — Banner
- **[16, 0]** — Table header row
- **[14, 32]** — CTA button
- **[12, 24]** — Buttons (primary/secondary)
- **[40, 0]** — Metric cards (left border style)

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **56px** — Content Horizontal Padding
- **64px** — Section Gap (vertical between major sections)
- **42px** — Hero Padding (top), 56px (sides and bottom)

---

## Corner Radius

This design uses **zero corner radius** throughout, creating editorial print-inspired precision, a timeless classic aesthetic, clear alignment with the grid, and sophisticated restraint.

- **0px** — ALL elements (no rounded corners)

---

## Icons

### Icon Style

- **Text-based characters only** — No icon library. All navigation and actions use text characters, reinforcing the editorial/typographic aesthetic.

### Icons Used

- **Navigation:** arrows (left arrow, right arrow)
- **Actions:** "View All" with arrow, "Export" with arrow
- **Dismiss:** multiplication sign
- **Separators:** forward slash

### Icon Sizes

- **20px** — Close/Dismiss
- **16px** — Navigation Arrows (left arrow, right arrow)
- **14px** — Separators (forward slash)
- **Inline** — Action Arrows (inline with text, e.g., "View All" with arrow)

### Icon Color States

- #000000 — Active/Primary
- #888888 — Inactive/Secondary
- #CCCCCC — Muted
- #888888 — Muted on dark background (for close)
- #FFFFFF — On Dark Background
