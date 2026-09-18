# EXP-009 verdict - CONFIRMED: the defect lower bounds of rings and frames are attained; the abnormal-edge numbers are bounded below but not decided

Date: 2026-09-18. Hypothesis committed at `efed046b` before any run; addendum 1 (designated
witness search for `R_4`) committed before its instances ran. Runners `run.py`, `run_r4.py`; logs
and results under `artifacts/` (`controls.json`, `pd-*.json`, `ab-*.json`, `p5-R2.json`,
`r4-designated.json`, `run-*.log`); formulas under
`E:/_Datos/caos-research/petersen-coloring/EXP-009/`. Theorems: `context/2026-09-18-defect-unbounded.md`.

## Result

| object | order | edge connectivity | girth | `pd` lower bound (theorem) | `pd` witness | `pd` | `ab` |
|---|---|---|---|---|---|---|---|
| `R_2` | 104 | 2 | 5 | 2 | bound 2 SAT, 41.2 s, checker defect 2, one bad vertex per copy | 2 | 2 <= ab <= 4 (bound 4 SAT in 528.6 s, checker 4; bounds 2, 3 undecided at 30 minutes) |
| `R_3` | 156 | 2 | 5 | 3 | bound 3 SAT, 159.2 s, checker defect 3, one per copy | 3 | at least 3 (bounds 3, 4 undecided) |
| `R_4` | 208 | 2 | 5 | 4 | cardinality bound 4 undecided at 30 minutes, bound 5 SAT (defect 5); designated relaxation of local vertices (18, 46, 20, 18) SAT in 7.4 s, checker defect 4 | 4 | at least 4 (bounds 4, 5 undecided) |
| `K_4[G52]` | 204 | 3 | 5 | 4 | bound 4 SAT, 203.3 s, checker defect 4, one per copy | 4 | at least 4 (bounds 4, 5 undecided) |

Predictions:

| prediction | outcome |
|---|---|
| P1 (controls: rings and the `K4` frame of `J5` are Petersen colorable) | PASS: `R_2[J5]`, `R_3[J5]`, `K_4[J5]` SAT at bound 0, checker defect 0 |
| P2 (structure) | PASS: all four objects cubic, girth 5; rings have edge connectivity 2, the frame 3 |
| P3 (`pd` equals the number of copies) | PASS for all four objects; for `R_4` through the designated witness of addendum 1 |
| P4 (`ab` equals the number of copies) | UNDECIDED: only `ab(R_2) <= 4` was obtained; every other bounded instance hit the 30-minute limit. The runs shared the machine with EXP-007 and were stopped after two bounds each. The committed expectation `ab = t` is neither confirmed nor refuted |
| P5 (same-copy pair relaxations of `R_2` are impossible) | PASS: 20 of 20 UNSAT with proofs verified by drat-trim (mean 128 s) |

## What this establishes

- `pd(R_t) = t` for `t = 2, 3, 4` and `pd(K_4[G52]) = 4`: the lower bounds of Theorems 2 and 3 are
  tight on the smallest instances, with exactly one bad vertex in every block of each witness.
- Machine agreement with Theorem 2 on twenty instances where the theorem predicts UNSAT.
- `ab` is at least the number of copies by Lemma 1; its exact value on these graphs is open
  (`2 <= ab(R_2) <= 4`).

## Adversarial validation record

The witnesses are counted by `checkers.petersen_defect` and `checkers.normal_defect`, which read
only the graph and the labels. The controls show that the constructions by themselves do not
create defects. P5 is a check that could have refuted Theorem 2 or the relaxed encoder.

## How could this be wrong?

- The lower bounds are proofs, not computations; an error there would be an error in the cut-space
  argument (three lines, and consistent with P5 and with the class probe on 1,326 stored
  witnesses).
- A designated witness proves an upper bound only; all four upper bounds meet the proved lower
  bounds.
- Nothing is claimed about `ab` beyond `ab >= pd`.
