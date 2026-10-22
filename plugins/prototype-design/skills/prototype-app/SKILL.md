---
name: prototype-app
description: Build a runnable, clickable prototype inside the frontend project — a prototypes/ directory mirroring the real pages one-to-one, with working navigation between prototype pages, on-demand multi-variant comparison per page, and a single-file logic demo for sanity-checking state models. Use when the user wants to prototype a UI flow end-to-end, explore what a page or flow should look like, compare layout options, or validate business logic before writing real code.
---

# Prototype App

A prototype app is a **runnable mirror of the product that answers design questions**. It lives inside the frontend project as a self-contained `prototypes/` directory — fully isolated from the production source tree — whose pages map one-to-one onto the real routes, navigate between each other like the real app, and run on the existing dev server with zero new tooling. When a prototype page is validated it is promoted into real code — and **kept**: the directory is a design archive that evolves alongside the codebase, not a scratch space.

## Pick a branch

Identify which question is being answered, from the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). A single, self-contained HTML file that lets anyone drive a state model by pressing buttons — free-play actions plus guided walkthroughs, shareable to a non-developer. Files live under `prototypes/logic/`.
- **"What should this look like / how should this flow feel?"** → [UI.md](UI.md). Clickable prototype pages in `prototypes/`, mirroring the real routes, navigating between each other, with optional multi-variant comparison per page.

The two branches produce very different artifacts, so getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or flow → UI) and state the assumption at the top of the prototype.

Restate the brief in one sentence before building — what the prototype answers, and which routes (or which state model) it covers.

## Hard rules

1. **Physical isolation.** All prototype code lives in a single top-level `prototypes/` directory, outside the production source tree. Prototype routes are mounted dev-only:
   - Next.js App Router: one-line re-export shims under a route group such as `app/(prototype)/prototype/`, guarded in the segment layout with `if (process.env.NODE_ENV === 'production') notFound()`. The shims are the only bridge.
   - React Router / Vite: register the prototype route array only when `import.meta.env.DEV`.

   The prototype files are permanent residents of the repo, so the gate must not depend on anyone remembering to remove them.
2. **Mirror convention, file-for-file.** A prototype route is `/prototype/` plus the real page's path: `app/dashboard` ↔ `/prototype/dashboard`; a page that doesn't exist yet mirrors the route it *will* live at — pick the path up front and keep it stable. File mirroring is a source-root prefix swap across the whole referenced subtree: `src/components/device/DataSourceSelector.tsx` → `prototypes/components/device/DataSourceSelector.tsx` — same relative path, same file name, same export style. **One prototype file per production file**: never merge several production components into one invented file, never coin a name production doesn't use. Every mirrored file opens with a one-line header comment naming its production counterpart, making tree-to-tree consistency greppable (the bundled `scripts/mirror-check.sh` runs the check mechanically). Only prototype-only artifacts sit outside the mirroring — mock data, the variant harness, `logic/` demos — under clearly prototype-only names and locations (`shared/`, `logic/`), each declaring itself (`原型私有`) in its header. Two sanctioned deviations: a mirrored file re-implements its counterpart with the **same public signature** — subsets are fine, deliberate signature drift goes in the header; and files that cannot coexist with production in one program (global ambient declarations) keep a prototype-prefixed name in a prototype-only location, reason in the header. Production files with no prototype counterpart (api, lib, auth, tests) are simply absent. The correspondence drives navigation and serves as the archive's index; it carries no shared code and no sync obligation: when production reorganizes, the archive stays frozen.
3. **Zero code coupling.** Prototype code never imports production code, and production code never imports prototype code — the dev-only mount shims are the sole exception. Enforced mechanically by `scripts/mirror-check.sh` in both directions (bridge files exempt via `BRIDGE_ALLOW`). Visual consistency is by reference: token values, layout shapes, and components are copied or redeclared inside `prototypes/`, never imported; mock data lives in the prototype surface too. This is what makes the archive immune to refactors of the real code, and the real code safe from prototype experiments.
4. **Archive, never discard.** Promotion never deletes the prototype page. Prototypes commit with the feature branch — there is no throwaway branch. A prototype file is removed only when the user explicitly asks.
5. **Trivial to run.** The project's existing dev server is the only command. No new toolchain, no separate server, no bundler config.
6. **In-memory state only.** Cross-page prototype state lives in a prototype-private in-memory store. Persistence is never a dependency; if the question is about persistence itself, hit a scratch store with a clear "PROTOTYPE, wipe me" name.
7. **One picker spec.** When a page needs competing options, the picker is [PICKER.md](PICKER.md) — copy it verbatim. It stays identical across every project so it always reads as harness chrome, never as part of the design being judged.

## Workflow

1. Scope: one question per run. If the ask spans several pages ("the dashboard"), pick the highest-leverage route set, say which and why, and offer the rest as follow-ups.
2. Recon: framework and routing convention, styling system and tokens, where the pages render and beside what. Every prototype page should look like it could ship in this product tomorrow.
3. Build per the branch file, verify it runs and every interaction responds, then hand off with the URL (and, for variants, the picker keys).
4. On selection: promote per [UI.md](UI.md) or [LOGIC.md](LOGIC.md). The prototype stays — that's the archive.
