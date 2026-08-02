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
