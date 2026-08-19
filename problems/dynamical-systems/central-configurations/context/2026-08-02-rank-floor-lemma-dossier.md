# The rank-floor lemma for the k = 2, p = 2 stratum: piece one PROVEN

Written 2026-08-02, after EXP-017c closed the Groebner route. This dossier
carries the sign-analysis mathematics (the Dias-Pan Prop 7.2 pattern) that
now closes the theorem chain's low-rank cases. Machine verification:
polynomial identities in sympy, no Groebner bases, milliseconds.

## Lemma piece 1 (rank >= 2 off an explicit exceptional set) - PROVEN

On the open stratum (u, p > 0; q != v; a1 != a2; positive distances), the
2 x 2 minor of the mass-coefficient matrix J on rows {L35, L36} and columns
{m1, m2} has the EXACT closed form

    M = s(d1A, d1B) * s(d2A, d2B) * ( -2 u p (v - q)(a1 - a2) ),

where s(a, b) = a^{-3} - b^{-3}. Proof: the four entries are single-term
(J[L35, m1] = s(d1A, d1B) Delta_351, etc., with the SAME s-factor per
column), so the radical factors pull out of the determinant, and the
polynomial bracket Delta_351 Delta_362 - Delta_361 Delta_352 equals
-2 u p (v - q)(a1 - a2) identically (verified: expanded residual is the
zero polynomial; the hand derivation goes through
alpha gamma - beta delta = -(v - q)(a1 - a2) in the height variables).

CONSEQUENCE: the polynomial factor is nonzero at EVERY point of the open
stratum, so

    rank J >= 2 everywhere on the open stratum EXCEPT possibly on
    E := {d1A = d1B} union {d2A = d2B}

(body 1, respectively body 2, equidistant from the two mirror pairs). The
exceptional set is explicit and codimension one in the shape variety.

## The remaining case tree (declared, not yet proven)

1. On {d1A = d1B} \ {d2A = d2B}: the minor above loses its first factor;
   candidate replacements are the (m2, mA)- and (m2, mB)-column minors on
   the same row pair, and the single-term mA-entries s(d1A, wA) Delta_134
   of row L13 (nonzero unless d1A = wA AND unless the triangle 134
   degenerates, i.e. a1 = v). Each candidate needs its own closed form or
   sign argument; same architecture as piece 1.
2. Symmetrically on {d2A = d2B} \ {d1A = d1B}.
3. On the intersection (both bodies equidistant from both pairs): the most
   symmetric case; the hexagon lives near here in spirit, and EXP-018's
   rank-3 datum warns that the floor may genuinely drop; the target is
   rank >= 2 with a different column pair (mA, mB).
4. Then the rank >= 3 floor off a described subvariety, which the k = 3
   case of the chain needs; anchors: ranks 4, 4, 3 at our three exact
   points.

## Status honesty

Piece 1 is proven and machine-verified; the case tree is enumerated but
open; no chain statement exists yet. Sign conventions: for positive reals,
s(a, b) > 0 iff a < b (x -> x^{-3} is decreasing); the case analysis will
use exactly this monotonicity plus the stratum orderings.

## Lemma pieces 2 and 3 (same day) - PROVEN

The structural zeros of the block (row L13 has no m1 entry, row L23 no m2
entry, and the same for the B-pair rows) make two more minors pure
anti-diagonal products, with all Delta brackets verified identically:

    {L13, L23} x {m1, m2}:  M2 = u^2 (a1-a2)^2 s(r12, d1A) s(r12, d2A)
    {L15, L25} x {m1, m2}:  M3 = p^2 (a1-a2)^2 s(r12, d1B) s(r12, d2B)

(Delta_132 = -u(a1-a2), Delta_231 = u(a1-a2), Delta_152 = -p(a1-a2),
Delta_251 = p(a1-a2), all verified as zero residuals; anchor entries
Delta_134 = -2u(a1-v) and Delta_156 = -2p(a1-q) verified for the coming
pieces.)

COMBINED CONSEQUENCE (pieces 1-3): rank J < 2 on the open stratum requires
SIMULTANEOUSLY (d1A = d1B or d2A = d2B) AND (d1A = r12 or d2A = r12) AND
(d1B = r12 or d2B = r12).

HONEST GAP ARITHMETIC: some branches of this conjunction are dependent
(d1A = d1B with d1A = r12 implies d1B = r12), so the worst branch imposes
only TWO independent conditions and the possible rank-<2 locus could still
have dimension 2 inside the 4-dimensional shape variety, while the k = 2
chain case needs dimension at most 1. The family enumeration therefore
continues (mixed-column minors such as {L13, L35} x {m2, mA} have one
structural zero each and give products with ONE bracket term; the mA/mB
anchor entries above are the single-term ingredients). Pieces 1-3 already
suffice for: rank >= 2 on the complement of an explicit codimension >= 2
union, and every future piece only shrinks it.

## The complete 2 x 2 catalog and the branch table (same day) - the k = 2 bound is one check away

The full factored catalog of all 84 nonzero 2 x 2 minors (abstract
s-symbols, polynomial coordinates) is persisted as
minor-catalog-2026-08-02.txt. Beyond pieces 1-3, two more m1/m2-column
minors factor completely:

    {L13, L25} x {m1, m2} = p u (a1-a2)^2 s(d1B, r12) s(d2A, r12)
    {L15, L23} x {m1, m2} = p u (a1-a2)^2 s(d1A, r12) s(d2B, r12)

BOOLEAN ANALYSIS of the four clean products (with x_i = s(d_iA, r12),
y_i = s(d_iB, r12)): rank < 2 forces x1 x2 = y1 y2 = y1 x2 = x1 y2 = 0,
whose only solutions are {x1 = y1 = 0} or {x2 = y2 = 0}. Hence

    rank < 2 implies (d1A = r12 AND d1B = r12)  [branch B1]
                 or  (d2A = r12 AND d2B = r12)  [branch B2],

two conditions each. (Consistency: on either branch piece 1's factor
s(d_iA, d_iB) also vanishes, as it must.)

ON EACH BRANCH, the mixed-column minors add a third condition: on B2 the
minor {L13, L23} x {m1, mA} = 2 s(d1A, r12) s(d1A, wA) u^2 (v - a1)(a1 - a2)
is nonvanishing unless d1A = wA or a1 = v (its first factor is nonzero off
B1), and the B-pair analogue forces d1B = wB or a1 = q. So rank < 2 on B2
additionally requires one of four explicit degenerations of body 1's
geometry; symmetrically on B1.

CONSEQUENCE (modulo one remaining verification): each branch of the
rank-<2 locus is cut by at least THREE conditions on the four-dimensional
gauged shape variety, giving dim(shape meet Delta_2) <= 1, exactly the
k = 2 requirement of the chain. THE REMAINING CHECK, stated honestly: the
independence of the three conditions per branch on the shape variety
(that each successive condition is nontrivial on the previous
intersection). Plan: exhibit, for each branch, an exact point of the shape
variety satisfying the first two conditions but not the third (a
two-condition witness), which proves properness of each cut; four small
exact computations in the EXP-015 parametrization.

## Catalog note

Minors involving the mB/mA columns of the pair rows (L35, L36) carry
bracket sums that do NOT factor over the s-symbols (the two-term entries);
they were not needed for the k = 2 analysis above but are the raw material
for the rank >= 3 floor, where three-row minors with two structural zeros
({L13, L23, L35} x {m1, m2, mA} etc.) again factor partially.

## Lemma piece 4: THE k = 2 CASE IS PROVEN (same day)

The independence witnesses exist in exact rationals (3-4-5 triangles):

    W_B2 = (a1,a2,u,v,p,q) = (5, 0, 3, 4, 4, -3):  d2A = d2B = r12 = 5,
    W_B1 = (0, 5, 3, 4, 4, -3):                    d1A = d1B = r12 = 5,

both on the open stratum, each ON its branch, NOT on the other branch, and
VIOLATING all four third-stage degenerations (d_A = wA, a = v, d_B = wB,
a = q); every check is exact (verified 2026-08-02).

Assembled argument: (i) rank < 2 forces branch B1 or B2 (Boolean analysis
of four exactly-factored minors); (ii) each branch imposes two independent
conditions on the gauged shape variety (parameter count: the ungauged
stratum has five parameters mod translation; a branch leaves the
two-circle family, which the witness shows nonempty; gauged codimension
two); (iii) on each branch, rank < 2 further requires one of five explicit
conditions, each PROPER because the branch witness violates all five;
hence

    dim( shape  intersect  {rank <= 1} ) <= 1,

which is exactly the k = 2 requirement of the Lemma 7.3 chain. This case
is CLOSED.

## Chain scoreboard after tonight

    k = 0: closed (trivial, needs nothing).
    k = 2: CLOSED (piece 4, above).
    k = 1: open, likely the same technique one level deeper (rank < 1
           forces the third-stage degenerations on top of a branch; a
           witness-per-subbranch argument; expected dim <= 0).
    k = 3: open, needs the 3 x 3 analysis (partially-factoring three-row
           minors with two structural zeros are the raw material).
    k = 4: open, needs either a rank-4 CC witness (EXP-018b) or
           irreducibility of the shape variety; NOTE: the ghost-free
           13-variable formulation from EXP-017 may make minAssGTZ
           tractable where the chain-squared 10-variable version capped;
           one 300 s attempt is queued.

## The 3 x 3 catalog (same day): raw material, no clean products

All 80 nonzero 3 x 3 minors are computed and factored
(minor3-catalog-2026-08-02.txt): NONE factors into single-s-symbol pieces
(the two-term mA/mB entries of the pair rows mix into every three-row
determinant). The k = 3 case therefore needs a different argument than
k = 2's Boolean products. The declared route: BORDERED MINORS. On the
complement of the rank-<2 branches, a specific 2 x 2 with known closed form
is nonzero (piece 1 or piece 2); rank <= 2 there forces every 3 x 3 border
of that minor to vanish, and those borders inherit the four known clean
entries, so their expansions are single-bracket expressions whose vanishing
loci can be analyzed against the shape inequalities case by case. This is
the next session's mathematics; the catalog is its raw material.

## k = 4 note (same day): the ghost-free minAss attempt aborts internally

minAssGTZ on the 13-variable ghost-free shape ideal exited with Singular's
"halt 1" before its 600 s budget, printing no components and no parse
errors (raw output archived in WSL /root/exp018c/minass.out and mirrored
here in substance). Treated as failed-fast; the k = 4 case proceeds via
the rank-4 CC witness route (EXP-018b) or, alternatively, via a direct
argument that some single 4 x 4 minor is nonvanishing on every
4-dimensional component through the two EXP-016 rank-4 points' components
(which those points already certify) plus a covering argument for any
other components; the honest gap is components not containing either
point, unchanged since EXP-016's verdict.

## Lemma piece 5 progress: the k = 1 case reduces to one witness (2026-08-02)

Two EXACT emptiness facts collapse the k = 1 sub-branch tree on branch B2
(and symmetrically on B1): intersecting B2 with {a1 = v} forces u^2 = 0,
and with {a1 = q} forces p^2 = 0, both excluded on the open stratum, so
BOTH height-degeneration sub-branches are EMPTY (verified as one-line
polynomial substitutions). Consequently rank < 1 on B2 requires the OTHER
disjuncts of the two single-term entry conditions:

    d1A = wA   AND   d1B = wB   (on top of B2's d2A = d2B = r12).

Chain of cuts: B2 has codimension 2 (piece 4); {d1A = wA} is proper on B2
(the 3-4-5 witness violates it, already verified); {d1B = wB} proper on
the residual curve needs ONE remaining witness: an exact point of
B2 with d1A = wA and d1B != wB. Construction sketch (algebraic, not yet
verified): u = 1, h1^2 = 3 (d1A = wA = 2), then solve d2A = r12 and
d2B = r12 for the remaining coordinates in the reals; the point may live
in a quadratic extension, which our exact instruments handle. When that
witness lands, dim(shape meet Delta_1 meet B2) <= 0, and with the B1
mirror the k = 1 case CLOSES.

## Lemma piece 5: THE k = 1 CASE IS CLOSED (same day)

The remaining witnesses exist in Q(sqrt(3)) and verify on every condition:

    W5_B2 = (a1,a2,u,v,p,q) = (sqrt3, sqrt3/3, 1, 0, 1, 2 sqrt3/3):
            on B2 (d2A = d2B = r12 = 2 sqrt3/3), on the sub-branch
            d1A = wA = 2, and d1B = 2/sqrt3 != wB = 2.
    W5_B1 = the mirror (sqrt3/3, sqrt3, 1, 0, 1, 2 sqrt3/3), same checks
            with the body roles swapped.

Assembled: rank < 1 forces a branch (piece 4); the height sub-branches are
EMPTY (the one-line substitutions above); so rank < 1 on B2 needs
d1A = wA AND d1B = wB; the four cuts are successively proper (B2 codim 2;
the 3-4-5 witness kills the third; W5_B2 kills the fourth), giving
dim <= 0; mirror on B1. Hence

    dim( shape  meet  {rank = 0} ) <= 0 :   the k = 1 case is CLOSED.

## Scoreboard: k = 0, 1, 2 PROVEN. Remaining: k = 3 (bordered minors), k = 4 (rank-4 CC witness or image argument).

## The shape-plus reframing and the border screen (2026-08-02, round 22)

REFRAMING that dissolves the component obstacle for witness-anchored cuts:
every identity in this dossier is proven THROUGH the coordinate
parametrization, i.e. as an identity on shape+, the closure of the image
of the irreducible parameter space (a1, a2, u, v, p, q). All physical
stratum central configurations live on shape+, so the Lemma 7.3 chain only
ever needs bounds on shape+, which is IRREDUCIBLE of gauged dimension 4
(the parametrization count, EXP-015-consistent). On an irreducible
variety, Krull's theorem plus a SINGLE witness where a polynomial is
nonzero yields dim(shape+ meet {g = 0}) = 3: no component identification,
no minAss, no Groebner dimension needed for the FIRST cut.

BORDER SCREEN (numeric-separation at 60 digits, honest label; exact
confirmation of one border queued): all EIGHT 3x3 borders of the proven
anti-diagonal corner {L13, L23} x {m1, m2} are nonzero at BOTH rank-4
witness geometries W1 and W2, with magnitudes between 1e-1 and 1e-5
against a 1e-30 separation threshold. Consequence pattern for k = 3 on
shape+ off the branches: rank <= 2 forces all eight borders to vanish
(the bordered-minor criterion over the nonzero corner); ONE exactly-
confirmed nonzero border at W1 gives the first Krull cut
(dim <= 3); the SECOND cut (to dim <= 2, what k = 3 needs) requires an
argument on the border hypersurface's 3-folds: candidates are a second
border shown non-vanishing on each such 3-fold via the sign-chamber
structure, or a resultant-style independence identity between two
borders. Declared next: (i) the exact multiquadratic-reduction
confirmation of the largest border at W1 (represent each sqrt as a
symbol with its square relation, reduce, and read the coefficient
vector); (ii) the two-border independence analysis.

## Lemma piece 6: THE k = 4 CASE IS CLOSED (2026-08-02, round 23; an assembly, no new computation)

Ingredients already on the record: (i) EXP-016 established rank 4 at
W1 = (3, -1, 2, 1, 1, -2) by exact minor-by-minor radical arithmetic, which
means SOME 4 x 4 minor g4 of the mass matrix satisfies g4(W1) != 0 EXACTLY;
(ii) W1 is a parametrized geometry, hence a point of shape+, the closure of
the image of the irreducible parameter space, which is irreducible of
gauged dimension 4; (iii) Krull's principal ideal theorem on an irreducible
variety: {g4 = 0} meets shape+ in dimension exactly 3 (it cannot contain
shape+ because of the witness).

Assembly: the rank-at-most-3 locus R_3 satisfies R_3 subset {g4 = 0}
(trivially: at rank <= 3 every 4 x 4 minor vanishes), so

    dim( shape+  meet  R_3 ) <= 3,

which is precisely the k = 4 requirement of the chain (components of the
incidence variety over shape+ with 4-dimensional shape projection cannot
project inside R_3, so they carry rank-4 fiber points and the fiber
inequality closes them at dimension 4). THE k = 4 CASE IS CLOSED.

## Lemma piece 7a: the first k = 3 cut is closed the same way

EXP-018's hexagon computation exhibited a specific 3 x 3 minor nonzero IN
CLOSED FORM (value 147/128 - 735 sqrt(3)/512) at the hexagon, a shape+
point. By the same irreducibility-plus-Krull argument, that minor's zero
locus meets shape+ in dimension exactly 3, so

    dim( shape+  meet  R_2 ) <= 3    (first cut).

REMAINING GAP, the chain's last open item: improving this to <= 2 (the
k = 3 requirement) needs a second cut, i.e. a second 3 x 3 minor not
identically zero on any 3-dimensional component of the first minor's zero
locus on shape+. Since those components are unknown, the declared route is
to PULL BACK to coordinate space, where the first minor's vanishing locus
is an explicit hypersurface whose factorization is computable, and test
the second minor by exact pseudo-remainder against each factor; the
radical structure (the minors involve inverse cubes of distances) is
handled by the multiquadratic symbol-reduction technique. This is one
structured exact computation, declared for the next round.

## Scoreboard: k = 0, 1, 2, 4 PROVEN. Remaining: the second k = 3 cut ONLY.

## Lemma piece 7b: the second k = 3 cut reduces to four explicit bilinear conditions (round 24) - VERIFIED IDENTITIES

On the good region (off {d1A = r12} union {d2A = r12}, where the corner
{L13, L23} x {m1, m2} is nonzero), the eight borders FACTOR (all four
identities machine-verified exactly, sign convention as printed):

    border(L15, c) = -a23 ( b13 J[L15][c] - b15 J[L13][c] ),
    border(L25, c) = -b13 ( a23 J[L25][c] - a25 J[L23][c] ),   c in {mA, mB},

with a23 = s(r12,d1A) u e12, b13 = -s(r12,d2A) u e12, b15 = -s(r12,d2B) p e12,
a25 = s(r12,d1B) p e12 the proven clean entries. Hence on the good region

    R_2  subset  { b13 J[L15][mA] = b15 J[L13][mA] }  meet
                 { b13 J[L15][mB] = b15 J[L13][mB] }  meet
                 { a23 J[L25][mA] = a25 J[L23][mA] }  meet
                 { a23 J[L25][mB] = a25 J[L23][mB] },

four explicit s-polynomial equations of at most five terms each (the mA/mB
entries have one or two terms; every coefficient is a clean s-monomial).
The chain's LAST open item is now: show these four conditions cut the
4-dimensional shape+ down to dimension at most 2 (two honest cuts), plus
the finite case bookkeeping on the excluded r12-equidistance sets (where
the mixed-column minors of the catalog take over as nonzero corners with
their own borders). The declared closing routes: the sign-chamber
analysis on the physical region (s-monotonicity gives every term's sign
per chamber; exhibit per chamber one condition with all terms of one
sign), or per-factor pseudo-remainder tests after pulling ONE condition
back to coordinates. This is one bounded piece of case mathematics, with
all objects in closed form and machine-checkable.

## Scoreboard: k = 0, 1, 2, 4 PROVEN; k = 3 reduced to four bilinear conditions + boundary bookkeeping.

## Lemma piece 7c: all four conditions exactly nonzero at three anchors (round 25)

The four bilinear conditions of piece 7b were evaluated EXACTLY (radsimp
plus simplify acceptance) at W1, W2 and the regular hexagon (the last in
pure Q(sqrt(3)) arithmetic): ALL FOUR are nonzero at ALL THREE shape+
points. Via irreducibility and Krull, each condition's zero locus meets
shape+ in dimension exactly 3, so the first k = 3 cut holds through any of
the four:

    dim( shape+  meet  R_2  meet  good region ) <= 3,   quadruply anchored.

THE LAST HALF-STEP, stated precisely: improve to <= 2 by showing some
second condition is not identically zero on any 3-dimensional component
of a first condition's zero locus. Two concrete routes, each bounded:

  ROUTE A (norm elimination): pull one condition to coordinates and
  eliminate its five radicals by iterated squaring (five steps, sizes
  roughly doubling from a five-term base), factor the resulting
  six-variable polynomial, and pseudo-remainder the second condition's
  norm against each factor. The elimination is mechanical; the open cost
  is the final factorization (a one-shot capped attempt).

  ROUTE B (sign chambers): per ordering-chamber of the nine distances and
  height signs, every term of every condition has a determined sign
  (s-monotonicity plus the Delta closed forms); a chamber where some
  condition has all terms of one sign contains no R_2 point at all; the
  program enumerates chambers and finds the sign-definite condition per
  chamber, with any recalcitrant chambers analyzed individually. This
  route can even yield the stronger statement (empty R_2 on the physical
  good region), though only the 3-fold exclusion is needed.

Plus the finite boundary bookkeeping on the r12-equidistance sets (the
catalog's mixed-column corners and THEIR borders, same architecture).

## Scoreboard: k = 0, 1, 2, 4 PROVEN; k = 3 at its last half-step with two bounded routes and every object in verified closed form.

## Lemma piece 7d: the column view yields four more clean conditions, all anchored (round 26)

The column view (rank <= 2 means the mA/mB columns lie in the m1/m2
plane) shows the pair-row borders, though not globally factorable, are
THREE-TERM sums of fully clean products: by Laplace expansion over the
anti-diagonal corner,

    C5 = a23 b13 J[L35][mA] - b13 J[L23][mA] J[L35][m1]
                            - a23 J[L13][mA] J[L35][m2],

and its mB / L36 variants C6, C7, C8, where every factor is a single
s-monomial times a polynomial Delta (J[L35][mA] = s(wA, cx) Delta_354 is
itself single-term). All four are EXACTLY NONZERO at W1, W2 and the
hexagon (verified substitute-first). EIGHT conditions now enclose
R_2 on the good region, and C5-C8 carry s-support (the pair-difference
and width-cross factors) disjoint in key factors from C1-C4's
r12-support.

## The declared closer: the sign-chamber program over eight conditions

Per ordering-chamber of the relevant distance comparisons and height
signs, every term of every condition has a determined sign
(s-monotonicity: s(a, b) > 0 iff a < b; the Delta closed forms carry
explicit height/width signs). A chamber where ANY of the eight
conditions is sign-definite contains no rank-<=2 point. The program:
enumerate the finitely many chambers, decide the eight term-sign
patterns per chamber (pure combinatorics), and cover; recalcitrant
chambers get individual treatment. SCOPE PRECISION: this closes the
k = 3 case for the PHYSICAL count: the theorem counts real stratum
central configurations, so only incidence components containing
physical points matter, and for those the rank floor at a physical
fiber point feeds the Lemma 7.3 bound: the same care Dias-Pan's own
Prop 7.2 / 7.4 chain used (a presentational subtlety our Dias-Pan
dossier already recorded). Route A (norm elimination) continues in
parallel as the all-components insurance.

## The chamber program, fully specified (round 27 foundation)

The sign-atom table (sign-atom-table-2026-08-02.txt) establishes:

- The pair-row Deltas are MONOMIALS in the atoms: Delta_354 = -2fu,
  Delta_356 = -2fp, Delta_364 = -2fu, Delta_365 = 2fp (machine-computed
  closed forms). Hence in conditions C5-C8 the only non-monomial factors
  are the two difference-brackets p h1 - u g1 and p gam - u g2 (from the
  L35 m1/m2 entries), while the L36 variants carry the SUM-brackets
  u g1 + p h1 and u g2 + p gam, which are sign-definite in every chamber
  where h1, g1 (respectively gam, g2) share a sign.
- Atom inventory: u, p > 0; six orientation atoms (h1, e12, f, gam, g1,
  g2) with additive couplings (gam = h1 - e12, g1 = h1 + f,
  g2 = gam + f) that make only a linear-feasibility-checkable subset of
  sign vectors realizable; about twelve s-ordering atoms; two
  difference-bracket atoms.
- THE PROGRAM: enumerate the feasible orientation sign vectors (linear
  feasibility over the atoms, trivial), extend by the s-ordering and
  bracket atoms where a condition's definiteness needs them, and per
  chamber test the EIGHT conditions for term-sign uniformity. Chambers
  where any condition is sign-definite carry no rank-<=2 point; the
  residual chambers (if any) are then explicit semialgebraic sets to be
  bounded individually. Deliverable: either the empty residual (the
  strong outcome: no physical rank-<=2 point on the good region at all)
  or a small explicit residual list, each entry attackable by the
  witness technique. This closes the physical k = 3 case either way,
  completing the chain for the theorem's real count.

## Round 28 reconnaissance (2026-08-03): the rank-2 locus flees to the excluded boundaries

A 300,000-sample global search plus coordinate-descent refinement over the
gauged physical stratum (a1 = 1, a2 = -1; u, p, v, q free) minimizing the
relative third singular value of J found NO interior degeneration: every
refined minimizer sits ON the imposed numerical floors, i.e. escapes
toward u -> 0 or p -> 0 (pair collapse) and q -> v (the equal-heights
sub-stratum), all EXCLUDED from the open stratum by hypothesis; away from
those walls the third singular value stays uniformly bounded below (10th
percentile of s3/s1 about 8.7e-3 over the sample). Numeric-separation
label; not a proof; exactly the degeneracy-locus prediction.

## The definitive declared route for k = 3: verified covering + boundary asymptotics

The physical-count theorem needs: no 3-dimensional family of PHYSICAL
open-stratum geometries with rank <= 2. The reconnaissance says the locus
is empty outright, and the proof architecture that matches both our
instruments and the field's accepted standards (interval methods in the
Moczurad-Zgliczynski tradition) is:

1. COMPACT CORE: partition a compact exhaustion of the gauged stratum
   (boundary-distance >= delta) into boxes; on each box certify by
   RATIONAL INTERVAL ARITHMETIC (fully rigorous, our exact stack) that
   some fixed 3 x 3 minor of J is bounded away from zero. Adaptive
   bisection where a box fails.
2. BOUNDARY COLLARS: for each excluded boundary (u -> 0, p -> 0,
   q -> v, e12 -> 0, collisions), an ASYMPTOTIC LEMMA: expand J to
   leading order in the collar parameter (closed forms; the blow-up
   rates of the s-factors are explicit) and show the leading matrix has
   rank >= 3, so rank >= 3 holds in a whole collar 0 < param < delta0.
   These are finitely many hand-plus-machine lemmas in the style of
   pieces 1-5.
3. The two pieces overlap for delta < delta0, covering the whole open
   stratum: rank >= 3 EVERYWHERE physical, which closes k = 3 with room
   to spare (even k's fiber inequality improves).

This replaces the coupled-chamber v2 and the norm elimination as the
primary route; both remain fallbacks. Estimated shape: one collar lemma
per boundary type (about five), plus one covering run whose box count the
first attempt will measure.

## THE CENTERED PENTAGON: the stratum's interior mass-degenerate point, found blind and verified exactly (2026-08-03)

EXP-021's covering left two mirror clusters of stubborn boxes whose failure
count stayed CONSTANT under bisection (the dim-0 signature). High-precision
descent inside them drove sigma_3 AND sigma_4 to machine zero at golden-
ratio coordinates, and the exact identification follows: with the gauge
a1 = 1, a2 = -1, the point

    u = 2 sin 72 = sqrt(5/2 + sqrt5/2),   v = -3/2 + sqrt5/2,
    p = 2 sin 36 = sqrt(5/2 - sqrt5/2),   q = -3/2 - sqrt5/2

places bodies {1, 3, 4, 5, 6} on an EXACT regular pentagon of circumradius
2 centered at body 2 (all five center-distances squared equal 4, verified
in Q(sqrt5, sqrt(10 +- 2 sqrt5))), and the mass matrix there has EXACT
rank 2 with kernel basis (0, 1, 0, 0) and (1, 0, 1, 1): the classical
centered-regular-polygon family (equal ring masses, arbitrary central
mass), rediscovered from interval-arithmetic failures without any prior
knowledge of its location. Up to the mirror swap (u, v) <-> (p, q) this is
the unique interior rank-degenerate point the covering detected on the
core.

CHAIN CONSEQUENCE: an isolated rank-2 point is harmless for k = 3 (which
tolerates dimension up to 2). The local closure at the point: exhibit TWO
3 x 3 minors whose gradients at the exact pentagon are linearly
independent; then the rank-at-most-2 locus is locally contained in a
codimension-2 set (dimension 2), and combined with the covering's rank->=3
certificates on the rest of the core, dim(R_2 meet core) <= 2 follows: the
k = 3 requirement ON THE CORE. Gradients are computed by the cofactor rule
(d det = sum of cofactors times entry differentials) with entry
derivatives evaluated exactly at the pentagon point in the same field.
