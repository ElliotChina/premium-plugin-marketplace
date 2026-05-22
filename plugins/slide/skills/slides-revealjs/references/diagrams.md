# Diagrams with Mermaid

Add flowcharts, sequence diagrams, class diagrams, and more using the Mermaid plugin. Mermaid renders diagrams from a simple text syntax directly in your slides.

## Setup

The scaffold does not include Mermaid by default. Add these to your HTML:

```html
<!-- Before Reveal.initialize() -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin@11.12.3/plugin/mermaid/mermaid.js"></script>
```

Add `RevealMermaid` to the plugins array:

```javascript
Reveal.initialize({
  plugins: [ RevealMermaid ],
  // Optional: Mermaid configuration
  mermaid: {
    // flowchart: { curve: 'linear' },
  },
});
```

## Basic Usage

Wrap Mermaid syntax in a `<div class="mermaid">` with a `<pre>` inside:

```html
<section>
  <h2>System Architecture</h2>
  <div class="mermaid">
    <pre>
      flowchart LR
        Client --> API
        API --> Database
        API --> Cache
    </pre>
  </div>
</section>
```

## Diagram Types

### Flowchart

```html
<div class="mermaid">
  <pre>
    flowchart TD
      A[Start] --> B{Decision}
      B -- Yes --> C[Process A]
      B -- No --> D[Process B]
      C --> E[End]
      D --> E
  </pre>
</div>
```

**Direction keywords:**
- `TD` / `TB` — Top to Down (Top to Bottom)
- `BT` — Bottom to Top
- `LR` — Left to Right
- `RL` — Right to Left

**Node shapes:**
- `A[text]` — Rectangle
- `A(text)` — Rounded rectangle
- `A{text}` — Diamond
- `A((text))` — Circle
- `A{text}` — Diamond (decision)
- `A>text]` — Flag shape
- `A{{text}}` — Hexagon

**Arrow types:**
- `-->` — Solid arrow
- `---` — Solid line (no arrow)
- `-.-` — Dotted line
- `-.->` — Dotted arrow
- `==>` — Thick arrow
- `-->text-->` — Arrow with label

### Sequence Diagram

```html
<div class="mermaid">
  <pre>
    sequenceDiagram
      participant Client
      participant Server
      participant DB
      Client->>Server: HTTP Request
      Server->>DB: Query
      DB-->>Server: Results
      Server-->>Client: Response
  </pre>
</div>
```

**Arrow types:**
- `->>` — Solid line with arrow
- `-->>` — Dotted line with arrow
- `--)` — Dotted line with open arrow (async)
- `-x` — Solid line with X (lost message)

**Add notes and activation:**

```
sequenceDiagram
  participant A as Alice
  participant B as Bob
  activate A
  A->>B: Hello
  activate B
  Note right of B: Thinking...
  B-->>A: Hi!
  deactivate B
  deactivate A
```

### Class Diagram

```html
<div class="mermaid">
  <pre>
    classDiagram
      class Animal {
        +String name
        +int age
        +makeSound()
      }
      class Dog {
        +fetch()
      }
      class Cat {
        +purr()
      }
      Animal <|-- Dog
      Animal <|-- Cat
  </pre>
</div>
```

### State Diagram

```html
<div class="mermaid">
  <pre>
    stateDiagram-v2
      [*] --> Idle
      Idle --> Processing : Submit
      Processing --> Success : Complete
      Processing --> Error : Fail
      Success --> [*]
      Error --> Idle : Retry
  </pre>
</div>
```

### Gantt Chart

```html
<div class="mermaid">
  <pre>
    gantt
      title Project Timeline
      dateFormat YYYY-MM-DD
      section Planning
        Research       :a1, 2024-01-01, 10d
        Design         :a2, after a1, 5d
      section Development
        Frontend       :b1, after a2, 15d
        Backend        :b2, after a2, 12d
      section Testing
        QA Testing     :c1, after b1, 7d
  </pre>
</div>
```

### Pie Chart

```html
<div class="mermaid">
  <pre>
    pie title Market Share
      "Product A" : 40
      "Product B" : 30
      "Product C" : 20
      "Other" : 10
  </pre>
</div>
```

### ER Diagram

```html
<div class="mermaid">
  <pre>
    erDiagram
      CUSTOMER ||--o{ ORDER : places
      ORDER ||--|{ LINE_ITEM : contains
      CUSTOMER {
        string name
        string email
      }
      ORDER {
        int id
        date created
      }
      LINE_ITEM {
        string product
        int quantity
      }
  </pre>
</div>
```

### Mind Map

```html
<div class="mermaid">
  <pre>
    mindmap
      root((Central Topic))
        Topic A
          Sub A1
          Sub A2
        Topic B
          Sub B1
        Topic C
  </pre>
</div>
```

### Git Graph

```html
<div class="mermaid">
  <pre>
    gitGraph
      commit
      commit
      branch develop
      checkout develop
      commit
      commit
      checkout main
      merge develop
      commit
  </pre>
</div>
```

### User Journey

```html
<div class="mermaid">
  <pre>
    journey
      title Customer Journey
      section Discovery
        Visit website: 5: Customer
        Browse products: 4: Customer
      section Purchase
        Add to cart: 4: Customer
        Checkout: 3: Customer
        Payment: 2: Customer
  </pre>
</div>
```

### Timeline

```html
<div class="mermaid">
  <pre>
    timeline
      title Project History
      section 2023
        Q1 : Project kickoff
        Q2 : Alpha release
      section 2024
        Q1 : Beta launch
        Q2 : Public release
  </pre>
</div>
```

## Theming

### Dark Theme (recommended for dark slide backgrounds)

```
%%{init: {'theme': 'dark', 'themeVariables': { 'darkMode': true }}}%%
flowchart TD
  A --> B
```

### Light Theme

```
%%{init: {'theme': 'default' }}}%%
flowchart TD
  A --> B
```

### Forest Theme

```
%%{init: {'theme': 'forest' }}}%%
flowchart TD
  A --> B
```

### Custom Colors

Override specific theme variables:

```
%%{init: {'theme': 'dark', 'themeVariables': {
  'primaryColor': '#2196F3',
  'primaryTextColor': '#fff',
  'primaryBorderColor': '#1565C0',
  'lineColor': '#90CAF9',
  'secondaryColor': '#4CAF50',
  'tertiaryColor': '#FF9800'
}}}%%
flowchart TD
  A[Start] --> B[Process]
```

## Size Considerations

Mermaid diagrams can overflow slides if they're too large. To manage this:

1. **Keep diagrams simple** — Limit to 8-12 nodes for flowcharts, 4-6 participants for sequence diagrams
2. **Use shorter labels** — Long text in nodes makes diagrams wider
3. **Choose direction wisely** — Use `LR` (left-right) for wide slides, `TD` (top-down) for tall diagrams
4. **Style the container** — Constrain the diagram size:

```html
<div class="mermaid" style="max-width: 900px; margin: 0 auto;">
  <pre>
    flowchart LR
      A --> B --> C
  </pre>
</div>
```

## Diagram with Title and Content

Combine a diagram with explanatory text using a two-column layout:

```html
<section style="display: flex; flex-direction: column; height: 100%;">
  <h2>Request Flow</h2>
  <div style="flex: 1; display: grid; grid-template-columns: 2fr 1fr; gap: 30px; min-height: 0;">
    <div class="mermaid">
      <pre>
        flowchart LR
          Client --> LoadBalancer
          LoadBalancer --> Server1
          LoadBalancer --> Server2
          Server1 --> Database
          Server2 --> Database
      </pre>
    </div>
    <div style="display: flex; flex-direction: column; justify-content: center;">
      <p><strong>Key Points:</strong></p>
      <ul>
        <li>Load balancer distributes traffic</li>
        <li>Two active servers</li>
        <li>Shared database backend</li>
      </ul>
    </div>
  </div>
</section>
```

## Fragments with Diagrams

You can't fragment individual diagram elements with Mermaid. Instead, use multiple diagrams across slides with auto-animate, or use the reveal.js fragment system on the container level:

```html
<section>
  <h2>Architecture Evolution</h2>
  <div class="fragment">
    <div class="mermaid">
      <pre>
        flowchart LR
          Monolith --> Database
      </pre>
    </div>
  </div>
  <div class="fragment">
    <div class="mermaid">
      <pre>
        flowchart LR
          API --> ServiceA
          API --> ServiceB
          ServiceA --> Database
          ServiceB --> Database
      </pre>
    </div>
  </div>
</section>
```

## References

- [Mermaid Plugin](plugins/plugin-mermaid.md)
- [Mermaid Documentation](https://mermaid.js.org/)
