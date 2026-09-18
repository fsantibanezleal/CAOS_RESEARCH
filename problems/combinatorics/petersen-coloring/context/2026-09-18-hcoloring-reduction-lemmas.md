# Two reduction lemmas for H-colorings with an unknown target (2026-09-18)

Marks: `[D]` derived here with a full proof, `[V]` verified against the primary source.
Setting: `G` a connected cubic graph on `n` vertices, `H` a connected bridgeless cubic multigraph
(parallel edges allowed, no loops), `f : E(G) -> E(H)` an `H`-coloring, and `phi : V(G) -> V(H)`
a vertex map with `f(d_G(v)) = d_H(phi(v))` for every `v` (one exists by definition; it is unique
unless `H` is the triple edge). For `x` in `V(H)` write `n_x = |phi^{-1}(x)|` (the fiber size);
`x` is *used* if `n_x > 0`. `U` is the set of used vertices, `W` its complement.

## Lemma A (fiber parity) `[D]`

For every edge `e = xy` of `H`, the preimage `f^{-1}(e)` is a matching of `G` whose set of covered
vertices is exactly `phi^{-1}(x) + phi^{-1}(y)`. Hence `n_x + n_y` is even for every edge `xy`, and,
`H` being connected, all fiber sizes have the same parity.

Proof. A vertex `v` of `G` is incident with an edge of image `e` if and only if `e` lies in
`f(d_G(v)) = d_H(phi(v))`, that is, if and only if `phi(v)` is `x` or `y`. It is incident with at
most one such edge because `f` is injective on `d_G(v)`. So `f^{-1}(e)` is a perfect matching of
the subgraph induced on `phi^{-1}(x) + phi^{-1}(y)`, whose order is therefore even. QED

Consequences. Either every fiber is odd, and then `phi` is onto (mode O), or every fiber is even,
and then at most `n/2` target vertices are used (mode E).

## Lemma B (unused target vertices reduce to at most one) `[D]`, using the splitting lemma `[V]`

Suppose `W` is not empty and let `m = |d_H(W)|`. Then there is a connected bridgeless cubic
multigraph `H'` with vertex set `U + W'`, where `W'` is empty if `m` is even and a single vertex
if `m` is odd, and an `H'`-coloring of `G` with the same vertex map `phi`. In particular
`|V(H')| <= |V(H)|`.

Splitting lemma, in the form of Kaiser, Kuzel, Li, Wang, "A note on k-walks in bridgeless
graphs", Graphs Combin. 23 (2007) (journal data `[U]`), Lemma 1 `[V, read in the authors' PDF, SHA-256 94bda692...946f]`,
who derive it from Fleischner's Splitting Lemma (Discrete Math. 101 (1992) 33-37) and Zhang,
"Integer flows and cycle covers of graphs", Theorem A.5.2: graphs are finite and loopless with
multiple edges allowed; if `v` has degree at least 4 in a bridgeless graph `K`, there are edges
`e1, e2` at `v` such that splitting them off `v` (a new vertex `v*` takes over the ends of `e1`
and `e2` at `v`) gives a bridgeless graph. Connectedness is not part of this form and is proved
separately below.

Proof of Lemma B. Every edge with an end in `U` is an image of `f` (the star of a used vertex is
the image of a star), and no edge inside `W` is. Identify `W` to a single vertex `w*` and delete
the loops. Every edge cut of the new graph `H_1` is an edge cut of `H`, so `H_1` is bridgeless;
`w*` has degree `m >= 2`, and every other vertex is a used vertex with its star intact.
While `deg(w*) >= 4`, split a pair of edges `a w*`, `b w*` off `w*` so that the result is
bridgeless, and suppress the new vertex of degree 2, replacing its two edges by one edge `ab`.
Here `a != b`: otherwise the new vertex would be joined to the cubic vertex `a` by two parallel
edges and the third edge at `a` would be a bridge. Suppressing a vertex of degree 2 keeps the
graph bridgeless and loopless. The degree of `w*` drops by 2 each time. At the end `deg(w*)` is 2
(same argument: suppress it) or 3 (keep it as the single unused vertex). Call the result `H'`; it
is cubic, loopless and bridgeless. It is connected: for an edge `uv` of `G` with
`phi(u) != phi(v)` the edge `f(uv)` joins `phi(u)` to `phi(v)`, has both ends in `U` and was never
touched, so `U` is connected in `H'` because `G` is connected; and `w*`, if kept, is joined to `U`.
Let `mu` send each edge of `H` with an end in `U` to the edge of `H'` that contains it. For a used
vertex `u`, `d_{H'}(u) = mu(d_H(u))` and `mu` is injective on `d_H(u)` (the two edges merged in one
step have distinct ends `a != b` away from `w*`, so two edges at the same used vertex are never
merged). So `mu o f` is an `H'`-coloring with vertex map `phi`. QED

## Corollary (the search space of EXP-007) `[D]`

`G` is colored by a connected bridgeless cubic multigraph of order less than `n` if and only if it
is colored by one, of even order `k < n`, with a vertex map in one of the modes

- O: `phi` onto, every fiber odd;
- E0: `phi` onto, every fiber even (so `k <= n/2`);
- E1: exactly one unused vertex, every other fiber even and positive (so `k - 1 <= n/2`).

For `n = 52`: mode O for every even `k <= 50`; modes E0 and E1 only for `k <= 26`. In mode O with
`k = 50` the fibers are forty-nine singletons and one triple.

Remarks. With at most one unused vertex the target is connected automatically (the image of a
connected graph is connected through used edges, and the unused vertex has all three edges going
to used vertices); bridges remain possible and are still excluded lazily.
