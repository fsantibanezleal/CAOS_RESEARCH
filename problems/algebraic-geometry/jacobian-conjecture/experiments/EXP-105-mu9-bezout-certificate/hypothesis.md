# EXP-105: A compact exact \(\mu_9\)-graded Bézout certificate

## Question

Can the EXP-104 curve-cover proof be compressed from 100-point interpolation
plus modular gcds to two exact polynomials in \(z=u^9\) and an explicit
Bézout identity?

## Grading prediction

For each selected 125-by-125 chart, every nonzero entry term should admit
weights \(r_i,c_j\in\mathbb Z/9\) satisfying

\[
e\equiv r_i+c_j\pmod9
\]

for its \(u\)-exponent \(e\in\{0,7,9,14\}\). Then every determinant monomial
has the same residue modulo 9.

EXP-104's first determinant has exact valuation \(1628\equiv8\pmod9\) and
primitive normalized polynomial

\[
F(z)=21-96z-1024z^2,\qquad z=u^9.
\]

The endpoint-safe second chart has bounds
\([777,903]\), both congruent to \(3\pmod9\). If the grading holds, it has the
exact form

\[
u^{777}G(u^9),\qquad \deg G\le14.
\]

## Method

1. Solve the row/column grading equations exactly over \(\mathbb Z/9\) for
   both chart support graphs and verify every nonzero entry term.
2. Evaluate the second determinant exactly at \(u=1,\ldots,15\), divide by
   \(u^{777}\), and interpolate \(G(z)\) at \(z=u^9\).
3. Require integer coefficients and nonzero degree-0 and degree-14 endpoints.
4. Verify independently at \(u=-1\) and \(u=16\).
5. Remove integer contents, compute \(\gcd_{\mathbb Q[z]}(F,G)\), and require
   it to be \(1\).
6. Compute \(A(z),B(z)\in\mathbb Z[z]\) and nonzero \(D\in\mathbb Z\) with
   \[
   A(z)F(z)+B(z)G(z)=D.
   \]
   Persist all coefficients and verify the identity exactly.

## Proof value

The exact constant Bézout identity proves the two normalized maximal minors
have no common zero over any characteristic-zero extension. It is a smaller,
fully rational certificate for the same complete residual-curve coverage as
EXP-104 and exposes the hidden grading for possible use when adding further
GGHV coefficients.

No implication beyond the declared two-coefficient slice is permitted.

## Budget

Fifteen exact 125-by-125 determinants plus two independent checks; two-minute
target and five-minute hard stop.

Declared 2026-07-26 before creating or running `run.py`.
