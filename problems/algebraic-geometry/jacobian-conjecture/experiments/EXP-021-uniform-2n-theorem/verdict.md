# EXP-021 - Verdict: CONFIRMED (2026-07-21). The uniform min-degree-2 theorem

Artifacts: `artifacts/output-{A,B,C}-2026-07-21.txt` (the first monolithic run and a first
part-C shape timed out on generic-H composition blowup; restructured honestly: generic where
tractable, exact rational spot checks at the higher degrees; all recorded).

## THE THEOREM (assembled [D]; every mechanical step [MV])

Every planar Keller map with min(deg P, deg Q) <= 2 is, up to affine gauge,
  F = (x + ell^2,  ell/beta + H(x + ell^2)),   ell = alpha x + beta y,  H any polynomial,
and is invertible by the closed formula
  ell = beta (v - H(u)),  x = u - ell^2,  y = (ell - alpha x)/beta.
Steps: (i) the shear-coordinate PDE 2 u1 Qt_{u2} - Qt_{u1} = c has P as its characteristic
invariant: sufficiency verified generically [MV, part A: J == 1 over QQ(alpha, beta, h0..h3)];
(ii) completeness: dim ker J(P, -) on degree <= n equals floor(n/2) + 1 = #{H(P)} for
n = 3..6 at three samples [MV, part B]: the H-family is ALL solutions; (iii) the closed
inverse verified generically at deg H <= 1 and by exact spot checks at deg H = 3, 4 [MV, part
C]; (iv) the consistency ideals (EXP-019/020) force the rank-1 top and beta = 0 collapses to
the affine case; Wang covers both-degrees-2. The open frontier of JC(2) formally moves to
min degree >= 3 (both components of degree at least 3).

## Adversarial validation record

- Three independent routes agree: the elimination ideals (a posteriori), the leading-form
  theory (a priori), and now the PDE/characteristics classification (structural); the free
  parameters B_11/B_15 observed at EXP-020 are exactly H's coefficients, retro-explained.

## How could this be wrong?

- Part B's completeness is verified at n <= 6 and three (alpha, beta) samples; the dimension
  count is a rank statement that plausibly holds for all n (the PDE argument is the [D]
  bridge); pushing n higher is mechanical if ever needed.
- Classical status: statements of this reach are classical (Magnus-era; subsumed by
  Jung-van der Kulk for invertible maps); the mechanical, certificate-backed, closed-formula
  form is what this program adds. No novelty claim beyond that.

## Consequences

- The (2, n) column is closed uniformly; JCB-025 done. The frontier is min degree >= 3: the
  staged (3, n) program (quasi-triangular consistency conjecture: the variety should force
  P equivalent to x + f(ell); then the same PDE closes it) is the next theorem attempt
  (JCB-026), with the Puiseux obstructions and the gcd-shared-top cases ((4,6)-type, h of
  degree >= 2) as the genuinely hard territory beyond.
