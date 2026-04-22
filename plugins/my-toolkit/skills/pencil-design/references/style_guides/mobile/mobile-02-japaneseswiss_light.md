# Use the following style guide in the current design task

## Name of the styleguide: `mobile-02-japaneseswiss_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Japanese Swiss Mobile Dashboard — Style Guide

---

## Style Summary

### Description

Tranquil warm-canvas mobile interface breathing with intentional white space. Inter at light 300 weight delivers an airy, elegant headline while maintaining precision for body text. The design embraces warm off-white (#FAF8F5) as primary background with pure white (#FFFFFF) cards featuring generous 16px corner radius. Deep navy accent (#1E3A5F) provides sophisticated emphasis without harshness. Indented dividers with padded spacing create zen-like rhythm. The iOS 18-style pill tab bar floats as a unified element. Rounded checkboxes (11px radius) and circular week indicators soften the interface. Suited for wellness apps, meditation tools, and lifestyle products targeting users who appreciate calm sophistication and mindful interaction.

### Key Aesthetics

- **Ma (間) White Space:** Intentional emptiness as a design element; wider 28px content padding for generous breathing room.
- **Swiss Clarity:** Precise typography and geometric forms with Inter's clean letterforms.
- **Japanese Restraint:** Minimal palette with deep navy accent (#1E3A5F) and muted semantics—color is meaningful, not decorative.
- **Soft Geometry:** 16px card radius, 11px rounded checkboxes, circular week indicators create gentle transitions.
- **Indented Dividers:** Lines with left padding (52px) for visual breathing room within lists.
- **Floating Pill Tab Bar:** iOS 18-style icon-only navigation (no labels) with 80px pill radius.

### Tags

`mobile` · `light-mode` · `japanese` · `swiss` · `zen` · `minimal` · `calm` · `rounded` · `airy` · `sophisticated`

---

## Color System

Color is applied with Japanese restraint. Warm canvas creates contemplative, calm atmosphere. White cards float above as distinct content zones. Navy accent provides sophisticated emphasis. Most interactions remain within the neutral palette.

### Core Backgrounds

- #FAF8F5 — Page Background (warm off-white)
- #FFFFFF — Card Surface (pure white)
- #F5F3F0 — Surface Muted (slightly warm muted)

### Text Colors

- #1C1C1C — Text Primary (headlines)
- #6B6B6B — Text Secondary (descriptions)
- #9A9A9A — Text Muted (labels, meta)

### Border Colors

- #E8E5E0 — Border Default; dividers, subtle boundaries
- #D4D0C8 — Border Strong; form controls, emphasis

### Accent Colors

- #1E3A5F — Navy Primary; active states, emphasis, CTAs
- #1E3A5F15 — Soft Navy (15% opacity tint)
- #3D6B4F — Status Positive; success states
- #8B4049 — Status Negative; error states

---

## Typography

Single-font system using Inter throughout. Light 300 weight for display headlines creates airy elegance. Medium 500 for section labels and values. The extreme weight contrast between headlines (300) and functional text (500) creates hierarchy through weight alone.

### Font Families

- **Inter** — All text: headlines, body, labels, navigation (neo-grotesque sans-serif)

### Type Scale

- **38px** — Large Title. Inter, light 300, letterSpacing: -0.5, lineHeight: 1.05
- **32px** — Metric Value. Inter, medium 500, letterSpacing: -0.5
- **24px** — Featured Stat. Inter, medium 500
- **18px** — Card Title. Inter, medium 500, letterSpacing: -0.3
- **15px** — Headline, Body. Inter, medium 500 / normal
- **14px** — Callout. Inter, normal
- **13px** — Section Label, Subhead. Inter, medium 500, letterSpacing: 0.3
- **12px** — Footnote. Inter, normal
- **11px** — Caption. Inter, normal / medium 500
- **10px** — Micro Text. Inter, medium 500

### Font Weights

- **600** — Semibold. Active states only
- **500** — Medium. Section labels, values, emphasis
- **400** — Normal. Body text, descriptions
- **300** — Light. Large display headlines only

### Letter Spacing

- **-0.5px** — Display titles (light weight)
- **-0.3px** — Card titles (slight tightening)
- **+0.3px** — Section labels (subtle tracking)
- **0** — Default; body text

### Line Height

- **1.05** — Tight; large display headlines
- **1.15** — Comfortable; program card titles
- **auto** — Default; most elements

---

## Spacing System

### Gap Scale (between elements)

- **28px** — Content wrapper horizontal padding
- **20px** — Content wrapper to header, card internal
- **16px** — Standard; section header to content, row padding
- **14px** — Row; content spacing, schedule cards
- **12px** — Medium; cards within sections
- **10px** — Day indicator to label
- **8px** — Header left, program scroll padding
- **6px** — Small pairs (icon + label)
- **2px** — Tight stacks (title + description)

### Padding Scale

- **[0, 28]** — Content wrapper (horizontal, wider than average)
- **[28, 24]** — Empty state card
- **[20, 18]** — Metric cards
- **[20, 16]** — Program cards, week progress card
- **[16, 16]** — Habit rows, schedule rows, accordion
- **[12, 21, 21, 21]** — Tab bar container

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **28px** — Content Padding (horizontal, wider than average)
- **20px** — Section Gap (vertical)
- **12px** — Card Gap (within sections)
- **160px** — Program Card Width (fixed)

---

## Corner Radius

Corner radius creates the soft, approachable aesthetic. 16px standard radius balances rounded softness with geometric precision. The pill-shaped tab bar (80px) creates a signature floating element. No shadows—depth through color contrast only.

- **80px** — Tab bar pill (full round)
- **60px** — Active tab item (pill within pill)
- **22px** — Empty state icon circle
- **20px** — Notification button
- **16px** — Cards, major containers
- **12px** — Search bar, segmented control container
- **11px** — Checkboxes (rounded square)
- **8px** — Segmented control items
- **2px** — Schedule accent bars

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, check-square, bar-chart, user (icons only, no labels)
- **Actions:** search, bell, plus, chevron-down, chevron-right

### Icon Sizes

- **20px** — Navigation (tab bar)
- **18px** — Notification, search, chevrons
- **14px** — Action buttons
- **12px** — Checkmarks

### Icon Color States

- #FFFFFF — Active navigation (white on navy)
- #9A9A9A — Inactive navigation (muted)
- #3D6B4F — Positive status (green)
- #FFFFFF — On accent backgrounds
