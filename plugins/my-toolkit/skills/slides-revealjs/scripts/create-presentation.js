#!/usr/bin/env node

/**
 * Reveal.js Presentation Scaffold Generator
 *
 * Generates a basic reveal.js HTML structure with optional slide layout.
 *
 * Usage:
 *   node create-presentation.js [output-dir] [options]
 *
 * Options:
 *   --structure <pattern>   Slide structure pattern (e.g., "1,1,d,3,1,d,1")
 *                           1 = single slide, N = vertical stack of N slides,
 *                           d = divider/title slide
 *   --title <title>         Presentation title (default: "Presentation")
 *   --theme <theme>         Reveal.js theme (default: "solarized")
 *   --no-css                Skip copying base-styles.css
 *   --local                 Use local reveal.js files instead of CDN
 *                           (requires reveal.js to be installed in parent directory)
 *
 * Examples:
 *   node create-presentation.js ./my-deck --structure 1,1,d,3,1
 *   node create-presentation.js ./slides --title "My Talk" --theme black
 */

const fs = require('fs');
const path = require('path');

// Reveal.js CDN version (5.x stable; 6.x available but switches build tooling to Vite)
const REVEAL_CDN_VERSION = '5.2.1';

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    outputDir: './presentation',
    structure: '1',
    title: 'Presentation',
    theme: 'solarized',
    includeCss: true,
    useCdn: true,  // Default to CDN for better portability
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];

    if (arg === '--structure' && args[i + 1]) {
      options.structure = args[i + 1];
      i += 2;
    } else if (arg === '--title' && args[i + 1]) {
      options.title = args[i + 1];
      i += 2;
    } else if (arg === '--theme' && args[i + 1]) {
      options.theme = args[i + 1];
      i += 2;
    } else if (arg === '--no-css') {
      options.includeCss = false;
      i += 1;
    } else if (arg === '--local') {
      options.useCdn = false;
      i += 1;
    } else if (!arg.startsWith('--')) {
      options.outputDir = arg;
      i += 1;
    } else {
      i += 1;
    }
  }

  return options;
}

// Parse structure pattern
function parseStructure(pattern) {
  return pattern.split(',').map((item) => {
    const trimmed = item.trim().toLowerCase();
    if (trimmed === 'd') return { type: 'divider' };
    const count = parseInt(trimmed, 10);
    if (isNaN(count) || count < 1) return { type: 'single', count: 1 };
    if (count === 1) return { type: 'single', count: 1 };
    return { type: 'vertical', count };
  });
}

// Generate slide HTML
function generateSlideContent(structure, slideIndex) {
  const slides = [];
  let currentSlide = slideIndex || 1;

  structure.forEach((item, idx) => {
    if (item.type === 'divider') {
      slides.push(`  <!-- Section Divider -->
  <section id="section-${idx + 1}">
    <h2 class="r-fit-text">Section ${idx + 1}</h2>
  </section>`);
      currentSlide++;
    } else if (item.type === 'vertical') {
      const verticalSlides = [];
      for (let i = 0; i < item.count; i++) {
        verticalSlides.push(`    <section id="slide-${currentSlide}">
      <h2>Slide ${currentSlide}</h2>
      <p>Content for slide ${currentSlide}</p>
    </section>`);
        currentSlide++;
      }
      slides.push(`  <!-- Vertical Stack -->
  <section>
${verticalSlides.join('\n')}
  </section>`);
    } else {
      slides.push(`  <section id="slide-${currentSlide}">
    <h2>Slide ${currentSlide}</h2>
    <p>Content for slide ${currentSlide}</p>
  </section>`);
      currentSlide++;
    }
  });

  return { html: slides.join('\n\n'), totalSlides: currentSlide - 1 };
}

// Generate full HTML document
function generateHtml(options) {
  const structure = parseStructure(options.structure);
  const { html: slidesHtml } = generateSlideContent(structure);

  const customCssLink = options.includeCss
    ? '    <link rel="stylesheet" href="./assets/custom.css" />\n'
    : '';

  // Use CDN by default for easier setup
  const basePath = options.useCdn
    ? `https://cdn.jsdelivr.net/npm/reveal.js@${REVEAL_CDN_VERSION}`
    : '.';

  const revealCss = options.useCdn
    ? `<link rel="stylesheet" href="${basePath}/dist/reveal.css" />`
    : `<link rel="stylesheet" href="dist/reveal.css" />`;

  const themeCss = options.useCdn
    ? `<link rel="stylesheet" href="${basePath}/dist/theme/${options.theme}.css" />`
    : `<link rel="stylesheet" href="dist/theme/${options.theme}.css" />`;

  const revealJs = options.useCdn
    ? `<script src="${basePath}/dist/reveal.js"></script>`
    : `<script src="dist/reveal.js"></script>`;

  const notesJs = options.useCdn
    ? `<script src="${basePath}/plugin/notes/notes.js"></script>`
    : `<script src="plugin/notes/notes.js"></script>`;

  return `<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>${options.title}</title>

    ${revealCss}
    ${themeCss}
${customCssLink}
    <style>
      /* Inline customizations */
      .reveal h1, .reveal h2, .reveal h3 {
        text-transform: none;
      }
    </style>
  </head>

  <body>
    <div class="reveal">
      <div class="slides">
        <!-- Title Slide -->
        <section id="title-slide">
          <h1>${options.title}</h1>
        </section>

${slidesHtml}
      </div>
    </div>

    ${revealJs}
    ${notesJs}
    <script>
      Reveal.initialize({
        hash: true,
        slideNumber: 'c/t',
        plugins: [RevealNotes],
      });
    </script>
  </body>
</html>
`;
}

// Generate base CSS file (aligned with references/base-styles.css)
function generateBaseCss() {
  return `/* Base Styles for Reveal.js Presentations */

/* CSS Variables for Theming */
:root {
  --background-color: #fdf6e3;
  --surface-color: rgba(255, 255, 255, 0.72);
  --heading-font: "Source Sans Pro", Helvetica, sans-serif;
  --body-font: "Source Sans Pro", Helvetica, sans-serif;

  /* Typography Scale (pt units for presentation readability) */
  --text-size: 16pt;
  --h1-size: 48pt;
  --h2-size: 36pt;
  --h3-size: 28pt;

  /* Semantic Colors */
  --primary-color: #b58900;
  --secondary-color: #cb4b16;
  --accent-color: #d33682;
  --text-color: #657b83;
  --muted-color: #93a1a1;

  /* Spacing & Layout */
  --box-radius: 8px;
  --box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  --gap: 1.5rem;
}

/* Text Size Utilities */
.text-sm   { font-size: 14pt !important; }
.text-base { font-size: 16pt !important; }
.text-lg   { font-size: 18pt !important; }
.text-xl   { font-size: 20pt !important; }
.text-2xl  { font-size: 24pt !important; }
.text-3xl  { font-size: 28pt !important; }
.text-4xl  { font-size: 32pt !important; }
.text-5xl  { font-size: 36pt !important; }

/* Color Utilities */
.text-primary   { color: var(--primary-color) !important; }
.text-secondary { color: var(--secondary-color) !important; }
.text-accent    { color: var(--accent-color) !important; }
.text-muted     { color: var(--muted-color) !important; }

.bg-primary   { background-color: var(--primary-color) !important; }
.bg-secondary { background-color: var(--secondary-color) !important; }
.bg-accent    { background-color: var(--accent-color) !important; }
.bg-surface   { background-color: var(--surface-color) !important; }

/* Layout Utilities */
.reveal .cols {
  display: flex;
  gap: var(--gap);
  align-items: flex-start;
  width: 100%;
}

.reveal .col    { flex: 1; }
.reveal .col-70 { flex: 0 0 70%; }
.reveal .col-60 { flex: 0 0 60%; }
.reveal .col-50 { flex: 0 0 50%; }
.reveal .col-40 { flex: 0 0 40%; }
.reveal .col-30 { flex: 0 0 30%; }

.reveal .grid   { display: grid; gap: var(--gap); }
.reveal .grid-2 { grid-template-columns: repeat(2, 1fr); }
.reveal .grid-3 { grid-template-columns: repeat(3, 1fr); }

.reveal .center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}

/* Panel Component */
.reveal .panel {
  background: var(--surface-color);
  border-radius: var(--box-radius);
  box-shadow: var(--box-shadow);
  padding: calc(var(--gap) * 1.2);
}

/* Section Divider Styling */
.reveal .divider-slide {
  text-align: center;
}

.reveal .divider-slide h2 {
  font-size: var(--h1-size);
  color: var(--primary-color);
}

/* Callout Boxes */
.reveal .callout {
  padding: 1rem 1.5rem;
  border-radius: var(--box-radius);
  margin: 1rem 0;
}

.reveal .callout-note {
  background: rgba(181, 137, 0, 0.1);
  border-left: 4px solid var(--primary-color);
}

/* Tight Lists */
.reveal ul.tight li,
.reveal ol.tight li {
  margin: 0.25rem 0;
}

/* Overflow Prevention */
.reveal pre {
  max-height: 500px;
  overflow: auto;
}

.reveal .scrollable {
  max-height: 420px;
  overflow-y: auto;
}

.reveal .compact h2,
.reveal .compact h3 {
  margin-bottom: 0.3em;
}

.reveal .compact li {
  margin: 0.15em 0;
}
`;
}

// Main execution
function main() {
  const options = parseArgs();

  // Create output directory
  const outputDir = path.resolve(options.outputDir);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Generate and write HTML file
  const html = generateHtml(options);
  const htmlPath = path.join(outputDir, 'index.html');
  fs.writeFileSync(htmlPath, html, 'utf8');
  console.log(`Created: ${htmlPath}`);

  // Generate and write CSS file if requested
  if (options.includeCss) {
    const assetsDir = path.join(outputDir, 'assets');
    if (!fs.existsSync(assetsDir)) {
      fs.mkdirSync(assetsDir, { recursive: true });
    }
    const css = generateBaseCss();
    const cssPath = path.join(assetsDir, 'custom.css');
    fs.writeFileSync(cssPath, css, 'utf8');
    console.log(`Created: ${cssPath}`);
  }

  console.log(`\nPresentation scaffold created at: ${outputDir}`);
  console.log(`Total slides: ${options.structure.split(',').reduce((acc, item) => {
    const val = item.trim().toLowerCase();
    if (val === 'd') return acc + 1;
    return acc + parseInt(val, 10);
  }, 1)} (including title)`);
  console.log(`\nTo preview, serve the directory with a local web server:`);
  console.log(`  npx serve ${outputDir}`);
}

main();
