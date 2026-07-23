# EXP-070 - Verdict: DEGREE 2 CLOSED (an infeasible pair subsystem)

**Status: DECIDED. No degree-2 covector exists for the (72,108) reduced system.**

## Results (artifacts/output-2026-07-23.txt, ~24 min to the decision)

0. **[MV, PASS]** Setup invariants reproduce the chain (rank 124, kernel 165,
   51 operators); the u-composed maps (one solve deep) built exactly.
1. **[MV, DECIDED]** The pair-subsystem sweep hit an INFEASIBLE necessary
   condition at support {(2,6), (5,9)} (checked and infeasible mod BOTH primes
   2147483629 and 2147483587; for this all-integer system mod-p infeasibility is
   conclusive over Q). The subsystem (4 gamma-blocks, 500 rows, unknowns u and v
   over the support, 825 columns) admits no solution: NO degree-2 covector can
   exist. 800+ pair subsystems before it were feasible.
2. Blocker-triple stage not reached (the decision arrived earlier).

## The reading

- Degree 1 closed at 8 DIAGONAL blocks (EXP-067); degree 2 closes at a MIXED
  pair far from those blockers: the obstruction pattern moves through the
  operator lattice as the degree rises, rather than sitting at fixed operators.
- Combined standing: no degree-1 and no degree-2 covector. The truncation route
  to the simultaneous-symbolic certificate is closed through degree 2; the
  floor-raise claim remains gated, and the published Paper B scope is unchanged.
- Declared next options (for the following round): (a) the degree-3 pair
  necessaries at the same cost profile (the sweep generalizes; expectation now
  calibrated toward closure there too); (b) aim at the PATTERN: a theorem that
  EVERY truncation degree is obstructed would close this route honestly and
  redirect the certificate hunt to non-polynomial covector forms (rational in
  eps, or per-chart covers); (c) the [125,150] frontier (C13) in parallel.

## RETRACTION (2026-07-23, session 43, EXP-071)

The decision above is RETRACTED. EXP-070's modular assembly reduced rational
entries (E, N, P and their compositions) with int() TRUNCATION instead of
num * den^-1 mod p (mat_int and the rhs lines in run.py). Under the corrected
reduction (EXP-071 modfrac + overflow-safe matmul), the pair subsystem at
{(2,6),(5,9)} is FEASIBLE mod both primes: the reported infeasibility was an
artifact. The corrected full pair sweep and the EXP-069a re-audit run in
EXP-071 (run4 artifact); the true degree-2 status is recorded there. EXP-067's
degree-1 closure is UNAFFECTED (its 8 blocking singles were decided in exact
Fraction arithmetic; only mod-p reductions of rational data carried the bug).
Lesson recorded: NEVER reduce Fractions mod p with int(); always num*den^-1;
regression-gate every new arithmetic path against a known exact decision.
