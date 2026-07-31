# EXP-118 - Verdict: two monomial charts close the complete \(d=0\) plane

Verdict: **confirmed exact cover**.

## Result

The complete 302-by-124 quotient augmented matrix is equivariant for
\[
\operatorname{wt}(a,b)=(7,3).
\]
Exact integer row and column weights solve all 1,293 support equations:
1,069 in the origin matrix, 112 in the \(a\)-direction, and 112 in the
\(b\)-direction. The covariance certificate has SHA-256
`6478354BC5F67B79A072CD7098148A058A521CACB8B3C60C4DD90AF22E237449`.

A deterministic alternative 124-row basis gives the exact maximal minor
\[
\Delta_{\mathrm{alt}}(a,b)
=
C_{\mathrm{alt}}a^{107},
\]
where
\[
C_{\mathrm{alt}}
=
565958961373026707416394506369000218368019105220316408315206265193917054976
0000000000000000000.
\]
In particular, this minor is independent of \(b\) and is nonzero at every
point with \(a\ne0\).

EXP-117's selected chart satisfies
\[
\Delta_{\mathrm{sel}}(0,b)=b^{95}.
\]
It is therefore nonzero on \(a=0,\ b\ne0\). At the remaining point
\((a,b)=(0,0)\), direct exact ranks reproduce
\[
\operatorname{rank}M_{\mathrm{quot}}=112,\qquad
\operatorname{rank}[M_{\mathrm{quot}}\mid t]=113,
\]
so the system is inconsistent there as well.

The complete \(d=0\) \(T_B\) quotient plane is consequently inconsistent.
The cover has three strata:

| stratum | certificate |
|---|---|
| \(a\ne0\) | \(\Delta_{\mathrm{alt}}=C_{\mathrm{alt}}a^{107}\ne0\) |
| \(a=0,\ b\ne0\) | \(\Delta_{\mathrm{sel}}(0,b)=b^{95}\ne0\) |
| \(a=b=0\) | exact rank gap \(112/113\) |

## Invariant reconstruction

The alternative determinant has weighted degree 749. Its possible
\(a\)-exponents lie in one residue class modulo three. On the \(b=1\) chart,
writing \(z=a^3\), exact interpolation reduces it to
\[
a^2 H(z),\qquad
H(z)=C_{\mathrm{alt}}z^{35}.
\]
Thus
\[
a^2H(a^3)=C_{\mathrm{alt}}a^{107}.
\]

The reconstruction used five exact 124-by-124 determinant evaluations.
Two additional exact values, at \(a=6\) and \(a=7\), were not used in the
interpolation and agree exactly. The gcd with EXP-117's squarefree
degree-nine residual is one after this first chart:
\[
\gcd(P_9(z),H(z))=1,
\]
because \(P_9(0)\ne0\).

## Adversarial validation

- Covariance was derived from the support of the complete quotient matrix,
  not inferred from EXP-117's determinant.
- Every support equation was rechecked exactly.
- The exact interpolant respects the predicted weighted support and agrees
  at two unused rational points.
- The selected alternative basis has a nonzero determinant at two distinct
  good-prime representatives of each of the six irreducible factors of
  \(P_9\), for 12 independent component controls.
- The \(b=0\) determinant was evaluated directly and exactly at \((1,0)\).
- The origin ranks were recomputed from exact nullspaces.
- The final artifact SHA-256 is
  `18FBC75201E38E6ACFB6C7B4E76869DB9A5654F0E0EE14D6C08A49F39E1C2E94`.

## Execution corrections

The first run stopped after proving the unit invariant gcd because a validator
incorrectly required the full two-variable admissible support of the axis
minor to contain only one exponent. Nonvanishing on \(b=0\) requires only
that the pure \(a^{749/7}=a^{107}\) term be present and nonzero. The failed
log is preserved.

The second run completed the exact cover. A final validation pass corrected
the recorded axis exponent from the first admissible support index, 95, to
the pure-axis exponent, 107, and added the declared two-prime controls for
all six residual factors. Neither correction changes a determinant, row
basis, rank, or mathematical conclusion.

## What this proves

- The explicit \(P\)-kernel quotient is inconsistent at every point of the
  complete \(d=0\) \(T_B\) plane.
- EXP-117's nine invariant residual values need no separate algebraic-number
  charts: one monomial alternative minor covers all of them simultaneously.
- The structural boundary route is closed exactly.

## What this does not prove

- EXP-115 proved only generic non-containment on the three \(d\ne0\)
  components. Their proper intersections are not closed by this result.
- The result concerns the three-parameter \(T_B\) restriction, not the
  24-parameter core or the full 51-parameter GGHV family.
- It does not exclude the full \((72,108)\) case, raise the planar degree
  floor, or prove JC(2).

## How could this be wrong?

The exact cover depends on EXP-115's kernel quotient and EXP-116's claim that
the 302 rows are the complete canonical equation union. EXP-111 audited that
row union and EXP-118 reconstructs it through the same deterministic code,
but this experiment does not independently rederive the GGHV reduction from
the source paper. A defect in that upstream transcription would limit the
claim to the persisted matrix model.

Within that model, the proof uses exact rational arithmetic, exact support
covariance, exact determinants, exact gcd, and exact ranks. The finite-field
calculations choose and stress row bases only; no characteristic-zero
conclusion depends on a modular sample.

## Strategy consequence and exploration moment

The finite-residual plan was stronger than needed. Weighted covariance
exposes a coordinate-open cover:
\[
D(a,b)\bigl(C_{\mathrm{alt}}a^{107}\bigr)
\]
together with the origin rank gap. This is the new viewpoint from the round:
search alternative quotient charts for monomial determinants before
factoring a selected residual.

The next priority returns to EXP-115's \(d\ne0\) components. Compute the
exact restrictions of its persisted alternative minors to \(G,L,Q\), use
weighted invariant coordinates, and determine the proper intersection
ideals. The goal is a complete \(T_B\) cover, not another generic
non-containment statement.
