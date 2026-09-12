# EXP-004 adversarial validation record

Date: 2026-09-12. Declaration commit:
`e03413b2301bf45ca68ff6e945f25add9a1c3a89`.
This record distinguishes paper review from the deterministic computation and the
later publication gates. It is not external peer review or formal verification.

## Independent preflight review

The separately authored [primary-source and parity audit](../../context/2026-09-12-parity-transfer-adversarial-audit.md)
predates experimental implementation. It checked the finite residual identities,
the exact distinct-count correction, the classical odd-support convention, interval
packing, fixed support and smooth-test limits, and the claimed threshold scope.
It found no fatal gap. Its exact inspected source locations and novelty limits
remain in that record.

## Coordinating review of the complete proof

The coordinating reviewer read the complete [mathematical proof](mathematical-proof.md)
after declaration and independently checked the following attacks.

| Possible failure | Check and outcome |
|---|---|
| Conjugation or inner-product convention changes the kernel square | Rank-one multiplication with the declared second-slot-linear inner product gives the ordinary complex square. Evenness and the complete trace, not termwise positivity, justify the real Hilbert--Schmidt quantity. |
| Min-max loses a dimension or the empty/simple-singular case | The positive index of the remainder is at most r+b; the shifted eigenvalue inequality and the cost of omitted terms give the claimed coefficient. Zero padding contributes Psi(0)=1. The d>=h case has a nonpositive right side and remains valid. |
| Odd multiplicity is silently counted as simplicity | Each odd multiple point costs at least one unit of E. The universal atom formula proves s+E-O>=0 for arbitrary multiplicities; no density of simple zeros is assumed in the seed. |
| Distinct bound has the wrong sign on excess | The identity 2Z=N+s-E+2b has a negative E term. The separate residual certificate has nonnegative terms s+E-O, 6b and 2sigma. The real triple point rejects the tempting half-sum shortcut. |
| Sinc controls are misrepresented as actual zeta configurations | Integer supports realize orthogonal finite features and show sharpness of the finite inequality only. The scalar LP omits geometric and mass constraints; its exact optimum is limited to that relaxation. |
| The seed only holds globally or counts copies | Karatsuba's printed Theorem B and the primary sign-change counting convention supply distinct odd zeros in every sufficiently high seed interval. The source theorem is imported, not proved by the census. |
| Packing duplicates zeros or needs a moving seed constant | Half-open seed intervals are disjoint. Endpoint reserves are negligible; the uncovered tail is O(T^alpha)=o(T^theta). One fixed seed constant serves every fixed longer exponent, with no uniform moving-exponent assertion. |
| Rational deweighting has the wrong sign | The Fourier multiplier for g-g''/(4L^2) equals 1-(rho-rho')^2/4 at the encoded difference. Two separate fixed-test applications cancel the weight exactly and leave the required asymptotic functional. |
| Positivity of c is incorrectly assumed for the arithmetic theorem | The cosine density and the fixed-support pair formula are valid below the root. Apply each fixed smooth test before taking its approximation/support limits. No lambda=theta substitution is made in the error term. |
| The improved exponent is manufactured from a decimal root or unknown density | Exact cos/sin and tan comparisons give c(51/100)<0<c(1) and c'<4 on the required interval. The symbolic delta yields a strictly smaller exponent for one fixed unspecified kappa. A new decimal exponent remains unquantified. |
| The distinct-above-one-half consequence is inferred from simplicity | It is substituted into the separate parity distinct formula with delta_d<=kappa/16, giving c>-kappa/4 and the bound 1/2+kappa/12. |
| A newer short-mollifier theorem already supplies the claimed count | The inspected theorem supplies critical zeros with high-degree derivatives; simplicity and every-interval localization do not follow automatically. The source dossier records three missing gates for a separate stronger-seed proposal. |

No mathematical objection remained after this review. One transcription defect in
the displayed cosine evaluation was corrected before proof freeze: a form-feed
character had replaced a LaTeX backslash. The subsequent scan of all 50 problem and
scratch-manuscript Markdown/TeX files found no forbidden control bytes. The
distinct-corollary notation was also separated from Wang's existing distinct
positivity threshold. Neither edit changes a mathematical identity or the
declared experiment.

## Computational validation

The declared single full run passed in 8.0353704 seconds, below the 60-second cap.
Its 19,683 count vectors and 59,049 slack evaluations passed, together with two
symbolic identities, 24 atom regressions, 42 exact primal/dual controls and 36
sinc sharpness configurations. The negative control correctly rejects the false
distinct half-sum inequality. The 36 focused software tests passed, including
forged weighted-odd counts, missing conjugate copies, negative/float slack,
source-byte changes, interruption-prefix preservation and existing-output refusal.

Two reviewers then independently parsed every stored census row using direct
count and residual formulas without importing the runner. Both checks passed.
The coordinating review also verified each linked raw-artifact SHA-256, the
absence of a failure record, the original stdout hash, the observed budget, and
null fields for unquantified numerical constants. The source-bound run itself
checked its hypothesis and four exact premise files against declaration e03413b.

All eight process-generated files were copied unchanged into artifacts, followed
by a portable execution receipt. The deterministic result hash is
`bc9e28ca1792657e24da77268e6e2108c3f52684b7e16504f07b32cfce014d6e`;
the full census hash is
`03e3f42e3c887e729057e02b88b53c07673c171113f5389e0b7d92ee18acc421`.
No failed full run, replacement search or budget extension was omitted. The
[confirmed verdict](verdict.md) states the theorem and its exact boundaries.

## Residual risks and theorem limits

The result inherits the stated external analytic theorems, including Wang's recent
preprint, and the finite stability mechanism. The dated novelty search is bounded;
it cannot establish absolute priority or community acceptance. The theorem is a
qualitative strict range extension with a specified dependence on an unknown
positive seed constant. It does not give a usable decimal exponent, effective
height, global record, universal simplicity, or an RH solution.
