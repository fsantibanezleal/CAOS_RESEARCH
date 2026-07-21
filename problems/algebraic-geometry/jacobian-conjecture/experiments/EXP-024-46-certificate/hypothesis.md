# EXP-024 - The (4,6) window: from samples to a certificate

- **Question.** Upgrade EXP-023's sampled emptiness to variety-level: for h = xy, does EVERY
  P = x + P2 + P3 + a h^2 with a != 0 (all seven lower coefficients arbitrary) fail to admit a
  Keller partner of degree <= 6?
- **Motivation.** JCB-028(a). The completion system is LINEAR in Q's 25 coefficients, so
  all-parameter inconsistency is a rank statement: the reduced row echelon form of the
  augmented system over the parameter field must contain an obstruction row 0 = f(params)
  with f a NONZERO polynomial vanishing only where a = 0. If f factors as (unit) * a^k, the
  window is empty for ALL parameter values with a != 0: a theorem, not a scan.
- **Falsifiable predictions.**
  1. [MV] (Pure slice, all a) For P = x + a (xy)^2 with a symbolic: the augmented RREF over
     QQ(a) yields an obstruction polynomial f(a) = c * a^k (c != 0 rational, k >= 1): no
     completion exists for ANY a != 0 (not merely generic a).
  2. [MV -> D] (Full parameters) With all seven lower coefficients symbolic as well: an
     obstruction row exists over the 8-parameter function field and its polynomial content
     divides a power of a times a unit, certifying emptiness for every parameter choice with
     a != 0. If the fraction-field RREF exceeds the 570 s cap, the cap-out is documented
     (EXP-020 precedent) and staged variants are queued.
- **Method.** sympy: build M(params) B = rhs(params) from the coefficients of J(P,Q) - 1;
  Matrix.rref over the fraction field; collect obstruction rows (zero left block, nonzero
  right entry); factor the right entries.
- **Success criterion.** Prediction 1 exact; prediction 2 either certified or honestly capped.
- **Failure criterion.** An obstruction polynomial with a root off {a = 0} (the exclusion
  would NOT cover some special parameter locus: that locus becomes a counterexample-candidate
  stratum to probe immediately).

Declared 2026-07-21 before the run.
