# EXP-008 mathematical proof: rank-six local transfer

Date: 2026-09-20. Status: implementation proof for adversarial review.

## 1. Imported detector

Pearce-Crump proves a vector-profile diagonal theorem for every fixed finite
rank. For an admissible profile `q` with diagonal constant `C[q]`, the fixed
mollifier has

$$
S_q(1,U)=\frac{C[q]+o(1)}{\log U}.
\tag{1}
$$

The source states that a fixed ten-direction, six-square profile `q_6` has

$$
C_6=C[q_6]\in
0.6566338678379319741683641732\pm5.63\cdot10^{-18}.
\tag{2}
$$

The public source does not print the coefficient matrix for `q_6`. Equation
(2), including existence of the admissible profile, is therefore an attributed
analytic input. EXP-008 does not claim to reproduce its contraction.

## 2. Why EXP-005 localizes every fixed rank

Fix `1/2 < theta < 1`, put `H=T^theta`, and choose a fixed

$$
0<u<\frac{\theta-1/2}{2}.
\tag{3}
$$

Pearce-Crump's vector detector is a finite sum of squares. Its analytic half is
a fixed finite vector of Dirichlet polynomials. The horizontal argument bound
used in EXP-005 applies componentwise. Summing over a fixed number of
components changes only a fixed implicit constant, so every horizontal term is
still

$$
O_q\!\left(U\log(2T)\{\log^2(2T)+\eta_U+1\}\right)=o(H).
\tag{4}
$$

The right-edge Dirichlet expansions and the auxiliary zeta and mollifier terms
are likewise componentwise finite sums. They remain `o(H)`.

The diagonal calculation (1) is pointwise before height averaging. For fixed
`q`, its remainder is

$$
O_q(T^{-1/2}U^2\log^2(2U))=o(1).
\tag{5}
$$

Pearce-Crump's arbitrary-subinterval rational-frequency estimate controls each
mixed component. After division by `H`, every off-diagonal entry is

$$
O_q(T^{1/2+2u-\theta}\log T)=o(1)
\tag{6}
$$

by (3). A fixed finite matrix has finitely many entries, so summing (6) does not
alter the exponent. The approximate-functional-equation error is also
componentwise `o(1)` because (3) implies `u<1/4`.

Consequently the local mean square is

$$
\frac1H\int_T^{T+H}|\beta_{q,U}(\delta+it)|^2dt
\le\frac{C[q]+o(1)}{x\log U}.
\tag{7}
$$

For a fixed endpoint regularization, all profile-dependent constants in
(4)-(7) are fixed before `T` tends to infinity. Take `T` to infinity first and
then remove the regularization as in the source's vector-profile theorem. No
rank, coefficient, or regularization parameter moves with `T`.

Jensen's inequality and the short rectangle now repeat EXP-005 verbatim:

$$
A(T,H)\ge\frac{H}{\pi x}
\left\{\log\frac{x\log U}{C[q]}-2\log2+o(1)\right\}.
$$

The optimum is `x=4eC[q]/log U`, whence

$$
A(T,H)\ge\frac{H\log U}{4\pi eC[q]}(1+o(1)).
$$

Since `N(T,T^theta)~H log T/(2pi)` and `log U~u log T`, taking the supremum
over fixed `u` satisfying (3) proves

$$
\liminf_{T\to\infty}\frac{A(T,T^\theta)}{N(T,T^\theta)}
\ge \frac{\theta-1/2}{4eC[q]}.
\tag{8}
$$

Apply (8) to the fixed source profile `q_6` and define

$$
k_6(\theta)=\frac{\theta-1/2}{4eC_6}.
\tag{9}
$$

## 3. Hilbert-parity consequence

EXP-006 proves for every finite conjugation-invariant multiset

$$
(Q-S)(N-O)\ge2(N-S)^2.
\tag{10}
$$

Normalize by `N^2`, pass to a subsequence realizing the lower simple density,
insert Wang's fixed-test pair limit `q_theta=2-c(theta)` and (9), and use the
nonnegativity of both factors exactly as in EXP-006. The resulting necessary
quadratic is

$$
2(1-s)^2\le(2-c(\theta)-s)(1-k_6(\theta)).
\tag{11}
$$

Its smaller root is

$$
h_6(\theta)=\frac{3+k_6(\theta)-
\sqrt{(1-k_6(\theta))(9-k_6(\theta)-8c(\theta))}}4.
\tag{12}
$$

Together with the direct Wang and linear parity transfers, (12) proves

$$
\liminf\frac{N_0^s(T,T^\theta)}{N(T,T^\theta)}\ge
\max\left\{0,c(\theta),\frac{c(\theta)+2k_6(\theta)}3,h_6(\theta)\right\}.
\tag{13}
$$

The root sign is equivalent to

$$
F_6(\theta)=c(\theta)(1-k_6(\theta))+2k_6(\theta)>0.
$$

On `(1/2,1)`,

$$
F_6'(\theta)=c'(\theta)(1-k_6(\theta))
 +(2-c(\theta))k_6'(\theta)>0.
$$

Thus the onset is unique. Directed exact evaluation supplies its brackets.
Because the printed upper enclosure of `C_6` is below the lower enclosure of
`C_3`, one has `k_6>k_3`; the strict endpoint signs prove an earlier onset
without subtracting nearly equal numerical roots.

## 4. Optimized spectral companion

EXP-007's defect-parity theorem and frame argument are independent of the
source of the odd-support lower bound. For any fixed `rho>2`, set

$$
R=\frac\rho{h_6(\theta)},\qquad
epsilon=d=(b/B)^2,\qquad p=d/R,
$$

where `b,B` are the analytic triangle quantities. With frame parameter two,

$$
\alpha=\frac{2d}{5},\qquad \beta=\frac{4d}{5R}.
$$

At the frozen `rho=11/5`,

$$
\alpha h_6-\beta
=\frac{2dh_6}{5}-\frac{4dh_6}{11}
=\frac{2dh_6}{55}>0.
\tag{14}
$$

The coupled defect-parity quadratic is

$$
2(1-s)^2\le(1-k_6)
\{2-c+\beta-(1+\alpha)s\}.
\tag{15}
$$

Let `H_6` be its smaller root. Evaluating the left side minus the right side at
`h_6` gives `(1-k_6)(alpha h_6-beta)>0`. As in EXP-007, the derivative between
the two roots has absolute value at most four. Therefore

$$
H_6-h_6\ge\frac{(1-k_6)(\alpha h_6-\beta)}4>0.
\tag{16}
$$

This correction is valid at every fixed point with `h_6(theta)>0`. It does not
move the onset because `R` diverges as `h_6` tends to zero.

## 5. Claim boundary

The new analytic deduction is the rank-independent short-interval localization
and its combination with the sharp finite product. The existence and value of
`q_6` are imported from Pearce-Crump. Wang's pair theorem, Pearce-Crump's
vector-profile estimates, and the EXP-006/007 finite products remain analytic
inputs. The result is asymptotic, has no effective starting height, and does
not prove the Riemann hypothesis.
