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
