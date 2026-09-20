# 2. Known results, optimization barriers, and formal scope

## The source-backed ladder

The exact global constant relevant to this program is

$$C_{\mathrm{MT}}=\frac12+\frac1{\sqrt2}\cot(1/\sqrt2),
\qquad C_0=2-C_{\mathrm{MT}}.$$

[Lamzouri v2, Theorem 1.1](https://arxiv.org/html/2609.02882v2) gives the
following unconditional limiting lower bounds, with the counts defined in
[Chapter 1](01-statement.md):

| Quantity divided by $N$ | Exact lower bound | Decimal |
|---|---|---:|
| $N_0^s$ | $C_0$ | 0.6725007036794116 |
| $N^d$ | $C_1=(1+C_0)/2$ | 0.8362503518397058 |
| $(N_s+N_0)/2$ | $C_1$ | 0.8362503518397058 |
| $N_{s\cup0}$ | $C_2=(1+2\sqrt2+2C_0)/(3+2\sqrt2)$ | 0.8876200081733543 |

The first two reproduce the recent Alpoge-Furman/Claude conclusion; the two
simplicity/location tradeoffs are added in Lamzouri v2. The
[EXP-001 artifact](../experiments/EXP-001-source-and-constant-audit/artifacts/result.json)
certifies these constants arithmetically, not their analytic prerequisites.

[Wang, Theorem 1.1](https://arxiv.org/html/2609.07918v1) gives, for every fixed
$0<\theta<1$, the short-interval bounds

$$c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2),
\qquad d(\theta)=\frac{1+c(\theta)}2.$$

Since $c'(\theta)=\tfrac12\cot^2(\theta/\sqrt2)>0$, the simple-critical
bound becomes positive above its unique zero $\theta_0$. EXP-002 improves
these positive values. The global limit $\theta=1$ and an exponent below the
threshold are different claims and are not obtained by relabeling the result.

## Why the cosine optimization is already saturated

For an even nonnegative density $f$ supported in
$I_\lambda=[-\lambda/2,\lambda/2]$ and normalized by $\int f=1$, the evaluated
pair sum has functional

$$\mathcal C(f)=\int f(x)^2\,dx+
\iint |x-y|f(x)f(y)\,dx\,dy.$$

The minimizing profile is

$$f_\lambda(x)=\frac{\cos(\sqrt2x)}{\sqrt2\sin(\lambda/\sqrt2)}
\mathbf1_{I_\lambda}(x),
\qquad \mathcal C(f_\lambda)=\frac\lambda2+
\frac1{\sqrt2}\cot(\lambda/\sqrt2).$$

This is the Montgomery-Taylor extremal problem, identified in the earlier
literature and explicitly invoked in
[Lamzouri, Remark 3.4](https://arxiv.org/html/2609.02882v2). The broader
nonnegative bandlimited one-delta problem, including uniqueness, is solved in
[Carneiro et al., Section 3.5, Corollary 14](https://arxiv.org/pdf/1406.5462).

[D, reproduction] There is a short independent way to see the rigidity. Define
$J(x)=\int_{I_\lambda}|x-y|f_\lambda(y)\,dy$. Because
$J''=2f_\lambda$ and $f_\lambda''=-2f_\lambda$, the sum $J+f_\lambda$ is
affine. Evenness makes it constant. Evaluation at $x=\lambda/2$ gives the
displayed value of $\mathcal C(f_\lambda)$. For $h=f-f_\lambda$ with
$\int h=0$, put $H(x)=\int_{-\lambda/2}^xh(y)\,dy$. The cross term vanishes
because $J+f_\lambda$ is constant. Integration by parts gives

$$\mathcal C(f)-\mathcal C(f_\lambda)
=\|h\|_2^2-2\|H\|_2^2.$$

The primitive $H$ is odd and has zero endpoint values. Its first available
Dirichlet frequency is $2\pi/\lambda$, so

$$\mathcal C(f)-\mathcal C(f_\lambda)
\ge\left(1-\frac{\lambda^2}{2\pi^2}\right)\|f-f_\lambda\|_2^2.$$

The coefficient is sharp in this even class: use a small perturbation
$h(x)=\varepsilon\cos(2\pi x/\lambda)$. It preserves positivity for
sufficiently small $\varepsilon$. This calculation provides an explanatory
stability certificate for an already known optimum, not a new zero-proportion
record. It is persisted in the
[Lamzouri analysis](../context/2026-09-12-lamzouri-analysis.md).

## The discarded multiplicity route

Another plausible direction was to keep the full multiplicities in the
three-block Hilbert argument. Let $n$ count simple real points, $r$ count
distinct multiple real points, $k$ count nonreal conjugate pairs, and $N$ count
all copies. Set $d=r+k$. The existing coefficient inequalities give, for every
$t\ge1$,

$$Q\ge2tN-(2t-1)n-t^2d.$$

For $d>0$, choose $t=(N-n)/d\ge2$ to obtain

$$Q\ge n+\frac{(N-n)^2}{d}.$$

With $x=N-n$ and $\Delta=x-2d$, the exact scalar rearrangement is

$$Q-N\ge(3+2\sqrt2)\Delta+
\frac{\{x-(1+\sqrt2)\Delta\}^2}{x-\Delta}.$$

This controls the sum of real multiplicity excess above two and nonreal
multiplicity excess above one. However, the arbitrary-parameter inequality
was already present in Anthropic's
[RankTraceMult.lean](https://github.com/anthropics/formal-math/blob/fbdc36bbf17d20af3fd0447c6d1a8a02773c9844/zeta23/Zeta23/ZeroSide/RankTraceMult.lean),
with abstract sharpness in
[TightMult.lean](https://github.com/anthropics/formal-math/blob/fbdc36bbf17d20af3fd0447c6d1a8a02773c9844/zeta23/Zeta23/ZeroSide/TightMult.lean).
The [low-multiplicity draft](https://github.com/zach7036/riemann-hypothesis-research/blob/main/publication/low-multiplicity-zeta/THEOREM.md)
also contains related consequences. The route was rejected as a novelty claim.
For $d=0$, all points are simple and real; division is unnecessary.

Even a complete reoptimization of these aggregate blocks recovers the same
$C_2$ union bound. Normalizing $N=1$ and writing $u$ for the simple-or-real
mass gives $d\le(1+u-2n)/4$. Minimizing
$n+4(1-n)^2/(1+u-2n)$ over $n$ gives
$1+(3/2+\sqrt2)(1-u)$. The missing information is realizability of the full
Gram matrix, which the selected experiment retains.

## What the formal repositories establish

[AxiomMath/ZetaZerosV2](https://github.com/AxiomMath/ZetaZerosV2/tree/4c73b317232173a5e6d4253702c9870ee66c2c7b)
formalizes Lamzouri's finite mechanism and its zeta transfer. The two classical
analytic inputs remain explicit hypotheses in the headline zeta statements.
They are established mathematical inputs, so this boundary is compatible with
an unconditional mathematical argument; it is still a boundary in the formal
development. The [persisted audit](../context/2026-09-12-formalization-audit.md)
distinguishes default-library compilation from comparator replay.

At the inspected Axiom head, public CI compiled the default library. It did
not run the comparator in that workflow. No local Lean build was performed in
this research session. The current
[Anthropic formal-math source](https://github.com/anthropics/formal-math/tree/fbdc36bbf17d20af3fd0447c6d1a8a02773c9844)
has a different toolchain and headline statements without those explicit
analytic assumptions. Its historical receipts and current source signatures
must not be substituted for a new local replay of all its verification jobs.

## Higher-percentage candidates and corrections

The [Ainta snapshot](https://github.com/ainta/zeta-simple-zeros/tree/040c5e899e658aed7b56a2a87f501798fe10761d)
supplies the known convex Gram defect used by EXP-002. The inspected
[trmdy successor](https://github.com/trmdy/zeta-simple-zeros-673137/tree/1610b97b7895ff34982260f8dcaf04a0f7b82cf7)
advertises a nine-point candidate $0.6733127422722459\ldots$, explicitly
pending further review and an end-to-end formalization. Its repository name
does not identify the latest claimed constant. These global candidates are
prior work and are not displaced by a short-interval $41.9076\%$ example.

The [Yang-Yang 79.62 percent record](https://zenodo.org/records/21975237) is
quarantined as an unverified analytic claim in this program. Its higher-moment
transport and modulus truncation require justification beyond finite
optimization. A public DOI, an exact matrix computation, or a Lean wrapper
assuming a moment formula does not prove that formula. The detailed objections
and [Palomar candidate](https://github.com/teal-sea/zeta-lab/blob/main/lean/PALOMAR.md)
scope questions are preserved in the
[successor review](../context/2026-09-12-original-and-successor-review.md).

Finally, EXP-001 checks a concrete normalization issue in the revised source:

$$N(T,2T)-\left\lfloor\frac{T\log(T/(2\pi))}{2\pi}\right\rfloor
=\frac{(2\log2-1)T}{2\pi}+O(\log T).$$

The additive discrepancy is of order $T$, rather than $\log T$. It remains
$o(N)$ and therefore does not alone refute the asymptotic theorem. The
[exact reproduction verdict](../experiments/EXP-001-source-and-constant-audit/verdict.md)
records this limited conclusion.

## Optimized Selberg detector and explicit localization

Pearce-Crump's 2026 preprint gives a coefficient-uniform sign-preserving
Selberg detector with a certified rank-three diagonal constant and an
off-diagonal lemma formulated for arbitrary subintervals of a dyadic block.
The global source theorem exceeds seven percent on the critical line. EXP-005
uses the arbitrary-subinterval quantifier to retain the true averaging length
$H=T^\theta$, producing a normalized error
$O(T^{1/2+2u-\theta}\log T)$.

The resulting [local theorem](08-local-selberg-transfer.md) gives explicit
distinct odd-critical density throughout $\theta>1/2$ and, after the EXP-004
parity transfer, a simple-critical positivity threshold in $(0.5459,0.546)$.
The source's global percentage, detector construction and certified profile
remain attributed prior work; the localized theorem and its parity combination
are the scoped derived contribution.

## Hilbert dimension and parity compression

EXP-006 returns to the arbitrary-parameter coefficient inequality that was
correctly classified above as prior work. Instead of relabeling that premise,
it combines its optimized form

$$Q\ge S+\frac{(N-S)^2}{r+k}$$

with the new parity count $2(r+k)\le N-O$. The result is the sharp product

$$
(Q-S)(N-O)\ge2(N-S)^2.
$$

After Wang's pair limit and the EXP-005 odd-support curve, this product becomes
a quadratic lower bound for the simple-critical proportion. The exact root is
bracketed by $0.545884<\theta_{\rm HP}<0.545885$, and the bound is already
positive at $\theta=0.5459$. The arbitrary-parameter premise is attributed;
the parity-compressed product and short-interval consequence are the scoped
deduction. See the [complete proof](09-hilbert-parity-compression.md).

[Previous: statement](01-statement.md) | [Next: full proof](03-mechanism.md)


## Confirmed pressure-frame extension

EXP-003 strengthens the first released short-interval bound. See the
[complete odd-frame theorem](06-odd-frame-pressure.md) and
[separate-stage verdict](../experiments/EXP-003-odd-frame-pressure/verdict.md).
The expanded [prior-art review](../context/2026-09-12-pressure-frame-prior-art.md)
credits global pressure and capacity methods and distinguishes their dyadic
formal statements from the short-interval application. The general RH remains open.


## Classical parity input and the new range extension

The primary Selberg theorem, restated in Karatsuba's 1985 paper, counts distinct
odd-multiplicity critical zeros in intervals of length T^(1/2+epsilon). Karatsuba's
stronger theorem uses exponent 27/82+epsilon. The proof's sign-change intervals
confirm the distinct odd convention. EXP-004 uses only the fixed Selberg seed at
51/100, packs it into longer fixed-exponent intervals, and retains its unspecified
positive density. The [source dossier](../context/2026-09-12-critical-mass-and-multiplicity-route.md)
records the exact pages and an independent source audit.

Odd zeros are not assumed simple. The new [parity theorem](07-parity-density-transfer.md)
charges each nonsimple odd point to multiplicity excess and combines that fact
with Wang's pair estimate. The result extends the simple-critical positivity
range qualitatively; a separate inequality also extends distinct density above
one half. It does not improve the already much shorter classical range for
merely positive distinct density. The finite spectral inequalities and imported
classical theorems retain their original attribution.

## Spectral defect retained through parity

EXP-007 keeps the same simple-real Gram defect used by the stability program
through the EXP-006 product. Its finite theorem is

$$
(Q-S-D(G))(N-O)\ge2(N-S)^2.
$$

Together with the analytic pressure estimate, this strictly improves every
positive point of the EXP-006 `h3(theta)` curve. The positivity onset remains
unchanged because the construction needs `h3>0`. The arbitrary-parameter
rank-trace theorem and spectral profile are attributed; the defect-parity
coupling is the scoped deduction. See the
[complete proof](10-spectral-defect-parity.md).

## Rank-independent local transfer and the source-certified rank-six onset

EXP-008 proves that the EXP-005 short-rectangle localization works for every
fixed finite detector rank $q$. It gives

$$
\liminf\frac ON\ge k_q(\theta)=\frac{\theta-1/2}{4eC_q}.
$$

Pearce-Crump's public paper states a certified $C_6$ interval below $C_3$.
Using that attributed input in the EXP-006 quadratic transfer yields
$0.5458837<\theta_6<0.5458838$, strictly earlier than the independently
certified rank-three bracket $0.5458846<\theta_3<0.5458847$. The public paper
does not print the rank-six coefficient matrix, so this is not an independent
reconstruction of $C_6$. The [rank-six chapter](11-rank-six-local-transfer.md)
states the exact theorem, arithmetic, and source boundary.
