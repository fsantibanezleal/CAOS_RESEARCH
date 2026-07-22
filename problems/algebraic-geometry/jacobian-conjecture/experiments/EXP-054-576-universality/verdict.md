# EXP-054 - Verdict: predictions 2-3 REFUTED as declared; the closure route is the perturbative covector (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## The refutation, honestly

1. **[MV] Lambda extracted:** support entries 576 at (2,0), 24 at (9,16), 51 at
   (16,32), 612 t at (17,33), 4148 t^2 at (18,34); bare pairing 576.
2. **[MV] Universality REFUTED:** 51 of 260 lower-point x support-row combinations
   enter with nonzero bracket factors: the FIXED five-row covector is not left-null
   once lower coefficients turn on; the adversarial samples confirm (identity
   residual nonzero) even though the recomputed per-stratum pairing remains 576.
3. **The measured truth:** EXP-053's certificates were per-stratum (each recomputed
   covector pairs to the SAME constant 576): the obstruction value is stable, the
   covector is not rigid. Universality must come from a PARAMETRIZED covector
   Lambda(eps), polynomial in the lower coefficients, with Lambda(0) the five-row
   one: the certificate equation is linear in Lambda and affine in eps, so the
   construction is a perturbative nullspace solve, order by order, terminating iff
   the covector is polynomial (the 576-stability across strata is the evidence it
   is).

## Next round's first task (sharpened by the refutation)

Build Lambda(eps) perturbatively on small eps-subsets (the 51 entering monomials,
   batched), verify termination and the 576 pairing symbolically per batch; if the
   batches compose, the reduced (72,108) stratum closes universally.

## How could this be wrong?

- The per-stratum 576 could be coincidental across the tested strata (three so far
  plus two adversarial pairing checks); more strata cheap to add.
