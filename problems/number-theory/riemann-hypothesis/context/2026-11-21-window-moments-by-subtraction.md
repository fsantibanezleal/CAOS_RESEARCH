# The two discrete moments on a window, by subtraction: which terms of the published argument pass and which need work

Date: 2026-11-21. Status: a reduction [D] by the coordinating session for focus RH-F17 (backlog RH-058), written on
the exact transcription of the two source papers made the same day
(`wip/caos-research/rh-f17-contour-formulas-2026-11-21.md` of the coordination repository: Conrey, Ghosh and Gonek,
Proc. London Math. Soc. (3) 76 (1998), cited as CGG with its equation numbers; Bui and Heath-Brown,
arXiv:1302.5018v1, cited as BHB). Marks: [S] as printed in a source, with its number; [D] derived here; [I] an input
that is named and not proved here. Read on 2026-11-21 by a reviewer other than the writer (second round of the report
`wip/caos-research/rh-f17-notes-review-2026-11-21.md`): the additivity argument, formulas (1) to (7) and the
arithmetic of Section 5 confirmed by hand and by symbolic computation, the reduction valid and the inputs well
posed; six minor findings, applied here. It does not prove target T1 of
`2026-11-21-short-window-discrete-moments-target.md`; it reduces T1 to three named inputs and says what each needs.

Notation of CGG: L = log(T/2 pi); B(s) = sum over k <= y of b(k) k^(-s), b(k) = mu(k) P(log(y/k)/log y), y = T^nu
(CGG write theta for nu); S_1(T) and S_2(T) the sums of B(rho) zeta'(rho) and of B(rho) zeta'(rho) B(1 - rho)
zeta'(1 - rho) over the zeros with gamma <= T. Throughout, T_0 = T, T_1 = T + H, H = T^theta with 1/2 < theta < 1,
and both T_0 and T_1 are at distance >> 1/L from every ordinate (CGG assume this of T, p. 501; see Section 5). The
identities at the two heights are taken on one vertical line, with the abscissa c = 1 + 1/L(T_0) in both (CGG take
c = 1 + 1/L at the height in question); the estimates of CGG Section 3 and their Lemmas 1 and 2 hold for it at both
heights, since they are uniform for c in a fixed range and use only that c - 1 is of order 1/log T.

## 1. The published identities are additive in the height

[S] CGG write S_1 and S_2 as integrals over the rectangle with vertices 1 - c + i, c + i, c + iT, 1 - c + iT,
c = 1 + 1/L ((2.8) to (2.10)), and obtain

    S_1(T) = (1/2 pi i) * integral from c + i to c + iT of
             ( (chi'/chi)^2 zeta - 2 (chi'/chi) zeta' + (zeta'/zeta) zeta' ) B ds  -  conj I_1(T)  +  O(T^(1/2) y L^5),     ((3.9), (3.11) to (3.13))
    S_2(T) = M_1(T) + M_2(T) - 2 Re I_2(T) + O(T^(1/2) y L^8),                                                     ((3.15), (3.17), (3.21))

    M_1(T) = (1/2 pi) * integral from 1 to T of (chi'/chi)(1/2 - it)^3 |B zeta(1/2 + it)|^2 dt,                       (3.18)
    M_2(T) = -(3/2 pi) * integral from 1 to T of (chi'/chi)(1/2 - it) |B zeta'(1/2 + it)|^2 dt,                      (3.19)
    I_nu(T) = (1/2 pi i) * integral from c + i to c + iT of chi(1 - s) A_nu(s) B(1 - s) ds,                           (5.1)
    A_1 = (zeta'/zeta) zeta',   A_2 = (zeta'/zeta) zeta'^2 B,                                                       ((5.2), (5.3))
    I_nu(T) = C_nu(T) + O(T^(1/2) y L^7),    C_nu(T) = sum over k <= y of (b(k)/k) * sum over m <= kT/2 pi of a_nu(m) e(-m/k).   ((5.4), (5.5))

(CGG use the letters M_1, M_2 twice: for the integrals (3.18), (3.19) and, as M_nu, for the coefficient sums (5.4);
BHB keep M_nu for the coefficient sums. Here the integrals keep the names M_1(T), M_2(T) and the coefficient sums are
written C_nu(T).)

[D] Each of S_1, S_2, the first integral, I_nu, M_1(T), M_2(T) and C_nu(T) is a sum or an integral up to the height
T, so its value on the window is the difference of its values at T_1 and at T_0. Writing D f = f(T_1) - f(T_0),

    D S_1 = (1/2 pi i) * integral from c + iT_0 to c + iT_1 of ( ... ) B ds  -  conj D C_1  +  O(T^(1/2) y L^7),     (1)
    D S_2 = D M_1(.) + D M_2(.) - 2 Re D C_2  +  O(T^(1/2) y L^8),                                                  (2)

where D M_1(.) and D M_2(.) are the integrals (3.18), (3.19) over [T_0, T_1], and D C_nu is the coefficient sum
over the range kT_0/2 pi < m <= kT_1/2 pi. Nothing is re-proved for this: the errors of the horizontal sides and of
Gonek's lemma are bounds for each height, and a difference of two terms that are O(T^(1/2) y L^A) is of the same
size. In particular Gonek's lemma (CGG Lemma 1, quoted from Gonek 1984, and Lemma 2) needs no two-endpoint
version. The errors of (1) and (2) are o(H) exactly when nu < theta - 1/2.

What does not pass by subtraction is every term whose published error is larger than T^(1/2) y: the first
integral of S_1 (error O(T L) in (3.11)), the integrals M_1(T), M_2(T) (error O(T L^2 (log L)^5) in (3.26), (3.27)),
and the coefficient sums C_nu(T) (error T exp(-C L^(1/2)) + T L^(-A') + (T^(3/4) y^(1/2) + T^(1/2) y) T^eps on p. 516,
or O(y^(1/3) T^(5/6 + eps) + eta^(-1/2) T L^C) in BHB Lemma 2, eta a power of L). These are Sections 2, 3 and 4.

## 2. The first integral of S_1 on the window [D, complete]

On Re s = c the three Dirichlet series zeta B, zeta' B and (zeta'/zeta) zeta' B converge absolutely; write one of
them as the sum of d_n n^(-s). Only zeta B has a term n = 1, and it is b(1) = 1. With (3.10),
(chi'/chi)(c + it) = -log(t/2 pi) + O(1/t), so on the window the integrand is
log^2(t/2 pi) + (terms with n >= 2) + O((L/T) * sum of |d_n| n^(-c)). For n >= 2, an integration by parts gives
that the integral over [T_0, T_1] of g(t) n^(-it) dt, g a power of log(t/2 pi) of degree at most 2, is
O(L^2/log n), and the sum of |d_n| n^(-c)/log n over n >= 2 is O(L^C) (the coefficients are bounded by divisor
functions times powers of log n, and c = 1 + 1/L). Hence

    (1/2 pi i) * integral from c + iT_0 to c + iT_1 of ( ... ) B ds = (1/2 pi) * integral over [T_0, T_1] of log^2(t/2 pi) dt + O(L^C)
                                                                  = (H/2 pi) L^2 (1 + O(H/T)) + O(L^C).              (3)

No hypothesis is used. This is the window form of (3.11); its O(T L) was the lower order part of the same integral.

## 3. The integrals M_1(.) and M_2(.) on the window: input [I1]

For T_0 <= t <= T_1, (chi'/chi)(1/2 - it) = -L + O(H/T) (the window form of (3.25)). So

    D M_1(.) = -(L^3/2 pi)(1 + O(H/(T L))) * integral over [T_0, T_1] of |B zeta(1/2 + it)|^2 dt,
    D M_2(.) =  (3 L/2 pi)(1 + O(H/(T L))) * integral over [T_0, T_1] of |B zeta'(1/2 + it)|^2 dt.

[S] CGG evaluate these through a mean value of Conrey (their (3.22) to (3.24), from Conrey, J. Number Theory 16
(1983)): for F(s) = sum over m of Q(log m/L) m^(-s), Q a real polynomial,

    integral over [T, T + U] of |B F(1/2 + it)|^2 dt
        = U ( Q(0)^2 + nu * double integral over [0, 1]^2 of ( P(u) Q'(v) + (1/nu) P'(u) Q(v) )^2 du dv ) + O(U L^(-1) (log L)^5),   (3.24)

stated for U = T L^(-10) and nu < 1/2 (and valid for nu < 4/7 by Conrey 1989, CGG p. 504).

[I1] The same formula with U replaced by H = T^theta and nu < theta - 1/2, with an error o(H). This is the mollified
mean square of zeta and of zeta' on a short interval; it is the kind of statement this programme uses for its
Levinson detector on windows (mollifier T^nu, nu < theta - 1/2), there at the abscissa 1/2 - R/L. It is expected
to be unconditional (only zeta enters); backlog RH-067 decides.

What the programme has [S, its own manuscript `short-interval-levinson`, theorem 'Mollified moment on a short
window', marked there as derived; unrefereed]: for 0 < nu < theta - 1/2, R > 0, Q a real polynomial with Q(0) = 1,
a smooth weight w equal to 1 on [T, T + H] and supported within H/L of it, and the mollifier at the abscissa
1/2 - R/L, the integral of w |V psi|^2 is c(P, Q, R, nu) times the mass of w plus O(H/L), with
c = 1 + (1/nu) * double integral of ( e^(Rv) Q(v) P'(u) + nu (e^(Rv) Q(v))' P(u) )^2. At R = 0 and with Q(0)^2 in
place of 1 this is the bracket of (3.24). Its proof evaluates the twisted integral of zeta at two shifts,
uniformly for the shifts on annuli of radius of order 1/L, without any hypothesis. So RH-067 is three checks, each
to be written and reviewed: the proof read at R = 0; the constant term Q(0)^2 for a polynomial with Q(0) = 0 (the
form is quadratic in Q); and the passage from the smooth weight to the sharp window, by two weights that
sandwich it (the integrand is nonnegative), which costs O(H/L).

[D] Given [I1], with Q = 1 for zeta and Q(x) = -x for zeta'/L (the integral of P P' is 1/2):

    D M_1(.) = -(H L^3/2 pi) ( 1 + (1/nu) * integral of P'^2 ) + o(H L^3),
    D M_2(.) =  (3 H L^3/2 pi) ( 1/2 + nu * integral of P^2 + (1/(3 nu)) * integral of P'^2 ) + o(H L^3),            (4)

the window forms of (3.26), (3.27); their sum is (H L^3/2 pi)(1/2 + 3 nu * integral of P^2), the first term of
BHB Lemma 1 for S_2 with H in place of T.

## 4. The coefficient sums on the window: inputs [I2] and [I3]

[S] CGG turn the additive characters into multiplicative ones ((5.6) to (5.13)) and obtain

    C_nu(T) = sum over q <= y, sum over primitive psi mod q, of tau(conj psi) * sum over k <= y/q of (b(kq)/(kq))
              * sum over d | kq of delta(q, kq, d, psi) * sum over m <= kqT/(2 pi d) of a_nu(md) psi(m),              (5.14)

with |delta(q, kq, d, psi)| <= (d, k)/phi(kq) for kq squarefree ((5.13)). For q = 1 the inner sum has the main term
R_nu(w, d) = the residue at s = 1 of A_nu(s, 1, d) w^s/s ((6.8)), where A_nu(s, psi, d) is the Dirichlet series of
a_nu(md) psi(m), continued through (6.4) to (6.6).

[I2], under the Riemann hypothesis, and [I3], under the Riemann hypothesis for Dirichlet L-functions: uniformly
for T << w << T^2, d <= y, q <= y and psi primitive modulo q,

    sum over m <= w of a_nu(md) psi(m) = [q = 1] R_nu(w, d) + O( tau_r(d) w^(1/2 + eps) T^eps ).                     (5)

The route is the one BHB name (p. 3): Perron's formula (CGG Lemma 4) and a shift of the line to
Re s = 1/2 + eps, where under the two hypotheses L'/L(s, psi) is O(log^2(q(|t| + 2))), L(s, psi) and L'(s, psi) are
O((q(|t| + 2))^eps), and, for nu = 2, the twist of the mollifier, the sum over k <= y of
mu(k) psi(k) P(log(y/k)/log y) k^(-s), is O((q y (|t| + 2))^eps); the factors that the continuation (6.4) to (6.6)
attaches to the primes dividing d are bounded by a divisor function of d on that line. Writing this out, with the
terms where m and k have a common factor, is backlog RH-062. Only Dirichlet characters occur.

[D] Given (5), the part of (5.14) outside the residues is, by (5.13), |tau(conj psi)| = q^(1/2) and at most phi(q)
characters,

    << T^(1/2 + eps) * sum over q <= y of phi(q) q^(1/2) * sum over k <= y/q of (1/(kq)) * sum over d | kq of ((d, k)/phi(kq)) (kq/d)^(1/2)
    << T^(1/2 + eps) * sum over q <= y of 1 * sum over k of tau(k) k^eps/phi(k)   <<   y T^(1/2 + 2 eps),

for each height. So, with R~_nu(T) = sum over k <= y of (b(k)/k) * sum over d | k of delta(1, k, d, 1) R_nu(kT/(2 pi d), d),

    D C_nu = R~_nu(T_1) - R~_nu(T_0) + O(y T^(1/2 + eps)).                                                           (6)

R_nu(w, d) is w times a polynomial in log w (of degree at most 2 for nu = 1 and 4 for nu = 2: A_2 has a pole of order 5 at s = 1), so R~_nu is a smooth
function of T and R~_nu(T_1) - R~_nu(T_0) = H R~_nu'(xi) for some xi in the window. [S] CGG Section 8 evaluates
R~_nu(T): for nu = 1, (T/2 pi)((1/2) L^2 - L log y * integral of P), and for nu = 2 the bracket of BHB (8) times
T L^3/2 pi, each 'asymptotically', with Lemmas 5 and 6 and Lemma A. The derivative replaces each polynomial p_d by
p_d + p_d', and the second part is of one degree less.

[I2'] The evaluation of CGG Section 8 applied to the polynomials p_d' gives O(T L^(1 + eps)) for nu = 1 and
O(T L^(2 + eps)) for nu = 2 (the same lemmas with one power of the logarithm less). Then
R~_nu'(xi) = R~_nu(T)/T * (1 + O(L^(-1 + eps))), and

    D C_1 = (H L^2/2 pi) ( 1/2 - nu * integral of P ) + o(H L^2) + O(y T^(1/2 + eps)),
    D C_2 = (H L^3/2 pi) ( 1/12 - (nu/2) I + (3 nu/2) * integral of P^2 - (nu^2/2) I^2 - (1/(24 nu)) * integral of P'^2 ) + o(H L^3) + O(y T^(1/2 + eps)),   (7)

I the integral of P: the window forms of BHB (7), (8). This is backlog RH-061. [R] R~_nu is an exact sum of
residues and is smooth; the risk of [I2'] is in the evaluation of its derivative by the lemmas of CGG Section 8
(their Lemmas 5, 6 and A, and the replacement of the sum of Lambda(d) log d), not in oscillating terms, which are
inside the error of (5).

## 5. The reduction

Proposition [D], conditional on [I1], [I2], [I2'] and [I3]. Let 1/2 < theta < 1, 0 < nu < theta - 1/2, y = T^nu and
H = T^theta, with T and T + H at distance >> 1/L from the ordinates. Then, from (1), (3), (7) and from (2), (4), (7),

    D S_1 = (H L^2/2 pi) ( 1/2 + nu * integral of P ) (1 + o(1)),
    D S_2 = (H L^3/2 pi) ( 1/3 + nu I + nu^2 I^2 + (1/(12 nu)) * integral of P'^2 ) (1 + o(1)),

the main terms of CGG Theorem 2 with H in place of T. Under the Riemann hypothesis D S_2 is the sum of
|B(rho) zeta'(rho)|^2 over the zeros of the window, the number of zeros of the window is (H L/2 pi)(1 + o(1)), and
the Cauchy-Schwarz inequality (CGG (2.1)) restricted to the zeros of the window gives a proportion of simple zeros
at least a^2/b; with the optimal P this is 1 - 1/(1 + nu)^3, and letting nu tend to theta - 1/2, target T1.

Arithmetic check of the main terms [D], in units of H L^2/2 pi and H L^3/2 pi. For S_1: (3) contributes 1 and
-conj D C_1 contributes -(1/2 - nu I), total 1/2 + nu I. For S_2: (4) contributes 1/2 + 3 nu * integral of P^2, and
-2 Re D C_2 contributes
-1/6 + nu I - 3 nu * integral of P^2 + nu^2 I^2 + (1/(12 nu)) * integral of P'^2; the sum is
1/3 + nu I + nu^2 I^2 + (1/(12 nu)) * integral of P'^2, which is (2.7).

The endpoint condition. For a general T the two heights are moved by at most 1 to heights at distance >> 1/L from
the ordinates; this changes the window by O(L) zeros, and under the Riemann hypothesis each term B(rho) zeta'(rho)
is O(y^(1/2) T^eps), so D S_1 changes by O(y^(1/2) T^eps) and D S_2 by O(y T^eps), both inside the errors. (To be
written with the bound for zeta'(rho) made explicit; part of RH-063.)

What the hypotheses are used for. The Riemann hypothesis: to write S_2 as a sum of squares (CGG p. 500), for [I2]
and for the endpoint condition. The hypothesis for Dirichlet L-functions: for [I3] only. Sections 1 and 2 are unconditional, and [I1] is expected to be.

## 6. What remains, as units

- RH-067: match [I1] with the programme's short-window mollified mean square (hypotheses, the abscissa 1/2, the two
  polynomials Q), or prove the short-interval form of (3.24) for nu < theta - 1/2.
- RH-062: prove (5), [I2] and [I3], with the dependence on d, q and the terms of common factor.
- RH-061: prove [I2'], the evaluation of the derivative of the main terms.
- RH-063: assembly, the endpoint condition, certified constants, the corollary for distinct zeros.
- RH-065: the primary-source search, before any claim.
Backlog RH-058 (the contour identity on a window and Gonek's lemma with two endpoints) is closed by Section 1:
no two-endpoint version is needed.

## How could this be wrong?

- Section 1 rests on the identities as transcribed. One term of CGG (3.16) could not be read on the page image; it
  is an intermediate display between (3.14) and (3.17), and (3.17) to (3.21), which are used here, were read.
- The two identities must be written on one vertical line; with the abscissa fixed at 1 + 1/L(T_0) nothing changes.
- A difference of two error terms is bounded by their sum; nothing in Section 1 uses cancellation. But it needs both
  heights to satisfy the assumption on the distance to the ordinates, and the bound (3.8) at both.
- (5) is the main unproved statement. The uniformity in d and q, and the twist of the mollifier for nu = 2, are
  the points where a factor larger than T^eps could enter; if the bound were y^a T^(1/2 + eps) with a > 1 in total,
  the range of nu would shrink to (theta - 1/2)/a and the target would be weaker, not void.
- [I2'] is asserted from the shape of the residues, not from a computation.
- [I1]: the programme's theorem is stated at the abscissa of the Levinson detector, for Q(0) = 1 and with a smooth
  weight; the three checks of Section 3 are not written yet, and that theorem is itself unrefereed.
- The arithmetic check of Section 5 uses BHB (7), (8) and CGG (3.26), (3.27) as transcribed; it reproduces (2.7).
