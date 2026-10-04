# Complete internal analytic review of the rational-frequency moment

Review date: 2026-10-04. This is an internal mathematical review relative to
attributed inputs, not independent external peer review or formal verification.
The universal argument is the persisted analytic derivation. Finite receipts
are separate controls and retain their false analytic-theorem flags.

## Re-derive the actual normalization before estimating

Use h=gq,k=gp, gcd(p,q)=1 in the original Gaussian identity. Its coefficient
is 2pi*b(gq)*conj(b(gp))/(gq), and F(x)=A(x*p/q). In the shifted transformation,
a=alpha,b=-beta,z=alpha-beta,d=alpha+beta. Its Mellin factor is
Ftilde(s)=(q/p)^s*Atilde(s). Substituting u=1-s-z/2 into the full transformed
expression gives exactly

    (4pi/g)*(pq)^(-1)*(p/q)^(z/2)*n^(-z/2)
      * integral Gamma(u-d/2)Gamma(u+d/2)cos(pi*u)
          *[pq/(4pi^2*n)]^u*Atilde(1-u-z/2) du/(2pi*i).

Thus all p,q,n-dependent factors other than exp(it*log(pq/n)) are fixed
coefficients. The original b orientation is retained. The factor (4pi^2)^(-it)
belongs to the common multiplier and has modulus one. The inverse additive
phase has modulus one and requires no separate inverse estimate, including
q=1. No family with different coefficient dependence is substituted.

The profile includes x^(-beta). The more precise zeroth amplitude factor
is H*T^(-sigma-Re(d)/2), which is bounded by a fixed multiple of H*T^(-sigma)
on |alpha|,|beta|<=C/log T. The paired gamma real parts sum to 2sigma;
Stirling gives polynomial order 2sigma-1 after its exponential decay cancels
the cosine. Near t=0 its poles are outside the fixed line sigma>=1/2 for
large T. The full finite Fourier profile, not separated Hermite monomials,
has arbitrary fixed Mellin decay at scale K=T/H. Its dependence on beta,
profile order and the center is common to every coefficient in a block.

## Universal mean-square estimates and weighted use

Cross multiplication and log(y/x)>=(y-x)/y give the actual gap
1/(16PQN). A ratio r/s in lowest terms has n=ks,pq=kr with at most 2N
possible k, each with at most max_{m<=4PQ}tau(m) factorizations. The grouped
coefficient inequality is Cauchy--Schwarz within each group, so its factor
R<=2N max tau cannot be omitted. Actual restrictions only shrink groups.

First route: integrate the finite sum against exp(-t^2/L^2), use its exact
Fourier transform, and sum the positive Gaussian off-diagonal entries by
ordered-frequency distance. The Schur bound is

    integral_{-L}^L |S(t)|^2 dt
       <= e*sqrt(pi)*(L+2sqrt(pi)/delta)*R*sum |c|^2.

Second route: integrate directly on [-L,L], bound each off-diagonal entry
2sin(L*(lambda-mu))/(lambda-mu) by 2/(|j-k|*delta), and sum the harmonic
rows. This gives [2L+4*delta^(-1)*(1+log(max(1,J)))]*R*sum |c|^2.
It has no Gaussian Fourier normalization and an extra logarithm. Since
J<=constant*PQN, log N is absorbed into N^epsilon in the dual tail. Both
routes are proofs for arbitrary finite complex coefficients; the classical
Evans mean-value lemma is context, not an imported rational-frequency theorem.

For sigma>=1/2 apply Cauchy--Schwarz only on |t|<=K and finite dyadic
bands beyond it. On the central interval the multiplier supremum is
O(H*T^(-sigma)*K^(2sigma-1)); its square norm costs another K^(1/2).
The sum's square norm is O((K+PQN)^(1/2)*R^(1/2)*||c||_2). Consequently

    integral |gamma(t)*S(t)| dt
      << H*T^(-sigma)*K^(2sigma)*sqrt(1+PQN/K)*sqrt(R)*||c||_2,

up to the independent route's harmless logarithm. The j-th outer band
costs at most constant*2^(j*(2sigma-B)), choosing B>2sigma+1 after all
fixed orders are known. This proves an integrable weighted estimate without
an illegal whole-line unweighted L2 norm. The multiplier phase causes no
problem because only its absolute value is used at this step.

## Coefficients, all dual blocks and gcds

The fixed coefficient square norm is bounded by
(PQ)^(sigma-1/2+epsilon)*N^(1/2-sigma+epsilon). The shifted divisor bound
and collision divisor count cost epsilon powers. The factors n^(C/log T)
are absorbed into N^epsilon, not claimed uniformly bounded on an infinite
range. Fix epsilon smaller than every strict exponent margin.

At sigma=1/2 the raw relative-to-H cost is

    g^(-1)*A^(1/2)*N^(1/2)*(1+sqrt(PQN/K)), A=T/H^2.

The two N slopes are 1/2 and 1. For N>N0=A*PQ, moving each finite block
to sigma=1/2+D supplies exactly (N0/N)^D. With D=4 the slopes become
-7/2 and -3 before the small epsilon allocation; both remain negative.
If N0<1 all blocks use that larger contour, and N0^D is at most both
N0^(1/2) and N0. There is no unsummed series on the short contour, hidden
sharp dual cutoff, or neglected ratio-one resonance at n=pq. That resonance
lies beyond N0 when A<1 and is included in the same tail estimate.

After summing every N block the cost is

    (H/g)*T^epsilon*[A*sqrt(PQ)+A^(3/2)*K^(-1/2)*(PQ)^(3/2)].

Both p,q powers are positive, including unbalanced blocks. Substituting
P,Q<=M/g gives convergent g^(-2) and g^(-4) sums and only logarithmically
many outer dyadic scales. The resulting error is

    O_epsilon(H*T^epsilon*[T*M/H^2+T*M^3/H^(5/2)]).

No Bettin--Chandee trilinear theorem is used in this new estimate. Its range
is nu<min(1/2,2theta-1,(5theta-2)/6) for every fixed 1/2<theta<1.
The two new branches cross at theta=4/7. The older trilinear range becomes
stronger again above theta=12/13, so it must not be erased or described as
universally superseded.

## Complete assembly and counting checks

| obligation | attack and reviewed resolution |
|---|---|
| representation error | EXP-024's complete absolute error is T^(1+nu+epsilon) times arbitrarily high fixed powers of T/H^2 or H/T; choose orders before the limit, using theta>1/2 and theta<1 |
| finite profile family | each whole Fourier profile keeps its cancellations and has factor (T/H^2)^j<=1; every fixed derivative is charged |
| smooth cutoff | the complementary original branch is uniformly nonstationary, including the exponentially small remote stationary tail; broad indicators are replaced only after this bound |
| contour interchange | start with the absolutely convergent dual series, shift finite n blocks inside Re u>0, then recombine after the summable estimates; no gamma pole is crossed |
| nonoscillatory branch | gamma exponential decay remains; a large fixed sigma gives absolute error O(H*T^epsilon*(M^2/T)^sigma), negligible because nu<1/2 |
| original crossed pole | it retains its Gaussian exponential suppression from EXP-024, and is not confused with the two transformed residues |
| both transformed poles | direct substitution gives the exact powers in the candidate; the leading full Gaussian mass is sqrt(pi), center replacement costs H/T and higher profiles cost (T/H^2)^j |
| residue summation | inverse gpq weights make absolute outer sums logarithmic rather than M powers; no sign cancellation is presumed for those errors |
| coalescence | combine both poles before taking alpha+beta=0; a fixed enclosing shift contour and Cauchy estimates cost fixed powers of log T |
| general Q | uniform shift disks cover every fixed normalized derivative; Young's arithmetic evaluation at nu<1/2 is unchanged, including Q(0)^2 for arbitrary Q |
| upper window | evaluate the new exponents at theta-eta, not theta; the inverse-heat mixture norm H/sigma_window cancels its Gaussian error scale sigma_window |
| window remainder | use only coarse polynomial bounds for the zeta-mollifier integrand; choose fixed inverse-heat order to absorb them, including logarithmic edge seminorms |
| window mass and centers | nonzero compact-window derivatives have integral zero; mass is exact, while log U-log T=O(H/T) causes only power-small errors |
| counting premise | EXP-010 Section 3 uses its length restriction only through the general-Q moment; its finite zeta-derivative errors have O(1/log T) coefficients and moment O(H) |
| multiplicity transfer | the detector counts distinct odd sign changes, not simple zeros; simplicity uses the separate EXP-006 parity transfer and Wang's attributed pair theorem |
| fixed endpoint | the frozen accepted detector entry at nu=499/10000 is unchanged; native and independent rational intervals agree, and a zero detector fails positivity |

The explicit smoothing choice theta=527/1000, nu=499/10000, eta=1/100000
has exponents -51/12500 and -6711/40000. Fixed logarithmic derivative losses
are absorbed by these strict power margins. No effective height follows,
particularly for the fixed degree-201 detector and large expansion orders.

## Actual refutations and controls

The first exact control covers 432 dyadic blocks, 524,400 triples and 180
exponent configurations. Its initial spacing mutation is not a stand-alone
log-gap refutation; the independent rational control supplies the proper
upper-log-gap witness and keeps the original receipt unchanged. An actual
coprime ratio-one group of six triples has normalized interval mass 36,
where a diagonal-only substitution would give 6. The unweighted constant
sum has integral 2L on [-L,L] and divergent whole-line norm.

The declared raw-cost control independently reconstructs gamma, coefficient,
collision, spacing and gcd exponents on 6,426 configurations, including
N0<1, transitions, unbalanced blocks and far tails. It reaches the two
proposed worst exponents and rejects zero margin, excessive window loss and
an uncontrolled tail. The universal slope proof above, rather than these
finite samples, covers all dyadic variables. Native and stdlib rational
parity enclose h>0.0005947542001 using the frozen detector receipt.

## Admission and limits

The proposed moment range and its theta=0.527 simple-critical consequence
survive this complete internal analytic review. Their scientific verdict
is confirmed internally relative to the retained attributed inputs. The
universal derivation and arithmetic controls have different evidential roles.
External specialist review, worldwide priority, full Lean formalization and
an effective starting height are unconfirmed. RH remains open. Published
v0.02 and the live 0.76.000 app retain their original claims and exact bytes;
a coherent stronger manuscript and subsequent release are separate gates.
