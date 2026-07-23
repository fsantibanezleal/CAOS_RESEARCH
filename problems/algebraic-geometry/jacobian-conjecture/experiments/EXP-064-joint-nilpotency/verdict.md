# EXP-064 - Verdict: the pinned ladder does NOT terminate (chain stabilizes at dim 39)

**Status: prediction 3 REFUTED (machine-verified either-way outcome, as declared).**

## What ran

Two runs of the same declared computation. The original sympy run (run.py, background)
produced no flushed output in over 20 hours and was stopped without a claim (cap
discipline; stdout was block-buffered on top of sympy Matrix overhead). run2.py is the
identical mathematics re-staged operationally: exact Fraction arithmetic on plain
lists, an incremental-elimination span reducer replacing repeated rank() calls, and
per-step flushed prints. Total runtime 88 s (artifacts/output-run2-2026-07-23.txt).

## Results against the declared predictions

1. **[MV, PASS]** The rref-with-transform right-inverse solves a first-order
   corrector and the solution verifies identically (A x = b residual zero).
   M0^T is 125 x 289 on the H-pool, rank 124, one consistency row (the kernel is
   the constants, EXP-058, reconfirmed).
2. **[MV, PASS]** The Krylov closure V_inf of Lambda_0 under the 51 operators
   A_i = sigma T_i is computed exactly and is bounded: dim 122, closed in 3
   iterations.
3. **[MV, REFUTED]** The descending chain W_{k+1} = sum_i A_i W_k does NOT reach
   zero: it descends monotonically 121, 111, 101, 91, 81, 74, 67, 60, 54, 49, 45,
   42, 40, 39 and STABILIZES at dim 39 (step 15 reproduces the span of step 14
   exactly). The operators are NOT jointly nilpotent on V_inf for THIS pinned
   sigma: this ladder does not terminate.

## What this does and does not mean

- It does NOT overturn all-orders solvability (EXP-058): every corrector exists at
  every order. What fails is TERMINATION of this particular recursion: the pivot-
  pinned right-inverse recirculates a 39-dimensional invariant core forever.
- It does NOT prove the simultaneous-symbolic certificate impossible: sigma has a
  large gauge freedom (ker of the solve map has dimension 289 - 124 = 165 per
  application), and joint nilpotency is a property of the CHOSEN sigma. A different
  gauge may terminate; alternatively the finite-degree covector can be attacked
  DIRECTLY, bypassing sigma entirely (the degree-D truncation is one finite exact
  linear system per D; this is the declared successor, EXP-067).
- The floor-raise claim therefore REMAINS GATED. The published Paper B (DOI
  10.5281/zenodo.21503368) already states exactly this certified scope; no
  published claim needs amendment.

## Cap discipline note

The sympy run consumed far beyond the cap with zero flushed output; verdict taken
entirely from run2. Recorded lesson: long exact-linear-algebra runs get the
Fraction backend and flushed staged prints FIRST, background sympy never again for
this shape of computation.
