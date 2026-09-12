# Reproduce the Riemann short-interval result

The [research wiki](../../problems/number-theory/riemann-hypothesis/wiki/) explains the theorem.
This guide describes the evidence flow and public replay. All arithmetic runs offline on CPU.

## Restore and verify the sources

Install the repository development requirements and the problem's pinned requirements. Run
`python problems/number-theory/riemann-hypothesis/code/restore_sources.py` from the repository
root. The manifest checks each original document's size and SHA-256. Full text remains in
the local ignored cache where redistribution rights were not identified; licensed upstream
code ZIPs are tracked with their original notices. Use `--verify-only` to check existing bytes.

## Reproduce the arithmetic

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-001-source-and-constant-audit/run.py --math-only --output-dir tmp/riemann-baseline
python problems/number-theory/riemann-hypothesis/experiments/EXP-002-short-interval-stability/run.py --output-dir tmp/riemann-replay --radius 21/4 --threshold 1/7000
pytest tests/test_riemann_baseline.py tests/test_riemann_certificates.py
```

EXP-001's math-only mode checks exact constants and symbolic identities without claiming PDF
verification. Its full mode checks the restored primary documents. EXP-002 records rational
parameters, a binary interval partition, checkpoint state, rational constant enclosures,
and a second kernel evaluator. The full canonical certificate has 48,761 nodes and no
unresolved boxes. A failed budget or any unresolved box is not a passing certificate.

The derivation and adversarial audit are separate evidence. A numerical kernel inequality
does not by itself establish a zero-proportion theorem. Both evaluators share Arb, partition
logic and a Lipschitz bound; this is not end-to-end formal verification or peer review.

## Bake and inspect the public replay

After committing the source artifacts, run `python -m researchlab.pipeline all`. The Riemann
export reads experiment bytes from Git HEAD, records source paths, experiment identifiers,
source commits, sizes and SHA-256 hashes, and writes `data/derived/research/riemann.json` plus
its manifest. It refuses absent committed evidence or unconfirmed arithmetic receipts.
The Riemann experiment dialogs also read Git HEAD, including their hypothesis, verdict and
artifact sizes; dirty, staged-only or locally deleted files cannot change the exported record.
Use a full-history clone so the source-changing commits agree with release provenance.
The exporters and experiment runners write explicit UTF-8/LF bytes on Windows and Unix.

Build the existing frontend with `npm ci` and `npm run build` in `frontend/`. On the Program
page, follow the Riemann hypothesis link in the portfolio table. The six sections cover the
statement, historical context, sources, strategy, experiments and remaining questions.
The proof-stage controls explain persisted reasoning; they perform no numerical optimization.
Experiment records open the source verdicts. The manuscript link uses the Zenodo concept DOI.

For a release, inspect every section in English and Spanish, in light and dark themes, at
desktop and phone widths. Navigate with the pointer from Program, exercise the proof controls
and experiment modal, check document viewport fit and formula rendering, then verify the
deployed build and artifact hashes. Compilation and HTTP success alone do not close this gate.

## Reproduce the rendered release matrix

Install the tested browser harness dependency in a disposable directory and start the built
frontend with `npm run preview -- --host 127.0.0.1 --port 4182` in `frontend/`. Then, from the
repository root in PowerShell:

```powershell
npm install --prefix tmp/ui-qa-tools --no-save playwright@1.61.0
node tmp/ui-qa-tools/node_modules/playwright/cli.js install chromium
$env:PLAYWRIGHT_MODULE = (Resolve-Path tmp/ui-qa-tools/node_modules/playwright).Path
node scripts/verify_riemann_ui.mjs --base-url http://127.0.0.1:4182/ --output-dir tmp/riemann-ui-review --adr-viewports --content-screenshots all
```

The harness drives real pointer navigation from Program, language/theme controls, all six
research sections, four proof stages, both experiment records and the architecture modal.
It records viewport containment, single-row navigation, browser errors, equation rendering,
source links and screenshot hashes. It captures successive content viewports, including long
experiment records. Automated success and visual inspection are recorded separately.
The published QA record is under `program/riemann-hypothesis/release-0.64.000/`.
