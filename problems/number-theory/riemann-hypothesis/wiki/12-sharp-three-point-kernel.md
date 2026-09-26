# Sharp three-point kernel and improved global proportions

EXP-009 isolates the auxiliary ratio in Wang's global refinement. For
$\alpha,\beta\ge0$, put

$$
R(\alpha,\beta)=
\frac{\sqrt{(1+\alpha^2)(1+\beta^2)}+
\alpha\sqrt{1+\alpha^2}+\beta\sqrt{1+\beta^2}}
{1+\alpha^2+\alpha\beta+\beta^2}.
$$

The experiment proves

$$
R(\alpha,\beta)\le\sqrt2,
$$

with equality exactly at $(0,1)$ and $(1,0)$. Set
$\alpha=\sinh u$, $\beta=\sinh v$ and
$X=\cosh(u+v)$, $Y=\cosh(u-v)$. Then

$$
R=\frac{X/2+Y(\sqrt{X^2-1}+1/2)}
{X/2+Y(X-1/2)}.
$$

For fixed $X>1$, this is increasing in $Y$ because
$1+\sqrt{X^2-1}-X>0$. Since $1\le Y\le X$, its maximum occurs at $Y=X$.
The remaining inequality is

$$
\frac{1+\sqrt{X^2-1}}{X}\le\sqrt2,
$$

whose squared residual is $(X^2-2)^2\ge0$. Boundary and equality analysis
gives exactly the two stated ordered pairs.

The resulting kernel parameter is

$$
d_\dagger=
\frac{\sqrt{2+8\sqrt2}-(2+\sqrt2)}{2(\sqrt2-1)}
=0.283165430808537327\ldots.
$$

At the frozen rational substitution $H=372019/100000$, directed arithmetic
gives

$$
\liminf_{T\to\infty}\frac{N_0^s(T)}{N(T)}
>0.672500799594675755828355056296\ldots,
$$

and the distinct-zero companion exceeds
$0.836250399797337877914177528148\ldots$. The gain above the baseline exceeds
$9.5915264110093975\times10^{-8}$, about 43.88 percent larger than the
correction reproduced from Wang's printed substitution.

At $\theta=0.5459$, packing the sharp local cell into the EXP-007/008
rank-six curve gives a certified strict gain above
$3.0867809983334187\times10^{-31}$. It does not change the positivity onset.

The elementary ratio proof and directed arithmetic are internal. The global
transfer imports Wang's arXiv:2609.24167v1 finite spectral inequality, block
lemma, pair statistic, smoothing argument and triple packing. That preprint is
a recent unreviewed v1. The result has no effective starting height and proves
neither RH nor universal simplicity.

- [Complete proof](../experiments/EXP-009-wang-kernel-sharpening/mathematical-proof.md)
- [Adversarial audit](../experiments/EXP-009-wang-kernel-sharpening/adversarial-audit.md)
- [Confirmed source-bounded verdict](../experiments/EXP-009-wang-kernel-sharpening/verdict.md)
- [Published preprint](https://doi.org/10.5281/zenodo.22940291)
