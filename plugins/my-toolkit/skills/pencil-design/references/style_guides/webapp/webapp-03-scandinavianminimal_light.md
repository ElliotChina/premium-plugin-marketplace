# Use the following style guide in the current design task

## Name of the styleguide: `webapp-03-scandinavianminimal_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Scandinavian Minimal Dashboard — Style Guide

---

## Style Summary

### Description

A serene, nature-inspired dashboard combining a warm cream canvas (#FAF8F5) with generous white cards featuring soft rounded corners (20px). The design marries elegant serif typography (Fraunces) for headlines with clean sans-serif (Inter) for UI, creating an approachable yet sophisticated hierarchy. A muted sage green (#7C9082) serves as the single accent color, used sparingly for CTAs, icons, and positive indicators. The result is a calming, organic interface ideal for productivity apps, analytics platforms, and modern SaaS products seeking warmth over cold corporate aesthetics.

### Key Aesthetics

- **Warm Foundation:** Cream background (#FAF8F5) replaces cold white, creating visual warmth; all neutrals have warm undertones (cream, taupe, stone).
- **Generous Curves:** 20px corner radius on cards creates soft, approachable containers; interactive elements use 24px for pill-like friendliness.
- **Serif Elegance:** Fraunces typeface brings editorial refinement to headlines; Inter handles all functional UI; IBM Plex Mono for data indicators.
- **Nature-Derived Palette:** Sage green (#7C9082) accent evokes forest, calm, and organic authenticity; used exclusively for interactive elements.
- **Horizontal Flow:** Top navigation bar keeps content as the primary focus with generous whitespace and breathing room.
- **Subtle Borders:** 1px warm gray borders (#E8E4DF) define without dominating; no shadows, pure border-based structure.

### Tags

`scandinavian` · `minimal` · `webapp` · `warm` · `organic` · `serif-display` · `rounded` · `sage-accent` · `soft` · `wellness`

---

## Color System

The palette draws from nature — sage green against a warm cream canvas. Warm neutrals (#FAF8F5 backgrounds, #E8E4DF borders) replace cold grays throughout, while the single sage accent maintains a focused, organic atmosphere that feels inviting rather than clinical.

### Core Backgrounds

- #FAF8F5 — Page Background (warm cream canvas)
- #FFFFFF — Card Background (pure white for elevated surfaces)
- #F5F3EF — Surface Tint (subtle warm gray for table headers, icon containers)
- #F0EDE8 — Surface Muted (warm stone for banners, image placeholders)

### Text Colors

- #2D2D2D — Text Primary (charcoal)
- #8A8A8A — Text Secondary (labels, metadata, navigation, subtle text)
- #ADADAD — Text Muted (placeholders, disabled states, search icons)
- #5A5A5A — Text Body (banner text, body content)

### Accent Colors

- #7C9082 — Sage Primary; CTAs, icons, positive indicators, chart bars
- #7C908215 — Sage Tint 15%; badge backgrounds, hover states
- #22C55E — Success; positive amounts, growth indicators (semantic only)
- #E8E4DF — Border Primary; card strokes, navigation borders, input borders
- #F0EDE8 — Border Subtle; table row dividers, list item separators
- #DADADA — Placeholder Gray; placeholder icons, disabled elements

---

## Typography

The three-font system creates clear visual hierarchy — Fraunces brings editorial elegance and brand personality to headlines, Inter handles the interface efficiently without competing with display type, and IBM Plex Mono gives data a technical foundation while maintaining warmth.

### Font Families

- **Fraunces** — Page titles, section headers, logo text (display serif, editorial, refined)
- **Inter** — Navigation, buttons, labels, body text, badges (clean, neutral, highly legible)
- **IBM Plex Mono** — Metric values, amounts, technical content (modern monospace, warm)

### Type Scale

- **48px** — Page Title. Fraunces, normal 400, letterSpacing: -1
- **32px** — Metric Value. IBM Plex Mono, medium 500, letterSpacing: -1
- **20px** — Section Title, Logo Text. Fraunces, normal 400, letterSpacing: -0.5
- **14-15px** — Body. Inter, normal/medium
- **14px** — Navigation. Inter, normal 400 inactive / medium 500 active
- **13px** — Button, Label. Inter, medium 500
- **12-13px** — Small Text. Inter, normal/medium
- **11px** — Badge, Avatar Initials. Inter, medium 500 / semibold 600

### Font Weights

- **600** — Semibold. Avatar initials only
- **500** — Medium. Headlines, buttons, active nav, metric values, labels
- **400** — Normal. Body text, inactive navigation, descriptions

### Letter Spacing

- **-1px** — Page titles, metric values (large display text)
- **-0.5px** — Section titles, logo (medium display text)
- **0** — Default; all other text

### Line Height

- **1.5** — Body, descriptions; comfortable reading
- **1.4** — Gallery descriptions
- **1.0** — Headlines, labels; single line

---

## Spacing System

### Gap Scale

- **48px** — Navigation logo to links gap
- **40px** — Major; content sections gap
- **32px** — Navigation padding (horizontal), section title gap
- **28px** — Section headers to content
- **20px** — Large; metrics row gap, gallery items gap, sections internal
- **16px** — Medium; chart bars gap, list item icon to content, table padding
- **12px** — Standard; banner elements, action button icon gaps, title to subtitle
- **10px** — Logo elements gap
- **8px** — Small; button icon gaps, gallery navigation, badge text padding
- **6px** — Compact; change indicator icon to text
- **4px** — Tight; title + description in cards

### Padding Scale

- **[32, 80]** — Content area (vertical, horizontal)
- **[20, 80]** — Top navigation (vertical, horizontal)
- **[28, 28]** — Metric cards, chart sections
- **[20, 24]** — List items
- **[20, 20]** — Gallery card content, card content padding
- **[16, 24]** — Table cells
- **[16, 20]** — Banner
- **[12, 20]** — Secondary buttons, export button
- **[10, 16]** — Search box, upgrade button, pill buttons
- **[6, 12]** — Status badges

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **Horizontal** — Navigation (top bar, full width, height ~76px)
- **80px / 32px** — Content Padding (horizontal / vertical)
- **40px** — Section Gap between major sections
- **20px** — Card Grid Gap
- **4 columns** — Metric Card Grid, equal width
- **3 columns** — Gallery Card Grid, equal width

---

## Corner Radius

This design uses generous, consistent rounding throughout, creating visual warmth and approachability that evokes organic, natural forms aligned with Scandinavian design.

- **20px** — Cards, tables, gallery items, navigation arrows
- **24px** — Buttons, pill shapes
- **28px** — Search input (pill shape)
- **18px** — Avatar, pagination dots
- **16px** — Badges, banner
- **12px** — Icon containers, small elements
- **8px** — Logo icon, chart bars (subtle rounding)

---

## Icons

### Icon Style

- **Lucide** — Line icons, consistent stroke weight (1.5-2px)

### Icons Used

- **Navigation:** layout-dashboard, trending-up, users, file-text, settings
- **Actions:** search, plus, download, calendar, arrow-right
- **Status:** trending-up, trending-down, minus

### Icon Sizes

- **32px** — Placeholder icons (gallery)
- **18px** — List item icons
- **16px** — Navigation icons, action icons
- **14px** — Button icons, trend arrows

### Icon Color States

- #7C9082 — Active, Sage (accent)
- #FFFFFF — On dark fill (buttons)
- #8A8A8A — Primary UI
- #ADADAD — Muted, placeholder
- #DADADA — Disabled, placeholder icons
