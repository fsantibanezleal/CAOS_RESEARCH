# EXP-009 mathematical proof: the sharp Wang ratio and its transfers

## 1. Scope and notation

This note sharpens one elementary inequality in Biao Wang,
*Proportions of the non-trivial zeros of the Riemann zeta function*,
arXiv:2609.24167v1.  Wang's finite spectral inequality, three-point packing
lemma, analytic pair statistic, smoothing order, and notation are used with
attribution.  The new step is an exact optimization of the auxiliary ratio in
his kernel proof.  We then repeat the downstream algebra with the sharper
constant and combine it with the already proved EXP-007/008 local interface.

For `alpha,beta>=0`, put

$$
 R(\alpha,\beta)=
 \frac{\sqrt{(1+\alpha^2)(1+\beta^2)}
 +\alpha\sqrt{1+\alpha^2}+\beta\sqrt{1+\beta^2}}
 {1+\alpha^2+\alpha\beta+\beta^2}.
 \tag{1}
$$

## 2. Sharp ratio theorem

**Theorem 1.** For all `alpha,beta>=0`,

$$
 R(\alpha,\beta)\le\sqrt2.
 \tag{2}
$$

Equality holds exactly at `(alpha,beta)=(0,1)` and `(1,0)`.

**Proof.** Write

$$
 \alpha=\sinh u,\qquad \beta=\sinh v,qquad u,v\ge0,
$$

and define

$$
 X=\cosh(u+v),\quad Y=\cosh(u-v),\quad
 S=\sinh(u+v)=\sqrt{X^2-1}.
$$

Because `u,v>=0` and cosine hyperbolic is even and increasing on the
nonnegative axis,

$$
 X\ge Y\ge1. \tag{3}
$$

The product-to-sum identities give

$$
 \cosh u\cosh v=\frac{X+Y}{2},\qquad
 \sinh u\cosh u+\sinh v\cosh v=SY.
$$

The numerator `N` of (1) is therefore

$$
 N=\frac X2+Y\left(S+\frac12\right). \tag{4}
$$

For the denominator `A`, direct expansion gives

$$
 A=1+\sinh^2u+\sinh u\sinh v+\sinh^2v
   =\frac X2+Y\left(X-\frac12\right). \tag{5}
$$

Fix `X>1`.  Differentiating the quotient of (4) and (5) with
respect to `Y` shows that its derivative has the sign of

$$
 \left(S+\frac12\right)-\left(X-\frac12\right)
 =1+S-X. \tag{6}
$$

This is strictly positive: `S>X-1` follows after squaring from
`X^2-1>(X-1)^2`, which is equivalent to `X>1`.  Hence (1) is maximized,
for each fixed `X`, at the largest allowed `Y`, namely `Y=X`.

Equality `Y=X` in (3) means
`cosh(u-v)=cosh(u+v)`.  With `u,v>=0`, this is equivalent to `u=0` or
`v=0`.  On this boundary the quotient becomes

$$
 \frac{1+\sqrt{X^2-1}}{X}. \tag{7}
$$

All terms are nonnegative.  Squaring (7) against `sqrt(2)` reduces first to

$$
 2\sqrt{X^2-1}\le X^2,
$$

and then to

$$
 4(X^2-1)\le X^4
 \quad\Longleftrightarrow\quad
 (X^2-2)^2\ge0. \tag{8}
$$

Thus (2) holds.  Equality in (8) requires `X=sqrt(2)`.  Together with
`Y=X`, this gives either `u=0,sinh(v)=1` or
`v=0,sinh(u)=1`, hence precisely the two stated pairs.  When `X=1`,
`u=v=0` and `R=1`, so the excluded endpoint is strict.  This completes the
proof.  `square`

The proof also handles all unbounded directions; no numerical
compactification or unresolved interval boxes remain.

## 3. Sharpened three-point kernel energy

Use Wang's notation

$$
 a=\sqrt2\pi\cot(1/\sqrt2),\qquad
 \mathcal F(x)=ax\sin(\pi x)-\cos(\pi x),
$$

and `K_0` for the Fourier transform of his limiting cosine profile.  His
exact identity is

$$
 \mathcal F(x)=(2\pi^2x^2-1)K_0(x). \tag{9}
$$

For `u,v>=0`, set

$$
 d=\max(|\mathcal F(u)|,|\mathcal F(v)|,|\mathcal F(u+v)|),
 \quad \alpha=au,\quad\beta=av.
$$

If `d>=1`, the bound below is immediate.  If `d<1`, Wang's vector triangle
inequalities and trigonometric addition identity give, before he inserts his
coarser estimate `R<=2`,

$$
 (1-d)^2\le d(1+d)R(\alpha,\beta). \tag{10}
$$

Theorem 1 therefore gives

$$
 (1-d)^2\le\sqrt2\,d(1+d). \tag{11}
$$

The positive solution of equality in (11) is

$$
 d_\dagger=
 \frac{\sqrt{2+8\sqrt2}-(2+\sqrt2)}{2(\sqrt2-1)}
 =0.2831654308085373270052981480781329\ldots . \tag{12}
$$

The left side minus the right side of (11) is positive at zero and crosses
zero at `d_dagger`; hence `d>=d_dagger`.  Directed exact arithmetic in the
certificate proves

$$
 d_\dagger>
 \frac{\sqrt{57}-7}{2}>
 \sqrt5-2. \tag{13}
$$

If `u+v<=H`, then all three arguments in (9) have modulus at most `H`.
At least one of the three `mathcal F` values has modulus at least
`d_dagger`, and

$$
 |2\pi^2x^2-1|\le1+2\pi^2H^2.
$$

Consequently

$$
 \boxed{
 K_0(u)^2+K_0(v)^2+K_0(u+v)^2
 \ge e_\dagger(H):=
 \frac{d_\dagger^2}{(1+2\pi^2H^2)^2}.}
 \tag{14}
$$

This replaces Wang's numerator `(sqrt(5)-2)^2` without altering his kernel,
Gram matrix, or triple packing argument.

## 4. Global simple and distinct zero proportions

Let

$$
 C_0=\frac32-\frac1{\sqrt2}\cot(1/\sqrt2),\qquad
 a_\dagger(H)=\frac{2e_\dagger(H)}3. \tag{15}
$$

Wang's disjoint-triple count and finite spectral inequality, with (14) in
place of his kernel bound, give

$$
 \liminf_{T\to\infty}\frac{N_0^s(T)}{N(T)}
 \ge u_\dagger(H):=
 \frac{C_0-2a_\dagger(H)/H}{1-a_\dagger(H)}. \tag{16}
$$

For completeness, the order of limits is unchanged: first `T` tends to
infinity with smoothing parameter and cell length fixed, and only then does
the smoothing parameter tend to zero.  Since (14) is uniform on each fixed
cell, the replacement commutes with this order.

Take the declared rational value

$$
 H_*=\frac{372019}{100000}=3.72019. \tag{17}
$$

The exact directed certificate proves

$$
 \begin{aligned}
 C_0&=0.6725007036794116457343797908032951\ldots,\\
 u_\dagger(H_*)-C_0
 &=0.0000000959152641100939752654930995979\ldots,\\
 \boxed{u_\dagger(H_*)
 &=0.6725007995946757558283550562963947\ldots .}
 \end{aligned} \tag{18}
$$

At Wang's stated
`H_0=372018941724/10^11`, the same certificate reproduces his correction as

$$
 \delta_0=
 0.0000000666624583334125249521207539241\ldots, \tag{19}
$$

strictly between the printed decimal thresholds `6.66624e-8` and
`6.66625e-8`.  The lower endpoint of the new correction interval is larger
than the upper endpoint of (19).  Thus (18) is a strict quantitative
improvement within the same analytic framework.

Wang's distinct-zero algebra also remains unchanged and gives

$$
 \boxed{
 \liminf_{T\to\infty}\frac{N_d(T)}{N(T)}
 \ge\frac{1+u_\dagger(H_*)}{2}.}
 \tag{20}
$$

## 5. Short-interval transfer

Fix the EXP-008 point `theta=0.5459`, and let `h_6(theta)`,
`k_6(theta)`, and `q(theta)` be the source-pinned rank-six lower bound,
odd-support term, and pair statistic used there.  The certified value
`h_6(theta)>0` permits a fixed triple cell length.

Partition the scaled real zero interval into cells of length at most `H`.
If `S` simple real points occupy `M` cells, disjoint triples can be chosen with

$$
 J\ge\frac{S-2M}{3}. \tag{21}
$$

The scaled interval length divided by the short-interval zero count tends to
one, so `M/N<=1/H+o(1)`.  Wang's block lemma and (14) then give

$$
 \liminf\frac{\Delta_K}{N}
 \ge \alpha_Hs-\beta_H,qquad
 \alpha_H=\frac{2e_\dagger(H)}3,quad
 \beta_H=\frac{2\alpha_H}{H}. \tag{22}
$$

Substituting (22) into the EXP-007 finite defect-parity product before taking
limits yields the necessary condition

$$
 2(1-s)^2\le(1-k_6)
 \{q+\beta_H-(1+\alpha_H)s\}. \tag{23}
$$

At

$$
 H=140730, \tag{24}
$$

the certificate proves `H>2/h_6`, equivalently
`alpha_H*h_6-beta_H>0`.  Evaluating the left side minus the right side of
(23) at `s=h_6` is therefore positive, while the relevant quadratic branch is
decreasing.  Its smaller root `J_6` satisfies

$$
 \boxed{J_6(0.5459,140730)>h_6(0.5459)}. \tag{25}
$$

The mean-value bound certifies

$$
 J_6-h_6>
 3.08678099833341875132438420197419\times10^{-31}. \tag{26}
$$

This is strictly larger than the EXP-008 spectral gain
`1.776662254114...e-68`.  It remains tiny compared with the rank-six
improvement itself and does not change the onset exponent.

## 6. What is proved and what remains open

Theorem 1 is an unconditional elementary inequality.  Equations (14)--(20)
are obtained by substituting it into the source-pinned Wang v1 proof; (22)--
(26) also use the source-pinned EXP-007/008 local inputs.  The numerical
claims are exact directed interval statements with an independent 120-digit
interval replay.

No effective starting height is obtained.  The rank-six coefficient remains
an attributed input whose full coefficients are not printed in its source.
The cited Wang preprint has not been peer reviewed.  These results do not
prove the Riemann hypothesis, density one, or universal simplicity.

