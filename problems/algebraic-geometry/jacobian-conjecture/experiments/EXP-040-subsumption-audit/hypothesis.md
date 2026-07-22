# EXP-040 - Subsumption and recalibration: closing JCB-028 against Theorems 1-2 and the verified literature floor

- **Question.** JCB-028's remainder (4+ coefficient slices at (4, <= 6); the closed-form
  all-degree pure-slice certificate) and the honest placement of the whole (4, *) and
  composite-gcd ladder against the literature floor verified today
  (context/2026-07-22-literature-pass-dossier.md).
- **Motivation (derivation, declared).**
  (i) The pure slice x + a (xy)^2 is x + a x^u y^v with (u, v) = (2, 2): THEOREM 1 excludes
  it at ALL degrees; the queued closed-form certificate [C] is a corollary, not new work.
  (ii) Under the Theorem-2 grading (v, 1-u) = (2, -1), the seven lower coefficients split:
  xy (weight 1), y^2 (-2), xy^2 (0), y^3 (-3) are BELOW the x-class weight 2 (Theorem 2
  covers any combination at all degrees); x^2 (4), x^2 y (3), x^3 (6) are ABOVE (staircase
  territory, EXP-037).
  (iii) The literature floor verified from primary sources: counterexample gcd B satisfies
  B >= 16 (Heitmann 1990), B composite, B != p (Abhyankar 2008), B != 2p and B = 16 or
  B > 20 (GGV 2017); coverage gcd <= 8 is the FULL interval (Magnus / Nakai-Baba /
  Appelgate-Onishi / Nagata), not the set {1, 8} as one program note read. Hence gcd 9 and
  gcd 12 (EXP-026/027/028) are INSIDE the excluded region: those certificates are
  replications, and the genuinely open frontier is the GGV B = 16 normal form and the
  single surviving degree pair (72, 108) below 125 (GGHV 2204.14178, gcd 36).
- **Falsifiable predictions.**
  1. [MV] (Classification) The machine confirms the weight split of the seven coefficients
     and the Theorem-1 shape of the pure slice.
  2. [MV] (Below-weight consistency with Theorem 2) A slice with ALL below-weight
     additions, e.g. x + a (xy)^2 + b xy + c y^2 + d y^3 + e xy^2, has an EMPTY window at
     N = 10 (deeper than EXP-025 went): consistent with the all-degree theorem.
  3. [MV] (4+ coefficient sweep) Every 4-subset of the seven coefficients, sampled over
     rational value tuples on the (4, <= 6) window, is EMPTY: the JCB-028 remainder holds
     at the sampled level, and each subset is tagged with its closure owner (Theorem 2 at
     all degrees if purely below-weight; staircase/EXP-037 territory otherwise).
  4. [D] (Recalibration) The audit table places EXP-024..028 correctly against the
     verified floor: gcd 2, 9, 12 are literature-covered (replication value only); the
     open ladder is B = 16 (with GGV's explicit directions and normal form as attack
     surface) and B > 20 composite non-2p, with (72, 108) the lone survivor below 125.
- **Method.** sympy over QQ; weight arithmetic; window solves at N = 6 and N = 10;
  itertools sweep over 4-subsets with 3 value tuples each (105 solves). Caps 570 s.
- **Success criterion.** 1-3 verified, 4 recorded; JCB-028 CLOSES (pure slice and
  below-weight: theorem corollaries; above-weight: owned by JCB-038; sampled remainder
  clean); the frontier retarget recorded as new backlog (B = 16 attack; (72, 108)).
- **Failure criterion.** A consistent 4-subset sample (escalate); a below-weight slice
  inconsistent with Theorem 2 (would contradict an unconditional theorem: instrument bug
  until proven otherwise).

Declared 2026-07-22 before the run.
