# EXP-076 - Verdict: the C13 sibling-discard arithmetic EXTENDS in shape; gaps sourced

**Status: DECIDED at probe scope (all checks pass).**

## CORRECTION (2026-07-24, EXP-077): predictions 2-3 below were WRONG

EXP-077 (sourced from GGV1 1401.1784 + GGV2 1605.09430) showed the d_0 = 8
branch is arithmetically impossible: the bottom vertex of the max-x edge is the
SHARED corner A1 = (8,28) (below it the polygon turns to A2 at x = 11/4 < 8), so
d_0 | gcd(8,28) = 4 and d_0 = 8 would need y^{3.5}. Hence d_0 = 4 UNIQUELY (no
fork); q_1 = 4 as for the sibling; the correct forcing is R = x^2 y^7 (cubic)
of bidegree (2,10), NOT R' = x y^4 (y-1), and the post-shift candidate corner is
(8,4), NOT (8,12). Prediction 2's "(8,40) = 8(1,5)" reading bounded d_0 only by
the TOP vertex and is strictly weaker. The gap list of prediction 3 is
superseded by EXP-077's single narrowed gap (the multi-root shift terminus).
The original (wrong) text is kept below for the record.

1. **[MV, PASS]** The (8,32) sibling-discard arithmetic reproduces: the (4,-1)
   direction is well-defined (v = 4 on both A1 and A2); (8,28) = 4(2,7) coprime;
   R = x^2 y^7 (y-1) bidegree bookkeeping matches; post-shift corner (8,4).
2. **[MV, PASS]** The C13 analogues exist: (8,40) = 8(1,5) coprime; R' =
   x y^4 (y-1) with 8m-power matching the staircase; post-shift corner (8,12);
   one structural DIFFERENCE recorded: v_{4,-1}(A0) = -8 for C13 vs 0 for the
   sibling (may change the en-point computation).
3. **[D]** GAP LIST persisted (no discard claim until sourced): (i) the q' = 8
   divisibility hypothesis of Cor 7.4 at (8,40); (ii) Prop 3.29 (GGV2) at the
   corner (8,12); (iii) the en-point recomputation under v(A0) = -8. Next
   round: fetch GGV2 + GGHV22 section 3 from arXiv, verify the three gaps,
   then either the C13 discard closes (floor progress in [125,150]) or C13's
   Phase B reduction begins (our certificate machinery is already tooled for
   its final corner, shared with (72,108)).
