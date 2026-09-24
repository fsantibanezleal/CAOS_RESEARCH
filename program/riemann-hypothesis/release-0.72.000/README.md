# Riemann release 0.72.000: rank-six local transfer

This release packages the confirmed EXP-007 spectral-defect refinement,
EXP-008 fixed-finite-rank localization, their exact certificates, replay v7,
and manuscript v0.07. The Riemann hypothesis remains open.

## Mathematical result

EXP-007 proves the finite inequality

`(Q-S-D(G))(N-O) >= 2(N-S)^2`.

It gives a strict improvement wherever the scalar Hilbert-parity curve is
positive. EXP-008 proves that the local Selberg detector transfer works for
every fixed finite rank and gives

`liminf O(T,T^theta)/N(T,T^theta) >= (theta-1/2)/(4eC[q])`.

Applying Pearce-Crump's stated rank-six interval moves the positivity onset to
`0.5458837 < theta6 < 0.5458838`, compared with the independently replayed
rank-three bracket `0.5458846 < theta3 < 0.5458847`. At `theta=0.545884`, the
rank-six term exceeds `2.5541123454645702e-7` while the rank-three term remains
negative. At `theta=0.5459`, the rank-six lower bound exceeds
`0.0000177645181613023236390595079` and improves rank three by more than
`9.263543061777356e-7`.

The source prints the certified rank-six constant interval but not its
coefficient matrix. The rank-six application is therefore attributed and is
not an independent reconstruction. The theorem is asymptotic for each fixed
exponent, supplies no effective starting height, and proves neither RH nor
universal simplicity.

## Candidate validation

The release candidate starts from develop merge
`fe5515bac5400872467af3c1f4a9fe4766daa829`. Research PR
[#325](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/325) passed 443
Python tests in a fresh Linux checkout, plus Ruff, the pipeline smoke, artifact
consistency, and repository guards. The merged candidate also passed 66 scoped
Riemann and export tests, 22 frontend tests, TypeScript, the production build,
and all local content, structure, manuscript-voice, template, and artifact
guards.

The pointer-driven browser harness passed 20 scenarios, 120 research-tab
visits, and 3,072 screenshots at 1440x1000, 390x844, 1280x800, 1600x900, and
2560x1440, in English and Spanish and in both themes. It reported zero failed
checks, console warnings or errors, page errors, request failures, HTTP errors,
or layout failures. Visual inspection covered the summary, eight-record
catalogue, EXP-007 and EXP-008 verdicts, and workflow architecture on desktop
and phone. It identified and corrected one overflowing eight-experiment SVG
label before the final matrix was recorded.

The raw browser receipt remains in the ignored local evidence directory; its
91,615,727 bytes and SHA-256 are recorded in [qa.json](qa.json). The portable
canonical EXP-007 result has SHA-256
`98094f267a78b88b8a976de6b6d816fbb25231869a6ad5dc8c941411bfa45947`, and
the EXP-008 result has SHA-256
`1ccfa56face643fb96148856c4608577b3afa75947383cf738423ce13eeb5781`.
Manuscript v0.07 is published at
[10.5281/zenodo.22860012](https://doi.org/10.5281/zenodo.22860012); its fresh
public download matched the reviewed 575,351-byte PDF exactly.

## Deployment

Release PR [#330](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/330)
and promotion PR
[#331](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/331) are merged.
Tag `v0.72.000` points exactly to main commit
`45c34c810ffb20a03afbb32fccd63c3e7abd82f5`; the
[GitHub release](https://github.com/fsantibanezleal/CAOS_RESEARCH/releases/tag/v0.72.000),
[main CI](https://github.com/fsantibanezleal/CAOS_RESEARCH/actions/runs/35948883726),
and [Pages deployment](https://github.com/fsantibanezleal/CAOS_RESEARCH/actions/runs/35948883705)
all passed.

The [live verification](live-verification.json) byte-matched the root, three
hashed assets, and seven replay/manifests files against the exact-main build.
Eight desktop/phone EN/ES light/dark scenarios visited all six research tabs
and captured 352 screenshots with zero failed checks, console warnings or
errors, page errors, request failures, or HTTP errors. The live payload exposes
replay v7, both portable canonical hashes, the rank-six and rank-three onset
brackets, and the pointwise and spectral gains. The static direct route returns
the expected Pages 404 response; pointer navigation from the 200 root reached
and verified the client route.
