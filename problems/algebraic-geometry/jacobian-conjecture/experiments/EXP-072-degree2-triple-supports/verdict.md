# EXP-072 - Verdict: DEGREE 2 CLOSED (triple support, sound pipeline)

**Status: DECIDED. No degree-2 covector exists; the decision now stands on the
corrected arithmetic with the regression gate green.**

## Results (artifacts/output-2026-07-23.txt, ~40 s)

0. **[MV, PASS]** Setup invariants (rank 124, kernel 165, 51 ops).
1. **[MV, PASS]** Regression gate: 20 sampled pair supports reproduce EXP-071
   run4's feasible verdicts on the imported modfrac pipeline.
2. **[MV, DECIDED]** The triple-support sweep hit an INFEASIBLE subsystem at
   support {(0,1), (1,0), (3,5)} (both primes 2147483629 and 2147483587;
   conclusive over Q for this integer system): NO DEGREE-2 COVECTOR EXISTS.
   The support contains TWO of the eight degree-1 blockers ((1,0), (3,5)) plus
   (0,1): the degree-1 obstruction pattern persists at triple scope after all,
   visible only one support tier up.

## Standing

Degree 1 closed (EXP-067, exact); degree 2 closed (this experiment, sound mod-p,
two primes, gate-verified pipeline; EXP-070's retracted claim is SUPERSEDED by
this independent decision at a DIFFERENT support). Degree 3: open at pair scope
(EXP-071); its triple-support sweep is the declared next tier. If degree 3
closes too, the pattern-theorem proposal (every truncation degree obstructed)
goes TO FELIPE as a proposal. The floor-raise stays gated; the published Paper B
scope is unchanged.
