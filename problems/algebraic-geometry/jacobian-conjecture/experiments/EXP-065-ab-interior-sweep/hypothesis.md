# EXP-065 - The a/b interior sweep (hardening task 1b)

- **Question.** Complete hardening task 1: the interior lattice points of the a/b
  sub-polygon, each with its coefficient SYMBOLIC (one at a time), on the forced
  R^2 right edge (chart a1 = 1, a0 sampled at 2).
- **Motivation.** EXP-061 closed the a/b forced edges with interior SAMPLES only;
  the audit requires the axis-symbolic interior coverage here too (the a/b analog
  of EXP-062/063). The systems are small (25/47 lattice points): runs are fast.
- **Predictions.** 1. [MV] Every interior point admits a one-symbol certificate
  with nonzero polynomial pairing (constants/monomials expected). 2. [D] With
  EXP-063, hardening task 1 is COMPLETE on both polygon families; the simultaneous
  statement stays gated on EXP-064.
- **Method.** sympy over QQ(eps); the EXP-061 harness; background per cap.
- **Failure criterion.** A vanishing locus inside the stratum: adjudicate directly;
  escalate genuine consistency.

Declared 2026-07-22 before the run.
