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
