# Fourier optimization, extremal functions and pair-correlation detectors for simple / critical zeros (with short-interval transplant analysis)

> Research-method note (read first). In this session every full-text fetch was blocked by the network egress proxy (arxiv.org, ar5iv, export.arxiv, alphaxiv, pith.science, zenodo.org, semanticscholar, the anthropic CDN PDF, and university mirrors all returned EGRESS_BLOCKED). All cited findings therefore come from **search-engine snippets** of the primary pages (arXiv abstract/HTML pages, publisher pages, ADS). Where a number comes from a snippet, the snippet was checked against at least one other source or against an independent computation done here. **Two numerical checks were run in this session** (floating-point, not certified), and they reproduce the published constants 0.6725 (Montgomery-Taylor), 0.6727 (Cheer-Goldston) and 0.6792 (Chirre-Gonçalves-de Laat). This is strong evidence that the extremal problems written below are the right ones. Facts I recall but could not confirm with a source in this session are marked **[unverified recollection]** and are also listed under Gaps.

---

## Q1. Classical and 2017-2026 pair-correlation to simple/distinct-zero machinery: which bounds, which optimization problems, which supports?

### Takeaway
All pair-correlation bounds on multiplicities reduce to one linear-fractional Fourier extremal problem: minimize `(r̂(0) + ∫|α| r̂(α)dα) / r(0)` over r ≥ 0 with r̂ supported where F(α) is known (|α| ≤ 1 under RH). The line of improvements runs Montgomery 4/3 (simple ≥ 2/3), then Montgomery-Taylor 1.3275 (0.6725), then Cheer-Goldston (0.6727), then GGOS under GRH using extra F-information on [1, 3/2] (0.6738), then Chirre-Gonçalves-de Laat's Cohn-Elkies class with SDP (0.6792). The 2026 unconditional "simple AND critical" results of Alpöge-Furman/Claude and Lamzouri get exactly the Montgomery / Montgomery-Taylor constants (2/3 and 0.6725, with distinct zeros at 5/6 and 0.8362) without RH. That strongly suggests that every later RH-conditional improvement (Cheer-Goldston, CGdL SDP, GGOS) is a candidate for the same unconditional upgrade.

### Cited Findings
- **Montgomery (1973).** The pair correlation method gave "a short proof that at least 2/3 of zeta-zeros are simple zeros, the first result of its type" (under RH). Source: [Goldston-Suriajaya, Zeta Zeros on the Critical Line, arXiv:2511.20059](https://arxiv.org/abs/2511.20059).
- **Montgomery-Taylor window.** "With the Montgomery–Taylor window the constants become 0.6725 and 0.8362" (simple-and-critical / distinct, in the 2026 unconditional setting). Source: [Alpöge-Furman, arXiv:2608.13637](https://arxiv.org/html/2608.13637v1), and [Lamzouri arXiv:2609.02882](https://arxiv.org/html/2609.02882v1), whose abstract gives "at least 67.25% ... simple and on the critical line, and ... at least 83.62% ... distinct."
- **Cheer-Goldston.** Under RH, "Cheer and Goldston improved to κ* ≥ 0.6727," described as "the previous best result known [by pair correlation] ... 67.27% of the zeros are simple." Source: search snippet of [BGST arXiv:2501.14545 / Goldston et al. 2503.15449](https://arxiv.org/html/2503.15449v4).
- **Conrey-Ghosh-Gonek.** Under RH plus GLH they got simple ≥ 19/27 and distinct κ_d ≥ 0.84568 (mollifier method, not pair correlation). Same source: [arXiv:2503.15449](https://arxiv.org/html/2503.15449v4).
- **Goldston-Gonek-Özlük-Snyder (GGOS, Proc. LMS 2000).** Under GRH for Dirichlet L-functions, `F(α) ≥ 3/2 − α − ε` for `1 ≤ α ≤ 3/2 − ε`. Feeding this extra lower bound beyond α = 1 into the extremal problem gives "67.38% are simple zeros." Sources: [CGdL arXiv:1810.08843](https://arxiv.org/pdf/1810.08843) (snippet); [GGOS, Proc. LMS 80 (2000)](https://academic.oup.com/plms/article-abstract/80/1/31/1529728).
- **Carneiro-Chandee-Littmann-Milinovich (Crelle 725 (2017) 143-182, arXiv:1406.5462).** They give a complete solution, via reproducing kernel Hilbert spaces of entire functions (de Branges spaces), to the problem of optimal bandlimited majorants and minorants of the indicator of [−β, β] that minimize L¹-error *with respect to the pair-correlation measure*. This extends Gallagher (1985), who handled β ∈ (1/2)ℕ with non-extremal functions. It yields bounds for N(β,T)-type counts of pairs of zeros in windows. Source: [arXiv:1406.5462](https://arxiv.org/abs/1406.5462); [Crelle](https://degruyter.com/view/journals/crll/2017/725/article-p143.xml?language=en).
- **Chirre-Gonçalves-de Laat (Adv. Math. 2020, arXiv:1810.08843).** "The key innovation was to replace the usual bandlimited auxiliary functions by the class of functions used in the linear programming bounds developed by Cohn and Elkies for the sphere packing problem, reducing the problems to convex optimization problems that can be solved numerically via semidefinite programming." This improved "the proportion of distinct zeros, counts of small gaps between zeros, and sums involving multiplicities," explicitly N*(T), N_d(T) and N(λ,T). A snippet reports the improved simple-zero-type constant **0.6792**. Sources: [arXiv:1810.08843](https://arxiv.org/abs/1810.08843); [TU Delft portal](https://research.tudelft.nl/en/publications/pair-correlation-estimates-for-the-zeros-of-the-zeta-function-via/); the BGST Acta Arith. snippet ("Under RH ... at least 67.9% ... simple") at [arXiv:2306.04799](https://arxiv.org/html/2306.04799v1).
- **Carneiro-Chandee-Chirre-Milinovich, "A tale of three integrals" (Crelle 786 (2022) 205-243).** The paper studies three integrals: ∫F(α) over bounded intervals; Selberg's integral for primes in short intervals; and the second moment of ζ'/ζ near the line. Each asymptotic is equivalent to the pair correlation conjecture, and under RH the paper "substantially improve[s] the known upper and lower bounds ... by introducing new connections to certain extremal problems in Fourier analysis." Source: [arXiv:2108.09258](https://arxiv.org/abs/2108.09258).
- **Carneiro-Milinovich-Ramos, "Fourier optimization and Montgomery's pair correlation conjecture" (arXiv:2310.01913, 2024).** Under RH, the long-interval average of F(α,T) (conjectured to be 1) lies in **[0.9303, 1.3208]**. The two key ideas are new averaging mechanisms and "the full use of the class of test functions introduced by Cohn and Elkies ... going beyond the usual class of bandlimited functions." The paper also improves the Dirichlet-family analogue. Source: [arXiv:2310.01913](https://arxiv.org/abs/2310.01913).
- **Das-Ismoilov-Ramos, "Fourier optimization and pair correlation problems" (arXiv:2502.05106).** They build a generic framework for pair-correlation (form-factor analogue) bounds for arbitrary sequences satisfying basic assumptions. Source: [arXiv:2502.05106](https://arxiv.org/html/2502.05106).
- **q-analogue (Dirichlet family).** [arXiv:2108.10238, On the q-analogue of the pair correlation conjecture via Fourier optimization](https://arxiv.org/pdf/2108.10238).
- **Small gaps via pair correlation.** Bui-Goldston-Milinovich-Montgomery (Acta Arith. 210 (2023)) show under RH that μ_D < 0.6039 and μ_d ≤ 0.991, with ≫ T^{1−ε} small gaps between distinct zeros. Source: [arXiv:2208.02359](https://arxiv.org/html/2208.02359).
- **Prime gaps via Fourier optimization.** Carneiro-Milinovich-Soundararajan (Comment. Math. Helv. 2019) show under RH that there is a prime in (x, x + (22/25)√x log x], via a new Fourier extremal problem. Sources: [arXiv:1708.04122](https://arxiv.org/abs/1708.04122); [EMS](https://ems.press/journals/cmh/articles/16497). Follow-ups: [arXiv:2411.05095 (Fourier optimization and consequences of GRH, survey)](https://arxiv.org/pdf/2411.05095); [arXiv:2404.08380 (least quadratic non-residue, least prime in AP)](https://arxiv.org/pdf/2404.08380).

### Inferences (including computations done in this session)
- **The master extremal problem (Montgomery-Taylor / Cheer-Goldston form).** Take the multiplicity-weighted pair sum Σ_{γ,γ'} r((γ−γ')L/2π)w(γ−γ') = N·∫F(α) r̂(α)dα, where F(α) = |α| + δ₀-type term + o(1) for |α| ≤ λ. Using r ≥ 0 and dropping off-diagonal pairs:
  `Σ_ρ m_ρ ≤ N · Q(r)`, with `Q(r) = (r̂(0) + ∫_{−λ}^{λ} |α| r̂(α) dα) / r(0)`.
  - Then simple ≥ 2 − Q, because N_s ≥ Σ(2 − m) over zeros counted with multiplicity.
  - Distinct ≥ (3 − Q)/2, because (3m − m²)/2 ≤ 1 for every integer m ≥ 1, with equality at m = 1, 2.
  - Check: Q = 4/3 gives 2/3 and 5/6 (matching Alpöge-Furman's "five sixths distinct"). Q = 1.3275 gives 0.6725 and 0.83625 (matching "0.8362").
- **Montgomery-Taylor as a Rayleigh quotient (reproduced here).** Write r̂ = g ∗ g̃ with supp g ⊂ [−λ/2, λ/2], so r = |ǧ|² ≥ 0 automatically. Then `Q = ⟨g,(I+K)g⟩ / ⟨g,1⟩²` with `K(x,y) = |x−y|`, and min Q = `1/⟨1,(I+K)^{−1}1⟩`. This is a finite, exactly certifiable problem: an integral equation with explicit cot-type solution, or a Gram matrix after discretization. A 1500-point discretization gave:

  | Fourier support λ | Montgomery-Taylor Q_min | simple ≥ | distinct ≥ | Fejér Q = 1/λ + λ/3 |
  |---|---|---|---|---|
  | 1.0 | 1.32750 | 0.67250 | 0.83625 | 1.33333 |
  | 0.8 | 1.51373 | 0.48627 | 0.74313 | 1.51667 |
  | 0.6 | 1.86545 | 0.13455 | 0.56728 | 1.86667 |
  | 0.55 | 2.00058 | −0.0006 | 0.49971 | 2.00152 |
  | 0.534 | 2.04980 | −0.0498 | 0.47510 | 2.05066 |

  So the pure first-moment method has a positivity threshold of **λ\* ≈ 0.55019** (Montgomery-Taylor), against 3 − √6 ≈ 0.55051 for Fejér. The research program's threshold θ ≥ 0.534 is therefore already below the whole classical bandlimited family. Its gain comes from the parity/Hilbert product inequality (a second-order ingredient), not from the kernel choice.
- **Cohn-Elkies relaxation (reproduced here by LP).** The relaxation allows r̂ to extend beyond [−λ, λ] provided r̂ ≤ 0 there (valid because F(α) ≥ 0 for all α), keeping r ≥ 0. An LP discretization (piecewise-linear r̂ on [0, 2.5λ], r ≥ 0 checked on a grid up to 40/λ; not rigorous) gave:
  - λ = 1: Q = 1.32071, i.e. simple ≥ **0.6793**. This matches CGdL's 0.6792.
  - The bandlimited LP gave Q = 1.32731, i.e. **0.6727**, matching Cheer-Goldston.
  - λ = 0.6: 1.86061 (simple ≥ 0.1394).
  - λ = 0.55: 1.99609 (simple ≥ 0.0039).
  - λ = 0.534: 2.04544.
  - The Cohn-Elkies threshold for pure first-moment positivity is therefore about **λ ≈ 0.5487**, against 0.5502 for bandlimited kernels.
  - Lesson: at small support the Cohn-Elkies gain is roughly 0.0015 in threshold and about 0.004 in proportion. It is useful but much smaller than the gain at λ = 1 (0.0067).
- **GGOS-type information is what moves thresholds.** The big gains come from *new information on F*, not from better kernels. Examples: a lower bound F(α) ≥ 3/2 − α beyond the support (GGOS), or Tsang/Goldston-type lower bounds on averages of F. The short-interval analogue would be any lower bound for F_θ(α) with α slightly above θ, for example from a Goldston-Gonek-type argument with primes in short progressions or a Selberg-integral lower bound in short windows. Heuristically such a bound would move λ\* the way GGOS moved 0.6727 to 0.6738.

### Gaps
- Exact CGdL theorem statements (the precise N*(T), N_d(T), N(λ,T) constants, and whether 0.6792 is the "simple" or a "Σm" derived number) could not be read. Full text blocked; only the snippet value 0.6792 is confirmed, and my LP reproduces it for the simple-zero problem.
- CCLM's exact numerical outputs, e.g. N*(T) bounds and specific N(β,T) values, and the tale-of-three-integrals numerical intervals, could not be retrieved.
- **[unverified recollection]** CCLM's Hilbert space is the de Branges space of bandlimited functions with norm weighted by the pair-correlation density 1 − (sin πx/πx)²; the reproducing kernel of that space gives the extremal majorants.

---

## Q2. What is unconditional, or can be made unconditional in short intervals with a support-λ < θ pair-correlation theorem?

### Takeaway
Since 2023 Goldston and coauthors have systematically removed RH from Montgomery's method. In 2026 two lines landed. First, Alpöge-Furman/Claude and then Lamzouri got an **unconditional** 2/3 (0.6725 with Montgomery-Taylor) proportion of zeros that are simple **and** critical, and 5/6 (0.8362) distinct. Second, Wang transplanted this to short intervals (T, T+T^θ] with an unconditional Montgomery theorem of support below θ. Wang has since refined Lamzouri's method slightly (arXiv:2609.24167). Every purely "F-linear" improvement (Cheer-Goldston, Cohn-Elkies/SDP) should transplant verbatim to support λ < θ, provided the short-interval F_θ is a nonnegative form factor.

### Cited Findings
- **Baluyot-Goldston-Suriajaya-Turnage-Butterbaugh (Acta Arith. 2024, arXiv:2306.04799).** An unconditional Montgomery theorem. If every zero with T^{3/8} < γ ≤ T satisfies |β − 1/2| < 1/(2 log T), then ≥ **61.7%** of these zeros are simple. "The method of proof neither requires nor provides any information on whether any of these zeros are or are not on the critical line." Source: [arXiv:2306.04799](https://arxiv.org/abs/2306.04799); [Acta Arith.](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/online/115529/an-unconditional-montgomery-theorem-for-pair-correlation-of-zeros-of-the-riemann-zeta-function).
- **BGST, "Pair Correlation of Zeros I: Proportions of simple zeros and critical zeros" (arXiv:2501.14545, revised 2026).** The pair-correlation method proves "at least 2/3 of zeros are simple, and yields at least 2/3 of the zeros on the critical line," and 1/3 simple and critical. This is shown under hypotheses weaker than RH. Source: [arXiv:2501.14545](https://arxiv.org/abs/2501.14545).
- **Goldston-Lee-Schettler-Suriajaya (arXiv:2503.15449).** Montgomery's pair correlation *conjecture* implies, without RH, that 100% of zeros are simple and on the critical line. Part II (arXiv:2507.06823, J. Number Theory 2026) treats the Alternative Hypothesis. Sources: [2503.15449](https://arxiv.org/html/2503.15449v4); [2507.06823](https://arxiv.org/abs/2507.06823).
- **Goldston-Suriajaya, "Zeta zeros on the critical line" (arXiv:2511.20059; Analysis Math. 2026).** "If RH could be removed from Montgomery's simple zero proof, then this would also give a proof that 2/3 of the zeros are simple and on the critical line." Source: [arXiv:2511.20059](https://arxiv.org/abs/2511.20059); [Springer](https://link.springer.com/article/10.1007/s10476-026-00186-w).
- **Alpöge-Furman (arXiv:2608.13637, Aug 2026).**
  - Unconditionally, at least two thirds of nontrivial zeros, counted with multiplicity, are simple and on the critical line, and at least five sixths are distinct. With the Montgomery-Taylor window these become ≈ 0.6725 and 0.8362.
  - The same holds for L(s, χ) for fixed primitive χ, and a Lean 4 formalization accompanies the paper.
  - The argument was discovered by an internal Claude model and verified by the authors.
  - Method: "a finite-dimensional matrix representation of Weil's Hermitian form and a rank-trace inequality for Hermitian matrices, with a second moment calculation over the zeros using the explicit formula."
  - Sources: [arXiv:2608.13637](https://arxiv.org/html/2608.13637v1); Lamzouri's abstract at [2609.02882](https://arxiv.org/html/2609.02882v1).
- **Lamzouri (arXiv:2609.02882, 3 Sep 2026).** A new, shorter proof with the same constants (67.25%, 83.62%). It "replac[es] the entire finite-dimensional matrix framework by a Hilbert space inequality, which allows for a direct application of Montgomery's theorem on the pair correlation." Source: [arXiv:2609.02882](https://arxiv.org/abs/2609.02882).
- **Wang (arXiv:2609.07918).** Uses Lamzouri's method to bound simple-critical and distinct zeros in (T, T+H], H = T^θ with 0 < θ < 1 fixed. The paper establishes "Montgomery's theorem on the pair correlation of zeros ... in short intervals and then uses Lamzouri's inequality on finite multisets of complex numbers that are invariant under complex conjugation." Source: [arXiv:2609.07918](https://arxiv.org/pdf/2609.07918).
- **Wang (arXiv:2609.24167), "Proportions of the non-trivial zeros of the Riemann zeta function."** "By refining Lamzouri's method, the paper slightly improves the bounds" 67.25% / 83.62%. Exact new constants were not visible in the snippet. Source: [arXiv:2609.24167](https://arxiv.org/html/2609.24167).
- **Related follow-ups (Zenodo, not peer reviewed).**
  - "A stability refinement for simple critical zeros in short intervals" claims refinements of Wang's bounds that are "strictly positive for each fixed exponent theta above the unique positive-proportion threshold of the cosine bound." [Zenodo 22727389](https://zenodo.org/records/22727389).
  - Further Zenodo records: "stability, parity, localization, Hilbert compression, and spectral defect" [22860012](https://zenodo.org/records/22860012) and [22851518](https://zenodo.org/records/22851518).
  - "A 67.92% Bound for Simple Critical Zeros in a Vanishing Vertical Box" [Zenodo 21879591](https://zenodo.org/records/21879591). This is apparently a CGdL-constant transplant under a zero-localization hypothesis. These may be the research program's own outputs and are unrefereed.

### Inferences
- **Why the 2026 constants equal the RH constants.** Lamzouri's Hilbert inequality consumes F(α) linearly, through the same test-function functional as Montgomery. Off-line zeros come in conjugate-symmetric pairs (β ± …) that behave like "double" contributions in the multiset inequality. So one zero-counting functional penalizes both multiplicity and off-line location, and the RH hypothesis is replaced by a parity/symmetry argument. On this reading, **any kernel improvement valid under RH is valid unconditionally for simple-critical zeros**, as long as it only uses r ≥ 0, supp r̂ ⊂ [−λ, λ] and F's asymptotics. That covers Cheer-Goldston (0.6727) and the Cohn-Elkies relaxation (0.6792, CGdL), provided the Hilbert inequality accepts kernels whose r̂ is not compactly supported but is ≤ 0 outside. This must be checked: the Lamzouri/Weil-form framework may require r̂ compactly supported so that the explicit formula has a finite prime sum. Cohn-Elkies r̂ with a negative tail over |α| > λ is fine for Montgomery's F (F ≥ 0 everywhere), but in the explicit-formula route F must be *defined* beyond the support. The Zenodo "67.92%" record suggests someone has done this under an extra localization hypothesis.
- **Short-interval transplant, first-moment level.** With support λ = θ, the pure Montgomery-Taylor threshold is θ\* ≈ 0.5502 and the Cohn-Elkies threshold is ≈ 0.5487 (computed above). The program's 0.534 already uses the second-order product inequality. The Cohn-Elkies relaxation should push the program's own threshold down by a comparable ~0.001-0.002, if its product inequality is linear in the kernel functional.
- **What unconditional short-interval information exists beyond α < θ?** Only upper-bound-type information such as F ≥ 0 and trivial Tauberian limits. A GGOS-type lower bound F_θ(α) ≥ c(α) for α ∈ [θ, θ + η] needs GRH-type prime equidistribution in short intervals, so it is presumably not available unconditionally. A Selberg-integral or Montgomery-Soundararajan type second moment for primes in (x, x + x^θ] would supply it conditionally.

### Gaps
- Wang's explicit constants as functions of θ, and whether his threshold is exactly the Montgomery-Taylor/cosine λ\* ≈ 0.55. The Zenodo abstract mentions "the unique positive-proportion threshold of the cosine bound," consistent with ≈ 0.55 but not confirmed.
- Whether Lamzouri's inequality needs compact Fourier support (decisive for the Cohn-Elkies/SDP transplant).
- Wang 2609.24167's improved constants.

---

## Q3. 2024-2026 results using SDP, LP bounds or machine-learned test functions for zeta zeros

### Takeaway
SDP/Cohn-Elkies Fourier optimization is now the standard engine: CGdL 2020; Carneiro-Milinovich-Ramos 2024; Gonçalves-de Laat-Leijenhorst 2024 for multiplicities via n-level correlations, which used clustered low-rank SDP solvers; Das-Ismoilov-Ramos 2025. I found no published use of machine-learned test functions for zeta-zero proportions. The 2026 Claude-discovered proof uses a finite Weil-form/Gram matrix plus a rank-trace inequality, not learned test functions.

### Cited Findings
- **Gonçalves-de Laat-Leijenhorst, "Multiplicity of nontrivial zeros of primitive L-functions via higher-level correlations" (arXiv:2303.01095; Math. Comp. 94 (2025)/online 2024).** They give universal bounds on the fraction of zeros of given multiplicity for L-functions of cuspidal automorphic representations of GL_m/ℚ. Method: "the higher-level correlation asymptotic of Hejhal and Rudnick & Sarnak in conjunction with semidefinite programming bounds." Source: [arXiv:2303.01095](https://arxiv.org/abs/2303.01095).
- **Solver technology.** "Solving clustered low-rank semidefinite programs arising from polynomial optimization" (Leijenhorst-de Laat, Math. Prog. Comp. 2024) is the solver line associated with these bounds. Source: [Springer](https://link.springer.com/article/10.1007/s12532-024-00264-w).
- **Pair correlation for Dedekind zeta of abelian extensions** (de Laat-Rolen et al., arXiv:1908.04876): the same Fourier optimization in number fields. Source: [arXiv:1908.04876](https://arxiv.org/abs/1908.04876).
- **Carneiro-Milinovich-Ramos 2024**: the Cohn-Elkies class gives average-F bounds of [0.9303, 1.3208] (see Q1). Source: [arXiv:2310.01913](https://arxiv.org/abs/2310.01913).
- **Sign uncertainty (2025)**: "Fourier inequalities and sign uncertainty" (arXiv:2505.15994) improves the Bourgain-Clozel-Kahane lower bound in high dimensions and can match Torquato-Stillinger bounds for the Cohn-Elkies LP. Carneiro and Quesada-Herrera study a generalized sign uncertainty principle ([arXiv:2006.00959](https://arxiv.org/pdf/2006.00959)). Source: [arXiv:2505.15994](https://arxiv.org/pdf/2505.15994).
- **Finite Weil-form and certified-positivity preprints (2026, not refereed, relevant as certificate technology):**
  - "A finite Guinand-Weil dictionary and archimedean tail order for the truncated Weil quadratic form" [arXiv:2607.02828](https://arxiv.org/pdf/2607.02828).
  - "Weil positivity in compact windows: a finite reduction, certified two-sided bounds, and a Landau-Widom decay law" [arXiv:2608.24827](https://arxiv.org/pdf/2608.24827).
  - "Construction of Finite Hilbert-Pólya Matrices from Weil's Explicit Formula" [arXiv:2609.04908](https://arxiv.org/pdf/2609.04908).
  - "Simple and distinct zeros in a prime-modulus Dirichlet family from near-microscopic to polylogarithmic heights" [arXiv:2608.16034](https://arxiv.org/pdf/2608.16034).
- **Pearce-Crump (arXiv:2609.15329)** optimizes the arithmetic mean value in Zhuravlev's 1974 quantitative form of Selberg's method. The mean value has "an exact closed form for reciprocal-square-root coefficients" and is "improved further by a positive-semidefinite family of mollifiers," giving ≥ 7% of zeros on the line. This is the strongest result yet from Selberg's method. Source: [arXiv:2609.15329](https://arxiv.org/abs/2609.15329).

### Inferences
- A PSD-mollifier family (Pearce-Crump) is a finite SDP in the mollifier coefficients. The Montgomery-Taylor problem is a finite Gram quotient. The Cohn-Elkies relaxation is an LP/SDP. All three are therefore certifiable by rational/interval-arithmetic dual certificates, as in de Laat's sphere-packing and energy work. The natural "master" program is a **joint SDP**: kernel r (Cohn-Elkies class, sum-of-squares certified positivity of r and sign of r̂ outside the support) plus the product/parity inequality as a Schur-complement constraint.
- ML-found test functions are not needed for these one-dimensional problems. They are solved to high precision by SDP. ML might help only in higher-level (n ≥ 3) correlation problems, where the function space is multivariate.

### Gaps
- No source found for machine-learned test functions in zeta-zero proportion problems (2024-2026).
- The numerical bounds in Gonçalves-de Laat-Leijenhorst (e.g. the simple-zero fraction for GL_1, GL_2, GL_3 via 2-, 3-, 4-level correlation) could not be extracted.

---

## Q4. Triple / n-level correlation with restricted support: used for multiplicities? Would a three-point input improve a two-point Hilbert-parity product?

### Takeaway
Yes, n-level correlations have been used for multiplicities. Gonçalves-de Laat-Leijenhorst apply the Hejhal/Rudnick-Sarnak n-level asymptotics (support Σ|u_i| < 2) with SDP to bound fractions of zeros of each multiplicity for GL_m L-functions. For ζ (m = 1), the 2-level support [−1, 1] under RH is already stronger per level than what n-level can add at fixed total support, and I found no zeta-specific improvement over CGdL from triple correlation. In short intervals no unconditional n-level theorem exists, so a three-point input would need a new short-interval Rudnick-Sarnak theorem.

### Cited Findings
- Rudnick-Sarnak proved that zeta zeros have the same n-correlation as unitary matrices "provided that the test function had a Fourier transform with limited support," specifically `|ξ₁| + … + |ξ_n| < 2` (with Hejhal for n = 3). Sources: [search summary of Rudnick-Sarnak, Duke 1996](https://www.math.tau.ac.il/~rudnick/papers/nlevelDuke.pdf); [Rudnick publications](https://www.math.tau.ac.il/~rudnick/pub.html); ["In support of n-correlation" arXiv:1212.5537](https://arxiv.org/pdf/1212.5537).
- Universal multiplicity bounds for GL_m come from higher-level correlations plus SDP (Gonçalves-de Laat-Leijenhorst). Source: [arXiv:2303.01095](https://arxiv.org/abs/2303.01095).
- The Rudnick-Sarnak n-level results for principal L-functions are for GL_m; for m ≥ 2 the pair-correlation support shrinks (to 2/m), which is why higher levels help there. Source: [Rudnick-Sarnak Duke paper](https://www.math.tau.ac.il/~rudnick/papers/nlevelDuke.pdf) (support restriction verified via snippet; the 2/m form is **[unverified recollection]**).

### Inferences
- **Mechanism for multiplicities.** For a zero of multiplicity m, the k-point diagonal sum contributes m^k. With a k-level kernel R ≥ 0, the k-point sum ≥ Σ m^k R(0), and the k-level form factor gives an upper bound on Σ_ρ m_ρ^{k−1}. Knowing E[m^{k−1}] for several k constrains the multiplicity distribution much more tightly than E[m] alone, via a moment problem that is itself an LP over distributions on {1, 2, 3, …}. Example: if Σm ≤ Q₁N and Σm² ≤ Q₂N, then simple ≥ max over LP duals of combinations a + b·m + c·m² ≤ 1_{m=1}.
- **For the parity/Hilbert product (Q−S)(N−O) ≥ 2(N−S)².** This is a Cauchy-Schwarz/Hilbert-type second-order inequality. A three-point input would add information on Σ m² (or on the "Q" variable directly), which could tighten the product. The product inequality looks like the Cauchy-Schwarz instance of the moment LP just described, so a 3-level upper bound on Σ_ρ m_ρ² is exactly the type of input that improves it. **But** at total support Σ|u_i| < θ (short-interval analogue), each variable has effective support around θ/2 in the relevant directions. Numerically the 3-level information at small support is weak, and it is not clear it beats the 2-level information at support θ.
- The short-interval version of Rudnick-Sarnak (n-level in (T, T+T^θ], Σ|u_i| < θ?) would need to be proved. It is plausible by the same method as Wang's two-level short-interval theorem (a mean value for Dirichlet polynomials over short intervals), but I found no source.

### Gaps
- No paper found that uses triple correlation to improve ζ's simple-zero proportion beyond CGdL 0.6792 (RH).
- No short-interval n-level correlation theorem found.
- Exact numbers from GdLL were unavailable (full text blocked).

---

## Q5. Kernel positivity / energy / Hilbert-type inequalities from other fields that give sharper finite inequalities

### Takeaway
The directly relevant transplantable tools are:
1. **Cohn-Elkies LP class**, already shown here to reproduce CGdL, with only a small gain at support ≈ 0.53-0.55.
2. **de Branges/RKHS extremal majorants** (CCLM) for window-count functionals.
3. **Montgomery-Vaughan weighted Hilbert inequality and its extremal functions** (Carneiro-Littmann; the optimal-constant question was reopened by Rodgers 2026: the optimal constant is strictly larger than π).
4. **Hilbert-transform extremal problems** (Carneiro-Das-Florea-…-Wang 2021).
5. **Fourier interpolation with zeta zeros** (Bondarenko-Radchenko-Seip), the Radchenko-Viazovska-type route to certificates of sharpness.

Universal optimality (Cohn-Kumar-Miller-Radchenko-Viazovska) and potential-theoretic energy minimization are conceptually adjacent. I found no application of them to zeta-zero proportions.

### Cited Findings
- **Carneiro-Littmann** give optimal one-sided exponential-type majorants for the signum function and a Fourier-analysis proof of the weighted Hilbert (Montgomery-Vaughan) inequality. Source: search summary at [arXiv:2104.00105 context](https://arxiv.org/abs/2104.00105). Related: "Monotone extremal functions and the weighted Hilbert's inequality" [arXiv:2302.14658](https://arxiv.org/abs/2302.14658), and "On the Montgomery-Vaughan weighted generalization of Hilbert's inequality" [arXiv:2203.14950](https://arxiv.org/abs/2203.14950) (Proc. AMS Ser. B 2023).
- **Rodgers (arXiv:2608.12315, 12 Aug 2026).** If the Montgomery-Vaughan weighted Hilbert inequality holds for all N ≥ 2 with constant C, then C > π, and an explicit α₀ > π is a lower bound. This disproves the conjectured optimal constant π. Source: [arXiv:2608.12315](https://arxiv.org/pdf/2608.12315).
- **Carneiro, Das, Florea, Kumchev, Malik, Milinovich, Turnage-Butterbaugh, Wang (JFA 281 (2021)).** They connect the Erdős-Turán discrepancy inequality to an extremal problem on maxima of Hilbert transforms and improve its bounds. Source: [arXiv:2104.00105](https://arxiv.org/abs/2104.00105).
- **Bondarenko-Radchenko-Seip (Constr. Approx. 57 (2023) 405-461, arXiv:2005.02996).** They construct Fourier interpolation bases for functions analytic in a strip, with nodes built from nontrivial zeros of ζ and L-functions. A duality principle relates the bases to kernels of general Dirichlet series with meromorphic continuation and a functional equation, and modular integrals for the theta group appear. Source: [arXiv:2005.02996](https://arxiv.org/abs/2005.02996); [Springer](https://link.springer.com/article/10.1007/s00365-022-09599-w).
- Kulikov, "Fourier interpolation and time-frequency localization" [arXiv:2005.12836](https://arxiv.org/pdf/2005.12836), studies the density limits of interpolation sets.
- The Cohn-Elkies sphere-packing function class is exactly the class CGdL and Carneiro-Milinovich-Ramos imported. Sources: [arXiv:1810.08843](https://arxiv.org/abs/1810.08843); [arXiv:2310.01913](https://arxiv.org/abs/2310.01913).

### Inferences
- **Hilbert inequality ↔ parity product.** Lamzouri's finite Hilbert inequality on conjugation-invariant multisets is a Hilbert-type bilinear inequality. Its sharp constant and extremizers (Montgomery-Vaughan type, now known *not* to have constant π in the weighted case per Rodgers) matter directly. If the program's product inequality uses a Hilbert-type constant, **a sharper finite (N-dependent) constant or a spectral refinement** is a concrete lever. Candidates: the largest eigenvalue of the finite Hilbert matrix 1/(λ_i − λ_j), whose sharp asymptotics are known for the classical case; or de Carli/Carneiro-Littmann majorant-based proofs, which give explicit kernels.
- **Sharpness certificates.** The Montgomery-Taylor problem at support λ has an explicit extremal kernel. Its dual (a measure supported where equality holds) certifies optimality within the first-moment class. Beating the class needs either new F-information or a second-order (product/Hilbert) inequality. This is the same dichotomy as in sphere packing: LP bound versus 3-point SDP bound (de Laat-Oliveira-Vallentin). **The 3-point SDP analogue for zeros is exactly a triple-correlation/Hilbert product constraint** (see Q4).
- **Energy / universal optimality.** In Cohn-Kumar universal optimality, a configuration minimizes energy for all completely monotone potentials via a "magic" interpolation function. The analogue here would be a kernel that is simultaneously optimal for all multiplicity functionals (simple, distinct, Σm). For the one-dimensional Montgomery-Taylor family, the λ = 1 kernels for simple and distinct zeros coincide (both depend only on Q), so there is nothing to gain. This is background inference; no source was found.

### Gaps
- No source found applying Cohn-Kumar universal optimality, Riesz energy minimization or potential theory to zeta-zero proportions.
- The exact form of the "Anthropic/Alpöge-Furman cosine kernel Gram matrix" could not be read. Only the abstract-level description (finite Weil Hermitian form matrix plus rank-trace inequality) was available.

---

## Q6. Zero statistics via Hankel/Toeplitz or RKHS spectral problems with computable certificates

### Takeaway
The live connections are:
- the finite Weil Hermitian form (a Toeplitz/Gram-type matrix built from the explicit formula) with the rank-trace inequality `rank(A) ≥ (tr A)² / tr(A²)` (Alpöge-Furman);
- de Branges spaces and reproducing kernels (CCLM);
- 2026 preprints on finite truncations of Weil's quadratic form with certified two-sided bounds and a Landau-Widom (prolate/Slepian concentration) eigenvalue law.

These are all computable-certificate frameworks.

### Cited Findings
- Alpöge-Furman use a finite-dimensional matrix representation of Weil's Hermitian form plus a rank-trace inequality for Hermitian matrices, with a second moment over zeros from the explicit formula. Source: [arXiv:2608.13637](https://arxiv.org/html/2608.13637v1); Lamzouri abstract [2609.02882](https://arxiv.org/html/2609.02882v1).
- "Weil positivity in compact windows: a finite reduction, certified two-sided bounds, and a Landau-Widom decay law" [arXiv:2608.24827](https://arxiv.org/pdf/2608.24827). "A finite Guinand-Weil dictionary and archimedean tail order for the truncated Weil quadratic form" [arXiv:2607.02828](https://arxiv.org/pdf/2607.02828). "Construction of Finite Hilbert-Pólya Matrices from Weil's Explicit Formula" [arXiv:2609.04908](https://arxiv.org/pdf/2609.04908).
- CCLM solve the pair-correlation majorant problem in reproducing kernel Hilbert spaces of entire functions. Source: [arXiv:1406.5462](https://arxiv.org/abs/1406.5462).

### Inferences
- **Rank-trace = distinct-zero detector.** Take A = Σ_ρ v_ρ v_ρ^* for vectors v_ρ = (x^{iγ})_x over a finite frequency set, i.e. a Gram/Toeplitz matrix of the zeros. Then rank(A) ≤ #distinct zeros, and (tr A)²/tr(A²) is exactly the pair-correlation quotient N²/(N·Q). This recovers N_d ≥ N/Q, weaker than (3 − Q)/2. So the Claude proof must use a sharper finite inequality, e.g. a rank-trace bound applied after projecting out the conjugation-paired off-line zeros.
- **Landau-Widom connection.** For a short interval of length H = T^θ and frequency support λ, the Weil form restricted to the window is a time-frequency concentration operator with about λ·(window count) eigenvalues near 1 and a plunge region of log width. The Landau-Widom count of "effective degrees of freedom" is a natural upper bound on how much any Gram/rank method can see. This might explain why thresholds cluster near θ ≈ 1/2 (support times window ≈ half the zero count). This is a heuristic, not sourced.
- **Certificates.** The Montgomery-Taylor Gram quotient `1/⟨1,(I+K)^{−1}1⟩` can be certified with interval arithmetic on a finite-element discretization plus an explicit continuous extremal. The Cohn-Elkies LP needs SOS certificates of r ≥ 0 on ℝ and r̂ ≤ 0 on |α| ≥ λ (as in Cohn-Elkies / de Laat numerics).

### Gaps
- The precise definitions of the finite Weil matrices in 2608.24827 and 2609.04908, and whether their certified bounds give zero-proportion information, are unknown (full text blocked).
- No source was found for Hankel-operator spectral formulations of multiplicity bounds.

---

## Summary table of constants (as confirmed in this session)

| Result | Hypothesis | Support / info on F | Simple (or simple+critical) | Distinct | Source |
|---|---|---|---|---|---|
| Montgomery 1973 | RH | [−1,1], Fejér | ≥ 2/3 | ≥ 5/6 (derived) | [2511.20059](https://arxiv.org/abs/2511.20059) |
| Montgomery-Taylor | RH | [−1,1], optimal g∗g̃ | 0.6725 | 0.8362 | [2608.13637](https://arxiv.org/html/2608.13637v1) |
| Cheer-Goldston | RH | [−1,1], general r ≥ 0 | 0.6727 | - | [2503.15449](https://arxiv.org/html/2503.15449v4) |
| GGOS 2000 | GRH | + F ≥ 3/2 − α on [1, 3/2] | 0.6738 | - | [1810.08843](https://arxiv.org/pdf/1810.08843) |
| CGdL 2020 | RH | Cohn-Elkies class, SDP | 0.6792 | improved (value not retrieved) | [1810.08843](https://arxiv.org/abs/1810.08843) |
| Conrey-Ghosh-Gonek | RH + GLH | mollifier (not pair correlation) | 19/27 | 0.84568 | [2503.15449](https://arxiv.org/html/2503.15449v4) |
| BGST 2024 | zeros in \|β−1/2\| < 1/(2 log T), T^{3/8} < γ ≤ T | unconditional Montgomery theorem | 0.617 | - | [2306.04799](https://arxiv.org/abs/2306.04799) |
| Alpöge-Furman 2026 | none | Weil form + rank-trace | 2/3 simple+critical (0.6725 with MT) | 5/6 (0.8362) | [2608.13637](https://arxiv.org/html/2608.13637v1) |
| Lamzouri 2026 | none | Hilbert inequality + Montgomery | 0.6725 simple+critical | 0.8362 | [2609.02882](https://arxiv.org/abs/2609.02882) |
| Wang 2026 | none | short interval T^θ, support < θ | θ-dependent (not retrieved) | θ-dependent | [2609.07918](https://arxiv.org/pdf/2609.07918) |
| Wang 2026b | none | refined Lamzouri | slightly > 0.6725 (value not retrieved) | slightly > 0.8362 | [2609.24167](https://arxiv.org/html/2609.24167) |
| Pearce-Crump 2026 | none | Selberg/Zhuravlev + PSD mollifiers | ≥ 7% critical | - | [2609.15329](https://arxiv.org/abs/2609.15329) |

Computed here (floating point, not certified; scripts `../scripts/montgomery_taylor_quotient.py` and `../scripts/cohn_elkies_relaxation.py`). Pure first-moment positivity thresholds in the support λ are **0.55051** (Fejér), **0.55019** (Montgomery-Taylor) and **≈ 0.5487** (Cohn-Elkies relaxation). At λ = 1 the same code reproduces 0.67250 (MT), 0.67269 (CG) and 0.67929 (CGdL).
