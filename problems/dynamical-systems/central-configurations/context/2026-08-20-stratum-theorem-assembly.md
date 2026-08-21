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

## 6. Status

Proven: k = 0, 1, 2, 4; the ladder's j = 0 level globally; the reduction,
the pair-equality lemma, the symmetry identities, ten lemma pieces.
Established by certified covering: the ladder's j = 1, 2 levels on the
core, band, collision tube (three w-ranges), pair-collapse collar, the
opposite bi-corner, the far-A chart, and the corner charts (with piece 10
closing their collars).
In flight, all with zero failures at the time of writing: uplow, deep,
fa2b, fartube, bicorner-same, M1, M1-vert, M2.
Not yet run: nothing. Every region of the open stratum now has a chart.

When the in-flight coverings finish, the chain is complete and the
statement wording goes to Felipe FIRST, per the standing rule, before any
manuscript or Zenodo step.

## 7. The statement being assembled (draft, NOT yet to be recorded elsewhere)

For the two-pair reflection-symmetric stratum of the planar six-body
problem - two bodies on the symmetry axis, two mirror pairs at distinct
heights, no collisions - the pair masses are forced equal by the
Laura-Andoyer equations, and for all mass vectors (m1, m2, mA, mB) outside
a proper closed subset the number of such central configurations, counted
in the gauge, is finite. The centered regular pentagon (bodies 1, 3, 4, 5,
6 on a circle centered at body 2, exact rank 2, kernel = free central mass
plus equal ring masses) is the sharp degenerate point: it is where the
rank-2 locus attains the dimension the chain allows.
