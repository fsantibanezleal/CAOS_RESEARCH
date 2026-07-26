# EXP-102: Third chart on the residual GGHV minor curve

## Question

Does a third augmented minor cover the residual curve left by EXP-101, or reduce
it to an explicit finite set of parameter values?

## Motivation

EXP-101 proves that the first two augmented minors cover the component
\(st=8\). Their remaining common zero locus is

\[
C:\quad 2^{15}s^9=(st-8)^7.
\]

Since \(\gcd(7,9)=1\), the curve has the rational parametrization

\[
s=8u^7,\qquad
t=\frac{8u^9+1}{u^7},
\qquad u\ne0.
\]

At \(u=1\), the point is \((s,t)=(8,9)\). Both existing minors vanish there.
If the full augmented matrix still has rank 125, pivot extraction gives a third
minor nonzero at this point.

Pulling that third determinant back to the \(u\)-line turns the remaining
constructible-cover question into one exact univariate factorization.

## Falsifiable predictions

1. At \((s,t)=(8,9)\), the first and second EXP-101 minors both vanish.
2. The full matrix still satisfies
   \[
   \operatorname{rank}M=124,\qquad
   \operatorname{rank}[M\mid b]=125.
   \]
3. Pivot extraction produces a third augmented minor containing the
   right-hand-side column and nonzero at \((8,9)\).
4. The third minor polynomial can be computed exactly by a shifted low-rank
   determinant reduction and independently verified at exact points.
5. Its pullback to \(C\) is nonzero. If its numerator is a nonzero monomial,
   the three charts exclude the complete two-parameter slice. Otherwise its
   factorization gives the exact finite residual on the normalization
   parameter \(u\).

A zero pullback would refute this third chart on the entire curve. A rank drop
of the full augmented matrix below 125 at \(u=1\) would be escalated as a
candidate solvable fiber.

## Premise dependencies

- EXP-101 owns the exact first-minor factorization, the alternative second
  minor, their residual Gröbner factor, and the curve parametrization.
- EXP-058 supplies the constant-\(Q\) kernel, so augmented rank 125 with bracket
  rank at most 124 certifies inconsistency.
- The two coefficients \((0,1)\) and \((1,7)\) are used only on this declared
  slice; no inference is made about the other 49 free coefficients.

## What a PASS or FAIL proves

- A monomial pullback PASS proves exact inconsistency on the whole
  two-parameter slice.
- A nonconstant pullback PASS proves inconsistency off an explicit finite
  residual set and provides the exact points for further rank checks.
- A zero pullback closes only this third minor.
- None of these outcomes proves simultaneous coverage when the other GGHV
  coefficients vary.

## Method

1. Load the persisted EXP-101 alternative minor selection.
2. Verify both old determinants at \((8,9)\).
3. Recompute the full bracket and augmented ranks.
4. Extract a third nonzero augmented minor.
5. Compute its bivariate determinant around \((8,9)\) by Sylvester reduction.
6. Substitute the exact parametrization, cancel Laurent units in \(u\), and
   factor the numerator.
7. Verify the pullback at independent rational \(u\)-values by direct
   determinant evaluation.

## Invariant-first note

Normalization of the residual curve is the decisive invariant. It changes a
two-variable ideal-cover problem into a one-variable nonvanishing problem.
Laurent powers of \(u\) are units because \(u=0\) is not a point of \(C\).

## Compute budget and kill criterion

CPU only, exact arithmetic. Five-minute hard budget. Emit full ranks before
the third determinant and the combined perturbation rank before symbolic
reduction. Stop if the reduction does not emit progress within 60 seconds.
No root sampling can replace factorization.

Declared 2026-07-26 before creating or running `run.py`.
