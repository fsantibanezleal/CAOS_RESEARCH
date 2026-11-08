# EXP-004 verdict: PARTIAL, no counterexample in the 17.6% of case A covered within the budget

Date: 2026-11-08. Hypothesis frozen at 61b93faf before any production computation.

## Result

- **Gate 1 PASS [MV]** (`artifacts/gates.txt`): the sharper degree-sum generator, `join6` and EXP-001's `mnh`
  filter reproduce the case-A counts of EXP-002's split at orders 10, 11 and 12: 27, 57 and 114 (the order-12 gate
  read 11,687,144 graphs in 2,901 seconds on one process).
- **Production PARTIAL [MV on the covered parts]:** the 6-hour cap on 6 processes stopped the run with 353 of the
  2,000 disjoint parts complete (17.6%), 160,312,171 graphs read (`artifacts/parts-summary.txt`; a part counts only
  when its pipeline finished). In those parts there are **43 maximal non-Hamiltonian graphs of order 13 with a
  universal vertex**, every one of circumference 12, and **every one satisfies Hoa's conjecture** (each longest
  cycle leaves a complete residual; `artifacts/mnh-n13-caseA-partial.txt`).
- **Gate 2 PASS [MV]:** EXP-001's independent `verify.py` re-checks all 43 graphs (non-Hamiltonian, every
  nonadjacent pair joined by a Hamilton path, circumference, longest-cycle sets, residual flags): 0 disagreements.

## Predictions

- Count between 180 and 320: **not decided** (only 17.6% of the parts are covered; 43 found so far).
- No counterexample to Hoa's conjecture: **holds on the covered parts**; open on the rest.

## Deviation and cost

The budget was set from the generator's speed; the MNH filter dominates (about 250 microseconds per graph at
order 12, more at 13). Measured: about 0.45 million graphs per part on average, so case A is about 9 x 10^8 graphs
and roughly 70 CPU-hours. The parts are disjoint and resumable: a follow-up with a larger budget can complete the
remaining 1,647 parts with the same pipeline (`run.sh` skips any part with a recorded `.err`).
