# Interaction & Navigation

Guide for navigating slides, linking between them, searching content, and controlling the presentation experience.

## Table of Contents

1. [Internal Links](#internal-links)
2. [Navigation Buttons](#navigation-buttons)
3. [Jump to Slide](#jump-to-slide)
4. [Slide States](#slide-states)
5. [Overview Mode](#overview-mode)
6. [Fullscreen Mode](#fullscreen-mode)
7. [Search Plugin](#search-plugin)
8. [Zoom Plugin](#zoom-plugin)
9. [Touch Navigation](#touch-navigation)

---

## Internal Links

Link from one slide to another using anchor tags with `href="#/<id>"`. Give the target slide a unique `id` attribute:

```html
<section>
  <a href="#/summary">Skip to summary</a>
</section>
<section>
  <h2>Middle slide</h2>
</section>
<section id="summary">
  <h2>Summary</h2>
  <a href="#/0">Back to start</a>
</section>
```

### Numbered Links

Link by slide index instead of id:

```html
<a href="#/2">Go to 3rd slide (0-indexed)</a>
<a href="#/3/2">Go to 2nd vertical slide inside 4th horizontal slide</a>
```

### Lightbox Links

Open external websites in an iframe overlay without leaving the presentation:

```html
<a href="https://example.com" data-preview-link>Open in lightbox</a>
```

The target website must allow iframe embedding. Many sites block this via `x-frame-options` or `Content-Security-Policy`.

---

## Navigation Buttons

Add clickable elements that navigate relative to the current slide. Apply one of these CSS classes to any HTML element inside `.reveal`:

```html
<button class="navigate-left">Left</button>
<button class="navigate-right">Right</button>
<button class="navigate-up">Up</button>
<button class="navigate-down">Down</button>
<button class="navigate-prev">Previous</button>
<button class="navigate-next">Next</button>
```

- `navigate-prev` / `navigate-next` move through both vertical and horizontal slides
- Each button automatically receives an `enabled` class when that navigation direction is valid from the current position

**Example — custom navigation controls:**

```html
<section>
  <h2>Custom Navigation</h2>
  <p>Use the buttons below to navigate:</p>
  <div style="display: flex; gap: 15px; justify-content: center; margin-top: 20px;">
    <button class="navigate-left" style="padding: 10px 20px;">Previous</button>
    <button class="navigate-right" style="padding: 10px 20px;">Next</button>
  </div>
</section>
```

---

## Jump to Slide

Quickly navigate to any slide by number or id:

1. Press **G** to activate
2. Type a slide number or id string
3. Press **Enter** to navigate

| Input | Result |
|:------|:-------|
| `5` | Navigate to slide number 5 |
| `6/2` | Navigate to horizontal slide 6, vertical slide 2 |
| `the-end` | Navigate to the slide with `id="the-end"` |

Disable in config:

```javascript
Reveal.initialize({
  jumpToSlide: false,
});
```

---

## Slide States

Apply dynamic CSS based on the active slide using the `data-state` attribute. The state value is added as a class to the viewport element (`.reveal-viewport`) when the slide is active:

```html
<section data-state="dark-mode">
  <h2>This slide triggers "dark-mode" class on viewport</h2>
</section>
```

```css
/* In styles.css */
.dark-mode .reveal {
  filter: brightness(0.8);
}

.highlight-section {
  border: 3px solid gold;
}
```

### JavaScript State Events

Listen for state changes:

```javascript
Reveal.on('dark-mode', () => {
  console.log('Dark mode activated');
});
```

This is useful for:
- Changing global styles when specific slides are active
- Triggering JavaScript actions on slide entry
- Creating context-sensitive UI changes

---

## Overview Mode

View all slides in a grid layout. Useful for getting a bird's-eye view and jumping to distant slides.

### Keyboard

- Press **ESC** or **O** to toggle overview mode
- Click any slide to jump to it
- Navigate with arrow keys while in overview

### JavaScript API

```javascript
// Toggle overview
Reveal.toggleOverview();

// Force on/off
Reveal.toggleOverview(true);   // activate
Reveal.toggleOverview(false);  // deactivate

// Check state
Reveal.isOverview();  // true/false
```

### Events

```javascript
Reveal.on('overviewshown', (event) => {
  // Overview mode activated
});
Reveal.on('overviewhidden', (event) => {
  // Overview mode deactivated
});
```

---

## Fullscreen Mode

Present your slides in the browser's fullscreen mode:

- Press **F** to enter fullscreen
- Press **ESC** to exit

No configuration needed — this works out of the box with reveal.js.

### Fullscreen Plugin (External)

For programmatic fullscreen control or to stretch embedded content (like iframes) to fill the entire viewport:

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js-plugins@4.6.0/fullscreen/plugin.js"></script>
```

```javascript
Reveal.initialize({
  plugins: [RevealFullscreen],
});
```

Usage on slides:

```html
<section data-fullscreen="true">
  <iframe class="stretch" src="https://example.com"></iframe>
</section>
```

---

## Search Plugin

Search across all slide content using the built-in search plugin.

### Keyboard Shortcut

Press **Ctrl+Shift+F** (or **Cmd+Shift+F** on Mac) to open the search overlay.

### Setup

Include the plugin script and add it to the plugins array:

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/search/search.js"></script>
```

```javascript
Reveal.initialize({
  plugins: [RevealSearch],
});
```

The scaffold generated by `create-presentation.js` does not include this plugin by default. Add the script tag and plugin entry manually if you need search functionality.

---

## Zoom Plugin

Zoom into any element on a slide for closer inspection during a presentation.

### Usage

Hold **Alt** and click any element to zoom in (Ctrl+click on Linux). Click again to zoom out.

### Setup

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/zoom/zoom.js"></script>
```

```javascript
Reveal.initialize({
  plugins: [RevealZoom],
});
```

This is particularly useful for:
- Zooming into small code blocks
- Showing detail in complex diagrams
- Highlighting specific parts of a chart

---

## Touch Navigation

On touch-enabled devices, swipe to navigate through slides:

- **Horizontal swipe** — move between horizontal slides
- **Vertical swipe** — move between vertical slides

### Disable Touch

```javascript
Reveal.initialize({
  touch: false,
});
```

### Prevent Swipe on Specific Elements

If part of your content needs touch interaction (scrollable areas, interactive widgets), prevent reveal.js from capturing swipes:

```html
<section>
  <div data-prevent-swipe style="max-height: 400px; overflow-y: auto;">
    <p>This content can be scrolled without changing slides.</p>
  </div>
</section>
```

## References

- [Links](official-docs/links.md)
- [Jump to Slide](official-docs/jump-to-slide.md)
- [Slide States](official-docs/markup.md)
- [Overview](official-docs/overview.md)
- [Fullscreen](official-docs/fullscreen.md)
- [Plugins](official-docs/plugins.md)
- [Touch Navigation](official-docs/touch-navigation.md)
- [Slide Numbers](official-docs/slide-numbers.md)
- [Slide Visibility](official-docs/slide-visibility.md)
- [Vertical Slides](official-docs/vertical-slides.md)
- [Scroll View](official-docs/scroll-view.md)
- [Fullscreen Plugin](plugins/plugin-fullscreen.md)
