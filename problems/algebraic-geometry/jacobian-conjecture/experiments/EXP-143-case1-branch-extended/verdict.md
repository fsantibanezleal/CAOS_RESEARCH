# EXP-143 verdict: UNKNOWN (both branch certificates exceed 20,000 primes)

Date: 2026-11-08. Hypothesis frozen at b7b2d655.

## Result

- The two branch runs of EXP-142 continued from their stored residues with the same method and code, first on 6
  processes each while EXP-141 finished, then on 14 each (about 7,000 primes per hour per branch).
- Every prime was lucky (no prime discarded). Final counts: 20,217 kept primes on q1 = +c and 20,134 on q1 = -c (the
  budget is checked after each batch of 1,440, so the runs overshot 20,000 by 217 and 134).
- At the last checkpoints (20,214 and 20,131 primes, moduli of about 188,000 digits) no sampled coordinate
  reconstructs, also with the common-denominator pass. In every sampled coordinate the numerator or the
  denominator has more than about 94,000 digits.

## Reading

JCB-103 by cofactor certificates now has a measured lower bound: on the branch systems the certificate coordinates
are above about 94,000 digits (EXP-141: above 28,000 on the unsplit system, with a smaller budget). The cost is
linear in the height, but the exact verification grows with it too. A useful next step must first shrink the
inputs, for example an L-valued change of the variables q0..q5 that lowers the heights of the branch equations
(small-prime scalings remove only about 10 percent, `EXP-142/structure.md`), or replace the certificate by a
smaller exact object. The residues of all runs are kept in the data root for any continuation.
