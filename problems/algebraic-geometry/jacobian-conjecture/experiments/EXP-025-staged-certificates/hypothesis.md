# EXP-025 - Staged certificates: two-parameter slices, the (4, <= 10) window, and the sources

- **Question.** Push JCB-028 past the capped 8-parameter run along three fronts: (A) sound
  all-value certificates on every two-parameter slice (a, single lower coefficient) at (4,6);
  (B) the pure-slice window widened to degree <= 10, which directly tests the (4,10) rung of
  the primitive ladder (where the descent has no subtraction move); (C) the JCB-029
  primary-source pass for the gcd literature context (Magnus; Appelgate-Onishi; Nagata).
- **Motivation.** EXP-024 established the instrument (cleared left-null vectors: polynomial
  identities, sound at every parameter point) and its reach (1-param instant, 8-param capped).
  Two-parameter fields should be tractable; each slice theorem covers a full plane of
  parameter values that EXP-023 only sampled. The degree <= 10 window matters because the
  descent argument only reduces degrees 7 and 8 into the empty window; degree 10 (top
  b (xy)^5) is the first rung with NO reduction move, so its emptiness on the pure slice is
  new territory, not a corollary.
- **Falsifiable predictions.**
  1. [MV] (Slice certificates) For each of the seven slices P = x + s m + a (xy)^2 (m one
     lower monomial, s and a symbolic): certificate pairings exist and their gcd is a pure
     a-power times a unit, so the (4, <= 6) window is empty for ALL (a != 0, s arbitrary).
     Any slice whose gcd retains s-dependence defines an unresolved curve to probe (honest
     outcome, reported as such).
  2. [MV] (The (4, <= 10) window) For P = x + a (xy)^2, a symbolic, Q of degree <= 10 (54
     unknowns): certificate pairings exist with gcd a pure a-power: NO Keller partner of
     degree <= 10 for ANY a != 0. This kills the (4,10) rung on the pure slice.
  3. [C -> verified] (Sources) The primary sources confirm: Magnus 1955 (gcd of the degrees
     equal 1 implies invertibility), Appelgate-Onishi 1985 and Nagata (gcd prime, and the
     2-descent structure theory); wiki 04's hedge is then replaced by verified citations.
     Anything not confirmed stays flagged UNVERIFIED.
- **Method.** sympy over QQ(a, s) and QQ(a): the EXP-024 certificate pipeline (M, rhs from
  bilinearity; nullspace of M^T; clear denominators; assert c^T M = 0 identically; factor the
  pairings and their gcd). Runtime capped per part at 570 s with honest cap-out records.
  Sources via web search of the primary literature.
- **Success criterion.** 1-2 verified (or capped honestly with the completed slices recorded);
  3 resolved to verified citations or explicit UNVERIFIED flags.
- **Failure criterion.** A slice or window with vanishing gcd on a locus off {a = 0}: that
  locus is a candidate stratum, probed immediately with the EXP-015 checker.

Declared 2026-07-21 before the run.
