# GGHV outreach draft - APPROVED BY FELIPE, ready to send from his email (2026-07-23)

To: the authors of arXiv:2204.14178 (Guccione, Guccione, Horruitiner, Valqui)
Subject: Machine certificates for the (72,108) reduced systems of your Prop. 4.3

Dear Professors Guccione, Guccione, Horruitiner and Valqui,

Your paper (arXiv:2204.14178) leaves one case below 125 open, remarking that with
enough computing power the bound could be raised from 108 to 125. We have been
attacking exactly that case by machine, building directly on your Proposition 4.3:
we transcribed the reduced systems ([P,Q] = x^2 on the small Newton polygons of
your three branches, verified against your LaTeX sources) and computed exact
left-null certificates (cleared covectors with polynomial identity verification,
sympy over Q and Q(t)) showing inconsistency across the forced-edge families:

- cases a/b: certificates with monomial pairings on two normalization charts of the
  forced R-squared right edge, with vanishing loci excluded by your own vertex
  forcing;
- case c: the forced top edge parameter normalizes to 1 by a torus gauge (verified
  concretely), and the certificates pair to nonzero monomials; the degenerate
  corner is covered separately;
- interior coefficients: complete axis-symbolic sweeps over every interior lattice
  point of both polygon families (each coefficient fully symbolic with the others
  sampled), all with nonzero constant pairings, plus dense mixed-direction
  sampling.

Stated carefully: this is strong machine evidence toward the closure of (72,108),
not yet a complete proof; the remaining step on our side is a
simultaneous-in-all-coefficients certificate (a termination computation for a
corrector ladder whose all-orders solvability we have proved). Every script,
artifact and verdict is public in the repository
github.com/fsantibanezleal/CAOS_RESEARCH (problem folder
algebraic-geometry/jacobian-conjecture, experiments EXP-052 through EXP-066,
including an adversarial audit of our own chain). We would be glad to share
anything in a form convenient to you, and would very much welcome your scrutiny:
if the certificates withstand it, the missing case closes and your bound rises to
125 as you anticipated.

With admiration for your program,
Felipe Santibanez-Leal
fsantibanez@gmail.com - github.com/fsantibanezleal
