# The Petersen defect and the number of abnormal edges are unbounded (2026-09-18)

Marks: `[D]` derived here with a full proof; `[V]` verified in the primary source; `[MV]` machine
verified in this repository.

## Definitions

`P` is the Petersen graph. For a cubic graph `G` and a map `s : E(G) -> E(P)`, a vertex `v` is
*good* if `s` maps the star of `v` bijectively onto a star of `P`, and *bad* otherwise. The
*Petersen defect* `pd(G)` is the least number of bad vertices over all maps (EXP-004, EXP-006).
For a proper 5-edge-coloring `c`, an edge `uv` is *abnormal* if the number of colors on the two
end stars is 4 (neither 3 nor 5); `ab(G)` is the least number of abnormal edges over all proper
5-edge-colorings (they exist for every cubic graph by Vizing's theorem). Goedgebeur et al.
(arXiv:2608.10028v3, Question 12, quoting Mattiolo, Mazzuoccolo, Mkrtchyan) `[V]` record that the
five known counterexamples have `ab <= 2` without being normally 5-edge-colorable.

Known `[MV]`: `pd = 2` for `G52`, `G112`, `H112`; `ab(G52) = 2`. Parity theorem `[D]`
(`2026-09-03-defect-parity-lemma.md`): for any map, the sum over the bad vertices of the label
vectors `chi_v` lies in the cut space of `P`; in particular `pd` is never 1.

## Lemma 1 (`pd <= ab`) `[D]`

For every cubic graph `G`, `pd(G) <= ab(G)`.

Proof. View `P` as the Kneser graph `K(5,2)`: vertices are the 2-subsets of `{1..5}`, edges the
disjoint pairs, and the *color* of an edge `{A, B}` is the element outside `A + B`; the three
edges at `A` have the three colors outside `A`. Let `c` be a proper 5-edge-coloring with set of
abnormal edges `N`. For a vertex `v` put `A_v = {1..5} - c(star of v)`. For an edge `e = uv` the
*view from `u`* is the edge of `P` at `A_u` of color `c(e)`. If `e` is poor then `A_u = A_v` and
the two views coincide; if `e` is rich then `A_u` and `A_v` are disjoint, both avoid `c(e)`, and
both views are the edge `{A_u, A_v}`. Define `s(e)` as the common view when `e` is normal and as
the view from one chosen end when `e` is abnormal. A vertex all of whose edges carry its own view
is good (its star maps onto the star of `A_v`). So every bad vertex is the non-chosen end of an
abnormal edge, and the number of bad vertices is at most `|N|`. QED

## Theorem 2 (rings) `[D]`

Let `G_1, ..., G_t` (`t >= 2`) be cubic graphs without a Petersen coloring (not necessarily
distinct), `e_i = a_i b_i` an edge of `G_i`, and let the *ring* `R` be obtained from the disjoint
union of the graphs `G_i - e_i` by adding the edges `c_i = a_i b_{i+1}` (indices modulo `t`). Then
every map `E(R) -> E(P)` has a bad vertex in every `V(G_i)`. Hence `ab(R) >= pd(R) >= t`. If every
`G_i` is bridgeless, so is `R`.

Proof. Fix `i` and suppose every vertex of `V(G_i)` is good. Over `F_2`, the sum of the label
vectors `chi_v`, `v` in `V(G_i)`, is the indicator of `{s(c_i)}` plus the indicator of
`{s(c_{i-1})}`, since an edge inside `V(G_i)` is counted twice and exactly the two ring edges
`c_i` (at `a_i`) and `c_{i-1}` (at `b_i`) leave `V(G_i)`. Each `chi_v` is the indicator of a star
of `P`, a cut. So the sum is a cut of `P` with at most 2 edges, hence empty because `P` is
3-edge-connected: `s(c_i) = s(c_{i-1}) = x`. Give `e_i` the label `x` and keep `s` elsewhere on
`G_i`: the stars at `a_i` and `b_i` carry the same labels as in `R`, so this is a Petersen
coloring of `G_i`, a contradiction. For bridgelessness: every `G_i - e_i` is connected, so `R` has
a cycle through all ring edges and no ring edge is a bridge. Let `f` be an edge of `G_i - e_i`.
Since `G_i - f` is connected, any two vertices of `V(G_i)` are joined in `G_i - f` by a path that
may use `e_i`; in `R - f` the edge `e_i` can be replaced by the detour from `a_i` around the ring
to `b_i`, which avoids `f`. So `R - f` is connected. QED

## Theorem 3 (frames, 3-edge-connected) `[D]`

Let `F` be a cubic graph with `t` vertices (the frame), and for each vertex `x` of `F` let `G_x`
be a cubic graph without a Petersen coloring and `v_x` a vertex of `G_x`. Replace every vertex `x`
of `F` by `G_x - v_x`, attaching the three edges of `F` at `x` to the three neighbours of `v_x`.
Then every map from the edges of the resulting cubic graph to `E(P)` has a bad vertex in every
`V(G_x - v_x)`, so `ab >= pd >= t`. If `F` and all `G_x` are 3-edge-connected, so is the result.

Proof. If all vertices of `V(G_x - v_x)` are good, the sum of their label vectors is a cut of `P`
and equals the sum of the indicators of the labels of the three leaving edges; it has odd weight,
since the number of summands `|V(G_x)| - 1` is odd and every star has weight 3. Weight 1 is
impossible (`P` is bridgeless), so the three labels are distinct and form a 3-edge cut of `P`,
which is a star because `P` is cyclically 5-edge-connected (the argument of the parity theorem).
Restoring `v_x` with these three labels on its edges gives a Petersen coloring of `G_x`. The
connectivity statement is the standard 3-cut substitution. QED

## Consequences

- There is no constant bounding the Petersen defect of bridgeless cubic graphs, and none bounding
  the least number of abnormal edges of a proper 5-edge-coloring, already among 3-edge-connected
  cubic graphs. This complements the negative answer to Question 12 of v3: not only does `ab <= 2`
  fail to imply normal 5-edge-colorability, `ab` takes arbitrarily large values.
- The constructions have cyclic edge connectivity 2 or 3. Open: is `pd` (or `ab`) bounded on
  cyclically 4-edge-connected cubic graphs? All five known counterexamples with that connectivity
  have `pd = 2`.
- Exact values for small rings and frames built from `G52`: EXP-009.
