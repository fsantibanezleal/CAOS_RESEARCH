# boij-soderberg-realizability history

## 2026-11-19 - opened

External status: Erman-Sam Questions 6.1 and 6.2 are answered negatively by the Rethlas paper (arXiv:2605.25259, still
v2 of 2026-05-28), with one primitive point each; no follow-up found in the external refresh of 2026-11-19 [V].
- Opened from the 2026-09-02 dossier and the portfolio review of 2026-11-19 (rank 1, decision 1; the 2026-10-30 order
  "open after hoa-mnh" is met).
- Thirteen arXiv sources and the two Rethlas raw outputs fetched to the data root with SHA-256 (the dossier's copies and
  its census scripts were under a temporary path that no longer exists).
- Toolchain checked: Macaulay2 1.22 in WSL; `pureBetti {0,4,9,10}` returns {1, 3, 8, 6}, `pureBetti {0,1,6,10}` returns
  {6, 8, 3, 1}, `pureAll {0,4,9,10}` returns (70, 70, 15).
- Plan: the realizability table of the 220 rays with d3 <= 12 (EXP-001: census, closures, random search), then U(H)
  toward the smallest counterexample to Question 6.1.

## 2026-11-19 - literature pass absorbed; EXP-001 and EXP-002 frozen

- Literature pass (four lanes, twelve items re-read by skeptics; [context note](../context/2026-11-19-literature-pass.md)):
  16 primitive points of the dossier's undecided list are realized by printed sources or by scaling (Macaulay2
  documentation outputs over ZZ/101; Soderberg's extremely compressed level modules); c_d = 2 on (0,4,9,10) and
  (0,1,6,10); over U(H) the Kostant modules L(p,q) of sp_4 realize eleven primitive points in characteristic 0;
  Boocher-Huang-Wolf (arXiv:2512.24320, December 2025) describe the rays with B1 = 2, of which (0,6,20,21) is the second.
  Four claimed items did not survive the skeptics (Pieri candidates, a purity reading of relatively compressed
  algebras, a tool limitation, a lane's reading of the gcd restriction).
- Derived by hand, before any machine run: U(H)/U(H)(x^2, y^2) has Hilbert function (1,2,2,2,1) and the pure resolution
  (1,2,2,1) of type (0,2,6,8) when 6 is invertible (written in the EXP-002 hypothesis).
- EXP-001 (the table over S) and EXP-002 (the three rays left open over U(H), the family U/U(x^e, y^e), calibration and
  duality) frozen before computation.

## 2026-11-19 - EXP-002 CONFIRMED: the three open rays are realized over U(H); a family for every e; characteristic 2

- EXP-002 (hypothesis ac4f4880): an exact U(H) library (`code/uhlib`: PBW arithmetic, graded quotients, Betti numbers by
  the Tor complex) and Singular Plural, calibrated on 17 modules including the 15 Kostant modules L(p,q), p <= 4. Over QQ:
  U/U(x^2, y^2) has Hilbert function (1,2,2,2,1) and the pure table (1,2,2,1) on (0,2,6,8), as derived by hand before the
  run; U/U(x^e, y^e) is pure of type (0,e,3e,4e) for e = 3..6; cokernels of random 2 by 3 matrices of quadrics are pure
  (2,3,3,2) on (0,2,10,12) (10 of 10, also lifted to QQ). So all ten parity-passing S-excluded rays with d3 <= 12 are
  realized over U(H) in characteristic 0.
- The pair (x^2, y^2) fails in characteristics 2 and 3 as predicted; in characteristic 3 other pairs work; in
  characteristic 2 none of 80 random pairs gives a finite quotient. Duality reverses Betti tables on 20 of 20 modules.
- Derived the same day [D], to be reviewed: the Hilbert series and the one-dimensional socle of U/U(x^e, y^e) for every e
  in characteristic 0 (context note), and that in characteristic 2 no pair of quadrics gives a finite length quotient,
  so (1,2,2,1) on (0,2,6,8) is realizable over neither ring there (EXP-002 verdict; EXP-003 next).

## 2026-11-19 - EXP-003 CONFIRMED: characteristic 2, the proof steps of the family, genericity; EXP-001 search state

- EXP-003 (hypothesis 8028f796): all 35 and 357 two-dimensional subspaces of U_2 over GF(2) and GF(4) (and 400 random ones
  over GF(16), GF(256)) give a quotient nonzero in every degree up to 20, each with the central quadric of the derivation.
  With the proof (x^2, y^2, z central in characteristic 2), the primitive point of (0,2,6,8) is realizable over neither S
  nor U(H) in characteristic 2: a counterexample to Question 6.1 with d3 = 8 there, on a ray realized over U(H) in every
  other characteristic.
- The derivation for U/U(x^e, y^e) is confirmed step by step for e <= 8 (weight pieces, kernel of y, socle, Hilbert
  series), with the k[z]-structure for e <= 5 and the bad primes for e <= 5 exactly as predicted. A general pair of forms
  of degree e is not pure for e = 4, 5, 10. The substitution of x^e, y^e in the presentation of L(1,1) is pure for
  e = 2, 3.
- Characteristic 2 searches: the rays (0,1,2a+1,2a+2), a <= 5, and (0,3,5,8) are realized; (0,3,9,12) and (0,2,10,12)
  are never of finite length (open, BSB-014).
- EXP-001: 189 primitive points realized over GF(32003) or by constructions, 12 excluded, 19 open (d3 >= 10); 76 of 76
  parity-failing rays with d3 <= 9 realized; 58 of 60 QQ rechecks passed, the rest running.

## 2026-11-19 - The two derivations reviewed: correct after minor fixes; the family is pure exactly for characteristic 0 or >= 2e

- An independent reader re-derived the derivation of U/U(x^e, y^e) (steps 1a to 1g) and the characteristic 2 statement,
  with its own computation (M_1 to M_5 over QQ, all 35 subspaces over GF(2) through degree 24, the primes up to 17 for
  e <= 7). No blocker, no major finding; 13 minor ones, all applied: the context note is rewritten (normal ordering
  proved, the column range of the scaling, the weights beyond e, the explicit last map of the resolution of the trivial
  module, the semilinear symmetry) and the EXP-003 verdict has addendum 1.
- New from the review: the converse. For every prime p <= 2e - 1 the module is nonzero in degree 4e - 2, so
  U/U(x^e, y^e) has the pure resolution of type (0, e, 3e, 4e) if and only if the characteristic is 0 or at least 2e
  (hook-content for the tableau counts; a zero column for the converse). Re-checked with `uhlib` for e <= 6, p <= 13.
- Positioning: arXiv:2605.25259 Theorem 3.7 already answers Question 6.1 negatively over every field (parity test on
  (0,6,20,21)); the result on (0,2,6,8) is the dependence of the answer on the characteristic. An explicit pair over
  GF(3) with the pure table is recorded (f = x^2 + y^2 + yx, g = x^2 + yx - z).

## 2026-11-19 - EXP-001 CONFIRMED: the table over S for d3 <= 12; no counterexample with d3 <= 9 in characteristic 0

- The search ended (no timeout): of 220 rays the primitive point is realized over S on 193, excluded on 12 (twice the
  primitive point is realized on each, so c_d = 2) and open on 15, all with d3 >= 10. c_d is determined on 205 rays.
- Rechecks: 130 hits recomputed in a fresh Macaulay2 process and in Singular, none fails; over QQ 64 pass, 2 fail (the
  integer lifts on (0,3,8,10) and (0,3,11,12)), 7 stop at the limit, 57 not run. The rechecks of (0,3,7,9), (0,4,7,9) and
  (0,4,8,9) were run by ray and pass; with duality every realized ray with d3 <= 9 is realized in characteristic 0 (79).
- With EXP-002 (the five excluded rays with d3 <= 9 are realized over U(H) in characteristic 0): Question 6.1 has no
  counterexample with d3 <= 9 in characteristic 0; (0,4,9,10) and (0,1,6,10) are counterexamples with d3 = 10 over every
  field (obstructions over S, parity over U(H)); the published one has d3 = 21. To be reviewed (BSB-015).
- Flags over small fields (stage 1e): a generic module is pure for some seed on 98, 126 and 130 of 130 generators over
  GF(2), GF(3) and GF(5).
- Prediction P1's count was wrong (78 points at stage 0, not 52 to 56: the second Eisenbud-Floystad-Weyman formula adds
  26 in characteristic 0); P4 fails on 2 of 66 completed rechecks.

## 2026-11-19 - Characteristic 2, the general statement [D]; EXP-004 frozen

- Derived (context note `2026-11-19-characteristic-two-general.md`, not yet reviewed): in characteristic 2, a module
  with a generators in degree 0 and at most a + 1 relations, all of one degree e >= 2, never has finite length over
  U(H). Route: U is free of rank 4 over the central ring k[x^2, y^2, z]; each parity of U is a module over the quadric
  t^2 + Z t + XY (t = left multiplication by yx), the even part free and the odd part a line bundle of bidegree (0,1);
  a finite length quotient would give a surjection O^b to L^a with L ample, impossible for b <= a + 1 by Chern classes.
- Consequences: the point (1,2,2,1) of (0, e, 3e, 4e) is realized over neither ring in characteristic 2 for every
  e >= 2, while U/U(x^e, y^e) realizes it in characteristic 0 for every e; the points of (0,3,9,12) and (0,2,10,12) are
  not realizable in characteristic 2 (BSB-014).
- The derivation predicts the eventual Hilbert function of a general presentation: 2 for two quadrics, 4 for two
  cubics, 6 for a 2 by 3 matrix of quadrics. The EXP-003 artifacts, read afterwards, show 2, 4 and 6.
- EXP-004 frozen (e11af1f2): rank certificates for the lift of the prime-field realizations of EXP-001 to
  characteristic 0, with a lemma on flat lifts of pure resolutions; the run is in progress.

## 2026-11-19 - The least-counterexample statement reviewed: correct after fixes

- An independent reader recomputed the evidence of all 84 rays with d3 <= 9: the formulas from the primary texts on 37
  rays, all 29 explicit modules over QQ in Singular (pure, with the Herzog-Kuhl lengths), Ext^3 duals over QQ on 12 of
  13 rays, two Kostant modules over U(H), and the two exclusions at d3 = 10 from Erman's Proposition 3.1. No case fails.
- Fixes applied in addendum 1 of the EXP-001 verdict: the direct-sum step for non-primitive points, the counts by
  evidence (35 + 2, 29 + 13, 5), how the modules over QQ are built (from the generator matrix, not from the lifted
  prime-field presentation), d3 - d0, and the attribution of the exclusion over S to Erman 2009.
- Open from the review: store the rational presentations and tables with the hits (BSB-019).

## 2026-11-19 - The general characteristic 2 statement reviewed: correct; BSB-019 closed

- An independent reader re-derived the four steps and found no error (5 minor, 7 notes; all applied in the note): the
  quadric is P^1 x P^1 over k itself, so no extension of the field is needed; the hypotheses e >= 2 and b <= a + 1 are
  both sharp; the eventual Hilbert function of a general presentation is (a(a+1)/2) L.L in every degree, by an
  argument of the reviewer for the other parity.
- Machine check with the reviewer's own code: no finite length module among all 651 two-dimensional spaces of cubics and
  all 35 of quadrics over GF(2), 720 random pairs of quartics and quintics over GF(2), GF(4), GF(16), and 60 matrices of
  2 by 3 cubics; eventual values 2, 4, 8, 12, 12 as predicted.
- The modules over QQ of the rays with d3 <= 9 are stored with the experiment: the reviewer's Singular scripts (each
  builds the module from the saved generator matrix) and their tables, with SHA-256 (`artifacts/qq-modules.json`).

## 2026-11-19 - EXP-004 CONFIRMED: rank certificates lift every prime-field realization to characteristic 0

- Gates: the ranks over GF(32003) reproduce the pure Hilbert function on 1,087 matrices of 130 hits; the rank test
  passes on the 64 known answers; python-flint and PARI/GP agree on 842 of 842 matrices.
- All 130 hits pass (one matrix by PARI/GP alone). With the lift lemma, all 193 realized rays are realized in
  characteristic 0 (147 before).
- The prediction that the two hits not pure over QQ in EXP-001 would fail was refuted: both pass. Recomputed over QQ in
  Singular with independent scripts: both are pure ((7,16,21,12) on (0,3,8,10), length 280; (6,11,27,22) on (0,3,11,12),
  length 396). The Macaulay2 results of EXP-001 on these two were false negatives; cause not established.
- The lemma is a derivation and awaits review (BSB-020) before the table of EXP-001 is restated.

## 2026-11-19 - The lift lemma reviewed: correct; 193 rays realized in characteristic 0

- An independent reader derived the lemma in both forms and found it correct (two minor additions to the proof). On all
  130 hits the prime-field rank is maximal in every needed degree, which forces the rational rank: the certificate
  needs no computation over QQ.
- The two rechecks that EXP-001 recorded as failures over QQ were runs cut short after about 110 s; the script recorded
  a run without a result line as a failure. Both modules are pure over QQ (Singular; the recheck script run to the end
  on one of them). Corrected in addenda of the EXP-001 and EXP-004 verdicts.
- The table over k[x,y,z]: 193 rays realized in characteristic 0, 12 excluded, 15 open.

## 2026-11-20 - First manuscript published: v0.01, 10.5281/zenodo.24385387

- `manuscripts/boij-soderberg-realizability/primitive-points-realizability`, 45 pages, concept 10.5281/zenodo.24385386; SHA-256 of the PDF
  `7075a70f90c6f81d774a5e9822a7c086a0f909162cb6599ebad22e7f80b3d2e6`.
- Before release: a review by a reader other than the writer (blockers on a generated table that printed another table,
  a field-scope count, an attribution and the description of two rechecks, all fixed), a closing check and a final
  confirmation; the release build has no warning and no overfull or underfull box; the 45 rendered pages were read.
- Records: governance (manuscript entry, EXP-001 to EXP-004 as its primary evidence, the success gate of BSR-F2 met), the
  map, RESUME, backlog BSB-013 done, state.

## 2026-11-20 - Strategic review: BSR-F2 closed, BSR-F3 current; EXP-005 and EXP-006 frozen

- BSR-F2 met its gate with the publication of v0.01. BSR-F3 is the current focus: the characteristic questions the
  manuscript leaves open, and the open rays.
- EXP-005 (frozen): the reviewers' machine checks of the characteristic 2 theorem and of the family at e = 6, 7, rerun
  with the repository's instrument and a second system, archived.
- EXP-006 (frozen): odd characteristic below 2e for e = 3 and 4. Derived before the run: at e = 3 the pure Hilbert
  function is the generic one; at e = 4 a pure pair must drop the rank of the multiplication map into degree 12 from 49
  to 48, and the class 300 sigma_2 + 325 sigma_(1,1) of that locus in Gr(2, 9) is not zero, so the locus is not empty
  and has dimension at least 12 in every characteristic.

## 2026-11-20 - EXP-005 CONFIRMED: the machine checks of the characteristic 2 theorem archived

- Four gates passed (the 35 known answers of EXP-003; two code paths on 160 presentations; Singular on 75 sampled
  Hilbert functions and on the 24 modules of the family; 13 unit tests).
- 0 finite length cases among 1,574 presentations with at most one more relation than generators in characteristic 2;
  the 1,372 that become constant all have the predicted value; over GF(2) 137 grow, over GF(4) 2, over GF(16) none.
  With one more relation 39 of 40 have finite length.
- U/U(x^e, y^e) at e = 6 and 7: pure exactly over QQ and for p >= 2e among the primes up to 31, two instruments.
- Re-check by the coordinating session without the experiment's routine: counts re-tallied, 16 cases recomputed, no
  finding. Raw outputs of the second instrument and the run log are under the data root.

## 2026-11-20 - EXP-006 CONFIRMED on its question: odd characteristic below 2e at e = 3 and 4

- Pure pairs of cubics over GF(3) (1,944 of the 11,011 spaces, exhaustive) and GF(5); pure pairs of quartics over
  GF(3), GF(5), GF(7); pure pairs of quintics over GF(3). Each sampled table confirmed by Singular (270 of 270), and
  60 spaces and the quoted pairs rebuilt by the coordinating session.
- So for e = 2, 3, 4 the point (1,2,2,1) of (0, e, 3e, 4e) is realized over U in every characteristic other than 2.
- Over GF(11) and GF(13), 217 pure spaces at e = 4 and none in the orbit of <x^4, y^4>.
- Refuted: the share of the rank condition (predicted near q^(-2), observed near 1/q). The derivation was wrong: the
  locus contains the resultant hypersurface. The review of the family-dimension note found the same independently.
- The family-dimension note is reviewed (correct after fixes): the pure pairs form a family of dimension at least
  4e - 4 through <x^e, y^e>. The review's tangent space computation and explicit pairs over QQ wait for an archived
  experiment (BSB-025).
- Found while checking the generator: the manifest table of the published v0.01 prints the hash of a CRLF working copy
  of one artifact (BSB-024).

