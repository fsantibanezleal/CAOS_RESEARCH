# Odd-frame pressure refinement of the short-interval cosine bound

Date: 2026-09-12. Declaration: `8ed806d`, committed before computation.
Status: complete paper derivation; quantitative experiment outcomes are recorded
separately in the experiment verdict and artifacts. This document does not constitute
an end-to-end formal proof.

The contribution considered here is a stronger short-interval consequence of known
stability and pressure methods, using an alternating cover by triples and the existing
EXP-002 certificate. The spectral defect, finite Hilbert representation, cosine
optimization, three-point root obstruction, and general pressure-frame framework
are attributed prior work. The [prior-art dossier](../../context/2026-09-12-pressure-frame-prior-art.md)
records the precise source and priority boundaries.

## 1. The theorem and counting conventions

Write

$$
c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2).
$$

Let $\theta_0$ be its unique zero on $(0,1)$. Indeed
$c'(\theta)=\tfrac12\cot^2(\theta/\sqrt2)>0$, $c(\theta)\to-\infty$ at
zero, and $c(1)>0$. Throughout, $\theta_0<\theta<1$ is fixed. Put

$$
f_\theta(t)=\frac{\cos(\sqrt2t)}{\sqrt2\sin(\theta/\sqrt2)}
\mathbf1_{[-\theta/2,\theta/2]}(t),\qquad
K_\theta(x)=\int f_\theta(t)e^{-2\pi ixt}\,dt.
$$

This is a nonnegative even density of integral one. Its real-frequency kernel is
real and even, with $K_\theta(0)=1$ and $|K_\theta(x)|\le1$.

**Pressure theorem.** Suppose positive real numbers $p,\epsilon$ satisfy

$$
2\{K_\theta(u)^2+K_\theta(v)^2+K_\theta(u+v)^2\}
+p(u+v)\ge\epsilon\qquad(u,v\ge0).
\tag{1}
$$

Let $k\ge1$ be a fixed integer with $k\epsilon\le1$, and set

$$
M=2k+1,\qquad
c_{\mathrm{odd}}(\theta;\epsilon,p,k)
=\frac{M c(\theta)-2kp}{M-k\epsilon}
=c(\theta)+\frac{k\{\epsilon c(\theta)-2p\}}{M-k\epsilon}.
\tag{2}
$$

Then

$$
\liminf_{T\to\infty}\frac{N_0^s(T,T^\theta)}{N(T,T^\theta)}
\ge c_{\mathrm{odd}},\qquad
\liminf_{T\to\infty}\frac{N^d(T,T^\theta)}{N(T,T^\theta)}
\ge\frac{1+c_{\mathrm{odd}}}{2}.
\tag{3}
$$

Here $N(T,H)$ counts all nontrivial zero copies in $(T,T+H]$, including
multiplicity; $N_0^s$ counts simple zeros on the critical line; and $N^d$ counts
each distinct complex zero once. The new term in (2) is positive when
$\epsilon c(\theta)>2p$. The denominator is positive since $M-k\epsilon\ge M-1$.

Equation (3) is an asymptotic statement for each fixed parameter choice. For every
positive tolerance the claimed constant minus that tolerance holds at all sufficiently
large heights. It is not a finite-height guarantee at the exact limiting constant.

## 2. Exact finite Hilbert operator, including nonreal points

This section rechecks the [EXP-002 finite argument](../EXP-002-short-interval-stability/mathematical-proof.md).
Let $Z\subset\mathbb C$ be a finite conjugation-invariant support with positive
integer multiplicities $m_z=m_{\bar z}$, and let $N=\sum_zm_z$. Let $\eta$ be
real, even, compactly supported, and normalized by $\int\eta^2=1$. Write

$$
v_z(t)=\eta(t)e^{-2\pi izt},\qquad K=\widehat{\eta^2},\qquad
A=\sum_{z\in Z}m_z|v_z\rangle\langle v_{\bar z}|.
\tag{4}
$$

Work in the finite-dimensional span $\mathcal H$ of these vectors. Use the convention
$\langle v,w\rangle=\int\bar v w$, linear in the second slot, and
$|v\rangle\langle w|:h\mapsto v\langle w,h\rangle$.

Conjugation invariance makes $A$ selfadjoint. Each rank-one term has trace
$\langle v_{\bar z},v_z\rangle=1$, so $\operatorname{tr}A=N$. Direct multiplication
also gives

$$
Q:=\|A\|_{\mathrm{HS}}^2=\operatorname{tr}A^2
=\sum_{z,w\in Z}m_zm_wK(z-w)^2.
\tag{5}
$$

In detail, the trace of the product of the $z$ and $w$ rank-one factors is
$\langle v_{\bar z},v_w\rangle\langle v_{\bar w},v_z\rangle
=K(w-z)K(z-w)=K(z-w)^2$, because $K$ is even. Equation (5) is an ordinary
complex square, not an absolute square. Individual summands need not be positive
or real. Their full sum is nonnegative by the operator identity.

Let $x_1<\cdots<x_s$ be the simple real support points, $r$ the number of
multiple real support points, and $b$ the number of nonreal conjugate pairs. Set

$$
P=\sum_{j=1}^s|v_{x_j}\rangle\langle v_{x_j}|=VV^*,\qquad
G=V^*V=(K(x_i-x_j))_{i,j=1}^s,\qquad C=A-P.
$$

The matrix $G$ is positive semidefinite with diagonal one. Each multiple real
point contributes at most one positive direction to $C$. For a conjugate pair define
$g=(v_z+v_{\bar z})/2$ and $h=(v_z-v_{\bar z})/(2i)$. Its contribution is

$$
m_z\{|v_z\rangle\langle v_{\bar z}|+|v_{\bar z}\rangle\langle v_z|\}
=2m_z\{|g\rangle\langle g|-|h\rangle\langle h|\}.
$$

On the orthogonal complement of the span of the $r$ multiple-real vectors and the
$b$ vectors $g$, the quadratic form of $C$ is nonpositive. Thus
$n_+(C)\le r+b$. Counting multiplicities gives $N\ge s+2r+2b$.

Define the convex nonnegative function

$$
\Psi(t)=\begin{cases}(t-1)^2,&0\le t\le2,\\2t-3,&t\ge2,\end{cases}
\qquad D(G)=\operatorname{tr}\Psi(G).
$$

The following is the unit-column case of the known
[Ainta stability lemma](https://github.com/ainta/zeta-simple-zeros/blob/040c5e899e658aed7b56a2a87f501798fe10761d/paper/riemann.tex):

$$
\|P+C\|_{\mathrm{HS}}^2
\ge4\operatorname{tr}(P+C)-3s-4d+D(G),\qquad n_+(C)\le d.
\tag{6}
$$

For completeness, put $m=\dim\mathcal H$, and order the eigenvalues of $P$ as
$0\le p_1\le\cdots\le p_m$. The min-max principle gives
$\lambda_i(P+C)\le p_{i+d}$ for $1\le i\le m-d$ when $d<m$:
intersect the first $i+d$ eigenspaces of $P$ with a codimension-at-most-$d$
subspace on which $C\le0$. The intersection has dimension at least $i$.
Consequently

$$
\operatorname{tr}(P+C-2I)^2
\ge\sum_{j=1}^m(2-p_j)_+^2-4d.
$$

For $d\ge m$ the right side is nonpositive, so this remains valid. Now
$(2-p)_+^2=\Psi(p)-2p+3$, $\operatorname{tr}P=s$, and
$\operatorname{tr}\Psi(P)=D(G)+m-s$. The last identity follows because $VV^*$
and $V^*V$ have the same nonzero eigenvalues and $\Psi(0)=1$. Expanding the
square proves (6), including singular matrices and either ordering of $m,s$.

Applying (6) with $d=r+b$ yields

$$
Q\ge4N-3s-4r-4b+D(G)\ge2N-s+D(G).
$$

The number of distinct support points is $D_Z=s+r+2b$, and

$$
(4N-3s-4r-4b)-(3N-2D_Z)=N-s-2r\ge0.
$$

We therefore have both exact finite inequalities

$$
\boxed{s\ge2N-Q+D(G)},\qquad
\boxed{2D_Z\ge3N-Q+D(G)}.
\tag{7}
$$

All nonreal and multiple points are retained in $N,Q,C$. No pointwise positivity
at nonreal kernel arguments, Gabor grid, or asymptotic Hilbert approximation was used.

## 3. Spectral energy and disjoint pinching

For any positive semidefinite unit-diagonal matrix $B$, put

$$E(B)=\operatorname{tr}(B-I)^2=2\sum_{i<j}|B_{ij}|^2.$$

If every eigenvalue is at most two, then $D(B)=E(B)$. If an eigenvalue exceeds
two, its own $\Psi$ value exceeds one. Thus the known elementary bound is

$$D(B)\ge\min\{1,E(B)\}.\tag{8}$$

For $P_0\ge0$ and $0<A_0\le1$, (8) immediately implies

$$E(B)+P_0\ge A_0\quad\Longrightarrow\quad D(B)+P_0\ge A_0.\tag{9}$$

When $E(B)\le1$ use $D(B)\ge E(B)$; otherwise use $D(B)\ge1\ge A_0$.

For a disjoint partition of the indices into principal blocks $B_j$, convex trace
pinching gives

$$D(G)\ge\sum_jD(B_j).\tag{10}$$

One proof expresses the pinching map as an average of diagonal-unitary conjugations
and uses convexity and unitary invariance of $G\mapsto\operatorname{tr}\Psi(G)$.
Leftover singleton blocks contribute exactly $\Psi(1)=0$. Equations (8)-(10) are
known stability tools; their use here does not claim a new spectrum-energy envelope.

## 4. Pair-disjoint triples inside an odd frame

This section is finite and applies to any real even positive-type kernel $K$ with
$K(0)=1$ satisfying the pressure inequality (1). Take $M=2k+1$ ordered points
$y_1\le\cdots\le y_M$ and their Gram matrix $G_F$.

For $j=1,\ldots,k$, use the triple $(y_{2j-1},y_{2j},y_{2j+1})$. Two adjacent
triples share one vertex; no two selected triples contain the same unordered pair.
Since every real-pair squared kernel term is nonnegative,

$$
E(G_F)\ge\sum_{j=1}^k E_3(y_{2j}-y_{2j-1},y_{2j+1}-y_{2j}).
$$

Their spans telescope exactly:

$$\sum_{j=1}^k(y_{2j+1}-y_{2j-1})=y_M-y_1=:L_F.$$

Adding the $k$ pressure inequalities and using $k\epsilon\le1$ in (9) proves

$$
E(G_F)+pL_F\ge k\epsilon,\qquad
\boxed{D(G_F)+pL_F\ge k\epsilon}.
\tag{11}
$$

This argument adds pair energies inside one frame. It does not add the spectral
defects of overlapping triples.

Now take $s$ ordered points $x_1<\cdots<x_s$, with total span
$L=x_s-x_1$ when $s\ge2$ and $L=0$ otherwise. For every residue class of frame
starts modulo $M$, use all complete length-$M$ frames in that class, and complete
the partition with singleton blocks. The frames within one class are disjoint.

Across the $M$ classes, every possible frame start $a\in\{1,\ldots,s-M+1\}$
occurs once. Thus there are $(s-M+1)_+$ complete frames. Also

$$
\sum_{a=1}^{s-M+1}(x_{a+M-1}-x_a)\le(M-1)L\qquad(s\ge M).
\tag{12}
$$

To verify (12), expand each span into adjacent gaps. Each gap is included at most
$M-1$ times, since a frame of $M$ points contains $M-1$ gaps.

Apply (10) and (11) to each partition and average. With

$$\alpha=\frac{k\epsilon}{M},\qquad\beta=\frac{(M-1)p}{M}=\frac{2kp}{M},$$

the result is

$$
\boxed{D(G)\ge\alpha(s-M+1)-\beta L}.
\tag{13}
$$

For $s<M$, the right side is nonpositive and (13) follows directly from $D(G)\ge0$.
For $s\ge M$, the exact preceding inequality uses $(s-M+1)_+$ and (12).
The boundary cost $\alpha(M-1)$ is fixed independently of height.

## 5. Wang's fixed-test input and the distinct companion

Use [Wang, arXiv:2609.07918v1, Theorem 2.2 and Lemma 3.1](https://arxiv.org/pdf/2609.07918v1),
with the detailed verification in the [transfer dossier](../../context/2026-09-12-wang-transfer-audit.md).
Fix $0<\lambda<\theta<1$, $H=T^\theta$, and a real even
$\eta\in C_c^\infty((-\lambda/2,\lambda/2))$ with $\int\eta^2=1$. Put $f=\eta^2$.

For the zero multiset

$$z_\rho=\frac{i(\rho-1/2)\log T}{2\pi},\qquad T<\operatorname{Im}\rho\le T+H,$$

the functional equation preserves multiplicity and sends $z_\rho$ to $\bar z_\rho$.
Its simple real points are precisely the simple critical zeros. Their available
normalized span satisfies

$$L\le X_T=\frac{H\log T}{2\pi},\qquad N=X_T+O(H+\log T),\qquad X_T/N\to1.$$

The ordinary complex-square pair sum in (5), for this same $f$, obeys

$$
\frac QN\longrightarrow\mathcal C(f),\qquad
\mathcal C(f)=\int f^2+\iint|u-v|f(u)f(v)\,du\,dv.
\tag{14}
$$

The normalized error is $O_f(1/\log T+T^{\lambda-\theta}\log T)=o(1)$.
The pair weight is removed exactly using the two fixed tests $q=f*f$ and $q''$.
At $z=i(\rho-\rho')\log T/(2\pi)$,

$$
\left(\widehat q(z)-\frac{\widehat{q''}(z)}{4\log^2 T}\right)
\frac4{4-(\rho-\rho')^2}=K(z)^2.
$$

The coefficient depends on $T$, but the tests do not. This explains both the
complex-square convention and the strict support condition $\lambda<\theta$.

For the moment suppose the smooth kernel satisfies (1) with parameters $p,\epsilon$.
Set $c_f=2-\mathcal C(f)$ and $b_f=(c_f-\beta)/(1-\alpha)$. Equations (7),
(13), and $L\le X_T$ imply

$$
(1-\alpha)\frac sN
\ge2-\frac QN-\beta\frac{X_T}{N}-\frac{\alpha(M-1)}N,
$$

so $\liminf s/N\ge b_f$. For distinct points the second part of (7) gives

$$
2\liminf\frac{D_Z}{N}
\ge1+c_f+\alpha b_f-\beta=1+b_f.
\tag{15}
$$

The equality follows from $(1-\alpha)b_f=c_f-\beta$. In particular the distinct
improvement follows from the stronger finite stability inequality. It does not follow
from a generally valid identity $D_Z\ge(N+s)/2$, which would be false for high
multiplicities.

## 6. Smoothing the cosine profile, including the cap endpoint

The limiting cosine density has

$$\mathcal C(f_\theta)=\frac\theta2+\frac1{\sqrt2}\cot(\theta/\sqrt2)=2-c(\theta).$$

It is not smooth at its support endpoints. Choose $\lambda_n<\theta$ tending to
$\theta$, and even smooth cutoffs strictly inside each interval
$(-\lambda_n/2,\lambda_n/2)$. Multiplying $\sqrt{f_{\lambda_n}}$ by the cutoffs
and normalizing in $L^2$ gives smooth $\eta_n$ for which $f_n=\eta_n^2\to f_\theta$
in $L^1$ and $L^2$. Hence $\mathcal C(f_n)\to2-c(\theta)$.

For all real $x$,

$$|\widehat f_n(x)-K_\theta(x)|\le\|f_n-f_\theta\|_1,$$

and all these normalized real kernel values have absolute value at most one. Their
three-point energies therefore differ by at most $12\|f_n-f_\theta\|_1$, uniformly
for all real nonnegative gaps.

Fix any $0<\epsilon'<\epsilon$. For all sufficiently large $n$, (1) holds for
$\widehat f_n$ with the same $p$ and with $\epsilon'$ in place of $\epsilon$.
Keep $k$ fixed, so $k\epsilon'<1$ even when $k\epsilon=1$. For each individual
$n$, apply the preceding section and first take $T\to\infty$ with $f_n,\lambda_n$
fixed. Next take $n\to\infty$. Finally let $\epsilon'\uparrow\epsilon$.
The scalar bounds are continuous since $M-k\epsilon\ge M-1>0$. This proves (3).

One may instead preserve the pressure inequality on the fixed triangle
$u+v\le\epsilon/p$ and use pressure alone outside it. The global uniform kernel
estimate above is stronger and gives the same conclusion. Neither proof requires a
smoothing scale or support parameter varying with $T$.

## 7. Reusing a compact certificate and strengthening the entire curve

Suppose $E_3(u,v)\ge d>0$ whenever $u,v\ge0$ and $u+v\le R$. Since energy is
nonnegative everywhere,

$$E_3(u,v)+(d/R)(u+v)\ge d\qquad(u,v\ge0).$$

Apply the pressure theorem with $\epsilon=d$, $p=d/R$, and $kd\le1$. It gives

$$
c_A=c(\theta)+\frac{kd}{2k+1-kd}\{c(\theta)-2/R\}.
\tag{16}
$$

For $R>2/c(\theta)$ and $k>1$, (16) is strictly stronger than the EXP-002
bound using the same $R,d$, because

$$
\frac{kd}{2k+1-kd}-\frac d{3-d}
=\frac{d(k-1)}{(2k+1-kd)(3-d)}>0.
\tag{17}
$$

This applies to the complete positive curve, not just to a numerical parameter.
Here is an explicit available $d$ from the EXP-002 analytic proof. Put

$$
a=\theta/\sqrt2,\quad q=a\tan a,\quad S=\pi\theta R,\quad B=q(1+S^2/a^2),
$$
$$
b=\min\left\{\frac q2,\frac{q^4}{4(q+S)^2(S+3q/2)}\right\},
\qquad d=(b/B)^2.
\tag{18}
$$

These are positive and $d<1/4$, so $k=2$ is always admissible. Choosing, for
example, $R=4/c(\theta)$ gives a completely specified strict whole-curve refinement.

To recall why (18) is rigorous, write $X=\pi\theta u$ and
$A_X=q\cos X-X\sin X$. The kernel identity

$$A_X=q(1-X^2/a^2)K_\theta(X/(\pi\theta))$$

holds by continuity even at the removable denominator points $X=\pm a$.
For $X,Y\ge0$, $Z=X+Y\le S$, angle addition gives

$$
(X^2+XY+Y^2+q^2)\sin X\sin Y
=A_XA_Y-XA_X\sin Y-YA_Y\sin X-qA_Z.
$$

If $h=\max(|A_X|,|A_Y|,|A_Z|)\le q/2$, then
$|\sin X|,|\sin Y|\ge q/[2(q+S)]$. Taking absolute values in the identity yields
$q^4/[4(q+S)^2]\le h^2+(S+q)h\le(S+3q/2)h$. Otherwise $h>q/2$ already.
Thus $h\ge b$, while $|A_X|,|A_Y|,|A_Z|$ are bounded by $B$ times the
corresponding absolute kernel values. It follows that $E_3\ge2(b/B)^2=2d$.
The smaller $d$ in (18) matches the reserve used in EXP-002, so the comparison in
(17) genuinely uses its same analytic input. The root obstruction itself is prior
work; the explicit EXP-002 lower bound is reused here.

For its stronger certified example, EXP-002 proves $d=1/7000$ for
$\theta=3/4$ and $R=21/4$. With $k=7000$, $M=14001$, and $kd=1$, (16) becomes

$$
c_A=c(3/4)+\frac{c(3/4)-8/21}{14000},\qquad
\text{distinct companion}=\frac{1+c_A}{2}.
\tag{19}
$$

The gain ratio over the EXP-002 gain is exactly

$$\frac{d/2}{d/(3-d)}=\frac{3-d}{2}=\frac{20999}{14000}>1.$$

Equation (19) is an exact consequence of the earlier finite certificate and the
present paper theorem. Decimal enclosures and byte-verified replay belong to the
new experiment artifacts. No new geometric optimization is needed for this result.

## 8. New two-variable pressure certificates and the declared target

For positive rational $p,\epsilon$, pressure alone proves (1) when
$u+v\ge R_{\mathrm{cut}}:=\epsilon/p$. A new certificate therefore need only
cover the closed triangle $u,v\ge0$, $u+v\le R_{\mathrm{cut}}$. The radius is
derived from the same exact $p,\epsilon$ used in the theorem.

The declared Stage B restricts $R_{\mathrm{cut}}\le12$, $\epsilon\le1/2$, and
$k=\lfloor1/\epsilon\rfloor\ge2$. This choice maximizes the unit-cap family for
fixed $p,\epsilon$ with positive gain: writing $A=\epsilon c-2p>0$,
$g_k=kA/\{(2-\epsilon)k+1\}$ has

$$g_{k+1}-g_k=\frac{A}{\{(2-\epsilon)(k+1)+1\}\{(2-\epsilon)k+1\}}>0.$$

The frozen target compares the gains above the same baseline:

$$
\frac{k\{\epsilon c(3/4)-2p\}}{2k+1-k\epsilon}
>\frac54\frac{c(3/4)-8/21}{14000}.
\tag{20}
$$

A candidate meeting (20) numerically is not a proof of its global pressure inequality.
An exhaustive interval certificate and the stipulated independent evaluator replay
must establish (1). Conversely a valid certificate below the declared improvement
target remains a finite theorem but does not confirm Stage B's target. The experiment
verdict must retain these distinct outcomes.

## 9. Attribution and limits

The exact finite operator follows [Lamzouri](https://arxiv.org/abs/2609.02882v2),
with stability supplied by [Ainta](https://github.com/ainta/zeta-simple-zeros/tree/040c5e899e658aed7b56a2a87f501798fe10761d).
The short-interval arithmetic input and optimized cosine baseline are
[Wang's](https://arxiv.org/abs/2609.07918v1). Window pressure, larger frames,
nonuniform pair capacities, and spectral envelopes are developed in
[trmdy](https://github.com/trmdy/zeta-simple-zeros-673137/tree/1610b97b7895ff34982260f8dcaf04a0f7b82cf7),
[tawanerguo](https://github.com/tawanerguo-cn/zeta-simple-zeros/tree/45149f6d403059a71be73c5e3f884cee7cd62b20),
and [Yuhang Shi](https://github.com/yuhangshi888/zeta-simple-zeros-673316977/tree/1aeda8e9f0678166a824c75313a813b09eb478cd).

The alternating schedule is a simple choice within this established global finite
framework. The scoped candidate contribution is its stronger short-interval consequence,
the full proof with lawful limits and distinct companion, and quantitative certificate
reuse or improvement. The completed source sweep located no identical short-interval
result, but does not guarantee priority against unindexed or concurrent work.

The argument does not improve $\theta_0$, provide an effective height threshold,
assert uniformity as $\theta\downarrow\theta_0$, establish a global record, or solve
RH. It supplies no new prime-correlation estimate. Independent paper review, numerical
certification, formal verification, publication, and community acceptance are separate
forms of evidence.
