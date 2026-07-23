# EXP-067 - Verdict: degree 1 CLOSED (no degree-1 covector; 8 blocking operators)

**Status: DECIDED. Prediction 2 refuted; predictions 1, 3, 4 verified; the
experiment's question is answered: no eps-degree-1 covector exists.**

## Results against the declared predictions (artifacts/output-2026-07-23.txt, 288 s)

1. **[MV, PASS]** Order-1 solvability reconfirms: all 51 particular solutions
   exist (EXP-058 consistent). Setup: M0^T is 125 x 289 on the pool, rank 124,
   left-kernel dimension 165.
2. **[MV, REFUTED]** Eight single-index blocks are INFEASIBLE: no kernel
   adjustment achieves Lambda_i M_i = 0 for
   i in {(1,0), (3,5), (4,6), (4,7), (5,8), (7,13), (8,14), (8,15)}.
   Notably (1,0) is the x-term itself, and the rest cluster just below the
   staircase top edge.
3. **[MV, PASS]** All 1275 pair blocks are feasible in isolation: the obstruction
   at degree 1 is carried ENTIRELY by the diagonal (2e_i) conditions, not by the
   mixed (e_i + e_j) couplings.
4. **[MV, PASS]** The full degree-1 system is decided: INFEASIBLE mod the prime
   2147483629 (rank 1116 of 8415 unknowns when inconsistency is hit at the
   single-block equations). For this all-integer system, mod-p inconsistency is
   conclusive over Q. DEGREE 1 IS CLOSED.

## The structural reading (CORRECTED by EXP-068)

**Correction (2026-07-23, EXP-068):** the paragraph below was WRONG as first
written. EXP-068 showed the cokernel covector c annihilates ALL bracket images:
solvability conditions hold automatically at every order (the dual annihilation
identity), so blocks do NOT reduce to scalar obstructions against c. The
degree-1 infeasibility found here is a VECTOR-level fact (the 8 singles' 125-dim
conditions), and higher degrees must be decided at the vector level too
(EXP-069). The original text is kept below for the record.

## The structural reading (for the next experiment, declared here) [SUPERSEDED]

The cokernel of the pool system is ONE-dimensional (rank 124 of 125): every block
condition therefore reduces to ONE scalar obstruction, the pairing of its
right-hand side against the cleared covector c spanning the cokernel. A single
block i is infeasible exactly when c annihilates the image of the kernel under
M_i (c^T B_i = 0) while the particular pairing c^T (P_i M_i) is nonzero. The
degree-1 refutation says this happens for exactly 8 operators. This makes the
whole truncation question a question about ONE explicit linear functional: the
obstruction calculus (which combinations of blocks can be cancelled at which
degree) is finite and computable degree by degree, and a closed-form pattern in
the 8 blocking operators is the plausible route to a THEOREM (either: some finite
degree closes, with an explicit certificate; or: every degree is obstructed,
closing the truncation route honestly).

## Consequences

- The simultaneous-symbolic certificate does not exist at degree 1; the
  floor-raise claim REMAINS GATED (the published Paper B scope is unchanged and
  correct).
- Next: the obstruction-functional analysis (EXP-068): compute c, the 8
  obstruction scalars, and the degree-2 system's obstruction pattern directly.
