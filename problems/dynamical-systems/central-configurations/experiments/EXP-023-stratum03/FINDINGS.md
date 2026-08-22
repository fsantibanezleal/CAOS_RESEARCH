# EXP-023 findings so far: the (0,3) stratum is structurally simpler

2026-08-20.

## 1. The reduction (verified to 40 digits)

Mirror symmetry kills L12, L34, L56 identically and pairs off the rest,
leaving SIX independent equations {L13, L14, L15, L16, L35, L36} over
THREE masses: a 6 x 3 matrix.

## 2. Generic rank is 3 = FULL rank

Twenty of twenty random shapes. For a 6 x 3 matrix full rank means the
kernel is trivial, so a generic shape admits NO masses: central
configurations of this stratum are confined to the rank <= 2 locus, a
codimension-2 subvariety of the 4-dimensional shape space. The covering
therefore proves ABSENCE over most of the space, which is a stronger and
cheaper thing to certify than the (2,2) stratum's situation.

## 3. Instrument validated on a known member

The regular hexagon: rank exactly 2, kernel exactly the equal-mass ray,
reproducing the classical regular-hexagon central configuration.

## 4. NO rank-dropping faces (measured, not assumed)

The (2,2) stratum needed three closed-form lemmas (pieces 10, 11, 12) for
faces where the rescaled matrix drops to rank 2. The (0,3) stratum has
none:

  pair collapse (u2 -> 0), mB column x 4 u2^2:
      sigma_3 stays in [3.1e-2, 8.3e-1] as u2 -> 0, and the FACE ITSELF
      certifies rank 3 at 27 of 27 sample points. Adding the piece-11
      column division makes it WORSE (sigma_3 -> 0), so the simple
      rescale is not merely sufficient but correct.
  pairs B and C merging, no rescale at all:
      sigma_3 in [2.8e-3, 2.0e-1] as the merge closes.
  pair B merging with pair A, no rescale at all:
      sigma_3 in [3.5e-1, 8.4e-1].

The reason is structural: (0,3) has no axis bodies, so it has no
axis-body mass columns to vanish, and that vanishing was exactly what
produced the (2,2) stratum's rank-2 faces. Full rank is stable, and here
it is the generic condition, so it persists onto the faces.

## 5. What remains for this stratum

  - the bounded covering (running, zero failures so far)
  - the pair-C collapse chart: the S3 image of the pair-B one, free
  - blow-up charts at the two merge faces: the entries BLOW UP there
    (unlike the collapse faces, where they cancel), so those regions need
    the tube-style polar blow-up even though the rank is fine
  - the outer region |v| > 3 by inverted charts
  - then the same three requirements as the (2,2) chain: R_0 empty,
    dim R_1 <= 1, dim R_2 <= 2
