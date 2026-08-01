# Correction note for pgb-union.json (2026-08-01, same day as the run)

EXP-012's exact-reproduction control (its P1b) caught an order-inconsistency
bug in this experiment's harvester: sympy's `groebner(...).polys` default to
LEX ordering regardless of the requested basis order, so `monoms()[0]`
returned the LEX leading monomial of each grevlex basis element. The 16
exponent vectors archived in `pgb-union.json` are therefore LEX leads of
grevlex basis polynomials, NOT the grevlex leading ideal of subideal 3.

Impact on EXP-011's verdict: NONE of its conclusions change. The P4 bound was
computed from these monomials and reported as VACUOUS (d_pgb = 10) and
"informative-weak, below the declared success threshold"; a vacuous bound
that is additionally order-inconsistent is still vacuous, and no downstream
claim consumed it. The verdict's phrase "produced by a reduced grevlex
Groebner basis" is corrected by this note: the basis WAS grevlex, the
harvested leads were not.

The file is retained unmodified for the record; the harvester
(`pgb_worker.py`) is fixed in place with the same date, and EXP-012's P1b
control now uses a grevlex-correct sympy recomputation as its reference.
This is exactly the failure class the exact-reproduction control was declared
to catch, one experiment after the instrument's first live run.
