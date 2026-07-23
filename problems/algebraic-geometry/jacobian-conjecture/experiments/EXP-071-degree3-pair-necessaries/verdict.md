# EXP-071 - Verdict: the retraction round; degrees 2 and 3 OPEN at pair necessaries

**Status: DECIDED at pair scope, with a MAJOR CORRECTION to the record.**

## Results (artifacts/output-run4-2026-07-23.txt; runs 1-3 record the bug hunt)

1. **[MV, PASS]** Setup invariants (rank 124, kernel 165, 51 ops).
1b. **[MV, RETRACTION CONFIRMED]** The corrected degree-2 pair sweep: ALL 1326
   pair subsystems FEASIBLE mod p. EXP-070's closure was an artifact of
   int(Fraction) truncation (see its RETRACTION addendum): DEGREE 2 IS OPEN at
   pair necessaries.
1c. **[MV, PASS]** EXP-069a re-audited under correct arithmetic: all diagonal
   triples feasible (its conclusion was right despite sharing the bug class).
2. **[MV, DECIDED; expectation refuted]** The degree-3 pair sweep: ALL 1326
   pair subsystems FEASIBLE: degree 3 also open at pair scope.

## The declared-gate story

The regression gate declared in this experiment's hypothesis caught the bad
arithmetic path in run 1; run 2 fixed an int64 overflow (16-bit split matmul);
run 3 fixed the real bug (modfrac: rationals reduced as num * den^-1, never
int()); run 4 is the corrected decision. Every run's artifact is kept.

## Standing and the declared next steps

Degree 1 closed (EXP-067, exact). Degrees 2 and 3: no pair-support obstruction.
The truncation route is ALIVE. Next: (a) triple-support necessaries for degree 2
(cost one tier up; any hit closes it); (b) attempt to CONSTRUCT a degree-2
covector mod p (decide the full joint system by building a solution candidate,
then exact confirmation staged; an upgrade proposal would go TO FELIPE only
after the exact pass); (c) the [125,150] frontier (C13).
