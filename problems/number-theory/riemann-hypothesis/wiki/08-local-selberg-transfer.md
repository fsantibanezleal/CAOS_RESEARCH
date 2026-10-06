# 8. Explicit local Selberg transfer

[D+MV] EXP-005 turns an optimized global Selberg sign detector into an
explicit theorem in every fixed power interval above exponent one half. It
then combines that odd-multiplicity density with the parity inequality of
Chapter 7.

## Local odd-zero theorem

Let $O(T,H)$ count distinct odd-multiplicity critical zeros in $(T,T+H]$ and
let $N(T,H)$ count all nontrivial zero copies. Pearce-Crump's rank-three
positive-semidefinite detector has certified diagonal constant

$$
C_3\in0.6567752140190419405677628751089899133\pm10^{-17}.
$$

For every fixed $1/2<\theta<1$,

$$
\liminf_{T\to\infty}\frac{O(T,T^\theta)}{N(T,T^\theta)}
\ge\frac{\theta-1/2}{4eC_3}.
\tag{1}
$$

Choose $H=T^\theta$ and a mollifier $U\asymp T^u$. The source's
rational-frequency estimate is stated on arbitrary subintervals of $[T,2T]$.
After division by $H$, its off-diagonal is

$$
O(T^{1/2+2u-\theta}\log T).
$$

It vanishes for every fixed $u<(\theta-1/2)/2$. The diagonal estimate is
pointwise before averaging, the approximate-functional-equation error is
$O(T^{-1/4}U\log^3T)$, and each horizontal increment is $O(U\log^3T)$ for
the fixed regularization. All are negligible at the same scale. The rectangle
optimization therefore gives

$$
O(T,H)\ge\frac{H\log U}{4\pi eC_3}(1+o(1)),
$$

where the factor four retains the source normalization
$\aleph Y=2\operatorname{Re}\beta$. Riemann--von Mangoldt normalization and a
supremum over fixed legal $u$ prove (1).

## Explicit simple-critical threshold

Chapter 7 proves the pointwise finite inequality

$$3S\ge2N-Q+2O+D,\qquad D\ge0.$$

Combining (1) with Wang's fixed-test pair limit gives

$$
\liminf\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{0,c(\theta),
\frac{c(\theta)+(\theta-1/2)/(2eC_3)}3\right\},
\tag{2}
$$

with

$$c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2).$$

The numerator of the third term is strictly increasing because its derivative is

$$
\frac12\{\csc^2(\theta/\sqrt2)-1\}+\frac1{2eC_3}>0.
$$

The exact certificate is negative at $0.5459$ and positive at $0.546$.
Consequently the new positivity threshold satisfies

$$0.5459<\theta_{\rm Sel}<0.546,$$

below Wang's reported cosine threshold $0.550193964744154\ldots$.

At $\theta=0.546$, the fixed admissible exponent $u=0.02299$ has strict
off-diagonal margin $0.00002$ and proves

$$
\liminf\frac{O}{N}>0.0064386933093719401643291911693851080,
$$

$$
\liminf\frac{S}{N}>0.0000976239413345396825264438351212564.
$$

The optimized limiting curve gives the slightly larger simple-critical bound
$0.0000994910410327771597380805441742896$.

## Evidence and limits

The [confirmed verdict](../experiments/EXP-005-local-selberg-transfer/verdict.md),
[complete proof](../experiments/EXP-005-local-selberg-transfer/mathematical-proof.md),
[adversarial audit](../experiments/EXP-005-local-selberg-transfer/adversarial-audit.md),
and [canonical result](../experiments/EXP-005-local-selberg-transfer/artifacts/canonical/result.json)
are the primary record. The result hash is
`3f0ca476c0e2fe688e4e4f43fc11861d9491b3066d067e46bf88d1a441c696a5`.

The computation verifies constants, strict inequalities, source bytes and
negative controls. The all-height theorem comes from the paper proof. Recent
preprint inputs were source-checked but are not end-to-end formalized or
externally peer reviewed. No effective onset height, global proportion record,
universal simplicity result, or proof of RH is claimed.

[Previous: parity density transfer](07-parity-density-transfer.md) |
[Return to overview](README.md)
