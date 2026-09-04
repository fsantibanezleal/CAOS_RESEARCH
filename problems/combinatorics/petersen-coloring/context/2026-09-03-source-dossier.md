# Source dossier: the 2026 disproof of the Petersen coloring conjecture (2026-09-03)

Marks: `[V]` read in the primary source (full text under `E:/_Datos/caos-research/petersen-coloring/sources/`),
`[MV]` machine-verified in this repository, `[D]` derived here, `[U]` unverified. Every claim below
carries one mark. Secondary sources may guide; they never certify.

## 1. Definitions (transcribed)

- Multipole, `k`-pole, semi-edge, join: Jooken Section 1 `[V]`. A multipole may have semi-edges
  (edges with one end); a `k`-pole has exactly `k`; joining two semi-edges deletes both and adds
  the edge between their vertices.
- `H`-coloring: for a cubic multipole `G` and graph `H`, total maps `sigma: E(G) -> E(H)` and
  `tau: V(G) -> V(H)` with `sigma` a proper edge coloring and `sigma(d_G(u)) = d_H(tau(u))` for
  every vertex `u`; `sigma` is an `H`-coloring (Jooken Section 1 `[V]`; Putman Section 1 in the
  bijective form "the three incident edges map bijectively to the three edges incident with some
  vertex of `H`" `[V]`). A Petersen coloring (P-coloring) is an `H`-coloring with `H = P`, the
  Petersen graph.
- Normal 5-edge-coloring: a proper 5-edge-coloring in which every edge is poor (three colors on
  its two endpoint stars) or rich (five) (Putman Section 2 `[V]`); Mazzuoccolo-Mkrtchyan: "the
  set of colors on any edge and the four adjacent edges has exactly five or exactly three
  distinct colors" `[V, abstract]`. The normal chromatic index `chi'_N(G)` is the least such `k`.
- P-coloring set of a 4-pole: `P-Col(M) = {(sigma(a), sigma(b), sigma(c), sigma(d))}` over all
  P-colorings `sigma` of `M`, for semi-edges `a, b, c, d` (GJMMM Section 2 `[V]`).
- Cyclic `k`-edge-connectivity: no set of fewer than `k` edges separates the graph into two
  components each containing a cycle (GJMMM introduction `[V]`).
- Weak snark: cyclically 4-edge-connected cubic graph of girth at least 4 that is not
  3-edge-colorable; snark: weak snark of girth at least 5 (GJMMM Section 5, attributing the
  definitions to Brinkmann et al. `[V]`).

## 2. The conjecture and its implication ladder

- Jaeger 1988, "Nowhere-zero flow problems", Selected Topics in Graph Theory 3, Academic Press,
  71-95: every bridgeless cubic graph has a P-coloring (cited as the origin by Putman [2], Jooken
  [5], GJMMM [4] `[V]`; the 1988 chapter itself is not read here `[U]`).
- Jaeger 1985, "On five-edge-colorings of cubic graphs and nowhere-zero flow problems", Ars
  Combinatoria 20-B, 229-244: a cubic graph has a P-coloring iff it has a normal 5-edge-coloring
  (Putman Proposition 2.1 gives a bijective form and proves it in Kneser notation `[V]`; GJMMM
  Section 5 cites it `[V]`).
- The conjecture implies the Berge-Fulkerson conjecture (six perfect matchings covering every
  edge exactly twice) and the 5-cycle double cover conjecture (Jooken Section 1: "If true, this
  conjecture would imply simultaneously the famous Berge-Fulkerson conjecture [3] and the 5-cycle
  double cover conjecture [2, 12]" `[V]`; Mazzuoccolo-Mkrtchyan abstract `[V]`; Open Problem Garden
  entry `[V]`). The Berge conjecture (perfect matching index at most 5) and the Fan-Raspaud
  conjecture (three perfect matchings with empty intersection) are consequences of
  Berge-Fulkerson (standard; `[U]` as to a specific primary citation, `[D]` trivially: five of
  the six Fulkerson matchings cover, and any three of them meet in no edge since every edge is
  in exactly two).
- 3-edge-colorable cubic graphs are P-colorable (Open Problem Garden: "trivially true for all
  3-edge-colorable cubic graphs" `[V]`; `[D]`: map the three color classes onto the three edges
  at one vertex of `P`... this maps every star onto the same star, which is a valid P-coloring).
- Universal target families: Ma, Mattiolo, Steffen, Wolf, "Sets of r-graphs that color all
  r-graphs", Combinatorica 45 (2025), Article 16, doi:10.1007/s00493-025-00144-4. Putman's
  Corollary 5.1 uses their Theorem 4.8(i) and Theorem 1.1 to conclude that one counterexample
  yields infinitely many connected simple bridgeless cubic counterexamples and that the minimal
  3-complete family `H_3` is infinite `[V, Putman Section 5]`.

## 3. Verification frontier before August 2026

- Brinkmann, Goedgebeur, Hagglund, Markstrom, "Generation and properties of snarks", JCTB 103
  (2013), 468-488, doi:10.1016/j.jctb.2013.05.001, arXiv:1206.6690: all snarks on at most 36
  vertices generated; "some of the strongest versions of the cycle double cover conjecture hold
  for all snarks of these orders, as does Jaeger's Petersen colouring conjecture, which in turn
  implies that Fulkerson's conjecture has no small counterexamples" `[V, abstract]`. GJMMM add
  that they verified every weak snark on at most 34 vertices `[V, GJMMM Section 5]`.
- Goedgebeur, Macajova, Skoviera, "Smallest snarks with oddness 4 and cyclic connectivity 4 have
  order 44", Ars Math. Contemp. 16 (2019), 277-298: completed the order-36 case for weak snarks
  of girth 4, so the conjecture has no counterexample on at most 36 vertices; "it is well-known
  that a smallest counterexample to the Petersen Coloring Conjecture must be a weak snark"
  (GJMMM Section 5 `[V]`; the reduction argument itself is not reproduced here `[U]`).
- Consequently every counterexample has at least 38 vertices (GJMMM `[V]`).
- Structured families known to be P-colorable: Hagglund-Steffen 2014 (Ars Math. Contemp. 7,
  161-173, doi:10.26493/1855-3974.288.11a); Ferrarini-Mazzuoccolo-Mkrtchyan 2020 (Loupekhine
  snarks); Sedlar-Skrekovski 2024 (superpositioned snarks); Zhou-Hao-Luo-Luo 2026 (Putman's
  reference list `[V]`; the papers themselves `[U]`).

## 4. The disproof

### 4.1 Putman, arXiv:2608.10012 (2026-08-06 Zenodo v1.0.0, DOI 10.5281/zenodo.21819153; v1.1.0 2026-08-08, DOI 10.5281/zenodo.21845291) `[V]`

- Theorem 1.1: a simple connected bridgeless cubic graph `G` with 112 vertices and 168 edges,
  no Petersen coloring, no normal 5-edge-coloring, girth 5, edge- and vertex-connectivity 3;
  digest of the normalized sorted edge list (ASCII JSON, `[u,v]` with `u<v`, lexicographic,
  compact separators) `dc16cc18600cf77c8661b7baf89c7019f265299308541961ff884ea7187b4e8b`.
- Construction: `F` is the Petersen graph minus the endpoints of one edge (an 8-vertex 4-pole
  with 10 edges); `C` a claw six-pole; `L = 4F + C` (36 vertices); `G = 3L + C`.
- Verification: two direct SAT encodings (Petersen: 3,640 variables, 68,324 clauses; normal-5:
  1,960 variables, 25,484 clauses), CaDiCaL 3.0.1, drat-trim; all archived with SHA-256.
- Corollary 5.1: infinitely many counterexamples (via Ma-Mattiolo-Steffen-Wolf).
- Section 6: a nonisomorphic `D3`-symmetric counterexample `H` (three copies of a 36-vertex
  4-pole `Q`, a center and three leaves), digest
  `0f2d8858110c6f012de7ddffa92fdbc709d7da630f199b0e3c81bb56eb6b35c7`, automorphism group of
  order 6.
- "We do not address whether 112 is minimum."
- AI statement: "OpenAI language-model systems were used extensively in the discovery,
  computational search, verification, and preparation of this work."
- Artifacts: Zenodo record 21845291 v1.1.0 (five files; manifest, ancillary, DRAT archive of
  277,279,647 bytes with four proofs), all downloaded and hash-verified `[MV, EXP-001]`.

### 4.2 Jooken, arXiv:2608.10028v2 (2026-08-14) `[V]`

- Lemma 2.1 (P-colorings of `F`, semi-edges `i1, i2, o1, o2`; `Q` the line graph of `P`):
  `dist_Q(sigma(i1), sigma(i2)) <= 2`; at distance 0 all four semi-edge labels coincide; at
  distance 1, `sigma(o1) = sigma(i1)` and `sigma(o2) = sigma(i2)`; at distance 2, either the
  same, or `sigma(o1) = sigma(i1)*` and `sigma(o2) = sigma(i2)*` (the unique common neighbours
  with the middle edge). Proof by a 64-case table of which 9 complete to P-colorings.
- Lemma 2.2 (P-colorings of `L`): with inputs `i1(L), i2(L)` and outputs `o1(L), o2(L)`: at
  distance 0 the outputs coincide and sit at distance 1 from the inputs; at distance 1 the
  outputs copy the inputs; at distance 2 or 3 the outputs are the inputs swapped. Proof by the
  eight cases `(S/O)^3` at the claw leaves; only `(S,O,S)` and `(O,S,O)` survive.
- Theorem 2.3: the 112-vertex `G` (three `L`, one claw) has no P-coloring: a P-coloring forces
  four edges of `P` pairwise at distance 1 in `Q`, a 4-clique in the line graph of a
  triangle-free cubic graph, contradiction.
- Announces the 52-vertex counterexample and the infinite cyclically 4-edge-connected girth-5
  family (Zenodo 10.5281/zenodo.21933785). AI statement: ChatGPT (GPT-5.6 Sol) for proofreading,
  presentation, rewriting parts of proofs, figures and tables; all content critically reviewed.

### 4.3 Goedgebeur, Jooken, Macajova, Mattiolo, Mazzuoccolo, Zenodo record 21933786 (2026-08-14) `[V, read in full]`

- Lemma 2: P-colorings of the trimmed-`K4` 4-pole (internal 4-cycle) either copy one label to
  all four semi-edges or permute a pair.
- Lemma 3 and its iteration: `P-Col(F_n) = P-Col(F)` for `F_n = F_(n-1) o C`, `|V(F_n)| = 8 + 4n`.
- Section 4: replacing `F` by `F_n` inside any counterexample containing `F` gives an infinite
  family `S_n`, cyclically 4-edge-connected, girth 4 for `n >= 1`; Theorem 4: cyclically
  4-edge-connected girth-5 counterexamples exist on every even order `n >= 76` (poles `F`,
  `FF`, `FIF` share their `P-Col`).
- Section 5: Problem 5 (cyclically 5-edge-connected counterexamples?); a strong normal
  6-edge-coloring of `S_0` (one 112-vertex graph) was verified; Conjecture 6 (every bridgeless
  cubic graph has a normal 6-edge-coloring, attributed to Samal and stated in
  Mazzuoccolo-Mkrtchyan 2020) remains open; Problem 7 (smallest counterexample); the order-36
  frontier; a 68-vertex counterexample posted on X by `@NeuralReformist`
  (`https://x.com/NeuralReformist/status/2080369979388805555`, not retrievable here `[U]`); the
  52-vertex graph (cyclically 4-edge-connected, girth 5, edge list in the appendix; digest of
  our 0-based transcription `27db5d3b680441cf...` `[MV]`); "the order of a smallest
  counterexample lies between 38 and 52"; all known counterexamples contain `F`.
- "This is a first version. We are currently working on a subsequent version with further
  developments and more detailed results."

## 5. What is NOT in the literature as of 2026-09-03

Searched (WebSearch, arXiv listings, Zenodo, the three papers' reference lists): no source
reports, for any of the 2026 counterexamples, a Berge-Fulkerson cover, a Berge cover, the
perfect matching index, a Fan-Raspaud triple, a 5-cycle double cover, a nowhere-zero 5-flow,
oddness, resistance, a normal 6-edge-coloring of the 52-vertex graph, or any measure of how far
the graphs are from a Petersen coloring. GJMMM report only the strong normal 6-edge-coloring of
one 112-vertex graph `[V]`. This is the audit surface of this problem.

## 6. Independence of the CAOS route

The CAOS encodings (`pcclib.encoders`) use edge-image variables with pairwise adjacency clauses
(Petersen) and side-presence plus rich-indicator variables (normal), sharing no variable scheme
with Putman's vertex-witness and missing-pair encodings `[V, encoder read]`. Putman's public
proofs were additionally checked with the CAOS drat-trim binary `[MV, EXP-001]`.
