# EXP-009 - Characteristic-p reductions: explicit non-injective Keller maps over F_ell with degree < ell

- **Question.** Do the family counterexamples reduce, at suitable primes ell, to explicit
  non-injective Keller maps over F_ell of total degree LESS than ell?
- **Motivation.** In characteristic p the classical counterexample x - x^p has degree equal to
  p (its failure is Frobenius-linear). By standard reduction arguments (integer models,
  Connell-van den Dries), a characteristic-0 counterexample yields degree < p examples for
  almost all p; our contribution here is the EXPLICIT certificate, which the classical
  literature did not have because no characteristic-0 counterexample existed.
- **Falsifiable predictions.** For the P3 instance (seed w - 2w^3, k = 3, det = -3, total
  degree 12) and ell in {13, 101}:
  1. Every coefficient of the three components is an ell-integral rational (denominator prime
     to ell), so the reduction mod ell is well defined.
  2. det J = -3 is nonzero mod ell: the reduced map is Keller over F_ell.
  3. The EXP-004 collision points (-1/15, 18, 5130) and (1/24, -18, -10368) are ell-integral,
     DISTINCT mod ell, and their exact images are both (-54, -54, 1); hence the reduced map is
     non-injective over F_ell.
  4. Total degree 12 < 13 <= ell: the examples have degree strictly below the characteristic
     (unlike the Frobenius-based classical ones).
- **Method.** sympy exact rationals; explicit modular reduction of coefficients and points
  (a/b -> a b^{-1} mod ell); distinctness and degree checks.
- **Success criterion.** Predictions 1-4 hold for both primes.
- **Failure criterion.** A denominator collides with ell (pick another prime and document), or
  points collapse mod ell (certificate fails for that prime; document and test others).

Declared 2026-07-20 before the run.
