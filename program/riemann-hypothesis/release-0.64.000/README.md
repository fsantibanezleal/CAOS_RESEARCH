# Riemann release 0.64.000: validation evidence

Release v0.64.000 is deployed and live-verified. The research and release PRs are merged,
the release tag is present, and the live receipt closes the web delivery gate. The
[preprint](https://doi.org/10.5281/zenodo.22727389) is published; its frozen public PDF and
metadata were verified independently of the website.

## Observed release closure

- Research [PR #263](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/263) merged at
  `00eace9e2a746c0b4122c5b085b84d804f5f47a0`.
- Release [PR #264](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/264) merged to main
  at `08660dc2d6bc91eae0d3a5105447793f0fbc670c`, tagged `v0.64.000`.
- [Pages run 34706614866](https://github.com/fsantibanezleal/CAOS_RESEARCH/actions/runs/34706614866)
  succeeded, and the deployed site is [research.fasl-work.com](https://research.fasl-work.com/).
- [Live verification](live-verification.json), recorded at 2026-09-12 17:01:22 UTC,
  checks 13 public build/data files against the reviewed bytes and records eight passing
  pointer-driven browser scenarios with 224 screenshots. The live matrix covers
  1440x1000 and 390x844, EN/ES and light/dark, with all six research tabs visited.
  Every scenario has empty console, page and HTTP error arrays.

The receipt is preserved as an exact 5,958-byte copy of the original live record,
SHA-256 `fb35a9d06d82ef3befafaf2a8ee6e412c67ccff014785725dc63eca27d69ebc6`.
Its two referenced raw-receipt hashes were checked against the retained local evidence.
The live screenshots and raw receipts remain in ignored `tmp/riemann-live-0.64/`;
the public summary preserves their hashes and scenario outcomes. These deployment
checks are separate from mathematical proof acceptance and the earlier visual sampling.

## Automated and visual evidence

[qa.json](qa.json) records the exact frontend source commit, build files, data hashes,
test results, 20 browser scenarios and 960 screenshot hashes. The matrix covers 1440x1000,
390x844, 1280x800, 1600x900 and 2560x1440, English/Spanish and light/dark, all six research
sections, proof-stage controls, experiment records and architecture panels. All automated
gates pass. The full Python suite has 251 passing tests; two frontend tests, TypeScript/build,
Ruff and content/template/structure/artifact-contract checks pass.

Separate agent visual inspections are recorded in [light review](review-light.md) and
[dark review](review-dark.md), with exact inspected filenames and explicit sampling scope.
They inspect 72 and 68 original screenshots respectively. An additional root review inspected
six-section overviews at 1440x1000 and 2560x1440 in complementary language/theme combinations,
plus full-resolution strategy and phone-verdict views. These reviews are not a claim that
every screenshot was individually inspected, nor human peer review of the mathematics.

The [supplementary architecture receipt](architecture-lower/receipt.json) records 16 successful
checks of complete Method/Science diagrams and bottom source links, using real mouse-wheel
scrolling after locator-click setup. Its [script](review-architecture-lower.cjs) is retained.
The main matrix separately verifies pointer navigation from Program and shell controls.

The pre-existing Program page's document dimensions are measured but are outside this
Riemann route's viewport certification. The new route and its dialogs fit their viewports;
long prose, equations and navigation rows use their declared internal scroll containers.

## Representative captured views

These are unmodified PNGs from the passing matrix. The complete raw set and receipts remain
in the local ignored archive `tmp/riemann-release-ui/`; the committed harness and
[reproduction guide](../../../docs/guides/riemann-replay.md) regenerate that evidence.

- [Desktop English light: strategy](screenshots/desktop-en-light-strategy.png)
- [Desktop Spanish dark: proof stages](screenshots/desktop-es-dark-proof.png)
- [Phone English light: proof stages](screenshots/phone-en-light-proof.png)
- [Phone Spanish dark: persisted EXP-002 verdict](screenshots/phone-es-dark-verdict.png)

## Findings resolved before this gate

The review corrected phone navigation wrapping, a fragmented Program touch target, Markdown
math delimiters and rendering, relative experiment links, inherited Jacobian content in the
Riemann architecture panels, Windows newline-dependent replay hashes, and export dependence
on dirty or locally deleted experiment files. The failed diagnostic receipts were retained
locally; only the fresh passing matrix supports this gate.

The mathematical scope is unchanged: a strict asymptotic short-interval refinement based on
the inspected analytic input, with a certified example. RH, an effective starting height,
a lower positivity exponent, global-record status and external proof acceptance remain open.
