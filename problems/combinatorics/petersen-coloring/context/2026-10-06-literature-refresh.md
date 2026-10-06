# Literature refresh (2026-10-06)

Marks as in `2026-09-03-source-dossier.md`: `[V]` read in the primary source.

## arXiv:2608.10028v4 (Goedgebeur, Jooken, Máčajová, Mattiolo, Mazzuoccolo, Ulyanov, 2026-09-30) `[V]`

Stored at `E:/_Datos/caos-research/petersen-coloring/sources/arxiv/gjmmmu-2608.10028v4.pdf`
(276,857 bytes, SHA-256 `655b396ef336b37e04169e0c58f6f283e2e2a8ef15aa21a57b9ae360553fa3b7`), text
`gjmmmu-v4.txt`. Same title, authors and mathematical content as v3; the introduction is rewritten
and the statements are renumbered:

| v3 | v4 | content |
|---|---|---|
| Problem 8 | Problem 9 | smallest bridgeless cubic graph without a P-coloring |
| Observation 9 | Observation 10 | the smallest counterexample has at least 40 and at most 52 vertices |
| Problem 10 | Problem 11 | cyclically 5-edge-connected counterexamples |
| Conjecture 11 | Conjecture 12 | normal chromatic index at most 6 |
| Question 12 (= MMM Question 3.1) | Question 13 | abnormal edges |
| Conjecture 13 | Conjecture 14 | Hakobyan-Mkrtchyan P12 conjecture |
| Section 5.4 | Section 5.4 | `H_b` and the question whether the 52-vertex counterexamples are colorable only by themselves |

New in v4: P-coloring is presented as equivalent to a cycle-continuous map to `P` (DeVos, Nešetřil,
Raspaud); links to matroids (Edmonds), polyhedral optimization (Schrijver), zero-temperature states
of spin models (Beaudin, Ellis-Monaghan, Pangborn, Shrock; Jaeger 1992 on spin models for the
Kauffman polynomial) and topology (Kauffman; Hell-Nešetřil homomorphisms); a reference to
Inoue, Kawarabayashi, Matsuo, Miyashita, Mohar, Sonobe, "Three-edge-coloring apex cubic graphs",
arXiv:2608.22870 (2026), described as completing the framework of Tutte's 3-edge-coloring
conjecture (bridgeless cubic graphs without a Petersen minor are 3-edge-colorable). Section 5.4
still asks whether the 52-vertex counterexamples are colorable only by themselves: v4 does not
answer it.

## Searches (2026-10-06)

- arXiv full-text search "Petersen coloring", newest first, 50 results: no paper after v4 on the
  conjecture or its counterexamples. Adjacent: Ferrarini, Mkrtchyan, "Some new results on Sylvester
  colorings of cubic graphs", arXiv:2607.06396 (H-colorings by `S_10`, `S_12`); arXiv:2509.14184
  (counterexample to the `S_10` and `S_12` conjectures); arXiv:2508.20565 (normal 6-edge-colorings).
- arXiv "abnormal edges": only Mattiolo, Mazzuoccolo, Mkrtchyan (2021) in this area.
- arXiv "r-graphs" color: Ma, Steffen, Wolf, Zhang, "Some conjectures on r-graphs and equivalences",
  arXiv:2411.01753v2 (2026-05-28), on perfect-matching conjectures for planar and minor-free
  r-graphs; no statement on `H_r` membership or on Petersen colorings.
- Web search for cyclically 5-edge-connected counterexamples: still open (v4 Problem 11).

## Novelty status of the CAOS results (methodology 13)

| result | internally proved | primary-source overlap checked | external novelty |
|---|---|---|---|
| both 52-vertex counterexamples are colorable only by themselves (EXP-007; conditional on v4 Observation 10) | yes (certificates, two lemmas) | v3, v4 and MMSW 2025 read; v4 still poses the question | not independently confirmed |
| statement (e) of MMM Conjecture 3 false; Conjecture 3 holds (EXP-012) | yes (conduction lemma, ring theorem, certificates) | MMM 2021 and v4 read; no later work found | not independently confirmed |
| statements (c), (d) false (EXP-009) | yes | the constructions are MMM's; their conclusion was weaker | not independently confirmed |
| parity theorem, universal 2-criticality on fifteen graphs, consequence audit | yes | v3/v4 overlap on BF, index at most 4, 5-CDC, normal 6, two abnormal edges, stated in the audit | partly overlapping, as stated |

A negative literature search is not a proof of novelty.
