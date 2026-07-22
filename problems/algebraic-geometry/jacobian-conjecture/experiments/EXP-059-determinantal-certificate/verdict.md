# EXP-059 - Verdict: predictions 2-3 REFUTED (the minor is NOT constant); every sampled value NONZERO; run stopped after the decisive data (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt` (the run was STOPPED once the interim
data decided predictions 2-3: continuing the symbolic parts would have burned hours
confirming a foregone refutation; recorded per the honesty discipline).

## Findings

1. **[MV]** The base augmented minor exists: rank[M|r] = 125 at the base with an
   explicit 125-row selection and a huge nonzero determinant.
2. **[MV] Prediction 2 REFUTED:** the minor determinant VARIES with (t, eps) at
   every one of the sampled random points (40/40 differ from the base; at some
   points the row-label set itself changes). The constant-576 phenomenon lives in
   the CLEARED pairing normalization (content division), not in a constant minor:
   consistent in hindsight with EXP-044's growing clearing constants.
3. **THE LOAD-BEARING OBSERVATION [MV]:** every sampled determinant is NONZERO:
   at every parameter point ever tested across EXP-052..059, the reduced system
   remains inconsistency-certified. No candidate consistent point has appeared
   anywhere.

## The corrected closure frame

A single constant minor does not exist; the correct statement is that the IDEAL of
125 x 125 augmented minors has EMPTY vanishing locus on the stratum (t != 0): a
Nullstellensatz-type statement. Two honest routes forward: (a) study THIS minor's
zero locus (find points where it vanishes, if any rational ones exist, and certify
inconsistency there via alternative row selections: a covering-by-minors argument
with finitely many charts); (b) return to the ladder with all-orders solvability
proved (EXP-058) and attack termination directly. Route (a) first: it is finite
chart-checking, and the row-set-changed trials already exhibit the alternative
charts.

## How could this be wrong?

- Nonvanishing observed on samples only; the zero locus of the sampled minor is
  nonempty in principle (it is a hypersurface unless constant, which it is not):
  the chart-covering argument is REQUIRED, not optional; stated as the next task.
