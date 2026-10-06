# EXP-007 mathematical proof: spectral-defect parity coupling

Date: 2026-09-20. Status: proof candidate frozen before the canonical run.

## 1. Finite setting

Let `Z` be a nonempty finite multiset of complex numbers, invariant under
complex conjugation, with positive integer multiplicities. Let `N` count
copies, `S` count simple real support points, and `O` count distinct real
support points of odd multiplicity. For a normalized real even compactly
supported function `eta`, put `K=widehat{eta^2}` and

$$
Q=\sum_{z,w\in Z}K(z-w)^2.
$$

The square is the ordinary complex square. The full sum is real and
nonnegative through its Hilbert--Schmidt operator representation; individual
nonreal terms need not be positive.

List the nonsimple real support points in number `r` and the nonreal support in
`k` conjugate pairs. Put

$$d=r+k.$$

Let `G` be the `S` by `S` Gram matrix of the simple real support vectors. It is
positive semidefinite, has unit diagonal, and `tr G=S`.

## 2. Parameterized spectral defect

For `t>0`, the multiplicity-aware rank-trace theorem in the attributed
Anthropic formal source uses the convex function

$$
g_t(x)=x^2-tx-(x-t)_+^2.
$$

Apply that theorem to the positive operator formed by the simple real vectors
and to the selfadjoint remainder. The remainder has positive index at most
`d`. Evaluate the positive operator in an eigenbasis. Because its nonzero
spectrum agrees with that of `G`, the theorem gives

$$
Q\ge tS+\sum_{j=1}^Sg_t(\lambda_j)
+2t(N-S)-t^2d,
\tag{1}
$$

where `lambda_j` are all `S` eigenvalues of `G`, including zeros.

For `t>=2`, define

$$
\Psi_t(x)=g_t(x)+(t-2)x+1.
$$

Directly from the positive-part definition,

$$
\Psi_t(x)=
\begin{cases}
(x-1)^2,&0\le x\le t,\\
(t-1)(2x-t-1),&x\ge t.
\end{cases}
\tag{2}
$$

Since `sum lambda_j=S`, summing the affine correction in (2) gives

$$
\sum_j\Psi_t(\lambda_j)
=\sum_jg_t(\lambda_j)+(t-1)S.
\tag{3}
$$

Equations (1)-(3) prove

$$
\boxed{Q\ge2tN-(2t-1)S-t^2d+D_t(G),}
\qquad D_t(G)=\operatorname{tr}\Psi_t(G).
\tag{4}
$$

This parameterized rank-trace content is attributed prior work. The affine
normal form makes its relation to the Ainta defect explicit.

At `t=2`, (2) is exactly

$$
\Psi_2(x)=
\begin{cases}(x-1)^2,&0\le x\le2,\\2x-3,&x\ge2,
\end{cases}
$$

and we write `D(G)=D_2(G)`. For every `t>=2`, pointwise comparison gives

$$
\Psi_t(x)-\Psi_2(x)=
\begin{cases}
0,&0\le x\le2,\\
(x-2)^2,&2\le x\le t,\\
(t-2)(2x-t-2),&x\ge t.
\end{cases}
\tag{5}
$$

The last expression is nonnegative because `x>=t>=2`. Therefore

$$D_t(G)\ge D(G).\tag{6}$$

## 3. Defect-parity product

If `d=0`, every point is simple and real, so `N=S=O`; the claimed product has
both sides zero. Assume `d>0`. Multiplicity gives

$$N-S\ge2d,$$

so `t=(N-S)/d>=2` is admissible in (4). Substitution and (6) give

$$
Q\ge S+\frac{(N-S)^2}{d}+D(G).
\tag{7}
$$

Let `o=O-S` be the number of odd nonsimple real support points. Counting two
copies for every nonsimple real point and every nonreal pair, plus the one
additional copy forced at each of those `o` odd points, gives

$$
N-S\ge2r+o+2k=2d+O-S,
$$

or

$$2d\le N-O.\tag{8}$$

Multiplying (7) by `N-O` and using (8) proves

$$
\boxed{(Q-S-D(G))(N-O)\ge2(N-S)^2.}
\tag{9}
$$

This strictly strengthens EXP-006 whenever `D(G)>0` and `N>O`. The universal
coefficient two cannot increase: one real point of multiplicity two has
`N=2,S=O=0,Q=4,D=0`, and one real point of multiplicity three has
`N=3,S=0,O=1,Q=9,D=0`. Both give equality in (9).

## 4. Short-interval transfer

Fix `1/2<theta<1`, put `H=T^theta`, and use the same zero multiset and fixed
smooth tests as EXP-006. Write

$$
c(\theta)=2-\frac\theta2-
\frac1{\sqrt2}\cot(\theta/\sqrt2),
\qquad q(\theta)=2-c(\theta),
$$

and

$$
\kappa(\theta)=k_3(\theta)
=\frac{\theta-1/2}{4eC_3}.
$$

Wang's fixed-test theorem gives `Q/N -> q(theta)` after the lawful smoothing
limits, and EXP-005 gives `liminf O/N>=kappa(theta)`.

Suppose the limiting real kernel has an EXP-003 pressure certificate

$$
E_3(u,v)+p(u+v)\ge\epsilon,
$$

and fix an integer `ell>=1` with `ell*epsilon<=1`. Put

$$
M=2\ell+1,
\qquad \alpha=\frac{\ell\epsilon}{M},
\qquad \beta=\frac{2\ell p}{M}.
$$

The disjoint-frame and span argument in EXP-003 gives

$$
\liminf\frac{D(G)}N\ge\alpha s-\beta,
\qquad s=\liminf\frac SN.
\tag{10}
$$

Apply (9) before taking limits. Choose a subsequence on which `S/N` tends to
its liminf `s`. On that subsequence, the pair term tends to `q`, while the
liminf statements give, for every positive `delta` and all sufficiently large
indices,

$$
O/N\ge\kappa-\delta,
\qquad D/N\ge\alpha s-\beta-\delta.
$$

Both finite factors in (9) are nonnegative. Upper-bounding them with these
two estimates, then sending `delta` to zero, yields the necessary condition

$$
2(1-s)^2\le(1-\kappa)
\{q+\beta-(1+\alpha)s\}.
\tag{11}
$$

The left side minus the right side of (11) is an upward-opening quadratic.
Any feasible `s` therefore lies between its two real roots and, in particular,
is at least its smaller root

$$
H(\theta;\alpha,\beta)=
\frac{4-(1+\alpha)(1-\kappa)-
\sqrt{[4-(1+\alpha)(1-\kappa)]^2
-8[2-(1-\kappa)(q+\beta)]}}4.
\tag{12}
$$

At `alpha=beta=0`, (12) is `h_3(theta)` from EXP-006.

## 5. Strict improvement of the complete positive curve

Assume `h=h_3(theta)>0`. The analytic triangle estimate already proved in
EXP-002 and recorded as equation (18) of the EXP-003 proof gives a positive
number `d(theta,R)` for every finite `R`. Choose

$$
R=\frac4h,
\qquad \epsilon=d(\theta,R),
\qquad p=\frac dR,
\qquad \ell=2.
$$

The same source proves `d<1/4`, so `ell*epsilon<1`. Here

$$
\alpha=\frac{2d}{5},
\qquad \beta=\frac{4d}{5R}=\frac{dh}{5},
$$

and hence

$$
\alpha h-\beta=\frac{dh}{5}>0.\tag{13}
$$

For `1/2<theta<1`, direct differentiation gives
`c(theta)<c(1)<7/10`, and hence `q(theta)>13/10`. Also `d<1/4` gives
`alpha<1/10`. Thus

$$
q+\beta-(1+\alpha)>1/5,
$$

so the new quadratic is negative at `s=1` and its larger root exceeds one.
By definition, `h` makes (11) an equality when `alpha=beta=0`. At `s=h`,
the strengthened quadratic has value

$$
(1-\kappa)(\alpha h-\beta)>0.
$$

Because `0<h<1`, these two signs put `h` strictly below the new smaller root.
There is also a quantitative correlated certificate. Let `F` be the left side
minus the right side of (11). On `[h,H]`, which lies to the left of the smaller
root, `F'<0`, while

$$
F'(s)=4s-4+(1-\kappa)(1+\alpha)\ge-4.
$$

The mean value theorem and `alpha*h-beta=beta` therefore give

$$
H-h\ge\frac{F(h)}4
=\frac{(1-\kappa)\beta}{4}>0.
\tag{14}
$$

Consequently

$$
\boxed{H(\theta;\alpha,\beta)>h_3(\theta)}
\tag{15}
$$

for every fixed `theta` above the EXP-006 onset. Combining (12)-(15),

$$
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge H(\theta;\alpha,\beta)>h_3(\theta).
\tag{16}
$$

The support function, pressure parameters, and smoothing approximation are
fixed before `T` tends to infinity. Only after that limit does one approach the
cosine profile, exactly as in EXP-003 and EXP-006.

The improvement does not lower the onset exponent. At `h_3=0`, the chosen
radius is unavailable and the simple-point Gram defect can vanish. Moving the
threshold requires geometry that remains informative at `S=0` or a new
analytic statistic.

## 6. Attribution and limits

The function `g_t`, the general multiplicity-aware rank-trace inequality, and
its abstract tightness are attributed to the Anthropic formal source. The
eigenbasis interpretation and identification of the `t=2` spectral profile are
also present in the inspected teal-sea bridge. Ainta supplies the stability
profile; the active pressure repositories supply broader global block methods.
Wang supplies the short-interval pair theorem. Pearce-Crump and EXP-005 supply
the explicit odd-support curve.

The candidate contribution proved here is the defect-parity product (9), the
retention of the same defect in (11), and the strict full-curve consequence
(15). This is not a lower exponent threshold, an effective-height result, a
global proportion record, density one, or a proof of RH. Absolute priority and
external mathematical acceptance remain open.
