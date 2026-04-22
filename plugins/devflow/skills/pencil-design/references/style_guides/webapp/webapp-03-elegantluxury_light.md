# Use the following style guide in the current design task

## Name of the styleguide: `webapp-03-elegantluxury_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Elegant Luxury Dashboard — Style Guide

---

## Style Summary

### Description

A sophisticated dark luxury dashboard pairing deep black backgrounds with warm gold accents (#C9A962). The design marries classical elegance—Cormorant Garamond serif for headlines—with modern functionality through Inter and JetBrains Mono for UI and data. A left sidebar navigation with icon-led menu items creates structured hierarchy. Gold serves as the exclusive accent color, appearing in active states, CTAs, positive metrics, and decorative elements with subtle glow effects. The result is an opulent, premium interface ideal for wealth management, luxury brand analytics, high-end SaaS, and executive dashboards.

### Key Aesthetics

- **Deep Black Canvas:** #0A0A0A background creates maximum depth and contrast for a premium, immersive dark-mode experience.
- **Monochromatic Gold:** Single warm gold accent (#C9A962) used throughout creates unmistakable luxury brand identity without competing colors.
- **Classical Typography:** Cormorant Garamond brings old-world elegance to modern data headlines and key metric values.
- **Icon-Led Navigation:** Sidebar items pair Lucide icons with labels for clear, structured wayfinding in a luxury context.
- **Transparent Layers:** Gold at 40% opacity (#C9A96240) creates subtle borders and glows that add depth without complexity.
- **Refined Restraint:** No gradients, minimal shadows, zero corner radius — architectural precision and sophisticated visual language.

### Tags

`luxury` · `dark-mode` · `gold-accent` · `elegant` · `premium` · `webapp` · `sidebar` · `serif` · `sophisticated` · `high-end`

---

## Color System

The palette achieves luxury through restraint — a single gold accent color (#C9A962) creates unmistakable brand identity, white on black provides maximum legibility and premium feel, and transparency layers (#C9A96240) add depth without complexity. No competing colors exist; semantic states use gold or neutral grays exclusively.

### Core Backgrounds

- #0A0A0A — Page Background (deep black canvas)
- #0A0A0A — Sidebar Background (unified with page, border-separated)
- #141414 — Surface Dark (gallery image backgrounds, subtle elevation)
- transparent — Card Background (cards defined by borders, not fills)

### Text Colors

- #FFFFFF — Text Primary (headlines, values, primary content)
- #848484 — Text Secondary (labels, descriptions, inactive icons)
- #6A6A6A — Text Tertiary (gallery descriptions, muted icons)
- #4A4A4A — Text Muted (dismiss icons, very muted elements)
- #0A0A0A — Text on Gold (text on accent backgrounds)

### Accent Colors

- #C9A962 — Gold Primary; active states, CTAs, positive indicators, icons
- #C9A96240 — Gold Transparent 40%; subtle borders, glows, badges
- #2A2A2A — Border Gray; all borders, dividers, table lines
- #1A1A1A — Surface Gray; gallery card strokes, subtle separators
- #E8E5DF — Surface Warm (reserved for avatar backgrounds)
- #8B5A5A — Warning; muted rose for pending (optional)
- #848484 — Inactive; gray text for inactive status

---

## Typography

The three-font system creates clear information hierarchy — Cormorant Garamond handles the prestige voice for headlines and key metrics, Inter handles the functional voice for navigation, labels, and UI elements, and JetBrains Mono handles the precision voice for monetary figures and financial data.

### Font Families

- **Cormorant Garamond** — Page titles, section headers, metric values, gallery titles, logo mark (classical serif)
- **Inter** — Navigation, buttons, labels, descriptions, table content (modern humanist sans)
- **JetBrains Mono** — Monetary values in lists, financial figures (technical monospace)

### Type Scale

- **48px** — Page Title. Cormorant Garamond, medium 500
- **40px** — Metric Value. Cormorant Garamond, medium 500, letterSpacing: -1
- **24px** — Section Title. Cormorant Garamond, medium 500
- **20px** — Gallery Title, Upgrade Title. Cormorant Garamond, medium 500
- **18px** — Logo Mark. Cormorant Garamond, semibold 600
- **16px** — Logo Text. Inter, medium 500, letterSpacing: 3
- **14px** — Navigation, Body. Inter, medium 500 / normal 400
- **13px** — Labels, Descriptions, Bar Labels. Inter, medium 500 / normal 400
- **12px** — Table Header, Meta, Dates, Export Buttons. Inter, normal 400 / medium 500
- **10px** — Badge. Inter, medium 500

### Font Weights

- **600** — Semibold. Logo mark letter
- **500** — Medium. Headlines, active navigation, buttons, badges, table cells
- **400** — Normal. Labels, descriptions, inactive navigation, table headers

### Letter Spacing

- **-1px** — Large metric values (40px)
- **+3px** — Logo text (creates premium spacing)
- **0** — Default; all other text

### Line Height

- **1.5** — Body, descriptions; comfortable reading
- **1.0** — Headlines and labels; single line

---

## Spacing System

### Gap Scale

- **48px** — Content section gaps (between major sections)
- **40px** — Sidebar top section gap
- **32px** — Chart section internal, header title section gap
- **24px** — Sidebar bottom section gap, list section gaps, table section gaps, list item right section
- **20px** — Metric cards gap, gallery cards gap, metric internal gap
- **16px** — Nav icon to label, list item icon to content, left section components
- **12px** — Logo components gap, bar to label, user avatar to info
- **10px** — Gallery navigation buttons gap
- **8px** — Icon to text in buttons, change indicator, content title/description
- **6px** — Pagination items, badge text padding vertical
- **4px** — Navigation items vertical gap
- **2px** — User info name/role stack

### Padding Scale

- [40, 56] — Main content area
- [28, 40] — Sidebar
- [28, 28] — Metric cards
- [20, 24] — List items
- [20, 20] — Upgrade box, gallery content
- [18, 20] — Table body rows
- [16, 20] — Banner
- [14, 20] — Table header horizontal
- [12, 20] — Primary/secondary buttons
- [10, 16] — Export button
- [6, 12] — Status badges
- [0, 14] — Navigation items vertical

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **280px** — Sidebar Width (fixed)
- **fill_container** — Content Area (flexible)
- **40px / 56px** — Content Padding (vertical / horizontal)
- **48px** — Section Gap between major sections
- **20px** — Card Grid Gap

---

## Corner Radius

This design system uses **zero corner radius** throughout, creating architectural precision and sophistication, modern luxury aesthetic with sharp lines, strong geometric structure and authority, and timeless elegance over trendy softness.

- **0px** — All elements (no rounded corners)

---

## Icons

### Icon Style

- **Lucide** — Light line icons, consistent stroke width

### Icons Used

- **Navigation:** layout-dashboard, activity, users, package, file-text, settings
- **Actions:** credit-card, trending-up, chevron-left, chevron-right, download, x
- **Content:** image (placeholder)

### Icon Sizes

- **32px** — Image placeholders
- **18px** — Navigation, list item icons
- **16px** — Carousel navigation, close/dismiss
- **14px** — Change indicators, action buttons

### Icon Color States

- #C9A962 — Active (gold, active navigation, positive indicators)
- #848484 — Inactive (gray, standard icons)
- #6A6A6A — Muted (dark gray, secondary actions)
- #0A0A0A — On Gold Background (black text/icons on gold)
- #2A2A2A — Placeholder (very dark, image placeholders)