# EXP-005 mathematical proof: local optimized Selberg transfer

Date: 2026-09-19. Status before the canonical run: complete candidate proof,
pending adversarial adjudication and verdict. Source attribution and exact
interfaces are in the [2026-09-19 dossier](../../context/2026-09-19-local-selberg-transfer.md).

## 1. Statement

Let $A(T,H)$ count distinct zeros of odd multiplicity of
$\zeta(1/2+it)$ with ordinate in $(T,T+H]$, and let $N(T,H)$ count all
nontrivial zeta zeros in that interval with multiplicity. Let

$$
C_3=0.6567752140190419405677628751089899133\ldots
$$

be the rank-three diagonal constant of Pearce-Crump's Theorem 11.5 and
Proposition B.3.

**Local Selberg theorem.** For every fixed $1/2<\theta<1$,

$$
\liminf_{T\to\infty}\frac{A(T,T^\theta)}{N(T,T^\theta)}
\ge \frac{\theta-1/2}{4eC_3}.
\tag{1}
$$

Consequently, with

$$
c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2),
$$

the EXP-004 parity theorem gives

$$
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{0,c(\theta),
\frac{c(\theta)+(\theta-1/2)/(2eC_3)}3\right\}.
\tag{2}
$$

Here $S$ counts simple critical zeros. In particular, the exact certificate
declared for EXP-005 tests that the final quantity in (2) exceeds $9\cdot10^{-5}$
at $\theta=273/500=0.546$, while $c(273/500)<0$.

## 2. Imported detector and source notation

Use Pearce-Crump's positive-semidefinite rank-three mollifier of length
$U\asymp T^u$. Its critical-line detector is Hardy's real function times a
nonnegative weight, so every sign change detects a distinct critical zero of
odd multiplicity. Write $\beta_U$ for the source's analytic half. The
critical-line identity has normalization

$$
\aleph(s)Y_U(s)=2\operatorname{Re}\beta_U(s).
\tag{3}
$$

Thus the constant called $c$ in the source's Proposition 4.3 equals two. The
source proves

$$
S_C(1,U)\le\frac{C_3+o(1)}{\log U}
\tag{4}
$$

for this detector. The $o(1)$ is obtained by first fixing the regularized
profile, taking $T\to\infty$, and only afterward removing the regularization.
We retain that order.

## 3. Short rectangle inequality

Fix $1/2<\theta<1$, set $H=T^\theta$, and choose a fixed

$$
0<u<\frac{\theta-1/2}{2}.
\tag{5}
$$

Use the same rectangle as source Lemma 4.1, with vertical endpoints $T$ and
$T+H$. Littlewood's rectangle inequality is independent of the vertical
length. On the critical edge, divide at sign changes exactly as in the source.
The difference between the two horizontal argument integrals is at most

$$
\pi(1/2-\delta)A(T,H)+o(H).
$$

The source's horizontal estimate is
$O(U\operatorname{polylog}T)$ for each boundary. This is $o(H)$ under (5).
On the right auxiliary edge, the absolutely convergent logarithmic Dirichlet
series have integrals bounded by a polylogarithm uniformly in the starting
height; this is also $o(H)$. Therefore, for $x=1-2\delta$,

$$
\frac{\pi x}{2}A(T,H)
\ge-\int_T^{T+H}\log|\beta_U(\delta+it)|\,dt-H\log2-o(H).
\tag{6}
$$

Endpoint zeros are treated by the same limiting indentations as in Lemma 4.1.
Changing open to half-open counting affects at most two support points and is
$o(H\log T)$.

## 4. Local mean square

The diagonal estimate used in Proposition 5.8 is pointwise before averaging.
It therefore gives the same main bound on $[T,T+H]$:

$$
\frac1H\int_T^{T+H}|\beta_U(\delta+it)|^2dt
\le\frac{C_3+o(1)}{x\log U}+\text{off diagonal}.
\tag{7}
$$

It remains to show that the off-diagonal is $o(1)$. Source Lemma 5.7 applies
to arbitrary intervals $I_{\xi,\eta}\subseteq[T,2T]$ and gives, before
normalization, a factor

$$
T^{\delta-1/2}XU^2\log(2XU),\qquad X\asymp T^{1/2}.
$$

At the optimized displacement, $x\asymp1/\log T$, so
$T^{\delta-1/2}=T^{-x/2}=O(1)$. Divide by $H$ rather than by the source's
dyadic length $T$. The normalized off-diagonal is

$$
O\!\left(T^{1/2+2u-\theta}\log T\right)=o(1)
\tag{8}
$$

by (5). The source's approximate-functional-equation error is pointwise

$$
O(T^{-1/4}U\log^3T)=o(1),
$$

because (5) implies $u<1/4$. Its square and cross term are therefore $o(1)$
on the normalized shorter interval as well. Equations (7)--(8) prove

$$
\frac1H\int_T^{T+H}|\beta_U(\delta+it)|^2dt
\le\frac{C_3+o(1)}{x\log U}.
\tag{9}
$$

Every parameter in this argument is fixed before $T\to\infty$.

## 5. Optimization and odd-zero density

Jensen's inequality and (9) give

$$
\int_T^{T+H}\log|\beta_U(\delta+it)|dt
\le \frac H2\log\frac{C_3+o(1)}{x\log U}.
$$

Insert this into (6). The calculation in source Proposition 4.3 is unchanged
except that $H$ replaces $T$:

$$
A(T,H)\ge\frac{H}{\pi x}
\left\{\log\frac{x\log U}{C_3}-2\log2+o(1)\right\}.
$$

The right side is optimized at
$x=4eC_3/\log U$, yielding

$$
A(T,H)\ge\frac{H\log U}{4\pi eC_3}(1+o(1)).
\tag{10}
$$

For fixed $\theta>0$, Riemann--von Mangoldt gives

$$
N(T,T^\theta)\sim\frac{T^\theta\log T}{2\pi}.
$$

Since $\log U\sim u\log T$, (10) implies

$$
\liminf\frac{A(T,T^\theta)}{N(T,T^\theta)}
\ge\frac{u}{2eC_3}.
\tag{11}
$$

This holds for every fixed $u$ satisfying (5). Taking the supremum over those
fixed choices proves (1). No mollifier exponent moves with $T$.

## 6. Transfer to simple critical zeros

EXP-004 proves for every finite interval zero multiset

$$
3S\ge2N-Q+2A+D,
$$

where $D\ge0$ and $A$ is exactly the distinct odd-multiplicity critical
support counted above. Wang's fixed-test pair estimate and the legal
height-first support limit give $(2N-Q)/N\to c(\theta)$. Combining this with
(1), then discarding $D$, proves (2).

The source detector counts sign changes, so a multiple zero contributes once,
not by its multiplicity. This matches the $A$ term in EXP-004. The denominator
continues to count all nontrivial zero copies.

## 7. What remains imported

The proof imports Pearce-Crump's Lavrik approximate functional equation,
coefficient-uniform horizontal bound, diagonal evaluation, exact rank-three
profile, and rational-frequency lemma. EXP-005 checks their interfaces and the
new length bookkeeping; it does not reprove those analytic inputs from first
principles. The theorem is unconditional relative to those published lemmas in
the ordinary mathematical sense. It is not an end-to-end formal proof, an
effective-height theorem, or a proof of the Riemann hypothesis.
