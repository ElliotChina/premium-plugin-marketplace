# Design System Composition Guidelines

Helpful patterns for composing screens and dashboards using design system components in `.pen` files. These are suggestions to get you started—feel free to adapt them to your needs.

---

## 1. Common Component Patterns

Component naming patterns you might encounter:
- `Button/*` — Button variants
- `Input/*` or `Input Group/*` — Form inputs
- `Card` — Card containers
- `Sidebar` — Navigation sidebar
- `Table` or `Data Table` — Table elements
- `Alert/*` — Feedback alerts
- `Modal/*` or `Dialog` — Modal dialogs

---

## 2. Understanding Slots

Slots are placeholder frames inside components where you insert child components. They're marked with the `slot` property containing an array of recommended component IDs.

### How to Identify Slots

When reading a component, look for frames with slot property:
```json
{
  "id": "slotId",
  "name": "Content Slot",
  "slot": ["recommendedComponentId1", "recommendedComponentId2"]
}
```

### How to Use Slots

A typical approach:
1. **Insert the parent component** and capture its binding
2. **Insert children into the slot** using path: `parentBinding/slotId`
3. **Consider using recommended components** listed in the slot's `slot` array (though you can insert other content too)

```javascript
sidebar=I(page, {type: "ref", ref: "sidebarComponentId", height: "fill_container"})
item1=I(sidebar+"/contentSlotId", {type: "ref", ref: "sidebarItemId", descendants: {...}})
item2=I(sidebar+"/contentSlotId", {type: "ref", ref: "sidebarItemId", descendants: {...}})
```

If you don't need to use a particular slot in a component instance, mark the slot `enabled: false` to hide it.

---

## 3. Icons

### Available Icon Sets

You can use `icon_font` type for icons with these font families:

| Font Family | Style | Example Names |
|-------------|-------|---------------|
| `lucide` | Outline, rounded | `home`, `settings`, `user`, `search`, `plus`, `x` |
| `feather` | Outline, rounded | `home`, `settings`, `user`, `search`, `plus`, `x` |
| `Material Symbols Outlined` | Outline | `home`, `settings`, `person`, `search`, `add`, `close` |
| `Material Symbols Rounded` | Rounded | `home`, `settings`, `person`, `search`, `add`, `close` |
| `Material Symbols Sharp` | Sharp corners | `home`, `settings`, `person`, `search`, `add`, `close` |

### Icon Usage

Standalone icon with Lucide, and Material Symbols with weight:

```javascript
icon=I(container, {type: "icon_font", iconFontFamily: "lucide", iconFontName: "settings", width: 24, height: 24, fill: "$--foreground"})
icon=I(container, {type: "icon_font", iconFontFamily: "Material Symbols Rounded", iconFontName: "dashboard", width: 24, height: 24, fill: "$--foreground", weight: 400})
```

### Overriding Icons in Components

When a component contains an icon, override it via descendants:
```javascript
descendants: {
  "iconNodeId": { iconFontName: "settings" }
}
```

### Common Icon Names

| Action | Lucide/Feather | Material Symbols |
|--------|----------------|------------------|
| Home | `home` | `home` |
| Settings | `settings` | `settings` |
| User | `user` | `person` |
| Search | `search` | `search` |
| Add | `plus` | `add` |
| Close | `x` | `close` |
| Edit | `edit`, `pencil` | `edit` |
| Delete | `trash`, `trash-2` | `delete` |
| Check | `check` | `check` |
| Arrow right | `arrow-right` | `arrow_forward` |
| Chevron down | `chevron-down` | `expand_more` |
| Menu | `menu` | `menu` |
| Dashboard | `layout-dashboard` | `dashboard` |
| Folder | `folder` | `folder` |
| File | `file` | `description` |
| Calendar | `calendar` | `calendar_today` |
| Mail | `mail` | `mail` |
| Bell | `bell` | `notifications` |

---

## 4. Sidebar Composition

### Structure

```
Sidebar Component
├── Header (logo, brand)
├── Content Slot ← Insert navigation items here
└── Footer (user profile, settings)
```

### Populating Sidebar Navigation

Insert the sidebar, then add section title (if available), active item, and default items:

```javascript
sidebar=I(page, {type: "ref", ref: "sidebarId", height: "fill_container"})
newSectionTitle=I(sidebar+"/contentSlotId", {type: "ref", ref: "sidebarSectionTitleId", descendants: {"labelTextId": {content: "Main Menu"}}})
itemDashboard=I(sidebar+"/contentSlotId", {type: "ref", ref: "sidebarItemActiveId", descendants: {"iconId": {iconFontName: "dashboard"}, "labelId": {content: "Dashboard"}}})
itemUsers=I(sidebar+"/contentSlotId", {type: "ref", ref: "sidebarItemDefaultId", descendants: {"iconId": {iconFontName: "users"}, "labelId": {content: "Users"}}})
itemSettings=I(sidebar+"/contentSlotId", {type: "ref", ref: "sidebarItemDefaultId", descendants: {"iconId": {iconFontName: "settings"}, "labelId": {content: "Settings"}}})
```

---

## 5. Card Composition

### Structure

Cards typically have three slots:

```
Card Component
├── Header Slot ← Title, description
├── Content Slot ← Main content
└── Actions Slot ← Buttons
```

### Populating Card Slots

Insert card, replace header with custom content, setup content slot for form, setup actions slot with buttons:

```javascript
card=I(container, {type: "ref", ref: "cardId", width: 480})
newNode=R(card+"/headerSlotId", {type: "frame", layout: "vertical", gap: 4, padding: 24, width: "fill_container", children: [
  {type: "text", content: "Card Title", fill: "$--foreground", fontFamily: "$--font-primary", fontSize: 18, fontWeight: "600"},
  {type: "text", content: "Card description goes here", fill: "$--muted-foreground", fontFamily: "$--font-secondary", fontSize: 14}
]})
U(card+"/contentSlotId", {layout: "vertical", gap: 16, padding: 24})
input=I(card+"/contentSlotId", {type: "ref", ref: "inputGroupId", width: "fill_container", descendants: {"labelId": {content: "Email"}}})
U(card+"/actionsSlotId", {gap: 12, justifyContent: "end", padding: 24})
cancelBtn=I(card+"/actionsSlotId", {type: "ref", ref: "buttonOutlineId", descendants: {"iconId": {enabled: false}, "labelId": {content: "Cancel"}}})
saveBtn=I(card+"/actionsSlotId", {type: "ref", ref: "buttonPrimaryId", descendants: {"iconId": {enabled: false}, "labelId": {content: "Save"}}})
```

---

## 6. Tab Composition

### Structure

```
Tabs Container
└── Direct children: Tab Items (active/inactive)
```

### Building Tabs

Insert tabs container, then add tab items directly (first one active):

```javascript
tabs=I(container, {type: "ref", ref: "tabsId", width: "fit_content"})
tab1=I(tabs, {type: "ref", ref: "tabItemActiveId", descendants: {"labelId": {content: "General"}}})
tab2=I(tabs, {type: "ref", ref: "tabItemInactiveId", descendants: {"labelId": {content: "Security"}}})
tab3=I(tabs, {type: "ref", ref: "tabItemInactiveId", descendants: {"labelId": {content: "Billing"}}})
```

---

## 7. Dropdown Composition

### Structure

```
Dropdown Container
└── Direct children: Search, Dividers, Titles, List Items
```

### Building Dropdowns

Optional search, divider, section title, and items:

```javascript
dropdown=I(container, {type: "ref", ref: "dropdownId", height: "fit_content"})
search=I(dropdown, {type: "ref", ref: "searchBoxId"})
divider=I(dropdown, {type: "ref", ref: "listDividerId"})
title=I(dropdown, {type: "ref", ref: "listTitleId", descendants: {"labelId": {content: "Actions"}}})
optionA=I(dropdown, {type: "ref", ref: "listItemCheckedId", descendants: {"labelId": {content: "Option A"}}})
optionB=I(dropdown, {type: "ref", ref: "listItemUncheckedId", descendants: {"labelId": {content: "Option B"}}})
```

---

## 8. Table Composition

### Table Structure

```
Table (frame)
├── Table Header — Search/filter + action buttons
├── Table Wrapper — Contains all rows
│   ├── Header Row (frame)
│   │   └── Cell (frame)
│   │       └── Content (text, label, button, etc.)
│   ├── Data Row 1 (frame)
│   │   └── Cell (frame)
│   │       └── Content (text, label, button, etc.)
│   ├── Data Row 2 (frame)
│   │   └── Cell (frame)
│   │       └── Content (text, label, button, etc.)
│   └── ...
└── Table Footer — Row count + pagination
```

### Building Tables Step by Step

### Table Hierarchy

**Important:** Tables follow this strict nesting structure:
Table → Row → Cell (frame) → Cell Content (text, label, button, etc.)

- **Table**: Container with vertical layout holding all rows
- **Row**: Horizontal container holding cells
- **Cell**: Frame wrapper that controls column width
- **Cell Content**: The actual content inside the cell (text, badges, buttons, etc.)

**Add data rows with cells**

Note: For tables with many rows, split into multiple `batch_design` calls (e.g., 2-3 rows per call).

```javascript
row1=I(table, {type: "ref", ref: "dataTableRowId", width: "fill_container"})
nameCell=I(row1, {type: "ref", ref: "dataTableCellId", width: "fill_container"})
nameText=I(nameCell, {type: "text", content: "John Doe"})
emailCell=I(row1, {type: "ref", ref: "dataTableCellId", width: "fill_container"})
emailText=I(emailCell, {type: "text", content: "john@example.com"})
statusCell=I(row1, {type: "ref", ref: "dataTableCellId", width: 120})
statusBadge=I(statusCell, {type: "ref", ref: "labelSuccessId", descendants: {"textId": {content: "Active"}}})
actionsCell=I(row1, {type: "ref", ref: "dataTableCellId", width: 100})
actionBtn=I(actionsCell, {type: "ref", ref: "iconButtonId"})
```

### Column Width Strategy

Suggested starting points (adjust as needed):

| Column Type | Typical Width |
|-------------|-------|
| Primary identifier (name) | 200-250px |
| Email, URL | `fill_container` |
| Status, badge | 100-120px |
| Date | 120-150px |
| Actions | 80-100px |
| Numbers | 80-100px |

---

## 9. Pagination Composition

### Structure

```
Pagination Component
├── Previous Button
├── Page Numbers Slot ← Insert page items here
└── Next Button
```

### Building Pagination

Insert page numbers into slot:

```javascript
pagination=I(container, {type: "ref", ref: "paginationId"})
page1=I(pagination+"/pageNumbersSlotId", {type: "ref", ref: "paginationItemActiveId", descendants: {"labelId": {content: "1"}}})
page2=I(pagination+"/pageNumbersSlotId", {type: "ref", ref: "paginationItemDefaultId", descendants: {"labelId": {content: "2"}}})
page3=I(pagination+"/pageNumbersSlotId", {type: "ref", ref: "paginationItemDefaultId", descendants: {"labelId": {content: "3"}}})
ellipsis=I(pagination+"/pageNumbersSlotId", {type: "ref", ref: "paginationItemEllipsisId"})
page10=I(pagination+"/pageNumbersSlotId", {type: "ref", ref: "paginationItemDefaultId", descendants: {"labelId": {content: "10"}}})
```

---

## 10. Screen Layout Patterns

These patterns show the structure for common layouts. Each pattern is typically one batch_design call (3-5 ops). Combine with content from other sections to reach maximum 25 ops per call, or use as a first call then populate sections in subsequent calls.

### Pattern A: Sidebar + Content (Dashboard)

```
┌──────────┬────────────────────────────────┐
│          │                                │
│ Sidebar  │     Main Content Area          │
│  280px   │      fill_container            │
│          │                                │
└──────────┴────────────────────────────────┘
```

```javascript
screen=I(document, {type: "frame", name: "Dashboard", layout: "horizontal", width: 1440, height: "fit_content(900)", fill: "$--background", placeholder: true})
sidebar=I(screen, {type: "ref", ref: "sidebarId", height: "fill_container"})
main=I(screen, {type: "frame", layout: "vertical", width: "fill_container", height: "fill_container(900)", padding: 32, gap: 24})
```

### Pattern B: Header + Content

```
┌────────────────────────────────────────────┐
│              Header Bar (64px)             │
├────────────────────────────────────────────┤
│                                            │
│            Content Area                    │
│                                            │
└────────────────────────────────────────────┘
```

Fixed header and scrollable content:

```javascript
screen=I(document, {type: "frame", layout: "vertical", width: 1200, height: "fit_content(800)", fill: "$--background", placeholder: true})
header=I(screen, {type: "frame", layout: "horizontal", width: "fill_container", height: 64, padding: [0, 24], alignItems: "center", justifyContent: "space_between", stroke: {align: "inside", fill: "$--border", thickness: {bottom: 1}}})
content=I(screen, {type: "frame", layout: "vertical", width: "fill_container", height: "fit_content(736)", padding: 32, gap: 24})
```

### Pattern C: Two-Column Layout

```
┌─────────────────────┬─────────────┐
│                     │             │
│    Main (2/3)       │  Side (1/3) │
│   fill_container    │   360px     │
│                     │             │
└─────────────────────┴─────────────┘
```

Main column (flexible) and side column (fixed):

```javascript
columns=I(content, {type: "frame", layout: "horizontal", width: "fill_container", height: "fill_container(900)", gap: 24})
mainCol=I(columns, {type: "frame", layout: "vertical", width: "fill_container", height: "fit_content(900)", gap: 24})
sideCol=I(columns, {type: "frame", layout: "vertical", width: 360, height: "fit_content(900)", gap: 24})
```

### Pattern D: Card Grid

```
┌──────────┐ ┌──────────┐ ┌──────────┐
│  Card 1  │ │  Card 2  │ │  Card 3  │
└──────────┘ └──────────┘ └──────────┘
```

```javascript
cardGrid=I(container, {type: "frame", layout: "horizontal", width: "fill_container", gap: 16})
card1=I(cardGrid, {type: "ref", ref: "cardId", width: "fill_container"})
card2=I(cardGrid, {type: "ref", ref: "cardId", width: "fill_container"})
card3=I(cardGrid, {type: "ref", ref: "cardId", width: "fill_container"})
```

---

## 11. Common Compositions

These snippets show maximum 25 ops each. Combine with screen layout patterns, or use as standalone batch_design calls after the initial structure is created.

### Page Header with Breadcrumbs + Actions

Breadcrumbs on the left, action buttons on the right:

```javascript
pageHeader=I(main, {type: "frame", layout: "horizontal", width: "fill_container", justifyContent: "space_between", alignItems: "center"})
breadcrumbs=I(pageHeader, {type: "frame", layout: "horizontal", gap: 0, alignItems: "center"})
crumb1=I(breadcrumbs, {type: "ref", ref: "breadcrumbItemId", descendants: {"labelId": {content: "Dashboard"}}})
sep=I(breadcrumbs, {type: "ref", ref: "breadcrumbSeparatorId"})
crumb2=I(breadcrumbs, {type: "ref", ref: "breadcrumbItemActiveId", descendants: {"labelId": {content: "Users"}}})
actions=I(pageHeader, {type: "frame", layout: "horizontal", gap: 12})
exportBtn=I(actions, {type: "ref", ref: "buttonOutlineId", descendants: {"iconId": {enabled: false}, "labelId": {content: "Export"}}})
addBtn=I(actions, {type: "ref", ref: "buttonPrimaryId", descendants: {"iconId": {enabled: false}, "labelId": {content: "Add User"}}})
```

### Form Layout

Two fields in a row, then full-width fields:

```javascript
card=I(container, {type: "ref", ref: "cardId", width: "fill_container"})
form=I(card+"/contentSlotId", {type: "frame", layout: "vertical", gap: 16, width: "fill_container"})
row=I(form, {type: "frame", layout: "horizontal", gap: 16, width: "fill_container"})
firstName=I(row, {type: "ref", ref: "inputGroupId", width: "fill_container", descendants: {"labelId": {content: "First Name"}}})
lastName=I(row, {type: "ref", ref: "inputGroupId", width: "fill_container", descendants: {"labelId": {content: "Last Name"}}})
email=I(form, {type: "ref", ref: "inputGroupId", width: "fill_container", descendants: {"labelId": {content: "Email"}}})
message=I(form, {type: "ref", ref: "textareaGroupId", width: "fill_container", descendants: {"labelId": {content: "Message"}}})
```

### Metric Cards

Replace header with custom metric content, disable unused slots:

```javascript
metrics=I(content, {type: "frame", layout: "horizontal", gap: 16, width: "fill_container"})
metric1=I(metrics, {type: "ref", ref: "cardId", width: "fill_container"})
newNode=R(metric1+"/headerSlotId", {type: "frame", layout: "vertical", gap: 4, padding: 24, width: "fill_container", children: [
  {type: "text", content: "Total Users", fill: "$--muted-foreground", fontFamily: "$--font-secondary", fontSize: 14},
  {type: "text", content: "12,543", fill: "$--foreground", fontFamily: "$--font-primary", fontSize: 32, fontWeight: "600"}
]})
U(metric1+"/contentSlotId", {enabled: false})
U(metric1+"/actionsSlotId", {enabled: false})
```

---

## 12. Spacing Reference

Common spacing values as a starting point:

| Context | Gap | Padding |
|---------|-----|---------|
| Screen sections | 24-32 | — |
| Card grid | 16-24 | — |
| Form fields (vertical) | 16 | — |
| Form row (horizontal) | 16 | — |
| Button groups | 12 | — |
| Inside cards | — | 24 |
| Inside buttons | — | [10, 16] |
| Inside inputs | — | [8, 16] |
| Page content area | — | 32 |
| Sidebar items | 0 | [12, 16] |

---

## 13. Button Hierarchy

A good rule of thumb: one primary action per section helps users focus. Rough priority order:

| Priority | Variant | Often used for |
|----------|---------|---------|
| 1 | Primary/Default | Main action (Save, Submit, Create) |
| 2 | Secondary | Alternative actions |
| 3 | Outline | Tertiary, Cancel, Back |
| 4 | Ghost | Inline actions, navigation |
| 5 | Destructive | Delete, Remove |

### Button Actions Alignment

Common conventions:
- **Cards/Modals:** Right-align actions (`justifyContent: "end"`)
- **Forms:** Right-align submit buttons
- **Toolbars:** Left-align primary, right-align secondary
- **Destructive + Cancel:** Cancel on left, Destructive on right

---

## 14. Design Tokens

Using design token variables helps keep things consistent:

### Colors
| Token | Usage |
|-------|-------|
| `$--background` | Page background |
| `$--foreground` | Primary text |
| `$--muted-foreground` | Secondary text, placeholders |
| `$--card` | Card backgrounds |
| `$--border` | Borders, dividers |
| `$--primary` | Primary actions, brand |
| `$--secondary` | Secondary elements |
| `$--destructive` | Danger actions |

### Semantic Colors
| State | Background | Foreground |
|-------|------------|------------|
| Success | `$--color-success` | `$--color-success-foreground` |
| Warning | `$--color-warning` | `$--color-warning-foreground` |
| Error | `$--color-error` | `$--color-error-foreground` |
| Info | `$--color-info` | `$--color-info-foreground` |

### Typography
| Token | Usage |
|-------|-------|
| `$--font-primary` | Headings, labels, navigation |
| `$--font-secondary` | Body text, descriptions, inputs |

### Border Radius
| Token | Usage |
|-------|-------|
| `$--radius-none` | Tables, sharp containers |
| `$--radius-m` | Cards, modals |
| `$--radius-pill` | Buttons, inputs, badges |

---

## 15. Design Principles

These principles help ensure designs are grounded, consistent, and maintainable.

### Visual Hierarchy
- One clear focal point per section
- Use size, weight, and color to establish importance
- Primary actions should be visually dominant

### Alignment & Grid
- Align elements to an implicit grid
- Use consistent edge alignment within containers
- Avoid orphaned or floating elements

### Spacing Consistency
- Always use existing gap/padding values from the design system
- Don't mix arbitrary spacing values - pick from the established scale
- Maintain consistent vertical rhythm between sections

### Color Usage
- Always use `$--variable` tokens, never hardcode hex/rgb values
- Ensure sufficient contrast for text readability
- Use semantic colors for their intended purpose (error for errors, etc.)

### Content Density
- Don't overcrowd - leave breathing room
- Cards should contain one primary idea
- Tables should have reasonable column counts (typically 4-7)

### Grounding Rules
- Get component list via `get_editor_state` and then only get specific components you need via `batch_get`
- Verify with `get_screenshot` after major design operations
- Use existing components before creating custom frames
