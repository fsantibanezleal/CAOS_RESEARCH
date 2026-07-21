# EXP-008 - Degree laws and family-internal minimality

- **Question.** What are the exact component-degree laws of the seed family, is the announced F
  degree-minimal WITHIN the family, and does the family extend to fiber degree 6 with a fully
  verified new instance?
- **Motivation.** JC-P3 (minimality axis). Observed pattern from EXP-004 instances (affine q):
  degrees (5d-3, 5d-4, 4) for seed degree d. If the law holds and degrees are monotone in both
  d and the q-tail, then (7, 6, 4) is minimal within the family class, and the fiber-degree
  floor is 3.
- **Falsifiable predictions.**
  1. (Fiber floor) Seed degree 1 is impossible: p = p1 w with integral_0^1 p = 0 forces p = 0.
     The constructor rejects it (assertion), i.e. fiber degree >= 3 in the family.
  2. (Degree law, affine q) For d = 2, 3, 4, 5 the component total degrees are exactly
     (5d - 3, 5d - 4, 4).
  3. (d = 5 instance, new) Seed p = w - 3w^5 (integral = 1/2 - 1/2 = 0, p(1) = -2,
     p'(1) = -14, p'(1) - 2p(1) = -10 != 0), k = 5: a Keller map with det = -20, degrees
     (22, 21, 4), generic fiber degree 6, exact reconstruction, and an explicit rational
     collision. (A previously unpublished counterexample instance, like P3/P4/P5.)
  4. (q-tail monotonicity) Adding tails v^2 and v^3 to the d = 2 seed strictly increases the
     component degrees rowwise (checked exactly), so tails never beat the affine-q minimum.
  5. (Minimality within the family) Consequently min over the family of the degree vector is
     attained at d = 2, q affine: (7, 6, 4), the announced map (up to the scale k, which does
     not change degrees; verified at k = 7).
- **Method.** sympy over QQ; constructor v2; degrees via Poly total_degree; the d = 5 instance
  gets the full EXP-004 verification pipeline (polynomiality, det, fiber degree + squarefree,
  reconstruction mod fiber polynomial, engineered collision).
- **Success criterion.** Predictions 1-5 verified exactly.
- **Failure criterion.** Any fails (e.g. the degree law breaks at d = 5): the law is then
  corrected in the verdict with the observed data.
- **Scope note (declared).** This is minimality WITHIN the constructor-v2 class. Global
  minimality (is there ANY C^3 counterexample of total degree < 7?) is untouched; Wang's
  degree-2 theorem is the only general floor we can cite, so degrees 3..6 remain open there.

Declared 2026-07-20 before the run.
