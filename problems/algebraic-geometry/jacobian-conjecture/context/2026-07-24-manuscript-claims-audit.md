# Manuscript claims audit (2026-07-24)

Directive: no fake or invalid statement may persist in the published record. All
three manuscripts audited claim-by-claim against the experiment verdicts.

## Paper B (planar) - TWO invalid statements found and corrected

1. **The finite-ceiling / decision-procedure claim (v0.09, v0.10).** Asserted the
   truncation tower has a computable finite ceiling (the Krylov-closure dimension),
   hence the campaign is a finite decision procedure. INVALID: the derivation
   presupposes termination of the pinned corrector ladder, which EXP-064 measured
   to FAIL (chain stabilizes nonzero at dim 39). No a priori bound exists.
   ACTION: withdrawn in text (v0.11), replaced by what survives (upward-closedness
   of the feasible-degree set, d0 >= 3; the one-sidedness of support sweeps).

2. **The "obstruction moves with the degree" claim (v0.09 - v0.11).** Asserted the
   obstruction migrates (diagonal at degree 1, "a mixed support" at degree 2).
   INVALID: that reading came from EXP-070, which is RETRACTED (int(Fraction)
   truncation bug). The SOUND degree-2 result (EXP-072) obstructs at the triple
   support {(0,1),(1,0),(3,5)}, which CONTAINS TWO of the eight degree-1 blockers,
   and EXP-072's verdict states the degree-1 pattern PERSISTS. ACTION: corrected
   in text (v0.12): the obstruction persists; what grows is the support size
   needed to expose it. The dependent "Stokes phenomenon / obstruction's motion"
   phrasing in the flat-connection lead was rewritten accordingly.

## Paper A (foundational) - no invalid statements found
Claims checked against EXP-005/006/010/011/012 records (2D obstruction, rigidity,
real fiber census, weighted landscape/uniqueness). Consistent.

## Paper C (cascade) - no invalid statements found
Claims checked against EXP-016/018/041: the cascade corollaries (GMC false at some
finite dimension; Zhao vanishing; Image conjecture), the explicit dimension-48
witness (homogeneous Hessian-nilpotent quartic, 382 monomials over Q(i), exact
two-point collision), and the Thompson nilpotency-index correction (18, not 17).
All match the verdicts.

## Standing rule reinforced
Both defects were CLAIM-LEVEL readings that outran their evidence, and both were
caught by scrutiny rather than by a failing computation. Any narrative sentence
("the obstruction moves", "the campaign is a decision procedure") must be traced
to a verdict before it enters a manuscript; retracted experiments must be swept
for downstream narrative dependencies, not just for their headline result.
