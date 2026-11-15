# EXP-006 verdict - CONFIRMED on the sampled space: no member of the odd-cycle family on C5 has a frontier value above 1, so none reaches 9/8

Date: 2026-11-15. Hypothesis frozen at `b3aea839` (2026-11-14) before any computation. Instrument: `ufclib.frontier_value_cp`
(exact cutting-plane frontier evaluator), `ufclib.odd_cycle_instance` and `ufclib.afrasyab_uniform`, research PR #425
(`2e064021`). CPU only, exact rationals, 14 worker processes.

## Result

| stage | members evaluated | largest frontier value | above 9/8 | above 1 |
|---|---:|---|---:|---:|
| A (calibration, uniform C5) | 5 | 79/120 (eps = 1/120) | 0 | 0 |
| B (symmetric members) | 572 | 5/6 | 0 | 0 |
| C (random non-uniform members) | 2,000 | 11/12 | 0 | 0 |
| D (local search from the 10 best of B and C) | 1,124 | 42/43 | 0 | 0 |

Every evaluated member of the odd-cycle family on C5 has a frontier value at most 1; the largest found is 42/43. The
programme's lower bound alpha* >= 9/8 (EXP-005) is not raised by this family on the sampled space.

## Predictions

| prediction | outcome | evidence |
|---|---|---|
| P1 (Stage A equals 2/3 - eps) | PASS at all five eps: 79/120, 13/20, 5/8, 29/48 and 23/39 are 2/3 - eps for eps = 1/120, 1/60, 1/24, 1/16, 1/13; the builder equals Afrasyab's uniform instance at each | `artifacts/stage-A.jsonl`, `summary.json` `A` |
| P2 (no member of B, C, D above 9/8) | PASS: 0 of 3,696 | `summary.json` `best.*.above_9_8`, `P2` |
| P3 (no member above 1) | PASS: 0 of 3,696 | `summary.json` `best.*.above_1`, `P3` |
| P4 (largest value per stage, exploration) | B 5/6, C 11/12, D 42/43, with parameters, witness cost vectors and R4 descriptors in `summary.json` `best` | `summary.json` |

The largest members of B, C and D have a witness cost vector with a single arc of cost 1 and every other arc of cost 0.
The ten local searches ended at 23/24, 23/24, 12/13, 13/14, 71/73, 13/14, 14/15, 15/16, 43/45 and 42/43; three of them
(71/73, 43/45, 42/43) stopped at the budget of 150 evaluations while still improving. The values approach 1 from
below in steps of the form n/(n+1); this run does not decide whether the family's supremum is 1 or whether it is
attained.

## Run record

- Stage A ran first (2026-11-14 18:08). Stages B, C and D ran as `run.py --stages BCD --jobs 14` with a 4.5-hour limit;
  at 19:38 that run was stopped by the coordinating session (its own processes, by PID) because stage D could not
  complete within the limit, and restarted as `run.py --stages ABCD --jobs 14` with a 5-hour limit. Stages A, B and C
  resume from their records (`run_pool` skips recorded members), so no evaluation was repeated or lost; the 15 members in
  flight at the stop were evaluated again. Logs: `artifacts/run-log-BCD-part1.txt`, `artifacts/run-log-ABCD.txt` (exit 0).
  The restarted run took 10,443 s.
- Stage C drew 9,382,017 invalid parameter vectors to reach 2,000 valid members (acceptance about 0.02%): the builder's
  validity conditions (acyclic, single source, nonnegative flows with exact conservation, three simple paths per terminal)
  reject most independent draws.
- The local search steps of 1/24 can leave the normalisation `d_max = 1` (the best D member has `b_4 = 43/24`); the
  frontier value is invariant under a common scaling, so the values are unaffected and the recorded parameters are the
  unnormalised ones.

## Adversarial-validation record

- The evaluator agrees with the independent enumeration `frontier_value` on every instance where both finish (37 tests in
  PR #425) and reproduces 79/120 on Afrasyab's uniform member; P1 is a five-point calibration of the whole pipeline
  against Theorem 8 of arXiv:2609.17568 v1.
- No member reached the "P2 fails" branch, so the planned independent re-check of a value above 9/8 was not triggered.

## Consequences

- UFB-065 is answered on the sampled space: the odd-cycle family on C5, uniform or not, does not raise alpha* past 9/8,
  and no sampled member is a counterexample instance at all (frontier value at most 1).
- The climbs approach 1 from below with single-arc witness pricings; whether the supremum over the family is 1 is a
  new, bounded question (recorded in the backlog).

## How could this be wrong?

- The sampled space is finite: B is a grid, C is 2,000 random members, D is ten budgeted climbs. A member outside it
  could behave differently; nothing is claimed beyond it.
- The evaluator could be wrong on members unlike its tests; P1 and the 37 agreement tests are the evidence that it is
  not, and every value is an exact rational.
- The validity conditions exclude members that satisfy Afrasyab's realisation conditions in a different way; the
  conditions follow the spec of 2026-11-14 (`wip/caos-research/uf-afrasyab-construction-2026-11-14.md` in CAOS_MANAGE).
