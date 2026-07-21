# EXP-006 - Verdict: CONFIRMED (2026-07-20)

Output: `artifacts/output-2026-07-20.txt` (second pass; the first pass repeated EXP-005's
vacuity and diagnosed it: valuation constraints for negative exponents were never imposed, so
every nonzero-sample instantiation was non-polynomial. Fix: valuation-aware ansatz, i.e. the
coefficients of $v^i$, $i < \lceil -b/a \rceil$, are zeroed structurally.)

## Results

- The scan is now NON-vacuous: 382 branches, **216 polynomial Keller instances**, 648 in-image
  fiber checks (targets are F(x0, y0) for rational points, so empty fibers cannot fake
  injectivity).
- **Every tested fiber has exactly one preimage.** No multi-point fiber anywhere.
- Sharper than predicted: the surviving instance shapes are exactly six, and ALL are linear
  (up to the equivariant representation): (a, b1, b2, deg f, deg g) in
  {(1,-1,1,1,0), (1,1,-1,0,1), (2,-2,1,1,0), (2,1,-2,0,1), (3,-3,1,1,0), (3,1,-3,0,1)},
  i.e. maps of the form (f0 x, g1 y) and the swap variants: within the scanned window
  (a in {1,2,3}, b1 in [-3,3], deg f, deg g <= 3), a Gm-equivariant Keller map of C^2 is not
  merely injective, it is LINEAR-diagonal in the equivariant coordinates.

## Adversarial validation record

- Discards are counted, not silent: 930 branch-instantiations failed the exact ODE residual
  re-check (parametric branches whose free-parameter choices violate side constraints); 0
  non-polynomial survivors after the valuation-aware ansatz; 0 degenerate.
- Fiber counts are exact (lex Groebner eliminant degree over QQ).

## How could this be wrong?

- The window is finite (a <= 3, |b1| <= 3, degrees <= 3); the rigidity CONJECTURE (wiki 04)
  remains a conjecture beyond it, now with real supporting coverage instead of vacuity.
- Weights (1, -a) normalize gcd(w1, w2) = 1 cases only up to the chosen form; general weight
  pairs (w1, w2) with w1 > 1 are a follow-up widening.

## Consequences

- The 2D equivariant road to a counterexample is now measured, not just argued: inside the
  scanned class nothing nonlinear even EXISTS as a Keller map. This strengthens the structural
  reading (one invariant leaves no room) with data.
- Follow-up widening (general weight pairs, higher degrees) is a mechanical extension of this
  script when JC-P5 resumes.
