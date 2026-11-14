# EXP-014 preflight: are X6 and X7 the only blocks? (BJB-026, first half)

Date: 2026-11-14. Status: frozen before any computation of this experiment. CPU only.

## Background

Proposition prop:where of the second-regime note v0.03 (10.5281/zenodo.24229265), conditional on Didin's Theorem 3
(Zenodo 10.5281/zenodo.22831382, under review), shows that a k-connected extremal graph G of the second regime without
a partition into alpha cliques is either in case (a), k = 3, alpha odd, s(G) = 1, n <= 4 alpha - 1, or in case (b),
p(G) = 1 at six small triples. EXP-013 built graphs of case (a) from two blocks X6 and X7 found in the data, and the
note lists as open whether every case (a) graph has that shape: clique parts of orders 3 and 4, cross edges forming a
matching, X in {X6, X7}, attached at the observed triples.

## A reduction, derived before computing (to be checked by the computation and written as a proof)

Let G be as in case (a), n vertices, c = t(n, alpha) + (3 alpha + 1)/2 edges, and H an alpha-core of G with
p = alpha - 1 components V_1, ..., V_{alpha-1}. The proof of prop:where(a) holds with equality throughout:
- e(H) = t(n+1, alpha) - 1, and floor(n/alpha) = 3, so 3 alpha + 1 <= n <= 4 alpha - 1;
- exactly q = (3 alpha - 3)/2 edges of G join different components, and every component sends exactly 3 of them;
- c = e(H) + q, so G has no edge inside a component that is not in H: each G[V_i] = H[V_i].

Since the independence numbers of the components sum to alpha over alpha - 1 components, exactly one component X has
alpha(X) = 2 and the others are cliques (a connected graph with independence number 1). X is alpha-critical: an edge
of X whose deletion keeps alpha(X) would keep alpha(H). Hence the only spanning subgraph of X with independence number
2 is X itself, p(X) = 1 and s(X) = 1, and Didin's Theorem 3 applied to X (m = |X| >= 3 = max(alpha(X) + 1, p(X)))
gives e(X) >= t(m + 1, 2) - 1. With a_1, ..., a_{alpha-2} the clique orders,

  t(n+1, alpha) - 1 = e(H) = sum_i binom(a_i, 2) + e(X) >= sum_i binom(a_i, 2) + t(m+1, 2) - 1 >= t(n+1, alpha) - 1,

the last step because the right side counts the edges of alpha cliques on n + 1 vertices. Equality forces:
- e(X) = t(m+1, 2) - 1;
- the alpha clique orders a_1, ..., a_{alpha-2}, floor((m+1)/2), ceil((m+1)/2) are balanced over n + 1 vertices, so
  all lie in {3, 4} (3 alpha + 2 <= n + 1 <= 4 alpha);
- hence m + 1 is in {6, 7, 8}: m = 5, 6 or 7 with e(X) = 5, 8 or 11.

Three-connectivity adds, without Didin:
- every part has exactly three vertices with a cross edge (if at most two vertices of a part carry its three edges,
  they separate the rest of the part, nonempty because every part has at least 3 vertices, from the other parts);
  so each such vertex carries exactly one cross edge and the cross edges form a matching;
- the quotient (parts, cross edges) is a loopless cubic multigraph, and it is 3-edge-connected (a 2-edge cut gives a
  2-vertex cut: one end of each cut edge);
- for the block X with its attaching set A (|A| = 3): every vertex outside A has degree at least 3 in X, every vertex
  of A degree at least 2; and for every set T of at most two vertices of X, every component of X - T meets A \ T
  (otherwise T separates that component from the other parts).

No partition into alpha cliques adds theta(X) >= 3: with theta(X) = 2, the alpha - 2 cliques and the two cliques of X
partition V(G). (Partitions that use cross edges as cliques cost more: by the charging of thm:construction, a partition
into alpha cliques would need theta(X - S) + |S| <= 2 for a nonempty S of A, so X - a would be a clique for some a,
with binom(m-1, 2) > e(X) edges for m = 5, 6, 7; impossible.)

## Question

Which pairs (X, A) satisfy all of these necessary conditions:
- (C1) X has m in {5, 6, 7} vertices and exactly 5, 8, 11 edges respectively;
- (C2) X is connected, alpha(X) = 2, and every edge of X is critical;
- (C3) theta(X) >= 3;
- (C4) A is a set of 3 vertices; vertices outside A have degree >= 3 in X, vertices of A degree >= 2;
- (C5) for every T of at most 2 vertices of X, every component of X - T meets A \ T?

## Predictions (frozen)

- P1: no pair with m = 5.
- P2: with m = 6, X is isomorphic to X6 (graph6 `ETxO`) and A lies in the automorphism orbit of {0, 1, 5}.
- P3: with m = 7, X is isomorphic to X7 (graph6 `FQjRo`) and A lies in one of the orbits of {0, 1, 2}, {1, 2, 3},
  {1, 2, 6}.
- If P1 to P3 hold, then, conditional on Didin's Theorem 3, every extremal graph of case (a) is a graph of Theorem
  thm:construction (with X6 or X7 at an observed triple and a 3-edge-connected cubic quotient), and conversely; the
  case (a) graphs are characterised exactly.

## Method

`check_blocks.py` (NetworkX 3.4.1): every graph on 5, 6 and 7 vertices from NetworkX's graph atlas (all 1,253 graphs
up to 7 vertices, one per isomorphism class), filtered by C1 to C3; for each survivor every 3-subset A, filtered by C4
and C5; survivors grouped by isomorphism of (X, A) and compared with X6, X7 and the observed triples. Cross-check of
the atlas: the numbers of graphs on 5, 6, 7 vertices (34, 156, 1,044) against OEIS A000088. Independent check of C2
and C3 by brute force over vertex subsets. Outputs: `artifacts/check-blocks.json` and `artifacts/run-output.txt`.

## Refutation

Any surviving (X, A) outside P1 to P3 refutes the prediction. It would then be checked whether it yields an extremal
graph (a construction with that block), which would be a new block.
