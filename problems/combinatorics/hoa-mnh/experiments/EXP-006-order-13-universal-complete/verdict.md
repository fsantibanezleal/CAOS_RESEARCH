# EXP-006 verdict: PARTIAL, 82.7% of order-13 case A, 286 MNH graphs, no counterexample

Date: 2026-11-08. Hypothesis frozen at 8c8bffaf.

## Result

- **Pipeline check:** the generator rebuilt from EXP-004's committed hook reproduces 27 and 57 at orders 10 and 11.
- **Coverage [MV on the covered parts]:** with EXP-004's 353 parts kept, the 6-hour cap on 28 processes stopped the
  run with **1,653 of the 2,000 disjoint parts complete** (82.7%); 941,011,164 graphs read
  (`artifacts/parts-summary.txt`; the 347 missing parts are listed in `artifacts/missing-parts.txt`).
- **286 maximal non-Hamiltonian graphs of order 13 with a universal vertex** in the covered parts
  (`artifacts/mnh-n13-caseA-partial.txt`), with circumference 12 (265 graphs), 11 (14), 10 (4), 9 (1), 8 (1) and
  7 (1). **Every one satisfies Hoa's conjecture**: each longest cycle leaves a complete residual.
- **Gate PASS:** EXP-001's independent `verify.py` re-checks all 286 graphs with 0 disagreements.

## Predictions

- Total between 180 and 320: **not decided**, and at risk of failing: 286 are already found with 17.3% of the
  parts left.
- No counterexample to Hoa's conjecture: **holds on all 1,653 covered parts**; open on the 347 others.

## Deviation

The remaining parts took longer than EXP-004's average (parts near the middle of the order are the largest).
They are resumable with `run.sh` (a part with a recorded `.err` is kept); the parts are archived in the data root
under `caos-research/hoa-mnh/exp004-order13-caseA/`. EXP-004's `run.sh` named a generator path in the temp root;
`run.sh` here takes every path as an argument.
