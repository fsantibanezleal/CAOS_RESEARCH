# EXP-141 verdict: UNKNOWN (the unsplit certificate exceeds the 6,000-prime budget)

Date: 2026-11-08. Hypothesis frozen at a5d1ad66.

## Result

- **Field step [D], checked exactly:** P = y^5 - y^4 + 3y^3 + 3y^2 + 26 is irreducible over Q and h(A(y)) = 0 mod
  P, so v -> A(y) identifies EXP-140's quintic field with L = Q[y]/(P); the 13 equations rewritten over L have
  integer coordinates of 35 to 552 digits (`artifacts/gates-output.txt`).
- **Gates PASS:** the five gate primes (unit; first four equations non-unit of dimension 4); the planted
  certificate recovered and verified twice, with a negative control; interpolation on random data. The planted gate
  caught a CRT representative bug before production (recorded in the gate output).
- **Certificate UNKNOWN:** 6,049 kept primes in [2^30, 2^31), every one lucky (no prime discarded), 58,605
  coordinates (11,721 cofactor terms). At the last checkpoint (6,046 primes, a modulus of about 56,400 digits) no
  coordinate reconstructs, sampled or full: in each, the numerator or the denominator has more than about 28,000
  digits. The budget is checked after each batch of 96, so the run overshot 6,000 by 49 primes.

## Changes during the run

The reconstruction gained a common-denominator pass and a sampled pre-pass (`crt_recon.c`), both checked on the
planted gate with an identical certificate, and `cert.py` now reads the WSL distribution and the crt_recon path from
the environment. Neither changes the method or a stored residue.

## Follow-up

The branch split of EXP-142 (E2 = a2 (q1^2 - c^2)^2 over L) reduces the system to two smaller ones; their
certificates also exceeded 6,000 primes, and EXP-143 continues them with an extended budget. The residues of this
run are kept in the data root, so the unsplit certificate can be continued the same way if the branches do not
close.
