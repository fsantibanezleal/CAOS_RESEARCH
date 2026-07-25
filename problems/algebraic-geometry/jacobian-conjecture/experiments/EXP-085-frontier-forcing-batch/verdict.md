# EXP-085 - Verdict: GGV Remark 7.9 sourced; the frontier exclusions now hinge on one precise question

**Status: one of the two blocking sources OBTAINED. Partition sharpened; the
remaining gap is now a single, precisely stated question.**

Preflight (methodology/12): P1 satisfied (the remark was mined from a source we
already held on disk, E:\_Temp\ggv-sources\1401\src.tex, before any computation).
P4: matching a remark case EXCLUDES a config; not matching proves nothing.
P6: minutes, no long run; kill criterion = stop at an unsourced link, do not guess.

## What was obtained [VERIFIED, arXiv:1401.1784 source, the "GGV Remark 7.9" that
GGV2's closing remark cites]

Definitions: B_0 := (1/m) st_{1,0}(P) and B_1 := (1/m) en_{1,0}(P).

For B <= 50 the remark states (without proof, as the authors note):
a) A_0 lies in an explicit 23-element set X = {(4,12),(5,20),(6,15),(6,30),
   (7,21),(7,35),(7,42),(8,24),(8,28),(9,21),(9,24),(9,36),(10,25),(10,30),
   (10,40),(11,33),(12,28),(12,30),(12,33),(12,36),(14,35),(15,35),(18,30)}.
b) B_0 in X, or B_0 = (8,40) with A_0 = (4,12).
c) B_1 in X or B_1 in {(8,32),(8,40),(6,18),(6,24),(6,36),(6,42),(9,27)}, with
   the forcings:
     - B_1 = (8,32)     => B_0 = (8,28)
     - B_1 = (8,40)     => B_0 = B_1 or B_0 = (8,28)
     - B_1 = (6,18+6k)  => B_0 = (6,15)
     - B_1 = (9,27)     => B_0 = (9,21) or B_0 = (9,24)
The remark also records that a) and b) coincide with Heitmann Thm 2.24(1) under
the transposition B_0 = (E_1,D_1) written as (D_1,E_1), while list c) is STRICTLY
LARGER than Heitmann's, adding {(6,18),(6,24),(6,36),(6,42),(9,27)}.

## Effect on our frontier partition

- The GGV2 exclusions are stated in terms of the PAIR (B_0, B_1), not A_0:
  (6,15)/(6,18+6k) with 18+6k not a multiple of 30; (8,28)/(8,40); (9,21)/(9,27).
  Note that by c) the condition B_1 = (6,18+6k) ALREADY forces B_0 = (6,15), so
  that exclusion is governed entirely by B_1.
- **C19, C20** (our table lists A_0 = (6,15)): these are excluded IF their B_1 is
  of the form (6, 18+6k) with 18+6k not a multiple of 30. Our transcribed table
  does not carry B_1 for these rows. GAP: obtain B_1 per configuration (the GGHV17
  section-5/6 tables), then apply the divisibility test. This is now a pure
  table-lookup question, not a derivation.
- **C10, C11** (A_0 = (7,21)): GGV2 states that Heitmann's infinite families
  (5k+3,3k+2) and (4k+3,k+1), "corresponding to A_0 = (7,21)", come from
  A_0' = (2,1), which is impossible. The remaining question is EXACTLY: does
  A_0 = (7,21) force A_0' = (2,1) in general, or only within those two families?
  If in general, C10 and C11 are both EXCLUDED. GAP: Heitmann Thm 2.25 (the family
  parameterisation) or an independent forcing derivation.
- **C13** stays excluded (EXP-082): its chain is the (8,28)/(8,40) case verbatim.

## Net
Frontier status: 1 confirmed excluded (C13); 4 strong candidates (C10, C11, C19,
C20) reduced from "reconcile two different A_0' notions" to two crisp, finite
questions: (i) the B_1 values of C19/C20, a table lookup; (ii) whether A_0=(7,21)
forces A_0'=(2,1) generally, one statement from Heitmann Thm 2.25. Neither needs
machine time. If both resolve affirmatively, FIVE of the twenty-four [125,150]
configurations collapse, leaving C01 and C04 as the only printed-open family cases
plus the 16 unprinted-A_0' sporadics.
