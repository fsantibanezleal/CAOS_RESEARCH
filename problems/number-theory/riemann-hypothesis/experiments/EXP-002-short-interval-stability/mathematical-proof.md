# A strict improvement of the short-interval cosine bound

Date: 2026-09-12. Status: mathematical derivation with independent adversarial
review; not an end-to-end Lean certificate. The application uses Wang's stated
unconditional short-interval pair-correlation theorem. The stable rank-trace
lemma is prior work of Ainta; the candidate contribution is its direct finite
Hilbert transfer and the ensuing short-interval strict-improvement theorem.

## Statement

Put

\[
c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2).
\]

Define \(\theta_0\) to be the unique zero of \(c\) on \((0,1)\);
numerically \(\theta_0=0.550193964744154\ldots\). Uniqueness and the sign on
either side follow from \(c'(\theta)=\tfrac12\cot^2(\theta/\sqrt2)>0\),
\(c(\theta)\to-\infty\) as \(\theta\downarrow0\), and \(c(1)>0\).

Fix \(\theta_0<\theta<1\). For every real \(R>2/c(\theta)\), define

\[
a=\theta/\sqrt2,\quad q=a\tan a,\quad S=\pi\theta R,
\quad B=q(1+S^2/a^2),
\]
\[
b=\min\left\{\frac q2,
 \frac{q^4}{4(q+S)^2(S+3q/2)}\right\},
\qquad e=2(b/B)^2,\qquad \delta=\frac12\min\{1,e\}.
\]

All these quantities are positive, and \(0<\delta\le1/2\). The argument below
gives

\[
\boxed{\liminf_{T\to\infty}
 \frac{N_0^s(T,T^\theta)}{N(T,T^\theta)}
 \ge c(\theta)+\frac{\delta\{c(\theta)-2/R\}}{3-\delta}
 >c(\theta).}
\]

Writing the displayed improved constant as \(c_*(\theta,R)\), the same proof
also gives

\[
\boxed{\liminf_{T\to\infty}
 \frac{N^d(T,T^\theta)}{N(T,T^\theta)}
 \ge\frac{1+c_*(\theta,R)}2>\frac{1+c(\theta)}2.}
\]

Here \(N(T,H)\) counts all zero copies with \(T<\gamma\le T+H\), and
\(N_0^s(T,H)\) counts simple zeros on the critical line. The explicit gain is
small; its purpose is to certify strictness without a numerical minimization.
For example, \(R=4/c(\theta)\) is an admissible fully specified choice.
The theorem does not improve the positivity threshold \(\theta_0\), does not
claim a global record, and does not establish RH. The distinct-zero companion
follows from the stronger finite stability inequality proved below.

## 1. Exact finite Hilbert construction

Let \(Z\) be a finite conjugation-invariant multiset of complex points, with
multiplicities \(m_z=m_{\bar z}\), and \(N=\sum m_z\). Sums in this section
are over distinct support points, with the displayed multiplicities. Take a
real even compactly supported \(\eta\in L^2(\mathbb R)\), normalized by
\(\int\eta^2=1\), and put

\[
f_z(u)=\eta(u)e^{-2\pi izu},\qquad K(t)=\widehat{\eta^2}(t).
\]

Use the Hilbert convention \(\langle v,w\rangle=\int\bar v w\), and write
\(|v\rangle\langle w|\) for the map \(h\mapsto v\langle w,h\rangle\).
On the finite-dimensional span \(E\) of the \(f_z\), define

\[
A=\sum_zm_z|f_z\rangle\langle f_{\bar z}|.
\]

Conjugation invariance makes \(A\) selfadjoint. Each summand has trace one
before multiplication by \(m_z\), since
\(\langle f_{\bar z},f_z\rangle=\int\eta^2=1\). Direct multiplication of
rank-one operators, evenness of \(K\), and reindexing give the exact identities

\[
\operatorname{tr}A=N,\qquad
Q:=\|A\|_{HS}^2=\operatorname{tr}A^2
 =\sum_{z,w}m_zm_wK(z-w)^2.
\]

Explicitly, the trace of the product of the \(z\) and \(w\) summands before
multiplicity factors is
\(\langle f_{\bar z},f_w\rangle\langle f_{\bar w},f_z\rangle
=K(w-z)K(z-w)=K(z-w)^2\). This also fixes the conjugation convention in the
norm calculation.

This is the square of the complex kernel, not its absolute square. The full
sum is nonnegative because it is an operator norm squared. There is no
termwise positivity assertion at nonreal arguments.

Let \(x_1<\cdots<x_s\) be the simple real points of \(Z\), \(r\) the number
of distinct multiple real points, and \(k\) the number of nonreal conjugate
pairs. Set

\[
P=\sum_{j=1}^s|f_{x_j}\rangle\langle f_{x_j}|=VV^*,\quad
G=V^*V=(K(x_i-x_j))_{i,j=1}^s,\quad C=A-P.
\]

The matrix \(G\) is positive semidefinite with diagonal one, so
\(\operatorname{tr}P=s\). For a nonreal conjugate pair put
\(g=(f_z+f_{\bar z})/2\) and \(h=(f_z-f_{\bar z})/(2i)\). Its contribution
to \(C\) is \(2m_z(|g\rangle\langle g|-|h\rangle\langle h|)\).
On the orthogonal complement of the span of the \(r\) multiple-real vectors
and the \(k\) vectors \(g\), the quadratic form of \(C\) is nonpositive.
Consequently \(n_+(C)\le r+k\), while \(N\ge s+2r+2k\).

## 2. Stable rank-trace inequality, with a self-contained spectral proof

For \(t\ge0\), define the convex nonnegative function

\[
\Psi(t)=\begin{cases}(t-1)^2,&0\le t\le2,\\2t-3,&t\ge2.\end{cases}
\]

The following is the known Ainta stability inequality in the unit-column
case needed here:

\[
\|P+C\|_{HS}^2\ge4\operatorname{tr}(P+C)-3s-4d+
 \operatorname{tr}\Psi(V^*V),\qquad n_+(C)\le d.
\]

For completeness let \(m=\dim E\) and let \(p_1\le\cdots\le p_m\) be the
eigenvalues of \(P\). If \(d<m\), the min-max principle gives
\(\lambda_i(P+C)\le p_{i+d}\) for \(1\le i\le m-d\): intersect the span
of the first \(i+d\) eigenvectors of \(P\) with a codimension-at-most-\(d\)
subspace on which \(C\le0\). The intersection has dimension at least \(i\).
Since \(0\le(2-p_j)_+^2\le4\), it follows that

\[
\operatorname{tr}(P+C-2I)^2
 \ge\sum_{j=1}^m(2-p_j)_+^2-4d.
\]

For \(d\ge m\), the right side is nonpositive, and the same inequality is
trivial. Now use
\((2-p)_+^2=\Psi(p)-2p+3\) and \(\operatorname{tr}P=s\).
The nonzero spectra of \(P=VV^*\) and \(G=V^*V\) agree, and \(\Psi(0)=1\),
so \(\operatorname{tr}\Psi(P)=\operatorname{tr}\Psi(G)+m-s\).
Expanding the preceding square proves the asserted inequality. This argument
handles singular Gram matrices and either ordering of \(m,s\).

Applying it with \(d=r+k\), and then using the multiplicity bound, gives

\[
Q\ge4N-3s-4(r+k)+D(G)\ge2N-s+D(G),\qquad
D(G)=\operatorname{tr}\Psi(G).
\]

Thus the strengthened finite multiset bound is

\[
\boxed{s\ge2N-Q+D(G).}\tag{F}
\]

If \(D_Z=s+r+2k\) is the number of distinct support points, then

\[
\{4N-3s-4(r+k)\}-\{3N-2D_Z\}=N-s-2r\ge0.
\]

The same strong inequality therefore also proves

\[
\boxed{D_Z\ge\frac{3N-Q+D(G)}2.}\tag{FD}
\]

The improvement uses the Gram matrix of actual simple real points. The
nonreal and multiple points remain in the remainder \(C\); no positivity of
their pairwise kernel interactions is needed.

## 3. Consecutive triples and the factor one third

For a positive semidefinite matrix \(M\) with diagonal one, let
\(E(M)=2\sum_{i<j}|M_{ij}|^2\). Then

\[
D(M)\ge\min\{1,E(M)\}.
\]

Indeed, if every eigenvalue is at most 2, the defect equals
\(\operatorname{tr}(M-I)^2=E(M)\). If an eigenvalue exceeds 2, its own
\(\Psi\) value exceeds 1.

Suppose a real even kernel satisfies

\[
2\{K(u)^2+K(v)^2+K(u+v)^2\}\ge\delta,\qquad
u,v\ge0,\quad u+v\le R,\quad0<\delta\le1.
\]

Let \(L=x_s-x_1\), with \(L=0\) if \(s\le1\). Among the \(s-2\)
consecutive triples, the sum of their spans is at most \(2L\). Therefore at
most \(2L/R\) have span greater than \(R\). Every remaining triple has
defect at least \(\delta\).

For each of the three residue classes of starting indices modulo 3, the
triples are disjoint principal blocks. Complete them with leftover singleton
blocks. Convex trace pinching gives \(D(G)\ge\sum D(G_{\rm block})\).
One justification is to express the pinching map as an average of unitary
conjugations and use convexity of \(M\mapsto\operatorname{tr}\Psi(M)\).
Averaging the three resulting inequalities proves

\[
\boxed{D(G)\ge\frac\delta3\left(s-2-\frac{2L}{R}\right).}\tag{T}
\]

When the right side is negative this remains true by nonnegativity. The
factor is \(1/3\), not \(1/2\). Triple overlap cannot be discarded without
this partition argument.

## 4. Cosine kernels: root obstruction and an explicit quantitative bound

For \(0<\lambda\le1\), define the normalized density

\[
f_\lambda(x)=\frac{\cos(\sqrt2x)}{\sqrt2\sin(\lambda/\sqrt2)}
 \mathbf1_{[-\lambda/2,\lambda/2]}(x),\qquad K_\lambda=\widehat f_\lambda.
\]

Put \(a=\lambda/\sqrt2\), \(q=a\tan a>0\), \(X=\pi\lambda t\). Integration
gives the entire function

\[
K_\lambda(t)=\frac{\cos X-(X/a)\cot(a)\sin X}{1-X^2/a^2}.
\]

The apparent singularities at \(X=\pm a\) are removable. In particular the
numerator equation at \(X=a\) must not be counted as a zero of the kernel.
Every actual positive root satisfies \(\tan X=q/X\). If \(X,Y,X+Y\) were
three such roots, the tangent addition formula would give
\(X^2+XY+Y^2+q^2=0\), impossible for positive \(X,Y,q\). The exceptional
case where the tangent denominator vanishes cannot be a root either.
At a zero gap \(K_\lambda(0)=1\). This already proves a positive compact
three-point energy minimum.

An explicit bound follows without solving for those roots. Put
\(A_X=q\cos X-X\sin X\). For \(Z=X+Y\), elementary angle addition gives

\[
(X^2+XY+Y^2+q^2)\sin X\sin Y
 =A_XA_Y-XA_X\sin Y-YA_Y\sin X-qA_Z.\tag{A}
\]

Fix \(X,Y\ge0\), \(X+Y\le S\), and let
\(h=\max(|A_X|,|A_Y|,|A_Z|)\). If \(h\le q/2\), then

\[
q\le q|\cos X|+q|\sin X|
 \le h+(q+X)|\sin X|,
\]

and similarly for \(Y\). Hence
\(|\sin X|,|\sin Y|\ge q/[2(q+S)]\). Taking absolute values in (A) yields

\[
\frac{q^4}{4(q+S)^2}\le h^2+(S+q)h\le(S+3q/2)h.
\]

If \(h>q/2\), the alternative lower bound is immediate. In either case
\(h\ge b\), with \(b\) as in the theorem. Moreover
\(A_X=q(1-X^2/a^2)K_\lambda(X/(\pi\lambda))\), including the removable
points by continuity. Consequently

\[
\max(|K_\lambda(u)|,|K_\lambda(v)|,|K_\lambda(u+v)|)\ge b/B,
\]

where \(S=\pi\lambda R\), \(B=q(1+S^2/a^2)\). Therefore the triple energy
is at least \(e=2(b/B)^2>0\). This bound is deliberately conservative.

## 5. Analytic input, smoothing, and the order of limits

Wang, arXiv:2609.07918v1, Theorem 2.2 and Lemma 3.1, give the following
unconditional interface. Fix \(0<\lambda<\theta<1\), \(H=T^\theta\), and
a real even smooth normalized density \(f=\eta^2\) with
\(\eta\in C_c^\infty((-\lambda/2,\lambda/2))\). For

\[
Z_T=\{i(\rho-1/2)\log T/(2\pi):T<\operatorname{Im}\rho\le T+H\},
\]

the full pair sum from (F) satisfies

\[
\frac QN\longrightarrow\mathcal C(f),\qquad
\mathcal C(f)=\int f^2+\iint |x-y|f(x)f(y)\,dx\,dy.
\]

The rational pair weight is removed by applying the fixed-test theorem
separately to \(f*f\) and \((f*f)''\), and combining the results with the
coefficient \(-1/[4(\log T)^2]\). This is valid with fixed \(f\), despite
the combining coefficient depending on \(T\). The theorem's normalized error
tends to zero because \(\lambda<\theta\).

For the nonsmooth limiting density, a direct calculation gives

\[
\mathcal C(f_\lambda)=\frac\lambda2+
 \frac1{\sqrt2}\cot(\lambda/\sqrt2)=2-c(\lambda).
\]

To approximate it, choose an even smooth cutoff \(\chi\) supported strictly
inside \((-\lambda/2,\lambda/2)\), approaching one on the interior, and
normalize \(\eta=\chi\sqrt{f_\lambda}/\|\chi\sqrt{f_\lambda}\|_2\).
Then \(f=\eta^2\to f_\lambda\) in both \(L^1\) and \(L^2\), so
\(\mathcal C(f)\to\mathcal C(f_\lambda)\). As \(\lambda\uparrow\theta\),
the same convergences hold from \(f_\lambda\) to \(f_\theta\).

The kernel error obeys
\(\sup_{t\in\mathbb R}|\widehat f(t)-K_\theta(t)|\le\|f-f_\theta\|_1\).
All real kernel values have absolute value at most one. Thus the three-point
energy error is at most \(12\|f-f_\theta\|_1\). The explicit gap \(e\) for
\(K_\theta\) persists with lower bound \(\delta=\tfrac12\min(1,e)\) for
all sufficiently close smooth approximations with \(\lambda<\theta\).

For each such fixed approximation, take \(T\to\infty\) first. Neither
\(\lambda\) nor the smoothing scale is allowed to depend on \(T\). Only
afterwards take a sequence of closer approximations. No uniform error in
\(\lambda\uparrow\theta\) is being asserted.

## 6. Completing the deduction

The functional equation makes \(Z_T\) conjugation-invariant. Its simple real
points are exactly the simple critical zeros. Their total normalized span is
at most \(X_T=H\log T/(2\pi)\). Riemann-von Mangoldt in this interval gives
\(N=X_T+O(H+\log T)\), hence \(X_T/N\to1\).

Combine (F) and (T), replacing the actual span by \(X_T\), to obtain

\[
\left(1-\frac\delta3\right)\frac sN
 \ge2-\frac QN-\frac{2\delta}{3N}-\frac{2\delta X_T}{3RN}.
\]

For a fixed smooth approximation, take the lower limit and then let the
approximations approach \(f_\theta\) as described above. It follows that

\[
\liminf\frac sN\ge
 \frac{c(\theta)-2\delta/(3R)}{1-\delta/3}
 =c(\theta)+\frac{\delta\{c(\theta)-2/R\}}{3-\delta}.
\]

The final term is positive by the choice of \(R\). This proves the
simple-critical-zero statement.

For the distinct-zero statement, use (FD) and (T). For each fixed smooth
approximation, put \(c_f=2-\mathcal C(f)\) and
\(c_{f,*}=(c_f-2\delta/(3R))/(1-\delta/3)\). The preceding finite inequalities
give \(\liminf s/N\ge c_{f,*}\). They then give

\[
\liminf\frac{D_Z}{N}
 \ge\frac{1+c_f}2+\frac\delta6(c_{f,*}-2/R)
 =\frac{1+c_{f,*}}2.
\]

The equality uses \(c_{f,*}-c_f=\delta(c_{f,*}-2/R)/3\).
Letting the fixed approximations approach \(f_\theta\) proves the companion.
Thus both improved constants follow directly from the signed finite operator
inequality with all multiplicities retained.

## 7. Using a stronger certified three-point energy constant

Suppose an independent certificate proves, for the limiting cosine kernel,

\[
2\{K_\theta(u)^2+K_\theta(v)^2+K_\theta(u+v)^2\}\ge d,
\quad u,v\ge0,\quad u+v\le R,\quad0<d\le1.
\]

The full certified \(d\) may replace \(\delta\) in the final constants:

\[
c_{*,d}=\frac{c(\theta)-2d/(3R)}{1-d/3},\qquad
\liminf N_0^s/N\ge c_{*,d},\quad
\liminf N^d/N\ge(1+c_{*,d})/2.
\]

To justify this without losing the smoothing margin, first fix any
\(0<\delta<d\). Choose \(\lambda<\theta\) and the smooth density sufficiently
close that the energy loss is smaller than \(d-\delta\). Apply the fixed-test
argument, take \(T\to\infty\), and then take the approximation limit exactly
as above. This gives the stated formulas with \(\delta\) for every
\(\delta<d\). Finally let \(\delta\uparrow d\) in those scalar bounds.
The limit is continuous because \(d\le1<3\). No changing test function within
the \(T\)-limit is involved. An implementation using the full certified energy
threshold must use this corollary; the earlier explicit formula instead keeps
half the analytic gap as an immediate fixed reserve.

## Attribution, novelty boundary, and limitations

- [Lamzouri, arXiv:2609.02882v2](https://arxiv.org/html/2609.02882v2): finite
  conjugation-invariant kernel framework, ordinary rank-trace bound, and
  smooth deweighting. Proposition 2.1 and Lemmas 3.1–3.2.
- [Wang, arXiv:2609.07918v1](https://arxiv.org/html/2609.07918v1): the
  short-interval analytic input and the baseline \(c(\theta)\). Theorems 1.1,
  2.2; Lemma 3.1.
- [Ainta stability manuscript](https://github.com/ainta/zeta-simple-zeros/blob/main/paper/riemann.tex):
  stable rank-trace inequality and Gram-defect/pinching method. These are
  prior work; they are not claimed as new here.
- [trmdy contributor manuscript](https://github.com/trmdy/zeta-simple-zeros-673137/blob/main/paper/main.tex):
  existing global window/block refinements demonstrate that improving the
  global 0.6725007 constant is not itself a new target.

The candidate new statement is strict improvement of Wang's entire positive
short-interval cosine curve by direct finite-Hilbert stability and a
three-point root obstruction. It uses no new prime-sum estimate. Live searches
on 2026-09-12 for `zeta "short intervals" "stability" "2026"`,
`"2609.07918" improvement`, `"simple zeros" "short intervals" "Gram"`,
and `"short-interval" "Ainta"` did not identify this theorem. That search is
not a guarantee of priority or independent acceptance.

The proof provides no explicit height threshold, no uniformity as
\(\theta\downarrow\theta_0\), and no claim to eliminate every exceptional
off-line zero. The finite and analytic arguments require independent review;
verification of numerical constants is separate from that proof review.
