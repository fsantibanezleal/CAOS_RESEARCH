# Riemann-zeta proportion results: primary-source review

Review cutoff: 2026-09-12. This dossier distinguishes published mathematics, new preprints, finite numerical certificates, formal theorem scopes, and unverified higher-moment claims. Companion PDFs, extracted text, and version metadata are inventoried in the source archive manifest. The portable `source-manifest.json` records the persisted locations and integrity hashes. The acquisition set comprises 16 PDFs, 559 pages, and three pinned repository clones. This document is a review, not a claim that all 559 pages received equal line-by-line mathematical scrutiny.

## Findings that change the research baseline

The recent result concerns **simple zeros on the critical line divided by all nontrivial zeros counted with multiplicity**, not RH itself. Its optimized constant is

$$
C_0=\frac32-\frac1{\sqrt2}\cot\frac1{\sqrt2}
=0.67250070367941164573437979080329518859\ldots.
$$

The paired distinct-zero bound is `(1+C0)/2 = 0.8362503518397058...`. The original dyadic statements are asymptotic: every fixed epsilon is eventually admissible, and they do not identify a computable practical starting height. [Claude original, pp. 3–4 and 20–21](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf).

Lamzouri has already supplied the principal simplification requested by the research brief. His second version adds bounds for simple-or-critical zeros and the average of the separate simple and critical proportions. Axiom's second formalization explicitly assumes the two classical analytic inputs in its headline arithmetic statements. This is compatible with an unconditional mathematical proof, since the assumptions are established mathematical theorems, but it differs from an end-to-end formal derivation of those inputs. [Lamzouri v2, Theorem 1.1 and Appendix A](https://arxiv.org/abs/2609.02882v2), [AxiomMath](https://github.com/AxiomMath/ZetaZerosV2).

The most directly useful newer mathematical development is **Biao Wang's September short-interval theorem**, discovered during this review. It makes the same optimization work in every interval `(T,T+T^theta]`, yielding

$$
c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot\frac\theta{\sqrt2},\quad
d(\theta)=\frac{1+c(\theta)}2.
$$

For `theta=3/4`, `c(theta)=0.4190750129754243337...`; positivity begins at `theta0=0.5501939647441547418...`. This is a natural target for an additional finite-geometry stability argument. [Wang, Theorem 1.1, pp. 2–3](https://arxiv.org/abs/2609.07918v1).

## Dated chronology and source versions

| Date | Primary item | What changed / qualification |
|---|---|---|
| 2019 preprint revision, journal 2020 | PRZZ, arXiv:1802.10521v3 | Explicit global proportions `0.417293962` critical and `0.407511457` simple-critical; different counting problems. |
| 2022 journal; arXiv 2019 | Aryan, arXiv:1902.05473 | Unconditional Fejer-kernel variant of pair-correlation arithmetic. |
| 2023-06-07; journal 2024 | BGSTB, arXiv:2306.04799 | Unconditional complex-zero version of Montgomery's formula. |
| 2025-01-24, revised 2025-11-21 | BGSTB, arXiv:2501.14545 | Horizontal zero information under a narrow-box hypothesis. |
| 2025-11 | Goldston–Suriajaya, arXiv:2511.20059 | General double-sum criterion clarifying how simple-critical zeros can follow. |
| 2026-03-30 | Goldston–Suriajaya, arXiv:2603.28104 | Narrow-box direct proof recovering two-thirds when the normalized width tends to zero. |
| 2026-08-10 | Anthropic announcement and supplied 35-page PDF | Initial two-thirds theorem, optimized Montgomery–Taylor constant, extensive exploratory discussion. |
| 2026-08-11 printed PDF; blog updated 2026-08-13 | Replacement 17-page PDF `95c246...` | Shorter presentation; important narrowing of claims concerning the bandwidth-one ceiling. |
| 2026-08-13 arXiv v1; 2026-08-19 arXiv v2 | Alpoge–Furman arXiv:2608.13637 | Responsibility/authorship metadata differs from PDF credited to Claude. Current PDF prints date August 21, which must be preserved separately from the submission timestamp. |
| 2026-08 | ainta and subsequent GitHub drafts | Stability of the rank-inertia step plus finite configurations of 3, 7 and 9 consecutive simple zeros; several candidate constants above `C0`. |
| 2026-08-17 | Yang–Yang, Zenodo:21975237 | `0.7962` claim; self-graded certified candidate, analytic layers incomplete as formalization. Existing serious objection to modulus truncation. |
| 2026-08-25 | teal-sea/Palomar entry 000005 | Claimed registered unconditional 3- and 4-point formal improvements, with larger general certificates conditional; parent task separately audits the registered statements. |
| 2026-09-01 | BGSTB arXiv:2501.14545v3 | Corrects error terms in the older Montgomery theorem. Relevant integrated applications remain valid; this version was reportedly submitted to a journal June 10. |
| 2026-09-02 | Lamzouri arXiv:2609.02882v1 | 14-page Hilbert-space simplification. |
| 2026-09-03 | MPIM special lecture | Primary institutional confirmation of Lamzouri's public presentation. |
| 2026-09-07 | Wang arXiv:2609.07918v1 | 13-page short-interval extension; printed manuscript date September 9. |
| 2026-09-08 | Lamzouri arXiv:2609.02882v2 | 17 pages, adds the simple-or-critical and average-proportion conclusions; printed manuscript date September 9. |

Sources: [PRZZ](https://arxiv.org/abs/1802.10521), [Aryan](https://arxiv.org/abs/1902.05473), [BGSTB 2024](https://arxiv.org/abs/2306.04799), [BGSTB v3](https://arxiv.org/abs/2501.14545v3), [GS 2025](https://arxiv.org/abs/2511.20059), [GS 2026](https://arxiv.org/abs/2603.28104), [Anthropic announcement](https://www.anthropic.com/research/riemann-zeta), [Alpoge–Furman](https://arxiv.org/abs/2608.13637), [MPIM](https://www.mpim-bonn.mpg.de/node/15886), [Wang](https://arxiv.org/abs/2609.07918), [Lamzouri](https://arxiv.org/abs/2609.02882).

## Original proof: dependency map and checks

The revised proof has three independently inspectable interfaces:

1. **Zero geometry.** Build a smoothed band-limited test family and its finite Weil matrix. A critical zero produces a positive rank-one contribution. A reflected off-line pair gives `2m(aa^T-bb^T)` and therefore at most one positive direction. Multiplicity is retained in the zero budget.
2. **Prime arithmetic.** Evaluate the trace and Hilbert–Schmidt square through the explicit formula. A Poisson summation identity collapses the sample-grid sum. Montgomery–Vaughan controls off-diagonal prime frequencies at support at most one.
3. **Finite inequality.** The simple-critical part `P1` and remainder `Q` obey a rank–trace estimate. Combining rank, positive index and moment budgets produces `S >= (2-R(window)-o(1))N`.

The source locations are revised §§2–6, pp. 3–12: smoothing/Poisson at pp. 4–5; linear algebra at pp. 5–6; zero blocks, trace and tail at pp. 6–7; moment calculation pp. 8–11; assembly p. 12. [Revised PDF](https://www-cdn.anthropic.com/95c246936988e43127bc6b2ceb7077c1dad2d68e.pdf).

Independent reconstruction of the crucial geometry: if `v=a+ib`, then `vv^T+bar(v)bar(v)^T=2(aa^T-bb^T)`. Replacing the transpose with conjugate transpose changes this into a positive form and destroys the arithmetic interpretation. Therefore any proposed refinement that sums positive pair energies must explicitly handle the indefinite interaction with the critical part. This is the main adversarial check for all extensions.

For the finite inequality, write `Q=Q+-Q-`. Bounding the mixed trace by von Neumann reduces the negative part to scalar minimization; the positive part is bounded using `(q-2)^2>=0`. The method discards a nonnegative residual measuring how far the simple-zero Gram matrix is from the equality configurations. Keeping that residual is an actual source of new information, whereas rearranging the already optimized scalar inequality cannot improve its constant.

The functional for a normalized nonnegative density `f` on an interval of length `lambda` is

$$
\mathcal C(f)=\int f^2+\iint|u-v|f(u)f(v)\,du\,dv.
$$

Its optimizer is `f_lambda(u)=cos(sqrt(2)u)/(sqrt(2)sin(lambda/sqrt(2)))` on `[-lambda/2,lambda/2]`. If `h=f-f_lambda` has integral zero and `P(u)=integral_{-lambda/2}^u h`, direct integration gives `C(f)-C(f_lambda)=||h||_2^2-2||P||_2^2`. Poincare then proves strict convexity on the affine integral-one slice for `lambda<=1`. This reconstruction explains why an unchanged window-only optimization is saturated, and why a Gram-geometry residual may evade that saturation.

## Corrections and scope qualifications

### Original grid dimension error

The revised PDF §2.2 and current arXiv version define `L=log(T/(2pi))` and `d=floor(LT/(2pi))`, then state `d=N(T,2T)+O(L)`. Their own Riemann–von Mangoldt formula instead implies

$$
N(T,2T)-d=\frac{2\log2-1}{2\pi}T+O(\log T).
$$

The leading coefficient is `0.0614806570607562576...`. Consequently the stated additive estimate is false, while `d/N=1+O(1/log T)` remains correct. This is an independently identified presentation/rate error; it does not by itself refute the asymptotic theorem. Every later use of the stronger estimate should be replaced or audited, particularly finite-height rates.

### Historical denominators

The Anthropic abstract/introduction treats `5/12` as the prior simple-critical record. PRZZ's actual paper distinguishes the two proportions at p. 8 and reports the sharper numerical values at p. 56. A rigorous historical table must use `0.417293962` for critical-line zeros counted with multiplicity and `0.407511457` for simple-critical zeros. Lamzouri v2 p. 2 also makes the distinction. [PRZZ primary PDF](https://arxiv.org/pdf/1802.10521v3).

Lamzouri additionally cites Ki–Lee (2012), Theorem 5, for more than 70% distinct zeros, conflicting with the older `0.6603` record cited by Anthropic. The Ki–Lee primary paper was not recovered in this bounded subreview, so this is a bibliographic discrepancy requiring direct theorem checking, not a verified historical correction.

### Bandwidth ceiling

The approximately `0.68185` figure must not be described as a universal, unqualified ceiling. The revised §7.2 pp. 13–14 uses a finite periodic-law value `p0<=0.6818287` and a correction depending on derivatives of the test function. The displayed error is `2.55e-6*(|r'(1)|+integral|r''|)` once the endpoint value vanishes. The stated bound below `0.6819` applies to the cited windows and a controlled-derivative class. The enclosure hypothesis `EnclOK` was numerically interval-certified rather than kernel-checked at the cited tag. Main theorems are independent of that ceiling certificate. [Revised §7.2](https://www-cdn.anthropic.com/95c246936988e43127bc6b2ceb7077c1dad2d68e.pdf).

### Later extensions in the original arXiv paper

Current arXiv v2 already discusses the zeros of `xi'`, with simple-critical values `0.85838` and an optimized `0.86864` in Remark 7.1, pp. 14–15. The Dirichlet-family average values `0.811` and `0.905` in Remark 7.2 are stated with proof details omitted and excluded from the Lean formalization. These directions therefore cannot simply be called untouched, but a full proof audit of their omitted arithmetic could still be useful. [Alpoge–Furman v2](https://arxiv.org/pdf/2608.13637v2).

### BGSTB correction

BGSTB v3 §3, pp. 6–7 corrects the older Theorem 1's uniform error formulation. At `x=c log T` the previously claimed relative error failed to absorb lower-order dependence on `c`. The corrected theorem adds a uniform `O(T sqrt(log T))` allowance. Footnote 2 explicitly preserves the older integrated Lemma 5 and Lemma 7 applications. The original authors credit Ramunas Garunkstis and Julija Paliulionyte for identifying the issue. This is a real recent correction, not a withdrawal of the proportion result. [BGSTB v3](https://arxiv.org/pdf/2501.14545v3).

## Supplementary improvement claims

### Ainta and trmdy: plausible stability route, precise trust boundary

Pinned snapshots:

- `ainta/zeta-simple-zeros`: `040c5e899e658aed7b56a2a87f501798fe10761d`.
- `trmdy/zeta-simple-zeros-673137`: `1610b97b7895ff34982260f8dcaf04a0f7b82cf7`.

Ainta's argument keeps a convex spectral residual and lower-bounds it using the geometry of 3 or 7 consecutive points. It supplies an analytic nonvanishing proof for three-point kernel energy, then interval-certified quantitative bounds. The claimed seven-point proportion is `0.673008527927...`. The root mechanism is independent of conjectural higher pair correlations: the new information is realizability of the Gram matrix by locations on a line. It remains necessary to audit both the finite verifier and the asymptotic assembly. [Ainta proof](https://github.com/ainta/zeta-simple-zeros/blob/040c5e899e658aed7b56a2a87f501798fe10761d/docs/proof.md).

The live trmdy README has progressed beyond its repository name to a nine-point candidate `0.6733127422722459...`. It explicitly labels the result a record candidate awaiting expert review and an end-to-end formalization; its analytic/window/stability interfaces are not all ported to Lean. Same-day candidate repositories `tawanerguo-cn/zeta-simple-zeros` and `npip99/zeta-zeros` appear in its comparison table. Their numbers are not treated here as established records. [Pinned trmdy](https://github.com/trmdy/zeta-simple-zeros-673137/tree/1610b97b7895ff34982260f8dcaf04a0f7b82cf7).

### Teal-sea / Palomar

The live lab page distinguishes formally registered unconditional three/four-point instances from larger interval-certificate candidates. The four-point headline is `0.672847019766...`; its identified registration is `PALOMAR-2026-08-25-000005`. The site also documents retracted off-line pair refinements and a discovered verifier defect. This is stronger evidence than a numerical README alone, but the exact registered challenge, pinned dependency tree, statement equivalence and kernel axioms must be checked independently. That audit belongs to the parent task's formal-source reviewer. [Lab](https://zeta.teal-sea.com/), [Palomar metadata in source](https://github.com/teal-sea/zeta-lab/blob/main/lean/PALOMAR.md).

### Yang–Yang 79.62%: quarantined analytic claim

The [Zenodo record](https://zenodo.org/records/21975237) explicitly calls this a certified candidate. Finite exact sine-kernel integrals and a rational moment certificate do not establish that those moments describe the actual zeta compression.

There is a concrete existing objection in [repository issue 1](https://github.com/JoshuaHKU/zeta-0.7947-reproduction/issues/1): Proposition 5.3 uses a per-cell decay `ell^-k` to discard moduli above `(log X)^B`, while `ell1` was defined as a fixed trace normalization of size `log T`. The shipped ledger instead carries weights `Lambda(b1)Lambda(b2)/(b1 b2)`. The small-modulus fraction is approximately `(B loglog X/log X)^2`, tending to zero, not one. The text and implementation cited by the issue match the archived paper's §5 p. 17. The critique is pre-existing; it is not a novel result of this review. The fourth-through-sixth-moment claims remain unaccepted here until the missing large-modulus contribution is controlled.

An additional caution is that the major/minor-arc section presents some scale and aggregation estimates as classical while validating them numerically. A finite comparison cannot discharge an arbitrary-height uniform asymptotic. No numerical reproduction of the terminal rational polynomial repairs an earlier missing analytic estimate. The snapshot and issue content are archived so any later correction can be compared rather than silently overwriting this state.

## Proposed novel research target

Combine Wang's short-interval pair-correlation input with a finite Hilbert-space stability residual and the sum-free zero set of the cosine-window kernel. This is more focused than attempting to optimize the global constant against several active preprint repositories. The [Wang transfer audit](2026-09-12-wang-transfer-audit.md) verifies every arithmetic input, normalization, and limiting operation needed here. The independent [experiment proof](../experiments/EXP-002-short-interval-stability/mathematical-proof.md) develops the finite argument and an explicit analytic positive gap.

Let `theta>theta0` and write the baseline as `c_theta=2-C_theta>0`. The verified interface is:

1. Work first with fixed `lambda<theta` and a smooth nonnegative density `f=eta^2` supported strictly inside `(-lambda/2,lambda/2)`. Wang supplies `S_K/N -> C(f)`.
2. The finite stability inequality is `S >= 2N-S_K+D(G)`, where `D(G)=tr Psi(G)` is the spectral defect of the simple-real Gram matrix. The indefinite off-line part remains in the finite proof.
3. Among the consecutive simple-real triples, at most `2X_T/R` have span exceeding `R`, because the sum of their spans is at most twice the total real span `X_T`.
4. Suppose the doubled triangle energy `2(K(u)^2+K(v)^2+K(u+v)^2)` is at least `delta`, with `0<delta<=1`, whenever `u,v>=0` and `u+v<=R`. Averaging the three disjoint pinched triple partitions gives `D(G) >= delta*(S-2-2X_T/R)/3`.
5. As `X_T/N -> 1`, the resulting proportion is at least `c_theta+delta*(c_theta-2/R)/(3-delta)`, strictly above `c_theta` for `R>2/c_theta`.

The factor one third follows from the explicit shifted-partition proof. Earlier exploratory suggestions using a factor one half are superseded and are not retained as a proved bound. This dossier records an apparently new short-interval consequence under active independent mathematical review, not community validation or an end-to-end formal certificate.

For the sharp cosine profile, `K_lambda(x)=integral f_lambda(u) cos(2pi x u) du`. Away from removable exceptional locations, a positive root satisfies `x tan(pi lambda x)=tan(lambda/sqrt(2))/(sqrt(2)pi)`. If `x`, `y`, and `x+y` all satisfied that equation, tangent addition would force `x^2+xy+y^2+c^2=0`, impossible for positive real `x,y,c`. Exceptional cosine or removable-denominator locations are checked separately in the proof. Compactness supplies positive triangle energy on the fixed triangle; the experiment proof strengthens this with an explicit conservative analytic formula. The root non-additivity is already present in Ainta's global argument. The potentially new contribution is its rigorous short-interval application and quantitative certification.

The support and smoothing parameters remain fixed while `T` tends to infinity. The limiting sharp profile at `lambda=theta` is reached afterwards through fixed smooth approximations, using uniform real-kernel convergence. There is no claim of uniformity as `theta` approaches the positivity threshold or a reduction of that threshold. A separately proved finite inequality for distinct points establishes the improved companion `(1+c_star)/2`; the improved simple-critical constant alone would not imply that conclusion by elementary counting.

The completed EXP-002 illustrative certificate uses `theta=3/4`, `R=21/4`, and doubled triangle energy `d=1/7000`. It gives `c_star=0.4190768284253039967366657875...`, compared with Wang's `0.4190750129754243337...`, and distinct companion `0.7095384142126519983...`. The certificate has 48,761 proof-tree nodes and is independently replayed with a Taylor-series kernel evaluator. These finite certifications support the quantitative corollary; the universal strict-improvement argument uses its own explicit analytic positive gap.

## Novelty-search boundary

Primary searches covered the user sources; current arXiv versions and linked references; `Lamzouri + zeta + 2026`; `67.25 + zeros`; correction queries; short-interval `stability`, exact threshold and example-constant queries; and the active GitHub candidate lineage. No primary paper or public proof was located that applies the finite residual/triple-density improvement to Wang's `c(theta)` family. This is evidence supporting a scoped novelty claim, not proof that no such work exists. Wang v1 is only days old at this cutoff.

Global window optimization alone is already saturated. A different basis with the same two moments does not automatically add information. Higher moments require a proved arithmetic transport, not merely an exact random-matrix integral. Extending support beyond one requires new prime correlation control or averaging over an explicitly specified family. GPU use is appropriate for discovery of finite geometric certificates, but exact rational or interval arithmetic must certify the final inequalities.

## Reading coverage and remaining source work

Reviewed the complete 17-page revised core proof; original 35-page statements, extensions, ceiling and verification sections; current 21-page arXiv text and its changed remarks; Lamzouri's statements/appendix; all of Wang's mathematical proof; BGSTB's corrected theorem section; PRZZ's numerical result pages; Ainta's proof outline; trmdy's trust declarations; Yang's moment-transfer and truncation sections plus its existing issue. The 95-page discovery appendix and 116-page transcripts are downloaded and indexed as process evidence, but were not individually line-audited throughout. This dossier does not claim otherwise.

Priority remaining historical sources are Ki–Lee 2012 Theorem 5, Bombieri 2000, the original Montgomery 1973/1975 texts, and exact registered Palomar statements. The parent task's separate Lamzouri and formalization reviews provide deeper coverage of those two central supplied sources.

## Additional bibliography leads

- Carneiro, Chandee, Littmann, Milinovich. *Hilbert spaces and the pair correlation of zeros of the Riemann zeta-function*. J. Reine Angew. Math. 725 (2017), 143–182. [arXiv:1406.5462](https://arxiv.org/abs/1406.5462), [publisher DOI](https://doi.org/10.1515/crelle-2014-0078). Window extremality and reproducing kernels.
- Chirre, Goncalves, de Laat. *Pair Correlation Estimates for the Zeros of the Zeta Function via Semidefinite Programming*. Adv. Math. 361 (2020), 106926. [arXiv:1810.08843](https://arxiv.org/abs/1810.08843). RH-conditional positivity outside unit Fourier support; cannot transfer automatically.
- Goldston, Lee, Schettler, Suriajaya. *Pair Correlation Conjecture ... I: Simple and Critical Zeros*. [arXiv:2503.15449](https://arxiv.org/abs/2503.15449). Full-support PCC yields density one without assuming RH, still not RH.
- Matomaki, Radziwill, Tao. *Correlations of the von Mangoldt and higher divisor functions I. Long shift ranges*. Proc. Lond. Math. Soc. 118 (2019), 284–350. [arXiv:1707.01315](https://arxiv.org/abs/1707.01315), [author explanation](https://terrytao.wordpress.com/2017/07/06/correlations-of-the-von-mangoldt-and-higher-divisor-functions-i-long-shift-ranges/). Averaged shifts are essential; no arbitrary fixed-shift substitution.
- Bombieri. *Remarks on Weil's quadratic functional in the theory of prime numbers, I*. Rend. Lincei Mat. Appl. 11 (2000), 183–233. Negative index/off-line geometry; direct PDF not recovered here.
- Rudnick, Sarnak. *Zeros of principal L-functions and random matrix theory*. Duke Math. J. 81 (1996), 269–322. Essential support qualifications for higher correlations.
- Bui, Heath-Brown. *On simple zeros of the Riemann zeta-function*. Bull. Lond. Math. Soc. 45 (2013), 953–961. RH-conditional `19/27`, using information distinct from the unit-support quadratic route.
- Ki, Lee. *Zeros of the derivatives of the Riemann zeta-function*. Funct. Approx. Comment. Math. 47 (2012), 79–87. Lamzouri cites Theorem 5 as a distinct-zero historical record.
