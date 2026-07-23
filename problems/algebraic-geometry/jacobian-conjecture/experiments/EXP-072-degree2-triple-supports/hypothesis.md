# EXP-072 - Degree-2 triple-support necessaries (the practical form of the joint decision)

- **Question.** Does any TRIPLE-support subsystem of the order-3 conditions
  obstruct a degree-2 covector?
- **Motivation (the declared derivation).** The full joint system (227k gauge
  unknowns) exceeds practical dense elimination, so the decision proceeds by
  growing support: after EXP-071's corrected all-feasible pair sweep, the triple
  supports are the next complete tier of necessary conditions (support S,
  |S| = 3: 10 gamma-blocks, 1250 rows, 12 gauge blocks, 1980 unknowns; any
  infeasible S closes degree 2 conclusively). The pipeline is EXP-071's
  (imported verbatim: modfrac, overflow-safe solvem, deg2_subsystem_feasible,
  which already handles arbitrary support size).
- **Falsifiable predictions.**
  1. [MV] Regression gate: 20 sampled pair supports reproduce EXP-071 run4's
     feasible verdicts on the imported pipeline.
  2. [MV] The triple-support sweep over all C(51,3) = 20825 supports (plus the
     mixed multisets are covered by the pair tier already) is decided with
     early-abort and two-prime confirmation on any hit. No calibrated
     expectation is declared (the last two calibrations were refuted); either
     outcome is recorded: a hit closes degree 2; all-pass stages quadruples or
     the constructive path.
- **Method.** Import EXP-071/run.py as a module; identical exact setup; numpy
  mod-p; flushed progress; background with tee; cap-disciplined (the sweep is
  resumable by support index if it exceeds the session).
- **Success criterion.** 1 passing and 2 decided (or an honest partial with the
  resume index recorded).
- **Failure criterion.** The regression gate failing.

Declared 2026-07-23 before the run.
