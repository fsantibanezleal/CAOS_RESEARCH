# EXP-008 verdict - CONFIRMED: the second 52-vertex and the 68-vertex counterexamples have the same invariants as `G52`, and every vertex pair of both is critical

Date: 2026-09-18. Hypothesis committed at `dd82817d` before the run; addendum 1 (edge-orbit stage
withdrawn) committed at 12:10. Runner `run.py` (stages `battery`, `pairs`; stage `edges` stopped,
see P6). Artifacts: `artifacts/battery-G52b.json`, `battery-G68.json` (every witness),
`pairs-G52b.json`, `pairs-G68.json` (every pair witness), `run-*.log`; formulas and proofs under
`E:/_Datos/caos-research/petersen-coloring/EXP-008/`. Certification of the two graphs (no Petersen
coloring, no normal 5-edge-coloring, four checked proofs): EXP-007 part P0,
`EXP-007/artifacts/p0-G52b.json`, `p0-G68.json`.

## Result

| invariant | `G52b` (House of Graphs 57278) | `G68` (House of Graphs 57280) |
|---|---|---|
| structure | cubic, girth 5, edge connectivity 3, no cycle-separating cut below 4, explicit cycle-separating 4-cut `{0, 11, 70, 71}`; 6 automorphisms, 14 edge orbits | same, 4-cut `{2, 11, 90, 97}`; trivial automorphism group |
| Berge-Fulkerson cover | yes (witness) | yes (witness) |
| Berge cover by 5 / by 4 / by 3 perfect matchings | yes / yes / no (verified proof) | yes / yes / no (verified proof) |
| perfect matching index | 4 | 4 |
| Fan-Raspaud triple | yes | yes |
| 5-cycle double cover, nowhere-zero 5-flow | yes, yes | yes, yes |
| nowhere-zero 4-flow | no (verified proof) | no (verified proof) |
| oddness | 2 (bound 1 refuted, bound 2 witness with 2 odd cycles) | 2 (same) |
| resistance | 2 (bound 1 refuted, bound 2 witness) | 2 (same) |
| normal and strong normal 6-edge-colorings | yes, yes (normal chromatic index 6) | yes, yes (6) |
| proper 5-edge-coloring with two abnormal edges | yes (checker counts 2) | yes (checker counts 2, 33 s) |
| Petersen defect | exactly 2 | exactly 2 |
| critical vertex pairs | 1,326 of 1,326, each witness with exactly the two relaxed vertices bad (slowest 28.5 s) | 2,278 of 2,278, same (slowest 29.2 s) |

Predictions:

| prediction | outcome |
|---|---|
| P1 (covers, index 4) | PASS on both graphs |
| P2 (5-CDC, 5-flow, no 4-flow) | PASS on both graphs |
| P3 (oddness 2, resistance 2) | PASS on both graphs, including the low-confidence expectation for `G68` |
| P4 (normal and strong normal 6) | PASS on both graphs |
| P5 (defect 2, every pair critical) | PASS on both graphs: universal 2-criticality now holds on all five known counterexamples (17,362 pair witnesses in total with EXP-006) |
| P6 (normal-5 defect exactly 2) | PASS: two-abnormal-edge witnesses here; the lower bound is Proposition 3 of Mattiolo, Mazzuoccolo, Mkrtchyan and, independently, `pd <= ab` with the parity theorem. The edge-orbit stage was withdrawn (addendum 1) after four instances hit their 15-minute limit on a saturated machine without a decision |

One pair of `G52b` (8-13) first returned a solver ERROR after 0.6 s (a WSL start failure under
load); it was retried alone and is SAT with the expected bad set; the first answer is kept in the
`retried` field of `pairs-G52b.json`.

## Relation to arXiv:2608.10028v3

v3 reports, for the same two graphs, Berge-Fulkerson covers, perfect matching index at most 4,
5-cycle double covers, strong normal 6-edge-colorings and colorings with two abnormal edges; those
rows are reproductions with our own witnesses. Not in v3: the exact index (lower bound 4 is the
snark property), flows, oddness, resistance, the Petersen defect and the pair criticality.

## How could this be wrong?

Every witness is re-verified from the graph alone by `pcclib.checkers`; every refutation carries a
proof checked by drat-trim. The graphs were taken from House of Graphs entries and their
non-colorability was certified with our own encoders before use; an error in transcription would
most likely have produced a colorable graph.
