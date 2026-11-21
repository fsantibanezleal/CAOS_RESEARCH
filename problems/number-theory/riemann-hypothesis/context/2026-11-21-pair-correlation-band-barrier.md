# What the pair correlation method gives with the form factor on a band, and why it stops at 0.5502 on short windows for band-limited test functions

Date: 2026-11-21. Status: derivation [D] by the coordinating session, written while establishing what stays open
after the formal proof of 2026-11-20 (dossier `2026-11-21-claimed-proof-review.md`, section 7). Read on 2026-11-21
by a reviewer other than the writer (report `wip/caos-research/rh-f17-notes-review-2026-11-21.md` of the
coordination repository): the formula and every step of its proof confirmed and the numbers recomputed; one
blocker (the first version said more than it proves about 'the method'), two major and four minor findings, all
applied here. The extremal problem solved here is the one Montgomery and Taylor solved for the full band; the
dependence on the band is a short computation and no priority is claimed. What it shows: on windows
(T, T + T^theta], Montgomery's inequality with test functions whose transform is supported in the band cannot give
simple zeros for theta <= 0.550194. Under the Riemann hypothesis the relaxation of section 4 lowers this to about
0.5487 (a probe, not certified). Information on the form factor beyond the band under the hypothesis for Dirichlet
L-functions has not been examined on windows. So this note does not bound what pair correlation can do; it measures
two forms of it.

## 1. The inequality

Let a set of zeros be given (all zeros up to height T, or the zeros with ordinate in a window), N its number
counted with multiplicity, N* the sum of the multiplicities over these zeros counted with multiplicity (so
N* is the sum over distinct zeros of m^2) and N_s the number of simple ones. Since a zero of multiplicity m >= 2
contributes m to N and m^2 >= 2m to N*, one has N* >= N_s + 2 (N - N_s), that is

    N_s >= 2 N - N*.                                                                               (1)

Montgomery's method bounds N* from above. Suppose the form factor F(alpha) of the set is known on a band
|alpha| <= lambda, in the usual shape F(alpha) = |alpha| + (a term that acts as a unit mass at alpha = 0) + o(1).
Under the Riemann hypothesis, for an even function r >= 0 on the line with r(0) = 1 whose Fourier transform r^ is
supported in [-lambda, lambda], summing r over the normalized differences of pairs of zeros and keeping the diagonal
gives

    N* <= ( r^(0) + integral over [-lambda, lambda] of r^(alpha) |alpha| d alpha + o(1) ) N.            (2)

So everything depends on

    J(lambda) = inf over r of ( r^(0) + integral of r^(alpha) |alpha| d alpha ),

the infimum over even r >= 0 with r(0) = 1 and r^ supported in [-lambda, lambda]. Then N_s >= (2 - J(lambda) -
o(1)) N. (Without the hypothesis the same bound holds for the simple zeros on the critical line, with r the square
of a transform, by Lamzouri's inequality as used in Wang, arXiv:2609.07918v2, Proposition 2.1. On a window Wang's
Theorem 2.2 gives the form factor for lambda < theta strictly and smooth test functions, so J(theta) is reached as
a limit.)

## 2. The value of J(lambda)

Proposition. For 0 < lambda <= 1,

    J(lambda) = lambda/2 + (1/sqrt 2) cot(lambda/sqrt 2).                                           (3)

Proof. Put r^(alpha) = (1/lambda) s^(alpha/lambda), so that s^ is supported in [-1, 1], the integral of s^ is 1 and

    r^(0) + integral of r^(alpha)|alpha| d alpha = (1/lambda) ( s^(0) + lambda^2 integral of s^(beta) |beta| d beta ).

A nonnegative integrable function with transform supported in [-1, 1] is |g|^2 with g^ supported in [-1/2, 1/2]
(Krein), so s^ is the convolution of phi with its reflection, phi = g^ supported in [-1/2, 1/2]; one may take phi
real and even. Then the integral of s^ is (integral of phi)^2 = 1, s^(0) is the integral of phi^2, and the
quantity in brackets is

    Q(phi) = integral of phi(x)^2 dx + mu * double integral of phi(x) phi(y) |x - y| dx dy,      mu = lambda^2,

to be minimized subject to the integral of phi being 1. The Euler-Lagrange equation is
phi(x) + mu integral of phi(y) |x - y| dy = c on [-1/2, 1/2]; multiplying by phi and integrating gives Q = c at a
critical point. Differentiating twice, phi'' + 2 mu phi = 0, so phi(x) = a cos(omega x) with omega = sqrt(2 mu) =
lambda sqrt 2 (the even solution), and a = omega/(2 sin(omega/2)) from the normalization. (Conversely
a cos(omega x) does solve the integral equation: for even phi the integral of cos(omega y) |x - y| dy over
[-1/2, 1/2] is -2 cos(omega x)/omega^2 plus a constant, with no linear term.) Evaluating the equation at x = 0,

    c = a + mu * 2a ( sin(omega/2)/(2 omega) + (cos(omega/2) - 1)/omega^2 ) = a ( (omega/2) sin(omega/2) + cos(omega/2) )
      = omega^2/4 + (omega/2) cot(omega/2).

Dividing by lambda and putting omega = lambda sqrt 2 gives (3). The critical point is the minimum: for a variation
psi with integral 0 the second variation is the integral of psi^2 plus mu times the double integral of
psi(x) psi(y) |x - y|, and the operator psi -> - integral of psi(y)|x - y| dy on functions of integral 0 on
[-1/2, 1/2] has largest eigenvalue 2/pi^2 (its eigenfunctions satisfy psi'' = -(2/kappa) psi), so the second
variation is at least (1 - 2 mu/pi^2) times the integral of psi^2, which is positive for mu < pi^2/2, in particular
for mu <= 1. QED.

Checks. (i) lambda = 1: J = 1/2 + 2^(-1/2) cot(2^(-1/2)) = 1.3274992963..., the constant of Montgomery and Taylor,
and 2 - J = 0.6725007036..., the proportion of simple zeros under the Riemann hypothesis by this method.
(ii) A direct numerical minimization of Q on a grid of 400 points gives 1.327497, 1.580923 and 2.000279 at
lambda = 1, 3/4 and 0.5501, against 1.3274993, 1.580925 and 2.0002796 from (3). (iii) With the Fejer kernel of
band lambda, r^(alpha) = (1/lambda) max(1 - |alpha|/lambda, 0), the bracket of (2) is 1/lambda + lambda/3, larger
than (3), and 2 - 1/lambda - lambda/3 is positive exactly for lambda > 3 - sqrt 6 = 0.55051.... Script and output:
data root, `caos-research/riemann-hypothesis/claim-2026-11-20/coordinator/barrier_numbers.py` and `.log`.

## 3. The barrier

Put c(lambda) = 2 - J(lambda) = 2 - lambda/2 - 2^(-1/2) cot(lambda/sqrt 2). It increases with lambda, and

    c(lambda) > 0   exactly for   lambda > lambda_0 = 0.5501939647441547...,
    c(3/4) = 0.4190750..., c(0.552) = 0.00535..., c(0.55) = -0.00058..., c(0.534) = -0.04980...

These are the numbers of Wang's short-interval theorem (arXiv:2609.07918v2: a positive proportion of simple
critical zeros in (T, T + T^theta] for theta > 0.5501..., more than 41.9 percent at theta = 3/4), which is the
unconditional form of this method with band lambda = theta. The source preflight of RH-F17 read his text
(page 2, before Theorem 1.1): 'c(theta) = 2 - theta/2 - (1/sqrt 2) cot(theta/sqrt 2)', strictly increasing, with a
unique zero theta_0 = 0.5501...; his C_theta of Theorem 1.2 is J(theta) of (3). The two formulas are identical
term by term, and the preflight recomputed c(1), c(3/4), c(0.552), c(0.534) and the root. (The formula for c(theta)
written in the report `rh-literature-refresh` of 2026-11-21 was wrong and is superseded.)

Why the band is theta on a window of length H = T^theta. The form factor on the window is the mean square over the
window of a Dirichlet polynomial in the primes of length T^alpha; the mean value theorem on an interval of length H
isolates the diagonal for lengths below H, that is for alpha < theta. Beyond that the off-diagonal terms are
correlations of primes that the Riemann hypothesis for zeta does not supply; under the hypothesis for Dirichlet
L-functions a lower bound beyond the band is known for the form factor of all the zeros up to T (Goldston, Gonek,
Ozluk and Snyder, as used by Chirre, Goncalves and de Laat, arXiv:1810.08843, in the proof of their Lemma 8; the
primary was not opened), and its window form is not known. So on these windows the band of the form factor is
theta whether or not the Riemann hypothesis holds: the hypothesis removes the words 'on the critical line' from
the conclusion and moves lambda_0 only through the sign condition of section 4. (This paragraph is the programme's
reading of the method. What is proved:
Wang's Theorem 2.2 gives the form factor on the window for test functions supported in [-lambda, lambda] with
lambda < theta, without any hypothesis, with error O(H + T^lambda L^2); the preflight found no statement with a
larger band on a window under the hypothesis, and could not open Goldston and Montgomery (1987) or Goldston, Gonek
and Montgomery (2001), which concern the form factor of all the zeros up to T.)

Consequences for the programme.
- Below theta = 0.5502 a positive proportion of simple zeros in (T, T + T^theta] needs an input other than pair
  correlation with test functions supported in the band (and, by the probe of section 4, below about 0.5487 an
  input other than its relaxation by the sign condition). The programme's unconditional theorem (theta >= 0.534) has one: the Levinson detector on the
  window, used with the pair correlation bound through the Hilbert-parity inequality. At theta = 0.534 the pair
  correlation term alone is negative (c = -0.0498), which measures what the detector contributes.
- Under the Riemann hypothesis and the hypothesis for Dirichlet L-functions the natural input is the mollified
  discrete moments of zeta'(rho) over the zeros of
  the window (Conrey, Ghosh and Gonek; Bui and Heath-Brown), which give a positive proportion for a mollifier of
  any positive length; with a mollifier T^nu, nu < theta - 1/2, they would reach every theta > 1/2, with the
  proportion 1 - 8/(2 theta + 1)^3, larger than c(theta) on the whole range (note
  `2026-11-21-short-window-discrete-moments-target.md`: a target under the Riemann hypothesis and the hypothesis
  for Dirichlet L-functions, with its proof obligations).

## 4. With the sign of the form factor outside the band (a preflight probe, not a certified statement)

The form factor of the zeros of a window is nonnegative for every alpha without any hypothesis (Wang, Lemma 2.3:
it is the mean square of a Dirichlet polynomial). What the Riemann hypothesis adds is that inequality (2) holds for
every r >= 0 on the line, because every difference of ordinates is real; then the part of the integral of F r^
outside the band can be dropped when r^(alpha) <= 0 for |alpha| > lambda, and the test function need not have its
transform supported in the band. Whether this gain survives without the hypothesis, through Lamzouri's class of
kernels, is open. This is the linear programme of Cohn and Elkies type that Chirre,
Goncalves and de Laat solved for the full band (arXiv:1810.08843: 1.3208 in place of 1.3275). A probe with 25
Laguerre-Gaussian basis functions and constraints on grids (script and log under the data root,
`caos-research/riemann-hypothesis/claim-2026-11-20/coordinator/lp_band_probe.py`) gives:

| band lambda | bound with support in the band, (3) | bound with the sign condition (probe) | simple zeros, (3) | simple zeros, probe |
|---|---|---|---|---|
| 1 | 1.327499 | 1.3209 | 0.672501 | 0.6791 |
| 0.75 | 1.580925 | 1.5753 | 0.419075 | 0.4247 |
| 0.6 | 1.865446 | 1.8607 | 0.134554 | 0.1393 |
| 0.5502 | 1.999982 | 1.9956 | 0.000018 | 0.0044 |
| 0.534 | 2.049802 | 2.0455 | negative | negative |

(Probe values to four decimals: the reviewer re-solved the programme with constraints on ten times as many points
out to 30 and the fifth decimal moved; the optimal functions of the first probe violated the constraints by up to
6e-6 between grid points.)

The value at the full band agrees with the published 1.3208 to the precision of the probe. The zero of the
proportion moves from 0.550194 to about 0.5487 (the reviewer's finer run: +0.0024 at 0.5495, +0.0009 at 0.549,
-0.0021 at 0.548). So the sign condition gains about 0.005 in the proportion and 0.0015 in the onset. The probe
solves the primal programme: it exhibits test functions, so 0.5487 is an upper estimate of the onset of this
relaxation; that the relaxation gives nothing below it would need a dual certificate, and nothing here bounds what
other pair correlation inputs could give. These figures are estimates (constraints on grids, a finite basis); a
statement would need a verified test function, and it is not worth a declared experiment by itself. It enters the
tool spectrum of the plan as a small, cheap gain.

## How could this be wrong?

- (2) is used in the shape stated; the precise form of the form factor on a band (the term at alpha = 0, uniformity)
  is taken from the literature and re-read in the source preflight. The proposition itself is self-contained.
- The reduction to phi real and even loses nothing: for phi = u + iv, Q(phi) = Q(u) + Q(v); the functional is
  invariant under reflection and convex on the constraint set for mu < pi^2/2, by the second variation.
- The identification of lambda_0 with Wang's onset rests on his formula, read by the source preflight on the page
  image of his paper.
- 'The method' in this note means two precise forms (support in the band; the sign condition under the hypothesis).
  A lower bound for the form factor beyond the band, of the kind known for all the zeros under the hypothesis for
  Dirichlet L-functions, would change the numbers; no window form of it was looked for.
- For lambda > 1 the form factor is not |alpha| and nothing here applies.
