# Characteristic 2: a presentation with at most one more relation than generators, in one degree e >= 2, never gives a finite length module over U(H)

Date: 2026-11-19. Status: derivation [D] by the coordinating session, written after EXP-003, and reviewed on 2026-11-19
by a reader other than the writer (independent re-derivation of every step and an independent machine check with its
own code; record `bs-char2-general-review-2026-11-19` in the coordination repository; verdict: correct after wording
fixes, no blocker, no major finding; all fixes are applied in this revision, and the proof of the last section and the
remark that the quadric splits over k are the reviewer's). It generalizes the statement of EXP-003 (pairs of quadrics)
and explains its three observations on the rays (0,2,6,8), (0,3,9,12) and (0,2,10,12).

## Statement

Let k be a field of characteristic 2 and U = U(H) = k<x,y,z>/(xy - yx - z, z central), deg x = deg y = 1, deg z = 2.

Theorem. Let e >= 2, a >= 1 and 0 <= b <= a + 1, and let F_1, ..., F_b in (U_e)^a be arbitrary (possibly zero or
dependent). Then the left module M = U^a / (U F_1 + ... + U F_b) has infinite length. More precisely the part of M of
the parity of e (step 2) has Krull dimension at least 1 over the centre. The same holds for right modules (through the
anti-automorphism that fixes x and y).

Corollary 1. For every e >= 2 and every two forms f, g of degree e, U/(Uf + Ug) has infinite length. So over a field of
characteristic 2 the primitive point (1,2,2,1) of the ray (0, e, 3e, 4e) is the Betti table of no finite length module
over U(H), for every e >= 2; it is the Betti table of no finite length module over k[x,y,z] in any characteristic (two
forms cannot cut out a finite length quotient); and in characteristic 0 it is realized over U(H) by U/U(x^e, y^e) for
every e (the family of the other context note). The answer to Question 6.1 of Erman and Sam on these points depends on
the characteristic for every e >= 2. Question 6.1 already has a negative answer in general, by a parity obstruction on
the Hilbert series (Jiang, Li, Sun, Wang, Xiao and Yu, arXiv:2605.25259, Theorem 3.7); the points here satisfy that
test, are realized in characteristic 0, and are excluded in characteristic 2 by the structure of U(H).

Corollary 2. In characteristic 2 a primitive point with beta_1 = beta_0 + 1 on a ray with d1 >= 2 is realizable over
neither ring (over k[x,y,z] a finite length module has beta_1 >= beta_0 + 2). Of the degree sequences with d3 <= 12,
eight have a primitive point with beta_1 = beta_0 + 1, all passing the parity test: five with d1 = 1 and the three rays
(0,2,6,8), (0,3,9,12) (table (1,2,2,1)) and (0,2,10,12) (table (2,3,3,2)), which are the three rays on which the
searches of EXP-003 never found a finite length module in characteristic 2.

Both hypotheses are sharp. With e = 1: U/(Ux + Uy) = k, and the points on rays with d1 = 1 are realized in
characteristic 2 (EXP-003, claim B1). With b = a + 2: three general forms of degree 2, or of degree 3, give a finite
length quotient in characteristic 2 (Hilbert functions (1,2,1) and (1,2,4,3,3) in the reviewer's runs over GF(16)).

## Step 1: the centre and the two parities (characteristic 2)

x^2, y^2 and z are central (x^2 y - y x^2 = 2xz, y^2 x - x y^2 = -2yz), C = k[X, Y, Z] with X = x^2, Y = y^2, Z = z is a
polynomial ring, and U is free over C on 1, x, y, yx (EXP-003, addendum 1 of the verdict). Left multiplication on that
basis, from xy = yx + z:

    x.x = X      x.y = yx + Z      x.yx = X y + Z x
    y.x = yx     y.y = Y           y.yx = Y x
    yx.x = X y   yx.y = Y x + Z y  yx.yx = XY + Z yx

Put U+ = C + C yx (the even part) and U- = C x + C y (the odd part); C lies in even degrees. Left multiplication by yx
preserves each part, and left multiplication by x or y exchanges them. On U+ in the basis (1, yx), and on U- in the
basis (x, y), left multiplication by yx is the C-linear map with matrix

    T+ = [[0, XY], [1, Z]]        T- = [[0, Y], [X, Z]]

(columns are the images of the basis vectors), and both satisfy t^2 = Z t + XY.

## Step 2: one parity of M is a module over a quadric

Let B = C[t]/(t^2 + Z t + XY). Give X, Y, Z, t degree 1 (so the degree in U is twice this degree, plus the degree of
the basis element). B is a graded hypersurface domain of dimension 3, free over C on 1, t. With u = t and v = t + Z the
equation is uv = XY, so Sigma = Proj B is the Segre quadric P^1 x P^1 over k itself (no extension of k is needed), with
O(1) = O(1,1); it is smooth (the partial derivatives of t^2 + Zt + XY are Z, t, Y, X).

Through the action of yx, U+ and U- are graded B-modules. U+ is free of rank 1 on the vector 1 (T+ sends (1,0) to
(0,1)), with alpha + beta yx corresponding to alpha + beta t. U- is not free. Right multiplication by x,
phi(alpha x + beta y) = alpha X + beta yx = X alpha + t beta, commutes with the left action, so it is B-linear; it is
injective with image the ideal J = (X, t) = XC + tC. Right multiplication by y gives a second embedding,
alpha x + beta y to (t + Z) alpha + Y beta, with image J' = (t + Z, Y). J and J' are the ideals of two disjoint lines of
the same ruling of Sigma (X = t = 0 and Y = t + Z = 0 have only the origin in common), and phi raises the degree by 1,
so U- = J(1) and the sheaf N- of U- on Sigma is the line bundle O(1)(-line) = O(0,1) for that ruling. N+ = O.

Let e = 2m (even) or e = 2m + 1 (odd); m >= 1 exactly when e >= 2. If e is even every entry of F_j lies in U+ and has
the form alpha + beta yx with alpha of degree m and beta of degree m - 1 in X, Y, Z; if e is odd every entry lies in U-
and has the form alpha x + beta y with alpha, beta of degree m. Write P for the part of U that contains the entries
(U+ or U-) and P^a for the corresponding part of U^a. Since C is central, U F_j = C F_j + C x F_j + C y F_j + C yx F_j;
F_j and yx F_j lie in P^a, the other two in the other parity; so the part of the sum of the U F_j in P^a is the sum of
the B F_j, and M is the direct sum, as a graded C-module, of

    M_P = P^a / (B F_1 + ... + B F_b)

and the quotient of the other parity. M_P is a graded B-module. If M has finite length, so has M_P.

## Step 3: M_P is not of finite length

Write L = N(m), that is L = O(m, m) for e even and L = O(m, m + 1) for e odd, and let

    psi: O^b to L^(+a)   (direct sum of a copies of L)

be the map of sheaves on Sigma given by F_1, ..., F_b. Its cokernel is the sheaf of M_P twisted by m. A finitely
generated graded B-module of finite length is killed by a power of the irrelevant ideal, so its sheaf is 0. Hence, if
M_P has finite length, psi is surjective at every point of Sigma. Both bidegrees of L are positive because m >= 1, so
L is ample and L.L = 2m^2 (e even) or 2m(m + 1) (e odd) is positive.

- b < a: a surjection from a bundle of smaller rank does not exist.
- b = a: psi is an isomorphism, so its determinant gives O = L^(tensor a), impossible for an ample L.
- b = a + 1: the kernel K of psi is a line bundle and 0 to K to O^(a+1) to L^(+a) to 0 is exact, so
  c(K) c(L^(+a)) = 1 with c(L^(+a)) = 1 + a L + binom(a, 2) L.L. In degree 1, c_1(K) = -a L; in degree 2,
  binom(a, 2) L.L + (a L).(-a L) = -(a(a + 1)/2) L.L = 0, impossible.

Hence psi is not surjective at some point of Sigma, the sheaf of M_P is not zero, the Krull dimension of M_P is at
least 1, and M is not of finite length. The point can be taken on Sigma over k; nothing uses the size of k. For a = 1
and b = 2 this is the statement that two curves of the same ample class on P^1 x P^1 meet.

For e even there is a proof without sheaves: M_P = coker(B(-m)^b to B^a), whose support is V(I_a) with I_a the ideal of
the a by a minors (zero if b < a). I_a is generated by forms of degree am > 0, so it is a proper ideal, of height at
most max(0, b - a + 1) <= 2 by the theorem of Eagon and Northcott, while the irrelevant ideal has height 3; so I_a is
not primary to it and M_P is not of finite length.

Where the argument stops: with e = 1 (m = 0, odd) L = O(0,1) has L.L = 0 and two sections of it need not meet (the
trivial module); with b = a + 2 the expected codimension of the degeneracy locus is 3 and a general presentation has
finite length (the statement above).

## Step 4: the corollaries

N(t) = 1 - 2t^e + 2t^(3e) - t^(4e) vanishes to order 3 at t = 1 and vanishes at t = -1, so a module with Betti table
(1,2,2,1) on (0, e, 3e, 4e) has a polynomial Hilbert series and finite length; it is cyclic with two relations of degree
e, that is U/(Uf + Ug): excluded by the theorem with a = 1, b = 2. In general a module with a pure table on
(0, d1, d2, d3) with beta_0 = a and beta_1 = b is U^a modulo b elements of degree d1; Question 6.1 asks for finite
length modules, and the theorem excludes a finite length module with b <= a + 1 and d1 >= 2 in characteristic 2.

## The eventual Hilbert function of a general presentation

Let D be the locus where psi is not surjective. When D is finite and psi has corank at most 1 at each of its points
(automatic for a = 1), the cokernel of psi is locally cyclic, of length the degree of D with its determinantal
structure, which is L.L for a = 1 and, by the formula of Thom and Porteous for the corank one locus of
O^(a+1) to L^(+a), c_1^2 - c_2 = (a(a + 1)/2) L.L in general (the same number that obstructs surjectivity in step 3).
Reducedness is not needed. So dim (M_P)_n = (a(a + 1)/2) L.L for large n.

The other parity has the same eventual dimension (the reviewer's argument). The odd elements x, y and x + y have the
central squares X, Y and X + Y + Z, with no common zero on Proj C. Each odd element w satisfies w t = (t + Z) w
(x.yx = (yx + Z) x and y.yx = (yx + Z) y), so w b = sigma(b) w for the involution sigma of B that fixes C and sends t to
t + Z (it exchanges the two rulings). Where w^2 does not vanish, left multiplication by w is a sigma-semilinear
isomorphism between the localizations of the two parities of any graded U-module, with inverse w^(-2) w. Hence the
sheaves of the two parities have the same length and the Hilbert function of M is eventually the number above in every
degree.

| presentation | e | m | predicted eventual value | observed in characteristic 2 |
|---|---|---|---|---|
| two quadrics (ray (0,2,6,8)) | 2 | 1 | 2 m^2 = 2 | 2 on 29 of the 35 subspaces over GF(2) (linear growth on the other 6) |
| two cubics (ray (0,3,9,12)) | 3 | 1 | 2 m (m + 1) = 4 | 4 on 530 of all 651 subspaces over GF(2) (linear growth on 121); 34 of 40, 39 of 40, 40 of 40 random pairs over GF(2), GF(4), GF(16) in EXP-003 |
| two quartics | 4 | 2 | 8 | 8 wherever the value is constant (reviewer: 120 random pairs per field over GF(2), GF(4), GF(16)) |
| two quintics | 5 | 2 | 12 | 12 wherever the value is constant (same sample sizes) |
| 2 by 3 matrix of quadrics (ray (0,2,10,12)) | 2 | 1 | 3 . 2 = 6 | 6 on 28 of 40, 39 of 40, 40 of 40 seeds over GF(2), GF(4), GF(16) in EXP-003 |
| 2 by 3 matrix of cubics (ray (0,3,15,18)) | 3 | 1 | 3 . 4 = 12 | 12 wherever the value is constant (reviewer: 20 per field) |

No presentation of finite length was found in any of these runs (the reviewer's code is independent of `uhlib` and
agrees with it on 40 presentations). The first three values of the table (2, 4 and 6) were derived before the EXP-003
artifacts were read.

## Literature

Not found in the searches of the review (the p-centre of the Heisenberg enveloping algebra, Azumaya loci, graded
modules; Erman and Sam; arXiv:2605.25259): the theorem, its corollaries, or the mechanism for graded modules (the even
part of U as the coordinate ring of a quadric, the odd part as a line bundle on P^1 x P^1). The ingredients are
standard (Revoy's theorem on Weyl algebras in characteristic p, the centres of nilpotent enveloping algebras,
Thom-Porteous, Eagon-Northcott). Two papers on the centres of nilpotent enveloping algebras in prime characteristic
(arXiv:2111.13432, arXiv:2405.08325) were read only through their abstracts. A negative search is not a proof of
novelty.

## Open

- Odd characteristic p: x^p, y^p and z are central and U has rank p^2 over them, but no such exclusion holds in general
  (pairs of quadrics with the pure table exist in characteristic 3). For which (p, e) is the point (1,2,2,1) of
  (0, e, 3e, 4e) realized over U(H)?
- The points with beta_1 = beta_0 + 1 on scaled Kostant rays in characteristic 0 (the substitution of x^e, y^e in the
  Kostant presentations, backlog BSB-012).
