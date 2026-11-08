# Structure of the Case 1 system over L, found while the certificates run (2026-11-07)

Exact facts about our 13 Case 1 equations E''_e over L = Q[y]/(P), P = y^5 - y^4 + 3y^3 + 3y^2 + 26 (EXP-141's
field step). Each is computed in exact rational arithmetic modulo P (python-flint) or by PARI `nffactor`, with the
script under `probes/` (set JCB141_WORK to EXP-141's `cert.py build` directory and JCB142_WORK to `branches.py`'s
output). Facts marked "mod p" come from Singular over F_p at a root of P and are evidence only.

## Exact

1. **E1 and E2 are proportional over L** (`gcd_probe.py`), so E1 is redundant.
2. **E2 = a2 (q1^2 - c^2)^2** with c = 5290384/2128893 y^4 - 89962304/2128893 y^3 + 1956896/2128893 y^2
   - 5999168/163761 y - 639627376/2128893 (`factor_probe.py`; checked again by `branches.py`, which EXP-142's
   reduction rests on). Every Case 1 zero has q1 = c or q1 = -c.
3. **On each branch q1 = +-c**, E1, E2, E4 and E8 vanish identically; nine equations remain in q0, q2, q3, q4, q5,
   with 22 to 52 terms and at most 479 digits (`branches.py`).
4. **Every branch equation is linear in q5** (`elim_probe.py`). E3, E7 and E13 are also linear in q3 (and E3 in
   q4), and their coefficients of q5 and of q3 are proportional over L (`prop_probe.py`). So E7 - lambda E3 and
   E13 - mu E3 are free of q5 and q3, and they are proportional to each other: one quadric
   S(q0, q2, q4) with 10 terms, degree 2 in each variable and 38-digit coordinates (18 after row reduction)
   (`combo_probe.py`).
5. **The nine branch equations have rank 8 over L** (`rref_probe.py`, Gauss-Jordan with q5, q3, q4, q2, q0
   eliminated in that order). Full row reduction makes the other rows taller (about 650 digits), so it does not
   shorten the system as a whole.

## Mod p (evidence)

6. Every leave-one-out subset of the 13 equations is still unit, and a greedy minimal unit subset is
   {E2, E3, E5, E6, E7, E10, E11} at three primes (`subset_probe.py`). On a branch, a minimal unit subset of the
   reduced basis keeps two rows of about 650 digits (`rref_subset.py`).
7. Dropping any one row from that minimal subset leaves a zero-dimensional ideal of 100 to 138 points
   (`dim_probe.py`), so a certificate through the finite point set would not be shorter.
8. Exact `std` over Q(y) with minpoly P on the branch q1 = +c, with S added, did not finish in one hour
   (`exact_branch.py`); EXP-139 and EXP-140 did not finish in six hours on the unsplit system.

## Reading

The system has a layered shape (a quadric S in three variables, then equations linear in q5 and q3) that a
triangular decomposition with explicit case splits (on the leading coefficients alpha + beta q0 of q5 and on the
q3 coefficient) could exploit, if the multi-modular certificates of EXP-141 and EXP-142 prove too tall.
