# Scoping: the reflection-symmetric strata of planar n = 6 (CCB-036 stage 2)

Written 2026-08-01, after the Dias-Pan full read (same-day dossier). Purpose:
enumerate the reflection-symmetric types of the planar six-body problem, record
which are closed and by whom, size the open ones in quotient variables, and
rank them as candidate Dias-Pan-style closures for our instruments.

## 1. The ladder (reflection symmetry: k bodies ON the axis, p mirror pairs, k + 2p = 6)

| Type | Geometry | Status | Source / note |
|---|---|---|---|
| k = 6, p = 0 | collinear | CLOSED for ALL masses (n!/2 = 360 labeled classes; finiteness classical) | Moulton 1910 [V: primary read] |
| k = 4, p = 1 | CROSS: four on the axis, one mirror pair (m5 = m6 forced) | CLOSED generically (proper closed exceptional mass set; statement misprints "open") | Dias-Pan arXiv:1811.08681 [V: read in full 2026-08-01] |
| k = 2, p = 2 | two on the axis, two mirror pairs | OPEN as far as we can verify: two targeted searches on 2026-08-01 surfaced no closure | [U: absence of evidence only; one unexamined hit arXiv:2004.08437 remains to be checked] |
| k = 0, p = 3 | three mirror pairs, nobody on the axis | OPEN as far as we can verify (same searches) | [U: same caveat] |

Beyond reflections: rotational types (central symmetry, C3, twisted regular
polygons per Yu-Zhang 2012) and the fully asymmetric bulk are NOT in this
ladder; the general n = 6 problem is Chang-Chen's programme (24 residual
zw-diagrams by our arithmetic). Montaldi (Dias-Pan's [20]) guarantees
EXISTENCE per symmetry type and mass choice, so none of these strata is
vacuous.

## 2. Quotient sizes (why these are n-4-to-5-scale, not n-6-scale)

Independent mutual distances after the reflection identification (mirror-pair
members share distances to every on-axis body; pair-pair distances collapse to
a same-side and a cross-side value):

- k = 2, p = 2: axis-axis 1; axis-to-pair 2 x 2 = 4; within-pair 2; pair-pair
  2 (same-side + cross). TOTAL 9 distance unknowns (vs 15 unrestricted), plus
  shape equations of Dias-Pan (2.2) type (Pythagoras + collinearity from the
  symmetric frame) and the mass-linear reduced Laura-Andoyer block. Mass
  unknowns after the forced pair-equalities: 4 (two axis + two pairs),
  projectivized 3.
- k = 0, p = 3: within-pair 3; pair-pair same-side 3 + cross-side 3. TOTAL 9
  distance unknowns; masses 3 after pair-equalities, projectivized 2.

Both sit between our n = 4 systems (6 distances) and n = 5 systems (10
distances): the Dias-Pan pipeline (shape variety dimension; mass-linear
Jacobian rank off determinantal loci; partial-GB bounds where full GBs wall;
one explicit witness with an exact rank certificate) is exactly EXP-011's
toolkit at comparable size. The pair-equality lemmas (m_i = m_j per mirror
pair) need the Laura-Andoyer Delta-relation argument of their Prop. 3.1 per
type; these are short exact computations, not new theory.

## 3. Ranked next steps (gated, no spend before EXP-011's verdict)

1. Check the unexamined search hit (arXiv:2004.08437) and one dedicated pass
   for "stacked" or "double pair" six-body results before ANY build (novelty
   pass, methodology).
2. k = 2, p = 2 first: it strictly contains richer geometry (two independent
   pairs interacting with two axis bodies) and its 9-variable quotient is the
   direct sibling of the CROSS case's setup; a closure here would be the
   second-ever symmetric n = 6 stratum theorem if the novelty pass holds.
3. k = 0, p = 3 second: smaller mass space (projectivized 2), likely easier,
   but also likely nearer to existing "three pairs" literature; novelty pass
   decides.
4. The witness sub-rungs reuse the Dias-Pan Section 5 pattern (eliminate to a
   one-variable eliminant, Sturm-isolate, extend): our census_positive +
   CRootOf machinery does this exactly, without truncation arguments.

## 4. Honesty

- The OPEN statuses in Section 1 rest on two recorded searches (2026-08-01),
  not on a systematic review; MathSciNet/zbMATH were not queried. The novelty
  pass in Section 3 is mandatory before any claim of newness.
- Nothing here is a run; no hypothesis is declared for these strata yet. This
  dossier only sizes and ranks. EXP-011's verdict decides whether the toolkit
  is ready for a stratum campaign.
