# EXP-108: An exact third chart closes the promoted three-coefficient slice

## Verdict

**CONFIRMED exactly over characteristic zero.**

EXP-107 leaves only the fiber \(z=-1/8\), where its first chart restricts to
a squarefree degree-12 polynomial \(Q(y)\). The first deterministic pivot
chart in EXP-108 produces a degree-13 determinant \(H(y)\) with

\[
\gcd_{\mathbb Z[y]}(Q,H)=1.
\]

The exact lift removes the connected mod-9 row/column weights, constructs
ordinary rational 125-by-125 matrices at \(z=-1/8\), and interpolates their
determinants under structural degree bounds 14 and 13. All 29 interpolation
values and two independent exact determinant checks pass. The primitive
polynomials reduce proportionally to the independent modular
reconstructions.

The exact \(Q\) is irreducible over \(\mathbb Q\). The third-chart polynomial
has the compact factorization, up to sign,

\[
\begin{aligned}
H(y)={}&y(49y^2+168y+192)(2401y^4+1568y^2+1024)\\
&\mathrel{}\cdot
(117649y^6-403368y^5+921984y^4-1053696y^3+786432).
\end{aligned}
\]

The artifact stores a verified integer identity

\[
A(y)Q(y)+B(y)H(y)=
3036277895244878564727703434378848855121939007419328699039744.
\]

Exact artifact SHA256:
`E2613D21D333CA6AA1C417F6DEA493ABEE98EC6AEAEE68EC0997E13A730D1AEA`.

## Consequence

Any common zero of the endpoint chart
\(G(z)=(8z+1)^{14}\) must have \(z=-1/8\), but the exact fiber polynomials
\(Q\) and \(H\) have no common zero. Hence three maximal-minor charts prove
rank 125 throughout the declared
\(\{(0,1),(1,7),(0,7)\}\) coefficient slice.

This excludes one exact three-coefficient slice of the reduced GGHV family.
It does not cover the other coefficients, exclude the complete
\((72,108)\) case, or prove or disprove JC(2).
