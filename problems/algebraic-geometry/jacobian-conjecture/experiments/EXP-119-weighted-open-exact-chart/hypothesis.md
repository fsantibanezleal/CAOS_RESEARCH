# EXP-119 - Exact alternative chart on the weighted-open residual

## Question

On the \(d\ne0\) chart of \(T_B\), does the persisted EXP-115 alternative
row basis yield an exact maximal minor whose principal open, together with
the EXP-114 selected minor, covers the three residual components
\[
G(A,B)=0,\qquad L(A,B)=0,\qquad Q(A,B)=0?
\]

## Motivation

EXP-115 proves only that none of \(G,L,Q\) is wholly rank-deficient. It does
not close the proper intersections of its alternative minors with those
curves. EXP-118 shows that support covariance can turn a modularly selected
row basis into a simple exact monomial chart. The strongest next test is to
apply that mechanism before launching component-by-component elimination.

On \(d\ne0\), use
\[
a=A u^7,\qquad b=B u^3,\qquad d=u^9.
\]
The normalized selected determinant has residual \(G L Q=0\) on \(d=1\).
EXP-115's \(L\)-basis is exactly nonzero at the rational anchor
\[
(A,B,d)=(0,-4/5,1).
\]
This supplies an exact normalization point for dependency-graph
decomposition.

## Source and invariant preflight

The 2026-07-29 primary-source sweep found no newer result closing the GGHV
\((72,108)\) chain. The source still presents that chain as its only open
degree pair below 125. The cheap invariant-first gate is the full
\((7,3,9)\) support covariance of the 302-by-125 augmented matrix. If it
holds, every 125-row minor is weighted homogeneous, and setting \(d=1\)
preserves an exact bounded support in \(A,B\).

## Premise dependencies

- [MV] EXP-111 supplies the complete 302-row effective augmented system.
- [MV] EXP-114 supplies the exact selected factors \(G,L,Q\) on \(d=1\).
- [MV] EXP-115 supplies irreducibility of \(G,L,Q\), the persisted
  alternative row bases, and the exact rational \(L\)-anchor.
- [MV] EXP-118 validates the support-covariance method on the \(d=0\)
  quotient matrix.
- [D] Exact unit ideal tests in each component coordinate ring prove that
  the selected and alternative principal opens cover that component.

## Predictions

1. [C] The complete 302-by-125 augmented matrix has exact diagonal support
   covariance with weights \((7,3,9)\).
2. [C] Normalization of EXP-115's \(L/Q\) row basis at
   \((0,-4/5,1)\) splits its parameter-dependency graph into cyclic blocks,
   with largest block at most 60.
3. [C] Its exact determinant on \(d=1\) completes inside six minutes and has
   at most 500 monomials after factorization.
4. [C] The exact alternative determinant removes \(L\) and \(Q\) completely
   and reduces the remaining intersection on \(G\) to a finite invariant
   set, or closes all three components.

## Method

1. Reconstruct EXP-115's full 302-by-125 system as
   \[
   A_0+aA_a+bA_b+dA_d
   \]
   around the weighted origin \(d=0\).
2. Solve and recheck every integer row-column support equation for weights
   \(0,7,3,9\). Persist the weight certificate and digest.
3. Load EXP-115's persisted \(L/Q\) row basis. Verify its determinant is
   exactly nonzero at \((0,-4/5,1)\).
4. Normalize at that anchor, build the exact dependency graph for
   \(A\) and \(B+4/5\) on \(d=1\), and compute its strongly connected
   components.
5. If the largest cyclic block is at most 60, compute and factor each block
   determinant over \(\mathbb Q[A,B]\). If it is larger, stop before the
   determinant and persist the graph.
6. Reassemble the alternative determinant as a factored expression, verify
   it at five unused exact rational points, and check its weighted support
   against the \((7,3,9)\) certificate.
7. For each of \(G,L,Q\), compute exact gcd, resultant, or Groebner
   certificates needed to decide whether the selected residual component
   and the alternative determinant have an empty intersection. Persist any
   proper residual ideal that survives.

## What a PASS proves and what a FAIL proves

A PASS with unit component ideals proves that the complete \(d\ne0\) \(T_B\)
chart is inconsistent. Together with EXP-118, this would close the entire
three-parameter \(T_B\) restriction.

A PASS that leaves a nonunit component ideal proves only a strict reduction
to that persisted proper intersection. It does not close \(d\ne0\).

A FAIL at covariance refutes the proposed torus mechanism. A determinant
budget stop proves only that this row basis is not yet an affordable exact
chart. Neither failure supports existence of a reduced solution.

## One-sidedness and scope

Even a complete \(T_B\) cover concerns only three active directions. It does
not close the 24-parameter core, the full 51-parameter family,
\((72,108)\), the planar degree floor, or JC(2).

## Adversarial validation

- Recheck covariance on every nonzero matrix entry.
- Reproduce the EXP-115 modular determinant at \(p=1009\).
- Verify the exact rational anchor determinant independently.
- Compare the block product with five direct exact 125-by-125 determinants.
- Check every promoted factorization by exact expansion or quotient.
- A component is called covered only with an exact unit certificate in its
  coordinate ring. A single witness remains generic non-containment only.

## Exploration moment

The round tests whether EXP-118's monomial-chart phenomenon lifts from the
structural boundary to the weighted-open system. If it does not, the graph
and exact factor support decide whether the next lens should be elimination
on plane curves, toric compactification, or a different row-basis search.

## Compute budget and kill criterion

CPU-only. Two-minute graph and covariance budget. Six-minute determinant
budget, with a 240-second limit on the largest block and 420 seconds total.
Stop before a cyclic block larger than 60 or an expanded product above
10,000 monomials. Persist graph, completed blocks, timings, and partial
factor data. A budget stop is inconclusive on the residual rank locus.

Declared 2026-07-29 before implementation or run.
