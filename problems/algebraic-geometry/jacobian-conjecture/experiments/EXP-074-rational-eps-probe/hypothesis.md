# EXP-074 - The rational-in-eps relaxation: first probe at the 8 blockers

- **Question.** Does the rational-covector form c(eps)/d(eps) escape the
  degree-1 obstructions?
- **Motivation (declared derivation).** For c(eps)^T M(eps) = d(eps) b0 with
  deg d >= 2, the order-2 diagonal conditions relax from Lambda_i M_i = 0 to
  Lambda_i M_i = s_i b0 (s_i the d-coefficient at 2e_i): ONE extra scalar
  freedom per blocked condition, which the truncation obstructions (EXP-067)
  do NOT exclude. Probe: for each of the 8 blocked operators, is
  B_i u = -(P_i M_i) + s b0 feasible in (u, s)? Any infeasible i keeps the
  block closed even rationally AT THIS ORDER; all-feasible OPENS the rational
  route and stages the full rational ladder.
- **Predictions.** 1. [MV] Setup + gate (b0 has its nonzero at the (2,0) row
  target: pairing 576). 2. [MV] The 8 relaxed single blocks decided mod two
  primes (no calibrated expectation).
- **Method.** Import EXP-072's setup (which imports EXP-071: modfrac pipeline);
  augmented feasibility [B_i | b0 | rhs] via modgauss; both primes; flushed.
- **Success.** 2 decided either way. **Failure.** Gate failing.

Declared 2026-07-23 before the run.
