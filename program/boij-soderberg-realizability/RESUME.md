# boij-soderberg-realizability: RESUME (session handoff)

Updated 2026-11-20 (first manuscript published). First read for any session, per methodology 07. Derived view: experiment verdicts win.

## 1. State in one screen

Pure rays of the Boij-Soderberg cone in three variables are indexed by degree sequences d = (0,d1,d2,d3); their integral
points are the multiples m beta_d of the primitive Herzog-Kuhl point. Erman-Sam Question 6.1 asked whether every integral
point is realized by a finite length module over S = k[x,y,z] or over U(H) (Heisenberg, deg z = 2). Jiang, Li, Sun, Wang,
Xiao and Yu (the Rethlas paper, arXiv:2605.25259v2, Theorem 3.7) answered no with (0,6,20,21), beta (1,2,9,8): Krull over
S, parity p(-1) = 16 over U(H) [V].

What the programme has, all in the published manuscript v0.01 (section 5) and in the verdicts of EXP-001 to EXP-004:

- U/U(x^e, y^e) has the pure resolution of type (0, e, 3e, 4e) with table (1,2,2,1) if and only if the characteristic is
  0 or at least 2e [D, reviewed; MV for e <= 8].
- In characteristic 2 a module over U(H) with a generators and at most a + 1 relations, all of one degree e >= 2, never
  has finite length; so (1,2,2,1) on (0, e, 3e, 4e) is realized over neither ring there for every e >= 2, and (0,2,10,12)
  is excluded there [D, reviewed; MV on the observed cases].
- The ten rays with d3 <= 12 that pass the parity test and are excluded over S are realized over U(H) in characteristic 0
  [MV, two instruments].
- Over S, of the 220 rays with d3 <= 12 the primitive point is realized in characteristic 0 on 193, excluded on 12 (least
  multiple 2 on each) and open on 15, all with d3 >= 10 [MV; the last 46 rays through rank certificates and a reviewed
  lift lemma].
- In characteristic 0 no counterexample to Question 6.1 has d3 <= 9; (0,4,9,10) and its dual (0,1,6,10) are
  counterexamples with d3 = 10 over every field (the exclusion over S is Erman's, the half over U(H) is the parity test)
  [MV plus cited results, reviewed].

Open: the 15 rays, the odd characteristics below 2e, the substitution of x^e, y^e in the Kostant presentations (focus
BSR-F3, proposed).

## 2. The objects table

| Object | Definition / authority |
|---|---|
| degree sequence, pure ray | d = (0 < d1 < d2 < d3); the ray of Betti tables supported in degrees (i, d_i) (Eisenbud-Schreyer 2009) |
| primitive point beta_d | least integral point of the ray, proportional to (prod over j != i of \|d_i - d_j\|^-1) (Herzog-Kuhl 1984); Macaulay2 `pureBetti` |
| realizable over A | some finite length graded A-module has exactly that Betti table; depends on the field |
| c_d | least m with m beta_d realizable (Erman 2009, Section 7 question (2)) |
| U(H) | enveloping algebra of [x,y] = z, deg x = deg y = 1, deg z = 2; Hilbert series 1/((1-t)^2 (1-t^2)); cubic AS-regular algebra of dimension 3 |
| parity test | over U(H) a ray is realizable only if p(-1) = 0, p(t) = sum (-1)^i beta_i t^(d_i); scale invariant |
| duality | Ext^3(-, S) reverses Betti tables: d to (0, d3 - d2, d3 - d1, d3) |
| scaling | x to x^e is flat: (d, m beta) realizable implies (e d, m beta) realizable (dossier section 1.4) |
| dossier | [2026-09-02 dossier](../../problems/combinatorics/petersen-coloring/context/scouting-2026-09/2026-09-02-dossier-boij-soderberg-realizability.md) |

## 3. Experiment index

| Experiment | Question | Verdict | Load-bearing result |
|---|---|---|---|
| EXP-001-pure-ray-census | the d3 <= 12 table over S: census, obstructions at every m, closures, generic level modules and generic presentations over GF(32003), every hit rechecked in Singular and over QQ | CONFIRMED (2026-11-19) | over S, of 220 rays the primitive point is realized on 193 (147 in characteristic 0 by this experiment alone; all 193 after EXP-004, addendum 2 of the verdict), excluded on 12 (c_d = 2 on each) and open on 15, all with d3 >= 10; c_d determined on 205; every ray with d3 <= 9 is realized in characteristic 0 (79) or is one of five excluded parity-passing rays that U(H) realizes (EXP-002), so no counterexample to Question 6.1 has d3 <= 9 in characteristic 0, and (0,4,9,10), (0,1,6,10) are counterexamples with d3 = 10 over every field; 64 of 66 completed QQ rechecks pass |
| EXP-002-heisenberg-primitive-points | the three S-obstructed parity-passing rays left open over U(H): (0,2,6,8), (0,3,9,12), (0,2,10,12); U/U(x^e, y^e); calibration on the Kostant modules; duality | CONFIRMED (2026-11-19) | all three realized over QQ: U/U(x^2, y^2), U/U(x^3, y^3), cokernels of 2 by 3 matrices of quadrics; U/U(x^e, y^e) pure for e <= 6; the pair (x^2, y^2) fails in characteristics 2 and 3; other pairs work in characteristic 3, none of 80 in characteristic 2; duality reverses tables on 20 of 20 examples; two instruments agree on 96 of 96 modules |
| EXP-003-heisenberg-characteristic-two | characteristic 2 over U(H); the proof steps of U/U(x^e, y^e); genericity | CONFIRMED (2026-11-19) | no pair of quadrics has a finite length quotient in characteristic 2 (exhaustive over GF(2) and GF(4), with a proof for every field), so (1,2,2,1) on (0,2,6,8) is realizable over neither ring there: a counterexample with d3 = 8 in characteristic 2 on a ray realized in every other characteristic; the proof steps of the family hold for e <= 8 and the bad primes are exactly the predicted ones; a general pair is not pure for e >= 4; (0,1,5,6), (0,1,7,8), (0,1,9,10), (0,1,11,12), (0,3,5,8) realized in characteristic 2; (0,3,9,12) and (0,2,10,12) never in the searches |
| EXP-004-lift-certificates | do the prime-field realizations of EXP-001 lift to characteristic 0? A rank test per degree on the lifted integer matrices, with a lemma on flat lifts of pure resolutions, on the 130 verified hits (64 as known answers) | CONFIRMED (2026-11-19) | the rank test passes on all 130 hits (two instruments; one matrix by one instrument), reproduces the 64 known answers, and with the lift lemma makes every ray realized over GF(32003) a ray realized in characteristic 0 (193 of 193, 147 before); the two rechecks of EXP-001 that had failed over QQ were false negatives (both modules are pure over QQ in Singular); the lemma awaits review (BSB-020) |

## 4. In flight

Opened 2026-11-19 (portfolio review of 2026-11-19, decision 1). The literature pass is done
([context note](../../problems/commutative-algebra/boij-soderberg-realizability/context/2026-11-19-literature-pass.md)):
over S the census is 68 realized, 12 obstructed, 140 undecided; c_d = 2 on the two d3 = 10 counterexample rays; over
U(H) Kostant's theorem for sp_4 realizes eleven primitive points in characteristic 0 and leaves (0,2,6,8), (0,3,9,12)
and (0,2,10,12) among the S-obstructed parity-passing rays. Derived by hand on 2026-11-19 [D]: U(H)/U(H)(x^2, y^2) has
Hilbert function (1,2,2,2,1) and realizes (1,2,2,1) on (0,2,6,8) in characteristic other than 2 and 3 (EXP-002
hypothesis). EXP-002 CONFIRMED it and more (2026-11-19): with the Kostant modules, every one of the ten rays with
d3 <= 12 that pass parity and are excluded over S is realized over U(H) in characteristic 0, so in characteristic 0 a
counterexample with d3 <= 12 lies on a parity-failing ray. Derived [D], to be reviewed: U/U(x^e, y^e) is pure of type
(0,e,3e,4e) for every e in characteristic 0 (`context/2026-11-19-uh-power-family-proof-sketch.md`); in characteristic 2
no cyclic module has the table (1,2,2,1) on (0,2,6,8), which would make that point a counterexample with d3 = 8 there
(EXP-002 verdict, Consequences). EXP-003 CONFIRMED both the characteristic 2 statement (every subspace over GF(2) and
GF(4)) and every machine-checkable step of the family's proof for e <= 8. Both derivations were reviewed on 2026-11-19 by
a reader other than the writer (correct after minor fixes, applied; BSB-015): U/U(x^e, y^e) has the pure resolution of
type (0,e,3e,4e) if and only if the characteristic is 0 or at least 2e; the point (1,2,2,1) of (0,2,6,8) is realized over
U(H) in characteristic 0 and in every odd characteristic (an explicit pair in characteristic 3) and over neither ring in
characteristic 2. Question 6.1 already has a negative answer over every field (arXiv:2605.25259, Theorem 3.7), so the
result is the dependence of the answer on the characteristic. EXP-001 (the table over S) is CONFIRMED on its question:
193 primitive points realized (147 in characteristic 0), 12 excluded, 15 open, all open ones with d3 >= 10. Every ray with
d3 <= 9 is realized over S in characteristic 0 or is one of the five excluded parity-passing rays that U(H) realizes, so
in characteristic 0 the least d3 of a counterexample to Question 6.1 is 10 ((0,4,9,10) and (0,1,6,10), excluded over S by
Erman's 2009 obstructions and over U(H) by parity, over every field); the published counterexample has d3 = 21. Reviewed
on 2026-11-19 by a reader other than the writer: correct after fixes, no case fails, the 29 explicit modules recomputed
over QQ in a second system (addendum 1 of the EXP-001 verdict).

## 5. Next actions

Published on 2026-11-20: the first manuscript, v0.01, [10.5281/zenodo.24385387](https://doi.org/10.5281/zenodo.24385387) (concept
[10.5281/zenodo.24385386](https://doi.org/10.5281/zenodo.24385386)), `manuscripts/boij-soderberg-realizability/primitive-points-realizability`. It carries
Theorem A (`U/U(x^e, y^e)` is pure of type (0, e, 3e, 4e) exactly in characteristic 0 or at least 2e), the general
characteristic 2 theorem (no finite length module with at most one more relation than generators in one degree e >= 2), the
table over U(H), the census over k[x,y,z] (193 rays realized in characteristic 0, 12 excluded, 15 open), the rank
certificates with the lift proposition, and the least counterexample in characteristic 0 (d3 = 10). The success gate of
BSR-F2 is met and the focus is closed.

Strategic review of 2026-11-20: BSR-F2 is closed and BSR-F3 is the current focus.

1. EXP-005 (hypothesis frozen 2026-11-20): the machine checks of the characteristic 2 theorem and of the family at
   e = 6, 7, rerun with `uhlib` and Singular and archived (backlog BSB-021). In progress.
2. EXP-006 (hypothesis frozen 2026-11-20): is (1,2,2,1) on (0, e, 3e, 4e) realized over U in odd characteristic below
   2e, for e = 3 (p = 3, 5) and e = 4 (p = 3, 5, 7)? Derived before the run: for e = 3 the pure Hilbert function is
   the generic one; for e = 4 a pure pair needs rank 48 for the multiplication map into degree 12, and the locus of
   that condition is not empty and has dimension at least 12 in Gr(2, 9) in every characteristic (a Thom-Porteous
   class). Backlog BSB-023.
3. BSB-022: the census recheck must record a run that ends without a result separately from a computed negative.
4. The 15 open rays with d3 >= 10; the substitution of x^e, y^e in the Kostant presentations (BSB-012).
5. Manuscript v0.02 after EXP-005 and EXP-006 are confirmed and reviewed: artifacts for each machine claim, and the
   statement on odd characteristic.

## 6. Where everything lives

- Records: `program/boij-soderberg-realizability/`; problem tree: `problems/commutative-algebra/boij-soderberg-realizability/`.
- Sources: data root `caos-research/boij-soderberg-realizability/sources/` (manifest with SHA-256 in `context/references.md`).
- Tools: Macaulay2 1.22 in WSL (`/usr/share/Macaulay2/BoijSoederberg.m2`, SHA-256 `3ce45c08f73ea4c3fcc049f261d35c73b4b5a1afcf9c239a9806e2e0ed53b415`;
  AssociativeAlgebras, TensorComplexes, BGG present); Singular 4.3.2 in WSL (Plural for U(H)).

## 7. Gotchas

- Realizability depends on the field: a module found over GF(32003) realizes the point in characteristic 32003 only;
  the QQ re-verification gives characteristic 0; formula constructions state their own fields (EFW is characteristic 0).
  A prime-field hit is carried to characteristic 0 by the rank certificate of EXP-004 (maximal prime-field rank in
  every needed degree) with the lift lemma, without a resolution over QQ.
- The census recheck of EXP-001 records a run over QQ that ends without a result line as a failure: two such
  runs were read as modules that do not lift, and both lift (BSB-022).
- `randomSocleModule` and `randomModule` default to `ZZ/101`; pass `CoefficientRing`.
- A random miss proves nothing; only obstructions exclude.
- The Rethlas raw output `question_6_1.md` misstates the survey ("dimension <= 3"); the paper's Question 2.7 is correct.
- The dossier flags a discrepancy: EFW Example 6.3 reports an Eisenbud-Schreyer multiple 380 for (0,4,9,13), the formula
  gives 3080; recompute before quoting either.
