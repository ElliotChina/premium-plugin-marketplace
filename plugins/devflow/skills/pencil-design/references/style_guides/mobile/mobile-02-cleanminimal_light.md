# Use the following style guide in the current design task

## Name of the styleguide: `mobile-02-cleanminimal_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Clean Minimal Mobile Dashboard — Style Guide

---

## Style Summary

### Description

Warm cream canvas mobile interface that feels like a cozy morning. Outfit geometric sans-serif at semibold 600 weight delivers friendly confidence while soft shadows and generous corner radii create approachable depth. The design embraces natural green (#3D8A5A) and terracotta (#D89575) accents that evoke organic warmth. White surface cards float on a warm off-white foundation (#F5F4F1), creating subtle layering through shadow rather than stark contrast. Circular status indicators and pill-shaped controls provide soft geometric rhythm throughout. Metric values use bold weight with negative letter-spacing for confident density. Suited for wellness apps, habit trackers, and lifestyle products targeting users who appreciate gentle sophistication and calming functionality.

### Key Aesthetics

- **Scandinavian Hygge:** Warm cream canvas (#F5F4F1) with pure white floating cards for cozy comfort.
- **Organic Minimalism:** Nature-inspired green (#3D8A5A) and terracotta (#D89575) accents meet geometric precision.
- **Approachable Depth:** Soft shadows (8% opacity, warm-toned) create friendly layering without harshness.
- **Pillow-Soft Shapes:** Generous corner radii (12–16px on cards, 100px pills) create welcoming forms.
- **Friendly Typography:** Outfit semibold 600 for confident warmth, bold 700 for metric impact.
- **Circular Indicators:** Round status markers and pill-shaped controls for playful geometry.

### Tags

`mobile` · `light-mode` · `minimal` · `scandinavian` · `clean` · `warm` · `soft` · `organic` · `friendly` · `rounded`

---

## Color System

Color creates warmth and gentle emphasis. Primary green indicates active states and positive progress. Warm coral provides friendly contrast. Shadows are extremely subtle, adding depth not drama. Most UI remains in warm neutrals.

### Core Backgrounds

- #F5F4F1 — Page Background (warm cream)
- #FFFFFF — Card Surface (white)
- #FAFAF8 — Elevated Surface (slightly warm white)
- #EDECEA — Muted Surface (warm gray for controls)

### Text Colors

- #1A1918 — Text Primary (headlines)
- #6D6C6A — Text Secondary (descriptions)
- #9C9B99 — Text Tertiary (labels, placeholders)
- #A8A7A5 — Tab Inactive (navigation)

### Border Colors

- #E5E4E1 — Border Subtle; card strokes, dividers
- #D1D0CD — Border Strong; form controls, emphasis

### Accent Colors

- #3D8A5A — Primary Green; active states, positive actions, CTAs
- #C8F0D8 — Light Green; progress backgrounds, soft badges
- #4D9B6A — Dark Green; positive metrics, success states
- #D89575 — Warm Coral; secondary accent, schedule markers
- #D08068 — Warm Red; negative metrics, warnings
- #D4A64A — Warning; warning states

### Shadow System

- **Standard Card:** offset (0, 2px), blur 12px, color #1A191808
- **Elevated Card:** offset (0, 2px), blur 8px, color #1A191808
- **Subtle Element:** offset (0, 1px), blur 6px, color #1A191808
- **Active Segment:** offset (0, 1px), blur 2px, color #00000008

---

## Typography

Single-font system using Outfit throughout. Semibold 600 for section headers delivers confident warmth, bold 700 for large metric values provides visual impact. Hierarchy comes from weight and size, with subtle negative letter-spacing on display values.

### Font Families

- **Outfit** — All text: headlines, body, labels, navigation, badges (geometric sans-serif)

### Type Scale

- **32px** — Large Title, Metric Value. Outfit, bold 700, letterSpacing: -1
- **26px** — Screen Header. Outfit, semibold 600, letterSpacing: -0.5
- **22px** — Section Emphasis. Outfit, semibold 600, letterSpacing: -0.3
- **18px** — Section Header. Outfit, semibold 600, letterSpacing: -0.2
- **15px** — Headline, Body. Outfit, medium 500 / normal
- **14px** — Callout. Outfit, medium 500
- **13px** — Subhead. Outfit, medium 500
- **12px** — Footnote. Outfit, normal
- **11px** — Caption. Outfit, semibold 600
- **10px** — Tab Label. Outfit, medium 500–600

### Font Weights

- **700** — Bold. Large metrics, display values
- **600** — Semibold. Headlines, section titles, active states
- **500** — Medium. Labels, subheads, emphasis
- **400** — Normal. Body text, descriptions

### Letter Spacing

- **-1px** — Large metric numbers (tight for impact)
- **-0.5px** — Screen headers
- **-0.2px** — Section titles (slightly tight)
- **0** — Default; body text and labels

### Line Height

- **1.5** — Readable; expanded content, paragraphs
- **1.4** — Standard; descriptions, meta text
- **1.2** — Compact; single-line elements, metrics
- **auto** — Default; most elements

---

## Spacing System

### Gap Scale (between elements)

- **24px** — Major; section gaps
- **20px** — Large; week card padding
- **16px** — Standard; component spacing
- **14px** — Row; habit row content
- **12px** — Medium; cards within sections, search internals
- **10px** — Program card internal
- **8px** — Internal card content
- **6px** — Small element groups
- **4px** — Icon to label (navigation)
- **2px** — Tight stacks (title + description)

### Padding Scale

- **[0, 24]** — Content wrapper (horizontal)
- **[20, 20]** — Week progress card
- **[18, 18]** — Metric cards
- **[16, 18]** — List rows
- **[16, 16]** — Program cards
- **[12, 0, 34, 0]** — Tab bar (includes safe area)
- **[4, 8]** — Small badges and tags

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **24px** — Content Padding (horizontal)
- **24px** — Section Gap (vertical)
- **12px** — Card Gap (within sections)
- **160px** — Program Card Width (fixed)

---

## Corner Radius

Rounded corners are central to this design language. Generous radii create approachable, friendly forms. Full-round elements provide playful contrast for interactive components.

- **100px** — Pills, circular buttons, avatars (full round)
- **20px** — Large featured cards
- **16px** — Cards, major containers
- **12px** — Search bars, inputs, buttons, segmented control container
- **8px** — Secondary elements
- **6px** — Segmented control items, small buttons
- **4px** — Small badges, tags

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, check-square, bar-chart, user (with labels)
- **Actions:** search, bell, plus, chevron-down, chevron-right

### Icon Sizes

- **22px** — Navigation (tab bar)
- **20px** — Notification bell
- **18px** — Search, chevrons
- **16px** — Action buttons
- **14px** — Trend indicators, checkmarks

### Icon Color States

- #3D8A5A — Active navigation (primary green)
- #A8A7A5 — Inactive navigation (gray)
- #9C9B99 — Search, chevrons (muted)
- #4D9B6A — Positive status (green)
- #D08068 — Negative status (warm red)
- #FFFFFF — On dark/colored backgrounds
