# petersen-coloring: problem backlog

| id | title | status | priority | notes |
|---|---|---|---|---|
| PCB-001 | Source dossier: Putman, Jooken, GJMMM, Jaeger 1985/1988, BGHM 2013, GMS 2019, Hagglund-Steffen 2014, Mazzuoccolo-Mkrtchyan 2020, Ma-Mattiolo-Steffen-Wolf 2025 | done | P0 | 2026-09-03 `context/2026-09-03-source-dossier.md`; Jaeger 1985/1988, GMS 2019 and Hagglund-Steffen still `[U]` (cited through the 2026 papers) |
| PCB-002 | EXP-001: independent certification of the 112 (main, D3) and 52 graphs with a second encoding; positive and corrupted controls | done | P0 | 2026-09-03 CONFIRMED P1-P6 |
| PCB-003 | EXP-002: Berge-Fulkerson, Berge (perfect matching index), Fan-Raspaud on all three | done | P0 | 2026-09-03 CONFIRMED; perfect matching index 4 on all three |
| PCB-004 | EXP-003: 5-cycle double cover, nowhere-zero 5-flow, oddness, resistance | done | P1 | 2026-09-03 CONFIRMED; oddness 4/4/2, resistance 3/3/2 |
| PCB-005 | EXP-004: normal 6 and strong normal 6 on all three (GJMMM did strong normal 6 on one 112 only) | done | P1 | 2026-09-03 CONFIRMED: normal chromatic index exactly 6 on all three |
| PCB-006 | Exact P-defect and normal-5 defect | P-defect done; normal-5 running | P1 | EXP-006: parity theorem (never 1); P-defect exactly 2 on all three; G52 edge-relaxation sweep for the normal-5 defect running |
| PCB-007 | Manuscript v0.01 on Zenodo (preprint) transcribed from EXP-001..006 verdicts | done | P1 | 2026-09-03 published: DOI 10.5281/zenodo.22285165 (concept 10.5281/zenodo.22285164), 7 pages, 351,989 bytes |
| PCB-014 | Read Goedgebeur-Macajova-Skoviera 2019 in full before comparing oddness 4 with their order-44 theorem in the manuscript | todo | P1 | the comparison is `[U]` until then |
| PCB-008 | Reproduce `P-Col(F)`, `P-Col(C)`, `P-Col(L)` exactly and the GJMMM composition lemmas | todo | P2 | anatomy lens |
| PCB-009 | Composition classes C(k,m) below 52 vertices | inconclusive; verdict written | P2 | EXP-005: (5,0), (6,0) exhausted (pure-F proposition); (5,2), (6,2) budget-stopped; next PCR-4b symmetry-broken enumeration |
| PCB-010 | Retrieve the 68-vertex X-posted graph if it becomes public; add to the audit | blocked | P3 | X is paywalled for fetch |
| PCB-011 | Wiki pages 01-05 (statement and history; implication ladder; counterexamples; audit; open questions) | done | P2 | 2026-09-03 written with the round |
| PCB-012 | Web problem page | built and gated | P3 | `frontend/src/pages/PetersenColoring.tsx`; 24-shot gate pass; goes live at the next serialized release (bake) |
| PCB-013 | Cyclically 5-edge-connected counterexamples (GJMMM Problem 5) | todo | P3 | only after PCB-009 |
| PCB-015 | Full 6,216-pair sweeps of G112 and H112 (EXP-006 addendum 3, P9) | done | P2 | 2026-09-03: every pair critical in both |
| PCB-016 | Explain universal 2-criticality (PCR-3): is every pair critical in every counterexample? structure of the two bad stars in pair witnesses | todo | P1 | after PCB-015: the pair set is complete, so the object is the witnesses |
| PCB-017 | EXP-007: is `G52` colored by a smaller bridgeless cubic graph? | done | P1 | CONFIRMED for both 52-vertex graphs (orders 40 to 50 refuted); colorable-only-by-itself v0.01 |
| PCB-018 | Cite arXiv:2608.10028v3 and state the concurrency in the next manuscript version | done | P1 | audit v0.04 (10.5281/zenodo.22836612) |
| PCB-019 | Close the normal-5 defect of G52 at exactly 2 | done | P2 | EXP-006 addendum 4: orbit argument over 42 refuted edges (6 automorphisms, 14 edge orbits) plus explicit two-abnormal-edge witnesses |
| PCB-020 | EXP-008: the full invariant battery on `G52b` (HoG 57278) and `G68` (HoG 57280) | done | P1 | CONFIRMED: same invariants as `G52`; all pairs critical |
| PCB-021 | EXP-007 scope extension: `G68` (orders 40 to 60), unconditional form | gated (PCC-F5) | P3 | first action: G68 at target order 52 (portfolio, addendum 7) |
| PCB-022 | Manuscripts: audit versions and the two focused papers | done | P1 | audit v0.06, unbounded-defect v0.01, colorable-only-by-itself v0.01 |
| PCB-023 | EXP-009: unbounded Petersen defect and abnormal-edge number (rings, frames); exact values on small instances | done | P1 | CONFIRMED; `ab` values beyond `ab >= pd` undecided |
| PCB-024 | EXP-010: non-colorable 4-poles and statement (e) | done | P1 | verdict written; statement (e) settled by EXP-012 |
| PCB-025 | A cyclically 4-edge-connected cubic graph with Petersen defect at least 3 | done | P1 | EXP-012 rings |
| PCB-026 | Exact `ab` of the rings `R_t` (is `ab(R_t) = t`?) on a free machine | todo | P3 | EXP-009 P4 undecided |
| PCB-027 | EXP-011: criticality of the adjacent pairs of the ten 102-vertex dot products | done | P1 | CONFIRMED: 1,530 of 1,530 critical; the dot products have cyclic edge connectivity exactly 4 |
| PCB-028 | Theorem 6 ((e) equivalent to defect at most 2 on cyclically 4-edge-connected graphs) into the audit manuscript (next version) and the page | done | P1 | audit v0.05 published 2026-09-19 (10.5281/zenodo.22846757) |
| PCB-029 | EXP-012: conduction and alternating rings | done | P1 | CONFIRMED; open: exact pd(R_3) (addendum 4 running) |
| PCB-030 | Methodology 13 adoption (governance record, manuscript map, READMEs) | done | P1 | guard passes, 3 governed programs |
| PCB-031 | EXP-013: conducted charge orbits of 6-poles (focus PCC-F6) | done | P1 | every 6-pole of P, J5, J7, dodecahedron conducts the core {0, E, D2}; P3 refuted |
| PCB-032 | EXP-014: transfer semigroups of 6-poles over the six charge sectors | done (F4, F5 at their caps) | P1 | every ring of claws, Petersen superedges or both is Petersen colorable (certificates re-checked); flower-snark junctions are antipodal triples; odd superedge rings are cyclically 5-edge-connected snarks of girth 5; G52 control: zero trace where charges agree |
| PCB-033 | `unbounded-defect` v0.02: pd(R_3) = 3 and Section 6 (6-poles, transfer semigroups) | done | P1 | published 2026-10-06, 10.5281/zenodo.23196817 (12 pages) |
| PCB-034 | EXP-015: 6-poles without small internal cuts whose transfer semigroup has a zero-trace element (cyclically 5-edge-connected snarks up to order 28) | todo | P1 | next bounded action of PCC-F6; declare before running |
