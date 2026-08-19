# EXP-021 - The verified covering: rational interval certificates for rank >= 3 on the core

Declared: 2026-08-03, BEFORE any run. The definitive k = 3 route per the
round-28 reconnaissance (the physical rank-<=2 locus flees to the excluded
boundaries) and the field-standard interval tradition (Moczurad-
Zgliczynski).

## Method

RATIONAL INTERVAL ARITHMETIC, fully rigorous: Fraction endpoints; outward
rounding to denominator 2^40 after every operation (floor/ceil to
multiples of 2^-40); square roots by integer-sqrt bracketing
(isqrt(floor(x 2^80))/2^40 below, (isqrt(ceil(x 2^80)) + 1)/2^40 above);
reciprocals on sign-definite intervals only. No floating point anywhere in
the certificate path.

On the gauge a1 = 1, a2 = -1, the CORE is u, p in [1/4, 3], v, q in
[-3, 3], |q - v| >= 1/4. Adaptive bisection: per box, evaluate the CHOSEN
3 x 3 minor {L13, L15, L23} x {m1, m2, mA} (equal to a23 * C1, nonzero at
the hexagon); a box is CERTIFIED when its minor interval excludes zero,
DISCARDED when it lies wholly inside the excluded band |q - v| < 1/4, and
BISECTED (widest dimension) otherwise, to a declared depth cap. Every
certificate (box, minor id, interval) is persisted. A failed deep box is
recorded for minor-switching in the follow-up (sound: ANY nonzero minor
certifies rank >= 3 on the box).

## Predictions

- P1 (feasibility): the depth-14 adaptive covering of the core terminates
  with under 5,000,000 boxes processed.
- P2 (the mathematical outcome): every non-discarded box is certified
  (zero failed deep boxes), i.e. rank >= 3 HOLDS on the entire core with
  a machine-checkable certificate list. Failed boxes, if any, localize
  genuine near-degeneracies for exact study and are a finding, not a
  defeat.

## What remains after P2 (the honest enumeration)

The core is NOT an exhaustion of the open stratum. The remaining collars
and outer regions, each needing its own closed-form leading-matrix lemma
(the pieces-1-5 techniques):

  (i) q -> v (the excluded sub-stratum's collar), (ii) u -> 0 and
  p -> 0 (pair collapse), (iii) u, p large, (iv) |v| or |q| large
  (bodies escaping), (v) collision collars (d-distances -> 0) and
  e12 -> 0 are OUTSIDE the open stratum by non-collision, needing only
  the collar statement near them. The gauge fixes r12 = 2, so e12 is
  bounded away from 0 automatically; collisions among the six bodies
  remain excluded by hypothesis.

## Preflight

- Source-complete: entries from the dossier's machine-verified closed
  forms; the interval module is self-contained and its soundness is by
  construction (outward rounding everywhere).
- Smoke: the module must reproduce the hexagon minor's sign on a tiny box
  around the hexagon geometry, and the interval evaluation at a
  degenerate-point-free box must be finite and sign-correct against a
  60-digit numeric reference (reference only, never certificate).
- One-sidedness: P2 can fail via failed boxes (localized findings); P1
  can fail by explosion (measured, route adjusted).
- Budget: one run, depth cap 14, wall cap by the harness; artifacts
  persisted incrementally.
