# EXP-002 preflight: primitive points over the Heisenberg enveloping algebra U(H) on the rays that are obstructed over k[x,y,z]

Date: 2026-11-19. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (linear algebra
over QQ and over prime fields; noncommutative Groebner bases in Singular Plural).

## Question

U(H) = k<x,y>/([x,[x,y]], [y,[x,y]]), z = [x,y] central, deg x = deg y = 1, deg z = 2; Hilbert series
1/((1-t)^2 (1-t^2)). Ten rays with d3 <= 12 pass the parity test and have their primitive point excluded over S. The
literature pass of 2026-11-19 ([context note](../../context/2026-11-19-literature-pass.md), Table F) realizes seven of
them over U(H) in characteristic 0 by Kostant's theorem for sp_4 (the modules L(p,q)), and leaves three:

- (0,2,6,8) with (1,2,2,1),
- (0,3,9,12) with (1,2,2,1),
- (0,2,10,12) with (2,3,3,2).

Erman-Sam Question 6.1 has a counterexample on one of these rays exactly when its primitive point is realizable over
neither ring. Questions:

1. Is the primitive point of each of the three rays the Betti table of a finite length graded U(H)-module, and over
   which characteristics?
2. Is U(H)/U(H)(x^e, y^e) a finite length module with pure resolution of type (0, e, 3e, 4e) and Betti numbers
   (1,2,2,1), for e = 1, ..., 6, in characteristic 0?
3. Do the Kostant modules L(p,q), p <= 4, have the tables of Table F when computed by the instruments of this
   experiment (calibration), and does Ext-duality reverse Betti tables on non-self-dual examples?

## Derivation to be checked [D] (done by hand on 2026-11-19, before any machine computation)

Take M = U(H)/U(H)(x^2, y^2), with yx = xy - z. In U(H): y x^2 = x^2 y - 2xz and y^2 x^2 = x^2 y^2 - 4xyz + 2z^2.
- Degree 2: I_2 = span(x^2, y^2), so M_2 has basis xy, z.
- Degree 3: I_3 = span(x^3, x^2 y - 2xz, x y^2, y^3), dimension 4 of 6, so dim M_3 = 2.
- Degree 4: I_4 is spanned by x^4, x^3 y - 2x^2 z, x^2 y^2 - 4xyz + 2z^2, x^2 z, x^2 y^2, x y^3, y^4, y^2 z: dimension 8 of 9
  when 2 is invertible, so dim M_4 = 1.
- Degree 5: I_5 = U_1 I_4 contains x^5, x^4 y, x^3 y^2, x^2 y^3, x y^4, y^5, x^3 z, x y^2 z, y^3 z, the three elements
  -4x^2 yz + 2xz^2, -5x^2 yz + 4xz^2, x^2 yz - 2xz^2 (rank 2 exactly when 6 is invertible) and 6 y z^2; so I_5 = U_5 and
  M_5 = 0 when 6 is invertible.
Hence, in characteristic different from 2 and 3, M has Hilbert function (1,2,2,2,1), which is the Hilbert series
(1 - 2t^2 + 2t^6 - t^8)/((1-t)^2 (1-t^2)) of the pure table. Its socle is M_4 (no element of degree 1, 2 or 3 is killed by
x and y), so the last Betti number is 1 in degree 8; with one generator and two relations of degree 2, the Hilbert series
forces the second syzygies to be 2 in degree 6. So M realizes the primitive point (1,2,2,1) of (0,2,6,8) over U(H). In
characteristic 2 the element 4xyz - 2z^2 vanishes and dim M_4 = 2; in characteristic 3 the three elements above are
proportional and M_5 != 0: the pair (x^2, y^2) fails there.

The same pattern is expected for every e: M/zM = k[x,y]/(x^e, y^e), a complete intersection with Hilbert series
(1 + t + ... + t^(e-1))^2, and the pure table of (0,e,3e,4e) has Hilbert series
(1 + t + ... + t^(e-1))^2 (1 + t^2 + ... + t^(2e-2)) over U(H), which is what M has if it is free over k[z]/(z^e).

For (0,2,10,12), the Hilbert series of the pure table (2,3,3,2) over U(H) is
2 + 4t + 5t^2 + 6t^3 + 6t^4 + 6t^5 + 5t^6 + 4t^7 + 2t^8, which is the series (2 - 3t^2) times the series of U(H)
truncated at its first non-positive coefficient: the table is the one a cokernel of a 2 by 3 matrix of quadrics has when
every multiplication map has maximal rank (an exact balance, 60 = 60, in degree 9).

## Instruments

- I1 (own, exact): U(H) in the PBW basis x^a y^b z^c with the straightening rule yx = xy - z, over QQ (`Fraction`) and
  over GF(p); a left ideal or a submodule of a free module degree by degree by exact row reduction; the quotient M as
  a graded vector space with the matrices of x and y; the graded Betti numbers as the homology of the complex obtained
  by tensoring M with the minimal resolution of the trivial module, 0 to U(-4) to U(-3)^2 to U(-1)^2 to U (the
  Chevalley-Eilenberg complex after cancellation; Erman-Sam 2016, Section 6).
- I2 (Singular 4.3.2, Plural): `nc_algebra` with the weighted ordering wp(1,1,2), homogeneous input, `mres`; graded
  Betti numbers read from the degrees of the generators of each syzygy module, never from `betti()` (its output on
  G-algebras is not reliable, context note item L4.8).
- A claim is accepted only when I1 and I2 agree.

## Claims

- C0 (calibration): I1 and I2 give (1,2,2,1) on (0,1,3,4) for k; (1,3,3,1) on (0,2,4,6) for U/U(x^2, y^2, xy + yx) (the
  four-dimensional module L(1,0)); and the tables of Table F for L(p,q), p <= 4, built as the U(H)-submodule generated
  by a highest weight vector inside the tensor products of the standard representation of sp_4 and its exterior square
  (the construction of the literature pass, rebuilt here).
- C1: over QQ and over GF(32003), U/U(x^2, y^2) has Hilbert function (1,2,2,2,1) and Betti table (1,2,2,1) on (0,2,6,8).
- C2: over GF(2^k) and GF(3^k) the pair (x^2, y^2) does not give that table (Hilbert functions as derived above).
- C3: over QQ, U/U(x^e, y^e) has the pure table (1,2,2,1) on (0,e,3e,4e) for e = 3, 4, 5, 6; in particular the primitive
  point of (0,3,9,12) is realized over U(H).
- C4: a cokernel of a random 2 by 3 matrix of quadrics over U(H) (entries random in the four-dimensional space U_2) has
  the pure table (2,3,3,2) on (0,2,10,12), over GF(32003) and, with the matrix lifted, over QQ; 10 seeds.
- C5 (exploration, no prediction of the outcome): random pairs of quadrics over GF(2^k) and GF(3^k), k = 1, 2, 3, 4,
  20 seeds each: is (1,2,2,1) on (0,2,6,8) realized in characteristics 2 and 3 by some pair?
- C6 (duality): for 20 random finite length modules that are not self-dual (cokernels of random matrices with the
  degrees of C4 and of 3 by 5 matrices of linear forms truncated to finite length), the Betti table of the dual module
  (the right module Ext^3(M, U) made a left module through the antipode x to -x, y to -y) is the reverse of the Betti
  table of M.

## Predictions

C0 holds (0.9; a failure is an instrument defect and stops the run). C1 holds (0.97). C2 holds (0.9). C3 holds for e = 3
(0.8) and for e = 4, 5, 6 (0.7). C4 holds for at least 9 of 10 seeds (0.6). C6 holds on every example (0.85).

## Consequences fixed in advance

- C1 and C3 (e = 3) and C4 hold: every parity-passing ray with d3 <= 12 whose primitive point is excluded over S is
  realized over U(H) in characteristic 0, so within d3 <= 12 a counterexample to Question 6.1 in characteristic 0 can
  lie only on a parity-failing ray; with EXP-001 this decides whether the two d3 = 10 rays are the smallest.
- C1 fails: the hand derivation is wrong; it is redone before anything else. C3 or C4 fails: the ray stays open over
  U(H); a failed random search is not an exclusion, and a structured search (other pairs, other presentations) follows.
- C2 holds and C5 finds no pair in characteristic 2 or 3: a lead on characteristic dependence over U(H), not a result.

## What a PASS proves and what a FAIL proves

A computed module with the pure table proves realizability over U(H) over the field of the computation, and over QQ
over every field of characteristic 0 (base change). C3 for e <= 6 proves those six cases only; the statement for every
e needs a proof. A random miss proves nothing. C6 is evidence for the duality lemma, not a proof.

## Premise dependencies

- The parity test and the list of ten rays: dossier section 4 and Appendix A [D], recomputed by EXP-001 stage 0.
- The minimal resolution of the trivial module over U(H): Erman-Sam 2016, Section 6 [V], and C0.
- No verdict of EXP-001 is used; the two experiments are independent.

## Budget and kill criterion

Every module here has length at most a few hundred; the whole experiment is expected in under one hour. A single
resolution that exceeds 30 minutes is recorded as not finished. Killed at 6 hours.

## Invariant-first note

The Hilbert series of the pure table over U(H) is the invariant: it must be a polynomial with nonnegative coefficients
(parity), and for the three rays it equals the maximal-rank series, which is why a generic or a monomial presentation
is the first candidate and why the check is a rank computation in one exact-balance degree.
