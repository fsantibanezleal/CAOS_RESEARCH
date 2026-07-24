# EXP-077 - Verdict: the C13 d_0 FORK COLLAPSES; the discard's forcing extends; the endgame exclusion is DERIVATION NEEDED

**Status: DECIDED (all checks pass; regression gate green).** No floor-moving
claim is made here; the residual is a single, narrower source-dependent step.

## The decision

The dossier / EXP-076 feared a FORK: reading (8,40) = 8(1,5) as coprime gave
d_0 <= 8, so with q_1 = 4 the divisibility 4 | d_0 would allow d_0 in {4, 8} and
the single-shape discard would fail verbatim. **That fork does not exist.**

1. **[MV, PASS] q_1 = 4 for C13, identical to the sibling.** By [GGV1 =
   arXiv 1401.1784, Prop "Case II" tex 2563 + Thm 7.6(3) tex 4288],
   en_{4,-1}(F_1) = mu (abar, bbar) with (abar, bbar) = (2,7) the primitive of the
   shared corner A1 = (8,28) = 4(2,7), d = gcd(8,28) = 4, and mu = (rho+sig) /
   v_{4,-1}(2,7) = 3 / 1 = 3, so en(F_1) = (6,21) and q_1 = d/gcd(mu,d) = 4. The
   (4,-1) leading form of P is exactly the shared edge A1--A2 (both at
   v_{4,-1} = 4); A0 sits strictly below (v_{4,-1}(A0) = -8 for C13, 0 for the
   sibling) and never enters the en-point. The v_{4,-1}(A0) difference the earlier
   probe recorded is real but does NOT change q_1.

2. **[MV, PASS] d_0 <= 4 for C13, not <= 8.** l_{1,0}(P) = R^{m d_0} forces
   d_0 * st_{1,0}(R) = st_{1,0}(P). The bottom vertex of the max-x (x = 8) edge is
   st_{1,0}(P) = A1 = (8,28), SHARED with the sibling (below A1 the polygon turns to
   A2 at x = 11/4 < 8). Hence d_0 | gcd(8,28) = 4. **d_0 = 8 is arithmetically
   impossible** (28/8 is not an integer; R would need y^{3.5}). The (8,40) = 8(1,5)
   reading bounds d_0 only by the TOP vertex A0 (gcd 8) and is strictly weaker; the
   shared BOTTOM vertex binds d_0 <= 4. **This corrects EXP-076**, whose
   d_0 = 8 / R' = x y^4(y-1) branch was wrong (its bottom is (8,32), not the shared
   (8,28)).

3. **[MV, PASS] d_0 = 4 uniquely -> the fork collapses.** q_1 = 4 | d_0 and
   d_0 <= 4 give d_0 = 4, exactly as the sibling. The forcing step of the discard
   EXTENDS to C13.

4. **[MV, PASS] The endgame SHAPE differs.** With d_0 = 4, R = x^2 y^7 * (cubic),
   bidegree (2,10), whereas the sibling has R = x^2 y^7 (y - lambda_1), bidegree
   (2,8): a degree-3 y-tail vs degree-1. Under the analogous single-root shift both
   yield the candidate last corner d_0(2,1) = (8,4).

5. **[MV, PASS] The exclusion is sourced exactly.** [GGV2 = arXiv 1605.09430,
   Prop "casos imposibles" tex 1009]: wp(n', n'-1) with n' >= 2 is NOT a possible
   last lower corner; the remark at tex 1053 names (2,1),(3,2),(6,3),(8,4)
   explicitly. (8,4) = 4(2,1), n' = 2, is excluded. This is the published
   "Proposition 3.29" analog (source numbering is symbolic; the printed 3.29
   corresponds to this statement, the (8,4) exclusion being stated in the following
   remark). Regression checks confirm the criterion on the explicit list and reject
   non-forms.

6. **[D] DERIVATION NEEDED (source-dependent), NO floor claim.** The one remaining
   gap: whether C13's degree-3 tail, after the shift, terminates at (8,4) as the
   LAST lower corner of H(P), or whether the two extra (shifted) roots create a
   longer admissible sub-chain whose final corner differs. The sibling's single root
   leaves nothing below the shift corner, so (8,4) is clean; a cubic tail may not.
   Certifying this requires transcribing GGHV22 section 3's exact (8,32) endgame and
   adapting it to a multi-root tail. **If** it resolves to (8,4) (or any excluded
   wp(n',n'-1)), C13's (8,40) chain discards and the [125,150] floor implication
   goes TO THE MAIN SESSION. Not claimed here.

## Net

The dossier's central worry (a d_0 fork that breaks the discard verbatim) is
**REFUTED**: q_1 = 4 and d_0 = 4 uniquely, exactly as the sibling, because the
bottom vertex of the max-x edge, A1 = (8,28), is SHARED and binds d_0 <= 4. The
discard's forcing extends; the residual is the strictly narrower endgame question
of the multi-root shift's terminal corner, marked DERIVATION NEEDED. No claim about
the floor moving is made without that sourced step.

Sources: E:\_Temp\ggv-sources\1401\src.tex (GGV1: Thm central 826, Case II 2563,
Thm 7.6 "divisibilidad" 4288); E:\_Temp\ggv-sources\1605\src.tex (GGV2: casos
imposibles 1009, explicit (8,4) remark 1053). Artifacts:
artifacts/output-2026-07-24.txt.
