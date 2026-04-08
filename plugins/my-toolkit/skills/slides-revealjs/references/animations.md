# Animations & Transitions

Guide for adding motion to your presentation: progressive content reveal, automatic element animations, slide transitions, and auto-advance.

## Table of Contents

1. [Fragments](#fragments)
2. [Auto-Animate](#auto-animate)
3. [Slide Transitions](#slide-transitions)
4. [Auto-Slide](#auto-slide)

---

## Fragments

Fragments let you reveal content progressively — elements appear one at a time as you advance through a slide. Any element with `class="fragment"` becomes a fragment.

### Built-in Fragment Styles

Add a fragment style class to control how the element appears:

| Class | Effect |
|-------|--------|
| `fragment fade-out` | Fades out |
| `fragment fade-up` | Fades in from bottom |
| `fragment fade-down` | Fades in from top |
| `fragment fade-left` | Fades in from left |
| `fragment fade-right` | Fades in from right |
| `fragment fade-in-then-out` | Fades in, then out on next step |
| `fragment fade-in-then-semi-out` | Fades in, then dims to 50% |
| `fragment highlight-red` | Text turns red |
| `fragment highlight-green` | Text turns green |
| `fragment highlight-blue` | Text turns blue |
| `fragment highlight-current-red` | Current step turns red (others reset) |
| `fragment highlight-current-green` | Current step turns green (others reset) |
| `fragment highlight-current-blue` | Current step turns blue (others reset) |
| `fragment slide-up` | Slides in from below |
| `fragment slide-down` | Slides in from above |
| `fragment slide-left` | Slides in from right |
| `fragment slide-right` | Slides in from left |

**Default**: `fragment` alone (no style class) is equivalent to `fragment fade-in`.

### Usage Examples

```html
<!-- Basic fade-in -->
<p class="fragment">Appears first</p>
<p class="fragment">Appears second</p>
<p class="fragment">Appears third</p>

<!-- Mixed styles -->
<p class="fragment fade-up">Slides up from below</p>
<p class="fragment highlight-red">Turns red</p>
<p class="fragment fade-in-then-out">Appears then disappears</p>

<!-- On list items (applies to each item) -->
<ul>
  <li class="fragment">Item 1</li>
  <li class="fragment">Item 2</li>
  <li class="fragment">Item 3</li>
</ul>
```

### Custom Fragment Order

By default, fragments appear in DOM order. Override with `data-fragment-index`:

```html
<p class="fragment" data-fragment-index="3">Appears third</p>
<p class="fragment" data-fragment-index="1">Appears first</p>
<p class="fragment" data-fragment-index="2">Appears second</p>
```

Multiple fragments can share the same index — they appear simultaneously:

```html
<p class="fragment" data-fragment-index="1">Appears together</p>
<p class="fragment" data-fragment-index="1">With this one</p>
<p class="fragment" data-fragment-index="2">Then this one</p>
```

### Nested Fragments

Nesting fragments creates a sequential hierarchy — inner fragments reveal after outer ones:

```html
<div class="fragment">
  <p>Container appears first</p>
  <p class="fragment">Then this text inside appears</p>
</div>
```

### Custom Fragment Animations

Define your own fragment effects via CSS. Use `.fragment.effectname` for the hidden state and `.fragment.effectname.visible` for the revealed state:

```css
/* Custom "blur-in" effect */
.fragment.blur-in {
  filter: blur(10px);
  opacity: 0;
  transition: all 0.4s ease;
}

.fragment.blur-in.visible {
  filter: blur(0);
  opacity: 1;
}
```

Then use it in HTML:

```html
<p class="fragment blur-in">Custom blur-in effect</p>
```

### Fragment Events

Listen for fragment navigation in JavaScript:

```javascript
Reveal.on('fragmentshown', function(event) {
  // event.fragment = the fragment element
  // event.fragments = array of all fragments shown in this step
});

Reveal.on('fragmenthidden', function(event) {
  // event.fragment = the fragment element
  // event.fragments = array of all fragments hidden in this step
});
```

---

## Auto-Animate

Auto-Animate automatically transitions matching elements between consecutive slides. When two slides both contain an element with the same `data-id`, reveal.js animates it from its position/state on the first slide to its position/state on the second.

### Basic Usage

Add `data-auto-animate` to two consecutive `<section>` elements. Matching elements (by tag name or `data-id`) will animate between slides:

```html
<section data-auto-animate>
  <h2>Step 1</h2>
  <p data-id="box" style="background: #2196F3; width: 100px; height: 100px;"></p>
</section>

<section data-auto-animate>
  <h2>Step 2</h2>
  <p data-id="box" style="background: #F44336; width: 200px; height: 200px; margin-left: 100px;"></p>
</section>
```

The box smoothly transitions its size, color, and position.

### Matching by `data-id`

Elements with the same `data-id` value are matched across slides. This is more reliable than tag-name matching:

```html
<section data-auto-animate>
  <h2 data-id="title">Introduction</h2>
  <p data-id="desc" style="font-size: 14pt;">A brief overview</p>
</section>

<section data-auto-animate>
  <h2 data-id="title" style="font-size: 48pt; color: #E91E63;">Deep Dive</h2>
  <p data-id="desc" style="font-size: 24pt;">A detailed explanation</p>
</section>
```

### Grouping with `data-auto-animate-id`

When you have multiple auto-animate sequences, use `data-auto-animate-id` to group them. Only slides with the same ID animate between each other:

```html
<!-- Group A -->
<section data-auto-animate data-auto-animate-id="group-a">
  <p data-id="item">First state</p>
</section>
<section data-auto-animate data-auto-animate-id="group-a">
  <p data-id="item">Second state</p>
</section>

<!-- Group B (separate sequence) -->
<section data-auto-animate data-auto-animate-id="group-b">
  <p data-id="item">Different sequence</p>
</section>
```

### Restarting with `data-auto-animate-restart`

To break an auto-animate chain (start a fresh sequence), add `data-auto-animate-restart`:

```html
<section data-auto-animate>
  <p data-id="x">State 1</p>
</section>
<section data-auto-animate>
  <p data-id="x">State 2</p>
</section>
<!-- This breaks the chain -->
<section data-auto-animate data-auto-animate-restart>
  <p data-id="x">State 3 (fresh start)</p>
</section>
```

### Animation Timing and Easing

Control animation speed per-slide:

```html
<section data-auto-animate data-auto-animate-duration="2.0">
  <!-- 2-second animation -->
</section>
```

Override easing function:

```html
<section data-auto-animate data-auto-animate-easing="ease-in-out">
  <!-- Custom easing -->
</section>
```

### Delaying Individual Elements

Add a delay to specific elements so they animate after others:

```html
<section data-auto-animate>
  <h2>First</h2>
  <p data-id="delayed" style="--r-auto-animate-delay: 0.5s;">I animate later</p>
</section>
```

### Excluding Elements from Auto-Animate

Prevent specific elements from being animated:

```html
<section data-auto-animate>
  <h2>Animated</h2>
  <p data-auto-animate-delay="0">I animate</p>
  <p data-auto-animate-exclude>I don't animate</p>
</section>
```

### Auto-Animate with Code Blocks

Code blocks auto-animate between matching content. The diff is highlighted:

```html
<section data-auto-animate>
  <pre><code data-trim>
function hello() {
  console.log("hello");
}
  </code></pre>
</section>
<section data-auto-animate>
  <pre><code data-trim>
function hello(name) {
  console.log("hello " + name);
  return name;
}
  </code></pre>
</section>
```

Changed lines are briefly highlighted during the transition.

### Moving Elements Between Containers

Elements can move from one container to another if they share a `data-id`:

```html
<section data-auto-animate>
  <div style="display: flex; gap: 20px;">
    <div data-id="card-1" style="background: #E3F2FD; padding: 20px;">Card A</div>
    <div data-id="card-2" style="background: #E8F5E9; padding: 20px;">Card B</div>
  </div>
</section>
<section data-auto-animate>
  <div style="display: flex; gap: 20px;">
    <div data-id="card-2" style="background: #E8F5E9; padding: 20px;">Card B</div>
    <div data-id="card-1" style="background: #E3F2FD; padding: 20px;">Card A</div>
  </div>
</section>
```

The cards swap positions with a smooth animation.

---

## Slide Transitions

Transitions control how the entire slide changes when navigating between slides.

### Global Transition

Set the default transition in `Reveal.initialize()`:

```javascript
Reveal.initialize({
  transition: 'slide', // none/fade/slide/convex/concave/zoom
});
```

| Value | Effect |
|-------|--------|
| `none` | Instant switch |
| `fade` | Cross-fade |
| `slide` | Horizontal slide |
| `convex` | 3D convex rotation |
| `concave` | 3D concave rotation |
| `zoom` | Zoom in from previous slide |

### Per-Slide Transition

Override the transition for specific slides using `data-transition`:

```html
<section data-transition="zoom">
  <h2>This slide zooms in</h2>
</section>

<section data-transition="convex">
  <h2>This slide rotates convex</h2>
</section>
```

### Separate In/Out Transitions

Use `data-transition-in` and `data-transition-out` for different enter/exit effects:

```html
<section data-transition-in="zoom" data-transition-out="fade">
  <h2>Zooms in, fades out</h2>
</section>
```

### Transition Speed

Control animation speed globally or per-slide:

```javascript
// Global
Reveal.initialize({
  transitionSpeed: 'default', // default/fast/slow
});
```

```html
<!-- Per-slide -->
<section data-transition-speed="fast">
  <h2>Fast transition</h2>
</section>
```

### Background Transitions

Background transitions are separate from content transitions:

```javascript
Reveal.initialize({
  backgroundTransition: 'fade', // none/fade/slide/convex/concave/zoom
});
```

Override per slide:

```html
<section data-background-transition="zoom">
  <h2>Background zooms</h2>
</section>
```

---

## Auto-Slide

Automatically advance through slides at a timed interval.

### Global Auto-Slide

Set `autoSlide` in config (milliseconds between slides):

```javascript
Reveal.initialize({
  autoSlide: 5000, // 5 seconds per slide
});
```

### Per-Slide Override

Override timing on individual slides:

```html
<section data-autoslide="10000">
  <h2>This slide stays for 10 seconds</h2>
</section>

<section data-autoslide="2000">
  <h2>This slide stays for 2 seconds</h2>
</section>
```

### Auto-Slide with Fragments

By default, auto-slide pauses at fragments until all are revealed, then advances to the next slide. Control this behavior:

```javascript
Reveal.initialize({
  autoSlideStoppable: true, // Pause on user interaction (default: true)
  autoSlideMethod: Reveal.navigateRight, // Direction to auto-advance
});
```

### Resume After Interaction

After a user manually navigates, auto-slide resumes after a delay. The pause/play control appears in the bottom-right corner.

### Auto-Slide Events

```javascript
Reveal.on('autoslideresumed', function(event) { /* ... */ });
Reveal.on('autoslidepaused', function(event) { /* ... */ });
```

### Loop Presentations

Combine auto-slide with loop for a self-running kiosk display:

```javascript
Reveal.initialize({
  autoSlide: 5000,
  loop: true,
  controls: false,
});
```

## References

- [Fragments](official-docs/fragments.md)
- [Slide Transitions](official-docs/transitions.md)
- [Auto-Animate](official-docs/auto-animate.md)
- [Auto-Slide](official-docs/auto-slide.md)
