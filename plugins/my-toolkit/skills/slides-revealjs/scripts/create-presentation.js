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
 *
 * Examples:
 *   node create-presentation.js ./my-deck --structure 1,1,d,3,1
 *   node create-presentation.js ./slides --title "My Talk" --theme black
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    outputDir: './presentation',
    structure: '1',
    title: 'Presentation',
    theme: 'solarized',
    includeCss: true,
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

  return `<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>${options.title}</title>

    <link rel="stylesheet" href="dist/reveal.css" />
    <link rel="stylesheet" href="dist/theme/${options.theme}.css" />
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

    <script src="dist/reveal.js"></script>
    <script src="plugin/notes/notes.js"></script>
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

// Generate base CSS file
function generateBaseCss() {
  return `/* Base Styles for Reveal.js Presentations */

/* CSS Variables for Theming */
:root {
  --background-color: #fdf6e3;
  --heading-font: "Source Sans Pro", Helvetica, sans-serif;
  --body-font: "Source Sans Pro", Helvetica, sans-serif;
  --text-size: 16pt;
  --h1-size: 48pt;
  --h2-size: 36pt;
  --h3-size: 28pt;
  --primary-color: #b58900;
  --secondary-color: #cb4b16;
  --accent-color: #d33682;
  --text-color: #657b83;
  --muted-color: #93a1a1;
  --box-radius: 8px;
  --box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Text Size Utilities */
.text-sm { font-size: 14pt !important; }
.text-base { font-size: 16pt !important; }
.text-lg { font-size: 18pt !important; }
.text-xl { font-size: 20pt !important; }
.text-2xl { font-size: 24pt !important; }
.text-3xl { font-size: 28pt !important; }
.text-4xl { font-size: 32pt !important; }
.text-5xl { font-size: 36pt !important; }

/* Color Utilities */
.text-primary { color: var(--primary-color) !important; }
.text-secondary { color: var(--secondary-color) !important; }
.text-accent { color: var(--accent-color) !important; }
.text-muted { color: var(--muted-color) !important; }

/* Background Utilities */
.bg-primary { background-color: var(--primary-color) !important; }
.bg-secondary { background-color: var(--secondary-color) !important; }
.bg-accent { background-color: var(--accent-color) !important; }

/* Layout Utilities */
.reveal .cols {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.reveal .col { flex: 1; }
.reveal .col-70 { flex: 0 0 70%; }
.reveal .col-60 { flex: 0 0 60%; }
.reveal .col-50 { flex: 0 0 50%; }
.reveal .col-40 { flex: 0 0 40%; }
.reveal .col-30 { flex: 0 0 30%; }

/* Panel/Box Component */
.reveal .panel {
  background: var(--background-color);
  border-radius: var(--box-radius);
  box-shadow: var(--box-shadow);
  padding: 1.5rem;
}

/* Section Divider Styling */
.reveal .divider-slide {
  text-align: center;
}

.reveal .divider-slide h2 {
  font-size: var(--h1-size);
  color: var(--primary-color);
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
