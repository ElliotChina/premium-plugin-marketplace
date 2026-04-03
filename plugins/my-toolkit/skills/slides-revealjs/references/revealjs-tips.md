# Reveal.js Tips

Common reveal.js techniques and code snippets.

---

## Design & Visual Quality

For comprehensive design guidance including color palette selection, typography hierarchy, slide archetypes, content density limits, and visual review checklists, see [Slide Design Guide](./slide-design-guide.md).

---

## 1) Title slide with custom background

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

---

## 2) Move/resize a logo after leaving title slide

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

---

## 3) Background image sizing (`cover` vs `contain`)

`cover` fills the slide and may crop. `contain` preserves the entire image.

```html
<section data-background-image="images/2024.jpg" data-background-size="cover"></section>
<section data-background-image="images/2024.jpg" data-background-size="contain"></section>
```

---

## 4) Slide structure control (replacement for Quarto `slide-level`)

Pure reveal.js does not use Pandoc `slide-level`. Control structure explicitly:

- HTML mode: one `<section>` per slide, nested `<section>` for vertical slides.
- Markdown mode: use configured separators (`---`, `--`) to split slides.

---

## 5) Emoji support

Quarto's `from: markdown+emoji` is not a reveal.js feature. In reveal.js:

- Use native Unicode emoji directly.
- Or render emoji through your markdown/HTML pipeline before reveal initializes.

---

## 6) Fit large text and stretch media

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

---

## 7) Reveal content on key press with fragments

```html
<section>
  <h2>It's a candy dog</h2>
  <p style="font-size: 44pt; color: #75aadb;">Would you like to see a candy dog?</p>
  <img class="fragment fade-up" src="./images/dog.webp" alt="Candy dog" />
</section>
```

---

## 8) Two-column and 4-quadrant layouts

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

---

## 9) Custom inline short-code transform (`==text==` to `<mark>text</mark>`)

```js
function convertMarkedTextInSlide(slide) {
  if (!slide) return;
  // Note: In production, consider using a sanitizer like DOMPurify
  const content = slide.textContent;
  // Transform ==text== patterns safely
}

Reveal.on('ready', (event) => convertMarkedTextInSlide(event.currentSlide));
Reveal.on('slidechanged', (event) => convertMarkedTextInSlide(event.currentSlide));
```

---

## 10) Inline style and custom CSS

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

---

## 11) Hide captions and style callouts from generated output

Some pipelines generate caption or callout markup. Hide if not needed:

```css
.reveal p.caption,
.reveal figcaption {
  display: none;
}
```

---

## 12) Vertical flow, slide IDs, menu labels, numbering, and notes

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

---

## Related References

- [Slide Design Guide](./slide-design-guide.md) - Design principles, color palettes, typography
- [Anti-Patterns](./anti-patterns.md) - Common pitfalls and solutions
- [Quarto Migration](./quarto-migration.md) - Migrating from Quarto to reveal.js
- [Base Styles](./base-styles.css) - CSS utilities and components
