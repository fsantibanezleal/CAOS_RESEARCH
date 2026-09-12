# Critical mass, odd multiplicity, and the short-interval positivity threshold

Date: 2026-09-12. Status: primary-source preflight and paper derivation. No new numerical experiment was run for this route. The published version 0.01 manuscript is unchanged; the separate version 0.02 pressure manuscript remains a scratch draft pending the coordinating review.

## 1. Finding and scope

Retaining multiplicity excess in the known finite stability inequality gives a useful connection to classical sign-change methods. A positive density of **distinct odd-multiplicity critical zeros** forces either simple critical zeros or a positive multiplicity excess. Both alternatives improve the simplicity conclusion when the optimized pair sum is near its positivity threshold.

The resulting candidate deduction is qualitative but concerns a different parameter from EXP-003: there exists a fixed exponent strictly smaller than

$$
\theta_0=0.550193964744154\ldots
$$

for which every sufficiently high interval of that power length contains a positive proportion of simple critical zeros. This follows from the paper argument below using an established Selberg or Karatsuba seed. No numerical value for the new exponent is claimed: extracting a usable numerical classical density constant remains separate work.

The finite spectral inequality is attributed to the existing stability method. The classical odd-zero theorem, Wang's short-interval arithmetic input, and elementary multiplicity accounting are also inherited. The potentially new conclusion is their short-interval combination and its strict extension of the cosine positivity range. The bounded novelty search did not locate that combination; this is not an exhaustive priority determination or independent journal review.

## 2. Primary sources and the relevant count conventions

| Source | Precisely relevant established input | Limitation |
|---|---|---|
| [Karatsuba, Math. USSR-Izv. 24 (1985), 523–537](https://doi.org/10.1070/IM1985v024n03ABEH001246) | Main theorem, p. 524: for fixed $0<\varepsilon\le0.001$, $H=T^{27/82+\varepsilon}$ has at least $a_\varepsilon H\log T$ odd-order critical zeros, with $a_\varepsilon>0$. | These zeros need not be simple. |
| Selberg (1942), as restated in Karatsuba's Theorem B, p. 523 | For fixed $\varepsilon>0$, the same positive odd-zero density holds at $H=T^{1/2+\varepsilon}$. | The original 59-page Selberg paper was not independently acquired here. The exact statement is reproduced in Karatsuba's primary article. |
| [Steuding, Acta Math. Hungar. 96 (2002), 259–308](https://doi.org/10.1023/A:1019767816190) | A positive proportion is simple and critical in every sufficiently high interval with $T^{0.552}\le H\le T$. | The 2002 publisher abstract was inspected; detailed corresponding arguments were read in the author's archived 1999 dissertation. |
| [Wang, arXiv:2609.07918v1](https://arxiv.org/abs/2609.07918v1) | The explicit simple-critical curve $c(\theta)$ below; the fixed-test arithmetic estimate holds for every $0<\lambda<\theta<1$. | Positive baseline only for $\theta>\theta_0$. This is a September 2026 preprint. |

Karatsuba's notation $N_0$ means odd-order critical zeros, whereas Wang's $N_0$ counts critical zeros with multiplicity. They must not be identified. Karatsuba's final argument on p. 536 covers sign-changing intervals and selects a disjoint subcollection; it counts distinct zeros. The main theorem and this counting step were visually checked against the actual PDF, beyond OCR. His Russian original is from 1984; the English translation is from 1985. The ResearchGate indexing date 2007 is not the publication date. [Official metadata and access](https://www.mathnet.ru/eng/im1456).

The full Karatsuba proof was inspected for its structure: a real Hardy–Selberg function, a set of intervals witnessing sign change, lower first-moment and upper second-moment estimates, and an interval-counting conclusion. Its trigonometric-sum estimates are imported, not independently reproved here. The paper itself says its exponent could be reduced with additional estimates; $27/82$ is therefore not described as an intrinsic barrier.

Steuding's [1999 dissertation](https://webdoc.sub.gwdg.de/ebook/e/1999/steuding/253563305.pdf), printed p. 11, states a mollified second-moment estimate with error

$$O\bigl(T^{1/3+\varepsilon}M^{4/3}\bigr).$$

A simple choice yields the $0.591$ threshold; the following paragraph uses the stronger mollifier choice leading to $0.552$. The separate assertion that intervals of length $T^{1/2+\varepsilon}$ contain a simple zero concerns possibly off-critical zeros and does not assert a positive critical proportion. The dissertation was defended in December 1998 and published in January 1999. Its full analytic proof was not independently reproduced.

Other apparent improvements were screened by their actual scope. Bounds with only $\gg H$ zeros give zero normalized density relative to $H\log T$. Almost-all short intervals do not imply a theorem for every interval. Global mollifier proportions do not automatically localize to every fixed power interval. Ivić's [2017 paper on multiplicities and very short value integrals](https://arxiv.org/abs/1706.08268) concerns multiplicity bounds and values of $\zeta$; the inspected statements do not provide a stronger every-interval simple-critical positive-proportion seed. Korolev's [2006 multiplicity paper](https://www.mathnet.ru/eng/im723) is a relevant further source, but its estimates were not substituted for an odd-zero density without a matching theorem.

Within this bounded primary-source sweep, Wang gives the strongest located explicit every-interval simplicity positivity threshold. This is deliberately weaker than claiming an exhaustive best-known classification of all short-interval results.

## 3. Retaining the exact multiplicity excess

Use the finite conjugation-invariant zero multiset and Hilbert operator from [EXP-003, Section 2](../experiments/EXP-003-odd-frame-pressure/mathematical-proof.md). Let

- $N$ be the total number of zero copies;
- $s$ be the number of simple real support points;
- $r$ be the number of real support points of multiplicity at least two;
- $b$ be the number of nonreal conjugate pairs of distinct support points;
- $O$ be the number of distinct real support points of odd multiplicity;
- $D_Z=s+r+2b$ be the total number of distinct complex support points.

For a real even density $f=\eta^2$ with integral one, put $K=\widehat f$ and

$$
v_z(t)=\eta(t)e^{-2\pi izt},\qquad
A=\sum_zm_z|v_z\rangle\langle v_{\bar z}|.
$$

Then $A$ is selfadjoint,

$$
\operatorname{tr}A=N,\qquad Q=\operatorname{tr}A^2
=\sum_{z,w}m_zm_wK(z-w)^2.
\tag{1}
$$

The square in the last sum is an ordinary complex square. Positivity belongs to the complete Hilbert–Schmidt sum, not to individual nonreal terms.

Let $G_s$ be the unit-diagonal Gram matrix of the simple real vectors, and set

$$
\Psi(t)=\begin{cases}(t-1)^2,&0\le t\le2,\\2t-3,&t\ge2,\end{cases}
\qquad \mathcal D=\operatorname{tr}\Psi(G_s)\ge0.
$$

The established stable finite inequality is

$$Q\ge4N-3s-4r-4b+\mathcal D.$$

Its proof comes from the known [Ainta stability lemma](https://github.com/ainta/zeta-simple-zeros/blob/040c5e899e658aed7b56a2a87f501798fe10761d/paper/riemann.tex), applied to the direct finite operator. Define the exact excess

$$
E=N-s-2r-2b
=\sum_{\substack{x\in Z\cap\mathbb R\\m_x\ge2}}(m_x-2)
 +2\sum_{\{z,\bar z\}\subset Z\setminus\mathbb R}(m_z-1)\ge0.
\tag{2}
$$

Retaining this quantity gives

$$
\boxed{s\ge 2N-Q+2E+\mathcal D.}
\tag{3}
$$

No new finite spectral lemma is needed for (3). It is an exact rearrangement before dropping a nonnegative term.

Every nonsimple odd real support point has multiplicity at least three and contributes at least one to $E$. Consequently

$$O\le s+E.$$

Combine this with (3), writing $q_0=2N-Q$:

$$
3s\ge q_0+2O+\mathcal D.
\tag{4}
$$

This formula remains correct when $q_0<0$. Its usefulness depends on the imported odd-zero density, not on asserting that odd multiplicity means simplicity.

### 3.1 Correct distinct-zero companion

The exact identity

$$D_Z=\frac{N+s-E}{2}+b$$

shows why a simple-proportion lower bound alone cannot be inserted into $(1+s/N)/2$: $E$ has the opposite sign there. Instead,

$$
3(s-E)=2(s-2E)+(s+E)
\ge2q_0+2\mathcal D+O.
$$

Thus

$$
\boxed{D_Z\ge\frac{7N-2Q+O+2\mathcal D}{6}.}
\tag{5}
$$

Equations (4) and (5) are the appropriate pair of parity bounds. They supplement the existing separate bounds $s\ge q_0+\mathcal D$ and $2D_Z\ge3N-Q+\mathcal D$.

## 4. A fixed classical seed extends to longer power intervals

Assume one established seed theorem: for a fixed $0<\alpha<1$ there are constants $a>0$ and $T_a$ such that

$$
O(t,t^\alpha)\ge a t^\alpha\log t\qquad(t\ge T_a),
\tag{6}
$$

where $O(t,H)$ counts distinct odd-multiplicity critical zeros in $(t,t+H]$. A change between open and half-open endpoints can be absorbed by a smaller constant: at most two distinct odd support points are affected per seed interval.

Fix $\theta\in(\alpha,1)$ and $H=T^\theta$. Starting at $t_0=T$, successively set $t_{j+1}=t_j+t_j^\alpha$, stopping before the next complete interval would cross $T+H$. The complete half-open seed intervals are disjoint. The uncovered tail has length at most $(T+H)^\alpha=O(T^\alpha)=o(H)$, while $\log t_j\ge\log T$. Summing (6), after any fixed endpoint reserve, gives

$$O(T,H)\ge (a+o(1))H\log T.$$

Since

$$N(T,H)\sim \frac{H\log T}{2\pi},$$

there is a constant $\kappa>0$, depending only on the fixed seed, such that

$$
\liminf_{T\to\infty}\frac{O(T,T^\theta)}{N(T,T^\theta)}\ge\kappa
\qquad\text{for every fixed }\theta\in(\alpha,1).
\tag{7}
$$

For example, after the endpoint reserve one may take any sufficiently small fixed $\kappa<2\pi a$. The eventual height can depend on $\theta$. No uniform assertion as $\theta-\alpha$ tends to zero with $T$ is required.

Karatsuba permits a fixed $\alpha=27/82+\varepsilon$ with $0<\varepsilon\le0.001$. Selberg alone already permits the convenient fixed seed $\alpha=0.51<\theta_0$. The latter choice is sufficient for strict improvement below $\theta_0$; the shorter Karatsuba seed does not by itself produce an explicit improved numerical simplicity exponent.

## 5. Short-interval transfer and the qualitative exponent improvement

Wang's fixed-test theorem and the exact removal of the rational pair weight are documented in the [arithmetic transfer audit](2026-09-12-wang-transfer-audit.md). For every fixed $0<\lambda<\theta<1$, admissible smooth test densities yield the pair functional limit with normalized error

$$O_f(1/\log T+T^{\lambda-\theta}\log T)=o(1).$$

Approximate the cosine density of bandwidth $\lambda$, first keeping the density fixed while $T\to\infty$. Taking the smooth approximation limit then gives the optimized value

$$
q(\lambda)=\frac\lambda2+\frac1{\sqrt2}\cot(\lambda/\sqrt2),\qquad
c(\lambda)=2-q(\lambda).
$$

The positive density itself is admissible for every $0<\lambda<1$; the requirement $\lambda>\theta_0$ only determines whether $c(\lambda)$ is positive. Apply (4) and (5), discard $\mathcal D\ge0$, use (7), and finally let $\lambda\uparrow\theta$. This proves the paper-level transfer statements

$$
\liminf\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge \max\left\{0,c(\theta),\frac{c(\theta)+2\kappa}{3}\right\},
\tag{8}
$$

$$
\liminf\frac{D_Z(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{\frac{1+c(\theta)}2,
\frac{3+2c(\theta)+\kappa}{6}\right\}.
\tag{9}
$$

Here and below all limits are as $T\to\infty$, for fixed $\theta>\alpha$. One may additionally retain the elementary lower bound $D_Z/N\ge O/N$ in (9). No test parameter varies with $T$, and the unsupported substitution $\lambda=\theta$ in the error term is never made.

The function $c$ is continuous, has $c(\theta_0)=0$, and satisfies

$$c'(\theta)=\tfrac12\cot^2(\theta/\sqrt2)>0.$$

At $\theta_0$, (8) gives $\liminf S/N\ge2\kappa/3>0$. By continuity there exists $\theta_1\in(\alpha,\theta_0)$ with $c(\theta_1)>-\kappa$. Equation (8) then gives

$$
\liminf_{T\to\infty}\frac{S(T,T^{\theta_1})}{N(T,T^{\theta_1})}
\ge\frac\kappa3>0.
\tag{10}
$$

This is a strict extension of the cosine simplicity positivity range, obtained without a new pair-correlation support estimate. It also persists for every fixed larger exponent. By choosing $\theta_1$ even closer to $\theta_0$, with $c(\theta_1)>-\kappa/2$, (9) gives a distinct proportion strictly greater than one half there. This does not improve the known exponent for merely having a positive distinct proportion, which is already implied by the classical odd-zero theorem on much shorter intervals.

An explicit dependence on the unspecified seed constant is available. For the fixed Selberg seed $\alpha=0.51$, use $\tan x>x$ for $0<x<\pi/2$ to get $c'(\theta)<1/\theta^2<4$ on $[\alpha,\theta_0]$. Therefore

$$
\delta=\min\left\{\frac{\theta_0-0.51}{2},\frac\kappa4\right\}>0,
\qquad \theta_1=\theta_0-\delta
$$

has $\theta_1>0.51$ and $c(\theta_1)>-\kappa$, proving (10). This formula is explicit in $\kappa$; it is not an explicit decimal exponent because the imported $\kappa$ has not been evaluated.

The original pressure improvement from EXP-003 is strongest where an explicit numerical proportion is wanted. Equations (8)–(10) serve a different purpose. They use a classical positive density to cross a threshold at which a self-improving simple-zero-only Gram argument has no initial positive density.

## 6. Weighted Gram fallback using all critical mass

This route is useful when the available classical input counts critical copies rather than distinct odd support points. It is more elaborate and is not needed for (10), because Karatsuba's distinct convention is confirmed.

Let the distinct real support have multiplicities $m_1,\ldots,m_n$, total mass $C_0=\sum m_j$, and weighted feature matrix with columns $\sqrt{m_j}v_{x_j}$. Let $B$ be its Gram matrix and $P$ its Hilbert-space product. The remaining operator contains only the $b$ nonreal pairs and has positive index at most $b$. The same min-max argument gives

$$Q\ge4N-2C_0-n-4b+\operatorname{tr}\Psi(B).\tag{11}$$

For clarity, the square-completion proof is independent of unit diagonals. With ambient dimension $h$ and eigenvalues $p_j$ of $P$,

$$
\operatorname{tr}(A-2I)^2
\ge\sum_{j=1}^h(2-p_j)_+^2-4b.
$$

Use $(2-t)_+^2=\Psi(t)-2t+3$, $\operatorname{tr}P=C_0$, and
$\operatorname{tr}\Psi(P)=\operatorname{tr}\Psi(B)+h-n$; the latter accounts for the different zero-eigenvalue padding because $\Psi(0)=1$. Expanding yields (11), including singular cases or $b\ge h$.

Define the weighted diagonal defect

$$\Delta=\operatorname{tr}\Psi(B)-\sum_{j=1}^n\Psi(m_j)\ge0.$$

Nonnegativity follows from convex trace pinching to the diagonal. Since $\Psi(1)=0$ and $\Psi(m)=2m-3$ for integers $m\ge2$, (11) becomes

$$
Q\ge4N-3s-4r-4b+\Delta
=2N-s+2E+\Delta.
\tag{12}
$$

### 6.1 A sharp local estimate for diagonal entries in $[1,2]$

Let $B\succeq0$ be an $m\times m$ matrix with diagonal $a_i\in[1,2]$. Put
$H=B-\operatorname{diag}(a_i)$ and $\mathcal E=\operatorname{tr}H^2$.
Using $\Psi(t)=(t-1)^2-(t-2)_+^2$,

$$\Delta=\mathcal E-\operatorname{tr}(B-2I)_+^2.$$

Since $B-2I\preceq H$, ordered eigenvalue monotonicity gives
$\operatorname{tr}(B-2I)_+^2\le\operatorname{tr}H_+^2$. If $H\ne0$, its positive and negative eigenvalues have equal total magnitude $\tau$, because $\operatorname{tr}H=0$. Therefore

$$
\operatorname{tr}H_+^2\le\tau^2,
\qquad \operatorname{tr}H_-^2\ge\frac{\tau^2}{m-1},
$$

and hence

$$\boxed{\Delta\ge\mathcal E/m.}\tag{13}$$

The zero matrix case is immediate. Equality holds for $B=2J_m$, so the factor cannot be improved for arbitrary matrices in this class. The assertion uses ordered eigenvalue monotonicity, not the generally invalid claim that squaring preserves Loewner order.

### 6.2 Density transfer for low critical multiplicities

Let $q$ count the real support points of multiplicity one or two, with total real span at most $L$. Suppose the limiting unit cosine kernel obeys

$$2\{K(u)^2+K(v)^2+K(u+v)^2\}\ge d>0
\quad(u,v\ge0,\ u+v\le R).$$

Each three-point weighted Gram block from these $q$ points has off-diagonal energy at least the unit energy, so (13) gives diagonal defect at least $d/3$. The three shifted disjoint triple partitions, with every other real index placed in singleton blocks, give

$$\Delta\ge\frac d9\left(q-2-\frac{2L}{R}\right).\tag{14}$$

This uses both convex trace pinching and the unchanged diagonal subtraction. The summed consecutive triple spans are at most $2L$; at most $2L/R$ of the $q-2$ windows have span greater than $R$. Empty or negative right sides cause no difficulty.

For critical multiplicities at least three, $m-2\ge m/3$. Thus their total number of copies is at most $3E$, and

$$C_0\le2q+3E.$$

Write $e=E/N$. If $\liminf C_0/N\ge a>0$ and $L\le X_T$ with $X_T/N\to1$, equations (12) and (14) yield, in the same legal fixed-test limiting order,

$$
\liminf\frac{s}{N}
\ge c(\theta)+\frac d{18}\left(a-\frac4R\right),
\qquad 0<d\le12,
\tag{15}
$$

because the additional excess coefficient is $2-d/6\ge0$. For the distinct count the exact identity gives

$$2D_Z\ge N+(2N-Q)+E+\Delta.$$

Consequently, for $0<d\le6$,

$$
\liminf\frac{D_Z}{N}
\ge\frac12\left[1+c(\theta)+\frac d{18}\left(a-\frac4R\right)\right].
\tag{16}
$$

Here the remaining excess coefficient is $1-d/6\ge0$. Unlike an unsupported inference from simplicity alone, (16) follows from the stronger finite identity.

For the cosine kernel, its known absence of three positive additive roots gives a positive compact energy minimum at each fixed $R$. Choose $R>4/a$. At $\theta_0$, (15) is positive. Compact uniform continuity in the bandwidth and the smooth-density approximation preserves any strictly smaller $d$, so another continuity argument reaches some $\theta_1<\theta_0$. The support limit is again taken only after $T\to\infty$. No explicit $R,d,a$ was numerically optimized or certified in this source-only investigation.

### 6.3 Why arbitrary high multiplicities cannot replace the excess term

The bound (13) relies on diagonal entries at most two. For diagonal entries three, take a positive semidefinite matrix $B=3I+H$ with nonzero small off-diagonal $H$ and spectrum entirely greater than two. The function $\Psi$ is linear on that spectrum, so $\Delta=0$ although $\operatorname{tr}H^2>0$. This is an exact obstruction to extending (13) unchanged. High multiplicities must be paid for through $E$, as in (12)–(16).

## 7. Adversarial checks and what is not being claimed

The following issues were checked on paper:

- A multiple critical zero can be odd without being simple. Its required charge is supplied by $m-2$, not by counting it as simple.
- A nonreal conjugate pair of simple zeros contributes two to $N$ and two to the distinct count, zero to $s,O,E$. Its signed operator contribution remains present in $Q$.
- The parity distinct companion is (5), not an automatic half-sum of the improved simple bound. For general high multiplicities the latter would ignore the negative $-E$ term.
- The fixed seed interval packing loses $o(H)$ length and at most $O(H/T^\alpha)$ endpoint counts, which is $o(H\log T)$. It does not require an unproved uniform classical constant as the seed exponent moves.
- A positive but unspecified classical constant suffices for the existential threshold theorem. It does not supply a certified decimal threshold or explicit starting height.
- Wang's strict support inequality remains $\lambda<\theta$. Positivity of the baseline is not a hypothesis of the pair-sum theorem or of the finite operator inequality.
- The weighted fallback treats all omitted indices as singleton blocks, so diagonal baselines cancel correctly under pinching.
- No empirical zero list, GPU calculation, real-zero-only replacement of the pair sum, or RH assumption is used.

The new route does not solve RH, prove all zeros simple, improve the global proportion record, or establish a new prime-correlation asymptotic. It is proposed as an unconditional deduction from the classical seed and the cited spectral and arithmetic inputs, pending the coordinating mathematical review. Its validation status must not be represented as an end-to-end formal proof.

## 8. Bounded novelty search and next gate

The source sweep included the exact strings `simple zeros short intervals positive proportion`, `simple critical zeros Karatsuba`, `simple zeros short intervals Ivic Korolev`, the numerical threshold signature, and Wang combined with Selberg or odd multiplicity. It returned the primary sources above and did not locate a public statement of (8) or (10).

The pinned source snapshots were also searched across their Markdown, TeX, and Lean files for `Karatsuba`, `Selberg`, `odd ... multiplicity`, `weighted ... Gram`, and `short ... interval`: Ainta `040c5e899e65`, Anthropic `fbdc36bbf17d`, Axiom `4c73b3172321`, Tawanerguo `45149f6d4030`, Trmdy `1610b97b7895`, and Yuhang Shi `1aeda8e9f067`. None of those search expressions matched. Absence of a phrase is evidence of a bounded search, not proof of absence of the mathematical consequence. The known general multiplicity/rank inequalities can already contain the finite accounting as an immediate corollary.

The [Teal Sea frontier notes at the inspected pin](https://github.com/teal-sea/zeta-lab/blob/c614e65188f0b5d73b342436383ae558fbd3aafd/hunts/rogue_frontier/FRONTIER_MAP.md) were used only as discovery leads. No classical odd-density transfer was located there. Their global counting summaries contain caveats and are not a substitute for the primary count conventions.

The recommended next gate is a declared, committed exact verification experiment covering the finite multiplicity identities, their sharp limitations, the weighted matrix lemma if retained, the legal seed-packing and support limits, and an independent proof review. An explicit classical density extraction would be a separate, source-heavy project. The qualitative exponent deduction is already the more relevant target than another small optimization of the EXP-003 numerical curve.

### 8.1 The short-mollifier novelty lead is a separate analytic task

[Conrey, Farmer, Kwan, Lin, and Turnage-Butterbaugh, *Short mollifiers*, arXiv:2508.11108v1](https://arxiv.org/abs/2508.11108v1) proves critical-zero positivity with arbitrarily short mollifiers by allowing high-degree derivative combinations. It does not state the corresponding simplicity theorem. Its Section 7, question (5), explicitly leaves the bound $\kappa(u)>2u/3$ on the whole interval $0<u\le1/2$ open; Theorem 1 establishes it only for sufficiently small $u$. The larger-parameter table is numerical evidence. The ending questions and bibliography were inspected.

The standard simple-zero refinement relies on common zeros of $\zeta$ and $\zeta'$. Higher derivative combinations need not vanish at a multiple zero of low multiplicity, so that refinement cannot be silently imported. A primary illustration of this distinction appears in [Conrey, Iwaniec, and Soundararajan, *Critical zeros of Dirichlet L-functions*, p. 176](https://aimath.org/~kaur/publications/78.pdf), where the use of only the first derivative is tied explicitly to the simple-zero count.

Localizing a fixed high-degree combination with a suitable short-interval moment theorem could furnish a stronger explicit critical or odd seed. Neither the needed localized theorem nor a certified numerical seed is asserted here. This possible extension is excluded from the premises of the classical-seed parity deduction and should have a separate declaration before numerical work.

### 8.2 What Steuding's proof supplies for that separate extension

The printed Theorem 2.1 treats $F=\zeta+\zeta'/\log T$. Its derivation introduces arbitrary derivative orders on printed p. 12 and arbitrary-order Cauchy bounds for the divisor-error function in (2.43)–(2.44), printed p. 37. However, the final error analysis explicitly specializes to orders at most two on p. 41. Thus an arbitrary fixed polynomial detector is a plausible extension of the machinery, not the theorem as stated. The final estimate and closing discussion on pp. 48–49 were inspected.

To make the extension rigorous, one would need a uniform two-shift estimate for

$$
\int_T^{T+T^\theta}
\zeta(a+z_1+it)\zeta(a+z_2-it)|M(a+it)|^2\,dt,
\qquad |z_1|,|z_2|\le C/\log T,
$$

with mollifier length $T^u$ and error $O_{C}(T^{1/3+4u/3+\varepsilon})$ after the required main term is subtracted. Cauchy differentiation would multiply the error by powers of $\log T$, canceled by the normalized derivative operator; fixed-degree constants can depend on the detector. It remains necessary to establish the shifted estimate, including the fact that the mollifier is held fixed while the zeta factors are differentiated. The sufficient interval condition would then be $\theta>1/3+4u/3+\varepsilon$.

There are three independent gates before inferring a useful explicit simplicity exponent from this lead:

1. Prove the arbitrary fixed-degree localized moment and its required uniformity.
2. Establish precisely which critical zeros the high-degree detector counts. A mass bound cannot be substituted for the distinct odd count in (8).
3. Certify a concrete numerical seed for the selected parameters. The CFKL numerical table alone does not discharge this gate.

Even if the first gate passes, a critical-mass-only result initially feeds the weighted fallback, not the stronger parity formula. No claim near the exponent $1/2$ follows from the present source review.

## 9. Source persistence and current artifact boundary

The local source cache now contains the full Karatsuba 1985 PDF and text and the Steuding 1999 dissertation PDF and text. Their acquisition hashes, access URLs, publication provenance, and rights notes are in `source-cache/critical-mass-source-downloads.json`; the coordinating source agent owns the canonical manifest update. No open redistribution license was identified, so these PDFs remain local reference-cache material rather than being added to a public manuscript source package.

The Karatsuba PDF is 518106 bytes, SHA-256 `af5d1c40afeb3cbbe24286427a26dafefaa09c25618c371844b9923a2ec20c55`. The Steuding PDF is 460641 bytes, SHA-256 `6a8a742287f71c1e0dbf9e8d49527462c70bba0ee24c217aa72392bb55e692b2`. The archive is evidence for source provenance; it is not a numerical certificate of the candidate theorem.
