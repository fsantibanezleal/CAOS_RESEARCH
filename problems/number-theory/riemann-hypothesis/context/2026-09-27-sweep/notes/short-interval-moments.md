# Mollified moments of zeta in short intervals (T, T+T^theta], theta slightly above 1/2: technology survey for RH-027 / RH-028

Access note (read first): arxiv.org, springer, aimath.org, zenodo, alphaxiv, adsabs, pith.science, researchgate and the Goettingen host of Steuding's dissertation were all blocked by the egress proxy in this session (403 on CONNECT). Everything below therefore comes from (a) search-engine abstracts and snippets, (b) the arXiv source tarballs already cached locally at `problems/number-theory/riemann-hypothesis/context/source-cache/` (Wang arXiv:2609.24167v1, Pearce-Crump arXiv:2609.15329v1), and (c) the program's own earlier primary-source reading, recorded in local context files (cited by path). Those files record what was read directly from Steuding's 1999 dissertation, Conrey 1989 and BCHB 1985. Anything recalled from memory that I could not re-check is marked **[unverified]**.

## Q1. What exactly did Steuding (and Karatsuba, Selberg, Rezvyakova, Conrey-Ghosh-Gonek) prove in short intervals? Is nu < (3theta-1)/4 proved for general Q and with two shifts?

### Takeaway
Steuding (dissertation 1999; Acta Math. Hungar. 96 (2002) 259-308) proved one short-interval mollified mean square. It is for F = zeta + zeta'/log T, i.e. Levinson's degree-one Q, with fixed shifts. The Dirichlet polynomial has length M = T^nu, and the error is O(T^{1/3+eps} M^{4/3}) **under the extra condition nu < 3/8**. Positivity of simple critical zeros follows for H >= T^{0.552}. The range nu < (3theta-1)/4 is not stated as such. It is what you get by requiring T^{1/3}M^{4/3} = o(H), and it is proved only for Levinson's Q, with the absolute cap nu < 3/8. No published source proves it for general Q or for uniform two-shift moments.

### Cited Findings
- Steuding computes, "in a new way", the mean square of the product of a zeta-type F(s) and a Dirichlet polynomial A(s) of length M = T^theta over short intervals on sigma = a near the critical line. **If theta < 3/8** (his theta = the mollifier exponent), the integral equals I(T,H) + O(T^{1/3+eps} M^{4/3}). This error is "much smaller" than the O(T^{1/2+eps} M) that other approaches give. - [Springer abstract, Acta Math. Hungar. 2002](https://link.springer.com/article/10.1023/A:1019767816190); [ResearchGate record](https://www.researchgate.net/publication/225856285_On_simple_zeros_of_the_Reimann_zeta-function_in_short_intervals_on_the_critical_line); [Ovid abstract](https://www.ovid.com/journals/acmah/abstract/00133301-200209640-00001~on-simple-zeros-of-the-reimann-zeta-function-in-short?redirectionsource=fulltextview)
- Consequence stated in the abstract: by Levinson's method, the proportion of zeros with ordinates in [T, T+H] that are simple and on the critical line is positive when H >= T^{0.552}. - [Springer abstract](https://link.springer.com/article/10.1023/A:1019767816190)
- Method: "combining ideas and methods of Atkinson, Jutila and Motohashi to treat short intervals [T, T+H]". - [search snippet of Steuding, LNM 1877 (2007)](https://nzdr.ru/data/media/biblio/kolxoz/M/Mln/Steuding%20J.%20Value%20Distribution%20of%20L-Functions%20(LNM1877,%20Springer,%202007)(ISBN%203540265260)(319s)_Mln_.pdf)
- Program's earlier direct reading of the dissertation ([PDF](https://webdoc.sub.gwdg.de/ebook/e/1999/steuding/253563305.pdf)):
  - Theorem 2.1 (printed p. 11) treats F = zeta + zeta'/log T with error O(T^{1/3+eps}M^{4/3}).
  - "A simple choice yields the 0.591 threshold", and a stronger mollifier choice gives 0.552.
  - Arbitrary derivative orders are introduced on p. 12 and in (2.43)-(2.44) on p. 37, but the final error analysis "explicitly specializes to orders at most two on p. 41".
  - Reach: "Degree-one Q and fixed shifts only". The 2002 journal version was not accessed.
  - Motohashi 1986 (Note V) announced the global E(T,A) << T^{1/3} M^{4/3} T^eps, unshifted.
  - Sources: local `problems/number-theory/riemann-hypothesis/context/2026-09-12-critical-mass-and-multiplicity-route.md` (secs. 1, 8.2) and `.../2026-09-26-levinson-localization-preflight.md` (source table).
- The program's preflight concluded: "No published theorem states the needed short-interval shifted moment". A Steuding-type range nu < (3theta-1)/4 for general Q "would need a two-shift Atkinson analysis far beyond a few pages". - local `.../2026-09-26-levinson-localization-preflight.md`
- A complete explicit Atkinson-type formula for the error term E(T;A) in the mean square of zeta times a Dirichlet polynomial A exists, including complex coefficients: Ishikawa-Matsumoto, Cent. Eur. J. Math. / Open Math. 9 (2011) 102-126. This is the natural engine for a general-Q, shifted version of Steuding's estimate. - [EuDML](https://eudml.org/doc/269380); [Springer](https://link.springer.com/article/10.2478/s11533-010-0085-5)
- Selberg (1942), as restated as Theorem B in Karatsuba: a positive proportion of odd-order critical zeros in H = T^{1/2+eps}. Karatsuba (Izv. 1984, English 1985): at least a_eps H log T odd-order critical zeros for H = T^{27/82+eps}. These zeros need not be simple, and no explicit proportion is given. - local `.../2026-09-12-critical-mass-and-multiplicity-route.md` (read from the Karatsuba PDF, [DOI](https://doi.org/10.1070/IM1985v024n03ABEH001246)); [Wikipedia: Selberg's zeta function conjecture](https://en.wikipedia.org/wiki/Selberg%27s_zeta_function_conjecture)
- Karatsuba (1992) proved the analogue for almost all intervals of length H = T^eps. - [Wikipedia](https://en.wikipedia.org/wiki/Selberg%27s_zeta_function_conjecture)
- Rezvyakova's located work is a Selberg/Levinson-type positive proportion of critical zeros for automorphic L-functions, and for linear combinations with Selberg's approach. No short-interval Levinson constant for zeta was found. - [Math. Notes 2010](https://link.springer.com/article/10.1134/S0001434610090154); [arXiv:2501.00551](https://arxiv.org/pdf/2501.00551)

### Inferences
- Derivation of the range. The Levinson main term on the window is proportional to H, up to log factors. Steuding's error T^{1/3+eps} T^{4nu/3} is o(H) iff nu < (3theta-1)/4 - eps. His hypothesis also needs nu < 3/8. The admissible Steuding range is therefore nu < min{(3theta-1)/4, 3/8}. The two bounds coincide at theta = 5/6.
  - Check: theta = 0.552 gives (3*0.552 - 1)/4 = 0.164, and theta = 0.591 gives 0.193. These match the positivity thresholds of Levinson's Q(x) = 1-x with the two mollifier choices (onsets near nu ~ 0.164 and 0.193). This agrees with the local note but is not quoted from Steuding.
- Comparison with the program's localized Young range nu < theta - 1/2. The difference is (3theta-1)/4 - (theta - 1/2) = (1-theta)/4 > 0 for theta < 1. At theta -> 1/2+, Steuding's range is nu -> 1/8, while the localized Young range tends to 0.
  - The 3/8 cap binds only for theta > 5/6.
  - theta - 1/2 overtakes 3/8 only for theta > 7/8. There the localized Young range is better.
  - For the stated slope kappa > 0.7170 nu, a general-Q Steuding moment gives kappa > 0.7170 * (3theta-1)/4 ~ 0.0896 at theta -> 1/2+. That explains the RH-027 target "positivity for every theta > 1/2".
- The T^{1/3}M^{4/3} error is the twisted analogue of Atkinson's E(T) << T^{1/3}. It comes from Atkinson/Jutila/Motohashi transformations (Voronoi-type summation of the off-diagonal) rather than Young-style integration by parts. That is why it beats the H >= T^{1/2}M-type barrier.
- Steuding's Theorem 2.1 already involves zeta' (a derivative, i.e. a shift by Cauchy's formula). So "two-shift at fixed shift sizes" is in scope of his machinery. What is missing is uniformity in the shifts (alpha, beta << 1/L) and polynomial Q of arbitrary degree. Uniformity in fixed-size shifts, carried through Cauchy's integral on circles of radius about 1/L, typically costs only log powers. So the extension to general Q is plausible, but it is not proved. **[inference]**

### Gaps
- The 2002 journal paper's exact theorem statement (whether it keeps theta < 3/8, and which Q) could not be read (Springer blocked). The dissertation text is not in the local source cache (only its hash is recorded).
- Why the cap nu < 3/8 arises (Steuding's specific estimate versus the global Motohashi E(T,A) bound) was not verified.
- Conrey-Ghosh-Gonek: no short-interval Levinson result was found. Their known work (simple zeros, e.g. 19/27 under RH [unverified]) is global.

## Q2. Best known twisted second moments (global and short-interval), with exact exponents

### Takeaway
The global records are as follows.
- General coefficients: nu < 1/2 (BCHB 1985), improved to nu < 17/33 = 1/2 + 0.01515 (Bettin-Chandee-Radziwill).
- Conrey's structured (mu * P) coefficients: 4/7.
- Feng-type pieces: 6/11 (Pratt-Robles, via Kloosterman sums).

In short intervals, the only located twisted-moment results are Steuding's (nu < min{(3theta-1)/4, 3/8}, Levinson's Q) and Tang's 2026 short-interval reciprocity formula (delta in (1/2,1)). Tang's is an exact identity for a prime-type twist and was judged unusable for mollifiers in the program's preflight.

### Cited Findings
- Balasubramanian-Conrey-Heath-Brown 1985 handle Dirichlet polynomials of length up to T^{1/2} for the twisted second moment. - [snippet in Bettin-Chandee-Radziwill context, arXiv:2211.11450](https://arxiv.org/pdf/2211.11450); program reading of BCHB Theorems 1-2: critical-line twisted mean squares, Gaussian windows with error Delta^{-7/2} T^{5/2+eps} M^2, no shifts - local `.../2026-09-26-levinson-localization-preflight.md`
- Bettin-Chandee-Radziwill: asymptotics for the twisted second moment (no shifts) for any Dirichlet polynomial of length at most T^{17/33-eps}, i.e. T^{1/2+delta} with delta = 0.01515... - [search snippets, arXiv:2211.11450 and Semantic Scholar](https://www.semanticscholar.org/paper/The-mean-square-of-the-product-of-$\zeta(s)$-with-Bettin-Chandee/79bd41817a564be5b82388501cb8c5a0ad7be3ca)
- Conrey 1989 (Crelle 399): int_2^T |VB|^2 ~ c(P,Q,R) T for mollifier exponent < 4/7, with no error term (Theorem 2, eq. (39)). Its Gaussian windows T^{1-delta} with uniform shifts need delta < 1/7 - nu/4, i.e. windows only for theta > 6/7 + nu/4 (Proposition p. 11, eq. (75)). - local `.../2026-09-26-levinson-localization-preflight.md`
- Pratt-Robles: the Feng mollifier length can be raised from theta < 17/33 to theta < 6/11. The method decomposes the error into Type I/II sums and uses sums of Kloosterman sums. - [Pratt-Robles, Res. Number Theory 2018](https://link.springer.com/article/10.1007/s40993-018-0103-4); [arXiv:1706.04593](https://arxiv.org/abs/1706.04593)
- The PRZZ search snippet mentions "bilinear Kloosterman sums leading to theta = 48/95". This is garbled in the snippet and the context was not verified. - [arXiv:1802.10521](https://arxiv.org/pdf/1802.10521)
- Tang (UT Dallas), arXiv:2608.14852 (14 Aug 2026): a reciprocity formula for a twisted second moment of zeta over a short interval of length T^delta, delta in (1/2,1), centred at height T. It extends Khan's reciprocity (arXiv:2401.01057) and "makes explicit the relation between the twisting parameters and the interval length". - [arXiv:2608.14852](https://arxiv.org/abs/2608.14852)
- The program's preflight classifies Tang (together with Bettin-Chandee-Radziwill and Hughes-Young) as "Long mollifiers, fourth moments, or prime-twist reciprocity - Not usable here". - local `.../2026-09-26-levinson-localization-preflight.md`
- Short-interval untwisted mean values (Ivić): results on the mean square of E*(t) and R(t) over [T, T+H] for T^{2/3+eps} <= H <= T, plus related short-interval moment results. - [arXiv:1212.0660](https://arxiv.org/abs/1212.0660); [arXiv:1305.2028](https://arxiv.org/html/1305.2028)
- Mean square of the product of zeta and a Dirichlet polynomial inside the critical strip (a recent global refinement): - [arXiv:2312.10614](https://arxiv.org/pdf/2312.10614) (contents not read)

### Inferences
- The short-interval analogue of BCHB by the Young/integration-by-parts route gives only hk <= Delta^2 T^{-1-eps}, i.e. nu < theta - 1/2. This matches the program's Prediction A.
- Globally (theta = 1), Steuding's route gives nu < 3/8, strictly worse than BCHB's 1/2. So Steuding's technique trades global length for good dependence on H.
- A hybrid is needed for theta near 1/2: an Atkinson-type off-diagonal treatment in the window with a general-Q main term. Ishikawa-Matsumoto's explicit formula is the most relevant existing ingredient.
- Tang's reciprocity is an exact identity for twists by a single h/k (Khan-type). In principle, summing it over the mollifier coefficients h, k <= T^nu would give a short-interval twisted moment in whatever (h, k, delta) range his explicit relation allows.
  - Tang's exact admissible range could not be read. If it allows hk up to T^{2(3delta-1)/4}-type sizes, it would be a direct route to RH-027.
  - This is the single most important unread source. **[unverified]**

### Gaps
- Tang's exact hypotheses on h, k versus delta, and his error term: not accessible.
- Whether any 2019-2026 paper gives an asymptotic for int_T^{T+H} |zeta A|^2 with A of length T^nu, nu > theta - 1/2, for general coefficients: none found beyond Steuding.
- Chandee-Soundararajan, Bettin-Gonek, Goldston-Gonek short-interval twisted moments: none located in these searches.

## Q3. Short-interval mean-value theorems for Dirichlet polynomials; does Guth-Maynard help?

### Takeaway
Guth-Maynard (arXiv:2405.20552, 2024) improves large-value frequency bounds for Dirichlet polynomials of size near N^{3/4}. That yields N(sigma,T) <= T^{30(1-sigma)/13+o(1)} and primes in almost all short intervals of length x^{2/15+eps}, and in all intervals of length x^{17/30+eps}. It is an upper-bound (large-values) technology. It does not provide the main-term asymptotics with power-saving off-diagonal control that Levinson moments require, and I found no paper applying it to twisted second moments.

### Cited Findings
- Guth-Maynard: new large-value estimates for Dirichlet polynomials near N^{3/4}. Consequences: zero density N(sigma,T) <= T^{30(1-sigma)/13+o(1)} and primes in short intervals of length x^{17/30+o(1)}. - [arXiv:2405.20552](https://arxiv.org/abs/2405.20552); [Oxford ORA](https://ora.ox.ac.uk/objects/uuid:ad11b8bf-ad2b-4ebf-a627-647f023c378f/files/s73666708v)
- Tao's comments: the Ingham exponent improved from 3/5 to 13/25, and the almost-all short-interval PNT range from theta > 1/6 to theta > 2/15. - [Mathstodon](https://mathstodon.xyz/@tao/112557249982780815)
- Montgomery-Vaughan-type mean values: the relevant "conditional mean values of long Dirichlet polynomials" literature exists (arXiv:2201.02108, arXiv:2105.03525). These are conditional or divisor-type results and not short-interval twisted zeta moments. - [arXiv:2201.02108](https://arxiv.org/pdf/2201.02108); [arXiv:2105.03525](https://arxiv.org/pdf/2105.03525)

### Inferences
- Where large-value inputs can matter: they bound the measure of t in (T, T+H] where the mollifier or the off-diagonal is large, which enters upper bounds for error terms. The standard mean-value theorem int_T^{T+H} |sum a_n n^{-it}|^2 = (H + O(N)) sum |a_n|^2 already shows the H >= N barrier for the mollifier squared, i.e. |M|^2 of length T^{2nu} <= H.
  - In Young's framework, the diagonal-dominance condition is instead hk <= Delta^2/T, coming from the zeta part (approximate functional equation length sqrt T).
  - Guth-Maynard does not change the diagonal/off-diagonal balance for a mean square with prescribed main term. It controls frequency of large values, not the average of a product with oscillating zeta. **[inference]**
- Jutila's large-values and short-interval mean values, and Huxley's large-values estimates, are of the same nature. None of them appeared in the located short-interval Levinson literature.

### Gaps
- No source found that applies Guth-Maynard to mollified or twisted moments (2024-2026).
- The Jutila/Huxley short-interval mean-value theorems were not individually checked.

## Q4. Multi-piece mollifiers (Feng, BCY, PRZZ, Wu): constants, lengths, localization

### Takeaway
The multi-piece mollifiers are these.
- Feng (JNT 132 (2012)): two-piece. Conrey piece theta_C = 4/7 - eps plus a second piece of length theta_F. Rigorously kappa > 0.4107 with theta_F = 3/7 - eps. The claimed 0.4128 needs a longer theta_F.
- Bui-Conrey-Young (Acta Arith. 150 (2011)): two pieces with y_1 <= T^{4/7} and y_2 <= T^{1/2}, giving more than 41%.
- Pratt-Robles raised theta_F to 6/11 via Kloosterman sums.
- Pratt-Robles-Zaharescu-Zeindler (Res. Math. Sci. 7 (2020)): kappa > 0.417293962 > 5/12. This is the best mollifier-method proportion.
- Wu 2018 extended Levinson-Conrey to Dirichlet L-functions (> 2/5, also simple).

None has been localized to short intervals in any located source.

### Cited Findings
- PRZZ context: Feng's two-piece mollifier with theta_C = 4/7 - eps and theta_F = 3/7 - eps gives kappa > 0.4107. Decomposing Feng's error terms into Type I/II sums and handling incomplete Kloosterman sums allows theta_F = 6/11 - eps. - [arXiv:1802.10521](https://arxiv.org/pdf/1802.10521); [Res. Math. Sci. 2020](https://link.springer.com/article/10.1007/s40687-019-0199-8)
- PRZZ: 41.7293962% of zeros are on the critical line, improving Pratt-Robles' long-mollifier / Kloosterman results to slightly over 5/12. - [Illinois Experts](https://experts.illinois.edu/en/publications/more-than-five-twelfths-of-the-zeros-of-%CE%B6-are-on-the-critical-lin); [arXiv:1802.10521](https://arxiv.org/abs/1802.10521)
- The PRZZ snippet also refers to "Feng's claim that ... kappa > 0.4128", with the associated theta garbled in the snippet. - [PRZZ search snippet](https://arxiv.org/pdf/1802.10521)
- Feng introduced a two-piece mollifier to show kappa >= 41.28%. BCY introduced two pieces with y_1 <= T^{4/7} and y_2 <= T^{1/2}. "Pushing theta past 6/11 to (perhaps) 4/7 will require more effort." - [BCY, Acta Arith. 150.1 (2011)](https://aimath.org/~kaur/publications/69.pdf); [ResearchGate snippet, "An application of generalized mollifiers"](https://www.researchgate.net/publication/326001958_An_application_of_generalized_mollifiers_to_the_riemann_zeta-function)
- Feng, "Zeros of the Riemann zeta function on the critical line", J. Number Theory 132 (2012), no. 4, 511-542 (bibliographic data verified in the cached Wang tex). PRZZ is Res. Math. Sci. 7 (2020), Paper No. 2, 74 pp. - local cache `/source-cache/wang-global-refinement-2609.24167v1.tar.gz` and `pearce-crump-2609.15329v1.tar.gz` bibliographies
- Wu (2018), as summarized by Ray's survey: more than two fifths of the zeros of Dirichlet L-functions are on the critical line, and more than two fifths are simple and critical, using a longer mollifier. Ray reproves Levinson via Young's short proof. - [Ray, arXiv:2511.06109](https://arxiv.org/abs/2511.06109)
- A January 2026 paper, "Bilinear forms with Kloosterman fractions and applications", gives improved bilinear Kloosterman-fraction bounds. Its snippets reference the long-mollifier / five-twelfths line. Whether it raises theta_F or kappa was not visible. - [arXiv:2601.00292](https://arxiv.org/pdf/2601.00292)

  Correction recorded 2026-10-03: the primary v2 is withdrawn. A missing
  L^2 factor invalidated the claimed improvement; none of its stronger
  bounds is eligible as an input. Read the current
  [subdyadic and non-abelian review](../../2026-10-03-subdyadic-and-nonabelian-review.md)
  and the [withdrawal notice](https://arxiv.org/abs/2601.00292v2).
- Short-mollifier regime (directly relevant to kappa/nu): Conrey-Farmer-Kwan-Lin-Turnage-Butterbaugh (arXiv:2508.11108, Aug 2025) use the calculus of variations to construct linear combinations of derivatives of zeta adapted to Levinson's method. These "yield a positive proportion of zeros ... on the critical line, regardless of how short the mollifier is". - [arXiv:2508.11108](https://arxiv.org/abs/2508.11108)

### Inferences
- For RH-028 (kappa/nu > 0.7173 in short windows), the relevant multi-piece benchmark is a Feng/BCY second piece of the same small length nu, not PRZZ's lengths.
  - The Feng piece's second-moment cross terms have coefficients built from mu * Lambda^{*k}-type convolutions.
  - For short lengths, the off-diagonal conditions in the window are identical to those of the Conrey piece (hk <= Delta^2/T). So a localized two-piece moment at nu < theta - 1/2 should follow from the same localized Young argument. The gain is then purely in the main-term optimization. **[inference]**
- The Kloosterman-sum extensions (17/33, 6/11, 4/7) are global. Their Deshouillers-Iwaniec inputs use smooth weights of width about T. A window of width H introduces a Fourier dual variable of size T/H, which inflates the Kloosterman moduli ranges. No source quantifies this. **[inference]**
- CFKLT 2025 is the closest published analogue of the program's "general-Q, small-nu slope" computation. Its small-nu slope should be compared to 0.7170 to check whether it matches or beats it.

### Gaps
- The exact kappa-versus-nu slope as nu -> 0 in CFKLT 2025 (and in Bernard, Kühn-Robles-Zeindler for modular L-functions) was not accessible.
- The exact BCY constant (commonly quoted as 0.4105 **[unverified]**) and the exact lengths in Feng's unconditional claim.
- No located localization of any multi-piece mollifier to (T, T+T^theta].

## Q5. 2024-2026 papers on Levinson / critical zeros in short intervals with explicit proportions

### Takeaway
September 2026 changed the landscape.
- Alpöge-Furman (with Claude), arXiv:2608.13637, proved unconditionally that more than 2/3 of zeros (0.6725 with the Montgomery-Taylor window) are simple and critical, and 5/6 (0.8362) are distinct. The method is a rank-trace inequality on Weil's form, with no mollifier.
- Lamzouri (arXiv:2609.02882) gave a new proof.
- Wang (arXiv:2609.07918) localized the Lamzouri method to H = T^theta. This gives explicit short-interval proportions for theta above about 0.55019, a threshold just below Steuding's 0.552.
- Pearce-Crump (arXiv:2609.15329) optimized Selberg's method (>= 7% globally).

I found no 2024-2026 paper doing Levinson's method in short intervals other than this program's own work.

### Cited Findings
- arXiv:2608.13637 (Alpöge-Furman, argument discovered and written by Claude). At least two thirds of zeros are simple and on the critical line, and at least five sixths are distinct. With the Montgomery-Taylor window the constants are 0.6725 and 0.8362. "No mollifier, zero-density estimate, or zero-free region is used." - [arXiv:2608.13637](https://arxiv.org/html/2608.13637v1); [Anthropic PDF](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf)
- Lamzouri, "A new proof that more than 2/3 of the zeros of the Riemann zeta function are simple and on the critical line", arXiv:2609.02882. - [arXiv:2609.02882](https://arxiv.org/html/2609.02882)
- Wang, arXiv:2609.07918: applies Lamzouri's method. It establishes Montgomery's pair-correlation theorem in short intervals and applies Lamzouri's inequality for conjugation-invariant finite multisets. It studies N_0^s(T,H)/N(T,H) and N^d(T,H)/N(T,H) for H = T^theta. "Levinson's method does not yield a result if theta is too small, but tends to yield much stronger explicit bounds ... and ... simple zeros". - [arXiv:2609.07918](https://arxiv.org/pdf/2609.07918)
- The program's local notes record Wang's fixed-test arithmetic estimate as holding for every 0 < lambda < theta < 1, positive only for theta > theta_0. The manuscript lists thresholds 0.552 (Steuding), 0.55019... (Wang) and 0.5458838 (parity inequality). - local `.../2026-09-12-critical-mass-and-multiplicity-route.md`; `manuscripts/riemann-hypothesis/short-interval-levinson/main.tex` l. 77-103
- Wang, "Proportions of the non-trivial zeros of the Riemann zeta function" (arXiv:2609.24167, cached locally). A stability refinement of Lamzouri's inequality, which "can be used to improve" the short-interval proportions of Wang 2026 (sec. near l. 912 of main.tex). - local cache `source-cache/wang-global-refinement-2609.24167v1.tar.gz`; [arXiv:2609.24167](https://arxiv.org/html/2609.24167)
- Pearce-Crump optimized Zhuravlev's quantitative Selberg method: at least 7% of zeros are critical (global). - [arXiv:2609.15329](https://arxiv.org/abs/2609.15329)
- The program's own public outputs (for provenance, not independent evidence):
  - Zenodo records claim a theta = 3/4 certificate with simple-critical proportion >= 0.41907682842... and distinct >= 0.70953841421....
  - They claim a localized Selberg detector giving (theta - 1/2)/(4eC_3) for 1/2 < theta < 1.
  - PR #341 claims "localized Levinson detector moves the simple-critical onset to 0.534".
  - Sources: [Zenodo 22727389](https://zenodo.org/records/22727389); [Zenodo 22851518](https://zenodo.org/records/22851518); [Zenodo 22860012](https://zenodo.org/records/22860012); [CAOS_RESEARCH PR #341](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/341)
- Ray (arXiv:2511.06109, rev. June 2026) is an expository reproof of Levinson via Young plus Wu's Dirichlet L-function generalization. It has no short intervals. - [arXiv:2511.06109](https://arxiv.org/abs/2511.06109)
- Kühn-Robles-Zeindler / Bernard-type modular L-function proportions are more than doubled by CFKLT with the same arithmetic inputs. - [arXiv:2508.11108](https://arxiv.org/abs/2508.11108)

### Inferences
- The Lamzouri/Wang route needs short-interval pair correlation with Fourier support lambda < theta. The Levinson route needs a short-interval mollified moment with nu < (range).
  - These are different analytic inputs. Both degenerate as theta -> 1/2 for the same structural reason: the diagonal needs about sqrt T of room.
  - So a Steuding-type general-Q moment (RH-027) is the only located mechanism that would give positivity uniformly down to theta -> 1/2+ via Levinson.

### Gaps
- Wang's explicit curve c(theta) and its exact threshold were not re-read (arXiv blocked). The value 0.55019 comes from the program manuscript.
- No independent (non-program) 2024-2026 short-interval Levinson paper was found. The absence is from bounded searching, not an exhaustive MathSciNet check.

## Q6. Obstacles to mollifier length beyond theta - 1/2 in short windows

### Takeaway
The obstacles are:
- (i) The Young/BCHB integration-by-parts off-diagonal bound requires hk <= Delta^2 T^{-1-eps} with Delta = H/L. This is exactly nu < theta - 1/2.
- (ii) Going past it needs Atkinson/Jutila/Motohashi transformations of the off-diagonal, which is Steuding's T^{1/3}M^{4/3}. These are proved only for degree-one Q with the cap nu < 3/8, and with final error analysis only up to second-order derivatives.
- (iii) The global Kloosterman routes (Conrey 4/7, Pratt-Robles 6/11, BCR 17/33) have no short-window versions. Conrey's own window proposition needs theta > 6/7 + nu/4.

### Cited Findings
- Localized Young: off-diagonal terms are bounded by H(1+mn/T)^{-A}(2 sqrt(hkmn)/Delta)^j. This is T^{-A} whenever hk <= Delta^2 T^{-1-eps}, giving nu < theta - 1/2. The contour-shift error is O(H T^{-delta(1-2nu)+eps}). Young's Lemma 5 needs hk <= T^{2theta} globally, with off-diagonal controlled by |log(hm/kn)| >= 1/(2 sqrt(hkmn)). - local `.../2026-09-26-levinson-localization-preflight.md`; [Young, arXiv:1002.4403](https://arxiv.org/pdf/1002.4403)
- Conrey 1989 windows: Gaussian windows of width T^{1-delta} with uniform shifts need delta < 1/7 - nu/4. - local preflight file (Conrey 1989, Proposition p. 11, eq. (75))
- BCHB windows: error Delta^{-7/2} T^{5/2+eps} M^2, no shifts. - local preflight file
- Steuding: error O(T^{1/3+eps}M^{4/3}) versus O(T^{1/2+eps}M) for "other approaches"; valid for nu < 3/8. - [Springer abstract](https://link.springer.com/article/10.1023/A:1019767816190)
- Steuding's final error analysis is specialized to derivative orders <= 2 (dissertation p. 41). - local `.../2026-09-12-critical-mass-and-multiplicity-route.md` sec. 8.2
- Program note: pair-correlation support beyond lambda < theta makes the prime-pair off-diagonal of the order of the main term (Lamzouri/Wang route). - local preflight file sec. 4

### Inferences
- The "O(T^{1/2+eps}M)" error of other approaches corresponds to requiring H >> T^{1/2}M, i.e. nu < theta - 1/2. This is the same barrier as localized Young. Steuding's improvement is precisely the Atkinson-type treatment of the off-diagonal.
- The O(H/L) smoothing error from Delta = H/L is harmless for the proportion (it gives o(H log T) zeros). It is not the binding constraint. The binding constraint is the off-diagonal.
- Diagonal/off-diagonal balance: with zeta's approximate functional equation of length sqrt T, the diagonal hm = kn dominates only if the frequency spacing 1/(hkmn)^{1/2} exceeds the window's resolution 1/Delta.
  - Beyond this, the off-diagonal contributes genuine main terms (it does so globally past nu = 1/2, which is the source of BCR's and Conrey's extra terms).
  - Steuding's method evaluates, rather than bounds, these terms. So a general-Q version must track an additional off-diagonal main term in the window, or show it is negligible below (3theta-1)/4. **[inference]**

### Gaps
- Whether the cap nu < 3/8 is intrinsic to the Atkinson approach or an artifact of Steuding's bounds: not determined. Motohashi's global E(T,A) << T^{1/3+eps}M^{4/3} has no stated cap in the note seen, but that was an announcement.
- No source was found that discusses a lower-bound barrier (a proof that nu > (3theta-1)/4 is impossible by these methods).
