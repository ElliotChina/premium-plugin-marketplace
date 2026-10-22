# UI Prototype

Build **clickable prototype pages** in `prototypes/` that mirror the real routes one-to-one, navigate between each other through the real router, and run on the existing dev server. The user clicks through whole flows — list → detail → checkout — exactly as they would in the shipped product, then the validated pages are promoted into real code and kept as the design record.

If the question is about logic/state rather than what something looks like, this is the wrong branch. Use [LOGIC.md](LOGIC.md).

## When this is the right shape

- "What should this flow look like?" — several pages that need to work as a sequence.
- "I want to click through the new checkout before we build it."
- "Try a different layout for the settings screen." — single page, optionally with competing variants.
- Any time the choice would otherwise be made between three vague mockups in someone's head.

## Two starting points

**From existing code** (redesign or extension): read the production page first — its route path, directory organization, data shapes, and the token values it uses — then rebuild a faithful standalone copy under the mirror path. The prototype starts true to the current design and diverges only as the design questions demand. This is "generation from code": recon plus rebuild, no imports.

**From zero** (new page or flow): there is no production page to mirror yet, so the mirror path names the route it *will* live at — `/prototype/new-feature` ↔ the future `app/new-feature`. Decide the path up front and keep it stable; the convention is the archive's index, including for pages that don't exist yet.

Structure still needs a template. Pick the **closest production page** — most recent, most similar in shape — and mirror its organization pattern: entry-file naming, css naming, whether page parts live in a subdirectory, how components are colocated. Build the prototype at production granularity from the start, so promotion can adopt the structure as-is. With no in-repo reference (greenfield project), fall back to the framework's house conventions. Realistic context comes from the prototype surface's own rebuilt layout.

Promotion is where a from-zero structure gets anchored: production adopts it — or normalizes it to conventions as they have since evolved. From that commit on the mirror is real, and the frozen-archive rule takes over.

Both start points converge on the same build process below.

## Process

### 1. State the question and list the routes

One sentence: what the prototype answers, which routes it covers. Then a route list mapping real path → prototype path. The directory grows page-by-page as questions arise; each page still answers one question — the clickable whole is what makes it worth more than isolated mockups.

### 2. Build the mirror pages

- **Path convention**: `/prototype/` + the real page's path, using whatever routing conventions the project already uses. Don't invent a new top-level structure.
- **Structure mirrors production file-for-file**: the mirror path is a source-root prefix swap — `src/pages/HistoryQuery.tsx` → `prototypes/pages/HistoryQuery.tsx`, `src/components/common/QueryPriceTag.tsx` → `prototypes/components/common/QueryPriceTag.tsx`. Same name, same relative location, same export style. One prototype file per production file — never merge components into an invented convenience file, never coin a name production doesn't use. Each mirrored file opens with a one-line header comment naming its production counterpart. Prototype-only files (mock data, variant harness) keep clearly prototype-only names (`mock-data.ts`, `proto-store.ts`) and live apart from mirrored files.
- **Real context, not a vacuum**: prototype pages render with realistic siblings — a header/footer layout rebuilt in the prototype surface to mimic the real one, plausible data, product-shaped copy, believable names and numbers. No lorem ipsum, no dead buttons, no "imagine this part".
- **Craft bar**: every page individually meets it — `ease-out` on entrances (never `ease-in`), UI motion under 300ms, `transform`/`opacity` only, correct `transform-origin`, `prefers-reduced-motion` handled. A sloppy page doesn't widen the exploration; it loses on execution and teaches nothing about its direction.
- **Native to the product, self-contained**: copy the project's token values, fonts, and spacing as reference, and rebuild the components you need inside `prototypes/` — never import production components (hard rule 3). A prototype page should look like it could ship tomorrow, and keep looking that way no matter how the real code is refactored.

### 3. Wire navigation and shared state

- Navigate between prototype pages with the framework's real router (`Link`, `router.push`, …) pointing at `/prototype/*` siblings, so whole flows click through end-to-end.
- Cross-page state lives in a **prototype-private in-memory store**: a module-level object, a React context, or a tiny store the project already uses. Step 1's form feeds step 2's summary. No persistence, no backend.
- Data is mocked or stubbed inside the prototype surface, read-only — no production API clients, data hooks, or stores. Never wire a prototype page to real mutations; the question is "what should this feel like", not "does the backend work".

### 4. Multi-variant on demand (per page)

When a single page needs competing options, give it variants — and only that page:

- **3 variants by default, 5 at most.** More than 5 stops being a comparison and becomes noise.
- **Diverge on a named axis** — layout, density, personality, motion, interaction model. Each variant needs a name and a stated axis before any code; if two proposed variants differ only in colour or copy, they are one direction — replace one. Three slightly-tweaked card grids is wallpaper, not exploration.
- **Completion criterion**: every variant has a name and an axis, and no two variants share an axis position.
- **The picker is [PICKER.md](PICKER.md), verbatim.** Number keys `1–N`, `←`/`→`, `R` to replay; selection persists via `?v=N`; the variant swap is instant (no transition) while only the picker's highlight slides. In a framework, keep the same behavior contract and express it idiomatically (state instead of `innerHTML`, a keyed re-mount so entrance animations re-run).
- Shared components between variants of one page: a shared prototype-local `<Header>` is fine; a shared `<Layout>` defeats the point. Each variant is free to throw out the layout.

### 5. Present and hand off

Before handing off, run the **mirror check**: grep the header comments across `prototypes/` and match them against both trees — every prototype file must map to exactly one production file, and every production file the prototype needs must appear exactly once. Gaps, merges, and invented names surface mechanically.

Surface the route list (start URL plus the pages it covers), or for variants the picker URL and keys. When presenting variants, give the honest table and stop — the choice belongs to the user:

| # | Variant | Axis | When it's the right choice | Its cost |
| --- | --- | --- | --- | --- |
| 1 | Quiet | Minimal motion, borders over shadows | Daily-use tool | Least memorable |
| 2 | Editorial | Large type, generous whitespace | The moment deserves weight | Eats vertical space |

One line on when each wins, one on what it costs. Never pre-pick a favorite. The most valuable feedback is usually **"I want the header from B with the sidebar from C"** — that combination is the actual design.

### 6. Promote and archive

Fold the winner into real code — **rewritten properly**: tests, error handling, and project conventions that prototypes skip. Promotion is a rewrite by construction — nothing was shared, so nothing carries over mechanically.

Then archive: the prototype page **stays** in `prototypes/`, committed with the feature branch. No throwaway branch, no deletion — the mirror mapping (`app/dashboard` ↔ `/prototype/dashboard`) is the archive's index, and the preserved page is the design record of why the real one looks the way it does.

## Anti-patterns

- **Variants that differ only in colour or copy.** That's a tweak, not a prototype. Real variants disagree about structure.
- **A shared `<Layout>` between variants.** Each variant should be free to throw out the layout.
- **Wiring variants to real mutations.** Read-only prototypes; stub anything that writes.
- **Promoting prototype code directly to production.** Rewrite it properly when you fold it in.
- **Importing across the boundary.** No production imports in `prototypes/`, no prototype imports in app code — the dev-only mount shim is the only bridge. Coupled prototype code is neither a valid reference nor a safe permanent resident.
- **Deleting or "cleaning up" promoted prototype pages.** The archive is the point; removal is the user's explicit call.
- **Judging a page in a vacuum.** An empty route hides the design problems its populated neighbors would expose. Render realistic context.
- **Inventing a new top-level prototype structure.** Follow the project's routing conventions.
- **Marking mirrored files with a `Proto` prefix, or boxing flat pages into directories.** The mirror path is the marker — name files exactly as their production counterparts (`Login.tsx`, not `ProtoLogin.tsx`; `Login.css`, not `login.css`; hooks keep production casing). A production flat page stays a flat file; only production directories become prototype directories. Identical basenames in the two trees are fine: imports are explicit paths, nothing collides at runtime.
- **Inventing convenience files.** Merging two production components into one handy `SearchControls.tsx` breaks the file-for-file index — split them back to their mirror paths, one file per production counterpart.
