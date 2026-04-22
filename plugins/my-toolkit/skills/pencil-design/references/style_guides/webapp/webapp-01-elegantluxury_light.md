# Use the following style guide in the current design task

## Name of the styleguide: `webapp-01-elegantluxury_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Elegant Luxury Dashboard — Style Guide

---

## Style Summary

### Description

A refined, dark-mode dashboard radiating understated luxury through a champagne gold accent (#C9A962) against rich near-black surfaces (#0F0F0F). The design pairs the editorial elegance of Playfair Display serif headlines with the modern clarity of Manrope sans-serif body text, creating a sophisticated contrast between classic and contemporary. Cream-toned text (#FAF8F5) provides warmth, while hairline borders (#1F1F1F) and outlined icon indicators with semantic color tints add subtle structure. Suited for premium SaaS platforms, financial dashboards, luxury brand tools, and professional services applications.

### Key Aesthetics

- **Editorial Luxury:** Playfair Display serif headlines bring magazine-quality refinement; Manrope sans-serif handles all functional interface elements.
- **Dark Opulence:** Near-black backgrounds (#0F0F0F page, #0A0A0A sidebar) create depth and premium feel.
- **Champagne Gold Accent:** Muted gold (#C9A962) for CTAs, active states, and accent elements—sophisticated, never garish.
- **Warm Text Tones:** Cream text (#FAF8F5) over cool backgrounds creates inviting contrast rather than harsh pure white.
- **Structure:** Hairline borders (#1F1F1F) define structure throughout. Left-accent borders (2px gold) and tinted backgrounds for active navigation states.
- **Zero Decoration:** No shadows, gradients, or rounded corners—pure refined form. Outlined icons with semantic color tint backgrounds as indicators.

### Tags

`luxury` · `elegant` · `dark-mode` · `gold-accent` · `serif` · `editorial` · `premium` · `sophisticated` · `webapp` · `dashboard` · `champagne` · `executive`

---

## Color System

The design achieves visual harmony through careful temperature balance—warm elements (#FAF8F5 cream text, #C9A962 gold accent) against cool elements (#0F0F0F backgrounds, #1F1F1F borders, #888888 secondary text). The interplay creates depth without coldness, luxury without heaviness.

### Core Backgrounds

- #0F0F0F — Page Background
- #0A0A0A — Sidebar Background
- #1F1F1F — Border, Divider
- #C9A96210 — Gold Tint active states (10% opacity)
- #C9A96208 — Gold Tint banners (8% opacity)

### Text Colors

- #FAF8F5 — Text Primary (cream off-white)
- #888888 — Text Secondary
- #666666 — Text Tertiary
- #0A0A0A — Text On Gold

### Accent Colors

- #C9A962 — Gold Primary; CTAs, active states, chart bars
- #C9A96240 — Gold Tint 40%; icon indicator backgrounds
- #C9A96230 — Gold Tint 30%; banner borders
- #4ADE80 — Success; positive indicators, completed status
- #4ADE8040 — Success Tint; icon indicator backgrounds
- #60A5FA — Info; information highlights, new items
- #60A5FA40 — Info Tint; icon indicator backgrounds
- #F87171 — Error; negative indicators, failed status
- #888888 — Neutral; unchanged metrics

---

## Typography

The dual-font system creates deliberate emotional separation—Playfair Display handles the aspirational layer (what inspires and impresses), Manrope handles the functional layer (what you read and interact with). Normal weight (400) on Playfair maintains a refined appearance; various weights (400–600) on Manrope create interface hierarchy.

### Font Families

- **Playfair Display** — Headlines, page titles, section headers, metric values, logo text, card titles
- **Manrope** — Navigation, buttons, labels, body text, metadata

### Type Scale

- **48px** — Page Title. Playfair Display, normal
- **36px** — Metric Value. Playfair Display, normal
- **22px** — Section Title, Logo Text. Playfair Display, normal, letterSpacing: 1 (logo only)
- **18px** — Logo Mark Letter. Playfair Display, medium 500
- **16px** — Card Title. Playfair Display, normal
- **14px** — Navigation. Manrope, normal/medium
- **13-14px** — Body, Table Cell. Manrope, normal/medium, lineHeight: 1.5
- **12px** — Button, Label. Manrope, medium 500 / semibold 600
- **11px** — Table Header. Manrope, semibold 600
- **10-11px** — Meta, Badge. Manrope, medium 500

### Font Weights

- **600** — Semibold. Buttons on gold, table headers, upgrade badge
- **500** — Medium. Active navigation, labels, badges, logo mark
- **400** — Normal. All Playfair Display headlines, body text, inactive nav

### Letter Spacing

- **+1px** — Logo text, premium label
- **0** — Default; all other text

### Line Height

- **1.5** — Body, descriptions; comfortable reading
- **1.0** — Headlines, labels; single line

---

## Spacing System

### Gap Scale (between elements)

- **56px** — Content side; content area horizontal padding
- **48px** — Major; main content vertical gaps, content area top/bottom padding
- **28px** — Panel; chart/activity section internal padding
- **24px** — Section; sidebar section gaps, chart internal gaps, table section gaps
- **20px** — Large; metric card gap, gallery card gap, upgrade box padding
- **16px** — Card; metric card internal, upgrade box internal
- **14px** — Navigation; nav item icon to text
- **12px** — Medium; logo section gaps, gallery nav gaps
- **10px** — Medium-small; gallery card content gaps, bar chart label gaps
- **8px** — Standard; button icon gaps, pagination gaps
- **6px** — Small; change indicator icon/text, table action button gaps
- **4px** — Tight; activity item title/description, content stacks
- **2px** — Minimal; account info name/email stack

### Padding Scale

- **[48, 56]** — Main content area (top/bottom, left/right)
- **[40, 28]** — Sidebar
- **[28, 28]** — Panel sections (chart, activity, table)
- **[18, 24]** — Banner
- **[14, 16]** — Navigation items
- **[12, 20]** — Standard buttons (search, date, new report)
- **[10, 14]** — Small buttons (table search/export)

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **280px** — Sidebar Width (fixed, #0A0A0A)
- **fill_container** — Content Area (flexible, #0F0F0F)
- **48px / 56px** — Content Padding (vertical / horizontal)
- **48px** — Section Gap between major sections
- **24px** — Main Row Gap (chart + activity side by side)
- **4 columns** — Metric Card Grid, equal width, 20px gap
- **3 columns** — Gallery Card Grid, equal width, 20px gap
- **340px** — Activity Feed fixed width

---

## Corner Radius

This design system uses **zero corner radius** throughout, reinforcing architectural precision befitting the luxury aesthetic.

- **0px** — ALL elements (no rounded corners whatsoever)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight

### Icons Used

- **Navigation:** layout-grid, trending-up, users, file-text, settings
- **Actions:** search, calendar, plus, download, x, crown, sparkles
- **Arrows:** arrow-left, arrow-right, chevron-right, chevron-down
- **Status:** check, user-plus, trending-up, trending-down, minus

### Icon Sizes

- **18px** — Navigation (sidebar icons)
- **14-16px** — Activity, Gallery Nav (icon frames, prev/next arrows)
- **12-14px** — Button/Action (buttons, indicators)

### Icon Color States

- #C9A962 — Active, Gold (active nav, pending status)
- #4ADE80 — Success (completed status)
- #60A5FA — Info (new status)
- #F87171 — Error (failed status)
- #666666 — Inactive, Muted
- #0A0A0A — On Gold (buttons with gold background)
- #FAF8F5 — Primary Light (on dark backgrounds)
