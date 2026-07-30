# EXP-117 - Exact determinant of the 51-column boundary quotient core

## Question

What is the exact quotient augmented determinant on the \(d=0\) \(T_B\)
plane after EXP-116's \(P\)-kernel removal, and what residual factors remain
for alternative 124-column charts?

## Structural input

EXP-116 normalizes the 302-by-124 quotient system at
\[
(a,b)=(0,1).
\]
With
\[
s=b-1,
\]
its exact dependency graph has nontrivial SCC sizes
\[
51,11,10,9,8,7
\]
plus sixteen one-dimensional loop blocks. The 51-block exceeded EXP-116's
declared determinant gate and was not promoted there.

The SCC decomposition makes the full selected quotient determinant the
product of the diagonal block determinants. This experiment declares the
51-block computation explicitly.

## Premise dependencies

- [MV] EXP-115 proves the global \(P\)-kernel on \(d=0\).
- [MV] EXP-116 validates the 124-column quotient, exact anchor, row basis,
  and SCC decomposition.
- [D] After a simultaneous row/column permutation into condensation order,
  the normalized matrix is block triangular, so its determinant is the
  product of SCC diagonal-block determinants.

## Predictions

1. [C] The 51-block determinant completes within five minutes.
2. [C] It has total degree substantially below 51 and at most 200 monomials.
3. [C] At least one of the nontrivial block determinants factors further
   over \(\mathbb Q[a,s]\).
4. [C] On the axis \(a=0\), the combined factorization exposes the deeper
   \(112/113\) origin stratum through a positive power of \(s+1=b\).
5. [D] The combined determinant is one at the anchor \((a,s)=(0,0)\) and
   agrees with direct exact 124-by-124 determinants at independent controls.

## Method

1. Reconstruct EXP-116's exact quotient normalization and SCCs.
2. Compute the 51-block determinant by exact domain Gaussian elimination,
   with a five-minute block budget.
3. Compute the smaller 11/10/9/8/7 and singleton block determinants.
4. Factor every block over \(\mathbb Q[a,s]\) and record degree, monomial
   count, irreducible factors, and the \(a=0\) specialization.
5. Multiply evaluations of the persisted block factors and compare them with
   five direct exact 124-by-124 determinants.

## One-sidedness

- A nonzero combined determinant proves the quotient rank gap on its
  principal open set.
- Its factor locus still requires alternative 124-column charts.
- Factorization on the two-parameter \(T_B\) boundary does not close the
  24-parameter core or the full family.

## Adversarial validation

- Recompute the SCC decomposition and require the declared sizes.
- Require every block determinant to equal one at the anchor.
- Verify five direct exact determinant evaluations, including the deeper
  origin and EXP-115's nonlinear boundary control.
- Persist the exact expressions and artifact hash.

## Compute budget and kill criterion

CPU-only. Budget 300 seconds for the 51-block and 360 seconds total. Stop
before any expanded product of all block factors. If the 51-block exceeds
the budget, persist only its elapsed partial state and do not infer a
factorization.

Declared 2026-07-29 before implementation or run.
