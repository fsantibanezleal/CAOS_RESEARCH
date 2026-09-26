# EXP-010 mathematical proof

This document proves Predictions A, B and D of the
[EXP-010 declaration](hypothesis.md). Prediction C and the numerical parts of
D are exact or Arb-certified computations recorded in the canonical artifacts.
References to Young are to arXiv:1002.4403v1 (Arch. Math. 95 (2010)
539-548); his section and equation numbers are those of the arXiv version.

## 0. Setting and conventions

Fix `1/2<theta<1`, `0<nu<theta-1/2`, `R>0`, a real polynomial `P` with
`P(0)=0` and `P(1)=1`, and a real polynomial `Q` with `Q(0)=1`. Let `T` be
large and put

$$
L=\log T,\qquad H=T^\theta,\qquad y=T^\nu,\qquad \Delta=H/L,\qquad
\sigma_0=\tfrac12-\tfrac RL .
$$

With `D=d/ds`,

$$
V(s)=Q(-D/L)\zeta(s),\qquad
\psi(s)=\sum_{h\le y}\frac{\mu(h)}{h^{s+1/2-\sigma_0}}
P\Bigl(\frac{\log(y/h)}{\log y}\Bigr).
$$

All implied constants may depend on `theta, nu, R, P, Q` and on the auxiliary
parameters named in each step, never on `T`. `Z(t)=e^{i\vartheta(t)}\zeta(1/2+it)`
is Hardy's function, so `chi(1/2+it)=e^{-2i\vartheta(t)}`. `N(T,H)` counts zero
copies with `T<gamma<=T+H`; `O(T,H)` counts distinct `t in (T,T+H]` at which `Z`
changes sign; `S(T,H)` counts simple critical zeros in the same window.

## 1. Statements

**Theorem A.** Let `w` be smooth with `0<=w<=1`, `w=1` on `[T,T+H]`, support in
`[T-Delta,T+H+Delta]` and `w^{(j)}<<_j Delta^{-j}`. Then, uniformly for `R` in
compact subsets of `(0,infinity)`,

$$
\int_{\mathbb R}w(t)\,|V\psi(\sigma_0+it)|^2\,dt=c(P,Q,R,\nu)\,\widehat w(0)+O(H/L),
$$

$$
c(P,Q,R,\nu)=1+\frac1\nu\int_0^1\!\!\int_0^1
\bigl(w_R(v)P'(u)+\nu w_R'(v)P(u)\bigr)^2du\,dv,\qquad w_R(v)=e^{Rv}Q(v).
$$

**Theorem B.** Suppose moreover that `Q(x)+Q(1-x)` is a nonzero constant `beta`.
Then

$$
\liminf_{T\to\infty}\frac{O(T,T^\theta)}{N(T,T^\theta)}\ge
\kappa(P,Q,R,\nu):=1-\frac1R\log c(P,Q,R,\nu).
$$

**Theorem D.** Let `c(theta)=2-theta/2-(1/sqrt2)cot(theta/sqrt2)` be Wang's pair
term and `k` any constant with `liminf O(T,T^theta)/N(T,T^theta)>=k>=0`. Then

$$
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}\ge
h(\theta;k):=\frac{3+k-\sqrt{(1-k)(9-k-8c(\theta))}}4 .
$$

With `k=kappa` from Theorem B, the certified values of Section 5 give a positive
proportion of simple critical zeros in `(T,T+T^theta]` for every fixed
`theta` in `[0.534,1)`.

## 2. Proof of Theorem A

The proof is Young's proof of his Theorem 2 with one change of scale. Young
works with a weight supported in `[T/4,2T]`, `w^{(j)}<<Delta_Y^{-j}`,
`Delta_Y=T/L`, and a mollifier of length `M=T^{theta_Y}`, `theta_Y<1/2`. Here the
weight has support of length `H+2Delta<=2H` inside `[T/2,2T]`, derivatives
`<<(H/L)^{-j}`, and the mollifier length is `y=T^nu`. We go through his lemmas
in order and record every place where a length enters.

### 2.1 The approximate functional equation

Young's Lemma 4 (the approximate functional equation for
`zeta(1/2+alpha+it)zeta(1/2+beta-it)`, with the weight `V_{alpha,beta}(x,t)`, the
factor `X_{alpha,beta,t}` and `G(s)=e^{s^2}p(s)`,
`p(s)=((alpha+beta)^2-(2s)^2)/(alpha+beta)^2`) does not involve `w` and is used
verbatim. We work on the annuli `alpha,beta asymp 1/L`, `|alpha+beta|>>1/L` of
Young's Lemma 6; there `p(s)<<L^2(1+|s|^2)`, so every bound below holds with an
extra factor `L^2` that is absorbed into the stated errors. Two properties are
needed, for `t>=T/2`:

$$
t^j\frac{\partial^j}{\partial t^j}V_{\alpha,\beta}(x,t)\ll_{A,j}L^2(1+x/t)^{-A},
\qquad
X_{\alpha,\beta,t}=(t/2\pi)^{-\alpha-\beta}(1+O(t^{-1})).
$$

The first is Young's (4.3) and the second is his (4.2). As printed, (4.3) has the
decay factor `(1+|t/x|)^{-A}`; the Mellin representation (4.1) gives
`(1+x/t)^{-A}`, which is also the form used in the proof of his Lemma 5.

### 2.2 The twisted integral (replacing Young's Lemma 5)

**Lemma 2.1.** Let `h,k<=y` and let `alpha,beta` lie on the annuli. Then

$$
\int w(t)\Bigl(\frac hk\Bigr)^{-it}\zeta(\tfrac12+\alpha+it)\zeta(\tfrac12+\beta-it)\,dt
=\sum_{hm=kn}\frac{\int V_{\alpha,\beta}(mn,t)w(t)\,dt}{m^{1/2+\alpha}n^{1/2+\beta}}
+\sum_{hm=kn}\frac{\int V_{-\beta,-\alpha}(mn,t)X_{\alpha,\beta,t}w(t)\,dt}{m^{1/2-\beta}n^{1/2-\alpha}}
+O_A(T^{-A}).
$$

*Proof.* Insert Lemma 4. The terms with `hm=kn` are the displayed main terms. The
error term of Lemma 4 contributes `O(H T^{-A})`. For `hm!=kn`, on the support of
`w` we have `T/2<=t<=2T`, so
`partial_t^j[w(t)V_{alpha,beta}(x,t)]<<_{j,A}L^2(1+x/T)^{-A}Delta^{-j}` (each
derivative of `V` costs `t^{-1}<=Delta^{-1}`). Integrating by parts `j` times over
the support, whose length is at most `2H`,

$$
\int w(t)\Bigl(\frac{hm}{kn}\Bigr)^{-it}V_{\alpha,\beta}(mn,t)\,dt
\ll_{j,A}HL^2\,\frac{(1+mn/T)^{-A}}{(\Delta|\log(hm/kn)|)^j}
\le HL^2(1+mn/T)^{-A}\Bigl(\frac{2\sqrt{hkmn}}{\Delta}\Bigr)^j,
$$

using `|log(hm/kn)|>=1/(2sqrt(hkmn))` when `hm!=kn` (Young, proof of Lemma 5).
Also `|m^{-1/2-alpha}n^{-1/2-beta}|<=(mn)^{-1/2+O(1/L)}`. Put `eta=theta-1/2-nu>0`
and `epsilon=eta/2`.

For `mn<=T^{1+epsilon}`,

$$
\frac{2\sqrt{hkmn}}{\Delta}\le\frac{2y\,T^{(1+\epsilon)/2}L}{T^\theta}
=2L\,T^{-\eta+\epsilon/2}=2L\,T^{-3\eta/4},
$$

and there are at most `T^{2+2epsilon}` such pairs `(m,n)`, so these terms
contribute `<<H L^2 T^{2+2epsilon}(2L T^{-3eta/4})^j`, which is `O(T^{-A})` once
`j>(4/(3eta))(A+5)`.

For `mn>T^{1+epsilon}` no integration by parts is needed: the trivial bound
`<<HL^2(mn/T)^{-A'}` summed against `(mn)^{-1/2+O(1/L)}` over `mn>T^{1+epsilon}` gives
`<<HL^3T^{A'}T^{(1+epsilon)(1/2-A'+o(1))}=HL^3T^{(1+epsilon)/2-epsilon A'+o(1)}`,
which is `O(T^{-A})` for `A'>=(A+3)/epsilon`.

The reflected part of Lemma 4 is treated identically, because
`t^j partial_t^j X_{alpha,beta,t}<<|X_{alpha,beta,t}|<<1` by Stirling. `[]`

### 2.3 Reduction to the diagonal (Young, Section 5)

Inserting the mollifier,

$$
I(\alpha,\beta):=\int w(t)\zeta(\tfrac12+\alpha+it)\zeta(\tfrac12+\beta-it)|\psi(\sigma_0+it)|^2dt
=I_1(\alpha,\beta)+I_2(\alpha,\beta)+O(T^{-A}),
$$

with `I_1` given by Young's (5.1) (with `M` replaced by `y`) and `I_2` the
reflected analogue, which is `I_1(-beta,-alpha)` with `X_{alpha,beta,t}` inserted in
the `t`-integral. On the support of `w`, `t=T(1+O(H/T))`, so by (4.2)

$$
X_{\alpha,\beta,t}=(T/2\pi)^{-\alpha-\beta}\bigl(1+\rho(t)\bigr),\qquad \rho(t)\ll H/T .
$$

The contribution of `rho` is bounded with absolute values. Write `h=gh'`, `k=gk'`
with `(h',k')=1`; then `hm=kn` means `m=k'r`, `n=h'r`, and

$$
\sum_{h,k\le y}\frac{1}{\sqrt{hk}}\sum_{hm=kn}\frac{(1+mn/T)^{-A}}{(mn)^{1/2-O(1/L)}}
\ll L\sum_{g\le y}\frac1g\Bigl(\sum_{h'\le y}\frac1{h'}\Bigr)^2\ll L^4 .
$$

With `|V_{-beta,-alpha}(x,t)|<<L^2(1+x/T)^{-A}` and `|P|<<1` on `[0,1]`, the `rho`-part
of `I_2` is `<<H(H/T)L^6=o(H/L)`, because `theta<1`. Hence
`I=I_1(alpha,beta)+(T/2pi)^{-alpha-beta}I_1(-beta,-alpha)+o(H/L)`. Finally
`(2pi)^{alpha+beta}=1+O(1/L)` and `|I_1(-beta,-alpha)|<<H` by Lemma 2.2 below (the
annuli are invariant under `(alpha,beta)->(-beta,-alpha)`), so

$$
I(\alpha,\beta)=I_1(\alpha,\beta)+T^{-\alpha-\beta}I_1(-\beta,-\alpha)+O(H/L),
$$

which is the displayed identity of Young's Section 5 with `T/L` replaced by `H/L`.

### 2.4 The diagonal (replacing Young's Lemma 6)

**Lemma 2.2.** Uniformly on the annuli,

$$
I_1(\alpha,\beta)=c_1(\alpha,\beta)\,\widehat w(0)+O(H/L),\qquad
c_1(\alpha,\beta)=\frac{1}{(\alpha+\beta)\log y}\int_0^1(P'(u)+\alpha\log y\,P(u))(P'(u)+\beta\log y\,P(u))\,du .
$$

*Proof.* Follow Young, Section 6, with `M` replaced by `y`. After the Mellin
representation (6.1) and the arithmetic identity (6.2), the `u,v`-contours are
moved to `Re=delta` and then the `s`-contour to `Re s=-delta+epsilon`. The only pole
crossed is at `s=0`, because `G` vanishes at the pole `s=-(alpha+beta)/2` of
`zeta(1+alpha+beta+2s)`. The only factor that depends on `w` is
`int w(t) g_{alpha,beta}(s,t) dt`. On the new contour
`|g_{alpha,beta}(s,t)|<<(t/2pi)^{-delta+epsilon}(1+|s|^2)` by (4.2), so this integral is
`<<H T^{-delta+epsilon}(1+|s|^2)`, while `M^{u+v}` becomes `y^{2delta}` in absolute value.
The decay of `G(s)`, the bounds for the zeta quotients and the arithmetic factor
are unchanged, so the new contour contributes
`<<H y^{2delta}T^{-delta+epsilon}L^{O(1)}=H T^{-delta(1-2nu)+epsilon}L^{O(1)}`, which is `o(H/L)`
for `epsilon<delta(1-2nu)/2` because `nu<1/2`. The residue at `s=0` has
`g_{alpha,beta}(0,t)=1` and `G(0)=1`, hence contributes exactly
`widehat w(0) zeta(1+alpha+beta) sum_{i,j}(...)J_{alpha,beta}(y)` as in Young's (6.3). Young's
Lemma 7 (the asymptotic for `J`) and Section 7 (the arithmetic factor equals one
at the origin) involve neither `w` nor `T`; they give the main term
`c_1(alpha,beta) widehat w(0)` with relative error `O(1/L)`, i.e. `O(H/L)`. `[]`

### 2.5 End of the proof of Theorem A

As in Young's proof that his Lemma 6 implies his Lemma 3: `c_1(alpha,beta)+c_1(-beta,-alpha)
=int_0^1 2P'P=P(1)^2-P(0)^2=1`, and
`(1-T^{-alpha-beta})/((alpha+beta)log y)=nu^{-1}int_0^1T^{-v(alpha+beta)}dv`. Hence
`I(alpha,beta)=c(alpha,beta) widehat w(0)+O(H/L)` on the annuli, with `c(alpha,beta)` given
by Young's (3.3) with `theta` replaced by `nu`. Both sides are holomorphic for
`alpha,beta<<1/L`, so the maximum modulus principle extends the error bound to
discs of radius `asymp 1/L`. Finally, by Young's (3.4),

$$
\int w|V\psi(\sigma_0+it)|^2dt
=Q\Bigl(-\frac1L\frac{\partial}{\partial\alpha}\Bigr)Q\Bigl(-\frac1L\frac{\partial}{\partial\beta}\Bigr)
I(\alpha,\beta)\Big|_{\alpha=\beta=-R/L};
$$

the derivatives are Cauchy integrals over circles of radius `asymp 1/L`, on which
the error `O(H/L)` is uniform, and the operator applied to `c(alpha,beta)` gives
Young's (1.3) with `theta` replaced by `nu` (his Section 3). Expanding
`d/dx[e^{R nu x}P(x+u)Q(v+nu x)]` at `x=0` gives `e^{-Rv}(w_R(v)P'(u)+nu w_R'(v)P(u))`,
so Young's form equals the form of Theorem A. Uniformity in `R` on compact sets
follows because every bound above is uniform for `alpha,beta` in discs of radius
`<<1/L`. `[]`

**Remark.** The only use of `nu<theta-1/2` is Lemma 2.1; the only use of `nu<1/2`
is the contour shift in Lemma 2.2; the only use of `theta<1` is the bound for
`rho` in Section 2.3. No other step depends on the window length. The condition
`Q(0)=1` is used only to evaluate the operator in the final form; for any real
polynomial `Q` the same argument gives `int w|V psi|^2=O(H)`.

## 3. Proof of Theorem B

### 3.1 The exact identity on the critical line

Let `lambda(s)=-chi'(1-s)/chi(1-s)`. Since `zeta(1-s)=chi(1-s)zeta(s)` and
`chi(s)chi(1-s)=1`, differentiating `k` times gives

$$
\chi(s)\zeta^{(k)}(1-s)=(-1)^k(D+\lambda)^k\zeta(s),
$$

where `(D+lambda)^k` is the `k`-fold composition of `f -> f'+lambda f`. Writing
`Q(x)=sum q_k x^k`,

$$
\chi(s)V(1-s)=\sum_k q_kL^{-k}(D+\lambda)^k\zeta(s).
$$

Put `E_beta=beta zeta-V-chi(s)V(1-s)` and `Vt=V+E_beta/2`. Using
`Q(x)+Q(1-x)=beta`, i.e. `Q(-D/L)+Q(1+D/L)=beta`,

$$
E_\beta(s)=\sum_k q_kL^{-k}\bigl[(D+L)^k-(D+\lambda)^k\bigr]\zeta(s). \tag{3.1}
$$

On `s=1/2+it`: `1-s=s-bar`, `V(1-s)=conj V(s)` (real coefficients), and with
`omega=e^{i vartheta(t)}`, `omega chi(s) V(1-s)=conj(omega V(s))` and `omega zeta=Z(t)`.
Therefore `beta Z=2 Re(omega V)+omega E_beta`; the left side and `2Re(omega V)` are real,
so `omega E_beta` is real, and

$$
\beta Z(t)=2\,\mathrm{Re}\bigl(\omega(t)\,Vt(\tfrac12+it)\bigr). \tag{3.2}
$$

This holds for every real `Q`; the symmetry of `Q` only controls the size of
`E_beta`.

### 3.2 Size of the error term

By Stirling, uniformly for `sigma` in a fixed strip and `|t| asymp T`,
`lambda(s)=log(|t|/2pi)+O(1/|t|)` and `lambda^{(j)}(s)<<1/|t|` for `j>=1`. Hence
`lambda-L=O(1)` there. Expanding the compositions in (3.1), every term of
`(D+L)^k-(D+lambda)^k` contains a factor `L-lambda` or a derivative of `lambda`,
and at most `k-1` further factors of size `<<L`. Therefore

$$
E_\beta=\sum_{j<\deg Q}\varepsilon_j(s)L^{-j}\zeta^{(j)}(s),\qquad
\varepsilon_j(s)\ll 1/L, \tag{3.3}
$$

uniformly for `sigma_0<=sigma<=sigma_1`, `T/2<=t<=2T`. (With `L=log(T/2pi)` in the
definition of `V` one even gets `epsilon_j<<(H+1)/(TL)` on the window; this is not
needed.) For `j>=1`, `L^{-j}zeta^{(j)}=(-1)^j(V_{1+x^j}-zeta)`, where `V_{1+x^j}` is the
`V` of the polynomial `1+x^j`; Theorem A for the polynomials `1` and `1+x^j`
(both have constant term one) therefore gives
`int w|psi L^{-j}zeta^{(j)}(sigma_0+it)|^2dt<<H` for every `j`. With Cauchy-Schwarz,

$$
\int w\,|\psi E_\beta(\sigma_0+it)|^2dt\ll L^{-2}\sum_{j<\deg Q}\int w\,|\psi L^{-j}\zeta^{(j)}(\sigma_0+it)|^2dt
\ll H/L^2. \tag{3.4}
$$

### 3.3 Distinct sign changes

**Lemma 3.1.** For `T` avoiding the ordinates of zeros of `Vt` (a set of
arbitrarily small perturbations of `T` and `T+H` suffices),

$$
O(T,H)\ge N(T,H)-2N_{Vt}-O(L),
$$

where `N_Vt` counts zeros of `Vt` with multiplicity in the closed-left rectangle
`[1/2,sigma_1]x(T,T+H]`, zeros on `sigma=1/2` included, and `sigma_1=sigma_1(Q)` is
fixed large.

*Proof.* Let `t_1<...<t_J` be the zeros of `Vt(1/2+it)` in `(T,T+H)`, of orders
`k_1,...,k_J`, `K=sum k_j`. Write `Vt(s)=prod_j(s-1/2-it_j)^{k_j}F(s)` with `F`
holomorphic and zero-free on the segment. On the line,
`omega Vt=i^K prod_j(t-t_j)^{k_j} omega F`, so by (3.2)
`beta Z(t)=2p(t)Re W_0(t)` with `p(t)=prod(t-t_j)^{k_j}` real and
`W_0=i^K omega F` continuous and zero-free on `[T,T+H]`.

Let `phi` be a continuous argument of `W_0` on `[T,T+H]`; after a small
perturbation of `T` and `T+H`, `cos phi` is nonzero at both ends. Assume
`phi(T)<phi(T+H)` (the other case is symmetric) and let `c_1<...<c_M` be the levels
of `pi/2+pi Z` in `(phi(T),phi(T+H))`, so `M>=|Delta phi|/pi-1`. Put `p_0=T`,
`p_M=T+H`, and for `0<i<M` let `p_i` be the first point where `phi=c_i+pi/2`. Then
`p_0<p_1<...<p_M`, and `cos phi(p_i)` alternates in sign, because `phi(p_0)` lies in
`(c_1-pi,c_1)`, `phi(p_M)` lies in `(c_M,c_M+pi)` and `phi(p_i)=c_i+pi/2`. Moving
each interior `p_i` slightly, no `p_i` is a `t_j`. Now
`sgn Z(p_i)=sgn(beta) sgn p(p_i) sgn cos phi(p_i)`, and `p` changes sign only at the
`t_j`, so `Z` has opposite signs at the ends of at least `M-J` of the disjoint
intervals `(p_{i-1},p_i)`. Each such interval contains a point where `Z` changes
sign, hence

$$
O(T,H)\ge\frac{|\Delta\phi|}{\pi}-1-J .
$$

Apply the argument principle to `F` on the rectangle `[1/2,sigma_1]x[T,T+H]`. `F`
is zero-free on the left side, and its zeros inside are the zeros of `Vt` with
`sigma>1/2`. On the bottom, right and top sides
`arg F=arg Vt-sum_j k_j arg(s-1/2-it_j)`, and each factor `s-1/2-it_j` turns by
exactly `+pi` along these three sides (from direction `-pi/2` at `1/2+iT` to `+pi/2`
at `1/2+i(T+H)`). Hence

$$
\Delta\phi=\Delta\vartheta+\Delta_{\rm brt}\arg Vt-\pi K-2\pi N_>,
$$

with `N_>` the zeros of `Vt` with `sigma>1/2`. Riemann-von Mangoldt gives
`Delta vartheta/pi=N(T,H)+O(L)`. On `sigma=sigma_1`, `|V-Q(0)|<=1/4` for `sigma_1` large and
`|E_beta|<<1/L`, so `Re Vt>0` and that side contributes `O(1)`; on the horizontal
sides the classical Backlund-Jensen argument gives `O(L)`, because
`Vt=(beta zeta+V-chi V(1-s))/2=sum_{j<=deg Q}a_j(s)zeta^{(j)}(s)` with each `a_j` a
polynomial in `L^{-1}`, `lambda` and its derivatives, so `Vt` is holomorphic and
polynomially bounded near the window and `Re Vt>=1/2` at `sigma_1+iT`. Since `J<=K`,

$$
O(T,H)\ge N(T,H)-2(N_>+K)-O(L)=N(T,H)-2N_{Vt}-O(L). \qquad[]
$$

The count is of distinct sign changes: double zeros of `Z`, which are not sign
changes, are never counted, and each is paid for in `N_Vt` (for `deg Q=1` as an
on-line zero of `Vt`, for higher degree typically as a zero of `Vt` to the right
of the line). If the zeros on the line were omitted from `N_Vt` the lemma would be
false; the preflight toy functions with planted double zeros exhibit this.

### 3.4 Littlewood's lemma on the window

Let `F_1=psi Vt`. Littlewood's lemma on `[sigma_0,sigma_1]x[T,T+H]` gives

$$
2\pi\int_{\sigma_0}^{\sigma_1}n(\sigma)\,d\sigma
=\int_T^{T+H}\log|F_1(\sigma_0+it)|dt-\int_T^{T+H}\log|F_1(\sigma_1+it)|dt
+O(L),
$$

where `n(sigma)` counts zeros of `F_1` with real part `>sigma` and the `O(L)`
collects the horizontal argument integrals (Backlund-Jensen again). Every zero of
`Vt` counted in `N_Vt` is a zero of `F_1` with real part `>=1/2>sigma` for all
`sigma<1/2`, so the left side is `>=2pi(R/L)N_Vt`.

On `sigma=sigma_1`: `psi V` is a Dirichlet series `1+sum_{n>=2}b_n n^{-s}` whose
logarithm has absolutely convergent coefficients small for large `sigma_1`, so
`int_T^{T+H}log|psi V(sigma_1+it)|dt=O(1)`; and `|E_beta/(2V)|<<1/L` there, so
`int log|1+E_beta/(2V)|=O(H/L)`. On `sigma=sigma_0`, by concavity of the logarithm,
`w>=1` on `[T,T+H]`, the inequality `|a+b|^2<=(1+L^{-1/2})|a|^2+(1+L^{1/2})|b|^2`,
Theorem A and (3.4),

$$
\int_T^{T+H}\log|F_1(\sigma_0+it)|dt\le\frac H2\log\Bigl(\frac1H\int w|\psi Vt|^2\Bigr)
\le\frac H2\log c(P,Q,R,\nu)+O(HL^{-1/2}).
$$

Combining, `N_Vt<=(L/(4 pi R))H log c + o(HL)`. Since `N(T,H)=(H/2pi)L(1+o(1))`,
Lemma 3.1 gives

$$
\frac{O(T,H)}{N(T,H)}\ge1-\frac1R\log c(P,Q,R,\nu)-o(1),
$$

which is Theorem B. `[]`

## 4. Proof of Theorem D

Section 2 of the EXP-006 proof applies its finite inequality
`(Q_T-S)(N-O)>=2(N-S)^2` to Wang's scaled zero multiset of the window. Here `Q_T` is
the pair sum of a test function `f=eta^2`, `eta` supported in `(-lambda/2,lambda/2)`,
`0<lambda<theta` (it is unrelated to the polynomial `Q` of Sections 0-3), and `O` is
the number of distinct odd-multiplicity critical zeros, i.e. `O(T,H)`. With
`q_T,s_T,o_T` the ratios to `N(T,H)`, its (13) reads
`(q_T-s_T)(1-o_T)>=2(1-s_T)^2`, Wang's theorem gives `q_T->C(f)` (its (14)), and the
detector enters only through its (15), `liminf o_T>=k_3(theta)`. Replacing (15) by
`liminf o_T>=k` changes nothing else: for every `epsilon>0` and all large `T`,

$$
2(1-s_T)^2\le(\mathcal C(f)+\epsilon-s_T)(1-k+\epsilon),
$$

so `liminf s_T>=R(C(f),1-k)`, where `R(A,b)=(4-b-sqrt(b(b+8(A-1))))/4` is its (17).
Letting `f` approach the cosine density at fixed `lambda`, so that
`C(f)->C_lambda=2-c(lambda)`, and then `lambda->theta` gives
`liminf s_T>=R(2-c(theta),1-k)=h(theta;k)`, because `4-b=3+k` and
`b(b+8(A-1))=(1-k)(9-k-8c)`. This is the EXP-008 substitution with `k_6` replaced
by `k`. `[]`

For `k` fixed, `h` increases with `c` (the radicand decreases) and with `k`
(`d/dk[(1-k)(9-k-8c)]=-(10-2k-8c)<0` since `c<1` and `k<1`). Since
`c'(theta)=cot^2(theta/sqrt2)/2>0`, `c` increases on `(0,1)`. Hence if
`h(theta_*;kappa(nu_*))>0` with `nu_*<theta_*-1/2`, the same `nu_*` is admissible and
`h(theta;kappa(nu_*))>0` for every `theta` in `[theta_*,1)`.

## 5. Certified numbers

The canonical runner certifies, for the frozen parameter sets, exact
admissibility and the enclosures below; the independent audit replays them by
validated quadrature from the Chebyshev generators and by `mpmath.iv`.

| `theta` | `nu` | `kappa` (lower) | `h_L` (lower) |
|---|---|---|---|
| 0.534 | 0.0339 | 0.02431764197988 | 1.4806994e-5 |
| 0.535 | 0.0349 | 0.02503497665228 | 0.0015246940 |
| 0.54 | 0.0399 | 0.02862164964681 | 0.0090231376 |
| 0.5459 | 0.0458 | 0.03285392367255 | 0.0177638490 |
| 0.55 | 0.0499 | 0.03579499548791 | 0.0237708528 |
| 0.60 | 0.0999 | 0.07166400518009 | 0.0929528998 |

With `nu_*=0.0339` and `theta_*=0.534`, Section 4 gives a positive proportion of
simple critical zeros in `(T,T+T^theta]` for every fixed `theta` in `[0.534,1)`. At
`theta=0.5459` the bound exceeds the EXP-008 value `1.7764e-5` by a factor above
`999`.

## 6. Attribution

Young's method, Conrey's constant, CFKL's high-degree operator polynomials,
Wang's pair term and the EXP-006 product are prior results. New here: the
short-interval version of Young's argument (Section 2, via Lemma 2.1 and the
contour estimate of Lemma 2.2), the distinct sign-change count with full-weight
on-line zeros for general `Q` (Section 3.3), the localized Littlewood bookkeeping
with the error term `E_beta` (Sections 3.2 and 3.4), the combination with the
Hilbert-parity product, and the certified constants.
