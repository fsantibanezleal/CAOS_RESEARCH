# Riemann release 0.70.000: explicit local Selberg threshold

This release packages the confirmed EXP-005 localization theorem, its exact
certificate, the `riemann-replay-v4` source bindings and manuscript v0.05. The
Riemann Hypothesis remains open.

## Mathematical result

For every fixed `1/2 < theta < 1`, the localized optimized Selberg detector
gives

`liminf O(T,T^theta)/N(T,T^theta) >= (theta-1/2)/(4 e C3)`.

Combining it with the exact EXP-004 parity identity and Wang's short-interval
calculation gives

`liminf S/N >= max(0, c(theta), (c(theta)+(theta-1/2)/(2 e C3))/3)`.

The unique new positivity threshold lies in `(0.5459,0.546)`. At
`theta = 0.546`, the fixed admissible witness `u = 0.02299` proves
`S/N > 0.0000976239413345396825`; the optimized curve gives
`S/N > 0.0000994910410327771597`.

The theorem is asymptotic. It gives no effective starting height, does not
reach `theta = 1/2`, and does not prove universal simplicity or RH.

## Candidate validation

The release candidate starts from develop merge
`c0a0d030dab24f9e721646304ef8f524adf0ada2`. The full data bake includes all
five Riemann experiment records. The production build passed 16 frontend tests,
TypeScript, Ruff, the content/structure/template guards and the scoped Riemann
tests. Research PR #309 passed all 415 Python tests in a fresh Linux checkout.

The pointer-driven browser harness passed 20 scenarios, 120 research-tab visits
and 2,370 screenshots at 1440x1000, 390x844, 1280x800, 1600x900 and 2560x1440,
in English and Spanish and in both themes. It reported zero console, page,
request, HTTP, interaction or layout failures. Seven representative captures
were inspected for the summary, results catalogue, EXP-005 verdict, exact
threshold disclosure and science architecture.

The raw browser receipt remains in the ignored local evidence directory; its
64,270,168 bytes and SHA-256 are recorded in [qa.json](qa.json). The manuscript
is published at [10.5281/zenodo.22851518](https://doi.org/10.5281/zenodo.22851518),
and its fresh public download matched the reviewed 526,178-byte PDF.

## Deployment

The release PR, tag, Pages run and live-file/browser verification are recorded
after main promotion in `live-verification.json`. Until that receipt exists,
this directory proves candidate validation rather than deployment.
