# EXP-004 verdict - normal 6 CONFIRMED; defect ladders INCONCLUSIVE except the P-defect of G52

Date: 2026-09-03. Hypothesis committed before the run at `e1e7a3b`. Runner: `run.py`; raw log
`artifacts/run.log` (the run was interrupted by nothing; it completed at 13:19); manifest
`artifacts/manifest.json`; witnesses `artifacts/witnesses.json`; CNFs and proofs under
`E:/_Datos/caos-research/petersen-coloring/EXP-004/`.

## Result

| prediction | outcome | evidence |
|---|---|---|
| P1 | PASS | Petersen graph and `J5`: normal-5 defect 0 and P-defect 0 (SAT at bound 0, validated); all six bound-0 target instances UNSAT with verified proofs (reproducing EXP-001 with the counter attached) |
| P2 | PASS | `G112`, `H112`, `G52` admit normal 6-edge-colorings (validated witnesses, under 0.3 s each); with EXP-001 the normal chromatic index of each is exactly 6 |
| P3 | PASS, committed expectation right | all three admit STRONG normal 6-edge-colorings (every edge rich), validated |
| P4 | UNDECIDED | normal-5 defect: bound 0 UNSAT (verified) for all three; bound 1 TIMEOUT at the 30-minute cap for all three; value at least 1 |
| P5 | DECIDED for `G52` only | P-defect: bound 0 UNSAT (verified) for all three; bound 1 UNSAT with verified proof for `G52` (532 s) and TIMEOUT for the 112-vertex graphs; bound 2 SAT for `G52` (0.09 s, checker defect exactly 2). So the P-defect of `G52` is exactly 2 by this route; the committed expectation 1 is REFUTED |
| P6 | PASS | corrupted normal-6 witness rejected |

Instances (CaDiCaL 1.7.3 in WSL, drat-trim):

| instance | status | seconds | verified |
|---|---|---|---|
| `G112` normal-5 defect 0 / 1 | UNSAT / TIMEOUT | 1,529.7 / 1,800 | yes / - |
| `G112` P-defect 0 / 1 | UNSAT / TIMEOUT | 262.1 / 1,800 | yes / - |
| `H112` normal-5 defect 0 / 1 | UNSAT / TIMEOUT | 859.1 / 1,800 | yes / - |
| `H112` P-defect 0 / 1 | UNSAT / TIMEOUT | 278.6 / 1,800 | yes / - |
| `G52` normal-5 defect 0 / 1 | UNSAT / TIMEOUT | 137.4 / 1,800 | yes / - |
| `G52` P-defect 0 / 1 / 2 | UNSAT / UNSAT / SAT | 50.4 / 532.4 / 0.09 | yes / yes / witness |
| normal 6 and strong normal 6, all three | SAT | under 0.3 each | witnesses |

## Exact-arithmetic status

Propositional; positives are validated witnesses; negatives carry verified proofs; TIMEOUT
rows carry nothing and are reported as intervals.

## Adversarial validation record

- Controls with known answers pass; corrupted witness rejected.
- The `G52` P-defect value 2 is reached here by the cardinality (sequential counter) encoding and
  independently by EXP-006's designated-relaxation encoding (52 single refutations, 1,326 pair
  witnesses): two encodings, one value.
- The parity theorem (context note `2026-09-03-defect-parity-lemma.md`) proves the bound-1
  P-defect instances are UNSAT for every cubic graph, so the two TIMEOUT rows for P-defect 1 are
  now known to be UNSAT in truth, without a proof object from this run.

## Consequences for the strategy

Cardinality-encoded defect bounds are the wrong tool for these instances; designated relaxation
(EXP-006) decides the P-defect of all three graphs quickly. The normal-5 defect remains open at
"at least 1" and is attacked by edge relaxation in EXP-006 addendum 2.

## How could this be wrong?

- The TIMEOUT rows are not evidence of anything; they are reported as such.
- The `G52` bound-2 witness has exactly two bad vertices under the checker; the bound-1 proof is
  verified; the value 2 does not depend on the counter encoding being correct beyond soundness
  (a counter that under-counted would produce a witness with more than 2 bad vertices, which the
  checker would have reported).
