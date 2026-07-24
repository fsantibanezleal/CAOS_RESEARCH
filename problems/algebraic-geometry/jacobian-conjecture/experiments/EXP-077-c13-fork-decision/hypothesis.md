# EXP-077 - The C13 fork: does the (8,32) sibling discard extend to (8,40)?

- **Question.** GGHV22 section 3 discards C13's sibling, the (8,32) chain, by a
  single-shape forcing: q_1 = 4 divides d_0 and d_0 <= 4, so d_0 = 4 uniquely,
  which pins l_{1,0}(P) = (lambda_P x^2 y^7 (y - lambda_1))^{4m}; the shift
  phi(y) = y + lambda_1 exposes the last lower corner (8,4), excluded by
  [GGV2, "casos imposibles"] (the published Proposition 3.29 analog). C13's own
  chain is (8,40) with the SAME tail (A1 = (8,28), A2 = (11/4,7), (m,n) = (3,2)).
  The dossier (2026-07-24) feared a FORK: since (8,40) = 8(1,5) is coprime it read
  d_0 <= 8, so if q_1 stays 4 then 4 | d_0 would allow d_0 in {4, 8} and the
  single-shape discard would fail verbatim. Decide the fork from primary sources.

- **Primary sources secured (E:\_Temp\ggv-sources).**
  - [GGV1 = arXiv 1401.1784] Theorem 7.6 ("divisibilidad", tex 4288-4341) and
    Proposition "Case II" (tex 2563-2650) and Theorem "central" (tex 826): the
    q_j definition via the en-point of F_j.
  - [GGV2 = arXiv 1605.09430] Proposition "casos imposibles" (tex 1009) with the
    explicit remark (tex 1053) naming (2,1),(3,2),(6,3),(8,4) as NOT possible last
    lower corners.

- **Predictions.**
  1. **[MV] q_1 = 4 for C13, identical to the sibling.** By [GGV1, Case II],
     en_{rho,sigma}(F_1) = mu (abar, bbar) where (abar, bbar) is the primitive of
     the regular corner A1 = (8,28) = 4(2,7), d = gcd(8,28) = 4, and mu solves
     v_{rho,sigma}(en F_1) = rho + sigma. The (4,-1) leading form of P depends ONLY
     on the shared edge A1--A2 (both at v_{4,-1} = 4; A0 sits strictly below at
     v_{4,-1} = -8 for C13 / 0 for the sibling, so A0 is NOT in the leading form).
     Hence en_{4,-1}(F_1) = (6,21), q_1 = d / gcd(mu, d) = 4 for BOTH chains. The
     v_{4,-1}(A0) difference does not reach the en-point.
  2. **[MV] d_0 <= 4 for C13, NOT <= 8: the fork collapses.** l_{1,0}(P) = R^{m d_0}
     forces d_0 * st_{1,0}(R) = st_{1,0}(P). The bottom vertex of the max-x (x = 8)
     edge is st_{1,0}(P) = A1 = (8,28), SHARED with the sibling (below A1 the polygon
     turns to A2 at x = 11/4 < 8). So d_0 | gcd(8,28) = 4. d_0 = 8 is arithmetically
     IMPOSSIBLE (28/8 not an integer: R would need y^{3.5}). The (8,40) = 8(1,5)
     reading bounds d_0 by the TOP vertex only and is not the binding constraint.
  3. **[MV] d_0 = 4 uniquely; NO fork.** q_1 = 4 | d_0 and d_0 <= 4 give d_0 = 4,
     exactly as the sibling. R = x^2 y^7 * (cubic), bidegree (2,10), vs the sibling's
     x^2 y^7 (y - lambda_1), bidegree (2,8): the tail degree is 3 vs 1.
  4. **[MV] The GGV2 exclusion is sourced exactly.** wp(n', n'-1) with n' >= 2 is
     not a possible last lower corner; (8,4) = 4(2,1), n' = 2, is on the explicit
     excluded list. The single-root shift of C13's R gives min y-power 1 -> the same
     candidate corner (8,4) = d_0 (2,1), excluded.
  5. **[D] DERIVATION NEEDED (source-dependent), no floor claim.** Whether the
     multi-root (degree-3) tail's shift terminates at (8,4) as C13's LAST lower
     corner (vs a longer admissible sub-chain landing elsewhere) needs GGHV22
     section-3's exact treatment of the (8,32) endgame adapted to a cubic tail.
     Any floor-moving statement routes to the main session; NOT claimed here.

- **Method.** Exact integer / Fraction arithmetic (no mod-p reduction in this
  experiment; the modfrac hard rule does not apply). Regression gate: recompute
  the SIBLING (8,32) chain through the identical code path and require it to
  reproduce GGHV22's published decision (q_1 = 4, d_0 = 4, corner (8,4), excluded).

Declared 2026-07-24 (session 47) before run.py.
