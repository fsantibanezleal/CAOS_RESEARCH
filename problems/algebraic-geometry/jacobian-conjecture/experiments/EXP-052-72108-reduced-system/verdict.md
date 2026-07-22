# EXP-052 - Verdict: CONFIRMED; the reduced (72, 108) system is on the bench (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`. Input: the GGHV dossier (Prop 4.3).

## Findings

1. **Sizes [MV].** The reduced polygons enumerate to 61 (P side) and 125 (Q side)
   lattice points: the open case's system is SMALL in reduced coordinates.
2. **Sampled emptiness [MV].** Four random rational P samples (corners forced nonzero)
   and one structured sample (top edge y^8 (xy - 1)^8): the linear system
   [P, Q] = x^2 over the full Q polygon is INCONSISTENT every time (12-14 s per
   random sample; 1.9 s structured): no partner exists for any tested P.
3. **Framing [D].** Sampled evidence toward closing the lone open pair below 125;
   the decisive object is the parametrized certificate over ALL P (61 parameters,
   linear in 125 unknowns): exactly the cleared-certificate machinery's shape, and
   the declared next-round target. GGHV never printed this system; ours is
   reconstructed from their Prop 4.3 (dossier, with DERIVED flags).

## How could this be wrong?

- The reduced-polygon transcription is the dossier's (verified against the LaTeX
  sources, with two source typos flagged there); the bracket target x^2 is Prop 4.3's.
- Five samples; the all-P certificate is the real closure.
