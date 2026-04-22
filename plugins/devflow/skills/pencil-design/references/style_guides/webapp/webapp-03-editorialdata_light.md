# Use the following style guide in the current design task

## Name of the styleguide: `webapp-03-editorialdata_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Editorial Data Dashboard — Style Guide

---

## Style Summary

### Description

A sophisticated editorial dashboard combining magazine-quality typography with clean data presentation. The design marries classical elegance—italic serif headlines (Playfair Display) with generous letter-spacing—against a warm off-white canvas. A horizontal masthead replaces traditional sidebars, creating an open, content-forward layout. Section dividers use subtle top borders with italic serif labels. Black serves as the primary accent against warm neutrals, while semantic colors (green/amber) handle status communication. The result is a refined, editorial-quality interface ideal for business intelligence, content platforms, and executive dashboards.

### Key Aesthetics

- **Editorial Heritage:** Playfair Display italic headlines evoke high-end print publications with classical typographic sophistication.
- **Warm Minimalism:** Off-white (#FDFCF9) background creates a paper-like reading experience with gentle warmth throughout.
- **Monochromatic Accent:** Black (#1A1A1A) serves as the single accent color for CTAs, featured elements, and emphasis — no vivid brand colors.
- **Top Navigation:** Horizontal masthead instead of sidebar maximizes content real estate and creates an open, editorial feel.
- **Typographic Hierarchy:** Dramatic size contrast between 72px headlines and 13px body text creates strong visual rhythm.
- **Zero Decoration:** No shadows, no gradients, no rounded corners — pure editorial clarity with sharp geometric structure.

### Tags

`editorial` · `magazine` · `serif` · `warm` · `elegant` · `webapp` · `masthead` · `data-focused` · `italic` · `classical`

---

## Color System

The palette achieves luxury through restraint — black (#1A1A1A) serves as the single accent color, warm neutrals create visual interest through subtle tonal shifts, and semantic colors (green/amber) only appear for status indication, never for decoration. The warm off-white canvas (#FDFCF9) with #E5E2DC borders creates cohesive warmth throughout.

### Core Backgrounds

- #FDFCF9 — Page Background (warm off-white canvas, paper-like)
- #FDFCF9 — Card Background (matches page for seamless integration)
- #F5F2ED — Surface Tint (subtle warm gray for image placeholders)
- #1A1A1A — Inverted Surface (dark containers for featured elements)

### Text Colors

- #1A1A1A — Text Primary (headlines, metric values, primary content)
- #777777 — Text Secondary (subtitles, descriptions, secondary labels)
- #999999 — Text Tertiary (muted content, inactive pagination, placeholders)
- #666666 — Text Muted (avatar initials, subdued elements)
- #FFFFFF — Text Inverted (text on dark backgrounds)

### Accent Colors

- #1A1A1A — Black Primary; headlines, buttons, featured elements, emphasis
- #E5E2DC — Border Warm; all borders and dividers
- #E8E5DF — Surface Warm; avatar backgrounds, subtle fills
- #CCCCCC — Placeholder; icon placeholders in image areas
- #22C55E — Success/Positive; completed status, positive change, active
- #F59E0B — Warning/Pending; pending status, caution indicators
- #DC2626 — Error/Negative; error states (reserved)
- #999999 — Inactive; inactive status text

---

## Typography

The dual-font system creates clear editorial hierarchy — Playfair Display (italic) handles the editorial voice that captures attention, while Inter handles the functional voice for everything you read, click, and analyze. The dramatic size range from 72px page titles to 9px badge labels creates a strong visual rhythm.

### Font Families

- **Playfair Display** — Page titles, section headers, gallery titles, logo; classical serif, italic for headlines, regular for logo
- **Inter** — Navigation, buttons, labels, data, body text; humanist sans, clean, highly legible

### Type Scale

- **72px** — Page Title. Playfair Display, italic, medium 500, letterSpacing: -2
- **42px** — Hero Metric. Inter, semibold 600, letterSpacing: -2
- **28px** — Metric Value. Inter, semibold 600, letterSpacing: -1
- **24px** — Logo. Playfair Display, bold 700, letterSpacing: 4
- **22px** — Section Title. Playfair Display, italic, semibold 600, letterSpacing: 0.5
- **16px** — Subtitle, Gallery Title. Inter normal 400 / Playfair Display italic semibold 600
- **13-14px** — Navigation, Body, Label. Inter, normal 400 to medium 500
- **12px** — Meta, Change Indicators. Inter, medium 500
- **11px** — Button Small, Pagination. Inter, semibold 600 / medium 500
- **9px** — Badge. Inter, bold 700, letterSpacing: 1

### Font Weights

- **700** — Bold. Logo, small badges
- **600** — Semibold. Page titles, metric values, section headers, active nav
- **500** — Medium. Body text, table cells, list items, buttons
- **400** — Normal. Labels, descriptions, inactive navigation

### Letter Spacing

- **-2px** — Large headlines (72px page title, hero metric)
- **-1px** — Medium metric values (28px)
- **+0.5px** — Section titles (22px italic)
- **+1px** — Small all-caps (badges, upgrade button)
- **+4px** — Logo text
- **0** — Default; all other text

### Line Height

- **1.6** — Subtitles; comfortable reading
- **1.0** — Headlines and labels; single line

---

## Spacing System

### Gap Scale

- **48px** — Section divider; between major content sections, two-column gap
- **32px** — Major; logo to navigation, hero metric padding
- **24px** — Large; navigation items gap, section title to content, gallery items gap, chart bars
- **18px** — Section; hero title to subtitle
- **16px** — Medium; metric card internal, gallery card internal, list/table row gaps
- **12px** — Standard; bar to label, search/upgrade/avatar gap
- **8px** — Small; list item title/date stack, navigation arrows, pagination
- **6px** — Tight; icon to change text, title/description stacks
- **1px** — Metric card separator (visual divider)

### Padding Scale

- [40, 64] — Main content area
- [32, 32] — Hero metric box
- [20, 64] — Masthead
- [16, 24] — Banner
- [16, 0] — List items vertical, table rows
- [12, 20] — Metric card (standard)
- [10, 0] — Table header row
- [8, 16] — Upgrade button
- [4, 10] — Badge label

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **~60px** — Masthead Height (content-defined)
- **40px / 64px** — Content Padding (vertical / horizontal)
- **48px** — Section Gap between major sections
- **48px** — Column Gap for two-column layouts
- **24px** — Card Grid Gap horizontal
- **1px** — Metric Card Separator (with #E5E2DC fill)

---

## Corner Radius

This design system uses **zero corner radius** throughout, creating editorial/print publication aesthetic alignment, sharp authoritative visual presence, classical elegance over friendly approachability, and strong geometric structure.

- **0px** — All elements (no rounded corners)

---

## Icons

### Icon Style

- **Lucide** — Simple, lightweight line icons

### Icons Used

- **Actions:** search, zap, chevron-left, chevron-right, x
- **Status:** trending-up
- **Content:** image (placeholder)

### Icon Sizes

- **32px** — Image placeholders
- **16px** — Navigation (search, close)
- **14px** — Upgrade button (zap)
- **12-16px** — Change indicators (trending-up)
- **12px** — Carousel navigation (chevrons)

### Icon Color States

- #1A1A1A — Primary on light background
- #FFFFFF — On dark background
- #999999 — Muted
- #CCCCCC — Placeholder
- #22C55E — Positive (success)
- #F59E0B — Warning (pending)