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

## Reproduce odd-frame amplification and the frozen pressure candidate

EXP-003 has two separate confirmed stages. Stage A reuses the original full
certificate and verifies the exact odd-frame incidence argument. Stage B validates
the frozen ranked candidates under the declared pressure and gain conditions.
Run each stage into a fresh directory from the repository root:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/run.py --stage smoke --output-dir tmp/riemann-pressure-smoke
python problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/run.py --stage A --output-dir tmp/riemann-pressure-a
python problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/run.py --stage B --output-dir tmp/riemann-pressure-b --candidates problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/artifacts/candidates.json --smoke-receipt tmp/riemann-pressure-smoke/smoke-result.json
pytest tests/test_riemann_pressure.py tests/test_riemann_certificates.py
```

The smoke stage forces a small interrupted construction, resumes it, and checks
the replay boundary. A construction checkpoint can save work; a replay checkpoint
is a validated restart whose prior arithmetic is rechecked. No saved prefix is
trusted as a substitute for verification. Stage A has a 60-second budget. Each
Stage B candidate has a combined construction/replay budget of 600 seconds and
the fixed node cap; incomplete replay is not a certificate.

The winning rational parameters are theta=3/4, p=1/12500 and
epsilon=443239/10^9, with k=2256. The cutoff epsilon/p is derived internally.
Pressure handles the outer region; all remaining boxes must pass the exact
partition and directed interval checks. The canonical certificate has 16,797
nodes and zero unresolved boxes. Candidate 1 passed the declared gain target;
candidates 2 and 3 remain recorded as unrun after that success.

The [execution receipt](../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/artifacts/execution-receipt.json)
records the original commands, source hashes, timings and archive scope. The
floating design pass and its 16 trial outcomes are retained for provenance;
reproduction of the proved inequality uses the frozen candidates. A changed
parameter search is a new research experiment, not an overwrite of this one.

## Reproduce parity density transfer

EXP-004 has a universal mathematical proof and a separate exact arithmetic gate.
Run its frozen census in a fresh output directory:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-004-parity-density-transfer/run.py --output tmp/riemann-parity-replay
pytest tests/test_riemann_parity.py
```

The runner verifies both residual identities, multiplicity atoms, all 19,683
declared count vectors and 59,049 slack cases, rational primal/dual witnesses,
sharpness controls, and the counterexample to the false distinct half-sum.
It binds the exact hypothesis and four source premises to declaration e03413b.
The classical constant, kappa and numerical new exponent remain null. A finite
PASS is not an all-height theorem: the separate proof-review file must confirm
the universal finite argument and asymptotic transfer and match the source hashes.

The original run's stdout, full raw census, exact controls, checkpoint and timing
are retained. Fresh replay rechecks all arithmetic; a saved prefix is not trusted
as a mathematical certificate. Exact CPU arithmetic completed the declared run
in 8.0353704 seconds; GPU acceleration was unnecessary.

## Reproduce the explicit local Selberg transfer

EXP-005 localizes Pearce-Crump's optimized Selberg sign detector and combines
its explicit odd-zero curve with the EXP-004 parity inequality. Run the exact
certificate and focused adversarial tests in fresh paths:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-005-local-selberg-transfer/run.py --output-dir tmp/riemann-exp005-replay --budget-seconds 60
pytest tests/test_riemann_local_selberg.py tests/test_riemann_parity.py
```

The run checks all 14 declared controls, the source hashes, the rank-three
constant enclosure, the negative point at theta=0.5459, the positive point at
theta=0.546, the fixed legal mollifier exponent u=0.02299, and rejection of the
zero-margin boundary u=0.023. Its independent interval replay uses a separate
high-precision implementation. The canonical result SHA-256 is
`3f0ca476c0e2fe688e4e4f43fc11861d9491b3066d067e46bf88d1a441c696a5`.

The finite certificate does not establish the all-height theorem by itself.
The exporter also requires the separate analytic localization proof review and
binds its hypothesis to declaration commit `6fd59fec`. CPU arithmetic completed
the canonical run in 0.313 seconds; no GPU workload was justified.

## Reproduce Hilbert-parity compression

EXP-006 combines the first Hilbert-subspace dimension with distinct odd support.
Its canonical theorem is `(Q-S)(N-O)>=2(N-S)^2`; the exact certificate checks
the frozen threshold point and root bracket without promoting the finite census
to a universal proof.

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/run.py --output-dir tmp/riemann-exp006-replay --budget-seconds 120
pytest tests/test_riemann_hilbert_parity.py tests/test_riemann_local_selberg.py tests/test_riemann_parity.py
```

The run checks 18,479 atom profiles, equality and empty-dimension branches,
directed rational enclosures for the threshold, the scalar zero-simple witness,
and a separate 100-digit interval replay. At theta=0.5459 the strengthened lower
bound exceeds `0.0000168381638551244569880374399`, and the unique root lies in
`(0.545884,0.545885)`. The canonical result SHA-256 is
`82c4761b5c97011ff86cdd379d647ad0f94643a7eb8324a4a09aa37f58848bbf`.

The exporter requires the execution receipt and proof-review bindings for the
hypothesis, runner, focused tests, proof, audit, result and verdict. The original
declared inequality and both superseded runs remain preserved.

## Reproduce spectral-defect parity coupling

EXP-007 retains `D(G)=tr Psi(G)` in the EXP-006 product and couples it to the
pressure-frame lower bound. Its canonical theorem is
`(Q-S-D(G))(N-O)>=2(N-S)^2`. Run the exact certificate and focused tests in
fresh paths:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/run.py --output-dir tmp/riemann-exp007-replay --budget-seconds 180
python -m pytest -q tests/test_riemann_spectral_defect_parity.py
```

The run checks 652,260 rational spectral profiles, 18,479 multiplicity
profiles, a directed-rational correlated gain, source hashes, and overlap with
an independent 100-digit interval implementation. At theta=0.5459 it proves
`H-h3>1.3732525985593292701164661575215e-70`. The strict gain does not lower
the onset exponent or justify another printed decimal for the baseline bound.
The canonical result SHA-256 is
`7b254608198f0025e490c2c169603ae68637f60d6a685a63370bc062323b0bf3`.

The artifact directory preserves two failed attempts. One rejected an
incorrect containment relation between independently rounded enclosures. The
other rejected a positive-sign assumption for the historical theta=3/4
sensitivity control. Fresh replay must target an empty directory and start
from a tracked-clean commit.

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
research sections, proof stages, all released experiment records and the architecture modal.
It records viewport containment, single-row navigation, browser errors, equation rendering,
source links and screenshot hashes. It captures successive content viewports, including long
experiment records. Automated success and visual inspection are recorded separately.
Published QA records are versioned under `program/riemann-hypothesis/release-*/`.
