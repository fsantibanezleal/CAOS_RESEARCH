# Input [I1] of the window reduction: the mollified mean square of zeta and zeta' on a window, from the programme's short-window theorem

Date: 2026-11-22. Status: three checks [D] by the coordinating session for focus RH-F17 (backlog RH-067), on the
programme's manuscript `manuscripts/riemann-hypothesis/short-interval-levinson/main.tex` (version 0.02, cited as SIL
with its line numbers) and on the reduction note `2026-11-21-window-moments-by-subtraction.md` (cited as WMS). Marks:
[S] as printed in a source, with its place; [D] derived here; [C] checked by symbolic computation (script
`verify_i1.py` and its log `verify_i1.log` under the data root, `caos-research/riemann-hypothesis/rh-067/`; SHA-256
`7d98a61f...84eb` and `0cc810ca...2f72`). Read on 2026-11-22 by a reviewer other than the writer (report
`wip/caos-research/rh-067-window-mean-square-review-2026-11-22.md` of the coordination repository): correct after
fixes, one major and three minor findings (J1 to J4), applied here; the reviewer re-ran `verify_i1.py` to an identical
log and made an independent symbolic check (P of degree 5, Q of degree 4). It proves nothing about target T1 beyond
input [I1]; T1 stays a target.

Notation as in WMS: B(s) = sum over k <= y of b(k) k^(-s), b(k) = mu(k) P(log(y/k)/log y), y = T^nu, P a real
polynomial with P(0) = 0 and P(1) = 1; H = T^theta with 1/2 < theta < 1 fixed and 0 < nu < theta - 1/2 fixed;
L = log T (SIL) and L_C = log(T/2 pi) (CGG, WMS).

## 0. What is needed

[S, WMS Section 3] [I1]: for F(s) = sum over m of Q(log m/L_C) m^(-s), with Q = 1 (F = zeta) and Q(x) = -x
(F = zeta'/L_C),

    integral over [T, T + H] of |B F(1/2 + it)|^2 dt = H ( Q(0)^2 + nu * double integral over [0, 1]^2 of ( P(u) Q'(v) + (1/nu) P'(u) Q(v) )^2 du dv ) + o(H),

the short-window form of Conrey's mean value (CGG (3.24), proved there for windows of length T L^(-10)).

## 1. What the programme's theorem says

[S, SIL lines 158-176, Theorem 'Mollified moment on a short window', marked there as derived] Let 0 < nu < theta - 1/2,
R > 0, P with P(0) = 0, P(1) = 1, Q a real polynomial with Q(0) = 1, sigma_0 = 1/2 - R/L, Delta = H/L,

    V(s) = Q(-(1/L) d/ds) zeta(s),      psi(s) = sum over h <= y of mu(h) h^(-(s + 1/2 - sigma_0)) P(log(y/h)/log y),

and w smooth with 0 <= w <= 1, w = 1 on [T, T + H], support in [T - Delta, T + H + Delta], w^(j) << Delta^(-j). Then

    integral of w(t) |V psi(sigma_0 + it)|^2 dt = c(P, Q, R, nu) * (integral of w) + O(H/L),
    c(P, Q, R, nu) = 1 + (1/nu) * double integral over [0, 1]^2 of ( w_R(v) P'(u) + nu w_R'(v) P(u) )^2 du dv,  w_R(v) = e^(Rv) Q(v).

[S, SIL lines 339-348, Remark] The hypothesis nu < theta - 1/2 is used only in the twisted-integral lemma, nu < 1/2
only in the diagonal lemma, theta < 1 for the support of w and the bound of rho; "the normalization Q(0) = 1 enters
only through the constant term", and for every real polynomial Q the constant is Q(0)^2 + (1/nu) times the double
integral.

Three things separate this from [I1]: the abscissa (sigma_0 = 1/2 - R/L with R > 0, against 1/2), the polynomial
Q(x) = -x (Q(0) = 0, against Q(0) = 1), and the weight (smooth, against the indicator of [T, T + H]). Each is a check.

## 2. Check (a): the abscissa 1/2, that is R = 0 [D]

The mollifier. In psi(sigma_0 + it) the exponent is -(sigma_0 + it + 1/2 - sigma_0) = -(1/2 + it), so
psi(sigma_0 + it) = B(1/2 + it) for every R: the mollifier of the theorem is CGG's B on the critical line,
whatever the abscissa of V.

Where R enters the proof. The proof (SIL lines 205-337) establishes, for

    I(alpha, beta) = integral of w(t) zeta(1/2 + alpha + it) zeta(1/2 + beta - it) |psi(sigma_0 + it)|^2 dt,

the formula I(alpha, beta) = c(alpha, beta) (integral of w) + O(H/L) first on the annuli alpha, beta of order 1/L
with |alpha + beta| >> 1/L (the twisted-integral lemma, SIL 236-266, and the diagonal lemma, 288-312; neither
mentions R), then for alpha, beta << 1/L by the maximum modulus principle (SIL 320-322), and finally applies the
operator Q(-(1/L) d/d alpha) Q(-(1/L) d/d beta) at alpha = beta = -R/L (SIL 323-336). R occurs only as that point of
evaluation. The value R > 0 is used in the theorem on sign changes (SIL 178-185, kappa = 1 - R^(-1) log c), not in
the moment; the Remark's list of uses does not contain it.

The step at R = 0, written out. Put E(alpha, beta) = I(alpha, beta) - c(alpha, beta) (integral of w). The
function c is entire: with a = alpha L, b = beta L,

    c = 1 + (1/nu) * integral over [0, 1] of e^(-v(a + b)) dv * integral over [0, 1] of (P' - b nu P)(P' - a nu P) du    [C, check 1]

(the removable singularity of c_1 at alpha + beta = 0 cancels between the two terms), and I is holomorphic in
(alpha, beta) for |alpha|, |beta| <= 3/L because zeta is holomorphic away from 1 and t >= T/2 on the support of w.
On the torus |alpha| = 3/L, |beta| = 1/L both variables are of order 1/L and |alpha + beta| >= 2/L, and Young's
Lemma 6 holds uniformly on any fixed annuli (the region SIL uses), so the annulus estimate gives |E| <= C H/L there
(the swapped torus |alpha| = 1/L, |beta| = 3/L is used in the same way where the roles of the variables are
exchanged); the maximum modulus principle applied in one variable and then in the other gives
|E| <= C H/L on the closed polydisc |alpha| <= 3/L, |beta| <= 1/L. For R = 0 the operator acts at alpha = beta = 0.
By Cauchy's formula on the circles |alpha| = |beta| = 1/(2L), which lie in that polydisc,
d^j/d alpha^j d^k/d beta^k E(0, 0) << j! k! (2L)^(j + k) H/L, and the operator multiplies the term (j, k) by
L^(-j - k) times a coefficient of Q; so the error after the operator is O_Q(H/L). The same argument, with the polydisc
enlarged to contain -R/L, is what SIL 329-330 states for R > 0.

So the theorem holds at R = 0 with V evaluated at 1/2 + it and psi(sigma_0 + it) = B(1/2 + it).

## 3. Check (b): the polynomial Q(x) = -x, that is Q(0) = 0 [D, C]

The operator identity. For a real polynomial Q, Q(-(1/L) d/d alpha) zeta(1/2 + alpha + it) = V(1/2 + alpha + it) term
by term, and Q(-(1/L) d/d beta) zeta(1/2 + beta - it) = V(1/2 + beta - it), the complex conjugate of
V(1/2 + beta + it) for real beta. So at alpha = beta = -R/L the operator turns the integrand of I into
w |V(sigma_0 + it)|^2 |psi(sigma_0 + it)|^2 (SIL 323-327, Young's (3.4)). The identity is linear in Q in each factor
and uses no value of Q.

The main term. On the entire form of c the operator acts as follows. The constant 1 goes to Q(0)^2. For the second
term, Q(-d/da)[e^(-va) f(a)] = e^(-va) Q(v - d/da) f(a); with f(a) = P'(u) - a nu P(u), linear in a,
Q(v - d/da) f = Q(v) f(a) + nu Q'(v) P(u), which at a = -R equals Q(v)(P' + R nu P) + nu Q'(v) P. Multiplied by e^(vR)
this is w_R(v) P'(u) + nu w_R'(v) P(u), and the same holds in b. Hence, for every real polynomial Q,

    Q(-d/da) Q(-d/db) c |_(a = b = -R) = Q(0)^2 + (1/nu) * double integral of ( w_R P' + nu w_R' P )^2,

the Remark's formula (SIL 345-346). [C, checks 2 and 2'] the identity holds for P of degree 3 and Q of degree 3 with
free coefficients, Q(0) among them, for R different from 0 and for R = 0 (substituted before the integration).

At R = 0, w_0 = Q, and the constant is Q(0)^2 + (1/nu) * double integral of (Q(v) P'(u) + nu Q'(v) P(u))^2, which is
CGG's bracket Q(0)^2 + nu * double integral of (P Q' + P' Q/nu)^2 [C, check 3]. The two values WMS uses [C, checks 4a,
4b], with the integral of P P' equal to 1/2:

    Q = 1:       1 + (1/nu) * integral of P'^2,
    Q(x) = -x:   1/2 + nu * integral of P^2 + (1/(3 nu)) * integral of P'^2.

The error is the one of check (a): the Cauchy estimate uses no value of Q.

The normalization of the logarithm. SIL writes Q(-(1/L) d/ds) with L = log T, CGG write Q(log m/L_C) with
L_C = log(T/2 pi). For a general real Q, CGG's F is Q_lambda(-(1/L) d/ds) zeta with Q_lambda(x) = Q(lambda x) and
lambda = L/L_C = 1 + O(1/L); the coefficients of Q_lambda differ from those of Q by O(1/L), the constant is a
polynomial in them, and the error of the theorem is uniform for coefficients in a compact set (the Cauchy estimate
of check (a) uses only their size), so the main term changes by O(1/L) relative to its size (correction J2). For
Q = 1 the two coincide. For Q(x) = -x, CGG's F is zeta'/L_C = lambda V with
lambda = L/L_C = 1 + O(1/L), so |B F|^2 = lambda^2 |B V|^2 and the main term changes by a factor 1 + O(1/L), inside
the error O(H/L). The mollifier is the same in both (y = T^nu, b(k) = mu(k) P(log(y/k)/log y)).

## 4. Check (c): the sharp window [D]

Let f(t) = |B F(1/2 + it)|^2 >= 0 and c the constant of check (b) at R = 0.

Upper bound. Take w_+ smooth, 0 <= w_+ <= 1, w_+ = 1 on [T, T + H], support in [T - Delta, T + H + Delta],
w_+^(j) << Delta^(-j). Then the integral of f over [T, T + H] is at most the integral of w_+ f, which is
c (integral of w_+) + O(H/L) = c H + O(H/L), since H <= integral of w_+ <= H + 2 Delta = H (1 + O(1/L)).

Lower bound. Take w_- smooth, 0 <= w_- <= 1, w_- = 1 on [T + Delta/2, T + H - Delta/2], support in [T, T + H],
w_-^(j) << Delta^(-j). SIL's proof (lines 205-337) never uses "w = 1 on [T, T + H]": the weight enters only through
its support (of length at most 2H, inside [T - Delta, T + H + Delta]), the bounds w^(j) << Delta^(-j) (lines 249-250),
and the integrals of w and of w g (lines 270-272, 302-305), exactly as in Young's conditions on the weight. So the
proof runs unchanged for w_- at the same T, H, y = T^nu and L, and gives c (integral of w_-) + O(H/L) [D, read on
SIL; correction J1 of the review: an earlier version applied the theorem at the height T + Delta/2, where the
mollifier length and the logarithm of the theorem are not those of the sandwich]. Then the integral of f over
[T, T + H] is at least the integral of w_- f, which is c (integral of w_-) + O(H/L) = c H + O(H/L), since
integral of w_- >= H - Delta.

So, for fixed theta in (1/2, 1), 0 < nu < theta - 1/2, P with P(0) = 0, P(1) = 1, and every real polynomial Q,

    integral over [T, T + H] of |B F(1/2 + it)|^2 dt = H ( Q(0)^2 + nu * double integral of ( P Q' + P' Q/nu )^2 ) + O(H/L).   (I1)

## 5. What this gives the reduction

Proposition [D], conditional on the correctness of SIL's theorem on the mollified moment (derived in the programme's
manuscript, unrefereed). Input [I1] holds, unconditionally (only the zeta function enters), with the error O(H/L) in
place of o(H). With WMS Section 3, for 1/2 < theta < 1,

    D M_1(.) = -(H L^3/2 pi) ( 1 + (1/nu) * integral of P'^2 ) + O(H L^2),
    D M_2(.) =  (3 H L^3/2 pi) ( 1/2 + nu * integral of P^2 + (1/(3 nu)) * integral of P'^2 ) + O(H L^2),

the window forms (4) of WMS with an explicit error (L there is L_C; the factor (chi'/chi)(1/2 - it) = -L_C + O(H/T)
of WMS Section 3 contributes O(H^2 L^2/T), smaller). At theta = 1 the reduction is not needed: CGG and BHB apply
directly.

What stays open for target T1 after this note: [I2] and [I3] (bound (5) of WMS, backlog RH-062, the main unproved
statement), [I2'] (RH-061), the assembly with the endpoint condition (RH-063), and the primary-source search
(RH-065). Of the four inputs of the reduction, [I1] is the first that is no longer a bare input: it rests on a
theorem of the programme, read here at the abscissa 1/2, for Q(0) = 0 and on a sharp window.

## How could this be wrong?

- SIL's theorem is the programme's own and is unrefereed; its proof uses steps of Young's Theorem 2 verbatim, and a
  defect there carries over here. This note does not re-prove those steps.
- The maximum modulus step needs the annulus estimate on the whole torus |alpha| = 3/L, |beta| = 1/L with constants
  uniform there; SIL states the estimate on the annuli of Young's Lemma 6 with that uniformity.
- The symbolic checks cover P and Q of degree at most 3; the hand computation of check (b) covers every degree.
- CGG (3.24) is compared through the transcription of 2026-11-21 (`wip/caos-research/rh-f17-contour-formulas-2026-11-21.md`
  of the coordination repository), not re-read on the paper for this note (J4).
- The passage from log T to log(T/2 pi) for a general Q uses the uniformity of the error in the coefficients of Q
  (J2); for the two Q of the reduction it is explicit.
- The error O(H/L) depends on P and Q; for target T1 only fixed P (the optimal quadratic of the target note) and the
  two fixed Q occur.
