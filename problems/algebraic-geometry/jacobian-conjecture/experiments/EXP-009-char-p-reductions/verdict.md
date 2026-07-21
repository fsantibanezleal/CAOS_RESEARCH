# EXP-009 - Verdict: CONFIRMED (2026-07-20)

Output: `artifacts/output-2026-07-20.txt`. All predictions verified for ell = 13 and ell = 101.

## Established results (ours, exact)

The P3 instance (seed w - 2w^3, k = 3, det = -3, total degree 12) reduces mod ell = 13 and
ell = 101 to EXPLICIT non-injective Keller maps over F_ell:
- all coefficients are ell-integral (reduction well defined);
- det J = -3 is a nonzero constant mod ell (10 mod 13; 98 mod 101);
- the exact rational collision reduces to distinct points of F_ell^3 with a common image
  (mod 13: (6, 5, 8) and (6, 8, 6) both to (11, 11, 1));
- total degree 12 is STRICTLY BELOW the characteristic, unlike the classical Frobenius-based
  char-p counterexample x - x^p whose degree equals p.

## Adversarial validation record

- Exact end-to-end: images verified in characteristic 0 (equality of rationals), reductions
  computed with modular inverses, distinctness checked in F_ell^3; two independent primes.

## How could this be wrong?

- Nothing here is claimed novel-in-principle: standard reduction arguments (integer models,
  Connell-van den Dries) predicted such examples must exist once a char-0 counterexample
  exists. The contribution is the explicit certificate, which did not exist before July 2026.
- "Keller over F_ell" refers to the reduced polynomial map on affine 3-space over F_ell; no
  claim is made about lifting/reduction of the inverse-theoretic statements beyond
  non-injectivity + constant nonzero determinant.

## Consequences

- The family gives concrete low-degree char-p non-injective Keller maps at every prime not
  dividing the structure constants; a systematic "which primes fail" sweep is a cheap future
  widening if char-p structure becomes load-bearing.
