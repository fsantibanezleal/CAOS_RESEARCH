# Exact shifted Gaussian transform and controlled phase expansion

This is classical analytic machinery assembled for RH-F4. Its purpose is
to expose the complete signed arithmetic obligation. It establishes no
new moment main term, zero proportion, short-window onset or RH statement.
The derivation below is analytic; finite controls only test normalizations.

## 1. Exact identity, including the crossed residue

Let H>0, T be real, h,k positive integers, and
|Re alpha|,|Re beta|<1/4. Set

\[
 G(s)=\exp((s-\tfrac12-iT)^2/H^2),\qquad
 \sigma_{\alpha,-\beta}(n)=\sum_{uv=n}u^{-\alpha}v^{\beta}.
\]

Define the entire-phase kernel for x>0 by

\[
 K_\beta(x)=\frac{2x^{-\beta}}{\sqrt\pi}
 \int_{\mathbb R}e^{-y^2}
 e^{(1-2\beta+2iT)y/H}\cos(2\pi x e^{2y/H})\,dy.\tag{1}
\]

All powers of positive real numbers use their real logarithms. The integral
in (1) converges absolutely. Then the whole-real-line Gaussian moment is

\[
 \begin{split}
 I_{\alpha,\beta}(h,k)&=
 \int_{\mathbb R}\zeta(\tfrac12+\alpha+it)
 \zeta(\tfrac12+\beta-it)(h/k)^{it}e^{-(t-T)^2/H^2}\,dt\\
 &=2\pi\sqrt{k/h}\sum_{n\ge1}\sigma_{\alpha,-\beta}(n)
 K_\beta(nk/h)
 -2\pi\zeta(\alpha+\beta)G(1-\alpha)(h/k)^{1/2-\alpha}.
 \end{split}\tag{2}
\]

The series in (2) converges absolutely for each stated input. This statement
concerns Gaussian windows, not sharp interval indicators.

To justify the kernel transform, put u=exp(2y/H) in (1). It becomes

\[
 K_\beta(x)=\frac{H x^{-\beta}}{\sqrt\pi}
 \int_0^\infty u^{-1/2-\beta+iT}
 e^{-H^2(\log u)^2/4}\cos(2\pi xu)\,du.\tag{3}
\]

The amplitude and all its derivatives tend to zero faster than any power
at both endpoints and have finite L1 norms. Integration by parts therefore
gives arbitrarily rapid decay in x at infinity. At zero, (1) gives
O(x^{-Re beta}). Its Mellin transform is holomorphic in Re s>Re beta.

First evaluate that transform in 0<Re(s-beta)<1. Insert exp(-epsilon*x),
epsilon>0, in the x integral. Fubini now holds absolutely. The inner cosine
integral equals

\[
 \frac{\Gamma(s-\beta)}2
 \{(\epsilon-2\pi i e^{2y/H})^{-(s-\beta)}
 +(\epsilon+2\pi i e^{2y/H})^{-(s-\beta)}\}.
\]

Its magnitude is bounded, uniformly as epsilon decreases to zero, by a
constant times exp(-2Re(s-beta)y/H). The remaining Gaussian is integrable.
Dominated convergence on y is valid. Dominated convergence on x follows
from the kernel's endpoint bounds. Gaussian integration consequently gives

\[
 \int_0^\infty K_\beta(x)x^{s-1}\,dx
 =2(2\pi)^{-(s-\beta)}\Gamma(s-\beta)
 \cos(\pi(s-\beta)/2)G(s).\tag{4}
\]

Both sides extend holomorphically to Re s>Re beta. This avoids exchanging
an unregularized, infinite vertical Mellin integral with a Gaussian Fourier
integral. On any fixed vertical line in that half-plane the right side is
integrable because G has Gaussian vertical decay. Mellin inversion applies.

Use s=1/2+it in the definition of I. Move the upward contour to
c>max(1-Re alpha,1+Re beta). Polynomial growth of zeta in a fixed vertical
strip and Gaussian decay justify the horizontal limits. Only the pole
s=1-alpha is crossed: the other original pole is s=beta, to the left of
the original line. Its residue is
zeta(alpha+beta)G(1-alpha)(h/k)^(1/2-alpha).
The left upward integral equals the right upward integral minus 2*pi*i
times that residue. Hence the minus sign and factor 2*pi in (2).

On the right line the functional equation gives exactly

\[
 \zeta(1-s+\beta)=2(2\pi)^{-(s-\beta)}\Gamma(s-\beta)
 \cos(\pi(s-\beta)/2)\zeta(s-\beta).
\]

Open zeta(s+alpha)zeta(s-beta) as its absolutely convergent Dirichlet
series, then apply (4). A putative pole at s=1+beta is cancelled by the
cosine zero; it is not another residue. The shift convention is important:
the dual coefficient is sigma_(alpha,-beta), so EXP-021's second shift must
be replaced by -beta when decomposing this series into characters.

## 2. Finite exact Gaussian expressions

For J>=1 and epsilon in {-1,1}, set

\[
 z_{a,\epsilon}=(1-2\beta+2iT+\epsilon4\pi ix+2a)/H,
 \quad P_c(z)=\frac{c!}{2^c}
 \sum_{r=0}^{\lfloor c/2\rfloor}\frac{z^{c-2r}}{(c-2r)!r!}.
\]

Thus P_0=1 and P_(c+1)=P_c'+z P_c/2. Differentiating Gaussian integration
shows that its c-th moment is P_c(z)exp(z^2/4). Define

\[
 \begin{split}
 K_{\beta,J}(x)=x^{-\beta}\sum_{\epsilon=\pm1}e^{\epsilon2\pi ix}
 \sum_{j=0}^{J-1}\frac{(\epsilon2\pi ix)^j}{j!}
 \sum_{a+b+c=j}\frac{j!}{a!b!c!}(-1)^{b+c}(2/H)^c
 P_c(z_{a,\epsilon})e^{z_{a,\epsilon}^2/4}.
 \end{split}\tag{5}
\]

This keeps the linear Fourier phase exact and expands only
exp[epsilon*2*pi*i*x*(exp(2y/H)-1-2y/H)]. It does not Taylor-expand the
original zeta gamma phase across the t window.

Put B=|1-2Re beta|. For all x,H>0,

\[
 |K_\beta(x)-K_{\beta,J}(x)|
 \le \frac{2\sqrt2(2J-1)!!}{J!}
 e^{(B+2J)^2/(2H^2)} x^{-\Re\beta}
 (4\pi x/H^2)^J.\tag{6}
\]

Indeed the Taylor remainder of exp(i v) for real v is at most
|v|^J/J!. The nonlinear real phase has magnitude at most
4*pi*x*y^2*exp(2|y|/H)/H^2. Combine this with the Gaussian amplitude and
use -y^2+L|y|<=-y^2/2+L^2/2, L=(B+2J)/H.
The remaining normalized Gaussian even moment is
sqrt(2)*(2J-1)!!. There are two cosine branches, yielding (6).
The multinomial expansion of (exp(2y/H)-1-2y/H)^j yields (5).

On any fixed band x comparable to T, for H=T^theta, theta>1/2, the
remainder decreases as T^(-J(2theta-1)) for every fixed J. This kernel
statement alone does not justify summing (6) over all n: its right side
grows with x and is not a global summable remainder.

## 3. Off-band estimates and the full bounded mollifier average

Here T tends to infinity, 1/2<theta<1 is fixed, H=T^theta,
0<nu<1 is fixed, M<=T^nu, and |alpha|,|beta|<=C/log T with C fixed.
Uniformity is only in these explicitly bounded shifts and coefficient
families; the constants may depend on theta, nu, C and fixed expansion orders.

Let C_T=[T/(4*pi),T/pi]. For every fixed A the exact kernel outside C_T
satisfies

\[
 |K_\beta(x)|\le C_A x^{-\Re\beta}
 \{(H/(T+x))^A+
 H(T+H^2+1)^A e^{-cH^2}\min(1,x^{-A})\},\tag{7}
\]

where c>0 and C_A are independent of T and x. To see this, choose a fixed
smooth cutoff supported on (3/4,5/4), equal to one on (7/8,9/8), in (3).
On its support each phase T log u +/- 2*pi*x*u has derivative bounded
away from zero by a fixed multiple of T+x whenever x is outside C_T.
Its higher derivatives are O_j(T+x). The cutoff Gaussian amplitude has
j-th derivative L1 norm O_j(H^(j-1)) for H>=1: rescale v=H log u and
differentiate, retaining Gaussian polynomial moments. Repeated application
of (i*phase')^(-1)d/du, followed by integration by parts with vanishing
boundary terms, gives the first term in (7), including the prefactor H.

For the complementary amplitude |log u| is bounded away from zero. Every
fixed derivative L1 norm is O_A((T+H^2+1)^A exp(-cH^2)), possibly reducing
c. This follows by completing the square in log u after all powers of u
are retained. Its Fourier transform is bounded both by its zeroth L1 norm
and by x^(-A) times its A-th derivative norm. This gives the second term.
The estimate includes stationary points far from u=1, rather than silently
discarding them. It is a uniform asymptotic bound, not an explicit numerical
constant for a finite T.

Consider bounded coefficients |b_h|<=C_b and the signed sum

\[
 S=\sum_{h,k\le M}\frac{b_h\overline b_k}{\sqrt{hk}}
 I_{\alpha,\beta}(h,k).
\]

Replacing the dual kernel by (5) only for nk/h in C_T, and dropping its
complement with (7), gives

\[
 S=2\pi\sum_{h,k\le M}\frac{b_h\overline b_k}{h}
 \sum_{nk/h\in C_T}\sigma_{\alpha,-\beta}(n)K_{\beta,J}(nk/h)
 + O_{A,J,\epsilon}(T^{1+\nu+(1+\nu)\epsilon}\log T
 \{(T/H^2)^J+(H/T)^A\}),\tag{8}
\]

for any sufficiently small fixed epsilon>0. The crossed residue and
complementary Gaussian tail are smaller than any fixed inverse power of T.
The same statement with conjugated/reversed twist follows by swapping h,k.

For completeness, |sigma_(alpha,-beta)(n)|<=d(n)n^eta with
eta=C/log T and d(n)<<_epsilon n^epsilon. On the central band,
n<=const*T*M, so n^eta and x^(-Re beta) are bounded uniformly.
There are O(T*h/k) terms for each pair since nu<1. The normalization in
(2) turns 1/sqrt(hk) into 1/h. Thus the absolute central error is at most
const*(TM)^epsilon*T*M*log M*(T/H^2)^J, proving its part of (8).

For the first tail term put a=k/h, N=T/a>=T/M. Sum
a^(-Re beta)*n^(eta+epsilon-Re beta)*(T+an)^(-A)
by an integral when A>1+eta+epsilon-Re beta. It is bounded by
const*a^(-1-eta-epsilon)*T^(1+eta+epsilon-Re beta-A).
The factors a^(-eta) and T^(eta-Re beta) are uniformly bounded here.
After multiplication by H^A/h and summation over h,k this is
O(T^(1+epsilon)*M^(1+epsilon)*log M*(H/T)^A).
The second tail term is summable for A large; all h,k factors grow at
most polynomially in T and are absorbed by exp(-cH^2).
The residue in (2) has the same exponential suppression, since alpha is
bounded by C/log T and alpha+beta stays away from the pole at one.

Choose J and A so that
J(2theta-1)>1+nu-theta+(1+nu)epsilon and
A(1-theta)>1+nu-theta+(1+nu)epsilon.
Then (8)'s error is o(H). No cancellation premise is used to bound this
representation error. The entire main signed sum in (8) remains unevaluated.

## 4. What is still missing

Equation (8) is a shifted composite-twist reduction for Gaussian windows,
not the desired signed moment asymptotic. Mobius coefficients and their
cutoff/polynomial weights must remain in its main sum. With h=gH0,
k=gK0, the phase is exp(+/-2*pi*i*n*K0/H0); the outer weight is
b_(gH0)*conjugate(b_(gK0))/(gH0), with the original cutoff.
EXP-021 applies to the corresponding shifted additive divisor series with
second shift -beta. Nonunit residue classes and all primitive conductor
and parity factors must remain.

A further divisor/Voronoi transformation has a characteristic dual length
T*h*k/H^2. Making that length vanish uniformly recovers the familiar
nu<theta-1/2 restriction. Exceeding it still requires a signed average,
not a Taylor expansion or the Gaussian representation alone. That scale
observation is a route diagnostic; no new Voronoi asymptotic is asserted
here. Compact-window localization and the needed cancellation estimate
are open. No manuscript or new zero bound is licensed by (8).
