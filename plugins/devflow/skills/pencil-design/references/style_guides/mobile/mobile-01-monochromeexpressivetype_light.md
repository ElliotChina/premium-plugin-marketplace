# Use the following style guide in the current design task

## Name of the styleguide: `mobile-01-monochromeexpressivetype_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Monochrome Expressive Type Mobile Dashboard — Style Guide

---

## Style Summary

### Description

A pure white canvas mobile interface that transforms typography into the primary design element. Anton display font at dramatic scales (32–72px) delivers bold poster-style headlines in all-caps while Crimson Text serif provides elegant, italicized body content. The design embraces a strict monochrome palette—pure black, pure white, and calibrated grays—with no accent colors whatsoever. Typography itself serves as the status system through expressive symbols (✓, ◐, ○, →) replacing traditional checkbox UI. Cards use flat fills (black or light gray) without borders or shadows. Suited for editorial apps, reading tools, and minimalist productivity applications targeting users who appreciate dramatic typography and publication-quality aesthetics.

### Key Aesthetics

- **Poster Typography:** Anton display at 32–72px creates dramatic, poster-scale headlines in all-caps with wide letter-spacing (+2px).
- **Editorial Serifs:** Crimson Text italic for body content, descriptions, and meta text brings publication-quality refinement.
- **Pure Monochrome:** Zero accent colors. All differentiation through typography scale, weight, and black/white/gray fills.
- **Typography as UI:** Expressive symbols (✓, ◐, ○, →, ↓, ↑) replace traditional checkbox and icon-based status indicators.
- **Flat Fills Only:** No borders, no shadows—hierarchy from fill color contrast (black/white/gray) and spatial separation.
- **Sharp Geometry:** Zero corner radii throughout. Traditional bottom navigation with Anton all-caps labels.

### Tags

`mobile` · `light-mode` · `monochrome` · `editorial` · `typographic` · `serif` · `display` · `high-contrast` · `minimal` · `poster`

---

## Color System

This is a strictly monochrome design. Pure black for primary elements and display type. Pure white for backgrounds and reverse text. Calibrated grays for secondary hierarchy. Typography symbols replace colored status indicators. Visual interest comes entirely from type scale and weight.

### Core Backgrounds

- #FFFFFF — Page Background (pure white)
- #F5F5F5 — Card Surface Light (gray)
- #000000 — Card Surface Dark (black)

### Text Colors

- #000000 — Text Primary (pure black)
- #666666 — Text Secondary (descriptions)
- #888888 — Text Tertiary (labels)
- #999999 — Text Muted (meta, timestamps)
- #CCCCCC — Text Disabled (inactive, empty markers)

### Border Colors

- #E5E5E5 — Border Subtle; list row dividers, navigation top stroke

### Accent Colors

- None. This design uses no accent colors. All differentiation through typography scale, weight, and black/white/gray fills.

---

## Typography

The dual-font system creates editorial drama—Anton handles the commanding display layer (headlines, section headers, labels, symbols), Crimson Text handles the refined editorial layer (body content, descriptions, titles). The extreme scale range (72px to 10px) creates hierarchy through size contrast alone.

### Font Families

- **Anton** — Headlines, section headers, labels, navigation labels, status symbols, badges, buttons (condensed display sans-serif)
- **Crimson Text** — Body content, descriptions, list titles, accordion content, program descriptions (transitional serif, often italic)

### Type Scale

- **72px** — Hero Title. Anton, normal, letterSpacing: -2, lineHeight: 0.85
- **42px** — Metric Value. Anton, normal, letterSpacing: -1, lineHeight: 0.9
- **32px** — Section Header, Week Percentage. Anton, normal, letterSpacing: 2 / +1px
- **28px** — Program Title. Anton, normal, letterSpacing: 1, lineHeight: 0.9
- **24px** — Status Symbol, Progress Label. Anton, normal
- **18px** — List Title, Arrow/Symbol, Time. Anton / Crimson Text, semibold 600
- **16px** — Body, Accordion Title. Crimson Text, normal / semibold 600
- **14px** — Callout, Description, Segment Label. Crimson Text, italic / Anton, letterSpacing: 2
- **13px** — Subhead, Timestamp. Crimson Text, italic
- **12px** — Button Label, Day Label. Anton, letterSpacing: 2 / +1px
- **11px** — Badge Label. Anton, letterSpacing: 2, uppercase
- **10px** — Tab Label. Anton, letterSpacing: 2, uppercase

### Typography as UI

- **✓** — (Anton 24px) Completed items
- **◐** — (Anton 24px) In progress items
- **○** — (Anton 24px) Not started items
- **→** — (Anton 18px) Accordion closed
- **↓** — (Anton 18px) Accordion expanded
- **↑/↓** — (Anton 14px) Metric positive/negative change

### Font Weights

- **600** — Semibold. Crimson Text titles, list item headers
- **400** — Normal. All Anton text, Crimson Text italic body

### Letter Spacing

- **-2px** — Hero headlines (72px, very tight)
- **-1px** — Metric values (tight)
- **+2px** — Section headers, labels, badges, tabs (wide)
- **+1px** — Program titles, progress numbers (slightly wide)
- **0** — Default; Crimson Text body

### Line Height

- **1.5** — Readable; paragraph content, accordion answers
- **0.9** — Tight; multi-line display titles, metrics
- **0.85** — Hero; 72px display (extremely tight)
- **auto** — Default; single-line elements

---

## Spacing System

### Gap Scale (between elements)

- **32px** — Major; section gaps
- **20px** — Large; internal padding, schedule content
- **16px** — Standard; row padding, accordion, section gaps
- **12px** — Medium; program card internal, horizontal card gap
- **8px** — Standard; day column gaps
- **4px** — Tight; metric label gaps, nav icon to label
- **2px** — Minimal; title + description pairs

### Padding Scale

- **[20, 20]** — Content wrapper
- **[24, 20]** — Program cards
- **[24, 16]** — Metric cards (vertical, horizontal)
- **[20, 0]** — Habit rows (vertical only)
- **[16, 16]** — Accordion rows
- **[10, 16]** — Add button
- **[16, 20, 34, 20]** — Bottom navigation

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **20px** — Content Padding (all around)
- **32px** — Section Gap (vertical)
- **16px** — Card Gap (within sections)
- **200px** — Program Card Width (fixed)

---

## Corner Radius

Every element uses sharp corners. The complete absence of rounded corners creates a dramatic, editorial quality reminiscent of print magazine layouts and poster design.

- **0px** — ALL elements (cards, indicators, segments, navigation, buttons)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)
- Many UI elements use typography symbols instead of icons (✓, ◐, ○, →, ↓, ↑, +)

### Icons Used

- **Navigation:** home, check-square, bar-chart, user (with Anton labels)
- **Actions:** bell, search

### Icon Sizes

- **24px** — Navigation (bottom nav icons)
- **20px** — Notification (header bell)
- **18px** — Search

### Icon Color States

- #000000 — Active navigation (black)
- #CCCCCC — Inactive navigation (gray)
- #999999 — Search, notification (muted)
