# EXP-119 - Verdict: exact open chart leaves three finite component intersections

Verdict: **mixed, exact residual reduction**.

## Result

The complete 302-by-125 augmented matrix has exact diagonal support
covariance for
\[
\operatorname{wt}(a,b,d)=(7,3,9).
\]
The support certificate checks 1,425 nonzero entries: 1,077 at the weighted
origin \(d=0\), 112 in each of the \(a\)- and \(b\)-directions, and 124 in
the \(d\)-direction. Its SHA-256 is
`9EAAAD5210C7EB89591EEB4E65C853D59E99966FF20DFFBDEA57D6D68C8FF8B0`.

EXP-115's persisted \(L/Q\) row basis is exactly invertible at
\[
(A,B,d)=(0,-4/5,1).
\]
Normalization there gives cyclic SCC sizes
\[
26,13,12,11,10,9,8,7,1,\ldots,1.
\]
The largest block is 26, well inside the declared gate. Its determinant
completed in 6.75 seconds. The full run, including three exact resultants,
completed in 93.75 seconds.

## Exact alternative determinant

Set
\[
X=A^3.
\]
On \(d=1\), the new alternative determinant is a nonzero rational scalar
times
\[
B^{36}K(X,B)
\prod_{c\in\mathcal C_7}(cX+78125B^7),
\]
where
\[
\mathcal C_7=
\{4096,8192,16384,32768,49152,65536,86016\}.
\]
The factor \(K\) has degree 6 in \(X\), degree 22 in \(B\), and 30
monomials. Its complete exact expression is persisted in
`artifacts/compact-invariant.json`.

The determinant has weighted degree 456 in the full \((a,b,d)\) system.
Homogenizing the nine displayed \(d=1\) factors accounts for weight 384;
the full determinant has an additional factor \(d^8\), whose weight is 72.
This factor is a unit on the \(d\ne0\) chart and disappears after setting
\(d=1\).

The expanded \(d=1\) determinant has total degree 108 and 114 monomials,
below the predicted 500-monomial bound.

## Proper intersections with \(G,L,Q\)

The exact gcd of the alternative determinant with each irreducible selected
factor is one:
\[
\gcd(G,\Delta_{\mathrm{alt}})
=
\gcd(L,\Delta_{\mathrm{alt}})
=
\gcd(Q,\Delta_{\mathrm{alt}})
=1
\]
in \(\mathbb Q[A,B]\). Thus no curve component survives, reproducing and
strengthening EXP-115's generic non-containment result.

However, the exact resultants eliminating \(A\) are nonconstant:

| component | degree in \(B\) | monomials | consequence |
|---|---:|---:|---|
| \(G\) | 852 | 211 | finite proper residual |
| \(L\) | 324 | 217 | finite proper residual |
| \(Q\) | 648 | 433 | finite proper residual |

Therefore the selected EXP-114 chart and this first exact alternative chart
do not cover \(d\ne0\). They reduce each residual curve to a
zero-dimensional elimination target.

## Adversarial validation

- Every full-system covariance equation was rechecked exactly.
- EXP-115's \(p=1009\) determinant 768 at
  \((A,B,d)=(0,201,1)\) reproduces.
- The same row basis is exactly nonzero at
  \((0,-4/5,1)\) over \(\mathbb Q\).
- The SCC block product agrees with five direct exact 125-by-125
  determinants not all used for normalization.
- Every block is one at the rational anchor.
- All 114 determinant monomials lift to nonnegative \(d\)-degree with total
  weighted degree 456.
- The compact \(X=A^3\) factorization reconstructs the original determinant
  exactly.
- The final raw artifact SHA-256 is
  `EDCB36EF966A874A493ADCCCDEAEED4564AB564D82C140B4C5B7A778BE8FCD2B`.
- The compact factor artifact SHA-256 is
  `7619AF5DBA95838CFC958185717A4CDABF57387852FE714D9FFFA9C3670988A7`.

## Compute-gate corrections

The first compact postprocessor incorrectly required every \(d=1\) factor
to be homogeneous in \(X,B\). The 30-term factor \(K\) is instead a
dehomogenized \((21,3,9)\)-homogeneous factor: its \(X,B\) weights are all
congruent modulo 9 and homogenize exactly after restoring \(d\).

Two optional attempts to factor or squarefree the compact invariant
resultants were stopped. The final exact \(X\)-resultant attempt was
terminated at 428.3 seconds, the declared total gate. No compact resultant,
squarefree degree, or factorization is promoted. The compact artifact
persists only the exact invariant determinant factorization, the unit-gcd
logic inherited from the exact \(\mathbb Q[A,B]\) calculation, the already
proved raw resultant degrees, and the budget-stop record.

## What this proves

- The full weighted covariance extends from EXP-118's boundary quotient to
  the 125-column \(d\ne0\) system.
- One exact alternative chart reduces all three selected residual curves to
  finite proper intersections.
- The invariant coordinate \(X=A^3\) is exact for the selected and
  alternative determinant factors.
- The next round can target finite algebraic sets rather than plane curves.

## What this does not prove

- The \(d\ne0\) chart is not covered. Each component retains a nonempty
  resultant target.
- The raw resultant degree is an elimination degree with multiplicity, not
  a certified count of distinct affine points.
- EXP-118 closes \(d=0\), but EXP-119 does not yet complete \(T_B\).
- The 24-parameter core, full 51-parameter family, \((72,108)\), degree
  floor, and JC(2) remain open.

## How could this be wrong?

As in EXP-118, the claim is exact inside the persisted 302-row matrix model
and depends on the upstream GGHV transcription and EXP-111's completeness
audit. Resultants can include projection or leading-coefficient artifacts;
they are used here only as exact finite targets, not as exact geometric
point counts. A third chart must be checked in the full component coordinate
rings before any complete cover is claimed.

## Strategy consequence and exploration moment

The new structural viewpoint is that the open and boundary determinants
share the binomial ladder
\[
cX+78125B^7.
\]
EXP-119 adds the two coefficients \(65536\) and \(86016\), a \(B^{36}\)
factor, and the 30-term factor \(K\). This recurring toric ladder should be
used for row-basis selection rather than treating the 852/324/648
resultants as unstructured point sets.

The strongest next experiment is a third-chart gate using EXP-115's
independent \(G\)-component row basis. Compute its exact SCC factorization on
\(d=1\), then test the ideal generated by the selected, \(L/Q\)-basis, and
\(G\)-basis minors in each of
\(\mathbb Q[X,B]/(G)\), \(\mathbb Q[X,B]/(L)\), and
\(\mathbb Q[X,B]/(Q)\). A unit ideal closes \(d\ne0\); otherwise the common
finite residual, not any pairwise resultant, becomes the next target.
