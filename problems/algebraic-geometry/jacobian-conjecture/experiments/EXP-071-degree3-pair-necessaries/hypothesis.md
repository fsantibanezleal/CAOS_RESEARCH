# EXP-071 - Degree-3 pair necessaries (does the truncation route close again?)

- **Question.** Does any pair-support subsystem of the order-4 conditions
  obstruct a degree-3 covector?
- **Motivation (the declared derivation).** Truncations are closed through
  degree 2 (EXP-067: 8 diagonal blockers at degree 1; EXP-070: the mixed pair
  {(2,6),(5,9)} at degree 2). For degree 3 the binding conditions are order 4;
  for a support S = {i, j} they involve only the gauges over S (u, level-2 v,
  level-3 w: 9 blocks, 1485 unknowns, 5 gamma-blocks, 625 rows). Any infeasible
  subsystem closes degree 3 conclusively. All composed maps are built modulo the
  prime directly (numpy int64 matvec through the transform E), a two-prime
  confirmation on any hit; the exact setup (E, N, T_i, P_i) is Fraction-exact as
  in EXP-067/069/070.
- **Falsifiable predictions.**
  1. [MV] Setup invariants reproduce (rank 124, kernel 165, 51 ops), and the
     mod-p composed pipeline reproduces EXP-070's degree-2 decision on the known
     pair {(2,6),(5,9)} (regression gate for the new numpy path).
  2. [MV] The degree-3 pair sweep (all 1326 supports, early-abort) is decided.
     Calibrated expectation after two closures: SOME pair obstructs, closing
     degree 3 (the alternative, all-feasible, is a valid recorded outcome that
     stages triple supports).
  3. [D] On a third closure: the PATTERN-THEOREM PROPOSAL (every truncation
     degree obstructed; the polynomial-covector route closes) is drafted FOR
     FELIPE as a proposal, not a claim.
- **Method.** Exact Fraction setup; mod-p composition caches (U, Ce, W2 keyed by
  small op tuples); numpy forward elimination; primes 2147483629 / 2147483587;
  flushed prints; background with tee.
- **Success criterion.** 1-2 decided either way.
- **Failure criterion.** The regression gate (prediction 1) failing: fix before
  any claim.

Declared 2026-07-23 before the run.
