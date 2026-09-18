# EXP-021 addendum: the integrated rerun with explicit ball certificates

Declared before the run (2026-08-19), extending the original hypothesis.

## What changes

The phase 1-3 certificates are spread across three scripts and the phase 3
input was a 3,000-box sample of 4,414 failures. This rerun is ONE pipeline
producing ONE complete certificate artifact. Two methodological additions:

1. **Four exclusion balls.** The centered pentagon has four symmetric
   copies in the core: P0 = (u*, v*, p*, q*) with u* = sqrt((5+sqrt5)/2),
   v* = (-3+sqrt5)/2, p* = sqrt((5-sqrt5)/2), q* = (-3-sqrt5)/2, and its
   images under the mirror (u,v,p,q) -> (u,-v,p,-q) and the pair swap
   (u,v,p,q) -> (p,q,u,v). Both maps permute the six reduced rows up to
   the established reflection identities and permute the mass columns, so
   rank is invariant and all four copies have rank exactly 2. Around each
   copy we remove a dyadic axis ball (center rounded to the 2^-20 grid,
   radius 2^-8 on each axis, bounds on the 2^-8 grid so bisection aligns).

2. **Ball certificates replace the IFT.** On each excluded ball we certify
   with dual-interval arithmetic that two 3x3 minors M1, M2 have gradients
   whose 2x4 interval matrix contains a 2x2 subdeterminant excluding zero
   over the WHOLE ball. Since every 3x3 minor vanishes on the rank <= 2
   locus, that locus is contained in {M1 = M2 = 0} which is then a smooth
   2-manifold on the ball. This gives dim(R_2 meet ball) <= 2 with an
   EXPLICIT radius, upgrading lemma piece 8 (which used a local IFT
   neighborhood of unspecified size). Candidate pairs are searched by
   descending gradient magnitude at the ball center; the successful pair
   and its certified subdeterminant enclosure are recorded per ball.

## Ladder amendment (declared 2026-08-19, before the run)

The mass-fiber dimension count needs the full ladder dim(R_j meet
shape+) <= j for j = 0, 1, 2, not only j = 2. Each ball therefore ALSO
carries a rank >= 2 certificate: one 2x2 minor of J interval-nonzero over
the whole ball, making R_1 meet ball EMPTY (and R_0 with it). Off the
balls the rank >= 3 certificates handle all three ladder levels at once.

## Success criteria (declared)

- Every box of the core partition is either certified rank >= 3 (plain
  interval or mean-value form, with the certifying minor recorded) or lies
  inside one of the four exclusion balls (recorded as ball-covered), with
  ZERO residual failures at depth cap 44.
- All four ball certificates succeed at radius 2^-8 (fallback radii 2^-10,
  2^-12 declared allowed, recorded if used).
- Budget: 12 h wall clock, checkpointed every 120 s, resumable. If the
  budget is exhausted the run FAILS and the failure is recorded; no
  extension under this declaration.

## Artifact

Full certificate list to the heavy store
(E:/_Datos/caos-research/central-configurations/EXP-021/), sha256 + counts
+ the four ball certificates in artifacts/integrated-summary.json in the
repo.
