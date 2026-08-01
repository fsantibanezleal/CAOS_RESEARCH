# Jacobian strategy audit after EXP-135

Date: 2026-08-01. This audit supersedes the EXP-134 graph-field solve as the
first principal-open task.

## New exact fact

EXP-135 proves that the accepted EXP-124 determinant is unchanged by the
transverse direction `(2,8)` on the complete normalized `(A,B,C)` chart. The
proof uses exact rank and degree bounds, a complete tensor grid over 30
primes, and a CRT modulus larger than the explicit characteristic-zero
coefficient bound. It is not probabilistic modular evidence.

## Route evaluation

| Priority | Route | Decision | Reason |
|---|---|---|---|
| P0 | Lift the two EXP-129 residual sections | continue | these sections complete the old graph atlas and now carry the only unresolved graph fibres |
| P0 | Rebuild transverse `d=0` quotient | continue independently | EXP-118's explicit `P` kernel may change after `(2,8)` and cannot be inherited |
| P1 | Lift EXP-130 finite-base section | continue after graph sections | its old dependence is quadratic and the finite product algebra offers blockwise certificates |
| retired | 33-by-33 symbolic determinant | do not resume | EXP-134 gated and EXP-135 replaces it with a proved low-rank finite certificate |
| retired | graph-function-field inversion for EXP-124 | do not resume | the stronger ambient polynomial identity is already proved |
| fallback | complete-grid CRT certificate | reuse selectively | it is exact when separate degree and coefficient-height bounds are persisted; use low-rank updates to control cost |

## Alternate view retained

The useful change of viewpoint is from symbolic rational inversion to a
finite coefficient certificate. Rank controls the interpolation degree,
low-rank determinant lemmas control each evaluation, and an explicit integer
height bound upgrades multi-prime zero residues to a characteristic-zero
identity. This route should be tested first on the observed-inert EXP-129
section; the affine and quadratic sections should reconstruct their actual
`T` coefficients instead of assuming inertness.

## Scope gate

One retained divisor is not an atlas. No five-coefficient closure is claimed
until the EXP-129/130 lifts and transverse `d=0` quotient are all covered.
Nothing here excludes `(72,108)`, raises the planar floor, or decides JC(2).
