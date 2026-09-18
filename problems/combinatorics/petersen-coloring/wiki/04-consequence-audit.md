# 04 - The consequence audit

Sources: EXP-002, EXP-003, EXP-004 verdicts and the EXP-006 sweep (in progress). Every value below is exact: positive
entries carry an explicit witness re-verified from the graph alone, negative entries carry a
drat-trim-verified DRAT proof.

## What the conjecture used to imply, tested on the first counterexamples

| property | `G112` | `H112` | `G52` | Petersen graph (control) |
|---|---|---|---|---|
| Berge-Fulkerson cover (6 perfect matchings, every edge twice) | yes | yes | yes | yes |
| Berge cover by 5 perfect matchings | yes | yes | yes | yes |
| cover by 4 perfect matchings | yes | yes | yes | no (proof) |
| perfect matching index | **4** | **4** | **4** | 5 |
| Fan-Raspaud triple (3 perfect matchings, empty intersection) | yes | yes | yes | yes |
| 5-cycle double cover | yes | yes | yes | yes |
| nowhere-zero 5-flow | yes | yes | yes | yes |
| nowhere-zero 4-flow (equivalently 3-edge-colorable) | no (proof) | no (proof) | no (proof) | no (proof) |
| oddness | **4** | **4** | 2 | 2 |
| resistance | **3** | **3** | 2 | 2 |
| normal 6-edge-coloring | yes | yes | yes | yes |
| strong normal 6-edge-coloring (every edge rich) | yes | yes | yes | yes |
| normal chromatic index | 6 | 6 | 6 | 5 |
| Petersen defect (min. number of bad vertices over all edge maps) | **2** (every one of the 6,216 vertex pairs is critical) | **2** (every one of the 6,216 vertex pairs is critical) | **2** (every one of the 1,326 vertex pairs is critical) | 0 |

The defect is never 1 for any cubic graph: the parity theorem in
`context/2026-09-03-defect-parity-lemma.md` (the bad set's label vectors sum to an element of the
cut space of the Petersen graph, and an odd cut of size 1 or 3 in the Petersen graph is a star).
So every counterexample has defect at least 2, and the three known ones attain it.

Bold entries are the ones that differ from the Petersen graph.

## Reading

- Every conjecture that the Petersen coloring conjecture implied (Berge-Fulkerson, Berge,
  Fan-Raspaud, 5-cycle double cover) survives on all three known retrievable counterexamples.
  [MV, EXP-002, EXP-003]
- The counterexamples are better covered by perfect matchings than the Petersen graph itself:
  four perfect matchings suffice, so the perfect matching index is 4, not 5. [MV, EXP-002]
- The two 112-vertex graphs have oddness 4 and resistance 3; the 52-vertex graph has oddness 2
  and resistance 2. [MV, EXP-003] Our committed expectation (oddness 2 everywhere) was refuted
  on the 112-vertex graphs and is preserved in the record.

## How the values are certified

- Perfect matching covers: matchings $M_1, \dots, M_k$ as edge sets, each checked to be
  perfect, then the coverage count per edge.
- Cycle double covers: five even subgraphs (degree 0 or 2 at every vertex), each edge in exactly
  two.
- Flows: values $1..4$ on edges oriented from the smaller to the larger endpoint, conservation
  modulo 5 at every vertex.
- Oddness: a perfect matching $M$; the odd cycles of $E \setminus M$ are counted by a component
  walk. The SAT encoding uses the fact that a 2-vertex-coloring of a 2-factor has at least one
  monochromatic edge on every odd cycle and none on even cycles, so
  $$\mathrm{oddness}(G) = \min_{M,\,\mathrm{col}} \#\{e \in E \setminus M : \mathrm{col}(u_e) = \mathrm{col}(v_e)\}.$$
- Resistance: a deletion set $S$ and a proper 3-edge-coloring of $G - S$.

Witness files: `experiments/EXP-002-perfect-matching-covers/artifacts/witnesses.json`,
`experiments/EXP-003-cycle-covers-flows-oddness/artifacts/witnesses.json`.

## The two graphs added in round 2 (EXP-008, CONFIRMED)

`G52b` (the second 52-vertex counterexample, House of Graphs 57278) and `G68` (House of Graphs
57280) agree with the `G52` column of every table on this page: Berge-Fulkerson cover, Berge cover
by 5 and by 4 perfect matchings (none by 3, checked proof), perfect matching index 4, Fan-Raspaud
triple, 5-cycle double cover, nowhere-zero 5-flow, no 4-flow (checked proof), oddness 2 and
resistance 2 (bound 1 refuted, bound 2 witnessed), normal and strong normal 6-edge-colorings
(normal chromatic index 6), Petersen defect exactly 2. Every vertex pair is critical: 1,326 of
1,326 for `G52b` and 2,278 of 2,278 for `G68`, each witness with exactly the two relaxed vertices
bad. Universal 2-criticality therefore holds on all five known counterexamples (17,362 pair
witnesses with EXP-006). On the 1,326 stored witnesses of `G52` the label vectors of the two bad
vertices always lie in the same nonzero class modulo the cut space of `P`
(`code/probes/classes_mod_cut_space.py`), as the parity argument requires.

arXiv:2608.10028v3 (2026-09-11) reports, for the same five graphs, Berge-Fulkerson covers, perfect
matching index at most 4, 5-cycle double covers, strong normal 6-edge-colorings and colorings with
two abnormal edges; round 1 of this record (2026-09-03) had obtained those items for the first
three graphs independently. The abnormal-edge number, its relation to the Petersen defect, and the
graphs of large defect are on page 07.
