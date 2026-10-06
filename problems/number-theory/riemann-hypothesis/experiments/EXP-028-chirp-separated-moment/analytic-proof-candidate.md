# Candidate uniform moment extension: analytic review required

Status: proposed proof under adversarial review. The arithmetic receipt is
conditional and does not certify this argument. This file must not be cited
as an established onset improvement before the review obligations at the end
are closed. No manuscript bytes or published theorem are changed here.

## 1. Exact input and normalized oscillatory weight

Use EXP-024's shifted smooth-window reduction and EXP-027's exact Voronoi
identity. Let H=T^theta, M<=T^nu, nu<1/2, and |alpha|,|beta|<=C/log T.
For each fixed gcd g write h=gq, k=gp, (p,q)=1, (g,pq)=1 on squarefree
support. Both mollifier polynomials and the cutoff p,q<=M/g remain in
the coefficients. Their absolute values are bounded by a fixed constant.
The outer factor is 1/(gq), not 1/sqrt(pq) and not a primitive conductor.

The two primal phases are e(epsilon*n*p/q). Their smooth amplitudes are
the complete fixed-order profiles V_epsilon(x) in EXP-024. They satisfy
Schwartz bounds on the scale x=T/(2pi)+H*v/(2pi), uniformly in small
complex shifts. To see this without individually bounding large cancelling
Hermite coefficients, keep their defining Gaussian Fourier integrals:

    V_(epsilon,j)(x) = x^(-beta) (epsilon*2pi*i*x)^j/j!
       * integral exp(-y^2+(1-2beta)*y/H)
         exp(2i*(T+epsilon*2pi*x)*y/H)
         (exp(2y/H)-1-2y/H)^j dy/sqrt(pi).

For fixed j, the last factor and all its fixed y derivatives, after the
Gaussian amplitude is included, have Schwartz seminorms O_j(H^(-2j)).
Repeated integration by parts in y therefore bounds every v derivative
and every polynomial v weight, with factor (T/H^2)^j on the fixed central
x band. x derivatives of its x^j prefactor cost H/T<=1. All j are fixed,
so their sum has uniformly bounded seminorms when theta>1/2. The epsilon=+
profile is smaller than every fixed power of H/T on this positive band.
The central smooth cutoff only adds terms already in that small tail.

Put z=alpha-beta and d=alpha+beta. In the oscillatory transformed branch,
change the primal integration variable to x=n*p/q. Apart from separate
p,q and dual-integer powers of real part O(1/log T), the kernel is

    -(2pi/p) integral V_epsilon(x)
       [sin(pi*d/2)J_d(4pi*sqrt(r*x))
        +cos(pi*d/2)Y_d(4pi*sqrt(r*x))] dx,
    r=dual_integer/(pq).

The precise factors (dual_integer*q/p)^(-z/2) and x^(-z/2) come from
EXP-027 and are retained. Their magnitudes are bounded on polynomial
T ranges; logarithmic shift derivatives remain to be charged.
After also including the outer 1/(gq), the unshifted magnitude scale is

    H/[g*(pq)^(3/4)*T^(1/4)] * dual_integer^(-1/4).

Small-shift powers can be assigned to the separated coefficient sequences.
This explicit normalization is essential to the proposed range.

## 2. Weight norm and tails

On p~P, q~Q, dual_integer~N, write lambda=sqrt(N*T/(PQ)) and
mu=H*sqrt(N/(T*PQ)). Since nu<1/2 and N>=1, the Bessel argument on the
central band tends uniformly to infinity. The classical positive-argument
Hankel representation has the form z_B^(-1/2) exp(+/-i*z_B) times order-zero
symbols, with uniform differentiated bounds for d in a fixed compact set.
Use the large-argument expansions with their remainder bounds, not a bare
leading-term replacement. Alternatively a finite expansion of sufficiently
large fixed order leaves an absolute o(H) error after all polynomial-length
sums; its derivative bounds must also be retained.

Normalize by the magnitude scale above and write the remaining profile as
W(log r), with a smooth log cutoff covering the ratio range of this dyadic
box. Its log-support has bounded length. Absolute integration of the primal
profile bounds ||W||_2 by a fixed constant, and differentiation in log r
costs at most 1+lambda. Repeated nonstationary integration by parts in the
primal x integral gives, for every fixed A,

    ||W||_2 + (1+lambda)^(-1)||W'||_2
       <<_A (1+mu)^(-A).

Indeed the Bessel phase derivative in x is comparable to sqrt(r/T), while
the amplitude derivatives cost H^(-1). Thus the integration-by-parts gain
is mu^(-1). Derivatives of the Hankel symbol and of x powers cost T^(-1),
which is no worse. The fixed smooth cutoff eliminates endpoints; the
Gaussian profile bounds control its tails. Log-r differentiation inserts
a Bessel phase factor O(lambda), and repeating the same integration by
parts preserves the displayed derivative estimate.

Use Fourier inversion in log r. With L=1+lambda, Cauchy-Schwarz and
Parseval give the explicit bound

    (1/(2pi)) integral |What(t)|dt
       <= sqrt(L/2)*(||W||_2^2+L^(-2)||W'||_2^2)^(1/2)
       <<_A (1+lambda)^(1/2)*(1+mu)^(-A).

This is the complete separation cost. At a fixed Fourier frequency, r^it
factors as dual_integer^it*p^(-it)*q^(-it), each unimodular. No derivative
factor is charged separately in three variables. The estimate is classical
Sobolev/Fourier analysis, without a priority claim.

The nonoscillatory K_d branch is exponentially small because its argument
is at least a constant times sqrt(T)/M. The positive-frequency primal
profile is also negligible after taking a sufficiently large fixed
Schwartz order. These claims must be uniform under the full bounded-shift
and fixed-Q differentiation before either branch is omitted.

## 3. Actual coefficient norms and attributed trilinear estimate

Apply Bettin-Chandee 1502.00769v1 Theorem 1 with its parameter vartheta=+/-1.
It permits arbitrary complex separated coefficients and imposes (p,q)=1.
For fixed g, the factors imposing squarefree support and (g,pq)=1 are
assigned separately to the p and q sequences. Both original P weights and
the cutoffs p,q<=M/g remain. Their l2 norms are O(sqrt(P)), O(sqrt(Q)).
The dual coefficient sigma_(-alpha,+beta)(n)*n^(-1/4), including the
separate shift powers, has l2 norm <<_epsilon N^(1/4+epsilon); the usual
divisor bound is enough. Fourier frequencies do not change these norms.

The source bound is

    ||u||_2||v||_2||w||_2*(1+N/(PQ))^(1/2)
       *[(NPQ)^(7/20+epsilon)*(P+Q)^(1/4)
         +(NPQ)^(3/8+epsilon)*(N*(P+Q))^(1/8)].

Multiply by the actual normalization and separation cost. At nu<1/2,
lambda>1 uniformly. Ignoring harmless arbitrarily small epsilon powers,
the ratio to H is bounded by

    (1/g)*[N^(17/20)*(PQ)^(-3/20)*(P+Q)^(1/4)
             +N*(PQ)^(-1/8)*(P+Q)^(1/8)]
      *(1+N/(PQ))^(1/2)*(1+sqrt(N/N0))^(-A),
    N0=T*P*Q/H^2.

The factor 1+N/(PQ) cannot be dropped for the far tail. Since
N0/(PQ)=T/H^2<1, it is absorbed by choosing A sufficiently large.
Summing all dyadic N, including N0<1, gives

    (1/g)*[(T/H^2)^(17/20)*(PQ)^(7/10)*(P+Q)^(1/4)
             +(T/H^2)*(PQ)^(7/8)*(P+Q)^(1/8)]

up to arbitrarily small epsilon powers. This also handles unbalanced P,Q:
use P,Q<=M/g, rather than assuming P~Q or dropping a short block.
The g sums have exponents -1-33/20 and -1-15/8 and converge, so they
introduce no M power. Dyadic decomposition costs logarithms only.
The resulting proposed off-diagonal bound is

    <<_epsilon H*T^epsilon
       [T^((17/20)*(1-2theta)+(33/20)*nu)
         +T^(1-2theta+(15/8)*nu)].

Both exponents are negative if nu<(17/33)*(2theta-1); its bound is stricter
than (8/15)*(2theta-1), which comes from the second term. A fixed positive
margin permits a sufficiently small epsilon and all fixed logarithmic
derivative losses. The source theorem remains an attributed dependency.

## 4. Residues, general Q and compact windows

The two pole residues in EXP-027 become, before outer summation,

    q^(-1+alpha+beta) zeta(1-alpha-beta) Ftilde(1-alpha),
    q^(-1-alpha-beta) zeta(1+alpha+beta) Ftilde(1+beta).

With F(n)=V_-(np/q), change variables x=np/q. The leading Gaussian profile
has integral H/(2sqrt(pi)), up to its negligible positive-x truncation.
The second residue therefore produces H*sqrt(pi) times

    zeta(1+alpha+beta)*q^(-1-alpha)*p^(-1-beta)/g

after the outer 2pi/(gq) factor. The first produces H*sqrt(pi) times

    (T/(2pi))^(-alpha-beta)*zeta(1-alpha-beta)
       *q^(-1+beta)*p^(-1+alpha)/g.

These are the two standard twisted-moment main terms with the actual
mollifier weights. Profile expansion errors cost fixed powers of H/T or
T/H^2, times logarithms after the absolute 1/(gpq) sum. They are o(H).
At alpha+beta=0 use the combined pole contour; never estimate the two
singular zeta terms separately. Maximum-modulus/Cauchy estimates on a
circle of radius constant/log T extend the error through coalescence,
with only fixed logarithmic losses.

EXP-024's finite-profile representation error is made o(H) by choosing
its fixed orders large enough. EXP-010's residue/Euler evaluation requires
nu<1/2, which is retained, and gives the same Conrey constant. Fixed-degree
general Q is applied by Cauchy differentiation in the small shifts, with
normalized log(T) factors. Every differentiation loss is logarithmic and
is absorbed by the fixed power margin. EXP-024's inverse-heat compact-
window conversion is then applied uniformly to the shifted moment and its
derivatives; no sharp indicator is assumed automatically.

## 5. Conditional consequence and unresolved review gates

For theta=0.5339, nu=0.0349, the exact proposed exponents are -9/200000
and -189/80000. The original nu<theta-1/2 range rejects this nu. The existing
certified EXP-010 detector has kappa>0.02503497665228; its parity transfer
at this new theta is greater than 0.0003985233159135. These arithmetic facts
are certified separately. They remain conditional on the uniform moment.

Before a confirmed verdict, independently recheck:

1. Full differentiated Hankel symbol/remainder bounds and the normalized
   W,W' estimate, including complex order and all fixed profile terms.
2. Residue error estimates through pole coalescence and their absolute
   outer sums; the fixed-Q Cauchy constants and compact-window conversion.
3. Every p,q,dual-n power, unbalanced/small blocks, the far-tail source factor,
   and the actual g/cutoff restrictions against the source theorem.
4. The immutable EXP-010 detector source/receipt and an independent parity
   enclosure; source-overlap research and manuscript coherence assessment.

Until these are resolved, 0.5339 is an unproved candidate, not a new onset,
and the current established onset remains 0.534. No effective height follows.
