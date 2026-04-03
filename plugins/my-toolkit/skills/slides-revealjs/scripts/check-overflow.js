#!/usr/bin/env node

/**
 * Reveal.js Slide Overflow Checker (Playwright)
 *
 * Checks each slide for content overflow using Playwright browser automation.
 *
 * Usage:
 *   node check-overflow.js <html-file-or-url> [options]
 *
 * Options:
 *   --browser <browser>     Browser to use: chromium, firefox, webkit (default: chromium)
 *   --threshold <pixels>    Minimum overflow to report (default: 5)
 *   --json                  Output results as JSON
 *   --verbose               Show detailed output
 *
 * Examples:
 *   node check-overflow.js ./presentation/index.html
 *   node check-overflow.js http://localhost:3000 --browser firefox
 *   node check-overflow.js ./slides/index.html --json > results.json
 */

const { chromium, firefox, webkit } = require('playwright');

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    target: null,
    browser: 'chromium',
    threshold: 5,
    json: false,
    verbose: false,
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];

    if (arg === '--browser' && args[i + 1]) {
      options.browser = args[i + 1];
      i += 2;
    } else if (arg === '--threshold' && args[i + 1]) {
      options.threshold = parseInt(args[i + 1], 10);
      i += 2;
    } else if (arg === '--json') {
      options.json = true;
      i += 1;
    } else if (arg === '--verbose') {
      options.verbose = true;
      i += 1;
    } else if (!arg.startsWith('--')) {
      options.target = arg;
      i += 1;
    } else {
      i += 1;
    }
  }

  return options;
}

// Get browser instance
function getBrowser(name) {
  switch (name) {
    case 'firefox':
      return firefox;
    case 'webkit':
      return webkit;
    default:
      return chromium;
  }
}

// Main overflow check function
async function checkOverflow(options) {
  const browserType = getBrowser(options.browser);
  const browser = await browserType.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
  });
  const page = await context.newPage();

  const results = {
    url: options.target,
    browser: options.browser,
    timestamp: new Date().toISOString(),
    slides: [],
    summary: {
      total: 0,
      withOverflow: 0,
      maxVerticalOverflow: 0,
      maxHorizontalOverflow: 0,
    },
  };

  try {
    // Resolve target path/URL
    let targetUrl = options.target;
    if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
      const path = require('path');
      targetUrl = 'file://' + path.resolve(targetUrl);
    }

    if (options.verbose && !options.json) {
      console.log(`Loading: ${targetUrl}`);
    }

    await page.goto(targetUrl, { waitUntil: 'networkidle' });

    // Wait for Reveal.js to initialize
    await page.waitForFunction(() => {
      return typeof Reveal !== 'undefined' && Reveal.isReady();
    }, { timeout: 10000 });

    // Get total slide count
    const totalSlides = await page.evaluate(() => Reveal.getTotalSlides());
    results.summary.total = totalSlides;

    if (options.verbose && !options.json) {
      console.log(`Found ${totalSlides} slides`);
    }

    // Check each slide
    for (let i = 0; i < totalSlides; i++) {
      // Navigate to slide
      await page.evaluate((index) => {
        Reveal.slide(index);
      }, i);

      // Wait for slide transition
      await page.waitForTimeout(300);

      // Check for overflow
      const slideInfo = await page.evaluate(() => {
        const currentSlide = Reveal.getCurrentSlide();
        if (!currentSlide) return null;

        // Get slide dimensions
        const slideRect = currentSlide.getBoundingClientRect();
        const slideContent = currentSlide.querySelector('.slide-content') || currentSlide;

        // Check vertical overflow
        const verticalOverflow = Math.max(
          0,
          slideContent.scrollHeight - slideRect.height
        );

        // Check horizontal overflow
        const horizontalOverflow = Math.max(
          0,
          slideContent.scrollWidth - slideRect.width
        );

        // Get slide identifier
        const slideId = currentSlide.id || `slide-${Reveal.getIndices().h}-${Reveal.getIndices().v || 0}`;
        const indices = Reveal.getIndices();

        return {
          id: slideId,
          h: indices.h,
          v: indices.v || 0,
          verticalOverflow: Math.round(verticalOverflow),
          horizontalOverflow: Math.round(horizontalOverflow),
          slideHeight: Math.round(slideRect.height),
          contentHeight: Math.round(slideContent.scrollHeight),
        };
      });

      if (slideInfo) {
        const hasOverflow =
          slideInfo.verticalOverflow > options.threshold ||
          slideInfo.horizontalOverflow > options.threshold;

        if (hasOverflow) {
          results.summary.withOverflow++;
          results.summary.maxVerticalOverflow = Math.max(
            results.summary.maxVerticalOverflow,
            slideInfo.verticalOverflow
          );
          results.summary.maxHorizontalOverflow = Math.max(
            results.summary.maxHorizontalOverflow,
            slideInfo.horizontalOverflow
          );
        }

        results.slides.push(slideInfo);

        if (options.verbose && !options.json && hasOverflow) {
          console.log(
            `  Slide ${slideInfo.h}.${slideInfo.v}: ` +
              `V=${slideInfo.verticalOverflow}px, ` +
              `H=${slideInfo.horizontalOverflow}px`
          );
        }
      }
    }
  } catch (error) {
    results.error = error.message;
    if (!options.json) {
      console.error(`Error: ${error.message}`);
    }
  } finally {
    await browser.close();
  }

  return results;
}

// Format human-readable output
function formatOutput(results, threshold) {
  const lines = [];

  lines.push('='.repeat(60));
  lines.push('Reveal.js Overflow Check Results');
  lines.push('='.repeat(60));
  lines.push(`Target: ${results.url}`);
  lines.push(`Browser: ${results.browser}`);
  lines.push(`Timestamp: ${results.timestamp}`);
  lines.push('');

  lines.push('Summary:');
  lines.push(`  Total slides: ${results.summary.total}`);
  lines.push(`  Slides with overflow: ${results.summary.withOverflow}`);
  lines.push(`  Max vertical overflow: ${results.summary.maxVerticalOverflow}px`);
  lines.push(`  Max horizontal overflow: ${results.summary.maxHorizontalOverflow}px`);
  lines.push('');

  if (results.summary.withOverflow > 0) {
    lines.push('Slides with overflow:');
    results.slides.forEach((slide) => {
      if (
        slide.verticalOverflow > threshold ||
        slide.horizontalOverflow > threshold
      ) {
        lines.push(
          `  [${slide.h}.${slide.v}] ${slide.id}: ` +
            `V=${slide.verticalOverflow}px, H=${slide.horizontalOverflow}px`
        );
      }
    });
  } else {
    lines.push('No overflow detected in any slide.');
  }

  lines.push('='.repeat(60));

  return lines.join('\n');
}

// Main execution
async function main() {
  const options = parseArgs();

  if (!options.target) {
    console.error('Usage: node check-overflow.js <html-file-or-url> [options]');
    console.error('Options:');
    console.error('  --browser <name>     Browser: chromium, firefox, webkit');
    console.error('  --threshold <px>     Minimum overflow to report (default: 5)');
    console.error('  --json               Output as JSON');
    console.error('  --verbose            Show detailed progress');
    process.exit(1);
  }

  const results = await checkOverflow(options);

  if (options.json) {
    console.log(JSON.stringify(results, null, 2));
  } else {
    console.log(formatOutput(results, options.threshold));
  }

  // Exit with error code if overflow detected
  process.exit(results.summary.withOverflow > 0 ? 1 : 0);
}

main().catch((error) => {
  console.error('Fatal error:', error.message);
  process.exit(2);
});
