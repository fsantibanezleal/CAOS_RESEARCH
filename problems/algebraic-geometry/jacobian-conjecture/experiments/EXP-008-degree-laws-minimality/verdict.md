# EXP-008 - Verdict: CONFIRMED (2026-07-20)

Output: `artifacts/output-2026-07-20.txt`. All five predictions verified exactly.

## Established results (ours, exact)

1. **Fiber-degree floor 3.** Degree-1 seeds are impossible (the integral condition forces
   p = 0); the constructor rejects them. Fiber degree in the family is always >= 3.
2. **Degree law.** For affine sections q, the component total degrees are exactly
   (5d - 3, 5d - 4, 4) for seed degree d, verified at d = 2, 3, 4, 5. The scale k never
   changes degrees; q-tails v^2, v^3 strictly increase them rowwise ((8,7,5), (10,9,7)).
3. **A NEW fiber-degree-6 counterexample (P5d5).** Seed p = w - 3w^5, k = 5: polynomial Keller
   map with det = -20, degrees (22, 21, 4), generic fiber degree 6, exact reconstruction
   verified, and the explicit rational collision (-1/70, 75, 399000) and
   (1/160, -150, -3824000) both mapping exactly to (-750, -750, 1).
4. **Family-internal minimality.** The minimum degree vector over the family is (7, 6, 4),
   attained exactly at d = 2 with affine q: the announced map F. Within the constructor-v2
   class, the July 2026 counterexample is THE smallest.

## Adversarial validation record

- The law was tested at every available d (including the new d = 5 build, which is also its
  own full verification pipeline: polynomiality, constant det, squarefree fiber,
  reconstruction, collision); monotonicity claims verified in both axes (d, tail) and
  invariance in k.

## How could this be wrong?

- The degree law is verified at d = 2..5 and derivable from the monomial structure (leading
  term of a1 is u^{d} c1^{d} / k^{d-2}-type with weights 2 and 3); a symbolic
  arbitrary-d proof is written analytically in the wiki, with these runs as certification.
  Beyond d = 5 the statement rests on that derivation.
- SCOPE: minimality is WITHIN the family. Globally, Wang's theorem excludes degree 2 only:
  whether a C^3 counterexample of total degree 3..6 exists is OPEN and untouched here.

## Consequences

- The family inventory now spans fiber degrees 3, 4, 5, 6 with fully certified instances
  (F, P3, P4, P5d5) plus the off-family-shape q-tail instance P5.
- The global-minimality gap (degrees 3..6 in C^3) is a sharply defined open target for a
  future search experiment (JC-P3 continuation; the 2-variable-style ansatz enumeration with
  symbolic pruning, GPU-widened).
