# 9. Hilbert dimension and parity compression

[D+MV] EXP-006 is confirmed by its [verdict](../experiments/EXP-006-hilbert-parity-compression/verdict.md), [adversarial audit](../experiments/EXP-006-hilbert-parity-compression/adversarial-audit.md), and [proof-review binding](../experiments/EXP-006-hilbert-parity-compression/proof-review.json). The exact certificate checks the finite census and numerical threshold; the written argument supplies the universal and asymptotic quantifiers. General RH remains open.

## 1. Finite theorem

Let `Z` be a nonempty finite multiset of complex numbers invariant under
complex conjugation, with positive integer multiplicities. Let `N` be its
cardinality counted with multiplicity, `S` the number of simple real support
points, and `O` the number of distinct real support points of odd
multiplicity.

Let `eta` be a real even function in `L^2(R)`, supported in a bounded interval
and normalized by

$$
\widehat{\eta^2}(0)=1.
$$

Put `K=widehat{eta^2}` and

$$
Q=\sum_{z,w\in Z}K(z-w)^2,
$$

where the sums count multiplicity. Then

$$
\boxed{(Q-S)(N-O)\ge 2(N-S)^2.} \tag{1}
$$

In particular, the weaker inequality declared before computation,
`Q(N-O)>=2(N-S)^2`, also holds. The coefficient two in (1) is sharp. A
single real point of multiplicity two has `N=2`, `S=O=0`, and `Q=4`, so
equality holds. A single real point of multiplicity three gives another
equality case: `N=3`, `S=0`, `O=1`, and `Q=9`.

### Proof

Use the notation and construction in the proof of Proposition 2.1 of
Lamzouri, arXiv:2609.02882v2. List the simple real support points as

$$x_1,\ldots,x_S,$$

the nonsimple real support points as

$$x_{S+1},\ldots,x_{S+r},$$

and the nonreal support as `k` conjugate pairs

$$z_1,\overline z_1,\ldots,z_k,\overline z_k.$$

Lamzouri associates functions `f_x`, `g_z`, and `h_z` in a real-structured
Hilbert space and introduces three nested Gram-Schmidt ranges. The first has
exact dimension

$$
d=r+k. \tag{2}
$$

This follows from linear independence of distinct exponentials on the
positive-measure set where `eta` is nonzero.

Let `alpha_j` be the real diagonal tensor coefficients in that proof, divided
into first, middle, and last ranges. Its second-moment identity and Bessel
inequality give

$$
Q=\|F\|_2^2\ge\sum_j\alpha_j^2. \tag{3}
$$

Write the coefficient sums in the three ranges as `A_U`, `A_M`, and `A_L`.
The same proof establishes

$$
A_U+A_M+A_L=N,\qquad A_M\le S,\qquad
\alpha_j\le0\quad\hbox{in the last range}. \tag{4}
$$

For any `t>=1`, apply `x^2>=2tx-t^2` to each of the `d` first-range
coefficients, `x^2>=2x-1` to each of the `S` middle-range coefficients, and
`x^2>=2tx` to every nonpositive last-range coefficient. Equations (3)-(4)
give the attributed arbitrary-parameter inequality

$$
\begin{aligned}
Q
&\ge 2tA_U-t^2d+2A_M-S+2tA_L\\
&=2tN-(2t-2)A_M-S-t^2d\\
&\ge2tN-(2t-1)S-t^2d. \tag{5}
\end{aligned}
$$

This parameter inequality is also present in Anthropic's archived
`RankTraceMult.lean`; EXP-006 does not claim it as new.

If `d=0`, there is no nonsimple real point and no nonreal conjugate pair.
Every element is simple and real, so `N=S=O`; both sides of (1) vanish.
Assume `d>0`. Multiplicity alone gives `N-S>=2d`, so
`t=(N-S)/d>=2` is allowed in (5). Substitution yields

$$
Q\ge S+\frac{(N-S)^2}{d}. \tag{6}
$$

Let `o=O-S` be the number of odd nonsimple real support points. Each
nonsimple real point contributes at least two copies, each odd nonsimple real
point contributes at least one additional copy, and each nonreal conjugate
pair contributes at least two copies. Hence

$$
N-S\ge2r+o+2k=2d+O-S,
$$

or equivalently

$$
2d\le N-O. \tag{7}
$$

Combining (6) and (7) proves

$$
(Q-S)(N-O)
\ge\frac{(N-S)^2}{d}(N-O)
\ge2(N-S)^2,
$$

which is (1).

## 2. Short-interval theorem

Let `N(T,H)` count all nontrivial zero copies of the Riemann zeta function in
`(T,T+H]`, let `S(T,H)` count simple critical-line zeros, and let `O(T,H)`
count distinct odd-multiplicity critical-line zeros. Fix

$$
\frac12<\theta<1,\qquad H=T^\theta.
$$

Define

$$
c(\theta)=2-\frac\theta2-
\frac1{\sqrt2}\cot\!\left(\frac\theta{\sqrt2}\right), \tag{8}
$$

and, using Pearce-Crump's reproducible rank-three constant,

$$
k_3(\theta)=\frac{\theta-1/2}{4eC_3}. \tag{9}
$$

Put

$$
h_3(\theta)=
\frac{3+k_3(\theta)-
\sqrt{(1-k_3(\theta))(9-k_3(\theta)-8c(\theta))}}4. \tag{10}
$$

Then

$$
\boxed{
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge h_3(\theta).} \tag{11}
$$

The right side may be negative away from the range of interest. Combining it
with the trivial bound, Wang's cosine bound, and EXP-004 gives

$$
\boxed{
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge
\max\left\{0,c(\theta),
\frac{c(\theta)+2k_3(\theta)}3,
h_3(\theta)
\right\}.} \tag{12}
$$

### Proof

Fix `0<lambda<theta` and a real even smooth test function of the form
`f=eta^2`, with `eta` supported in `(-lambda/2,lambda/2)` and normalized by
`integral f=1`. Apply (1) to Wang's scaled zero multiset

$$
Z_T=\left\{\frac{i(\rho-1/2)\log T}{2\pi}:
T<\operatorname{Im}\rho\le T+T^\theta\right\}.
$$

The functional equation makes this multiset invariant under conjugation. Its
`N`, `S`, and `O` are exactly `N(T,H)`, `S(T,H)`, and `O(T,H)`. Put

$$
q_T=\frac{Q_T}{N(T,H)},\qquad
s_T=\frac{S(T,H)}{N(T,H)},\qquad
o_T=\frac{O(T,H)}{N(T,H)}.
$$

After division of (1) by `N(T,H)^2`, one obtains the pointwise inequality

$$
(q_T-s_T)(1-o_T)\ge2(1-s_T)^2. \tag{13}
$$

The left side is nonnegative. If `N=O`, every zero is simple and critical and
(11) is automatic. Otherwise `q_T>=s_T` follows directly from (13).

Wang's deweighted fixed-test short-interval pair formula gives

$$
q_T\longrightarrow\mathcal C(f), \tag{14}
$$

where

$$
\mathcal C(f)=\int f(u)^2\,du+
\iint|u-v|f(u)f(v)\,du\,dv.
$$

The confirmed EXP-005 theorem gives

$$
\liminf_{T\to\infty}o_T\ge k_3(\theta). \tag{15}
$$

For every positive `epsilon`, (14)-(15) imply, for all sufficiently large
`T`,

$$
q_T\le\mathcal C(f)+\epsilon,
\qquad
o_T\ge k_3(\theta)-\epsilon.
$$

Insert these bounds pointwise in (13). Since all factors being enlarged are
nonnegative,

$$
2(1-s_T)^2
\le(\mathcal C(f)+\epsilon-s_T)
(1-k_3(\theta)+\epsilon). \tag{16}
$$

Let `epsilon` decrease to zero. Write `A=mathcal C(f)` and
`b=1-k_3(theta)`. The smaller root in `s` of

$$
2(1-s)^2=b(A-s)
$$

is

$$
R(A,b)=\frac{4-b-\sqrt{b\{b+8(A-1)\}}}{4}. \tag{17}
$$

The quadratic is positive below its smaller root and (16) forces

$$
\liminf s_T\ge R(\mathcal C(f),1-k_3(\theta)). \tag{18}
$$

Now use the same legal approximation order as Wang and EXP-004. For fixed
`lambda`, approximate the normalized cosine density by smooth functions
`f=eta^2`, take the height limit first, and then take the smoothing limit. The
functional approaches

$$
\mathcal C_\lambda=
\frac\lambda2+\frac1{\sqrt2}\cot(\lambda/\sqrt2).
$$

Finally let `lambda` increase to `theta`. Since

$$
\mathcal C_\theta=2-c(\theta),
$$

(17)-(18) become (10)-(11). The other three terms in (12) are the previously
confirmed pointwise consequences and may be maximized independently.

## 3. Positivity threshold

The new term in (12) is positive exactly when its defining quadratic is
negative at zero:

$$
(2-c(\theta))(1-k_3(\theta))<2.
$$

Equivalently,

$$
F(\theta):=c(\theta)+(2-c(\theta))k_3(\theta)>0. \tag{19}
$$

On `(1/2,1)`,

$$
c'(\theta)=\frac12\cot^2(\theta/\sqrt2)>0,
\qquad
k_3'(\theta)=\frac1{4eC_3}>0.
$$

Also `k_3(theta)<1` and `c(theta)<2` throughout this interval. Therefore

$$
F'(\theta)=c'(\theta)(1-k_3(\theta))
+(2-c(\theta))k_3'(\theta)>0. \tag{20}
$$

The exact EXP-006 certificate proves

$$
F(0.545884)<0<F(0.545885). \tag{21}
$$

Consequently (19) has a unique root in that interval:

$$
\boxed{0.545884<\theta_{\rm HP}<0.545885.} \tag{22}
$$

At the previously excluded point `theta=0.5459`, the exact certificate gives

$$
c(0.5459)<0,
$$

$$
\frac{c(0.5459)+2k_3(0.5459)}3
<-0.0000107367174936433552040195369,
$$

while the strengthened term satisfies

$$
\boxed{
h_3(0.5459)
>0.0000168381638551244569880374399.} \tag{23}
$$

For comparison, the weaker finite inequality originally declared would give
only

$$
1-\sqrt{\frac{(2-c(0.5459))(1-k_3(0.5459))}{2}}
>0.0000126556179972388281537305037.
$$

Thus the retained simple-real contribution improves the explicit lower bound
by more than 33 percent at the frozen target. The new finite transfer, rather
than a change of analytic constant, crosses `0.5459`.

## 4. Scalar barrier and attribution

At `theta=0.5459`, all scalar conclusions explicitly stated in Lamzouri's
Proposition 2.1 and the EXP-004 scalar relaxation still permit `S=0`. Take a
normalized mixture of real triple points of support density `o=k_3(theta)`
and real double points of support density `(1-3o)/2`. It has

$$
N=N_0=1,\qquad S=N_s=0,\qquad O=o,
\qquad Z=\frac{1-o}{2}.
$$

The exact certificate verifies every applicable scalar inequality. Lamzouri's
simple-or-real inequality assumes a pair constant below two, while here
`2-c(theta)>2`, so that fourth headline inequality is inapplicable. The gain in
(23) comes from retaining the dimension `r+k` before scalar compression and
then coupling it to odd support through (7).

The arbitrary-parameter Hilbert estimate, Wang's pair limit, and
Pearce-Crump's Selberg constant are attributed inputs. The proposed
contribution is the parity-compressed product (1), its quadratic transfer
(11), and the threshold (22). The source and exact-phrase search described in
the preflight did not locate these formulas, but it was bounded and does not
establish absolute priority.

Pearce-Crump also prints a smaller rank-six constant. EXP-006 records that it
would improve (23) to a lower bound above
`0.0000177645181613023236390595079`, but the rank-six profile is not printed.
That sensitivity value is not a premise of (11), (22), or (23).

The result is asymptotic for every fixed exponent. It gives no effective onset
height, does not improve any global simple-zero percentage, and does not solve
the Riemann hypothesis.

[Previous: explicit local Selberg transfer](08-local-selberg-transfer.md) | [Return to overview](README.md)
