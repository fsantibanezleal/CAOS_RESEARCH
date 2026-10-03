# Signed character interface and two different Mellin weights

This derives the interface to EXP-021 and identifies the remaining signed
estimate. It changes neither the source-bound proof nor its control receipts.
All transforms and character identities used here are classical. No larger
moment range or new zero proportion is asserted.

## The phase-peeled divisor sum

For the Gaussian width H_w, the finite EXP-024 expansion has branches
K_J(x)=e(x)V_+(x)+e(-x)V_-(x). Insert a fixed smooth cutoff in x/T,
equal to one around the stationary band x=T/(2*pi); the complementary
original-kernel contribution has the arbitrary-power nonstationary bound
proved in proof.md. The plus branch has no positive-x stationary point;
its finite-order Gaussian profiles are exponentially suppressed there.
Keep it explicitly or bound it before dropping it. The minus profile is
localized on scale H_w around T/(2*pi), with all finite Hermite terms.

Write h=g*H_0, k=g*K_0, gcd(H_0,K_0)=1. The original mollifier coefficient
is b_h*bar(b_k)/h. Mellin inversion of a smooth compact profile V gives

    sum_n sigma_(alpha,-beta)(n)*e(-n*K_0/H_0)*V(n*K_0/H_0)
      = (1/(2*pi*i))*integral_(c)
          Vhat(s)*(H_0/K_0)^s*D_(alpha,-beta)(s,-K_0/H_0) ds,

where c>1+|Re(alpha)|+|Re(beta)| and Vhat(s)=integral V(x)x^(s-1)dx.
Absolute Dirichlet convergence and rapid vertical decay justify this
identity for each fixed finite twist. Subsequent contour moves need every
crossed pole and uniform growth estimate. The profile's Mellin frequency
scale is T/H_w; it is not the original Gaussian height T.

Apply EXP-021 with its generic second shift replaced by -beta. Thus the
local recurrence has A=p^(-alpha), B=p^beta and AB=p^(-alpha+beta).
For d|H_0, q=H_0/d, every gcd class and character is retained. Induced
characters contribute both Euler corrections E_q(s+alpha), E_q(s-beta).
The functional equation of the primitive conductor f applied to z=s-beta
retains

    eps_chi*(f/pi)^(1/2-z)
       *Gamma((1-z+epsilon)/2)/Gamma((z+epsilon)/2),

and L(s+alpha,chi*)*L(1-s+beta,bar(chi*)). This is a positive square only
in the appropriate zero-shift critical-line specialization. The Mobius
signs, the f=1 terms, unequal shifts, polynomial weights and cutoffs remain.

## The unshifted pole and its arithmetic normalization

For gcd(a,H_0)=1, write the unshifted additive divisor series as the finite
Hurwitz decomposition

    D(s,a/H_0)=H_0^(-2s)*sum_(u,v=1)^H_0
                   e(a*u*v/H_0)*zeta(s,u/H_0)*zeta(s,v/H_0).

Each Hurwitz factor has residue one at s=1. Summing the additive character
over v vanishes unless u=H_0. Consequently the double-pole coefficient is
1/H_0. In the simple-pole coefficient the same finite orthogonality selects
the constant term gamma of zeta(s,1); differentiation of H_0^(-2s) adds
-2*log(H_0)/H_0. Hence the Laurent principal part is

    (1/H_0)/(s-1)^2 + 2*(gamma-log(H_0))/(H_0*(s-1)).

The residue after multiplying by Vhat(s)*(H_0/K_0)^s is

    (1/K_0)*[Vhat'(1)+(2*gamma-log(H_0*K_0))*Vhat(1)].

After the original 2*pi*b_h*bar(b_k)/h prefactor, the arithmetic coefficient
is exactly 2*pi*gcd(h,k)/(h*k). This recovers the expected gcd normalization
without a primitive-modulus-only assumption. For unequal shifts the poles
at 1-alpha and 1+beta must be retained, with coalescence handled as a double
pole. They are poles of this phase-peeled series; they must not be confused
with the original zeta-contour residue in proof.md.

## A gamma simplification that cannot be inserted into the wrong weight

Let C_zeta(z)=2*(2*pi)^(-z)*Gamma(z)*cos(pi*z/2). Reflection and duplication
give the meromorphic identities

    C_zeta(z)*pi^(z-1/2)*Gamma((1-z)/2)/Gamma(z/2)=1,
    C_zeta(z)*pi^(z-1/2)*Gamma((2-z)/2)/Gamma((z+1)/2)=cot(pi*z/2).

References: [DLMF 5.5](https://dlmf.nist.gov/5.5) and the primitive
[Dirichlet functional equation](https://dlmf.nist.gov/25.15).
These identities simplify a product only when C_zeta is actually present.
The whole Gaussian kernel has Mellin transform C_zeta(s-beta)*G(s), with
G centered at imaginary height T. The phase-peeled compact profile above
has Mellin transform Vhat(s), centered on frequency scale T/H_w; it does
not carry that C_zeta factor. Removing the phase and also canceling a
nonexistent gamma factor would combine two different representations.

Moreover, i*cot(pi*z/2) approaches +1 at positive imaginary height and
-1 at negative height. With Q=exp(i*pi*z), it equals (1+Q)/(1-Q). For
Im(z)!=0 its difference from sign(Im(z)) is bounded by
2*exp(-pi*|Im(z)|)/(1-exp(-pi*|Im(z)|)). A frequency profile around zero
contains both signs and a central segment; replacing this multiplier by
one throughout is unjustified. Unequal shifts move the central segment.

The open task is to estimate the retained signed conductor/divisor sum
uniformly with these weights and poles. A legitimate spectral conversion
must keep its Eisenstein term before applying cancellation estimates.
Neither a gamma identity nor positive absolute-value bounds supply the
missing asymptotic. The short-window onset remains 0.534.
