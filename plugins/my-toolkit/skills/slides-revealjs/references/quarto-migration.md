# Quarto to reveal.js Migration Guide

This reference helps you migrate from Quarto (`.qmd`) to pure reveal.js HTML presentations. Quarto has its own extended Markdown syntax that does not work directly in reveal.js.

## Key Differences

| Feature | Quarto Syntax | reveal.js Equivalent |
|---------|---------------|---------------------|
| Slide separators | `---` (configurable) | `<section>` elements |
| Vertical slides | `--` or explicit nesting | Nested `<section><section>` |
| Columns | `::: columns` / `::: {.column}` | HTML/CSS flexbox or grid |
| Slide level | `slide-level: X` in YAML | Explicit `<section>` nesting |
| Emoji | `from: markdown+emoji` | Use Unicode emoji directly |
| Callouts | `::: {.callout}` blocks | Custom HTML/CSS panels |
| Speaker notes | `::: {.notes}` | `<aside class="notes">` |
| Image captions | Automatic `![alt](img){fig-cap="..."}` | Manual `<figcaption>` |

## Migration Steps

### 1. Slide Structure

Quarto uses `---` to separate slides and `slide-level` to control nesting. In reveal.js, structure is explicit:

**Quarto:**
```markdown
---
title: "My Deck"
slide-level: 2
---

# Section

## Slide 1

## Slide 2
```

**reveal.js HTML:**
```html
<div class="reveal">
  <div class="slides">
    <section>
      <h1>Section</h1>
    </section>
    <section>
      <section>
        <h2>Slide 1</h2>
      </section>
      <section>
        <h2>Slide 2</h2>
      </section>
    </section>
  </div>
</div>
```

### 2. Columns

Quarto's `::: columns` syntax is not native reveal.js. Convert to HTML/CSS:

**Quarto:**
```markdown
::: columns
::: {.column width="60%"}
Left content
:::
::: {.column width="40%"}
Right content
:::
:::
```

**reveal.js:**
```html
<section>
  <div class="cols">
    <div class="col col-60">
      <p>Left content</p>
    </div>
    <div class="col col-40">
      <p>Right content</p>
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

.reveal .col-60 { flex: 0 0 60%; }
.reveal .col-40 { flex: 0 0 40%; }
```

### 3. Emoji

Quarto supports `from: markdown+emoji` to convert `:smile:` to Unicode. In reveal.js:

- Use native Unicode emoji directly: 😄
- Or render emoji through your markdown pipeline before reveal initializes

### 4. Callouts and Captions

Quarto auto-generates callout blocks and figure captions. In pure reveal.js:

**Hide Quarto-emitted markup (if using a shared pipeline):**
```css
.reveal p.caption,
.reveal figcaption {
  display: none;
}

.reveal .callout-title {
  display: none;
}
```

**Or build custom callouts:**
```html
<section>
  <div class="panel callout">
    <strong>Note:</strong> Important information here.
  </div>
</section>
```

### 5. Speaker Notes

Quarto uses `::: {.notes}` syntax. In reveal.js, use the native `<aside>` element:

**Quarto:**
```markdown
::: {.notes}
Speaker notes here.
:::
```

**reveal.js:**
```html
<section>
  <h2>Slide Content</h2>
  <aside class="notes">Speaker notes here.</aside>
</section>
```

Enable the Notes plugin:
```js
Reveal.initialize({
  plugins: [RevealNotes],
});
```

Press `S` during presentation to open speaker view.

### 6. Figure Options

Quarto supports extensive figure options in code chunks. In reveal.js, use standard HTML:

```html
<section>
  <figure>
    <img src="image.png" alt="Description" style="max-height: 500px;">
    <figcaption>Optional caption</figcaption>
  </figure>
</section>
```

For full-bleed backgrounds:
```html
<section data-background-image="image.png" data-background-size="cover">
  <h2>Content over image</h2>
</section>
```

## Preserve Behavior First

When migrating from Quarto to reveal.js:

1. **Fragment timing:** Check any `fragment` classes and ensure reveal order matches.
2. **Navigation flow:** Verify horizontal/vertical slide structure matches the original.
3. **Note visibility:** Ensure speaker notes appear correctly in presenter view.
4. **Visual styling:** Match the original appearance before making design changes.

After behavior is preserved, adjust visual styling as needed.

## External Resource

- [Quarto reveal.js tips](https://www.avonture.be/blog/quarto-revealjs-tips/) — Extract reveal.js-applicable patterns; ignore Quarto-only syntax.
