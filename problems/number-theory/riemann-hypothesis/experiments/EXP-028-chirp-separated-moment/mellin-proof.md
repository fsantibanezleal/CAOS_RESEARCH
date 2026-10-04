# Independent Mellin proof of the proposed short-window moment extension

This derives the same proposed exponents directly from gamma multipliers,
without a differentiated Hankel asymptotic or a guessed dual cutoff.
It supersedes those unresolved symbol assumptions in the original candidate.
The final experiment verdict and manuscript admission still require the
adversarial review of the complete assembly. No published version is edited.

## Uniform profile lemma

Let A(x) be any of the finitely many compactly cut off EXP-024 profiles
V_epsilon,j(x), including the x^(-beta) factor. For fixed j and fixed
orders ell,B, its Gaussian Fourier representation proves

    integral |(x*d/dx)^ell [A(x)*x^(-sigma-z/2)]| dx
       << H*T^(-sigma)*(T/H)^ell,
    |Atilde(1-sigma-it-z/2)|
       <<_(B,sigma) H*T^(-sigma)*(1+|t|*H/T)^(-B).            (1)

Here sigma>0 is fixed, z=alpha-beta, |alpha|,|beta|<=C/log T, and the
constants depend on C,j,ell,B and the fixed central cutoff. The x^(-z/2)
and x^(-beta) factors have bounded magnitude on x~T. A fixed imaginary
shift changes t by O(1/log T), absorbed by (1).

For completeness, (exp(2y/H)-1-2y/H)^j times the Gaussian has all its
fixed Schwartz seminorms O(H^(-2j)): Taylor's integral remainder supplies
the factor H^(-2j), and Gaussian decay absorbs the resulting fixed
polynomials and exp(2j|y|/H). Its Fourier transform is uniformly Schwartz
in (T+epsilon*2pi*x)/H. Multiplication by x^j gives (T/H^2)^j<=1.
Differentiating x^j or x^(-beta) costs 1/T; differentiating the Fourier
profile costs 1/H. The smooth cutoff has 1/T derivatives. Thus the first
bound in (1) follows. Mellin integration by parts ell times gives the
second, also using the zeroth bound. No separate absolute bounds of large
cancelling Hermite monomials are used.

## Exact gamma integral and coefficient separation

Take the EXP-027 transformed sum with a=alpha, b=-beta, d=alpha+beta.
With primal F(n)=A(np/q), change u=1-s-z/2. The oscillatory dual profile,
including the primal outer factor 2pi/(gq), is exactly

    (4pi/(gpq))*n^(-z/2)*(q/p)^(-z/2)
      * integral_(Re u=sigma) Gamma(u-d/2)Gamma(u+d/2)cos(pi*u)
         *[pq/(4pi^2*n)]^u*Atilde(1-u-z/2) du/(2pi*i).       (2)

The nonoscillatory profile has cos(pi*d/2) in place of cos(pi*u).
All primal/dual phases are those fixed by EXP-027. Shifting the paired
u contour to any fixed sigma>0 is valid for sufficiently large T:
its gamma poles lie at Re u<=|Re d|/2, while Atilde is entire and has
arbitrary vertical decay. There is no omitted residue in this shift.
Start on sigma>1+O(1/log T), where the dual Dirichlet series is absolutely
convergent. Move the contour for each finite dyadic n block, not for an
unjustified infinite series on sigma=1/4. The summable estimates below
justify recombining the blocks; far-tail blocks use a larger sigma.

For fixed sigma, uniform Stirling bounds on the compact shift family give

    |Gamma(sigma+it-d/2)Gamma(sigma+it+d/2)cos(pi*(sigma+it))|
       <<_sigma (1+|t|)^(2sigma-1).                          (3)

The gamma exponential decay cancels the cosine growth. Near t=0 boundedness
follows from sigma>|Re d|/2 and compactness; the large-t bound is uniform.
Equations (1)-(3), with B>2sigma, imply the absolute multiplier norm

    integral |Gamma(u-d/2)Gamma(u+d/2)cos(pi*u)
                *Atilde(1-u-z/2)|dt
       << H*T^(-sigma)*(T/H)^(2sigma).                     (4)

At each t, the coefficient [pq/n]^it splits into the three unimodular
factors p^it, q^it, n^(-it). There is only this one integral. The exact
coalescent residue is outside it and is retained separately. Apart from
bounded small-shift powers, (2)-(4) have magnitude prefactor

    (H/g)*(pq)^(sigma-1)*(T/H^2)^sigma*n^(-sigma).           (5)

In particular sigma=1/4 recovers the normalized one-variable separation
cost (T/H)^(1/2) from the earlier chirp/Sobolev calculation. This is an
independent route to its dominant-scale cost. For the far tail choose
sigma=1/4+A. Relative to sigma=1/4, (5) supplies (N0/N)^A on each dyadic
block, N0=T*P*Q/H^2. Thus the tail bound is a contour consequence and does
not assume an unproved Gaussian Bessel damping estimate.

## Source theorem and every dyadic block

For fixed g use the actual b_(gp), b_(gq), both polynomial weights and
p,q<=M/g. Squarefree support imposes (g,p)=(g,q)=1 separately, and
Bettin-Chandee's sum retains (p,q)=1. No restriction is discarded.
With p~P, q~Q, n~N, the three coefficient norms after (5) are

    << P^(sigma-1/2), Q^(sigma-1/2), N^(1/2-sigma+epsilon).

Small-shift powers have bounded magnitude on the contributing polynomial
T ranges, or an arbitrarily small epsilon loss on the far tail. The
unbounded dual n range is not called polynomial in T: n^(C/log T) is
bounded by n^epsilon for sufficiently large T, and the tail contour
absorbs this loss along with the divisor and source-theorem losses.
divisor bound controls sigma_(-alpha,+beta)(n). The norms are independent
of t, so the absolute integral (4) permits the attributed source theorem
inside it. Its exact parameter factor (1+N/(PQ))^(1/2) remains present.

At sigma=1/4, Bettin-Chandee Theorem 1 bounds the ratio to H by

    (1/g)*(T/H^2)^(1/4)
      *[N^(3/5)*(PQ)^(1/10)*(P+Q)^(1/4)
         +N^(3/4)*(PQ)^(1/8)*(P+Q)^(1/8)]
      *(1+N/(PQ))^(1/2) * T^epsilon.                     (6)

For N<=N0, N0/(PQ)=T/H^2<1. Both N powers in (6) are positive, so their
dyadic sums are bounded by their values at N0. For N>N0 use
sigma=1/4+A, multiplying (6) by (N0/N)^A. Any sufficiently large fixed
A absorbs both N powers, their epsilon losses and the source parameter
factor; the sum is again bounded by the N0 expression. If N0<1 this
argument applies to every N>=1 and is only stronger: N0^A<=N0^(3/5)
or N0^(3/4) for A larger than those powers. Thus no small dual range or
unbalanced block is omitted.

The result for this g,P,Q is

    << (H/g)*T^epsilon
       [(T/H^2)^(17/20)*(PQ)^(7/10)*(P+Q)^(1/4)
          +(T/H^2)*(PQ)^(7/8)*(P+Q)^(1/8)].                (7)

If the inverse phase at q=1 is outside the source theorem's convention,
handle it without that theorem. In the admitted range nu<2theta-1,
N0<=T^(1+nu-2theta)<1 whenever q=1 (also when p=1). Move to an arbitrarily
large fixed sigma in (5) and sum all n absolutely using the divisor bound.
The resulting negative power of N0 dominates the polynomial number of
outer coefficients. Thus these endpoint blocks are o(H) with any fixed
power saving; no inverse modulo 1 estimate is presumed.

Use P,Q<=M/g and P+Q<=2M/g. The g sums in (7) are convergent with
exponents 1+33/20 and 1+15/8. The p,q dyadic decompositions cost logarithms
and are absorbed by epsilon. This proves the proposed off-diagonal bound

    <<_epsilon H*T^epsilon
       [T^((17/20)*(1-2theta)+(33/20)*nu)
         +T^(1-2theta+(15/8)*nu)].                         (8)

The nonoscillatory branch does not require (3)'s growing multiplier:
the gamma product retains exp(-pi*|t|). Its norm in (4) is instead
O(H*T^(-sigma)). Choosing sigma large gives (pq/(nT))^sigma and makes
its absolute outer sum o(H), because pq<=M^2 and nu<1/2. The discarded
primal epsilon=+ branch is handled by the arbitrary Schwartz order in
(1); its frequency is separated from zero by a multiple of T/H. These
bounds and the contour argument are uniform in the stated complex shifts.

## Residues and the complete moment assembly

The residue terms and exact powers are those in EXP-027. For the leading
epsilon=- profile put x=T/(2pi)+Hv/(2pi). Its common Gaussian amplitude is

    exp(-v^2-i*(1-2beta)*v/H+(1-2beta)^2/(4H^2)).

Its whole-v integral is exactly sqrt(pi); the positive-x truncation and
central cutoff errors are smaller than every fixed power of H/T. Hence
the two main residues after the outer factor are

    H*sqrt(pi)/g *[zeta(1+alpha+beta)*q^(-1-alpha)*p^(-1-beta)
       +(T/(2pi))^(-alpha-beta)*zeta(1-alpha-beta)
           *q^(-1+beta)*p^(-1+alpha)].                     (9)

Replacing x^(-alpha-beta) by its center value has error O(H/T) times
fixed logarithmic factors, by the first absolute v moment. Every j>=1
profile residue is O((T/H^2)^j) times its leading size, by its Fourier
Schwartz bounds. The absolute outer coefficient sum is at most a fixed
power of log T: sum_g (1/g)*sum_p (1/p)*sum_q (1/q). Separate small-shift
powers are bounded. Therefore these residue errors are o(H), and in fact
smaller than H/log^B T for any fixed B. These estimates do not acquire an
M power from absolute summation.

At alpha+beta=0 combine the poles. For uniformity write their total as a
single fixed contour around them. Equivalently bound the analytic error
on a circle |alpha+beta|=C'/log T enclosing the desired shift disk,
where both zeta factors are O(log T), and use the maximum principle.
The companion shift alpha-beta remains in a compact O(1/log T) disk.
This avoids a spurious 1/(alpha+beta) loss. Fixed-order Cauchy derivatives
cost only fixed powers of log T. The negative exponents in (8) and the
fixed powers in the residue errors absorb them.

Choose the fixed EXP-024 expansion and off-band orders so its absolute
representation error and all fixed shift derivatives are o(H/log^B T).
Then (8),(9) give the standard shifted mollified moment whenever

    0<nu<min(1/2,(17/33)*(2theta-1)),  1/2<theta<1.

EXP-010's Euler/residue evaluation applies at nu<1/2 and yields its same
Conrey constant for fixed P,Q,R. General Q is obtained by the normalized
small-shift derivatives, not by substituting a pointwise gamma expansion.
Finally use EXP-024's fixed-order inverse-heat construction with a strictly
narrower Gaussian width sigma_window=T^(theta-eta). This incurs a genuine
loss: (8) must hold at theta-eta, not theta. Choose fixed eta>0 such that
theta-eta>1/2 and nu<(17/33)*(2(theta-eta)-1). Such an eta exists by the
strict original margin. The mixture's absolute coefficient norm O(H/sigma_window)
multiplies a Gaussian error O(sigma_window*T^(-delta)) to give
O(H*T^(-delta)); it does not introduce another relative T^eta loss.
The inverse-heat remainder uses only a coarse polynomial bound for the
zeta-mollifier integrand, not the desired moment, so this is not circular.

For EXP-010's upper window, whose edge derivatives cost (H/log T)^(-j),
the finite derivative seminorms acquire fixed powers of log T. Its mixture
norm is O((H/sigma_window)*sum_(j<D)(sigma_window*log T/H)^(2j))=O(H/sigma_window).
The approximation error is O(T^(-2D*eta)*log^(2D+O(1))T); a sufficiently
large fixed D absorbs the coarse polynomial integrand bound and every
fixed normalized shift derivative. All orders precede T tending to infinity.
The integral of the mixture equals the integral of the original window
exactly, since its nonzero derivatives integrate to zero and the Gaussian
is normalized. Thus its main term has the correct window mass. Gaussian
centers U in T+O(H) satisfy log U=log T+O(H/T); changing the fixed logarithmic
normalization and centered dual main term costs only a power-small error.
This proves the smooth upper-window statement with error O(H/log T);
there is no silent replacement by a sharp indicator.

## Consequence and final review boundary

The independently checked frozen candidate theta=5339/10000 and
nu=349/10000 has exponents -9/200000 and -189/80000, with a fixed positive
margin. The already certified detector gives a positive parity lower bound
greater than 0.0003985233159135 at this theta. If this complete proof passes
the final adversarial review, the existing counting/parity machinery then
extends positivity to every fixed theta in [0.5339,1). The established
repository onset remains 0.534 until that verdict is recorded.

One explicit smoothing choice is eta=1/100000. At the narrower Gaussian
exponent theta-eta=53389/100000 the charged exponents are
E1=-7/250000 and E2=-937/400000. They are strictly negative. The number
of fixed inverse-heat derivatives needed may be enormous; this supplies
no effective height or practical numerical zeta-window test.

Classical inputs: EXP-024/027's source-bound transformations,
[Bettin-Chandee Theorem 1](https://arxiv.org/abs/1502.00769v1),
uniform Stirling bounds, and EXP-010's detector/counting machinery.
This is not a reproof of the source trilinear theorem, an effective-height
estimate, external peer review, a worldwide-priority claim or an RH proof.
