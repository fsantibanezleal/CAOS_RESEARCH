# EXP-030 - The perturbed weight-class theorem: lower-weight tails never rescue

- **Question.** JCB-033. Does the weight-class obstruction survive perturbation? Candidate
  THEOREM 2 (to certify step by step): let u >= 2, v >= 1, a != 0, and let R be ANY
  polynomial whose every monomial has (v, 1-u)-weight STRICTLY BELOW v. Then
  P = x + a x^u y^v + R is never a Keller component, at any partner degree.
- **Motivation (the reasoning, declared before the machine).** With w = (v, 1-u):
  L_top = J(x + a x^u y^v, .) raises w-weight by exactly u - 1, while each perturbation
  monomial of weight lam < v raises it by lam + u - v - 1 < u - 1. Consequences: (i) the
  topmost graded equation of J(P, Q) = 1 is L_top(Q^(M)) = 0 alone; (ii) L_top is banded on
  every weight class (single ray) with diagonal entries j (the y-exponent) and positive
  a-band, and a LAST-ENTRY argument (the final nonzero coefficient maps to an unmatched
  output slot with positive coefficient) makes it INJECTIVE on every class, including the
  x-power classes with a j = 0 slot; (iii) downward induction then kills every class above
  the y-class, and the constant's equation reduces EXACTLY to the pure chain, whose
  contradiction (EXP-029) is unchanged. The perturbation NEVER appears in the obstruction.
  Scope honesty: quasi-triangular components (which DO exist) have x-power or linear-base
  tops, violating u >= 2, v >= 1 for the leading monomial: the theorem is silent there, as
  it must be.
- **Falsifiable predictions.**
  1. [MV] (Shift bookkeeping) On a grid of (u, v) and perturbation monomials: w-weight
     shifts of L_top and each L_lam match the formulas; every lower-weight monomial's
     contribution to the constant's row comes from a class STRICTLY ABOVE the y-class.
  2. [MV] (Injectivity of L_top per class) For (u, v) in a grid and every weight class
     intersecting a degree window (incl. x-power classes with a j = 0 slot): the banded
     matrix of L_top restricted to the class has zero kernel (exact nullspace), with the
     last-entry mechanism visible.
  3. [MV] (End to end) For perturbed P's with random lower-weight tails (several shapes,
     unbounded-looking degrees within the window), the FULL completion window is
     inconsistent at numeric samples; the positive CONTROL x + (x+y)^2 (a genuine component,
     hypothesis violated) remains consistent: the theorem's boundary is real.
  4. [MV] (The obstruction is unchanged) Certificates over QQ(a, b) for
     P = x + a (xy)^2 + b m (m a lower-weight monomial): the pairing gcd is a PURE a-power,
     b-free: the perturbation cancels out of the obstruction exactly as the induction
     predicts.
  5. [MV] (Beyond every floor, perturbed) A perturbed instance of degree > 108 (e.g.
     x + a x^54 y^81 + b x^2 y^100, weight check first): the y-class subsystem is unchanged
     pure-chain inconsistent for all a != 0; with 1-2 the class reduction certifies no
     partner in machine-checked truncations.
- **Method.** sympy over QQ, QQ(a), QQ(a, b): class decomposition by w-weight; banded
  matrices per class; full-window linsolve; left-null pairings. Caps 570 s per part.
- **Success criterion.** 1-5 verified: THEOREM 2 recorded with its proof skeleton, each step
  machine-shadowed; honest folklore caveat carried over.
- **Failure criterion.** A kernel element on some class (the induction breaks: find what
  rescues); a consistent perturbed sample (the theorem is false as stated: characterize the
  rescuing tail and refine); a b-dependent pairing (the reduction leaks: rework).

Declared 2026-07-22 before the run.
