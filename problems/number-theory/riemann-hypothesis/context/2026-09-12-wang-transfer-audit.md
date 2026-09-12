# Wang's short-interval input: analytic transfer and novelty audit

Date: 2026-09-12. Primary source: Biao Wang, *Simple critical zeros and distinct zeros of the Riemann zeta-function in short intervals*, [arXiv:2609.07918v1](https://arxiv.org/abs/2609.07918v1), submitted 2026-09-07 at 19:30:23 UTC. The 13-page PDF prints September 9. Page references below are PDF page numbers. The version is a recent preprint, not a claim of journal acceptance or independent community consensus.

## Audit conclusion

Wang's fixed-test short-interval theorem supplies the complete arithmetic input needed to transfer a finite Hilbert-space stability inequality to intervals of length $T^\theta$. The necessary normalized pair sum converges with error tending to zero for every **fixed** $0<\lambda<\theta<1$ and every fixed admissible smooth density. The rational pair weight can be removed by an exact two-test identity. The normalization of actual zero locations gives available real span asymptotic to the number of all zero copies in the interval.

No new prime-correlation conjecture, no extension beyond the proved Fourier support, and no test family varying with $T$ are required for that transfer. Smooth approximation and the limit $\lambda\uparrow\theta$ must follow the limit $T\to\infty$. These points were checked against the full proof, including the explicit-formula estimates, not inferred from the abstract.

The finite stability argument and the resulting strict-improvement statement are recorded separately in [the experiment proof](../experiments/EXP-002-short-interval-stability/mathematical-proof.md). This audit verifies its arithmetic interface and records the primary-source priority boundary; it does not substitute for review of the finite spectral proof or a formal Lean certificate.

## 1. Exact quantities and counting conventions

Fix $0<\lambda<\theta<1$, put $H=T^\theta$, $L=\log T$, and $I=(T,T+H]$. Let $N(T,H)$ count all nontrivial zeros $\rho=\beta+i\gamma$ with $\gamma\in I$, including multiplicity. Let $S(T,H)$ count simple zeros on the critical line in the same interval. A zero of multiplicity two contributes two to $N$ and zero to $S$. Wang's distinct-zero count counts every different complex zero once, whether on the critical line or elsewhere.

The established short-interval baseline is

$$
c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2),\qquad
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}\ge c(\theta).
$$

The distinct-zero baseline is $(1+c(\theta))/2$. Since $c'(\theta)=\tfrac12\cot^2(\theta/\sqrt2)>0$, the simple-critical baseline becomes positive at the unique root

$$
\theta_0=0.5501939647441547418018013084912171208\ldots.
$$

At $\theta=3/4$, $c(\theta)=0.4190750129754243337345536106982424662\ldots$. These are asymptotic lower bounds in **every** sufficiently high interval of the specified power length, with the eventual height allowed to depend on fixed parameters. They are not finite-height assertions and do not state that all zeros lie on the critical line. [Wang, Theorem 1.1, pp. 2–3](https://arxiv.org/pdf/2609.07918v1).

Wang distinguishes two earlier short-interval problems. Steuding's 2002 result gives a positive proportion of simple critical zeros for lengths at least $T^{0.552}$. Karatsuba's result gives a positive proportion of odd-multiplicity critical zeros for length $T^{27/82+\varepsilon}$, which does not imply simplicity. The latter does imply distinct zeros in shorter intervals than the positivity range of Wang's explicit distinct-zero curve. Thus the statements must not be conflated. This historical comparison follows Wang's references and has not independently reproduced Steuding's or Karatsuba's full proofs.

## 2. Finite zero multiset and real-coordinate span

Define

$$
z_\rho=\frac{i(\rho-1/2)L}{2\pi}
=-\frac{\gamma L}{2\pi}+i\frac{(\beta-1/2)L}{2\pi}.
$$

The functional equation maps $\rho$ to $1-\bar\rho$, preserving its ordinate and multiplicity. It maps $z_\rho$ to $\bar z_\rho$. Consequently the finite multiset $Z_T=\{z_\rho:\gamma\in I\}$ is conjugation-invariant. A point is real exactly when $\beta=1/2$, and a simple real point is exactly a simple critical zero. Reversing the sign of the ordinate reverses ordering but does not change pair gaps or total span.

The real coordinates lie in an interval of length

$$
X_T=\frac{HL}{2\pi}.
$$

The Riemann-von Mangoldt formula gives

$$
N(T,H)=\frac{H\log T}{2\pi}+O(H+\log T),\qquad 1\le H\le T.
$$

Hence $N/X_T=1+O(1/L+1/H)$ and $X_T/N\to1$. This is sufficient for the finite spacing-density inequality. No assertion that a sample-grid dimension differs from the zero count by only $O(\log T)$ is needed. In particular, this transfer avoids the incorrect stronger dyadic additive estimate identified in the original Claude presentation. [Wang, (1.1)–(1.2), p. 1; Lemma 3.1, pp. 9–10](https://arxiv.org/pdf/2609.07918v1).

## 3. The precise fixed-test pair-correlation theorem

Use the Fourier convention

$$
\widehat g(z)=\int_{\mathbb R}g(\alpha)e^{-2\pi i\alpha z}\,d\alpha.
$$

For real even $g\in C_c^\infty(\mathbb R)$ supported in $[-\lambda,\lambda]$, set

$$
W_I(g)=\sum_{\gamma,\gamma'\in I}
 \widehat g\!\left(\frac{i(\rho-\rho')L}{2\pi}\right)
 \frac4{4-(\rho-\rho')^2}.
$$

Every zero sum counts multiplicity. Wang's Theorem 2.2 states

$$
W_I(g)=\frac{HL}{2\pi}
 \left(g(0)+\int_{\mathbb R}|\alpha|g(\alpha)\,d\alpha\right)
 +O_g(H+T^\lambda L^2).
$$

The constants may also depend on fixed $\lambda,\theta$. Upon division by $N(T,H)\asymp HL$, the error is

$$
O_g\!\left(\frac1L+T^{\lambda-\theta}L\right)=o(1).
$$

This directly explains the strict inequality $\lambda<\theta$. At $\lambda=\theta$ the displayed error would be of order $L$, so substituting the endpoint into the error estimate would be invalid. An eventual approximation argument reaches the limiting optimizer without making that substitution. [Wang, Theorem 2.2, p. 4](https://arxiv.org/pdf/2609.07918v1).

### 3.1 Reconstruction of the uniformity dependency

The proof first expresses the complex-zero pair sum

$$
F_I(x)=\sum_{\gamma,\gamma'\in I}x^{\rho-\rho'}
\frac4{4-(\rho-\rho')^2}
$$

as a positive integral of an absolute square. Positivity is for the total pair sum in this representation; the individual complex pair terms need not be positive. The identity uses the rational factor and the reflection symmetry of the zeros. [Lemma 2.3, pp. 4–5](https://arxiv.org/pdf/2609.07918v1).

Let $A_I(x,t)$ be the rational zero sum restricted to $I$, and let $A(x,t)$ be its full-zero analogue. Removing the sharp zero restriction while restricting the $t$-integral to $I$ costs $O(xL^3)$, uniformly for $1\le x\le T^\lambda$. This includes leakage at both interval endpoints. Local zero counts control the rational tails. [Lemma 2.4, pp. 5–6](https://arxiv.org/pdf/2609.07918v1).

The explicit formula then decomposes $A$ into a Dirichlet series and elementary terms. The prime coefficients are

$$
a_n=\frac{\Lambda(n)}{\sqrt n}\min\!\left(\frac nx,\frac xn\right).
$$

They obey $\sum a_n^2=\log x+O(1)$ and $\sum n a_n^2\ll x\log^2(2x)$. The Montgomery-Vaughan mean-value bound over an interval of length $H$ therefore yields the required main term $H\log x$ and off-diagonal error $O(H+x\log^2(2x))$. Its error depends on the interval length in exactly the way needed here; it is not a global mean value silently transplanted to a shorter interval. [Lemma 2.5 and proof of Proposition 2.6, pp. 6–8](https://arxiv.org/pdf/2609.07918v1).

The resulting uniform estimate is

$$
F_I(x)=\frac H{2\pi}\left(\frac{L^2}{x^2}+\log x\right)
+O\!\left(H+\frac{HL}{x^2}+\frac{H\sqrt L}{x}
+xL^3+\frac L{\sqrt x}\right),\qquad 1\le x\le T^\lambda.
$$

Substitute $x=T^\alpha$, integrate against the fixed test on $0\le\alpha\le\lambda$, and use evenness. The $L^2/x^2$ term concentrates at $\alpha=0$ and supplies $Lg(0)$ with bounded test-dependent remainder. The prime diagonal supplies $L\int|\alpha|g(\alpha)\,d\alpha$. Integrating $xL^3$ costs $O(T^\lambda L^2)$, since $\int_0^\lambda T^\alpha d\alpha=(T^\lambda-1)/L$. The other displayed errors contribute $O_g(H)$ or smaller for these fixed parameters. This verifies the stated normalized error and the absence of an unproved full-support or higher-correlation premise. [Proposition 2.6 and completion of Theorem 2.2, pp. 6–9](https://arxiv.org/pdf/2609.07918v1).

### 3.2 Relation to the recent BGSTB correction

The September 1 revision of [BGSTB, arXiv:2501.14545v3, Section 3, pp. 6–7](https://arxiv.org/pdf/2501.14545v3) corrects the error formulation in its earlier global Montgomery theorem near $x$ comparable to $\log T$. The corrected global estimate has a separate uniform $O(T\sqrt{\log T})$ allowance. That paper explicitly says the older integrated applications in Lemmas 5 and 7 remain valid.

Wang proves the displayed short-interval estimate with separate error terms, including $H\sqrt L/x$, and integrates those terms explicitly. Thus the transfer audited here depends on Wang's corrected-style direct estimate, not on the discarded overly strong relative-error assertion in the older global theorem. This is a meaningful dependency check, not a claim that every earlier presentation was error-free.

## 4. Exact rational-weight removal

Choose a real even $\eta\in C_c^\infty((-\lambda/2,\lambda/2))$ with $\int\eta^2=1$. Put $f=\eta^2$, $K=\widehat f$, and $Q=f*f$. Then $Q,Q''$ are fixed smooth even functions supported inside $(-\lambda,\lambda)$, and $\widehat Q(z)=K(z)^2$.

The ordinary square is essential. For complex pair differences, $K(z)^2$ cannot be replaced by $|K(z)|^2$. The finite Hilbert operator makes the full sum real and nonnegative, without any termwise claim for nonreal points.

Fourier differentiation gives

$$
\widehat {Q''}(z)=-4\pi^2z^2K(z)^2.
$$

At $z=i(\rho-\rho')L/(2\pi)$ this becomes

$$
\widehat {Q''}(z)=L^2(\rho-\rho')^2K(z)^2.
$$

Consequently the identity

$$
\left(\widehat Q(z)-\frac{\widehat {Q''}(z)}{4L^2}\right)
 \frac4{4-(\rho-\rho')^2}=K(z)^2
$$

holds for every pair. There is no asymptotic replacement of the rational weight by one. Sum the exact identity and apply Theorem 2.2 separately to the two fixed tests to obtain

$$
S_K:=\sum_{\gamma,\gamma'\in I}K(z_\rho-z_{\rho'})^2
=W_I(Q)-\frac{W_I(Q'')}{4L^2}.
$$

The $T$-dependent scalar coefficient is harmless: neither test function depends on $T$, and the theorem is applied before forming their scalar combination. Their main terms are

$$
Q(0)+\int|u|Q(u)du
=\int f^2+\iint|u-v|f(u)f(v)du\,dv=:\mathcal C(f)
$$

and

$$
Q''(0)+\int|u|Q''(u)du
=-\int(f')^2+2\int f^2.
$$

The latter is a finite constant for the fixed smooth density, and its contribution is $O_f(H/L)$, absorbed by $O_f(H)$. It follows that

$$
S_K=\mathcal C(f)\frac{HL}{2\pi}+O_f(H+T^\lambda L^2),
\qquad \frac{S_K}{N(T,H)}\longrightarrow\mathcal C(f).
$$

This is the exact interface used by the new finite-Hilbert argument. [Wang, Lemma 3.1 and its proof, pp. 9–10](https://arxiv.org/pdf/2609.07918v1).

## 5. Sharp density, smoothing, and legal order of limits

Wang minimizes $\mathcal C(f)$ over normalized densities on an interval of length $\lambda$. The limiting density is

$$
f_\lambda(u)=\frac{\cos(\sqrt2u)}{\sqrt2\sin(\lambda/\sqrt2)}
\mathbf1_{[-\lambda/2,\lambda/2]}(u),
\qquad
\mathcal C(f_\lambda)=\frac\lambda2+\frac1{\sqrt2}\cot(\lambda/\sqrt2).
$$

Because its endpoint values do not vanish, this density does not meet the smooth-test hypothesis. To approximate it, take even smooth cutoffs $0\le\chi_\varepsilon\le1$ supported strictly inside the interval and converging to one in the interior. Set

$$
b_\varepsilon=\int\chi_\varepsilon^2 f_\lambda,
\qquad
\eta_\varepsilon=\frac{\chi_\varepsilon\sqrt{f_\lambda}}{\sqrt{b_\varepsilon}},
\qquad f_\varepsilon=\eta_\varepsilon^2.
$$

Then $f_\varepsilon\to f_\lambda$ in $L^1$ and $L^2$, and $\mathcal C(f_\varepsilon)\to\mathcal C(f_\lambda)$. For the stability extension an extra continuity fact is needed:

$$
\sup_{x\in\mathbb R}|\widehat f_\varepsilon(x)-K_\lambda(x)|
\le\|f_\varepsilon-f_\lambda\|_1\longrightarrow0.
$$

All these real kernels have absolute value at most one. Therefore the doubled triple energy $2(K(u)^2+K(v)^2+K(u+v)^2)$ changes by at most $12\|f_\varepsilon-f_\lambda\|_1$, uniformly over the entire real triangle domain. A strict positive energy margin survives sufficiently close fixed smooth approximations. [Wang, Section 4, pp. 10–12](https://arxiv.org/pdf/2609.07918v1).

The density $f_\lambda$ also approaches $f_\theta$ in $L^1$ and $L^2$ as $\lambda\uparrow\theta$. The justified order is:

1. Fix $\theta$, a finite span parameter $R$, a support $\lambda<\theta$, and a smooth approximation.
2. Let $T\to\infty$ using the fixed-test asymptotic.
3. Improve the smooth approximation and let $\lambda\uparrow\theta$ afterwards, keeping a chosen positive energy margin by continuity.

Equivalently, choose a sequence of fixed smooth approximations to $f_\theta$ with support parameters below $\theta$, prove an asymptotic inequality for each member, and then pass to the supremum of their constants. There is no need for estimates uniform in a smoothing parameter or in $\lambda\uparrow\theta$. Allowing either parameter to vary with $T$ would require an additional proof.

## 6. Interface with the finite stability proof

The finite proof uses the full zero multiset directly. For its simple-real Gram matrix $G$, it establishes

$$
S\ge 2N-S_K+D(G),\qquad
D(G)=\operatorname{tr}\Psi(G),
$$

where $\Psi(t)=(t-1)^2$ for $0\le t\le2$ and $\Psi(t)=2t-3$ for $t\ge2$. Nonreal and multiple-real points stay in an indefinite remainder whose positive index is bounded using multiplicity; their mixed kernel terms are not thrown away.

For a uniform lower bound $0<\delta\le1$ on the doubled three-point energy up to span $R$, shifted disjoint triple partitions give

$$
D(G)\ge\frac\delta3\left(S-2-\frac{2X_T}{R}\right).
$$

The factor $1/3$ is justified by averaging three pinched block partitions. It must not be replaced by $1/2$ without a separate stronger spectral inequality. Substituting the audited arithmetic and span limits leads to

$$
\liminf\frac SN\ge
c(\theta)+\frac{\delta\{c(\theta)-2/R\}}{3-\delta}.
$$

It is strictly larger than $c(\theta)$ when $c(\theta)>0$, $R>2/c(\theta)$, and a positive gap persists through smoothing. The experiment proof supplies an explicit positive analytic gap; numerical certification can supply a more useful one. This derivative-free real-kernel continuity is sufficient to retain the finite geometric gain while the original weighted pair sum is evaluated only for smooth fixed tests.

The root obstruction for the cosine kernel is prior art in Ainta's global stability argument. The current contribution under investigation is this complete short-interval transfer and strict improvement of Wang's positive curve, not a new global record or a newly invented stability inequality. The experiment proof separately establishes the stronger finite distinct-point inequality $N^d\ge(3N-S_K+D(G))/2$. Together with the improved simple-real estimate and the same defect, it proves the companion $(1+c_*)/2$. This conclusion depends on that extra finite inequality; it is not inferred by a counting-only substitution.

The final interval certificate uses $\theta=3/4$, $R=21/4$, and doubled triangle energy threshold $d=1/7000$. Its exact conclusion is $c_*=(c(3/4)-2d/(3R))/(1-d/3)=0.4190768284253039967366657875\ldots$, with distinct companion $(1+c_*)/2=0.7095384142126519983\ldots$. The full certificate threshold is reached by first applying the smooth approximation with any fixed $\delta<d$, taking the arithmetic limits, and only then letting $\delta\uparrow d$. The experiment record contains the interval proof tree and an independent Taylor-series evaluator; this audit records their mathematical interface rather than replacing the numerical verifier audit.

## 7. Primary-source novelty sweep and its limits

The search cutoff is September 12, 2026. The sweep included version-pinned arXiv pages and current successor references, the full Wang manuscript, the Lamzouri v2 paper, and the active Ainta/trmdy global refinement lineage. It also inspected the Yang repository's primary issue evidence and the Teal-sea source index to distinguish genuine scope changes from unproved moment transport. Indexed web searches used these exact query families:

- `"2609.07918"`, including exclusions of arXiv and aggregation pages, and `"2609.07918" stability improvement`.
- `"Wang" "short intervals" "zeta" "stability"` and `"Wang" "simple critical zeros" improvement`.
- `"Lamzouri" "short intervals" "improvement"`.
- `"simple critical zeros" "stability"` and `"short intervals" "zeta" "Gram" stability`.
- Exact numerical signatures `"0.550193964744154" zeros`, `"0.419075" "zeros"`, and `"0.550193" "stability"`.
- `"zeta" "short intervals" "cosine" "2026"` and `"short-interval" "Ainta"`.

No primary paper or public proof matching the short-interval stability strengthening was located. Broad `Gram` searches produced many unrelated Gram-point universality papers, which were not treated as evidence for or against this result. The primary Wang result itself was repeatedly retrieved, confirming the same arXiv identifier and version rather than an independent follow-up.

A local `rg` sweep of Markdown, TeX, and Python files in pinned copies of `ainta/zeta-simple-zeros`, `trmdy/zeta-simple-zeros-673137`, and `JoshuaHKU/zeta-0.7947-reproduction` searched `short.intervals`, `Wang`, `2609.07918`, `550193`, `419075`, and power-length theta notation. No matching short-interval extension was found in those snapshots. The Ainta and trmdy pins are respectively `040c5e899e658aed7b56a2a87f501798fe10761d` and `1610b97b7895ff34982260f8dcaf04a0f7b82cf7`.

This supports the wording **apparently new short-interval consequence, after a dated primary-source search**. It does not establish absolute priority, detect unpublished manuscripts, or imply expert acceptance. The source theorem is only days old at this review date. The existing global finite stability and root non-additivity ideas receive explicit attribution, even though the direct finite-Hilbert implementation and the short-interval combination are developed locally.

## 8. Archive and verification boundary

The archive manifest records source URLs, PDF byte counts and SHA-256 digests, page counts, local source paths, version notes, and the version landing-page licenses. The Wang, Lamzouri, and Alpoge-Furman arXiv pages each link the arXiv nonexclusive distribution license. Local research retention and provenance do not convert these texts to the repository's license.

Wang acknowledges using ChatGPT-6 Astra to implement his ideas and states that the author verified, corrected, and rewrote the content and assumes responsibility. This is source-reported process information; it neither establishes nor undermines the mathematical estimates by itself. [Wang, Acknowledgments, p. 12](https://arxiv.org/pdf/2609.07918v1).

Audit performed: full primary mathematical proof read; asymptotic error normalized independently; derivative signs and cancellation reconstructed; zero-coordinate conjugation and interval span checked; smooth-density convergence and legal order of limits derived; current prior-art repositories and searches checked. Not performed by this audit: formal verification of Wang's analytic number theory, independent reproduction of all earlier classical proofs, a computable starting height, or a claim of complete knowledge of all unpublished follow-ups.
