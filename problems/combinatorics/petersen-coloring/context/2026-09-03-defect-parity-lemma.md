# Derivation note: the Petersen defect is never 1 (2026-09-03)

Status: `[D]` derived here; motivated by EXP-006 (all 52 single-vertex relaxations of `G52`
refuted with verified proofs, all 1,326 pair relaxations satisfiable with checker-validated
witnesses). Machine cross-checks: the 52 refutations are instances of the lemma; the K4 and
Petersen controls of EXP-004 are consistent.

## Setting

`P` is the Petersen graph, `G` a cubic graph, and `sigma : E(G) -> E(P)` any map. A vertex `v`
of `G` is good if `sigma` maps the three edges at `v` bijectively onto the three edges at some
vertex `w_v` of `P`, and bad otherwise. The Petersen defect of `G` is the least number of bad
vertices over all maps `sigma`; a Petersen coloring is a map of defect 0.

Write `chi(S)` for the indicator vector in `GF(2)^{E(P)}` of a multiset `S` of edges of `P`
(edges counted mod 2). For a vertex `v` of `G` put `chi_v = chi(sigma(d_G(v)))`, where
`sigma(d_G(v))` is the multiset of the three labels at `v`.

## Lemma 1 (parity)

For every map `sigma`, `sum over all v in V(G) of chi_v = 0`.

Proof. Every edge `e` of `G` has two endpoints, so its label `sigma(e)` is counted twice in the
sum, and twice is zero mod 2.

## Lemma 2 (good stars are cuts)

If `v` is good then `chi_v = chi(d_P(w_v))`, the indicator of the star of `w_v` in `P`, which is
an edge cut of `P` (the cut of the single vertex `w_v`). The stars of `P` span the cut space
(bond space) of `P` over `GF(2)`, a subspace of dimension `|V(P)| - 1 = 9`.

## Lemma 3 (odd cuts of the Petersen graph)

Every edge cut of `P` of size 1 or 3 is a star, and no cut has size 1.

Proof. `P` is bridgeless, so no cut has size 1. Let `d(S)` be a cut of size 3 with sides `S`
and `T`. `P` has cyclic edge connectivity 5 (a classical fact: the smallest cycle-separating
cuts of the Petersen graph are the 5-edge boundaries of its 5-cycles), so `S` or `T` induces a
forest; say `S` induces a forest with `c` components. Counting degrees, `|d(S)| = 3|S| -
2(|S| - c) = |S| + 2c >= |S| + 2`, so `|S| + 2 <= 3` gives `|S| = 1`: the cut is a star.

## Theorem (the defect is never 1)

For every cubic graph `G` and every map `sigma : E(G) -> E(P)`, the number of bad vertices is
not 1. Consequently the Petersen defect of a cubic graph is either 0 (a Petersen coloring
exists) or at least 2.

Proof. Suppose `v` is the only bad vertex. By Lemma 1 and Lemma 2,
`chi_v = sum over good u of chi(d_P(w_u))`, a sum of stars, hence an element of the cut space
of `P`. The vector `chi_v` has odd weight: weight 3 if the three labels at `v` are distinct, and
weight 1 if two of them coincide (the third label survives; the repeated label cancels) or all
three coincide. Weight 1 is impossible by Lemma 3. Weight 3 forces the three distinct labels to
form a 3-edge cut of `P`, which by Lemma 3 is a star `d_P(w)`; then `sigma` maps the star of `v`
bijectively onto the star of `w`, so `v` is good, a contradiction.

## Corollary (the smallest known counterexample is extremal)

Every counterexample to the Petersen coloring conjecture has Petersen defect at least 2. The
52-vertex counterexample of Goedgebeur, Jooken, Macajova, Mattiolo and Mazzuoccolo has defect
exactly 2, and every one of its 1,326 vertex pairs is a critical pair: for each pair there is an
edge map that is a Petersen coloring except exactly at those two vertices (EXP-006, explicit
witnesses re-verified by the checker `[MV]`).

## Remarks

- The same argument gives a necessary condition on any bad set `B`: `sum over v in B of chi_v`
  lies in the cut space of `P`. For `|B| = 2` this says the symmetric difference of the two
  label multisets (as indicator vectors) is a cut of `P`, which is easy to satisfy and is
  consistent with every pair being critical.
- The theorem does not use anything about `G` beyond cubicity; it applies to graphs with
  bridges and to multigraphs alike.
- An analogous statement for the normal-5 defect (edges that are neither poor nor rich) does
  not follow from this argument; the normal-5 defect is left as a lower bound in this round.
