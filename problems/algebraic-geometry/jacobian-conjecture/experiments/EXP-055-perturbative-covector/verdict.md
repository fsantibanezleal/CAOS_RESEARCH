# EXP-055 - Verdict: CONFIRMED 1-2; prediction 3 REFUTED as declared (order-1 termination fails); the construction advances one order (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt` (run exceeded the 590 s cap and completed in background at 1374 s for the 26 solves; cap discipline noted).

## Findings

1. **[MV]** rhs is the constant x^2 vector; Lambda0 is GLOBALLY left-null on M0
   (column-by-column, symbolic t): the base is sound.
2. **[MV] First-order universality.** All 26 entering lower monomials admit
   correctors Lambda_i with Lambda_i M0 = -Lambda0 M_i and the (2,0)-entry pinned
   (pairing stays exactly 576 to first order); supports localized (<= 19 rows).
3. **[MV] Prediction 3 REFUTED as declared:** 15 of 36 tested second-order pairs
   have nonzero residuals: Lambda(eps) does NOT terminate at order 1. The
   construction is not blocked: the same solvability mechanism applies to the
   order-2 correctors Lambda_ij (15 small solves on the tested sample; the full
   pair set next round), with termination re-tested at order 3.

## Honest state of the (72,108) closure

Emptiness now holds for all t and all lower coefficients TO FIRST ORDER around the
bare stratum, with per-stratum exact certificates (EXP-053) at every sampled point.
The remaining ladder: order-2 correctors -> order-3 residual test -> (if terminating)
the universal polynomial covector and the stratum closes; then the dossier's other
forcing branches; then the floor rises to 125.

## How could this be wrong?

- 36 of 351 second-order pairs tested (sampled); the full sweep is next.
- The restricted-row search space (i - j <= 2, degree window) was generous but fixed;
  an unsolvable higher-order corrector could require enlarging it (record if so).
