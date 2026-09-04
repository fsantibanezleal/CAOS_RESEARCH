# EXP-002 verdict - CONFIRMED ON P1-P5; committed index prediction right

Date: 2026-09-03. Hypothesis committed before the run at `4ea64f5` (the commit carrying EXP-001's
verdict). Runner: `run.py`; raw log `artifacts/run.log`; manifest `artifacts/manifest.json`;
compact witnesses `artifacts/witnesses.json`; CNFs and proofs under
`E:/_Datos/caos-research/petersen-coloring/EXP-002/` with SHA-256 in the manifest.

## Result

All three certified counterexamples admit a Berge-Fulkerson cover, a Berge cover by five perfect
matchings, three perfect matchings with empty intersection, and a cover by FOUR perfect
matchings. Their perfect matching index is therefore exactly 4 (index 3 is excluded because they
are not 3-edge-colorable). Every witness is decoded from the model and re-verified from the graph
alone.

| prediction | outcome | evidence |
|---|---|---|
| P1 | PASS | Petersen graph: Berge-Fulkerson SAT, Berge-5 SAT, Berge-4 UNSAT with verified DRAT (index 5, the classical value), Fan-Raspaud SAT; `K4`, prism: everything SAT including Berge-3; `J5`: Berge-Fulkerson and Fan-Raspaud SAT, Berge-4 SAT |
| P2 | PASS | `G112`, `H112`, `G52`: Berge-Fulkerson SAT (1,008 / 1,008 / 468 variables; 7,058 / 7,058 / 3,278 clauses; each under 0.3 s), checker `check_berge_fulkerson` true |
| P3 | PASS | Berge-5 and Fan-Raspaud SAT with validated witnesses on all three (also implied by P2) |
| P4 | PASS, committed expectation 4 confirmed | Berge-4 SAT with validated witnesses on all three: perfect matching index 4 for `G112`, `H112`, `G52` |
| P5 | PASS (attempt 2) | order-swapped Berge-Fulkerson witness accepted, single-edge-moved witness rejected |

## Instrumentation incident (preserved)

Attempt 1 (`artifacts/run-attempt1-control-bug.log`, `manifest-attempt1-control-bug.json`)
reported "P5 corrupted witness handling" while every target and control instance was already
identical to attempt 2. The cause was in the CONTROL code, not in the verifier: the corrupted
witness was built by removing an edge from a matching and adding the smallest edge index absent
from it, which could be the removed edge itself, reproducing the valid witness. The control now
excludes the removed edge. No target result changed between attempts.

## Exact-arithmetic status

Propositional; witnesses explicit (the six matchings of each Berge-Fulkerson cover, the four
matchings of each index-4 cover, in `witnesses.json`); the one UNSAT (Petersen Berge-4) carries a
verified DRAT proof.

## Adversarial validation record

- Positive controls with known answers (Petersen index 5 recovered; 3-edge-colorable graphs
  covered by three matchings).
- Checkers read only the graph and the decoded matchings.
- Corrupted witnesses rejected (attempt 2).

## Consequences for the strategy

The first counterexamples to the Petersen coloring conjecture satisfy the Berge-Fulkerson,
Berge and Fan-Raspaud conjectures, with perfect matching index 4, one below the Petersen graph's
own value. PC-P2 closes. Next: cycle double covers, flows, oddness and resistance (EXP-003).

## How could this be wrong?

- A shared bug between the matching encoder and `is_perfect_matching` is excluded by the
  Petersen index-5 control (the encoder must fail there and does) and by the explicit witness
  lists, which any reader can re-check by hand.
- Nothing is claimed about any other graph; in particular nothing here bears on the
  Berge-Fulkerson conjecture in general.
