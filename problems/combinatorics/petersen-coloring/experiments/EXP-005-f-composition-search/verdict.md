# EXP-005 verdict - INCONCLUSIVE on the question; two classes exhausted, the pure-F proposition, and a measured non-convergence

Date: 2026-09-03. Hypothesis committed before the run at `817afdb`. Runner: `run.py`
(targets with `--skip-controls --classes "5,0;6,0;5,2;6,2" --budget 7200`, log
`artifacts/run-targets.log`); the tooling smoke (`(2,0)`, `(3,2)` at a 15-minute budget) ran
from a scratch script before the declaration's controls could be scheduled and is recorded in
`E:/_Temp/pcc-smoke5/` ledgers. Manifest `artifacts/manifest.json`; learned-clause ledgers with
witnesses under `E:/_Datos/caos-research/petersen-coloring/EXP-005/` (`k5m0.jsonl`,
`k6m0.jsonl`, `k5m2.jsonl` 2.36 MB, `k6m2.jsonl` 2.35 MB).

## Result

| class | n | status | iterations | learned clauses | seconds | counterexamples |
|---|---|---|---|---|---|---|
| `(2,0)` (smoke) | 16 | exhausted by a universal coloring | 2 | 1 | seconds | 0 |
| `(3,2)` (smoke control) | 26 | budget (15 min) | 1,059 | 29,052 | 900 | 0 |
| `(5,0)` | 40 | exhausted by a universal coloring | 15 | 14 | 3.2 | 0 |
| `(6,0)` | 48 | exhausted by a universal coloring | 27 | 26 | 5.5 | 0 |
| `(5,2)` | 42 | budget (2 h) | 1,992 | 80,832 | 7,206 | 0 |
| `(6,2)` | 50 | budget (2 h) | 1,498 | 75,286 | 7,207 | 0 |

Predictions:

| prediction | outcome |
|---|---|
| P1 (controls `(2,0)`, `(3,2)`, `(4,4)` exhaust) | PARTIAL: `(2,0)` exhausts; `(3,2)` hit its budget; `(4,4)` was not run (the target classes were prioritized after the `(3,2)` measurement showed non-convergence) |
| P2 (`G52` has six disjoint copies of `F`; `(6,4)` finds a counterexample) | first half PASS by exhaustive packing (six copies, four free vertices; the 112-vertex graphs have twelve copies and sixteen free vertices); the `(6,4)` positive control was not run for the same reason |
| P3 (no counterexample below 52 in the listed classes) | UNDECIDED: `(5,0)`, `(6,0)` exhausted with none; `(5,2)`, `(6,2)` budget-stopped with none found and not exhausted; the remaining listed classes were not started |
| P4 (every learned clause's witness re-verifies) | PASS: every coloring witness was checked against the exact P-coloring set of `F` (315 boundary tuples) and the star sets before its clause was added (assertion in the loop; no failure) |

## What was established

- Proposition (derived, machine-witnessed): every composition of copies of `F` without free
  vertices is Petersen colorable, because `F` has a coloring with all four boundary labels equal
  (`context/2026-09-03-pure-f-compositions.md`). `(5,0)` and `(6,0)` are its instances.
- The counterexample-guided loop is sound (P4) but does not converge at 26 or more semi-edges:
  each coloring clause removes only the matchings whose joined pairs are equal under that
  coloring, and the equality patterns are too numerous. This is a measured tooling fact, not a
  statement about the classes.

## Exact-arithmetic status

Propositional; universal-coloring exhaustion is a witness re-verified against `PCOL_F` and the
star sets; the join formulas' final UNSAT was never reached for the budget-stopped classes, so
no exhaustion proof exists for them.

## Consequences for the strategy

The question of counterexamples below 52 vertices inside `C(5,2)`, `C(6,2)` and the larger
classes stays open. The declared next step (research lines PCR-4b) is a symmetry-broken
enumeration of matchings with lex-leader constraints for the generators of the join-formula
symmetry group, or a QBF formulation (PCR-4c). The tooling (encoders, checkers, `P-Col` set of
`F`, composition builder) is in place.

## How could this be wrong?

- Nothing negative is claimed for the unexhausted classes; a counterexample may exist there.
- The universal-coloring exhaustion relies on `F` admitting an all-equal boundary coloring; the
  witness is recorded and re-verified, and the argument is the proposition's one-line proof.
