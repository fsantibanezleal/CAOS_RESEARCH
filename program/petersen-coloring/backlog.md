# petersen-coloring: problem backlog

| id | title | status | priority | notes |
|---|---|---|---|---|
| PCB-001 | Source dossier: Putman, Jooken, GJMMM, Jaeger 1985/1988, BGHM 2013, GMS 2019, Hagglund-Steffen 2014, Mazzuoccolo-Mkrtchyan 2020, Ma-Mattiolo-Steffen-Wolf 2025 | done | P0 | 2026-09-03 `context/2026-09-03-source-dossier.md`; Jaeger 1985/1988, GMS 2019 and Hagglund-Steffen still `[U]` (cited through the 2026 papers) |
| PCB-002 | EXP-001: independent certification of the 112 (main, D3) and 52 graphs with a second encoding; positive and corrupted controls | done | P0 | 2026-09-03 CONFIRMED P1-P6 |
| PCB-003 | EXP-002: Berge-Fulkerson, Berge (perfect matching index), Fan-Raspaud on all three | done | P0 | 2026-09-03 CONFIRMED; perfect matching index 4 on all three |
| PCB-004 | EXP-003: 5-cycle double cover, nowhere-zero 5-flow, oddness, resistance | done | P1 | 2026-09-03 CONFIRMED; oddness 4/4/2, resistance 3/3/2 |
| PCB-005 | EXP-004: normal 6 and strong normal 6 on all three (GJMMM did strong normal 6 on one 112 only) | done | P1 | 2026-09-03 CONFIRMED: normal chromatic index exactly 6 on all three |
| PCB-006 | Exact P-defect and normal-5 defect | P-defect done; normal-5 running | P1 | EXP-006: parity theorem (never 1); P-defect exactly 2 on all three; G52 edge-relaxation sweep for the normal-5 defect running |
| PCB-007 | Manuscript v0.01 on Zenodo (preprint) transcribed from EXP-001..004 verdicts | todo | P1 | header standard; prereserve flow; after EXP-004 |
| PCB-014 | Read Goedgebeur-Macajova-Skoviera 2019 in full before comparing oddness 4 with their order-44 theorem in the manuscript | todo | P1 | the comparison is `[U]` until then |
| PCB-008 | Reproduce `P-Col(F)`, `P-Col(C)`, `P-Col(L)` exactly and the GJMMM composition lemmas | todo | P2 | anatomy lens |
| PCB-009 | Composition classes C(k,m) below 52 vertices | partial | P2 | EXP-005: (5,0), (6,0) exhausted (pure-F proposition); CEGAR non-convergent at 26 semi-edges; next PCR-4b symmetry-broken enumeration |
| PCB-010 | Retrieve the 68-vertex X-posted graph if it becomes public; add to the audit | blocked | P3 | X is paywalled for fetch |
| PCB-011 | Wiki pages 01-05 (statement and history; implication ladder; counterexamples; audit; open questions) | done | P2 | 2026-09-03 written with the round |
| PCB-012 | Web problem page | built and gated | P3 | `frontend/src/pages/PetersenColoring.tsx`; 24-shot gate pass; goes live at the next serialized release (bake) |
| PCB-013 | Cyclically 5-edge-connected counterexamples (GJMMM Problem 5) | todo | P3 | only after PCB-009 |
| PCB-015 | Full 6,216-pair sweeps of G112 and H112 (EXP-006 addendum 3, P9) | running | P2 | launched 2026-09-03 13:08 and 13:09 |
| PCB-016 | Critical-pair structure (PCR-3): distance profile, which pairs, per graph | todo | P2 | after PCB-015 |
