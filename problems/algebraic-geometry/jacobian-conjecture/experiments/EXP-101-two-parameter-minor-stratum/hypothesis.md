# EXP-101: First two-parameter determinantal stratum in the GGHV system

## Question

What is the exact augmented-minor polynomial on the first genuine interior
cycle \((0,1),(1,7)\), and does its zero locus admit an explicit transition to
an alternative nonzero augmented minor?

## Motivation

EXP-098 proves that a useful certificate cover must include closed
specialization strata. EXP-100 compresses the first nontrivial interaction of
the selected EXP-059 minor to the two coefficient directions

\[
s=\varepsilon_{(0,1)},\qquad t=\varepsilon_{(1,7)},
\]

with exact product trace \(13/8\).

For the selected square matrix,

\[
A(s,t)=A_0+sA_s+tA_t,
\]

write

\[
B_s=A_0^{-1}A_s,\qquad B_t=A_0^{-1}A_t.
\]

The determinant can be computed without a 125 by 125 symbolic expansion.
If the combined column space of \(B_s,B_t\) has basis \(U\), write
\(B_i=UV_i\). Sylvester's determinant identity gives

\[
\frac{\det A(s,t)}{\det A_0}
=\det\left(I_r+sV_sU+tV_tU\right),
\]

where \(r\leq\operatorname{rank}B_s+\operatorname{rank}B_t\).

This is the first actual determinantal stratum calculation on the GGHV
coefficient family.

## Falsifiable predictions

1. The forced \((1,0)\) direction has exact characteristic polynomial
   \[
   \lambda^{109}(\lambda-1)^{16},
   \]
   explaining the five EXP-100 axis checks even though the matrix is not
   idempotent.
2. The combined rank \(r\) of the \((0,1),(1,7)\) perturbations is small enough
   for exact bivariate determinant computation inside the five-minute budget.
3. The reduced determinant polynomial \(f(s,t)\) is nonconstant, and its
   quadratic coefficient agrees with the trace identity implied by
   \(\operatorname{tr}(B_{(1,7)}B_{(0,1)})=13/8\).
4. A bounded rational search finds a point on \(V(f)\). At any such point, the
   full augmented matrix still has rank 125 and supplies an alternative nonzero
   minor.

Prediction 4 is two-sided: a found rank drop below 125 is an actual candidate
consistent fiber requiring immediate escalation. Failure to find a rational
point proves nothing about the algebraic zero locus and is recorded as a
bounded null.

## Premise dependencies

- EXP-059 owns the selected base augmented minor.
- EXP-099 proves that the full common-flag condition fails.
- EXP-100 identifies the first residual two-parameter cycle and records the
  exact product trace \(13/8\). Its suggested forced-axis factor remains
  unproved until prediction 1 is checked here.
- EXP-058 proves the bracket matrix has a constant-\(Q\) kernel, so augmented
  rank 125 certifies inconsistency.

## What a PASS or FAIL proves

- Predictions 1 through 3 passing give an exact equation for the first
  residual minor hypersurface and a validated low-rank method for later chart
  calculations.
- Prediction 4 passing with augmented rank 125 gives the first explicit minor
  transition on an actual GGHV coefficient slice.
- Augmented rank below 125 at a zero of the first minor does not by itself prove
  consistency; the exact rank of the bracket matrix and solvability of the
  right-hand side must then be decided.
- No finite collection of sampled points proves coverage of \(V(f)\).
  A complete slice exclusion requires an ideal/radical certificate from the
  first and alternative minors.

## Method

1. Reconstruct the EXP-099 selected matrix and normalized directions.
2. Compute and factor the exact characteristic polynomial of the forced
   direction.
3. Build a basis of the combined column space of \(B_s,B_t\).
4. Compute \(f(s,t)\) from the reduced Sylvester matrix and factor it.
5. Verify \(f\) against exact direct determinants at independent points.
6. Search a declared rational grid for zeros.
7. At the first zero, compute exact full augmented rank and extract an
   alternative nonzero augmented minor when one exists.

## Adversarial controls

- Compare the reduced formula with direct 125 by 125 determinants.
- Verify the linear and mixed quadratic coefficients independently from trace
  formulas.
- Reconstruct every selected row by label, not by changing positional index.
- Treat a missing rational zero as a null, not as nonvanishing.

## Invariant-first note

The combined perturbation rank is the cost-deciding invariant. Sylvester
reduction replaces a 125-dimensional symbolic determinant with an
\(r\)-dimensional one. The characteristic polynomial settles the forced-axis
factor before any residual interpretation.

## Compute budget and kill criterion

CPU only, exact arithmetic. Five-minute hard budget. Emit the combined rank
before symbolic determinant computation. Kill if \(r>48\) or if no progress is
emitted within 60 seconds. The rational search is limited to integer pairs
\((s,t)\in[-12,12]^2\), followed by rational-root checks on factored univariate
specializations. Budget exhaustion yields an inconclusive computational
verdict, not a mathematical one.

Declared 2026-07-26 before creating or running `run.py`.
