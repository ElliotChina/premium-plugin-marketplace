#!/usr/bin/env node

/**
 * Reveal.js Slide Overflow Checker (Browser Injection)
 *
 * Injects a detection script into a reveal.js HTML file. When you open the
 * file in a browser, it automatically checks every slide for content overflow
 * and prints a report to the browser console.
 *
 * No external dependencies required — pure Node.js + browser APIs.
 *
 * Usage:
 *   node check-overflow.js <html-file>           # Inject detection code
 *   node check-overflow.js <html-file> --restore  # Remove injected code
 *   node check-overflow.js <html-file> --check    # Inject & open in browser
 *
 * Options:
 *   --restore     Remove previously injected detection code
 *   --check       Inject detection code and open in default browser
 *   --threshold   Minimum overflow pixels to report (default: 5)
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    target: null,
    restore: false,
    check: false,
    threshold: 5,
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    if (arg === '--restore') {
      options.restore = true;
      i += 1;
    } else if (arg === '--check') {
      options.check = true;
      i += 1;
    } else if (arg === '--threshold' && args[i + 1]) {
      const val = parseInt(args[i + 1], 10);
      options.threshold = (isNaN(val) || val < 0) ? 5 : val;
      i += 2;
    } else if (!arg.startsWith('--')) {
      options.target = arg;
      i += 1;
    } else {
      i += 1;
    }
  }

  return options;
}

// Marker comments used to identify injected code
const START_MARKER = '<!-- OVERFLOW-CHECK-START -->';
const END_MARKER = '<!-- OVERFLOW-CHECK-END -->';

// Generate the browser-side detection script
function generateDetectionScript(threshold) {
  return `
${START_MARKER}
<script data-overflow-checker>
(function() {
  function checkOverflow() {
    var sections = document.querySelectorAll('.reveal .slides section');
    var results = [];
    var hasOverflow = false;

    sections.forEach(function(section, index) {
      // Skip nested sections (they are measured as part of their parent)
      if (section.parentElement.closest('section')) return;

      var rect = section.getBoundingClientRect();
      var overflowV = Math.max(0, section.scrollHeight - rect.height);
      var overflowH = Math.max(0, section.scrollWidth - rect.width);

      if (overflowV > ${threshold} || overflowH > ${threshold}) {
        hasOverflow = true;
        var id = section.id || ('slide-' + index);
        results.push({
          id: id,
          index: index,
          vertical: Math.round(overflowV),
          horizontal: Math.round(overflowH),
        });
      }
    });

    // Also check visible slides specifically
    var currentSlide = Reveal ? Reveal.getCurrentSlide() : null;
    var totalSlides = Reveal ? Reveal.getTotalSlides() : sections.length;

    console.log('');
    console.log('%c══════ Slide Overflow Check ══════', 'font-weight:bold; font-size:14px; color:#268bd2;');
    console.log('Total slides: ' + totalSlides);
    console.log('Threshold: ${threshold}px');

    if (hasOverflow) {
      console.log('%c' + results.length + ' slide(s) with overflow:', 'color:#dc322f; font-weight:bold;');
      results.forEach(function(r) {
        console.log(
          '  [%c' + r.id + '%c] V=%c' + r.vertical + 'px%c  H=%c' + r.horizontal + 'px',
          'color:#b58900', '',
          r.vertical > 30 ? 'color:#dc322f;font-weight:bold' : 'color:#cb4b16', '',
          r.horizontal > 30 ? 'color:#dc322f;font-weight:bold' : 'color:#cb4b16'
        );
      });
    } else {
      console.log('%c\u2713 No overflow detected.', 'color:#859900; font-weight:bold;');
    }
    console.log('%c═════════════════════════════════', 'font-weight:bold; color:#268bd2;');
    console.log('');

    return results;
  }

  // Run after Reveal.js is ready
  function runCheck() {
    if (typeof Reveal !== 'undefined') {
      if (Reveal.isReady && Reveal.isReady()) {
        checkOverflow();
      } else {
        Reveal.on('ready', checkOverflow);
      }
    } else {
      // Fallback: wait a bit for Reveal to load
      setTimeout(checkOverflow, 1000);
    }
  }

  // Also re-check on slide change for verification
  if (typeof Reveal !== 'undefined') {
    Reveal.on('slidechanged', function(e) {
      var section = e.currentSlide;
      var rect = section.getBoundingClientRect();
      var overflowV = Math.max(0, section.scrollHeight - rect.height);
      var overflowH = Math.max(0, section.scrollWidth - rect.width);
      if (overflowV > ${threshold} || overflowH > ${threshold}) {
        console.warn('[Overflow] Slide ' + (e.indexh) + ': V=' + Math.round(overflowV) + 'px H=' + Math.round(overflowH) + 'px');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runCheck);
  } else {
    runCheck();
  }
})();
</script>
${END_MARKER}`;
}

// Remove injected code from HTML
function removeInjectedCode(html) {
  const startIdx = html.indexOf(START_MARKER);
  const endIdx = html.indexOf(END_MARKER);
  if (startIdx === -1 || endIdx === -1) {
    return null; // Nothing to remove
  }
  return html.slice(0, startIdx) + html.slice(endIdx + END_MARKER.length);
}

// Main
function main() {
  const options = parseArgs();

  if (!options.target) {
    console.error('Usage: node check-overflow.js <html-file> [--restore] [--check] [--threshold <px>]');
    process.exit(1);
  }

  const filePath = path.resolve(options.target);
  if (!fs.existsSync(filePath)) {
    console.error('Error: File not found: ' + filePath);
    process.exit(2);
  }

  let html = fs.readFileSync(filePath, 'utf8');

  if (options.restore) {
    const cleaned = removeInjectedCode(html);
    if (cleaned) {
      fs.writeFileSync(filePath, cleaned, 'utf8');
      console.log('Removed overflow detection code from: ' + filePath);
    } else {
      console.log('No injected detection code found in: ' + filePath);
    }
    return;
  }

  // Remove any previously injected code first
  const cleaned = removeInjectedCode(html);
  if (cleaned) {
    html = cleaned;
  }

  // Inject detection script before </body>
  const detectionCode = generateDetectionScript(options.threshold);
  const bodyCloseIdx = html.lastIndexOf('</body>');
  if (bodyCloseIdx === -1) {
    console.error('Error: No </body> tag found in: ' + filePath);
    process.exit(2);
  }

  html = html.slice(0, bodyCloseIdx) + '\n' + detectionCode + '\n' + html.slice(bodyCloseIdx);

  // Create backup before modifying user's file
  fs.writeFileSync(filePath + '.bak', fs.readFileSync(filePath, 'utf8'), 'utf8');
  fs.writeFileSync(filePath, html, 'utf8');
  console.log('Injected overflow detection code into: ' + filePath);
  console.log('Open the file in a browser and check the console for results.');

  if (options.check) {
    const cmd = process.platform === 'darwin' ? 'open' : process.platform === 'win32' ? 'start' : 'xdg-open';
    exec(cmd + ' "' + filePath + '"', function(err) {
      if (err) console.error('Could not open browser: ' + err.message);
    });
  }
}

main();
