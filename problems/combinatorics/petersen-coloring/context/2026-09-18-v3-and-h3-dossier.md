# Source dossier addendum: version 3 of the disproof paper and the set H_3 (2026-09-18)

Marks as in `2026-09-03-source-dossier.md`. Sources stored under
`E:/_Datos/caos-research/petersen-coloring/sources/arxiv/`: `gjmmmu-2608.10028v3.pdf` (271,957
bytes, SHA-256 `c17a6fdf0fd1b0ec5c9d6f18aa21cb91b370ebcb3759749479b56dc6c849fe0d`), text
`gjmmmu-v3.txt`; `mmsw-2305.08619.pdf`, text `mmsw.txt`.

## 1. Goedgebeur, Jooken, Macajova, Mattiolo, Mazzuoccolo, Ulyanov, arXiv:2608.10028v3 (2026-09-11) `[V, read in full]`

New title: "Disproving the Petersen Coloring Conjecture: Theoretical Analysis and an Infinite
Family of Counterexamples". It supersedes Jooken's v2 note and the Zenodo first version.

- Two counterexamples of order 52 with a purely theoretical proof (Theorem 5), House of Graphs
  ids 57244 and 57278 (the site was not reachable from this machine on 2026-09-18 `[U]`; our
  `G52` is the graph printed in the first version's appendix).
- Theorem 7: a cyclically 4-edge-connected cubic graph without a Petersen coloring exists for
  every even order at least 60.
- Observation 9: the smallest counterexample has at least 40 and at most 52 vertices. The lower
  bound uses Brinkmann and Van Overberghe's list of all 7,142,217,899 weak snarks on 38
  vertices; the check took about 12 CPU years. "It is well-known that a smallest counterexample
  must be a weak snark."
- Problem 8 (smallest counterexample), Problem 10 (cyclically 5-edge-connected
  counterexamples), Conjecture 11 (normal 6-edge-colorings, attributed to Samal).
- The 68-vertex counterexample is credited to GPT-5.6 Sol Ultra, posted by `@NeuralReformist`.
- Their computational checks on the two 52-vertex, the 68-vertex and the two 112-vertex graphs:
  strong normal 6-edge-colorings (normal chromatic index exactly 6); Berge-Fulkerson holds and
  the perfect matching index is at most 4; 5-cycle double covers exist; each admits a proper
  5-edge-coloring with exactly two abnormal edges, answering Question 3.1 of Mattiolo,
  Mazzuoccolo, Mkrtchyan negatively; the graphs also refute the `P12`-coloring conjecture of
  Hakobyan and Mkrtchyan (any cubic graph with perfect matching index at most 4 admits a
  `P12`-coloring), since `P12` is Petersen colorable.
- Section 5.4: the set `H_b` of bridgeless cubic graphs colorable only by themselves is the
  unique minimal family coloring every bridgeless cubic graph (Ma-Mattiolo-Steffen-Wolf), it is
  infinite, and "it would be interesting to investigate whether our counterexamples of order 52
  are also colorable only by themselves. This question is of particular relevance, as it is
  naturally tied to the question whether they are the smallest bridgeless cubic graphs without a
  Petersen coloring." EXP-007 attacks exactly this.
- No notion of a vertex defect, no parity statement, no oddness, resistance or flow values.

## 2. Timeline and overlap with the CAOS record (honest statement)

CAOS preprint v0.01 (Zenodo 10.5281/zenodo.22285165) is dated 2026-09-03; v3 is dated
2026-09-11. Both report, independently: Berge-Fulkerson covers, perfect matching index at most
4, 5-cycle double covers, and (strong) normal 6-edge-colorings of the 112-vertex graphs and of a
52-vertex graph. v3 covers more graphs (the second 52 and the 68). The next CAOS manuscript
version must cite v3 for these items and state the concurrency. What remains specific to the
CAOS record: exact index 4 (their statement is "at most 4", ours adds the snark lower bound,
the same one-line argument), oddness and resistance, nowhere-zero 5-flows, the Petersen defect
with the parity theorem and universal 2-criticality, the pure-`F` proposition, and the
independent certification with a second encoding. v3's two-abnormal-edge colorings settle the
upper bound of the normal-5 defect (at most 2); our single-edge relaxation sweep of `G52`
(40 of 78 edges refuted with verified proofs when it was interrupted) is the matching lower
bound in progress.

## 3. Ma, Mattiolo, Steffen, Wolf, "Sets of r-graphs that color all r-graphs", Combinatorica 45 (2025), Article 16, arXiv:2305.08619 `[V, Sections 1 and 3.2 read]`

- Graphs are finite, may have parallel edges, no loops. An `H`-coloring of `G` is
  `f : E(G) -> E(H)` with adjacent edges receiving distinct images and, for every vertex `v`,
  `f(d_G(v)) = d_H(u)` for some vertex `u` of `H`. `H` colors `G` is written `H < G`; the
  relation is transitive.
- For `r = 3`, an `r`-graph is a bridgeless cubic graph. `H_r` is an inclusion-wise minimal set
  of connected `r`-graphs coloring every connected `r`-graph; it is unique (Corollary 3.8).
- Theorem 3.4: if `G` is a class 2 `r`-graph that cannot be colored by an `r`-graph of smaller
  order, then every `H`-coloring of `G` by a connected `r`-graph `H` is an isomorphism.
- Theorem 3.7: for a connected `r`-graph `G` the following are equivalent: `G` is in `H_r`;
  the only connected `r`-graph coloring `G` is `G` itself; `G` cannot be colored by a smaller
  `r`-graph.
- Observation 3.1: an `H`-coloring pulls back disjoint perfect matchings and 2-regular
  subgraphs, and `chi'(G) <= chi'(H)`.
- Either `H_3 = {P}` or `H_3` is infinite; after the disproof it is infinite.

Consequence used by EXP-007 `[D]`: if a connected bridgeless cubic `H` colors a counterexample
`G`, then `H` is itself a counterexample (otherwise `P < H < G`). So deciding, for every even
`k < 52`, whether some bridgeless cubic multigraph on `k` vertices colors `G52` either produces
a counterexample smaller than 52 or proves `G52` is in `H_3`.
