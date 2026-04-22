# Use the following style guide in the current design task

## Name of the styleguide: `webapp-03-swisscleanexpressive_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Swiss Clean Expressive Dashboard — Style Guide

---

## Style Summary

### Description

A bold dashboard design that amplifies the Swiss Clean foundation with expressive dark zones. Features a dramatic dark sidebar (#0A0A0A) with numbered navigation items, paired with a bright content area. Typography is commanding — 54px page titles with tight letter-spacing create immediate visual impact. The design introduces strategic dark inversions: the first metric card uses a dark background as a hero element, and table headers are inverted dark. iOS-standard red (#FF3B30) serves as the accent, appearing in the logo, avatars, CTAs, and chart bars. The result is a confident, premium interface ideal for executive dashboards, fintech platforms, and enterprise SaaS applications.

### Key Aesthetics

- **Dark Sidebar Foundation:** True dark (#0A0A0A) sidebar creates an authoritative navigation zone with numbered items (01, 02, 03...) for systematic precision.
- **Strategic Inversions:** Dark hero metric card and dark table headers break monotony and create powerful visual anchors across the interface.
- **Commanding Typography:** 54px page titles with -2px letter-spacing and bold 700 weight demand attention; Space Grotesk dominates with architectural authority.
- **iOS Red Accent:** #FF3B30 provides vibrant, recognizable activation for logo, avatars, CTAs, chart bars, and negative amounts.
- **Premium Density:** Larger padding and gaps create executive-level breathing room; 56px horizontal content padding establishes generous margins.
- **Zero Decoration:** No shadows, no gradients, no rounded corners — pure geometric precision with flat color system throughout.

### Tags

`swiss` · `expressive` · `bold` · `dark-sidebar` · `webapp` · `dashboard` · `numbered-nav` · `premium` · `high-impact` · `red-accent`

---

## Color System

The design operates with a strategic dark zone approach — sidebar, hero metric card, and table headers share dark treatment to create visual anchors that command attention. A vivid iOS red accent provides vibrant activation throughout, while an extended grayscale palette handles the wide range of text and UI states.

### Core Backgrounds

- #FFFFFF — Page Background (pure white canvas for content)
- #0A0A0A — Sidebar Background (true dark for navigation zone)
- #1A1A1A — Dark Surface (upgrade box, slightly elevated dark)
- #0A0A0A — Hero Metric Card (dark inversion for first metric)
- #0A0A0A — Table Header (dark inversion for column labels)
- #F5F5F5 — Surface Tint (gallery image placeholders)

### Text Colors

- #0A0A0A — Text Primary (true dark; primary text, filled buttons, active badges)
- #666666 — Gray 700 (banner text)
- #777777 — Text Secondary (inactive nav, secondary text, timestamps)
- #999999 — Text Muted (metric labels on dark, period text, muted icons, pending badges)
- #AAAAAA — Close icons
- #D0D0D0 — Placeholder (image placeholder icons)

### Accent Colors

- #FF3B30 — Red Primary; logo, avatars, CTAs, chart bars, negative amounts, active nav numbers
- #22C55E — Success Green; positive amounts, growth indicators
- #E0E0E0 — Border Gray; all borders, strokes, dividers

---

## Typography

Bold weights dominate this system for executive presence — Space Grotesk 700 creates commanding headlines and metrics, while Inter provides comfortable reading for supporting content. Tight tracking on large text increases density and visual impact.

### Font Families

- **Space Grotesk** — Page titles, section titles, metrics, navigation, buttons, logo, amounts (geometric, architectural, bold)
- **Inter** — Descriptions, labels, body text, table content, badges, timestamps (humanist, approachable, highly legible)

### Type Scale

- **54px** — Page Title. Space Grotesk, bold 700, letterSpacing: -2
- **36px** — Metric Value. Space Grotesk, bold 700, letterSpacing: -2
- **24px** — Section Title. Space Grotesk, bold 700, letterSpacing: -0.5
- **18px** — Upgrade Title. Space Grotesk, semibold 600
- **16px** — Logo, Amount. Space Grotesk, bold 700
- **15px** — Navigation, List Title, Gallery Title. Space Grotesk, semibold 600 active / normal 400 inactive
- **14px** — Body, Table. Inter, normal 400
- **13px** — Button, Action Link. Space Grotesk, medium 500
- **12px** — Label, Badges. Inter/Space Grotesk, varies
- **11px** — Period Chips, Timestamps. Inter, normal 400

### Font Weights

- **700** — Bold. Page titles, section titles, metric values, logo, amounts
- **600** — Semibold. Active nav, list titles, buttons, change percentages
- **500** — Medium. Buttons, action links, table headers, badges
- **400** — Normal. Body text, labels, inactive navigation, descriptions

### Letter Spacing

- **+2px** — Logo text (ACME); expanded for brand authority
- **-0.5px** — Section titles (24px)
- **-2px** — Page titles and metric values; tightened for display impact
- **0** — Default; all other text

### Line Height

- **1.5** — Body text, descriptions

---

## Spacing System

### Gap Scale

- **40px** — Section; content area vertical gap
- **32px** — Major; sidebar padding, chart section internal, top nav gap
- **28px** — Large; sidebar bottom section gap
- **24px** — Section; metrics gap, list section gap, gallery section gap, table section gap
- **20px** — Cards; upgrade internal, gallery items content padding, list item horizontal
- **16px** — Medium; metric card internal, chart bars gap
- **14px** — Nav items; nav padding
- **12px** — Navigation; logo gap, chart bar to label, buttons gap
- **8px** — Standard; button icons, pagination, action links, gallery content
- **6px** — Small; list item content, navigation internal
- **4px** — Minimal; title stacks, upgrade text
- **2px** — Tight; user info stacks

### Padding Scale

- **[40, 56]** — Content area (vertical, horizontal)
- **[32, 32]** — Sidebar, chart section
- **[28, 28]** — Metric cards
- **[24, 28]** — List items
- **[20, 20]** — Gallery content
- **[18, 24]** — Table rows
- **[16, 24]** — Table header
- **[16, 20]** — Banner
- **[16, 16]** — Upgrade box
- **[12, 20]** — Action buttons
- **[10, 18]** — Export buttons
- **[8, 14]** — Period chips
- **[5, 12]** — List badges
- **[4, 10]** — Table badges

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **260px** — Sidebar Width (fixed, wider for numbered nav)
- **fill_container** — Content Area (flexible)
- **40px / 56px** — Content Padding (vertical / horizontal)
- **40px** — Section Gap between major sections
- **24px** — Card Grid Gap (4-column metrics, 3-column gallery)

---

## Corner Radius

This design system uses zero corner radius throughout, creating sharp, authoritative visual boundaries with Swiss design precision. The absence of rounding produces a premium, architectural appearance that clearly distinguishes from consumer-friendly rounded interfaces.

- **0px** — All elements (no rounded corners whatsoever)

---

## Icons

### Icon Style

- **Lucide** — Clean, geometric, consistent 2px stroke weight

### Icons Used

- **Actions:** download, plus, arrow-right, chevron-left, chevron-right, x
- **Content:** credit-card, arrow-up-right, user, image

### Icon Sizes

- **32px** — Large (gallery placeholders)
- **20px** — Medium (list item icons)
- **18px** — Standard (navigation arrows, chevrons)
- **14-16px** — Small (button icons, action icons, close)

### Icon Color States

- #FFFFFF — In primary buttons, next arrows
- #666666 — In secondary buttons
- #0A0A0A — Action links
- #999999 — In icon boxes, muted/secondary, prev arrows
- #AAAAAA — Close, dismiss
- #D0D0D0 — Placeholder
