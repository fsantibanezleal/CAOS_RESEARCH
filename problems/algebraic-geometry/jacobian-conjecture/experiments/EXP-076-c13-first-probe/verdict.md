# EXP-076 - Verdict: the C13 sibling-discard arithmetic EXTENDS in shape; gaps sourced

**Status: DECIDED at probe scope (all checks pass).**

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
