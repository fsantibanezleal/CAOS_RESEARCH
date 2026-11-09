# EXP-007 verdict: case A of order 13 COMPLETE, exactly 286 MNH graphs with a universal vertex, Hoa holds

Date: 2026-11-09. Hypothesis frozen at 85e0e1f6.

## Result [MV]

- The last 347 parts of order-13 case A ran in 3,846 seconds on 28 processes (EXP-006's `run.sh`, unchanged).
  With EXP-004 and EXP-006, **all 2,000 disjoint parts are complete**: 1,100,439,010 graphs H on 12 vertices read
  through the sharper degree-sum generator (`artifacts/parts-summary.txt`).
- The last 347 parts contain no MNH graph, so **exactly 286 maximal non-Hamiltonian graphs of order 13 have a
  universal vertex** (`artifacts/mnh-n13-caseA.txt`, the same 286 graphs as EXP-006's list: identical sorted files).
- **Every one satisfies Hoa's conjecture** (each longest cycle leaves a complete residual), and all 286 were
  re-checked by EXP-001's independent `verify.py` in EXP-006 with 0 disagreements.

## Predictions

- "The total exceeds 286 and stays below 400": **refuted**, the total is exactly 286 (the remaining parts held none).
- No counterexample to Hoa's conjecture: **CONFIRMED** for every MNH graph of order 13 with a universal vertex.

## What follows

The case-A counts are now 27, 57, 114 and 286 at orders 10 to 13. A185306(13) needs case B (maximum degree at most
9), which still needs an MNH-restricted generator (EXP-005 stopped). Hoa's conjecture is now settled for order 13
except case B.
