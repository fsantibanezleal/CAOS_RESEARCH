# Riemann release 0.65.000: validation evidence

This release packages the confirmed EXP-003 pressure refinement and the EXP-004
parity-density transfer in the public replay. The Riemann hypothesis remains
open. EXP-004 is a qualitative fixed-exponent extension: its classical density
constant, new exponent and effective starting height remain unquantified.

## Pre-release closure

- The release branch starts from public develop merge `65980d33f40c291c86a384420afa888b53abbea0`.
- The replay schema is `riemann-replay-v3`; the exporter binds committed EXP-004
  source bytes, the declaration, four raw artifacts and a separate proof review.
- Zenodo v0.02 is published at [10.5281/zenodo.22728744](https://doi.org/10.5281/zenodo.22728744).
  The 21-page PDF is 498,500 bytes with SHA-256
  `56b0ce29935fe3d115d9d40432f87f82b030355b028f3ea942fd3d3c671e2b1c`.
- The earlier v0.01 archive remains immutable at
  [10.5281/zenodo.22727389](https://doi.org/10.5281/zenodo.22727389).

## Automated evidence

The release checkout passed 364 Python tests, 14 frontend tests, Ruff, the
research structure guard, the complete data bake, TypeScript and the production
build. The committed browser harness passed 20 scenarios, 120 research-tab
visits and 2,102 screenshots at 1440x1000, 390x844, 1280x800, 1600x900 and
2560x1440, in English and Spanish and in both themes. It reported zero
console, page, request or HTTP failures. The raw receipt is retained in the
ignored `tmp/riemann-ui-v065/` archive and its hash is recorded in `qa.json`.

The representative captures in `screenshots/` were inspected at desktop and
phone scale for the summary, results list, EXP-004 declaration and EXP-004
verdict. The full matrix is evidence of automated rendering and interaction;
it is not a claim that every PNG received a separate human visual review.

## Scientific boundary

EXP-003 supplies the certified numerical example at theta = 3/4. EXP-004
proves the exact parity identities and transfers one fixed positive classical
odd-zero density to a qualitative interval-range extension below Wang's cosine
root. It does not prove RH, all zeros simple, an effective height, a new decimal
positivity exponent or a new global record. Publication and automated audits do
not replace external mathematical peer review or end-to-end formalization.

Deployment, the GitHub release tag and live-file verification are recorded only
after the main-release PR and Pages run succeed.
