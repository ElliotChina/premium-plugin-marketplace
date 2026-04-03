---
name: slides-revealjs
description: Create professional reveal.js presentations with expert design and interactive features. **ALWAYS use this skill when users mention:** slides, presentation, deck, slide deck, slideshow, 幻灯片, 演示文稿, 演讲, or want to present/展示 content visually — even without explicitly naming reveal.js. Also trigger for speaker notes, lecture materials, workshop content, conference talks, product demos, training materials, or any scenario requiring visual storytelling with animations, diagrams, code highlighting, or step-by-step reveals. Covers HTML/Markdown authoring, themes, animations, fragments, Mermaid diagrams, speaker view, PDF export, and full design system setup. **Do NOT use for:** regular web pages, dashboards, or static documentation.
compatibility:
  scripts:
    create-presentation.js: "Node.js 16+"
    check-overflow.js: "Node.js 16+ (no external dependencies)"
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
4. Build the minimal deck structure: `.reveal > .slides > section`. Default to `solarized` theme unless user explicitly requires otherwise.
5. Register only required plugins (Markdown, Highlight, Notes, Math, Mermaid, Search, Zoom, etc.).
6. Author content and interactions:
   - Use Mermaid diagrams for architecture/process/flow content to increase clarity and visual consistency
   - Build horizontal/vertical slides, fragments, backgrounds, transitions, media
7. Configure runtime behavior: navigation, keyboard, `hash`, `slideNumber`, `autoSlide`, `view: 'scroll'`.
8. Validate content quality:
   - Run overflow check (`node scripts/check-overflow.js <file> --check`)
   - Review composition rhythm (avoid 3 consecutive slides with same layout pattern)
   - Verify all slides fit within viewport; adjust content or split slides if overflow detected
9. Verify customizations (if applicable):
   - If custom CSS was added, verify selector scope is limited to `.reveal` or slide-level classes
   - Check impact scope (which slides/components each rule affects)
10. Final delivery:
    - Local preview with no console errors
    - Test speaker view (press S)
    - Verify PDF export workflow
    - For React components: verify mount/unmount cleanup

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
- `--no-css` - Skip generating custom.css
- `--local` - Use local reveal.js files instead of CDN (requires reveal.js installed nearby)

**Note:** By default, the scaffold uses CDN links for reveal.js (jsDelivr). This ensures the presentation works immediately without installing dependencies. Use `--local` only if you have reveal.js installed and need offline access or custom builds.

**Example:** `--structure 1,1,d,3,1` creates:
- 1 title slide
- 1 content slide
- 1 section divider
- 1 vertical stack with 3 slides
- 1 final slide

The scaffold is a **starting point**, not a constraint. After generation, freely adjust structure, styling, and content.

### Overflow Checker

Inject a browser-side detection script into a presentation, then open it in a browser to check every slide for content overflow. No external dependencies (no Playwright needed).

**Usage:**
```bash
# Inject detection code into HTML
node scripts/check-overflow.js ./presentation/index.html

# Inject and immediately open in browser
node scripts/check-overflow.js ./presentation/index.html --check

# Remove injected code after review
node scripts/check-overflow.js ./presentation/index.html --restore

# Adjust minimum overflow threshold (default: 5px)
node scripts/check-overflow.js ./presentation/index.html --threshold 10
```

**Options:**
- `--check` - Inject and open in default browser
- `--restore` - Remove injected detection code
- `--threshold <px>` - Minimum overflow to report (default: 5)

Results appear in the browser's developer console, showing which slides overflow and by how many pixels.

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

## Content Strategy

### Word Limits per Slide

Keep slides clear and readable by respecting these limits:

| Slide Type | Title | Body | Bullet Points |
|-----------|------|------|--------|
| Title | 3-6 words | 0-15 words (subtitle) | none |
| Content | 3-8 words | 30-50 words | 3-5 items |
| Divider | 2-5 words | 0-10 words | none |
| Diagram | 3-6 words | 10-20 words (caption) | none |
| Summary | 3-6 words | 20-35 words | 3-4 key points |

**Guidelines:**
- One core idea per slide
- Prefer short phrases over long paragraphs
- Split across multiple slides when limits are exceeded

### Slide Type Preferences

Choose the right slide structure based on content type:

- **Concept intro**: Title + 3-4 bullet points + optional icons
- **Process / Architecture**: Mermaid diagram + brief explanation
- **Data showcase**: Chart or table + key insight
- **Comparison**: Two-column layout (`.cols` + `.col-50`)
- **Case study**: Left-image-right-text or top-image-bottom-text
- **Quote / Testimonial**: Large quotation + attribution
- **Call to action**: Centered large text + accent color

---

## Speaker Notes

### Basic Notes

```html
<section>
  <h2>Key Insight</h2>
  <p>Content visible to audience</p>
  <aside class="notes">
    This is only visible in speaker view (press S).
    Include talking points, timing cues, and transitions.
  </aside>
</section>
```

### TTS-Optimized Notes

For text-to-speech (TTS) or video recording, structure speaker notes as follows:

```html
<aside class="notes">
  <p><strong>Duration:</strong> 45 seconds</p>

  <p><strong>Opening:</strong> Let's look at this key insight...</p>

  <p><strong>Key Points:</strong></p>
  <ul>
    <li>Point 1: Clear and concise explanation</li>
    <li>Point 2: Supporting data or example</li>
    <li>Point 3: Practical application scenario</li>
  </ul>

  <p><strong>Transition:</strong> Next we'll discuss how to apply this insight...</p>
</aside>
```

**TTS formatting guidelines:**
- Use complete sentences; avoid abbreviations
- Spell out numbers in full words ("three" not "3")
- Include pause cues ("..." for a brief pause)
- Annotate pronunciation of difficult terms (jargon, acronyms)
- Avoid tables and complex formatting

---

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

For common reveal.js techniques including title slides with backgrounds, logo positioning, column layouts, fragments, emoji support, and more, see [Reveal.js Tips](./references/revealjs-tips.md).

Key design requirements:
- State your design approach before writing slide code.
- Use `pt` units for font sizes in slide CSS/inline styles.
- Prefer official reveal `solarized` theme for light-tone decks unless explicitly overridden.
- Each deck must have a deliberate aesthetic direction, not generic styling.

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
- Overflow check passed (run `node scripts/check-overflow.js <file> --check` to verify).
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
| Reveal.js Tips     | Common techniques: backgrounds, layouts, fragments, emoji, custom transforms.        | [Reveal.js Tips](./references/revealjs-tips.md) |
| Quarto Migration   | Migrating from Quarto `.qmd` to pure reveal.js HTML.                                  | [Quarto Migration](./references/quarto-migration.md) |
| Base Styles        | CSS variables, text utilities, layout helpers, and components for presentations.      | [Base Styles](./references/base-styles.css) |
| Anti-Patterns      | Common Reveal.js pitfalls and solutions (CSS specificity, layout, fragments).         | [Anti-Patterns](./references/anti-patterns.md) |

### Helper Scripts

| Script              | Description                                                                           | Path                                              |
| ------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Scaffold Generator  | Generate presentation skeleton with predefined slide structure.                       | [create-presentation.js](./scripts/create-presentation.js) |
| Overflow Checker    | Inject browser-side overflow detection into presentations (no dependencies).        | [check-overflow.js](./scripts/check-overflow.js) |

### Examples

| File           | Description                                                                           | Path                                              |
| -------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Basic Deck     | Simple presentation with fragments, columns, and speaker notes.                      | [basic-deck.html](./examples/basic-deck.html) |
| Advanced Deck  | Full-featured deck with Mermaid, code highlighting, and custom design tokens.          | [advanced-deck.html](./examples/advanced-deck.html) |

### Other

| Topic                  | Description                                                             | Reference                                                |
| ---------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------- |
| Upgrading Instructions | Migration notes for updating reveal.js versions without breaking decks. | [Upgrading Instructions](./references/official/upgrading.md) |
| React (Manual Setup)   | Legacy integration patterns for older React versions.                   | [React Legacy](./references/official/react-legacy.md)   |
