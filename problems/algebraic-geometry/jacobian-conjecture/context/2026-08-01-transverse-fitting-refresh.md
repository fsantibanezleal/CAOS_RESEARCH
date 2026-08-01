# 2026-08-01 transverse Fitting and polynomial-matrix refresh

## Scope

This source refresh asks whether the transverse `(2,8)` lift should continue
as a chart-by-chart determinant search or be reformulated as a polynomial
module problem. It supports EXP-132's strategy but supplies no theorem about
the GGHV matrix without an explicit applicability check.

## Primary source

- Dong Lu, Yuanyuan Ruan, Dingkang Wang, and Fanghui Xiao,
  *Matrix equivalence to Smith normal form: new theoretical results for
  multivariate polynomial matrices*, arXiv:2605.09286v1, submitted 2026-05-10.
  Primary URL: <https://arxiv.org/abs/2605.09286>. Accessed 2026-08-01.

## Verified claims

- [V] For a polynomial matrix `F`, the ideals of minors, determinantal
  divisors, and reduced-minor ideals are invariants under unimodular matrix
  equivalence (Definitions 2--5 and Proposition 7).
- [V] A full-column-rank rectangular polynomial matrix is called zero right
  prime when its maximal minors generate the unit ideal (Definition 10).
- [V] The paper proves a Smith-form equivalence criterion for matrices whose
  highest determinantal divisor has a triangular factorization
  `f1(x1)*prod_i (xi-fi(x1,...,x_{i-1}))^ti`, and extends the criterion to
  rectangular and rank-deficient matrices (Theorem 32).
- [V] The paper explicitly states that efficient construction of the required
  unimodular transformations remains algorithmically underdeveloped; known
  Quillen--Suslin-based construction can be at least exponential.

## Applicability decision

- [D] The zeroth Fitting/maximal-minor ideal is the correct exact object for
  the 302-by-125 augmented family. A unit ideal proves the cokernel support is
  empty and gives the zero-right-prime interpretation used in EXP-132.
- [U] The triangular highest-determinantal-divisor hypothesis of Theorem 32
  has not been established for the GGHV augmented matrix. The theorem cannot
  be invoked to replace the determinant atlas.
- [D] Smith/Popov or invariant-factor computation remains a conditional
  compression route only. Any fraction-field reduction must preserve a full
  denominator and exceptional-fibre ledger.

## Effect on route ranking

The direct Fitting atlas remains P0 because it asks exactly whether the
maximal-minor ideal is the unit ideal and permits small exact certificates.
Polynomial-matrix normal forms remain P1: they can compress a residual but do
not remove the need to prove the relevant structured-divisor hypothesis or to
audit denominator fibres. Lee--Li, Jelonek, and intersection-21 transport stay
conditional on their previously recorded bridges.
