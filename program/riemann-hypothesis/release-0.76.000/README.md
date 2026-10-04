# Riemann release 0.76.000: longer short-window moment

EXP-028's internally reviewed uniform shifted mollified second moment admits

    1/2 < theta < 1,
    0 < nu < min(1/2, (17/33)(2theta-1)).

Before the cap at 1/2, the admissible exponent range is 34/33 times the
earlier `nu < theta-1/2` range. Two analytic routes, Mellin separation and an
exact Hankel symbol, retain both residues, shift coalescence, unbalanced
blocks, all signed coefficients, gcd sums, fixed general Q, far tails and
the narrower Gaussian used for compact windows. This is the substantive
gain; it does not come from another detector search.

The unchanged detector and EXP-010 counting/parity transfer, through Wang's
attributed pair input, give a positive asymptotic simple-critical density in
every `(T,T+T^theta]` for every fixed theta in `[0.5339,1)`. At the frozen
endpoint, the independent rational audit certifies
`h(0.5339) > 0.0003985233159135`; the earlier repository onset was 0.534.
The charged exponents are `-7/250000` and `-937/400000`.

Levinson v0.02 is published as
[version DOI 10.5281/zenodo.23132248](https://doi.org/10.5281/zenodo.23132248),
[concept DOI 10.5281/zenodo.22984154](https://doi.org/10.5281/zenodo.22984154).
All fourteen PDF pages were inspected. The 80-member source package replays
all three auditors after extraction, and both public downloads match their
exact reviewed bytes. See the immutable
[publication receipt](../../../manuscripts/riemann-hypothesis/short-interval-levinson/versions/v0.02/publication-receipt.json).
Earlier published files remain unchanged.

The replay-v9 export adds `riemann-short-window-moment-v1`, with twenty-three
committed input roles and fail-closed source, analytic review, arithmetic and
publication checks. All six existing tabs explain the result in EN/ES and
both themes. Experiments 026-028 join the viewer; EXP-010 stays historical,
and suspended EXP-019 and stopped incomplete EXP-023 stay excluded from
admitted candidate bounds.

RH remains open. The analytic theorem relies on attributed Bettin-Chandee,
Young and Wang inputs and internal review. Arithmetic controls do not prove
the universal theorem. External peer review, worldwide priority, independent
formalization and an effective starting height remain unestablished.

[Focused validation](validation.json) records 55 selected research/export
tests, 34 frontend tests, TypeScript/build, Ruff and repository guards.
[Scope comparison](scope-check.json) verifies all 264 unrelated experiment
records, other scientific payloads and frozen earlier manuscripts unchanged.
The four unsuccessful QA attempts are retained and excluded in
[prior attempt dispositions](prior-qa-attempts.json).

The complete local rendered matrix passes: 20 scenarios, 120 tabs and 6,354
full-panel screenshots, followed by the corrected-build regression with 20
scenarios, 120 tabs and 1,760 screenshots. All actual PNG bytes are hash-checked.
The separate clarification replay passes 20 scenarios and 40 screenshots.
Selected final images pass [manual review](manual-final-review.json); the
two earlier stale paragraphs and their resolution remain in the review history.

App delivery passes: PR #371 merged to develop with CI 37190215722;
PR #372 merged to main at fc4f82685bb5104443236da5a8d5d5c723ae45e0, with CI
37190319416 and Pages 37190319392 passing. Tag v0.76.000 records this
build. All 76 live files match the actual CI artifact and reviewed
candidate. Production replay passes 8 scenarios, 48 tabs and
704 verified PNGs; selected production inspection passes.
See [promotion](promotion.json), [live byte verification](production-byte-verification.json)
and [production replay](qa-production.json).
