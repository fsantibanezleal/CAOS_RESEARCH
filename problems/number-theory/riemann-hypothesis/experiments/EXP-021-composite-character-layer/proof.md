# Complete arithmetic layer; analytic reciprocity still open

Use e(x)=exp(2*pi*i*x), tau_q(chi)=sum_(u mod q) chi(u)e(u/q),
and sigma(n)=sum_(uv=n)u^(-alpha)v^(-beta). Characters vanish at non-units.
For q=1 the unique character is one, phi(1)=tau_1=1 and L(s,chi)=zeta(s).
These conventions retain the completely divisible residue class.

## Gcd classes and shifted Euler correction

Assume gcd(a,h)=1, Re(s+alpha)>1 and Re(s+beta)>1. Partition n uniquely as
n=d*m with d=gcd(n,h) and q=h/d. Then gcd(m,q)=1 and e(a*n/h)=e(a*m/q).
Finite character orthogonality on the unit group gives

    e(a*m/q) = (1/phi(q))*sum_(chi mod q) tau_q(bar(chi))*chi(a)*chi(m).

Indeed, expand tau, interchange the finite sums and use
sum_chi chi(a*m)*bar(chi(u))=phi(q) when u=a*m mod q and zero otherwise.
This step uses every character, including principal and induced characters.
All d|h classes are disjoint and exhaustive.

Set A=p^(-alpha), B=p^(-beta), and S_b=sum_(j=0)^b A^j B^(b-j), S_-1=0.
The recurrence S_(b+1)=(A+B)S_b-AB S_(b-1) gives the formal identity

    sum_(j>=0) S_(b+j) x^j = (S_b-AB*S_(b-1)*x)/((1-A*x)*(1-B*x)).

It holds also when A=B and without dividing by S_b. Thus define

    C_(d,q,chi)(s) = product_(p^b||d, p|q) S_b
        * product_(p^b||d, p not|q) (S_b-AB*S_(b-1)*chi(p)*p^(-s)).

Multiplicativity and the absolutely convergent Euler products now give

    D(s,a/h) = sum_(d|h) d^(-s)/phi(q)
        * sum_(chi mod q) tau_q(bar(chi))*chi(a)*C_(d,q,chi)(s)
          * L(s+alpha,chi)*L(s+beta,chi),  q=h/d.

There are finitely many d and chi. The coefficient at m on the right is
sigma(d*m)*chi(m), including all primes shared by d and q. No asymptotic,
short-window error or averaging estimate has been used. Meromorphic
continuation follows from this finite expression and the established
continuation of Dirichlet L-functions; contour shifts still need their own
pole and growth estimates.

## Primitive conductor, parity and gamma ratio

Let chi be induced by the primitive chi* of conductor f|q, with parity
epsilon in {0,1}. Write

    E_q(u)=product_(p|q, p not|f) (1-chi*(p)*p^(-u)).

Then L(u,chi)=E_q(u)*L(u,chi*). The primitive functional equation gives

    L(u,chi*) = eps_chi*(f/pi)^(1/2-u)
        * Gamma((1-u+epsilon)/2)/Gamma((u+epsilon)/2)
        * L(1-u,bar(chi*)),
    eps_chi=tau_f(chi*)/(i^epsilon*sqrt(f)).

Apply this to u=s+beta, keeping both Euler factors E_q(s+alpha),
E_q(s+beta). The remaining product is
L(s+alpha,chi*)*L(1-s-beta,bar(chi*)). At s=1/2+it and alpha=beta=0 it
is |L(1/2+it,chi*)|^2. For unequal shifts it cannot generally be replaced
by a positive square. The conductor-one case uses the zeta functional
equation as a meromorphic identity, with its poles retained.

For a prime modulus p, the d=p, q=1 correction is
p^(-s)*(p^(-alpha)+p^(-beta)-p^(-alpha-beta-s)). The principal d=1 term
is -(1-p^(-s-alpha))*(1-p^(-s-beta))/(p-1) times zeta(s+alpha)zeta(s+beta).
At zero shifts these give 2p^(-s)-p^(-2s) and the principal correction.
After multiplying by (p/k)^s and choosing a=-k, they reproduce Tang's
Section 3 arithmetic split. The primitive Gauss product converts its parity
factor to i^(-epsilon), exactly rather than by an absolute-value estimate.

## Supported squarefree mollifier and induction signs

If h is squarefree, then d and q are coprime and q=f*r with gcd(f,r)=1.
Chinese remainder decomposition and the unit-frequency Ramanujan sum give

    tau_q(bar(chi)) = mu(r)*bar(chi*)(r)*tau_f(bar(chi*)).

For clarity, write a residue modulo f*r using the two CRT inverses. Its
additive character splits into unit frequencies on f and r. The f-factor
is bar(chi*)(r)*tau_f(bar(chi*)); the r-factor is mu(r). This proves the
identity without using primitive Gauss normalization at the induced modulus.
The established primitive identity
tau_f(chi*)tau_f(bar(chi*))=chi*(-1)*f then yields

    mu(h)*tau_q(bar(chi))*eps_chi
      = mu(d)*mu(f)*bar(chi*)(r)*i^epsilon*sqrt(f).

The induction mu(r) cancels the outer mu(r); the other signs, character
phases, Euler corrections and gamma ratios remain. The same formula holds
for f=1. This is an exact reorganization, not a saving in a signed family.

When expanding a squarefree Mobius mollifier double sum, first put
h=g*H, k=g*K, gcd(H,K)=1. Squarefree support forces pairwise coprimality
of g,H,K and mu(h)mu(k)=mu(H)mu(K). The coefficient becomes
mu(H)mu(K)*P[gH]*P[gK]/(g*sqrt(HK)). Regrouping H=d*f*r therefore preserves
the cutoff and both polynomial weights; it must not factor them into
independent unrestricted Euler products. In Tang's Mellin integral the
factor (H/K)^s remains, so K^(-it) is retained on the critical Mellin line.

## Remaining obligation and attribution

This is classical finite character Fourier analysis and Euler-product
bookkeeping. [DLMF sections 27.8 and 27.10](https://dlmf.nist.gov/27.10)
give the character and Gauss identities. Tang's
[arXiv:2608.14852v1](https://arxiv.org/abs/2608.14852v1), including its full
proof and closing remarks, supplies the prime, unshifted analytic model.
This derivation addresses the composite arithmetic layer only. A complete
shifted short-window reduction must still justify its Mellin weight,
functional-equation contributions, residues and uniform analytic errors.
An asymptotic evaluation of the remaining signed conductor family is another
obligation. No longer mollifier, new onset, new proportion, novel-method
priority or RH conclusion follows here.
