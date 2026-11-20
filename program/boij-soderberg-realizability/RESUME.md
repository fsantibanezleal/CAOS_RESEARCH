# boij-soderberg-realizability: RESUME (session handoff)

Updated 2026-11-20 (manuscript v0.02 published; EXP-009 to EXP-017 closed; v0.03 in its third pass). First read for any session, per methodology 07. Derived view: experiment verdicts win.

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
| EXP-005-characteristic-two-machine-checks | do the repository's instruments reproduce the reviewers' machine checks of the characteristic 2 theorem and of the family at e = 6, 7? Exhaustive quadrics and cubics over GF(2), random quartics to septics and matrices over GF(2), GF(4), GF(16), the sharpness shapes, 24 modules of the family | CONFIRMED (2026-11-20) | 0 finite length cases of 1,574 with b <= a + 1; every eventually constant case has the value (a(a+1)/2) L.L; b = a + 2 gives finite length in general; U/U(x^e, y^e) pure exactly for p >= 2e at e = 6, 7 (primes up to 31, and QQ) |
| EXP-006-odd-characteristic-below-2e | is the point (1,2,2,1) of (0, e, 3e, 4e) realized over U in odd characteristic below 2e? Exhaustive cubics over GF(3); random cubics over GF(5), GF(9), GF(25), GF(27); random quartics over GF(3), GF(5), GF(7), GF(9) and, as controls with the orbit test, GF(11), GF(13); quintics over GF(3) | CONFIRMED on its question (2026-11-20); one prediction refuted | explicit pure pairs over GF(3), GF(5) at e = 3 and over GF(3), GF(5), GF(7) at e = 4, so for e = 2, 3, 4 the point fails only in characteristic 2; at e = 5 realized in characteristic 3; 217 pure spaces over GF(11), GF(13), none in the orbit of <x^4, y^4>; the locus of the rank condition is not of the expected codimension (it contains the resultant hypersurface) |
| EXP-007-pure-family-at-the-power-pair | do the repository's instruments reproduce the review's computations on the family of pure pairs through <x^e, y^e>? The tangent space of the rank locus (e = 4 to 7; the rationals, GF(13), GF(17), GF(32003)), five explicit pairs over the rationals with controls, the linear family, a plane section, the common-factor locus | CONFIRMED (2026-11-20) | tangent dimension exactly 4e - 4 over the rationals (12, 16, 20, 24), so the pure locus is smooth of that dimension at <x^e, y^e> in characteristic 0; 22 at e = 6 over GF(13) and 26 at e = 7 over GF(17); explicit pure modules over the rationals outside the published family, for example U/U(x^4 + x y^3, y^4) |
| EXP-008-odd-characteristic-e5-e6 | pure pairs of quintics over GF(5), GF(7) and of sextics over GF(3)? Random search with the rank filter first, early stop at 40 pure spaces | CONFIRMED (2026-11-20) | 43 pure of 86,250 over GF(5), 42 of 162,500 over GF(7), 40 of 289,000 sextic pairs over GF(3); so for e = 2, 3, 4, 5 the point (1,2,2,1) of (0, e, 3e, 4e) fails only in characteristic 2, and at e = 6 it is realized in characteristic 3; the shares are 0.31, 0.62, 0.91 times q^(-2 h_e(3e)) |
| EXP-009-linear-family-below-2e | does the linear family L_e contain a pure member in odd characteristic below 2e? Every member over GF(p) for e = 4 to 7 (fifteen pairs, five controls); GF(p^2) where none is found | CONFIRMED in six pairs, REFUTED in nine (2026-11-20) | pure members at (4,5), (4,7), (5,7), (6,11), (7,11), (7,13): e = 6 is settled in characteristic 11 and e = 7 in 11 and 13 (x^6 + y^4 z, y^6 + 3 x^4 z over GF(11); x^7 + y^5 z, y^7 + x^5 z over GF(13)); no pure member for p <= e, at (5,5) and at (6,7); no member above the rank in any pair |
| EXP-010-weight-class-strata | does an admissible stratum S(m; i, j) (f, g homogeneous for the weight modulo m) hold a pure pair in the open pairs (6,5), (6,7), (7,3), (7,5), (7,7)? Nine settled pairs as controls; e = 8 exploratory | CONFIRMED (2026-11-20) | pure pairs over GF(p) in all five pairs (two instruments); none of the 410 strata that are not admissible holds a member with the pure Hilbert function; e = 8 by search over GF(3), GF(7), GF(13) |
| EXP-011-central-pair-machine-checks | are the central pairs x^e + z^s l_1, y^e + z^s l_2 pure in characteristic p dividing an odd e? Sixteen cases, e up to 15, five cases outside the hypotheses | CONFIRMED (2026-11-20) | pure in all sixteen cases and both instruments; e = 7 in characteristic 7 (x^7 + y z^3, y^7 + x z^3), e = 9 in characteristic 3 |
| EXP-012-central-commutator-criterion | are the explicit pairs of the criterion pure for e = 0 or 1 modulo p, and does the criterion agree with purity on random pairs of the class? Eleven explicit pairs, 1,600 random pairs, three built to fail | CONFIRMED (2026-11-20) | pure in all eleven cases and both instruments, among them x^6 + z^3, y^6 + z^3 over GF(5) and x^7 + y z^3 + x^3 z^2, y^7 + x z^3 over GF(3); the criterion equals purity on every random pair |
| EXP-013-pull-back-scaling | does the pull-back along an endomorphism of degree d multiply the degrees of the Betti table by d? Seven pairs, three modules that are not pairs, two controls | CONFIRMED (2026-11-20) | the scaled table in all ten cases and both instruments; pure pairs of degree 8 over GF(3), 12 over GF(5), 16 and 24 over GF(7), where p divides neither e nor e - 1 |
| EXP-014-middle-strata | do the strata S(e; 0, e/2), S((e + 1)/2; 0, (e - 1)/2) and S(e - 1; 0, 1) hold pure pairs at e = 8, 9, 10, 12? | PARTLY CONFIRMED (2026-11-20; one amendment) | pure pairs (x^e + b y^e, G(xy, z)) at e = 8 for p = 5, 7, 11, 13, at e = 10 for p = 3, 7, 11, 13, at e = 12 for p = 5; degree 9 over GF(7) and GF(17); none found at (9,11), (9,13), (12,7) |
| EXP-015-linear-rule-and-e9 | does the rule of the linear family (pure members exactly when 2e - p <= 3) hold for e = 10 to 13, and do other admissible strata hold a pure pair at (9,5), (9,11), (9,13)? | CONFIRMED (2026-11-20) | the rule in all twelve pairs (24 of 24 with the earlier ones; its 'none' half is now a proposition); pure pairs of degree 9 over GF(5), GF(11), GF(13): e = 9 complete |
| EXP-016-congruence-lists | which forms G over GF(p) satisfy the hypothesis and the one congruence, for e = 10 to 16, and is every one a pure pair in U? | CONFIRMED (2026-11-20; one case unfinished) | pure pairs at (10,17), (10,19), (12,7), (12,13), (12,17), (12,19), (12,23), (14,17), (14,19), (16,11); (16,13) as well; e = 10 and e = 12 complete; empty lists at (14,5), (14,11) and over GF(9) |
| EXP-017-odd-stratum-filter | does a member of the odd-e stratum that passes a filter of two congruences have the pure table, at (9,11), (9,13), (11,7), (13,5)? | CONFIRMED (2026-11-20) | pure pairs at the four pairs; all 1,699 members that pass have the pure Hilbert function and all 75 tables are pure; the filter is observed, not proved |

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

Strategic review of 2026-11-20: BSR-F2 is closed and BSR-F3 is the current focus. EXP-005 and EXP-006 are confirmed.

State of the characteristic question for the point (1,2,2,1) of (0, e, 3e, 4e) over U: never in characteristic 2
(Theorem C); always in characteristic 0 or at least 2e (Theorem A); for e = 2, 3, 4 also in every odd characteristic
below 2e, by explicit pairs (EXP-003 at e = 2, EXP-006 at e = 3, 4, EXP-006 and EXP-008 at e = 5): for e = 2 to 5 the
point fails only in characteristic 2. At e = 6 it is realized in characteristics 3 (EXP-008) and 11 (EXP-009) and open
in 5, 7; at e = 7 it is realized in characteristics 11 and 13 (EXP-009) and open in 3, 5, 7; open for e >= 8 below 2e.
The pure pairs form a family of dimension at least 4e - 4 through <x^e, y^e> in
characteristic 0 or at least 2e (context note of 2026-11-20, reviewed: correct after fixes); at that point the
dimension is exactly 4e - 4 over QQ for e = 4 to 7, and explicit pure pairs over QQ lie outside the orbit (EXP-007).

Published on 2026-11-20: the manuscript v0.02, [10.5281/zenodo.24388904](https://doi.org/10.5281/zenodo.24388904), with everything above.

1. Done after v0.02 (all on 2026-11-20). EXP-009: the linear family below 2e. Then five derivations, each read by a
   reviewer other than the writer: the weight classes and their necessary condition; the central pairs (characteristic
   p dividing an odd e); the criterion for pairs with a central commutator, with explicit pure pairs for every e = 0 or
   1 modulo p; the explicit complex as a base change along an endomorphism, which needs a central commutator; the
   pull-back, which multiplies the degrees of every Betti table by d = 0 or 1 modulo p. Then the decomposition over
   k[xy, z] of the pairs (x^e + b y^e, G(xy, z)), with a pure pair over the rationals at e = 4. EXP-011, EXP-012 and
   EXP-013 confirm the three theorems by machine; EXP-010 finds pure pairs at (6,5), (6,7), (7,3), (7,5).
2. State of the point (1,2,2,1) of (0, e, 3e, 4e) (all on 2026-11-20, each with a verdict): for 2 <= e <= 10 and for e = 12
   it fails only in characteristic 2: a pure pair over GF(p) for every odd prime p below 2e (EXP-006, EXP-008 to EXP-017 and
   the criterion). For every e it is realized in characteristic p dividing e(e - 1), for e = d e' with d = 0 or 1 modulo p
   and e' realized, and for even e over a finite field of characteristic p >= 2e - 1. Open: e = 11 at p = 3, 13, 17; e = 13
   at p = 7, 11, 17, 19; e = 14 at p = 5, 11, 23; e >= 15.
3. Three more derivations, each read by a reviewer other than the writer: for the pairs (x^e + b y^e, G(xy, z)) one
   congruence decides the pure Hilbert function and gives the pure Betti table; the projection on the weight-zero
   summand, which proves that the linear family has no pure member for p <= 2e - 5 and excludes weight-class strata; the
   proposition on the characteristic dividing the modulus. Working notes, not reviewed: one family of pairs
   x^e + alpha y^t, y^e + beta x^t governed by one form, with a filter of two congruences that matched every table
   computed (EXP-017).
4. In flight: the manuscript v0.03 (BSB-030; plan in the coordination repository): third pass, review, release. Then the
   strategic review of the focus; backlog BSB-031, BSB-033 to BSB-036, the 15 open rays with d3 >= 10, the substitution in
   the Kostant presentations (BSB-012), BSB-022.

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
