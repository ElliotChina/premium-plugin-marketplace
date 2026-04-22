# Use the following style guide in the current design task

## Name of the styleguide: `web-04-minimalcorporate_light`

Use the above name in `spawn_agent` if you want to pass it to subagents.

# Minimal Corporate SaaS Landing Page - Style Guide

---

## Style Summary

### Description

A quiet, austere landing page built around a dark-to-light vertical flow—the page opens with a near-black hero and header, then transitions into clean white and soft off-white gray sections below. The visual language is built on just two ideas: background contrast and typographic weight. There are no decorations, no illustrations, no photography, no gradients, and no shadows anywhere. Every section is a flat full-width rectangle of color with text inside it. Typography relies almost entirely on Geist, a neutral geometric sans-serif, with weight and size driving all hierarchy. Headlines use tight negative letter-spacing at large sizes for a compressed, editorial quality. Navigation links sit inside a translucent-bordered pill container on the dark header, and a segmented pill-shaped tab bar appears in the lower sections. The one chromatic accent in the entire design is a muted steel blue, used for a single feature visual block. The restraint is the style.

### Key Aesthetics

- **Dark-to-Light Page Flow:** The page opens with near-black header and hero, then transitions to white and soft gray sections—creating dramatic visual weight at the top that lightens as you scroll.
- **Single Font Family Dominance:** Geist handles all text—headlines, body, navigation, buttons, feature titles. The single workhorse font.
- **Extreme Minimalism:** Zero shadows, zero gradients, zero decorative elements, zero illustrations. The design communicates entirely through typography, whitespace, and background contrast.
- **Generous Uniform Padding:** Every section uses the same large padding on all sides, creating consistent, unhurried breathing room throughout.
- **Pill-Shaped Interactive Elements:** The navigation pill container and segmented tab bar use full border-radius, giving the few interactive elements a soft, modern feel against an otherwise sharp-edged design.
- **Bottom-Pinned Hero Content:** The hero headline and description sit at the bottom of a tall dark section, leaving dramatic empty space above.

### Tags

`dark-to-light` · `minimal` · `corporate` · `single-font` · `pill-shaped` · `austere` · `monochrome` · `geometric` · `flat`

---

## Color System

An extremely limited, nearly monochrome palette. Near-black anchors the top of the page, white and off-white carry the lower sections, and grays handle secondary text. One muted blue accent appears once, as a solid fill behind a feature visual. Its scarcity makes it feel intentional and premium.

### Core Backgrounds

- #0A0A0A — Dark surface; header and hero (near-black with faint warmth)
- #FFFFFF — Primary light surface; white sections
- #f7f8fa — Secondary light surface; soft off-white gray for alternating sections
- #eef0f2 — Tertiary surface; tab bar track background only
- #4A9FD8 — Accent surface; muted steel blue for a single feature visual block

### Text Colors

- #FFFFFF — Primary text on dark; hero headline, logo
- #CCCCCC — Secondary text on dark; description, navigation links (deliberately low-contrast, receding)
- #1A1A1A — Primary text on light; section headlines, feature titles, active tab text
- #666666 — Secondary text on light; body paragraphs, descriptions
- #888888 — Muted text; inactive tab labels only

### Accent Colors

- #4A9FD8 — Muted steel blue; the only chromatic color in the design, used once as a feature image block fill

---

## Typography

### Font Families

- **Geist** — Used for everything: headlines, body, navigation, buttons, feature titles, logo, descriptions. The single workhorse font.
- **Inter** — Used only for tab bar labels. A subtle optical differentiation most people wouldn't consciously notice.

### Type Scale

- **56px** — Hero Headline; medium (500), letterSpacing: -1, lineHeight: 1.1
- **40px** — Section Headlines; medium (500), letterSpacing: -1, lineHeight: 1.1
- **16px** — Body Text; regular (400), lineHeight: 1.4
- **16px** — Feature Titles; semibold (600), lineHeight: 1.4
- **16px** — Logo/Brand; semibold (600)
- **15px** — Tab Labels; medium (500), Inter font
- **14px** — Navigation Links; regular (400), lineHeight: 1.0
- **14px** — Button Text; medium (500), lineHeight: 1.0

### Font Weights

- **600** — Semibold. Logo, feature card titles (the heaviest weight used anywhere—there is no bold 700)
- **500** — Medium. Headlines, button labels, tab labels
- **400** — Regular. Body text, descriptions, navigation links

### Line Height

- **1.4** — Body text and descriptions; comfortable reading
- **1.1** — Headlines (hero and section); tight, modern compression
- **1.0** — Navigation, buttons, single-line elements

### Letter Spacing

- **-1px** — Headlines at 40px+ (tight tracking, the signature typographic move)
- **0** — Default; all other text

---

## Spacing System

### Gap Scale (between elements)

- **70px** — XXL; between section headline and feature grid, between feature columns (unusually wide, gives features a sparse, considered feel)
- **60px** — XL; between tab bar and feature content below
- **40px** — Large; between centered headline group and surrounding content
- **24px** — Content; within hero content stacks (description to buttons)
- **20px** — Medium; between feature headline and description
- **16px** — Standard; between navigation items, header vertical padding
- **12px** — Small; between feature title and description, icon to label in tabs, headline to sub-description

### Padding Scale

Every section uses **80px padding on all sides**—this is the dominant spacing value and creates the design's characteristic generous whitespace.

- **80px** — Section padding (all sides); the universal inset for every content section
- **16px / 80px** — Header padding (vertical / horizontal); horizontal matches section padding so edges align
- **14px / 48px** — Tab padding (vertical / horizontal); wide horizontal for comfortable hit targets
- **14px / 20px** — Button padding (vertical / horizontal); compact and uniform across all button types

### Layout Pattern (Stacked Full-Width Sections)

Sections stack vertically at full width with no gaps between them. Transitions happen as clean horizontal color cuts. Two-column layouts appear within sections for hero content and feature showcases.

- **1440px** — Screen Width; standard desktop
- **Vertical stacking** — All sections full-width, no gaps between them
- **~50/~50%** — Hero Split; headline left, description + buttons right, space_between
- **3 columns** — Feature Grid; evenly spaced with 70px gap
- **~50/~50%** — Feature Showcase; text left, visual block right, 70px gap
- **640px** — Hero Height; tall section with content pinned to bottom
- **~640px** — Centered text max-width; for comfortable reading in centered sections

---

## Corner Radius

The page is mostly sharp rectangles. Rounded corners appear only on interactive elements and one feature card. The contrast between sharp section edges and rounded interactive elements is deliberate—roundness signals interactivity.

### Scale

- **9999px** — Tab bar track and individual tab segments (full pill shape); the most distinctive shape in the design
- **16px** — Feature image/visual card only
- **8px** — Buttons and navigation pill container; subtle softening that signals interactivity
- **0px** — Everything else; sections, page frame, all structural elements
