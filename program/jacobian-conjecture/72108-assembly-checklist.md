# The (72, 108) closure: assembly checklist (2026-07-22, session 32 prep)

Source: context/2026-07-22-gghv-72108-dossier.md (verified against the LaTeX sources).
This checklist maps what a FULL closure of the open case requires, so the corrector
ladder's success (EXP-055/056, in flight) plugs into a complete argument.

## What our stratum covers

The forced-top-edge stratum on the REDUCED polygons: P with top edge y^8 (xy - t)^8
(t symbolic), all lower lattice-point coefficients (first-order universality proved;
ladder continuing), target [P, Q] = x^2, Q on the full reduced N(Q).

## The remaining forcing branches (from the dossier's Prop 4.3 pipeline)

1. THE EDGE NORMALIZATION: the dossier's forced forms are l_{1,-2}(P) =
   lambda (z - lambda1)^{8m} and the edge form y (x^4 y - alpha)^7 (with the q = 4
   forcing and the Prop 8.2 dichotomy k = 1, plus the inversion x -> x^{-1},
   y -> x^4 y). VERIFY: our y^8 (xy - t)^8 stratum is the correct image of their
   forced edge under the stated inversion and scaling; if the exact reduced-edge shape
   differs (e.g. multiplicity split (z - a)(z - b)... instead of an 8th power), the
   ladder must be re-run on the corrected stratum (cheap: same instruments).
2. THE OPTIONAL CORNERS: N(P) with/without (0, 8) and N(Q) with/without (0, 12) (the
   dossier brackets them). Our polygons INCLUDED both; the sub-polygon cases are
   subsets of the swept coefficient space (coefficients = 0), covered if the ladder's
   universality includes zero values (it does: polynomial identities).
3. THE Q-SIDE FORCING: the dossier's N(Q) chain (2,1), (12,21), (12,24): our Q ranged
   over the FULL reduced polygon (no forcing imposed): our certificates are therefore
   STRONGER than needed (any forced Q-subfamily is a subset). No extra work.
4. THE BRACKET CONSTANT: Prop 4.3 fixes [P, Q] = x^2 exactly (not a general scalar
   multiple); a scalar c x^2 rescales Q: covered by linearity. No extra work.
5. THE ORIENTATION: (72, 108) vs (108, 72): the reduction is stated for one
   orientation; the other is the transpose under the same pipeline (dossier); confirm
   the polygons swap consistently (one more ladder run at most).
6. GGHV ASSEMBLY: cite their Prop 4.3 chain verbatim (the dossier carries it) to
   conclude: reduced-system emptiness => no (72, 108) counterexample => (with their
   Thm 2.1) any counterexample has max degree >= 125: THE FLOOR RISES TO 125.

## Publication note

The floor-raise assembles OUR machine closure with THEIR reduction: the honest claim is
"(72,108) is discarded, completing the GGHV program's missing case, conditional on
their Prop 4.3 as published"; the manuscript should state the division of labor
exactly, and Felipe validates before any submission or outreach.
