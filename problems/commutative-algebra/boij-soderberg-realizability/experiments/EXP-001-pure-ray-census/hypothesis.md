# EXP-001 preflight: the realizability table of the 220 pure rays with d3 <= 12 over k[x,y,z]

Date: 2026-11-19. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (Betti tables of
explicit modules over prime fields and over QQ; rational arithmetic in the census).

Preflight P1 (source-complete) is the literature pass of 2026-11-19
([context note](../../context/2026-11-19-literature-pass.md)); its Tables A to D are known answers here.

## Question

For every degree sequence d = (0,d1,d2,d3) with d3 <= 12, with primitive Herzog-Kuhl point beta_d, over S = k[x,y,z]:

1. Census (stage 0): beta_d; the parity p(-1) and the Hilbert functions over S and over U(H); the multiples realized by
   the formula constructions; the multiples excluded by the published obstructions at every m; the closure under scaling
   (a realization at d gives one at e d; an exclusion at e d gives one at d) and duality (d to (0, d3-d2, d3-d1, d3) with
   the Betti numbers reversed); hence an interval [low_d, up_d] for the least realizable multiple c_d.
2. Search (stage 1): on every ray with low_d < up_d, is m beta_d the Betti table of a generic level module or of a module
   with a generic presentation, for m from low_d upward, over GF(32003)? Does each hit persist over QQ?
3. Which rays have c_d determined, which have the primitive point realized, which stay open, and what remains of the
   smallest-counterexample question on the 84 rays with d3 <= 9?

## Definitions and sources

- Primitive point, pure ray, realizable, c_d: the dossier, sections 1.2 to 1.4, and Erman 2009, Section 7 question (2).
- Formula constructions: Eisenbud-Schreyer (any field; `pureCharFree`), the two Eisenbud-Floystad-Weyman constructions
  (characteristic 0; `pureTwoInvariant`, `pureWeyman`), Soderberg's extremely compressed level modules on the rays
  (0,a,a+1,d3) (Proposition 4.1 of arXiv:math/0612047: a module with s = binom(d3-a, 2) generators and socle type
  t = binom(a+1, 2); infinite field), Koszul ((0,a,2a,3a)), S/m^a ((0,a,a+1,a+2)) and its dual, generic Pfaffians
  ((0,a,b,a+b) with beta = (1,n,n,1), n = 2r+1, a = r(b-a)), Buchsbaum-Rim ((0, delta, (a+1) delta, (a+2) delta) with
  table (a, a+2, a+2, a)).
- Obstructions at the multiple m (commutative ring, any field), with B = m beta_d: (O1) second syzygy, d2 <= (B0+1) d1;
  (O2) codimension, B1 >= B0 + 2, and in the equality case the table must be the Buchsbaum-Rim one; (O3) regularity,
  d3 <= (B0+2) d1 (Erman 2009, Proposition 3.1); (O4) a cyclic point (1,n,n,1) with n even is excluded (Buchsbaum-
  Eisenbud); (O5) a cyclic point with B1 = 3 forces d = (0,a,2a,3a) (three generators of a height three ideal form a
  regular sequence); (O6) the duals of O1 to O5 under the duality above. O1 to O6 are never applied over U(H).
- Search generators (Macaulay2 1.22, package BoijSoederberg, file SHA-256
  `3ce45c08f73ea4c3fcc049f261d35c73b4b5a1afcf9c239a9806e2e0ed53b415`): `randomSocleModule(L, m)` (m B0 generic elements
  in m B3 copies of the truncated injective hull: the generic level module with the Hilbert function of the pure table)
  and `randomModule(L, m)` (cokernel of a generic m B0 by m B1 matrix of forms of degree d1), with
  `CoefficientRing => ZZ/32003`. A hit is a module whose Betti table equals m times the pure diagram exactly; a pure
  table of this shape satisfies the Herzog-Kuhl equations, so the module has finite length.

## Stages

- Stage 0 (census, exact): an independent Python implementation (rational arithmetic) of beta_d, the parity, the
  Hilbert functions, the Eisenbud-Schreyer product, the two Eisenbud-Floystad-Weyman ranks (hook-content formula), the
  Soderberg multiple, the classical constructions, O1 to O6 for 1 <= m <= 12, and both closures; compared with
  Macaulay2 (`pureBetti`, `pureAll`) on all 220 rays.
- Stage 1a (known answers, run first): the eight documentation rays of Table A of the context note at m = 1;
  `randomModule({0,4,9,10}, 2)`; the package tests (`randomSocleModule` on (0,1,3,4) at m = 1, 2, 3 and on (0,2,3,6) at
  m = 1, 2, 3; `randomModule({0,4,9,10}, 1)` giving the Koszul table); each over ZZ/101, GF(32003) and QQ.
- Stage 1b (Soderberg family): `randomSocleModule(L, s/B0)` on the 55 rays (0,a,a+1,d3), 3 seeds each.
- Stage 1c (search): every ray with low_d < up_d after stage 0 and stages 1a, 1b, both generators, m from low_d up to
  min(up_d - 1, 4), stopping at the first hit; 3 seeds per (ray, m, generator); a resolution that exceeds 20 minutes is
  recorded as a timeout, not as a miss. Hits are closed again under scaling and duality.
- Stage 1d (verification of every hit): the module is saved as an explicit presentation matrix; its Betti table is
  recomputed in a fresh Macaulay2 process and in Singular 4.3.2 (`mres` over the same field); the same construction is
  repeated over QQ with the random matrix lifted to symmetric integer representatives, limit 30 minutes per hit.
- Stage 1e (characteristic flags, no claim): each hit's generator is rerun over GF(2), GF(3), GF(5), 5 seeds each.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1: Python and Macaulay2 agree on beta_d and on the three construction numbers for all 220 rays; the counts are 220
  rays, 44 with B0 = 1, 29 passing parity.
- G2: the columns beta, Eisenbud-Schreyer multiple and parity of the dossier's Appendix A are reproduced on every row;
  every difference in the status column is listed with its reason.
- G3: stage 1a reproduces every known answer over ZZ/101 and GF(32003).
- G4: no hit on a point excluded by O1 to O6 (a hit there is a bug or a refuted proof; both stop the run).
- G5: every hit passes the fresh-process and Singular rechecks; a hit that fails the QQ recheck stays a
  characteristic-32003 realization and is listed separately.
- G6: for (0,4,9,10) and (0,1,6,10): beta = (1,3,8,6) and (6,8,3,1), p(-1) = -16 and 16, O5 (and O1) excludes m = 1 on
  the first, O3 and the equality case of O2 exclude m = 1 on the second, and m = 2 is realized on both (Table B).
- G7: `pureCharFree({0,4,9,13})` is recorded (the dossier flags 380 in a printed example against 3080 from the formula).

## Predictions

- P1: G1, G2, G6 hold (0.95). Stage 0 (formulas and closures, the Soderberg family not counted before stage 1b) gives
  between 52 and 56 primitive points realized and exactly 12 excluded at m = 1 (0.85); O1 to O6 exclude no point with
  m >= 2 (0.8).
- P2: stage 1b is pure on all 55 rays at m = s/B0 over GF(32003) (0.85; the theorem is stated for an infinite field).
- P3: stage 1c realizes the primitive point on at least 60 of the rays still undecided after stage 0 (0.6), including
  (0,3,4,8), for which Boocher, Huang and Wolf state a module without giving it (0.8), and determines c_d on at least
  100 of the 220 rays in all (0.7).
- P4: every hit over GF(32003) persists over QQ (0.85 per hit).
- P5 (smallest counterexample): after stage 1, every parity-failing ray with d3 <= 9 has its primitive point realized
  over S (0.5). If so, a counterexample to Question 6.1 with d3 <= 9 can come only from a parity-passing ray that is
  obstructed over S, which EXP-002 treats.

## What a PASS proves and what a FAIL proves

A hit proves realizability of that point over the field of the computation (and over QQ when the recheck passes, hence
over every field of characteristic 0); with the direct-sum closure it realizes every larger multiple generated by the
hits. A miss proves nothing about the point (families of level algebras can be reducible; a generic member need not be
the right one): only O1 to O6 exclude. The table therefore has three honest values per point: realized (with field),
excluded (with the obstruction), open.

## Premise dependencies

- The scaling and duality lemmas: dossier section 1.4 [D] (flat base change along x to x^e; Ext^3(-, S)).
- The constructions and obstructions: the cited theorems [V] in the dossier and the context note; Soderberg's
  Proposition 4.1 rests on Boij's existence theorem for compressed level modules (J. Algebra 226 (2000)), not read: its
  consequence is tested in stage 1b rather than assumed for the table (a ray counts as realized by that route only with
  an explicit module from stage 1b).
- Macaulay2's `res` and `betti` over prime fields and QQ: exact; cross-checked in Singular (G5).

## Budget and kill criterion

Stage 0: seconds. Stages 1a, 1b: under one hour. Stage 1c: at most 12 hours of wall time on 16 processes (one Macaulay2
process per ray, results appended to a resumable JSONL, flushed progress); rays not reached are reported as not run.
Stage 1d: at most 6 hours. If the budget is hit, the table is published with the cells reached.

## Invariant-first note

The parity test and the Hilbert-function sign are ray invariants and are computed first (stage 0). The obstruction
bounds and the construction formulas decide every point they reach before any module is built; the search runs only on
what they leave open.
