# EXP-011 verdict - CONFIRMED: every adjacent pair of the ten 102-vertex counterexamples is critical

Date: 2026-09-19. Hypothesis committed on 2026-09-18 before any run (backlog PCB-027). Runner
`run.py` (one object per process, four in parallel after the `G52` control). Artifacts:
`artifacts/adjacent-pairs-<object>.json` (every witness), `artifacts/run-*.log`,
`artifacts/dot-products-cyclic-connectivity.json` (from `code/probes/dot_products_cyclic_connectivity.py`);
formulas under `E:/_Datos/caos-research/petersen-coloring/EXP-011/`.

## Result

| object | order | adjacent pairs | critical | slowest (s) | mean (s) |
|---|---|---|---|---|---|
| `G52` (control) | 52 | 78 | 78 | 5.6 | 1.5 |
| `D_0_3_0` | 102 | 153 | 153 | 171.5 | 21.2 |
| `D_0_4_0` | 102 | 153 | 153 | 130.9 | 24.1 |
| `D_0_5_0` | 102 | 153 | 153 | 170.9 | 26.0 |
| `D_0_7_0` | 102 | 153 | 153 | 117.2 | 27.2 |
| `D_0_8_0` | 102 | 153 | 153 | 80.6 | 10.5 |
| `D_0_3_1` | 102 | 153 | 153 | 68.3 | 11.9 |
| `D_0_4_1` | 102 | 153 | 153 | 57.4 | 8.9 |
| `D_0_5_1` | 102 | 153 | 153 | 69.5 | 11.4 |
| `D_0_7_1` | 102 | 153 | 153 | 35.5 | 9.1 |
| `D_0_8_1` | 102 | 153 | 153 | 46.6 | 8.1 |

In all 1,608 witnesses the independent checker finds exactly the two relaxed vertices bad.

Structure of the ten dot products (probe, same day): digests equal those recorded in EXP-010;
girth 5; edge connectivity 3; no cycle-separating edge cut with at most three edges (exhaustive,
the EXP-001 routine); the four edges joining the two parts form a cycle-separating cut. So their
cyclic edge connectivity is exactly 4: they are ten cyclically 4-edge-connected counterexamples
(no Petersen coloring, EXP-010, checked proofs).

Predictions:

| prediction | outcome |
|---|---|
| P1 (control: all 78 adjacent pairs of `G52` critical) | PASS |
| P2 (every adjacent pair of every dot product critical; committed, three quarters) | PASS: 1,530 of 1,530 |
| P3 (every witness has exactly the relaxed pair bad) | PASS: 1,608 of 1,608 |

## What this establishes

No 4-pole `D - {u, v}` (`uv` an edge) of these ten graphs is non-colorable, so none of them yields
a cyclically 4-edge-connected graph of Petersen defect at least 3 by the route of Theorem 6 and
its remark (`context/2026-09-18-defect-unbounded.md`). Together with EXP-006, EXP-008 and EXP-010,
every adjacent pair is critical in all fifteen cyclically 4-edge-connected counterexamples
examined (the five public ones and these ten), and every 4-pole `G - e1 - e2` of `G52`, `G52b`,
`G68` is colorable. Since, by Theorem 6, statement (e) of Mattiolo, Mazzuoccolo and Mkrtchyan is
equivalent to "Petersen defect at most 2 on every cyclically 4-edge-connected cubic graph", this
is evidence for (e) and against their Conjecture 3. It decides neither.

## How could this be wrong?

A SAT witness is re-verified from the graph; the cyclic connectivity probe uses the exhaustive
routine of EXP-001 and an explicit 4-cut. The dot products are one construction; nothing is
claimed about other cyclically 4-edge-connected counterexamples.
