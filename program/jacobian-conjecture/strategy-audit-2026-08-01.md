# Jacobian strategy audit after EXP-132

Date: 2026-08-01. This audit supersedes the transverse-route ranking in the
2026-07-31 audit. It does not alter the scope of earlier experiments.

## Result that changes the ranking

EXP-132 adds direction `(2,8)` to the direct `A=0,d=1` matrix and proves a
three-minor unit ideal in `QQ[B,C,T]`. The normalized sections are

\[
P=(5B+4)^3(25B^2-20B+16)^3,
\]

\[
Q=B^{95}(H(B)+9765625B^{11}CT),
\]

and

\[
R=B^{105}C.
\]

The exact identity reduces to a univariate Bezout calculation because
`Q-9765625*B*T*R` is independent of `C,T` and coprime to `P`. Thus the
complete `A=0,d=1` boundary of the five-coefficient restriction is closed.

This does not close the complete five-coefficient restriction. Its
`A!=0,d=1` sector and its transverse `d=0` quotient have not been covered.

## Methodological insight

The strongest object was the zeroth Fitting ideal of the augmented cokernel,
not a growing list of point charts. Two inherited sections reduced the
exceptional support; a residual-selected basis had an acyclic normalized
graph and yielded a monomial generator. The unit certificate then followed
from one exact elimination and one univariate Bezout identity.

Direct generic determinant expansion and generic expression-field quotient
elimination both hit their declared five-minute gates. Exact SCC decomposition
converted the final determinant to a product of singleton affine blocks and
finished in under one minute. Future lifts must profile the normalized graph
before any ambient determinant expansion.

## Ranked routes

| Rank | Route | Proof value now | Gate |
|---|---|---|---|
| P0 | Lift the accepted section suite to `A!=0,d=1` with `(2,8)` | can close the principal-open sector of the five-coefficient restriction | reuse the EXP-123 graph and EXP-130 finite algebras; compute section dependence in the new variable before elimination |
| P0 | Rebuild the transverse `d=0` quotient | can close the other missing sector | verify whether `(2,8)` preserves or changes the explicit `P` kernel before selecting 124-column quotient minors |
| P0-control | Fitting-generator and exact SCC compression | turns residual support into small unit-ideal calculations | normalize at an exact nonzero anchor; split every boundary and denominator |
| P1 | Polynomial-matrix Smith/Popov invariants | may compress a positive-dimensional residual | use only after a residual survives the direct atlas; record all fraction-field denominator fibres |
| P2-conditional | Intersection-21 boundary transport | could connect reduced coefficients to original-pair Newton data | require the full divisor ledger from EXP-097 |
| P3-hold | Lee--Li/Jelonek global geometry | may organize a different program | no applicability bridge to this reduced matrix |

## Next decision tree

1. Preserve EXP-132's direct-boundary identity as a regression gate.
2. On `A!=0,d=1`, evaluate the EXP-123, EXP-124, EXP-129, and EXP-130
   sections after adjoining `(2,8)`. Record sections that vanish identically;
   do not count them as charts.
3. If dependence on the transverse variable is affine or low-degree, eliminate
   it with a monomial or acyclic section before recursing on the graph/base
   algebras.
4. If a positive-dimensional residual remains, switch to a Fitting
   presentation or invariant factors and persist the denominator ledger.
5. Separately specialize `d=0` before division, identify the kernel dimension,
   and rebuild the quotient. EXP-118 cannot be assumed to lift for free.
6. Only when both sectors close may the five-coefficient restriction be called
   complete.

## Alternative view decision

Lu--Ruan--Wang--Xiao (arXiv:2605.09286v1) confirms that maximal-minor unit
ideals are naturally zero-right-prime/unimodular-completion questions and
provides Smith-form criteria for structured multivariate polynomial matrices.
Its triangular highest-determinantal-divisor hypothesis is unproved here, so
the theorem is context rather than a shortcut. The direct Fitting atlas remains
the strongest route.

JC(2), the complete `(72,108)` family, the 24-parameter cyclic core, the full
51-parameter family, and the planar degree floor remain open.
