# EXP-013 proof: second-line graphs without a partition into alpha cliques, for every odd alpha

Status: [D], with the finite facts F1 to F6 about two fixed graphs machine-verified by `check_lemmas.py` [MV].

## The building blocks

- X6: graph6 `ETxO`, vertices 0 to 5, edges 02 03 04 14 15 23 24 35, with attaching triple A = {0, 1, 5}.
- X7: graph6 `FQjRo`, vertices 0 to 6, edges 02 04 05 13 15 16 24 26 35 36 46, with attaching triple A one of
  {0, 1, 2}, {1, 2, 3} or {1, 2, 6}.

`check_lemmas.py` verifies, for each X and each of its triples A:

| Fact | Statement |
|---|---|
| F1 | alpha(X) = 2 and theta(X) = 3 |
| F2 | X - A contains two non-adjacent vertices |
| F3 | theta(X - S) + abs(S)/2 >= 5/2 for every nonempty S contained in A |
| F4 | e(X6) = e(K3 + K3) + 2 = 8 and e(X7) = e(K3 + K4) + 2 = 11 |
| F5 | for every set T of at most two vertices, every component of X - T meets A - T |
| F6 | X is 2-connected |

## The construction

Let alpha >= 3 be odd and 3 alpha < n <= 4 alpha - 1. Write n = 3 alpha + r with 1 <= r <= alpha - 1.
- T(n, alpha) has r cliques of order 4 and alpha - r of order 3.
- If alpha - r >= 2, replace two cliques of order 3 by X6. Otherwise (r = alpha - 1), replace the clique of order 3
  and one of order 4 by X7.
- This leaves alpha - 1 parts: alpha - 2 cliques P_1, ..., P_{alpha-2} and X.
- Let Q be a loopless cubic multigraph on these alpha - 1 parts that is 3-edge-connected. Such a Q exists because
  alpha - 1 is even:
  - the triple edge for alpha - 1 = 2;
  - K4 for 4;
  - the prism C_h x K2 for alpha - 1 = 2h >= 6.
- Give each part an injective map from its three Q-edges to its vertices: any three distinct vertices of a clique,
  and the triple A for X.
- Every Q-edge PR becomes an edge of G between the images of its two ends.

These are the cross edges. Each vertex carries at most one cross edge, so the cross edges form a matching. Call G the
resulting graph; it has n vertices.

## Theorem

G has t(n, alpha) + (3 alpha + 1)/2 edges, independence number alpha, vertex connectivity at least 3, and clique cover
number alpha + 1. In particular V(G) has no partition into alpha cliques, and s(G) >= 1 in Didin's notation.

### Proof

**Edges.** The clique parts span t(n, alpha) minus the edges of the replaced pair. By F4, X spans those edges plus 2.
There are 3(alpha - 1)/2 cross edges. The total is t(n, alpha) + 2 + (3 alpha - 3)/2 = t(n, alpha) + (3 alpha + 1)/2.

**Independence number.**
- Upper bound: an independent set meets each clique part in at most one vertex and X in at most alpha(X) = 2
  (F1), so it has at most alpha vertices.
- Lower bound, the pair in X: by F2, X - A contains non-adjacent vertices x and y. Neither carries a cross edge, so
  neither has a neighbour outside X.
- Lower bound, the clique parts: the cross edges between clique parts form a graph of maximum degree at most 1 on
  vertex classes of size at least 3 >= 2. By Haxell's theorem (P. E. Haxell, A note on vertex list colouring,
  Combin. Probab. Comput. 10 (2001) 345-347, doi:10.1017/S0963548301004758: classes of size at least 2 Delta admit
  an independent transversal), one vertex can be chosen from each clique part with no cross edge between two chosen
  vertices.
- Together with x and y this gives an independent set of size alpha - 2 + 2 = alpha.

**Connectivity.** Let S be a set of at most two vertices. We show that G - S is connected.
- Every part has at least three vertices, so every part keeps a vertex. Every clique part minus S is a nonempty
  clique, hence connected.
- Case 1: X - S is connected. Then every part minus S is connected. If G - S were disconnected, the parts would split
  into two nonempty sides with every cross edge between the sides destroyed. Each vertex of S destroys at most its own
  cross edge, so at most two are destroyed. But Q has at least three edges across any partition into two nonempty
  sides, a contradiction.
- Case 2: X - S is disconnected. By F6, S is contained in X, so every other part and every cross edge not incident to
  X survives.
  - Q - X is connected. A cut vertex v of a 3-edge-connected cubic multigraph is impossible: a side receiving at most
    one of v's three edges would be cut off by at most one edge, and two sides each receiving at least two would need
    four edges at v.
  - So the parts other than X lie in one component of G - S.
  - By F5, each component of X - S contains a vertex of A - S. Its cross edge leads to a part other than X, so it
    survives.
  - Hence G - S is connected.

**Clique cover number.**
- Upper bound: the alpha - 2 cliques and a cover of X by theta(X) = 3 cliques (F1) give theta(G) <= alpha + 1.
- Cliques of G: a clique of G that meets two parts is a single cross edge. Two of its vertices in different parts are
  joined by a cross edge, and a third vertex would need a second cross edge at one of them.
- Counting a partition: let a partition of V(G) into cliques use the set M' of cross edges as two-vertex cliques.
  Charge each of them 1/2 to each of the two parts it meets. A part P then carries
  c(P) = theta(P - V(M')) + abs(P meet V(M'))/2.
  - A clique part has c(P) >= 1: either something remains, needing one clique, or all its at least three vertices are
    covered, giving at least 3/2.
  - X has c(X) = 3 when S = V(M') meet X is empty, and c(X) >= 5/2 otherwise by F3, since S is contained in A.
- The number of cliques is the sum of the c(P), at least alpha - 2 + 5/2 > alpha. It is an integer, so it is at
  least alpha + 1.
- By the lemma of EXP-011 (`didin.py`), p(G) = alpha exactly when V(G) splits into alpha cliques, so s(G) >= 1.

## Consequences

- At (22,7,3), (23,7,3) and (24,7,3), f = t(n, alpha) + ceil(3 alpha/2) is proved by enumeration (EXP-007 to EXP-010).
  G is therefore extremal there, unconditionally, and has no partition into alpha cliques.
- For every odd alpha >= 3 and 3 alpha < n <= 4 alpha - 1, G is extremal if Didin's Theorem 9 holds. Case (a) of the
  EXP-011 proposition (k = 3, alpha odd, s = 1, n <= 4 alpha - 1) is then realised at every triple where it is allowed.
  The proposition needs s(G) = 1 here, and G has p(G) >= alpha - 1, since its parts satisfy the sum condition of the
  EXP-011 lemma.
- The construction needs a clique of order 3 in T(n, alpha), which exists exactly when n <= 4 alpha - 1. This is the
  same bound as in the proposition.
