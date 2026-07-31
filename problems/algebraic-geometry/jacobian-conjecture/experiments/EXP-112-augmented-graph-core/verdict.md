# EXP-112 - Verdict: the 125-column problem compresses exactly to a 36-column cyclic core

Verdict: **confirmed proper cyclic core**.

## Result

The exact run completed in 5.3 seconds. Predictions 1 through 4 are confirmed.
Prediction 5 is also confirmed: the largest strongly connected block is 36,
strictly smaller than 125.

After removing the structural constant \(Q\)-column and appending the target,
the complete affine-linear system has shape 302 by 125. The deterministic
pinned chart has exact rank 125 and an exact nonzero determinant.

For the exact normalized direction matrices
\[
N_i=A_0^{-1}A_i,
\]
the union dependency graph has 4212 edges and strongly connected component
sizes
\[
36,1,1,\ldots,1.
\]
There are four cyclic diagonal blocks:

1. one 36-by-36 block involving 24 of the 51 parameters;
2. three one-dimensional self-loop blocks, each depending only on
   \(\varepsilon_{(1,0)}\).

The 36-column block consists exactly of the \(Q\)-monomials
\[
\begin{aligned}
&x^0y^j,\quad 3\leq j\leq12,\\
&x^1y^j,\quad 2\leq j\leq13,\\
&x^2y^j,\quad 1\leq j\leq14.
\end{aligned}
\]
Its 24 active parameter directions are
\[
\begin{aligned}
&(0,j),\quad 1\leq j\leq7,\\
&(1,j),\quad 0\leq j\leq8,\\
&(2,j),\quad 2\leq j\leq9.
\end{aligned}
\]

All other 27 lower-family parameters occur only in acyclic off-diagonal
blocks for this chart. They cannot change its determinant.

## Exact factorization

Let \(C_{36}(\varepsilon)\) denote the normalized 36-by-36 cyclic block. The
selected full-family minor factors exactly as
\[
\det A_{\mathrm{selected}}(\varepsilon)
=
\det(A_0)\,(1+\varepsilon_{(1,0)})^3
\det C_{36}(\varepsilon).
\]

The forced-axis characteristic polynomial on the 36-core is
\[
\lambda^{23}(\lambda-1)^{13}.
\]
Therefore
\[
\det C_{36}(u,0,\ldots,0)=(1+u)^{13},
\]
and the full selected minor restricts to
\[
\det(A_0)(1+u)^{16},
\]
recovering EXP-101's forced-axis exponent independently.

This is an exact 51-to-24 parameter reduction and a 125-to-36 determinant
reduction for the pinned chart.

## The recovered rows

The 13 rows omitted by EXP-110 vanish at the pinned point, so none can enter
an invertible pinned minor. Every recovered row becomes nonzero in at least one
parameter direction. They are therefore unavailable for a one-chart proof
anchored at \(\varepsilon=0\), but are legitimate additional equations for
alternative charts on the exceptional locus.

## What this proves

- The 27 high-\(x\) parameter directions are determinant-inert on the selected
  pinned chart.
- The zero locus of that full 125-by-125 minor is pulled back from one explicit
  24-parameter, 36-by-36 determinant, together with the forced factor
  \(1+\varepsilon_{(1,0)}\).
- Exact determinant or chart work no longer needs to begin in 51 parameters or
  at size 125.
- The known forced-axis factor and the earlier two-parameter cycle are
  compatible with one common exact block structure.

## What this does not prove

- The 36-core determinant can vanish, so this single chart does not exclude
  the reduced family.
- Parameters that are inert for this selected determinant may matter to
  alternative minors on its zero locus.
- A full-family proof still needs to cover
  \[
  \{1+\varepsilon_{(1,0)}=0\}
  \cup
  \{\det C_{36}=0\}
  \]
  with alternative complete-row charts.
- JC(2), \((72,108)\), and the degree floor remain open.

## Adversarial validation

- Every normalized entry and graph edge was computed over
  \(\mathbb Q\), not inferred modulo a prime.
- The historical EXP-099 direction subset remains cyclic, reproducing its
  negative control.
- Three adversarial mixed integer/rational parameter points gave nonzero
  selected determinants.
- The forced-axis exponent 16 was reconstructed independently as 13 from the
  large core plus one from each of the three singleton loops.
- Every recovered row was checked both to vanish at the pinned point and to
  activate in at least one direction.

## How could this be wrong?

- The factorization concerns the deterministic pinned row basis, not every
  maximal minor.
- The component graph is basis-dependent. A different chart may yield a
  smaller core or a different parameter set.
- Strong connectivity is a support statement. It bounds where determinant
  dependence can occur but does not by itself describe the polynomial
  \(\det C_{36}\) or its zero locus.
- Completeness remains relative to the canonical EXP-071 pool. A source-level
  correction to that pool would require a new experiment.

## Strategy consequence

The next exact target is \(C_{36}\), not the raw full matrix. Before attempting
its 24-variable determinant, classify its parameter-group cycle structure and
factor out the forced direction. Then either:

1. derive a smaller cyclic core after forced-axis normalization; or
2. compute sparse determinant charts for the 36-core and use the recovered
   rows only on the residual closed strata.

The boundary-divisor route remains second priority because the graph route has
now delivered a strict exact compression.
