## petersen-coloring: open the problem and close round 1 (EXP-001 to EXP-006)

New problem `combinatorics/petersen-coloring` (new area `combinatorics`), opened from the
scouting round persisted under `problems/combinatorics/petersen-coloring/context/scouting-2026-09/`. Subject: the August 2026 disproof of
Jaeger's Petersen coloring conjecture (Putman; Jooken; Goedgebeur, Jooken, Macajova, Mattiolo,
Mazzuoccolo). CAOS scope: independent certification and the consequence audit; no minimality
race, no priority claim.

### Verdicts (all exact: DRAT proofs checked by drat-trim, or explicit witnesses re-verified from the graph alone)

- EXP-001 CONFIRMED: our own encodings (no shared variable scheme with the public ones) refute
  the two 112-vertex graphs and the 52-vertex graph; five colorable controls; Putman's proofs
  verified under our checker; cyclic edge connectivity exactly 4.
- EXP-002 CONFIRMED: Berge-Fulkerson, Berge, Fan-Raspaud hold on all three; perfect matching
  index exactly 4 (Petersen graph: 5).
- EXP-003 CONFIRMED: 5-cycle double covers and nowhere-zero 5-flows on all three; no 4-flows;
  oddness 4, 4, 2; resistance 3, 3, 2 (our oddness-2 prediction refuted on the 112s, preserved).
- EXP-004: normal and strong normal 6-edge-colorings on all three (normal chromatic index exactly
  6); counter-encoded defect ladders inconclusive except the G52 P-defect (2).
- EXP-005 partial: classes of k copies of the Petersen 4-pole F plus m free vertices; (5,0) and
  (6,0) exhausted by a universal coloring (proposition: pure compositions of F are colorable);
  counterexample-guided search measured non-convergent at 26 semi-edges.
- EXP-006: parity THEOREM (the Petersen defect is never 1 for any cubic graph); Petersen defect
  exactly 2 on all three counterexamples; every one of the 1,326 vertex pairs of the 52-vertex
  graph is critical; all 120 free-vertex pairs of each 112-vertex graph critical. Full pair
  sweeps and the G52 edge sweep continue in the background.

### Record

Context dossier and two derivation notes, wiki 01-05 with a theme-aware SVG, `pcclib` (11 tests),
six experiment folders with hypotheses declared before runs, manifests with SHA-256 of the heavy
artifacts under `E:/_Datos/caos-research/petersen-coloring/`, RESUME/state/backlog/research
lines, manuscript v0.01 (`manuscripts/petersen-coloring/consequence-audit/`, Zenodo DOI
10.5281/zenodo.22285165 reserved), web page `frontend/src/pages/PetersenColoring.tsx` (gated:
24 screenshots, light/dark, EN/ES, all tabs, no overflow), portfolio row and README rows.

No version bump, no bake, no tag: those belong to the serialized release step.
