# Plugins

Plugin catalog for reveal.js presentations. The scaffold includes **RevealChart** by default; all others require manual setup.

Plugins fall into two categories:

- **Built-in plugins** — shipped with reveal.js, loaded from `reveal.js@5.2.1/plugin/`
- **Third-party plugins** — separate packages, loaded from their own CDN

## How to Add a Plugin

Every plugin follows the same pattern:

1. Add `<script>` tag(s) before `Reveal.initialize()`
2. Register in the `plugins` array

```javascript
Reveal.initialize({
  // ... other config
  plugins: [ RevealNotes, RevealSearch ]
});
```

---

## Built-in Plugins

These ship with reveal.js. No extra dependencies needed.

### RevealNotes — Speaker Notes

Private notes visible only in the speaker view (press `S`). Essential for live presentations.

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/notes/notes.js"></script>
```

```javascript
plugins: [ RevealNotes ]
```

Usage — add `<aside class="notes">` inside any slide:

```html
<section>
  <h2>Revenue Growth</h2>
  <aside class="notes">Mention the Q3 spike was due to the enterprise deal.</aside>
</section>
```

See [visuals.md](visuals.md) for full speaker notes documentation.

### RevealSearch — Content Search

Search across all slide content. Useful for long presentations (30+ slides).

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/search/search.js"></script>
```

```javascript
plugins: [ RevealSearch ]
```

Press **Ctrl+Shift+F** (or **Cmd+Shift+F** on Mac) to open the search overlay.

### RevealZoom — Element Zoom

Zoom into any element for closer inspection during a presentation.

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/zoom/zoom.js"></script>
```

```javascript
plugins: [ RevealZoom ]
```

Hold **Alt** and click any element to zoom in (Ctrl+click on Linux). Click again to zoom out. Useful for code blocks, diagrams, and charts.

### RevealHighlight — Code Syntax Highlighting

Syntax highlighting for code blocks using highlight.js. Supports 190+ languages with configurable themes.

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/highlight/highlight.js"></script>
```

```javascript
plugins: [ RevealHighlight ]
```

To change the highlighting theme, add a CSS link in `<head>`:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/highlight/zenburn.min.css">
```

Built-in themes: `monokai`, `zenburn` (dark), `github` (light). For more themes, load from highlight.js CDN:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/styles/github-dark.min.css">
```

Available themes: [highlight.js demo](https://highlightjs.org/static/demo/)

See [code-slides.md](code-slides.md) for code slide patterns (line numbers, step-through highlights).

### RevealMath — Math Formulas (KaTeX)

Renders LaTeX math notation using KaTeX. Supports inline (`$...$`) and display (`$$...$$`) math.

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/math/math.js"></script>
```

```javascript
plugins: [ RevealMath ]
```

The plugin loads KaTeX automatically — no separate KaTeX scripts needed. Use on any slide:

```html
<section>
  <h2>Euler's Identity</h2>
  <p>$$e^{i\pi} + 1 = 0$$</p>
  <p>The value of $x$ is $42$.</p>
</section>
```

**Configuration options:**

```javascript
Reveal.initialize({
  plugins: [ RevealMath ],
  math: {
    // mathjax or katex (default)
    mathjax: 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js',
    config: 'TeX-AMS_HTML-full'  // MathJax config, ignored for KaTeX
  }
});
```

See [code-slides.md](code-slides.md) for more math formula patterns.

### RevealMarkdown — Markdown Slide Authoring

Write slides using Markdown instead of HTML. Supports `data-markdown` attribute and external `.md` files.

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/markdown/markdown.js"></script>
```

```javascript
plugins: [ RevealMarkdown ]
```

**Inline markdown** on a slide:

```html
<section data-markdown>
  <textarea data-template>
    ## Slide Title
    - Bullet point 1
    - Bullet point 2

    ```python
    print("Hello, World!")
    ```
  </textarea>
</section>
```

**External markdown file:**

```html
<section data-markdown="content.md"
         data-separator="^\n---\n$"
         data-separator-vertical="^\n--\n$"
         data-separator-notes="^Note:">
</section>
```

**Slide separators** in external files:
- `---` separates horizontal slides
- `--` separates vertical slides within a stack
- `Note:` marks speaker notes

See [code-slides.md](code-slides.md) for more markdown slide patterns.

---

## Third-Party Plugins

These require loading additional libraries beyond reveal.js.

### RevealChart — Chart.js Integration

**Included in the scaffold by default.** Renders Chart.js charts (bar, line, pie, doughnut, etc.) from JSON or CSV data embedded in `<canvas>` elements.

```html
<!-- In <head> -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7"></script>

<!-- Before Reveal.initialize() -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js-plugins@4.6.0/chart/plugin.js"></script>
```

```javascript
plugins: [ RevealChart ],
chart: {
  defaults: {
    color: 'rgba(0, 0, 0, 0.8)',
    borderColor: 'rgba(0, 0, 0, 0.8)',
    devicePixelRatio: 2
  }
}
```

See [charts.md](charts.md) for layout patterns and [plugins/plugin-chart.md](plugins/plugin-chart.md) for full API.

### RevealMermaid — Mermaid Diagrams

Renders flowcharts, sequence diagrams, class diagrams, and more from text syntax.

```html
<!-- Before Reveal.initialize() -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin@11.12.3/plugin/mermaid/mermaid.js"></script>
```

```javascript
plugins: [ RevealMermaid ],
mermaid: {} // optional config
```

Usage — wrap Mermaid syntax in `<div class="mermaid"><pre>`:

```html
<div class="mermaid">
  <pre>
    flowchart LR
      Client --> API --> Database
  </pre>
</div>
```

See [diagrams.md](diagrams.md) for all diagram types and styling.

### RevealAnimate — SVG Animations

SVG.js-based animations driven by fragments or auto-slide. Creates step-by-step SVG animations.

```html
<!-- Before Reveal.initialize() -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js-plugins@4.6.0/animate/plugin.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@svgdotjs/svg.js@3.2.4/dist/svg.min.js"></script>
```

```javascript
plugins: [ RevealAnimate ],
animate: { autoplay: true }
```

See [plugins/plugin-animate.md](plugins/plugin-animate.md) for the JSON-in-comments animation pattern.

### RevealD3 — D3.js Visualizations

Embed interactive D3.js, React-based, or Vega-lite visualizations in slides.

```html
<!-- Before Reveal.initialize() -->
<script src="https://cdn.jsdelivr.net/npm/reveald3@2.0.0/reveald3.min.js"></script>
```

```javascript
plugins: [ RevealD3 ]
```

Usage — load external visualization files:

```html
<div class="fig-container" data-file="visualizations/chart.html"></div>
```

See [plugins/plugin-d3.md](plugins/plugin-d3.md) for fragment-driven transitions and advanced usage.

### RevealFullscreen — Fullscreen Iframes

Allow iframes and other elements to stretch to full available space within a slide.

```html
<!-- Before Reveal.initialize() -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js-plugins@4.6.0/fullscreen/plugin.js"></script>
```

```javascript
plugins: [ RevealFullscreen ]
```

Usage:

```html
<section data-fullscreen="true">
  <iframe class="stretch" src="https://example.com"></iframe>
</section>
```

### KaTeX — Math Formulas (Standalone)

**Prefer RevealMath (built-in) for most use cases.** Use standalone KaTeX only if you need full control over rendering options or are not using the RevealMath plugin.

```html
<!-- In <head> -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">

<!-- Before Reveal.initialize() -->
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
```

Initialize after Reveal:

```javascript
Reveal.initialize({ /* config */ }).then(() => {
  renderMathInElement(document.body, {
    delimiters: [
      {left: '$$', right: '$$', display: true},
      {left: '$', right: '$', display: false},
    ],
  });
});
```

Use `$...$` for inline math and `$$...$$` for display math. See [code-slides.md](code-slides.md) for usage patterns.

---

## Choosing Plugins

| If your presentation needs... | Add this plugin |
|-------------------------------|-----------------|
| Bar/line/pie charts | RevealChart (already in scaffold) |
| Flowcharts, sequence diagrams | RevealMermaid |
| Code with syntax highlighting | RevealHighlight (built-in) |
| Math formulas ($...$, $$...$$) | RevealMath (built-in, uses KaTeX) |
| Markdown slide authoring | RevealMarkdown (built-in) |
| Speaker notes for live talks | RevealNotes (built-in) |
| Step-by-step SVG animations | RevealAnimate |
| Interactive D3 visualizations | RevealD3 |
| Fullscreen embedded content | RevealFullscreen |
| Search across many slides | RevealSearch (built-in) |
| Zoom into slide details | RevealZoom (built-in) |
