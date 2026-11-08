# EXP-143 preflight: the branch certificates of EXP-142 with an extended budget (JCB-103)

Date: 2026-11-08. Status: frozen before the continuation (EXP-142 ended UNKNOWN at its budget). CPU only.

## Why

EXP-142's two branch certificates did not reconstruct within about 6,080 kept primes (moduli of about 56,700 digits: every sampled coordinate has a numerator or denominator above about 28,000 digits).
Probes recorded in `EXP-142/structure.md` show no shorter exact route: exact standard bases over Q(y) do not
finish, a point-set certificate has 100 to 138 points, and a resultant chain ends in a univariate polynomial of
degree 568. The cofactor heights are therefore expected above 28,000 digits, and the multi-modular route remains
the one whose cost is linear in the height.

## Method

EXP-142's method, unchanged (`cert.py`, the same support rule, interpolation, CRT with held-out checks and the
common-denominator pass, exact verification twice). The runs resume from EXP-142's stored residues and kept
primes (the work directories are kept), with all processes once EXP-141 ends.

## Budget and stop condition

Up to 20,000 kept primes per branch (moduli of about 186,000 digits) and 24 hours of wall-clock time on up to 28
processes in total. Otherwise UNKNOWN with the measured lower bound on the heights.

## Prediction and claim

As EXP-142.
