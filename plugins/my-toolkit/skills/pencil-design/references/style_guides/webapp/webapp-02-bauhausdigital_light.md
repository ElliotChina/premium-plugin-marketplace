# Use the following style guide in the current design task

## Name of the styleguide: `webapp-02-bauhausdigital_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Bauhaus Digital Dashboard — Style Guide

---

## Style Summary

### Description

A vibrant constructivist dashboard built on the primary color triad—red (#E53935), blue (#1E88E5), yellow (#FFC107)—against a clean off-white canvas (#FAFAFA). Geometric shape markers (circle, square, triangle) serve as visual identifiers throughout the interface. Heavy 2px black borders reinforce Bauhaus structural clarity. A compact icon-only sidebar (88px) maximizes content area, while color-coded metric cards and a status dot system provide instant data comprehension. The pairing of Space Grotesk for headings with Space Mono for data creates an industrial yet legible typographic system.

### Key Aesthetics

- **Primary Color Triad:** Red, blue, and yellow as core accents echo Bauhaus color theory; each metric card maps to a specific color (Red 1st, Blue 2nd, Yellow 3rd, Black 4th).
- **Geometric Shape Markers:** Circle (red), square (blue), and triangle (green) identify list items, replacing traditional bullets with constructivist vocabulary.
- **Heavy Structure:** 2px black borders define containers with bold graphic clarity; zero corner radius enforces sharp, architectural edges.
- **Compact Icon Sidebar:** 88px black sidebar with icon-only navigation maximizes the content workspace.
- **Industrial Typography:** Space Grotesk for headings and UI paired with Space Mono for labels and data creates a functional, machine-inspired reading experience.
- **Color-Coded Metrics:** Each metric card is identified by a primary color fill, creating instant visual hierarchy across the dashboard.

### Tags

`bauhaus` · `primary-colors` · `geometric` · `webapp` · `constructivist` · `bold` · `color-blocks` · `industrial` · `functional` · `shapes`

---

## Color System

The palette channels Bauhaus color theory—red, blue, and yellow as primary accents against neutral off-white and black. Color is used structurally rather than decoratively, with each hue assigned a specific functional role. The black sidebar and heavy borders ground the composition while the triad energizes metric cards, status indicators, and navigation states.

### Core Backgrounds

- #FAFAFA — Page Background (off-white)
- #000000 — Sidebar Background
- #FFFFFF — Card Background

### Text Colors

- #000000 — Text Primary
- #777777 — Text Secondary
- #999999 — Text Muted
- #FFFFFF — Text On Dark (sidebar, dark cards)

### Accent Colors

- #E53935 — Red; 1st metric card, circle shape markers, primary action
- #1E88E5 — Blue; 2nd metric card, square shape markers, links
- #FFC107 — Yellow; 3rd metric card, triangle markers, highlights
- #4CAF50 — Success Green; positive indicators, triangle shape markers

---

## Typography

The typographic system pairs two members of the Space family for a cohesive industrial aesthetic. Space Grotesk handles the structural layer—headings, metrics, and UI elements—with bold weight for impact. Space Mono handles the data layer—labels, table content, and technical values—with its monospaced grid lending precision to numerical displays.

### Font Families

- **Space Grotesk** — Headings, page titles, metric values, navigation items, buttons (geometric sans)
- **Space Mono** — Labels, data values, table content, badges (monospace)

### Type Scale

- **48px** — Page Title, Metric Value. Space Grotesk, bold 700, letterSpacing: -2
- **20px** — Gallery Title. Space Grotesk, bold 700
- **16px** — Section Title, Item Title, Subtitle. Space Grotesk, semibold 600
- **14px** — Body, Button. Space Grotesk, semibold 600
- **13px** — Label. Space Mono, medium 500, letterSpacing: 1
- **12px** — Table Header. Space Mono, medium 500, letterSpacing: 1
- **11px** — Badge. Space Mono, normal 400

### Font Weights

- **700** — Bold. Page titles, metric values, gallery titles
- **600** — Semibold. Section titles, items, buttons
- **500** — Medium. Labels, table headers
- **400** — Normal. Body text, badges, data values

### Letter Spacing

- **-2px** — 48px titles and metric values (display compression)
- **+1px** — Section titles, labels, table headers (structured expansion)
- **0** — Default; all other text

### Line Height

- **1.5** — Body text; comfortable reading
- **1.0** — Headlines, metrics, labels; single line

---

## Spacing System

### Gap Scale

- **48px** — Major; section gaps between primary content blocks
- **32px** — Large; sidebar internal gaps
- **24px** — Section; metric card gaps, gallery gaps
- **16px** — Medium; chart bars, banner internal
- **12px** — Standard; header internal gaps
- **8px** — Small; nav icon gaps, gallery nav
- **4px** — Tight; pagination gaps
- **2px** — Minimal; stacked list items

### Padding Scale

- **[48, 48]** — Content area (vertical, horizontal)
- **[32, 0]** — Sidebar (vertical only)
- **[32, 32]** — Chart container
- **[24, 24]** — Metric card content
- **[16, 24]** — Banner
- **[0, 24]** — Buttons (horizontal only)

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **88px** — Sidebar Width (compact icon-only, #000000)
- **fill_container** — Content Area (flexible)
- **48px** — Content Padding (all sides)
- **48px** — Section Gap between major sections
- **160px** — Metric Card Height

---

## Corner Radius

This design uses **zero corner radius** throughout, enforcing the sharp geometric precision of Bauhaus constructivism. The only exceptions are circular elements used as shape markers and avatars.

- **0px** — All cards, buttons, containers, inputs (sharp Bauhaus default)
- **20px** — Avatar circles
- **Full circle** — Logo mark, status dots

---

## Icons

### Icon Style

- **Lucide** — Outlined, consistent stroke weight

### Icons Used

- **Navigation:** layout-grid, trending-up, users, file-text, settings
- **Actions:** search, plus, download, chevron-left, chevron-right
- **Status:** arrow-up-right, arrow-down-right, circle, square, triangle

### Icon Sizes

- **20px** — Navigation icons (sidebar)
- **18px** — Action button icons
- **16px** — Search, pagination arrows
- **14px** — Metric change indicators

### Icon Color States

- #FFFFFF — Active on dark (sidebar navigation)
- #000000 — Active on light (content area)
- #E53935 — Red accent state
- #1E88E5 — Blue accent state
- #FFC107 — Yellow accent state
- #999999 — Inactive, Muted
