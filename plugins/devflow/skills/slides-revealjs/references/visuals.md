# Visuals & Media

Guide for slide backgrounds, media overlays, speaker notes, and visual enhancements.

## Table of Contents

1. [Backgrounds](#backgrounds)
2. [Lightbox](#lightbox)
3. [Speaker Notes](#speaker-notes)

---

## Backgrounds

Backgrounds apply to the full browser viewport behind slide content. Set them via `data-background-*` attributes on `<section>` elements.

### Solid Color Backgrounds

```html
<section data-background-color="#1C2833">
  <h2 style="color: white;">Dark background</h2>
</section>

<section data-background-color="aquamarine">
  <h2>Named color background</h2>
</section>
```

### Gradient Backgrounds

```html
<!-- Linear gradient -->
<section data-background-gradient="linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
  <h2 style="color: white;">Purple gradient</h2>
</section>

<!-- Radial gradient -->
<section data-background-gradient="radial-gradient(circle, #2980b9, #2c3e50)">
  <h2 style="color: white;">Radial gradient</h2>
</section>
```

### Image Backgrounds

```html
<!-- Full cover -->
<section data-background-image="https://example.com/photo.jpg">
  <h2>Image background</h2>
</section>

<!-- With sizing and position -->
<section data-background-image="https://example.com/photo.jpg"
         data-background-size="contain"
         data-background-position="center"
         data-background-repeat="no-repeat">
  <h2>Contained image</h2>
</section>
```

**Image sizing options:**
- `data-background-size`: `cover` (default, fills viewport) | `contain` | `100px` | `50%`
- `data-background-position`: `center` (default) | `top` | `bottom` | `left` | `right` | `25% 75%`
- `data-background-repeat`: `no-repeat` (default) | `repeat` | `repeat-x` | `repeat-y`
- `data-background-opacity`: `0.5` (0–1, applies to all background types)

**Opacity for readability** — overlay a semi-transparent color on top of images:

```html
<section data-background-image="https://example.com/photo.jpg"
         data-background-opacity="0.3">
  <h2>Faded background image</h2>
</section>
```

### Video Backgrounds

```html
<section data-background-video="https://example.com/video.mp4"
         data-background-video-loop
         data-background-video-muted>
  <h2>Video background</h2>
</section>
```

**Video attributes:**
- `data-background-video-loop` — Loop the video
- `data-background-video-muted` — Mute the video (required for autoplay in most browsers)
- `data-background-opacity` — Adjust opacity (0–1)

**Multiple sources** for format compatibility:

```html
<section data-background-video='["video.webm", "video.mp4"]'
         data-background-video-loop
         data-background-video-muted>
  <h2>Video with fallback formats</h2>
</section>
```

### Iframe Backgrounds

Embed external web pages as backgrounds:

```html
<section data-background-iframe="https://example.com"
         data-background-interactive>
  <h2>Iframe background</h2>
</section>
```

- `data-background-interactive` — Allows mouse/keyboard interaction with the iframe content
- Without `data-background-interactive`, the iframe is visible but clicks pass through to the slide

### Parallax Backgrounds

Create a depth effect with a background image that scrolls at a different speed than the slide content:

```html
<section data-background-image="https://example.com/panorama.jpg"
         data-background-size="2000px"
         data-parallax-background-image="https://example.com/panorama.jpg">
</section>
```

Or configure globally:

```javascript
Reveal.initialize({
  parallaxBackgroundImage: 'https://example.com/panorama.jpg',
  parallaxBackgroundSize: '2100px 900px',
  // Optional: fine-tune movement
  parallaxBackgroundHorizontal: 200,
  parallaxBackgroundVertical: 50,
});
```

The parallax effect is automatic — the background shifts as you navigate horizontally or vertically.

### Background Transitions

Backgrounds transition independently from slide content:

```javascript
// Global
Reveal.initialize({
  backgroundTransition: 'fade', // none/fade/slide/convex/concave/zoom
});
```

Per-slide override:

```html
<section data-background-transition="zoom">
  <!-- Background zooms, content slides -->
</section>
```

### Slide Backgrounds vs Section Backgrounds

Backgrounds apply to the full viewport behind everything. If you want a colored/container effect just for the content area, use a CSS class on the `<section>` instead:

```css
/* Content area only */
.slide-dark {
  background: #1C2833;
  padding: 40px;
}
```

```html
<!-- Full viewport background -->
<section data-background-color="#1C2833">
  <h2 style="color: white;">Entire viewport is dark</h2>
</section>

<!-- Content area only -->
<section class="slide-dark">
  <h2>Only content area is dark</h2>
</section>
```

---

## Lightbox

The lightbox plugin enables click-to-preview for images, videos, and links in a full-screen overlay. This is built into reveal.js core.

### Image Preview

Click any image to show it full-screen:

```html
<img data-preview-image src="chart.png" alt="Click to enlarge">
```

### Video Preview

Click to play a video in a full-screen overlay:

```html
<a data-preview-video href="https://www.youtube.com/embed/dQw4w9WgXcQ">
  <p>Click to play video</p>
</a>

<!-- Or on an image thumbnail -->
<img data-preview-video src="thumbnail.jpg"
     data-preview-video-src="https://example.com/video.mp4">
```

### Link Preview

Open a URL in a full-screen iframe overlay:

```html
<a data-preview-link href="https://example.com">Visit website</a>
```

The link opens in a lightbox iframe instead of navigating away from the presentation.

### Combining with Fragments

Lightbox elements work with fragments — the preview only activates after the element is visible:

```html
<img class="fragment" data-preview-image src="diagram.png" alt="Appears then is clickable">
```

---

## Speaker Notes

Add private notes visible only in the speaker view (press `S` during presentation).

### Setup

The scaffold does not include the Notes plugin by default. Add the script before `Reveal.initialize()` and register it in the `plugins` array:

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/notes/notes.js"></script>
```

```javascript
Reveal.initialize({
  // ... other config
  plugins: [ RevealNotes ]
});
```

### Adding Notes

Place notes in an `<aside class="notes">` element inside the slide:

```html
<section>
  <h2>Revenue Growth</h2>
  <p>Revenue increased 25% YoY.</p>
  <aside class="notes">
    Mention the Q3 spike was due to the enterprise deal.
    Transition to the pipeline slide after this.
  </aside>
</section>
```

### Multi-line Notes

```html
<aside class="notes">
  <ul>
    <li>Key talking point 1</li>
    <li>Key talking point 2</li>
    <li>Transition: move to demo slide next</li>
  </ul>
</aside>
```

### Speaker View

Press `S` during the presentation to open the speaker view in a separate window. It shows:
- **Current slide** — What the audience sees
- **Upcoming slide** — Next slide preview
- **Speaker notes** — Your private notes
- **Timer** — Elapsed time
- **Slide number** — Current position

### Notes with Markdown

If using `data-markdown`, notes are separated by `Note:`:

```html
<section data-markdown>
  ## Revenue Growth
  Revenue increased 25% YoY.

  Note: Mention the Q3 spike was due to the enterprise deal.
</section>
```

## References

- [Slide Backgrounds](official-docs/backgrounds.md)
- [Media](official-docs/media.md)
- [Lightbox](official-docs/lightbox.md)
- [Speaker View](official-docs/speaker-view.md)
- [Layout](official-docs/layout.md)
- [Themes](official-docs/themes.md)
