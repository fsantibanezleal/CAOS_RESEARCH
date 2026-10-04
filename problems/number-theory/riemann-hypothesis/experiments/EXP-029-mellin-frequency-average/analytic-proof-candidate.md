# Rational-frequency mean-square route: unreviewed derivation

All steps below require final adversarial assembly before theorem admission.
No publication or new onset follows from this draft.

For dyadic positive integers p~P, q~Q, n~N, let c(p,q,n) be arbitrary
complex fixed coefficients with any fixed restrictions, and
S(t)=sum c(p,q,n) exp(it log(pq/n)). Combine equal frequencies into C(lambda).
For unequal ratios x=pq/n,y=p'q'/n', integer cross multiplication gives
|x-y|>=1/(4N^2); since max(x,y)<=4PQ/N, their logarithms differ by at least
delta=1/(16PQN). If pq/n=r/s in lowest terms, n=ks and pq=kr. At most 2N
possible k each permit at most tau(kr) factorizations. Thus every group has
size at most R=2N max_{m<=4PQ}tau(m), and
sum_lambda |C(lambda)|^2 <= R sum_{p,q,n}|c(p,q,n)|^2.
Restrictions only shrink those finite groups and sums.

On [-L,L], exp(-t^2/L^2)>=exp(-1). Exact Gaussian integration gives
integral exp(-t^2/L^2)|S(t)|^2 dt
=sqrt(pi)L sum C(lambda)conj(C(mu)) exp(-L^2(lambda-mu)^2/4).
Order the distinct frequencies. The k-th neighbor on each side lies at
distance at least k*delta. Since exp(-x^2) decreases,
sum_{k>=1} exp(-L^2 delta^2 k^2/4)<=sqrt(pi)/(L delta).
Using 2|C(lambda)C(mu)|<=|C(lambda)|^2+|C(mu)|^2,
integral_{-L}^L |S(t)|^2 dt
<= e sqrt(pi) (L+2sqrt(pi)/delta) sum |C(lambda)|^2.
This is an elementary separated-frequency upper bound, not a new classical
mean-value theorem or a cancellation estimate for each individual t.

In EXP-028 formula (2), remove the fixed outside factor 4pi/g and let
c(p,q,n)=b(gq)conj(b(gp)) (pq)^(sigma-1) n^(-sigma)
 times (p/q)^(z/2)*n^(-z/2)*sigma_(-alpha,+beta)(n)
 and the actual inverse additive phase, where z=alpha-beta. The b orientation
 is the original h=gq,k=gp convention; its reversal would have the same norm
 but is not silently substituted in the exact identity. All factors other than exp(it log(pq/n)) are independent of
t. The common weight is the gamma product, cosine and Atilde; A's dependence
on beta is fixed during this estimate, not on p,q,n. For fixed sigma>0,
K=T/H>=1 and any fixed large B,
|gamma(t)| <= C H T^(-sigma) (1+|t|)^(2sigma-1)(1+|t|/K)^(-B).
At sigma=1/2 this is C H T^(-1/2)(1+|t|/K)^(-B).

More generally choose sigma>=1/2. On |t|<=K, Cauchy--Schwarz and the mean
value bound give C H T^(-sigma) K^(2sigma)
 times sqrt(1+PQN/K)*sqrt(R)*||c||_2. On each successive band
2^jK<|t|<=2^(j+1)K the same bound is multiplied by at most
C 2^{j(2sigma-B)} sqrt(1+PQN/(2^jK)) / sqrt(1+PQN/K).
The last ratio is at most one. Pick B>2sigma+1 and sum j>=0.
This avoids the invalid whole-line unweighted L2 integral.

The divisor and fixed small-shift bounds give
||c||_2 <= C_epsilon (PQ)^(sigma-1/2) N^(1/2-sigma+epsilon)
 times (PQ)^epsilon, uniformly on polynomial outer ranges and all dual N.
The unbounded n^(C/log T) is absorbed into N^epsilon for sufficiently large
T; no polynomial-in-T claim is made for the entire tail. Divisor counts
in R cost another (PQ)^epsilon. At sigma=1/2 this yields block cost
(H/g) A^(1/2) N^(1/2) sqrt(1+PQN/K) times epsilon factors,
where A=T/H^2 and N0=A*PQ.

For N<=N0, both N^(1/2) and N (after expanding sqrt(1+x)<=1+sqrt(x))
are positive powers, so the dyadic sum is bounded by its N0 value.
For N>N0 move each finite block's contour to sigma=1/2+D.
The weighted mean-square proof still applies with B>2sigma+1, and relative
to sigma=1/2 its prefactor is (N0/N)^D. Choose fixed D>2+epsilon.
Both expanded N powers and their epsilon factors are summable. If N0<1,
all N>=1 lie in this tail, and N0^D<=N0^(1/2),N0, so the same final bounds
hold. The estimate does not assume a sharply supported dual cutoff.

Every g,P,Q block is consequently bounded by
(H/g) T^epsilon [A*(PQ)^(1/2)+A^(3/2)*K^(-1/2)*(PQ)^(3/2)].
Using P,Q<=M/g, the gcd sums have powers g^-2 and g^-4 and converge.
Outer dyadic sums cost logarithms. Dividing by H, the error becomes
T^epsilon [T*M/H^2+T*M^3/H^(5/2)].
The candidate range is nu<min(1/2,2theta-1,(5theta-2)/6).

Remaining assembly: explicitly bind every source and retained restriction,
the independent nonoscillatory branch, both residues and their coalescence,
all finite signed Gaussian profiles, fixed general Q via Cauchy derivatives,
the original representation remainder and compact conversion at theta-eta.
The prior proof can supply these unchanged components only after confirming
the new strict margins uniformly. No finite control can establish them.

## Independent interval-Gram re-derivation

For distinct ordered frequencies lambda_j, directly integrate their finite
exponential sum on [-L,L]. The diagonal entries are 2L and the off-diagonal
entries are 2 sin(L(lambda_j-lambda_k))/(lambda_j-lambda_k). Their absolute
values are at most 2/(|j-k| delta). Apply the same elementary inequality
2|C_j C_k|<=|C_j|^2+|C_k|^2 to each pair. If there are J frequencies,

    integral_{-L}^L |S(t)|^2 dt
       <= [2L+(4/delta)(1+log(max(1,J)))] sum_j |C_j|^2.

This second derivation has no Gaussian majorant or Fourier-transform
normalization. It has an extra logarithm, which is harmless here:
J<=constant*PQN, PQ is polynomial in T, and log N can be absorbed into
N^epsilon on the unbounded dual tail. Choose the tail contour D and
vertical-decay order B after allocating that extra epsilon loss. It yields
the same two T exponents and uniform range. The Gaussian route is sharper
but both require identical collision accounting and fixed coefficients.

## Complete moment assembly candidate

Apply either estimate to every finite signed Gaussian profile from EXP-024.
The proof uses each whole Fourier profile, preserving its cancellations;
it does not split large Hermite monomials and bound them separately. Fixed
profile orders and derivatives have the same common-weight bounds, with
the factor (T/H^2)^j<=1. All actual squarefree/coprime constraints and
original mollifier polynomial cutoffs remain in c; restrictions shrink the
groups and sums. Both complex shift disks are fixed multiples of 1/log T.

For each finite block shift only inside Re u>0, to the right of the paired
gamma poles. Start in the absolutely convergent dual half-plane and shift
finite n blocks; recombine them only after the summable tail bound. The
nonoscillatory branch retains gamma exponential decay and its common norm
is O(H T^(-sigma)); an arbitrarily large fixed sigma gives the factor
(pq/(nT))^sigma. Since pq<=M^2 and nu<1/2, its absolute outer sum is o(H)
with arbitrarily strong fixed power saving. The inverse modulo one is
defined as zero in EXP-027, giving phase one, which the frequency proof
also covers. No Kloosterman theorem or primitive-modulus restriction is
silently extended to that endpoint.

EXP-027 gives both residues exactly; in EXP-028 notation their leading
outer-normalized terms are

    H*sqrt(pi)/g * [zeta(1+alpha+beta)*q^(-1-alpha)*p^(-1-beta)
       +(T/(2pi))^(-alpha-beta)*zeta(1-alpha-beta)
            *q^(-1+beta)*p^(-1+alpha)].

The whole leading Gaussian amplitude has integral sqrt(pi). Replacing
the center power costs O(H/T) times fixed logarithms; higher profile
residues cost (T/H^2)^j. The absolute outer residue sums cost logarithms,
not M powers, because of the 1/(gpq) factors. At alpha+beta=0 combine
the two poles before estimating. A fixed enclosing shift contour and
maximum-modulus/Cauchy argument give only fixed logarithmic losses. The
positive power savings in the new off-diagonal bound absorb every fixed
shift derivative required by a fixed general Q. Young's arithmetic
residue evaluation is unchanged for nu<1/2. In particular arbitrary Q
retains the constant term Q(0)^2; it is not silently replaced by one.

Choose the fixed EXP-024 expansion and off-band orders to make its complete
representation remainder o(H/log^B T). This is possible for every fixed
theta>1/2 and nu<1, since both 2theta-1 and 1-theta are positive.
The crossed original residue and nonstationary complementary branch are
retained as their previously proved negligible terms.

For a compact upper window of nominal length H=T^theta and edge scale
H/log T, choose a narrower Gaussian sigma_window=T^(theta-eta), eta>0
fixed, such that theta-eta>1/2 and both

    1-2(theta-eta)+nu<0,
    1-(5/2)(theta-eta)+3nu<0.

The strict proposed range permits such eta. EXP-024's fixed-order inverse
heat construction has absolute mixture norm O(H/sigma_window); multiplying
the Gaussian error O(sigma_window*T^(-delta)) gives O(H*T^(-delta)),
with no additional relative T^eta loss. Log-dependent edge seminorms cost
fixed log powers. Choose the inverse-heat order before taking T to infinity,
large enough to absorb a coarse polynomial bound on the zeta-mollifier
integrand; do not assume the desired moment to estimate this remainder.
All nonzero window derivatives integrate to zero, so the mixture preserves
the exact window mass. Centers U=T+O(H) have log U-log T=O(H/T); their
fixed shift normalization and main term incur only power-small errors.
This yields the same compact upper-window moment with error O(H/log T).

EXP-010's Section 3 counting argument uses the length restriction only
through the moment it invokes. Its error E_beta is a finite sum of
normalized zeta derivatives with O(1/log T) coefficients. The new general-Q
moment bounds their mollified squares by O(H); its horizontal argument
and Littlewood bookkeeping are unchanged. The count is distinct odd
sign changes, not simple zeros. Only the separate EXP-006/Wang parity
transfer turns its certified detector bound into simple-critical density.

## Fixed conditional consequence and remaining admission boundary

At theta=527/1000, nu=499/10000 and eta=1/100000, the two charged error
exponents are -51/12500 and -6711/40000. Native and independent rational
receipts bind the frozen detector kappa lower and enclose conditional
h>0.0005947542001. For the same nu, both admissibility bounds increase with
theta and Wang's c(theta) is increasing. Thus, if the complete proof is
admitted, the same fixed detector would give positive simple-critical
density for every fixed theta in [0.527,1). No detector optimization was
performed, and this is not an effective-height or RH statement.

The two mean-value derivations and assembly above still require a recorded
adversarial review, source bindings, residue/counting premise review and
independent arithmetic comparison before analytic admission. Existing
conditional receipts correctly retain their false analytic-theorem flags.
No new manuscript or public assertion follows from this draft alone.
