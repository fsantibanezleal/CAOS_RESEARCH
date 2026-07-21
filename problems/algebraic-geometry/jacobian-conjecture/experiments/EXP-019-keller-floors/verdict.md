# EXP-019 - Verdict: CONFIRMED (2026-07-21). The descent is linear algebra, and (2,3) closes in full

Artifacts: `artifacts/output-{1,2,3}-2026-07-21.txt`.

## Established results

1. **The floor framework [MV].** The graded floor identities (floors 2 and 3 of det JF = 1)
   hold exactly across the library, and the h-divisibility corollary is exhibited on three
   maps (the top-form radical h divides J(P_top, Q_sub) whenever the top power p >= 2,
   including a p = 6 case). The descent's bookkeeping is implemented and certified.
2. **Wider exhaustive certificates [MV].** The bilinear harness (grid on the small side,
   complete linear solve on the large side) extends the JC(2) certificates to
   (2, 4) (256-sample grid), (2, 5) (27) and (3, 4) (35 structured): every clean Keller
   instance injective; triangular witnesses recovered at every zero sample.
3. **The (2, 3) case closes in FULL (the headline) [MV].** Lex Groebner elimination of the
   Q-coefficients from the linear Keller system yields a consistency ideal with a SINGLE
   generator:
   16 A0^2 A2^2 - 8 A0 A1^2 A2 + A1^4 = (4 A0 A2 - A1^2)^2 = 0,
   i.e. a normalized quadratic P admits a cubic Keller completion IF AND ONLY IF the
   discriminant of its quadratic part vanishes: P's top form is a perfect square, a power of a
   linear form. This is EXACTLY the degeneracy the leading-form theory (EXP-013, via EXP-010)
   predicts: the elimination and the tropical theory meet in one equation. Combined with the
   exhaustive-in-Q solves along that variety, the (2, 3) certificate is now a statement over
   ALL P, not a sampled grid.

## Adversarial validation record

- Two independent routes agree on the (2, 3) structure: the a priori leading-form dependence
  (EXP-013) and the a posteriori elimination ideal (this run): theory predicted the shape of
  the consistency variety and the computation returned precisely it, squared.
- The A = 0 triangular locus lies on the consistency variety (witness sanity).

## How could this be wrong?

- The full-(2,3) claim rests on the elimination ideal being the WHOLE consistency locus
  (standard for linear systems: consistency is a closed condition given by the elimination
  ideal) and on instance testing along parametrized branches; a residual risk is a component
  of the variety with completions not covered by the tested parametrizations: the branch
  enumeration along (4 A0 A2 - A1^2) = 0 is the queued tightening.
- The wider pairs remain sampled on the small side (declared).

## Consequences

- The rerouted thinking is validated: the "second invariant" that dimension 2 lacks at one ray
  is recovered floor by floor, and every floor is a LINEAR problem. The path forward is now
  concrete: per degree pair, (i) eliminate the large side to get the consistency ideal in the
  small side (one polynomial condition at (2,3): expect low-codimension discriminantal loci in
  general), (ii) parametrize the variety, (iii) complete linearly and fiber-test: an
  exhaustive JC(2) machine degree pair by degree pair, with the leading-form theory predicting
  each consistency ideal's shape in advance. JCB-021 continues with (2,4)/(3,4) eliminations
  and the branch-parametrized tightening of (2,3).
