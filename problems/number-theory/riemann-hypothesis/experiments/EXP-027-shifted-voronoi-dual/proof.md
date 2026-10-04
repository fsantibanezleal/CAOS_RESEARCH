# Shifted composite Voronoi transformation with all residues

This is classical supporting analysis for RH-F4, not a new signed estimate.
Write e(x)=exp(2pi*i*x), z=a+b, d=a-b, |Re a|,|Re b|<1/4,
and gcd(A,q)=1. At q=1 take the inverse residue to be zero.

## Finite Hurwitz representation and both inverse phases

Opening the two divisor variables in their residue classes gives, first on
Re s>1+max(-Re a,-Re b),

    D_(a,b)(s,A/q)=q^(-2s-a-b)
      sum_(r,t=1)^q e(A*r*t/q) zeta(s+a,r/q) zeta(s+b,t/q).

Every residue class occurs, including nonunits. The finite expression gives
meromorphic continuation. DLMF 25.11.9 expresses each Hurwitz factor in two
periodic Dirichlet series. On Re(s+a),Re(s+b)<0 both are absolutely
convergent, including r/q=1 and t/q=1. Their signs epsilon,eta contribute
the coefficient exp[-i*pi*(epsilon*(1-s-a)+eta*(1-s-b))/2].
The finite double Fourier sum is exactly

    sum_(r,t mod q) e((A*r*t+epsilon*n*r+eta*m*t)/q)
      = q*e(-epsilon*eta*n*m*Ainv/q).

To prove it, sum r first. It vanishes unless A*t+epsilon*n=0 mod q;
there is exactly one such t, including when n is a nonunit. Substitution
gives the displayed phase. Equal signs give -2cos(pi*(s+z/2)) and inverse
phase -Ainv; opposite signs give 2cos(pi*d/2) and phase +Ainv. Thus

    D_(a,b)(s,A/q)=2 q^(1-2s-z) (2pi)^(2s+z-2)
      Gamma(1-s-a) Gamma(1-s-b)
      [cos(pi*d/2) D_(-a,-b)(1-s,+Ainv/q)
       -cos(pi*(s+z/2)) D_(-a,-b)(1-s,-Ainv/q)].

This holds first in the absolutely convergent left half-plane and then
meromorphically everywhere. The finite integer controls check the Fourier
sum in cyclotomic rings; the interval controls check the full formula from
the independently evaluated finite Hurwitz expression. They are controls
of this universal derivation, not its proof.

## Smooth profile, poles and coalescence

Let F be complex valued, smooth and compactly supported inside (0,infinity),
and Ftilde(s)=integral F(x)x^(s-1)dx. Mellin inversion on c>2 gives
the sum as integral D(s,A/q) Ftilde(s)ds/(2pi*i). Shift to Re s=-1.
The finite Hurwitz expression has just the poles 1-a and 1-b. The rapid
vertical decay of Ftilde and polynomial growth of Hurwitz zeta on fixed
strips justify the horizontal limits. For a!=b the residue contribution is

    R_F=q^(-1+a-b) zeta(1-a+b) Ftilde(1-a)
        +q^(-1-a+b) zeta(1+a-b) Ftilde(1-b).

For example, at the first pole the sum over r kills every t except q;
its factor is q. This derives the power of q without a primitive-character
approximation. When a=b the two terms must be combined before taking a
limit, yielding

    R_F=(1/q) integral F(x)x^(-a)*(log x+2gamma-2log q)dx.

Equivalently integrate D(s,A/q)Ftilde(s) around one small circle enclosing
both poles. That expression is holomorphic in the shifts through a=b and
avoids two separately singular estimates. Uniform differentiation in small
complex shifts requires using this combined residue, not discarding one
term or dividing by a-b.

Put

    B(s,n)=2 q^(1-2s-z) (2pi)^(2s+z-2)
      Gamma(1-s-a) Gamma(1-s-b) n^(s-1) Ftilde(s),
    V_+(n)=integral_(Re s=-1) B(s,n)cos(pi*d/2)ds/(2pi*i),
    V_-(n)=integral_(Re s=-1) B(s,n)*[-cos(pi*(s+z/2))]ds/(2pi*i).

Then the exact transformed sum is

    sum_n sigma_(a,b)(n)e(A*n/q)F(n)
      = R_F + sum_n sigma_(-a,-b)(n)
          [e(+Ainv*n/q)V_+(n)+e(-Ainv*n/q)V_-(n)].

Both dual Dirichlet series converge absolutely on this line. Stirling's
bound and the cosine factor leave only polynomial vertical growth, which
Ftilde absorbs. Moving farther left gives arbitrary inverse powers of n;
no new poles are crossed. This proves absolute dual convergence for fixed
F,q,shifts. It does not assert any uniform power saving after q grows with T.
That requires explicit bounds on the actual F and its derivatives.

## Equivalent Bessel profiles, without a singular order quotient

Set Z=4pi*sqrt(n*x)/q. The same transforms are

    V_+(n)=(4/q)cos(pi*d/2)
       integral F(x)(n*x)^(-z/2) K_d(Z)dx,
    V_-(n)=-(2pi/q) integral F(x)(n*x)^(-z/2)
       [sin(pi*d/2)J_d(Z)+cos(pi*d/2)Y_d(Z)]dx.

Here K is the modified Bessel function, unrelated to EXP-026's Fourier
kernel. To check the normalization set u=1-s-z/2. The gamma product becomes
Gamma(u-d/2)Gamma(u+d/2), the scale is (4pi^2*n*x/q^2)^(-u), and
-cos(pi*(s+z/2))=cos(pi*u). DLMF 10.43.19 gives the inverse Mellin
gamma product as 2K_d(2sqrt(w)). DLMF 10.22.43 gives

    Mellin[J_(+d)(2sqrt(w))](u)
      = Gamma(u+d/2)Gamma(u-d/2)sin(pi*(u-d/2))/pi,
    Mellin[J_(-d)(2sqrt(w))](u)
      = Gamma(u+d/2)Gamma(u-d/2)sin(pi*(u+d/2))/pi.

Their difference gives the cosine multiplier. The connection formula
J_-d=cos(pi*d)J_d-sin(pi*d)Y_d removes the apparent division by
sin(pi*d/2); the resulting formula is regular at d=0. In particular it
gives -2pi*Y_0/q for the oscillatory branch and 4K_0/q for the other.

For rigor, pair these Mellin transforms with compact F. Choose the Mellin
u-line with |Re d|/2<Re u<1/4, where the two J transforms are absolutely
integrable at zero and infinity. The gamma product has no pole between that
line and the original transformed line Re u=2+Re z/2. Ftilde has rapid
vertical decay, so moving this paired contour is valid. Mellin Parseval
identifies the Bessel integrals; analytic continuation supplies d=0 and
all stated complex shifts. This uses the full profiles rather than a
pointwise asymptotic expansion with an unaccounted summation error.

## Actual mollifier family and the remaining estimate

In EXP-024 set a=alpha, b=-beta. Write h=g*q, k=g*p with gcd(p,q)=1.
Squarefree mollifier support also forces (g,pq)=1. After separating its
two original exponential branches, its smooth profiles have the form

    F_epsilon(n)=V_epsilon(n*p/q)*chi(n*p/(q*T)),

where V_epsilon is the complete finite Hermite/Gaussian amplitude of
EXP-024 (including all j terms), and chi is a fixed central smooth cutoff.
One may replace the earlier broad central indicator by such a cutoff:
its complement is separated by a fixed multiple of T from the stationary
center; the same nonstationary estimates in EXP-024 make the resulting
bounded mollifier error o(H), after choosing fixed orders large enough.
The outer coefficient remains b_(gq)*conjugate(b_(gp))/(g*q), including
both polynomial weights, g and the original length restriction.

Apply the exact identity separately with A=epsilon*p. The dual coefficient
is sigma_(-alpha,+beta), the Bessel order is alpha+beta, and the power
parameter is alpha-beta. All residue terms and both inverse signs remain.
No extra independent Gauss sum is created.

Changing variables x=n*p/q in the Bessel profiles shows that, apart from
separate powers of p,q and the dual integer, the new weight depends on
the single ratio dual_integer/(p*q). This provides a concrete one-variable
Mellin separation route. Its norm is not automatically bounded independently
of T/H. Large-argument Bessel oscillation, profile derivatives, tails and
coalescing residues must be charged before importing a trilinear estimate.

The signed dual sum and its main residues are now specified. Their uniform
asymptotic evaluation remains open. This proof does not prove a longer
mollifier range, onset improvement, worldwide novelty or RH.

Primary references: [Hurwitz series](https://dlmf.nist.gov/25.11.E1),
[Hurwitz Fourier formula](https://dlmf.nist.gov/25.11.E9),
[J Mellin transform](https://dlmf.nist.gov/10.22.E43),
[K Mellin transform](https://dlmf.nist.gov/10.43.E19),
[Bessel connections](https://dlmf.nist.gov/10.4).
