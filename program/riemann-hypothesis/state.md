# Riemann hypothesis state

Updated: 2026-09-12. Lifecycle: **consolidating**.

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
render and fresh public-byte/metadata verification passed. Public replay QA and scoped
promotion remain release gates. See `RESUME.md` and the source experiment verdicts.
