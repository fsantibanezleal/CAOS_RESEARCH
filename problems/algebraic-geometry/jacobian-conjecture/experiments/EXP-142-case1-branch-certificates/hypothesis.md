# EXP-142 preflight: Case 1 split at q1 = +c and q1 = -c, one certificate per branch (JCB-103)

Date: 2026-11-07. Status: frozen before the production computation. CPU only. Runs alongside EXP-141, which
continues unchanged under its own frozen plan.

## Why

EXP-141 (one cofactor certificate for the whole Case 1 system over L) had reconstructed no coordinate after about
960 primes (moduli of about 8,900 digits). Facts measured since, before this file (probes, not results):

1. Over L, E1 and E2 are proportional, and PARI `nffactor` gives E2 = a2 (q1 - c)^2 (q1 + c)^2 with
   c = 5290384/2128893 y^4 - 89962304/2128893 y^3 + 1956896/2128893 y^2 - 5999168/163761 y - 639627376/2128893.
   These are the two branches s = +c, -c named in JCB-103.
2. On either branch (q1 replaced by +c or -c) the equations E1, E2, E4 and E8 vanish identically; nine equations
   remain in q0, q2, q3, q4, q5, with 22 to 52 terms and at most 479 digits (EXP-141: 6 variables, up to 84 terms,
   552 digits).
3. At one root of P modulo 2147480941, Singular `lift` writes 1 in each branch ideal in 2 seconds with 6,054
   cofactor terms (8 of the 9 equations used); EXP-141 needs 11,721 terms at 3 to 10 seconds per root.

## Method

1. **Reduction [D].** Check exactly in L[q1] (`branches.py`) that E2 = a2 (q1^2 - c^2)^2 with a2 != 0. Then every
   common zero of Case 1 has q1 = c or q1 = -c, so Case 1 is empty iff both branch ideals
   I_sigma = (E''_e(q0, sigma c, q2, ..., q5)) of L[q0, q2, ..., q5] are the unit ideal (EXP-140's reduction and
   EXP-141's field step carry over unchanged).
2. **Certificates.** For each branch, EXP-141's pipeline (`cert.py`: lifts at the five roots of P modulo primes in
   [2^30, 2^31), the same support rule, interpolation, CRT with held-out checks, FLINT reconstruction) on the
   branch equations made primitive over Z.
3. **Exact verification [D].** For each branch, sum_e g_e E_e = 1 checked exactly in Q[q, y] modulo P
   (python-flint) and again in Singular over Q(y) with minpoly P. Both branches certified gives Case 1 empty.

## Gates (before production)

1. The factorisation identity holds exactly (branches.py prints it; failure stops the experiment).
2. At EXP-140's five gate primes, each branch system specialised at a root of P is the unit ideal.
3. The pipeline gates of EXP-141 (planted certificate, negative control, interpolation) apply unchanged: same code.

## Prediction

Both branch certificates are found and verified (MODERATE; heights unknown, but smaller than EXP-141's are
expected from the smaller inputs).

## Budget and stop condition

At most 12 hours of wall-clock time, 4 parallel processes per branch while EXP-141 runs (more once it ends), at
most 6,000 kept primes per branch. Otherwise UNKNOWN with the measured heights.

## What a CONFIRMED verdict claims

The same as EXP-141's: Case 1 of GGHV Proposition 4.3 at (72,108), as encoded by our 13 compatibility equations,
has no solution over the algebraic closure, with exact certificates checked twice; nothing beyond Case 1.
