# EXP-003 verdict (2026-07-24)

Hypothesis: `hypothesis.md` (declared and committed BEFORE the run, commit db85647).
Pipeline: `run.sh` (WSL2 Ubuntu 24.04; gfan 0.7 from the author tarball, two-line
cstdint patch for gcc 13; binary + tarball SHA-256 in `artifacts/hashes.txt`);
pointedness checker `check_pointedness.py`. Artifacts: `artifacts/` (system, inputs,
f-vectors, rays, hashes); full prevariety outputs (0.8 + 1.7 MB) at
`E:\_Datos\caos-research\central-configurations\EXP-003\`. Recorded run: 2026-07-24,
30 threads.

## Verdict: CONFIRMED on all three predictions (exact reproduction)

| Prediction | Outcome | Machine result |
|---|---|---|
| P1 system inventory | CONFIRMED | `gfan _nbody -N5 --masses --alsosymmetric --cayleymenger2` emits exactly 35 polynomials in Q[m1..m5, r12..r45] (20 asymmetric AC + 10 symmetric AC + 5 planar Cayley-Menger) |
| P2 powers-of-3 valuations | CONFIRMED | F_VECTOR = 1506 4744 8586 8787 4652 993 (EXACT match with JL25); pointedness: 1591 rays, 85 unbounded directions, ZERO with a positive coordinate: globally pointed recession cone, exactly as published. Wall time 5 m 52 s on 30 threads (146.8 cpu-min) |
| P3 squares valuations | CONFIRMED | F_VECTOR = 3586 12012 18531 15625 7072 1357 (EXACT match with JL25). Wall time 5 m 34 s (140.6 cpu-min) |

## What this establishes

Our toolchain now INDEPENDENTLY REPRODUCES the current state-of-the-art generic-mass
finiteness certificate for planar 5-body central configurations (Jensen-Leykin,
arXiv:2301.02305v2), end to end, from the author-published commands, in about 6
wall-clock minutes per valuation on this machine. The tropical lane is OPEN: the
frontier experiments the paper explicitly calls for (valuation search, CCB-030;
equation-variant prevariety shrinking, CCB-031, including toward n = 6 where their
single tried valuation was inconclusive at ~100 cpu-days) can now run on validated
infrastructure. Throughput estimate for planning: this machine delivers ~25
cpu-minutes per wall-minute at full width, so a JL25-scale n = 6 attempt (~100
cpu-days) is ~2.8 wall-days here; valuation/equation-variant screening at n = 4/5
(minutes each) is the rational first move.

## Adversarial-validation record (methodology/03)

- The reproduction IS the adversarial check of our toolchain against published
  independent results: two distinct valuation datasets, both exact-matching
  digit-for-digit f-vectors, plus the qualitative pointedness property verified by
  an independent parser (`check_pointedness.py`, exact Fraction arithmetic on the
  rays).
- Environment honesty: gfan required a two-line `#include <cstdint>` patch to build
  under gcc 13 (recorded in run.sh; no algorithmic code touched); the `--bits 64`
  fast pass was used, as in the paper's reported timing; the paper's overflow-checked
  templated rerun (~10x slower) was NOT repeated here and is noted as the
  hardening option if this rung ever carries a novel claim rather than a
  reproduction.
- The system generator was cross-checked against our independent cclib builders at
  inventory level (35 polynomials, the expected three families); a term-level
  equality check between gfan's `_nbody` output and cclib's cleared forms is queued
  for the EXP-004 planning pass (it requires normalizing monomial units).

## How could this be wrong?

- We matched f-vectors and pointedness, not the full face lattices; a hash-level
  comparison of the complexes is not possible against the paper (they publish
  f-vectors and claims, not raw outputs). Residual risk of "right numbers, different
  complex" is negligible but nonzero; the CCB-030 experiments will exercise the same
  code paths densely.
- The pointedness parser assumes gfan's documented RAYS semantics under
  --usevaluation (0th coordinate flags points vs directions); JL25 4.1.1 states the
  same reading and the counts are consistent (85 unbounded directions among 1591
  rays).

## Consequences for the strategy

1. CCB-029 DONE. The tropical lane infrastructure is validated.
2. Next experiments in the lane (hypothesis-first, per JL25's explicit call):
   EXP-005-class valuation screening at n = 5 (CCB-030) and equation-variant
   prevariety shrinking at n = 4/5 (CCB-031: add/remove Dziobek, e_IU, G-subsets and
   measure f-vector + pointedness deltas). A principled n = 6 shortlist is the goal
   before any multi-day n = 6 run is spent.
3. The msolve lane (CCB-025, census engine) proceeds in parallel for EXP-004 (P2
   completion + the n = 4 equal-mass planar census).
