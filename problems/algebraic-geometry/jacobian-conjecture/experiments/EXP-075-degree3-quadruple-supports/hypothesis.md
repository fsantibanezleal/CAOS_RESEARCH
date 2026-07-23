# EXP-075 - Degree-3 quadruple-support necessaries (resumable, multi-day)

- **Question.** Does any quadruple-support subsystem of the order-4 conditions
  obstruct a degree-3 covector?
- **Motivation.** Degree 3 survived pairs (EXP-071) and all 20825 triples
  (EXP-073). The quadruple tier: support S, |S| = 4: 35 order-4 gamma-blocks x
  125 rows; gauges u, v, w over S (34 blocks, 5610 unknowns). C(51,4) = 249900
  supports: a multi-day resumable background sweep (resume index checkpointed
  every 200 in the artifact; restart with run.py <index>). Any infeasible
  support closes degree 3 conclusively; degree 2 fell at its triple tier, so
  the quadruple tier is the calibration-free next test.
- **Predictions.** 1. [MV] Regression gate: 20 sampled pairs reproduce EXP-071
  run4 through deg3_subsystem_feasible. 2. [MV] The sweep is decided (or an
  honest partial with resume index): a hit closes degree 3 (pattern-theorem
  proposal TO FELIPE); completion all-pass stages the constructive path (R2).
- **Method.** EXP-071 pipeline imported via EXP-072's loader; numpy mod-p;
  two-prime confirmation; flushed; background tee; cap-disciplined.
- **Success.** Gate green and progress persisted. **Failure.** Gate failing.

Declared 2026-07-24 before the run.
