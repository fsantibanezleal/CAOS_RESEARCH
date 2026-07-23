# EXP-070 - The joint order-3 decision, staged by support (degree-2 stage b)

- **Question.** Decide (or bound) the existence of a degree-2 covector via the
  strongest support-restricted necessary conditions of the joint order-3 system.
- **Motivation (the declared derivation).** After EXP-069a, degree 2 survives all
  diagonal-triple necessaries. The full joint system (23426 triples x 125 rows,
  gauge unknowns u 8415 + v 218790) is beyond a naive pure-Python elimination,
  BUT every SUPPORT-RESTRICTED subsystem is a genuine necessary condition: for a
  support set S, the conditions with gamma supported in S involve ONLY the gauge
  unknowns indexed by S (u_i, v_ab for i, a, b in S). Any infeasible subsystem
  closes degree 2 conclusively.
- **Falsifiable predictions.**
  1. [MV] PAIR subsystems: for every pair {i, j} (all 1275), the 4-gamma system
     (500 rows x 825 unknowns) is decided mod p via dense modular elimination
     (numpy int64). Declared expectation from the stage-a surprise: all feasible.
  2. [MV] BLOCKER-TRIPLE subsystems: for every triple with at least two
     coordinates among the 8 degree-1 blockers (about 1.4k supports; 1250 rows x
     1485 unknowns each), decided mod p. Either outcome recorded; any
     infeasibility CLOSES DEGREE 2.
  3. [D] If 1-2 pass everywhere: the full joint elimination remains OPEN and is
     staged with proper GF(p) tooling; degree 2 is NOT decided this round and
     the record says so explicitly.
- **Method.** Exact Fraction setup identical to EXP-067/069 (hull/bracket/GJ/
  kernel/P/B); subsystem assembly mod 2147483629 (spot re-checks of any
  infeasibility at 2147483587); numpy int64 forward elimination; flushed
  progress; background with tee.
- **Success criterion.** Predictions 1-2 decided; 3 recorded honestly.
- **Failure criterion.** Setup invariants failing (rank 124 / kernel 165 / 51
  ops), or numpy overflow (guarded: p^2 < 2^63).

Declared 2026-07-23 before the run.
