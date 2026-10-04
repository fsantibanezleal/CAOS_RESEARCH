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

The complete rendered matrix is still in progress. PR #371 remains draft;
main promotion, tag, actual Pages artifact/live byte identity and full
production replay are required before this release is delivered. Local
validation and manuscript publication do not attest deployment.
