# Independent adversarial check: finite Hilbert stability for short intervals

Date: 2026-09-12. Status: hand derivation checked against Ainta's finite rank-trace lemma and Lamzouri/Axiom's exact kernel identities. This note is not a Lean certificate. Numerical experiments were not run. The application to short intervals relies on Wang's stated Theorem 2.2 and Lemma 3.1; it does not assume RH.

## Exact finite construction

Let Z be a finite conjugation-invariant support in C, with positive integer multiplicities m(z)=m(conj z), and total mass N=sum_Z m(z). Let eta be real and even, compactly supported and L2-normalized. Set

    f_z(u)=eta(u) exp(-2 pi i z u),
    K(w)=integral eta(u)^2 exp(-2 pi i w u) du.

All f_z belong to L2 because the support is compact and Z is finite. Work in the finite-dimensional complex Hilbert space E spanned by the f_z. For rank-one operators use |f><g|:h -> f integral(conj(g)h). Define

    A = sum_z m(z) |f_z><f_conj(z)|.

This reflected-kernel operator is the precise replacement for the original Gabor-compressed matrix. It is essential to use f_conj(z) in the second slot, rather than f_z or its pointwise complex conjugate indiscriminately.

1. A is selfadjoint: its adjoint swaps z and conj(z), and the support/multiplicities are invariant.
2. tr A=N exactly. Each term has trace integral(conj(f_conj(z)) f_z)=integral eta^2=1.
3. Its Hilbert-Schmidt norm squared is

       Q=||A||_HS^2=sum_{z,s} m(z)m(s) K(z-s)^2.

   To check the nonstandard square: direct integration first gives K(z-conj(s))^2 because K is even. Reindex s by conj(s). Thus the full sum is real and nonnegative even though individual terms need not be real or nonnegative. This step is consistent with `AxiomMath/ZetaZerosV2`, commit 4c73b317, `Hilbert/AlphaExpansion.lean:2477-2545` and `Hilbert/FIdentity.lean:81`.

Let S be the simple real support points, s=#S, r the number of distinct multiple real points, and b the number of conjugate nonreal pairs. Set

    P=sum_{x in S}|f_x><f_x|=VV*,
    R=A-P,
    G=V*V=(K(x-y))_{x,y in S}.

For real x the norm of f_x is exactly one, so G is PSD with diagonal 1 and tr P=s. A multiple real point contributes a positive rank-one operator. A conjugate pair contributes

    m(|f_z><f_conj(z)|+|f_conj(z)><f_z|)
      =2m(|g_z><g_z|-|h_z><h_z|),

where g_z=(f_z+f_conj(z))/2 and h_z=(f_z-f_conj(z))/(2i). Its positive index is at most one. More directly, on the orthogonal complement of the span of all r multiple-real vectors and b vectors g_z, the quadratic form of R is nonpositive. Therefore n_+(R)<=r+b, without any lower bound on the distance of nonreal points from the real axis and without any pointwise positivity assumption on K at complex arguments.

## Stability inequality, checked with padding

For t>=0 let Psi(t)=(t-1)^2 for 0<=t<=2 and Psi(t)=2t-3 for t>=2. It is convex and nonnegative. Ainta's `paper/riemann.tex:116-177` proves, for P=VV* with s columns of norm <=1, R Hermitian and n_+(R)<=d,

    ||P+R||_HS^2 >=4 tr(P+R)-3s-4d+tr Psi(V*V).

Its proof remains valid if s differs from dim E. Pad spectra to max(s,dim E): when s>dim E, the additional p=0 terms have 2p-1+Psi(p)=0, so there is no spurious zero-eigenvalue penalty; when s<dim E, discarded negative-part terms are nonnegative. No full-rank or invertibility assumption on G is needed.

Applying the inequality with d=r+b and tr A=N gives

    Q >=4N-3s-4(r+b)+tr Psi(G).

Since N>=s+2r+2b, we obtain the exact strengthened finite-multiset inequality

    s >=2N-Q+tr Psi(G).                         (F)

The strengthened statement requires the Gram matrix of the actual simple-real subset. The off-line points and multiple real points are entirely in R and must not be included in that Gram matrix. Formula (F) is a direct transfer of Ainta's known stability lemma to Lamzouri's finite Hilbert setting. It may be a useful new bridge/application but the stability lemma itself is prior work and must be attributed.

## Pinching and compact block energies

For any PSD principal block B of G,

    tr Psi(B) >= min(1, 2 sum_{i<j}|B_ij|^2).

If all eigenvalues are <=2 then tr Psi(B)=||B-I||_HS^2; if one exceeds 2 then its Psi value exceeds 1. Convex trace pinching gives tr Psi(G)>=sum_blocks tr Psi(B) for a disjoint partition into principal blocks, and leftover singleton blocks may be discarded because Psi>=0. No positivity of offdiagonal entries is used.

Thus a uniform positive lower bound for the three-point kernel energy on a compact triangle is enough. A uniform compact approximation of kernels preserves such a bound: for normalized densities f_epsilon=eta_epsilon^2 and f_0,

    sup_{x real}|K_epsilon(x)-K_0(x)| <= ||f_epsilon-f_0||_1,

and |K_epsilon(x)|,|K_0(x)|<=1. Consequently the triple energy 2[K(u)^2+K(v)^2+K(u+v)^2] changes by at most 12||f_epsilon-f_0||_1. This is a global-real estimate, stronger than compact-only convergence. For real even densities all these real-frequency kernel values are real, so squares and absolute squares agree.

## Short-interval analytic interface and limit order

Wang arXiv:2609.07918v1, Theorem 2.2, fixes 0<lambda<theta<1, H=T^theta and a smooth even test g supported in [-lambda,lambda]. Its error is O_g(H+T^lambda log^2 T). After normalizing by H log T, this tends to zero for every fixed lambda<theta; it is not uniform as lambda approaches theta.

Wang Lemma 3.1 removes the rational pair weight by applying the theorem separately to f*f and its second derivative for a fixed smooth eta supported in (-lambda/2,lambda/2). The resulting full Q/N tends to M(f)=integral f^2+double-integral |u-v|f(u)f(v). The finite Gram matrix in (F) involves the same K=Fourier(f), so there is no mismatch between the baseline pair sum and the defect kernel.

Correct order of choices for a claimed strict improvement:

1. Fix theta with Wang c(theta)>0.
2. Choose a finite triple-span bound R giving a positive-density block count from that baseline.
3. Choose lambda<theta sufficiently close and a smooth normalized eta sufficiently close to the cosine minimizer so that the baseline loss is smaller than a fixed fraction of the positive defect gain, while the compact kernel-energy gap persists.
4. Keep lambda, eta, R fixed as T tends to infinity. Both test functions used in weight removal remain fixed, so Wang's error is o(N).

One must not choose lambda=theta in Wang's stated error bound or let the smoothing scale shrink with T without a separate uniform error proof. A theorem for each fixed theta is supported; a uniform theta-dependent height threshold is not supplied by this argument. Short-interval Riemann--von Mangoldt gives normalized span X=H log T/(2pi) and N(T,H)=X+O(H+log T), hence X/N ->1 for fixed theta>0. No Gabor tails, endpoint deletion or long-interval trace transfer is required in this direct Hilbert construction.

## Explicit positive triple energy: independent algebra check

Fix 0<theta<1, let a=theta/sqrt(2), c=a tan(a)>0 and let the normalized cosine density be f_theta(u)=cos(sqrt(2)u)/(sqrt(2)sin(a)) on [-theta/2,theta/2]. Write k_theta for its Fourier transform. For X=pi theta x define A_X=c cos(X)-X sin(X). Direct integration gives the globally continuous identity

    A_X=c(1-X^2/a^2) k_theta(X/(pi theta)).

At the removable points X=+/-a this is still an identity by continuity; both A_X and the factor vanish, and no division there is required.

For X,Y>=0 with Z=X+Y<=S=pi theta R, direct expansion of sine/cosine addition formulas yields

    (X^2+XY+Y^2+c^2) sin(X)sin(Y)
      =A_X A_Y-X A_X sin(Y)-Y A_Y sin(X)-c A_Z.       (I)

Let e=max(|A_X|,|A_Y|,|A_Z|). If e<c/2, use |cos(t)|+|sin(t)|>=1 to get

    c<=|A_X|+(c+X)|sin(X)|,
    |sin(X)|>=c/[2(c+S)],

and likewise for Y. Hence the absolute value of the left side of (I) is at least c^4/[4(c+S)^2]. Its right side is at most e^2+(S+c)e, which is less than (S+3c/2)e. Therefore

    e>=b=min(c/2, c^4/[4(c+S)^2(S+3c/2)]).

The endpoint e=c/2 or e=b causes no issue: the conclusion is a non-strict lower bound. Set B=c(1+S^2/a^2). The kernel identity gives |A_X|<=B|k_theta(X/(pi theta))|, including the removable point, and the corresponding bounds for Y,Z. Therefore

    2[k_theta(u)^2+k_theta(v)^2+k_theta(u+v)^2]
      >=2(b/B)^2,              u,v>=0, u+v<=R.

Take delta=(b/B)^2. It satisfies 0<delta<=1/4 because b<=c/2 and B>=c. This formula both proves that additive triples of kernel zeros cannot exist and supplies a positive global compact lower bound; it does not rely on sampling a grid or on a numerical minimization.

## Shifted triple counting and smoothing: quantifiers checked

Order the s simple-real coordinates x_1<...<x_s and let L=x_s-x_1, with the empty/singleton case handled by L=0. There are s-2 consecutive triples when s>=3. Their spans sum to at most 2L. Thus at least s-2-2L/R triples have span <=R. Color their starting indices modulo 3. Within each color the triples are disjoint principal Gram blocks. Pinch separately for the three colors and add the three inequalities to obtain

    tr Psi(G)>=delta/3 (s-2-2L/R),                  (P)

provided each short triple has block defect >=delta. If the right side is negative the inequality follows from nonnegativity, so the small-s cases are covered without inventing triples.

For each fixed theta select lambda_n<theta tending up to theta and smooth normalized densities f_n=eta_n^2, supported inside (-lambda_n/2,lambda_n/2), that converge to f_theta in L1 and L2. Their pair main terms tend to A_theta=theta/2+cot(theta/sqrt(2))/sqrt(2), by continuity of the quadratic functional on the bounded support. The uniform Fourier error estimate above shows that when ||f_n-f_theta||_1<delta/12 every three-point energy remains at least delta, since its limiting lower bound is 2delta. The PSD block lemma and delta<=1 therefore give the same defect bound (P), for all sufficiently large n, uniformly in all real point locations.

Now fix n and let T tend to infinity. Wang's fixed-lambda theorem gives Q_n/N -> A_n, and the short-interval normalized span has L/N<=1+o(1). Combining (F) and (P) gives

    (1-delta/3) liminf s/N >= 2-A_n-2delta/(3R).

The left side is independent of n; taking n to infinity is legitimate and gives

    liminf s/N >= c_star(theta)
      :=c(theta)+delta(c(theta)-2/R)/(3-delta).

This is strictly greater than Wang c(theta) whenever c(theta)>0 and R>2/c(theta). Choosing R=4/c(theta) gives the explicit positive increment delta*c(theta)/[2(3-delta)]. The proof never asserts uniformity in lambda near theta or shrinks a test-function cutoff as T grows.

For distinct support cardinality D=s+r+2b, the same strong finite stability inequality yields

    Q>=3N-2D+tr Psi(G),

because the difference from the strong bound is N-s-2r>=0. Combining with (P) and the improved simple-real proportion gives the strict distinct proportion (1+c_star(theta))/2. This is a companion bound, not a separate optimization.

## Adversarial verdict and remaining gates

The final draft's shorter min-max proof of the stability lemma was independently checked. If p_1<=...<=p_m are the eigenvalues of P and n_+(C)<=d, intersecting the first i+d eigenspaces of P with a subspace on which C<=0 gives lambda_i(P+C)<=p_{i+d}. Therefore (lambda_i-2)^2>=(2-p_{i+d})_+^2, and discarding the first d terms loses at most 4d. Using (2-p)_+^2=Psi(p)-2p+3 and tr Psi(P)-tr Psi(G)=m-s cancels the dimensions exactly. The proof also works when d>=m, when the intermediate lower bound is nonpositive, and when either matrix is singular. No gap was found in this replacement of the eigenvalue-padding argument.

The numerical corollary may use a certified limiting-kernel energy threshold d in full, without halving it, provided the extra limiting argument is explicit: every delta<d survives a sufficiently close smooth approximation; take the fixed-test large-T limit first, then let delta increase to d. The resulting proportion formula is continuous for d<3. Using the unsmoothed threshold directly without either this outer limit or a smoothing reserve would leave a justification gap.

### Arithmetic implementation and adversarial certificate checks

The source audit of `code/riemann_certificates.py` found no interval-soundness defect. The separate sinc evaluator uses 96 terms; its error bound |x|^192/193! follows from the real sine Taylor formula through degree 192, including the zero even-degree coefficient, divided by x and extended continuously at zero. Arb evaluates the polynomial and error radius with outward enclosures. The derivative bound |K'|<=2pi integral|u|f(u)du<=pi theta is valid because the cosine density is nonnegative and normalized. Positive-interval guards precede lower-bound squaring. Comparing the resulting Arb interval against the threshold requires its entire lower bound to clear that threshold.

The B/E/O tree verifier reconstructs the entire square [0,R]^2. It discards a box only when the sum of its two lower coordinates is strictly greater than R, which preserves the triangle boundary. Branch nodes split a rectangle exactly; accepted leaves certify an energy lower bound on the full rectangle and hence its intersection with the domain. Missing, trailing, unknown and miscounted nodes are rejected. Hashing protects accidental tree corruption, while replay remains necessary because a maliciously altered tree can have a freshly recomputed hash.

The alternative sinc evaluator is independently derived arithmetic within a shared verifier: it shares the Lipschitz estimate, box geometry, partition decoder and python-flint/Arb implementation. It is not a wholly independent verifier or an independent arithmetic library. This distinction must remain visible in the result and manuscript.

On the final 48,761-node certificate with theta=3/4, R=21/4 and energy threshold 1/7000, eight manual adversarial mutations were rejected: false outside-root claim, false whole-square energy claim, truncated tree, appended tree data, altered node count, nonzero unresolved flag, invalid theta=1, and inflated threshold=1. The checked tree digest was `78829635026aeacd69c02213cc899b5029ef2566bbfaf1c86b757cc5f92ffe55`. The focused pytest file additionally exercises zero/removable kernel arguments, four comparisons with the direct cosine formula away from singularities, fail-closed checkpoint exhaustion and exact resume equivalence on a small domain. All 19 tests passed: 18 focused checks and one full certificate replay with the separate Taylor sinc evaluator at 256-bit precision. Ruff passed. Tests read committed-style artifacts and write temporary checkpoints only; no historical certificate was modified.

Wang's analytic transfer was also read beyond its statement, in the downloaded `wang-2609.07918v1.txt` (PDF pages 3-10). The restricted-zero identity in Lemma 2.3 uses rho-prime ->1-conj(rho-prime), which preserves the height interval and multiplicities. The contour shift for the elementary rational integral does not cross a pole: |Re(rho)-1/2|<1/2 keeps the integration line between the shifted poles. Lemma 2.4 controls the discarded zeros at both interval ends by O(x log^3 T), using only local O(log T) zero counts. Lemma 2.5 and the Montgomery--Vaughan mean-value theorem bound the prime-series error by O(x log^2 x). Since x<=T^lambda and lambda<theta, this term is smaller than H log T uniformly over that fixed support for large T. In Theorem 2.2 the substitution x=T^alpha and integration over alpha reduces the largest error to O_g(T^lambda log^2 T), while the near-origin Laplace term contributes g(0)H log T/(2pi) with O_g(H) error. The exact cancellation test Q-Q''/(4log^2 T) in Lemma 3.1 leaves the stated quadratic functional. No inconsistency was found in these source-level steps. The classical explicit formula, prime number theorem and Montgomery--Vaughan theorem are cited analytic inputs, not re-proved by this audit.

The off-line signs, inertia bound, multiplicity accounting, exact trace and exact pair-sum norm all check out. The natural concern that an off-line pair destroys positivity is resolved by the signed rank-two decomposition; all positivity occurs only at the Hilbert-Schmidt norm and simple-real Gram matrix levels.

No obstruction found in the stability transfer, explicit triple-energy bound, shifted packing, fixed-test-function limit passage or the inspected short-interval analytic proof. The proposed theorem is a strict improvement to Wang's c(theta) for each fixed theta above its positive-proportion threshold, with the corresponding distinct-zero improvement. It does not improve the threshold and does not establish a new global record above independently established Ainta/trmdy results. The remaining research gates are source-complete novelty comparison and any planned machine-checked or exact-arithmetic verification of the written formulas. The finite stability lemma itself must be attributed to Ainta; the contribution would be its direct Hilbert-space transfer and short-interval application.
