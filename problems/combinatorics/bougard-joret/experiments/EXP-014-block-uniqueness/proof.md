# EXP-014 proof: the extremal graphs of case (a) are exactly the construction graphs (conditional on Didin's Theorem 3)

Notation as in the second-regime note v0.03 (10.5281/zenodo.24229265): t(n, alpha) the edges of alpha balanced
cliques on n vertices; c = t(n, alpha) + ceil(k alpha / 2); theta the clique cover number; an alpha-core of G is a
spanning subgraph H with alpha(H) = alpha(G) in which every edge is critical; p(G) is the largest number of components
of an alpha-core and s(G) = alpha(G) - p(G). Didin's Theorem 3 (Zenodo 10.5281/zenodo.22831382, under review, used
as stated): a graph with independence number alpha, n >= max(alpha + 1, p) vertices and m edges has
m >= t(n + s, alpha) - s. Marks: [D] derived here; [MV] machine-verified by `check_blocks.py`; statements that use
Didin's theorem are conditional on it.

## Theorem

Assume Didin's Theorem 3. Let (n, alpha, 3) be in the second regime, alpha >= 3, and let G be a 3-connected graph with
n vertices, independence number alpha, c = t(n, alpha) + ceil(3 alpha / 2) edges and p(G) >= 2, without a partition of
V(G) into alpha cliques (case (a) of Proposition prop:where). Then G is a graph of Theorem thm:construction: alpha is
odd, 3 alpha < n <= 4 alpha - 1, V(G) splits into alpha - 2 cliques of orders 3 and 4 and one block X isomorphic to X6
or X7, the edges between parts form a matching, three at each part, along a 3-edge-connected loopless cubic quotient,
and X attaches at a triple in the orbit of {0, 1, 5} (X6) or of {0, 1, 2}, {1, 2, 3}, {1, 2, 6} (X7).

Conversely every such graph has these properties (Theorem thm:construction, unconditional), and it is extremal when
f(n, alpha, 3) = c, which holds for n <= 24 by the enumeration and for every n if Didin's Theorem 9 holds.

## Proof

Step 1 (equality in prop:where(a)) [D]. By Proposition prop:where, alpha is odd, s(G) = 1 and
floor(n/alpha) = 3. Let H be an alpha-core with p = alpha - 1 components V_1, ..., V_p and q the number of edges of G
between different V_i. The proof of prop:where(a) gives
c >= e(H) + q >= (t(n + 1, alpha) - 1) + ceil(3p/2) = t(n, alpha) + 3 - 1 + (3 alpha - 3)/2 = c,
using t(n+1, alpha) - t(n, alpha) = floor(n/alpha) = 3 (Lemma lem:tshift) and p = alpha - 1 even. So every inequality
is an equality: e(H) = t(n + 1, alpha) - 1, q = (3 alpha - 3)/2, every V_i sends exactly 3 of the q edges (each sends at least lambda(G) >= kappa(G) >= 3 and they sum to 2q = 3p), and e(G) = e(H) + q, so G[V_i] = H[V_i] for every i.

Step 2 (the parts) [D]. The independence numbers of the components of H sum to alpha(H) = alpha over alpha - 1
components, each at least 1, so exactly one component X has alpha(X) = 2 and the others have independence number 1,
hence are cliques. X is alpha-critical: deleting an edge of X raises alpha(H), hence alpha(X). Therefore the only
spanning subgraph of X with independence number 2 is X itself, X is connected, p(X) = 1 and s(X) = 1. Write m = |X|;
m >= 3 because alpha(X) = 2 and X is connected with an edge whose deletion raises alpha.

Step 3 (Didin on the block) [D, conditional]. Didin's Theorem 3 applied to X (m >= 3 = max(alpha(X) + 1, p(X)))
gives e(X) >= t(m + 1, 2) - 1. Let a_1, ..., a_{alpha-2} be the clique orders. Then
t(n + 1, alpha) - 1 = e(H) = sum_i binom(a_i, 2) + e(X) >= sum_i binom(a_i, 2) + t(m + 1, 2) - 1 >= t(n + 1, alpha) - 1,
where the last inequality holds because sum_i binom(a_i, 2) + t(m + 1, 2) is the number of edges of a disjoint union of
alpha cliques on (n - m) + (m + 1) = n + 1 vertices, at least t(n + 1, alpha) by convexity. Equality forces
e(X) = t(m + 1, 2) - 1 and all alpha clique orders a_1, ..., a_{alpha-2}, floor((m+1)/2), ceil((m+1)/2) to differ by
at most one, so they lie in {floor((n+1)/alpha), ceil((n+1)/alpha)}, a subset of {3, 4} because
3 alpha + 2 <= n + 1 <= 4 alpha. Hence m + 1 lies in {6, 7, 8}: m = 5, 6 or 7 with e(X) = 5, 8 or 11.

Step 4 (attachment) [D]. Let A_P be the set of vertices of a part P that carry an edge to another part. If
|A_P| <= 2, then A_P separates the nonempty set P - A_P (every part has at least 3 vertices) from the other parts
(there are alpha - 2 >= 1 others), a vertex cut of size at most 2: impossible. So |A_P| = 3, every vertex of A_P
carries exactly one of the three edges, and the edges between parts form a matching. The quotient Q (parts as
vertices, these edges as edges) is a loopless cubic multigraph. It is 3-edge-connected: a cut of at most two edges of
Q gives, by taking one end of each cut edge, a vertex cut of G of size at most 2 with both sides nonempty, because each side holds a part of at least 3 vertices, which loses at most 2. For the block
X with A = A_X: a vertex outside A has all its neighbours in X, so its degree in X is at least 3; a vertex of A has
degree at least 2 in X; and for every set T of at most two vertices of X, every component of X - T meets A \ T,
since otherwise T separates that component from the other parts.

Step 5 (no clique partition) [D]. theta(X) >= 3: if X splits into two cliques, these and the alpha - 2 clique parts
partition V(G) into alpha cliques.

Step 6 (the finite check) [MV]. Conditions C1 (m in {5, 6, 7} with 5, 8, 11 edges), C2 (connected, alpha = 2, every
edge critical), C3 (theta >= 3), C4 and C5 (Step 4) were tested on every graph on 5, 6 and 7 vertices (NetworkX graph
atlas: 34, 156 and 1,044 graphs, equal to OEIS A000088) and every 3-subset A (`check_blocks.py`,
`artifacts/check-blocks.json`). Three graphs pass C1 to C3; the pairs (X, A) passing C4 and C5 form exactly four
isomorphism classes of marked graphs: X6 with A in the orbit of {0, 1, 5}, and X7 with A in the orbits of {0, 1, 2},
{1, 2, 3} and {1, 2, 6}. Independence and clique cover numbers were computed by two methods each, with no
disagreement.

Step 7 (conclusion) [D]. The clique orders are those of T(n, alpha) with two cliques removed: with n = 3 alpha + r,
the a_i lie in {3, 4} and sum to n - m, so X6 (m = 6) leaves r cliques of order 4 and alpha - 2 - r of order 3
(T(n, alpha) without two K3), and X7 (m = 7) leaves r - 1 and alpha - 1 - r (T(n, alpha) without a K3 and a K4). With
Step 4 and Step 6, G is the graph of the construction with this X, its attaching triple and the quotient Q. Finally
3 alpha < n because n > k alpha, and n <= 4 alpha - 1 by Step 1.

## Consequence for BJB-026

Together with Proposition prop:where(b) and the complete enumeration at its six triples (EXP-011: case (b) is realised
only at (10,3,3), by 8 graphs), the extremal graphs of the second regime with alpha >= 3 and k >= 3 without a
partition into alpha cliques are, conditional on Didin's Theorem 3, exactly the construction graphs (k = 3, alpha odd,
3 alpha < n <= 4 alpha - 1) and the 8 graphs at (10,3,3). Here extremal means f(n, alpha, k) = c edges: Didin's
Theorem 9, which he derives from his Theorem 3, gives f = c for every n > k alpha, and the enumeration gives it for
n <= 24 without condition. The restriction alpha >= 3 is needed: at (7,2,3), f = 12 = c and the extremal graph
`FL~Cg` is 3-connected with independence number 2 and no partition into 2 cliques (independent review,
CAOS_MANAGE wip/caos-research/bj-exp014-proof-review-2026-11-14.md); Proposition prop:where assumes alpha >= 3. Those with a partition are the Bougard-Joret graphs
(Lemma lem:partition-structure, unconditional).
