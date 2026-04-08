# Slide Layouts

Common layout patterns for reveal.js slides. All layouts use inline CSS — each slide has different needs, so inline styles give full control without utility class bloat.

## Table of Contents

1. [Card Grids](#card-grids)
2. [Stat / Metric Boxes](#stat--metric-boxes)
3. [Image + Text](#image--text)
4. [Icon Feature Rows](#icon-feature-rows)
5. [Timeline & Process Steps](#timeline--process-steps)
6. [Full-Width Image](#full-width-image)
7. [Overlay Text on Image](#overlay-text-on-image)
8. [Comparison Layout](#comparison-layout)
9. [Quote Slides](#quote-slides)
10. [Logo / Partner Grid](#logo--partner-grid)
11. [Team / Profile Cards](#team--profile-cards)

---

## Card Grids

Feature cards, service listings, or any repeated item with title + description.

**Vertical filling**: The `.content` container stretches its direct children to fill available vertical space (via CSS `flex: 1`). Grid containers inside `.content` will automatically fill the full height. Cards inside the grid stretch vertically by default (`align-items: stretch` is the grid default). This prevents cards from bunching at the top with empty space below.

If you want cards to only take their natural height (not stretch), add `align-content: start` to the grid container.

### Anti-Pattern: `align-items: start` on outer grid

(Rule: never use `align-items: start` on grid containers inside `.content`.)

```html
<!-- ❌ Bad: align-items: start on the outer grid prevents vertical filling -->
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; align-items: start;">
  <div style="background: var(--secondary-color); padding: 25px;">Card 1</div>
  <div style="background: var(--secondary-color); padding: 25px;">Card 2</div>
</div>

<!-- ✅ Good: outer grid uses default stretch; inner alignment handled per-card -->
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px;">
  <div style="background: var(--secondary-color); padding: 25px;">Card 1</div>
  <div style="background: var(--secondary-color); padding: 25px;">Card 2</div>
</div>
```

### Anti-Pattern: Wrapper divs breaking card alignment

(Rule: put styled cards directly as grid children, no wrapper `<div>`.)

```html
<!-- ❌ Bad: wrapper div breaks card alignment -->
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
  <div>
    <div style="background: var(--secondary-color); padding: 22px; border-radius: var(--box-radius);">
      <h3>Short card</h3><p>Only 2 items</p>
    </div>
  </div>
  <div>
    <div style="background: var(--secondary-color); padding: 22px; border-radius: var(--box-radius);">
      <h3>Tall card</h3><p>Has more items here</p><p>And another line</p>
    </div>
  </div>
</div>

<!-- ✅ Good: cards are direct grid children, equal height automatically -->
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
  <div style="background: var(--secondary-color); padding: 22px; border-radius: var(--box-radius);">
    <h3>Short card</h3><p>Only 2 items</p>
  </div>
  <div style="background: var(--secondary-color); padding: 22px; border-radius: var(--box-radius);">
    <h3>Tall card</h3><p>Has more items here</p><p>And another line</p>
  </div>
</div>
```

### Content Distribution Inside Stretched Cards

(Rule: when cards stretch, use flex column to distribute content inside.)

**Pattern A — `justify-content: space-between`**: Best for 2-3 visual sections (title + content + footer).

```html
<div style="background: var(--secondary-color); padding: 22px; border-radius: var(--box-radius);
            display: flex; flex-direction: column; justify-content: space-between;">
  <div>
    <h3>Title</h3>
    <p>Main content here.</p>
  </div>
  <p class="text-muted" style="font-size: 12pt;">Footer note pushed to bottom</p>
</div>
```

**Pattern B — `margin-top: auto` on last element**: Best for a list + trailing summary/note.

```html
<div style="background: var(--secondary-color); padding: 22px; border-radius: var(--box-radius);
            display: flex; flex-direction: column;">
  <h3>Title</h3>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
  <p class="text-muted" style="font-size: 12pt; margin-top: auto;">Summary pushed to bottom</p>
</div>
```

**When to use which**: If a card has a clear "header + body + footer" structure, use Pattern A. If it has a list of items with one trailing summary/note, use Pattern B. Not every card needs this — only apply when the stretched card has visibly uneven content distribution compared to its neighbor.

### Anti-Pattern: Flex column of items without vertical distribution

(Rule: add `justify-content: space-between` when a grid column is a flex container with multiple items alongside a taller sibling column.)

This occurs in two-column grids where one column is a tall card (e.g., a table) and the other is a flex column of smaller items. The flex container stretches to match, but its children cluster at the top.

```html
<!-- ❌ Bad: items cluster at the top, whitespace at the bottom -->
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px;">
  <div style="background: var(--secondary-color); padding: 22px; border-radius: var(--box-radius);">
    <h3>Table Card (tall)</h3>
    <table>
      <tr><th>Col A</th><th>Col B</th></tr>
      <tr><td>Row 1</td><td>Data</td></tr>
      <tr><td>Row 2</td><td>Data</td></tr>
      <tr><td>Row 3</td><td>Data</td></tr>
    </table>
  </div>
  <div style="display: flex; flex-direction: column; gap: 15px;">
    <div class="model-card">Item 1</div>
    <div class="model-card">Item 2</div>
    <div class="model-card">Item 3</div>
  </div>
</div>

<!-- ✅ Good: items distribute evenly to match sibling height -->
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px;">
  <div style="background: var(--secondary-color); padding: 22px; border-radius: var(--box-radius);">
    <h3>Table Card (tall)</h3>
    <table>
      <tr><th>Col A</th><th>Col B</th></tr>
      <tr><td>Row 1</td><td>Data</td></tr>
      <tr><td>Row 2</td><td>Data</td></tr>
      <tr><td>Row 3</td><td>Data</td></tr>
    </table>
  </div>
  <div style="display: flex; flex-direction: column; gap: 15px; justify-content: space-between;">
    <div class="model-card">Item 1</div>
    <div class="model-card">Item 2</div>
    <div class="model-card">Item 3</div>
  </div>
</div>
```

### Basic Feature Cards

```html
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px;">
  <div style="background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius);">
    <i class="fa-solid fa-bolt" style="font-size: 24pt; color: var(--primary-color);"></i>
    <h3>Feature One</h3>
    <p>Short description of this feature and its benefit.</p>
  </div>
  <div style="background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius);">
    <i class="fa-solid fa-shield" style="font-size: 24pt; color: var(--primary-color);"></i>
    <h3>Feature Two</h3>
    <p>Short description of this feature and its benefit.</p>
  </div>
  <div style="background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius);">
    <i class="fa-solid fa-chart-line" style="font-size: 24pt; color: var(--primary-color);"></i>
    <h3>Feature Three</h3>
    <p>Short description of this feature and its benefit.</p>
  </div>
</div>
```

### 2x2 Card Grid

```html
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 25px;">
  <div style="background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius);">
    <h3>Card Title</h3>
    <p>Card content here.</p>
  </div>
  <div style="background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius);">
    <h3>Card Title</h3>
    <p>Card content here.</p>
  </div>
  <div style="background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius);">
    <h3>Card Title</h3>
    <p>Card content here.</p>
  </div>
  <div style="background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius);">
    <h3>Card Title</h3>
    <p>Card content here.</p>
  </div>
</div>
```

### Cards with Top Accent Border

```html
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px;">
  <div style="background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius); border-top: 4px solid var(--primary-color);">
    <h3>Highlighted Card</h3>
    <p>Content with a colored top border for emphasis.</p>
  </div>
  <!-- repeat for other cards -->
</div>
```

---

## Stat / Metric Boxes

Display KPIs, metrics, or key numbers. Center-aligned with large number + small label.

### Basic Stats Row

```html
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px;">
  <div style="text-align: center;">
    <p class="text-4xl font-bold" style="color: var(--primary-color);">95%</p>
    <p class="text-muted">Customer Satisfaction</p>
  </div>
  <div style="text-align: center;">
    <p class="text-4xl font-bold" style="color: var(--primary-color);">2.4M</p>
    <p class="text-muted">Active Users</p>
  </div>
  <div style="text-align: center;">
    <p class="text-4xl font-bold" style="color: var(--primary-color);">$18M</p>
    <p class="text-muted">Annual Revenue</p>
  </div>
</div>
```

### Stats with Background Boxes

```html
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">
  <div style="text-align: center; background: var(--secondary-color); padding: 25px 15px; border-radius: var(--box-radius);">
    <p class="text-4xl font-bold" style="color: var(--primary-color);">42</p>
    <p class="text-muted" style="font-size: 12pt;">Projects Delivered</p>
  </div>
  <div style="text-align: center; background: var(--secondary-color); padding: 25px 15px; border-radius: var(--box-radius);">
    <p class="text-4xl font-bold" style="color: var(--primary-color);">99.9%</p>
    <p class="text-muted" style="font-size: 12pt;">Uptime SLA</p>
  </div>
  <div style="text-align: center; background: var(--secondary-color); padding: 25px 15px; border-radius: var(--box-radius);">
    <p class="text-4xl font-bold" style="color: var(--primary-color);">12x</p>
    <p class="text-muted" style="font-size: 12pt;">ROI Improvement</p>
  </div>
  <div style="text-align: center; background: var(--secondary-color); padding: 25px 15px; border-radius: var(--box-radius);">
    <p class="text-4xl font-bold" style="color: var(--primary-color);">6</p>
    <p class="text-muted" style="font-size: 12pt;">Global Offices</p>
  </div>
</div>
```

### Single Big Stat (Hero Number)

```html
<section style="display: flex; align-items: center; justify-content: center; height: 100%;">
  <div style="text-align: center;">
    <p style="font-size: 72pt; font-weight: 700; color: var(--primary-color); line-height: 1;">$50M</p>
    <p class="text-xl text-muted">Revenue in 2024</p>
  </div>
</section>
```

---

## Image + Text

Side-by-side layouts for product showcases, case studies, or visual explanations.

### Image Left, Text Right

```html
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: center;">
  <div>
    <img src="product.jpg" style="width: 100%; border-radius: var(--box-radius);">
  </div>
  <div>
    <h3>Product Title</h3>
    <p>Key description of the product or feature.</p>
    <ul>
      <li>Benefit one</li>
      <li>Benefit two</li>
      <li>Benefit three</li>
    </ul>
  </div>
</div>
```

### Text Left, Image Right

```html
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: center;">
  <div>
    <h3>Section Title</h3>
    <p>Detailed explanation of the concept shown in the image.</p>
  </div>
  <div>
    <img src="diagram.png" style="width: 100%; border-radius: var(--box-radius);">
  </div>
</div>
```

### Unequal Split (2/3 image + 1/3 text)

```html
<div style="display: grid; grid-template-columns: 2fr 1fr; gap: 30px; align-items: center;">
  <div>
    <img src="screenshot.png" style="width: 100%; border-radius: var(--box-radius);">
  </div>
  <div>
    <p class="text-lg font-bold">Key Takeaway</p>
    <p>Supporting description.</p>
  </div>
</div>
```

---

## Icon Feature Rows

Highlight 3-5 key features or benefits with icons. Horizontal layout.

### Basic Icon Row

```html
<div style="display: flex; justify-content: space-around; gap: 30px;">
  <div style="text-align: center; flex: 1;">
    <i class="fa-solid fa-rocket" style="font-size: 32pt; color: var(--primary-color);"></i>
    <p class="font-bold" style="margin-top: 10px;">Fast</p>
    <p class="text-muted" style="font-size: 12pt;">Lightning performance</p>
  </div>
  <div style="text-align: center; flex: 1;">
    <i class="fa-solid fa-lock" style="font-size: 32pt; color: var(--primary-color);"></i>
    <p class="font-bold" style="margin-top: 10px;">Secure</p>
    <p class="text-muted" style="font-size: 12pt;">Enterprise-grade security</p>
  </div>
  <div style="text-align: center; flex: 1;">
    <i class="fa-solid fa-expand" style="font-size: 32pt; color: var(--primary-color);"></i>
    <p class="font-bold" style="margin-top: 10px;">Scalable</p>
    <p class="text-muted" style="font-size: 12pt;">Grows with your team</p>
  </div>
  <div style="text-align: center; flex: 1;">
    <i class="fa-solid fa-plug" style="font-size: 32pt; color: var(--primary-color);"></i>
    <p class="font-bold" style="margin-top: 10px;">Integrated</p>
    <p class="text-muted" style="font-size: 12pt;">Works with your tools</p>
  </div>
</div>
```

---

## Timeline & Process Steps

Show sequential steps, milestones, or a process flow.

### Horizontal Process Steps

```html
<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 15px;">
  <div style="text-align: center; flex: 1;">
    <div style="width: 50px; height: 50px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-size: 18pt; font-weight: 600;">1</div>
    <p class="font-bold">Discovery</p>
    <p class="text-muted" style="font-size: 12pt;">Understand requirements</p>
  </div>
  <div style="text-align: center; flex: 1;">
    <div style="width: 50px; height: 50px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-size: 18pt; font-weight: 600;">2</div>
    <p class="font-bold">Design</p>
    <p class="text-muted" style="font-size: 12pt;">Create solution architecture</p>
  </div>
  <div style="text-align: center; flex: 1;">
    <div style="width: 50px; height: 50px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-size: 18pt; font-weight: 600;">3</div>
    <p class="font-bold">Build</p>
    <p class="text-muted" style="font-size: 12pt;">Develop and iterate</p>
  </div>
  <div style="text-align: center; flex: 1;">
    <div style="width: 50px; height: 50px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-size: 18pt; font-weight: 600;">4</div>
    <p class="font-bold">Launch</p>
    <p class="text-muted" style="font-size: 12pt;">Deploy and monitor</p>
  </div>
</div>
```

### Timeline with Connecting Line

```html
<div style="position: relative; display: flex; justify-content: space-between; padding-top: 30px;">
  <!-- Connecting line -->
  <div style="position: absolute; top: 55px; left: 10%; right: 10%; height: 3px; background: var(--primary-color); opacity: 0.3;"></div>

  <div style="text-align: center; flex: 1; position: relative; z-index: 1;">
    <div style="width: 50px; height: 50px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-weight: 600;">Q1</div>
    <p class="font-bold">Planning</p>
  </div>
  <div style="text-align: center; flex: 1; position: relative; z-index: 1;">
    <div style="width: 50px; height: 50px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-weight: 600;">Q2</div>
    <p class="font-bold">Development</p>
  </div>
  <div style="text-align: center; flex: 1; position: relative; z-index: 1;">
    <div style="width: 50px; height: 50px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-weight: 600;">Q3</div>
    <p class="font-bold">Testing</p>
  </div>
  <div style="text-align: center; flex: 1; position: relative; z-index: 1;">
    <div style="width: 50px; height: 50px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-weight: 600;">Q4</div>
    <p class="font-bold">Launch</p>
  </div>
</div>
```

---

## Full-Width Image

Product screenshots, team photos, or visual hero slides.

### Image Fills Content Area

```html
<section id="product-screenshot">
  <h2>Product Overview</h2>
  <div class="content">
    <img src="screenshot.png" style="width: 100%; border-radius: var(--box-radius); box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
  </div>
</section>
```

### Stretched Image (Fills All Remaining Space)

```html
<section id="hero-image">
  <h2>Dashboard View</h2>
  <img class="r-stretch" src="dashboard.png" style="border-radius: var(--box-radius);">
</section>
```

---

## Overlay Text on Image

Place text over a background image, commonly used for hero slides or quote slides.

### Centered Overlay on Background Image

```html
<section data-background-image="photo.jpg" data-background-opacity="0.4">
  <div style="text-align: center; position: relative; z-index: 1;">
    <h1 style="color: white; font-size: 48pt;">Big Headline</h1>
    <p style="color: white; font-size: 20pt;">Supporting text overlay</p>
  </div>
</section>
```

### Quote with Background

```html
<section data-background-image="landscape.jpg" data-background-opacity="0.3">
  <div style="text-align: center; position: relative; z-index: 1; max-width: 800px; margin: 0 auto;">
    <blockquote style="border: none; padding: 0;">
      <p style="color: white; font-size: 28pt; font-style: italic; line-height: 1.4;">"Innovation distinguishes between a leader and a follower."</p>
      <cite style="color: rgba(255,255,255,0.8); font-size: 16pt;">Steve Jobs</cite>
    </blockquote>
  </div>
</section>
```

---

## Comparison Layout

Side-by-side comparison of options, before/after, or pros/cons.

### Two-Column Comparison

```html
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
  <div style="background: var(--secondary-color); padding: 30px; border-radius: var(--box-radius);">
    <h3 style="color: var(--text-muted);">Before</h3>
    <ul>
      <li>Manual data entry</li>
      <li>Slow processing</li>
      <li>Error-prone workflows</li>
    </ul>
  </div>
  <div style="background: var(--primary-color); padding: 30px; border-radius: var(--box-radius); color: white;">
    <h3>After</h3>
    <ul>
      <li>Automated pipelines</li>
      <li>Real-time processing</li>
      <li>Zero-touch workflows</li>
    </ul>
  </div>
</div>
```

### Three-Tier Pricing / Plan Comparison

```html
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; align-items: start;">
  <div style="background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius); text-align: center;">
    <h3>Starter</h3>
    <p class="text-4xl font-bold">$9</p>
    <p class="text-muted">/month</p>
    <ul style="text-align: left; margin-top: 15px;">
      <li>5 projects</li>
      <li>Basic analytics</li>
    </ul>
  </div>
  <div style="background: var(--primary-color); color: white; padding: 25px; border-radius: var(--box-radius); text-align: center; transform: scale(1.05);">
    <h3>Pro</h3>
    <p class="text-4xl font-bold">$29</p>
    <p style="opacity: 0.8;">/month</p>
    <ul style="text-align: left; margin-top: 15px;">
      <li>Unlimited projects</li>
      <li>Advanced analytics</li>
      <li>Priority support</li>
    </ul>
  </div>
  <div style="background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius); text-align: center;">
    <h3>Enterprise</h3>
    <p class="text-4xl font-bold">Custom</p>
    <p class="text-muted">pricing</p>
    <ul style="text-align: left; margin-top: 15px;">
      <li>Everything in Pro</li>
      <li>SSO & SAML</li>
      <li>Dedicated support</li>
    </ul>
  </div>
</div>
```

---

## Quote Slides

Full-slide or inline quotes for testimonials or key statements.

### Centered Full-Slide Quote

```html
<section style="display: flex; align-items: center; justify-content: center; height: 100%;">
  <div style="text-align: center; max-width: 900px;">
    <blockquote>
      <p class="text-2xl" style="line-height: 1.5;">"The best way to predict the future is to create it."</p>
      <cite style="margin-top: 15px; display: block;">Peter Drucker</cite>
    </blockquote>
  </div>
</section>
```

### Testimonial with Attribution

```html
<div style="background: var(--secondary-color); padding: 30px; border-radius: var(--box-radius); max-width: 800px; margin: 0 auto;">
  <p class="text-xl" style="font-style: italic; line-height: 1.5;">"This product transformed our workflow. We reduced processing time by 80%."</p>
  <div style="display: flex; align-items: center; gap: 15px; margin-top: 20px;">
    <div style="width: 45px; height: 45px; border-radius: 50%; background: var(--primary-color);"></div>
    <div>
      <p class="font-bold">Jane Smith</p>
      <p class="text-muted" style="font-size: 12pt;">CTO, Acme Corp</p>
    </div>
  </div>
</div>
```

---

## Logo / Partner Grid

Display partner logos, client logos, or technology stack icons.

### Logo Grid (3 columns)

```html
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; align-items: center; justify-items: center;">
  <div style="text-align: center;">
    <i class="fa-brands fa-aws" style="font-size: 36pt; color: var(--muted-color);"></i>
    <p class="text-muted" style="margin-top: 8px;">AWS</p>
  </div>
  <div style="text-align: center;">
    <i class="fa-brands fa-google" style="font-size: 36pt; color: var(--muted-color);"></i>
    <p class="text-muted" style="margin-top: 8px;">Google Cloud</p>
  </div>
  <div style="text-align: center;">
    <i class="fa-brands fa-microsoft" style="font-size: 36pt; color: var(--muted-color);"></i>
    <p class="text-muted" style="margin-top: 8px;">Azure</p>
  </div>
  <div style="text-align: center;">
    <i class="fa-brands fa-docker" style="font-size: 36pt; color: var(--muted-color);"></i>
    <p class="text-muted" style="margin-top: 8px;">Docker</p>
  </div>
  <div style="text-align: center;">
    <i class="fa-brands fa-github" style="font-size: 36pt; color: var(--muted-color);"></i>
    <p class="text-muted" style="margin-top: 8px;">GitHub</p>
  </div>
  <div style="text-align: center;">
    <i class="fa-brands fa-figma" style="font-size: 36pt; color: var(--muted-color);"></i>
    <p class="text-muted" style="margin-top: 8px;">Figma</p>
  </div>
</div>
```

For actual logo images (not Font Awesome icons), replace the `<i>` with:
```html
<img src="logo.png" style="max-height: 50px; max-width: 150px; object-fit: contain; opacity: 0.7;">
```

---

## Team / Profile Cards

Team introductions, speaker bios, or stakeholder profiles.

### Profile Cards Row

```html
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px;">
  <div style="text-align: center; background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius);">
    <div style="width: 80px; height: 80px; border-radius: 50%; background: var(--primary-color); margin: 0 auto 15px;"></div>
    <p class="font-bold text-lg">Alex Chen</p>
    <p class="text-muted" style="font-size: 12pt;">CEO & Co-founder</p>
    <p style="font-size: 12pt; margin-top: 10px;">15 years in enterprise software.</p>
  </div>
  <div style="text-align: center; background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius);">
    <div style="width: 80px; height: 80px; border-radius: 50%; background: var(--primary-color); margin: 0 auto 15px;"></div>
    <p class="font-bold text-lg">Maria Lopez</p>
    <p class="text-muted" style="font-size: 12pt;">CTO</p>
    <p style="font-size: 12pt; margin-top: 10px;">Former lead architect at Google.</p>
  </div>
  <div style="text-align: center; background: var(--secondary-color); padding: 25px; border-radius: var(--box-radius);">
    <div style="width: 80px; height: 80px; border-radius: 50%; background: var(--primary-color); margin: 0 auto 15px;"></div>
    <p class="font-bold text-lg">Sam Park</p>
    <p class="text-muted" style="font-size: 12pt;">VP of Sales</p>
    <p style="font-size: 12pt; margin-top: 10px;">Scaled revenue from $0 to $50M.</p>
  </div>
</div>
```

Replace the colored placeholder circle with an actual photo:
```html
<img src="photo.jpg" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; margin: 0 auto 15px;">
```
