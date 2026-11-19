# EXP-003 results summary

Run: `run.py` from the repository root; hypothesis.md frozen (not edited). Instrument I1 = `code/uhlib` (exact arithmetic: Fraction over QQ, integers mod p, GF(2^k) with a verified irreducible modulus; the numpy build `uhlib/fastmod.py` for prime fields and GF(2^k), the Python build for QQ). Instrument I2 = Singular 4.3.2 Plural in WSL (`singular_i2.py`, no shared code with I1). Betti tables are read from the degrees of the generators of `mres`, never from `betti()`.
Wall time of the run: 151.5 s (tasks ran in parallel processes). Status: complete.

## C0 calibration of the two instruments

| module | field | expected table | I1 | I2 | ok |
|---|---|---|---|---|---|
| k=U/(x,y) | QQ | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | True |
| k=U/(x,y) | GF(2) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | True |
| k=U/(x,y) | GF(2^2) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | True |
| k=U/(x,y) | GF(2^4) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | True |
| k=U/(x,y) | GF(2^8) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | True |
| k=U/(x,y) | GF(32003) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | (0, d=0, 1); (1, d=1, 2); (2, d=3, 2); (3, d=4, 1) | True |
| U/U(x2,y2) | QQ | (0, d=0, 1); (1, d=2, 2); (2, d=6, 2); (3, d=8, 1) | (0, d=0, 1); (1, d=2, 2); (2, d=6, 2); (3, d=8, 1) | (0, d=0, 1); (1, d=2, 2); (2, d=6, 2); (3, d=8, 1) | True |
| L(1,1) | QQ | (0, d=0, 2); (1, d=1, 3); (2, d=5, 3); (3, d=6, 2) | (0, d=0, 2); (1, d=1, 3); (2, d=5, 3); (3, d=6, 2) | (0, d=0, 2); (1, d=1, 3); (2, d=5, 3); (3, d=6, 2) | True |
| L(2,0) | QQ | (0, d=0, 1); (1, d=3, 4); (2, d=5, 4); (3, d=8, 1) | (0, d=0, 1); (1, d=3, 4); (2, d=5, 4); (3, d=8, 1) | (0, d=0, 1); (1, d=3, 4); (2, d=5, 4); (3, d=8, 1) | True |
| L(2,1) | QQ | (0, d=0, 2); (1, d=2, 4); (2, d=6, 4); (3, d=8, 2) | (0, d=0, 2); (1, d=2, 4); (2, d=6, 4); (3, d=8, 2) | (0, d=0, 2); (1, d=2, 4); (2, d=6, 4); (3, d=8, 2) | True |
| L(3,1) | QQ | (0, d=0, 2); (1, d=3, 5); (2, d=7, 5); (3, d=10, 2) | (0, d=0, 2); (1, d=3, 5); (2, d=7, 5); (3, d=10, 2) | (0, d=0, 2); (1, d=3, 5); (2, d=7, 5); (3, d=10, 2) | True |

Complex K exact in degrees 0..10 (rank counts): True. Numpy build equals Python build on U/U(x^3,y^3): True. All calibration cases ok: **True**. The trivial module over GF(2), GF(4), GF(16), GF(256) also exercises the Singular `minpoly` path used for A1, A2, B1 in characteristic 2.

## A1 and A2: two-dimensional subspaces of U_2 = span(x^2, xy, y^2, z) in characteristic 2

Each subspace is given by its reduced echelon basis in the monomial order (y^2, xy, x^2, z). Hilbert function of U/U(f, g) through degree 20 by the numpy build; 'nonzero' means the dimension is positive in every degree 2..20. The data of the derivation: the dimension of the central part of the subspace, the central quadric c, and for a one-dimensional central part the determinant of right multiplication by the non-central generator on U/Uc over R = C/(c) (C = k[x^2, y^2, z]); 'det degree' is the degree in the grading of U.

| claim | field | subspaces expected | computed | distinct bases | nonzero in every degree 2..20 | central part dimension | derivation data (central dim 1) | distinct Hilbert functions |
|---|---|---|---|---|---|---|---|---|
| A1 | GF(2) | 35 | 35 | [35] | 35 / 35 | dim0:0 dim1:28 dim2:7 | det nonzero 22, det zero 6 (degrees [8]) | 3 |
| A1 | GF(4) | 357 | 357 | [357] | 357 / 357 | dim0:0 dim1:336 dim2:21 | det nonzero 326, det zero 10 (degrees [8]) | 3 |
| A2 | GF(16) | 200 | 200 | [200] | 200 / 200 | dim0:0 dim1:199 dim2:1 | det nonzero 199, det zero 0 (degrees [8]) | 1 |
| A2 | GF(256) | 200 | 200 | [200] | 200 / 200 | dim0:0 dim1:200 dim2:0 | det nonzero 200, det zero 0 (degrees [8]) | 1 |

Exhaustive enumeration: the Gaussian binomials [4 choose 2]_q give 35 for q = 2 and 357 for q = 4; the code asserts the enumerated number equals them and the 'distinct bases' column counts distinct reduced echelon bases. The 200 subspaces over GF(16) and GF(256) are uniform random (fixed seeds 20261119 + q, duplicates rejected).

Cross-checks on 10 subspaces per field (indices drawn by a fixed seed): I1 numpy Hilbert function against the pure Python `ideal_hilbert` through degree 20, and against the Hilbert function recomputed from the Singular Betti table through degree 12.

| field | subspaces cross-checked | Python Hilbert equal | Singular Hilbert (through 12) equal | Singular errors |
|---|---|---|---|---|
| GF(2) | 10 | 10 | 10 | 0 |
| GF(4) | 10 | 10 | 10 | 0 |
| GF(16) | 10 | 10 | 10 | 0 |
| GF(256) | 10 | 10 | 10 | 0 |

Hilbert functions that occur (first nine terms, with counts per field):

- GF(16): [1, 2, 2, 2, 2, 2, 2, 2, 2] ... : 200 subspaces
- GF(2): [1, 2, 2, 2, 2, 2, 2, 2, 2] ... : 29 subspaces
- GF(2): [1, 2, 2, 2, 3, 3, 4, 4, 5] ... : 3 subspaces
- GF(2): [1, 2, 2, 3, 3, 4, 4, 5, 5] ... : 3 subspaces
- GF(256): [1, 2, 2, 2, 2, 2, 2, 2, 2] ... : 200 subspaces
- GF(4): [1, 2, 2, 2, 2, 2, 2, 2, 2] ... : 347 subspaces
- GF(4): [1, 2, 2, 2, 3, 3, 4, 4, 5] ... : 5 subspaces
- GF(4): [1, 2, 2, 3, 3, 4, 4, 5, 5] ... : 5 subspaces

Subspaces with a zero graded piece in some degree 2..20: none.
Comparison with the prediction (A1 and A2 hold in every case): the quotient is nonzero in every degree 2..20 for all computed subspaces; no machine statement of infinite length is made (the machine shows degrees up to 20 only).

## B1 random presentations, characteristic 2 and the GF(32003) control

For each ray: B0 generators in degree 0 and B1 relations in degree d1 (primitive pure table of the ray), entries uniform in U_(d1); degree bound d3 + 6; 'finite' = zero in three consecutive degrees within the bound; 'pure hits' = finite and the Betti table equals the primitive pure table. A miss proves nothing about realizability.

| ray | presentation | field | seeds | finite | not finite by the bound | pure hits | I1=I2 on hit records |
|---|---|---|---|---|---|---|---|
| (0,1,5,6) | B0=2 B1=3 d1=1 | GF(32003) | 20 | 20 | 0 | 20 | 3/3 |
| (0,1,5,6) | B0=2 B1=3 d1=1 | GF(2) | 40 | 12 | 28 | 12 | 3/3 |
| (0,1,5,6) | B0=2 B1=3 d1=1 | GF(2^2) | 40 | 20 | 20 | 20 | 3/3 |
| (0,1,5,6) | B0=2 B1=3 d1=1 | GF(2^4) | 40 | 38 | 2 | 38 | 3/3 |
| (0,1,7,8) | B0=3 B1=4 d1=1 | GF(32003) | 20 | 20 | 0 | 20 | 3/3 |
| (0,1,7,8) | B0=3 B1=4 d1=1 | GF(2) | 40 | 9 | 31 | 9 | 3/3 |
| (0,1,7,8) | B0=3 B1=4 d1=1 | GF(2^2) | 40 | 26 | 14 | 26 | 3/3 |
| (0,1,7,8) | B0=3 B1=4 d1=1 | GF(2^4) | 40 | 40 | 0 | 40 | 3/3 |
| (0,1,9,10) | B0=4 B1=5 d1=1 | GF(32003) | 20 | 20 | 0 | 20 | 3/3 |
| (0,1,9,10) | B0=4 B1=5 d1=1 | GF(2) | 40 | 7 | 33 | 7 | 3/3 |
| (0,1,9,10) | B0=4 B1=5 d1=1 | GF(2^2) | 40 | 26 | 14 | 26 | 3/3 |
| (0,1,9,10) | B0=4 B1=5 d1=1 | GF(2^4) | 40 | 37 | 3 | 37 | 3/3 |
| (0,1,11,12) | B0=5 B1=6 d1=1 | GF(32003) | 20 | 20 | 0 | 20 | 3/3 |
| (0,1,11,12) | B0=5 B1=6 d1=1 | GF(2) | 40 | 6 | 34 | 6 | 3/3 |
| (0,1,11,12) | B0=5 B1=6 d1=1 | GF(2^2) | 40 | 27 | 13 | 27 | 3/3 |
| (0,1,11,12) | B0=5 B1=6 d1=1 | GF(2^4) | 40 | 35 | 5 | 35 | 3/3 |
| (0,3,5,8) | B0=1 B1=4 d1=3 | GF(32003) | 20 | 20 | 0 | 20 | 3/3 |
| (0,3,5,8) | B0=1 B1=4 d1=3 | GF(2) | 40 | 18 | 22 | 3 | 3/3 |
| (0,3,5,8) | B0=1 B1=4 d1=3 | GF(2^2) | 40 | 31 | 9 | 19 | 3/3 |
| (0,3,5,8) | B0=1 B1=4 d1=3 | GF(2^4) | 40 | 40 | 0 | 33 | 3/3 |
| (0,5,7,12) | B0=1 B1=6 d1=5 | GF(32003) | 20 | 20 | 0 | 0 | 0/0 |
| (0,5,7,12) | B0=1 B1=6 d1=5 | GF(2) | 40 | 36 | 4 | 0 | 0/0 |
| (0,5,7,12) | B0=1 B1=6 d1=5 | GF(2^2) | 40 | 40 | 0 | 0 | 0/0 |
| (0,5,7,12) | B0=1 B1=6 d1=5 | GF(2^4) | 40 | 40 | 0 | 0 | 0/0 |
| (0,3,9,12) | B0=1 B1=2 d1=3 | GF(32003) | 20 | 20 | 0 | 20 | 3/3 |
| (0,3,9,12) | B0=1 B1=2 d1=3 | GF(2) | 40 | 0 | 40 | 0 | 0/0 |
| (0,3,9,12) | B0=1 B1=2 d1=3 | GF(2^2) | 40 | 0 | 40 | 0 | 0/0 |
| (0,3,9,12) | B0=1 B1=2 d1=3 | GF(2^4) | 40 | 0 | 40 | 0 | 0/0 |
| (0,2,10,12) | B0=2 B1=3 d1=2 | GF(32003) | 20 | 20 | 0 | 20 | 3/3 |
| (0,2,10,12) | B0=2 B1=3 d1=2 | GF(2) | 40 | 0 | 40 | 0 | 0/0 |
| (0,2,10,12) | B0=2 B1=3 d1=2 | GF(2^2) | 40 | 0 | 40 | 0 | 0/0 |
| (0,2,10,12) | B0=2 B1=3 d1=2 | GF(2^4) | 40 | 0 | 40 | 0 | 0/0 |

Primitive tables of the eight rays: (0,1,5,6): (0, d=0, 2); (1, d=1, 3); (2, d=5, 3); (3, d=6, 2); (0,1,7,8): (0, d=0, 3); (1, d=1, 4); (2, d=7, 4); (3, d=8, 3); (0,1,9,10): (0, d=0, 4); (1, d=1, 5); (2, d=9, 5); (3, d=10, 4); (0,1,11,12): (0, d=0, 5); (1, d=1, 6); (2, d=11, 6); (3, d=12, 5); (0,3,5,8): (0, d=0, 1); (1, d=3, 4); (2, d=5, 4); (3, d=8, 1); (0,5,7,12): (0, d=0, 1); (1, d=5, 6); (2, d=7, 6); (3, d=12, 1); (0,3,9,12): (0, d=0, 1); (1, d=3, 2); (2, d=9, 2); (3, d=12, 1); (0,2,10,12): (0, d=0, 2); (1, d=2, 3); (2, d=10, 3); (3, d=12, 2).

Finite non-pure tables over GF(32003) (what the generic presentation gives when the ray is not hit):

- ray (0,5,7,12): (0, d=0, 1); (1, d=5, 6); (2, d=7, 4); (2, d=8, 3); (2, d=9, 2); (3, d=10, 4) x 20

Comparison with the predictions: over GF(32003) the rays hit are [(0, 1, 5, 6), (0, 1, 7, 8), (0, 1, 9, 10), (0, 1, 11, 12), (0, 3, 5, 8), (0, 3, 9, 12), (0, 2, 10, 12)] and the rays not hit are [(0, 5, 7, 12)] (prediction: every ray hit except possibly (0,3,9,12) and the (1,6,6,1) ray (0,5,7,12)). In characteristic 2: rays with at least one hit over GF(2): [(0, 1, 5, 6), (0, 1, 7, 8), (0, 1, 9, 10), (0, 1, 11, 12), (0, 3, 5, 8)]; over GF(4): [(0, 1, 5, 6), (0, 1, 7, 8), (0, 1, 9, 10), (0, 1, 11, 12), (0, 3, 5, 8)]; over GF(16): [(0, 1, 5, 6), (0, 1, 7, 8), (0, 1, 9, 10), (0, 1, 11, 12), (0, 3, 5, 8)]. Rays with no hit over GF(2), GF(4), GF(16) respectively: [(0, 5, 7, 12), (0, 3, 9, 12), (0, 2, 10, 12)]; [(0, 5, 7, 12), (0, 3, 9, 12), (0, 2, 10, 12)]; [(0, 5, 7, 12), (0, 3, 9, 12), (0, 2, 10, 12)]. (0,2,10,12) has hits in characteristic 2: False. Rays with odd d1 ((0,1,*), (0,3,5,8), (0,3,9,12), (0,5,7,12)) hit in characteristic 2: {'GF(2)': [(0, 1, 5, 6), (0, 1, 7, 8), (0, 1, 9, 10), (0, 1, 11, 12), (0, 3, 5, 8)], 'GF(2^2)': [(0, 1, 5, 6), (0, 1, 7, 8), (0, 1, 9, 10), (0, 1, 11, 12), (0, 3, 5, 8)], 'GF(2^4)': [(0, 1, 5, 6), (0, 1, 7, 8), (0, 1, 9, 10), (0, 1, 11, 12), (0, 3, 5, 8)]}.
Rays hit over GF(32003) and not hit over GF(2), GF(4), GF(16) in the 40 seeds each: [(0, 3, 9, 12), (0, 2, 10, 12)]. By the hypothesis's own consequence rule such a ray is a candidate for a characteristic-dependent point and needs a proof before any claim; for these rays every one of the 40 random presentations per field had a nonzero quotient in every degree up to the bound (columns 'finite' = 0).

A ray not hit over GF(32003) is, per the hypothesis, not reachable by generic presentations and its characteristic 2 outcome is not interpreted. No statement of non-realizability is made for any ray.

## C1 proof steps for M_e = U/U(x^e, y^e), e = 2..8

| e | field | length | Hilbert series = product formula | (weight, degree) pieces = D_q(n') | nonzero pieces | ker y = span of z^c g_a | all z^c g_a in ker y | socle {(degree,weight): dim} | socle = weight 0, degree 4e-4, dim 1 | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | QQ | 8 | True | True | 7 | True | True | {'4,0': 1} | True | 0.0 |
| 2 | GF(32003) | 8 | True | True | 7 | True | True | {'4,0': 1} | True | 0.0 |
| 3 | QQ | 27 | True | True | 19 | True | True | {'8,0': 1} | True | 0.1 |
| 3 | GF(32003) | 27 | True | True | 19 | True | True | {'8,0': 1} | True | 0.1 |
| 4 | QQ | 64 | True | True | 37 | True | True | {'12,0': 1} | True | 0.3 |
| 4 | GF(32003) | 64 | True | True | 37 | True | True | {'12,0': 1} | True | 0.1 |
| 5 | QQ | 125 | True | True | 61 | True | True | {'16,0': 1} | True | 0.9 |
| 5 | GF(32003) | 125 | True | True | 61 | True | True | {'16,0': 1} | True | 0.2 |
| 6 | QQ | 216 | True | True | 91 | True | True | {'20,0': 1} | True | 2.5 |
| 6 | GF(32003) | 216 | True | True | 91 | True | True | {'20,0': 1} | True | 0.3 |
| 7 | QQ | 343 | True | True | 127 | True | True | {'24,0': 1} | True | 5.1 |
| 7 | GF(32003) | 343 | True | True | 127 | True | True | {'24,0': 1} | True | 0.6 |
| 8 | QQ | 512 | True | True | 169 | True | True | {'28,0': 1} | True | 12.6 |
| 8 | GF(32003) | 512 | True | True | 169 | True | True | {'28,0': 1} | True | 0.8 |

The QQ rows are the claim; the GF(32003) rows are the same computation over a prime field (the numpy build) and are listed as a second field, not a substitute. All QQ computations ran exactly (Fractions), including e = 7 and e = 8. The weight of a PBW monomial x^a y^b z^c is b - a. The kernel of y is compared degree by degree: the span of the classes of z^c g_a (a < e, g_a as in step 5 of the note, reordered into the PBW basis) against the kernel of the matrix of y.

Comparison with the prediction (C1 holds for every e <= 8): over QQ the four statements (weight pieces = D_q(n'), kernel of y = span of z^c g_a, socle one-dimensional of weight 0 and degree 4e-4, Hilbert series = product formula) are all True for e = [2, 3, 4, 5, 6, 7, 8]: True. This is a finite check of the derivation for e <= 8, not the proof.

## C2 k[z]-structure of M_e, e = 2..5, QQ

| e | length | k[z]-generators | (generator degree, length) multiset = pattern | lengths found | lengths predicted |
|---|---|---|---|---|---|
| 2 | 8 | 4 | True | {'1': 1, '2': 2, '3': 1} | {'1': 1, '2': 2, '3': 1} |
| 3 | 27 | 9 | True | {'1': 1, '2': 2, '3': 3, '4': 2, '5': 1} | {'1': 1, '2': 2, '3': 3, '4': 2, '5': 1} |
| 4 | 64 | 16 | True | {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3, '6': 2, '7': 1} | {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3, '6': 2, '7': 1} |
| 5 | 125 | 25 | True | {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 4, '7': 3, '8': 2, '9': 1} | {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 4, '7': 3, '8': 2, '9': 1} |

- e = 2, blocks (generator degree g, length L, multiplicity) of the summands k[z]/(z^L)(-g): [[0, 3, 1], [1, 2, 2], [2, 1, 1]]
- e = 3, blocks (generator degree g, length L, multiplicity) of the summands k[z]/(z^L)(-g): [[0, 5, 1], [1, 4, 2], [2, 3, 3], [3, 2, 2], [4, 1, 1]]
- e = 4, blocks (generator degree g, length L, multiplicity) of the summands k[z]/(z^L)(-g): [[0, 7, 1], [1, 6, 2], [2, 5, 3], [3, 4, 4], [4, 3, 3], [5, 2, 2], [6, 1, 1]]
- e = 5, blocks (generator degree g, length L, multiplicity) of the summands k[z]/(z^L)(-g): [[0, 9, 1], [1, 8, 2], [2, 7, 3], [3, 6, 4], [4, 5, 5], [5, 4, 4], [6, 3, 3], [7, 2, 2], [8, 1, 1]]

Comparison with the prediction (pattern holds): the (generator degree, length) multiset equals the pattern for e in [2, 3, 4, 5] of 2..5.

The pattern: one summand k[z]/(z^(2e-1-a-b)) for each a, b < e, generated in degree a + b (the hypothesis fixes the lengths; the generator degree a + b is the degree of x^a y^b and is how the comparison above reads the pattern, together with the lengths alone).

## C3 characteristics, e = 2..5, primes p <= 23

### e = 2

Predicted bad primes <= 23 (p divides (2e-1)! or a tableau count of the rectangle (e-w) x k, entries <= e): [2, 3]. Observed primes with a non-pure quotient: [2, 3]. Observed subset of predicted: True. Observed equals predicted: True.

| p | predicted bad | length | Hilbert function (to the bound) | I1 table | pure (I1) | I2 agrees |
|---|---|---|---|---|---|---|
| 2 | True | nonzero at bound 16 | [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] | - | False | Hilbert via I2 table: True |
| 3 | True | nonzero at bound 16 | [1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1] | - | False | Hilbert via I2 table: True |
| 5 | False | finite 8 | [1, 2, 2, 2, 1] | (0, d=0, 1); (1, d=2, 2); (2, d=6, 2); (3, d=8, 1) | True | True |
| 7 | False | finite 8 | [1, 2, 2, 2, 1] | (0, d=0, 1); (1, d=2, 2); (2, d=6, 2); (3, d=8, 1) | True | True |
| 11 | False | finite 8 | [1, 2, 2, 2, 1] | (0, d=0, 1); (1, d=2, 2); (2, d=6, 2); (3, d=8, 1) | True | True |
| 13 | False | finite 8 | [1, 2, 2, 2, 1] | (0, d=0, 1); (1, d=2, 2); (2, d=6, 2); (3, d=8, 1) | True | True |
| 17 | False | finite 8 | [1, 2, 2, 2, 1] | (0, d=0, 1); (1, d=2, 2); (2, d=6, 2); (3, d=8, 1) | True | True |
| 19 | False | finite 8 | [1, 2, 2, 2, 1] | (0, d=0, 1); (1, d=2, 2); (2, d=6, 2); (3, d=8, 1) | True | True |
| 23 | False | finite 8 | [1, 2, 2, 2, 1] | (0, d=0, 1); (1, d=2, 2); (2, d=6, 2); (3, d=8, 1) | True | True |

Reasons (per prime): 2: (2e-1)!, tableaux(w=1,k=1)=2; 3: (2e-1)!, tableaux(w=1,k=2)=3

### e = 3

Predicted bad primes <= 23 (p divides (2e-1)! or a tableau count of the rectangle (e-w) x k, entries <= e): [2, 3, 5]. Observed primes with a non-pure quotient: [2, 3, 5]. Observed subset of predicted: True. Observed equals predicted: True.

| p | predicted bad | length | Hilbert function (to the bound) | I1 table | pure (I1) | I2 agrees |
|---|---|---|---|---|---|---|
| 2 | True | nonzero at bound 20 | [1, 2, 4, 4, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4] | - | False | Hilbert via I2 table: True |
| 3 | True | nonzero at bound 20 | [1, 2, 4, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5] | - | False | Hilbert via I2 table: True |
| 5 | True | nonzero at bound 20 | [1, 2, 4, 4, 5, 4, 4, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3] | - | False | Hilbert via I2 table: True |
| 7 | False | finite 27 | [1, 2, 4, 4, 5, 4, 4, 2, 1] | (0, d=0, 1); (1, d=3, 2); (2, d=9, 2); (3, d=12, 1) | True | True |
| 11 | False | finite 27 | [1, 2, 4, 4, 5, 4, 4, 2, 1] | (0, d=0, 1); (1, d=3, 2); (2, d=9, 2); (3, d=12, 1) | True | True |
| 13 | False | finite 27 | [1, 2, 4, 4, 5, 4, 4, 2, 1] | (0, d=0, 1); (1, d=3, 2); (2, d=9, 2); (3, d=12, 1) | True | True |
| 17 | False | finite 27 | [1, 2, 4, 4, 5, 4, 4, 2, 1] | (0, d=0, 1); (1, d=3, 2); (2, d=9, 2); (3, d=12, 1) | True | True |
| 19 | False | finite 27 | [1, 2, 4, 4, 5, 4, 4, 2, 1] | (0, d=0, 1); (1, d=3, 2); (2, d=9, 2); (3, d=12, 1) | True | True |
| 23 | False | finite 27 | [1, 2, 4, 4, 5, 4, 4, 2, 1] | (0, d=0, 1); (1, d=3, 2); (2, d=9, 2); (3, d=12, 1) | True | True |

Reasons (per prime): 2: (2e-1)!, tableaux(w=1,k=2)=6, tableaux(w=1,k=3)=10 ...; 3: (2e-1)!, tableaux(w=1,k=1)=3, tableaux(w=1,k=2)=6 ...; 5: (2e-1)!, tableaux(w=1,k=3)=10, tableaux(w=2,k=3)=10

### e = 4

Predicted bad primes <= 23 (p divides (2e-1)! or a tableau count of the rectangle (e-w) x k, entries <= e): [2, 3, 5, 7]. Observed primes with a non-pure quotient: [2, 3, 5, 7]. Observed subset of predicted: True. Observed equals predicted: True.

| p | predicted bad | length | Hilbert function (to the bound) | I1 table | pure (I1) | I2 agrees |
|---|---|---|---|---|---|---|
| 2 | True | nonzero at bound 24 | [1, 2, 4, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8] | - | False | Hilbert via I2 table: True |
| 3 | True | nonzero at bound 24 | [1, 2, 4, 6, 7, 8, 8, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7] | - | False | Hilbert via I2 table: True |
| 5 | True | nonzero at bound 24 | [1, 2, 4, 6, 7, 8, 8, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7] | - | False | Hilbert via I2 table: True |
| 7 | True | nonzero at bound 24 | [1, 2, 4, 6, 7, 8, 8, 8, 7, 6, 4, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3] | - | False | Hilbert via I2 table: True |
| 11 | False | finite 64 | [1, 2, 4, 6, 7, 8, 8, 8, 7, 6, 4, 2, 1] | (0, d=0, 1); (1, d=4, 2); (2, d=12, 2); (3, d=16, 1) | True | True |
| 13 | False | finite 64 | [1, 2, 4, 6, 7, 8, 8, 8, 7, 6, 4, 2, 1] | (0, d=0, 1); (1, d=4, 2); (2, d=12, 2); (3, d=16, 1) | True | True |
| 17 | False | finite 64 | [1, 2, 4, 6, 7, 8, 8, 8, 7, 6, 4, 2, 1] | (0, d=0, 1); (1, d=4, 2); (2, d=12, 2); (3, d=16, 1) | True | True |
| 19 | False | finite 64 | [1, 2, 4, 6, 7, 8, 8, 8, 7, 6, 4, 2, 1] | (0, d=0, 1); (1, d=4, 2); (2, d=12, 2); (3, d=16, 1) | True | True |
| 23 | False | finite 64 | [1, 2, 4, 6, 7, 8, 8, 8, 7, 6, 4, 2, 1] | (0, d=0, 1); (1, d=4, 2); (2, d=12, 2); (3, d=16, 1) | True | True |

Reasons (per prime): 2: (2e-1)!, tableaux(w=1,k=1)=4, tableaux(w=1,k=2)=10 ...; 3: (2e-1)!, tableaux(w=2,k=1)=6, tableaux(w=2,k=4)=105; 5: (2e-1)!, tableaux(w=1,k=2)=10, tableaux(w=1,k=3)=20 ...; 7: (2e-1)!, tableaux(w=1,k=4)=35, tableaux(w=2,k=4)=105 ...

### e = 5

Predicted bad primes <= 23 (p divides (2e-1)! or a tableau count of the rectangle (e-w) x k, entries <= e): [2, 3, 5, 7]. Observed primes with a non-pure quotient: [2, 3, 5, 7]. Observed subset of predicted: True. Observed equals predicted: True.

| p | predicted bad | length | Hilbert function (to the bound) | I1 table | pure (I1) | I2 agrees |
|---|---|---|---|---|---|---|
| 2 | True | nonzero at bound 28 | [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12] | - | False | Hilbert via I2 table: True |
| 3 | True | nonzero at bound 28 | [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12] | - | False | Hilbert via I2 table: True |
| 5 | True | nonzero at bound 28 | [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13] | - | False | Hilbert via I2 table: True |
| 7 | True | nonzero at bound 28 | [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11] | - | False | Hilbert via I2 table: True |
| 11 | False | finite 125 | [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 10, 9, 6, 4, 2, 1] | (0, d=0, 1); (1, d=5, 2); (2, d=15, 2); (3, d=20, 1) | True | True |
| 13 | False | finite 125 | [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 10, 9, 6, 4, 2, 1] | (0, d=0, 1); (1, d=5, 2); (2, d=15, 2); (3, d=20, 1) | True | True |
| 17 | False | finite 125 | [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 10, 9, 6, 4, 2, 1] | (0, d=0, 1); (1, d=5, 2); (2, d=15, 2); (3, d=20, 1) | True | True |
| 19 | False | finite 125 | [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 10, 9, 6, 4, 2, 1] | (0, d=0, 1); (1, d=5, 2); (2, d=15, 2); (3, d=20, 1) | True | True |
| 23 | False | finite 125 | [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 10, 9, 6, 4, 2, 1] | (0, d=0, 1); (1, d=5, 2); (2, d=15, 2); (3, d=20, 1) | True | True |

Reasons (per prime): 2: (2e-1)!, tableaux(w=1,k=4)=70, tableaux(w=1,k=5)=126 ...; 3: (2e-1)!, tableaux(w=1,k=2)=15, tableaux(w=1,k=5)=126 ...; 5: (2e-1)!, tableaux(w=1,k=1)=5, tableaux(w=1,k=2)=15 ...; 7: (2e-1)!, tableaux(w=1,k=3)=35, tableaux(w=1,k=4)=70 ...

## D1 genericity: random pairs of forms of degree e over GF(32003)

| e | pairs | max-rank Hilbert function (first non-positive coefficient cut) | all pairs have it | pure tables | Betti table of pair 1 (I1) | I1=I2 (pairs with I2) |
|---|---|---|---|---|---|---|
| 2 | 5 | [1, 2, 2, 2, 1] | True | 5 | (0, d=0, 1); (1, d=2, 2); (2, d=6, 2); (3, d=8, 1) | 5/5 |
| 3 | 5 | [1, 2, 4, 4, 5, 4, 4, 2, 1] | True | 5 | (0, d=0, 1); (1, d=3, 2); (2, d=9, 2); (3, d=12, 1) | 5/5 |
| 4 | 5 | [1, 2, 4, 6, 7, 8, 8, 8, 7, 6, 4, 2] | True | 0 | (0, d=0, 1); (1, d=4, 2); (2, d=12, 1); (2, d=13, 2); (3, d=15, 2) | 5/5 |
| 5 | 5 | [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 10, 9, 6, 4] | True | 0 | (0, d=0, 1); (1, d=5, 2); (2, d=16, 3); (2, d=17, 2); (3, d=18, 4) | 5/5 |
| 10 | 5 | [1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 34, 38, 41, 44, 46, 48, 49, 50, 50, 50, 49, 48, 46, 44, 41, 38, 34, 30, 25, 20, 14, 8, 1] | True | 0 | (0, d=0, 1); (1, d=10, 2); (2, d=33, 6); (2, d=34, 2); (3, d=35, 6); (3, d=36, 1) | 1/1 |

Outcome by e: e = 2: maximal-rank Hilbert function in 5 of 5 pairs, pure table in 5 of 5; e = 3: maximal-rank Hilbert function in 5 of 5 pairs, pure table in 5 of 5; e = 4: maximal-rank Hilbert function in 5 of 5 pairs, pure table in 0 of 5; e = 5: maximal-rank Hilbert function in 5 of 5 pairs, pure table in 0 of 5; e = 10: maximal-rank Hilbert function in 5 of 5 pairs, pure table in 0 of 5.

Comparison with the prediction (D1: maximal-rank Hilbert function and a non-pure table for e = 4, 5, 10; a pure table for e = 2, 3): see the columns 'all pairs have it' and 'pure tables'. The pair counts (5 per e) are a choice of the run; the hypothesis says 'random pairs'.

## D2 the ray (0,3,15,18), table (2,3,3,2)

10 random 2 by 3 matrices of cubics over GF(32003): pure table (2,3,3,2) on (0,3,15,18) for 10 of 10. Pure Hilbert function of the ray: [2, 4, 8, 9, 12, 12, 14, 13, 14, 12, 12, 9, 8, 4, 2].

| seed | length | I1 table | I2 table | agree | pure | Hilbert = pure prediction |
|---|---|---|---|---|---|---|
| 800001 | 135 | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | True | True | True |
| 800002 | 135 | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | True | True | True |
| 800003 | 135 | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | True | True | True |
| 800004 | 135 | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | True | True | True |
| 800005 | 135 | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | - | None | True | True |
| 800006 | 135 | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | - | None | True | True |
| 800007 | 135 | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | - | None | True | True |
| 800008 | 135 | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | - | None | True | True |
| 800009 | 135 | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | - | None | True | True |
| 800010 | 135 | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | - | None | True | True |

Presentation of the Kostant module L(1,1) from `uhlib`: generator degrees [0, 0], 3 relations with entry degrees [1]:

- 1 * [gen 0] x^1 y^0 z^0
- 1 * [gen 1] x^0 y^1 z^0
- 1 * [gen 0] x^0 y^1 z^0 + 1 * [gen 1] x^1 y^0 z^0

Substituting x -> x^e, y -> y^e in every entry (over GF(32003)):

| e | target ray | length | Hilbert function | I1 table | I2 table | agree | pure on the target ray |
|---|---|---|---|---|---|---|---|
| 2 | (0, 2, 10, 12) | 40 | [2, 4, 5, 6, 6, 6, 5, 4, 2] | (0, d=0, 2); (1, d=2, 3); (2, d=10, 3); (3, d=12, 2) | (0, d=0, 2); (1, d=2, 3); (2, d=10, 3); (3, d=12, 2) | True | True |
| 3 | (0, 3, 15, 18) | 135 | [2, 4, 8, 9, 12, 12, 14, 13, 14, 12, 12, 9, 8, 4, 2] | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | (0, d=0, 2); (1, d=3, 3); (2, d=15, 3); (3, d=18, 2) | True | True |


## Instrument agreement

Betti tables compared between I1 and I2 on finite length modules: agree True = 127, False = 0, not compared (I2 on a module not finite by the bound: only the Hilbert function from the I2 table is compared) = 23, I2 errors = 0. Hilbert function recomputed from the I2 table equals I1's: {True: 140, 'A-check True': 40}.

## Wall times

Summed task seconds per claim (processes ran in parallel): A1 122 s, A2 366 s, B1 552 s, C1 24 s, C2 1 s, C3 37 s, D1 165 s, D2 19 s. Total wall time 151.5 s.

## Deviations and choices not fixed by the hypothesis

- A numpy build of the quotient module (`uhlib/fastmod.py`, same reduced echelon rule, tested equal to `quotient_module`) is the I1 build for prime fields and GF(2^k); the pure Python build is used for QQ. Without it the B1 search over GF(16) (about 10 minutes per module in pure Python) was not feasible.
- A1, A2: Hilbert functions come from the numpy build without module action; on 10 subspaces per field they are also computed by the pure Python `ideal_hilbert` and recomputed from the Singular Betti table (through degree 12). The ten indices are fixed by `random.Random(31 + k).sample`.
- B1: 20 seeds over GF(32003), 40 over GF(2), GF(4), GF(16); seeds are 1000000 (ray index + 1) + 1000 q + s. At most three hits per ray and field get an I2 run; all other tables are I1 only.
- C2: the hypothesis fixes the lengths of the summands; the generator degree a + b is an addition of this run.
- C3: the predicted set is computed over 0 <= w < e, 1 <= k <= e as the hypothesis states, with p <= 23.
- D1: five random pairs per e; I2 on every pair for e <= 5 and on the first pair for e = 10. D2(b): the substituted modules were built over GF(32003) only (not QQ).
- No statement about the realizability or non-realizability of any ray is made from these runs.

