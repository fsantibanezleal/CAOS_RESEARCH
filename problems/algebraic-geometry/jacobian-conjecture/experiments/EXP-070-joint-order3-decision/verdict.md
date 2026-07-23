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
