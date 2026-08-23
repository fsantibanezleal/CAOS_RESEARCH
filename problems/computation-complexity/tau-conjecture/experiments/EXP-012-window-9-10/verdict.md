# EXP-012 verdict: CONFIRMED: no 9-gate seven-rooter with a multiplicative last gate

Run 2026-08-20..23 (one teardown-induced resume; per-partition
checkpoints made it lossless), 20 workers under the Windows Task
Scheduler; 13.1 h of scanning. Artifacts: `artifacts/scan9_final.json`,
`artifacts/phase_a.json`, `artifacts/gate_slice.json`, `scan9.log`.

## Result

Over ALL 1,048,460,912 depth-7 states, every one-gate extension v8 and
every operand b of the state:

    max |R_v8 union R_b| = 6      (hits with union >= 7: ZERO)

So no 9-gate program whose final gate is a MULTIPLICATION computes a
polynomial with 7 distinct integer roots. Combined with EXP-011
(z_max(8) = 6, so the final gate of any 9-gate 7-rooter must involve the
8th value), the seven-root threshold is 10 unless an ADDITIVE 9-gate
7-rooter exists; that residual is EXP-013.

## Scorecard

- Prediction 1 (phase A empty): CONFIRMED (no operand of the 50 stored
  8-gate 6-rooter states has a root outside the 6-rooter's root set;
  since x is itself an operand, this also verified 0 in R_f8 for all 50).
- Prediction 2 (the full multiplicative case is empty): CONFIRMED. This
  is our third surviving emptiness commitment out of eight.
- The pre-registered GROWTH RHYTHM (context note 2026-08-23) predicted
  z_max(9) = 7 and is therefore REFUTED on the multiplicative side: the
  (+1, +1, 0) pattern of z_max(1..8) = 1,2,3,3,4,5,5,6 does not continue
  through a multiplicative ninth gate. If EXP-013 is also empty, the
  rhythm breaks outright at tau = 9 (a third plateau).

## Validation ledger

- Known-answer gate BEFORE production: the identical scan at threshold 6
  on one partition found 793 hits with max union 6 (4,095,733 states,
  13.3 min): the machinery finds unions when they exist.
- The reduction itself (only the last gate matters; a multiplicative last
  gate makes z a union of two known root sets) is proved in the
  hypothesis and is the same argument that decided depth 8.
- Frontier provenance: the depth-7 frontier is the EXP-011 asset, whose
  build carried an exact internal cross-anchor (2,013,706 new depth-7
  polynomials, matching the independent EXP-004 count).
- Resume integrity: the run was interrupted at 107/256 by a session
  teardown and resumed from checkpoints; partition results are written
  atomically, and the final aggregate covers exactly 256 partitions and
  1,048,460,912 states, matching the frontier size exactly.

## Consequence

    minimal tau for 7 distinct integer roots = 10,
    UNLESS a 9-gate witness has an additive last gate (EXP-013).
