# Riemann release 0.73.000: sharp three-point kernel

This release packages EXP-009, replay v8, the bilingual nine-experiment
workbench, and the published sharp-kernel preprint. The Riemann hypothesis
remains open.

## Mathematical result

EXP-009 proves, for nonnegative `alpha,beta`,

```text
R(alpha,beta) <= sqrt(2),
```

with equality exactly at `(0,1)` and `(1,0)`. Under the attributed global
framework in Wang, arXiv:2609.24167v1, the sharp constant changes the admissible
parameter to

```text
d_dagger = 0.283165430808537327...
```

and gives the conditional simple-critical proportion

```text
0.6725007995946757558283550562963947865...
```

The gain over the source baseline exceeds `9.5915e-8`; the independently
reproduced source correction lies between `6.66624e-8` and `6.66625e-8`.
The same kernel produces a positive but onset-neutral companion gain for the
short-interval rank-six curve at `theta=0.5459`.

The ratio theorem is proved exactly in the repository. The global transfer is
attributed to a recent unreviewed preprint, the short-interval pair and rank-six
inputs remain attributed, and there is no effective starting height. The result
does not prove RH, universal simplicity, or external peer acceptance.

## Publication and candidate validation

The seven-page preprint is public at
[10.5281/zenodo.22940291](https://doi.org/10.5281/zenodo.22940291). Its fresh
public download and repository PDF are both 323,565 bytes with SHA-256
`a60e2c21ebe3237d867ca94b682f86bb24a9cec868393e7d6a9e6eb31b510d82`.

The exact EXP-009 result has SHA-256
`0cea78e847d1bcec62eb8cd809b704ceaebd58f78f1c405f13ec40838fbb5a66`.
The scoped Python suite passed 64 tests. The frontend passed 24 tests,
TypeScript, and the production build. Content, governance, structure, template,
artifact, manuscript-voice, and diff guards are recorded in
[qa.json](qa.json).

The exact-candidate browser matrix passed eight desktop/phone, English/Spanish,
light/dark scenarios. It visited all six research tabs in every scenario and
captured 1,586 images with no failed checks, console errors or warnings, page
errors, request failures, HTTP errors, or layout failures. Representative
summary, EXP-009 verdict, and architecture images are committed under
[`screenshots/`](screenshots/); the raw receipt remains in the ignored local QA
archive and is bound by size and SHA-256 in `qa.json`.

## Deployment

Research PR [#337](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/337)
and promotion PR
[#338](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/338) are merged.
Tag `v0.73.000` points exactly to main commit
`e6f905f8509adbb9be7e9470b88b5071a4a08d9e`; the
[GitHub release](https://github.com/fsantibanezleal/CAOS_RESEARCH/releases/tag/v0.73.000),
[main CI](https://github.com/fsantibanezleal/CAOS_RESEARCH/actions/runs/36268684854),
and [Pages deployment](https://github.com/fsantibanezleal/CAOS_RESEARCH/actions/runs/36268684851)
all passed.

The [live verification](live-verification.json) byte-matched the root, three
hashed assets, and seven replay/manifest files against the exact-main build.
Eight desktop/phone EN/ES light/dark scenarios visited all six research tabs
and captured 368 screenshots with zero failed checks, console warnings or
errors, page errors, request failures, or HTTP errors. The live payload exposes
replay v8, the exact EXP-009 canonical hash, the sharp equality cases, the
global and short-interval gains, and the explicit attribution and non-claim
boundary. The static direct route returns the expected Pages 404 response;
pointer navigation from the 200 root reached and verified the client route.
