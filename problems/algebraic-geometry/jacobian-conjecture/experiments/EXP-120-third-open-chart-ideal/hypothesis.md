# EXP-120 - Third weighted-open chart and common residual ideal

## Question

Does EXP-115's independent \(G\)-component row basis supply a third exact
maximal minor that, together with the EXP-114 selected chart and EXP-119's
\(L/Q\)-basis chart, covers the complete \(d\ne0\) \(T_B\) system?

Equivalently, for each
\[
F\in\{G,L,Q\},
\]
is
\[
(F,\Delta_{LQ},\Delta_G)=\mathbb Q[X,B],
\qquad X=A^3?
\]

## Motivation

EXP-119 proves that \((F,\Delta_{LQ})\) is zero-dimensional for each
selected residual component, but its raw resultants retain high
multiplicity. A third chart selected independently on \(G\) can either:

1. make each component ideal a unit and close \(d\ne0\); or
2. define the true common finite residual for a fourth-chart search.

The recurring factors
\[
cX+78125B^7
\]
suggest that exact SCC factorization is more informative than expanding
pairwise resultants.

## Premise dependencies

- [MV] EXP-114 supplies the selected residual \(G L Q\).
- [MV] EXP-115 supplies the independent \(G\)-basis and its nonzero
  determinant at \((A,B,d)=(64,4,1)\bmod1009\).
- [MV] EXP-119 supplies exact \((7,3,9)\) covariance, the exact
  \(\Delta_{LQ}\) factorization, and finite pairwise component residuals.
- [D] A unit Groebner basis for
  \((F,\Delta_{LQ},\Delta_G)\) proves that the three principal opens cover
  the component \(F=0\).

## Predictions

1. [C] The persisted \(G\)-basis has a nonzero exact determinant at one of
   the first nine deterministic rational controls.
2. [C] Normalization at that anchor has largest cyclic SCC at most 60.
3. [C] Its \(d=1\) determinant has at most 500 monomials and factors through
   \(X=A^3\).
4. [C] At least two of the three ideals
   \((F,\Delta_{LQ},\Delta_G)\) are units.
5. [C] Any surviving common residual has an elimination polynomial of
   squarefree degree at most 100 in \(B\).

## Method

1. Reconstruct EXP-115's 302-by-125 system and load its persisted
   \(G\)-basis.
2. Reproduce the \(p=1009\) witness determinant 978.
3. Test the deterministic exact anchors
   \[
   (0,0),(1,0),(0,1),(1,1),(-1,1),(1,-1),(2,1),(1,2),(-1,-1)
   \]
   on \(d=1\), stopping at the first nonzero determinant.
4. Normalize there, compute the exact dependency graph, and enforce the
   60-column SCC gate.
5. Compute and factor the block determinants. Reassemble
   \(\Delta_G(A,B,d=1)\), verify five direct exact determinants, and prove
   that all \(A\)-exponents lie in one residue class modulo three.
6. Convert the determinant to a monomial in \(A\) times a polynomial in
   \(X=A^3,B\). Monomial coordinate factors are handled as separate strata,
   not cancelled silently.
7. For each \(F=G,L,Q\), compute an exact Groebner basis of
   \((F,\Delta_{LQ},\Delta_G)\). If it is not the unit ideal, persist its
   zero-dimensional lexicographic elimination polynomial and squarefree
   degree.

## What a PASS proves and what a FAIL proves

A PASS with three unit ideals closes the complete \(d\ne0\) chart. Combined
with EXP-118, it closes the full three-parameter \(T_B\) restriction.

A mixed PASS with a nonunit ideal proves only the persisted common finite
residual. It is still a strict reduction beyond EXP-119.

Failure to find a rational anchor does not imply rank deficiency; it promotes
an algebraic or modular normalization. A graph or Groebner budget stop is
inconclusive and must preserve all completed exact stages.

## One-sidedness and scope

Closing \(T_B\) would not close the 24-parameter core, the full
51-parameter family, \((72,108)\), the planar degree floor, or JC(2).

## Adversarial validation

- Reproduce EXP-115's modular witness exactly.
- Require the rational anchor determinant to be nonzero over \(\mathbb Q\).
- Compare the SCC product with five direct exact determinants.
- Reconstruct every invariant expression under \(X=A^3\) exactly.
- A component is covered only if the reduced Groebner basis is \([1]\).
- Recheck any nonunit elimination polynomial by substitution into the
  original three generators.

## Invariant-first and exploration note

The invariant-first object is the ideal in the two-variable quotient ring
\(\mathbb Q[X,B]\), not the high-multiplicity resultant in
\(\mathbb Q[A,B]\). This round tests whether independent row bases generate
the unit ideal before any point-by-point algebraic-number computation.

## Compute budget and kill criterion

CPU-only. Two-minute anchor and graph budget. Six-minute determinant budget,
with 240 seconds for the largest block. Each component Groebner calculation
has a 180-second limit and the total round has a 900-second gate. Stop before
a cyclic block larger than 60 or an expanded determinant above 10,000
monomials. A stopped Groebner stage promotes no unit or point-count claim.

Declared 2026-07-29 before implementation or run.
