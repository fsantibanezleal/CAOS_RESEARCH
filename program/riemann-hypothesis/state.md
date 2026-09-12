# Riemann hypothesis state

Updated: 2026-09-12. Lifecycle: **published** (research, web-content and live-release gates
passed for v0.64.000). Next investigation: **EXP-003 declared, run pending**.

[D] EXP-002 establishes a strict refinement of Wang's entire positive short-interval
cosine curve for each fixed theta between its positivity threshold and one. The derivation
has an independent adversarial audit; it is not an end-to-end Lean proof or peer review.
[MV] At theta=3/4 the certified bound is 0.4190768284253039967, compared with
0.4190750129754243337. All 48,761 certificate nodes were reconstructed; both arithmetic
evaluators accepted every energy leaf with zero unresolved boxes.

EXP-001 independently reproduces the baseline constants and normalization correction using
exact rational series and Arb. Its public CI mode deliberately does not claim local PDF
verification. Versioned source and formalization audits distinguish assumptions from proofs.

The candidate contribution is a short-interval theorem using attributed stability ideas.
There is no global-record or RH-solution claim and no guarantee of publication priority.
The 10-page preprint v0.01 is published as DOI 10.5281/zenodo.22727389. Its full PDF
render and fresh public-byte/metadata verification passed. The complete public replay QA
passed: 20 scenarios, five viewports, both languages/themes, 960 screenshots, and separate
visual reviews. The full Python suite has 251 passing tests; frontend tests, build and
applicable guards pass. Evidence: [release QA](release-0.64.000/README.md).

Research [PR #263](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/263) merged at
`00eace9e2a746c0b4122c5b085b84d804f5f47a0`. Release
[PR #264](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/264) merged to main at
`08660dc2d6bc91eae0d3a5105447793f0fbc670c`, tagged `v0.64.000`.
[Pages run 34706614866](https://github.com/fsantibanezleal/CAOS_RESEARCH/actions/runs/34706614866)
succeeded. The [live receipt](release-0.64.000/live-verification.json), verified at
2026-09-12 17:01:22 UTC, records 13 public files matching the reviewed build/data bytes
and eight passing desktop/phone language/theme scenarios with 224 screenshots. Console,
page and HTTP error arrays are empty in every scenario. These observed delivery gates
close RH-008; they do not establish mathematical acceptance.

[EXP-003](../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/hypothesis.md)
is declared to test odd-frame amplification, then a bounded pressure-certificate search.
Its [prior-art preflight](../../problems/number-theory/riemann-hypothesis/context/2026-09-12-pressure-frame-prior-art.md)
and expanded archive are complete. Implementation, runs, independent validation and verdict
remain pending. The published EXP-002 numerical bound remains the latest validated local
bound at this snapshot.
