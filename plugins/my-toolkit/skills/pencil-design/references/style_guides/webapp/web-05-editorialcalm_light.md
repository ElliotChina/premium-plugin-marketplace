# Use the following style guide in the current design task

## Name of the styleguide: `web-05-editorialcalm_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Editorial Calm Landing Page - Style Guide

---

## Style Summary

### Description

A literary-minimalist landing page that channels the quiet confidence of a high-end print journal. The entire design is deliberately anti-SaaS—no hero images, no gradient buttons, no card grids. Instead, it relies on a careful serif/sans-serif typographic pairing, a narrow green-gray monochrome palette, and extreme whitespace to build trust through restraint. Content sits directly on a pure white background with no containers or visual chrome. The only graphic elements are small colored indicator dots used inline as subtle markers. Hierarchy comes entirely from typeface contrast—a serif for identity and voice, a sans-serif for utility and support—never from color or decorative weight. Sections flow as a single left-aligned column, separated by near-invisible hairline dividers. CTAs are plain inline text rather than buttons. The overall impression is calm, stoic, and grown-up—a well-typeset contents page that happens to live on the web.

### Key Aesthetics

- **Literary Minimalism:** Extreme restraint defines the entire page—no images, icons, illustrations, shadows, gradients, or rounded corners. Every element earns its place.
- **Dual Typeface Hierarchy:** A serif (Newsreader) carries identity—logo, headlines, feature names. A sans-serif (Inter) handles utility—navigation, labels, body text. The interplay between the two creates all the rhythm the design needs.
- **Green-Gray Monochrome:** Primary and secondary text colors both live in the forest-green/olive-gray family, creating cohesive warmth without ever using black.
- **Typography-Only Structure:** No buttons, cards, badges, or containers. The design trusts its content completely—CTAs are inline text with a small dot, not boxed elements.
- **Generous Whitespace:** Sections breathe with 60–80px padding. Whitespace is structural, giving the page its calm, unhurried pace.
- **Print Sensibility:** The page reads like a book cover or journal contents page—sparse uppercase labels, serif chapter-like headings, and flat scannable index rows.
- **Muted Indicator Dots:** Small colored circles (14px) serve as the only graphic device, used inline next to list items. Their earthy palette feels hand-mixed rather than digital.

### Tags

`light-mode` · `literary` · `minimal` · `serif` · `calm` · `green-gray` · `whitespace` · `print` · `typography-only`

---

## Color System

A pure white canvas with no ornamentation. All text lives in a narrow green-gray range—warm and serious, never black. The only color variety comes from small inline indicator dots whose earthy tones feel hand-mixed.

### Core Backgrounds

- #FFFFFF — Page background; pure white, unadorned

### Text Colors

- #1E3322 — Primary text; deep forest green for headlines, navigation, logo, feature names
- #6B7B6B — Secondary text; muted olive-sage for body descriptions, supporting copy
- #2D6B3F — Emphasis text; richer mid-green for CTA text and key callouts

### Accent Colors

- #2D6B3F — Indicator dot; forest green
- #C8C0AD — Indicator dot; warm sand
- #E85D45 — Indicator dot; soft coral
- #D4A020 — Indicator dot; aged gold
- #808A80 — Indicator dot; stone gray

### Dividers

- #F4F5F5 — Hairline separator; bottom-only borders between list rows, barely visible

---

## Typography

### Font Families

- **Newsreader:** — serif; used for logo, headlines, feature/item names (voice and identity)
- **Inter:** — sans-serif; used for navigation, body text, labels, CTA text (utility and support)

### Type Scale

- **~60px** — Hero Headline; Newsreader, normal weight, tight leading
- **~28px** — Brand Logo; Newsreader, medium weight
- **~26px** — Feature/Item Name; Newsreader, normal weight
- **16-18px** — Body / Description; Inter, regular, comfortable reading size
- **16px** — CTA Text; Inter, semi-bold for emphasis phrase, regular for supporting text
- **14px** — Navigation; Inter, medium, uppercase, letter-spaced
- **14px** — Section Label; Inter, medium, uppercase, letter-spaced

### Font Weights

- **600** — Semi-bold. CTA emphasis text
- **500** — Medium. Logo, navigation, section labels
- **400** — Regular/Normal. Headlines, feature names, body text, descriptions

### Line Height

- **1.6** — Body text; generous, comfortable reading
- **1.12** — Hero Headline; tight, editorial tension
- **1.0** — Logo, navigation, labels; single line

### Letter Spacing

- **+1.5px** — Uppercase navigation items and section labels
- **0** — Default; headlines, body text, feature names

---

## Spacing System

### Gap Scale (between elements)

- **40px** — Navigation link spacing
- **28px** — Section label to list content
- **24px** — Between major elements within a section (headline to subtext)
- **16px** — Within list rows (between name, dot, and description)
- **12px** — CTA inline element spacing (dot to text)

### Padding Scale

Content uses generous, breathing padding. Horizontal padding is consistent across sections to maintain alignment.

- **80px** — All sides; hero section, major content sections
- **60-80px** — Vertical; denser list sections (60px top/bottom)
- **80px** — Horizontal; consistent left/right across all sections
- **24px** — Vertical; header/navigation bar
- **20px** — Vertical; individual list row internal padding

### Layout Pattern

- **1440px** — Screen Width; standard desktop
- **~640px** — Content Max Width; subtext and descriptions constrained for comfortable reading measure
- **Single column** — All content stacks vertically, left-aligned, no grid splits or sidebars
- **Full-width rows** — List/feature rows stretch the content width, separated by hairline bottom borders
- **Inline CTA** — No button containers; CTA is a horizontal row of dot + text elements

---

## Corner Radius

No rounded corners anywhere. The design is entirely rectilinear—sharp edges reinforce the editorial, print-like character.

### Scale

- **0px** — Everything; all frames, sections, and elements use sharp corners
