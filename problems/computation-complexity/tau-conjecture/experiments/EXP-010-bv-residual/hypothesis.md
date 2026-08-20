# EXP-010: the final-pm residual as decidable bit-vector SAT (QF_BV)

Declared 2026-08-20, before the run. Successor to EXP-008 per its
verdict: same evaluation encoding, arithmetic moved from Int (NIA,
solver-incomplete) to 64-bit signed bit-vectors (QF_BV, DECIDABLE: the
solver cannot return unknown; only sat/unsat/timeout). This is the
Fuhs-Schneider-Kamp regime (CDCL over bit-blasted structure search).

## The claim shape (precise scoping, committed)

All evaluation columns (the 7 roots AND the nonzero-witness column y,
with y in [0, 256]) carry signed no-overflow/no-underflow guards at
width 64. Therefore:

- UNSAT proves: NO 8-gate program with final gate +- involving the 7th
  value has 7 distinct integer roots in [-32, 32] SUCH THAT all gate
  values at those roots, and at some non-root y in [0, 256], fit in
  signed 64 bits. (A nonzero f of degree <= 2^8 always has a non-root
  in [0, 256], so the y column only adds the value-boundedness scope,
  not a root-pattern restriction.)
- SAT with a tclib-replayed witness proves z_max(8) >= 7 outright.
- This is a WINDOWED exclusion (roots and values bounded), stated as
  such; every census witness ever observed fits these windows with
  orders of magnitude to spare.

## Phases and predictions

1. Known-answer (6 gates, 5 roots, bound 8, no final restriction): SAT
   with valid replay. PREDICTION: passes (QF_BV searches structure
   where NIA could not); this also retroactively confirms EXP-008's
   diagnosis.
2. Residual (8 gates, 7 roots in [-32,32], final pm): PREDICTION:
   UNSAT (fifth emptiness-style commitment; the record is 1-of-4).

## Budget and kill (P6)

Known-answer 1 h cap; residual 12 h cap (QF_BV may be slow; timeout is
a recorded INCONCLUSIVE, not unknown-ambiguity). CEGAR loop budget 50.
Detached run; per-phase checkpoints; monitor armed.
