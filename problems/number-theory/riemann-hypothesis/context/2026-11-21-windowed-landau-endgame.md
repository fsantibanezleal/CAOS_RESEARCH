# The analytic end of the 2026-11-20 formal proof: a one-sided bound on windows excludes zeros (a human proof)

Date: 2026-11-21. Status: derivation [D] by the coordinating session, written for the review of the claimed proof
of the Riemann hypothesis released on 2026-11-20 (dossier `2026-11-21-claimed-proof-review.md`). Version 2 of the
same day. Version 1 (commit a6f70991) was read by a reviewer other than the writer: verdict correct after fixes,
two major and eight minor findings, every formula (1) to (11) of version 1 confirmed as a formula (the proof of (2)
was a finding) and the constants of Step 2 recomputed (report `wip/caos-research/rh-windowed-landau-review-2026-11-21.md` of the coordination repository). This version
applies the ten findings and goes further on the first one: Lemma W is now proved under the hypothesis of the
formal lemma (positive residues at the real poles only), by taking the coefficient at the second point in modulus.
The steps that changed for that (Step 1, Step 3, Step 4) are marked. The same reviewer read version 2: the
mathematics is correct as written, formulas (1) to (12) confirmed, five minor findings on wording and citations,
applied here (review record at the end of the note). The statement proved here is classical in kind (Landau's theorem on Dirichlet integrals of one sign,
localized to windows); no priority is claimed. Its purpose is narrow: the Lean development ends with a lemma of this
shape (`Deduction.landau_window`, `Deduction.zeroFree_of_rpow_window`), and this note gives a complete proof a
person can check in an hour, so that the last step of the formal proof is understood independently of the kernel.
It says nothing about the rest of the formal proof, which is where the one-sided bound itself is obtained.

## 1. The objects

Lambda is the von Mangoldt function and gamma is Euler's constant. For x >= 1 put

    S(x) = sum over n <= x of Lambda(n) (x/n - 1),        G(x) = S(x) - x log x + (1 + gamma) x.

These are `Formalism.Sz` and `Formalism.Gz` of the formal development (`src/Formalism/StatementOC.lean`, read at
commit 23aebbb3 of the mirror `leanprover-community/riemann-hypothesis`). With T(t) = sum over n <= t of
Lambda(n)/n and psi(t) = sum over n <= t of Lambda(n) one has S(x) = x T(x) - psi(x), and S is the integral of T
from 1 to x. S is continuous, S(1) = 0, and S is extended by 0 to (0, 1).

Lemma 1 (transform). For Re s > 1,

    integral from 1 to infinity of S(x) x^(-s-1) dx = - zeta'(s)/zeta(s) * 1/(s (s - 1)).

Proof. For n >= 1, the integral from n to infinity of (x/n - 1) x^(-s-1) dx equals n^(-s)/(s - 1) - n^(-s)/s =
n^(-s)/(s (s - 1)). Sum against Lambda(n); the interchange is justified by absolute convergence for Re s > 1. QED.

Near s = 1, -zeta'/zeta(s) = 1/(s - 1) - gamma + O(s - 1) and 1/(s (s - 1)) = 1/(s - 1) - 1 + O(s - 1), so the
transform is 1/(s - 1)^2 - (1 + gamma)/(s - 1) + O(1). The transforms of x log x and of x are 1/(s - 1)^2 and
1/(s - 1). Hence

    Phi(s) := integral from 1 to infinity of G(x) x^(-s-1) dx
            = - zeta'(s)/zeta(s) * 1/(s (s - 1)) - 1/(s - 1)^2 + (1 + gamma)/(s - 1)             (1)

is analytic at s = 1. Phi is meromorphic on the plane. Its poles are: each zero rho of zeta (trivial or not), simple,
with residue -m(rho)/(rho (rho - 1)), m(rho) the multiplicity; and s = 0, with residue zeta'(0)/zeta(0) = log 2 pi.

Lemma 2 (explicit formula). For x >= 1,

    G(x) = - sum over nontrivial zeros rho of x^rho/(rho (rho - 1)) + log 2 pi
           - sum over k >= 1 of x^(-2k)/(2k (2k + 1)),                                              (2)

the sum over zeros counted with multiplicity and absolutely convergent.

Proof. Invert the transform of S, not that of G. For y > 0 and 1 < c <= 2 the integral over the line Re s = c of
y^s/(s (s - 1)), divided by 2 pi i, is max(y - 1, 0): the integrand is O(|s|^(-2)); for y > 1 the line is moved to
the left and the residues at s = 1 and s = 0 are y and -1; for y <= 1 it is moved to the right and there is none.
Summing against Lambda(n) n^(-s) with y = x/n, which is legitimate because the sum of Lambda(n) n^(-c) converges and
the kernel is absolutely integrable on the line,

    S(x) = (1/(2 pi i)) * integral over Re s = c of ( - zeta'(s)/zeta(s) ) x^s/(s (s - 1)) ds        for every x > 0.

Now move the line to Re s = -2K - 1 through horizontal segments at heights T_m tending to infinity, chosen so that
|zeta'/zeta(sigma + i T_m)| = O(log^2 T_m) for -1 <= sigma <= 2; to the left of -1 and away from the even negative
integers |zeta'/zeta(s)| = O(log |s|). (Both are the standard bounds used for the explicit formula of psi:
Davenport, Multiplicative Number Theory, chapter 17; the reference is cited from memory.) Because of the factor
1/|s|^2 and of x^(Re s) <= x^c on the segments, the horizontal contributions tend to 0, and for x >= 1 the integral
over Re s = -2K - 1 tends to 0 as K grows, the value x = 1 included. The residues: at the double pole s = 1,
x log x - (1 + gamma) x (from x^s = x (1 + (s - 1) log x + ...) and the expansion above); at a nontrivial zero,
-m(rho) x^rho/(rho (rho - 1)); at s = 0, zeta'(0)/zeta(0) = log 2 pi; at s = -2k, where -zeta'/zeta has residue -1,
-x^(-2k)/(2k (2k + 1)). Moving x log x - (1 + gamma) x to the left side gives (2). The sum over zeros converges
absolutely because the sum of 1/|rho|^2 does. QED.

(Version 1 inverted (1) itself and said every integral converged absolutely. That is false for the terms
-1/(s - 1)^2 and (1 + gamma)/(s - 1) of (1), which do not carry the factor 1/(s (s - 1)): on a vertical line the
second is of size 1/|t| and its inversion converges only as a principal value, to (1 + gamma)/2 at x = 1. The
reviewer computed that value. Formula (2) was right; its proof is the one above.)

Consequence 3 (what the hypothesis gives back). If every nontrivial zero has real part 1/2, then
|rho (rho - 1)| = |rho|^2 and the sum over zeros of 1/|rho|^2 equals the sum of (1/rho + 1/(1 - rho)), which is
2 + gamma - log 4 pi = 0.0461914179... (the classical value of the sum of 1/rho, taken twice). So under the
Riemann hypothesis, for every x >= 1,

    | G(x) - log 2 pi | <= (2 + gamma - log 4 pi) sqrt(x) + (1 - log 2)/x^2.                       (3)

(The last term bounds the sum over k in (2), since the sum of 1/(2k (2k + 1)) is 1 - log 2. At x = 1 formula (2)
reads 1 + gamma = log 2 pi + (2 + gamma - log 4 pi) - (1 - log 2), which is an identity.)

A bound of the order sqrt(x) in both directions is therefore equivalent to the Riemann hypothesis; the point of
Section 3 is that a bound from above alone, of the order x^(1/2 + epsilon), on a sparse family of windows, already
suffices. Experiment EXP-029 checks (2) and the constant of (3) numerically (verdict PASS).

For a Dirichlet character chi the formal development uses `Deduction.Gchi`
(`src/Development/AutomorphicArithmetic/DedekindLFunctions/CharFamily.lean`). Its definition branches on `chi = 1`,
the principal character of its modulus: in that branch it is the function G above with chi(n) inserted in the sum;
otherwise it is

    G_chi(x) = sum over n <= x of Lambda(n) chi(n) (x/n - 1) + x L'(1, chi)/L(1, chi),

a complex number. A family (`CharFamily`) admits a principal character only of modulus 1 (its clause `adm`), so
inside a family the first branch is exactly G. The transform of G_chi is
-L'(s, chi)/L(s, chi) * 1/(s (s - 1)) + (L'/L)(1, chi)/(s - 1), analytic at s = 1 because L(s, chi) is analytic and
not zero at 1, so the first term has a simple pole there with residue -(L'/L)(1, chi), which the second cancels.
For a finite family F of characters chi_i with weights a_i > 0 the development uses
Gm(F, x) = sum of a_i Re G_(chi_i)(x). (`Formalism.Gchi` of `StatementOC.lean` is a different object, built on the
real parts of chi(n); it is not the one used here.)

## 2. The lemma

Lemma W (Landau's theorem on windows). Let g be a real, locally integrable function on [0, infinity) with
|g(u)| <= A e^(B u) for some A > 0 and some real B. Let Phi(s) be the integral of g(u) e^(-s u) over u >= 0, for
Re s > B. Assume:

(a) Phi extends to a meromorphic function on a half-plane Re s > theta_0, all of whose poles there are simple, and
    at every real pole the residue is positive.

(b) There are numbers theta in (theta_0, B), delta in (0, 1], eta >= 0, R > 0 and arbitrarily large U such that

        g(u) <= R e^(theta u + eta U)        for every u in [U, (1 + delta) U].

Then every pole rho of Phi in Re s > theta_0 satisfies Re rho <= theta + eta.

In particular, if (b) holds for every eta > 0 (with R and the set of U depending on eta), Phi has no pole with
real part larger than theta.

Remarks. (i) Only an upper bound for g is assumed, and only on the windows. (ii) With x = e^u, the window is
[Y, Y^(1 + delta)] and the bound is G(x) <= R Y^eta x^theta. (iii) Nothing is asked of the residues at the non-real
poles. Since g is real, Phi(conj s) = conj Phi(s), so the residue at a real pole is a real number, and (a) says it
is not negative. That cannot be dropped: g(u) = -e^(beta u) satisfies (b) for every theta and its transform
-1/(s - beta) has a pole at beta. (iv) The formal statement `Deduction.landau_window` has hypotheses
`PoleData g Phi Z` (g measurable with |g(u)| <= C e^(2u); Phi the Laplace transform for Re s > 2; Z a set of
isolated points of Re s > 0 off which Phi is holomorphic there; at every point of Z a simple pole with a nonzero
residue, and a positive real residue when the point is real), 0 < theta < 1, delta > 0 and `WindowHypU g theta
delta` (for every eta > 0 and arbitrarily large U, a nonnegative majorant R(u) of g on [U, (1 + delta) U], with
R(u) e^(-theta u) integrable on the window, whose integral against e^(-theta u) over the window is at most
e^(eta U)); its conclusion is `for every rho in Z,
rho.re <= theta`. So (a) is the residue clause of `PoleData` with theta_0 = 0 and B = 2. Hypothesis (b), asked for
every eta > 0, gives the integrated form for every eta > 0 (the pointwise majorant R e^(theta u + eta U) has
integral R delta U e^(eta U) against e^(-theta u), which is below e^(eta' U) for every eta' > eta and large U).
Conversely the proof below adapts to the integrated form: in (6) one bounds the kernel u^k e^(-(sigma - theta) u)
by its maximum (k/(e (sigma - theta)))^k <= k!/(sigma - theta)^k instead of integrating it, which changes one power
of sigma - theta and nothing in the conclusion. (v) Version 1 of this note assumed a residue of positive real part
at every pole, and used the fixed kernel 1 + cos(tau u) with the real parts of the coefficients. The reviewer
pointed out that the formal lemma asks less. The transforms of Section 4 satisfy the stronger assumption too, so
both versions cover them.

## 3. Proof of Lemma W

Notation. For a point z with Re z > B and an integer k >= 0 put a_k(z) = (-1)^k Phi^(k)(z)/k!, so that

    k! a_k(z) = integral of g(u) u^k e^(-z u) du        and        Phi(s) = sum over k of a_k(z) (z - s)^k near z.      (4)

For a real point sigma > B the number a_k(sigma) is real. A simple pole c/(s - p) contributes c/(z - p)^(k+1) to
a_k(z).

Suppose rho_0 is a pole with beta_0 = Re rho_0 > theta, and put tau = Im rho_0.

Step 1 (the kernel; changed in version 2). Let gamma and alpha be real and w(u) = 1 + cos(gamma u - alpha), which
is nonnegative and at most 2. Since cos(gamma u - alpha) is the real part of e^(i alpha) e^(-i gamma u) and g is
real, for real sigma > B,

    integral of g(u) w(u) u^k e^(-sigma u) du = k! ( a_k(sigma) + Re( e^(i alpha) a_k(sigma + i gamma) ) ).      (5)

Choosing alpha, for the given k and gamma, so that e^(i alpha) a_k(sigma + i gamma) = |a_k(sigma + i gamma)|, the
right side is k! ( a_k(sigma) + |a_k(sigma + i gamma)| ).

Step 2 (an upper bound). Fix sigma > B. Take U as in (b) and W = [U, (1 + delta) U]. Let w be any function with
0 <= w <= 2. On W, g w <= R e^(theta u + eta U) w <= 2 R e^(eta U) e^(theta u) (the first step uses w >= 0, the
second w <= 2 and R > 0). Off W, |g w| <= 2 A e^(B u). Hence

    integral of g w u^k e^(-sigma u) du <= 2 R e^(eta U) * integral over u >= 0 of u^k e^(-(sigma - theta) u) du
                                           + 2 A * integral over u outside W of u^k e^(-(sigma - B) u) du
                                         = 2 R e^(eta U) k!/(sigma - theta)^(k+1) + 2 A T_k(U).            (6)

The measure u^k e^(-(sigma - B) u) du has total mass k!/(sigma - B)^(k+1) and is that mass times the law of a
Gamma variable X with shape k + 1 and rate sigma - B, of mean mu = (k + 1)/(sigma - B). Put epsilon = delta/4 and
let K(U) be the set of integers k with

    (sigma - B) U/(1 - epsilon) <= k    and    (k + 1)(1 + epsilon/2) <= (sigma - B)(1 + delta) U.           (7)

Because (1 + delta)(1 - epsilon) > 1 + epsilon, K(U) is an interval of integers whose length tends to infinity
with U (its length is at least delta (sigma - B) U/3 - 2). For k in K(U): U <= (1 - epsilon) mu and
(1 + delta) U >= (1 + epsilon/2) mu. The Chernoff bounds for the Gamma law,
P(X <= (1 - a) mu) <= exp(-(k + 1) a^2/2) and P(X >= (1 + a) mu) <= exp(-(k + 1)(a - log(1 + a))) with
a - log(1 + a) >= a^2/3 for 0 < a <= 1/2, give

    T_k(U) <= 2 exp(-kappa (k + 1)) k!/(sigma - B)^(k+1),        kappa = epsilon^2/12 = delta^2/192.       (8)

Now choose sigma so large that sigma >= B + (B - theta)/kappa. Then (sigma - theta)/(sigma - B) = 1 + (B -
theta)/(sigma - B) <= 1 + kappa <= e^kappa, so the second term of (6) is at most 4 A k!/(sigma - theta)^(k+1).
With the kernel and the phase of Step 1 this reads

    a_k(sigma) + |a_k(sigma + i gamma)| <= (2 R e^(eta U) + 4 A)/(sigma - theta)^(k+1)
                                        for every real gamma, every U of (b) and every k in K(U).          (9)

Step 3 (a lower bound from the nearest poles; changed in version 2). The poles of Phi in Re s > theta_0 are a
closed discrete subset of that half-plane and have real part at most B, so they lie to the left of sigma. For real
gamma let

    D(gamma) = the smaller of sigma - theta_0 and the distance from sigma + i gamma to the set of poles.

Phi is analytic in the open disc of centre sigma + i gamma and radius D(gamma). When D(gamma) < sigma - theta_0 the
closed disc of that radius is a compact subset of the half-plane, so it contains finitely many poles, and at least
one of them is on its boundary. Since rho_0 is at distance sigma - beta_0 from sigma + i tau,

    D(tau) <= sigma - beta_0 < sigma - theta < sigma - theta_0.

The expansion at a centre. Let z = sigma + i gamma with d = D(gamma) < sigma - theta_0, let P be the finite set of
poles at distance d from z, and c_p the residue at p. Choose d' with d < d' < sigma - theta_0 such that the closed
disc of centre z and radius d' contains no pole outside P (possible: the closed disc of radius
(d + sigma - theta_0)/2 contains finitely many poles). Subtracting the principal parts, Phi(s) minus the sum over p
in P of c_p/(s - p) is analytic on a neighbourhood of that disc. Writing z - p = d e^(-i phi(p)) and using Cauchy's
inequality for the analytic remainder,

    a_k(z) = d^(-(k+1)) Tr(k + 1) + E_k,     Tr(n) = sum over p in P of c_p e^(i n phi(p)),     |E_k| <= M (d')^(-k).   (10)

Claim. There are c > 0 and an integer L such that every interval of L consecutive integers contains n with
|Tr(n)| >= c.

Proof of the claim. The points of P are distinct points of one circle, so the numbers e^(i phi(p)) are distinct,
and the residues c_p are not zero. The vectors (e^(i n phi(p))), n = 0, ..., |P| - 1, indexed by p in P, are
linearly independent (a Vandermonde determinant), so Tr(n_0) is not zero for some n_0 with 0 <= n_0 < |P|. Put
2c = |Tr(n_0)|. For every nu > 0 the set of integers t such that every t phi(p)/(2 pi), p in P, is within nu of an
integer is relatively dense: there is L_0 with at least one such t in every interval of L_0 consecutive integers.
(This is the relative density of the almost periods of a trigonometric polynomial. Proof: in the torus R^P/Z^P the
closure H of the points t alpha, t >= 0, alpha = (phi(p)/(2 pi)), is a compact group; the forward orbit is dense in
it, so by compactness there is L_0 such that every point of H is within nu of some t alpha with 0 <= t < L_0;
applying this to the point -N alpha gives such a t' = N + t in any interval [N, N + L_0).) For such t,
|Tr(n_0 + t) - Tr(n_0)| <= 2 pi nu times the sum of |c_p|, which is at most c for nu small. So the integers
n = n_0 + t with |Tr(n)| >= c are relatively dense. QED.

With (10) and d' > d the claim gives k_0 such that

    |a_k(z)| >= (c/2) d^(-(k+1))     for every k >= k_0 with |Tr(k + 1)| >= c.                           (11)

Two cases, for the fixed sigma.

Case A: D(gamma) >= D(0) for every real gamma. Then D(0) <= D(tau) <= sigma - beta_0 < sigma - theta_0, so there
are poles at distance D(0) from sigma. Let p be one. If p were not real, the point sigma + i Im p would be at
distance sigma - Re p < |sigma - p| = D(0) from p, so D(Im p) < D(0), against the case. So p is real, hence
p = sigma - D(0), and it is the only pole at that distance. Apply (10) at z = sigma with d = D(0) and
P = {p}: the angle is 0 and Tr(n) is the residue c_p for every n, which is positive by (a). Hence
a_k(sigma) >= c_p d^(-(k+1)) - M (d')^(-k) >= (c_p/2) d^(-(k+1)) for every large k, and a fortiori, for every
gamma, a_k(sigma) + |a_k(sigma + i gamma)| >= (c_p/2) d^(-(k+1)). Here d = D(0) <= sigma - beta_0.

Case B: D(gamma) < D(0) for some real gamma. Such a gamma can be chosen with D(gamma) <= sigma - beta_0: if
D(tau) < D(0) take gamma = tau; otherwise D(0) <= D(tau) <= sigma - beta_0 and any gamma of the case will do. Put
z = sigma + i gamma and d = D(gamma); then d < D(0) <= sigma - theta_0, so (10), the claim and (11) apply at z.
Phi is analytic in the open disc of centre sigma and radius D(0); fix e with d < e < D(0). Cauchy's inequality
gives |a_k(sigma)| <= M' e^(-k). So for k >= k_0 with |Tr(k + 1)| >= c,
a_k(sigma) + |a_k(sigma + i gamma)| >= (c/2) d^(-(k+1)) - M' e^(-k) >= (c/4) d^(-(k+1)) once (e/d)^k >= 4 M' d/c.

In both cases there are a real gamma, a number d <= sigma - beta_0, a constant c_* > 0 and integers L and k_1,
all depending on sigma and not on U, such that every interval of L consecutive integers k >= k_1 contains k with

    a_k(sigma) + |a_k(sigma + i gamma)| >= c_* d^(-(k+1)).                                              (12)

Step 4 (contradiction; constants changed in version 2). Take U as in (b), so large that K(U) has more than L
elements and lies above k_1. It contains k as in (12), and (9) and (12) give

    ((sigma - theta)/d)^(k+1) <= (2 R e^(eta U) + 4 A)/c_*.

Since d <= sigma - beta_0 and log(1 + y) >= y/(1 + y), the left side is at least
exp((k + 1)(beta_0 - theta)/(sigma - theta)), and k + 1 > (sigma - B) U by (7). Hence

    exp( (beta_0 - theta) U (sigma - B)/(sigma - theta) ) <= (2 R e^(eta U) + 4 A)/c_*

for arbitrarily large U, with A, R, c_* independent of U. So (beta_0 - theta)(sigma - B)/(sigma - theta) <= eta.
This holds for every admissible sigma, and the factor (sigma - B)/(sigma - theta) tends to 1 as sigma grows, so
beta_0 <= theta + eta. QED.

The order of the limits is the point to check: U tends to infinity at a fixed sigma, and only then sigma tends to
infinity; gamma, d, c_*, L and k_1 depend on sigma, and none of them on U. When (b) holds for every eta > 0, one
fixed sigma is enough (let eta tend to 0), which is how the formal development concludes.

## 4. Application to the zeta function and to Dirichlet L-functions

Theorem E (the end of the proof, for zeta). Let 0 < theta < 1 and suppose there is delta > 0 such that for every
eta > 0 there are arbitrarily large Y with

    G(x) <= Y^eta x^theta        for every x in [Y, Y^(1 + delta)].

Then zeta(s) is not 0 for Re s > theta. With theta = 1/2 this is the Riemann hypothesis.

Proof. Replace delta by min(delta, 1); the hypothesis on [Y, Y^(1 + delta)] implies it on the smaller window. Apply
Lemma W to g(u) = G(e^u), whose Laplace transform is Phi of (1) (the integral over x >= 1 of G(x) x^(-s-1) dx with
x = e^u). Growth: T(x) = log x + O(1) (Mertens) and psi(x) = O(x) (Chebyshev), so S(x) = x T(x) - psi(x) =
x log x + O(x), |G(x)| <= A x for x >= 1, and B = 1 > theta. Poles: by Lemma 1 the poles of Phi in Re s > 0 are the
nontrivial zeros, simple poles with residue -m(rho)/(rho (rho - 1)); zeta has no zero on the real axis to the right
of 1 (Euler product), and at a real zero beta in (0, 1) the residue would be m(beta)/(beta (1 - beta)) > 0. So (a)
holds on Re s > theta_0 for every theta_0 in (0, theta). Hypothesis (b) is the assumption, with U = log Y and
R = 1. Lemma W gives Re rho <= theta + eta for every eta > 0. QED.

(For the transforms of this section more is true than (a) asks: with rho = beta + i t, 0 < beta < 1, the real part
of -1/(rho (rho - 1)) is (t^2 + beta (1 - beta))/|rho (rho - 1)|^2 > 0 at every pole. Version 1 used that.)

Families. For a finite family of Dirichlet characters with positive weights the same proof applies to
g(u) = Gm(F, e^u). Since conj (L'/L)(1, chi) = (L'/L)(1, conj chi), Re G_chi is the half-sum of G_chi and
G_(conj chi), so the transform is the sum over i of a_i times the half-sum of the transforms for chi_i and its
conjugate. Growth: |Re G_chi(x)| <= S(x) + |(L'/L)(1, chi)| x because x/n - 1 >= 0 and |chi(n)| <= 1, so
|Gm(F, x)| = O(x log x) <= A x^2 and Lemma W applies with B = 2. Poles in Re s > 0: simple, at the zeros of the
L(s, chi_i) and of their conjugates, with residue -M(rho)/(rho (rho - 1)), where
M(rho) = sum over i of a_i (m_i(rho) + m'_i(rho))/2, m_i and m'_i the multiplicities of rho as a zero of
L(s, chi_i) and of L(s, conj chi_i). Because the weights are positive, M(rho) > 0 at every zero of every member:
no cancellation between characters can hide a zero. No L(s, chi) vanishes on the real axis at or to the right of 1
(L(1, chi) is not 0; Euler product beyond), and at a real zero beta in (0, 1) the residue is
M(beta)/(beta (1 - beta)) > 0. This is the reason a possible real zero needs no separate treatment. The formal
development packages the poles and residues as `PoleData`, whose field `pole` asks positivity only at real poles
(the residues themselves come from `poleData_char`), and derives the nonvanishing for Re s >= 1 separately (`Deduction.lemmaL`).

## 5. What this does and does not check

- It checks, by a proof on paper, the implication 'one-sided bound of order x^(theta + o(1)) on windows
  [Y, Y^(1 + delta)] for arbitrarily large Y implies no zero to the right of theta', which is the content of the
  last step of the formal proof as its statements read: Lemma W under hypothesis (a), with theta_0 = 0, B = 2 and
  (b) in the integrated form of remark (iv), implies `Deduction.landau_window`, and Theorem E and the families paragraph are those of
  `Deduction.zeroFree_of_rpow_window` and `Deduction.lemmaL`. The proof here was written from the statements, not
  translated from the Lean proof terms. Shared with the formal route, as its statements show (`landau_window_key`,
  `landau_window_ineq`, `landau_tails`): the Taylor coefficients at a real point sigma and at sigma + i gamma, the
  second taken in modulus through a phase chosen for each order k, a nonnegative kernel bounded by 2, one window
  per order, and positivity used only at a real nearest pole. Different: the formal route selects gamma so that the
  nearest pole to sigma + i gamma is the only one in a ball (`landau_dichotomy`, `landau_nearest`), where this note
  allows several poles at the least distance and uses the relative density of the orders at which their sum is not
  small; and the formal route fixes sigma and lets eta tend to 0, where this note lets sigma grow at a fixed eta,
  which gives the bound theta + eta from a single eta.
- It does not check that the windows exist. In the formal development the one-sided bound comes from the
  arithmetic geometry of the rest of the archive (families of Hermitian lattices, a slope inequality, period
  identities); that is where all the depth is, and nothing here bears on it.
- By (3) the bound that has to be supplied is far from sharp in size: under the hypothesis, |G(x) - log 2 pi| is at
  most 0.0462 sqrt(x) + 0.31/x^2 (and EXP-029 measured at most 0.0247 sqrt(x) up to 10^8). What is hard is to prove
  any bound of the order x^(1/2 + epsilon) from above, on any window.

## How could this be wrong?

- Hypothesis (a) enters in Case A of Step 3 (the positive residue at the real nearest pole) and through the
  simplicity of the poles, which gives the form of (10); a function with a real pole of negative residue to the
  right of theta is not covered, and the lemma is false for it (remark (iii)).
- Case B rests on the claim: distinct points of a circle and nonzero residues. The claim is proved by a Vandermonde
  determinant and a compactness argument on the finitely many angles of P; no independence of the angles is needed.
- The order of the limits (end of Section 3): every constant of Step 3 depends on sigma and none on U.
- The Chernoff constants in (8) are not optimized; only kappa > 0 matters. The reviewer recomputed the exact Gamma
  tails against (8) in 72 cases (worst ratio 0.0886) and the length of K(U) in 24.
- Classical inputs used without proof here: the analytic continuation of zeta and of L(s, chi); L(1, chi) not 0
  (to define G_chi and for the analyticity at 1); no zero on the real axis to the right of 1 (Euler product); the
  theorems of Mertens and Chebyshev (growth); and, for Lemma 2 only, the bounds of zeta'/zeta on horizontal
  segments and to the left.
- The lemma is about real g. The complex-valued sums for non-real characters enter only through their real parts,
  as in the formal development.
- The comparison with the Lean statements is a reading of statements (`PoleData`, `WindowHypU`, `landau_window`,
  `landau_window_key`, `landau_dichotomy`, `landau_nearest` were opened; their proofs were not followed).

## Review record

- Version 1 (commit a6f70991): reviewed on 2026-11-21 by a reader other than the writer. Findings F1 to F10
  (two major: the residue hypothesis against `PoleData`, and the proof of Lemma 2; eight minor) are applied here.
  The reviewer's scripts and logs are under the data root,
  `caos-research/riemann-hypothesis/claim-2026-11-20/review-windowed-landau/`.
- Version 2: Step 1, Step 3 (the claim, Case A, Case B) and Step 4 are new text. Second reading by the same reviewer
  on 2026-11-21 (addendum of the same report): Lemma W true as written under positivity at real poles only, with a
  single eta and a general real B; no counterexample found (the attempts need a negative residue at a real pole);
  formula (5) and the pole term checked numerically; Steps 2 to 4, the new proof of Lemma 2, Theorem E and the
  families paragraph correct; findings G1 to G5, all minor, applied in this text. A proof read twice by one reviewer
  is not a refereed proof.
