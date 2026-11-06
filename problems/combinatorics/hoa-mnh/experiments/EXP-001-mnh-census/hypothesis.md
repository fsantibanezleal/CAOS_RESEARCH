# EXP-001 preflight: exact census of maximal non-Hamiltonian graphs, with every longest cycle

Date: 2026-11-06. Status: frozen before any computation. CPU only.

## Question

For every order n up to 11 (and 12 if order 11 extrapolates to under 12 hours on 24 cores), list every MNH graph
on n vertices up to isomorphism and, for each, every vertex set of a longest cycle. Decide on that range:

1. Hoa's conjecture: is G - V(C) complete for every MNH graph G and every longest cycle C?
2. Zhan's Question 2: is every component of every residual complete?
3. Zhan's Question 3: is some residual connected but not complete?
4. Zhan's Question 4: the maximum number of residual components, f(n).

And extend OEIS A185306 (number of MNH graphs on n vertices, known for n <= 10) to n = 11 (and 12).

## Prediction

No counterexample to Hoa's conjecture at n <= 11 (Zhan's mechanism needs three gadgets of order at least about
ten each); f(n) = 1 on the range; Questions 2 and 3 have no witness on the range. Confidence MODERATE for n <= 11,
LOW for n = 12. A185306(11) unknown; no numeric prediction.

## Method (exact)

Generation: nauty geng 2.8.9 (`geng -c n`), every connected graph on n vertices up to isomorphism, split into
disjoint res/mod parts. An MNH graph on n >= 3 vertices is connected (a disconnected graph plus one edge has a
bridge) and not complete.

Filter `mnh.c`, per graph, exact:
- Necessary prune: every nonadjacent pair has d(u) + d(v) <= n - 1 (Bondy-Chvatal: a pair with d(u) + d(v) >= n
  can be added without changing Hamiltonicity, contradicting maximality).
- Hamilton paths by dynamic programming over vertex subsets: P[S][v] = set of start vertices of paths that cover
  exactly S and end at v. G is Hamiltonian iff some u in P[V][v] is adjacent to v (n >= 3); a nonadjacent pair u,
  v is joined by a Hamilton path iff u in P[V][v]. MNH iff not Hamiltonian and every nonadjacent pair is joined.
- Longest cycles: S carries a cycle iff |S| >= 3 and some u in P[S][v] is adjacent to v; the circumference is the
  largest such |S|; every S of that size with a cycle is a longest-cycle vertex set; its residual is G - S.

## Gates

1. Known answer: A185306 for n = 3..10 must be reproduced exactly: 1, 1, 3, 3, 7, 9, 18, 31.
2. geng sanity: connected graph counts must equal OEIS A001349 for n <= 8 (already checked on 2026-11-06: 21, 853,
   11117 for n = 5, 7, 8).
3. Independent re-check: every MNH graph found is re-verified by a second implementation (brute force over
   permutations for Hamilton cycles and paths, written separately in Python) for n <= 10, and for every graph that
   is a counterexample or a Question 2/3 witness at any n.

## Scope and stop conditions

Order 12 runs only if order 11 extrapolates to under 12 hours. A negative result is a lower bound on the least
counterexample order, nothing more. A counterexample is claimed only after gate 3.
