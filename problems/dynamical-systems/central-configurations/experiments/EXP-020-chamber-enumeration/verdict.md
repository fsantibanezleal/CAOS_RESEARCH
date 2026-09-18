# EXP-020 - Verdict: THE FREE-ATOM CHAMBER RELAXATION DOES NOT CLOSE k = 3 (2026-08-03; 125,097,984 residual assignments over 24 orientation chambers; the geometric couplings are essential, with the first coupling identified in closed form)

Runner: the GF(2) inclusion-exclusion count (exact; 256 affine-system ranks
per orientation chamber; artifacts/residual-count.json). Term tables from
the machine-verified dossier closed forms (term counts: six conditions
with 3 terms, two with 5).

## Outcome

Over the SOUND free-atom superset (22 s-ordering atoms and up to 4 bracket
atoms unconstrained except the sum-bracket forcings), every one of the 24
feasible orientation chambers retains residual assignments, totalling
125,097,984. The hoped-for empty residual did not occur, and by a wide
margin: sign combinatorics of the eight conditions ALONE cannot exclude
rank <= 2; the conclusion is measured, not guessed.

## The load-bearing reading

The relaxation discards exactly what matters: the s-ordering atoms are not
free in reality, they are FUNCTIONS of the geometry, coupled to the
orientation atoms and to each other. First coupling in closed form:
s(d1A, wA) has the sign of 4u^2 - d1A^2 = 3u^2 - h1^2, so this s-atom is
DETERMINED by the comparison |h1| vs sqrt(3) u, a new semialgebraic atom
linking heights to widths. Analogous couplings exist for every s-atom
(each distance is an explicit sqrt of coordinates), and the cs < cx chain
plus triangle-type inequalities bind the rest. The coupled chamber
program (v2) is therefore a semialgebraic satisfiability question over
the COORDINATE atoms, not a parity question over free signs: the right
tool is CAD-flavored case analysis on the six coordinates, or the
per-residual-family witness/impossibility technique that closed k = 1
and k = 2.

## Honest scoreboard impact

Unchanged: k = 0, 1, 2, 4 PROVEN; k = 3 open at its last half-step. What
this experiment adds is the measured knowledge that the last step
genuinely requires the geometric content (couplings or pull-back
factorization), closing off the cheapest imaginable route. Routes still
open, in cost order: (i) coupled chambers v2 with the closed-form
coupling atoms; (ii) the norm-elimination pull-back with capped
factorization (Route A, one prior attempt lost to session teardown before
saving); (iii) a second-condition properness proof on a per-component
basis after an irreducibility analysis of ONE condition's zero locus.
