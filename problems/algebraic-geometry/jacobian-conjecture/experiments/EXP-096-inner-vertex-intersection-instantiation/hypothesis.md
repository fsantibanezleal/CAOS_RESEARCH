# EXP-096: Instantiate inner vertices and intersection numbers on the open chain

## Question

What exact restrictions do the Lee--Li inner-vertex theorem and the GGHV
approximate-root formulas impose on the original polynomial Keller pair behind
the open \((72,108)\) case?

## Motivation

EXP-095 showed that source theorems requiring a polynomial pair with bracket
one must be applied before the GGHV Laurent reductions. The next ranked sources
provide two independent restrictions at that original stage:

1. Lee and Li confine the northeastern vertex of every nonzero inner or
   innermost polynomial to an explicit narrow lattice region.
2. Guccione, Guccione, Horruitiner, and Valqui express the intersection number
   \(I(P,Q)=\deg_x\operatorname{Res}_y(P,Q)\) exactly through the major final
   approximate roots.

Neither result has been instantiated in the repository for the open chain.

## Primary-source facts

### Lee--Li

For a polynomial pair with degree ratio \(a:b\), after the polynomial
rectangularization used in their reduction, Theorem 5.8 and Corollary 5.10 say
that a nonzero inner or innermost polynomial has northeastern vertex
\((m',n')\) in

\[
\mathfrak R=\left\{(x,y):
0\le y<\frac{a-1}{a}n,\quad
\mathfrak m\left(x-\frac{a}{a+b}\right)+\frac{a}{a+b}
\le y\le\frac nm x\right\},
\]

where

\[
\mathfrak m=
\frac{n-a/(a+b)}{m-a/(a+b)}.
\]

For the degree-72 component of the open pair:

\[
(a,b,m,n)=(2,3,16,56),\qquad
\mathfrak m=\frac{139}{39}.
\]

The source's stronger diagonal corollary does not apply because
\[
\frac ba=\frac32\not>\frac{n-m}{a}-1=19.
\]

### Approximate roots

For an \((m,n)\)-pair and a type-Ib final corner
\(((a/l,b),(\rho,\sigma))\), Proposition 3.21 gives

\[
|D_\tau^P|=mb.
\]

If the lower start is \((k/l,0)\), it also gives
\(\lambda_\tau^Q=k/l\). Theorem 3.15 gives the exact formula

\[
I(P,Q)=\sum_{\tau\in P_M}|D_\tau^P|\lambda_\tau^Q.
\]

The open chain has component factors \((m,n)=(3,2)\), final corner
\(A_1=(11/4,7)\), \(k=1\), and four major classes from the four roots of
the forced fourth-power edge. Therefore it predicts

\[
I(P,Q)=4\cdot(3\cdot7)\cdot\frac14=21.
\]

The four major classes account for \(84\) of the \(108\) roots of the
degree-108 component, leaving \(24\) minor roots, consistent with
\(m(A_0)_x=3\cdot8=24\).

## Premise dependencies

- The open-chain values
  \(A_0=(8,28)\), \(A'_0=(1,0)\), \(A_1=(11/4,7)\),
  \(k=1\), and \((m,n)=(3,2)\) are the verified GGHV17 transcription in
  `context/2026-07-22-gghv-72108-dossier.md`.
- The four major classes are supplied by the forced leading form
  \(cx(xy^4-r)^7\), equivalently by its four distinct fourth roots over the
  algebraically closed ground field.
- The Lee--Li rectangularization is a polynomial automorphism of the original
  pair. No Lee--Li claim is imported directly to the final Laurent pair.
- The source PDFs and TeX were reread before declaration:
  arXiv:2408.01279v1 and arXiv:1708.09367v2.

## Falsifiable prediction

Exact rational enumeration will show:

1. if the inner or innermost polynomial is nonzero, its northeastern vertex is
   one of exactly
   \[
   (1,3),(2,7),(3,10),(4,14),(5,17),(6,21),(7,24);
   \]
2. the open chain has four major classes, \(84\) major roots, \(24\) minor
   roots, and exact intersection number \(I(P,Q)=21\);
3. the published F1 example at its smallest member reproduces
   \(I(P,Q)=9\), providing an independent source control.

## Invariant-first note

The calculation uses only exact degree ratios, corners, multiplicities, and
the source formula. It does not build the 51-parameter reduced matrix. The
intersection number is a necessary invariant for every reconstruction of an
original open-case pair.

## What a PASS proves and what a FAIL proves

- PASS: the open case has a seven-point nonzero inner-vertex candidate set and
  exact intersection number \(21\). These are new instantiated necessary
  conditions, not an exclusion.
- FAIL: at least one source parameter or transformation identity has been
  mistranscribed. No restriction is recorded until the mismatch is resolved.

Neither outcome constructs a counterexample, proves the open chain realizable,
or raises the planar degree floor.

## Method and adversarial controls

Use exact `Fraction` arithmetic to:

1. enumerate every positive lattice point in the Lee--Li region;
2. test one admitted diagonal point and rejected upper, lower, and height
   boundary points;
3. evaluate the approximate-root sum;
4. reproduce the source's F1 smallest-member value \(I=9\);
5. reconcile major plus minor root counts with total degree \(108\).

## Compute budget and kill criterion

CPU only, exact rational arithmetic, expected runtime below one second. Budget:
10 seconds. There is no checkpoint because the decision is atomic. If the
script does not finish within the budget, record an infrastructure failure and
draw no mathematical conclusion.

Declared 2026-07-25 before running `run.py`.
