# EXP-047 - Verdict: CONFIRMED; the N2 pipeline runs at target scale in seconds (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## Findings

1. **Full-window certificates at the case-64 degrees [MV].** Three degree-48 samples of
   the B = 16 / F1 flavor (the pure shape x + R0(1)^3; a swallowed variant with x^2; a
   mixed variant with x^2 + 5 x^3 y^4): the similarity-filtered window at N = 64 (111
   unknowns, 270 equations) is EMPTY in 2.4-3.6 seconds each. By the verified similarity
   theorem (partners of any degree 2..64 must fit the nested scaled polygons), each run
   excludes ALL Keller partners of degree <= 64 for its sample.
2. **Framing [D].** These are the classical case-64 degrees (Moh's fully-detailed case;
   Heitmann): sampled-level machine replication on frontier-shaped polynomials. The
   value demonstrated is the COST: seconds per full-window certificate at the scale
   where the open territory lives; the identical pipeline at max degree > 150 or on the
   (72, 108) system produces genuinely new exclusions at comparable cost.

## What this changes

- Route N2 is validated end to end at target scale. Next: transcribe the (72, 108)
  shape data (GGHV ((8,28),(3,2)) family) and the beyond-150 B = 16 shapes, then run
  systematic sampled sweeps (lower-class terms swept, not just spot samples) with the
  same filter; the runs are seconds each, so wide sweeps are affordable.

## How could this be wrong?

- Sampled shapes (lambda_0 = 1, few lower-term variants); the systematic lower-class
  sweep is the next run.
- The filter's soundness leans on the similarity theorem's hypotheses (both degrees
  > 1; N^0 convention), which the dossier verified via Lee-Li's verbatim quotation; a
  degree-1 partner is an automorphism case anyway.
