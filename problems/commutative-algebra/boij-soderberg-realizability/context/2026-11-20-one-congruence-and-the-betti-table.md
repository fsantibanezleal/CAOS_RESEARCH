# The pairs (x^e + b y^e, G(xy, z)) for even e: one congruence decides the pure Hilbert function, and it gives the pure Betti table

Date: 2026-11-20. Status: derivation [D] by the coordinating session; NOT yet reviewed by a reader other than the
writer. Machine checks by the coordinating session (scripts and logs under the data root,
`caos-research/boij-soderberg-realizability/EXP-014/coordinator-run/`): Theorem 1 on every monic form over the prime
field in eleven cases (55,595 forms, 23,490 of them with the hypothesis); Theorem 2 on the 42 forms with the
hypothesis and the congruence in eight cases; Theorem 3 by power series in six cases over the rationals and five
over prime fields. Details in the last section.

This note continues `2026-11-20-pairs-over-the-invariants.md` (below: the first note) and uses its notation and its
results: h = xy, D = k[h, z], A_n(h) = h (h + z) ... (h + (n - 1) z), B_n(h) = (h - z) ... (h - n z), Lemma 1
(x d(h, z) = d(h + z, z) x, y d(h, z) = d(h - z, z) y, x^n y^n = A_n, y^n x^n = B_n), Lemma 2 (U is the direct sum of
the D e_n), the Proposition (M is the direct sum of the (D/J_r) v_r, r = -e, ..., e - 1), hypothesis (C) and the
Theorem (under (C): dim M <= e^3, with equality if and only if M has the pure Hilbert function, if and only if
J_r = (G_r, F_r) for every r, if and only if H_r lies in (G_r, F_r) for |r| <= m - 2).

## Setting and notation

k a field, e >= 4 even, m = e/2 >= 2, b in k not zero, G a form of degree m in D,

    f = x^e + b y^e,     g = G(h, z),     M = U/(Uf + Ug),     G_j = G(h + j z, z).

sigma is the automorphism d(h, z) -> d(h + z, z) of D and tau its inverse; so G_j = sigma^j(G), x d = sigma(d) x and
y d = tau(d) y. Put

    P_plus = G_(2e) A_e(h),        P_minus = G_(-2e) B_e(h),

two forms of degree m + e. In the first note these are the two generators G_(2e) c_(0,1) and G_(-2e) c_(0,-1) of J_0
other than G. From the first note, for 1 <= r <= e - 1,

    F_r = G_(r-2e) B_(e-r)(h),      H_r = G_(r+2e) A_e(h + r z),

and for -e <= r <= -1,

    F_r = G_(r+2e) A_(e+r)(h),      H_r = G_(r-2e) B_e(h + r z);

hypothesis (C) says that G_r and F_r have no common factor for -e <= r <= e - 1, where for r = 0 the form F_0 is
P_plus or P_minus, either.

Four identities are used throughout; each is read off the definitions of A_n and B_n:

    (I1)  B_e(h + r z) = A_r(h) B_(e-r)(h)          (0 <= r <= e),
    (I2)  A_e(h - s z) = B_s(h) A_(e-s)(h)          (0 <= s <= e),
    (I3)  sigma(B_n) = B_n(h + z) = h B_(n-1)(h)      (n >= 1),
    (I4)  tau(A_n) = A_n(h - z) = (h - z) A_(n-1)(h)  (n >= 1).

(I1): B_e(h + r z) is the product of the h - (k - r) z for k = 1, ..., e; the factors with k <= r give A_r(h) and
those with k > r give B_(e-r)(h). (I2): A_e(h - s z) is the product of the h + (k - s) z for k = 0, ..., e - 1; the
factors with k < s give B_s(h) and the others A_(e-s)(h). (I3) and (I4) are the cases r = 1 of (I1) for n in place
of e and s = 1 of (I2).

## Theorem 1: one congruence

Theorem 1. Assume (C). The following are equivalent.

(a) M has the pure Hilbert function h_e (equivalently, dim M = e^3).

(b) There is a nonzero scalar lambda with

    P_minus = lambda P_plus   modulo G,   that is,   G(h - 2e z, z) B_e(h) = lambda G(h + 2e z, z) A_e(h)  modulo G(h, z).

Under (a) and (b), G is coprime to P_plus and to P_minus; in particular neither h nor h - z divides G, and
J_0 = (G, P_plus) = (G, P_minus).

Proof. Step 1. Under (C), G divides neither P_minus nor P_plus. Suppose G divides P_minus = G_(-2e) B_e(h). Applying
sigma and (I3), G_1 divides G_(1-2e) h B_(e-1)(h) = h F_1. By (C) for r = 1, G_1 is coprime to F_1, so G_1 divides
h, which is impossible since G_1 has degree m >= 2. Suppose G divides P_plus = G_(2e) A_e(h). Applying tau and (I4),
G_(-1) divides G_(2e-1) (h - z) A_(e-1)(h) = (h - z) F_(-1), and by (C) for r = -1, G_(-1) divides h - z, impossible.

Step 2. (a) implies (b). By the Theorem of the first note, (a) gives H_0 in (G, F_0), where {F_0, H_0} =
{P_plus, P_minus} and F_0 is coprime to G. Both have degree m + e, so H_0 = a G + c F_0 with c a scalar, and c is
not zero by Step 1. Whichever of the two is F_0, this is (b) with lambda = c or 1/c.

Step 3. (b) implies (a). By the Theorem of the first note it is enough that H_r lies in (G_r, F_r) for every r with
1 <= |r| <= e - 1 and for r = 0. For r = 0 this is (b). Let 1 <= r <= e - 1 and apply sigma^r to (b):

    G_(r-2e) B_e(h + r z) = lambda G_(r+2e) A_e(h + r z) = lambda H_r   modulo G_r.

By (I1) the left side is G_(r-2e) A_r(h) B_(e-r)(h) = A_r(h) F_r. So lambda H_r lies in (G_r, F_r), and lambda is not
zero. Let 1 <= s <= e - 1 and r = -s, and apply tau^s to (b):

    H_r = G_(r-2e) B_e(h + r z) = lambda G_(r+2e) A_e(h - s z)   modulo G_r,

and by (I2) the right side is lambda B_s(h) G_(r+2e) A_(e-s)(h) = lambda B_s(h) F_r. So H_r lies in (G_r, F_r).

The last statement. By (b) with lambda not zero, G and P_plus have the same common factors as G and P_minus; by (C)
for r = 0 one of the two pairs is coprime, so both are. h divides A_e and h - z divides B_e. And
(G, P_plus) = (G, P_minus) is J_0 by the Theorem of the first note. QED.

Remarks.

1. The first note counts (m - 1)^2 conditions for (a), m - |r| - 1 for each r with |r| <= m - 2. Theorem 1 says that
   the m - 1 conditions at r = 0 imply all the others: the conditions at r are the shifts of the condition at 0,
   multiplied by A_r or B_s. So consequence 6 of the first note (for e >= 6 "more conditions than parameters") is
   superseded: under (C) the forms G with the pure Hilbert function are the solutions of m - 1 equations in the m
   coefficients of a monic G.

2. Dimension. Take G monic in h (under (C), z does not divide G). The pairs (G, lambda) with
   P_minus = lambda P_plus modulo G are the zeros of m polynomials (the coefficients of the remainder of
   P_minus - lambda P_plus modulo G) in the m + 1 unknowns (coefficients of G, lambda). By Krull's height theorem
   every irreducible component of this zero set over an algebraically closed field has dimension at least 1, and (C)
   with lambda not zero is an open condition. So over an algebraically closed field a form with (C) and the pure
   Hilbert function is never isolated: it lies on a curve of such forms. For e = 4 this curve is the quintic of the
   first note.

3. In terms of the roots. If G(h, 1) has m distinct roots rho_1, ..., rho_m in an extension of k, (b) says that the
   function

       Phi(rho) = G(rho - 2e) B_e(rho) / ( G(rho + 2e) A_e(rho) )

   takes the same nonzero value lambda at every root:

       prod_j (rho_i - rho_j - 2e)  prod_(k=1..e) (rho_i - k)  =  lambda  prod_j (rho_i - rho_j + 2e)  prod_(k=0..e-1) (rho_i + k)      (i = 1, ..., m).

   Equivalently, there is a polynomial Q of degree at most e with
   G(h - 2e) B_e(h) - lambda G(h + 2e) A_e(h) = Q(h) G(h). Equations of this shape (a second-order difference
   equation with polynomial coefficients for a polynomial G, and the system for its roots) are those of the
   algebraic Bethe ansatz for the rational six-vertex model, where they are called Baxter's T-Q equation and the
   Bethe equations with a twist lambda [U: the identification is by the shape of the equations; the literature was
   not read for this note, and nothing here depends on it].

4. The exchange of x and y (with z -> -z) sends G(h, 1) to (-1)^m G(1 - h, 1), so rho -> 1 - rho, and lambda to
   1/lambda.

## Theorem 2: the Betti table

Theorem 2. Assume (C). If M has the pure Hilbert function, then M has the pure Betti table (1, 2, 2, 1) on
(0, e, 3e, 4e). So under (C) the following are equivalent for the pair (x^e + b y^e, G(xy, z)), for every nonzero b:
the pair is pure; M has the pure Hilbert function; the congruence (b) of Theorem 1 holds.

Proof. Assume (C) and the pure Hilbert function. By the first note J_r = (G_r, F_r) for every r, and by Theorem 1
J_0 = (G, P_plus) = (G, P_minus), with G coprime to both and to h and h - z.

Step 1: the action of x and y on the summands. From Lemma 1 and the relations of the first note (v_e = - b v_(-e),
v_(-e-1) = - b^(-1) (h - z) v_(e-1)), for d in D:

    x (d v_r) = sigma(d) v_(r+1)            (0 <= r <= e - 2),       x (d v_(e-1)) = - b sigma(d) v_(-e),
    x (d v_r) = sigma(d) h v_(r+1)          (-e <= r <= -1)          [x y^s = h y^(s-1)],
    y (d v_r) = tau(d) v_(r-1)              (-e + 1 <= r <= 0),      y (d v_(-e)) = - b^(-1) tau(d) (h - z) v_(e-1),
    y (d v_r) = tau(d) (h - z) v_(r-1)      (1 <= r <= e - 1)        [y x^r = (h - z) x^(r-1)].

So x maps the summand of index r into the summand of index r + 1 (and e - 1 into -e), and y maps r into r - 1 (and
-e into e - 1).

Step 2: y is injective on the summand r for 1 <= r <= e - 1. Let tau(d)(h - z) lie in J_(r-1). Applying sigma,
d h lies in sigma(J_(r-1)) = (G_r, sigma(F_(r-1))). For r >= 2, sigma(F_(r-1)) = G_(r-2e) B_(e-r+1)(h + z) = h F_r by
(I3). For r = 1, J_0 = (G, P_minus) and sigma(P_minus) = G_(1-2e) B_e(h + z) = h F_1 by (I3). So d h = a G_r + c h F_r,
and h divides a G_r. Now h does not divide G_r: that would mean G(r, 1) = 0; for 2 <= r <= e - 1 this contradicts
(C) for the index 1 (G_1 is coprime to F_1, which is divisible by B_(e-1)(h), so G(1 + k, 1) is not zero for
1 <= k <= e - 1), and for r = 1 it contradicts Theorem 1 (h - z does not divide G). So h divides a, and
d = (a/h) G_r + c F_r lies in J_r.

Step 3: x is injective on the summand r for -e <= r <= -1. Let sigma(d) h lie in J_(r+1). Applying tau,
d (h - z) lies in tau(J_(r+1)) = (G_r, tau(F_(r+1))). For r <= -2, tau(F_(r+1)) = G_(r+2e) A_(e+r+1)(h - z) = (h - z) F_r
by (I4). For r = -1, J_0 = (G, P_plus) and tau(P_plus) = G_(2e-1) A_e(h - z) = (h - z) F_(-1) by (I4). So
d (h - z) = a G_r + c (h - z) F_r and h - z divides a G_r. h - z does not divide G_r: that would mean G(1 + r, 1) = 0
with 1 + r in {-(e - 1), ..., 0}; for 1 + r <= -1 this contradicts (C) for the index -1 (G_(-1) is coprime to F_(-1),
which is divisible by A_(e-1)(h), so G(-1 - k, 1) is not zero for 0 <= k <= e - 2), and for r = -1 it contradicts
Theorem 1 (h does not divide G). So d lies in J_r.

Step 4: the socle lies in the summand 0. Let w be a homogeneous element of M with x w = y w = z w = 0, and write
w as the sum of the d_r v_r. Since x and y permute the summands, x (d_r v_r) = 0 and y (d_r v_r) = 0 for every r. By
Step 2, d_r v_r = 0 for r >= 1; by Step 3, for r <= -1. So w = d v_0 with d a form of D, of degree N say.

Step 5: the socle in the summand 0. x w = sigma(d) v_1 = 0 means sigma(d) in J_1 = (G_1, F_1), that is, d in
(G, P_x) with P_x = tau(F_1) = G_(-2e) B_(e-1)(h - z) = G_(-2e) (h - 2z) ... (h - e z), so that (h - z) P_x = P_minus.
z w = 0 means z d in J_0 = (G, P_minus). Write d = a G + alpha P_x with alpha a form of degree j = N - (m + e - 1)
(alpha = 0 if j < 0), and z d = a' G + gamma P_minus. Then

    (z alpha - (h - z) gamma) P_x = 0   modulo G.

P_x divides P_minus, which is coprime to G; so G divides z alpha - (h - z) gamma, a form of degree j + 1. If
j + 1 < m this form is zero, so h - z divides alpha, alpha = (h - z) alpha', and d = a G + alpha' P_minus lies in
J_0: w = 0. If j < 0 then d lies in (G) and w = 0. So a nonzero w has j >= m - 1, that is N >= 2m + e - 2 = 2e - 2:
w has degree at least 4e - 4 in M. The pure Hilbert function is zero above 4e - 4 and equal to 1 there. Hence the
socle of M is M_(4e-4), of dimension 1.

Step 6: the Betti numbers. Tor^U_i(k, M) is the homology of the Chevalley-Eilenberg complex of the Heisenberg Lie
algebra <x, y, z> with coefficients in M (U is its enveloping algebra; Cartan and Eilenberg, Homological Algebra,
Chapter XIII, the standard complex; Weibel, An Introduction to Homological Algebra, Section 7.7 [U: the section
numbers are quoted from memory]), with x, y in degree 1 and z in degree 2. Its last differential sends
x^y^z (x) w to y^z (x) x w - x^z (x) y w + x^y (x) z w (the terms with brackets vanish: [x, y] = z gives z^z = 0, and
z is central). So Tor_3(k, M) in degree n is the socle of M in degree n - 4: b_3 = 1, in degree 4e, by Step 5.
b_0 = 1 in degree 0. Tor_1(k, M) = I/(U_+ I) for I = Uf + Ug, generated by two linearly independent forms of degree
e: b_1 = 2 in degree e. U has global dimension 3 and Hilbert series 1/((1 - t)^2 (1 - t^2)), so the alternating sum
of the series of the b_i is the Hilbert series of M times (1 - t)^2 (1 - t^2), which for the pure Hilbert function
is 1 - 2 t^e + 2 t^(3e) - t^(4e). Therefore the series of b_2 is 2 t^(3e). QED.

Remarks.

5. Theorem 2 turns consequence 5 of the first note (observed on the cases computed: with (C), the pure Hilbert
   function comes with the pure table) into a statement with a proof. Without (C) it fails: the first note and
   EXP-010, EXP-014 hold forms without (C) that have the pure Hilbert function and another table.

6. Purity does not depend on b: the conditions are on G alone.

7. What (C) is, by roots (first note, from its review): z does not divide G, no two roots of G(h, 1) differ by 2e,
   no root lies in {-(e - 1), ..., -1} or in {2, ..., e}, and 0 and 1 are not both roots. Under the congruence (b)
   neither 0 nor 1 is a root (Theorem 1). In characteristic p < 2e the excluded integers cover every residue other
   than 0 and 1 (and those too when p < e), so (C) with (b) means: G(h, 1) has no root in the prime field and no two
   roots differ by 2e. If p divides 2e, (C) fails for every G.

## Theorem 3: existence

Theorem 3. (i) Let e >= 4 be even and p = 2e - 1 a prime. There is a field K of characteristic p (the field
GF(p)((lambda)) of Laurent series, and also a finite field) and a form G over K with (C) and the congruence (b). So
by Theorem 2 the point (1, 2, 2, 1) of (0, e, 3e, 4e) is realized over U over a finite field of characteristic
p = 2e - 1, and over every field containing it.

(ii) Let k have characteristic 0, e >= 4 even, and S any subset of {1, ..., e} with m elements. There is a monic
form G over k[[lambda]], with G = prod over k in S of (h - k z) at lambda = 0, which satisfies (C) and (b) over
k((lambda)). So in characteristic 0, for every even e >= 4, there are pure pairs (x^e + b y^e, G(xy, z)) over
k((lambda)), and by remark 2 the forms G of such pairs make up at least a curve.

Proof. Work with z = 1 and with the roots. Let S = {k_1, ..., k_m} be a set of integers in {1, ..., e}, write
G(u) = prod_j (u - rho_j) and consider the m equations in the unknowns rho_1, ..., rho_m over R = F[[lambda]]
(F = GF(p) or F = k):

    E_i = G(rho_i - 2e) B_e(rho_i) - lambda G(rho_i + 2e) A_e(rho_i) = 0        (i = 1, ..., m).

At lambda = 0 the point rho = (k_1, ..., k_m) is a solution, since B_e(k_i) = 0. There the matrix of the partial
derivatives of the E_i in the rho_j is diagonal, with entries G_S(k_i - 2e) B_e'(k_i) (the other terms carry the
factor B_e(k_i) = 0), where G_S = prod_j (u - k_j). Suppose

    (H1)  G_S(k_i - 2e), G_S(k_i + 2e), A_e(k_i) and B_e'(k_i) are not zero in F for every i.

Then by Hensel's lemma there are unique rho_i in R with rho_i = k_i modulo lambda and E_i = 0, and the first-order
term is

    rho_i = k_i + c_i lambda + ...,      c_i = G_S(k_i + 2e) A_e(k_i) / ( G_S(k_i - 2e) B_e'(k_i) ),   not zero.

Put G = prod (h - rho_i). The E_i say that G(h - 2e) B_e(h) - lambda G(h + 2e) A_e(h) vanishes at the m distinct roots
of G, so it is divisible by G: this is (b), with the nonzero scalar lambda of the field L = F((lambda)). And (C) holds
over L: by remark 7 it fails only if a root lies in a finite set of elements of the prime field, which is impossible
because c_i is not zero, or if rho_i - rho_j = 2e or -2e for some i, j, which is impossible because at lambda = 0 it
would give G_S(k_i - 2e) = 0 or G_S(k_i + 2e) = 0 (and 2e is not zero in F by (H1) with i = j). (z does not divide G,
which is monic in h.)

(ii) In characteristic 0, (H1) holds for every S: |k_i - k_j| < e < 2e, A_e(k_i) > 0, and the roots of B_e are simple.

(i) Let p = 2e - 1 and S = {1, 3, ..., e - 1}, the odd numbers below e. Modulo p, 2e = 1. G_S(k_i - 2e) is the
product of the k_i - 1 - k_j and G_S(k_i + 2e) that of the k_i + 1 - k_j; these integers are odd, so not zero, and of
absolute value at most e - 1 < p. A_e(k_i) is the product of the integers k_i, ..., k_i + e - 1, all between 1 and
2e - 2 < p. B_e'(k_i) is the product of the k_i - k for k in {1, ..., e} other than k_i, of absolute value below
e < p. So (H1) holds, and the pair is pure over GF(p)((lambda)).

A finite field. The solution of Hensel's lemma already exists in the henselization of GF(p)[lambda] at lambda,
whose elements are algebraic over GF(p)(lambda); by uniqueness the rho_i are algebraic over GF(p)(lambda). So G has
its coefficients in a finite extension L' of GF(p)(lambda), the function field of a curve over a finite field. (C)
and (b) hold for G over L'. (C) and lambda not zero say that finitely many elements of L' (the resultants of G_r and
F_r, and lambda) are not zero, and (b) is a polynomial identity; so at all but finitely many places of L' the
coefficients of G are regular and their residues give a form over the residue field, a finite field, with (C) and
(b). QED.

Remarks.

8. Why only p = 2e - 1 in (i). For e < p < 2e the argument needs S inside {1, ..., p - e} (the roots of B_e that are
   not roots of A_e modulo p), with no two elements differing by d = 2e - p. Such a set with m = e/2 elements exists
   only if each of the d classes modulo d of {1, ..., e - d} has odd size, which forces e - d = d q with q odd, and
   then p = 2e - d = d (2q + 1) is a prime only for d = 1. A root placed at an integer that is a root of both A_e
   and B_e modulo p satisfies its equation for every lambda and stays there, against (C). So for the other primes
   below 2e this construction gives nothing, and existence is a matter of computation (remark 9); it is not a
   statement that no pure pair of this shape exists there.

9. Over a prime field. Theorem 3 gives a field of characteristic p, not the prime field. Over GF(p) the forms with
   (C) and (b) can be listed: p^m monic forms, each tested by two reductions modulo G. Their number is small and
   irregular in the cases listed so far (last section): 1, 1, 2, 16, 13 for e = 4 at p = 5, 7, 11, 13, 17 (the
   quintic curve); 2, 2, 4, 0, 2 for e = 6 at p = 5, 7, 11, 13, 17; 1, 4, 1, 1 for e = 8 at p = 5, 7, 11, 13. At
   (6, 13) there is none over GF(13), although 13 > 2e and the curve of Theorem 3 (ii) reduces modulo 13: a curve
   over a finite field may have no point over the prime field with a given open condition.

10. The primes p = 2e - 1 with e even are 7, 11, 19, 23, 31, 43, 47, 59, ... (e = 4, 6, 10, 12, 16, 22, 24, 30, ...).
    For e = 4 and 6 pure pairs over GF(7) and GF(11) were known from the linear family (EXP-009).

## Machine checks (coordinating session, 2026-11-20)

- Theorem 1 (`probe_tq.py`). For every monic G over GF(p), computed with polynomial arithmetic only: hypothesis (C)
  by greatest common divisors; the condition at r = 0; the conditions for every r with |r| <= m - 2. Cases and
  counts (forms, forms with (C), forms with (C) and the condition at r = 0, the same with all conditions):
  (4, 13): 169, 101, 16, 16. (4, 17): 289, 196, 13, 13. (6, 5): 125, 40, 2, 2. (6, 7): 343, 156, 2, 2.
  (6, 11): 1331, 552, 4, 4. (6, 13): 2197, 969, 0, 0. (6, 17): 4913, 2661, 2, 2. (8, 5): 625, 195, 1, 1.
  (8, 7): 2401, 798, 4, 4. (8, 11): 14641, 6107, 1, 1. (8, 13): 28561, 11715, 1, 1. No form with (C) on which the
  condition at r = 0 and the full set of conditions differ. The counts at e = 4 for p = 13, 17 and at e = 6 for
  p = 5, 7 equal those of the first note and its review (16, 13; 2, 2).
- Theorem 2 (`check_tq_betti.py`). For (e, p) = (4, 7), (4, 11), (4, 13), (4, 17), (6, 5), (6, 7), (6, 11), (6, 17):
  each of the 1, 2, 16, 13, 2, 2, 4, 2 forms with (C) and the congruence, rewritten in the PBW monomials, with
  f = x^e + y^e: length e^3 and the Betti table (1, 2, 2, 1) on (0, e, 3e, 4e) by the module construction of `uhlib`;
  42 forms, all pure. Forty forms with (C) and without the congruence (five per case): length 63 instead of 64 at
  e = 4, and 212 or 213 instead of 216 at e = 6.
- The pure members of EXP-014 at e = 8: the forms G of the pure members found over GF(5), GF(7), GF(11), GF(13)
  are exactly the 1, 4, 1, 1 forms with (C) and the congruence (compared by hand after rewriting g in h and z).
- Theorem 3 (`check_tq_branch.py`). The series rho_i(lambda) to order 8 by the fixed-point iteration
  rho_i = k_i + lambda G(rho_i + 2e) A_e(rho_i) / (G(rho_i - 2e) B_e(rho_i)/(rho_i - k_i)): the remainder of
  G(h - 2e) B_e - lambda G(h + 2e) A_e modulo G vanishes to that order and every c_i is not zero, for e = 4 with
  S = {1, 3}, {1, 2}, {2, 4}, e = 6 with S = {1, 3, 5}, {2, 3, 6} and e = 8 with S = {1, 3, 5, 7} over the
  rationals, and for (e, p) = (4, 7), (6, 11), (10, 19), (12, 23), (16, 31) with the odd numbers below e. For e = 4
  over the rationals the coefficients (alpha, gamma) of G = h^2 + alpha h + gamma satisfy the quintic
  P(alpha, gamma) = 0 of the first note to order 8, in the three cases.

## How could this be wrong?

- Theorem 1 rests on the Theorem of the first note (reviewed) and on the four identities; its machine check is on
  complete lists of forms and uses no part of the algebra U.
- Theorem 2: the points to check are the formulas of Step 1 at the two ends of the range of r, the two uses of (C)
  in Steps 2 and 3 (which integers are excluded as roots), and the degree count of Step 5. The check on 42 forms is
  made in U, by a construction that knows nothing of the decomposition. A form with (C), the pure Hilbert function
  and another table would refute it; none is known, and the forms without (C) that have another table (first note,
  consequence 4) do not satisfy the hypothesis.
- Theorem 3: Hensel's lemma for a system needs the Jacobian determinant to be a unit at the point, which (H1)
  gives. The passage to a finite field is a specialization argument; a reader should check that (C) and (b) are, as
  claimed, the nonvanishing of finitely many elements together with identities. No pure pair over a finite field of
  characteristic 2e - 1 was computed from this construction for e >= 10: those cases are for an experiment.
- Remark 3 names a classical family of equations by their shape only.
- Novelty is not claimed: no search of the literature was made for this note beyond the one of the first note.
