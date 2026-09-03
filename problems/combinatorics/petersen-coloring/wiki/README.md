# Petersen coloring counterexamples: research wiki

Transcribe only closed experiment verdicts and proved derivations. Pages land vertically with the
round that produces their content.

| page | content | status |
|---|---|---|
| [01-statement-and-history.md](01-statement-and-history.md) | the conjecture, normal colorings, the implication ladder, the 2026 disproof timeline | written at open (sources: context dossier) |
| [02-implication-ladder.md](02-implication-ladder.md) | what the conjecture implied and what survives after the disproof | written (EXP-002, EXP-003) |
| [03-the-counterexamples.md](03-the-counterexamples.md) | the three graphs, gadgets, our certification | written (EXP-001) |
| [04-consequence-audit.md](04-consequence-audit.md) | Berge-Fulkerson, Berge, Fan-Raspaud, double covers, flows, oddness, resistance (normal 6 and defects pending EXP-004) | written (EXP-002, EXP-003) |
| [05-open-questions.md](05-open-questions.md) | minimality in [38,52], cyclic 5-connectivity, normal 6 conjecture, our nulls and budget stops | written (round 1 close) |

| record | status | result |
|---|---|---|
| scouting and scoping | complete | problem selected at 18/18 on the counterexample radar; consequence audit chosen |
| EXP-001 | CONFIRMED | `G112`, `H112`, `G52` have no Petersen coloring and no normal 5-edge-coloring: six verified DRAT proofs; five colorable controls; Putman's proofs verified; cyclic edge connectivity 4 |
| EXP-002 | CONFIRMED | Berge-Fulkerson, Berge-5, Fan-Raspaud on all three; perfect matching index exactly 4 (committed prediction right) |
| EXP-003 | CONFIRMED | 5-cycle double covers and nowhere-zero 5-flows on all three; no 4-flows; oddness 4, 4, 2 and resistance 3, 3, 2 (oddness-2 prediction refuted on the 112-vertex graphs) |
| EXP-004 | normal 6 CONFIRMED; defects INCONCLUSIVE (except G52) | normal and strong normal 6 on all three (normal chromatic index exactly 6); counter-encoded defect ladders time out at bound 1, but the G52 P-defect is 2 by this route too |
| EXP-005 | partial | classes of k copies of F plus m free vertices: (5,0), (6,0) exhausted by a universal coloring (pure-F proposition); (3,2) control and (5,2) did not converge under counterexample-guided search |
| EXP-006 | CONFIRMED as redirected | parity THEOREM: the Petersen defect is never 1; G52: all 52 singles refuted, all 1,326 pairs critical (defect exactly 2); G112, H112: all 6,216 pairs critical each (defect exactly 2; universal 2-criticality on all three graphs); the G52 edge sweep (normal-5 defect) running |
| preprint v0.01 | published 2026-09-03 | consequence audit, parity theorem, universal 2-criticality, pure-F proposition; DOI [`10.5281/zenodo.22285165`](https://doi.org/10.5281/zenodo.22285165) (concept [`10.5281/zenodo.22285164`](https://doi.org/10.5281/zenodo.22285164)) |
