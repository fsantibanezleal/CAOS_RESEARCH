# Simple zeros in short intervals under the Riemann hypothesis: the target of focus RH-F17, its proportion and its proof obligations

Date: 2026-11-21. Status: a target with its error budget, written by the coordinating session from the source
preflight of the same day (`wip/caos-research/rh-f17-source-preflight-2026-11-21.md` of the coordination
repository; its unverified rows are not used). Marks: [S] read on a primary source by the preflight, with the place;
[D] derived here; [R] a reading of this programme, not proved. Nothing in this note is a theorem of the programme.
Section 2 is a short computation on formulas quoted from two papers; Sections 3 and 4 say what would have to be
proved. Read on 2026-11-21 by a reviewer other than the writer (report
`wip/caos-research/rh-f17-notes-review-2026-11-21.md` of the coordination repository): the target is stated as a
target throughout, the proposition of Section 2 is correct and appears in neither paper, the sizes and places of
the error budget are right; one blocker shared with the barrier note (the sentence on pair correlation said more
than is proved), three major findings (the budget omitted the mean values of the mollified zeta and zeta' on the
critical line; one sentence claimed every error was a power of T; one mark was wrong) and eight minor, applied
here. The term-by-term treatment now lives in `2026-11-21-window-moments-by-subtraction.md`.

## 1. The target

Notation: N(T, H) is the number of zeros of zeta with ordinate in (T, T + H], counted with multiplicity, N_s(T, H)
the number of simple ones, L = log(T/2 pi).

Target T1 [R]. Assume the Riemann hypothesis and the Riemann hypothesis for Dirichlet L-functions. Then for every
fixed theta with 1/2 < theta <= 1,

    liminf as T grows of N_s(T, T^theta)/N(T, T^theta) >= 1 - 8/(2 theta + 1)^3.                         (T1)

The right side is 19/27 at theta = 1 (the constant of Conrey, Ghosh and Gonek, and of Bui and Heath-Brown, for all
the zeros up to T), 0.4880 at theta = 3/4, 0.2487 at 0.6, 0.1362 at 0.55, 0.0954 at 0.534, and about
3 (theta - 1/2) near 1/2. It is positive for every theta > 1/2.

Why it matters. No theorem giving a positive proportion of simple zeros in (T, T + T^theta] for theta at or below
0.5501, with or without the hypothesis, was found in the searches listed in the preflight (its questions (a) to
(c); the review databases and Steuding's paper of 2002 could not be opened), other than this programme's
unconditional theorem for theta >= 0.534. Pair correlation with test functions supported in the band cannot give
one at or below 0.5502; with the sign condition under the hypothesis, not below about 0.5487 by an uncertified
probe; inputs beyond the band under the hypothesis for Dirichlet L-functions are unexamined
(`2026-11-21-pair-correlation-band-barrier.md`). The two hypotheses of T1 are exactly the two statements of the
formal proof released on 2026-11-20; T1 is a conditional statement of the usual kind whatever the fate of that
proof.

## 2. The proportion as a function of the length of the mollifier [D]

[S] Conrey, Ghosh and Gonek (Proc. London Math. Soc. (3) 76 (1998), Theorem 2 with (2.5) to (2.7)) and Bui and
Heath-Brown (arXiv:1302.5018, Lemma 1 and page 4): with the mollifier B(s) = sum over k <= y of
mu(k) P(log(y/k)/log y) k^(-s), y = T^nu, 0 < nu < 1/2, P a real polynomial with P(0) = 0 and P(1) = 1,

    S1 = sum over 0 < gamma <= T of B(rho) zeta'(rho)            ~ (T L^2/2 pi) a,
    S2 = sum over 0 < gamma <= T of |B(rho) zeta'(rho)|^2        ~ (T L^3/2 pi) b      (the form of S2 uses the hypothesis),

    a = 1/2 + nu I,        b = 1/3 + nu I + nu^2 I^2 + E/(12 nu),        I = integral of P,   E = integral of P'^2,

and, by the Cauchy-Schwarz inequality over the simple zeros, N_s >= |S1|^2/S2, so the proportion of simple zeros is
at least a^2/b.

Proposition [D]. For every nu > 0 the maximum of a^2/b over the admissible P is

    kappa(nu) = 1 - 1/(1 + nu)^3,

attained at P(x) = -nu x^2 + (1 + nu) x.

Proof. Since a^2 = 1/4 + nu I + nu^2 I^2,

    b = a^2 + r,        r = 1/12 + E/(12 nu),

so a^2/b = 1/(1 + r/a^2), and the task is to maximize a^2/r. For a given value of I the least E under P(0) = 0,
P(1) = 1 is attained by the quadratic with that integral (the Euler-Lagrange equation is P'' constant), so it is
enough to take P(x) = c x^2 + (1 - c) x, for which I = 1/2 - c/6 and E = 1 + c^2/3. Then
a = (3 + 3 nu - nu c)/6 and r = (3 (1 + nu) + c^2)/(36 nu), and

    a^2/r = nu (3 + 3 nu - nu c)^2/(3 (1 + nu) + c^2).

The derivative in c vanishes at c = -nu (from -nu (3 (1 + nu) + c^2) = c (3 + 3 nu - nu c)) and at c = 3 (1 + nu)/nu,
where a = 0 and the expression is 0, its minimum; c = -nu is the maximum (the expression tends to nu^3 at both ends,
below its value there). At c = -nu,
a^2/r = nu (3 + 3 nu + nu^2) = (1 + nu)^3 - 1. Hence a^2/b = 1 - (1 + nu)^(-3). QED.

Checks. kappa(1/2) = 19/27, with a = 19/24 and b = 57/64, the values of the two papers. Exact values:
kappa(2/5) = 218/343, kappa(1/4) = 61/125, kappa(1/5) = 91/216, kappa(1/10) = 331/1331, kappa(1/20) = 1261/9261,
kappa(1/100) = 30301/1030301. A numerical maximization over c agrees to machine precision at seven values of nu.
Script and log: data root, `caos-research/riemann-hypothesis/claim-2026-11-20/coordinator/kappa_table.py` and
`.log`. The papers state the optimal P and the value at nu = 1/2; the closed form for general nu is a line of
algebra on their formulas, and no priority is claimed (a search for it in print is backlog RH-065).

Reading the formula. If a mollifier of length T^nu is admissible on a window of length T^theta exactly for
nu < theta - 1/2 (Section 3), the proportion is kappa(theta - 1/2) = 1 - 8/(2 theta + 1)^3, which is (T1).

Against pair correlation on the same window (band theta, `2026-11-21-pair-correlation-band-barrier.md`):

| theta | 1 - 8/(2 theta + 1)^3 | pair correlation, 2 - theta/2 - cot(theta/sqrt 2)/sqrt 2 |
|---|---|---|
| 0.51 | 0.0294 | negative |
| 0.534 | 0.0954 | negative |
| 0.55 | 0.1362 | negative |
| 0.6 | 0.2487 | 0.1346 |
| 0.7 | 0.4213 | 0.3400 |
| 0.75 | 0.4880 | 0.4191 |
| 0.9 | 0.6356 | 0.5931 |
| 1 | 0.7037 | 0.6725 |

The first column is larger on the whole range (least difference 0.0312, at theta = 1). The second column is a
theorem without any hypothesis (Wang, arXiv:2609.07918v2) and counts simple zeros on the line; the first is a
target under two hypotheses.

## 3. Why nu < theta - 1/2, term by term [R]

The window sums are differences of the sums up to T + H and up to T, H = T^theta. The main terms of S1 and S2 are
smooth in T and give (H L^2/2 pi) a and (H L^3/2 pi) b. Each error term of the argument for 0 < gamma <= T has to
be shown to be o(H L^2) for a window. Where each stands:

| Step of the argument for 0 < gamma <= T | Size as proved, with the place [S] | On a window [R] |
|---|---|---|
| Horizontal sides of the contour | O(T^(1/2) y L^5) and O(T^(1/2) y L^8): Conrey, Ghosh and Gonek (3.9), (3.15); O(y T^(1/2 + eps)) in Bui and Heath-Brown, Lemma 1 | the same at each of the two heights: needs y T^(1/2 + eps) = o(H), that is nu < theta - 1/2 |
| Gonek's lemma turning the integral of chi(1 - s) times a Dirichlet series into sums of its coefficients against additive characters e(-m/k), m <= kT/2 pi | error O(T^(1/2) y log^A T): Conrey, Ghosh and Gonek, Lemma 1 (Gonek's lemma) and Lemma 2, applied in (5.4), (5.5) | the same at each endpoint; the sums over m become sums over kT/2 pi < m <= k(T + H)/2 pi |
| Principal characters (the main terms) | main terms with remainders O(T L) and O(T L^2): Bui and Heath-Brown (7), (8) | sums of coefficients such as Lambda * log over an interval (X, X + Y] with Y/X = T^(theta - 1): under the Riemann hypothesis each has error O(X^(1/2 + eps)), total about y^(1/2) T^(1/2 + eps); the remainders O(T L) have to be shown smooth in T, so that their increments are O(H L) |
| Characters of conductor up to a power of L | Siegel's theorem: Conrey, Ghosh and Gonek, Section 6; Bui and Heath-Brown (9) | Siegel's theorem is not needed under the hypothesis for Dirichlet L-functions; these characters are handled as the next row |
| Characters of conductor between that power and y | sixth moment under the generalized Lindelof hypothesis (Conrey, Ghosh and Gonek (7.28)); or the bound O(y^(1/3) T^(5/6 + eps) + eta^(-1/2) T L^C), eta a power of L, from the generalized Vaughan identity and the hybrid large sieve (Bui and Heath-Brown, Lemma 2); the first term is larger than a window main term for theta < 5/6 and the second for every theta < 1 | under the hypothesis for Dirichlet L-functions, Perron's formula and a shift to Re s = 1/2 + eps bound each twisted sum up to X by O(X^(1/2 + eps)) whatever the length of the range (Bui and Heath-Brown name this route, page 3); with Gauss sums of size q^(1/2) and the sum over k <= y with weights 1/k the total is O(y T^(1/2 + eps)): again nu < theta - 1/2 |
| The right side of the contour for S1 | T L^2/2 pi + O(T L): Conrey, Ghosh and Gonek (3.11) | computed on the window without hypothesis: (H/2 pi) L^2 (1 + O(H/T)) + O(L^C) (reduction note, Section 2) |
| The mean values of the mollified zeta and zeta' on the critical line, with the weights (chi'/chi)^3 and chi'/chi (two of the three integrals of the left side of S2, moved to the line 1/2) | Conrey's mean value on intervals of length T L^(-10), relative error O(L^(-1) (log L)^5), for nu < 1/2: Conrey, Ghosh and Gonek (3.18), (3.19), (3.24) to (3.27); the first term of S2 in Bui and Heath-Brown, Lemma 1 | the same mean value on an interval of length T^theta, expected for nu < theta - 1/2 and unconditional; to be matched with the mollified mean square the programme uses on windows, which has to cover zeta' and these weights (backlog RH-067) |

So under the two hypotheses the error terms that are powers of T are O(y T^(1/2 + eps)), by the known proofs read at
two heights, and the admissible length is nu < theta - 1/2, the range in which this programme already has the
mollified second moment of zeta on short windows. The other errors of the two papers (O(T L), O(T L^2),
O(T L^(2 + eps)), and the relative error of Conrey's mean value) are not powers of T: each has to be shown to have
increments o(H L^2) or o(H L^3) over the window, with the mollifier fixed (the main terms written as functions of T
at a fixed y, and the window sums as differences at T + H and at T with the same mollifier). Under the Riemann
hypothesis alone the character row is the one without a known short-window form [R, the reading of the preflight]:
the bound of Bui and Heath-Brown for the large conductors (their page 9: y T^(1/2 + 4 eps) + y^(1/2) T^(3/4 + 3 eps) +
y^(1/3) T^(5/6 + 3 eps) + eta^(-1/2) T L^109 [S, as read by the reviewer]) is a bound for the long sum and does not
shrink with the range of m [R].

The reduction note `2026-11-21-window-moments-by-subtraction.md` carries this out: the identities of Conrey, Ghosh
and Gonek are additive in the height, so every term of size T^(1/2) y passes by subtraction, and T1 is reduced to
three named inputs.

For S2 the Dirichlet series whose coefficients are summed contains the mollifier itself; its twist by a character
is O(y^eps (q T)^eps) on Re s = 1/2 + eps under the hypothesis for Dirichlet L-functions (partial sums of
mu(k) psi(k) k^(-s)), so the same bound holds [R].

## 4. Proof obligations, in the order of work, and where the route can fail

1. The contour identity for a window and the horizontal sides at two heights, with the mollifier bounded on the
   sides (Conrey, Ghosh and Gonek, Sections 2 and 3, re-derived with both endpoints). Fails if a side at height
   T + H costs more than y T^(1/2 + eps); none is expected.
2. Gonek's lemma with two endpoints and its error uniform in k <= y. (Not needed: the identities are additive in
   the height; reduction note, Section 1. The move of two integrals to the line 1/2 at both heights is of the same
   kind.)
2b. The mean values of the mollified zeta and zeta' on the window (Conrey, Ghosh and Gonek (3.16) to (3.27)) and the
   right side of the contour for S1 as an increment.
3. The principal-character terms of S1 and S2 as increments: the short sums of the coefficients under the Riemann
   hypothesis, and the lower order terms as differentiable functions of T at a fixed mollifier, including the
   approximations of Conrey, Ghosh and Gonek's Section 8 (the replacement of the sum of Lambda(d) log d by the sum of
   log^2 p, their Lemmas 5, 6 and A) and the errors O(T L), O(T L^(2 + eps)) of Bui and Heath-Brown's Lemma 1. This
   is the step most likely to hide a term that is not smooth; a failure here is written as an obstruction.
4. The non-principal characters under the hypothesis for Dirichlet L-functions, including the terms with
   gcd(m, k) > 1, where the coefficients are not multiplicative (both papers treat them; the bounds have to be
   re-derived pointwise).
5. The endpoint condition: the papers take T at a distance from the ordinates; a general T costs O(L) zeros, each
   contributing at most y^(1/2) T^eps to S1 and y T^eps to S2, still o(H) for nu < theta - 1/2.
6. Assembly: (T1) with every epsilon made explicit; the corollary for distinct zeros from Montgomery's inequality
   2 N_s <= N* - 5 N + 6 N_d, which both papers use, and the bound N* <= J(theta) N on the band theta: distinct zeros
   at least (5 + 2 s - J(theta))/6 with s the proportion of T1. At theta = 0.55 this is 0.5453 against the
   unconditional 0.4999 of Wang's Theorem 1.2; at theta = 1 it is 0.84665, the constant of Bui and Heath-Brown. It is
   the exact optimum of the linear programme over multiplicity profiles (probe `distinct_corollary.py` under the data
   root, next to `kappa_table.py`; the weaker Cauchy-Schwarz form gives 0.5364 and 0.8444). Under the hypothesis for
   Dirichlet L-functions the bound of N* for all the zeros is smaller (1.3155 in place of 1.3208, Chirre, Goncalves
   and de Laat); whether a window form exists is not examined.
7. A numerical control on tabulated zeros (a declared experiment): the two discrete moments on windows at several
   heights against (H L^2/2 pi) a and (H L^3/2 pi) b. At accessible heights L is between 9 and 30, so the control
   measures the approach to the main terms and cannot confirm a constant to better than about 1/L.
8. A primary-source search for T1 and for the closed form of Section 2 before any claim (Conrey, Ghosh and Gonek's
   paper of 1989, Steuding's paper of 2002 and the review databases, none of which the preflight could open).

Beyond T1 [R]. A longer mollifier on the window would need cancellation in the sum over k of the errors of the
character row, and smaller errors at the two heights (smoothed endpoints). Without a hypothesis the mollifier is
only O(y^(1 - sigma) L) (Conrey, Ghosh and Gonek (3.6)), which gives the T^(1/2) y of the horizontal sides near
sigma = 0. Under the Riemann hypothesis the partial sums of mu(k) k^(-s) should give O(y^(1/2 - sigma + eps) T^eps)
for sigma <= 1/2 (Perron's formula with 1/zeta and a shift to the line 1/2 + eps), hence (y T)^(1/2 + eps) on the
sides; this is not derived here, and by itself it would not lengthen the mollifier, because the character sums as
bounded above stay O(y T^(1/2 + eps)). Under the Riemann hypothesis alone (without the hypothesis for Dirichlet L-functions) the missing
input is a bound for sums of the coefficients against primitive characters of conductor up to y over a short range
of m that saves a power of T; it is not in the literature read.

## How could this be wrong?

- Section 3 compares orders of magnitude of terms as the papers bound them; it is not a proof. A term that is small
  as a sum up to T can have increments that are not small; items 2b and 3 of Section 4 are where that would show.
- Under the hypothesis for Dirichlet L-functions, pair correlation may have inputs beyond the band on windows; this
  bears on the comparison table of Section 2 and on the corollary for distinct zeros, not on T1.
- The claim that the hypothesis for Dirichlet L-functions is enough (no other L-function enters) rests on the fact
  that the only characters are those of the additive characters e(-m/k), k <= y.
- The proposition of Section 2 is exact, but it rests on the main terms as quoted; they were read on the two
  papers by the preflight and coincide.
- 'No theorem found' is a statement about the searches listed in the preflight, which could not open Steuding
  (2002), the 1989 paper of Conrey, Ghosh and Gonek, or the review databases.
