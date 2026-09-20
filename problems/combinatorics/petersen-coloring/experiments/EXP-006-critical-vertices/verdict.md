# EXP-006 verdict - CONFIRMED as redirected: the Petersen defect is exactly 2 on all three graphs, and every vertex pair is critical

Date: 2026-09-03. Hypothesis committed before the run at `2ffc6e3`-era commits (declaration
`cd4df4a` addendum 1, `4dc402d` addendum 2, `fd6eb2d` addendum 3, each before the instances it
governs ran). Runners: `run.py` (single vertices; edge relaxations with `--skip-vertices`),
`run_pairs.py` (pairs). Logs and manifests under `artifacts/` (`manifest.json`,
`pairs-G52.json`, `pairs-G112.json`, `pairs-H112.json`, `run-*.log`); CNFs and proofs under
`E:/_Datos/caos-research/petersen-coloring/EXP-006/`.

## Result

| graph | single-vertex relaxations | pair relaxations | Petersen defect |
|---|---|---|---|
| `G52` | all 52 UNSAT, proofs verified (0.9 to 5.4 s each) | all 1,326 pairs SAT, checker: bad set equals the relaxed pair (slowest 0.73 s) | exactly 2 |
| `G112` | vertex 8 UNSAT (verified); the rest decided by the parity theorem | all 6,216 pairs SAT, bad set equals the relaxed pair (slowest 20.0 s) | exactly 2 |
| `H112` | decided by the parity theorem | all 6,216 pairs SAT, bad set equals the relaxed pair (slowest 17.4 s) | exactly 2 |

Predictions:

| prediction | outcome |
|---|---|
| P1 (a critical single vertex of `G52`; defect 1) | REFUTED by machine: all 52 singles UNSAT with verified proofs |
| P2 (critical single vertices of the 112-vertex graphs) | REFUTED by theorem (context note `2026-09-03-defect-parity-lemma.md`): no cubic graph has a map with exactly one bad vertex; the one instance run (`G112` vertex 8) is UNSAT, verified, consistent |
| P3 (some non-critical vertex, decided) | PASS trivially (all are) |
| P4 (a critical edge of `G52`; normal-5 defect 1) | UNDECIDED at this verdict: 13 of 78 single-edge relaxations UNSAT (verified, 2 to 4 minutes each); the sweep continues under the monitor; normal-5 defect at least 1 |
| P5 (reproduction and corrupted witness) | PASS: bound-0 `G52` UNSAT reproduced; a swap at a non-relaxed vertex raises the checker defect above 1 |
| P6 (addendum 1: some pair of `G52` critical; not confined to free vertices) | PASS, stronger than committed: EVERY pair is critical |
| P7 (addendum 2: some free-vertex pair of `G112` critical) | PASS: all 120 |
| P8 (addendum 2: normal-5 defect of `G52` by edge relaxation) | in progress (see P4) |
| P9 (addendum 3: every pair of `G112` and `H112` critical) | PASS: 6,216 of 6,216 in each |

## The theorem this produced

Parity theorem (derived, context note): for any cubic graph and any edge map into `P`, the
number of vertices failing the star condition is never exactly 1, because the bad vertices'
label indicator vectors sum to an element of the cut space of `P`, and an odd cut of size 1 or 3
in the Petersen graph is a star (bridgeless; cyclically 5-edge-connected). Hence the Petersen
defect of every counterexample is at least 2, and the three known counterexamples attain the
minimum. The stronger finding, universal 2-criticality (every pair works), is machine-verified
for the three graphs and has no proof yet.

## Exact-arithmetic status

Propositional; every UNSAT carries a drat-trim-verified proof (52 for `G52` singles, 1 for
`G112`, 13 edge instances so far); every SAT carries a witness re-verified from the graph alone,
with the checker confirming that the bad set is exactly the relaxed pair (checked for all 13,758
pair witnesses: zero exceptions).

## Adversarial validation record

- Two encodings agree on `G52`'s defect 2 (EXP-004 counter route: bound 1 UNSAT verified, bound
  2 SAT; EXP-006 designated route).
- The single-vertex refutations are instances of a proved theorem.
- Corrupted witness rejected; bound-0 reproduced.

## Consequences for the strategy

The obstruction in each counterexample is spread evenly: removing the star constraint at any
two vertices restores colorability. PCR-3 (critical-pair structure) is therefore trivial for
pairs; the next structural object is the set of witnesses themselves (what the two bad stars look
like, and whether a pair witness can always be chosen with both bad vertices "almost stars").
The normal-5 defect stays open at this verdict (edge sweep running).

## How could this be wrong?

- A relaxed encoding that dropped too much would produce witnesses with fewer bad vertices than
  claimed, which the independent checker would report; it reported exactly the relaxed pair in
  every case.
- The universal 2-criticality is a finite verification on three graphs, not a theorem.
- The 13 edge refutations do not decide the normal-5 defect.

## Addendum 4 verdict (2026-09-18): the normal-5 defect of `G52` is exactly 2

Runner `run_normal_defect.py`, log in the session record, artifact `artifacts/normal-defect.json`
(automorphisms, edge orbits, orbit representatives, witnesses).

| prediction | outcome |
|---|---|
| P10 (every edge orbit of `G52` contains a refuted edge) | PASS: 6 automorphisms (each re-checked), 14 edge orbits, and the 42 single-edge relaxations refuted with verified proofs (edges 0 to 41) meet all 14 orbits. No proper 5-edge-coloring of `G52` has exactly one abnormal edge |
| P11 (a proper 5-edge-coloring with exactly two abnormal edges) | PASS on all three graphs: bound 2 SAT in 2.6 s (`G52`), 1.9 s (`G112`), 43.8 s (`H112`); the independent checker counts exactly 2 abnormal edges in each witness |

So the normal-5 defect of `G52` is exactly 2, from both sides with certificates. For `G112` and
`H112` it is at most 2 and at least 1. The upper bound reproduces, with our own witnesses, the
two-abnormal-edge colorings reported by Goedgebeur et al. (arXiv:2608.10028v3, 2026-09-11); the
lower bound for `G52` is not stated there. This closes P4 and P8 above for `G52`. The direct sweep
of the remaining 36 edges is not needed for the statement; it was left running as a redundancy and
ended at edge 42 when the proof check of that instance exceeded the runner's time limit while the
machine was loaded with the EXP-007 runs (no decision recorded for edge 42; log in
`artifacts/run-edges-G52-resume.log`).

How could this be wrong? The symmetry step uses only that the listed permutations are
automorphisms, which `is_automorphism` re-checks from the edge list; an error there would have to
be an error in a ten-line checker. The refuted edges rest on drat-trim.

Note added 2026-09-18 (literature): the lower bound "no proper 5-edge-coloring has exactly one
abnormal edge" is Proposition 3 of Mattiolo, Mazzuoccolo, Mkrtchyan (arXiv:2104.09241) for every
cubic graph, so the orbit argument above is an independent machine confirmation of a known
statement on `G52`, not a new bound; with the two-abnormal-edge witnesses it gives normal-5 defect
exactly 2 for `G112` and `H112` as well. The parity theorem of this experiment is the vertex
analogue for maps into `E(P)` and implies that proposition through `pd <= ab`
(`context/2026-09-18-defect-unbounded.md`, Lemma 1).
