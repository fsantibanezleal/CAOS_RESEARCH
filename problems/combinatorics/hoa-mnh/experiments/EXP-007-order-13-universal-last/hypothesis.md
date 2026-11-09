# EXP-007 preflight: the last 347 parts of order-13 case A (HMB-006)

Date: 2026-11-08. Status: frozen before the continuation. CPU only.

## Question

EXP-004 and EXP-006 completed 1,653 of the 2,000 disjoint parts of case A at order 13 (G = K_1 join H, H on 12
vertices) and found 286 maximal non-Hamiltonian graphs, all satisfying Hoa's conjecture. Complete the remaining 347
parts (listed in EXP-006 `artifacts/missing-parts.txt`): how many MNH graphs of order 13 have a universal vertex in
all, and does Hoa's conjecture hold for every one?

## Method

EXP-006's `run.sh` unchanged, from the parts archived in the data root (a part with a recorded `.err` is kept);
EXP-001's `verify.py` re-checks every graph found.

## Predictions

- The total exceeds 286 and stays below 400 (MODERATE).
- No counterexample to Hoa's conjecture (HIGH).

## Budget

At most 6 hours of wall-clock time on 28 processes. Otherwise PARTIAL with the coverage reached.
