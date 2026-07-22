# EXP-050 - Verdict: CONFIRMED; the first certificates at the (72, 108) degrees (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## Findings

1. **First contact [MV].** Two sampled degree-72 shapes with the GGHV corner geometry
   (corner (16, 56) = 2 (8, 28); a swallowed linear vertex; one with a two-term top
   ladder): the similarity-filtered windows at N = 108 (143 unknowns, ~320 equations)
   are EMPTY in 1.2-1.4 seconds each. By similarity nesting, ALL Keller partners of
   degree <= 108 are excluded for these samples: the first machine certificates at the
   lone open degree pair below 125.
2. **Cost verdict [D].** Seconds per certificate at the open pair's scale: the
   systematic sweep is limited only by shape transcription (the GGHV ((8,28),(3,2))
   parametrized family from the primary text), queued as the next N2 step.

## Honest framing

These are SAMPLED shapes with the right corner and degrees, not the GGHV counterexample
variety itself; a full closure of the (72, 108) case (which would raise the JC(2) floor
to 125) requires sweeping their parametrized family. The pipeline cost makes that sweep
an afternoon of machine time once the shapes are transcribed.

## How could this be wrong?

- The filter's soundness assumptions as in EXP-047 (similarity, both degrees > 1).
- Two samples; the parametrized sweep is the real target.
