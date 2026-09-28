# Cross-field reformulations of RH and zero-location statements: 2020-2026 progress and finite, certifiable experiments

Scope note: gathered 2026-09-27. arxiv.org, alphaxiv.org and alainconnes.org were blocked by the network proxy in this session, so arXiv abstracts come from search-engine snippets and from secondary pages (anthropic.com, Springer, Cambridge, ResearchGate), not full-text reads. Where a claim rests only on a snippet, it says so. Credibility tags used below:
- **[EST]**: established and refereed.
- **[EXP]**: preprint by known experts.
- **[NEW/UNK]**: recent preprint by an author I could not place; unrefereed.
- **[FRINGE]**: excluded.

**The biggest 2026 news, and the most relevant to "a finite certificate that links to zero proportions":** in August-September 2026, a *finite compression of Weil's Hermitian form*, combined with a rank/inertia argument, made Montgomery's pair-correlation deduction unconditional. This lifted the proportion of simple zeros on the critical line from 5/12 to more than 2/3 (0.6725). Short-interval versions followed within weeks. See Q2 and Q9.

---

## Q1. Operator / spectral realizations (Connes, CCM prolate, Berry-Keating/Sierra, BBM, de Branges/Lagarias/Burnol/Suzuki)

### Takeaway
The live spectral program is Connes-Consani-Moscovici (CCM):
- It builds a prolate wave operator and then (2025-2026) "zeta spectral triples": self-adjoint rank-one perturbations of the scaling operator on [λ⁻¹, λ], built only from the Euler factors for p ≤ λ².
- Their spectra reproduce the low zeros to extraordinary accuracy (for example, error 2.5·10⁻⁵⁵ on the first zero using only the primes ≤ 13).
- Connes-van Suijlekom (CMP 2025) proved the key reality mechanism: the minimal eigenvector of such a quadratic form has a Fourier transform with only real zeros.
- The open step is convergence as λ → ∞. This gives a very concrete, finite, computable pipeline.

The de Branges/canonical-system line has also been revived, by M. Suzuki (screw function, 2022-2026).

### Cited Findings
**CCM prolate operator**
- Connes-Consani-Moscovici, "Zeta zeros and prolate wave operators", Annals of Functional Analysis 15(4), no. 87 (2024). It introduces a semilocal analogue of the prolate wave operator:
  - Positive spectrum: spectral realization of the low-lying zeros.
  - Negative spectrum (Sonin space): their ultraviolet behaviour.
  - Archimedean case: prolate operator = (scaling operator)² + grading of orthogonal polynomials, and this form extends to the semilocal case.
  - [EST] - [arXiv 2310.18423](https://arxiv.org/abs/2310.18423); [Springer](https://link.springer.com/article/10.1007/s43034-024-00388-z)
- History: Connes found a self-adjoint extension of the prolate operator in 1998. In 2021, Connes-Moscovici found that its restriction to the complement of the finite interval has negative eigenvalues whose UV behaviour reproduces the squares of the (shifted) zeta zeros. [EST] - [search summary of CCM](https://arxiv.org/abs/2310.18423); [Connes-Moscovici draft "Prolate spheroidal operator and zeta"](https://alainconnes.org/wp-content/uploads/draft4.pdf)
- Earlier "Spectral triples and zeta-cycles" (Connes-Consani, 2021) is the predecessor that realizes zeros via spectral triples on intervals. [EXP/EST] - [arXiv 2106.01715](https://arxiv.org/abs/2106.01715)

**Zeta spectral triples (2025-2026)**
- Connes-Consani-Moscovici, "Zeta Spectral Triples" (arXiv Nov 2025; EMS Series of Lectures in Mathematics 2026).
  - The authors explicitly propose "a strategy toward a proof of RH". Self-adjoint operators are built as rank-one perturbations of the spectral triple of the scaling operator on [λ⁻¹, λ], using only Euler products over p ≤ x = λ².
  - The spectra "coincide with striking numerical accuracy" with the lowest zeros.
  - With the primes ≤ 13, the first 50 zeros have errors from 2.5·10⁻⁵⁵ (first zero) to about 10⁻³ (50th).
  - Because the operators are self-adjoint, the approximating values lie exactly on the critical line.
  - [EXP] - [arXiv 2511.22755](https://arxiv.org/abs/2511.22755); [Connes site post](https://alainconnes.org/2026/07/zeta-spectral-triples/)

**Connes-van Suijlekom reality theorem**
- Connes-van Suijlekom, "Quadratic Forms, Real Zeros and Echoes of the Spectral Action", Comm. Math. Phys. (2025).
  - Setting: a real even distribution on an interval whose quadratic form defines a lower-bounded self-adjoint operator. The lowest spectral value must be a simple isolated eigenvalue with an even eigenfunction.
  - Conclusion: all zeros of the Fourier transform of that eigenfunction are real.
  - Step 1 of the proof is a C*-algebraic proof of a corollary of Carathéodory-Fejér's 1911 Toeplitz structure theorem.
  - [EST] - [arXiv 2511.23257](https://arxiv.org/abs/2511.23257); [Radboud repository PDF](https://repository.ubn.ru.nl/bitstream/handle/2066/326192/326192pre.pdf?sequence=3)

**Related Connes-Consani geometry (2026 posts)**
- "On the absolute geometry of Spec Z" and "On the Jacobian of Spec Z" (Connes-Consani). [EXP] - [Connes site](https://alainconnes.org/2026/07/on-the-absolute-geometry-of-spec-z/); [Consani 2026 publication list](https://math.jhu.edu/~kc/Publ2026.pdf)

**Follow-on finite matrix models built on these ideas (unknown authors)**
- "Construction of Finite Hilbert-Pólya Matrices from Weil's Explicit Formula" (arXiv Sept 2026) [NEW/UNK].
  - Builds finite real-symmetric "Prime-Weil matrices" from pole, archimedean and prime-power data of the Ξ-specialized explicit formula.
  - Off-diagonal entries form a Loewner-type divided-difference matrix with a rank-two displacement identity.
  - Summarises CCM/Connes-van Suijlekom as giving, for a prime cutoff c and band N, an explicit (2N+1)×(2N+1) Galerkin matrix "whose deep spectrum is the finite-rank window on Weil positivity".
  - [arXiv 2609.04908](https://arxiv.org/abs/2609.04908)
- "High-Precision Approximation of Riemann Zeros via the Truncated Weil Form" (arXiv May 2026) [NEW/UNK] - [arXiv 2605.20224](https://arxiv.org/abs/2605.20224)
- "A finite Guinand-Weil dictionary and archimedean tail order for the truncated Weil quadratic form" (arXiv July 2026) [NEW/UNK] - [arXiv 2607.02828](https://arxiv.org/abs/2607.02828)

**De Branges / canonical systems (Suzuki)**
- Suzuki's screw function gives several RH-equivalent conditions. The link to RH runs through de Branges theory: a meromorphic inner function and a canonical system (a Hamiltonian), plus an inverse spectral problem for canonical systems. [EST] - [JLMS 2023 "Aspects of the screw function"](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12785); [arXiv 2209.04658](https://arxiv.org/abs/2209.04658)
- Suzuki: the Hilbert space derived from the Weil distribution is isomorphic to a de Branges space (via Fourier transform composed with a simple map), which gives new RH-equivalent conditions. [EXP] - [arXiv 2301.00421](https://arxiv.org/pdf/2301.00421)
- Suzuki, "Weil's quadratic form via the screw function" (June 2026): a unified operator-theoretic framework for Weil-form results. [EXP] - [arXiv 2606.09096](https://arxiv.org/abs/2606.09096)
- Suzuki (J. Number Theory 2025), "M-functions and screw functions: applications to Goldbach's problem and zeros of zeta". [EST] - [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0022314X25002689)
- Earlier: Suzuki, "A canonical system of differential equations arising from the Riemann zeta-function". [EST] - [arXiv 1204.1827](https://arxiv.org/pdf/1204.1827)

**Berry-Keating xp / Bender-Brody-Müller**
- No 2020-2026 advance turned up in my searches. BBM 2017 (PRL 118, 130201; arXiv 1608.03679) proposed a PT-symmetric Hamiltonian whose eigenvalues would be the zeros if a boundary condition is met. Its self-adjointness and rigor were disputed. I did not re-fetch in this session (background only; see Gaps).

### Inferences
- **Most transferable finite experiment:**
  - Build the CCM/Connes-van Suijlekom finite quadratic form (a Toeplitz/Galerkin matrix restricted to [λ⁻¹, λ] with p ≤ λ²).
  - Compute its minimal eigenvector in interval arithmetic.
  - Certify three things:
    - (i) the minimal eigenvalue is simple and isolated (a certified spectral gap);
    - (ii) the eigenvector is even;
    - (iii) hence, by Connes-van Suijlekom, the approximating zeros are exactly real. Measure their distance to the true zeros as a function of λ.
  - Each step is finite and certifiable. Only the λ → ∞ convergence is open.
- **Sub-question with a concrete verifiable claim:** for which (λ, N) can simplicity of the lowest eigenvalue be certified? Does the gap shrink like a Landau-Widom/prolate law (compare Zhu, Q2)?
- The de Branges/Suzuki framework turns RH into positivity of a Hamiltonian / inverse spectral data. Finite truncations of the screw function are computable, but I found no certified-numerics paper for them.

### Gaps
- I could not read CCM 2025/2026 full texts. It is unclear exactly which convergence statements are proved and which are conjectured (the abstract says "strategy").
- There is no reliable 2020-2026 source on Sierra's or Berry-Keating's models, nor on Burnol's recent work. The Bellissard/other critiques of BBM were not re-verified.
- Authorship and credibility of 2605.20224, 2607.02828 and 2609.04908 are unknown.

---

## Q2. Positivity (Weil explicit formula, Yoshida, Bombieri, Connes-Consani archimedean, finite certified versions)

### Takeaway
Weil positivity is where the 2026 action is, on two fronts:

**(a) Finite certified windows.** Xuefeng Zhu (preprint, Aug 2026) reduces positivity on a whole compact window to positive-semidefiniteness of *one* finite matrix. He certifies Q(f) ≥ 8.9·10⁻¹⁸‖f‖² for supp f ⊂ [-0.8, 0.8], an autocorrelation support of 1.6, which is 2.3× the classical Yoshida-type range.

**(b) Zero proportions.** The Claude/Alpöge-Furman argument (Aug 2026) uses a *finite compression of Weil's Hermitian form* with a rank-trace inequality and Sylvester inertia. It proves unconditionally that more than 2/3 (0.6725 with the Montgomery-Taylor window) of zeros are simple and on the line. Lamzouri gave a shorter Hilbert-space proof.

Weil-positivity machinery is now a *proven* engine for zero-proportion theorems, not just an RH-equivalence.

### Cited Findings
**Connes-Consani archimedean place (2021)**
- "Weil positivity and trace formula, the archimedean place" (Selecta Math. 2021): Weil positivity holds at the archimedean place for test functions with support in a small interval, via a semilocal trace formula. [EST] - [ResearchGate record](https://www.researchgate.net/publication/342436176_Weil_positivity_and_Trace_formula_the_archimedean_place)

**Zhu (2026), finite certified windows [NEW/UNK, ~1 month old, unrefereed]**
- Main idea: a "one-stroke reduction" turning positivity on a whole window into PSD-ness of a single finite matrix.
- Certified lower bound: Q(f) ≥ 8.9e-18 ‖f‖² for supp f ⊂ [-0.8, 0.8] (autocorrelation support 1.6, 2.3× the classical range).
- Variational upper bounds on the geometric side, in interval arithmetic, go down to 3.2e-283 at L = 2.
- Empirical law: −ln λ_min(L) ≈ 2π² N(T*)/ln N(T*), labelled a Landau-Widom decay law.
- At L = 0.8 both sides are certified: 8.9e-18 ≤ λ_min(0.8) ≤ 2.27e-17.
- Sources: [arXiv 2608.24827](https://arxiv.org/abs/2608.24827) (search snippet). Hobbyist or unknown GitHub projects already import it as a "conditional node" and try to replay the certificate ([example PR](https://github.com/DrMurphyIsIn/Arda/pull/580); [replay issue](https://github.com/murillo128/mathia/issues/152)). Treat these as signal of interest, not validation.
- An alphaXiv page titled "Certified Weil Positivity Beyond the Unit Window" appears related. Its provenance is unclear. - [alphaXiv](https://www.alphaxiv.org/abs/2609.weil-positivity-riemann-zeta-bounds)

**Claude / Alpöge-Furman (2026): Weil form turned into a zero-proportion theorem [EXP; reviewed by Conrey and Goldston per Anthropic; Lean-verified; not yet refereed]**
- Results:
  - Unconditionally, more than 2/3 of nontrivial zeros (with multiplicity) are simple and on the critical line, and more than 5/6 are distinct. The previous records were 5/12 and 0.6603.
  - With the Montgomery-Taylor window, the constants become 0.6725 and 0.8362.
  - Extends to primitive Dirichlet L-functions.
  - Formally verified in Lean 4.
- Method:
  - Montgomery's 1973 argument needed RH to read the zero side as a positive sum over real ordinates.
  - Here RH is replaced by a rank-trace inequality applied to a finite compression of Weil's Hermitian form, with Sylvester's law of inertia handling off-line pairs.
  - Sources: [arXiv 2608.13637](https://arxiv.org/abs/2608.13637); [Anthropic PDF](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf)
- Anthropic's description (Aug 10, 2026, updated Aug 13):
  - The proof "forms a suitable space of functions with quadratic form induced by Weil, and positive- (respectively negative-)definite subspaces arising from zeros on (respectively off) the line", then bounds the rank of the form.
  - It combines work of Aryan and of Baluyot-Goldston-Suriajaya-Turnage-Butterbaugh with Bombieri's 2000 paper.
  - Stated caveat: "We don't expect that the techniques Claude used will lead to proving the Riemann hypothesis."
  - External experts Brian Conrey and Dan Goldston reviewed it.
  - Source: [Anthropic research page](https://www.anthropic.com/research/riemann-zeta)

**Lamzouri: a second, human proof [EXP]**
- Replaces the finite-matrix framework with a Hilbert-space inequality and applies Montgomery's pair-correlation theorem directly. - [arXiv 2609.02882](https://arxiv.org/abs/2609.02882)
- New unconditional corollaries:
  - At least 88.76% of zeros are simple or on the line (or both).
  - The average of the simple proportion and the critical proportion is at least 83.62%.
  - Source: [arXiv 2609.02882](https://arxiv.org/abs/2609.02882)

**Other positivity-related work**
- A probabilistic interpretation of Weil's explicit sums and "arithmetic spectral measures". [NEW/UNK] - [arXiv 2311.08519](https://arxiv.org/abs/2311.08519)
- Suzuki: the Weil quadratic form expressed through continuous functions (screw function), which brings de Branges theory in. [EXP] - [arXiv 2606.09096](https://arxiv.org/abs/2606.09096)

### Inferences
- **Finite certifiable sub-questions (highest value)**
  - (i) Independently replicate Zhu's L = 0.8 certificate (PSD of one finite matrix plus tail bounds) in a trusted interval-arithmetic stack.
  - (ii) Push the certified window L upward. Under Zhu's empirical law, λ_min decays like exp(−2π² N/ln N), so the precision needed grows quickly with L; mapping that cost is itself a quantitative result.
  - (iii) Numerically optimise the finite Weil compression used in the Alpöge-Furman/Lamzouri argument, to test how far rank-trace plus better windows can push the 0.6725 constant. The optimisation step there is an explicit finite variational problem, which makes it a natural target for AlphaEvolve-style search.
- The link between Weil-positivity windows and pair-correlation/zero-proportion theorems is now explicit. A certified improvement to an admissible "window" function translates directly into an improved proportion constant.
- Caution: Zhu is unrefereed and by an author I could not place. Treat it as a replicate-before-use target.

### Gaps
- I could not read the full texts of 2608.13637, 2609.02882 or 2608.24827, so the exact optimisation problem and the window function are not extracted here.
- Whether Yoshida's or Bombieri's original ranges have been formally improved in refereed literature since 2020 was not verified.

---

## Q3. Heat flow / de Bruijn-Newman

### Takeaway
0 ≤ Λ ≤ 0.2 still stands:
- Rodgers-Tao proved Λ ≥ 0 (Forum Math. Pi 2020).
- Polymath15 proved Λ ≤ 0.22 (2019).
- Platt-Trudgian proved Λ ≤ 0.2 (2020/21).

I found no 2021-2026 improvement to the upper bound. Improving it is a finite computation: verify zero-freeness of H_t in a region, plus the RH height needed (zeros verified up to about 3·10¹²).

### Cited Findings
- Upper-bound history: 0.5 (1950) → < 0.5 (2008) → 0.22 (2019) → 0.2 (2020). [EST] - [Wikipedia: de Bruijn-Newman constant](https://en.wikipedia.org/wiki/De_Bruijn%E2%80%93Newman_constant)
- Polymath15 proved Λ ≤ 0.22 unconditionally by combining effective heat-flow estimates with numerics. Platt-Trudgian improved this to 0.2 in April 2020. [EST] - [Wikipedia](https://en.wikipedia.org/wiki/De_Bruijn%E2%80%93Newman_constant); [Polymath15 paper record](https://www.researchgate.net/publication/335414187_Effective_approximation_of_heat_flow_evolution_of_the_Riemann_xi_function_and_a_new_upper_bound_for_the_de_Bruijn-Newman_constant); [Polymath code repo](https://github.com/km-git-acc/dbn_upper_bound)
- Rodgers-Tao: "The de Bruijn-Newman constant is non-negative", Forum of Mathematics, Pi. [EST] - [Cambridge Core](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/de-bruijnnewman-constant-is-nonnegative/D4B85BA067E2D5A71D87E4FFB0D21E46)
- Newman-Wu survey (Bull. AMS 2020) connects de Bruijn-Newman-type constants in analytic number theory with Lee-Yang/statistical physics. [EST] - [arXiv 1901.06596](https://arxiv.org/abs/1901.06596)

### Inferences
- Λ ≤ 0.2 is a certifiable finite computation. The Polymath15 barrier-method code exists and is public ([repo](https://github.com/km-git-acc/dbn_upper_bound)). Better RH verification heights and faster multi-evaluation (Odlyzko-Schönhage-type) are the levers.
- Qualitatively, Rodgers-Tao's proof works by showing that negative Λ would force the zeros too regular, contradicting pair-correlation/GUE-type behaviour. Heat flow and zero statistics are therefore linked via zero repulsion (background knowledge; not re-fetched).

### Gaps
- There is no evidence found, either way, of a 2021-2026 improvement below 0.2. Absence in search is not proof of absence.

---

## Q4. Jensen polynomials / Turán inequalities

### Takeaway
Griffin-Ono-Rolen-Zagier (PNAS 2019) proved that for each degree d, the Jensen polynomials J^{d,n} of Ξ are hyperbolic for all sufficiently large n, through a Hermite-limit phenomenon. RH is equivalent to hyperbolicity for all d and n. The 2020-2026 follow-ups mostly generalise the Hermite-Jensen framework to partition-type sequences. Degree-by-degree explicit n-thresholds for Ξ are a finite certifiable target.

### Cited Findings
- RH is equivalent to hyperbolicity of all Jensen polynomials of the Taylor coefficients of Ξ at s = 1/2 (Pólya). Higher Turán inequalities correspond to hyperbolicity of higher-degree Jensen polynomials. [EST] - [GORZ, PNAS 2019](https://www.pnas.org/doi/10.1073/pnas.1902572116)
- "Jensen polynomials for the Riemann xi-function", Advances in Mathematics (2022): a follow-up on explicit ranges. Exact thresholds were not extracted because the page was not fetched. [EST] - [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0001870822000020)
- Banerjee-Bringmann-Rolen (arXiv, Sept 2026) [EXP]:
  - An analytic framework for hyperbolicity of Jensen polynomials for sequences with general asymptotic growth.
  - Partial converses to the GORZ Hermite-Jensen phenomenon.
  - Proves conjectures on log-concavity, higher-order Turán and Laguerre inequalities, and Toeplitz determinants for partition-type functions.
  - Source: [arXiv 2609.14295](https://arxiv.org/abs/2609.14295)
- Analogue for partitions: explicit thresholds N(3) = 94, N(4) = 206, N(5) = 381 and a general bound N(d) ≤ (3d)^{24d}(50d)^{3d²}. Jensen polynomials for Wright's-circle-method sequences are also asymptotically hyperbolic (INTEGERS 25, 2025). [EST] - [INTEGERS A36](https://math.colgate.edu/~integers/z36/z36.pdf); [arXiv 2301.02492](https://arxiv.org/abs/2301.02492)

### Inferences
- **Finite certifiable task:** for Ξ at fixed d (say d ≤ 10), certify hyperbolicity of J^{d,n} for all n ≤ N₀ by interval arithmetic (Sturm sequences or discriminants) and match it with an effective version of the GORZ asymptotics for n > N₀. The partition case shows that such explicit N(d) are feasible.
- There is no known link to zero proportions. This criterion is "global" and does not localise zeros in short intervals.

### Gaps
- The exact explicit ranges proved for Ξ (Adv. Math. 2022 and later) are not extracted.
- I did not verify whether anyone has certified hyperbolicity of J^{d,n}(Ξ) for all n at small d.

---

## Q5. Probability / random matrices / multiplicative chaos

### Takeaway
The Fyodorov-Hiary-Keating (FHK) conjecture on the max of |ζ| in short intervals is essentially resolved:
- Arguin-Bourgade-Radziwiłł established tightness of max|ζ|·(log log T)^{3/4}/log T, with a right tail of order y e^{-2y}.
- A mesoscopic-interval extension followed in 2024.

Multiplicative chaos (Saksman-Webb) and Harper's random multiplicative functions are the probabilistic models behind this. The link to zero statements goes through pair correlation: Montgomery's theorem is exactly what the 2026 proportion results make unconditional.

### Cited Findings
- ABR proved the lower bound for max|ζ(1/2 + iτ + ih)| over |h| ≤ 1. With their earlier upper bound, this gives tightness of max|ζ|·(log log T)^{3/4}/log T. [EST/EXP] - [FHK II, arXiv 2307.00982](https://arxiv.org/abs/2307.00982); [FHK I, arXiv 2007.00988](https://arxiv.org/abs/2007.00988)
- Strong upper bound: meas{t ∈ [T, 2T] : max|ζ| > e^y log T/(log log T)^{3/4}} ≪ y e^{-2y} T, uniformly in y ≥ 1. [EXP] - [FHK I/II](https://arxiv.org/abs/2307.00982)
- FHK on mesoscopic intervals (2024). [EXP] - [arXiv 2405.06474](https://arxiv.org/abs/2405.06474)
- Background survey: Harper's Bourbaki seminar on ζ in short intervals. [EST] - [arXiv 1904.08204](https://arxiv.org/abs/1904.08204)
- Survey: "Maxima of log-correlated fields: some recent developments". - [arXiv 2106.15141](https://arxiv.org/abs/2106.15141)
- Pair correlation and proportions (Baluyot-Goldston-Suriajaya-Turnage-Butterbaugh, Jan 2025) [EXP]:
  - First use of the pair-correlation method for *horizontal* distribution.
  - If all zeros with T < γ ≤ 2T lie in a vertical box of width b/log T with b = 0.3185, then at least 2/3 of zeros are simple and on the line.
  - Unconditionally, pair correlation gives at least 1/3 simple critical zeros.
  - Source: [arXiv 2501.14545](https://arxiv.org/abs/2501.14545)
- Goldston-Suriajaya, "Zeta zeros on the critical line" (Analysis Mathematica 2026). [EST] - [arXiv 2511.20059](https://arxiv.org/abs/2511.20059); [Springer](https://link.springer.com/article/10.1007/s10476-026-00186-w)
- Also "Zeta zeros in a narrow vertical box". - [arXiv 2603.28104](https://arxiv.org/abs/2603.28104)
- Background, not re-fetched this session:
  - Saksman-Webb, "The Riemann zeta function and Gaussian multiplicative chaos" (Ann. Probab. 2020) - [arXiv 1604.08378](https://arxiv.org/abs/1604.08378)
  - Harper, "Moments of random multiplicative functions I" (Forum Math. Pi 2020): better-than-square-root cancellation via critical multiplicative chaos - [arXiv 1703.06654](https://arxiv.org/abs/1703.06654)

### Inferences
- The bridge from probability to zeros is Montgomery pair correlation. Numerically certifiable targets:
  - (i) Explicit effective versions of Montgomery's F(α) theorem in short windows (needed by Wang's short-interval proportion bounds, Q9).
  - (ii) Finite-T verification of the FHK tail constants against zero data (Odlyzko/Platt tables). This is empirical, not a certificate.
- Multiplicative chaos gives no RH-equivalence, only distributional models. Its use here is for designing statistics, not certificates.

### Gaps
- I found no source linking multiplicative chaos directly to proportions of simple zeros.
- The status of full FHK (convergence in distribution of the recentred max) was not verified.

---

## Q6. Dynamics / ergodic theory (horocycles, Selberg/Ruelle zeta, transfer operators)

### Takeaway
Zagier's result stands: RH is equivalent to an optimal rate, O(y^{3/4−ε}), for equidistribution of long closed horocycles on the modular surface. Verjovsky and others followed. I found no 2020-2026 breakthrough.

The Mayer transfer operator realises Selberg zeta (not Riemann zeta) as a Fredholm determinant. It is a model for "finite matrix approximations with certified spectra", but gives no RH-equivalence.

### Cited Findings
- Zagier showed that an optimal equidistribution rate for long periodic horocycles is equivalent to RH. The Zagier/Sarnak/Verjovsky method uses Eisenstein series. It was revisited in the string-amplitude setting in "Equidistribution Rates, Closed String Amplitudes, and the Riemann Hypothesis" (JHEP 2010). [EST] - [arXiv 1007.3717](https://arxiv.org/abs/1007.3717); [JHEP](https://link.springer.com/article/10.1007/JHEP12(2010)025)
- Horocycle-flow structure: a Poincaré map for horocycle flow on PSL(2,Z)\H via the Stern-Brocot tree (2022). [EXP] - [arXiv 2207.03755](https://arxiv.org/abs/2207.03755)
- Horocycle-flow structure: effective equidistribution of expanding horospheres in SO(d)\SL(d,R)/SL(d,Z). [EXP] - [arXiv 2001.07693](https://arxiv.org/abs/2001.07693)

### Inferences
- The horocycle criterion reduces to Eisenstein-series values E(z, s) along a horocycle, which equal Fourier coefficients involving ζ(2s)/ζ(2s−1)... Numerically it is equivalent to classical estimates, so it offers little new certifiability. It could still give a visually distinct experiment: certified discrepancy of horocycle equidistribution versus y.
- Mayer transfer-operator truncations have certified-spectrum technology (Bandtlow-Jenkinson-type rigorous numerics, not searched here). That transferable technique could apply to CCM finite matrices.

### Gaps
- I found no 2020-2026 papers giving new RH equivalences via dynamics. Mayer/Ruelle 2020-2026 work was not searched in depth.

---

## Q7. Function-field / algebraic-geometry analogues, F₁, arithmetic site, Katz-Sarnak

### Takeaway
Over function fields, RH is a theorem (Weil for curves, Deligne in general). Connes-Consani's arithmetic site / "absolute geometry of Spec Z" (2026) tries to supply the missing geometry. Katz-Sarnak gives symmetry-type predictions that are testable numerically. None of these yields a finite certificate for ζ itself. Their value is conceptual: the analogue of the Hodge index theorem / Castelnuovo positivity is exactly Weil positivity (Q2).

### Cited Findings
- 2026 Connes-Consani posts "On the absolute geometry of Spec Z" and "On the Jacobian of Spec Z". [EXP] - [Connes site](https://alainconnes.org/2026/07/on-the-absolute-geometry-of-spec-z/); [Consani list](https://math.jhu.edu/~kc/Publ2026.pdf)
- The Lee-Yang theorem inspired speculation about statistical-mechanics models behind the zeros of Riemann/Selberg zeta and the Weil conjectures (historical survey). - [arXiv 1410.6450](https://arxiv.org/abs/1410.6450)

### Inferences
- The transferable technique is the positivity transfer. In the function-field case, positivity of the intersection pairing on C×C gives RH. Connes-Consani's semilocal trace formula (Q2) is the number-field attempt, and the finite Weil-window certificates are its computable shadow.

### Gaps
- I did not fetch the content of the 2026 Spec Z papers.
- No 2020-2026 Katz-Sarnak results were checked in this session.

---

## Q8. Machine learning / AI-driven discovery (2025-2026)

### Takeaway
The first credible AI-originated theorem in this area is the August 2026 Claude result: more than 2/3 of zeros are simple and on the line, Lean-verified. It was reviewed by Conrey and Goldston, and Lamzouri re-proved it by hand. AlphaEvolve (May 2025) and the Tao-Georgiev-Gómez-Serrano-Wagner large-scale study (Nov 2025) show LLM-driven search can find extremal test functions for functional inequalities. That is exactly the shape of the Weil-window / pair-correlation window optimisation.

### Cited Findings
- Anthropic (Aug 10, 2026): an unreleased research version of Claude improved the lower bound for zeros satisfying RH from 41.6% to 67.2%, with a Lean-verifiable proof. Alpöge and Furman verified it; Conrey and Goldston reviewed it. [EXP] - [Anthropic research page](https://www.anthropic.com/research/riemann-zeta); [arXiv 2608.13637](https://arxiv.org/abs/2608.13637)
- AlphaEvolve is DeepMind's LLM-driven evolutionary coding agent, unveiled May 2025. On 67 problems across analysis, combinatorics, geometry and number theory, it rediscovered the best known solutions in most cases and improved several. It has been used for best constants in functional inequalities (for example Hausdorff-Young and Gagliardo-Nirenberg). [EST/EXP] - [Wikipedia: AlphaEvolve](https://en.wikipedia.org/wiki/AlphaEvolve); [Tao blog](https://terrytao.wordpress.com/2025/11/05/mathematical-exploration-and-discovery-at-scale/); [arXiv 2511.02864](https://arxiv.org/abs/2511.02864)
- Counterpoint: "Simple Baselines are Competitive with Code Evolution" (2026). - [arXiv 2602.16805](https://arxiv.org/abs/2602.16805)
- Survey or essay: "The Riemann Hypothesis: Past, Present and a Letter Through Time" (Feb 2026; author and content not verified). - [arXiv 2602.04022](https://arxiv.org/abs/2602.04022)
- Community formalisation or replay projects around Weil-window certificates exist on GitHub. Their credibility is unknown; they are not mathematical evidence. - [monocap-tech/weil](https://github.com/monocap-tech/weil); [trureturing issue](https://github.com/the-omega-institute/trureturing/issues/8474)

### Inferences
- Concrete AI-search targets with finite, checkable scores:
  - (i) The test/window function in the rank-trace (Alpöge-Furman) or Hilbert-space (Lamzouri) inequality: maximise the proportion constant beyond 0.6725. Wang already nudged it with refinements (Q9).
  - (ii) Test functions maximising the certified Weil-window length L at fixed precision.
  - (iii) Beurling-Selberg-type majorants for short-interval zero counts.
- Each score can be verified rigorously with interval arithmetic, and the proof skeleton is already Lean-formalised.

### Gaps
- I found no "AxiomMath" RH-related result.
- I could not verify an AlphaEvolve application specific to zeta/Weil test functions.

---

## Q9. Short-interval / zero-proportion links and other credible 2025-2026 equivalences (signal processing, quantum computing, Lee-Yang)

### Takeaway
The zero-proportion front moved dramatically in Aug-Sep 2026:
- Proportions: 5/12 (PRZZ 2020) → more than 2/3 → 0.6725 simple-critical and 0.8362 distinct.
- Wang extended these to short intervals of length T^θ, using Lamzouri's method.
- Selberg's method for critical zeros is being re-optimised.

For Lee-Yang / stable polynomials, I found no credible new RH equivalence in 2024-2026. The theory (Borcea-Brändén) is a transferable toolbox of zero-preservers, not new evidence. No credible signal-processing or quantum-computing equivalence was found.

### Cited Findings
- Pratt-Robles-Zaharescu-Zeindler: more than 5/12 of zeros on the line, using long mollifiers and Kloosterman sums (Res. Math. Sci. 7, 2020). [EST] - [arXiv 1802.10521](https://arxiv.org/abs/1802.10521)
- Alpöge-Furman (Claude): more than 2/3, then 0.6725 simple and critical; more than 5/6, then 0.8362 distinct. Extends to Dirichlet L-functions; Lean-verified. [EXP] - [arXiv 2608.13637](https://arxiv.org/abs/2608.13637)
- Lamzouri: an alternative proof, plus at least 88.76% simple-or-critical. [EXP] - [arXiv 2609.02882](https://arxiv.org/abs/2609.02882)
- Biao Wang, "Simple critical zeros and distinct zeros of the Riemann zeta-function in short intervals" (Sept 2026) [NEW/UNK author, unrefereed]:
  - Lower bounds in intervals of length T^θ, 0 < θ < 1.
  - Proves a short-interval version of Montgomery's pair-correlation theorem, then applies Lamzouri's inequality on finite multisets of complex numbers.
  - Source: [arXiv 2609.07918](https://arxiv.org/abs/2609.07918)
- A Zenodo "stability refinement" of Wang's short-interval bounds. [UNK] - [Zenodo](https://zenodo.org/records/22727389)
- Biao Wang, "Proportions of the non-trivial zeros of the Riemann zeta function" (Sept 2026): refines Lamzouri's method to C₀ = 0.67250..., C₁ = C₀ + 1/2 = 0.83625.... [NEW/UNK] - [arXiv 2609.24167](https://arxiv.org/abs/2609.24167)
- "Optimising Selberg's method for critical zeros" (Sept 2026). Content not extracted. - [arXiv 2609.15329](https://arxiv.org/abs/2609.15329)
- Lee-Yang/Pólya-Schur (Borcea-Brändén):
  - Theory of stable polynomials and linear operators preserving stability (Invent. Math.; CPA). [EST] - [CPA](https://onlinelibrary.wiley.com/doi/10.1002/cpa.20295); [Inventiones](https://link.springer.com/article/10.1007/s00222-009-0189-3)
  - Lee-Yang zeros have been observed experimentally in physical systems (for example Rydberg atoms), but these carry no RH content. - [arXiv 2203.16128](https://arxiv.org/abs/2203.16128)

### Inferences
- **Most promising novel experiment** for a program that already has the classical dossier: a *certified finite Weil compression*, which unifies three strands.
  - The same finite object serves three purposes:
    - (a) the CCM/Connes-van Suijlekom spectral approximants: real zeros if the lowest eigenvalue is simple;
    - (b) Zhu-type window PSD certificates;
    - (c) the rank-trace / Sylvester-inertia argument that yields zero proportions.
  - Certifiable quantities: λ_min and its gap, PSD-ness up to window L, and the optimised proportion constant. For the short-interval version, add an explicit θ-dependence.
- Lee-Yang/stable-polynomial theory supplies operators that preserve real-rootedness (the Laguerre-Pólya class). These are useful for proving the Jensen/Turán inequalities in Q4 or the heat flow in Q3 (Pólya's universal factors), but they are not new equivalences.
- **Excluded [FRINGE]:** claimed proofs of RH, for example the arXiv "Proof that the real part of all non-trivial zeros is 1/2" (1602.03553) and the long-running "investigation of the non-trivial zeros" series (1804.04700 v20). These surfaced in searches and are excluded. - [arXiv 1602.03553](https://arxiv.org/abs/1602.03553); [arXiv 1804.04700](https://arxiv.org/abs/1804.04700)

### Gaps
- I found no credible 2025-2026 RH equivalence in signal processing or quantum computing. That is a negative search result, not proof of absence.
- The short-interval θ-range and constants in Wang's paper are not extracted.
- The author and content of "Optimising Selberg's method" are unknown.

---

## Catalogue summary (for the report writer): representation → finite certificate → zero-proportion or short-interval link

**Finite Weil compression + rank-trace / Sylvester inertia** (Alpöge-Furman/Claude 2026; Lamzouri; Wang)
- Field: functional analysis / quadratic forms.
- Status: [EXP], Lean-verified.
- Finite certificate: yes. The optimised window constant is explicit.
- Proportion / short-interval link: direct. Proportion 0.6725; short intervals via Wang.

**Certified Weil positivity in compact windows** (Zhu 2026)
- Field: positivity / numerics.
- Status: [NEW/UNK].
- Finite certificate: yes, PSD of one matrix. L = 0.8 is certified; L > 0.8 is open.
- Proportion / short-interval link: indirect.

**Zeta spectral triples / prolate operator** (CCM 2024-2026; Connes-van Suijlekom 2025)
- Field: operator theory / NCG.
- Status: [EST]/[EXP].
- Finite certificate: yes (simplicity of λ_min ⇒ real zeros of the approximant). λ → ∞ convergence is open.
- Proportion / short-interval link: none yet.

**Suzuki screw function / de Branges canonical systems**
- Field: spectral theory.
- Status: [EST]/[EXP].
- Finite certificate: partial (truncations).
- Proportion / short-interval link: none found.

**de Bruijn-Newman, 0 ≤ Λ ≤ 0.2**
- Field: heat flow / PDE.
- Status: [EST].
- Finite certificate: yes (barrier computation plus RH height). No improvement since 2020.
- Proportion / short-interval link: via zero repulsion (Rodgers-Tao).

**Jensen hyperbolicity** (GORZ; Banerjee-Bringmann-Rolen 2026)
- Field: combinatorics / real-rootedness.
- Status: [EST]/[EXP].
- Finite certificate: yes (explicit N(d) per degree).
- Proportion / short-interval link: none.

**FHK / multiplicative chaos** (ABR)
- Field: probability.
- Status: [EST]/[EXP].
- Finite certificate: empirical only.
- Proportion / short-interval link: via pair correlation.

**Horocycle equidistribution rate** (Zagier)
- Field: dynamics.
- Status: [EST].
- Finite certificate: no new certificate.
- Proportion / short-interval link: none.

**Lee-Yang / Pólya-Schur**
- Field: statistical mechanics.
- Status: [EST] toolbox.
- Finite certificate: indirect.
- Proportion / short-interval link: none.
