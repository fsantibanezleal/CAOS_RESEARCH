# EXP-011 - Spatial Dziobek dimension at n = 5: the reshaped lane's first scaling test

Declared: 2026-08-01, BEFORE any run. Backlog: CCB-033 (reshaped by EXP-010's
verdict) + CCB-037 (first live use of the partial-GB instrument).

## Question

Does the upper-bound toolkit that survived EXP-010 (recorded-section emptiness
probes, cheap; partial-Groebner leading-term unions, deterministic) scale from
n = 4 (6 distance variables) to n = 5 spatial (10 distance variables), and does
it certify dim <= 4 for the spatial Dziobek cut, the value the generic
finiteness picture predicts (projectivized mass-space dimension for five
bodies)?

## The object, stated honestly as a CUT, not as the CC locus

D5 in the torus of the 10 mutual distances (Rabinowitsch t * prod r - 1), cut
by:

- the FIFTEEN cleared Dziobek product differences h_ijkl = S_ij S_kl -
  S_ik S_jl (S = r^-3 - 1) over all quadruples of {1..5}, five independent
  [V: HJ11 eq. (5); the n = 4 avatar of these equations is already
  machine-exercised in EXP-008/010], monomial factors stripped;
- the spatial Cayley-Menger equation: the 6x6 bordered determinant of the five
  points vanishes (embeddability in R^3) [V: HJ11 eq. (6)].

HONESTY UP FRONT: this cut is an OVERVARIETY of the spatial Dziobek central
configurations. The product equations characterize the rank-one factorization
S_ij = z_i z_j only where enough S-entries are nonzero; strata with many
vanishing S-entries satisfy all products degenerately (the same phenomenon as
EXP-001's dimension-blindness, one level up). The smoke gate DOCUMENTS this
with an exact point: the unit-side unit-slant bipyramid (all distances 1
except r45, with r45^2 = 8/3 forced by realizability) lies on the cut with all
products vanishing trivially. The dimension claim under test concerns the
WHOLE cut; an upper bound for the cut is automatically an upper bound for the
CC locus inside it, so the useful direction survives the overcutting.

## Predictions

- P1 (smoke gate, exact rational arithmetic only, before any solver time):
  (a) the unit bipyramid point (nine distances 1, r45^2 = 8/3) satisfies all
  fifteen stripped products AND the spatial Cayley-Menger equation exactly
  (both memberships are pure rational arithmetic since CM has only even powers
  of r45); (b) the all-ones point (five unit mutual distances = the 4-simplex)
  satisfies the products but NOT Cayley-Menger (five equidistant points need
  R^4); (c) a fixed rational-coordinate 5-point configuration in R^3 satisfies
  Cayley-Menger exactly but violates at least one product. Three-way
  discrimination as in EXP-010.
- P2 (emptiness at codimension 5, the dimension upper bound): TWO independent
  recorded random 5-section draws (integer coefficients from [-10^6, 10^6],
  seeded generator, seed 20260811) give EMPTY sectioned systems in msolve
  within 300 s each. Empty here = probabilistic-exact support for
  dim D5 <= 4.
- P3 (the cap-signature control at codimension 4): the same instrument at
  codimension 4 does NOT return empty: expected outcome is inconclusive-cap at
  300 s (a nonempty finite section whose census walls, the EXP-010 signature)
  or, if msolve surprises us, a nonempty census. A fast EMPTY at codimension 4
  would REFUTE dim = 4 downward (dim <= 3), contradict the Moeckel picture,
  and stop the lane for exact re-examination. This rung uses the cap as
  signal, not as failure.
- P4 (partial-GB deterministic bound, CCB-037 live): with the declared
  subideal menu (each subideal = one stripped product + Cayley-Menger + the
  Rabinowitsch equation; fifteen subideals; grevlex; 120 s subprocess cap per
  subideal), the UNION of leading monomials yields a staircase dimension bound
  d_pgb, recorded whatever it is. SUCCESS threshold declared in advance:
  d_pgb <= 4 would be a deterministic match of the expected dimension;
  d_pgb in {5..8} is an informative partial bound (menu too weak, recorded as
  such, pairs of products become the next menu); caps are inconclusive-cap
  per subideal, and the union over the completing subideals is still a valid
  bound (monotonicity: fewer leading terms only weakens, never falsifies).

## Preflight (methodology/12)

- Source-complete: HJ11 eq. (5) and (6) are [V] (author PDF read 2026-07-23,
  method dossier); the n = 4 avatars of both equation families are
  machine-exercised (EXP-008, EXP-010); the Dias-Pan partial-GB device was
  read in full 2026-08-01 (their Lemma 6.4 + 7.5; our dossier). No [U] premise
  anywhere in P1-P4.
- Smoke test: P1 is the gate; it costs under a minute and spends no solver
  time. The bipyramid membership uses only rational arithmetic (r45 appears in
  CM through r45^2 = 8/3; the products never see r45 alone... correction,
  h_ijkl with {4,5} split across products DO contain S45 linearly; at the
  bipyramid point every product term carries a vanishing S-factor, so the
  evaluation is still exact rational: S45 enters through r45^3, and r45^3 is
  NOT rational). RESOLUTION, declared now: evaluate the products at the
  bipyramid point as polynomials in w = r45 over Q, then reduce modulo
  w^2 - 8/3 (exact polynomial reduction, the EXP-010 pattern); acceptance is
  zero remainder. CM uses only w^2, so it reduces to pure rationals.
- One-sidedness check: every rung can refute. P2 nonempty (or fast-empty in
  P3) would each be major structural surprises demanding exact study; P4 can
  come back too weak, which is an honest instrument measurement; caps are
  recorded as caps.
- Invariant-first: the recorded invariants are the emptiness/cap signature
  per codimension and d_pgb; both are the lane's scaling forecasters for the
  n = 6 incidence step.
- Budget and kill criterion: worst case about 2 x 300 + 2 x 300 + 15 x 120 =
  3000 s. No cap extensions. If BOTH P2 draws cap (not empty, not decided),
  the emptiness instrument itself failed to scale and the verdict says so
  (CCB-034 witness sets then carry the whole lane). If the pgb worker caps on
  every subideal, P4 is inconclusive-cap and the menu was too expensive, also
  recorded.

## Consequence ladder

- P2 + P4 both land at <= 4: the lane is calibrated at n = 5 with two
  independent upper-bound instruments agreeing with the literature's expected
  dimension; the n = 6 incidence step (masses as variables) gets its design
  from the measured costs, and the manuscript gains the scaling section.
- P2 lands, P4 too weak: sections carry the lane probabilistically; the
  subideal menu is enriched (pairs, then products sharing three indices)
  before any n = 6 spend.
- Any refutation (P2 nonempty, P3 fast-empty, P1 failure): stop, verify
  exactly, treat as a finding about the equation set (the overvariety's
  degenerate strata are then not dimension-negligible, which would itself
  redirect the lane to enriched cuts).
