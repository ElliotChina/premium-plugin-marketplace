# Use the following style guide in the current design task

## Name of the styleguide: `mobile-03-darkbold_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Dark Bold Mobile — Style Guide

---

## Style Summary

### Description

Pitch-black canvas mobile interface that hits with the energy of a late-night NYC street scene. Space Grotesk headlines deliver bold geometric confidence at extra-bold 700–800 weight while the electric lime accent (#C4F82A) cuts through darkness like neon signs. Manrope provides friendly humanist warmth for body text, and Space Mono delivers technical precision for metadata and timestamps. Dark zinc surfaces (#18181B) float above the void with subtle 1px borders (#27272A) creating sophisticated layering. Generous 20–24px corner radii soften the industrial edge while maintaining serious credibility. The pill-shaped tab bar floats above a gradient fade, completing the premium nightlife aesthetic. Suited for productivity apps, habit trackers, fitness tools, and lifestyle products targeting users who demand bold visual confidence and urban sophistication.

### Key Aesthetics

- **NYC Street Energy:** Bold neon accents against pitch darkness—electric lime as the singular signature highlight used strategically for maximum impact.
- **Industrial Precision:** Three-font system creates deliberate separation—Space Grotesk for display, Manrope for body, Space Mono for technical metadata.
- **Layered Depth:** Zinc surfaces (#18181B) with subtle 1px borders (#27272A) create hierarchy; pitch-black (#0A0A0A) background makes traditional shadows ineffective, so borders define edges instead.
- **Soft Industrial Radii:** Generous 16–24px corner radii on cards soften the industrial darkness into a premium, approachable feel. Fully rounded pill tab bar and day circles provide playful contrast.
- **Selective Glow:** Lime glow on highlighted cards and white glow on today indicators create dramatic emphasis—used sparingly, never as general elevation.
- **Gradient Personality:** Featured content cards use bold gradient fills (purple-blue, red-orange) for visual energy within the dark palette.

### Tags

`mobile` · `dark-mode` · `bold` · `urban` · `neon` · `electric` · `industrial` · `geometric` · `confident` · `premium`

---

## Color System

The design achieves electric energy against darkness through a strict pitch-black foundation with a singular lime accent. Zinc surfaces create subtle depth without competing with accents. Borders are subtle but essential for defining card edges. White provides maximum contrast for critical elements.

### Core Backgrounds

- #0A0A0A — Page Background (pitch black)
- #18181B — Card Surface (zinc)
- #27272A — Elevated Surface; nested elements, borders, dividers

### Text Colors

- #FFFFFF — Text Primary; headlines, primary content
- #A1A1AA — Text Secondary; body text, descriptions
- #71717A — Text Tertiary; labels, metadata, inactive items
- #52525B — Text Muted; placeholder text, disabled states
- #0A0A0A — Text Inverted; text on accent backgrounds

### Border Colors

- #27272A — Border Subtle; card strokes (1px), dividers
- #3F3F46 — Border Muted; inactive borders, empty states

### Accent Colors

- #C4F82A — Lime Primary; active states, CTAs, highlights
- #C4F82A25 — Lime Glow; shadow/glow on highlighted cards (25% opacity)
- #FA541C — Orange Alert; in-progress states, warnings
- #15803D — Green Success; positive metrics on light surfaces
- #7C3AED — Purple Accent; secondary schedule accent, gradient component
- #FFFFFF30 — White Glow; today indicator glow (30% opacity)

### Gradients

- #7C3AED → #2563EB — Purple-Blue; program card gradient (135°)
- #DC2626 → #F97316 — Red-Orange; program card gradient (135°)
- #0A0A0A00 → #0A0A0A — Fade; tab bar gradient overlay

### Shadows

- 0 4px 24px #C4F82A25 — Accent Glow; highlighted metric cards
- 0 0 12px (spread: 2px) #FFFFFF30 — Today Glow; current day indicator

---

## Typography

The three-font system creates deliberate emotional separation—Space Grotesk handles the display layer (bold geometric confidence), Manrope handles the functional layer (friendly humanist warmth), and Space Mono handles the technical layer (precise metadata and timestamps). Extra-bold 800 weight on metrics and bold 700 on headlines create commanding presence.

### Font Families

- **Space Grotesk** — Headlines, section titles, metric values, card titles
- **Manrope** — Body text, UI labels, navigation, accordion titles
- **Space Mono** — Timestamps, metadata, badge text, progress labels

### Type Scale

- **32px** — Display Value, Screen Title. Space Grotesk, bold 700 / extra-bold 800, lineHeight: 1.0–1.1
- **20px** — Section Header. Space Grotesk, bold 700
- **18px** — Featured Percentage. Space Grotesk, bold 700
- **16px** — Card Title, Headline. Space Grotesk bold 700 / Manrope semibold 600
- **15px** — Body, Accordion Title. Manrope, semibold 600
- **14px** — Callout, Label. Manrope, semibold 600
- **13px** — Subhead. Manrope, semibold 600
- **12px** — Footnote, Meta. Space Mono, normal 400 / medium 500
- **11px** — Caption, Tab Label, Badge. Manrope medium 500 / Space Mono medium 500

### Font Weights

- **800** — Extra Bold. Large metric values (Space Grotesk)
- **700** — Bold. Section headers, display titles (Space Grotesk)
- **600** — Semibold. Headlines, active tabs, item titles (Manrope)
- **500** — Medium. Labels, inactive tabs, meta info
- **400** — Normal. Body descriptions, meta text

### Letter Spacing

- **-0.5px** — Large display numbers (tight, optional)
- **0** — Default; all other text

### Line Height

- **1.0** — Metric numbers (compact)
- **1.1** — Screen titles (headlines)
- **1.4** — Card descriptions (standard)
- **1.5** — Expanded accordion content (readable)

---

## Spacing System

### Gap Scale (between elements)

- **24px** — Section; between major sections in scroll content
- **16px** — Standard; section header to content, search wrapper gap
- **14px** — Row; habit row internal spacing
- **12px** — Cards; within sections, horizontal scroll items
- **8px** — Internal; metric card content, day column gaps
- **6px** — Small; progress indicators, program card content
- **4px** — Tight; icon to label, status rows, day indicators
- **2px** — Minimal; title + description within list rows

### Padding Scale

- **[0, 24, 24, 24]** — Content wrapper (top, horizontal, bottom)
- **20px** — Metric cards, week progress card (uniform)
- **18px** — Accordion items (uniform)
- **[16, 20]** — List rows (vertical, horizontal)
- **16px** — Schedule cards, program card content
- **[0, 16]** — Search bar (horizontal only)
- **[12, 21, 21, 21]** — Tab bar section (gradient fade area)
- **[8, 16]** — Tab items (vertical, horizontal)
- **[8, 14]** — Action buttons
- **[6, 10]** — Small badges (duration)
- **4px** — Segmented control container, tab pill internal

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **874px** — Minimum Screen Height
- **24px** — Content Padding (horizontal)
- **24px** — Section Gap (vertical)
- **12px** — Card Gap (within sections)
- **16px** — Component Gap (header to content)
- **200px** — Program Card Width (horizontal scroll)

---

## Corner Radius

Rounded corners soften the industrial darkness. Generous 16–24px radii on cards create a premium, approachable feel while maintaining the bold urban aesthetic. Fully rounded elements (tab bar, day circles) provide playful contrast against the rectangular card grid.

- **8px** — Small badges (program duration)
- **10px** — Segmented control items, action buttons
- **14px** — Segmented control container, status checkboxes
- **16px** — Search bar, schedule cards
- **18px** — Day progress circles
- **20px** — Metric cards, week card, program cards, help card
- **24px** — Large cards (habits list card)
- **100px** — Tab bar pill (fully rounded)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, bar-chart, compass, user (tab bar)
- **Actions:** search, bell, plus, chevron-down, chevron-up
- **Status:** check, trending-up, trending-down

### Icon Sizes

- **22px** — Notification bell
- **20px** — Navigation tabs, search, chevrons
- **16–18px** — Status checkmarks, action buttons
- **14px** — Trend indicators

### Icon Color States

- #C4F82A — Active (navigation, expanded chevron, positive trend)
- #52525B — Inactive (navigation, search placeholder)
- #71717A — Tertiary (collapsed chevron)
- #FFFFFF — On Dark Surfaces
- #0A0A0A — On Lime Surfaces
- #15803D — Positive Trend (on light surfaces)