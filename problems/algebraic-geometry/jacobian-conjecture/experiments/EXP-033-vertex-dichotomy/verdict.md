# EXP-033 - Verdict: CONFIRMED (2026-07-22). The edge fan closes: THE VERTEX DICHOTOMY

Artifact: `artifacts/output-2026-07-22.txt`.

## Established results

1. **The k = 0 edges fall [MV].** For P = x phi(y): with weights (1, 0) the operator
   preserves each x-degree class, L(x^s q) = x^s (phi q' - s phi' q) [MV symbolic]; the
   constant's class equation is phi(y) h'(y) = 1, with no polynomial solution once
   deg phi >= 1 (truncations verified inconsistent over the symbolic coefficients);
   class-s kernels are exactly (x phi)^s [MV]; full windows empty including pure-y tails;
   certificate for x(1 + c1 y): pairing gcd -c1^6, a pure power of the edge coefficient.
2. **The m = 0 edges fall [MV + one line].** For P = x phi(x): J(P, Q) = (x phi)'(x) Q_y,
   so Q_y = 1/(x phi)' is not a polynomial unless phi is constant; windows confirm.
3. **THEOREM 4 (the vertex dichotomy).** Let P be a Keller component of C^2 with linear
   part x. If the monomial x is a VERTEX of the Newton polygon N(P), then P = x + f(y)
   (triangular). Proof: any support point x^i y^j with i >= 1, (i, j) != (1, 0) makes the
   first right-boundary edge at the vertex divisible by x, hence an excluded edge shape
   (Theorem 3 for interior directions; results 1-2 for the axis directions); the only
   admissible edges at the vertex are segments to pure-y vertices (0, d), which contain no
   interior lattice points; so the support is {x} u {powers of y}. Machine-verified on all
   three sides: vertex-x-with-mixed samples all inconsistent; triangular samples
   consistent (they are components); x-swallowed samples (x + (x+y)^2, x + (x+2y)^3)
   consistent: the escape route is real and exactly where non-triangular components live.

## The strategic frame (recorded as strategy, not claimed proved)

Non-triangular components have x strictly inside N(P) (dominated support, e.g. an
(x + y)^d block). A linear gauge rotation moves the dominating direction onto a coordinate
and the vertex analysis re-applies: the germ of an induction toward the classification of
ALL components (JC(2) = the induction closes on the triangular family). The open steps:
formalize the rotation normal form, control what rotation does to the excluded shapes, and
handle ties (several dominating directions). That is JCB-036.

## How could this be wrong?

- The dichotomy's proof rests on Theorems 3 + the axis cases, all machine-shadowed; its
  polygon-combinatorics step (first-edge divisibility) is elementary and stated in full.
- The with-tails statements inherit the single [D] annihilation gap (EXP-031), shared by
  Theorems 2-4's tail machinery.
- Novelty caveat as always: triangularity criteria for Keller components exist in the
  literature (Newton-polygon corner arguments); a dedicated novelty search for the exact
  dichotomy statement is queued with JCB-031.
