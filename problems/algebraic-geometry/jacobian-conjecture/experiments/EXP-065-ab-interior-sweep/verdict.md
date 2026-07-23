# EXP-065 - Verdict: CONFIRMED; hardening task 1 COMPLETE (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## Findings

1. **[MV]** All 20 interior lattice points of the a/b sub-polygon admit one-symbol
   certificates (chart a1 = 1, a0 = 2) with nonzero constant pairings (2240 through
   308281344000), in 98 s total.
2. **[D]** With EXP-062/063 (case c: 48 points + the trivially-free constant),
   HARDENING TASK 1 IS COMPLETE: the axis-symbolic interior coverage spans every
   interior lattice point of BOTH reduced polygon families. The simultaneous
   statement remains gated on EXP-064 (in flight), exactly per the audit.

## How could this be wrong?

- Axis coverage; one chart with a0 sampled (EXP-061 carries the chart-2 and
  a0-symbolic evidence); the simultaneous certificate is the gate.
