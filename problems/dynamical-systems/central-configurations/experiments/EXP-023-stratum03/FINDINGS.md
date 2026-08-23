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

## 11. The merge corner is the ESCAPE limit, i.e. the outer chart's seam

Widening the seed moved the failures to the NEW corner (921 of 921 on the
new edges), which settles that they track the box corner rather than any
feature. Probing that corner explains why, and it is not a defect:

  * sigma_3 there is 1.1e-5 and INDEPENDENT of rho, so it is a property of
    the underlying configuration, not of the merge.
  * A high-precision descent from that corner, with the two pairs kept
    genuinely separate (|B - C| = 0.043), plateaus at sigma_3 = 1.1e-3 and
    does NOT reach zero, so it is a near-degeneracy rather than a rank-2
    point.
  * Its near-kernel is (mA, mB, mC) = (-1, 0.0016, -0.0016): the pair-A
    column is what is nearly vanishing, and the kernel is NOT sign-definite,
    so even at the limit it would not give positive masses. No central
    configuration here.

The cause is geometric: as the merged B/C cluster climbs away from pair A,
every pair-A coefficient decays like the inverse cube of the separation,
so the matrix drifts toward rank 2 at large heights. That is the ESCAPE
limit, which belongs to the OUTER region, and the outer region is exactly
what rescales onto the all-narrow chart (finding 8). So the merge chart is
correctly refusing to certify on a seam it does not own; the all-narrow
chart must cover it. This is the same seam logic the (2,2) atlas uses, and
it is why that campaign needed a seam gate.

Consequence for the plan: build the all-narrow chart as a real covering,
then re-check that every mergeBC residue box lies inside it.

## 12. The all-narrow / outer chart is built and running

One chart serves both roles, since the outer region rescales onto the
all-narrow one (finding 8). Variables (eps, c1, c2, h): widths
u_i = eps * (1, c1, c2) with c1, c2 in [0, 1] by the S3 symmetry, heights
(0, 1, h) with h in [-2, 2], eps in [0, 1/4]. Each mass column is
multiplied by 4 u_i^2, clearing that pair's own 1/w_i^3 by the same exact
identity collapseB uses.

Its FACE at eps = 0 certifies rank 3 at 34 of 34 sample points, matching
the sigma_3 = 2.0 measurement from the probe.

Worth recording because the gate earned its keep again: the crosscheck
FAILED on first run, and the chart was right while the check was wrong. I
had compared against cover.py expecting a single uniform scale factor, but
the relation carries a per-COLUMN factor: under the length rescale taking
this gauge to cover.py's, an entry scales by lambda^-1 while this chart
additionally carries 4 u_j^2, so

    narrow[i][j] / cover[i][j] = 4 * eps * a_j^2 ,   a = (1, c1, c2).

The very first printed ratio, 0.875 at eps = 0.219, is exactly 4 eps,
which is what identified the error. With the per-column factor the check
passes 5/5.

## 13. Current state of this stratum

    cover.py      bounded interior      running, ZERO failures
    collapseB.py  pair collapse         running, ZERO failures
    mergeBC.py    pair-pair merge       running; residue is the ESCAPE seam
    narrow.py     all-narrow = outer    running (face 34/34)

The open item is the seam check: every mergeBC residue box must lie inside
narrow's certified region. That is the same seam argument the (2,2) atlas
uses, and it is what its seam gate was built to verify.

## 14. The seam is quantified and closed by construction

The open item from finding 13 was whether every mergeBC residue box lies
inside narrow's region. The map between the two charts is a pure rescaling
(divide all lengths by the B height):

    eps = 1 / v2,   c1 = u_B / u_A,   c2 = u_C / u_A,   h = v_C / v_B .

Applying it to all 1892 residue boxes, corner by corner, gives an exact
requirement:

    eps in [0.249998, 0.250122]
    c1  in [1.248901, 1.250007]
    c2  in [1.248894, 1.250000]
    h   in [0.999985, 1.000000]

against narrow's declared seed eps [0, 1/4], c [0, 1], h [-2, 2]. So the
residue sits a hair outside on three coordinates - eps by one part in two
thousand, and c1, c2 by 25%. narrow's seed is therefore widened to
eps [0, 1/2], c [0, 2], h [-2, 2], which contains the requirement with
room to spare, and relaunched.

Two honest notes. First, c > 1 means the first pair is no longer the
widest, so the S3 reduction is given up inside this chart; that costs
compute, not correctness. Second, the seam now closes BY CONSTRUCTION
(narrow's box provably contains the residue), but it will not be
ESTABLISHED until narrow finishes covering that region with certificates.

## 15. The charts PING-PONG, and the cause is the gauge (2026-08-20)

Widening narrow to close the seam produced 19084 failures of its own, and
all of them sit at ITS max corner (eps, c1, c2, h) -> (0.5, 2, 2, 1),
which is the B/C merge: mergeBC's territory. Mapping those boxes into
mergeBC's gauge puts them at wu ~ 2.0, while mergeBC covers wu in
[0.125, 1.25]. So the residue is NOT covered there either:

    mergeBC residue  ->  needs narrow beyond its declared box
    narrow residue   ->  needs mergeBC beyond its declared box

Each chart fails at its own boundary and hands the failure to a region the
other one does not cover. Widening either box just moves its corner and
regenerates the problem, which is exactly what the last two rounds
observed happening twice.

THE CAUSE IS THE GAUGE, not the charts. Both work in a gauge (v1 = 0,
u1 = 1) that leaves the shape space NON-COMPACT: widths and heights can
take any ratio, so every box bound is arbitrary, and an arbitrary bound
always produces a corner the covering cannot certify. No amount of
widening fixes a truncation of an unbounded region.

THE FIX is a gauge that makes the shape space compact, so that chart
boundaries are GEOMETRIC (where the maximum switches from one coordinate
to another) rather than arbitrary:

    translation:  v1 = 0
    scale:        max(u1, u2, u3, |v2|, |v3|) = 1

Then every coordinate lies in [-1, 1] and the space is covered by FIVE
charts, one per coordinate that attains the maximum, each a COMPACT
4-box:

    U1: u1 = 1,  free (u2, u3, v2, v3) in [0,1]^2 x [-1,1]^2
    U2: u2 = 1,  free (u1, u3, v2, v3)
    U3: u3 = 1,  free (u1, u2, v2, v3)
    V2: v2 = 1,  free (u1, u2, u3, v3) in [0,1]^3 x [-1,1]   (mirror gives v2 = -1)
    V3: v3 = 1,  free (u1, u2, u3, v2)

At a boundary between two of them the maximum is attained twice, and the
neighbouring chart owns the other side with the tie interior to it: that
is a genuine seam, and it is checkable, unlike an arbitrary cut.

This also explains, in hindsight, why the (2,2) campaign needed a family
of inverted charts at infinity: the same non-compactness, handled there by
inverting coordinates instead of bounding them. The compact gauge is the
cleaner instrument and should have been the starting point here.

FIRST STEP TAKEN: cover.py is chart U1 already except that its heights run
to +-3 instead of +-1; under the compact gauge its job SHRINKS to
[-1, 1] and everything beyond belongs to V2 and V3.

## 16. The compact atlas is built and its seam gate passes (2026-08-20)

Five charts, one per coordinate that can attain the maximum under the
compact gauge, all crosschecked 5/5 against cover.py by the exact
rescaling (an entry scales by lambda^-1 and column j additionally by
4 u_j^2):

    U1  u1 = 1   cover.py        running, zero failures
    U2  u2 = 1   chartU2.py U2   running
    U3  u3 = 1   chartU2.py U3   running
    V2  v2 = 1   chartV2.py      running
    V3  v3 = 1   chartU2.py V3   running

A shared collision_discard now serves every chart, testing CONTAINMENT
rather than overlap (an overlap test discarded a whole seed earlier in
this campaign). chartV2's first run produced 20983 failures for the simple
reason that it had been given no discard at all: every one of them sat at
its corner (1,1,1,1), which is the B = C collision, i.e. face-chart
territory. With the shared discard that disappears.

SEAM GATE (seam-gate.py): sample configurations, normalise into the
compact gauge, skip those inside a collision neighbourhood (the face
charts own those), and check the rest are claimed by some chart. Result:
48358 tested, ZERO gaps. And the part that makes it evidence rather than
decoration - all five negative controls fire, dropping any single chart
opens between 6570 and 14179 unclaimed configurations.

So the (0,3) stratum now has a COMPACT atlas whose covering property is
verified, replacing the pair of charts that were ping-ponging their
residues across arbitrary boundaries.

## 17. The compact atlas is running clean, faces included (2026-08-20)

All five interior charts and all three collapse face charts are covering
with ZERO failures:

    U1 (cover.py)   157056 boxes    0 failures
    U2               19184          0
    U3               25972          0
    V2               17574          0
    V3               17621          0
    collapse0          728          0
    collapse1         9469          0
    collapse2        10767          0

The collapse charts are the compact-gauge rebuild of the face treatment.
Each crosschecks 5/5 against the interior chart by the exact rescaling,
and each FACE certifies rank 3 on its own: 30 of 30, 24 of 24, 24 of 24.
Their discard keeps only the collar of the pair that is collapsing and
hands every other collision to the chart that owns it.

That is a complete turnaround from the previous gauge, where two charts
between them produced forty thousand failures and handed each other
residues neither covered. The difference is entirely the gauge: bounded
ranges with geometric boundaries instead of arbitrary truncations of an
unbounded region.

REMAINING for this stratum: the merge face charts in the compact gauge
(three of them, one per pair of pairs), then the residue and artifact
gates over the whole atlas.
