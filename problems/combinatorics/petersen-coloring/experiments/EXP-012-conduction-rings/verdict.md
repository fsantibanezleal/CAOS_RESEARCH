# EXP-012 verdict - CONFIRMED: rings of two 4-poles with disjoint conducted sets have Petersen defect at least t, so statement (e) of Mattiolo, Mazzuoccolo and Mkrtchyan is false

Date: 2026-09-19. Hypothesis committed at `0d6d8bbd` before any code of the experiment ran;
addendum 1 (the restoration argument and the pair of blocks) at 12:20, addendum 2 (checks on
`R_3`) at 12:35, addendum 3 (tooling) at 12:52, each before the runs it governs. Runners `run.py`,
`run_ring.py`, `run_r3_checks.py`, `run_r3_pairs.py`, probe `code/probes/ring_cuts_exhaustive.py`;
library `code/pcclib/poles.py`, `code/pcclib/rings.py`. Artifacts under `artifacts/`; formulas and
proofs under `E:/_Datos/caos-research/petersen-coloring/EXP-012/`. Theory:
`context/2026-09-19-conduction.md` (Lemmas 1 to 6, Theorems 4 and 7, Corollary 8).

## Result

The conducted set `D(M)` of a 4-pole with paired connectors (the distances in the line graph of
`P` between the two labels of a connector, over all maps with every vertex good) is the same at
both connectors (conduction lemma). Two 4-poles with disjoint conducted sets, alternated around a
ring, force a bad vertex in at least half of the blocks.

| 4-pole (pairing) | `D` | evidence |
|---|---|---|
| `A = G52 - {0,3} - {1,9}` (ends of `{0,3}` \| ends of `{1,9}`) | `{1}` | 0 refuted (7.7 s), 1 realized (0.5 s, checker accepts), 2 refuted (2.7 s), 3 refuted (2.1 s); all refutations with proofs verified by drat-trim; 0 also excluded by Lemma 5(a) |
| `B = G52 - {2,7}` (ends at 2 \| ends at 7) | `{0}` | 0 realized (0.2 s), 1, 2, 3 refuted (2.8, 2.2, 2.1 s) with verified proofs; 1 also excluded by Lemma 5(b) |
| `P - {u,v}` (three pairings) | `{0,1}`, `{0,1,2}`, `{0,1,2}` | all three contain 1 |
| `P - e1 - e2`, distance 2 and 3 (three pairings each) | contain 1 | |
| `G52 - {u,v}`, one per edge orbit (u\|v pairing) | `{0}` (11 orbits), `{0,3}` (2), `{0,2}` (1) | never contains 1, as Lemma 5(b) requires |
| `G52 - e0 - e` for the first four EXP-010 pairs with distance set `{1}` | `{1}` | reproduces EXP-010 with the new encoder |

Rings `R_t` alternating `A` and `B` (102 vertices per pair of blocks):

| ring | order | girth | edge connectivity | cycle-separating cuts below 4 | other |
|---|---|---|---|---|---|
| `R_1` | 102 | 5 | 3 | none (bridge search 0.6 s; exhaustive 32.3 s) | no Petersen coloring, proof verified (28.4 s solve, 23.7 s check) |
| `R_2` | 204 | 5 | 3 | none (4.1 s; exhaustive 509.0 s) | `pd = 2`, witness with the two bad vertices in the two `B`-blocks (234.2 s) |
| `R_3` | 306 | 5 | 3 | none (13.6 s) | "at most 2 bad vertices" UNSAT with a proof verified by drat-trim (5,802.5 s solve, 2,265.3 s check) |

In each ring the four edges joining one block to the rest form a cycle-separating cut, so the
cyclic edge connectivity is exactly 4.

Predictions:

| prediction | outcome |
|---|---|
| P1 (control: the `A`-type 4-poles conduct `{1}`) | PASS on four pairs |
| P2 (some candidate avoids distance 1) | PASS: every `G52 - {u, v}` under the u\|v pairing, by addendum 1 in advance and by computation for all 14 edge orbits. The Petersen 4-poles of candidates 1 and 2 all conduct 1; candidate 4 (`L`) was not needed |
| P3 (`R_1` non-colorable; `R_3` cyclically 4-edge-connected; "at most 2" UNSAT) | PASS, including the cardinality check, which the hypothesis allowed to time out |
| P4 (addendum 2: a map of `R_3` with exactly three bad vertices) | UNDECIDED: the cardinality instance at bound 3 hit its 1-hour limit. Only `pd(R_3) >= 3` is established |
| P5 (addendum 2: ten sampled pairs of `R_3` refuted) | PASS: 10 of 10 UNSAT with verified proofs (92 to 719 s each), five pairs inside one block and five across two blocks |
| P6 (addendum 2: exhaustive cut cross-check) | PASS on `R_1` and `R_2` |

## What this establishes

For every `t >= 2`, `R_t` is a cyclically 4-edge-connected cubic graph of girth 5 on `102t`
vertices with `pd(R_t) >= t` and `ab(R_t) >= t` (Theorem 7 of the context note; the ring lemma
carries the cyclic 4-edge-connectivity of `R_2` to every `t`). Hence no sublinear function bounds
the number of abnormal edges on cyclically 4-edge-connected cubic graphs: statement (e) of
Mattiolo, Mazzuoccolo and Mkrtchyan is false. With (a) false (the disproof), (b) false (their
Theorem 1) and (c), (d) false (EXP-009 and the audit manuscript), all five statements of their
Conjecture 3 are false, so the conjectured equivalence holds.

Two earlier readings are corrected by this result. The audit manuscript v0.05 called the universal
criticality of fifteen cyclically 4-edge-connected counterexamples "consistent with the defect
bound 2 on that class and against the conjectured equivalence": `R_2` is cyclically
4-edge-connected with non-critical adjacent pairs, and `R_3` has no critical pair, so that
inference from fifteen graphs to the class was wrong. The open question of the audit manuscript
("is there a cyclically 4-edge-connected cubic graph with Petersen defect at least 3?") is answered
yes.

## Adversarial validation record

- Both exclusions that make the conducted sets disjoint were computed and, independently, proved:
  distance 0 for `A` and distance 1 for `B` follow from the restoration lemma, and either
  computed restriction alone suffices for the theorem.
- The cyclic connectivity of `R_1` and `R_2` was computed twice, by a bridge search over all edge
  pairs and by the exhaustive routine of EXP-001 over all edge sets of size at most three; the two
  routines were first compared on three graphs of known type (none, 2-edge cuts, 3-edge cuts).
- The ring theorem predicts `pd(R_3) >= 3`; the cardinality instance at bound 2 is UNSAT with a
  verified proof, and ten designated pair relaxations are UNSAT with verified proofs. A single SAT
  answer in any of these eleven instances would have refuted the theorem or the construction.
- `pd(R_2) = 2` matches the theorem's bound for `t = 2` exactly, with the bad vertices in
  non-consecutive blocks as predicted.

## How could this be wrong?

- The conducted sets rest on DRAT proofs of small formulas (a few seconds each) and on two
  restoration arguments of three lines.
- The step from `R_2` to all `R_t` is the ring lemma, proved by hand; its base case is the
  computed absence of small cycle-separating cuts in `R_2`.
- The upper bound `pd(R_3) = 3` is not established; nothing depends on it.

## Addendum 4 outcome (2026-10-06): `pd(R_3) = 3`

`run_r3_upper.py` regenerated a map of `R_2` with exactly two bad vertices (local indices 4 and 35
of the two `B`-blocks), then relaxed the star condition at local vertex 4 of each of the three
`B`-blocks of `R_3`: SAT in 168.6 s, and the independent checker counts exactly three bad vertices.
With the verified UNSAT of "at most 2" (P3), `pd(R_3) = 3`. The ring bound `pd(R_t) >= t` is attained
at `t = 2` and `t = 3`, with the bad vertices in the `B`-blocks. P4 of addendum 2 is now PASS.
Artifacts: `artifacts/r3-upper.json`, `artifacts/run-r3-upper.log`.
