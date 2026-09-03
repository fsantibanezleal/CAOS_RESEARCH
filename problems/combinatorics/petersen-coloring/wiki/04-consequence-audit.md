# 04 - The consequence audit

Sources: EXP-002 and EXP-003 verdicts (EXP-004 pending). Every value below is exact: positive
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
