# Code & Text

Guide for presenting code with syntax highlighting, math formulas, and Markdown-authored slides.

## Table of Contents

1. [Code Highlighting](#code-highlighting)
2. [Math Formulas](#math-formulas)
3. [Markdown Slides](#markdown-slides)

---

## Code Highlighting

Reveal.js uses the built-in RevealHighlight plugin (wraps highlight.js) for syntax highlighting.

### Setup

The scaffold does not include RevealHighlight by default. Add the script and register the plugin:

```html
<!-- Before Reveal.initialize() -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/highlight/highlight.js"></script>
```

```javascript
Reveal.initialize({
  // ... other config
  plugins: [ RevealHighlight ]
});
```

Code blocks use `<pre><code>` with a language class.

### Basic Code Block

```html
<pre><code class="language-javascript" data-trim>
function greet(name) {
  console.log(`Hello, ${name}!`);
}
</code></pre>
```

- `data-trim` — Removes leading/trailing whitespace (recommended for all code blocks)
- The `language-*` class triggers syntax highlighting

### Supported Languages

Common languages and their class names:

| Language | Class |
|----------|-------|
| JavaScript | `language-javascript` or `language-js` |
| TypeScript | `language-typescript` or `language-ts` |
| Python | `language-python` or `language-py` |
| Java | `language-java` |
| Go | `language-go` |
| Rust | `language-rust` |
| C/C++ | `language-c` / `language-cpp` |
| HTML | `language-html` |
| CSS | `language-css` |
| SQL | `language-sql` |
| Bash/Shell | `language-bash` or `language-shell` |
| JSON | `language-json` |
| YAML | `language-yaml` |
| Markdown | `language-markdown` or `language-md` |
| XML | `language-xml` |
| PHP | `language-php` |
| Ruby | `language-ruby` |
| Swift | `language-swift` |
| Kotlin | `language-kotlin` |
| Scala | `language-scala` |

highlight.js supports 190+ languages. Use the full language name as the class.

### Line Numbers

Show line numbers on code blocks:

```html
<pre><code class="language-python" data-trim data-line-numbers>
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
</code></pre>
```

Start from a different line number:

```html
<pre><code class="language-python" data-trim data-line-numbers data-ln-start-from="42">
# This is line 42 in the source file
def main():
    print("Hello")
</code></pre>
```

### Highlighting Specific Lines

Use `|` to separate line numbers that should be highlighted:

```html
<!-- Highlight lines 1 and 4-6 -->
<pre><code class="language-javascript" data-trim data-line-numbers="1|4-6">
import React from 'react';          // highlighted
import ReactDOM from 'react-dom';   // normal

function App() {                    // normal
  return (                          // highlighted
    <div>Hello</div>                // highlighted
  );                                // highlighted
}
</code></pre>
```

### Step-Through Highlighting

Multiple highlight groups separated by `|` create sequential steps. Each click advances to the next group:

```html
<pre><code class="language-javascript" data-trim data-line-numbers="1-2|4-5|7-8">
// Step 1: Import statements (highlighted first)
import express from 'express';
import cors from 'cors';

// Step 2: Create app (highlighted second)
const app = express();
app.use(cors());

// Step 3: Define route (highlighted third)
app.get('/', (req, res) => {
  res.json({ message: 'Hello' });
});
</code></pre>
```

Navigation advances: first highlights lines 1-2, then 4-5, then 7-8.

### Avoiding HTML Escaping

If your code contains HTML tags like `<div>`, browsers may interpret them as real elements. Use `<script type="text/template">` to prevent parsing:

```html
<pre><code class="language-html" data-trim>
<script type="text/template">
<div class="container">
  <h1>Hello World</h1>
  <p>This HTML won't be parsed by the browser</p>
</div>
</script>
</code></pre>
```

This wraps the code in a template tag that the browser ignores, while highlight.js still processes the content.

### Code Themes

Change the syntax highlighting theme by swapping the CSS file in the scaffold's `<head>`:

```html
<!-- Default -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">

<!-- Light theme -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-light.min.css">

<!-- Other popular themes -->
<!-- github.min.css, monokai.min.css, dracula.min.css, vs2015.min.css -->
```

Browse all themes: https://cdnjs.com.com/libraries/highlight.js

Choose a theme that contrasts well with your slide background. Dark slides → dark code theme, light slides → light code theme.

### Code Block with Auto-Animate

Code blocks auto-animate between matching slides, highlighting changes:

```html
<section data-auto-animate>
  <pre><code class="language-python" data-trim>
def calculate(x):
    return x * 2
  </code></pre>
</section>
<section data-auto-animate>
  <pre><code class="language-python" data-trim>
def calculate(x, y):
    result = x * 2 + y
    return result
  </code></pre>
</section>
```

Added lines are briefly highlighted during the transition.

---

## Math Formulas

Reveal.js supports math rendering via the built-in RevealMath plugin (wraps KaTeX) or standalone KaTeX.

### Setup (Recommended: RevealMath)

The scaffold does not include RevealMath by default. Add the script and register the plugin:

```html
<!-- Before Reveal.initialize() -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/math/math.js"></script>
```

```javascript
Reveal.initialize({
  // ... other config
  plugins: [ RevealMath ]
});
```

RevealMath loads KaTeX automatically — no separate KaTeX scripts needed. Use `$...$` for inline math and `$$...$$` for display math.

### Setup (Standalone KaTeX)

For full control over rendering options, use KaTeX directly without the plugin:

```html
<!-- In <head> -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">

<!-- Before Reveal.initialize() -->
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js">
</script>
```

Initialize auto-render after Reveal:

```javascript
Reveal.initialize({
  // ... your config
}).then(() => {
  renderMathInElement(document.body, {
    delimiters: [
      {left: '$$', right: '$$', display: true},
      {left: '$', right: '$', display: false},
    ],
  });
});
```

### Inline Math

Wrap formulas in single `$`:

```html
<p>The equation $E = mc^2$ is famous.</p>
<p>The sum $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$ gives triangular numbers.</p>
```

### Display Math

Wrap formulas in double `$$` for centered, block-level equations:

```html
<p>The quadratic formula:</p>
$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$
```

### Common LaTeX Patterns

```html
<!-- Fractions -->
<p>$\frac{a}{b}$</p>

<!-- Subscripts and superscripts -->
<p>$x_1^{2}$</p>

<!-- Square root -->
<p>$\sqrt{a^2 + b^2}$</p>

<!-- Matrices -->
$$
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$

<!-- Integration -->
$$\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$

<!-- Greek letters -->
<p>$\alpha, \beta, \gamma, \delta, \epsilon$</p>

<!-- Summation -->
$$\sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}$$
```

### Math in Styled Containers

Math works inside any HTML container. Just make sure the delimiters are correct:

```html
<div style="background: #F5F5F5; padding: 20px; border-radius: 8px;">
  <p><strong>Euler's Identity:</strong></p>
  $$e^{i\pi} + 1 = 0$$
</div>
```

---

## Markdown Slides

As an alternative to HTML, write slide content in Markdown. Requires the built-in RevealMarkdown plugin.

### Setup

The scaffold does not include RevealMarkdown by default. Add the script and register the plugin:

```html
<!-- Before Reveal.initialize() -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/markdown/markdown.js"></script>
```

```javascript
Reveal.initialize({
  // ... other config
  plugins: [ RevealMarkdown ]
});
```

### Basic Markdown Slide

```html
<section data-markdown>
  ## Slide Title

  - First point
  - Second point
  - **Bold text** and *italic text*

  > A blockquote
</section>
```

### External Markdown File

Load content from a separate `.md` file:

```html
<section data-markdown="content.md"></section>
```

### Separating Slides in Markdown

Use `---` to separate slides within a Markdown file:

```markdown
## Slide 1

Content for the first slide.

---

## Slide 2

Content for the second slide.
```

Load the full file:

```html
<div class="reveal">
  <div class="slides">
    <section data-markdown="slides.md"
             data-separator="---"
             data-separator-vertical=">>>">
    </section>
  </div>
</div>
```

- `data-separator` — Pattern for horizontal slide breaks (default: `---`)
- `data-separator-vertical` — Pattern for vertical slide breaks (default: none)
- `data-separator-notes` — Pattern for speaker notes (default: `Note:`)

### Markdown with Speaker Notes

```html
<section data-markdown>
  ## Important Slide

  Key content here.

  Note: These are speaker notes. They won't appear on the slide.
</section>
```

### Markdown Features

Standard Markdown is supported:

```html
<section data-markdown>
  ## Rich Content

  ### Text formatting
  **Bold**, *italic*, ~~strikethrough~~, `inline code`

  ### Lists
  1. Ordered item
  2. Another item

  ### Links
  [Visit OpenAI](https://openai.com)

  ### Images
  ![Alt text](image.png)

  ### Tables
  | Name | Value |
  |------|-------|
  | A    | 1     |
  | B    | 2     |
</section>
```

### Markdown with HTML Mix

You can mix Markdown and HTML within the same slide:

```html
<section data-markdown>
  ## Market Analysis

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">

  ### Growth
  - Revenue up 25%
  - Users up 40%

  ### Risks
  - Competition increasing
  - Market saturation

  </div>
</section>
```

### Markdown Limitations

- Fragment classes must be added via HTML: `<p class="fragment fade-up">text</p>`
- Complex layouts (grids, flex) work best in HTML mode
- Auto-animate requires matching `data-id` attributes, which means HTML mode
- For content-heavy slides with simple layouts, Markdown is ideal. For visually rich slides, use HTML.

## References

- [Code](official-docs/code.md)
- [Markdown](official-docs/markdown.md)
- [Math](official-docs/math.md)
