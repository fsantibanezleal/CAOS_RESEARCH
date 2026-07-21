# EXP-010 - 2D equivariant rigidity for arbitrary weights: from conjecture to theorem

- **Question.** Does the 2D equivariant rigidity conjecture (wiki 04) hold for ALL weight pairs
  and ALL degrees, not just the EXP-006 window? Candidate proof found during design (to be
  machine-certified here): a classification argument with a leading-coefficient kill.
- **Motivation.** JC-P5. EXP-006 found only LINEAR instances empirically. The design analysis
  suggests this is a theorem: for the Gm-action with weights (w1, -w2), w1, w2 >= 1 coprime,
  every equivariant polynomial component of weight beta is a monomial times a polynomial in the
  invariant v = x^{w2} y^{w1}, and the Keller condition collapses to positivity-rigid data.
- **The derivation to certify.** For P = x^{i1} y^{j1} f(v), Q = x^{i2} y^{j2} g(v):
  det JF = x^{i1+i2-1} y^{j1+j2-1} [ (i1 j2 - i2 j1) f g + v (beta1 f g' - beta2 f' g) ],
  with beta_r = w1 i_r - w2 j_r. Keller (det = const != 0) then forces:
  (a) i1 + i2 = 1 and j1 + j2 = 1 (else the monomial prefactor cannot be cancelled);
  (b) the shapes with i1 j2 - i2 j1 = 0 (P = xy f, Q = g and its swap) are impossible
      (the bracket is divisible by v, the constant is not);
  (c) the surviving shapes (P = x f, Q = y g and the swap) reduce to the univariate ODE
      f g + v (w1 f g' + w2 f' g) = c (respectively its sign-swapped variant), whose
      v^N-coefficient at the top degree N = deg f + deg g is (1 + w1 deg g + w2 deg f) f_top
      g_top with a STRICTLY POSITIVE integer factor: the top coefficients die, and by descent
      f and g are constants.
  Conclusion: every such equivariant Keller map is (f0 x, g0 y) or (f0 y, g0 x): linear.
- **Falsifiable predictions.**
  1. [MV] The determinant identity holds symbolically for a sweep of weights
     (w1, w2) in {(1,1), (2,1), (3,1), (3,2), (5,2), (5,3), (4,3), (1,0)} and monomial
     exponents i, j in [0, 3], with generic symbolic f, g.
  2. [MV] For the excluded shapes (b), the coefficient system bracket = c has NO solution with
     c != 0 (empty solve), for the weight sweep.
  3. [MV] For the surviving shapes, solving the ODE symbolically for deg f, deg g <= 5 over the
     weight sweep yields ONLY constant (f, g) branches.
  4. [MV] The top-coefficient factor (1 + w1 dg + w2 df) is nonzero for every
     (w1, w2, df, dg) in the sweep ranges (integer positivity spot-check of the kill step).
- **Method.** sympy over QQ; symbolic identity checks; exhaustive solve over the sweeps; the
  arbitrary-degree/weight statement is then a derived theorem [D] whose every mechanical step
  is certified [MV] on sweeps, with the induction written out in the verdict and wiki.
- **Success criterion.** Predictions 1-4 verified; the conjecture upgrades to a theorem for the
  equivariant class (all weights w1, w2 >= 1 and the semi-trivial (1, 0) case).
- **Failure criterion.** Any prediction fails; in particular a nonconstant ODE solution would
  refute the classification (and revive a 2D construction route; escalate immediately).

Declared 2026-07-21 before the run.
