# A four-parameter family of pure pairs for every e >= 4: the weight argument

Date: 2026-11-20. Status: derivation [D] by the coordinating session, not yet reviewed by a reader other than the
writer; nothing here is used in a manuscript before that review. It proves for every e >= 4 the inclusion that the
review of the family-dimension note derived for e = 4 and 5 and that EXP-007 tested on 1,650 members.

## Setting and statement

Notation of the note `2026-11-20-pure-pairs-family-dimension.md`: U = U(H), PBW monomials x^a y^b z^c, G_e = Gr(2, U_e),
mu_n(W), r = 2 u(2e) - 2, D_e = {rank mu_(3e)(W) <= r}, P_e the set of pure W, W_0 = <x^e, y^e>, M_e = U/U(x^e, y^e).
For a, b, c, d in k put

    L_e(a, b, c, d) = < x^e + a x y^(e-1) + b y^(e-2) z ,  y^e + c x^(e-1) y + d x^(e-2) z >.

Proposition. Let e >= 4 and let k be an algebraically closed field of characteristic 0 or at least 2e.

(i) L_e(a, b, c, d) lies in D_e for every (a, b, c, d).

(ii) L_e(a, b, c, d) is pure for (a, b, c, d) in a nonempty Zariski open subset of k^4 that contains the origin.

(iii) L_e(a, b, c, d) lies in the orbit of W_0 under the graded automorphisms only for (a, b, c, d) = 0.

So for every e >= 4 the modules U/(U L_e(a, b, c, d)), for general parameters, are pure of type (0, e, 3e, 4e) with
Betti table (1, 2, 2, 1) and are not of the form U/U(l_1^e, l_2^e).

## Proof

Step 1 (the torus and the chart). The torus T of pairs t = (t_1, t_2) acts on U by graded automorphisms, x to t_1 x,
y to t_2 y, z to t_1 t_2 z; the PBW monomial m = x^a y^b z^c is an eigenvector with character
chi_m = t_1^(a+c) t_2^(b+c). T fixes W_0. In the chart W = <x^e + f, y^e + g> around W_0 (f, g in the span of the PBW
monomials of degree e other than x^e and y^e, with coordinates f_m, g_m), t W = <x^e + t_1^(-e) t(f), y^e + t_2^(-e) t(g)>.
Since a + b + 2c = e, the coordinate f_m is multiplied by t_1^(a+c-e) t_2^(b+c) = s^(b+c) and the coordinate g_m by
t_1^(a+c) t_2^(b+c-e) = s^(-(a+c)), where s = t_2 / t_1. Call these exponents the weights of the coordinates. The
four coordinates of L_e are f at x y^(e-1) and at y^(e-2) z, of weight e - 1, and g at x^(e-1) y and at x^(e-2) z, of
weight -(e - 1).

Step 2 (the characters of the resolution). By Theorem A, M_e has the pure resolution
0 to U(-4e) to U(-3e)^2 to U(-e)^2 to U. The module is T-stable, so the resolution can be taken T-equivariant: the
generators of the free modules are eigenvectors, with characters 1; t_1^e, t_2^e; S_1, S_2; S_3. With the Hilbert
series of U for the two gradings, 1/((1 - t_1)(1 - t_2)(1 - t_1 t_2)), the character of M_e is
N / ((1 - t_1)(1 - t_2)(1 - t_1 t_2)) with N = 1 - t_1^e - t_2^e + S_1 + S_2 - S_3. Each of S_1, S_2 is a monomial
t_1^p t_2^q with p + q = 3e, and S_3 = t_1^p t_2^q with p + q = 4e. M_e has finite length, so N vanishes at t_1 = 1:
S_1(1, t_2) + S_2(1, t_2) - S_3(1, t_2) = t_2^e. The exchange of x and y (with z to -z) is an automorphism that
preserves the ideal, so S_3 is symmetric, S_3 = (t_1 t_2)^(2e), and the exponents q_1, q_2 of t_2 in S_1, S_2 satisfy
t_2^(q_1) + t_2^(q_2) = t_2^e + t_2^(2e). Hence S_1 = t_1^(2e) t_2^e and S_2 = t_1^e t_2^(2e), and
N = (1 - t_1^e)(1 - t_2^e)(1 - (t_1 t_2)^e): the character of M_e is the sum of t_1^(a+c) t_2^(b+c) over
0 <= a, b, c <= e - 1.

Consequences in degree 3e. The left kernel K of A = mu_(3e)(W_0) is the space of second syzygies in degree 3e; it has
the characters t_1^(2e) t_2^e and t_1^e t_2^(2e). The cokernel Q = (M_e)_(3e) has the characters t_1^alpha t_2^(3e-alpha)
with alpha = a + c over the triples with a + b + 2c = 3e, 0 <= a, b, c <= e - 1. From b = 3e - alpha - c <= e - 1 and
c <= e - 1 follows alpha >= e + 2; from a = alpha - c <= e - 1 and c <= e - 1 follows alpha <= 2e - 2. So every
alpha lies between e + 2 and 2e - 2.

Step 3 (the local equations are semi-invariants of small weight). Identify W with W_0 through the basis of the chart,
so that mu(W) = mu_(3e)(W) is a map from E = U_(2e) tensor W_0 to U_(3e), u tensor x^e to u (x^e + f) and
u tensor y^e to u (y^e + g). With rho_E(t) the action of t on E (on U_(2e) and on W_0) and rho(t) the action on U_(3e),
mu(t W) = rho(t) mu(W) rho_E(t)^(-1): for the first generator,
u (x^e + t_1^(-e) t(f)) = t_1^(-e) t( t^(-1)(u) (x^e + f) ), and likewise for the second. T is diagonalizable, so
E = K + K' and U_(3e) = Q' + I with all four subspaces T-stable, K = ker A (as a left kernel: the vectors of E that A
sends to 0), I = im A, Q' a complement mapped isomorphically to Q. In these decompositions mu(W) has blocks
alpha(W): K to Q', beta(W): K' to Q', gamma(W): K to I, delta(W): K' to I, with delta(W_0) invertible and the other
three zero at W_0. On the open set where delta is invertible, rank mu(W) <= r if and only if the Schur complement
Sigma(W) = alpha - beta delta^(-1) gamma: K to Q' vanishes. Its entries, in eigenbases of K and Q', are regular
functions F on a neighbourhood of W_0 in the chart, they vanish at W_0, and the equivariance of mu gives
Sigma(t W) = rho(t) Sigma(W) rho_E(t)^(-1): the entry from the eigenvector of K with character t_1^p t_2^q to the
eigenvector of Q' with character t_1^alpha t_2^(3e-alpha) satisfies F(t W) = t_1^(alpha-p) t_2^(3e-alpha-q) F(W).
For (p, q) = (2e, e) the factor is s^(2e-alpha), for (p, q) = (e, 2e) it is s^(e-alpha). By step 2 these weights lie
between 2 and e - 2, or between -(e - 2) and -2.

Step 4 (vanishing on the family). A regular function near the origin of the chart that is multiplied by s^w under T
has a Taylor expansion at the origin in which every monomial of the coordinates has total weight w. On the
coordinate subspace L_e every monomial has a weight that is a multiple of e - 1 (step 1). The weights w of the
functions F are nonzero and of absolute value at most e - 2, so none is a multiple of e - 1: the restriction of each
F to L_e has a zero Taylor expansion at the origin, hence vanishes on the open subset of L_e (an affine space) where
it is defined. So an open neighbourhood of W_0 in L_e lies in D_e; D_e is closed and L_e is irreducible, so L_e lies in
D_e. This is (i).

Step 5 (general members are pure). P_e is open in D_e (statement (b) of the family-dimension note) and contains W_0,
which is the member with parameters 0. So the pure members of L_e form an open subset of k^4 that contains the
origin. This is (ii).

Step 6 (the orbit). Let W = L_e(a, b, c, d) be in the orbit of W_0, W = <l_1^e, l_2^e> with linear forms l_1, l_2. The
image of W in U/(z) = k[x, y] is spanned by x^e + a x y^(e-1) and y^e + c x^(e-1) y, whose coefficients at
x^(e-i) y^i vanish for 2 <= i <= e - 2 (a nonempty range, since e >= 4). The image of (alpha x + beta y)^e has the
coefficient binom(e, i) alpha^(e-i) beta^i there, nonzero when alpha beta is not 0 (the characteristic is 0 or larger
than e). So each l_j is a multiple of x or of y, W = <x^e, y^e>, and (a, b, c, d) = 0. This is (iii).

## Remarks

- The argument uses Theorem A twice: for the characters of the resolution (step 2) and for the purity of W_0 (step
  5). It says nothing in characteristic below 2e.
- For e = 4 the weights of step 3 are 2 and -2 (alpha = 6), and for e = 5 they are 2, 3, -2, -3 (alpha = 7, 8): the
  values the review read on its tangent matrices. Checks by machine: EXP-007, statement T4 (all 625 members with
  parameters in {-2, ..., 2} over the rationals have rank at most r, for e = 4 and for e = 5; 200 of 200 random members
  over GF(32003) are pure and outside the orbit, for each e) and T3 (L_4(1, 0, 0, 0) = <x^4 + x y^3, y^4> and
  L_4(2, -3, 5, 7), L_5(2, -3, 5, 7) are pure over the rationals in two instruments).
- The same argument applies to any coordinate subspace of the chart whose coordinate weights generate a subgroup of Z
  that contains none of the weights 2e - alpha, e - alpha. L_e is the subspace of the coordinates of weight e - 1 and
  -(e - 1).
- The torus identifies L_e(a, b, c, d) with L_e(s^(e-1) a, s^(e-1) b, s^(-(e-1)) c, s^(-(e-1)) d), so up to that action the
  family has three parameters.
- Not claimed: which members are pure (the open set is not described; EXP-007 found members of rank below r, so it is
  not all of k^4), and nothing about the other components of D_e.
