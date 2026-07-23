# EXP-061 - Verdict: CONFIRMED; cases a) and b) close on their forced families (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## Findings

1. **[MV]** Chart a1 = 1: cleared certificates with MONOMIAL pairings 200 a0^3
   (bare), 600 a0^3 and 560 a0^4 (interior samples), on the sub-polygon system
   (25/47 lattice points; 2-23 s per run). Chart a0 = 1: pairing 200 a1^4 (3 s).
2. **[MV] Locus vs stratum.** Chart-1 pairings vanish only at a0 = 0, where the
   (8,14) corner coefficient dies: excluded by cases a/b's own polygon forcing
   ((8,14) is a VERTEX there); chart-2 vanishes only at a1 = 0, excluded likewise
   by the (8,16) vertex. The two charts cover each other's gauge boundary; the
   vanishing loci miss the stratum entirely.
3. **Assembly [D].** With the verbatim edge verification (assembly checklist,
   session 36) and EXP-060's case-c certificate (in flight), all three branches of
   Prop 4.3's reduced systems are certificate-covered on their forced families;
   interior coefficients stand at sampled generality (the free-coefficient upgrade
   follows the established pattern and is queued), plus the orientation swap.

## How could this be wrong?

- Interior generality is sampled (two samples per chart family); the upgrade run is
  queued, cheap, and follows the EXP-042 discipline.
- The a/b Q-side coverage rests on the polygon-subset argument (bigger-polygon
  emptiness implies smaller), stated in the checklist.
