# Riemann release 0.71.000: Hilbert-parity compression

This release packages the confirmed EXP-006 finite theorem, its exact
certificate, the `riemann-replay-v5` source bindings, and manuscript v0.06.
The Riemann hypothesis remains open.

## Mathematical result

For every nonempty conjugation-invariant finite multiset in Lamzouri's kernel
setting, EXP-006 proves the sharp inequality

`(Q-S)(N-O) >= 2(N-S)^2`.

Here `N` counts copies, `S` counts simple real support, `O` counts distinct
odd-multiplicity real support, and `Q` is the squared-kernel pair sum. Combining
this finite theorem with Wang's fixed-test pair asymptotic and the localized
EXP-005 odd-support curve gives the new term

`h3(theta) = [3+k3(theta)-sqrt((1-k3(theta))(9-k3(theta)-8c(theta)))]/4`.

Its unique positivity root is certified in `(0.545884,0.545885)`. At
`theta=0.5459`, `h3` is greater than
`0.0000168381638551244569880374399` while the earlier linear parity term is
still negative. The theorem is asymptotic for each fixed exponent. It supplies
no effective starting height, does not improve the global 67.25 percent record,
and does not prove RH or universal simplicity.

## Candidate validation

The release candidate starts from develop merge
`56ef56e9bc11e6ed66db42c58abec25b7d549335`. Research PR
[#316](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/316) passed all
428 Python tests in a fresh Linux checkout, plus Ruff, the pipeline smoke,
artifact consistency, and repository guards. The merged candidate also passed
107 scoped Riemann tests, 18 frontend tests, TypeScript, the production build,
and a fresh data bake.

The pointer-driven browser harness passed 20 scenarios, 120 research-tab
visits, and 2,632 screenshots at 1440x1000, 390x844, 1280x800, 1600x900, and
2560x1440, in English and Spanish and in both themes. It reported zero failed
checks, console warnings or errors, page errors, request failures, HTTP errors,
or layout failures. Eight representative captures were inspected for the
summary, six-record catalogue, EXP-006 verdict, exact threshold disclosure,
and science architecture on desktop and phone.

The raw browser receipt remains in the ignored local evidence directory; its
74,077,417 bytes and SHA-256 are recorded in [qa.json](qa.json). The canonical
EXP-006 result contains 18,479 finite profiles and has SHA-256
`82c4761b5c97011ff86cdd379d647ad0f94643a7eb8324a4a09aa37f58848bbf`.
The manuscript is published at
[10.5281/zenodo.22852479](https://doi.org/10.5281/zenodo.22852479), and its
fresh public download matched the reviewed 545,773-byte PDF.

## Deployment

Promotion to `main`, the release tag, Pages byte comparison, and live browser
verification are serialized gates. Their exact commits, workflow runs, and
live receipt will be recorded here after deployment.
