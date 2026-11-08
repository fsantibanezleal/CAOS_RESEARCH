# EXP-006 preflight: complete order 13 with a universal vertex (HMB-006, case A, continuing EXP-004)

Date: 2026-11-08. Status: frozen before the continuation. CPU only.

## Question

EXP-004 covered 353 of the 2,000 disjoint parts of case A at order 13 (G = K_1 join H, H on 12 vertices) within its
budget and found 43 maximal non-Hamiltonian graphs there. How many MNH graphs of order 13 have a universal vertex
in all, and does Hoa's conjecture hold for each?

## Method

EXP-004's pipeline unchanged: the generator with the sharper degree-sum hook (`prune_degsumA.c`, gated at orders
10 to 12 in EXP-004), `join6`, and EXP-001's `mnh` filter, over the same 2,000 disjoint parts (`res/mod`). The parts
EXP-004 completed (those with a recorded `.err`) are kept from its archive in the data root; every other part,
including the six cut mid-run, is run from scratch. EXP-001's `verify.py` re-checks every graph found.

## Predictions

- The total number of order-13 MNH graphs with a universal vertex lies between 180 and 320 (as in EXP-004)
  (MODERATE).
- None is a counterexample to Hoa's conjecture (HIGH).

## Budget

At most 6 hours of wall-clock time on 28 processes (the remaining parts are about 58 CPU-hours by EXP-004's
measurements). Otherwise PARTIAL with the coverage reached.
