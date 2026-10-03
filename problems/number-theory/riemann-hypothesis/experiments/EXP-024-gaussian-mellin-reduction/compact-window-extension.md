# Compact smooth windows through controlled inverse Gaussian smoothing

This extends the Gaussian reduction in proof.md to the smooth compact
windows of RH-F4. It does not evaluate the signed dual sum or improve the
moment range. All parameters and orders below are fixed before T increases.

Let W(t)=w((t-T)/H), where w is a fixed smooth compactly supported function,
H=T^theta, 1/2<theta<1, and M<=T^nu with 0<nu<1. Shifts satisfy
|alpha|,|beta|<=C/log T and mollifier coefficients are uniformly bounded.
Choose a fixed eta in (0,theta-1/2), put sigma=T^(theta-eta), and set

\[
 \phi_\sigma(t)=\frac{e^{-t^2/\sigma^2}}{\sqrt\pi\sigma},\qquad
 W_D=\phi_\sigma*\sum_{j=0}^{D-1}
 \frac{(-\sigma^2/4)^j}{j!}W^{(2j)}.\tag{1}
\]

For the Fourier convention exp(-it xi), the multiplier is
exp(-u)sum_(j<D)u^j/j!, u=sigma^2*xi^2/4. The deficit R_D satisfies

\[
 R_D(0)=0,\qquad R_D'(u)=e^{-u}u^{D-1}/(D-1)!,\qquad
 0\le R_D(u)\le u^D/D!\quad(u\ge0).
\]

Fourier inversion and the Schwartz decay of the fixed w give the explicit
type of bound

\[
 \|W-W_D\|_\infty\le
 \frac{\int_{\mathbb R}|v|^{2D}|\widehat w(v)|\,dv}
 {2\pi 4^D D!}(\sigma/H)^{2D}.\tag{2}
\]

On |t|<=2T, the integrand consisting of the shifted zeta product and the
mollifier product has a uniform polynomial bound T^(B+nu), for a fixed B.
Any coarse vertical-strip polynomial bound suffices; no moment asymptotic
or signed cancellation is used. Its integral against W-W_D is therefore
O(T^(B+nu+1-2D*eta)). The zeta poles remain away from the real integration
line for the stated shifts. Outside |t|<=2T, W is zero for large T and
the Gaussian convolution in (1), with compactly supported derivatives,
has exponential tails exp(-c(t-T)^2/sigma^2). Those tails suppress every
polynomial bound. Taking D large gives an error smaller than any prescribed
fixed inverse power of T. This argument remains valid for fixed finite
shift derivatives by Cauchy's integral formula and slightly enlarged
O(1/log T) shift discs; fixed powers of log T are absorbed by the margin.

Equation (1) is a finite signed mixture of normalized Gaussian windows
centered at U in T+H*supp(w). Apply proof.md equation (8) uniformly with
center U and width sigma. All such U are comparable to T. Fubini applies
to the finite outer coefficient integrals and the Gaussian moments,
because their absolute integrals converge by polynomial growth. The total
L1 norm of mixture coefficients is O(H/sigma), since

\[
 \frac1\sigma\sum_{j<D}\sigma^{2j}\|W^{(2j)}\|_1
 =O((H/\sigma)\sum_{j<D}(\sigma/H)^{2j})=O(H/\sigma).
\]

Hence the compact-window signed moment equals the corresponding finite
mixture of the explicitly truncated Gaussian/Hermite dual sums, with error

\[
 O_{A,J,D,\epsilon}\left(
 H T^{1+\nu-(\theta-\eta)+(1+\nu)\epsilon}\log T
 \{T^{-J(2\theta-2\eta-1)}
   +T^{-A(1-\theta+\eta)}\}\right)
 +O(T^{B+\nu+1-2D\eta}).\tag{3}
\]

For any fixed desired power saving, choose eta as above, then J,A,D large
enough and epsilon small enough. Every exponent needed is positive because
theta-eta>1/2 and theta-eta<1. Thus (3) is o(H), uniformly in the stated
composite twists, bounded coefficients and shifts. The crossed residues
are exponentially small uniformly over the centers. No infinite-order
Taylor series or unspecified limit interchanges occur.

The main finite dual sum is retained in full, with Mobius signs, gcd
classes, cutoff and polynomial weights. The inverse Gaussian mixture can
be signed even when w is nonnegative; this is allowed because (2)-(3)
control its replacement error and preserve the original window in the
moment statement. It does not license a positive lower bound on the main
dual sum or a critical-zero count.

For example theta=0.534, nu=0.04 and eta=0.005 give Gaussian exponent
0.529. The phase scale is T^-0.058 and the tail scale is T^-0.471. Nine
phase orders and two tail orders already beat the representation exponent
1+nu-0.529=0.511 with a small fixed epsilon. More orders allow any desired
saving; a coarse heat approximation may need hundreds of derivatives of
the fixed w. These are asymptotic existence statements with constants
depending on those derivatives, not practical finite-height certificates.

This crosses the representation difficulty at nu=theta-1/2. It does not
cross the moment-estimation barrier: a subsequent divisor transformation
still leaves dual length T*h*k/sigma^2, and the signed average over that
nonempty range is open. The short-window onset therefore remains 0.534.
No claim of worldwide novelty is made for Gaussian smoothing, Mellin
inversion or these classical remainder mechanisms.
