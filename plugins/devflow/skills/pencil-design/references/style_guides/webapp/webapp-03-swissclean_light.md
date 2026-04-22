# Use the following style guide in the current design task

## Name of the styleguide: `webapp-03-swissclean_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Swiss Clean Dashboard — Style Guide

---

## Style Summary

### Description

A refined dashboard design built on maximum whitespace and geometric precision. The design pairs a clean white sidebar (separated by a subtle border) with a spacious content area. Typography combines Space Grotesk for headings and metrics — lending geometric authority — with Inter for body text and labels. A single vivid red accent (#E42313) punctuates key interactive elements: logo mark, active navigation, CTA buttons, and chart highlights. Soft near-black (#0D0D0D) text creates comfortable contrast without harshness. The result is a professional, contemporary interface ideal for SaaS dashboards, financial platforms, and enterprise applications.

### Key Aesthetics

- **Unified Light Foundation:** Both sidebar and content share a white base, differentiated purely by a subtle 1px border (#E8E8E8).
- **Geometric Typography:** Space Grotesk brings structured, architectural character to headings; Inter provides comfortable readability for supporting text.
- **Signaling Through Accent:** Single red accent (#E42313) used exclusively for activation states, CTAs, logo mark, and chart highlights.
- **Zero Decoration:** No shadows, no gradients, no rounded corners — pure geometric clarity throughout.
- **Soft Contrast:** Near-black (#0D0D0D) instead of pure black creates comfortable reading; all structure comes from borders, not background contrast.
- **Generous Breathing Room:** Large gaps (48px) and card padding (28px) create a spacious, professional feel.

### Tags

`swiss` · `clean` · `minimal` · `geometric` · `webapp` · `dashboard` · `whitespace` · `red-accent` · `sharp` · `professional`

---

## Color System

The system operates on a unified white foundation where structure comes purely from borders rather than background contrast. A disciplined neutral scale from near-black to border gray provides comfortable hierarchy, while a single vivid red accent creates clear visual activation and emphasis.

### Core Backgrounds

- #FFFFFF — Page Background (pure white canvas throughout)
- #FFFFFF — Sidebar Background (white with border separation)
- #FAFAFA — Surface Tint (table headers, image placeholders, upgrade box)

### Text Colors

- #0D0D0D — Text Primary (near-black; primary text, filled buttons, badges, avatar)
- #7A7A7A — Text Secondary (labels, descriptions, inactive nav)
- #B0B0B0 — Text Muted (close icons, minor UI elements)
- #D0D0D0 — Placeholder (image placeholder icons)

### Accent Colors

- #E42313 — Red Primary; logo mark, active nav, CTAs, chart bars, banner indicators
- #22C55E — Success Green; positive amounts, growth indicators, up arrows
- #E8E8E8 — Border Gray; all borders, strokes, dividers throughout

---

## Typography

The dual-font system creates clear visual distinction — Space Grotesk handles structural elements that anchor attention, while Inter handles supporting content that provides context. No additional typefaces are used.

### Font Families

- **Space Grotesk** — Page titles, section titles, metrics, navigation, buttons, logo (geometric, architectural, modern)
- **Inter** — Descriptions, labels, body text, table content, badges, timestamps (humanist, approachable, highly legible)

### Type Scale

- **40px** — Page Title. Space Grotesk, medium 500, letterSpacing: -1
- **36px** — Metric Value. Space Grotesk, semibold 600, letterSpacing: -1
- **18px** — Section Title, Logo. Space Grotesk, semibold 600
- **14px** — Subtitle, Navigation, Body. Inter/Space Grotesk, normal/medium
- **13px** — Button, Label. Space Grotesk/Inter, medium 500 / normal 400
- **12px** — Small Text, Badges. Inter/Space Grotesk, medium 500

### Font Weights

- **600** — Semibold. Section titles, metric values, amounts
- **500** — Medium. Page titles, active navigation, buttons, list item titles
- **400** — Normal. Body text, labels, inactive navigation, descriptions

### Letter Spacing

- **-1px** — Page titles and metric values (tightened for display sizes)
- **0** — Default; all other text

### Line Height

- **1.5** — Body text, descriptions

---

## Spacing System

### Gap Scale

- **48px** — Section; content area gap, top section gap
- **32px** — Major; sidebar horizontal padding
- **24px** — Section; metrics gap, bottom section gap, item amounts to badge
- **20px** — Cards; section internal gap, list section gap, gallery items gap
- **16px** — Medium; list item horizontal gap, chart bars gap, gallery content padding
- **12px** — Navigation; logo gap, nav dot to text, action buttons gap
- **10px** — List; chart bar to label
- **8px** — Standard; title section gap, pagination gap, navigation items gap, icon-to-text in buttons
- **6px** — Small; action link icon gap, gallery content
- **4px** — Minimal; title + description stacks, list item content
- **2px** — Tight; user info stacks

### Padding Scale

- **[40, 48]** — Content area (vertical, horizontal)
- **[32, 40]** — Sidebar (horizontal, vertical)
- **[28, 28]** — Metric cards, chart section
- **[20, 24]** — List items
- **[20, 20]** — Upgrade box
- **[16, 20]** — Table rows
- **[16, 16]** — Gallery content
- **[14, 20]** — Table headers, banner
- **[10, 20]** — Action buttons
- **[8, 16]** — Export buttons
- **[6, 12]** — Period chips
- **[4, 10]** — Status badges
- **[3, 8]** — Small badges

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **240px** — Sidebar Width (fixed)
- **fill_container** — Content Area (flexible)
- **40px / 48px** — Content Padding (vertical / horizontal)
- **48px** — Section Gap between major sections
- **24px** — Metric Card Grid Gap (4 columns, equal width)
- **20px** — Gallery Gap (3 columns, equal width)

---

## Corner Radius

This design system uses zero corner radius throughout, creating geometric, architectural alignment with Swiss design precision and authority. Sharp corners produce a clean, professional appearance and structured visual rhythm.

- **0px** — All elements (no rounded corners whatsoever)

---

## Icons

### Icon Style

- **Lucide** — Clean, geometric, consistent 2px stroke weight

### Icons Used

- **Actions:** trending-up, download, plus, arrow-right, chevron-left, chevron-right, x
- **Content:** credit-card, arrow-up-right, user, image

### Icon Sizes

- **28px** — Large (gallery placeholders)
- **18px** — Medium (list item icons)
- **16px** — Standard (navigation arrows, chevrons)
- **14px** — Small (button icons, action icons, close)

### Icon Color States

- #FFFFFF — In buttons (dark background)
- #7A7A7A — In buttons (light), muted/secondary
- #0D0D0D — Action links
- #B0B0B0 — Close, dismiss
- #D0D0D0 — Placeholder
- #22C55E — Success