# EXP-003 preflight: Zhan-type counterexamples from small gadgets (HMB-002)

Date: 2026-11-06. Status: frozen before any computation. CPU only.

## Mechanism [V] and derivation [D]

Bullock, Frick, Singleton, van Aardt, Mynhardt (EJC 15 (2008) R18), Theorem 3.13 [V, archived PDF]: let M have a
minimum vertex cut S = {x, y} such that M - S has three noncomplete components G_1, G_2, G_3 with
N_{G_i}(x) = N_{G_i}(y) = N_i != V(G_i). Then M is maximal nontraceable iff (i) xy is an edge; (ii) each
X_i = M[V(G_i) + x] is MNH; (iii) at most one M[N_i] has a universal vertex; (iv) all G_i are traceable and at
least two are homogeneously traceable; (v) if u is a universal vertex of M[N_i], then G_i is traceable from u.
Zhan (arXiv:2608.00957v3, Lemma 5) [V]: for connected maximal nontraceable M, K_1 join M is MNH with circumference
equal to the detour order of M plus one; a longest cycle through the new vertex z is z + a detour of M.

[D] (as in Zhan's Lemma 4): a longest path of M meets all three G_i, passes x and y, and has one "middle"
G_i between them; an end G_j contributes a Hamilton path of G_j ending in N_j (it exists because X_j is MNH and
N_j != V(G_j)); the middle contributes a longest (p, q)-path of G_i with p != q in N_i. With
d_i = |G_i| - (order of a longest (p, q)-path, p != q in N_i) >= 1, the detour order is 2 + sum |G_j| - min d_i,
and for a middle gadget attaining the minimum, the residual of the cycle z + detour is the set O_i of vertices
of G_i that its middle path omits. **If some such O_i is not a clique, K_1 join M is a counterexample to Hoa's
conjecture, of order 3 + sum |G_i|.**

## Question

A gadget is (X, x): X an MNH graph from the EXP-001 census (orders 4 to 11), x a vertex such that G = X - x is
connected and not complete and N_X(x) != V(G). Over all gadgets and all triples, is there a triple satisfying
(iii)-(v) whose minimum-d gadget has a longest middle path omitting a non-clique set? Report the least order
3 + sum |G_i| reached, and every gadget's invariants (traceable, homogeneously traceable, universal vertices of
N, d, omitted-set types).

## Prediction

No admissible triple from gadgets of order <= 11 (confidence MODERATE): Zhan needed gadgets of order 18 and 19,
built with care, which suggests small MNH graphs have d = 1 or clique omitted sets.

## Validation

Gadget invariants by two methods (subset dynamic programming and plain backtracking) on every gadget. Any
counterexample candidate is built explicitly and verified directly: K_1 join M is non-Hamiltonian, every
nonadjacent pair is joined by a Hamilton path, the cycle has the claimed length, no longer cycle exists, and the
residual is not complete; until that verification it is not claimed.
