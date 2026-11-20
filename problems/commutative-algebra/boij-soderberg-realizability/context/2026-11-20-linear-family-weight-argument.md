# A four-parameter family of pure pairs for every e >= 4: the weight argument

Date: 2026-11-20. Status: derivation [D] by the coordinating session. Reviewed on 2026-11-20 by a reader other than the
writer (record `bs-linear-family-weight-review-2026-11-20` in the coordination repository): every step holds; five
minor repairs, applied below (two justifications added, the symmetry argument of step 2 replaced by a shorter one, a
notation clash removed, one remark corrected). The first text is in commit 4ff4f3c3. The note proves for every e >= 4
the inclusion that the review of the family-dimension note derived for e = 4 and 5 and that EXP-007 tested on 1,650
members.

## Setting and statement

Notation of the note `2026-11-20-pure-pairs-family-dimension.md`: U = U(H), PBW monomials x^a y^b z^c, G_e = Gr(2, U_e),
mu_n(W), r = 2 u(2e) - 2, D_e = {rank mu_(3e)(W) <= r}, P_e the set of pure W, W_0 = <x^e, y^e>, M_e = U/U(x^e, y^e).
For a, b, c, d in k put

    L_e(a, b, c, d) = < x^e + a x y^(e-1) + b y^(e-2) z ,  y^e + c x^(e-1) y + d x^(e-2) z >.

Proposition. Let e >= 4 and let k be a field of characteristic 0 or at least 2e.

(i) L_e(a, b, c, d) lies in D_e for every (a, b, c, d) in k^4. (The proof is over an infinite field; a rank does not
change under an extension of the field, so the statement holds over every field of these characteristics.)

(ii) If k is algebraically closed, L_e(a, b, c, d) is pure for (a, b, c, d) in a nonempty Zariski open subset of k^4
that contains the origin.

(iii) L_e(a, b, c, d) lies in the orbit of W_0 under the graded automorphisms only for (a, b, c, d) = 0. (This part
needs only characteristic 0 or larger than e.)

So for every e >= 4 the modules U/(U L_e(a, b, c, d)), for general parameters, are pure of type (0, e, 3e, 4e) with
Betti table (1, 2, 2, 1) and are not of the form U/U(l_1^e, l_2^e).

## Proof

Step 1 (the torus and the chart). The torus T of pairs t = (t_1, t_2) acts on U by graded automorphisms, x to t_1 x,
y to t_2 y, z to t_1 t_2 z; the PBW monomial m = x^a y^b z^c is an eigenvector with character
chi_m = t_1^(a+c) t_2^(b+c). T fixes W_0. In the chart W = <x^e + f, y^e + g> around W_0 (f, g in the span of the PBW
monomials of degree e other than x^e and y^e, with coordinates f_m, g_m), t W = <x^e + t_1^(-e) t(f), y^e + t_2^(-e) t(g)>.
Since a + b + 2c = e, the coordinate f_m is multiplied by t_1^(a+c-e) t_2^(b+c) = s^(b+c) and the coordinate g_m by
t_1^(a+c) t_2^(b+c-e) = s^(-(a+c)), where s = t_2 / t_1. Call these exponents the weights of the coordinates. Every
chart coordinate has a weight of absolute value between 1 and e - 1, and the weights e - 1 and -(e - 1) occur exactly
at the four coordinates of L_e: f at x y^(e-1) and at y^(e-2) z, of weight e - 1, and g at x^(e-1) y and at x^(e-2) z,
of weight -(e - 1).

Step 2 (the characters of the resolution). U is graded by pairs of integers, x in degree (1, 0), y in (0, 1), z in
(1, 1) (the relation y x = x y - z is homogeneous), and x^e, y^e are homogeneous for it, so M_e is a bigraded module.
A minimal bigraded free resolution of M_e exists (U is connected graded) and is a minimal graded resolution for the
total degree; by Theorem A its generators therefore have total degrees 0; e, e; 3e, 3e; 4e. Write their characters as
1; t_1^e, t_2^e; S_1, S_2; S_3, with S_j = t_1^(p_j) t_2^(q_j), p_j + q_j = 3e for j = 1, 2 and p_3 + q_3 = 4e. With
the character of U, 1/((1 - t_1)(1 - t_2)(1 - t_1 t_2)), the character of M_e is
N / ((1 - t_1)(1 - t_2)(1 - t_1 t_2)) with N = 1 - t_1^e - t_2^e + S_1 + S_2 - S_3. M_e has finite length, so its
character is a polynomial and N vanishes at t_1 = 1 and at t_2 = 1. At t_1 = 1: t_2^(q_1) + t_2^(q_2) = t_2^e + t_2^(q_3),
so {q_1, q_2} = {e, q_3}. At t_2 = 1: {p_1, p_2} = {e, p_3}. Label so that q_1 = e; then p_1 = 2e, which is not e, so
p_1 = p_3 and p_2 = e, hence q_2 = 2e = q_3. So S_1 = t_1^(2e) t_2^e, S_2 = t_1^e t_2^(2e), S_3 = (t_1 t_2)^(2e), and
N = (1 - t_1^e)(1 - t_2^e)(1 - (t_1 t_2)^e): the character of M_e is the sum of t_1^(a+c) t_2^(b+c) over
0 <= a, b, c <= e - 1.

Consequences in degree 3e. The kernel K of A = mu_(3e)(W_0) (the pairs (u_1, u_2) in U_(2e)^2 with
u_1 x^e + u_2 y^e = 0) is the space of second syzygies in degree 3e; it has the characters t_1^(2e) t_2^e and
t_1^e t_2^(2e). The cokernel Q = (M_e)_(3e) has the characters t_1^alpha t_2^(3e-alpha) with alpha = a + c over the
triples with a + b + 2c = 3e, 0 <= a, b, c <= e - 1. From b = 3e - alpha - c <= e - 1 and c <= e - 1 follows
alpha >= e + 2; from a = alpha - c <= e - 1 and c <= e - 1 follows alpha <= 2e - 2. So every alpha lies between e + 2
and 2e - 2.

Step 3 (the local equations are semi-invariants of small weight). Identify W with W_0 through the basis of the chart,
so that mu(W) = mu_(3e)(W) is a map from E = U_(2e) tensor W_0 to U_(3e), u tensor x^e to u (x^e + f) and
u tensor y^e to u (y^e + g). With rho_E(t) the action of t on E (on U_(2e) and on W_0) and rho(t) the action on U_(3e),
mu(t W) = rho(t) mu(W) rho_E(t)^(-1): for the first generator,
u (x^e + t_1^(-e) t(f)) = t_1^(-e) t( t^(-1)(u) (x^e + f) ), and likewise for the second. T acts diagonally on E and on
U_(3e), so E = K + K' and U_(3e) = Q' + I with all four subspaces T-stable, I = im A, Q' a complement of I (mapped
isomorphically to Q). In these decompositions mu(W) has blocks A_11(W): K to Q', A_12(W): K' to Q', A_21(W): K to I,
A_22(W): K' to I, with A_22(W_0) bijective (dim K' = r = dim I) and the other three zero at W_0. The set where A_22 is
invertible is open and T-stable (det A_22(t W) is det A_22(W) times a character of T), and on it rank mu(W) <= r if
and only if the Schur complement Sigma(W) = A_11 - A_12 A_22^(-1) A_21: K to Q' vanishes. The equivariance of mu gives
Sigma(t W) = rho(t) Sigma(W) rho_E(t)^(-1): the entry F of Sigma from the eigenvector of K with character
t_1^p t_2^q to the eigenvector of Q' with character t_1^alpha t_2^(3e-alpha) satisfies
F(t W) = t_1^(alpha-p) t_2^(3e-alpha-q) F(W) on that set. For (p, q) = (2e, e) the factor is s^(2e-alpha), for
(p, q) = (e, 2e) it is s^(e-alpha). By step 2 these weights lie between 2 and e - 2, or between -(e - 2) and -2.

Step 4 (vanishing on the family). Let k be infinite. det A_22 is a polynomial in the chart coordinates that is
multiplied by a character under T and is not zero at the fixed point W_0, so that character is trivial; each entry F is
P / (det A_22)^m with P a polynomial in the coordinates multiplied by s^w under T, w the weight of F. Comparing
coefficients (k is infinite), every monomial of P in the coordinates has total weight w. On the coordinate subspace
L_e every monomial has a weight that is a multiple of e - 1 (step 1). The weights w are nonzero and of absolute value
at most e - 2, so none is a multiple of e - 1: the restriction of each P to L_e is zero. So Sigma vanishes on the
nonempty open subset of L_e where A_22 is invertible, which lies in D_e; D_e is closed and L_e (an affine space) is
irreducible, so L_e lies in D_e. This is (i).

Step 5 (general members are pure). P_e is open in D_e in every characteristic (statement (b) of the family-dimension
note) and contains W_0, the member with parameters 0, which is pure by Theorem A. So the pure members of L_e form an
open subset of k^4 that contains the origin. This is (ii).

Step 6 (the orbit). The graded automorphisms of U are GL_2 acting on U_1 = <x, y>, so the orbit of W_0 is the set of
<l_1^e, l_2^e> with l_1, l_2 independent linear forms in x, y. Let W = L_e(a, b, c, d) be one of them. The image of W
in U/(z) = k[x, y] is spanned by x^e + a x y^(e-1) and y^e + c x^(e-1) y, whose coefficients at x^(e-2) y^2 vanish
(2 <= e - 2, since e >= 4). The image of (alpha x + beta y)^e has the coefficient binom(e, 2) alpha^(e-2) beta^2
there, and binom(e, 2) is not zero in characteristic 0 or larger than e. So each l_j is a multiple of x or of y,
W = <x^e, y^e>, and (a, b, c, d) = 0. This is (iii). A graded isomorphism between cyclic modules generated in degree 0
sends the generator to a multiple of the generator, so the modules U/(U W) are of the form U/U(l_1^e, l_2^e) only for
W in the orbit.

## Remarks

- The argument uses Theorem A twice: for the total degrees of the resolution (step 2) and for the purity of W_0 (step
  5). It says nothing in characteristic below 2e, and the review's computations show that it does not extend as it
  stands: at e = 6 over GF(11) and at e = 7 over GF(13) the kernel and cokernel of mu_(3e)(W_0) have other characters,
  equations of weight e - 1 and -(e - 1) appear, and the tangent map is not zero on the coordinates of L_e.
- For e = 4 the weights of step 3 are 2 and -2 (alpha = 6), and for e = 5 they are 2, 3, -2, -3 (alpha = 7, 8).
- Checks by machine. EXP-007, statement T4: all 625 members with parameters in {-2, ..., 2} over the rationals have
  rank at most r, for e = 4 and for e = 5; 200 of 200 random members over GF(32003) are pure and outside the orbit, for
  each e. Statement T3: L_4(1, 0, 0, 0) = <x^4 + x y^3, y^4>, L_4(2, -3, 5, 7) and L_5(2, -3, 5, 7) are pure over the
  rationals in two instruments. The review adds, from a scratch run that is not archived: the characters of step 2
  and the weights of step 3 read on the matrices for e = 4 to 7; no member of L_6 or L_7 with rank above r (2,000
  random members each over GF(32003), 200 each over the rationals, all 28,561 members of L_6 over GF(13), all 83,521
  members of L_6 and of L_7 over GF(17), 5,000 random members over GF(19) and GF(23)); the 43 Betti tables computed
  for random members over GF(32003) and the rationals all pure. Over the small fields a large share of the members
  has rank below r and is not pure (28 percent over GF(13) at e = 6, 30 percent over GF(17) at e = 7; 4 of the 8
  members whose table was computed over primes between 2e and 4e), which (ii) allows: the pure set is open, not
  everything. On samples in characteristic below 2e (2,000 members of L_6 over GF(11) and of L_7 over GF(13)) no member
  has rank above r either, although the weight argument does not apply there: an observation, not a statement.
- L_e is the largest coordinate subspace of the chart to which the argument applies: it consists of the coordinates
  of extreme weight e - 1 and -(e - 1), and every other coordinate has a weight whose multiples meet the weights of
  the equations.
- The torus identifies L_e(a, b, c, d) with L_e(s^(e-1) a, s^(e-1) b, s^(-(e-1)) c, s^(-(e-1)) d), so up to that action the
  family has three parameters. Whether other automorphisms identify more members is not examined.
- Not claimed: which members are pure (the open set is not described; EXP-007 found members of rank below r, so it is
  not all of k^4), and nothing about the other components of D_e or about smoothness.
