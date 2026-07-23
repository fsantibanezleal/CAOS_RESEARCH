# EXP-076 - C13 first probe: does the (8,32) discard arithmetic extend to (8,40)?

- **Question.** Which parts of [GGHV22] section 3's discard of the (8,32) chain
  (C13's sibling) carry over arithmetically to C13's (8,40) chain?
- **Motivation.** Dossier head start: the sibling shares A1 = (8,28), A2 =
  (11/4,7), (m,n) = (3,2); its discard runs: direction (4,-1) from the A1/A2
  valuation equality; the Cor 7.4 forcing l_{1,0}(P) = lambda(x^2 y^7(y-1))^{4m}
  from (8,28) = 4(2,7); post-shift corner (8,4); impossible by [GGV2, Prop 3.29].
  The analogous objects for (8,40) are computable NOW; the two source-dependent
  steps (the q | d0 divisibility and Prop 3.29's exclusion at the new corner)
  are flagged UNVERIFIED pending the primary sources (next round).
- **Predictions.** 1. [MV] The (8,32) arithmetic reproduces: v_{4,-1}(A1) =
  v_{4,-1}(A2) = 4; (8,28) = 4(2,7) with gcd 1; R = x^2 y^7 (y-1) has bidegree
  (2,8) with 4m R-power matching st (8m,32m); post-shift corner (8, 32-28) =
  (8,4). 2. [MV] The (8,40) analogues: v_{4,-1}((8,40)) = -8 (differs from the
  sibling's 0: recorded); (8,40) = 8(1,5) gcd 1; R' = x y^4 (y-1) bidegree (1,5)
  with 8m power matching (8m,40m); post-shift corner (8,12). 3. [D] Gap list
  persisted: q' = 8 | d0 and Prop 3.29 at (8,12): UNVERIFIED, source fetch next.
- **Method.** Exact integer arithmetic; tiny script.

Declared 2026-07-24 before the run.
