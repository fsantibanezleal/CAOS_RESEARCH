# The modules U(H)/U(H)(x^e, y^e): a route to their Hilbert function for every e

Date: 2026-11-19. Status: derivation [D]. Steps 1 to 4 (the Hilbert series for every e, characteristic 0) are
complete and agree with the machine results of EXP-002 for e <= 6; the socle step (purity for every e) is open. To be
reviewed as a proof by a reader other than the writer before any claim.

## Setting

U = U(H), with xy - yx = z central, deg x = deg y = 1, deg z = 2. M_e = U/U(x^e, y^e) (left ideal). The pure ray
(0, e, 3e, 4e) has primitive point (1,2,2,1); over k[x,y,z] that point is excluded (two generators cannot cut out a
finite length quotient, Krull). Over U its Hilbert series is

    h_e(t) = (1 - 2t^e + 2t^(3e) - t^(4e)) / ((1-t)^2 (1-t^2)) = (1 + t + ... + t^(e-1))^2 (1 + t^2 + ... + t^(2e-2)).

Target: for k of characteristic 0, M_e has Hilbert series h_e(t), socle of dimension 1 in degree 4e - 4, hence the pure
resolution 0 <- U <- U(-e)^2 <- U(-3e)^2 <- U(-4e) <- 0. The case e = 1 is the trivial module (Erman-Sam). The case e = 2
is derived by hand in the EXP-002 hypothesis.

## Step 1: M_e as a cokernel over k[z]

Use the PBW basis y^b x^a z^c (x to the right). U x^e is spanned by the monomials with a >= e, so P = U/U x^e is a free
k[z]-module with basis y^b x^a, 0 <= a < e, b >= 0. With xy = yx + z,

    x^a y^e = sum over j of j! binom(a, j) binom(e, j) y^(e-j) x^(a-j) z^j,

so M_e = P / (image of U y^e) is the cokernel of the k[z]-linear map

    Phi(u_(a,b)) = sum over j with 0 <= j <= min(a, e) and a - j < e of j! binom(a,j) binom(e,j) z^j y^(b+e-j) x^(a-j),

over all a >= 0, b >= 0 (u_(a,b) stands for y^b x^a y^e). The torus weight w = (exponent of y) - (exponent of x) is
preserved: a source u_(a,b) of weight b - a + e maps to targets y^(b') x^(a') with b' - a' = b - a + e. So Phi splits into
blocks indexed by w.

## Step 2: the blocks are binomial Toeplitz matrices

In the block of weight w the rows are a' in [max(0, -w), e - 1] (with b' = a' + w) and the columns are a >= max(0, e - w)
(with b = a + w - e). The entry at (a', a) is (a - a')! binom(a, a - a') binom(e, a - a') z^(a - a')
= (a!/a'!) binom(e, a - a') z^(a - a'). After scaling row a' by a'! and column a by 1/a! (units in characteristic 0), the
block is

    T_w = [ binom(e, a - a') z^(a - a') ],

homogeneous for the grading that gives row a' the z-degree a' and column a the z-degree a. For such a matrix the
cokernel in z-degree n is the cokernel of the numeric matrix T[R_n, C_n] = [binom(e, a - a')] with rows
R_n = [max(0, -w), min(n, e - 1)] and columns C_n = [max(0, e - w), n]. The class of z^(n - a') y^(a' + w) x^(a') has total
degree 2n + w. Hence

    HS(M_e)(t) = sum over w and n of ( |R_n| - rank T[R_n, C_n] ) t^(2n + w).

## Step 3: the ranks (complete)

T = [binom(e, a - a')] has a nonzero entry exactly when 0 <= a - a' <= e. Only contiguous blocks occur, and only three
kinds of minors are needed.

- Weight w >= 0 (rows from 0, columns from e - w), n <= e - 1: rows 0..n, columns (e-w)..n. The square block on rows and
  columns (e-w)..n is upper unitriangular, so the rank is the number of columns, n - e + w + 1 (zero when n < e - w).
- Weight w >= 0, n >= e: rows 0..e-1; the columns beyond 2e - 1 vanish on these rows, so the usable columns are
  (e-w)..min(n, 2e-1), in number U = min(n, 2e-1) - e + w + 1. The k by k block on rows 0..k-1 and columns
  (e-w)..(e-w+k-1), k = min(e, U), is det[binom(e, (e-w) - s + s')], which by the dual Jacobi-Trudi identity is the Schur
  polynomial of the rectangle with e - w rows and k columns evaluated at e ones: the number of semistandard tableaux of
  that shape with entries at most e, positive because e - w <= e. So the rank is min(e, U).
- Weight w = -q < 0 (rows from q, columns from e + q): for n < e + q there is no column; for n >= e + q the usable
  columns are (e+q)..min(n, 2e-1) and the block on rows q..q+k-1 and columns (e+q)..(e+q+k-1) is lower unitriangular
  (binom(e, e) on the diagonal, zero above), so the rank is min(e - q, U) with U = min(n, 2e-1) - e - q + 1.

In characteristic 0 these minors are nonzero, and the ranks cannot be larger (number of rows, number of nonzero
columns). In characteristic p the condition is that p divides none of the row and column scalings a!/a'! (a <= 2e - 1)
nor the tableau counts above; at e = 2 the counts are 2 and 3.

## Step 4: the count (complete)

Write q = |w| and n' = n - max(0, -w). From step 3 the dimension of the block of weight w in z-degree n is

    D_q(n') = min(n' + 1, e - q) for 0 <= n' <= e - 1,    D_q(n') = max(0, 2e - 1 - q - n') for n' >= e,

the same for w and -w. Its generating function in s is the trapezoid (1 + s + ... + s^(e-q-1)) (1 + s + ... + s^(e-1)). The
class sits in total degree 2n + w = 2n' + q. Hence

    HS(M_e)(t) = (1 + t^2 + ... + t^(2e-2)) * sum over w, |w| < e, of t^|w| (1 + t^2 + ... + t^(2(e-|w|-1))),

and the last sum is (1 + t + ... + t^(e-1))^2 (group the monomials t^(a+b), a, b < e, by b - a). So
HS(M_e)(t) = h_e(t) for every e, in characteristic 0. In particular M_e has finite length e^3. [Agrees with the machine
Hilbert functions of EXP-002 for e = 2, ..., 6 over QQ, both instruments.]

## What the computation at e = 2 shows about the characteristic

The only numeric matrices that matter at e = 2 are (2, 1) (weight 1, n = 1), [[2,1],[1,2]] (weight 1, n = 2), (1, 2)
(weight 0, n = 2) and [[1,0],[2,1]] (weight 0, n = 3). The second has determinant 3 and entries 2: in characteristic 3
its rank drops and M_2 is too large in degree 5; in characteristic 2 the scaling by a!/a'! is not invertible and the
element 4xyz - 2z^2 vanishes. This matches the hand derivation of the EXP-002 hypothesis and suggests the general
condition: the characteristic must not divide the factorials up to 2e - 2 nor the binomial minors that occur.

## Structure over k[z] (a correction of a remark in the EXP-002 hypothesis)

M_e is not free over k[z]/(z^e): at e = 2, M_2 = k[z]/(z^3) + (k[z]/(z^2))^2 (-1) + k[z]/(z) (-2), generated by the classes
of 1, x, y and xy - z/2. The pattern suggested by e = 2 is one summand k[z]/(z^(2e - 1 - a - b)) for each monomial
x^a y^b with a, b < e, which has the same Hilbert series h_e(t) (both equal the sum over a, b < e of
t^(a+b) (1 + t^2 + ... + t^(2(2e - 2 - a - b)))). The Hilbert function claim of EXP-002 does not depend on which
description holds.

## Step 5: the socle is one-dimensional (complete)

Left multiplication by y on P is the shift y^b x^a z^c to y^(b+1) x^a z^c: it is injective and its image is spanned by the
basis elements with b >= 1. Let N be the image of U y^e in P, so M_e = P/N; N is spanned over k[z] by the classes of
y^b x^a y^e.

Kernel of y on M_e. Let m in P with y m in N. The terms y^b x^a y^e with b >= 1 are y times an element of N. For b = 0:
x^a y^e vanishes in P when a >= 2e; for e <= a <= 2e - 1 its component on the basis elements with b = 0 is
e! binom(a, e) z^e x^(a-e), and these are independent for different a; for a < e it is y g_a with

    g_a = sum over j <= a of j! binom(a, j) binom(e, j) z^j y^(e-j-1) x^(a-j).

Since y m lies in yP, the coefficients of the terms with e <= a <= 2e - 1 vanish (characteristic 0), and injectivity of y
on P gives m = n' + sum over a < e of c_a(z) g_a with n' in N. So the kernel of y on M_e is the k[z]-span of the classes of
g_0, ..., g_(e-1), and g_a has weight e - 1 - a >= 0.

Symmetry. sigma: x to y, y to -x, z to z is an automorphism of H that preserves U(x^e, y^e); it induces a bijection of
M_e that exchanges the kernels of x and y and sends weight w to -w. So the kernel of x on M_e lies in the weights <= 0.

Hence the socle (the kernel of x and y together) lies in weight 0, inside the kernel of y in weight 0, which is the
cyclic k[z]-module generated by the class of g_(e-1). A socle element is also killed by z = xy - yx, and the elements of
a cyclic torsion k[z]-module killed by z form a space of dimension at most 1. So the socle of M_e has dimension at
most 1; it is not zero because M_e is a nonzero module of finite length; and it contains the top degree 4e - 4, which
is one-dimensional. So the socle of M_e is M_e in degree 4e - 4.

## Step 6: the resolution

The minimal resolution of the trivial module over U is 0 <- U <- U(-1)^2 <- U(-3)^2 <- U(-4) <- 0 and the two entries
of its last map span U_1, so Tor_3(k, M)_j is the socle of M in degree j - 4 for a finite length M. For M_e this gives the
last Betti number 1 in degree 4e. The first two are 1 (degree 0) and 2 (degree e: x^e and y^e are minimal generators).
The alternating sum of the Betti series is HS(M_e)(t) (1-t)^2 (1-t^2) = 1 - 2t^e + 2t^(3e) - t^(4e), so the second syzygies
are 2 in degree 3e and nothing else.

Statement obtained. For k of characteristic 0 and every e >= 1, U(H)/U(H)(x^e, y^e) has length e^3 and the pure
resolution 0 <- U <- U(-e)^2 <- U(-3e)^2 <- U(-4e) <- 0: the primitive point (1,2,2,1) of the ray (0, e, 3e, 4e), excluded
over k[x,y,z] for every e, is realized over U(H). The case e = 1 is the example of Erman and Sam. [Agrees with EXP-002
for e <= 6. To be reviewed by a reader other than the writer before any claim; the search for this statement in the
literature (Sam's announced sp_4 work was never located) is part of that review.]

Remark (not generic for e >= 4). The Hilbert series of M_e is not the maximal-rank series of two forms of degree e over
U for e >= 4: in degree 4e - 4 the series (1 - 2t^e)/((1-t)^2 (1-t^2)) has a negative coefficient (for e = 4: 49 - 50),
while M_e is one-dimensional there. So for e >= 4 a general pair of forms of degree e gives a smaller quotient, and the
pair (x^e, y^e) is special. [To be checked by machine: a random pair of quartics.]
