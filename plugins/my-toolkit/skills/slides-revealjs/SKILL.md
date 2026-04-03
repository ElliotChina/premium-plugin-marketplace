---
name: slides-revealjs
description: Create reveal.js presentations with expert design. Triggers when users mention slides, presentations, decks, slide decks, slide shows, speaker notes, or want to present content visually — even without explicitly naming reveal.js. Covers HTML/Markdown authoring, themes, animations, fragments, Mermaid diagrams, PDF export, and full design system setup.
---

# Slides Skill for reveal.js

## Overview

This skill guides AI to create and update reveal.js slides quickly and reliably. Prefer documented reveal.js capabilities over guessed APIs, config keys, or plugin behavior.

## When to Use

- Creating a reveal.js presentation from scratch.
- Migrating existing content into reveal.js slides (HTML or Markdown).
- Enabling advanced behaviors like Fragments, Auto-Animate, Speaker View, Math, Code Highlight, PDF export, or Scroll View.
- Integrating reveal.js into npm/ESM or React projects.

## Core Workflow

1. Analyze the content first and state a content-informed design approach before writing code (topic, tone, audience, branding, and palette rationale).
2. Choose the integration mode: Static HTML (fastest) or npm/ESM (engineering).
3. If converting from an existing doc, inventory all source sections/items first and map each item to at least one slide.
4. Build the minimal deck structure: `.reveal > .slides > section`.
5. Register only required plugins (Markdown, Highlight, Notes, Math, Search, Zoom, etc.).
6. Author content and interactions: horizontal/vertical slides, fragments, backgrounds, transitions, media.
7. Configure runtime behavior: navigation, keyboard, `hash`, `slideNumber`, `autoSlide`, `view: 'scroll'`.
8. Validate and ship: local preview, overflow check, Speaker View, print/PDF export, and optional API control code.

## Helper Scripts

### Scaffold Generator

Quickly generate a reveal.js presentation skeleton with predefined structure:

```bash
node scripts/create-presentation.js ./my-deck --structure 1,1,d,3,1,d,1 --title "My Talk"
```

**Structure pattern syntax:**
- `1` = single slide
- `N` = vertical stack of N slides
- `d` = divider/title slide

**Options:**
- `--structure <pattern>` - Slide layout pattern (default: "1")
- `--title <title>` - Presentation title (default: "Presentation")
- `--theme <theme>` - Reveal.js theme (default: "solarized")
- `--no-css` - Skip copying base-styles.css

**Example:** `--structure 1,1,d,3,1` creates:
- 1 title slide
- 1 content slide
- 1 section divider
- 1 vertical stack with 3 slides
- 1 final slide

The scaffold is a **starting point**, not a constraint. After generation, freely adjust structure, styling, and content.

### Overflow Checker

Validate that slide content fits within bounds using Playwright:

```bash
node scripts/check-overflow.js ./presentation/index.html
node scripts/check-overflow.js http://localhost:3000 --browser firefox
```

**Options:**
- `--browser <name>` - Browser: chromium, firefox, webkit (default: chromium)
- `--threshold <px>` - Minimum overflow to report (default: 5)
- `--json` - Output as JSON for programmatic processing
- `--verbose` - Show detailed progress

**Exit codes:**
- `0` - No overflow detected
- `1` - Overflow detected in one or more slides
- `2` - Error during execution

Run this before finalizing presentations to catch content density issues.

### Base Styles

The scaffold automatically includes `references/base-styles.css` which provides:

- **CSS Variables** for theming (colors, fonts, sizes)
- **Text size utilities**: `.text-sm`, `.text-lg`, `.text-xl`, `.text-2xl`, etc.
- **Color utilities**: `.text-primary`, `.text-accent`, `.bg-surface`, etc.
- **Layout utilities**: `.cols`, `.col-50`, `.grid-2`, `.center`
- **Components**: `.panel`, `.callout`, `.divider-slide`

Copy and customize these variables for your design direction:

```css
:root {
  --primary-color: #b58900;
  --accent-color: #d33682;
  --h1-size: 48pt;
  --h2-size: 36pt;
}
```

## Implementation Templates

### 1) Static HTML (UMD)

```html
<html>
  <head>
    <link rel="stylesheet" href="dist/reveal.css" />
    <link rel="stylesheet" href="dist/theme/solarized.css" />
    <link rel="stylesheet" href="plugin/highlight/zenburn.css" />
  </head>
  <body>
    <div class="reveal">
      <div class="slides">
        <section>Slide 1</section>
        <section>
          <section>Vertical 1</section>
          <section>Vertical 2</section>
        </section>
      </div>
    </div>

    <script src="dist/reveal.js"></script>
    <script src="plugin/markdown/markdown.js"></script>
    <script src="plugin/highlight/highlight.js"></script>
    <script src="plugin/notes/notes.js"></script>
    <script>
      Reveal.initialize({
        hash: true,
        slideNumber: 'c/t',
        plugins: [RevealMarkdown, RevealHighlight, RevealNotes],
      });
    </script>
  </body>
</html>
```

### 2) npm/ESM

```js
import Reveal from 'reveal.js';
import Markdown from 'reveal.js/plugin/markdown/markdown.esm.js';
import Highlight from 'reveal.js/plugin/highlight/highlight.esm.js';
import Notes from 'reveal.js/plugin/notes/notes.esm.js';
import 'reveal.js/dist/reveal.css';
import 'reveal.js/dist/theme/white.css';

const deck = new Reveal({
  hash: true,
  slideNumber: 'c/t',
  plugins: [Markdown, Highlight, Notes],
});

await deck.initialize();
```

### 3) Markdown Slide Block

```html
<section data-markdown>
  <textarea data-template>
    ## Slide 1
    ---
    ## Slide 2
  </textarea>
</section>
```

## Feature Playbook

- Markdown: Enable the Markdown plugin; external markdown requires a local web server.
- Code: Enable Highlight and use `data-line-numbers` plus step highlights via `|`.
- Math: Use `RevealMath.KaTeX` by default (or MathJax when required).
- Speaker Notes: Enable Notes and press `S` for presenter view.
- Auto-Animate: Use adjacent `<section data-auto-animate>` and `data-id` for precise matching.
- Backgrounds: Use `data-background-*` (color/image/video/iframe).
- Architecture diagrams: Prefer Mermaid for system/process/flow slides to increase clarity and visual consistency.
- Scroll View: Use `view: 'scroll'` with optional `scrollSnap` and `scrollLayout`.
- PDF: Use `?print-pdf` then browser print to PDF.

## Reveal.js Tips

The items below should be preferred in this skill.

### Design & Visual Quality

For comprehensive design guidance including color palette selection, typography hierarchy, slide archetypes, content density limits, and visual review checklists, see [Slide Design Guide](./references/slide-design-guide.md).

Key requirements:
- State your design approach before writing slide code.
- Use `pt` units for font sizes in slide CSS/inline styles.
- Prefer official reveal `solarized` theme for light-tone decks unless explicitly overridden.
- Each deck must have a deliberate aesthetic direction, not generic styling.

### 1) Title slide with custom background

Use an explicit first `<section>` as a title slide and style it with reveal data attributes.

```html
<section
  id="title-slide"
  data-background-image="./img/background.jpg"
  data-background-size="cover"
  data-background-opacity="0.9"
>
  <h1>My Slide Show</h1>
</section>
```

### 2) Move/resize a logo after leaving title slide

Use CSS classes plus the `slidechanged` event.
Add a persistent logo element in your HTML, e.g. `<img class="slide-logo" src="./images/my-logo.svg" alt="Logo" />`.

```css
.reveal .slide-logo {
  position: fixed;
  display: block;
  max-width: none !important;
}

.reveal .slide-logo-bottom-right {
  right: 12px !important;
  bottom: 0 !important;
  left: auto !important;
  max-height: 2.2rem !important;
}

.slide-logo-max-size {
  top: 5px;
  left: 12px;
  right: auto !important;
  bottom: auto !important;
  height: 100px !important;
  max-height: none !important;
}
```

```js
function syncLogoForSlide(currentSlide) {
  const logos = document.querySelectorAll('.slide-logo');
  const onTitle = currentSlide && currentSlide.id === 'title-slide';
  logos.forEach((el) => {
    el.classList.toggle('slide-logo-max-size', onTitle);
    el.classList.toggle('slide-logo-bottom-right', !onTitle);
  });
}

Reveal.on('ready', (event) => syncLogoForSlide(event.currentSlide));
Reveal.on('slidechanged', (event) => syncLogoForSlide(event.currentSlide));
```

### 3) Background image sizing (`cover` vs `contain`)

`cover` fills the slide and may crop. `contain` preserves the entire image.

```html
<section data-background-image="images/2024.jpg" data-background-size="cover"></section>
<section data-background-image="images/2024.jpg" data-background-size="contain"></section>
```

### 4) Slide structure control (replacement for Quarto `slide-level`)

Pure reveal.js does not use Pandoc `slide-level`. Control structure explicitly:

- HTML mode: one `<section>` per slide, nested `<section>` for vertical slides.
- Markdown mode: use configured separators (`---`, `--`) to split slides.

### 5) Emoji support

Quarto's `from: markdown+emoji` is not a reveal.js feature. In reveal.js:

- Use native Unicode emoji directly.
- Or render emoji through your markdown/HTML pipeline before reveal initializes.

### 6) Fit large text and stretch media

`r-fit-text` and `r-stretch` are reveal classes and work directly.

```html
<section>
  <div class="r-fit-text">Big Text</div>
</section>

<section>
  <p>Here is an image:</p>
  <img class="r-stretch" src="image.webp" alt="Demo image" />
  <p>Some text after the image.</p>
</section>
```

### 7) Reveal content on key press with fragments

```html
<section>
  <h2>It's a candy dog</h2>
  <p style="font-size: 44pt; color: #75aadb;">Would you like to see a candy dog?</p>
  <img class="fragment fade-up" src="./images/dog.webp" alt="Candy dog" />
</section>
```

### 8) Two-column and 4-quadrant layouts

Quarto `::: columns` is not native reveal syntax. Use HTML/CSS layout wrappers.

```html
<section>
  <div class="cols">
    <div class="col col-70"><img src="./images/image_1.webp" alt="Left" /></div>
    <div class="col col-30">
      <img src="./images/image_2.webp" alt="Right top" />
      <img src="./images/image_3.webp" alt="Right bottom" />
    </div>
  </div>
</section>
```

```css
.reveal .cols {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.reveal .col-70 { flex: 0 0 70%; }
.reveal .col-30 { flex: 0 0 30%; }
```

For 4 quadrants, use a 2x2 CSS grid and reveal each cell with fragment classes (`fade-in-then-semi-out` or similar).

### 9) Custom inline short-code transform (`==text==` -> `<mark>text</mark>`)

```js
function convertMarkedTextInSlide(slide) {
  if (!slide) return;
  slide.innerHTML = slide.innerHTML.replace(/==([^=]+)==/g, '<mark>$1</mark>');
}

Reveal.on('ready', (event) => convertMarkedTextInSlide(event.currentSlide));
Reveal.on('slidechanged', (event) => convertMarkedTextInSlide(event.currentSlide));
```

### 10) Inline style and custom CSS

In reveal markdown, use inline HTML for precise text styling:

```html
<p>
  Make this <span style="color: red;">red</span> and this
  <span style="background: yellow;">highlighted</span>.
</p>
```

Load custom CSS in static HTML:

```html
<link rel="stylesheet" href="./assets/custom.css" />
```

Or import it in ESM:

```js
import './assets/custom.css';
```

### 11) Hide captions and style callouts from generated output

Some pipelines generate caption or callout markup. Hide if not needed:
```css
.reveal p.caption,
.reveal figcaption {
  display: none;
}
```

### 12) Vertical flow, slide IDs, menu labels, numbering, and notes

- Vertical chapters: nest sections (`<section><section>Child</section></section>`).
- Navigation behavior: use `navigationMode: 'default' | 'linear' | 'grid'`.
- Stable slide URL names: set section `id` and enable `hash: true`.
- Menu labels (when using the menu plugin): set `data-menu-title`.
- Slide number with total: `slideNumber: 'c/t'`.
- Speaker notes: `<aside class="notes">...</aside>` and press `S`.
- Overview mode shortcut: `Esc`.

```html
<section id="intro" data-menu-title="Introduction">
  <h2>Intro</h2>
  <aside class="notes">Presenter-only notes</aside>
</section>
```

```js
Reveal.initialize({
  hash: true,
  slideNumber: 'c/t',
  navigationMode: 'default',
  plugins: [RevealNotes],
});
```

For detailed design guidance (aesthetic direction, design tokens, typography hierarchy, palette strategy, atmosphere, motion, layouts, slide archetypes, content density limits, and typography baselines), see [Slide Design Guide](./references/slide-design-guide.md).

## Guardrails

- Do not invent reveal.js config keys; only use documented options.
- Do not use plugin syntax before registering the corresponding plugin (Markdown/Math/Notes/Highlight, etc.).
- For multi-instance pages, prefer `new Reveal(rootEl, config)` with `embedded: true`.
- In React, avoid duplicate initialization and call `destroy()` on unmount.
- When migrating from Quarto/Pandoc, preserve behavior first (fragment timing, navigation flow, note visibility), then adjust visual styling. See [Quarto Migration Guide](./references/quarto-migration.md) for syntax differences.
- Do not ship visually generic decks. Each deck must have a deliberate aesthetic direction, typography system, palette strategy, and motion intent.
- Prefer reveal official `solarized` theme for default/light-tone decks unless user requirements explicitly call for another theme.
- Minimize new custom CSS. First use built-in reveal classes/options; add CSS only when necessary.
- When adding CSS, scope selectors to `.reveal` or a slide-level class and verify impact scope (what selectors will match, which slides/components are affected).
- Do not reimplement slide engines (scroll-snap containers, custom nav chrome, custom keyboard routers) when using reveal.js. Use reveal built-ins unless there is a concrete gap.
- When borrowing HTML-slide design systems, translate the design language to reveal primitives (`section`, fragments, built-in navigation) instead of copying unrelated runtime architecture.

## Delivery Checklist

- First slide renders correctly with no obvious console errors.
- Plugin registration matches the content syntax used (Markdown/Notes/Math/Highlight/etc.).
- Navigation and interactions match requirements (keyboard, `hash`, `slideNumber`, `autoSlide`, touch).
- Theme defaults to official reveal `solarized` unless requirements explicitly override it.
- If custom CSS was added, selector scope and impact were reviewed (which slides/components each rule can affect).
- Architecture/process-heavy content uses Mermaid diagrams when appropriate.
- Source-to-slide coverage check was completed for conversion tasks (no major source section dropped).
- Composition rhythm was reviewed (no 3 consecutive slides with the same layout pattern).
- Density limits were respected or split across additional slides.
- Overflow check passed (run `node scripts/check-overflow.js <file>` to verify).
- If export is requested, verify print/PDF workflow end-to-end.

## References

### External Recipe Source

- [Some tips and tricks for Quarto when rendering as a reveal.js slideshow](https://www.avonture.be/blog/quarto-revealjs-tips/) (extract reveal.js-applicable patterns; ignore Quarto-only syntax)
- [Anthropic frontend-design skill](https://raw.githubusercontent.com/anthropics/skills/refs/heads/main/skills/frontend-design/SKILL.md) (aesthetic direction, typography, color, motion, composition discipline)
- [visual-explainer slide-patterns](https://raw.githubusercontent.com/nicobailon/visual-explainer/refs/heads/main/references/slide-patterns.md) (slide archetypes, pacing, density limits, presentation readability)

### Getting Started

| Topic        | Description                                                                               | Reference                                    |
| ------------ | ----------------------------------------------------------------------------------------- | -------------------------------------------- |
| Home         | Entry page for reveal.js docs, covering core concepts and navigation to all major guides. | [Home](./references/official/index.md)       |
| Installation | Explains how to install reveal.js in different environments and project setups.           | [Installation](./references/official/installation.md) |
| React        | Covers integration patterns and usage details for reveal.js in React apps.                | [React](./references/official/react.md)      |

### Support

| Topic       | Description                                                             | Reference                                  |
| ----------- | ----------------------------------------------------------------------- | ------------------------------------------ |
| Video Course| A structured tutorial path that teaches reveal.js basics step by step.  | [Course](./references/official/course.md)  |

### Content

| Topic            | Description                                                                    | Reference                                            |
| ---------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------- |
| Markup           | Shows the core HTML slide structure and how nested sections define navigation. | [Markup](./references/official/markup.md)            |
| Markdown         | Describes writing slides in Markdown and configuring the Markdown plugin.      | [Markdown](./references/official/markdown.md)        |
| Backgrounds      | Documents slide background options such as color, image, video, and iframe.    | [Backgrounds](./references/official/backgrounds.md)  |
| Media            | Covers embedding and controlling media content inside slides.                  | [Media](./references/official/media.md)              |
| Lightbox         | Explains how to present media in an enlarged lightbox-style experience.        | [Lightbox](./references/official/lightbox.md)        |
| Code             | Introduces code block rendering and syntax highlighting patterns for slides.   | [Code](./references/official/code.md)                |
| Math             | Shows how to render mathematical formulas with KaTeX or MathJax integrations.  | [Math](./references/official/math.md)                |
| Fragments        | Describes progressive reveal effects to show slide elements in sequence.       | [Fragments](./references/official/fragments.md)      |
| Links            | Explains internal and external linking behavior in reveal.js presentations.    | [Links](./references/official/links.md)              |
| Layout           | Covers layout techniques to organize content cleanly within each slide.        | [Layout](./references/official/layout.md)            |
| Slide Visibility | Describes controls for showing, hiding, or excluding specific slides.          | [Slide Visibility](./references/official/slide-visibility.md) |

### Customization

| Topic             | Description                                                                    | Reference                                              |
| ----------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------ |
| Themes            | Explains built-in themes and how to style presentations with custom theming.   | [Themes](./references/official/themes.md)              |
| Transitions       | Documents slide and element transition effects and their configuration.        | [Transitions](./references/official/transitions.md)    |
| Config Options    | Full reference for initialization and runtime configuration settings.          | [Config Options](./references/official/config.md)      |
| Presentation Size | Shows how to control deck dimensions, scaling behavior, and responsive sizing. | [Presentation Size](./references/official/presentation-size.md) |

### Features

| Topic            | Description                                                                   | Reference                                            |
| ---------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------- |
| Vertical Slides  | Explains vertical stacks for subtopics under a horizontal slide flow.         | [Vertical Slides](./references/official/vertical-slides.md) |
| Auto-Animate     | Describes automatic tweening between similar elements across adjacent slides. | [Auto-Animate](./references/official/auto-animate.md) |
| Auto-Slide       | Covers timed autoplay behavior and controls for automatic slide progression.  | [Auto-Slide](./references/official/auto-slide.md)    |
| Speaker View     | Shows presenter tools, notes view, and speaker-screen workflow.               | [Speaker View](./references/official/speaker-view.md)|
| Scroll View      | Explains continuous scroll-based presentation mode and related settings.      | [Scroll View](./references/official/scroll-view.md)  |
| Slide Numbers    | Documents numbering formats and display options for slide counters.           | [Slide Numbers](./references/official/slide-numbers.md) |
| Jump to Slide    | Shows how to quickly navigate to a specific slide during presentation.        | [Jump to Slide](./references/official/jump-to-slide.md) |
| Touch Navigation | Describes gesture and touch interactions on mobile and touch devices.         | [Touch Navigation](./references/official/touch-navigation.md) |
| PDF Export       | Explains the print-to-PDF workflow and export-specific adjustments.           | [PDF Export](./references/official/pdf-export.md)    |
| Overview Mode    | Documents the zoomed overview interface for fast deck navigation.             | [Overview Mode](./references/official/overview.md)   |
| Fullscreen Mode  | Covers fullscreen presentation behavior and toggling options.                 | [Fullscreen Mode](./references/official/fullscreen.md) |

### API

| Topic              | Description                                                                  | Reference                                                |
| ------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------- |
| Initialization     | Explains deck bootstrapping, config injection, and startup lifecycle.        | [Initialization](./references/official/initialization.md) |
| API Methods        | Reference for imperative methods used to control reveal.js programmatically. | [API Methods](./references/official/api.md)              |
| Events             | Lists emitted events and shows how to listen for deck state changes.         | [Events](./references/official/events.md)                |
| Keyboard           | Documents keyboard shortcuts and custom key-binding configuration.           | [Keyboard](./references/official/keyboard.md)            |
| Presentation State | Explains capturing, restoring, and sharing presentation state data.          | [Presentation State](./references/official/presentation-state.md) |
| postMessage        | Describes cross-window communication using the postMessage interface.        | [postMessage](./references/official/postmessage.md)      |

### Plugins

| Topic            | Description                                                              | Reference                                            |
| ---------------- | ------------------------------------------------------------------------ | ---------------------------------------------------- |
| Using Plugins    | Shows how to register and configure official or third-party plugins.     | [Using Plugins](./references/official/plugins.md)   |
| Creating Plugins | Guide to authoring custom reveal.js plugins and integrating them safely. | [Creating Plugins](./references/official/creating-plugins.md) |
| Multiplex        | Explains synchronized multi-client presentations for remote audiences.   | [Multiplex](./references/official/multiplex.md)      |

### Third Party Plugins

| Topic         | Description                                                                                    | Reference                                                       |
| ------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Animate       | Adds SVG.js-based slide animations that can be coordinated with reveal.js flow.                | [Animate](./references/plugins/plugin-animate.md)               |
| Chart         | Integrates Chart.js so presentations can render configurable data charts.                      | [Chart](./references/plugins/plugin-chart.md)                   |
| Fullscreen    | Provides fullscreen layout behavior to maximize available slide space.                         | [Fullscreen](./references/plugins/plugin-fullscreen.md)         |
| D3 (reveald3) | Embeds JavaScript visualizations (including D3-based content) with fragment-aware transitions. | [Reveal.js-d3 (reveald3)](./references/plugins/plugin-d3.md)    |
| Mermaid       | Adds Mermaid diagram rendering support directly inside reveal.js slides.                       | [reveal.js-mermaid-plugin](./references/plugins/plugin-mermaid.md) |

### Design & Migration

| Topic              | Description                                                                           | Reference                                              |
| ------------------ | ------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Slide Design Guide | Visual design, typography, color, layout, content pacing, and review checklists.     | [Slide Design Guide](./references/slide-design-guide.md) |
| Quarto Migration   | Migrating from Quarto `.qmd` to pure reveal.js HTML.                                  | [Quarto Migration](./references/quarto-migration.md) |
| Base Styles        | CSS variables, text utilities, layout helpers, and components for presentations.      | [Base Styles](./references/base-styles.css) |

### Helper Scripts

| Script              | Description                                                                           | Path                                              |
| ------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Scaffold Generator  | Generate presentation skeleton with predefined slide structure.                       | [create-presentation.js](./scripts/create-presentation.js) |
| Overflow Checker    | Validate slide content fits within bounds using Playwright.                           | [check-overflow.js](./scripts/check-overflow.js) |

### Other

| Topic                  | Description                                                             | Reference                                                |
| ---------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------- |
| Upgrading Instructions | Migration notes for updating reveal.js versions without breaking decks. | [Upgrading Instructions](./references/official/upgrading.md) |
| React (Manual Setup)   | Legacy integration patterns for older React versions.                   | [React Legacy](./references/official/react-legacy.md)   |
