# Riemann-hypothesis research bibliography and source roles

Review cutoff: 2026-09-12. This bibliography identifies the sources actually
used to establish the baseline, analyze the proof mechanism, and delimit the
candidate short-interval contribution. It does not treat every cited claim
as independently validated. Exact acquisition URLs, versions, byte lengths,
SHA-256 hashes, and redistribution metadata are recorded in the
[source manifest](context/source-manifest.json). The archive currently has
21 primary-source documents and four licensed code snapshots.

## Direct inputs to the current theorem

1. **Youness Lamzouri.** *A new proof that more than 2/3 of the zeros of the
   Riemann zeta function are simple and on the critical line.*
   [arXiv:2609.02882v2](https://arxiv.org/abs/2609.02882v2),
   [full text](https://arxiv.org/html/2609.02882v2),
   [DOI](https://doi.org/10.48550/arXiv.2609.02882).
   Version 1 was submitted September 2; version 2 September 8, 2026. The
   persisted v2 PDF prints September 9 and has 17 pages. Theorem 1.1 gives
   the simple-critical, distinct, average, and union bounds. Proposition 2.1
   and the Section 3 lemmas provide the finite Hilbert and analytic interfaces.
   Remark 3.4 identifies the known extremal window. The
   [local analysis](context/2026-09-12-lamzouri-analysis.md) separates this
   prior work from the proposed stability transfer.

2. **Biao Wang.** *Simple critical zeros and distinct zeros of the Riemann
   zeta-function in short intervals.*
   [arXiv:2609.07918v1](https://arxiv.org/abs/2609.07918v1),
   [full text](https://arxiv.org/html/2609.07918v1),
   [DOI](https://doi.org/10.48550/arXiv.2609.07918).
   Submitted September 7, 2026; the 13-page PDF prints September 9.
   Theorem 1.1 is the baseline curve; Theorem 2.2 and Lemma 3.1 supply the
   fixed-test short-interval pair sum. The
   [transfer audit](context/2026-09-12-wang-transfer-audit.md) verifies
   deweighting, normalization, support restrictions, and legal order of limits.
   The present derived theorem relies on this inspected preprint input.

3. **Ainta repository.** *zeta-simple-zeros*, pinned at
   [`040c5e899e658aed7b56a2a87f501798fe10761d`](https://github.com/ainta/zeta-simple-zeros/tree/040c5e899e658aed7b56a2a87f501798fe10761d).
   [Proof discussion](https://github.com/ainta/zeta-simple-zeros/blob/040c5e899e658aed7b56a2a87f501798fe10761d/docs/proof.md)
   and [manuscript](https://github.com/ainta/zeta-simple-zeros/blob/040c5e899e658aed7b56a2a87f501798fe10761d/paper/riemann.tex).
   Prior source for the convex Gram defect, stable rank-trace method,
   pinching, and cosine-root nonadditivity. These ingredients are not claimed
   as CAOS discoveries. Its higher global numerical claims are a separate
   audit target. The archived source retains its MIT license.

4. **Siegfred A. C. Baluyot, Daniel A. Goldston, Ade Irma Suriajaya, and
   Caroline L. Turnage-Butterbaugh.** Unconditional complex-zero
   pair-correlation development,
   [arXiv:2306.04799](https://arxiv.org/abs/2306.04799), and the later
   narrow-box work [arXiv:2501.14545v3](https://arxiv.org/abs/2501.14545v3).
   The latter version corrects a uniform error formulation. The integrated
   applications identified in its correction remain valid. The
   [source dossier](context/2026-09-12-original-and-successor-review.md)
   records the affected theorem and the preserved lemmas; a correction must
   be read at its exact scope rather than treated as wholesale withdrawal.

## Original announcement, proof, and discovery record

5. **Levent Alpöge and Ralph Furman.** *More than two thirds of the zeta
   zeros are simple and on the critical line.*
   [arXiv:2608.13637v2](https://arxiv.org/abs/2608.13637v2),
   [DOI](https://doi.org/10.48550/arXiv.2608.13637).
   Submitted August 13 and revised August 19, 2026; the 21-page PDF prints
   August 21. The metadata credits the autonomous Claude discovery and
   verification/communication by the listed authors. The finite Weil-form
   representation, inertia argument, trace calculation, and optimized
   proportion precede this research unit. Later remarks have different
   proof and formalization coverage from the headline theorem.

6. **Anthropic research announcement.**
   [Riemann-zeta research page](https://www.anthropic.com/research/riemann-zeta).
   Primary provenance for the discovery process and linked artifacts, rather
   than a substitute for checking the proof. The exact supplied
   [August 10 PDF](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf)
   is preserved separately from the
   [August 11 revision](https://www-cdn.anthropic.com/95c246936988e43127bc6b2ceb7077c1dad2d68e.pdf).
   They have 35 and 17 pages respectively. EXP-001 audits a dyadic
   normalization assertion in the revision and explains why its correction
   does not alone refute the limiting theorem.

7. **Anthropic supporting artifacts.**
   [Informal verification note](https://www-cdn.anthropic.com/23455459f8832d06bb175cc0f88d019aed962ef8.pdf),
   [discovery appendix](https://www-cdn.anthropic.com/d7f3ecf1d01392d887f8bc974ca187e2a121b1ed.pdf),
   and [annotated transcripts](https://www-cdn.anthropic.com/8a0d1add3c637b858a9a181e98c40e9548c3f44f.pdf).
   The archive preserves these as process evidence. The long appendix and
   transcripts were downloaded and indexed; they did not receive a uniform
   line-by-line proof audit. Their presence does not multiply independent
   mathematical evidence for a theorem.

## Pinned formal developments and their boundaries

8. **AxiomMath.** *ZetaZerosV2*, pinned at
   [`4c73b317232173a5e6d4253702c9870ee66c2c7b`](https://github.com/AxiomMath/ZetaZerosV2/tree/4c73b317232173a5e6d4253702c9870ee66c2c7b).
   Formalizes the Lamzouri mechanism. Headline zeta statements retain two
   explicit classical analytic hypotheses. The inspected
   [public CI run](https://github.com/AxiomMath/ZetaZerosV2/actions/runs/34242947077)
   compiled the default library, without comparator execution in that run.
   No fresh local upstream Lean replay is claimed. The portable archived ZIP
   is 140,709 bytes, SHA-256
   `2746d137514e4435c9af154d05137384993e998805facbfe6f8e71be09f16e09`,
   and retains the Apache-2.0 license. The archive compression differs from
   the initial acquisition ZIP; the manifest describes the final persisted one.

9. **Anthropic.** *formal-math*, inspected at
   [`fbdc36bbf17d20af3fd0447c6d1a8a02773c9844`](https://github.com/anthropics/formal-math/tree/fbdc36bbf17d20af3fd0447c6d1a8a02773c9844).
   The archived `zeta23` subset retains Apache-2.0 licensing. The current
   headline source has broader analytic coverage than the Axiom statements.
   Source signatures, historical build receipts, and current CI job coverage
   remain distinct forms of evidence. In particular,
   [RankTraceMult.lean](https://github.com/anthropics/formal-math/blob/fbdc36bbf17d20af3fd0447c6d1a8a02773c9844/zeta23/Zeta23/ZeroSide/RankTraceMult.lean)
   already contains the arbitrary-parameter multiplicity inequality, while
   [TightMult.lean](https://github.com/anthropics/formal-math/blob/fbdc36bbf17d20af3fd0447c6d1a8a02773c9844/zeta23/Zeta23/ZeroSide/TightMult.lean)
   proves abstract sharpness. These preempt a proposed novelty route.

The complete [formalization audit](context/2026-09-12-formalization-audit.md)
records toolchains, inspected declarations, licenses, and the checks actually
performed. None of the upstream formal repositories constitutes a formal
certificate of this unit's entire short-interval theorem.

## Optimization and historical comparison

10. **Emanuel Carneiro, Vorrapan Chandee, Friedrich Littmann, and Micah B.
    Milinovich.** *Hilbert spaces and the pair correlation of zeros of the
    Riemann zeta-function.* Journal für die reine und angewandte Mathematik
    725 (2017), 143-182.
    [arXiv:1406.5462](https://arxiv.org/abs/1406.5462),
    [publisher DOI](https://doi.org/10.1515/crelle-2014-0078).
    Section 3.5 and Corollary 14 solve the broader one-delta extremal
    problem, including uniqueness. This explains why merely reoptimizing
    the scalar window is not a new route. RH-conditional applications in
    this paper must be distinguished from the analytic extremal result.

11. **Kyle Pratt, Nicolas Robles, Alexandru Zaharescu, and Dirk Zeindler.**
    [arXiv:1802.10521v3](https://arxiv.org/abs/1802.10521v3), journal 2020.
    Historical proportions used here are $0.417293962$ for critical-line
    zeros counted with multiplicity and $0.407511457$ for simple-critical
    zeros. The two denominators/counting conventions are not interchangeable.
    The primary PDF's numerical pages, rather than a rounded historical
    headline in a later announcement, determine this comparison.

12. **Farzad Aryan.** [arXiv:1902.05473](https://arxiv.org/abs/1902.05473),
    journal 2022. The unconditional Fejer-kernel pair-correlation variant
    is part of the analytic lineage cited by the recent theorem.

13. **Daniel A. Goldston and Ade Irma Suriajaya.**
    [arXiv:2511.20059](https://arxiv.org/abs/2511.20059) and
    [arXiv:2603.28104](https://arxiv.org/abs/2603.28104).
    The double-sum criterion and narrow-box consequences explain earlier
    ways of relating complex zero geometry to simple-critical counts.
    A narrow-box hypothesis is not silently removed when importing a result.

14. **Andrés Chirre, Felipe Gonçalves, and David de Laat.**
    *Pair Correlation Estimates for the Zeros of the Zeta Function via
    Semidefinite Programming.* Advances in Mathematics 361 (2020), 106926.
    [arXiv:1810.08843](https://arxiv.org/abs/1810.08843).
    A useful optimization reference whose RH-conditional positivity beyond
    the basic Fourier-support range cannot be imported unconditionally.

15. **Goldston, Lee, Schettler, and Suriajaya.**
    [arXiv:2503.15449](https://arxiv.org/abs/2503.15449).
    Full-support pair-correlation hypotheses can yield density-one
    simple-critical conclusions. Density one still permits a zero-density
    exceptional set, so it does not itself imply RH.

16. **Kaisa Matomäki, Maksym Radziwiłł, and Terence Tao.**
    *Correlations of the von Mangoldt and higher divisor functions I. Long
    shift ranges.* Proceedings of the London Mathematical Society 118
    (2019), 284-350. [arXiv:1707.01315](https://arxiv.org/abs/1707.01315).
    Averaging over shifts is an essential hypothesis; it is not a bound for
    an arbitrary fixed shift. This matters when considering greater support.

## Successor claims requiring their own audit

17. **trmdy repository.** *zeta-simple-zeros-673137*, pinned at
    [`1610b97b7895ff34982260f8dcaf04a0f7b82cf7`](https://github.com/trmdy/zeta-simple-zeros-673137/tree/1610b97b7895ff34982260f8dcaf04a0f7b82cf7).
    The inspected README advertises a nine-point global candidate
    $0.6733127422722459\ldots$ and states its remaining expert-review and
    formalization boundaries. Its slug is not the current claimed constant.
    Global block refinements are prior art even where their complete
    verification is outside this unit. The archived snapshot retains MIT.

18. **teal-sea zeta lab / Palomar.**
    [Lab](https://zeta.teal-sea.com/) and
    [formal-registration metadata](https://github.com/teal-sea/zeta-lab/blob/main/lean/PALOMAR.md).
    Registration `PALOMAR-2026-08-25-000005` is associated with a claimed
    four-point global improvement. Exact statements, dependency pins, and
    axioms require separate comparison. Larger candidate certificates and
    registered statements must not be conflated.

19. **Yang-Yang candidate.** [Zenodo record 21975237](https://zenodo.org/records/21975237).
    Its 79.62 percent headline is quarantined as an unverified analytic
    claim in this program. The pre-existing
    [modulus-truncation objection](https://github.com/JoshuaHKU/zeta-0.7947-reproduction/issues/1)
    concerns an analytic interface before the finite rational certificate.
    The [successor review](context/2026-09-12-original-and-successor-review.md)
    records the precise distinction. A DOI does not discharge the objection.

20. **Low-multiplicity research draft.**
    [Theorem discussion](https://github.com/zach7036/riemann-hypothesis-research/blob/main/publication/low-multiplicity-zeta/THEOREM.md).
    Additional prior art against presenting consequences of the existing
    arbitrary-parameter rank-trace inequality as a fresh discovery.

21. **tawanerguo-cn repository.** *zeta-simple-zeros*, pinned at
    [`45149f6d403059a71be73c5e3f884cee7cd62b20`](https://github.com/tawanerguo-cn/zeta-simple-zeros/tree/45149f6d403059a71be73c5e3f884cee7cd62b20).
    Its [Bellman certificate](https://github.com/tawanerguo-cn/zeta-simple-zeros/blob/45149f6d403059a71be73c5e3f884cee7cd62b20/BELLMAN_COBBOUNDARY_PROOF.md),
    [finite trace-envelope proof](https://github.com/tawanerguo-cn/zeta-simple-zeros/blob/45149f6d403059a71be73c5e3f884cee7cd62b20/docs/trace_energy_envelope.md), and
    [global spectral dual](https://github.com/tawanerguo-cn/zeta-simple-zeros/blob/45149f6d403059a71be73c5e3f884cee7cd62b20/archive/original/GLOBAL_SPECTRAL_DUAL.md)
    are prior art for nonuniform pressure, capacity-constrained edges,
    cross-boundary packing and the finite-size envelope. The numerical
    thermodynamic conversion of the last framework is explicitly unfinished.
    The complete archived repository retains its MIT license.

22. **Yuhang Shi.** *zeta-simple-zeros-673316977*, pinned at
    [`1aeda8e9f0678166a824c75313a813b09eb478cd`](https://github.com/yuhangshi888/zeta-simple-zeros-673316977/tree/1aeda8e9f0678166a824c75313a813b09eb478cd).
    [Version 0.1.0 DOI](https://doi.org/10.5281/zenodo.21926962).
    The [proof outline](https://github.com/yuhangshi888/zeta-simple-zeros-673316977/blob/1aeda8e9f0678166a824c75313a813b09eb478cd/PROOF_OUTLINE.md)
    combines two existing trmdy certificates on one 219-point frame to claim
    $0.6733169771424713134\ldots$. The
    [claim ledger](https://github.com/yuhangshi888/zeta-simple-zeros-673316977/blob/1aeda8e9f0678166a824c75313a813b09eb478cd/CLAIM_LEDGER.md)
    states which upstream searches were not replayed and which inequalities
    remain formal hypotheses. Its local Palomar registration is not an
    end-to-end formal proof of the new zeta proportion. The complete archived
    repository retains its MIT license.

The [pressure-frame prior-art dossier](context/2026-09-12-pressure-frame-prior-art.md)
also records npip99's predecessor and the teal-sea registered four-point
bound versus its canceled stronger-candidate build. It distinguishes an
apparently new short-interval consequence from inherited global methods.

## Local derived record and publication status

23. **Andrew Pearce-Crump.** *Optimising Selberg's method for critical
    zeros.* [arXiv:2609.15329v1](https://arxiv.org/abs/2609.15329v1).
    Submitted September 14, 2026. The sign-preserving positive-semidefinite
    detector, coefficient-uniform approximate functional equation,
    arbitrary-subinterval rational-frequency estimate, and certified
    rank-three profile are imported by EXP-005. The source states a global
    critical-line proportion above seven percent; the short-interval
    localization is the separate derived result recorded here.

24. **AxiomMath.** *ZetaZerosV2*, pull request
    [#1](https://github.com/AxiomMath/ZetaZerosV2/pull/1), inspected at head
    `02dfc0b1c63d12e6d39649a0bbe08dfc7ef6cf75`.
    The inspected CI run passed and the new unconditional exports report only
    standard Lean axioms. The pull request formalizes global inputs and four
    headline bounds; it does not formalize Wang's short-interval theorem,
    EXP-004, or the EXP-005 localization.

25. **Eric Dubon.** *Zero-Density Concentration for Dirichlet Polynomials.*
    [arXiv:2609.17875v1](https://arxiv.org/abs/2609.17875v1), submitted
    September 15, 2026. The Jessen-potential, Bohr-lift, and
    anti-concentration results concern zeros of finite Dirichlet truncations.
    They do not by themselves transfer to nontrivial zeros of zeta.

26. **Joseph Najnudel and Ashkan Nikeghbali.** *Cauchy laws associated with
    the zeros of the Riemann zeta function.*
    [arXiv:2609.15862v1](https://arxiv.org/abs/2609.15862v1), submitted
    September 14, 2026. The projected-ordinate Cauchy limit is unconditional.
    Its stronger log-derivative comparison requires a separate small-total-
    horizontal-displacement condition, so it is recorded as a possible
    interface rather than evidence for RH.

27. **teal-sea.** *zeta-lab*, inspected at
    [`f402358c6c3f3c838605e71dd97cb6401a6963f0`](https://github.com/teal-sea/zeta-lab/tree/f402358c6c3f3c838605e71dd97cb6401a6963f0).
    The stable bridge identifies Ainta's `Psi` with the `c=2` eigenbasis form
    of Anthropic's `gc`. EXP-007 treats that parameterized spectral content as
    prior art and claims only the defect-parity coupling and its transfer.

The [EXP-001 verdict](experiments/EXP-001-source-and-constant-audit/verdict.md)
is the authority for exact formula reproduction, source-integrity checks,
and the normalization correction. The
[EXP-002 proof](experiments/EXP-002-short-interval-stability/mathematical-proof.md),
[adversarial audit](experiments/EXP-002-short-interval-stability/adversarial-audit.md),
and [verdict](experiments/EXP-002-short-interval-stability/verdict.md)
are the authority for the candidate strict short-interval refinement and
certified numerical example. The [wiki](wiki/README.md) transcribes them.

**Felipe Santib??ez-Leal.** *Simple critical zeros in short intervals: stability,
parity, localization, and Hilbert compression.* CAOS Research Preprint, version
0.06, September 20, 2026. [Public record](https://zenodo.org/records/22852479),
version DOI [10.5281/zenodo.22852479](https://doi.org/10.5281/zenodo.22852479),
and concept DOI [10.5281/zenodo.22727388](https://doi.org/10.5281/zenodo.22727388).
The [publication receipt](../../../manuscripts/riemann-hypothesis/short-interval-stability/publication-receipt.json)
records verification of fresh public metadata and the downloaded v0.06 PDF:
545,773 bytes, SHA-256
`dde6f2c9a6c0a9b46e66c9d44efc5786d1239dd1ada7664083a6d2134c452082`.
The immutable v0.01 baseline remains at [10.5281/zenodo.22727389](https://doi.org/10.5281/zenodo.22727389)
and its archived 10-page PDF is unchanged. This self-published preprint is not peer
reviewed. The dated novelty search does not guarantee priority against undiscovered
concurrent work.
