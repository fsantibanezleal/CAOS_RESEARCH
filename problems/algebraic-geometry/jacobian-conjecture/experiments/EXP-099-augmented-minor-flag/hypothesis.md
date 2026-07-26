# EXP-099: Common-flag gate for the augmented GGHV minor

## Question

Does the 125 by 125 augmented minor selected in EXP-059 remain identically
nonzero over its full 26-parameter lower-coefficient family because its
normalized perturbation matrices preserve a common strict flag?

## Motivation

EXP-059 found a nonzero augmented minor at the base point, verified it
symbolically on several axes, and observed the same value at 40 mixed samples.
It did not prove simultaneous constancy. EXP-098 shows that a nonconstant
generic certificate should be followed by residual closed-stratum analysis,
but the cheapest first gate is to ask whether this particular minor is
structurally constant.

Write the selected square submatrix as

\[
A(\varepsilon)=A_0+\sum_{i=1}^{26}\varepsilon_i A_i.
\]

Since \(A_0\) is invertible,

\[
\det A(\varepsilon)
=\det A_0\det\left(I+\sum_i\varepsilon_i B_i\right),
\qquad
B_i=A_0^{-1}A_i.
\]

If all \(B_i\) are strictly triangular in one common ordered basis, every
linear combination is nilpotent and

\[
\det A(\varepsilon)=\det A_0
\]

identically, without multivariate determinant expansion.

The existence of a common strict flag is decided by the directed union-support
graph of the \(B_i\): an acyclic graph gives a topological ordering that makes
every \(B_i\) strictly triangular.

## Falsifiable predictions

1. The EXP-059 row and column selection reconstructs deterministically, includes
   the right-hand-side column, and gives an invertible \(A_0\).
2. The union-support graph of the 26 exact matrices \(B_i\) is acyclic.
3. Independent exact substitutions at adversarial mixed parameter values give
   the same determinant as \(A_0\).
4. Consequently, the reduced equation is inconsistent for every simultaneous
   value of these 26 declared parameters, because the augmented rank is at
   least 125 while the bracket matrix rank is at most 124 due to the constant
   \(Q\)-kernel.

If prediction 2 fails, record the shortest directed cycle available from a
breadth-first search and evaluate exact low-order trace invariants along that
cycle. That failure does not imply the determinant is nonconstant; it refutes
only this common-flag proof.

## Premise dependencies

- EXP-052 owns the reduced polygons and the 125 \(Q\)-coefficient columns.
- EXP-058 proves the base bracket matrix has rank 124 and identifies the
  constant \(Q\)-direction in the kernel.
- EXP-059 owns the augmented-minor selection and its sampled/axis evidence.
  This experiment reconstructs the selection rather than importing serialized
  matrix data.
- EXP-098 proves that nonconstant certificate factors can be handled by
  recursive constructible strata. It does not predict that a common flag must
  exist.

## What a PASS or FAIL proves

- A PASS proves exact simultaneous inconsistency on the declared
  26-parameter EXP-059 subfamily. It does not cover the remaining GGHV
  parameters or all forced branches.
- A FAIL closes only the common-strict-flag proof. It identifies the earliest
  cyclic interaction and redirects the same minor to trace, determinant, or
  constructible-stratum analysis.
- Neither outcome alone excludes the complete \((72,108)\) case or proves
  \(JC(2)\).

## Method

Use exact SymPy rational matrices:

1. reconstruct the EXP-059 matrix and deterministic submatrix selection;
2. compute \(A_0^{-1}A_i\) exactly for all 26 parameter directions;
3. build the union-support directed graph and run a topological-sort gate;
4. if acyclic, verify strict triangularity in the recovered order;
5. independently evaluate the selected determinant at fixed adversarial mixed
   points.

Persist the order, graph counts, matrix hashes, determinant checks, and any
cycle witness.

## Invariant-first note

The common strict flag is a sufficient invariant for multivariate determinant
constancy. It costs one exact inverse and sparse graph analysis, and can replace
an exponentially large coefficient expansion. No full symbolic determinant is
authorized before this gate.

## Compute budget and kill criterion

CPU only, exact arithmetic. Expected runtime below two minutes; hard budget
five minutes. Emit progress after the inverse and after every five parameter
directions. If the inverse or graph construction exceeds the budget, stop and
record an inconclusive tooling result. No checkpoint is needed because every
completed direction is cheap and the total run is below the long-run threshold.

Declared 2026-07-26 before creating or running `run.py`.
