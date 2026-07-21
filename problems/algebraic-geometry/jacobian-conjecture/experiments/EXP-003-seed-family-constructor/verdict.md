# EXP-003 - Verdict: PARTIALLY REFUTED (v1 constructor wrong for deg p >= 3), with a sharp d=2 result (2026-07-20)

Output: `artifacts/output-2026-07-20.txt`.

## What was confirmed (prediction 1)

For seed degree 2, p = p1 w + p2 w^2, with the v1 ansatz (c1 = h(v) - t, b1 = k u h(u c1/k) + m):
polynomiality + constant det force EXACTLY the branch

  p1 = k, p2 = -3k/2, m = k^2/2, det JF = -k^3/4,

and the announced counterexample F is the k = 2 instance (components match symbolically term by
term). The normalization integral_0^1 p = 0 holds automatically on this branch (p1/2 + p2/3 = 0).
So at degree 2 the announced map is, up to the scale parameter k, THE UNIQUE map of this shape.

## What was refuted (predictions 2-4 as stated)

For d = 3 (p = w - 2w^3) and d = 4 seeds, the v1 ansatz admits NO (k, m): the polynomiality
residues are unsolvable. The v1 identification c1 = h(v) - t is a degree-2 coincidence (h is
affine exactly when deg p = 2), not the general law. Predictions 2-4 are therefore refuted FOR
THE v1 CONSTRUCTOR; the general family needs a different lift, which the failure analysis
identified (see consequences). The claimed external degree-4-fiber instance is neither confirmed
nor refuted by this run; it is retested under the corrected constructor in EXP-004.

## Adversarial validation record

- The refutation is an exact unsolvability statement (empty solution set of a polynomial system
  over QQ), not a numeric failure.
- The d=2 confirmation includes symbolic reproduction of F, an independent object-level check.

## How could this be wrong?

- solve() returning an empty set could in principle miss parametric branches; mitigated by the
  system being linear-triangular in (k, m) after expansion, and by EXP-004 exhibiting explicit
  d = 3, 4 maps under the corrected lift (showing the family exists and pinpointing exactly which
  v1 assumption failed).

## Consequences (the corrected theory, proved in EXP-004)

Working in reduced coordinates (w, s) (s = c1, w = u s / k), the correct potential form is

  V' = k^2 p(w) + m s,   T' = w V' - k^2 Phi(w),

which makes the fiber identity Phi(w) = (w V' - T')/k^2 hold BY CONSTRUCTION and gives
det d(V', T')/d(w, s) = -m^2 s, hence det JF = -m^2/k for ANY seed p and ANY polynomial
q(v) = c1 + t (the t-section), reducing the whole problem to three low-weight polynomiality
conditions at the origin. Those conditions yield: w* = alpha/k a root of Phi (the integral
condition after normalization), m = -k p(1), and a linear equation for beta = q'(0). The q-tail
beyond degree 1 is FREE, a family strictly larger than anything announced. EXP-004 verifies all
of this exactly and produces new explicit counterexamples with rational collisions.
