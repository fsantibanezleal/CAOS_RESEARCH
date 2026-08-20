# EXP-009 verdict: CONFIRMED: the orbit-quotient route is measured and closed

Run 2026-08-20, 3 s, exact; artifact `artifacts/symmetry.json`.

## Results (tau <= 5 catalog, 12,846 polynomials, decision-complete depths)

- Reflection f(x) -> f(-x): equality of tau in 98.32% of in-catalog
  pairs (204 unequal; 667 partners fall beyond the catalog, i.e. their
  tau is 6: also unequal). Negation f -> -f: 95.15% (542 + 1,664).
- The committed counterexamples verified: tau(2x) = 1 vs tau(-2x) = 2;
  tau(x^2) = 1 vs tau(-x^2) = 2. Predictions 1-3 CONFIRMED.
- The [D] lemma |tau(sigma f) - tau(f)| <= 1 (sigma either symmetry):
  ZERO violations across the catalog: machine-corroborated.

## Design consequence (what this experiment was for)

A strict symmetry quotient of census frontiers is UNSOUND (measured, not
just argued), and the 5-13% correction sets per level make a verified
quotient complex for at most ~2x savings. TCB-005 therefore proceeds as
an OUT-OF-CORE + multiprocess engineering route (external-sort dedup of
the depth-7 frontier on E:, then a parallel last-gate scan), not a
symmetry route. The +-1 lemma still halves WITNESS-hunting work (any
record found has its mirror within one gate) and joins the wiki-04 move
inventory.
