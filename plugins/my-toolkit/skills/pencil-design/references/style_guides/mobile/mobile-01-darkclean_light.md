# Use the following style guide in the current design task

## Name of the styleguide: `mobile-01-darkclean_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Dark Clean Mobile Dashboard — Style Guide

---

## Style Summary

### Description

A sophisticated dark-mode mobile interface that harmonizes elegant serif headlines with clean sans-serif body text for premium, refined clarity. Fraunces serif at medium weight delivers editorial authority while DM Sans provides crisp readability. The design embraces vibrant accent colors—emerald green (#32D583), indigo (#6366F1), and coral (#E85A4F)—that pop dramatically against a deep charcoal foundation (#0B0B0E). Cards float on layered dark surfaces with subtle shadows, and a distinctive floating pill tab bar with gradient fade anchors the bottom navigation. Suited for wellness apps, productivity tools, and premium lifestyle products targeting users who appreciate sophisticated dark interfaces.

### Key Aesthetics

- **Editorial Elegance:** Fraunces serif headlines (500–600 weight) bring magazine-quality refinement; DM Sans handles all functional interface text.
- **Dark Luxury:** Deep charcoal (#0B0B0E) with layered dark surfaces (#16161A, #1A1A1E) creates immersive depth.
- **Vibrant Accents:** Saturated green, indigo, and coral pop against dark backgrounds—enhanced by accent-colored glow shadows.
- **Floating Elements:** Cards with subtle shadows, gradient program cards, and a distinctive floating pill tab bar with gradient fade.
- **Generous Radii:** 16–20px corner radius standard for cards; fully rounded pill navigation (31px).
- **Geometric Indicators:** Circular status indicators with colored fills and strokes for clear state communication.

### Tags

`mobile` · `dark-mode` · `premium` · `clean` · `elegant` · `serif-sans` · `minimal` · `sophisticated` · `refined` · `floating-nav`

---

## Color System

Color creates drama and focal points against darkness. Vibrant accents command attention while layered dark tones create subtle depth. Accent-colored glow shadows reinforce element importance. Most UI remains in dark neutrals with color reserved for energy and emphasis.

### Core Backgrounds

- #0B0B0E — Page Background (deep charcoal)
- #16161A — Card Surface (elevated dark)
- #1A1A1E — Elevated Surface; interactive elements, buttons, tab bar

### Text Colors

- #FAFAF9 — Text Primary (near-white)
- #6B6B70 — Text Secondary (descriptions, labels)
- #4A4A50 — Text Tertiary (inactive, placeholders)
- #8E8E93 — Text Muted (help text, expanded content)

### Border Colors

- #2A2A2E — Border Subtle; card strokes, dividers
- #3A3A40 — Border Strong; emphasized borders, empty states

### Accent Colors

- #32D583 — Green Primary; success, completion, positive states
- #059669 — Green Gradient End
- #6366F1 — Indigo Primary; primary actions, featured elements
- #4F46E5 — Indigo Gradient End
- #E85A4F — Coral Primary; secondary accent, in-progress, CTAs
- #DC2626 — Coral Gradient End
- #FFB547 — Amber; warnings, partial states
- #FFFFFF — Text On Color (white on accent backgrounds)
- #FFFFFFCC — Text On Color Muted (80% white)
- #FFFFFF20 — Badge Overlay (20% white on colored backgrounds)

### Shadow System

- **Card Shadow:** {type:"shadow",offset:{x:0,y:4},blur:16,color:"#00000040"}
- **Subtle Shadow:** {type:"shadow",offset:{x:0,y:2},blur:12,color:"#00000025"}
- **Search Shadow:** {type:"shadow",offset:{x:0,y:1},blur:3,color:"#00000015"}
- **Tab Bar Shadow:** {type:"shadow",offset:{x:0,y:-4},blur:24,color:"#00000040"}
- **Accent Glow Indigo:** {type:"shadow",offset:{x:0,y:8},blur:24,color:"#6366F133"}
- **Accent Glow Green:** {type:"shadow",offset:{x:0,y:8},blur:24,color:"#32D58333"}
- **Accent Glow Coral:** {type:"shadow",offset:{x:0,y:8},blur:24,color:"#E85A4F33"}

---

## Typography

The dual-font system creates deliberate emotional separation—Fraunces handles the aspirational layer (what inspires and impresses), DM Sans handles the functional layer (what you read and interact with). Negative letter-spacing on headlines and metrics creates tight, confident impact.

### Font Families

- **Fraunces** — Headlines, page titles, section headers (variable serif, editorial authority)
- **DM Sans** — Navigation, buttons, labels, body text, metric values (geometric sans-serif)
- **Inter** — Tab bar labels only (system sans-serif)

### Type Scale

- **36px** — Large Metric. DM Sans, bold 700, letterSpacing: -1.2
- **28px** — Large Title. Fraunces, medium 500, letterSpacing: -0.8
- **24px** — Title 1. Fraunces, semibold 600, letterSpacing: -0.5
- **22px** — Section Title. Fraunces, semibold 600, letterSpacing: -0.3
- **18px** — Subsection. Fraunces, semibold 600, letterSpacing: -0.2
- **17px** — Medium Metric. DM Sans, bold 700
- **16px** — Headline. DM Sans, semibold 600
- **16px** — Body. DM Sans, normal
- **15px** — Callout. DM Sans, semibold 600 / bold 700
- **14px** — Subhead, Label. DM Sans, medium 500 / semibold 600
- **13px** — Footnote. DM Sans, normal / medium 500
- **12px** — Caption. DM Sans, medium 500 / semibold 600
- **11px** — Badge. DM Sans, semibold 600
- **10px** — Tab Label. Inter, medium 500 / semibold 600

### Font Weights

- **700** — Bold. Metric values, program titles
- **600** — Semibold. Section titles, active states, emphasis
- **500** — Medium. Labels, headlines, inactive states
- **400** — Normal. Body text, descriptions

### Letter Spacing

- **-1.2px** — Large metrics (very tight for density)
- **-0.8px** — Large title (tight for impact)
- **-0.5px** — Title 1
- **-0.3px** — Section headers
- **0** — Default; body text and labels

### Line Height

- **1.5** — Readable; expanded content, paragraphs
- **1.3** — Standard; status bar, single-line elements
- **1.2** — Compact; metrics

---

## Spacing System

### Gap Scale (between elements)

- **24px** — Section; main content sections
- **16px** — Card; section header to content
- **14px** — Row; habit rows, schedule content
- **12px** — Medium; cards within sections, program cards
- **8px** — Standard; internal card content, day indicators
- **6px** — Small; progress badges, add buttons
- **4px** — Tight; icon to label (tab bar, status pairs)
- **2px** — Minimal; title + description within rows

### Padding Scale

- **[0, 24]** — Content wrapper (horizontal only)
- **[20, 20]** — Cards uniform (metric, program, week)
- **[18, 18]** — Accordion rows, search bar
- **[16, 16]** — List rows, schedule content
- **[8, 14]** — Small buttons
- **[6, 12]** — Progress indicator badges
- **[4, 10]** — Badges and tags
- **[12, 21, 21, 21]** — Tab bar container (includes fade area)

### Layout Pattern

- **402px** — Screen Width (iPhone standard)
- **24px** — Content Padding (horizontal)
- **24px** — Section Gap (vertical)
- **12–16px** — Card Gap (within sections)
- **180px** — Program Card Width (fixed)
- **62px** — Tab Bar Pill Height

---

## Corner Radius

Rounded corners are essential to this design's friendly-yet-premium feel. Generous 16–20px radii on cards create approachable forms while maintaining sophistication. The distinctive pill tab bar (31px) serves as a signature element.

- **31px** — Tab bar pill (fully rounded)
- **20px** — Featured cards, metric cards, program cards
- **18px** — Day indicator circles (week view)
- **16px** — Standard cards, schedule cards, accordion
- **14px** — Status indicator circles (habit rows)
- **12px** — Segmented control container, progress badges
- **10px** — Small buttons
- **8px** — Segmented control items, small badges
- **100px** — Circular buttons (notification)

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight (1.5px)

### Icons Used

- **Navigation:** home, search, calendar, user (tab bar)
- **Actions:** bell, plus, chevron-down, chevron-right, search
- **Status:** check, trending-up, trending-down

### Icon Sizes

- **24px** — Navigation (tab bar icons)
- **22px** — Notification (header bell)
- **20px** — Search, Chevron/Arrows
- **16–18px** — Checkmarks, action buttons
- **14px** — Trend indicators, progress icons

### Icon Color States

- #FAFAF9 — Active navigation (text-primary)
- #6B6B6F — Inactive navigation (muted gray)
- #6B6B70 — Search, chevrons (text-secondary)
- #32D583 — Positive/success status
- #E85A4F — In-progress status
- #FFB547 — Warning/partial status
- #FFFFFF — On accent backgrounds
- #0B0B0E — On green backgrounds (dark)
