# Reveal.js Anti-Patterns and Common Pitfalls

Common issues encountered when working with Reveal.js and their solutions.

---

## CSS Specificity Issues

### Problem: Custom styles not applying

Reveal.js default styles have high specificity. Adding a class directly to an element may not take effect.

**Incorrect:**
```html
<section>
  <h2 class="text-primary">Title</h2>
</section>
```

If `.text-primary` is defined as:
```css
.text-primary {
  color: var(--primary-color);
}
```

It may not work because Reveal.js defaults can be more specific.

**Solution:**

1. **Increase selector specificity** — use the `.reveal` prefix:
```css
.reveal .text-primary {
  color: var(--primary-color) !important;
}
```

2. **Use `!important`** — acceptable for utility classes:
```css
.text-primary {
  color: var(--primary-color) !important;
}
```

---

## Layout Issues

### Problem: Content overflowing slide boundaries

When content is too dense, it overflows the visible area and gets clipped.

**Detection method:**
Inject the browser-side detection script and check the browser console for overflow reports:
```bash
node scripts/check-overflow.js ./presentation/index.html --check
# Restore the original file after review:
node scripts/check-overflow.js ./presentation/index.html --restore
```

**Solutions:**

1. **Reduce content** — follow the word limit guidelines
2. **Use smaller fonts** — apply `.text-sm` or `.text-base` classes
3. **Split across slides** — use vertical stacking or multiple slides
4. **Use compact layout** — apply the `.compact` class to reduce spacing

---

## Fragment Animation Issues

### Problem: Fragment animation order is chaotic

**Incorrect:**
```html
<ul>
  <li class="fragment">First item</li>
  <li class="fragment">Second item</li>
  <li>Third item (no fragment)</li>
  <li class="fragment">Fourth item</li>
</ul>
```

The third item displays immediately, breaking the animation flow.

**Solution:**
Ensure all sibling elements either all have fragments or none do. Alternatively, use `data-fragment-index` to control order:
```html
<ul>
  <li class="fragment" data-fragment-index="0">First item</li>
  <li class="fragment" data-fragment-index="1">Second item</li>
  <li class="fragment" data-fragment-index="2">Third item</li>
  <li class="fragment" data-fragment-index="3">Fourth item</li>
</ul>
```

---

## Image Issues

### Problem: Inconsistent image sizes causing layout jumps

**Solutions:**
1. Use CSS to constrain image maximum dimensions:
```css
.reveal section img {
  max-width: 100%;
  max-height: 500px;
  object-fit: contain;
}
```

2. Use fixed-size containers:
```html
<div style="height: 400px; display: flex; align-items: center;">
  <img src="image.png" style="max-height: 100%;">
</div>
```

---

## Mermaid Diagram Issues

### Problem: Mermaid diagrams too small or too large

**Solution:**
Adjust size using the `config` directive:
```html
<pre class="mermaid">
%%{init: {'theme': 'base', 'themeVariables': { 'fontSize': '18px' }}}%%
graph TD
    A[Start] --> B[End]
</pre>
```

Or set in CSS:
```css
.mermaid {
  font-size: 18px;
}
```

---

## Code Block Issues

### Problem: Long code lines overflowing

**Solutions:**
1. Enable code wrapping in Reveal.js config:
```javascript
Reveal.initialize({
  // ...
  highlight: {
    lineNumbers: true,
    wrap: true  // Enable wrapping
  }
});
```

2. Or manually wrap lines, keeping each under 60 characters

---

## Responsive Design Issues

### Problem: Layout breaks at different screen sizes

**Solutions:**
1. Use relative units (`rem`, `%`, `vw/vh`) instead of fixed pixels
2. Use the `r-fit-text` class for adaptive headings:
```html
<h2 class="r-fit-text">Adaptive Heading</h2>
```

3. Use the Overflow Checker to detect layout issues at different resolutions:
```bash
node scripts/check-overflow.js ./index.html --check
```

---

## Initialization Order Issues

### Problem: Plugins not loading correctly

**Incorrect:**
```html
<script src="dist/reveal.js"></script>
<script>
  Reveal.initialize({
    plugins: [RevealNotes, RevealMermaid]  // RevealMermaid may not be defined yet
  });
</script>
<script src="plugin/mermaid/mermaid.js"></script>
```

**Solution:**
Ensure plugin scripts load before `initialize()`:
```html
<script src="dist/reveal.js"></script>
<script src="plugin/notes/notes.js"></script>
<script src="plugin/mermaid/mermaid.js"></script>
<script>
  Reveal.initialize({
    plugins: [RevealNotes, RevealMermaid]
  });
</script>
```
