# EXP-057 - Verdict: prediction 1 REFUTED; THE ONE-DIMENSIONAL KERNEL discovered (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt` (the part-2 crash is downstream of the
refuted prediction: pivots yield 124 rows, the coded 125-row minor cannot exist).

## The refutation and the discovery

1. **[MV] Prediction 1 REFUTED:** rank(M0) = 124, not 125, at every sampled t
   (1, 2, -3, 5/7): the right kernel is ONE-DIMENSIONAL. All-orders solvability is
   NOT automatic.
2. **The discovery this forces:** there exists a single kernel object k(t) (a
   Q-polynomial on the reduced polygon with [P0, k] vanishing on the whole row
   pool), and the ladder's perfect record (276/276, EXP-055/056) means every rung
   rhs so far has annihilated k. Via the identity rhs . k = -Lambda_prev([m, k]),
   the all-orders solvability lemma is now CONCRETE: prove
   Lambda_prev([m, k]) = 0 for every perturbing monomial m and every ladder
   covector: the exact Jacobi/Leibniz annihilation pattern (EXP-036) with an
   explicit target.

## Next round's first task (sharp)

(a) Compute k(t) explicitly (one nullspace vector over QQ(t)); (b) identify its
closed form (candidate: a truncation of a bracket-commuting object built from P0);
(c) prove the annihilation condition structurally; (d) revisit termination with k in
hand (the kernel direction is also the only obstruction to rhs-freedom, so the two
lemmas may merge).

## How could this be wrong?

- Ranks sampled at four t values (generic behavior); the kernel dimension could jump
  at special t (checked when k(t) is computed).
- The pool restriction defines M0; k is a POOL kernel object (its bracket vanishes
  on pool rows), which is exactly what the ladder needs, but the closed-form
  identification should note the distinction.
