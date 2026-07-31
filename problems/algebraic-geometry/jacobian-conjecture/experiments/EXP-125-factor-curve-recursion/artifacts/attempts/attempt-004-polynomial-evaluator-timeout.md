# Attempt 004 - repeated polynomial-construction timeout

- Exit: modular reconnaissance timeout at the declared 120-second gate.
- Symbolic work: not started.
- \(F_3/p=1013\) again passed all four rank and basis checks.
- The vectorized modular linear algebra reproduced the accepted witness basis
  and was no longer the bottleneck.
- Cause: the scan called a helper that reconstructed a SymPy `Poly` object
  for every candidate pair. The \(F_6\) search exhausted the remaining gate
  before reaching a decision.

The retry precomputes modular monomial/coefficient records once per
factor/prime and evaluates those same exact terms in the unchanged
deterministic pair order.
