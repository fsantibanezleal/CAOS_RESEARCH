# EXP-009: symmetry audit of the census (does the orbit-quotient route exist?)

Declared 2026-08-20, before the run. Decides the design premise of the
TCB-005 depth-8 route: can frontiers be quotiented by the reflection
$f(x) \mapsto f(-x)$ or negation $f \mapsto -f$ without losing exactness?

## Pre-analysis (committed; the run tests it)

- [D] $|\tau(f(-x)) - \tau(f)| \le 1$ and $|\tau(-f) - \tau(f)| \le 1$:
  prepend $u = (-1) \cdot x$ (resp. append one multiplication).
- [D] Equality FAILS in general for both: $\tau(2x) = 1$ but
  $-2x$ is not among the nine depth-1 polynomials, so $\tau(-2x) = 2$;
  likewise $\tau(x^2) = 1$, $\tau(-x^2) = 2$. Hence a strict orbit
  quotient of the census is UNSOUND: the route, as a pure symmetry, is
  dead, and this experiment MEASURES how often equality holds (a
  near-100% rate would still permit a verified-per-level quotient with
  a correction list; a low rate kills the idea entirely).

## Questions and predictions

1. Over the full $\tau \le 5$ catalog (12,846 polynomials, exact
   depths): the fraction with $\tau(f(-x)) = \tau(f)$. PREDICTION:
   $\ge 90\%$ [C]. The counterexample census (list of all unequal
   pairs) is retained.
2. Same for negation. PREDICTION: lower than reflection (products are
   sign-rigid).
3. Verify the two committed counterexamples appear in the data.

## Budget

Single run, seconds to ~1 min (depth-5 catalog build is ~10 s); no kill
criterion needed beyond the standard timeout.
