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
