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

## 6. The merge chart (2026-08-20, later)

Built and verified. The merge is TWO simultaneous collisions (B+ with C+
and B- with C-, by the mirror), so the chart puts the B/C midpoint at
(wu, wv) and the difference at rho (alpha, beta), making the merging
distance exactly rho. Measured row orders: L13, L14, L15, L16, L36 blow up
like rho^-2 and L35 vanishes like rho^2, exactly the tube pattern from the
(2,2) campaign, so the row scalings are rho^2 on the five and 1/rho^2 on
L35. Both singular factors are cleared ALGEBRAICALLY:

    area(X, a, b)  = rho * [ (Pa - Px) x (-D) ]        D = the unit difference
    1/r_ak^3 - 1/r_bk^3 = rho * (-2 D.(mid - Pk)) (B^2 + AB + A^2)
                              / [ (B + A) A^3 B^3 ]

with the second identity needed only for row L35, where BOTH factors carry
a rho. Crosscheck 5/5 against the unscaled matrix with the declared
scalings, and the MERGE FACE ITSELF certifies rank 3 at 40 of 40 sample
points: full rank, no lemma needed, consistent with finding 4.

The A/B merge needs NO separate chart. The three pairs are interchangeable
(permuting them permutes rows and columns of the matrix), so re-gauging to
make pair C the reference turns "A and B merge" into "the other two pairs
merge", which is exactly this chart. The gauge choice, not the geometry,
is what distinguishes them.

## 7. Status of this stratum

  reduction, generic rank, hexagon validation      DONE
  bounded covering                                 running, zero failures
  pair-collapse chart (and its S3 image)           DONE, face full rank
  pair-merge chart (covers both merge types)       DONE, face full rank
  outer region |v| > 3                             TO DO (inverted charts)
  double-collapse corner                           TO DO

No face lemma has been needed anywhere in this stratum.

## 8. There is no region at infinity (2026-08-20)

In the gauge v1 = 0, u1 = 1 the heights are unbounded, so a naive reading
says this stratum needs inverted charts at infinity. It does not. Rescale
a configuration whose heights are of size V >> 1 by 1/V: the heights
become order 1 and every width becomes u_i/V <= 1/V, so the outer region
maps onto the region where ALL THREE pairs are narrow, a near-collinear
configuration. That is a COLLAPSE-type region, not a new kind of infinity,
and the collapse recipe already covers it: with each mass column rescaled
by 4 u_i^2 and all three widths scaled by a common eps, sigma_3 of the
row-normalised matrix is 2.0 at eps = 1e-2, 1e-4 and 1e-6, flat across
four orders of magnitude and over thirty samples at each scale.

So the (0,3) stratum's complete face inventory is:

    pair collapse            FULL RANK (27/27 on the face)
    pair-pair merge          FULL RANK (40/40 on the face)
    all pairs narrow         FULL RANK (sigma_3 = 2.0, flat)
    (= the outer region, by rescaling)

Every one of them is full rank, so this stratum needs NO face lemma and NO
chart at infinity: a finite set of BOUNDED charts suffices. The contrast
with the (2,2) stratum, which needed three closed-form face lemmas and a
family of inverted charts, is entirely explained by the absence of
axis-body mass columns here.

## 9. Correction and refinement (2026-08-20, later still)

The merge covering's first run produced failures, and chasing them
sharpened two things.

CONFIRMED, not retracted: the merge FACE is full rank. Re-verified
directly on the exact face rho = 0, where the matrix reads

    L13 ( 0,      0,     -0.9  )      L15 ( 0,     +0.9,   0    )
    L14 ( 0,      0,     -0.3  )      L16 ( 0,     +0.3,   0    )
    L35 (-0.115, +1.44,  +1.44 )      L36 ( 0,     +0.6,  +0.6  )

so the pair-A column survives ONLY through row L35, the row the chart
divides by rho^2, and the minor {L13, L15, L35} certifies. That is why the
face test returns 40 of 40, and it holds at every tau sampled including
right next to where the L35 pair-A entry crosses zero (tau ~ 0.813 at
wu ~ 1, wv = 3): the determinant does not vanish where that single entry
does.

REFINED: the failures are not a face problem but the ordinary difficulty
of resolving the rank <= 2 LOCUS, which in this stratum is exactly where
central configurations live. Near it the certifying determinant is small
(order 1e-5) while a box of width 5e-4 lets it vary by more, so the
interval straddles zero. Extra bisection of one failing box discharged 58
of its 74 descendants (28 by mean-value forms, 30 by trap certificates)
within fourteen further halvings. The lever is therefore the depth cap,
not new mathematics: it was 44 for a 4-dimensional box, giving only about
eleven halvings per coordinate, and is now 60.

So the honest statement about this stratum's faces is: every face is
generically full rank and none needs a lemma, while the rank <= 2 locus
inside the region needs the same resolution effort any covering needs
where the object it is bounding actually lives.

## 10. The merge failures are a CHART-BOUNDARY artifact (2026-08-20)

At depth 60 the merge covering still left 1083 failures, and locating them
settled what they are. All of them sit in one tiny cluster,

    rho -> 0,  tau ~ 0.8134,  wu -> 1,  wv -> 3,

with 81.5% of the boxes touching the seed edge wv = 3 outright. Both
limits are CHART boundaries, not geometry:

  * wu = 1 is where the merged B/C cluster's width TIES pair A's, which is
    the boundary of the S3 gauge choice "pair A is widest". At a tie the
    gauge is ambiguous and the neighbouring chart (B widest) owns the
    other side, so the covering was being asked to certify right on a seam
    it does not own.
  * wv = 3 was an arbitrary declared bound on the heights.

The trap diagnostic confirms the character: the rank-2 witness EXISTS on
those boxes (so R_1 is empty there, and R_0 with it), all twenty gradient
packs evaluate, and the only thing missing is a separating gradient pair,
whose best interval sits exactly astride zero - the signature of a box
pinned on a boundary rather than a genuine singularity.

Fix applied: the seed is extended past both boundaries, wu to 5/4 and wv
to +-4, so the tie is an interior point the covering can bisect around.
Earlier evidence that this is the right lever: bisecting one such box by
hand discharged 58 of its 74 descendants once there was room to refine.

Worth recording as a LEAD, not a claim: the limiting geometry there is
pair A at (+-1, 0) with the merged B/C cluster at (+-1, 3), i.e. the four
points forming a RECTANGLE. The rank <= 2 locus passes nearby, and in this
stratum that locus is where central configurations live, so a genuine
central configuration of the three-pair stratum may sit near a
rectangle-like shape. Not investigated yet.
