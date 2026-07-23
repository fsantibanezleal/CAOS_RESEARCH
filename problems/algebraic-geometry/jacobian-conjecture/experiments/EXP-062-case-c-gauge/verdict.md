# EXP-062 - Verdict: CONFIRMED; case c closes on its forced family (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## Findings

1. **[MV] The gauge works concretely:** the t = 4 system and its transported t = 1
   companion (rescaled target 8 x^2) give the SAME verdict (both EMPTY): emptiness
   is invariant along the torus orbit, so t normalizes to 1 WLOG on the stratum.
2. **[MV] The beta-symbolic certificates at t = 1:** pairing 23592960 beta on the
   bare family AND both interior-sampled variants (identical): vanishing only at
   beta = 0, where the (8,14) corner degenerates and the EXP-053/055 stratum
   certificates take over. CASE C IS CLOSED on its forced family for all t != 0
   and all beta.
3. **[MV] The free-interior upgrade opened:** four interior coefficients symbolic,
   one at a time: pairing the CONSTANT 368640 each time: nonvanishing for ALL
   values. The mechanical sweep over the remaining interior points is queued.

## Assembly state

All three Prop 4.3 branches are now certificate-covered on their forced families
(a/b: EXP-061; c: this record + the gauge). Remaining, mechanical: the rest of the
interior sweep; the orientation swap; then the assembled statement ((72,108)
discarded; floor to 125) goes to Felipe for phrasing validation per the checklist.

## How could this be wrong?

- The gauge argument's scalar bookkeeping (target rescaling) was machine-verified on
  one orbit sample; the general identity is one line of chain rule (stated).
- Interior generality: 4 of ~30 points symbolic so far + earlier samples; the sweep
  completes it.
