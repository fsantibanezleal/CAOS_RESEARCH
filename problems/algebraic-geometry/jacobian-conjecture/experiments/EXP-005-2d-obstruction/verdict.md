# EXP-005 - Verdict: CONFIRMED WITH CAVEATS (2026-07-20)

Output: `artifacts/output-2026-07-20.txt`. Honest per-prediction accounting:

## Prediction 1 - CONFIRMED (real content)

For a Gm-action with weights (1, -a) on C^2, every equivariant polynomial map has components
P = x^{b1} f(v), Q = x^{b2} g(v) (v = x^a y), and

  det JF = x^{b1 + b2 + a - 1} (b1 f g' - b2 f' g)

identically (verified for a in {1, 2, 3} and several (b1, b2) windows with fully symbolic f, g).
Hence Keller forces b1 + b2 = 1 - a AND the one-variable ODE b1 f g' - b2 f' g = const. The whole
2D equivariant Keller problem is a single univariate ODE: there is no room for the two-invariant
potential form that generates the 3D family.

## Prediction 2 - INCONCLUSIVE (vacuous scan; follow-up queued)

The enumeration solved the Keller ODE for deg f, deg g <= 3, a in {1, 2}, b1 in [-2, 3], but the
instantiation strategy (fixing residual free coefficients to arbitrary nonzero rationals, then
re-checking the Keller residual) yielded ZERO surviving polynomial instances. A zero-instance
scan proves nothing about injectivity. The claim "all 2D equivariant Keller maps are injective"
remains OUR CONJECTURE, well-motivated by prediction 1's reduction (the ODE's polynomial
solutions appear to force fg-type primitives that give de Joncquieres-like maps), but NOT yet
certified. Follow-up EXP-006 (queued, JCB-014): enumerate solutions branch by branch keeping
free parameters symbolic through the fiber computation.

## Prediction 3 - CONFIRMED AS A PROPOSITION (the computation is illustrative only)

The intended content is a one-line proposition, recorded as such: if the reduced data (V', T')
depend on ONE variable only (no independent second invariant), then dV' and dT' are proportional,
so J2 = det d(V', T')/d(v, s) vanishes identically and det JF = -J2/c1^2 = 0: no Keller map. The
scripted check instantiates this trivially (a frozen column of the Jacobian); it certifies the
statement but the statement needs no computation. The value is the localization it provides: the
counterexample mechanism NEEDS two independent weight-0 invariants, and a nontrivial Gm-action on
C^2 has only one; therefore THIS mechanism cannot refute JC(2), for structural (not accidental)
reasons.

## Prediction 4 - CONFIRMED (real scan)

No 2x2 coordinate slice of the announced F (each of x, y, z frozen at 3 rational values, every
output pair) has constant nonzero Jacobian: the counterexample does not hide a 2D Keller map in
any slice.

## Adversarial validation record

- Prediction 1 is a symbolic identity with free coefficients (the strongest route available).
- The self-refutation of prediction 2's scan (reporting 0 instances instead of claiming success)
  is itself the adversarial posture the methodology requires.

## How could this be wrong?

- Non-equivariant 2D Keller maps are untouched by all of this: the obstruction localizes the
  MECHANISM, it does not bear on JC(2) in general.
- Prediction 4's scan covers coordinate slices at finitely many values; non-coordinate
  (composed) slices are not excluded.

## Consequences

- The honest 2D picture: the road to a 2D counterexample, if one exists, must abandon weighted
  Gm-equivariance entirely (one invariant is not enough), or use a non-reductive symmetry
  (unipotent flows: additive group actions have polynomial invariant RINGS in 2D with one
  generator as well), or no symmetry at all. Candidate novel directions logged in JCB-012.
- EXP-006 (proper branch-symbolic enumeration) is the immediate next experiment.
