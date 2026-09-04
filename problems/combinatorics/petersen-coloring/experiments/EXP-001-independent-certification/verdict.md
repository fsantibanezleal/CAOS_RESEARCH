# EXP-001 verdict - CONFIRMED ON P1-P6

Date: 2026-09-03. Hypothesis committed before the run at `fa6910e`. Runner: `run.py` in this
folder; raw log `artifacts/run.log`; manifest `artifacts/manifest.json`; CNFs and DRAT proofs
under `E:/_Datos/caos-research/petersen-coloring/EXP-001/` with SHA-256 in the manifest.

## Result

Our own encodings certify that Putman's two 112-vertex graphs and the 52-vertex graph of
Goedgebeur, Jooken, Macajova, Mattiolo and Mazzuoccolo have no Petersen coloring and no normal
5-edge-coloring, with every refutation checked by drat-trim; every control is colorable with a
checker-validated witness; Putman's four public proofs verify under our checker.

| prediction | outcome | evidence |
|---|---|---|
| P1 | PASS | all three simple, cubic, connected, edge connectivity 3, girth 5; `G112` and `H112` digests match the public values; `G52` digest `27db5d3b680441cf...` recorded |
| P2 | PASS | Petersen, `K4`, prism, `J5`, `J7`: both encodings SAT, checker defect 0 in every case |
| P3 | PASS | six target instances UNSAT, six proofs verified (table below) |
| P4 | PASS | Putman's four archived proofs (archive SHA-256 `8af3eec4...`) accepted by our drat-trim against his archived CNFs in 23 to 64 s each |
| P5 | PASS | swapped identity witness rejected by the checker; removing both symmetry-breaking units leaves all three Petersen instances UNSAT with verified proofs; digest comparison rejects a mutated value |
| P6 | PASS | exhaustive search over all edge subsets of size at most 3 finds no cycle-separating cut in any target (72 s, 80 s, 5 s); explicit cycle-separating 4-cuts exhibited: `{2,6,9,12}` for both 112-vertex graphs, `{2,3,8,14}` for `G52`; cyclic edge connectivity is exactly 4 |

Target instances (CaDiCaL 1.7.3 in WSL, drat-trim; times in seconds):

| instance | vars | clauses | solve | proof bytes | check | verified |
|---|---|---|---|---|---|---|
| `G112` Petersen | 2,520 | 73,250 | 65.6 | 98,426,474 | 43.7 | yes |
| `G112` normal-5 | 2,688 | 11,088 | 1,216.8 | 786,818,036 | 900.5 | yes |
| `G112` Petersen, no symmetry breaking | 2,520 | 73,248 | 290.5 | 581,735,565 | 290.0 | yes |
| `H112` Petersen | 2,520 | 73,250 | 29.5 | 95,632,373 | 24.5 | yes |
| `H112` normal-5 | 2,688 | 11,088 | 977.2 | 868,156,862 | 1,293.5 | yes |
| `H112` Petersen, no symmetry breaking | 2,520 | 73,248 | 317.3 | 509,911,307 | 348.4 | yes |
| `G52` Petersen | 1,170 | 34,010 | 1.8 | 4,094,201 | 1.2 | yes |
| `G52` normal-5 | 1,248 | 5,148 | 178.8 | 226,490,830 | 231.8 | yes |
| `G52` Petersen, no symmetry breaking | 1,170 | 34,008 | 27.6 | 84,639,361 | 26.5 | yes |

## Exact-arithmetic status

All decisions are propositional with checked DRAT certificates; witnesses are verified by
`pcclib.checkers` from the graph alone. No floating point anywhere.

## Adversarial validation record

- Independent route: our encodings share no variables, clauses or code with Putman's (edge-image
  plus pairwise adjacency versus vertex-witness variables; side-presence plus rich indicator
  versus missing-pair variables). Both routes agree on all four public instances.
- Cross-implementation: Putman's CNF plus proof checked by our drat-trim binary (third route).
- Controls: five colorable graphs accepted with validated witnesses; corrupted witness rejected;
  symmetry-breaking removed without changing any status.

## Consequences for the strategy

The three graphs are certified counterexamples under CAOS machinery. PC-P1 closes. The
consequence audit (EXP-002 onward) may now condition on this verdict. Timing note: the normal-5
instances are the expensive ones (15 to 20 minutes with proofs near 0.8 GB); the Petersen
encoding with symmetry breaking is 20 to 40 times cheaper and is the preferred refutation route
for later gadget searches.

## How could this be wrong?

- The pairwise Petersen encoding relies on the Petersen graph being triangle-free (unit-tested)
  and on the equivalence "three pairwise-adjacent distinct edges form a star" (a one-line fact
  for triangle-free graphs). A bug common to encoder and checker cannot be excluded by the
  positive controls alone; the third route (Putman's independent encoding and proofs) closes it
  for the 112-vertex graphs, and the 52-vertex graph is covered by GJMMM's own verification.
- drat-trim is trusted as the proof checker; no second checker (for instance cake_lpr) was run.
- Nothing here says anything about graphs other than these three.
