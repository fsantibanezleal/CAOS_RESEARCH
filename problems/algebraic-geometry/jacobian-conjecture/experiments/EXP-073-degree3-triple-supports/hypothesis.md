# EXP-073 - Degree-3 triple-support necessaries

- **Question.** Does any triple-support subsystem of the order-4 conditions
  obstruct a degree-3 covector?
- **Motivation.** Degrees 1 and 2 are closed (EXP-067 exact; EXP-072 sound,
  gate-verified); degree 3 survived the pair tier (EXP-071 run4). The triple
  tier is the next complete set of necessary conditions: support S, |S| = 3:
  15 order-4 gamma-blocks x 125 rows; gauges u, v, w over S (19 blocks, 3135
  unknowns). Any infeasible support closes degree 3 conclusively. Pipeline =
  EXP-071's imported verbatim (modfrac, overflow-safe solvem,
  deg3_subsystem_feasible, which handles arbitrary support size), exactly as
  EXP-072 imported it for degree 2.
- **Falsifiable predictions.**
  1. [MV] Regression gate: 20 sampled PAIR supports reproduce EXP-071 run4's
     feasible degree-3 verdicts (run through deg3_subsystem_feasible).
  2. [MV] The sweep over combinations(51,3) = 20825 supports is decided with
     early-abort and two-prime confirmation; resumable by index. No calibrated
     expectation declared (two prior calibrations were refuted); if a support
     is infeasible, DEGREE 3 IS CLOSED and the pattern-theorem proposal goes
     TO FELIPE; all-pass stages quadruples or the constructive path.
- **Method.** Import EXP-071/run.py; exact setup; numpy mod-p; flushed prints;
  background with tee; cap-disciplined.
- **Success criterion.** 1 passing, 2 decided (or honest partial + resume index).
- **Failure criterion.** The regression gate failing.

Declared 2026-07-23 before the run.
