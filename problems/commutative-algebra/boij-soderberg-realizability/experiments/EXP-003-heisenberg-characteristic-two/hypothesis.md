# EXP-003 preflight: U(H) in characteristic 2, the structure behind U/U(x^e, y^e), and what is special about it

Date: 2026-11-19. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (the library
`code/uhlib` and Singular Plural, the two instruments of EXP-002, calibrated there).

## Questions

1. Characteristic 2. EXP-002 (C5) found no pair of quadrics over GF(2^k) with a finite length quotient. Is it true that
   over every field of characteristic 2 no cyclic U(H)-module has the Betti table (1,2,2,1) on (0,2,6,8)? With Krull over
   S, that would make the primitive point of (0,2,6,8) a counterexample to Erman-Sam Question 6.1 in characteristic 2,
   with d3 = 8, on a ray where the point is realized in characteristic 0 (EXP-002 C1).
2. Characteristic 2, the other rays. For the nine other rays with d3 <= 12 that pass parity and are excluded over S, is
   the primitive point realized over U(H) in characteristic 2?
3. The proof of the family. Do the intermediate statements of the derivation for U/U(x^e, y^e)
   ([context note](../../context/2026-11-19-uh-power-family-proof-sketch.md), steps 2 to 5) hold by machine for e <= 8:
   the dimensions of the weight blocks, the kernel of y, the socle? In which characteristics is U/U(x^e, y^e) pure?
4. Genericity. For e >= 4, is a general pair of forms of degree e not pure of type (0,e,3e,4e), as the Hilbert series
   predicts? Is the primitive point (2,3,3,2) of (0,3,15,18) (the next ray of the family of (0,1,5,6)) realized?

## Derivation to be checked [D] (question 1)

In characteristic 2, [x^2, y] = 2xz = 0 and [y^2, x] = 0, so C = k[x^2, y^2, z] is central, a polynomial ring in three
variables of degree 2, and U is a free C-module with basis 1, x, y, xy. U_2 = C_2 + k xy with C_2 = span(x^2, y^2, z).
Let f, g be linearly independent in U_2. If both are central, U/U(f, g) = U tensor_C C/(f, g) is infinite-dimensional
(C/(f, g) has dimension at least 1). Otherwise some combination of f and g is a nonzero central quadric c and the left
ideal is U f + U c with f not central. Then U/U c is a free module of rank 4 over R = C/(c), a graded polynomial ring
in two variables, and U/(U f + U c) is the cokernel of right multiplication by f on it, an R-linear endomorphism rho_f
that raises degrees by 2. If det rho_f = 0 the cokernel has positive rank; if not, det rho_f is homogeneous of positive
degree and the cokernel is supported on its zero set, which has dimension 1. In both cases the quotient has infinite
length. Since a module with table (1,2,2,1) on (0,2,6,8) is U/U(f, g) for two independent quadrics, no such module
exists in characteristic 2.

## Claims

- A1 (exhaustive, characteristic 2): for each of the 35 two-dimensional subspaces of U_2 over GF(2) and each of the 357
  over GF(4), the quotient by the left ideal it generates is nonzero in every degree from 2 to 20. For each subspace the
  central element c and det rho_f (zero, or its degree) are recorded, as in the derivation.
- A2 (random, characteristic 2): the same for 200 random two-dimensional subspaces over GF(16) and over GF(256).
- B1 (characteristic 2, exploration with a search): for each of (0,1,5,6), (0,1,7,8), (0,1,9,10), (0,1,11,12) (tables
  (a, a+1, a+1, a)), (0,3,5,8) and (0,5,7,12) (tables (1,4,4,1) and (1,6,6,1)), (0,3,9,12) (table (1,2,2,1), pairs of
  cubics), (0,2,10,12) (table (2,3,3,2), 2 by 3 matrices of quadrics): cokernels of random presentation matrices with
  B0 generators in degree 0 and B1 relations in degree d1, over GF(2), GF(4), GF(16), 40 seeds per field; the number of
  seeds with the pure table. The same search over GF(32003) is the positive control (each ray must be hit there, as
  the Kostant modules and EXP-002 show, if generic presentations suffice; a ray not hit over GF(32003) is reported as
  not reachable by generic presentations and the characteristic 2 outcome is then not interpreted).
- C1 (proof steps, e = 2..8, QQ): the dimension of the weight w, degree d piece of M_e equals the coefficient given by
  D_q(n') of the context note (q = |w|, d = 2n' + q); the kernel of y on M_e is spanned by the classes z^c g_a; the socle
  of M_e is one-dimensional, of weight 0 and degree 4e - 4; the Hilbert series is
  (1 + ... + t^(e-1))^2 (1 + t^2 + ... + t^(2e-2)).
- C2 (k[z]-structure, e = 2..5, QQ; exploration): the invariant factors of M_e as a module over k[z], against the
  pattern one summand k[z]/(z^(2e-1-a-b)) for each a, b < e.
- C3 (characteristics, e = 2..5, primes p <= 23): the set of p for which U/U(x^e, y^e) is pure of type (0,e,3e,4e) over
  GF(p), against the prediction of the context note: p does not divide (2e-1)! nor any of the numbers of semistandard
  tableaux of rectangular shape (e-w) by k with entries at most e that occur (0 <= w < e, 1 <= k <= e).
- D1 (genericity): for e = 4, 5 and 10 random pairs of forms of degree e over GF(32003), the quotient has the
  maximal-rank Hilbert function (the series (1 - 2t^e)/((1-t)^2 (1-t^2)) truncated at its first non-positive coefficient)
  and its Betti table is not pure; for e = 2, 3 a random pair is pure.
- D2 (exploration): (0,3,15,18) with (2,3,3,2): cokernels of 10 random 2 by 3 matrices of cubics over GF(32003), and the
  matrix obtained from a presentation of the Kostant module L(1,1) by substituting x^3 for x and y^3 for y (and the same
  substitution with squares, on (0,2,10,12), as a control of the idea).

## Predictions

A1 and A2 hold in every case (0.95: the derivation). B1: over GF(32003) every ray is hit by generic presentations
except possibly (0,3,9,12) and the (1,6,6,1) ray (0.7 for all eight); in characteristic 2, (0,2,10,12) is not hit (0.6:
a matrix of quadrics has a central column after column operations) and the rays with odd d1 are hit (0.6). C1 holds
for every e <= 8 (0.9). C2: the pattern holds (0.7). C3: the prediction holds for e = 2 (bad primes 2 and 3) and the
bad primes for each e are among the predicted ones (0.75). D1 holds (0.85). D2: no prediction.

## Consequences fixed in advance

- A1 and A2 hold: the derivation for characteristic 2 is supported on every subspace over GF(2) and GF(4); with a
  review of the proof, the statement "in characteristic 2 the primitive point of (0,2,6,8) is realizable over neither
  S nor U(H)" is established and Question 6.1 has a characteristic-dependent answer on that point.
- A1 fails on a subspace: the derivation is wrong; the module is examined (it would realize the point in
  characteristic 2).
- B1 finds a ray not hit in characteristic 2 but hit in characteristic 32003: a candidate for a second
  characteristic-dependent point; it needs a proof before any claim.
- C1 fails for some e: the derivation of the family is wrong at the step named; the family stays a machine result
  for e <= 6.

## What a PASS proves and what a FAIL proves

A1 is exhaustive over GF(2) and GF(4) only; the statement over every field of characteristic 2 rests on the derivation.
Finite length is refuted by a nonzero graded piece in every degree up to 20 together with the derivation's reason
(support of dimension 1); the machine alone shows degrees up to 20. B1 hits prove realizability over that field;
misses prove nothing. C1 to C3 are finite checks of a derivation, not the proof.

## Premise dependencies

- The instruments: EXP-002 (C0, agreement on 96 modules).
- The list of ten rays: dossier Appendix A [D]; EXP-001 gate G2 recomputes it.

## Budget and kill criterion

Everything is small (lengths up to a few hundred; e = 8 gives length 512); expected under one hour, killed at 6 hours.
A single computation over 30 minutes is recorded as not finished.

## Invariant-first note

For question 1 the invariant is the center: one central quadric in the ideal decides every case. For question 3 the
invariants are the torus weight and the z-adic structure, which reduce the Hilbert function to ranks of binomial
matrices.
