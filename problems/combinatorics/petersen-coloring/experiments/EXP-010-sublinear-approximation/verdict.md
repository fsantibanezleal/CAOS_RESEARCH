# EXP-010 verdict - REFUTED expectations, a sharper reduction: no non-colorable 4-pole in the known counterexamples; statement (e) stays open

Date: 2026-09-18. Hypothesis committed at `5bbe3661` (11:43) before any run; addenda 1 to 4 each
committed before the instances they govern ran (12:06, 13:14, 13:19, 16:26 with a budget note).
Runners `run.py` (4-pole sweep), `run_dot.py` (dot products), `run_dist.py` (distance sets).
Artifacts: `artifacts/poles-*.json`, `dot-products.json`, `dist-G52-e*.json`, `run-*.log`; formulas
and proofs under `E:/_Datos/caos-research/petersen-coloring/EXP-010/`. Theory:
`context/2026-09-18-defect-unbounded.md` (Corollary 4, Proposition 5).

## Result

| part | instances | outcome |
|---|---|---|
| control: 4-poles `M(J5; e1, e2)` | 28 orbit representatives | all SAT, checker accepts; patterns: crossed 16, restorable 10, four-distinct 2 |
| `M(G52; e1, e2)` | 482 of 482 orbit representatives | all SAT (colorable); crossed 348, four-distinct 134; no restorable, no other pattern |
| `M(G52b; e1, e2)` | 482 of 482 | all SAT; crossed 347, four-distinct 135 |
| `M(G68; e1, e2)` | 4,947 of 4,947 | all SAT |
| `M(H112; e1, e2)` | 540 of 2,324 (stopped by addendum 4) | all SAT |
| `M(G112; e1, e2)` | not run | - |
| 4-poles `N(G; uv) = G - {u, v}` (addendum 1) | no run needed | colorable for every edge of all five graphs: this is universal 2-criticality at adjacent pairs (EXP-006, EXP-008) |
| dot products `G52 . G52` (addendum 2) | 10 graphs on 102 vertices, girth 5, edge connectivity 3 | all 10 have NO Petersen coloring (DRAT proofs verified): new counterexamples; all have `pd = 2` (bound-2 witness, checker defect 2) |
| distance sets `Dist(e0, e)` of `G52` (addenda 3, 4) | 546 of 949 decided at the 18:30 limit (7 edge orbits complete, 5 partial, 1 not started) | EVERY set contains the distance 1: `{1}` 282, `{1, 2}` 232, `{1, 3}` 5, `{1, 2, 3}` 27; every UNSAT carries a verified proof |

Predictions:

| prediction | outcome |
|---|---|
| P1 (control `J5`) | PASS |
| P2 (no witness with the restorable pattern; only the two patterns the cut space allows) | PASS on 5,911 witnesses of `G52`, `G52b`, `G68`; the pattern was not tabulated beyond "crossed / four-distinct / restorable / other" and "other" never occurred |
| P3 (some non-colorable 4-pole `M` in `G52`, then in the other graphs) | REFUTED for `G52`, `G52b`, `G68` (complete sweeps); undecided for `H112` (23 percent swept, all colorable) and `G112` (not run) |
| P4 (consequence for statement (e)) | not reached |
| P5, P6 (4-poles `N`) | P5 PASS by restriction; P6 REFUTED for all five graphs by the existing pair sweeps |
| P7 (dot products) | all ten are counterexamples with `pd = 2` (the committed expectation) |
| P8, P9 (two disjoint distance sets for some `e0`) | REFUTED on every decided set (546): distance 1 is always realizable, so the 4-poles `Y(e, e')` built on any decided pair are colorable |

One entry (`e0 = 6`, `e = 74`, distance 1) first returned a solver ERROR after 0.8 s under load and
was shown as `Dist = {2}`; the runner was changed to retry undecided entries and the entry is
`{1, 2}`. No conclusion was drawn from the erroneous entry.

## What this establishes

- The cyclic joining of Mattiolo, Mazzuoccolo and Mkrtchyan cannot force bad vertices with the
  known counterexamples as raw material: all their 4-poles `G - e1 - e2` examined are colorable,
  and the ones with a crossed pattern chain around rings of even length.
- Proposition 5 `[D]` (threshold): one cyclically 4-edge-connected cubic graph with `pd >= 3`
  refutes statement (e); on that class `pd <= 2` everywhere or `pd` is unbounded.
- Ten new counterexamples on 102 vertices with checked certificates (dot products of `G52` with
  itself), all with defect 2.
- The observation that turns into EXP-011: universal 2-criticality is exactly what makes every
  piece `G - X`, `|X| >= 2`, colorable; a single non-critical adjacent pair in some counterexample
  would give a non-colorable 4-pole.

## How could this be wrong?

- SAT answers are checked from the definition (`check`); UNSAT answers carry verified proofs.
- The orbit reduction uses only listed automorphisms, each re-checked.
- The symmetry unit of the 4-pole formula conflicted with fixed pendant labels in the first
  launch of `run_dist.py`; it was caught before any output was read, the outputs were deleted and
  the unit is switched off when labels are fixed (commit message records it).
- Nothing is claimed about `G112`, about the unswept part of `H112`, or about the 403 undecided
  distance sets.
