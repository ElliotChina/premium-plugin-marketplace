# Slide Design Guide for reveal.js

This reference covers visual design, typography, color, layout, and content pacing for reveal.js presentations.

## Table of Contents

1. [Design Principles](#design-principles)
2. [Color Palette Selection](#color-palette-selection)
3. [Slide Content Principles](#slide-content-principles)
4. [Design Review Checklist](#design-review-checklist)
5. [Aesthetic Direction](#aesthetic-direction)
6. [Design Tokens](#design-tokens)
7. [Typography Hierarchy](#typography-hierarchy)
8. [Palette Strategy](#palette-strategy)
9. [Atmosphere and Depth](#atmosphere-and-depth)
10. [Motion as Choreography](#motion-as-choreography)
11. [Asymmetric Layouts](#asymmetric-layouts)
12. [Anti-Generic Design Pass](#anti-generic-design-pass)
13. [Mermaid for Architecture](#mermaid-for-architecture)
14. [Source Document Conversion](#source-document-conversion)
15. [Slide Archetypes](#slide-archetypes)
16. [Compositional Variety](#compositional-variety)
17. [Content Density Limits](#content-density-limits)
18. [Presentation-Scale Typography](#presentation-scale-typography)

---

## Design Principles

Before creating any presentation, analyze the content and choose design elements intentionally:

1. Consider the subject matter: what is this presentation about, and what tone/industry/mood does it suggest?
2. Check for branding: if the user mentions a company or organization, align with likely brand identity and colors.
3. Match palette to content: choose colors that reflect the topic, audience, and communication goal.
4. State your approach first: explain your design choices before writing slide code.

### Required Behavior

- State the content-informed design approach before writing code.
- Use web-safe fonts (`Arial`, `Helvetica`, `Georgia`, `Verdana`, etc.) or Google Fonts via `@import`.
- Create clear visual hierarchy through size, weight, and color.
- Ensure readability with strong contrast, appropriately sized text, and clean alignment.
- Keep visual consistency across slides: repeated spacing, component patterns, and color language.
- **Always use `pt` units for font sizes** in slide CSS/inline styles. Never use `em`, `rem`, or `px` for font-size values.

---

## Color Palette Selection

Choose colors creatively based on the actual content:

- Think beyond defaults: avoid autopilot palettes.
- Consider multiple angles: topic, industry, mood, energy level, audience, and mentioned brand identity.
- Be adventurous when useful: healthcare is not required to be green; finance is not required to be navy.
- Build a 3-5 color system: dominant colors, supporting tones, and accent colors.
- Always verify text/background contrast for readability.

### Palette References

Adapt freely or create your own:

| Name | Colors |
|------|--------|
| Classic Blue | deep navy `#1C2833`, slate gray `#2E4053`, silver `#AAB7B8`, off-white `#F4F6F6` |
| Teal and Coral | teal `#5EA8A7`, deep teal `#277884`, coral `#FE4447`, white `#FFFFFF` |
| Bold Red | red `#C0392B`, bright red `#E74C3C`, orange `#F39C12`, yellow `#F1C40F`, green `#2ECC71` |
| Warm Blush | mauve `#A49393`, blush `#EED6D3`, rose `#E8B4B8`, cream `#FAF7F2` |
| Burgundy Luxury | burgundy `#5D1D2E`, crimson `#951233`, rust `#C15937`, gold `#997929` |
| Deep Purple and Emerald | purple `#B165FB`, dark blue `#181B24`, emerald `#40695B`, white `#FFFFFF` |
| Cream and Forest Green | cream `#FFE1C7`, forest green `#40695B`, white `#FCFCFC` |
| Pink and Purple | pink `#F8275B`, coral `#FF574A`, rose `#FF737D`, purple `#3D2F68` |
| Lime and Plum | lime `#C5DE82`, plum `#7C3A5F`, coral `#FD8C6E`, blue-gray `#98ACB5` |
| Black and Gold | gold `#BF9A4A`, black `#000000`, cream `#F4F6F6` |
| Sage and Terracotta | sage `#87A96B`, terracotta `#E07A5F`, cream `#F4F1DE`, charcoal `#2C2C2C` |
| Charcoal and Red | charcoal `#292929`, red `#E33737`, light gray `#CCCBCB` |
| Vibrant Orange | orange `#F96D00`, light gray `#F2F2F2`, charcoal `#222831` |
| Forest Green | black `#191A19`, green `#4E9F3D`, dark green `#1E5128`, white `#FFFFFF` |
| Retro Rainbow | purple `#722880`, pink `#D72D51`, orange `#EB5C18`, amber `#F08800`, gold `#DEB600` |
| Vintage Earthy | mustard `#E3B448`, sage `#CBD18F`, forest green `#3A6B35`, cream `#F4F1DE` |
| Coastal Rose | old rose `#AD7670`, beaver `#B49886`, eggshell `#F3ECDC`, ash gray `#BFD5BE` |
| Orange and Turquoise | light orange `#FC993E`, grayish turquoise `#667C6F`, white `#FCFCFC` |

---

## Slide Content Principles

Even when slides share similar content types, avoid repeating the same visual pattern.

- Vary layout patterns across neighboring slides (columns, stacked blocks, cards, split hero, quote-led).
- Mix container styles (plain text, styled panels, blockquotes, icon-led callouts).
- Build hierarchy actively (`<strong>`, color emphasis, type scale, spacing rhythm).
- Break up long list sequences with visual elements and structural transitions.
- Do not repeat identical layout structures on consecutive slides.
- Keep slides scannable: short bullets, one main idea per slide where possible.
- Use icons (for example Font Awesome) when they improve clarity and pacing.
- When a slide has less content, increase scale and composition impact instead of leaving sparse tiny text.

---

## Design Review Checklist

Run this before considering a deck "done":

- [ ] Deck defaults to a light tone unless explicitly requested otherwise (prefer official reveal `solarized` theme).
- [ ] Aesthetic direction is explicit and consistent (not mixed styles).
- [ ] Typography has clear hierarchy (display vs body) and readable line lengths.
- [ ] Palette has one dominant tone and one intentional accent color.
- [ ] At least one memorable visual motif exists (layout move, background treatment, or motion sequence).
- [ ] Motion supports narrative pacing (not scattered decorative effects).
- [ ] Architecture/process slides use Mermaid when applicable instead of ad-hoc ASCII bullets.
- [ ] Slides stay readable on both desktop and mobile widths.

---

## Aesthetic Direction

Choose one bold aesthetic direction before styling. Do not start from random colors and utility classes. Define a single visual direction (for example: editorial, brutalist, retro-futuristic, luxury minimal, playful) and keep every design decision aligned with it.

**Practical rule:**
- One deck, one dominant visual idea.
- Keep typography, palette, motion, and background treatment coherent with that idea.

---

## Design Tokens

Create a token layer first, then style components/slides with those tokens.

```css
:root {
  --deck-bg: #f6f3ea;
  --deck-surface: rgba(255, 255, 255, 0.72);
  --deck-text: #1b1a18;
  --deck-accent: #c0392b;
  --deck-muted: #6f6a61;
  --deck-shadow: 0 20px 50px rgba(20, 16, 10, 0.18);
  --deck-radius: 18px;
  --deck-gap: 1.2rem;
}

.reveal {
  color: var(--deck-text);
  background:
    radial-gradient(circle at 12% 18%, rgba(192, 57, 43, 0.12), transparent 45%),
    radial-gradient(circle at 88% 82%, rgba(27, 26, 24, 0.1), transparent 42%),
    var(--deck-bg);
}
```

---

## Typography Hierarchy

Use a distinctive display face for headings and a separate body face for text-heavy slides. Define consistent scale and line length.

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:opsz@9..40&family=Manrope:wght@400;500;700;800&display=swap');

.reveal {
  font-family: 'Manrope', 'Helvetica Neue', Arial, sans-serif;
}

.reveal h1,
.reveal h2,
.reveal h3 {
  font-family: 'DM Serif Display', Georgia, 'Times New Roman', serif;
  letter-spacing: 0.01em;
  line-height: 1.05;
}

.reveal p,
.reveal li {
  line-height: 1.45;
  max-width: 58ch;
}
```

---

## Palette Strategy

Prefer dominant palette + sharp accent over evenly mixed colors. A strong deck usually has:

- One dominant background family.
- One primary text color.
- One high-contrast accent for emphasis, links, and key annotations.

```css
.reveal a,
.reveal strong,
.reveal mark {
  color: var(--deck-accent);
}

.reveal mark {
  background: transparent;
  border-bottom: 0.2em solid color-mix(in srgb, var(--deck-accent) 35%, transparent);
  padding: 0 0.08em;
}
```

---

## Atmosphere and Depth

Compose slides with atmosphere (not flat backgrounds). Avoid plain single-color canvases by default. Add depth with subtle gradients, textures, overlays, or layered shadows that match the chosen aesthetic.

```css
.reveal .panel {
  background: var(--deck-surface);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: var(--deck-radius);
  box-shadow: var(--deck-shadow);
  backdrop-filter: blur(6px);
  padding: calc(var(--deck-gap) * 1.2);
}
```

---

## Motion as Choreography

Use motion as choreography, not decoration. In reveal.js, prioritize:

- One meaningful entry sequence per slide (`fade-up`, `fade-in`, `zoom-in` fragments with stagger).
- Smooth global transition settings.
- Minimal micro-animations elsewhere.

```js
Reveal.initialize({
  transition: 'slide',
  backgroundTransition: 'fade',
  autoAnimateEasing: 'ease-out',
  autoAnimateDuration: 0.6,
});
```

```html
<section>
  <h2 class="fragment fade-in">Problem</h2>
  <p class="fragment fade-up">Constraint</p>
  <p class="fragment fade-up">Decision</p>
  <p class="fragment fade-up">Outcome</p>
</section>
```

---

## Asymmetric Layouts

Break predictable layouts with controlled asymmetry. Avoid centering everything. Mix alignment, width, overlap, and whitespace intentionally.

```css
.reveal .asym {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 2rem;
  align-items: end;
}

.reveal .asym .media {
  transform: translateY(1rem);
}
```

---

## Anti-Generic Design Pass

Before shipping, quickly verify:

- Font choice is intentional and not default/generic.
- Color system has a dominant tone plus a clear accent.
- At least one memorable visual motif exists (background treatment, type lockup, layout move, or motion sequence).
- Slide density is controlled; no wall-of-text pages.
- Mobile viewport still preserves hierarchy and readability.

---

## Mermaid for Architecture

For system overviews, sequence explanations, data flow, and decision logic, use Mermaid slides first. This usually communicates structure faster than dense bullet lists.

```html
<section>
  <h2>Architecture</h2>
  <pre class="mermaid">
flowchart LR
  Client["Client"] -->|HTTPS| API["API Gateway"]
  API --> Service["Application Service"]
  Service --> DB["PostgreSQL"]
  Service --> Queue["Background Queue"]
  Queue --> Worker["Worker"]
  </pre>
</section>
```

If Mermaid plugin setup is needed:

```js
Reveal.initialize({
  hash: true,
  plugins: [RevealMermaid],
});
```

**Decision rule:**
- Use Mermaid for complex graphs (branching/cycles/cross-links, usually 8+ nodes).
- For simple linear pipelines (`A -> B -> C -> D`), prefer HTML/CSS step cards because they fill slide space better and are easier to style at presentation scale.
- Never leave a tiny Mermaid graph alone in large empty space; pair it with supporting content or switch to a split layout.

---

## Source Document Conversion

Convert source documents with full coverage (no silent drops). When turning a plan/spec/review into slides:

- Inventory every source item first (sections, tables, cards, decisions, details).
- Map each item to slide(s) before writing markup.
- Verify coverage at the end: no major section from source should be missing in the deck.

If one source section has high density, split into multiple slides instead of compressing into unreadable bullets.

---

## Slide Archetypes

Use slide archetypes to control pacing. Build deck rhythm with explicit slide roles, not repeated generic content slides:

| Archetype | Purpose |
|-----------|---------|
| Title | Opening tone |
| Divider | Between major topics |
| Content | Explanation |
| Split | Comparison (before/after, text+diagram, problem/solution) |
| Diagram | Structure/flow |
| Dashboard | Metrics/KPIs |
| Table | Compact factual comparison |
| Code | Implementation detail |
| Quote | Emphasis |
| Full-bleed | Key visual moments |

Avoid long runs of the same archetype.

---

## Compositional Variety

Enforce compositional variety across consecutive slides. Alternate spatial compositions through the sequence:

- centered
- left-heavy
- right-heavy
- split
- edge-aligned
- full-bleed

**Rule of thumb:** do not use 3 consecutive slides with the same composition pattern.

---

## Content Density Limits

Keep presentation density within slide limits:

| Slide Type | Limit |
|------------|-------|
| Content slide | 1 heading + up to 5-6 bullets (max ~2 lines each) |
| Diagram slide | One primary diagram, usually up to 8-10 nodes at presentation size |
| Table slide | Up to ~8 rows; overflow moves to next slide |
| Code slide | Up to ~10 lines focused on one point |
| Quote slide | Short quote only; long quotes become content slides |

If limits are exceeded, split into additional slides instead of shrinking text.

---

## Presentation-Scale Typography

Slides are not documents; scale text for screen-share/projector readability. Use `pt` units throughout:

| Element | Size Range (pt) |
|---------|-----------------|
| Display/title | 36–90 pt |
| Heading | 21–36 pt |
| Body/bullets | 12–18 pt |
| Labels/captions | 8–11 pt |

Always prioritize readability from distance over document-like density.
