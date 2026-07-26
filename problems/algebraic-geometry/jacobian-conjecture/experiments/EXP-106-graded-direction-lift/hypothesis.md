# EXP-106: Classify grading-compatible coefficient lifts

## Question

Which of the remaining 24 coefficients in the persisted 26-parameter lower
family can be added to the closed EXP-105 slice while preserving its connected
\(\mathbb Z/9\) row/column grading?

## Criterion

For a new coefficient \(v\), its contribution to the scaled curve matrix is

\[
u^7vA_v.
\]

Given chart weights \(r_i,c_j\), this direction is grading-compatible if one
residue \(w_v\in\mathbb Z/9\) satisfies

\[
7\equiv r_i+c_j+w_v\pmod9
\]

for every nonzero selected entry of \(A_v\).

The test is exact and combinatorial. It must be applied independently to both
maximal-minor charts from EXP-105. A direction is promoted only if it is
compatible on both charts with the same intrinsic residue.

## Predictions and decisions

1. Compatibility is sparse rather than universal.
2. Compatible directions cluster by Newton-lattice residue.
3. If at least one direction survives, the lowest-support survivor becomes
   the next exact three-variable chart experiment.
4. If none survives, the \(\mu_9\) symmetry is slice-specific and the next
   route must use a multigraded or ungraded determinantal ideal.

Compatibility alone does not prove rank coverage after adding the parameter.
It only identifies directions for which the exact sparse determinant engine
can scale without reverting to dense multivariate expansion.

## Controls

- Recheck the two existing directions \((0,1)\) and \((1,7)\) as positive
  controls with their known exponent residues.
- Perturb one nonzero entry residue artificially as a negative control.
- Persist per-chart residues, support counts, disagreements, and the promoted
  ordering.

Declared 2026-07-26 before creating or running `run.py`.
