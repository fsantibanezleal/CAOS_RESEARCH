# EXP-002 verdict: CONFIRMED. Every ray with d3 <= 12 whose primitive point is excluded over k[x,y,z] and passes parity is realized over U(H) in characteristic 0

Date: 2026-11-19. Hypothesis frozen in commit ac4f4880 before any computation. Exact arithmetic throughout (linear
algebra over QQ and finite fields in the library `code/uhlib`; noncommutative Groebner bases in Singular 4.3.2 Plural).
Run: `run.py`, exit 0, 227 s; the library tests (25) pass; rerun of the tests by the coordinating session.

## Outcome per claim

| Claim | Outcome |
|---|---|
| C0 calibration | Holds. Both instruments give the expected tables on 17 modules: the trivial module, U/U(x^2, y^2, xy + yx), and all 15 Kostant modules L(p,q), p <= 4, each with beta = (q+1, p+2, p+2, q+1) on (0, p-q+1, p+q+3, 2p+4) (Table F of the context note). |
| C1 | Holds. Over QQ and GF(32003), U/U(x^2, y^2) has Hilbert function (1,2,2,2,1) and Betti table (1,2,2,1) on (0,2,6,8). The graded pieces of the left ideal in degrees 2 to 5 have dimensions 2, 4, 8, 12 and equal the spans of the hand derivation element by element. |
| C2 | Holds. Over GF(2^k) and GF(3^k), k = 1..4, the pair (x^2, y^2) gives an infinite quotient: dim M_4 = 2 in characteristic 2, dim M_5 = 2 in characteristic 3 (the three degree-5 elements of the derivation have rank 1 over GF(2) and GF(3), rank 2 over QQ, GF(5), GF(7), GF(32003)). |
| C3 | Holds. Over QQ, U/U(x^e, y^e) has the pure table (1,2,2,1) on (0, e, 3e, 4e) for e = 3, 4, 5, 6 (and e = 2 as a control), with Hilbert functions equal to (1 + ... + t^(e-1))^2 (1 + t^2 + ... + t^(2e-2)); lengths 27, 64, 125, 216. |
| C4 | Holds, 10 of 10 seeds. The cokernel of a random 2 by 3 matrix of quadrics has Hilbert function (2,4,5,6,6,6,5,4,2) and the pure table (2,3,3,2) on (0,2,10,12), over GF(32003) and over QQ with the lifted matrix. |
| C5 (exploration) | Characteristic 3: pairs of quadrics with the pure table exist (3 of 20 over GF(3), 18 of 20 over GF(9), 16 of 20 over GF(27), 17 of 20 over GF(81)); only the monomial pair fails there. Characteristic 2: all 80 random pairs over GF(2), GF(4), GF(8), GF(16) give an infinite quotient. |
| C6 duality | Holds on 20 of 20 non-self-dual modules: the Betti table of the graded dual (made a left module through the antipode) is the reverse of the table of the module. |

Instrument agreement: 96 of 96 modules computed by both instruments have equal tables; the Hilbert function recomputed
from the Singular table equals the library's in 104 of 104 checks. For the infinite quotients of C2 the library's Tor
complex does not apply and the comparison is through the Hilbert function.

## Verdict

CONFIRMED. The three rays left open by the Kostant family are realized over U(H) in characteristic 0 by explicit
modules: (0,2,6,8) by U/U(x^2, y^2), (0,3,9,12) by U/U(x^3, y^3), (0,2,10,12) by the cokernel of a 2 by 3 matrix of
quadrics (ten explicit matrices in the artifacts). With the Kostant modules, all ten rays with d3 <= 12 that pass parity
and have their primitive point excluded over S (the dossier's list) have that point realized over U(H) over QQ, hence
over every field of characteristic 0.

## Consequences

- In characteristic 0, with d3 <= 12, a counterexample to Erman-Sam Question 6.1 can lie only on a parity-failing ray.
  The two known ones are (0,4,9,10) and (0,1,6,10); whether a smaller one exists is decided by EXP-001 on the
  parity-failing rays with d3 <= 9.
- The family U/U(x^e, y^e): pure for e <= 6 by machine. A derivation of the statement for every e in characteristic 0
  (Hilbert series through binomial Toeplitz blocks, one-dimensional socle through the kernel of y and the symmetry
  x to y, y to -x) is written in `context/2026-11-19-uh-power-family-proof-sketch.md`; it agrees with every Hilbert
  function above and is to be reviewed before it is claimed.
- Characteristic 2 [D, derived after this run; to be machine-checked and reviewed, EXP-003]: x^2, y^2 and z are central,
  U_2 = span(x^2, y^2, z, xy), so any two quadrics have a nonzero central combination c or are both central; then
  U/U(f, g) is a finitely generated module over the two-dimensional ring k[x^2, y^2, z]/(c), cut by one square matrix,
  and cannot have finite length. So over a field of characteristic 2 no cyclic module has the table (1,2,2,1) on
  (0,2,6,8): that point is realizable over neither S (Krull) nor U(H), a counterexample to Question 6.1 with d3 = 8 in
  characteristic 2, on a ray where the point is realizable in characteristic 0. C5 is the evidence that prompted it.
- Duality over U(H) holds on every example tested, which supports using it to halve the U(H) table; it is not proved
  here.

## Deviations from the hypothesis

- C3 lists e = 2 as a control. C6 uses the graded dual with the antipode and not a separate Ext^3 computation (the
  hypothesis named the dual module through Ext^3; the two agree for finite length modules over an Artin-Schelter
  Gorenstein algebra, which is the statement being tested, so the test is of the reversal on the graded dual).
- The hypothesis remarks that the Hilbert series of M_e is what a module free over k[z]/(z^e) would have. M_2 is not free
  over k[z]/(z^2) (it is k[z]/(z^3) + (k[z]/(z^2))^2 + k[z]/(z)); the Hilbert function claim does not depend on the remark.
- Singular lists a zero vector in the last syzygy module; the parser skips it.

## Adversarial validation

Two instruments with no shared code (an exact linear-algebra library with a Tor complex; Plural Groebner bases read
through generator degrees), calibrated on 17 modules with known tables including 13 with more than one generator; the
hand derivation of C1 compared degree by degree, including its prediction of failure in characteristics 2 and 3 (C2),
which the machine reproduces with the predicted dimensions; lifted matrices over QQ for C4.

## How could this be wrong?

- Both instruments share a wrong convention for the algebra (for example the sign of z): the trivial module and the
  Kostant modules would then fail calibration; they do not.
- A finite length quotient is declared too early: the library stops only when the ideal contains everything in
  consecutive degrees, and Plural computes the full resolution independently.
- The realizations are over QQ and GF(32003); nothing is claimed for other positive characteristics except where
  computed (C2, C5).
- The statement about all ten rays depends on the dossier's list of S-excluded parity-passing rays, which EXP-001
  recomputes (gate G2).
