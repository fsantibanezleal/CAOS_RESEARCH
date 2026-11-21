# The analytic end of the 2026-11-20 formal proof: a one-sided bound on windows excludes zeros (a human proof)

Date: 2026-11-21. Status: derivation [D] by the coordinating session, written for the review of the claimed proof
of the Riemann hypothesis released on 2026-11-20 (dossier `2026-11-21-claimed-proof-review.md`). Not yet read by a
reviewer other than the writer. The statement proved here is classical in kind (Landau's theorem on Dirichlet
integrals of one sign, localized to windows); no priority is claimed. Its purpose is narrow: the Lean development
ends with a lemma of this shape (`Deduction.landau_window`, `Deduction.zeroFree_of_rpow_window`), and this note
gives a complete proof a person can check in an hour, so that the last step of the formal proof is understood
independently of the kernel. It says nothing about the rest of the formal proof, which is where the one-sided bound
itself is obtained.

## 1. The objects

Lambda is the von Mangoldt function and gamma is Euler's constant. For x >= 1 put

    S(x) = sum over n <= x of Lambda(n) (x/n - 1),        G(x) = S(x) - x log x + (1 + gamma) x.

These are `Formalism.Sz` and `Formalism.Gz` of the formal development (`src/Formalism/StatementOC.lean`, read at
commit 23aebbb3 of the mirror `leanprover-community/riemann-hypothesis`). With T(t) = sum over n <= t of
Lambda(n)/n and psi(t) = sum over n <= t of Lambda(n) one has S(x) = x T(x) - psi(x), and S is the integral of T
from 1 to x.

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

Lemma 2 (explicit formula). For x > 1,

    G(x) = - sum over nontrivial zeros rho of x^rho/(rho (rho - 1)) + log 2 pi
           - sum over k >= 1 of x^(-2k)/(2k (2k + 1)),                                              (2)

the sum over zeros counted with multiplicity and absolutely convergent.

Proof. Mellin inversion of (1) on a vertical line Re s = c > 1 and a shift of the line to the left; the factor
1/(s (s - 1)) makes every integral and the sum over zeros absolutely convergent (sum of 1/|rho|^2 converges), so
there is no conditional convergence to treat. The residues are those listed, at s = -2k the residue of
-zeta'/zeta is -1. QED.

Consequence 3 (what the hypothesis gives back). If every nontrivial zero has real part 1/2, then
|rho (rho - 1)| = |rho|^2 and the sum over zeros of 1/|rho|^2 equals the sum of (1/rho + 1/(1 - rho)), which is
2 + gamma - log 4 pi = 0.0461914179... (the classical value of the sum of 1/rho, taken twice). So under the
Riemann hypothesis, for every x >= 1,

    | G(x) - log 2 pi | <= (2 + gamma - log 4 pi) sqrt(x) + (1 - log 2)/x^2.                       (3)

(The last term bounds the sum over k in (2), since the sum of 1/(2k (2k + 1)) is 1 - log 2. At x = 1 formula (2)
reads 1 + gamma = log 2 pi + (2 + gamma - log 4 pi) - (1 - log 2), which is an identity, and (2) holds for x >= 1.)

A bound of the order sqrt(x) in both directions is therefore equivalent to the Riemann hypothesis; the point of
Section 3 is that a bound from above alone, of the order x^(1/2 + epsilon), on a sparse family of windows, already
suffices. EXP-029 checks (2) and the constant of (3) numerically.

For a Dirichlet character chi other than the trivial character of modulus 1 the formal development uses
(`Deduction.Gchi`, `src/Development/AutomorphicArithmetic/DedekindLFunctions/CharFamily.lean`)

    G_chi(x) = sum over n <= x of Lambda(n) chi(n) (x/n - 1) + x L'(1, chi)/L(1, chi),

whose transform is -L'(s, chi)/L(s, chi) * 1/(s (s - 1)) + (L'/L)(1, chi)/(s - 1), analytic at s = 1 for the same
reason. For a finite family F of characters chi_i with weights a_i > 0 it uses
Gm(F, x) = sum of a_i Re G_(chi_i)(x), with the trivial character of modulus 1 allowed and treated as in (1).

## 2. The lemma

Lemma W (Landau's theorem on windows). Let g be a real, locally integrable function on [0, infinity) with
|g(u)| <= A e^(B u) for some A > 0, B >= 1. Let Phi(s) be the integral of g(u) e^(-s u) over u >= 0, for
Re s > B. Assume:

(a) Phi extends to a meromorphic function on a half-plane Re s > theta_0, all of whose poles there are simple, and
    every pole rho has a residue r(rho) with Re r(rho) > 0.

(b) There are numbers theta in (theta_0, B), delta in (0, 1], eta >= 0, R > 0 and arbitrarily large U such that

        g(u) <= R e^(theta u + eta U)        for every u in [U, (1 + delta) U].

Then every pole rho of Phi in Re s > theta_0 satisfies Re rho <= theta + eta.

In particular, if (b) holds for every eta > 0 (with R and the set of U depending on eta), Phi has no pole with
real part larger than theta.

Remarks. (i) Only an upper bound for g is assumed, and only on the windows. (ii) With x = e^u, the window is
[Y, Y^(1 + delta)] and the bound is G(x) <= R Y^eta x^theta. (iii) The formal statement
`Deduction.landau_window` has hypothesis `WindowHypU g theta delta` (for every eta > 0, arbitrarily large U, a
majorant R(u) of g on [U, (1 + delta) U] whose integral against e^(-theta u) is at most e^(eta U)) and conclusion
`for every rho in Z, rho.re <= theta`; `Deduction.zeroFree_of_rpow_window` specializes it to
Gm(F, y) <= C y^theta on [Y, Y^(1 + delta)] for arbitrarily large Y. Hypothesis (b) with a pointwise majorant is a
special case of the integrated form. The proof below adapts to the integrated form: in (6) one bounds the kernel
u^k e^(-(sigma - theta) u) by its maximum (k/(e (sigma - theta)))^k <= k!/(sigma - theta)^k instead of integrating
it, which changes one power of sigma - theta and nothing in the conclusion.

## 3. Proof of Lemma W

Suppose rho_0 is a pole with beta_0 = Re rho_0 > theta. Put tau = Im rho_0 and w(u) = 1 + cos(tau u), which is
nonnegative and at most 2. For Re s > B put

    F(s) = integral of g(u) w(u) e^(-s u) du = Phi(s) + (1/2) Phi(s + i tau) + (1/2) Phi(s - i tau).      (4)

Step 1 (the poles of F). F is meromorphic on Re s > theta_0. Since g is real, Phi(conj s) = conj Phi(s), so the
poles of Phi are symmetric about the real axis with conjugate residues. A point p is a pole of at most the three
terms of (4), each simple, and the residue of F at p is

    R(p) = r(p) + (1/2) r(p + i tau) + (1/2) r(p - i tau),

where r is taken to be 0 at a point that is not a pole of Phi. By (a) each of the three numbers has nonnegative
real part, positive when the point is a pole. So no cancellation occurs: p is a pole of F exactly when one of
p, p + i tau, p - i tau is a pole of Phi, and then Re R(p) > 0. In particular the real point beta_0 is a pole of F
(because beta_0 + i tau = rho_0). Also F(conj s) = conj F(s), so R(conj p) = conj R(p).

Step 2 (an upper bound for the Taylor coefficients at a real point). Fix sigma > B. For k >= 0 let

    c_k = F^(k)(sigma)/k!,        so that        (-1)^k k! c_k = integral of g(u) w(u) u^k e^(-sigma u) du.      (5)

Take U as in (b) and W = [U, (1 + delta) U]. On W, g w <= R e^(theta u + eta U) w <= 2 R e^(eta U) e^(theta u)
(the middle step uses w >= 0, the last one w <= 2 and R > 0). Off W, |g w| <= 2 A e^(B u). Hence

    (-1)^k k! c_k <= 2 R e^(eta U) * integral over u >= 0 of u^k e^(-(sigma - theta) u) du
                     + 2 A * integral over u outside W of u^k e^(-(sigma - B) u) du
                   = 2 R e^(eta U) k!/(sigma - theta)^(k+1) + 2 A T_k(U).                               (6)

The measure u^k e^(-(sigma - B) u) du has total mass k!/(sigma - B)^(k+1) and is that mass times the law of a
Gamma variable X with shape k + 1 and rate sigma - B, of mean mu = (k + 1)/(sigma - B). Put epsilon = delta/4 and
let K(U) be the set of integers k with

    (sigma - B) U/(1 - epsilon) <= k    and    (k + 1)(1 + epsilon/2) <= (sigma - B)(1 + delta) U.           (7)

Because (1 + delta)(1 - epsilon) > 1 + epsilon, K(U) is an interval of integers whose length tends to infinity
with U (its length is at least c_0 delta (sigma - B) U - 2 for an absolute c_0 > 0). For k in K(U): U <= (1 -
epsilon) mu and (1 + delta) U >= (1 + epsilon/2) mu. The Chernoff bounds for the Gamma law,
P(X <= (1 - a) mu) <= exp(-(k + 1) a^2/2) and P(X >= (1 + a) mu) <= exp(-(k + 1)(a - log(1 + a))) with
a - log(1 + a) >= a^2/3 for 0 < a <= 1/2, give

    T_k(U) <= 2 exp(-kappa (k + 1)) k!/(sigma - B)^(k+1),        kappa = epsilon^2/12 = delta^2/192.       (8)

Now choose sigma so large that sigma >= B + (B - theta)/kappa. Then (sigma - theta)/(sigma - B) = 1 + (B -
theta)/(sigma - B) <= 1 + kappa <= e^kappa, so the second term of (6) is at most 4 A k!/(sigma - theta)^(k+1), and

    (-1)^k c_k <= (2 R e^(eta U) + 4 A)/(sigma - theta)^(k+1)      for every U of (b) and every k in K(U).      (9)

Step 3 (a lower bound from the nearest poles). Let d be the least distance from sigma to a pole of F. By Step 1,
d <= sigma - beta_0 < sigma - theta. The closed disc of centre sigma and radius sigma - beta_0 lies in
Re s >= beta_0 > theta_0, a region where the poles of F are a closed discrete set, so it contains finitely many of
them. Let P be the set of poles at distance exactly d and choose d' with d < d' < sigma - theta such that P is the
set of all poles in the closed disc of radius d'. Subtracting the principal parts, F(s) minus the sum over p in P
of R(p)/(s - p) is analytic on a neighbourhood of that disc; the k-th Taylor coefficient of R(p)/(s - p) at sigma
is (-1)^k R(p)/(sigma - p)^(k+1). Writing sigma - p = d e^(-i phi(p)) and using Cauchy's inequality for the
analytic remainder,

    (-1)^k c_k = d^(-(k+1)) Tr(k + 1) + E_k,     Tr(n) = sum over p in P of R(p) e^(i n phi(p)),     |E_k| <= M (d')^(-k). (10)

P is symmetric about the real axis and R(conj p) = conj R(p), so Tr(n) is real. Moreover

    Tr(0) = sum over p in P of R(p) = sum over p in P of Re R(p) > 0.

Put 2c = Tr(0). For every nu > 0 the set of integers n such that every n phi(p)/(2 pi), p in P, is within nu of
an integer is relatively dense: there is L with at least one such n in every interval of L consecutive integers.
(This is the relative density of the almost periods of a trigonometric polynomial. Proof: in the torus R^P/Z^P the
closure H of the points n alpha, n >= 0, alpha = (phi(p)/(2 pi)), is a compact group; the forward orbit is dense in
it, so by compactness there is L such that every point of H is within nu of some t alpha with 0 <= t < L; apply this
to the point -N alpha to find n = N + t in any interval [N, N + L).) For such n, |Tr(n) - Tr(0)| <= 2 pi nu times the sum
of |R(p)|, which is at most c for nu small. So there is L such that every interval of L consecutive integers
contains n with Tr(n) >= c. With (10) and d' > d this gives k_0 such that

    (-1)^k c_k >= (c/2) d^(-(k+1))     for every k >= k_0 with Tr(k + 1) >= c.                           (11)

Step 4 (contradiction). Take U as in (b), so large that K(U) has more than L elements and lies above k_0. It
contains k with Tr(k + 1) >= c, and (9) and (11) give

    ((sigma - theta)/d)^(k+1) <= (4 R e^(eta U) + 8 A)/c.

Since d <= sigma - beta_0 and log(1 + y) >= y/(1 + y), the left side is at least
exp((k + 1)(beta_0 - theta)/(sigma - theta)), and k + 1 > (sigma - B) U by (7). Hence

    exp( (beta_0 - theta) U (sigma - B)/(sigma - theta) ) <= (4 R e^(eta U) + 8 A)/c

for arbitrarily large U, with A, R, c independent of U. So (beta_0 - theta)(sigma - B)/(sigma - theta) <= eta.
This holds for every admissible sigma, and the factor (sigma - B)/(sigma - theta) tends to 1 as sigma grows, so
beta_0 <= theta + eta. QED.

## 4. Application to the zeta function and to Dirichlet L-functions

Theorem E (the end of the proof, for zeta). Suppose there is delta > 0 such that for every eta > 0 there are
arbitrarily large Y with

    G(x) <= Y^eta x^theta        for every x in [Y, Y^(1 + delta)].

Then zeta(s) is not 0 for Re s > theta. With theta = 1/2 this is the Riemann hypothesis.

Proof. Apply Lemma W to g(u) = G(e^u), whose Laplace transform is Phi of (1) (the integral over x >= 1 of
G(x) x^(-s-1) dx with x = e^u). Growth: S(x) <= x T(x) and T(x) = log x + O(1) (Mertens), so |G(x)| <= A x and
B = 1. Poles: by Lemma 1 the poles of Phi in Re s > 0 are the nontrivial zeros, simple poles with residue
r(rho) = -m(rho)/(rho (rho - 1)). With rho = beta + i t, 0 < beta < 1,

    Re( -1/(rho (rho - 1)) ) = (t^2 + beta (1 - beta))/|rho (rho - 1)|^2 > 0,

so (a) holds on Re s > theta_0 for every theta_0 in (0, theta). Hypothesis (b) is the assumption, with U = log Y.
QED.

For a finite family of Dirichlet characters with positive weights the same proof applies to
g(u) = Gm(F, e^u): its transform is the sum over i of a_i times the half-sum of the transforms for chi_i and its
conjugate, the pole at a zero rho has residue -M(rho)/(rho (rho - 1)) with M(rho) > 0 a weighted sum of
multiplicities, and the real part of the residue is positive for 0 < Re rho < 1 by the same computation,
including at a real zero (where it is M(beta)/(beta (1 - beta)) > 0). This is the reason a possible real zero
needs no separate treatment. The formal development packages these facts as `PoleData` and derives the
nonvanishing for Re s >= 1 separately (`Deduction.lemmaL`).

## 5. What this does and does not check

- It checks, by a proof on paper, the implication 'one-sided bound of order x^(theta + o(1)) on windows
  [Y, Y^(1 + delta)] for arbitrarily large Y implies no zero to the right of theta', which is the content of the
  last step of the formal proof as its statements read. The proof here was written from the statements, not
  translated from the Lean proof terms; the two agree in strategy (Taylor coefficients at a point sigma + i t
  together with the real point sigma, a positive kernel, a single window per order k), as the names
  `landau_coeff`, `landau_window_ineq`, `landau_tails`, `landau_nearest`, `landau_pole_asym` and the inequality of
  `landau_window_key` show.
- It does not check that the windows exist. In the formal development the one-sided bound comes from the
  arithmetic geometry of the rest of the archive (families of Hermitian lattices, a slope inequality, period
  identities); that is where all the depth is, and nothing here bears on it.
- By (3) the bound that has to be supplied is far from sharp in size: the truth is of order 0.046 sqrt(x) in both
  directions. What is hard is to prove any bound of the order x^(1/2 + epsilon) from above, on any window.

## How could this be wrong?

- Step 3 uses that the poles at the least distance have residues whose real parts are positive, so that their sum
  cannot vanish; this is where hypothesis (a) enters and it is the only place. A function with a pole of residue of
  negative real part to the right of theta is not covered (for the transforms of Section 4 there is none).
- The Chernoff constants in (8) are not optimized; only kappa > 0 matters.
- The relative density of the simultaneous approximations is a compactness argument on the finitely many angles
  of P; no independence of the angles is needed.
- The lemma is about real g. The complex-valued sums for non-real characters enter only through their real parts,
  as in the formal development.
