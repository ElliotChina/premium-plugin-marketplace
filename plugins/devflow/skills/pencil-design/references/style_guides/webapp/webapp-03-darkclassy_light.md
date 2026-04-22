# Use the following style guide in the current design task

## Name of the styleguide: `webapp-03-darkclassy_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Dark Classy Dashboard — Style Guide

---

## Style Summary

### Description

A refined dark-mode dashboard exuding premium sophistication through layered near-black surfaces, warm vibrant orange accents (#FF5C00), and elegant serif typography for titles. The design creates depth through subtle surface elevation—multiple dark gray tones from #0A0A0B to #2A2A2E—while maintaining warmth via gradient-filled elements and glowing status indicators. Soft rounded corners (6-12px) throughout create an approachable yet professional feel. The dual-font pairing of Inter for UI with DM Mono for data brings clarity, while Instrument Serif headlines add editorial elegance. Perfect for fintech dashboards, analytics platforms, and premium SaaS applications.

### Key Aesthetics

- **Layered Darkness:** Multiple elevation levels (#0A0A0B to #1A1A1D to #2A2A2E) create subtle depth across the interface without relying on shadows.
- **Warm Orange Energy:** Vibrant orange (#FF5C00) with gradient variations (#FF5C00 to #FF8A4C) brings life and energy to the dark canvas.
- **Editorial Elegance:** Instrument Serif for page titles adds refined, magazine-quality sophistication and premium distinction.
- **Soft Precision:** Consistent rounded corners (6-12px) create an approachable professionalism within the dark aesthetic.
- **Luminous Feedback:** Glowing status dots with outer shadow blur and gradient fills add premium polish throughout.
- **Monospace Data:** DM Mono for all financial and metric values maintains data clarity and technical precision.

### Tags

`dark-mode` · `premium` · `noir` · `orange-accent` · `sophisticated` · `gradient` · `soft-corners` · `fintech` · `editorial` · `layered`

---

## Color System

The palette layers near-black surfaces from deep black (#0A0A0B) through elevated charcoal (#2A2A2E), with warm vibrant orange (#FF5C00) as the primary accent. Semantic states use tinted backgrounds at 10% opacity for cohesive softness, while gradient variations on orange add dimension to key interactive elements.

### Core Backgrounds

- #0A0A0B — Page Background (deepest black, root canvas)
- #141417 — Sidebar Background, Card Background (elevated surface)
- #1A1A1D — Surface Elevated (hover states, subtle highlights)
- #111113 — Surface Deeper (table backgrounds, recessed areas)
- #1F1F23 — Border Dark (internal dividers, subtle borders)
- #2A2A2E — Border Elevated (more visible borders, dividers)

### Text Colors

- #FFFFFF — Text Primary (headlines, important content, active nav)
- #ADADB0 — Text Secondary (body content, data values, descriptions)
- #8B8B90 — Text Tertiary (inactive navigation labels)
- #6B6B70 — Text Muted (labels, metadata, placeholders)
- #4A4A4E — Text Disabled (disabled states, hints)

### Accent Colors

- #FF5C00 — Orange Primary; CTAs, active states, accent elements
- #FF8A4C — Orange Light; gradient end point, lighter accent
- #FF5C0018 — Orange Tint 10%; badge backgrounds, hover states
- #FF5C0033 — Orange Tint 20%; highlighted backgrounds
- #22C55E — Success Green; positive states, completion, growth
- #22C55E18 — Success Tint; success badge backgrounds
- #EF4444 — Error Red; negative states, decline, errors
- #6B6B7018 — Inactive Gray; inactive badge backgrounds

---

## Typography

The tri-font system creates clear content hierarchy — Instrument Serif handles the editorial headlines with premium distinction, Inter covers all interface elements with reliable readability, and DM Mono provides precise presentation for data and financial metrics.

### Font Families

- **Instrument Serif** — Page titles only; elegant, editorial, refined (display serif)
- **Inter** — Navigation, buttons, labels, body text, section titles (clean sans-serif)
- **DM Mono** — Metric values, monetary amounts, logo text (technical monospace)

### Type Scale

- **38px** — Page Title. Instrument Serif, normal, letterSpacing: -1
- **32px** — Metric Value. DM Mono, medium 500, letterSpacing: -1
- **20px** — Logo Text. DM Mono, semibold 600, letterSpacing: 4
- **14px** — Section Title, Subtitle, Navigation. Inter, semibold 600 / normal 400
- **13px** — Body, Button Labels. Inter, medium 500
- **12px** — Labels, View All Links. Inter, medium 500, letterSpacing: 0.5
- **11px** — Table Headers, Badges, Meta. Inter, semibold 600 / medium 500, letterSpacing: 0.5
- **10px** — Status Text. Inter, medium 500

### Font Weights

- **600** — Semibold. Section titles, table headers, logo, card titles
- **500** — Medium. Active nav, buttons, badges, metric values, labels
- **400** — Normal. Body text, inactive nav, descriptions, metadata

### Letter Spacing

- **-1px** — Page titles, metric values (tight for elegance)
- **0.5px** — Labels, table headers (subtle openness)
- **4px** — Logo text (expanded for brand presence)
- **0** — Default; all other text

### Line Height

- **1.4** — Body and descriptions; comfortable reading
- **1.0** — Headlines and labels; single line

---

## Spacing System

### Gap Scale

- **40px** — Content area horizontal padding
- **32px** — Major; sidebar top sections gap, content section gaps
- **24px** — Section; sidebar sections gap
- **20px** — Large; chart padding, table padding
- **16px** — Medium; section header to content, list items gap, gallery cards gap, card internal gaps
- **14px** — List item icon to content
- **12px** — Standard; nav icon to label, banner icon to text, action buttons gap, account elements
- **10px** — Search icon to text
- **8px** — Small; button icon to text, navigation items, pagination, bar chart labels
- **6px** — Status indicator groups (dot to label)
- **4px** — Content stacks (title to subtitle in lists, cards)
- **2px** — Tight stacks (account name to email)

### Padding Scale

- [32, 40] — Content area (vertical, horizontal)
- [24, 20] — Sidebar main padding
- 24 — Chart sections
- 20 — Metric cards
- 16 — Upgrade box, gallery content
- [14, 20] — Table header and rows
- [14, 16] — Banner
- [12, 14] — Navigation items
- [10, 16] — Standard buttons, search box
- [6, 12] — Small action buttons (table actions)
- [4, 10] — Status badges (pill shape)

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **260px** — Sidebar Width (fixed)
- **fill_container** — Content Area (flexible)
- **32px / 40px** — Content Padding (vertical / horizontal)
- **32px** — Section Gap between major sections
- **16px** — Card Grid Gap
- **8px** — List Item Gap

---

## Corner Radius

This design uses **consistent soft rounding** throughout, creating an approachable, friendly feel within the dark aesthetic. A graduated scale (6 to 12px) provides visual hierarchy, with full radius (100px) for badges creating distinct pill shapes.

- **12px** — Cards, charts, tables, upgrade box, gallery items
- **10px** — List items, banner
- **8px** — Navigation items, search box, avatars/icons containers, gallery nav
- **6px** — Small buttons, pagination items, small action chips
- **100px** — Pill badges (full radius for rounded ends)
- [4, 4, 0, 0] — Chart bars (rounded top only, flat bottom)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke width

### Icons Used

- **Navigation:** layout-dashboard, chart-line, users, package, file-text, settings
- **Actions:** plus, download, search, x, info, chevron-left, chevron-right, chevron-up
- **Status:** trending-up, trending-down, credit-card, arrow-up-right, user
- **Content:** image, zap

### Icon Sizes

- **32px** — Gallery placeholders
- **18px** — Sidebar navigation
- **16px** — Buttons, actions, search
- **14px** — Change indicators

### Icon Color States

- #FF5C00 — Active, Accent (active navigation, important icons)
- #FFFFFF — Primary on Dark (icons on accent backgrounds)
- #6B6B70 — Default (standard icons, inactive states)
- #4A4A4E — Muted (disabled states)
- #22C55E — Success (positive status)
- #EF4444 — Error (negative status)
