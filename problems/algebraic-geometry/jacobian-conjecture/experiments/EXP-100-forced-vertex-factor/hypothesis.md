# EXP-100: Factor the forced-vertex direction from the augmented minor

## Question

Does the self-loop found by EXP-099 come entirely from the nonzero forced
\((1,0)\) vertex coefficient, leaving a common strict flag for the other 24
effective parameters after that coefficient is normalized?

## Motivation

EXP-099 refuted a common strict flag for all 26 EXP-059 directions. Its shortest
cycle is a self-loop labelled by the \((1,0)\) coefficient, and the exact trace
of the corresponding normalized perturbation matrix is \(16\).

The 26 directions contain two special coordinates:

- \((0,0)\), whose bracket action should be identically zero;
- \((1,0)\), which varies the coefficient of the already forced \(x\) vertex.

The GGHV polygon requires that vertex coefficient to be nonzero, and the
reduced family normalizes it to \(1\). A rank-16 projector in this direction
would give

\[
\det(I+uB_x)=(1+u)^{16}.
\]

Its only zero would be \(u=-1\), exactly where the forced \(x\) coefficient
vanishes and the declared stratum is left.

The decisive remaining question is whether the other 24 normalized directions
preserve a common strict flag when the forced coefficient is fixed.

## Falsifiable predictions

1. The normalized \((0,0)\) direction is the zero matrix.
2. The normalized \((1,0)\) direction \(B_x\) is idempotent with rank and trace
   \(16\), proving
   \(\det(I+uB_x)=(1+u)^{16}\).
3. After removing \((0,0)\) and fixing the \((1,0)\) coefficient, the
   union-support graph of the remaining 24 exact perturbation matrices is
   acyclic.
4. The recovered order makes all 24 matrices strictly triangular, so the
   selected augmented minor equals its nonzero base value for every
   simultaneous value of those 24 coefficients.
5. Independent exact mixed substitutions with the forced coefficient fixed
   reproduce the base determinant.

If prediction 3 fails, persist its shortest cycle and an exact labelled-product
trace. If prediction 2 fails, the proposed forced-vertex factorization is
refuted and no normalization conclusion follows.

## Premise dependencies

- EXP-059 owns the selected augmented minor and already records that it is
  nonconstant on the unnormalized 26-parameter family.
- EXP-099 reconstructs that minor exactly, finds the \((1,0)\) self-loop and
  trace \(16\), and reproduces mixed determinant variation.
- The GGHV dossier records the forced nonzero \(x\)-vertex normalization. This
  experiment does not use the normalization unless the projector factor is
  proved exactly.
- The constant polynomial direction commutes with the bracket by direct
  algebra, but its selected matrix is recomputed rather than assumed zero.

## What a PASS or FAIL proves

- A full PASS proves exact simultaneous inconsistency on the 24-parameter
  normalized EXP-059 subfamily, because the augmented minor is a fixed nonzero
  constant while the bracket matrix has the constant-\(Q\) kernel.
- A projector PASS with a flag FAIL proves only the forced-vertex factor and
  identifies the first genuine interior cycle for the constructible-strata
  route.
- A projector FAIL refutes the proposed interpretation of trace \(16\).
- No outcome covers the remaining GGHV coefficients or all three forced
  branches, and no outcome alone excludes \((72,108)\).

## Method

Reuse the deterministic EXP-099 matrix reconstruction, then:

1. identify the \((0,0)\) and \((1,0)\) normalized directions;
2. test zero, idempotence, rank, and trace exactly;
3. verify the determinant factor at several exact values and by the projector
   eigenvalue identity;
4. build and topologically sort the union graph for the other 24 directions;
5. verify strict triangularity in the recovered order;
6. run fixed mixed determinant controls with the forced coefficient unchanged.

## Invariant-first note

Idempotence is the cheapest exact invariant explaining trace \(16\). A common
strict flag on the remaining directions then proves determinant constancy
without expansion. Only if either invariant fails should a symbolic
determinant or constructible residual-stratum calculation be considered.

## Compute budget and kill criterion

CPU only, exact arithmetic. Expected runtime below one minute; hard budget five
minutes. Stop on matrix-selection drift or a singular base minor. A failed
projector or graph prediction is a valid refutation and must still produce an
artifact.

Declared 2026-07-26 before creating or running `run.py`.
