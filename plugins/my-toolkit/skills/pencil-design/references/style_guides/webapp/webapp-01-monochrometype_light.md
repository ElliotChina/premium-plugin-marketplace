# Use the following style guide in the current design task

## Name of the styleguide: `webapp-01-monochrometype_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Monochrome Type Dashboard — Style Guide

---

## Style Summary

### Description

A refined editorial dashboard combining a pure black sidebar (#000000) with a soft gray content area (#F5F5F5), where typography is the hero. The design elevates Instrument Serif—an elegant italic serif—to display headlines, metric values, and status badges, creating a sophisticated publication aesthetic. Inter provides clean readability for UI elements and body text. Navigation uses numbered prefixes (01, 02, 03) for editorial structure. The purely monochromatic palette relies on black, white, and grays without any color accents, letting typographic contrast carry the visual hierarchy. Suited for premium analytics platforms, editorial dashboards, and sophisticated business applications.

### Key Aesthetics

- **Typography as Design:** Instrument Serif (always italic) carries all visual personality for display elements; Inter handles all functional UI text.
- **Pure Monochrome:** No color accents whatsoever—black, white, and grays only. Status communicated through typography weight and gray tones.
- **Editorial Structure:** Numbered navigation (01, 02, 03) creates publication-style hierarchy. Text-based status badges use italic serif words instead of colored pills.
- **Stark Contrast:** Pure black sidebar (#000000) against soft gray content (#F5F5F5). White cards (#FFFFFF) float on the gray canvas.
- **Inverted Sections:** Activity feed uses black background for contrast variety within the layout.
- **Zero Decoration:** No shadows, gradients, or rounded corners. Minimal icons—typography and text arrows handle most communication.

### Tags

`editorial` · `monochrome` · `typography` · `webapp` · `serif` · `elegant` · `publication` · `black-white` · `minimal` · `sophisticated`

---

## Color System

This design uses no color accents whatsoever. Positive, negative, and neutral states are communicated through typography weight and gray tones. Active states use black/white contrast rather than colored highlights. The entire palette lives in the grayscale spectrum.

### Core Backgrounds

- #F5F5F5 — Page Background (soft gray canvas)
- #000000 — Sidebar Background (pure black)
- #FFFFFF — Card Background (pure white, floating on gray)
- #000000 — Dark Section Background (inverted sections like activity feed)
- #DDDDDD — Placeholder/Image (light gray)

### Text Colors

- #000000 — Text Primary (headlines, primary content on light)
- #FFFFFF — Text Primary on Dark (headlines on black sections)
- #666666 — Text Secondary (descriptions, inactive nav)
- #888888 — Text Tertiary (labels, muted badges)
- #AAAAAA — Text Muted (placeholders, timestamps)

### Accent Colors

- #000000 — Primary Action; filled buttons, bars, active states
- #FFFFFF — Inverse Action; card backgrounds, text on dark, active pagination
- #CCCCCC — Neutral; unchanged indicators
- #F0F0F0 — Border Light; table borders, subtle dividers on light surfaces
- #222222 — Border Dark; dividers on dark surfaces, avatar background

---

## Typography

The dual-font system creates deliberate emotional separation—Instrument Serif (always italic) handles the aspirational layer (what inspires and impresses), Inter handles the functional layer (what you read and interact with). Without color accents, typography alone must carry the entire visual hierarchy.

### Font Families

- **Instrument Serif** — Page titles, section headers, metric values, logo, badges, card titles. Always italic (fontStyle: "italic")
- **Inter** — Navigation text, buttons, body copy, metadata, table content, labels

### Type Scale

- **64px** — Page Title. Instrument Serif, italic, normal weight
- **44px** — Metric Value. Instrument Serif, italic
- **24-32px** — Section Title. Instrument Serif, italic
- **28px** — Logo Text. Instrument Serif, italic
- **20px** — Card Title. Instrument Serif, italic
- **18px** — Upgrade Label. Instrument Serif, italic
- **14-16px** — Badge. Instrument Serif, italic (status text)
- **16px** — Navigation. Inter, normal 400
- **13-14px** — Body, Button. Inter, normal/medium
- **12px** — Table Header, Label, Meta. Inter, medium 500 / normal 400

### Font Weights

- **500** — Medium. Buttons, table headers, active text, names
- **400** — Normal. Body text, labels, navigation, descriptions; all Instrument Serif (italic style carries emphasis)

### Font Style

- **Italic** — All Instrument Serif text (headlines, values, badges, titles)
- **Normal** — All Inter text

### Letter Spacing

- **0** — Default; all text

### Line Height

- **1.6** — Body, descriptions; comfortable reading
- **1.0** — Headlines, labels; single line

---

## Spacing System

### Gap Scale (between elements)

- **56px** — Major; content area horizontal/vertical padding, section gaps
- **52px** — Sidebar; logo to nav gap
- **48px** — Content; content area padding
- **32px** — Large; sidebar horizontal padding, sidebar bottom section gap
- **28px** — Card; internal padding, chart/activity section gap
- **24px** — Section; metric cards row gap, gallery items gap, table section gap
- **20px** — Medium-large; metric card gap, card content padding
- **16px** — Standard; navigation gap, bar chart bars gap, banner content gap
- **14px** — Activity; item horizontal gap, account row gap
- **12px** — Medium; action buttons gap, gallery card content gap, bar chart label gap
- **8px** — Small; headline to subhead, pagination items, gallery nav
- **6px** — Tight; metric change arrow to percent, activity item content
- **2px** — Minimal; account info name/email stack

### Padding Scale

- **[48, 48]** — Main content area (all sides)
- **[48, 32]** — Sidebar (all sides)
- **[28, 28]** — Cards, chart sections, activity sections, table sections
- **[20, 0]** — Upgrade box, card content sections, gallery image areas
- **[16, 20]** — Banner
- **[12, 20]** — Primary action buttons
- **[12, 16]** — Search button, date selector
- **[10, 16]** — Export button
- **[10, 14]** — Icon-only buttons, small action buttons

### Layout Pattern

- **1440px** — Screen Width (standard desktop)
- **260px** — Sidebar Width (fixed, #000000)
- **fill_container** — Content Area (flexible, #F5F5F5)
- **48px** — Content Padding (all sides)
- **56px** — Section Gap between major sections
- **4 columns** — Metric Card Grid, equal width, 24px gap
- **3 columns** — Gallery Card Grid, equal width, 24px gap
- **380px** — Activity Feed fixed width

---

## Corner Radius

This design system uses **zero corner radius** throughout, creating sharp editorial edges that complement the typography-driven aesthetic.

- **0px** — All elements (cards, buttons, inputs, bars, badges)
- **20px** — Avatar only (circular/rounded)

---

## Icons

### Icon Style

- **Lucide** — Minimal usage; typography carries most communication

### Icons Used

- **Navigation:** None (numbered prefixes used instead)
- **Actions:** search, calendar, plus, download, x
- **Arrows:** chevron-left, chevron-right, chevron-down
- **Status:** Text arrows (↑ ↓ —) preferred over icon arrows

### Icon Sizes

- **14-18px** — Action button icons, chevrons

### Icon Color States

- #333333 — Active on light (action icons)
- #888888 — Secondary on light (muted actions)
- #FFFFFF — Active on dark (sidebar, dark sections)
- #666666 — Inactive/Muted (secondary elements)
