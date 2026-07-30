# EXP-118 - Finite boundary chart cover by weighted quotient minors

## Question

Do alternative 124-column quotient minors cover the complete residual left by
EXP-117 on the \(d=0\) \(T_B\) plane:

1. the divisor \(b=0\);
2. the five rational values of \(z=a^3/b^7\);
3. the four geometric roots of the squarefree quartic \(f_4(z)\)?

## Motivation and source preflight

EXP-117 reduces the zero locus of its selected quotient minor to
\[
b^{32}P_9(a^3/b^7)=0,
\]
where \(P_9\) is squarefree of degree nine. The primary GGHV source still
states that the \((72,108)\) case is the only degree pair below 125 that its
campaign does not discard. A fresh source sweep on 2026-07-29 found no
primary result closing that case or replacing this finite determinantal
target. The exact quotient route therefore remains decision-bearing.

## Structural input

On \(d=0\), EXP-115 supplies the polynomial kernel
\[
P=a y+b y^5+y^8(1-xy)^8.
\]
EXP-116 removes its fixed \(y^8\) coordinate and constructs a complete
302-by-124 augmented quotient matrix
\[
A(a,b)=A_0+aA_a+bA_b.
\]
EXP-117 proves that one 124-row minor is a nonzero scalar times
\[
b^{32}F_{28}(a,b)
\prod_{c\in\{4096,8192,16384,32768,49152\}}
(ca^3+78125b^7).
\]

Every non-\(b\) factor has weights
\[
\operatorname{wt}(a,b)=(7,3).
\]
The cheap invariant-first question is whether the entire quotient matrix,
not only the selected determinant, is equivariant under this weighted torus.
If it is, every maximal minor is weighted homogeneous and its nonvanishing is
constant along a weighted orbit. A minor on \(b\ne0\) can then be encoded by a
univariate invariant polynomial in \(z=a^3/b^7\).

## Premise dependencies

- [MV] EXP-115 proves the global \(P\)-kernel on \(d=0\).
- [MV] EXP-116 validates the 302-by-124 quotient matrix and exact rank gaps
  \(123/124\) at nonzero controls and \(112/113\) at the origin.
- [MV] EXP-117 proves the selected determinant factorization and squarefree
  degree-nine invariant residual.
- [D] If diagonal row and column weights solve all support equations for
  \(A_0,A_a,A_b\), then nonzero weighted rescaling preserves rank.
- [D] If alternative invariant minor polynomials \(H_i(z)\) satisfy
  \(\gcd(P_9,H_1,\ldots,H_k)=1\), their principal opens cover all nine
  geometric residual values.

## Predictions

1. [C] Integer row and column weights exist and exactly certify weighted
   covariance of the complete quotient matrix.
2. [C] Every selected alternative maximal minor has one residue class of
   \(a\)-exponents modulo three and reduces to a monomial times a polynomial
   \(H(z)\).
3. [C] A deterministic collection of at most six alternative row bases has
   exact invariant polynomials with
   \[
   \gcd(P_9,H_1,\ldots,H_k)=1.
   \]
4. [C] The \(b=0,\ a\ne0\) orbit is covered by an exact alternative minor at
   \((a,b)=(1,0)\).
5. [D] The origin remains inconsistent by EXP-116's exact \(112/113\) rank
   gap even though no 124-by-124 minor can be nonzero there.

## Method

1. Reconstruct EXP-116's complete quotient system.
2. Solve the integer support equations
   \[
   r_i+c_j=0,\ 7,\ 3
   \]
   for nonzero entries of \(A_0,A_a,A_b\), respectively. Recheck every
   nonzero entry and persist the weights and a digest.
3. Reproduce EXP-117's selected row basis and invariant polynomial \(P_9\).
4. At deterministic good-prime representatives of the five rational factors
   and the quartic factor, select alternative full-rank row bases. Reject a
   prime if a required component has no usable representative or any
   denominator vanishes.
5. For each selected row basis, determine the weighted degree from its row
   and column weights. Reconstruct its exact univariate invariant polynomial
   by exact determinant evaluation and interpolation, with modular
   interpolation used only to predict support and degree.
6. Compute the successive exact gcd with \(P_9\). Stop adding charts as soon
   as the gcd is one.
7. Independently cover \(b=0,\ a\ne0\) at \((1,0)\), and reproduce the exact
   origin rank profile.
8. Validate every reconstructed minor against direct exact determinant
   evaluations not used in interpolation and against two good-prime
   evaluations.

## What a PASS proves and what a FAIL proves

A PASS requires exact weighted covariance, an exact unit gcd on \(b\ne0\),
an exact nonzero \(b=0\) chart, and the reproduced origin rank gap. It proves
that the complete \(d=0\) \(T_B\) quotient system is inconsistent for every
\((a,b)\) over characteristic zero.

A FAIL does not produce a solution of the reduced equation and does not
support a counterexample. It identifies one of:

- failure of the proposed torus covariance;
- a surviving exact factor of the invariant gcd;
- an interpolation or exact-lift budget failure.

Any surviving factor becomes the declared target of a new experiment.

## One-sidedness and scope

Closing this finite cover closes only the \(d=0\) boundary of the
three-parameter \(T_B\) restriction. It does not close the proper
intersections on the \(d\ne0\) components, the 24-parameter core, the full
51-parameter GGHV family, \((72,108)\), the planar degree floor, or JC(2).

## Adversarial validation

- Derive covariance from the full matrix support rather than from the
  factorization of one determinant.
- Require exact equality for every support-weight equation.
- Reconstruct each invariant polynomial over \(\mathbb Q\), then test unused
  exact points.
- Compare the gcd route with direct full-rank checks on representatives of
  every residual component over two good primes.
- Reproduce EXP-116's exact origin and nonzero-axis rank profiles.
- Persist row bases, weights, polynomials, gcd sequence, hashes, timings, and
  all rejected-prime reasons.

## Invariant-first note

The weighted torus is the single cheap invariant that can turn nine algebraic
fibres into a univariate gcd certificate. Rank samples alone cannot close a
fibre, and a multivariate Groebner computation is not justified before this
covariance gate is tested.

## Compute budget and kill criterion

CPU-only. The covariance and modular selection stage has a 120-second budget.
The exact reconstruction stage has a 900-second total budget and a
180-second budget per determinant family. Checkpoint after every accepted
chart. Stop before more than 60 exact 124-by-124 determinant evaluations for
one chart. If the budget is hit, persist the covariance certificate, modular
row bases, partial gcd, and checkpoint; conclude only that the exact lift is
incomplete.

Declared 2026-07-29 before implementation or run.
