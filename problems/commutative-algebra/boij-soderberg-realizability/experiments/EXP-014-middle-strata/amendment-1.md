# EXP-014, amendment 1: the budget of the control (7, 11)

Date: 2026-11-20, written before any computation of families V and W. The hypothesis (`hypothesis.md`, commit
1ba04950) is not edited; this file records the one change made to it and why.

## What happened

Gate G1, family part, requires pure members in the O-stratum S(4; 0, 3) at the control (7, 11), with the budget of
family K, 30,000 members. The stratum has 259,371,025 members there. The run of family K examined 30,000 random
members: 559 of rank r, 8 with the pure Hilbert function, none pure. By the hypothesis the run stopped at the failed
gate, and families V and W were not computed.

## Why the gate was wrong, not the known answer

The known answer is that the stratum holds pure members: EXP-010 found them at (7, 11) in S(4; 0, 3) (its family C,
accepted and re-checked). A diagnostic by the implementer, outside the hypothesis and not stored in the results,
examined the same stratum with the same seed rule and a budget of 300,000: 236,000 members before the early stop,
4,259 of rank r, 39 with the pure Hilbert function, 37 tables, 5 pure. So about one member in 47,000 is pure there,
and a sample of 30,000 has no pure member with probability about one half. The gate asked a sampled control for a
certainty its budget could not give. The error is in the hypothesis written by the coordinating session.

## The change

The control (7, 11) of family K runs with budget 300,000 (the early stop at 5 pure members applies as elsewhere).
Nothing else changes: the other controls, families V and W, their budgets, the gates, the predictions and the order.
The stored result of the 30,000 sample is kept in this file (above) and replaced in `artifacts/results.json` by the
run with the amended budget.

## Note for the verdict

The predictions were frozen before the count of conditions of the note
`context/2026-11-20-pairs-over-the-invariants.md` was known; that note (under review) says that P1 at e = 8, 10, 12
is likely to fail. The predictions are not changed.
