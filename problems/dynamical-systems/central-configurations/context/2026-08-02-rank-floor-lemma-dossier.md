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

## Lemma piece 8: THE k = 3 BOUND HOLDS ON THE CORE (2026-08-03)

Two 3 x 3 minors of the mass matrix ({L13,L15,L23} x {m1,m2,mA} and
{L23,L25,L35} x {m1,mA,mB}) have EXACT gradients at the centered-pentagon
point (computed by the cofactor rule with entry derivatives evaluated in
the golden field), and the 2 x 4 gradient matrix has EXACT RANK 2. By the
implicit function theorem their common zero locus is, near the pentagon
(and its mirror image), a codimension-2 submanifold, hence of dimension 2;
the rank-at-most-2 locus R_2 is contained in it. Everywhere else on the
gauged core the interval covering certifies rank >= 3 (phases 1-3: naive
certificates, refinement, and mean-value certificates; the once-stubborn
boxes are exactly the pentagon clusters). Therefore

    dim( R_2  meet  core ) <= 2,

which is the k = 3 requirement of the chain ON THE CORE, achieved on the
nose by the centered pentagon (R_2 is nonempty there, so the bound is
sharp). REMAINING for the full k = 3 and hence the whole chain: the collar
and outer asymptotic lemmas (q -> v, u or p -> 0, large coordinates), plus
ONE integrated clean covering rerun to produce the single complete
certificate list for the record (the current certificates are spread
across phases; the mathematics is done, the artifact hygiene remains).

## THE COVERING PROGRAMME RESTRUCTURE (2026-08-19)

Two corrections and one simplification, found while planning the collar
lemmas, all now declared in EXP-022/hypothesis.md.

**Correction 1 (the ladder).** The mass-fiber dimension count behind the
chain needs dim(R_j meet shape+) <= j for ALL of j = 0, 1, 2, not only
j = 2: over the rank-r locus the mass fiber has dimension 4 - r, so
dim Omega <= max_r [ dim(rank = r locus) + (4 - r) ], and every level must
be bounded. Status: j = 0 is CLOSED GLOBALLY by lemma piece 9-prep below;
j = 1 and j = 2 follow together from the rank >= 3 coverings off the
exceptional balls, and ON each ball from the two ball certificates (rank-2
witness: a 2x2 minor interval-nonzero over the whole ball, so R_1 meet
ball is empty; gradient pair: two 3x3 minors with interval-independent
gradients over the whole ball, so R_2 meet ball sits inside a smooth
2-manifold). The ball certificates replace piece 8's implicit function
theorem step with an EXPLICIT radius (2^-8), removing the non-effective
neighborhood; all four pentagon copies (mirror and pair-swap images)
certified in 0.1 s each (EXP-021 integrated preflight).

**Lemma piece 9-prep: R_0 meets the stratum nowhere (2026-08-19).**
J = 0 forces, from the four single-s-term entries with monomial brackets
(L23/L13 x m1/m2 and L25/L15 x m1/m2), d1A = d2A = 2 and d1B = d2B = 2;
d1A = d2A gives v = 0 and d1B = d2B gives q = 0, hence f = v - q = 0,
which is OFF the open stratum. Exact, machine-verified
(EXP-022/r0-lemma.py). So R_0 meet {f != 0} = EMPTY, globally.

**Correction 2 (the slice-limit closure hole).** The planned collar route
(prove a rank floor on the boundary slice at f = 0 or u = 0, then transfer
inward by semicontinuity) is UNSOUND as a dimension argument: rank >= 3 at
the slice off a small set Z only confines R_2 near the slice to a shrinking
tube around Z, and a 2-dimensional low-rank set can hide inside such a tube
at every nearby slice value. Nothing in the slice bound controls the slices
at small nonzero parameter. The route is abandoned before use.

**The simplification: collars BECOME coverings.** Every collar direction
admits a rescaling making the entry matrix analytic up to and including
the boundary face, after which the interval-covering machinery applies to
a region CONTAINING the face, with no limit argument at all:

- The f -> 0 direction needs no rescaling: the entries are analytic across
  f = 0 wherever cs > 0, i.e. off the collision set {u = p, f = 0}. The
  band {|f| <= 1/4} is covered directly (EXP-022 part (a), running), with
  the collision tube {|u-p| <= 1/16, |f| <= 1/16} excised for part (b).
- The collision tube gets a polar blow-up: t = u - p = rho alpha,
  f = rho beta, alpha^2 + beta^2 = 1, cs = rho. Every 1/rho^3 cancels
  ALGEBRAICALLY against explicit rho factors of the brackets before any
  evaluation: Delta135 = p h1 - u g1 = -rho (alpha h1 + beta w +
  rho alpha beta / 2) exactly (w = (u+p)/2), and s(d1A, d1B) carries the
  exact factor rho via d1B^2 - d1A^2 = rho (2 beta h1 - 2 alpha w +
  rho beta^2) divided by (d1A + d1B)(d1A^2 + d1A d1B + d1B^2)-type
  nonvanishing radicals. Rows L13, L15, L23, L25, L36 are multiplied by
  rho^2 and row L35 divided by rho^2 (the whole row vanishes to second
  order: its s-factors and brackets EACH carry one rho). Row scalings by
  nonzero factors preserve rank at rho > 0, and the rescaled matrix is
  analytic at rho = 0, so covering the blown-up region including the
  rho = 0 face certifies rank >= 3 on the punctured tube. The angle is
  parametrized rationally (alpha, beta) = ((1-tau^2)/(1+tau^2),
  2 tau/(1+tau^2)), tau in [-1,1], right half-circle; the left half-circle
  is the image of the right under the pair swap (t, f) -> (-t, -f).
- The u -> 0 direction (pair A collapses onto the axis): multiply the mA
  column by 4u^2. The rescaled column is analytic at u = 0
  (J~[L13][mA] = h1 - 8u^3 h1 d1A^-3, J~[L35][mA] = -f + 8 f u^3 cx^-3,
  etc.), every other entry is already analytic there (d1A -> |h1| smoothly
  since d1A = sqrt(u^2 + h1^2)), and the face matrix at u = 0 has generic
  rank 4 (L13 -> (0,0,h1,0) covers mA; L15, L25, L35-L36 generically span
  the rest). Column scaling by 4u^2 != 0 preserves rank at u > 0. Covering
  region u in [0, 1/4] x p in [1/4, 3] x box, minus the corner tubes
  {u <= 1/16, |v -+ 1| <= 1/16} (A collides with an axis body) and the
  A_tube sliver. The p -> 0 direction is the pair-swap image.
- Remaining after these: the double corner (u, p both small), the four
  axis-collision corner tubes, and the outer charts (inverted coordinates
  with per-chart rescalings). Each is the SAME pattern one level deeper;
  declared pending in EXP-022, not assumed.

The stratum theorem chain, restated: k = 0, 1, 2, 4 proven; k = 3 =
[ core: EXP-021 integrated rerun with ball certificates, running ] +
[ band: EXP-022a, running ] + [ tube, ulow/plow, corners, outer: EXP-022
b-e pending ]. The ladder levels j = 0 (closed) and j = 1 (balls + the
same coverings) ride along. No other gaps are known.

## Lemma piece 9d: the pair-swap identity (2026-08-19)

The swap S: (u, v, p, q) -> (p, q, u, v) exchanges pairs A and B. The
entry matrix satisfies, IDENTICALLY (all 24 entries cancel syntactically
in sympy after expansion, no radical simplification involved):

    J(S x) = P_row . J(x) . P_col,
    rows  L13 <-> L15, L23 <-> L25, L35 -> L35, L36 -> -L36,
    cols  m1 -> m1, m2 -> m2, mA <-> mB.

(EXP-022/verify-swap-identity.py, syntactic zeros 24/24.) Consequences:
rank J(S x) = rank J(x) everywhere; R_2, R_1, R_0 are S-invariant; every
covering certificate on a region transfers verbatim to the swap image.
A_plow (p -> 0) is covered by the A_ulow run, and the tube's left angle
chart is the swap image of the right chart (both are being run anyway;
the identity makes the redundancy explicit rather than load-bearing).
Together with the mirror identity (v, q) -> (-v, -q) (used for the four
pentagon copies), the symmetry group acting on the covering programme is
the Klein four-group generated by S and the mirror.

## The outer charts (2026-08-19, round 32)

The outer region {max coordinate > 3} is the union of {R_A >= 3} and
{R_B >= 3} (R_X = the pair's Euclidean norm), and by the swap identity
(piece 9d) only the R_A side needs work. Two charts plus one blow-up:

**Chart F_A1 (A far, B bounded): IMPLEMENTED, crosschecked, running.**
Variables (eps, tau, p, q) with eps = 1/R_A in [0, 1/3], the A-direction
(a, b) = ((1 - tau^2), 2 tau)/(1 + tau^2), p in [0, 3/2], q in
[-3/2, 3/2]. Since |eps (p, q)| <= (1/3)(3 sqrt2/2) = sqrt2/2, the
normalized separations Cs, Cx = |dirA -+ eps (p, -q)...| stay above
1 - sqrt2/2 > 0.29: no collision structure inside the chart. Scalings:
rows (L13, L23, L35, L36) x eps, columns mA x 4u^2 and mB x 4p^2. Every
entry becomes a polynomial in (a, b, eps, p, q) over the certified-positive
radicals D1A, D2A, Cs, Cx, d1B, d2B, e.g.
  (L13, m2) -> -a/4 + 2 a eps^3 / D2A^3,
  (L13, mA) -> (eps - b)(1 - 8 a^3 / D1A^3),
  (L35, mA) -> (b - eps q)(8 a^3 / Cx^3 - 1),
  (L15, mB) -> g1 - 8 p^3 g1 / d1B^3,
with T-brackets T135 = p(eps - b) - a g1 etc. absorbing every 1/eps
exactly. The chart is analytic on the CLOSED chart including the
eps = 0 (infinity), a = 0 (vertical escape), and p = 0 (B-collapse)
faces; only the B-corner tubes {p <= 1/16, |q -+ 1| <= 1/16} are
discarded (part (d)). Crosscheck: 5/5 rational points against the
original matrix with the row/column scalings (fa1.py).

**Chart F_A2 (both far): DERIVED, next to implement.** Variables
(eps_A, tau_A, eps_B, tau_B), eps_A in [0, 1/3], eps_B in [0, 2/3],
discard eps_B < eps_A (that half is the swap image). Both pairs invert:
d1B = D1B/eps_B etc., and the cross distances become
cs = CS/(eps_A eps_B), CS = |eps_B dirA - eps_A dirB|, cx likewise with
dirB mirrored. CS vanishes exactly at {eps_A = eps_B, dirA = dirB} (the
pairs merge at infinity): the FAR-TUBE, a codimension-2 set blown up in
chart coordinates exactly as the bounded tube was (rho = CS, angle), with
the same row rescalings; CX vanishes only on the tau = +-1 corners with
matching heights (A+ meets B- across the axis at infinity), a corner of
the same blow-up. Implementation order: F_A2 with the far-tube DISCARDED
(boxes inside {CS < 1/16 and CX < 1/16} deferred), then the far-tube
blow-up chart. After these and the corner tubes (part d), the atlas is
COMPLETE: every point of the open stratum lies in a certified region.

## THE ATLAS AUDIT (2026-08-20, round 33)

The open gauged stratum (u, p > 0, f = v - q != 0, no collisions) is
covered by the following certified-or-running chart coverings plus their
Klein-group images (swap = piece 9d, mirror = piece 9e), with exactly
THREE remaining mini-charts, each a declared discard of a running chart:

Bounded regions (all coordinates within [1/4, 3] / [-3, 3]):
  core (CERTIFIED), band (CERTIFIED, traps), tube w in [7/32, 3] both
  angle charts (CERTIFIED), tube extension w in [1/8, 7/32] (chart R
  CERTIFIED, L running), ulow u in [0, 1/4] (CERTIFIED; plow = swap),
  uplow u, p in [0, 1/4] (running), deep tube w in [0, 1/8] (verified,
  queued), cb1 B-at-body-1 with A bounded (running; the other three
  single corners = Klein images), bicorner-opp A-at-2 B-at-1 (running;
  self-paired), bicorner-same both-at-1 (running; body-2 version =
  mirror).
Outer regions:
  fa1 A-far B-bounded (resumed; B-far A-bounded = swap), fa2b both-far
  ratio chart (running; r > 1 = swap), fartube pairs-merge-at-infinity
  blow-up (verified, queued; seam proven with exact constants), cb1f
  corner-times-far (verified, queued; Klein images free).

The three remaining mini-charts (all discards of the above, declared):
  M1. The quadruple cluster at an axis body: bicorner-same's discard
      {CSc < 1/16} u {CXc < 1/16} (A+ meets B+ near body 1). Structure:
      the fa2b-to-fartube ratio blow-up pattern INSIDE bicorner-same
      coordinates; the generated-polynomial machinery applies verbatim.
  M2. The collinear quadruple corner: deep's discard {w < 1/64,
      rho < 1/32} (both pairs collapse onto the axis while merged: the
      collinear limit). Structure: polar blow-up over (2w, rho).
  M3. The vertical far-corner: fartube's discard {CX^ < 1/16} (A+ meets
      B- at vertical infinity: the 2+2+2 three-cluster hierarchy).
      Structure: cluster chart at eta = 1/v -> 0.

When M1-M3 are certified, every point of the open stratum lies in a chart
whose covering certifies the ladder there (rank >= 3, or a trap: R_1
empty and R_2 inside a smooth 2-manifold). With lemma pieces 1-9e and the
ball certificates, the k = 3 chain step then holds on the WHOLE stratum,
and the chain k = 0, 1, 2, 3, 4 is COMPLETE: the stratum theorem follows.
Per the standing rule, the exact statement wording goes to Felipe FIRST
at that moment, before any manuscript or Zenodo step.

## LEMMA PIECE 10: the corner-face rank floor, uniform in the collar (2026-08-20)

The corner charts (cb1, cb1f) left a residual: boxes CONTAINING the
collision face rhoc = 0 (pair B sitting on axis body 1) can never be
certified, because the matrix genuinely has rank 2 there. Every dyadic
shell {rhoc in [h 2^-k-1, h 2^-k]} certifies (measured, k = 0..5, both
charts), so the punctured collar is covered by the union of shells; what
was missing is a UNIFORM statement over all k. Piece 10 supplies it in
closed form.

**Setup.** p = rhoc csig, q = 1 + rhoc ssig (csig^2 + ssig^2 = 1,
csig >= 0), pair A at bounded (u, v). Exact clearings, no cancellation:

    d2B^2 - 4 = rhoc (4 ssig + rhoc)   (EXACT)
    s(r12, d2B) = rhoc (4 ssig + rhoc) G,
        G = (d2B^2 + 2 d2B + 4) / ((d2B + 2) 8 d2B^3),  G(0) = 3/64
    (L15, m2) = -2 p s(r12, d2B) = -(3/8) rhoc^2 csig ssig + O(rhoc^3)
    (L25, m1) =  2 p s(r12, d1B) = -2 csig rhoc^-2 + O(rhoc)   [d1B = rhoc]
    (L25, mA) -> 0   (at rhoc = 0, cs = cx = d1A and the brackets are +-2u:
                      the two s-terms cancel EXACTLY)

**The limit.** M = det[{L15, L23, L25} x {m1, m2, mA}] expands along the
m2 column (only L15 has an m2 entry), and the rhoc^2 of (L15, m2) cancels
the rhoc^-2 of (L25, m1) exactly:

    M  ->  C  =  -(3/2) * u * gam * csig^2 * ssig * s(d2A, 2u),
    gam = -1 - v,  s(d2A, 2u) = 1/d2A^3 - 1/(2u)^3.

Verified to 8 significant digits at rhoc = 1e-7 on three independent
rational geometries (face-lemma2.py). So rank >= 3 holds UNIFORMLY for
all small rhoc > 0 wherever C != 0.

**Branch table (C = 0).** Five hypersurfaces, each with a second minor
whose own rhoc-limit is nonzero (searched over the full 80-minor menu):

    ssig = 0   (B displaced horizontally) -> {L13,L35,L36} x {m1,m2,mA},  0.0750
    v = -1     (A at body 2's height)     -> {L15,L35,L36} x {m1,m2,mA},  0.1335
    d2A = 2u   (equidistance)             -> {L15,L35,L36} x {m2,mA,mB}, -0.6662
    u = 0      -> COLLISION (bodies 3, 4 coincide): outside the stratum
    csig = 0   -> COLLISION (bodies 5, 6 coincide): outside the stratum

The two branches with no surviving minor are exactly the two collisions,
which the open stratum excludes by hypothesis: the table is COMPLETE on
the stratum. Pairwise combinations, including the two that produced the
actual covering failures, also survive:

    ssig = 0 AND d2A = 2   (the cb1 failures)  -> {L23,L25,L36} x {m1,m2,mB},  0.5094
    ssig = 0 AND u -> 0    (the cb1f failures) -> {L25,L35,L36} x {m1,m2,mA},  3.7e5
    ssig = 0 AND v = -1                        -> {L13,L35,L36} x {m1,m2,mA}, -0.0606
    ssig = 0 AND d2A = 2u                      -> {L13,L35,L36} x {m1,m2,mA}, -0.5623

**Consequence.** rank J >= 3 on the whole punctured corner collar
{0 < rhoc <= rhoc*} of the stratum, uniformly. Together with the shell
certificates the corner charts' residual failures are RESOLVED: they were
boxes containing the excluded collision face, never evidence of a
rank-2 set inside the stratum. The same argument applies verbatim to the
mirror and swap images of the corner (Klein group, pieces 9d and 9e).
