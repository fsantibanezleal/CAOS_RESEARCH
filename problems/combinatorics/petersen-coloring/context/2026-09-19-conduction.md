# Conduction of cut-space classes through 4-poles (2026-09-19)

Marks as in `2026-09-18-defect-unbounded.md`. `P` is the Petersen graph, `Cut(P)` its cut space in
`F_2^{E(P)}`, `L(P)` its line graph (diameter 3; from a fixed edge, 4 edges at distance 1, 8 at
distance 2, 2 at distance 3).

## Lemma 1 (small cuts of P) `[D]`

The cuts of `P` with at most four edges are the empty cut, the ten stars, and the fifteen sets of
four edges adjacent to one edge. Proof: `P` is 3-edge-connected and cyclically 5-edge-connected
with girth 5. For a vertex set `S`, `|δ(S)| = 3|S| - 2e(S)`; if `S` induces a forest with `c`
components this is `|S| + 2c`, which is 3 only for a single vertex and 4 only for two adjacent
vertices; if both sides contain cycles, `|δ(S)| >= 5`.

## Lemma 2 (the class of a pair of labels is its distance) `[D]`

For edges `x, y` of `P` let `[x, y]` be the class of `1_x + 1_y` modulo `Cut(P)`. Then
`[x, y] = [x', y']` implies `d(x, y) = d(x', y')`, where `d` is the distance in `L(P)`.

Proof. `[x, y] = 0` exactly when `x = y`, because a nonzero vector of weight 2 is not a cut. If
`x != y`, `x' != y'` and the classes agree, the symmetric difference of `{x, y}` and `{x', y'}` is a
cut of even weight at most 4: either empty (the same pair) or the four edges around an edge `st`
of `P`. In the second case the two pairs are either the two edges at `s` and the two at `t` (both at
distance 1) or each pair has one edge at `s` and one at `t` (both at distance 2, through `st`,
since `P` has no triangle). QED

So a class carried by two edges has a well-defined distance in `{0, 1, 2, 3}`; distance 1 is the
class of a single edge (the third edge at the common vertex).

## Lemma 3 (conduction) `[D]`

Let `M` be a 4-pole (a cubic graph with some vertices or edges removed and exactly four dangling
ends) whose dangling ends are paired into connectors `{p, q}` and `{r, s}`. For every map of `M`
into `E(P)` in which every vertex of `M` is good, `d(s(p), s(q)) = d(s(r), s(s))`.

Proof. The sum of the label vectors of the vertices of `M` is a sum of stars, hence a cut; an
internal edge is counted twice, so the sum equals `1_s(p) + 1_s(q) + 1_s(r) + 1_s(s)`. Hence the two
connectors have the same class, and by Lemma 2 the same distance. QED

`D(M)`, the conducted set, is the set of distances realized at `{p, q}` by such maps. It depends on
the pairing.

## Theorem 4 (alternating rings) `[D]`

Let `A`, `B` be 4-poles with paired connectors and `D(A)` disjoint from `D(B)`. Let `R_t(A, B)` be
the cubic graph made of `t` copies of `A` and `t` copies of `B` alternating around a cycle, the
second connector of each block joined by two edges to the first connector of the next. Then every
map `E(R_t) -> E(P)` has a bad vertex in at least `t` blocks, so `ab(R_t) >= pd(R_t) >= t`.

Proof. The two edges between consecutive blocks form a connector of both. If two consecutive
blocks had only good vertices, Lemma 3 applied to each would put the distance of their common
connector in `D(A)` and in `D(B)`. So no two consecutive blocks are both free of bad vertices, and
at least half of the `2t` blocks contain one. QED

Remarks.
- For `A = G - ab - cd`, `G` without a Petersen coloring, with connectors `{a, b}`, `{c, d}`,
  distance 0 is never conducted: it would give `s(a) = s(b)`, then `s(c) = s(d)` by Lemma 3, and
  `G` would be restored. EXP-010 found 282 edge pairs of `G52` with `D(A) = {1}`.
- The ring theorem is the 4-pole analogue of the ring and frame theorems of
  `2026-09-18-defect-unbounded.md`: there, 2- and 3-edge boundaries force a restorable pattern;
  here, two different 4-poles force incompatible conducted classes.
- If `A`, `B` are cyclically 4-edge-connected 4-poles (every vertex set containing a cycle has at
  least four boundary edges, dangling ends included) and `R_3(A, B)` is cyclically
  4-edge-connected, it is a cyclically 4-edge-connected cubic graph of Petersen defect at least 3,
  and statement (e) of Mattiolo et al. is false by Theorem 6 of that note (EXP-012 tests this).

## Lemma 5 (restoration) `[D]`

Let `G` be a cubic graph without a Petersen coloring.

(a) For independent edges `ab`, `cd` of `G`, the 4-pole `G - ab - cd` with connectors `{a, b}`,
`{c, d}` does not conduct distance 0. (Distance 0 at `{a, b}` gives `s(a) = s(b)`; by Lemma 3 also
`s(c) = s(d)`; restoring `ab` and `cd` with these labels colors `G`.)

(b) For an edge `uv` of `G` with other neighbours `u1, u2` of `u` and `v1, v2` of `v`, the 4-pole
`G - {u, v}` with connectors `{u1, u2}`, `{v1, v2}` does not conduct distance 1. (Distance 1 at both
connectors, with equal classes, means both pairs share a vertex of `P` with the same third edge
`z`; labelling `uv` by `z` colors `G`.)

## Lemma 6 (rings of the two 4-poles are cyclically 4-edge-connected) `[D]` with a computed base

Let `G` be cyclically 4-edge-connected (hence 3-edge-connected and 3-connected), `A = G - ab - cd`,
`B = G - {u, v}` as in Lemma 5, and `R_t = R_t(A, B)` the alternating ring (`A`'s connector `{c, d}`
joined to `B`'s `{u1, u2}`, `B`'s `{v1, v2}` joined to the next `A`'s `{a, b}`). If `R_2` has no
cycle-separating edge cut with at most three edges, then every `R_t`, `t >= 2`, is cyclically
4-edge-connected.

Block properties used (proofs from the cyclic 4-edge-connectivity of `G`):
- (a) both blocks are connected;
- (b) (holds, but the proof below does not need it) if `S` is a vertex set of a block containing a
  cycle, at least four edges leave `S` inside the ring (internal edges to the rest of the block plus
  the dangling ends at `S`): for `A` this count is at least `|δ_G(S)|`, for `B` it equals
  `|δ_G(S)|`, and `|δ_G(S)| >= 4` unless `V(G) - S` is a forest; that forest has at least the two
  vertices `u`, `v` for `B`, and for `A` it is empty (the four dangling ends leave) or a single
  vertex `w` (at least five edges leave: 3 + 4, or 2 + 3 when `w` is an end of `ab` or `cd`);
- (c) in each block, with a new vertex `s*` on the two first-connector ends and `t*` on the two
  second-connector ends, there are two edge-disjoint `s*`-`t*` paths: for `B` this graph is `G - uv`
  with `u`, `v` renamed `s*`, `t*`, and `λ_G(u, v) >= 3`; for `A` a single separating edge would be
  a bridge of `G` or would disconnect `A`.

Proof. Let `K` be a cycle-separating cut of `R_t` with at most three edges, sides `S`, `S'`. By (c)
the ring carries four edge-disjoint paths between any two blocks (two along each arc), so no block
lies entirely in `S` while another lies entirely in `S'`; say every unsplit block lies in `S`. By
(a) every split block contains an edge of `K`, so at most three blocks are split and `S'` lies in
them. A cycle of `R[S']` lies in one maximal run `Y` of consecutive split blocks (at most three
blocks, bounded by unsplit blocks on both sides), and the edges leaving `S' ∩ V(Y)` form a
cycle-separating cut of size at most `|K|` whose size depends only on `Y` and `S' ∩ V(Y)`. The same
configuration occurs in `R_2 = ABAB`, which contains every alternating run of at most three blocks
followed by at least one block on the other side, contradicting the hypothesis on `R_2`. QED

## Theorem 7 (cyclically 4-edge-connected cubic graphs of unbounded Petersen defect) `[D]` + `[MV]`

For `G = G52`, `ab = (0, 3)` (edge 0), `cd = (1, 9)` (edge 4), `uv = (2, 7)`, and every `t >= 2`,
the ring `R_t` is a cyclically 4-edge-connected cubic graph of girth 5 on `102 t` vertices with
`pd(R_t) >= t` and `ab(R_t) >= t`.

Ingredients: `G52` has no Petersen coloring (EXP-001, and the proof of arXiv:2608.10028v3); `D(A)
= {1}` (distance 0 by Lemma 5(a), distances 2 and 3 refuted with verified proofs in EXP-010 and
EXP-012); `D(B) = {0}` (distance 1 by Lemma 5(b), distances 2 and 3 refuted with verified proofs in
EXP-012); `D(A)` and `D(B)` are disjoint, so Theorem 4 gives the defect bound (either of the two
computed restrictions alone suffices, with the corresponding part of Lemma 5); `R_2` has no
cycle-separating cut below 4 (EXP-012, bridge search, cross-checked), so Lemma 6 gives cyclic
4-edge-connectivity for all `t >= 2`; girth 5 is local and read on `R_2`.

Corollary 8. There is no sublinear function bounding the number of abnormal edges of proper
5-edge-colorings on cyclically 4-edge-connected cubic graphs: statement (e) of Mattiolo,
Mazzuoccolo, Mkrtchyan is false, so all five statements of their Conjecture 3 are false and the
conjectured equivalence holds. In Theorem 6 of `2026-09-18-defect-unbounded.md` the four
equivalent statements are therefore all false, and the observation that every adjacent pair of
fifteen cyclically 4-edge-connected counterexamples is critical did not reflect the class: `R_2`
has non-critical adjacent pairs (two bad vertices must sit in non-adjacent blocks) and `R_3` has no
critical pair at all.
