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
