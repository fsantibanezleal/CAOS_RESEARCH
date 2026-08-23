# The stratum theorem: assembly record

2026-08-20. This document assembles the campaign's proof chain for the
two-pair reflection-symmetric stratum of the planar six-body problem and
states exactly what is proven, by what instrument, and what remains. It is
the single place where the pieces are put together; the mathematics lives
in `2026-08-02-rank-floor-lemma-dossier.md` (lemma pieces 1-10) and in the
per-experiment verdicts.

## 1. The object

Six bodies in the plane, reflection-symmetric about a vertical axis, with
two bodies ON the axis at heights a1, a2 and two mirror pairs off it:

    body 1 = (0, a1),  body 2 = (0, a2),
    pair A = (+-u, v),  pair B = (+-p, q),   u, p > 0.

Gauge (translation + scale): a1 = 1, a2 = -1. The open stratum S is the
set of such configurations with no collisions and with DISTINCT pair
heights, q != v. The pair-equality lemma (dossier, closed form) forces
mA-pair and mB-pair masses equal off {q = v}, so the mass vector is
(m1, m2, mA, mB) and the reduced Laura-Andoyer block is SIX mass-linear
equations {L13, L15, L23, L25, L35, L36} in the nine quotient distances:
a 6 x 4 matrix J(u, v, p, q) whose kernel gives the admissible masses.

## 2a. The count, written out (the logical spine)

Let X be the gauged shape variety of the stratum (dim X = 4, EXP-015,
two-way engine agreement) and let

    I = { (x, m) : x in X, m in ker J(x), m != 0 }

be the incidence variety, with pi : I -> mass space the projection. Over
the locus where rank J = r the fibre of I -> X is the kernel, of dimension
4 - r, so

    dim I  =  max over r of [ dim{ rank J = r } + (4 - r) ].

Term by term, with R_j = {rank J <= j}:

    r = 4 :  dim <= 4 + 0 = 4                          (X itself)
    r = 3 :  dim <= dim R_3 + 1 <= 3 + 1 = 4           needs R_3 != X
    r = 2 :  dim <= dim R_2 + 2 <= 2 + 2 = 4           needs dim R_2 <= 2
    r = 1 :  dim <= dim R_1 + 3                        needs R_1 = empty
    r = 0 :  dim <= dim R_0 + 4                        needs R_0 = empty

So dim I <= 4, which is the dimension of the mass space; hence pi has
finite generic fibres (and if pi is not dominant its image is a proper
closed subset, so generic masses admit no such configuration at all:
finiteness holds either way). The four requirements are exactly what the
campaign supplies:

    R_0 = empty      lemma piece 9-prep (exact, global)
    R_1 = empty      every certified box carries either a rank >= 3 minor
                     or a trap whose rank-2 witness excludes R_1
    dim R_2 <= 2     rank >= 3 certificates off the trapped boxes, and on
                     each trapped box R_2 lies in a smooth codimension-2
                     manifold; finitely many boxes, so dim R_2 <= 2
    R_3 != X         exact rank-4 witness W1 (EXP-016)

The centered pentagon shows dim R_2 = 2 is ATTAINED, so the bound is
sharp and no weaker hypothesis would do.

## 2. What the chain needs

Following the Dias-Pan pattern (their Lemma 7.3), generic finiteness for
the stratum follows from a dimension count over the rank strata of J. Let
R_j = {rank J <= j}. The count needs the LADDER

    dim (R_j intersect shape+)  <=  j        for j = 0, 1, 2,

together with the shape variety's dimension 4 (EXP-015, two-way engine
agreement) and the k = 4 case (EXP-016's exact rank-4 witness plus
irreducibility of the parametrized component). Cases k = 0, 1, 2, 4 of the
chain were closed in closed form (lemma pieces 4, 5, 6 and the R_0 lemma).
The last case, k = 3, is exactly the ladder above, and is what the
covering programme establishes.

## 3. The instrument

A box (u, v, p, q) is discharged by one of three certificates, all in
exact rational interval arithmetic with outward rounding:

  (a) RANK >= 3: some 3 x 3 minor of J excludes zero over the box (plain
      intervals, or a mean-value form with dual-interval gradients when
      the box is small). The box contributes nothing to R_2 or R_1.
  (b) TRAP: a 2 x 2 minor excludes zero over the box (so R_1 meets it
      nowhere) AND two 3 x 3 minors have a 2 x 2 gradient subdeterminant
      excluding zero over the box (so R_2 meets it inside a smooth
      codimension-2 manifold, dimension 2). Ladder-equivalent to (a).
  (c) BISECTION, to a declared depth cap; residual failures are recorded
      and investigated, never assumed away.

Charts. Where a region's limit is singular (collisions, pair collapses,
infinity) the matrix is put in an ANALYTIC chart first: rational
parametrization of directions, blow-up of the singular locus, and row or
column rescalings by nonvanishing factors (rank is preserved at interior
points). Every rescaling cancels the singular factors ALGEBRAICALLY before
any evaluation; the clearings are machine-generated where they are large.
Each chart is gated by a 5-point crosscheck against the original matrix
with its declared scalings BEFORE any covering run; this gate caught eight
real errors during construction.

## 4. The atlas

Bounded region (all coordinates within the gauge box):

    core        u, p in [1/4,3], |f| >= 1/4        CERTIFIED, 0 failures
    band        |f| <= 1/4, off the tube            CERTIFIED (44 trapped)
    tube R, L   collision tube, w >= 7/32           CERTIFIED, 0 failures
    tubeext R,L collision tube, w in [1/8,7/32]     CERTIFIED, 0 failures
    ulow        u in [0,1/4], p in [1/4,3]          CERTIFIED, 0 failures
    plow                                             = swap of ulow (9d)
    uplow       u, p in [0,1/4]                     running, 0 failures
    deep R, L   collision tube, w <= 1/8            running, 0 failures
    cb1         B at an axis body, A bounded        CERTIFIED + piece 10
    bicorner-opp  A, B at opposite axis bodies      CERTIFIED, 0 failures
    bicorner-same A, B at the same axis body        running
    M1          quadruple cluster                   running
    M1-vert     vertical quadruple cluster          running
    M2          collinear quadruple corner          running

Outer region (inverted coordinates):

    fa1         A far, B bounded                    CERTIFIED, 0 failures
    fa2b        both far, ratio chart               running, 0 failures
    fartube     pairs merging at infinity           running, 0 failures
    cb1f        corner times far                    CERTIFIED + piece 10
    swap images                                     free by piece 9d

Symmetry. The swap (u,v,p,q) -> (p,q,u,v) and the mirror (v,q) -> (-v,-q)
are exact matrix identities (lemma pieces 9d, 9e: all 24 entries cancel
syntactically), so they generate a Klein four-group under which rank, R_1,
R_2 and every certificate are invariant. Half the atlas is free.

## 5. The face principle (what the residual failures were)

Every residual failure in every chart shares one cause: the box CONTAINS
an excluded face - a collision locus or a blow-up face - where the matrix
genuinely drops rank. No interval certificate can succeed on such a box,
and bisection reproduces the situation forever. The resolution has two
halves, both established:

  (i) MEASURED: every dyadic shell {face-distance in [h 2^-k-1, h 2^-k]}
      certifies (six consecutive halvings, both corner charts). The
      punctured neighbourhood is the union of shells.
  (ii) PROVEN: lemma piece 10 makes it uniform in k for the corner face,
      by an exact order-zero limit of a designated minor plus a complete
      branch table; the two branches with no surviving minor are exactly
      the two collisions the open stratum excludes.

Since R_2 is closed and every point of the punctured neighbourhood lies in
a certified shell, R_2 misses the collar entirely. The same argument shape
applies to the other faces; where a chart's failures were instead a
WRONG-CHART artifact (deep's 13,354, at a sliver just outside the declared
M2 discard) the boundary was shifted and the rerun certifies with zero
failures.

## 5a. The face table (completed 2026-08-20)

The face principle needs, per face, either a full-rank rescaled matrix or
a uniform lemma. A dedicated gate settled every case by evaluating each
chart's matrix ON its face:

    FULL RANK on the face (no lemma needed), min sigma_3 in brackets:
      tube R [1.4e-2] / L [2.2e-2], tubeext, deep [1.5e-4],
      ulow [1.6e-1], uplow u=0 [3.4e-2] and p=0 [2.6e-2],
      fa1 [2.4e-1], fa2b [6.4e-2], cb1 [1.6e-1], cb1f [2.0e-1],
      bicorner-opp [2.2e-1], bicorner-same [1.4e-2]

    RANK DROPS, closed in closed form:
      corner face      (a pair on an axis body)      lemma piece 10
      collapse face    (both pairs onto the axis)    lemma piece 11
      merge faces      (cluster; and at infinity)    lemma piece 12

Piece 11 is now also EFFECTIVE: the collapse chart implements its column
rescale directly and certifies the collar including the face itself (19 of
19 face sample points certify rank >= 3), so the lemma's "for all
sufficiently small eps" is replaced by certificates. Its discard was
corrected in the process: an |f| < 1/16 test rejected precisely the region
M2's residue occupies, whereas the true criterion is cs < 1/32, since
cs^2 = eps^2 (c - s)^2 + f^2 stays bounded below whenever either
contribution does. With that fix the chart certifies M2's residue directly.

Pieces 11 and 12 share one mechanism: at those faces the two axis-body
mass columns vanish to first order while the two pair columns survive, so
dividing the vanishing columns by the face parameter (positive off the
face, so rank is untouched) restores rank. Piece 11 carries it out in
closed form, with the explicit leading coefficient
4ab[phi(1-v)phi(-1-q) - phi(-1-v)phi(1-q)], phi(x) = x(1/8 - 1/|x|^3),
and a branch table on its zero curve; piece 12 verifies the same mechanism
on the two merge faces at three scales and forty samples each.

Piece 10 is the different one: there the face is generically full rank and
drops only on five explicit hypersurfaces, three of which carry a second
minor while the remaining two ARE the collisions the stratum excludes.

Every face of every chart is therefore accounted for.

## 6. Status

### 6a. What is proven outright

k = 0, 1, 2, 4; the ladder's j = 0 level globally; the reduction, the
pair-equality lemma, the symmetry identities, and now thirteen lemma
pieces (piece 13 belongs to the (0,3) stratum, not this one).

### 6b. The residue accounting, measured 2026-08-23

Every chart of the atlas has now run far enough to be classified. The
decisive measurement is the BOX WIDTH of the residual failures: for every
chart that has any, the failures share EXACTLY ONE distinct width, which
is the width the seed reaches at the shared depth cap of 44. Not one
residue in the atlas is a box that failed before the cap. That is what
separates a resolution limit from mathematics, and the whole atlas falls
on the resolution side.

| chart | failures | interior (no axis at 0) | disposition |
|---|---|---|---|
| bicorner-opp | 0 | -- | complete |
| bicorner-same | 0 | -- | complete |
| collapse | 0 | -- | complete |
| deep-L | 0 | -- | complete |
| deep-R | 0 | -- | complete |
| fa1 | 0 | -- | complete |
| fartube | 0 | -- | complete |
| m1 | 0 | -- | complete |
| m1vert-S | 0 | -- | complete |
| tube-L | 0 | -- | complete |
| tube-R | 0 | -- | complete |
| tubeext-L | 0 | -- | complete |
| tubeext-R | 0 | -- | complete |
| ulow | 0 | -- | complete |
| uplow | 0 | -- | complete |
| cb1 | 5 | 0 | all face-touching, closed by piece 10 |
| cb1f | 2 | 0 | all face-touching, closed by piece 10 |
| band | 44 | 12 | at the cap; residue re-run pending |
| fa2b | 200 | 188 | at the cap; residue re-run at depth 76 IN FLIGHT |
| m2-L | 5824 | 5824 | region covered by the collapse chart, which is at zero |
| m2-R | 5683 | 5683 | region covered by the collapse chart, which is at zero |
| fa2 | 280140 | -- | RETIRED, superseded by fa2b (absolute far-tube criterion was a design error) |
| m1vert-N | 7144 | -- | RETIRED, superseded by M1's per-entry guards |

Fifteen charts are at exactly zero. Of the five live charts with any
residue, two (cb1, cb1f) have every failure on a face and are closed in
closed form by piece 10, and two (m2-L, m2-R) cover a region the collapse
chart also covers at zero failures. The one genuinely open item is fa2b,
whose 200 boxes tile a curve at ratio r = 0.9375 -- a dyadic value, i.e.
where the chart's bisection grid crosses, not a feature of any locus.

### 6c. Resolution of the two open residues (2026-08-23)

BOTH are now settled, and they came out differently.

fa2b: the residue re-run at depth 76 finished `ok = True` with 1544 boxes
processed and ZERO failures. The whole 200-box residue discharged, so it
was purely a depth-cap artifact exactly as the box-width measurement
predicted. fa2b is complete.

band: the residue does NOT discharge, and it should not. Following it
found an exact rank-2 point on the face `v = q = 0` -- the CROSS POINT --
with a two-dimensional kernel meeting the positive orthant, i.e. a
degenerate central configuration. A rank-3 certificate cannot exist at a
rank-2 point, so the covering was right to refuse one. This is the first
residue in the campaign that turned out to be mathematics rather than
resolution. See the dossier section "THE CROSS POINT".

So every residue in the atlas is now accounted for:

| residue | disposition |
|---|---|
| 15 charts | zero failures |
| fa2b (200) | DISCHARGED at depth 76, zero failures |
| cb1 (5), cb1f (2) | entirely face-touching, closed by piece 10 |
| m2-L, m2-R | region covered by the collapse chart at zero |
| band (44) | the CROSS POINT, a genuine rank-2 degenerate configuration |
| fa2, m1vert-N | retired and superseded |

### 6d. What remains

The covering side is closed. What is NOT closed is the STATEMENT, because
the cross point falsifies the draft's uniqueness clause. Section 7 records
the withdrawal and the three questions that have to be settled before any
statement is drafted again. Nothing goes to Felipe as a statement until
those are answered, and nothing goes anywhere else at all.

## 7. The statement being assembled (draft, WITHDRAWN 2026-08-23)

The draft below is kept for the record and is NOT to be used. It names the
centred regular pentagon as the sharp degenerate point of the stratum, and
that is false as written: a second exact rank-2 point with an admissible
mass ray was found on the face v = q = 0 (the cross point, see the
dossier). The cross point lies on a face the stratum's declaration
excludes from the interior, so a statement about the OPEN stratum may
still stand, but the uniqueness wording does not and the whole sentence
has to be rebuilt.

WITHDRAWN DRAFT, for the record only:

> For the two-pair reflection-symmetric stratum of the planar six-body
> problem - two bodies on the symmetry axis, two mirror pairs at distinct
> heights, no collisions - the pair masses are forced equal by the
> Laura-Andoyer equations, and for all mass vectors (m1, m2, mA, mB)
> outside a proper closed subset the number of such central
> configurations, counted in the gauge, is finite. The centered regular
> pentagon (bodies 1, 3, 4, 5, 6 on a circle centered at body 2, exact
> rank 2, kernel = free central mass plus equal ring masses) is the sharp
> degenerate point: it is where the rank-2 locus attains the dimension the
> chain allows.

What has to be settled before a statement is drafted again:

  1. whether the cross point is the ONLY degenerate point on the closure
     of the stratum, or only the only one on the cross face (the census
     covered the cross face alone, in a bounded window);
  2. whether the open stratum -- pairs at strictly distinct heights --
     contains any degenerate point besides the centred pentagon;
  3. whether the cross point is known in the literature. It has not been
     checked and must not be presented as new.

Per the standing rule, no statement wording goes anywhere until Felipe
sees it first, and there is now nothing ready to show.
