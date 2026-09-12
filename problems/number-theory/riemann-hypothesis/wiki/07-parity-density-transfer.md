# 7. Parity density transfer across the cosine positivity threshold

Date: 2026-09-12. Declaration: `e03413b2301bf45ca68ff6e945f25add9a1c3a89`, committed and pushed before implementation or computation. Status: complete paper derivation; this document contains no new numerical experiment result. The accompanying verdict and independent audit determine the experiment's validation status.

The finite spectral mechanism is inherited from the existing stability method. The analytic inputs are Wang's short-interval pair theorem and a classical Selberg odd-zero density, as recorded in the [primary-source dossier](../context/2026-09-12-critical-mass-and-multiplicity-route.md). The contribution considered here is the connection between their multiplicity information, yielding a qualitative extension of the interval range. No new global record, explicit numerical exponent, or RH proof is claimed.

## 1. Statement

For $0<\theta<1$, define

$$
c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2).
\tag{1}
$$

Let $\theta_0$ be the unique zero of $c$ on $(0,1)$ and put $\alpha=51/100$.
For $I=(T,T+H]$, let $N(T,H)$ count all nontrivial zeta-zero copies in $I$;
$S(T,H)$ count simple critical zeros; $O(T,H)$ count distinct critical zeros of
odd multiplicity; and $Z(T,H)$ count distinct complex zeros. An off-critical
conjugate pair in the transformed coordinates consists of two different complex
zeros, even when their ordinates agree.

**Theorem.** There exists a fixed constant $\kappa>0$ such that, for every fixed
$\theta\in(\alpha,1)$,

$$
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{0,c(\theta),\frac{c(\theta)+2\kappa}{3}\right\},
\tag{2}
$$

$$
\liminf_{T\to\infty}\frac{Z(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{\kappa,\frac{1+c(\theta)}2,
\frac{3+2c(\theta)+\kappa}{6}\right\}.
\tag{3}
$$

In particular, set

$$
\delta=\min\left\{\frac{\theta_0-\alpha}{2},\frac\kappa4\right\},
\qquad\theta_1=\theta_0-\delta.
\tag{4}
$$

Then $\alpha<\theta_1<\theta_0$ and every fixed $\theta\in[\theta_1,1)$ has

$$\liminf_{T\to\infty}S(T,T^\theta)/N(T,T^\theta)\ge\kappa/3>0.\tag{5}$$

There is also a simultaneous distinct-zero consequence. With

$$
\delta_{\mathrm{half}}=\min\left\{\frac{\theta_0-\alpha}{2},\frac\kappa{16}\right\},
\qquad\theta_{\mathrm{half}}=\theta_0-\delta_{\mathrm{half}},
\tag{6}
$$

every fixed $\theta\in[\theta_{\mathrm{half}},1)$ satisfies

$$\liminf_{T\to\infty}Z(T,T^\theta)/N(T,T^\theta)\ge\frac12+\frac\kappa{12}.\tag{7}$$

The same $\kappa$ works for all fixed exponents in the stated range. Eventual
heights may depend on the exponent and on the tolerance in the liminf statement.
The theorem gives no numerical value of $\kappa$, $\theta_1$, or the starting
height. The familiar decimal $\theta_0\approx0.550193964744154\ldots$ is attributed to
[Wang's Theorem 1.1](https://arxiv.org/abs/2609.07918v1); the proof below uses its
exact definition and elementary comparisons rather than that decimal.

## 2. Exact finite Hilbert operator

Let $\mathcal Z\subset\mathbb C$ be a finite conjugation-invariant support with
positive integer multiplicities $m_z=m_{\bar z}$. Let $\eta$ be real, even,
compactly supported and nonzero, with $\int\eta^2=1$. Put $f=\eta^2$ and use
the Fourier convention

$$K(z)=\widehat f(z)=\int_{\mathbb R}f(t)e^{-2\pi izt}\,dt.$$

On the finite-dimensional span of
$v_z(t)=\eta(t)e^{-2\pi izt}$, define

$$A=\sum_{z\in\mathcal Z}m_z|v_z\rangle\langle v_{\bar z}|.$$

Use $\langle v,w\rangle=\int\bar v w$, linear in the second argument. Thus
$|v\rangle\langle w|$ maps $h$ to $v\langle w,h\rangle$.
Conjugation invariance implies $A=A^*$. Moreover

$$\langle v_{\bar z},v_z\rangle=1,\qquad\operatorname{tr}A=N:=\sum_zm_z.$$

Multiplication of the rank-one factors gives

$$
\operatorname{tr}\bigl(|v_z\rangle\langle v_{\bar z}|
|v_w\rangle\langle v_{\bar w}|\bigr)
=K(w-z)K(z-w)=K(z-w)^2,
$$

because $K$ is even. Hence the exact pair quantity is

$$
Q=\operatorname{tr}A^2=\|A\|_{\rm HS}^2
=\sum_{z,w\in\mathcal Z}m_zm_wK(z-w)^2.
\tag{8}
$$

These are complex squares, not squared moduli. Individual nonreal terms may
have either sign or may be complex; the full sum is real and nonnegative by (8).

Let $s$ count simple real support points, $r$ count multiple real support points,
and $b$ count nonreal conjugate pairs. Extract the simple real part

$$P=\sum_{j=1}^s|v_{x_j}\rangle\langle v_{x_j}|=VV^*,\qquad C=A-P.$$

The Gram matrix $G=V^*V$ is positive semidefinite with diagonal one. Each multiple
real point contributes at most one positive direction to $C$. For a nonreal pair,
put $g=(v_z+v_{\bar z})/2$ and $h=(v_z-v_{\bar z})/(2i)$. Its contribution equals

$$
2m_z\bigl(|g\rangle\langle g|-|h\rangle\langle h|\bigr).
$$

On the orthogonal complement of the span of all $r$ multiple-real vectors and
the $b$ vectors $g$, the form of $C$ is nonpositive. Therefore $n_+(C)\le r+b$.

### 2.1 Attributed stability lemma, with the dimension bookkeeping

For $t\ge0$ set

$$
\Psi(t)=\begin{cases}(t-1)^2,&0\le t\le2,\\2t-3,&t\ge2,\end{cases}
\qquad D=\operatorname{tr}\Psi(G)\ge0.
$$

The following is the unit-column stability mechanism of
[Ainta, at the inspected revision](https://github.com/ainta/zeta-simple-zeros/blob/040c5e899e658aed7b56a2a87f501798fe10761d/paper/riemann.tex),
already used in [EXP-002](../EXP-002-short-interval-stability/mathematical-proof.md)
and [EXP-003](../EXP-003-odd-frame-pressure/mathematical-proof.md):

$$Q\ge4N-3s-4r-4b+D.\tag{9}$$

Here is a proof in the exact finite space. Write its dimension as $h$, put
$d=r+b$, and order the eigenvalues of $P$ as $0\le p_1\le\cdots\le p_h$.
The min-max principle and $n_+(C)\le d$ give
$\lambda_i(P+C)\le p_{i+d}$ for $1\le i\le h-d$ when $d<h$.
Indeed, intersect the first $i+d$ eigenspaces of $P$ with a codimension-at-most-$d$
subspace on which $C\le0$; the intersection has dimension at least $i$.
If $p_{i+d}\le2$, then
$(\lambda_i-2)^2\ge(2-p_{i+d})^2$; otherwise the lower bound zero suffices.
Since every omitted $(2-p_j)_+^2$ is at most four,

$$\operatorname{tr}(A-2I)^2\ge\sum_{j=1}^h(2-p_j)_+^2-4d.$$

For $d\ge h$ the right side is nonpositive, so the same inequality holds.
Use

$$
(2-t)_+^2=\Psi(t)-2t+3,\quad\operatorname{tr}P=s,\quad
\operatorname{tr}\Psi(P)=D+h-s.
$$

The last identity follows from the common nonzero spectra of $VV^*$ and $V^*V$
and $\Psi(0)=1$. Expanding the square yields (9). The argument includes singular
Gram matrices, empty simple support, and either ordering of $h$ and $s$.

## 3. Parity and the exact residual certificates

Define the excess and total distinct count by

$$E=N-s-2r-2b\ge0,\qquad Z=s+r+2b.$$

The nonnegativity follows directly from multiplicities. More precisely,

$$
E=\sum_{\substack{x\in\mathcal Z\cap\mathbb R\\m_x\ge2}}(m_x-2)
 +2\sum_{\{z,\bar z\}\subset\mathcal Z\setminus\mathbb R}(m_z-1).
$$

Let $O$ count distinct odd-multiplicity real points. Then $s+E-O\ge0$,
as seen from the following contributions:

| Support atom | Contribution to $s+E-O$ |
|---|---:|
| A simple real point | $0$ |
| A real point of even multiplicity $m\ge2$ | $m-2$ |
| A real point of odd multiplicity $m\ge3$ | $m-3$ |
| A conjugate pair with multiplicity $m\ge1$ at each point | $2(m-1)$ |

For an even atom $m=2j$ with $j\ge1$, the value is $2(j-1)$; for an odd multiple
atom $m=2j+1$ with $j\ge1$, it is again $2(j-1)$. These identities cover arbitrary
multiplicity and establish the sign without a finite census.

Set

$$\sigma=Q-(4N-3s-4r-4b+D)\ge0.$$

Using $N=s+2r+2b+E$, direct algebra gives the exact certificates

$$
\boxed{3s-(2N-Q+2O+D)=2(s+E-O)+\sigma\ge0,}
\tag{10}
$$

$$
\boxed{6Z-(7N-2Q+O+2D)=(s+E-O)+6b+2\sigma\ge0.}
\tag{11}
$$

The baseline consequences are also retained:

$$s\ge2N-Q+D,\qquad 2Z\ge3N-Q+D.\tag{12}$$

For the first, (9) is $s\ge2N-Q+2E+D$. For the second, subtracting $3N-2Z+D$
from the right side of (9) gives $N-s-2r\ge0$.

The distinct bound is independent of an invalid elementary shortcut. In fact

$$2Z-(N+s)=2b-E,$$

which can be negative. A single real point of multiplicity three has $N=3$,
$s=0$, $Z=1$, and fails $2Z\ge N+s$.

### 3.1 Sharpness controls and the scope of the scalar relaxation

Take $f=\mathbf1_{[-1/2,1/2]}$ and distinct integer real points. Their feature
vectors are orthonormal because $K(n)=\sin(\pi n)/(\pi n)$ vanishes at nonzero
integers. Give $s$ points multiplicity one and $r$ points multiplicity two. Then

$$N=s+2r,\quad Q=s+4r,\quad O=s,\quad E=b=D=\sigma=0,$$

so both (10) and (11) attain equality. This is a finite Hilbert-space sharpness
control, not an assertion that actual zeta zeros realize this configuration.

There is also an exact elementary optimization problem. For real $c$, $o\ge0$,
minimize $s$ subject to

$$s,e\ge0,\qquad s-2e\ge c,\qquad s+e\ge o.$$

The minimum is

$$s_* =\max\{0,c,(c+2o)/3\}.\tag{13}$$

Each term is a lower bound, the last obtained by adding one copy of $s-2e\ge c$
and two copies of $s+e\ge o$. For feasibility take $e_*=(o-s_*)_+$. If
$s_*\ge o$, then $e_*=0$ and all constraints hold. If $s_*<o$, then
$s_*-2e_*=3s_*-2o\ge c$, and the other constraints again hold.
Thus (13) has matching primal and dual certificates. It is optimal only for
this explicitly stated relaxation. Additional mass or geometric constraints can
improve it; no optimality among all zero configurations is asserted.

## 4. The classical odd-zero seed and interval packing

Selberg's theorem supplies, for the fixed $\alpha=51/100$, constants $a>0$ and
$T_a$ such that every sufficiently high seed interval contains at least
$a t^\alpha\log t$ distinct odd-order critical zeros. Its exact statement is
restated in Theorem B on p. 523 of
[Karatsuba's 1985 primary article](https://www.mathnet.ru/eng/im1456).
Karatsuba proves the stronger seed exponent $27/82+\varepsilon$ on p. 524.
His final interval argument on p. 536 counts distinct sign-changing zeros, which
confirms the counting convention needed here. The original Selberg proof is
imported through that verified primary restatement; no new classical constant
is extracted.

Fix $\theta\in(\alpha,1)$ and set $H=T^\theta$. Starting with $t_0=T$, recursively
put $t_{j+1}=t_j+t_j^\alpha$. Include every complete seed interval contained in
$(T,T+H]$, and stop before the first one that would cross its right endpoint.
The intervals are disjoint under the half-open convention. If the source is
stated with open endpoints, omit the affected endpoints and shrink $a$ once;
the loss is at most two distinct odd points per seed interval and is negligible
relative to $t_j^\alpha\log t_j$.

The uncovered tail is at most $(T+H)^\alpha=O(T^\alpha)=o(H)$, since $\theta>\alpha$.
Every $\log t_j\ge\log T$. Summation therefore yields

$$O(T,H)\ge(a+o(1))H\log T.$$

The Riemann–von Mangoldt formula gives

$$N(T,H)=\frac{H\log T}{2\pi}+O(H+\log T),\qquad H=T^\theta,$$

and hence $N(T,H)\sim H\log T/(2\pi)$. Choose any fixed sufficiently small
$\kappa>0$ below $2\pi a$. Then

$$\liminf_{T\to\infty}O(T,T^\theta)/N(T,T^\theta)\ge\kappa\tag{14}$$

for every fixed $\theta\in(\alpha,1)$. The constant comes from the one fixed
seed, so it is independent of the chosen longer exponent. The proof makes no
uniform assertion when $\theta-\alpha$ varies with $T$.

## 5. Wang's arithmetic input and the exact pair-sum interface

Fix $0<\lambda<\theta<1$, put $H=T^\theta$ and $L=\log T$, and transform each
zero $\rho=\beta+i\gamma$ in $(T,T+H]$ to

$$z_\rho=\frac{i(\rho-1/2)L}{2\pi}.$$

The functional-equation symmetry $\rho\mapsto1-\bar\rho$ preserves the ordinate
and maps $z_\rho$ to $\bar z_\rho$. Thus the finite operator applies, and its
simple real and odd real counts are precisely $S(T,H)$ and $O(T,H)$.

For a real even $g\in C_c^\infty(\mathbb R)$ supported in $[-\lambda,\lambda]$,
[Wang, Theorem 2.2](https://arxiv.org/pdf/2609.07918v1), states

$$
W_I(g):=\sum_{\gamma,\gamma'\in I}
\widehat g\!\left(\frac{i(\rho-\rho')L}{2\pi}\right)
\frac4{4-(\rho-\rho')^2}
=\frac{HL}{2\pi}\left(g(0)+\int |u|g(u)\,du\right)
 +O_g(H+T^\lambda L^2).
\tag{15}
$$

All sums count zero multiplicities. The complete arithmetic proof and its fixed
parameter dependencies were inspected in the [Wang transfer audit](../context/2026-09-12-wang-transfer-audit.md).
Equation (15) is the imported analytic theorem, not a result proved by a finite
symbolic test in this experiment.

Choose a smooth density $f=\eta^2$ with $\eta$ real, even, supported in
$[-\lambda/2,\lambda/2]$, and $\int f=1$. Put $g=f*f$, so $\widehat g=K^2$.
The rational pair weight is removed exactly by

$$Q=W_I(g)-\frac1{4L^2}W_I(g'').\tag{16}$$

Indeed, at $z=i(\rho-\rho')L/(2\pi)$,

$$
\widehat{g-g''/(4L^2)}(z)
=\left(1+\frac{\pi^2z^2}{L^2}\right)\widehat g(z)
=\left(1-\frac{(\rho-\rho')^2}{4}\right)\widehat g(z),
$$

which cancels the weight in (15). Apply (15) separately to the fixed functions
$g$ and $g''$; their second contribution divided by $L^2$ tends to zero after
normalization. Since $N\sim HL/(2\pi)$,

$$
\frac QN\longrightarrow\mathcal C(f)
:=\int f(t)^2\,dt+\iint|u-v|f(u)f(v)\,du\,dv.
\tag{17}
$$

The normalized error is $O_f(1/L+T^{\lambda-\theta}L)=o(1)$. At
$\lambda=\theta$ this displayed error does not tend to zero, which is why the
strict support inequality is maintained throughout the height limit.

## 6. Cosine evaluation and legal approximation limits

For fixed $0<\lambda<1$, define the normalized cosine density

$$
f_\lambda(t)=\frac{\cos(\sqrt2t)}{\sqrt2\sin(\lambda/\sqrt2)}
\mathbf1_{[-\lambda/2,\lambda/2]}(t).
$$

It is positive on its supporting interval and has integral one. Its known
optimization role comes from the Montgomery–Taylor/Lamzouri framework; only
its following explicit evaluation is needed here.

Let $J(x)=\int|x-y|f_\lambda(y)\,dy$. On the interior of the support,
$J''=2f_\lambda$ and $f_\lambda''=-2f_\lambda$. The even function
$f_\lambda+J$ therefore has zero second derivative and is constant. At the
right endpoint $b=\lambda/2$,

$$
J(b)=b,\qquad f_\lambda(b)=\frac1{\sqrt2}\cot(\lambda/\sqrt2).
$$

Multiplying the constant identity by $f_\lambda$ and integrating gives

$$\mathcal C(f_\lambda)=\frac\lambda2+\frac1{\sqrt2}\cot(\lambda/\sqrt2)=2-c(\lambda).\tag{18}$$

Choose even smooth cutoffs increasing to one in the interior of the support,
multiply $\sqrt{f_\lambda}$ by them, and normalize in $L^2$. Their squares
$f_{\lambda,n}$ have smooth compactly supported square roots and converge to
$f_\lambda$ in $L^1$ and $L^2$. The functional in (17) is continuous under these
convergences on the fixed compact support. Thus
$\mathcal C(f_{\lambda,n})\to\mathcal C(f_\lambda)$.

Apply (10)–(12) separately for each fixed $f_{\lambda,n}$. First take
$T\to\infty$, using (14) and (17), and drop the nonnegative defect. This gives

$$
\liminf S/N\ge\max\{0,2-\mathcal C(f_{\lambda,n}),
[2-\mathcal C(f_{\lambda,n})+2\kappa]/3\},
$$

$$
\liminf Z/N\ge\max\{\kappa,[3-\mathcal C(f_{\lambda,n})]/2,
[7-2\mathcal C(f_{\lambda,n})+\kappa]/6\}.
$$

The first term for the distinct count uses $Z\ge O$. Next let $n\to\infty$,
using (18). Finally let $\lambda\uparrow\theta$. Continuity of $c$ proves
(2) and (3). This order never makes the test family or the bandwidth depend on
$T$ and is valid even when $c(\lambda)\le0$.

## 7. The positivity threshold and the quantitative dependence on the seed

Differentiation gives

$$c'(\theta)=\tfrac12\cot^2(\theta/\sqrt2)>0.$$

Also $c(\theta)\to-\infty$ as $\theta\downarrow0$. The elementary inequality
$\tan x>x$ on $(0,\pi/2)$ implies $c(1)>1/2$, so $c$ has exactly one zero
$\theta_0\in(0,1)$.

To prove $\alpha<\theta_0$ without relying on a precomputed root, put
$a=\alpha/\sqrt2$. Since $\cos a\ge1-a^2/2>0$ and
$0<\sin a/a\le1$,

$$
a\cot a\ge1-\alpha^2/4,
\qquad
c(\alpha)\le2-\frac1\alpha-\frac\alpha4
=-\frac{1801}{20400}<0.
\tag{19}
$$

Thus $\alpha<\theta_0$. On $[\alpha,\theta_0]$, again using $\tan x>x$,

$$c'(\theta)<\frac1{\theta^2}\le\frac1{\alpha^2}<4.\tag{20}$$

The last comparison is rational: $1/\alpha^2=10000/2601<4$.
For $\delta$ in (4), the fundamental theorem of calculus yields

$$c(\theta_0-\delta)=-\int_{\theta_0-\delta}^{\theta_0}c'(t)\,dt>-4\delta\ge-\kappa.$$

Equation (2) now gives (5). Monotonicity of $c$ extends it to every fixed larger
exponent below one. For $\delta_{\mathrm{half}}$ in (6), the same argument gives
$c(\theta_{\mathrm{half}})>-\kappa/4$. Insert this into the separately proved distinct formula
(3) to obtain (7).

The improvements are positive for one fixed imported $\kappa$ even though its
size has not been evaluated. Reporting a decimal value of $\theta_1$ would
require additional information and is outside this theorem and experiment.

## 8. Attribution, prior-art limits, and excluded routes

The inherited ingredients are: the finite reflected Hilbert operator, the
stability defect and rank argument, the cosine pair functional, Wang's fixed-test
short-interval arithmetic theorem, Selberg's odd-zero density, and Karatsuba's
stronger classical interval result. Equations (10)–(11) retain their multiplicity
information; the proposed new consequence is the range extension (4)–(5).

The dated [source dossier](../context/2026-09-12-critical-mass-and-multiplicity-route.md)
and independent audit record a bounded search which did not locate this exact
short-interval combination. The finite inequalities may also be obtained as
corollaries of prior general multiplicity bounds; their novelty is not claimed.

Weighted all-critical Gram defects, negative spectral mass, high-degree short
mollifiers, and approximation criteria are separate further routes. None is a
premise of this proof. In particular, the CFKL short-mollifier theorem supplies
no automatic simple-zero count and no already-proved arbitrary-degree localized
Steuding theorem. Its numerical table is not used here.

The finite census and exact scalar checks specified in the hypothesis diagnose
implementation and transcription errors. They do not replace the universal
atom argument, the finite operator proof, or the imported analytic theorems.
No assertion of peer review or end-to-end formal verification is made.


[Confirmed verdict and exact evidence](../experiments/EXP-004-parity-density-transfer/verdict.md) | [Return to overview](README.md)
