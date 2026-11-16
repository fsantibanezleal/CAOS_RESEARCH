# EXP-147 hypothesis: GGHV Theorem 5.1 applies to the three polygon classes of their Proposition 4.2 (the (9,24) case)

Declared 2026-11-16, before any code of this experiment ran. Backlog JCB-107.

## Question

GGHV 2022 (arXiv:2204.14178v1) Theorem 2.1 states the planar floor: a counterexample has max deg >= 125 or degrees
(72,108) or (108,72). Its proof discards the case (9,24) (A0 = (9,24), (m,n) = (2,3), max deg 99) through Proposition 4.2,
which reduces it to three polygon classes with [P,Q] = x, and Section 5, whose Theorem 5.1 excludes polynomials with given
starting and end points. The paper prints the bridge from Theorem 5.1 only for the case (9,27) (Corollary 5.7); for (9,24)
the discard is claimed in the introduction and the section title (our audit of 2026-07-22, dossier
`context/2026-07-22-beyond125-and-audit-dossier.md`, D1). Question: does each class of Proposition 4.2 satisfy the
hypotheses of Theorem 5.1 as printed, so that Theorem 5.1 discards it with no further argument?

## Sources (archived in the data root, `sources/gghv/`, with SHA256SUMS)

- arXiv:2204.14178v1 e-print (`2204.14178.tex`): Proposition 4.2 at lines 668 to 680, Theorem 5.1 at lines 1402 to 1409,
  Corollary 5.7 at lines 1788 to 1811, the direction-order note at line 380, the case table at lines 304 to 320.
- arXiv:1401.1784 (GGV1) e-print: the Notation at lines 368 to 372 ("st and en denote the first and the last point that we
  find on H(l_{rho,sigma}(P)) when we run counterclockwise along the boundary of H(P)"), the Remark at lines 381 to 386 (if
  l_{rho,sigma}(P) is not a monomial, (rho,sigma) x (en - st) > 0, with A x B = det(A; B)), and the successor and
  predecessor of a direction at lines 1281 to 1285.
- arXiv:1708.07936 (GGHV17, the order on directions GGHV 2022 follows) line 1246: for rho > 0 the end point of a
  (rho,sigma)-homogeneous element is the support of its monomial of greatest degree in y.

## Definitions used

v_{rho,sigma}(i,j) = rho i + sigma j; for a polygon N and a direction (rho,sigma), the face H_{rho,sigma}(N) is the set of
points of N maximizing v_{rho,sigma}; st and en are the first and last points of that face met running counterclockwise
along the boundary of N (GGV1); for a face with two endpoints this is the order in which the counterclockwise boundary walk
meets them. P, Q in L^(1) = K[x, x^{-1}, y] have Newton polygons N(P), N(Q) equal to the listed convex hulls.

## Claims, for each class k = 1, 2, 3 of Proposition 4.2

- A1: every corner of N(P) and N(Q) has nonnegative coordinates, so P, Q lie in K[x,y] (Theorem 5.1 asks for polynomials).
- A2: hypothesis (1) of Theorem 5.1 holds with g = 0, because Proposition 4.2 gives [P,Q] = x.
- A3: en_{3,-1}(P) = st_{1,0}(P) = (6,16) and st_{-1,1}(P) = en_{1,0}(P) = (6,18) (hypothesis (2)).
- A4: en_{3,-1}(Q) = st_{1,0}(Q) = (9,24) and st_{-1,1}(Q) = en_{1,0}(Q) = (9,27) (hypothesis (3)).

Derivation expected [D]: in every class the (3,-1)-face of N(P) is the edge from (1,1) to (6,16) and the (1,0)-face the
edge from (6,16) to (6,18); the edge after (6,18) has outward normal (-1,1) in class 1 (to (0,12)), (-2,1) in class 2 (to
(0,6)) and (-3,1) in class 3 (to (0,0)), so the (-1,1)-face starts at (6,18) (an edge in class 1, the vertex itself in
classes 2 and 3). The same holds for N(Q) with (1,0), (9,24), (9,27) and (0,18), (0,9), (0,0).

## Method

`run.py`: exact integer geometry. For each polygon: the convex hull ordered counterclockwise, the face of each direction,
st and en by the counterclockwise walk, checked against the cross-product rule of GGV1, the successor direction of (1,0)
(the outward normal of the next edge, reduced to coprime integers), and the four claims. Output `artifacts/results.json`.

## Controls (each must behave as stated, or the instrument is wrong and no verdict is drawn)

- K1 (Corollary 5.7 before its shift): N(P) = {(0,0),(1,1),(6,16),(6,18),(0,18)} fails A3, with st_{-1,1}(P) = (0,18): the
  paper shifts x before applying Theorem 5.1 for exactly this reason.
- K2 (the paper's own usage, line 380): for a polygon whose (1,0)-face is the edge from (8,28) to (8,32), st_{1,0} = (8,28).
- K3 (orientation mutant): the same computation with the walk run clockwise fails A3 and A4 in every class.
- K4 (planted violation): N(P) = {(0,0),(1,1),(6,16),(6,18),(2,18)} fails A3 (its (-1,1)-face is the vertex (2,18)).

## Prediction

A1 to A4 hold in all three classes (confidence 0.95; the only risk is the orientation convention, which K2 and the
consistency of Theorem 5.1 with Corollary 5.7 fix).

## What a confirmation means, and what it does not

Theorem 5.1 then discards every class of Proposition 4.2, so the (9,24) case is discarded by a printed theorem and the
floor of Theorem 2.1 no longer rests on an unprinted bridge for this case. Nothing else is re-verified: neither the proof
of Theorem 5.1, nor the exhaustiveness of Proposition 4.2, nor any other row of the case table.
