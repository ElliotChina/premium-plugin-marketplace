# Advanced Development

Guide for JavaScript API, events, keyboard customization, presentation state, multiple instances, and full configuration reference.

## Table of Contents

1. [JavaScript API](#javascript-api)
2. [Event System](#event-system)
3. [Custom Keyboard Bindings](#custom-keyboard-bindings)
4. [Presentation State](#presentation-state)
5. [Multiple Presentations](#multiple-presentations)
6. [Configuration Reference](#configuration-reference)
7. [Plugin Extensions](#plugin-extensions)

---

## JavaScript API

Reveal.js exposes a comprehensive JavaScript API for programmatic control of your presentation.

### Navigation

```javascript
// Navigate to a specific slide
Reveal.slide(0, 0, 0);  // (horizontalIndex, verticalIndex, fragmentIndex)

// Directional navigation
Reveal.left();
Reveal.right();
Reveal.up();
Reveal.down();
Reveal.prev();
Reveal.next();

// Fragment navigation
Reveal.navigateFragment(fragmentIndex);  // Jump to specific fragment

// Check available routes
Reveal.availableRoutes();
// Returns: { left: false, right: true, up: false, down: true }

// Check available fragments
Reveal.availableFragments();
// Returns: { prev: false, next: true }
```

### Slide Information

```javascript
// Get slide objects
Reveal.getSlide(0, 0);          // Get slide by index
Reveal.getCurrentSlide();        // Currently active slide element
Reveal.getPreviousSlide();       // Previously active slide element

// Counting
Reveal.getTotalSlides();          // Total number of slides
Reveal.getHorizontalSlides();     // Number of horizontal slides
Reveal.getVerticalSlides();       // Number of vertical slides
Reveal.getSlidePastCount();       // How many slides user has visited

// All slides array
Reveal.getSlides();               // Array of all slide elements
```

### Position & Progress

```javascript
// Get current position
Reveal.getIndices();
// Returns: { h: 0, v: 0, f: 0 } (horizontal, vertical, fragment)

Reveal.getProgress();
// Returns: 0.5 (fraction of presentation completed, 0–1)

Reveal.getSlidePath();            // Returns slide path string (for hash routing)

// Query hash from URL
Reveal.getQueryHash();
// Returns object from URL query parameters
```

### Slide Content

```javascript
// Get slide metadata
Reveal.getSlidesAttributes();     // All slides' data attributes
Reveal.getSlideBackground(indexh, indexv);  // Background element for a slide
Reveal.getSlideNotes();           // Speaker notes for current slide
```

### Modes

```javascript
// Toggle modes
Reveal.toggleHelp();         // Show/hide keyboard shortcuts overlay
Reveal.toggleOverview();     // Toggle overview mode
Reveal.toggleAutoSlide();    // Toggle auto-advance
Reveal.togglePause();        // Pause/resume (dims the screen)

// Check mode state
Reveal.isOverview();         // true/false
Reveal.isAutoSliding();      // true/false
Reveal.isPaused();           // true/false
```

### Mode State Checks

```javascript
Reveal.isOverview();         // true when in overview mode
Reveal.isPaused();           // true when presentation is paused
Reveal.isAutoSliding();       // true when auto-slide is active
Reveal.isSpeakerNotes();      // true in speaker notes window
Reveal.isFirstSlide();        // true on first slide
Reveal.isLastSlide();         // true on last slide
Reveal.isVerticalSlide();     // true if current slide is in a vertical stack
```

### Slide Navigation Checks

```javascript
Reveal.hasHorizontalSlides();   // true if any horizontal navigation exists
Reveal.hasVerticalSlides();     // true if any vertical navigation exists
```

### DOM Access

```javascript
Reveal.getRevealElement();       // The .reveal container element
Reveal.getSlidesElement();       // The .slides container element
Reveal.getViewportElement();     // The .reveal-viewport element
Reveal.getBackgroundsElement();  // Background container element
```

### Utility

```javascript
// Re-layout after DOM changes
Reveal.layout();

// Sync after adding/removing slides dynamically
Reveal.sync();

// Shuffle slide order
Reveal.shuffle();

// Get current config object
Reveal.getConfig();

// Get current presentation scale factor
Reveal.getScale();
```

### Removing Slides

```javascript
// Remove slides that are conditionally hidden
Reveal.removeHiddenSlides();
```

---

## Event System

Listen for presentation events using `Reveal.on()` and clean up with `Reveal.off()`.

### Core Events

```javascript
// Presentation is ready
Reveal.on('ready', (event) => {
  console.log('Presentation ready', event.indexh, event.indexv);
});

// Slide changed
Reveal.on('slidechanged', (event) => {
  console.log('From:', event.previousSlide);
  console.log('To:', event.currentSlide);
  console.log('Index:', event.indexh, event.indexv);
});

// Slide transition animation completed
Reveal.on('slidetransitionend', (event) => {
  console.log('Transition complete for:', event.currentSlide);
});

// Viewport resized
Reveal.on('resize', (event) => {
  console.log('New scale:', event.scale);
});
```

### Fragment Events

```javascript
Reveal.on('fragmentshown', (event) => {
  console.log('Fragment shown:', event.fragment);
});

Reveal.on('fragmenthidden', (event) => {
  console.log('Fragment hidden:', event.fragment);
});
```

### Overview Events

```javascript
Reveal.on('overviewshown', () => {
  console.log('Overview activated');
});

Reveal.on('overviewhidden', () => {
  console.log('Overview deactivated');
});
```

### Auto-Slide Events

```javascript
Reveal.on('autoslideresumed', () => {
  console.log('Auto-slide resumed');
});

Reveal.on('autoslidepaused', () => {
  console.log('Auto-slide paused');
});
```

### Removing Event Listeners

```javascript
function onSlideChange(event) {
  console.log('Slide changed');
}

// Add listener
Reveal.on('slidechanged', onSlideChange);

// Remove specific listener
Reveal.off('slidechanged', onSlideChange);
```

### Event-Driven Patterns

**Example — Track slide visits:**

```javascript
const visited = new Set();
Reveal.on('slidechanged', (event) => {
  const id = event.currentSlide.id || Reveal.getIndices().h;
  visited.add(id);
  console.log(`Visited ${visited.size} of ${Reveal.getTotalSlides()} slides`);
});
```

**Example — Pause video when leaving a slide:**

```javascript
Reveal.on('slidechanged', (event) => {
  // Pause videos on previous slide
  const videos = event.previousSlide?.querySelectorAll('video');
  videos?.forEach(v => v.pause());
});
```

---

## Custom Keyboard Bindings

Customize keyboard shortcuts for your presentation.

### Disable Default Shortcuts

```javascript
Reveal.initialize({
  keyboard: false,  // Disable all keyboard navigation
});
```

### Override Specific Keys

Use the `keyboard` config to map key codes to actions:

```javascript
Reveal.initialize({
  keyboard: {
    13: 'next',          // Enter key → next slide
    32: null,            // Space → disabled (null removes binding)
    27: () => {          // Escape → custom function
      console.log('Escape pressed');
    },
  },
});
```

Common key codes:

| Key | Code |
|-----|------|
| Enter | 13 |
| Escape | 27 |
| Space | 32 |
| Left Arrow | 37 |
| Right Arrow | 39 |
| Up Arrow | 38 |
| Down Arrow | 40 |
| F | 70 |
| G | 71 |
| O | 79 |
| S | 83 |

### Add Key Bindings at Runtime

Add custom keyboard shortcuts after initialization:

```javascript
// Add a binding with description (shown in help overlay)
Reveal.addKeyBinding({ keyCode: 84, key: 'T' }, () => {
  console.log('T pressed — custom action');
});

// Add binding that triggers a named navigation action
Reveal.addKeyBinding({ keyCode: 82, key: 'R' }, 'next');

// Remove a binding
Reveal.removeKeyBinding(84);
```

### Conditional Keyboard

Only process keyboard events when the presentation has focus:

```javascript
Reveal.initialize({
  keyboardCondition: () => {
    // Return true to process keyboard events, false to ignore
    return document.activeElement === document.body;
  },
});
```

---

## Presentation State

Save and restore the exact state of a presentation — useful for resuming where a user left off.

### Save & Restore

```javascript
// Capture current state
const state = Reveal.getState();
// Returns: { indexh, indexv, indexf, paused, overview }

// Save to localStorage
localStorage.setItem('presentationState', JSON.stringify(state));

// Restore state later
const saved = JSON.parse(localStorage.getItem('presentationState'));
if (saved) {
  Reveal.setState(saved);
}
```

### Example — Auto-resume

```javascript
Reveal.on('slidechanged', () => {
  localStorage.setItem('presentationState', JSON.stringify(Reveal.getState()));
});

// On page load, restore position
window.addEventListener('load', () => {
  const saved = localStorage.getItem('presentationState');
  if (saved) {
    Reveal.setState(JSON.parse(saved));
  }
});
```

This is useful for long presentations where users may close the browser and return later.

---

## Multiple Presentations

Run more than one reveal.js instance on the same page.

### Creating Multiple Instances

Use the `Reveal` constructor instead of the default singleton:

```javascript
// Instead of Reveal.initialize(), use new Reveal()
const presentation1 = new Reveal(document.querySelector('.presentation-1'), {
  embedded: true,
  keyboard: true,
});

const presentation2 = new Reveal(document.querySelector('.presentation-2'), {
  embedded: true,
  keyboard: true,
});

presentation1.initialize();
presentation2.initialize();
```

### HTML Structure

```html
<div class="presentation-1 reveal">
  <div class="slides">
    <section>Slide 1A</section>
    <section>Slide 1B</section>
  </div>
</div>

<div class="presentation-2 reveal">
  <div class="slides">
    <section>Slide 2A</section>
    <section>Slide 2B</section>
  </div>
</div>
```

### Embedded Mode

When embedding a presentation inside a web page (not fullscreen), use `embedded: true`:

```javascript
Reveal.initialize({
  embedded: true,    // Only respond to keyboard when focused
  keyboard: true,
  touch: true,
});
```

### Cleanup

Destroy a presentation instance when no longer needed:

```javascript
presentation1.destroy();
// Removes event listeners, clears DOM references, stops auto-slide
```

---

## Configuration Reference

Complete list of all reveal.js configuration options. Use these in the `Reveal.initialize()` call.

### Presentation & Navigation

| Option | Default | Description |
|--------|---------|-------------|
| `width` | `960` | Presentation width in pixels |
| `height` | `700` | Presentation height in pixels |
| `margin` | `0.04` | Margin factor around slide content |
| `minScale` | `0.2` | Minimum scaling factor |
| `maxScale` | `2.0` | Maximum scaling factor |
| `center` | `false` | Vertically center content |
| `disableLayout` | `false` | Disable responsive scaling (use CSS instead) |
| `display` | `'block'` | Display mode for slide elements |
| `navigationMode` | `'default'` | `'default'` (grid), `'linear'` (left/right only), `'grid'` |

### Controls & UI

| Option | Default | Description |
|--------|---------|-------------|
| `controls` | `true` | Show navigation arrows |
| `controlsTutorial` | `true` | Show control hints on first visit |
| `controlsLayout` | `'bottom-right'` | Position: `'bottom-right'` or `'edges'` |
| `controlsBackArrows` | `'faded'` | Back arrow visibility: `'faded'`, `'hidden'`, `'visible'` |
| `progress` | `true` | Show progress bar |
| `slideNumber` | `false` | Show slide number: `true`, `false`, `'c/t'`, `'h.v'`, `'h.v.t'` |
| `showSlideNumber` | `'all'` | When to show: `'all'`, `'print'`, `'speaker'` |
| `hash` | `true` | Update URL hash for each slide |
| `hashOneBasedIndex` | `false` | Use 1-based indexing in URL hash |
| `respondToHashChanges` | `true` | Navigate when URL hash changes |
| `history` | `false` | Push each slide change to browser history |
| `jumpToSlide` | `true` | Enable G key jump-to-slide |
| `overview` | `true` | Enable overview mode (ESC/O) |
| `help` | `true` | Show keyboard shortcuts help (?) |
| `hideInactiveCursor` | `true` | Hide cursor after inactivity |
| `hideCursorTime` | `5000` | ms before hiding inactive cursor |

### Transitions & Animation

| Option | Default | Description |
|--------|---------|-------------|
| `transition` | `'slide'` | Slide transition: `none`, `fade`, `slide`, `convex`, `concave`, `zoom` |
| `transitionSpeed` | `'default'` | Speed: `default`, `fast`, `slow` |
| `backgroundTransition` | `'fade'` | Background transition type |
| `fragments` | `true` | Enable fragment animations |
| `fragmentInURL` | `true` | Include fragment index in URL hash |

### Auto-Slide

| Option | Default | Description |
|--------|---------|-------------|
| `autoSlide` | `0` | Auto-advance interval in ms (0 = disabled) |
| `autoSlideStoppable` | `true` | Allow pausing auto-slide with user input |
| `autoSlideMethod` | `null` | Custom navigation function for auto-slide |
| `defaultTiming` | `null` | Default timing per slide (seconds) |
| `loop` | `false` | Loop back to first slide after last |

### Input

| Option | Default | Description |
|--------|---------|-------------|
| `keyboard` | `true` | Enable keyboard navigation |
| `keyboardCondition` | `null` | Function returning boolean for keyboard processing |
| `touch` | `true` | Enable touch/swipe navigation |
| `mouseWheel` | `false` | Navigate with mouse wheel |
| `previewLinks` | `false` | Open all links in lightbox preview |

### Media & Iframes

| Option | Default | Description |
|--------|---------|-------------|
| `autoPlayMedia` | `null` | Auto-play media on slide entry: `true`, `false`, `null` (only autoplayed previously) |
| `preloadIframes` | `null` | Preload iframes: `true`, `false`, `null` (lazy load) |
| `preventIframeAutoFocus` | `true` | Prevent iframes from stealing focus |

### PDF Export

| Option | Default | Description |
|--------|---------|-------------|
| `pdfMaxPagesPerSlide` | `Number.POSITIVE_INFINITY` | Max pages per slide in PDF |
| `pdfSeparateFragments` | `true` | Create separate PDF pages for fragments |
| `pdfPageHeightOffset` | `-1` | Height offset for PDF pages |
| `showNotes` | `false` | Show speaker notes: `true`, `'separate-page'` |

### Performance & Rendering

| Option | Default | Description |
|--------|---------|-------------|
| `viewDistance` | `3` | Pre-load slides within this distance |
| `mobileViewDistance` | `2` | Pre-load distance on mobile |
| `shuffle` | `false` | Shuffle slide order on load |

### Auto-Animate Advanced

| Option | Default | Description |
|--------|---------|-------------|
| `autoAnimateMatcher` | `null` | Custom element matching function |
| `autoAnimateUnmatched` | `true` | Animate unmatched elements |
| `autoAnimateStyles` | `[]` | Additional CSS properties to animate |

### Embedding & Integration

| Option | Default | Description |
|--------|---------|-------------|
| `embedded` | `false` | Embedded mode (only respond when focused) |
| `pause` | `true` | Allow pausing with B key |
| `postMessage` | `true` | Respond to postMessage API |
| `postMessageEvents` | `false` | Broadcast slide events via postMessage |
| `focusBodyOnPageVisibilityChange` | `true` | Focus body when page becomes visible |

### Runtime Configuration

Change config options after initialization:

```javascript
Reveal.configure({
  controls: false,
  transition: 'fade',
  autoSlide: 5000,
});
```

---

## Plugin Extensions

Beyond the built-in plugins (Chart.js, Search, Zoom), reveal.js has a rich plugin ecosystem.

### Plugin API

```javascript
// Check if a plugin is loaded
Reveal.hasPlugin('search');     // true/false

// Get plugin instance
Reveal.getPlugin('search');     // Plugin object

// Get all loaded plugins
Reveal.getPlugins();            // { search: {...}, zoom: {...}, ... }
```

### Animate Plugin (SVG Animations)

Create SVG animations driven by fragments or auto-slide using SVG.js. The plugin uses a JSON-in-comments pattern to define setup and animation steps.

**Setup:**

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js-plugins@4.6.0/animate/plugin.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@svgdotjs/svg.js@3.2.4/dist/svg.min.js"></script>
```

```javascript
Reveal.initialize({
  animate: { autoplay: true },
  plugins: [ RevealAnimate ],
});
```

**Usage — animation via JSON comments:**

```html
<div data-animate data-load="drawing.svg">
<!--
{
  "setup": [
    { "element": "#box1", "modifier": "opacity", "parameters": [ 0 ] }
  ],
  "animation": [
    [{ "element": "#box1", "modifier": "opacity", "parameters": [ 1 ] }]
  ]
}
-->
</div>
```

Key concepts:
- `data-animate` — Marks an element as an animation container
- `data-load="file.svg"` — Loads an external SVG (requires loadcontent plugin)
- `setup` array — Manipulations applied when the slide loads
- `animation` array — Steps triggered by fragments or auto-slide
- Each item specifies `element` (CSS selector), `modifier` (SVG.js method), and `parameters`

For detailed usage including fragment-driven animations, sequential effects, and advanced examples, see [plugin-animate.md](plugins/plugin-animate.md).

### D3.js Integration

Embed D3.js or other JavaScript visualizations in slides.

**Setup:**

```html
<script src="https://cdn.jsdelivr.net/npm/reveald3@2.0.0/reveald3.min.js"></script>
```

```javascript
Reveal.initialize({
  plugins: [RevealD3],
});
```

**Usage — embed external visualization files:**

```html
<section>
  <h2>Interactive Visualization</h2>
  <div class="fig-container" data-file="visualizations/chart.html"></div>
</section>
```

**Fragment-driven transitions** — add a `_transitions` array in the visualization file's script:

```javascript
// Inside visualizations/chart.html
const _transitions = [
  { from: 'state1', to: 'state2' },
  { from: 'state2', to: 'state3' },
];
```

Each fragment click advances through the transitions array, letting you build step-by-step data visualizations.

## References

- [API](official-docs/api.md)
- [Events](official-docs/events.md)
- [Keyboard](official-docs/keyboard.md)
- [Presentation State](official-docs/presentation-state.md)
- [Multiple Presentations](official-docs/initialization.md)
- [Configuration](official-docs/config.md)
- [PDF Export](official-docs/pdf-export.md)
- [Presentation Size](official-docs/presentation-size.md)
- [Multiplex](official-docs/multiplex.md)
- [Animate Plugin](plugins/plugin-animate.md)
- [D3 Plugin](plugins/plugin-d3.md)
