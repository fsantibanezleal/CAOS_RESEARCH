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

