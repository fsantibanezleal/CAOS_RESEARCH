# Exploration: which strata does this machinery reach?

2026-08-20, written while the atlas coverings run. The campaign's standing
exploration cadence: take a deliberate look past the current target and
persist the assessment.

## The observation

The stratum now being closed is the reflection-symmetric stratum of the
planar six-body problem with k = 2 bodies ON the symmetry axis and p = 2
mirror pairs off it. Its shape space, after fixing translation and scale,
has dimension 4 and its reduced mass vector has 4 entries, which is what
made the whole covering programme possible: a 4-dimensional box tree is
affordable, and a 6 x 4 matrix has a menu of exactly 80 three-by-three
minors to certify with.

Count the OTHER reflection-symmetric strata of six bodies. With k bodies
on the axis and p pairs, k + 2p = 6, so (k, p) is one of

    (6, 0)  all six collinear
    (4, 1)  four on the axis, one mirror pair
    (2, 2)  THE CURRENT STRATUM
    (0, 3)  three mirror pairs, nothing on the axis

and the shape dimension is the same in every case: k heights plus 2p pair
coordinates is k + 2p = 6 numbers, minus one translation and one scale,
leaving 4. The reduced mass count differs: k + p, giving 6, 5, 4 and 3
respectively.

So the machinery's two structural requirements - a 4-dimensional shape box
and a matrix whose kernel is the mass vector - hold for ALL FOUR strata.
The current programme is not special to (2, 2); it is the first instance
of a method that covers the whole reflection-symmetric family of n = 6.

## What each case needs

- **(6, 0), all collinear.** Already finite by Moulton's theorem (exactly
  n!/2 = 360 collinear central configurations for any positive masses).
  No work needed; it is the classical anchor and a calibration target.

- **(4, 1), four axis bodies and one pair.** Mass vector has 5 entries, so
  the matrix is (number of reduced equations) x 5 and the ladder becomes
  dim R_j <= j for j = 0, 1, 2, 3. One more rung than the current case,
  and the box tree is still 4-dimensional. The collision faces are simpler
  (only one pair can collapse or meet an axis body), so the face table
  should be SHORTER than the current one.

- **(0, 3), three mirror pairs.** Mass vector has only 3 entries, so the
  matrix is (equations) x 3 and the ladder is dim R_j <= j for j = 0, 1
  only: TWO rungs instead of three. This is the EASIEST of the three
  unsolved cases by that measure. Its faces are the three pair collapses
  and the three pair-pair merges, all of which the current campaign has
  already met and closed in closed form (pieces 11 and 12 are exactly
  these two face types).

## The strategic read

(0, 3) is the natural next target: fewer ladder rungs, and its two face
types are precisely the two this campaign already closed with explicit
lemmas. (4, 1) is next after it, and its extra rung is the cost of its
larger mass space. Together with Moulton's (6, 0) they would give
finiteness for EVERY reflection-symmetric configuration of six bodies for
generic masses, which is a coherent statable result rather than a
collection of cases.

That is a much stronger destination than the single stratum, and the
distance to it is mostly re-instantiation of machinery that now exists:
the interval covering, the trap certificate, the crosscheck gate, the four
verification gates, and the face-lemma recipe (order probe, column or row
rescale, closed-form leading coefficient, branch table).

## Honest caveats

- The reduced-equation derivation (which Laura-Andoyer equations survive
  the symmetry, and which are dependent) must be redone per stratum; the
  current one took a full round and produced the pair-equality lemma as a
  by-product. Nothing guarantees the other strata have as clean a
  reduction.
- Reflection symmetry is an assumption. Non-symmetric six-body
  configurations are not touched by any of this, and the full n = 6
  finiteness question stays open regardless of how the four strata land.
- The Albouy-Kaloshin singular-sequence route (V11 in the approaches
  evaluation) remains the only known path to ALL masses rather than
  generic ones, and it stays the recommended second campaign.
