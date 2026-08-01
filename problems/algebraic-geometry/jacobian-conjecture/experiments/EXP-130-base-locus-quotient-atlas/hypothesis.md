# EXP-130 - Exact quotient-algebra atlas on the finite base locus

## Question

Does the finite EXP-123 base locus

\[
V(R,S)\cap D(X),\qquad X=A^3,
\]

survive after separating \(A=0\), and if it does, can a finite collection of
exact maximal-minor sections generate the unit ideal on its complete coordinate
algebra?

## Why this is the strongest next path

EXP-129 closes every point on the rational graph over \(AS\ne0\). The only
remaining boundaries of the declared four-parameter restriction are the finite
base locus and \(A=0\). Since \(R\) and \(S\) are coprime and have degrees 5 and
4 in \(X\), the base locus is the smallest remaining exact target. Treating it
as a finite algebra preserves conjugacy and multiplicity and avoids solving for
individual algebraic points.

## Premise dependencies

1. EXP-123 exactly reconstructs \(R\) and \(S\), proves \(\gcd(R,S)=1\), and
   records the formula \(A^{87}(R+A^2CS)\).
2. EXP-111 proves that the effective complete system is the 302-by-125
   augmented matrix obtained after removing the structural constant column.
3. EXP-129 proves that the complete \(AS\ne0\) rational graph is covered by a
   finite maximal-minor atlas.
4. The claim that saturation by \(X\) exactly separates the \(A=0\) boundary is
   a hypothesis of this experiment and will be checked by contraction and
   direct specialization.

## Pre-run predictions

1. The cleared integer forms of \(R,S\) define a zero-dimensional affine
   scheme, and independent resultant and Groebner computations agree on its
   projection and quotient dimension.
2. Saturation by \(X\) removes exactly the components supported at \(X=0\),
   leaving either the empty scheme or a finite principal-open algebra.
3. If the principal-open algebra is nonzero, modular probes at two admissible
   primes have augmented rank 125 at every represented block.
4. A deterministic greedy search returns a finite row-basis atlas whose exact
   reconstructed section classes generate the unit ideal in the saturated
   quotient algebra.
5. The unit-ideal conclusion is reproduced independently by multiplication
   matrices and a Groebner normal-form certificate.

Predictions 1 and 2 are the invariant-first gate. Predictions 3 through 5 run
only if the saturated algebra is nonzero.

## What PASS and FAIL prove

- A PASS at predictions 1 and 2 gives an exact scheme-theoretic description of
  the base locus and its separation from \(A=0\).
- A full PASS through prediction 5 closes the complete finite base locus of the
  declared four-parameter restriction.
- A rank defect in prediction 3 proves that the selected-minor route cannot
  cover that block and exposes a genuine residual rank stratum for a new
  experiment. It does not produce a Jacobian counterexample.
- Failure to find a small atlas is only a search null. It does not prove that
  the maximal-minor ideal is nonunit.
- A compute-budget stop is inconclusive and preserves the last exact
  checkpoint.

## Method

1. Hash-check the accepted EXP-123 and EXP-129 artifacts and reload \(R,S\).
2. Clear contents and denominators, then compute exact Groebner bases in both
   variable orders and the two projection resultants.
3. Saturate by \(X\) using an auxiliary inverse equation \(TX-1\). Construct a
   monomial basis and multiplication matrices for the finite quotient algebra.
4. Verify zero-dimensionality, quotient dimension, commuting multiplication
   matrices, and agreement between their characteristic polynomials and the
   squarefree projection data.
5. If nonempty, realize finite-field probes at two admissible primes and select
   full-rank row bases using the complete 302-row system.
6. Reconstruct accepted determinants by the validated SCC/block method, reduce
   their section classes in the quotient algebra, and test whether their ideal
   contains 1.
7. Recompute the unit test through multiplication determinants or linear
   combination matrices as an independent exact route.

## Invariant-first note

The cheapest decisive invariant is whether the saturated quotient algebra is
zero. Next are its vector-space dimension and the determinant of multiplication
by a section. Root finding, numerical continuation, and ambient parameter
elimination are unnecessary unless those invariants fail to decide the case.

## Compute budget and kill criteria

- CPU only, exact rational/integer arithmetic for every verdict-bearing claim.
- Each Groebner or resultant worker has a 300-second timeout and writes its
  result before the next stage.
- Modular row selection has a 180-second total gate.
- Each exact determinant reconstruction has a 300-second gate and is accepted
  only when its largest SCC is at most 60.
- The total initial run gate is 20 minutes. A hit at any gate is recorded as
  inconclusive for that stage; no characteristic-zero conclusion is inferred
  from modular evidence alone.

## Redirect rules

- If saturation is empty, stop: the principal-open base locus is closed and
  EXP-131 moves directly to \(A=0\).
- If the scheme is nonreduced, retain its full local algebra; do not replace it
  silently by its radical.
- If modular ranks drop, isolate the affected primary block as the next exact
  rank-stratum experiment.
- If a single section is not a unit, accumulate a minimal atlas and test the
  generated ideal rather than forcing one determinant.
- If exact reconstruction exceeds its gate, persist modular selection only as
  reconnaissance and declare a narrower follow-up.

## Scope

Even a full PASS concerns only \(V(R,S)\cap D(X)\) in the declared
four-parameter restriction. The \(A=0\) boundary, the remaining core
directions, the complete 51-parameter family, \((72,108)\), the planar degree
floor, and JC(2) remain open.

