# boij-soderberg-realizability: RESUME (session handoff)

Updated 2026-11-19 (opened). First read for any session, per methodology 07. Derived view: experiment verdicts win.

## 1. State in one screen

Pure rays of the Boij-Soderberg cone in three variables are indexed by degree sequences d = (0,d1,d2,d3); their integral
points are the multiples m beta_d of the primitive Herzog-Kuhl point. Erman-Sam Question 6.1 asked whether every integral
point is realized by a finite length module over S = k[x,y,z] or over U(H) (Heisenberg, deg z = 2). Rethlas
(arXiv:2605.25259v2) answered no with (0,6,20,21), beta (1,2,9,8): Krull over S, parity p(-1) = 16 over U(H) [V]. No
follow-up in six months [V, 2026-11-19]. The 2026-09-02 dossier holds smaller counterexamples, (0,4,9,10) with
(1,3,8,6) and its dual (0,1,6,10) with (6,8,3,1), d3 = 10, from published obstructions and the parity test [D, to be
machine-checked], and a census of the 220 rays with d3 <= 12 (about 52 primitive points realized by formulas, 12
obstructed, about 156 undecided) [D, scripts lost; recomputed in EXP-001].

First round: EXP-001, the exact census with formula bounds and closures, and a random-module search over GF(32003) with
every hit re-verified in Singular and over QQ.

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
| EXP-001-pure-ray-census | the d3 <= 12 table over S: census, obstructions at every m, closures, generic level modules and generic presentations over GF(32003), every hit rechecked in Singular and over QQ | hypothesis frozen 2026-11-19 | - |
| EXP-002-heisenberg-primitive-points | the three S-obstructed parity-passing rays left open over U(H): (0,2,6,8), (0,3,9,12), (0,2,10,12); U/U(x^e, y^e); calibration on the Kostant modules; duality | CONFIRMED (2026-11-19) | all three realized over QQ: U/U(x^2, y^2), U/U(x^3, y^3), cokernels of 2 by 3 matrices of quadrics; U/U(x^e, y^e) pure for e <= 6; the pair (x^2, y^2) fails in characteristics 2 and 3; other pairs work in characteristic 3, none of 80 in characteristic 2; duality reverses tables on 20 of 20 examples; two instruments agree on 96 of 96 modules |

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
(EXP-002 verdict, Consequences; EXP-003 to check). EXP-001 is running.

## 5. Next actions

1. EXP-001: census, gates, search, rechecks; the table state in the verdict.
2. EXP-002: the three U(H) rays, U/U(x^e, y^e), calibration and duality; then a proof of the pattern for every e.
3. With both: the smallest-counterexample statement (candidate B) and the first manuscript outline.

## 6. Where everything lives

- Records: `program/boij-soderberg-realizability/`; problem tree: `problems/commutative-algebra/boij-soderberg-realizability/`.
- Sources: data root `caos-research/boij-soderberg-realizability/sources/` (manifest with SHA-256 in `context/references.md`).
- Tools: Macaulay2 1.22 in WSL (`/usr/share/Macaulay2/BoijSoederberg.m2`, SHA-256 `3ce45c08f73ea4c3fcc049f261d35c73b4b5a1afcf9c239a9806e2e0ed53b415`;
  AssociativeAlgebras, TensorComplexes, BGG present); Singular 4.3.2 in WSL (Plural for U(H)).

## 7. Gotchas

- Realizability depends on the field: a module found over GF(32003) realizes the point in characteristic 32003 only;
  the QQ re-verification gives characteristic 0; formula constructions state their own fields (EFW is characteristic 0).
- `randomSocleModule` and `randomModule` default to `ZZ/101`; pass `CoefficientRing`.
- A random miss proves nothing; only obstructions exclude.
- The Rethlas raw output `question_6_1.md` misstates the survey ("dimension <= 3"); the paper's Question 2.7 is correct.
- The dossier flags a discrepancy: EFW Example 6.3 reports an Eisenbud-Schreyer multiple 380 for (0,4,9,13), the formula
  gives 3080; recompute before quoting either.
