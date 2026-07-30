# EXP-114 - Exact determinants on the two full-connectivity triples

## Question

What are the exact 36-core determinant polynomials on the two
deletion-minimal three-parameter supports that already generate full graph
connectivity?

The supports from EXP-113 are
\[
T_A=\{(0,1),(0,7),(2,9)\},
\qquad
T_B=\{(0,1),(0,5),(1,0)\}.
\]

## Motivation

EXP-113 refutes a second SCC compression: the 36-core remains strongly
connected without the forced direction, and three directions already suffice
to generate full connectivity. These triples are not arbitrary coefficient
slices. They are exact minimal controls for the complete cyclic mechanism.

Factoring their determinants is the cheapest way to determine whether full
connectivity produces a large irreducible algebraic obstruction or a compact
chart equation like the EXP-101 through EXP-108 residuals.

## Premise dependencies

- [MV] EXP-112 supplies the exact 36-core and pinned normalization.
- [MV] EXP-113 supplies both deletion-minimal full-connectivity triples.
- [D] The determinant of
  \(I+\sum_{i\in T}\varepsilon_iN_i\) is the selected augmented maximal minor
  restricted to that declared support, normalized by the nonzero pinned
  determinant.
- [D] A nonzero determinant excludes the selected support point, while a zero
  names only the residual locus for alternative charts.

## Predictions

1. [MV] Both triple matrices reconstruct from the exact EXP-112 core.
2. [C] Each determinant has substantially smaller total degree and support
   than the generic 36-by-36 bound.
3. [C] At least one determinant factors nontrivially over \(\mathbb Q\).
4. [C] The forced triple \(T_B\) contains a power of
   \(1+\varepsilon_{(1,0)}\), consistent with the forced-axis exponent 13.
5. [C] The two residual equations expose different chart geometry and should
   not be treated as one universal factor.

## Method

- Reconstruct the exact 36-core matrices.
- Form one symbolic 36-by-36 matrix for each declared triple.
- Compute the determinant with exact domain Gaussian elimination and factor it
  over \(\mathbb Q\).
- Record total degree, degree in each variable, monomial count, irreducible
  factor degrees and multiplicities.
- Verify each polynomial at five deterministic integer points by comparing
  symbolic evaluation with direct exact determinants.

## One-sidedness

- PASS gives exact equations for two graph-complexity controls and may identify
  a tractable residual chart.
- A compact factorization does not close the 24-parameter core or the full
  family.
- An irreducible high-degree result refutes the hoped compact chart on that
  triple only and redirects toward a structural univariate or boundary
  interpretation.

## Adversarial validation

- Exact rational symbolic determinant and independent direct exact evaluations
  must agree at five points per triple.
- The all-zero point must evaluate to 1.
- The \(T_B\) forced axis must recover \((1+u)^{13}\) on the 36-core.

## Invariant-first note

The triples are selected by deletion-minimal strong connectivity, not by
enumeration. Degree, support size, and factorization decide whether symbolic
chart work is justified before touching the full 24-variable determinant.

## Compute budget and kill criterion

CPU-only exact run. Budget five minutes per determinant, ten minutes total.
Stop after the first budget hit and record the other triple as not run. A
timeout is inconclusive and does not justify numerical factor claims.

Declared 2026-07-29 before implementation or run.
