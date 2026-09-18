# 05 · The in-app Architecture / "How it works" modal (ADR-0058)

Every CAOS/Faena web app **MUST** ship an in-app **Architecture / "How it works"** modal, opened by an
always-visible **ⓘ button in the header**. It is the fast visual proof the app is a *real, complete system*, not a
demo. The chrome (button + modal) is provided by the shared shell; each product supplies only its diagrams + copy.

Binding decision: [`conventions/architecture/0-archetype/ADR-0058-in-app-architecture-modal.md`](../../../conventions/architecture/0-archetype/ADR-0058-in-app-architecture-modal.md)
(in CAOS_MANAGE). Reference implementations: Veta and Circuita.

## What you inherit from the template

- **Chrome**, `@fasl-work/caos-app-shell` (≥ **0.1.2**) exposes the ⓘ button + the `ArchitectureModal`. The
  `ShellConfig` gained an `architecture` field; when it is present the button appears, when absent it is hidden.
- **Themed diagrams.** The template shipped five placeholder SVGs under `frontend/public/svg/tech/`; this
  repository draws its diagrams inline instead, in [`frontend/src/lib/architecture.ts`](../../frontend/src/lib/architecture.ts)
  (the programme-wide modal) and [`frontend/src/lib/riemannArchitecture.ts`](../../frontend/src/lib/riemannArchitecture.ts)
  (the Riemann page), and the unused placeholders were removed (2026-09-18). Every colour is a shell CSS-variable
  token (`--color-surface`, `--color-border`, `--color-accent`, `--color-fg`, `--color-good`, `--color-warn`, …) so
  the diagram repaints with the active light/dark theme.
- **A paste-ready config**, [`frontend/src/architecture.ts.txt`](../../frontend/src/architecture.ts.txt) with the
  five ADR-0058 tabs already wired to the SVGs and bilingual ES/EN bodies.

## How to wire it (per product)

1. **Copy** `frontend/src/architecture.ts.txt` to `frontend/src/architecture.ts`.
2. **Specialise** the product-specific tabs:
   - Draw the `app` tab's diagram for THIS product's domain (problem, input, method, value) and edit its
     `body_en` / `body_es`.
   - Draw the `science` tab's diagram with THIS product's real algorithm + equations and edit its body.
   - Tabs `lanes`, `web-flow`, `design` are archetype-generic, the shipped SVGs + copy are reusable as-is. Keep
     them; tweak only if your product deviates from the archetype.
   - Add domain tabs if useful (never *fewer* than the five).
3. **Pass it to the shell** in `frontend/src/main.tsx`:

   ```ts
   import { architecture } from './architecture';

   const shellConfig = {
     product: { name: 'YourProduct', mark: <YourIcon size={18} /> },
     routes: [/* … */],
     links: { github: '…' },
     version: '0.06.000',
     architecture,            // ← turns the ⓘ button on
   };
   ```

4. **Pin the shell** to `^0.1.2` in `frontend/package.json` (the version that ships the modal).

## The five mandatory tabs (ADR-0058 minimum)

| id | tab | generic? | what it must show |
|----|-----|----------|-------------------|
| `app` | The app | **product** | the domain problem, its input, the method and the value; why it is real, not a demo |
| `lanes` | Lanes, web / offline / compute | generic | what runs **live in the web** vs **offline/compute** (bake + train) vs **replay** |
| `web-flow` | Web-app flow | generic | App recomputes live; the 6 pages; contract mirror; copy-data overlay; deploy |
| `science` | The science | **product** | the real algorithm step by step, with the genuine equations |
| `design` | Data contracts / design | generic | the two contracts (ingestion + artifact) + the lane gate + cases-by-category |

## Verify before deploy

The screenshot-verify step (mandatory before any deploy) **must open the modal and confirm every tab renders its
diagram (themed, no broken SVG) + its text with no error**, in both light and dark. A product is **not "done"**
without the ⓘ Architecture modal at full depth, it is a NON-NEGOTIABLE row in the product-quality bar.
