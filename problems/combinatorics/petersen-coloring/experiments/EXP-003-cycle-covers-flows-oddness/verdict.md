# EXP-003 verdict - CONFIRMED ON P1-P6; oddness prediction REFUTED for the 112-vertex graphs

Date: 2026-09-03. Hypothesis committed before the run at `e1e7a3b` (the commit carrying the
EXP-002 verdict). Runner: `run.py`; raw log `artifacts/run.log`; manifest
`artifacts/manifest.json`; compact witnesses `artifacts/witnesses.json`; CNFs and proofs under
`E:/_Datos/caos-research/petersen-coloring/EXP-003/` with SHA-256 in the manifest.

## Result

| graph | 5-cycle double cover | nowhere-zero 5-flow | nowhere-zero 4-flow | oddness | resistance |
|---|---|---|---|---|---|
| `G112` | yes (witness) | yes (witness) | no (verified proof) | **4** | **3** |
| `H112` | yes (witness) | yes (witness) | no (verified proof) | **4** | **3** |
| `G52` | yes (witness) | yes (witness) | no (verified proof) | 2 | 2 |

Every value is exact: the SAT side carries a checker-validated witness (five even subgraphs
covering every edge twice; a flow with nonzero values conserving mod 5; a perfect matching
whose 2-factor has the stated number of odd cycles; a deletion set with a proper 3-edge-coloring
of the remainder), and the UNSAT side carries a drat-trim-verified proof at every lower bound
(oddness bounds 1, 2, 3 and resistance bounds 1, 2 for the 112-vertex graphs; bound 1 for
`G52`). All instances solved in under half a second.

| prediction | outcome |
|---|---|
| P1 | PASS: Petersen and `J5` have oddness 2, resistance 2, a 5-cycle double cover, a 5-flow and no 4-flow (verified); `K4` and prism have oddness 0, resistance 0 and a 4-flow |
| P2 | PASS: 5-cycle double covers on all three targets |
| P3 | PASS: 5-flows on all three; 4-flow UNSAT with verified proofs on all three |
| P4 | decided; committed expectation 2 REFUTED for `G112` and `H112` (oddness 4), right for `G52` (2) |
| P5 | decided; committed expectation 2 REFUTED for `G112` and `H112` (resistance 3), right for `G52` (2) |
| P6 | PASS: broken double cover and zeroed flow rejected |

## Reading

The 112-vertex counterexamples are "far" from 3-edge-colorable in the classical sense: oddness 4
is the largest oddness a cubic graph of cyclic connectivity 4 can have below order 44 according
to Goedgebeur-Macajova-Skoviera 2019 [U, title only; the theorem statement must be read before
this comparison enters a manuscript], while the 52-vertex graph has the minimum oddness 2 of a
snark. Both values are consistent with resistance at most oddness (a general fact [U]) and with
resistance strictly below oddness on the 112-vertex graphs.

## Exact-arithmetic status

Propositional with checked DRAT proofs on every negative; explicit witnesses on every positive.
Oddness is encoded exactly through the 2-coloring lemma (an odd cycle forces at least one
monochromatic edge; an even cycle admits zero), a derivation recorded in the encoder docstring
and tested on the Petersen graph (oddness 2 recovered) and `K4` (0).

## Adversarial validation record

Known-value controls (Petersen: oddness 2, resistance 2, no 4-flow; 3-edge-colorable graphs:
zeros and a 4-flow); corrupted witnesses rejected; bound ladders decided from both sides.

## Consequences for the strategy

PC-P3 closes: the 5-cycle double cover conjecture and Tutte's 5-flow conjecture survive on the
first counterexamples. The oddness gap between the 52-vertex graph and the 112-vertex graphs is
a new structural datum for the manuscript. Next: EXP-004 (normal 6, exact defects).

## How could this be wrong?

- A bug shared by the oddness encoder and `odd_cycles_of_two_factor` would be caught by the
  Petersen control only if it preserved the value 2 there; the K4 zero control and the explicit
  matchings (any reader can count the odd cycles by hand) reduce this risk.
- Nothing is claimed beyond these three graphs.
