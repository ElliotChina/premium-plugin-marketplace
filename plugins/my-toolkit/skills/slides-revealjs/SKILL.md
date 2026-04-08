---
name: slides-revealjs
description: Create professional reveal.js HTML presentations. Trigger when the user wants to create or modify slides, presentations, decks, pitch decks, talks, or any slide-based content — including converting outlines or notes into slides. Also use when the user mentions reveal.js or asks to edit/update an existing HTML presentation.
---

# Reveal.js Presentations

Create HTML presentations using reveal.js. No build step required - just open the HTML in a browser.

## What You Create

A reveal.js presentation consists of:

1. **HTML file** - Contains slides and loads reveal.js from CDN
2. **CSS file** - Custom styles for layouts, colors, typography, and components

## Design Principles

**CRITICAL**: Before creating any presentation, analyze the content and choose appropriate design elements:

1. **Consider the subject matter**: What is this presentation about? What tone, industry, or mood does it suggest?
2. **Check for branding**: If the user mentions a company/organization, consider their brand colors and identity
3. **Match palette to content**: Select colors that reflect the subject
4. **State your approach**: Explain your design choices before writing code

**Requirements**:
- ✅ State your content-informed design approach BEFORE writing code
- ✅ Use web-safe fonts (Arial, Helvetica, Georgia, Verdana, etc.) or Google Fonts via `@import` in CSS
- ✅ Create clear visual hierarchy through size, weight, and color
- ✅ Ensure readability: strong contrast, appropriately sized text, clean alignment
- ✅ Be consistent: repeat patterns, spacing, and visual language across slides
- ✅ **Always use `pt` (points) for font sizes** - slides are fixed-size, so `pt` is predictable and familiar (like PowerPoint/Keynote). Never use `em`, `rem`, or `px` for font sizes.

### Color Palette Selection

**Choosing colors creatively**:
- **Think beyond defaults**: What colors genuinely match this specific topic? Avoid autopilot choices.
- **Consider multiple angles**: Topic, industry, mood, energy level, target audience, brand identity (if mentioned)
- **Be adventurous**: Try unexpected combinations - a healthcare presentation doesn't have to be green, finance doesn't have to be navy
- **Build your palette**: Pick 3-5 colors that work together (dominant colors + supporting tones + accent)
- **Ensure contrast**: Text must be clearly readable on backgrounds

**Example color palettes** (use these to spark creativity - choose one, adapt it, or create your own):

1. **Classic Blue**: Deep navy (#1C2833), slate gray (#2E4053), silver (#AAB7B8), off-white (#F4F6F6)
2. **Teal & Coral**: Teal (#5EA8A7), deep teal (#277884), coral (#FE4447), white (#FFFFFF)
3. **Warm Blush**: Mauve (#A49393), blush (#EED6D3), rose (#E8B4B8), cream (#FAF7F2)
4. **Burgundy Luxury**: Burgundy (#5D1D2E), crimson (#951233), rust (#C15937), gold (#997929)
5. **Black & Gold**: Gold (#BF9A4A), black (#000000), cream (#F4F6F6)
6. **Sage & Terracotta**: Sage (#87A96B), terracotta (#E07A5F), cream (#F4F1DE), charcoal (#2C2C2C)

For more palettes (18+ options including dark/light backgrounds), see [references/color-palettes.md](references/color-palettes.md).

### Slide Content Principles

**Diverse presentation is key.** Even when slides have similar content types, vary the visual presentation:

- Use **different layouts** across slides: columns on one, stacked containers on another, styled cards on a third
- Mix container styles: plain text, custom styled containers, blockquotes
- Use **visual hierarchy**: `<strong>` for key terms, different colors to distinguish categories
- Break up lists with other elements (quotes, styled containers, columns)
- Don't repeat the same layout pattern on consecutive slides

**Keep it scannable:**
- Short bullet points, not paragraphs
- One main idea per slide when possible
- Use icons (Font Awesome) to add visual interest

**When a slide has less content, make it bigger** - don't leave empty space with tiny text.

## Reference Index

Two reference files are loaded for every presentation (after Step 2). All others are loaded only when needed.

| Feature | Reference | When to load |
|---------|-----------|-------------|
| Layout patterns | [layouts.md](references/layouts.md) | **Always** — loaded after Step 2 |
| Color palettes | [color-palettes.md](references/color-palettes.md) | **Always** — loaded after Step 2 |
| Animations & transitions | [animations.md](references/animations.md) | Content should appear progressively, auto-animate between slides, custom transition effects |
| Charts & data | [charts.md](references/charts.md) | Any bar, line, pie, doughnut, radar, or scatter chart (**MUST read before adding charts**) |
| Diagrams | [diagrams.md](references/diagrams.md) | Flowcharts, sequence diagrams, class diagrams, or any Mermaid diagram |
| Visuals & media | [visuals.md](references/visuals.md) | Custom backgrounds (gradient, image, video), lightbox previews, speaker notes |
| Code & math | [code-slides.md](references/code-slides.md) | Code blocks with syntax highlighting, math formulas ($...$, $$...$$), or Markdown-authored slides |
| Interaction | [interaction.md](references/interaction.md) | Internal slide links, custom navigation, keyboard shortcuts, slide states |
| Advanced JS API | [advanced-dev.md](references/advanced-dev.md) | JavaScript API, event listeners, custom keyboard bindings, multiple presentations |
| Plugins | [plugins.md](references/plugins.md) | Any plugin not in the scaffold (Notes, Search, Zoom, Highlight, Math, Markdown, Mermaid, Animate, D3, Fullscreen) |
| Full API & internals | [official-docs/](references/official-docs/) | Deep dive into reveal.js source documentation — only needed for advanced customization not covered above |

**Quick syntax** (no reference file needed):
- **Vertical slides**: nest `<section>` elements inside a parent `<section>` for vertical navigation
- **Slide numbers**: set `slideNumber: true` in config, or `"c/t"` for current/total format
- **Pause**: press `B` to pause (dims screen), press again to resume
- **PDF export**: add `?print-pdf` to the URL, then Ctrl+P in Chrome
- **Scroll view**: add `?view=scroll` to the URL for a scrollable web page
- **Slide visibility**: `data-visibility="hidden"` to exclude from navigation

## Workflow

### Branch A: Modifying an Existing Presentation

When the user asks to edit, update, or add slides to an existing reveal.js HTML file:

**A1. Read the existing file** — Understand the current structure: slide count, CSS variables, plugins in use, overall theme.

**A2. Identify needed reference files** — Load references based on what the user wants to add (charts → charts.md, diagrams → diagrams.md, etc.). Also load [layouts.md](references/layouts.md) and [color-palettes.md](references/color-palettes.md) if making significant additions.

**A3. Edit incrementally** — Use the Edit tool to modify the file. Never rewrite the entire file with Write. Insert new `<section>` elements before the closing `</div></div>` of the `.slides` container. Reuse the existing CSS variables (`var(--primary-color)`, `var(--secondary-color)`, etc.) — do not hardcode colors.

**A4. Validate** — Run `check-overflow.js` and `check-charts.js` (if charts were added) as described in Step 5.

**A5. Preview** — Start the preview server as described in "Preview the Presentation".

### Branch B: Creating a New Presentation

### Step 1: Plan the Structure

Analyze the user's request to understand what the presentation needs, then load only the relevant reference files.

**1a. Analyze requirements** — Based on the user's content, determine:
- How many slides are needed
- Which slides should be section dividers (centered, larger text)
- Where to use vertical slide stacks for drill-down content

**1b. Identify needed features** — Based on the user's topic and content, infer which features would best serve the presentation. The user may not explicitly mention features like "charts" or "animations" — it's your job to determine what visual approach fits their content.

Examples of inferring needs from context:
- "Q4 financial review" → likely needs charts (financial data), stat boxes
- "Technical architecture talk" → likely needs diagrams, code highlighting, animations
- "Team offsite agenda" → simple text, maybe timeline — no charts or code needed
- "Product launch" → likely needs animations, visuals (backgrounds), image+text layouts

Do NOT preload reference files speculatively. If the user's request is simple text-only content, skip all reference files and proceed to Step 2.

**1c. Load selected references** — Read each identified reference file before proceeding. Apply this knowledge during Step 4 when filling in slide content.

### Step 2: Generate the Scaffold

Use the `create-presentation.js` script (located in the `scripts/` directory next to this SKILL.md file) to generate the HTML scaffold.

```bash
node <path-to-skill>/scripts/create-presentation.js --structure 1,1,d,3,1,d,1 --title "My Presentation" --output presentation.html
```

**Finding the script path:** The script is at `scripts/create-presentation.js` relative to where this SKILL.md file is located. Common locations:
- Project skill: `.claude/skills/revealjs/scripts/create-presentation.js`
- User skill: `~/.claude/skills/revealjs/scripts/create-presentation.js`

**Options:**
- `--slides N` - Create N horizontal slides (simple mode)
- `--structure <list>` - Mixed layout with comma-separated values:
  - `1` = single horizontal slide
  - `N` (where N > 1) = vertical stack of N slides
  - `d` = section divider slide (centered, no content wrapper)
- `--output <file>` - Output filename (default: presentation.html)
- `--title <text>` - Presentation title
- `--styles <file>` - Custom CSS filename (default: styles.css)

**Examples:**
```bash
# 10 horizontal slides
node <path-to-skill>/scripts/create-presentation.js --slides 10 --output presentation.html

# Mixed structure: intro, 2 content slides, divider, 3-slide vertical stack, divider, closing
node <path-to-skill>/scripts/create-presentation.js --structure 1,1,1,d,3,d,1 --title "Q4 Review" --output presentation.html
```

### Step 2.5: Load Required References

Read these two reference files — they are needed for every presentation:
1. [layouts.md](references/layouts.md) — layout patterns for slide content
2. [color-palettes.md](references/color-palettes.md) — color palette options for theme customization

These are loaded after scaffold generation so you know the presentation structure and can match layouts to specific slides.

Also read any reference files identified in Step 1b at this point, before proceeding to Step 3.

### Step 3: Customize the CSS

The scaffold script automatically copies `base-styles.css` to your presentation directory as `styles.css`. Now customize the CSS variables (especially colors) for your presentation theme.

**Using Google Fonts:** The scaffold defaults to Source Sans 3. To use a different font, add an `@import` at the top of your CSS file:
```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;600&display=swap');

:root {
  --heading-font: "Playfair Display", Georgia, serif;
  --body-font: "Lato", Helvetica, sans-serif;
  /* ... */
}
```

Open the generated `styles.css` file to see all available CSS variables and customization options. The file is well-commented with clear sections for: 
- CSS variables (colors, typography, spacing)                                                                        
- Base reveal.js overrides                                                                                       
- Slide layout styles
- Text size utilities (`.text-lg`, `.text-xl`, etc.)

**Typography guidance:**
- Base text (`--text-size: 16pt`) is intentionally small to fit more content
- When a slide has less content, use `.text-lg`, `.text-xl`, etc. to fill space appropriately
- This approach prevents overflow on content-heavy slides while allowing flexibility on lighter slides

**Custom CSS classes for repeated patterns:**

Use inline styles for layout (grids, flex containers) since those vary per slide. But when a visual pattern appears on multiple slides, create a dedicated CSS class in `styles.css` instead of repeating inline styles. This keeps the HTML clean and ensures consistency. Common examples: stat boxes (number + label), feature cards (icon + title + description), timeline/process steps, profile/bio cards. If an element repeats 3+ times, it should be a class.

### CSS Components

The scaffold copies `base-styles.css` → `styles.css`. Open it to see all available CSS variables (colors, typography, spacing) and pre-built components. Key patterns:

- **Section dividers**: `<section class="section-divider">` — centered layout with large title
- **Content wrapper**: `<div class="content">` — flexbox container filling space below the title
- **Footnotes**: `<div class="footnote">` — positioned at slide bottom
- **Blockquotes**: `<blockquote>` — styled with left border and italic text
- **Icons**: Font Awesome is included — `<i class="fa-solid fa-lightbulb"></i>`
- **Text size utilities**: `.text-lg` (18pt), `.text-xl` (20pt), `.text-2xl` (24pt), `.text-3xl` (28pt), `.text-4xl` (32pt)
- **Text style utilities**: `.text-muted`, `.text-center`, `.text-uppercase`, `.font-light`, `.font-bold`

### Step 4: Fill in the HTML Content

**IMPORTANT: Use the Edit tool to fill in slides incrementally — at most 2 slides per Edit call.** Do NOT rewrite the entire HTML file with the Write tool, as large presentations will exceed output token limits and fail. The scaffold generates unique placeholder text per slide (e.g., `Slide 2 Title Here`), so each section can be targeted with Edit. Process slides in order: complete slides 1–2, then 3–4, and so on. For slides with complex content (charts with full configuration, multi-part diagrams, or extensive code blocks), process one slide at a time to avoid hitting token limits.

Follow these patterns:

**Standard slide structure:**
```html
<section id="unique-slide-id">
  <h2>Slide Title</h2>
  <div class="content">
    <!-- Content here -->
  </div>
</section>
```

**Multi-column layouts** - always use inline CSS grid (do NOT create utility classes like `.grid-2`):
```html
<!-- Equal columns -->
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 30px;">
  <div>Column 1</div>
  <div>Column 2</div>
</div>

<!-- Three columns -->
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px;">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>

<!-- Unequal columns -->
<div style="display: grid; grid-template-columns: 1fr 2fr; gap: 30px;">
  <div>Narrow sidebar</div>
  <div>Wide main content</div>
</div>
```

Why inline styles for grids? Each slide's layout needs vary - column ratios, gaps, etc. Inline styles give you full control per-slide without creating dozens of utility classes.

**Grid layout rules** (these prevent the most common layout bugs):

1. **No `align-items: start` on outer grids.** CSS Grid defaults to `align-items: stretch`, which makes all cards the same height — this is the desired behavior inside `.content`. Using `align-items: start` on the outer grid breaks vertical filling, leaving whitespace at the bottom. If you need top-alignment, apply it to individual cards, not the grid container.

2. **No unnecessary wrapper divs.** Put styled cards directly as grid children. Wrapping a card in an extra `<div>` prevents `align-items: stretch` from reaching the card — the wrapper stretches but the inner card doesn't, causing uneven heights.

3. **Distribute content inside stretched cards.** When cards stretch vertically (the default), cards with less content will have elements bunched at the top. Fix this by making the card a flex column: add `display: flex; flex-direction: column` to the card, then either:
   - Use `justify-content: space-between` to spread sections apart
   - Add `margin-top: auto` to the last element to anchor it at the bottom

4. **Distribute items in flex column grid children.** When a grid column is a flex container (`display: flex; flex-direction: column`) holding multiple items (e.g., a list of feature cards), the flex container stretches to match the sibling column's height, but its children only take their natural height — leaving whitespace at the bottom. Fix this by adding `justify-content: space-between` to the flex container. This is especially common in two-column layouts where one column has a tall card (like a table) and the other has several smaller items.

For complete layout patterns (card grids, stat boxes, image+text, icon rows, timeline, comparison, quotes, team cards, etc.), see [layouts.md](references/layouts.md) — loaded in Step 2.5. It includes detailed examples of all four rules above.

**Important HTML patterns:**
- Every `<section>` should have a unique `id` attribute for stable identification
- Use `class="section-divider"` for centered section title slides
- Wrap main content in `<div class="content">` for consistent spacing. This is a flexbox container that fills the remaining vertical space below the title, ensuring content flows properly.
- Use `<div class="footnote">` for attribution or source text at bottom
- **All visible text must be inside a text element** (`<p>`, `<li>`, or `<h1>`–`<h6>`). These elements inherit the base font-size, color, and line-height from the CSS. Never put text directly in `<span>` or `<div>` — they won't pick up the base styles and will render at the wrong size. Use `<div>` only as a layout container (for grids, flexbox, etc.), with `<p>` elements inside it for the actual text.

### Built-in Reveal.js Classes

- **`r-fit-text`** - Auto-sizes text to fill the slide
- **`r-stretch`** - Stretches element to fill remaining vertical space
- **`r-stack`** - Layers elements on top of each other

### Step 5: Validate Layout and Charts

Run the overflow checker and chart validator to ensure slides render correctly.

**5a. Check for content overflow:**

```bash
node <path-to-skill>/scripts/check-overflow.js presentation.html
```

The script checks each slide for:
- **Vertical overflow**: Content taller than slide height
- **Horizontal overflow**: Content wider than slide width

**5b. Validate charts (if the presentation contains charts):**

```bash
node <path-to-skill>/scripts/check-charts.js presentation.html
```

The script validates:
- Chart configuration syntax (type, data structure, options)
- Canvas sizing and layout correctness
- Data consistency (labels vs data array lengths)

If any issues are found, fix them before proceeding.

### Step 6 (Optional): Visual Review with Screenshots

**This step is skipped by default.** You MUST use the AskUserQuestion tool to ask the user whether they want to proceed. Do NOT execute this step unless the user explicitly confirms.

Ask: "Do you want to capture screenshots to visually review all slides? This helps catch color issues, icon rendering, and text wrapping problems that automated checks might miss."

Only if the user explicitly confirms, proceed with the following:

```bash
cd <presentation-directory>
npx decktape reveal "presentation.html?export" output.pdf \
  --screenshots \
  --screenshots-directory "screenshots/$(date +%Y%m%d_%H%M%S)"
```

**Note:** The `?export` query parameter disables chart animations for cleaner PDF rendering. Charts will still animate when viewing the HTML directly in a browser.

This creates a timestamped folder (e.g., `screenshots/20241210_143052/`) so you can track versions and compare before/after fixes.

Then use the Read tool to examine each screenshot image file.

#### What to Look For

The overflow script catches most layout issues, but these problems require visual inspection:

1. **Color inheritance in containers**: Text inside styled containers may inherit the wrong color from parent elements. If you have light text on a dark page background, text inside a light-colored container will be unreadable unless you explicitly set dark text color for that container.

2. **Custom bullet/list styling**: If you override default list styles, bullets may not contrast well on all container backgrounds.

3. **Icons not rendering**: If Font Awesome fails to load, you'll see empty squares or nothing where icons should be.

4. **Overflow edge cases**: The script catches most overflow, but complex nested layouts occasionally slip through.

5. **Unexpected text wrap**: Text that you expected to fit on one line actually overflows to two lines. This is especially common in column layouts, where the header of one column may wrap while the rest don't, making things uneven.

**Re-capture specific slides after fixes:**
```bash
npx decktape reveal "presentation.html?export" output.pdf \
  --screenshots \
  --screenshots-directory "screenshots/$(date +%Y%m%d_%H%M%S)" \
  --slides 2,5,7-9
```

Then re-examine the updated screenshots to verify fixes. The new timestamped folder makes it easy to compare with the previous version.

### Step 7 (Optional): Browser-Based Editing

**This step is skipped by default.** You MUST use the AskUserQuestion tool to ask the user whether they want to proceed. Do NOT execute this step unless the user explicitly confirms.

Ask: "Do you want to start a browser-based editor? This lets you click any text to edit it directly in the browser, then save changes back to the file. It's useful for wordsmithing, fixing typos, or tweaking copy without editing HTML."

Only if the user explicitly confirms, proceed with the following:

```bash
node <path-to-skill>/scripts/edit-html.js <presentation-directory>/presentation.html
```

The editor opens in a browser where they can click any text to edit, press Escape to deselect, then click Save. Inform them: "Press Ctrl+C to stop the server when done."

## Preview the Presentation

After completing the presentation, ALWAYS start a local server for preview:

```bash
# macOS / Linux
cd <presentation-directory> && npx serve -l 8000 &; sleep 1 && open http://localhost:8000/presentation.html

# Windows
cd <presentation-directory> && start /B npx serve -l 8000 && timeout /t 2 /nobreak >nul && start http://localhost:8000/presentation.html
```

- 如果没有 Node.js，用 Python 替代：`python -m http.server 8000`

## Reveal.js Configuration

The scaffold uses sensible defaults. Key options you'll want to customize:

| Option | Default | When to change |
|--------|---------|----------------|
| `transition` | `'slide'` | Set to `'fade'` for subtle, `'convex'`/`'concave'` for 3D effects |
| `center` | `false` | Set to `true` for minimal/creative presentations with little content |
| `slideNumber` | `false` | Set to `true`, `'c/t'` (current/total), or `'h.v'` (horizontal.vertical) |
| `autoSlide` | `0` | Set to ms interval (e.g., `5000`) for self-running presentations |
| `loop` | `false` | Set to `true` to loop back to first slide after last |
| `backgroundTransition` | `'fade'` | Change to match or complement `transition` |

The scaffold sets `width: 1280, height: 720` (16:9). Content scales to fit the viewport — change for different aspect ratios.

For the complete configuration reference (all 40+ options), see [references/advanced-dev.md](references/advanced-dev.md#configuration-reference).

### Vertical Slides

Nest `<section>` elements to create vertical slide stacks. Navigation: left/right for horizontal, up/down for vertical. Use `navigationMode: 'linear'` in config to ignore vertical structure.

### Slide Overview

Press `ESC` or `O` to see all slides in a grid. Click any slide to jump to it.

## Dependencies

Required for the scripts, should be already installed:
- **Node.js** (for running scripts)
- **Puppeteer** (for overflow checking): `npm install puppeteer` — optional; if not installed, `check-overflow.js` will skip and you can visually verify overflow in the browser instead
- **Cheerio** (for chart validation): `npm install cheerio`
- **Decktape** (for screenshots): `npx decktape` (runs directly)

## Troubleshooting

**CDN resources fail to load** — If reveal.js, Chart.js, or Font Awesome don't load (no internet, corporate firewall), download the files locally and update the `<script>`/`<link>` paths in the HTML to point to local copies.

**Font Awesome icons show as empty squares** — Usually caused by CDN loading failure. Check browser console for errors. If using a local setup, ensure the web server is running (opening the HTML file directly via `file://` may block font loading due to CORS).

**Large presentations are slow** — If you have 50+ slides with many charts or animations, consider splitting into multiple HTML files and linking between them with `<a href="part2.html">`. Each file loads independently.
