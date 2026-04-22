# Use the following style guide in the current design task

## Name of the styleguide: `webapp-02-industrialtechnical_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Industrial Technical Dashboard — Style Guide

---

## Style Summary

### Description

A dark-mode dashboard channeling terminal aesthetics and engineering interfaces through Oswald condensed headers paired with JetBrains Mono body text. The design embraces code-inspired conventions—snake_case naming, code comments (//), bracket syntax ([WARNING])—creating an interface that feels like a living development environment. Dual accents of orange (#FF6B35) and teal (#00D4AA) cut through layered gray surfaces (#1A1A1A through #3D3D3D). Containers are defined by fill color difference rather than borders, and a consistent 16px corner radius softens the industrial vocabulary throughout.

### Key Aesthetics

- **Code-Inspired Conventions:** snake_case labels, // comments, [BRACKET] messages, and 6x6 square status indicators create a developer-native visual language.
- **Layered Gray System:** Four-tier gray hierarchy (#1A1A1A page, #212121 cards, #2D2D2D elevated, #3D3D3D placeholder) defines depth without borders.
- **Dual Accent System:** Orange (#FF6B35) for primary actions and alerts paired with teal (#00D4AA) for success and active states provides clear functional separation.
- **Condensed Headers:** Oswald's narrow letterforms maximize information density in headings while JetBrains Mono brings authentic code-editor readability to body text.
- **Borderless Containers:** No external strokes—structure is communicated entirely through fill color layering.
- **Uniform Rounding:** 16px corner radius applied universally creates a modern, approachable softness atop the industrial foundation.

### Tags

`industrial` · `technical` · `dark-mode` · `monospace` · `developer` · `terminal` · `orange-accent` · `rounded` · `code-inspired` · `webapp`

---

## Color System

The palette builds depth through a four-level gray system where each surface layer is slightly lighter than its parent. Orange and teal serve as the only chromatic accents, strictly separated by function—orange for primary actions, warnings, and emphasis; teal for success, completion, and active states. No borders are used; containers are defined entirely by their fill color against the background.

### Core Backgrounds

- #1A1A1A — Page Background (darkest)
- #212121 — Card, Surface (primary container)
- #2D2D2D — Elevated Surface (secondary container)
- #3D3D3D — Placeholder, inactive fills

### Text Colors

- #FFFFFF — Text Primary
- #777777 — Text Secondary
- #0D0D0D — Text On Orange/Teal (accent backgrounds)

### Accent Colors

- #FF6B35 — Orange; primary actions, alerts, emphasis, CTA buttons
- #00D4AA — Teal; success, active states, completion indicators
- #3D3D3D — Inactive; completed items, disabled states

---

## Typography

The typographic pairing creates a deliberate contrast between display and data. Oswald's condensed, uppercase-friendly forms serve the structural layer—headings, titles, and section labels—where vertical space is at a premium. JetBrains Mono handles everything else—body text, navigation, data values, buttons—where its monospaced grid brings the precision and familiarity of a code editor to the interface.

### Font Families

- **Oswald** — Page titles, section titles, metric values, logo text (condensed sans)
- **JetBrains Mono** — Navigation, body text, labels, buttons, data values, badges (monospace)

### Type Scale

- **36px** — Page Title, Metric Value. Oswald, bold 700
- **20px** — Section Title, Logo. Oswald, semibold 600
- **16px** — Upgrade Title. Oswald, semibold 600
- **13px** — Navigation, Body. JetBrains Mono, normal 400
- **12px** — Label, Button, Table Header. JetBrains Mono, semibold 600
- **11px** — Badge. JetBrains Mono, semibold 600
- **9px** — Code Comment. JetBrains Mono, normal 400

### Font Weights

- **700** — Bold. Page titles, metric values
- **600** — Semibold. Section titles, labels, buttons, table headers, badges
- **400** — Normal. Body text, navigation, code comments, data values

### Letter Spacing

- **0** — Default; all text (no additional tracking)

### Line Height

- **1.5** — Body text; comfortable reading
- **1.0** — Headlines, metrics, labels; single line

---

## Spacing System

### Gap Scale

- **32px** — Major; section gaps between primary blocks
- **24px** — Large; card groups, chart gaps
- **16px** — Medium; internal card sections
- **12px** — Standard; list content gaps
- **10px** — Status; dot indicator spacing
- **8px** — Small; button internal gaps
- **6px** — List; content to metadata
- **4px** — Nav; stacked navigation items
- **2px** — Tight; minimal spacing
- **1px** — Minimal; stacked table rows

### Padding Scale

- **[40, 48]** — Content area (vertical, horizontal)
- **[24, 24]** — Sidebar
- **[20, 20]** — Metric cards, list items
- **[16, 16]** — Upgrade card, card content
- **[12, 16]** — Banner
- **[6, 12]** — Badges
- **[0, 20]** — Buttons (horizontal only)

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **220px** — Sidebar Width (same fill as page background)
- **fill_container** — Content Area (flexible)
- **40px / 48px** — Content Padding (vertical / horizontal)
- **32px** — Section Gap between major sections

---

## Corner Radius

This design uses a **universal 16px corner radius** on all elements, creating a consistent, modern softness that balances the industrial typography and dark color palette. No sharp corners appear anywhere in the interface.

- **16px** — All cards, buttons, containers, inputs, badges, metric cards, banners, sidebar items

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight

### Icons Used

- **Navigation:** layout-grid, trending-up, users, file-text, settings
- **Actions:** search, plus, download, chevron-left, chevron-right
- **Status:** alert-triangle, arrow-up-right, arrow-down-right, square (6x6 status indicators)

### Icon Sizes

- **16px** — Button icons, alert indicators
- **14px** — Navigation arrows, search icon

### Icon Color States

- #0D0D0D — On orange (orange button backgrounds)
- #FFFFFF — Active on dark (content area)
- #FF6B35 — Alert, emphasis
- #777777 — Inactive, Muted
