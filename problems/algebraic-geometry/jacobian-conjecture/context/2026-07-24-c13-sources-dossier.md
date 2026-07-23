# C13 sources dossier (2026-07-24, session 47 fetch 1: GGHV22 section 3 via ar5iv)

## The (8,32) discard, verbatim mechanism [VERIFIED against ar5iv 2204.14178]

- Divisibility: by [GGV1, Theorem 7.6(5)], q1 = 4 | d0, where
  d0 = max{d : l_{1,0}(P) = R^{md}} (the max perfect-power order of the initial
  form).
- Bound: d0 <= 4 because d0 * st_{1,0}(R) = (1/m) st_{1,0}(P) = (8,28) = 4(2,7)
  with gcd(2,7) = 1.
- Combined: q1 = 4 divides d0 and d0 <= 4 give d0 = 4 EXACTLY, forcing
  l_{1,0}(P) = R^{4m} = (lambda_P x^2 y^7 (y - lambda_1))^{4m}.
- Endgame: after phi(y) = y + lambda_1, l_{1,0}(phi(P)) =
  (lambda_P x^2 y (y + lambda_1)^7)^{4m}, so A0' = (8,4) would be the last
  possible corner of phi(P): impossible by [GGV2, Proposition 3.29].

## THE FORK AT C13 (DERIVED, machine-checkable next)

For (8,40): st_{1,0}(P)/m = (8,40) = 8(1,5), gcd(1,5) = 1, so d0 <= 8. IF the
chain-tail data (shared A1 = (8,28), A2 = (11/4,7)) again gives q1 = 4, then
4 | d0 allows d0 in {4, 8}: the forcing is NOT unique:
- d0 = 8: R = x y^4 (y - lambda), post-shift corner (8, 40 - 32)? bidegree
  bookkeeping: R bidegree (1,5), R^{8m} = (8m, 40m); after the shift the y-drop
  is 8m * 4 = 32m per the (y+l)^4 pattern: corner (8, 8): TO RECOMPUTE CAREFULLY.
- d0 = 4: R = x^2 y^a (y - lambda)^b with (2, a + b) = (2, 10): a + b = 10, b
  distribution NOT forced to 1: MULTIPLE shapes (b in 1..9 with constraints).
The single-shape discard therefore does NOT extend verbatim: EXP-077 must
either (a) verify q1 for the (8,40) chain from [GGV1, Thm 7.6(5)] (fetch
needed: GGV1 identity + statement), (b) enumerate the d0 = 4 and d0 = 8 shape
families and test EACH against Prop 3.29 (statement fetch needed: GGV2), or
(c) conclude the discard fails and start Phase B.

## Fetch queue (session 47+)
1. The [GGHV22] bibliography (arXiv ids of GGV1 and GGV2).
2. [GGV2, Prop 3.29]: the last-possible-corner exclusion statement.
3. [GGV1, Thm 7.6(5)]: the q | d0 statement and what q1 is for a given chain.

## Fetch 2 (arXiv author search): the GGV series candidates [VERIFIED ids]

- 1401.1784 On the shape of possible counterexamples to the Jacobian Conjecture
  (2014, 71 pp): the prime GGV1 candidate (deep numbering; Theorem 7.6 plausible).
- 1406.0886 A system of polynomial equations related to the JC (2014).
- 1605.09430 The two-dimensional JC and the lower side of the Newton polygon
  (2016): GGV2 candidate (corner-focused; our earlier dossier cites GGV2
  Remarks 3.2 + 3.29).
- 1708.07936 Some algorithms related to the JC (2017): the Algorithms 1-9 source.
- 1708.09367 Approximate roots and intersection numbers (2018).

Session 47+ verification order: ar5iv-fetch 1401.1784 for Theorem 7.6(5) (the
q | d0 statement + the DEFINITION of q for a chain: decides whether q1 = 4
carries to (8,40) or becomes 8); ar5iv-fetch 1605.09430 for Prop/Remark 3.29
(the last-possible-corner exclusion: decides whether (8,4)-style corners are
excluded in the form needed at (8,12)/(8,8)). Then EXP-077 decides the fork.
