# Riemann release 0.74.000: short-interval Levinson onset and the method's limit

This release packages EXP-010, EXP-011 and EXP-012 into replay v9 and the
bilingual twelve-experiment workbench. The Riemann hypothesis remains open.

## Mathematical content

EXP-010 (confirmed) localizes Levinson's method with Conrey's general operator
polynomial to every interval `(T,T+T^theta]` with mollifier exponent
`nu<theta-1/2`, as a count of distinct sign changes of Hardy's function. Fed into
the unchanged EXP-006 Hilbert-parity product, it gives a positive proportion of
simple critical zeros in every sufficiently high interval of length `T^theta`
for every fixed `theta>=0.534`, and

```text
h(0.5459) > 0.0177638490
```

which is more than 999 times the EXP-008 value at the same `theta`. The preprint
is public at [10.5281/zenodo.22984155](https://doi.org/10.5281/zenodo.22984155).

EXP-011 (confirmed) is a certified counterexample result: for the
Montgomery-Taylor window, no linear refinement `Q>=2N+beta O-4S` of the product
holds with `beta>=2.365`. Configuration C1 gives `Q-(2N+3O-4S)=-0.0582180002...`
and the lattice configuration C2 gives `(Q-2N)/O=2.35886369542621`.

EXP-012 (inconclusive) stopped the Tang reciprocity route: the dual moment weight
has size `H/sqrt(T)`, so the preflight target could not be reached.

EXP-010 uses Wang's recent unreviewed short-interval pair theorem. The results are
asymptotic with no effective starting height, and they prove neither RH nor
universal simplicity.

## Candidate validation

Replay v9 binds the EXP-010 canonical result, receipt, declaration, audit,
controls and fourteen proof-review hashes; the EXP-011 result, receipt, amended
declaration and audit; and the EXP-012 declaration, weight-size check and
verdict. The export fails closed on any hash mismatch.

The full Python suite passed 466 tests and the frontend passed 28 tests,
TypeScript and the production build. Ruff and the content, governance,
structure, template and artifact guards all passed; [qa.json](qa.json) records
them.

The browser matrix passed eight scenarios (desktop and phone, English and
Spanish, light and dark). It visited all six research tabs in each scenario and
opened the hypothesis and verdict of all twelve experiment records. It captured
416 images with zero failed checks, console errors or warnings, page errors,
request failures or HTTP errors. Representative images are committed under
[`screenshots/`](screenshots/). The raw receipt stays in the ignored local QA
archive; `qa.json` binds it by size and SHA-256.

The workbench also fixes a label bug: every experiment after EXP-007 used to be
titled "Rank-six local transfer".

## Deployment

Research PR [#346](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/346)
and promotion PR
[#347](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/347) are merged.
Main commit `a464bdb52d88ed22582668d9c94ebbe25262b5b4` passed
[CI](https://github.com/fsantibanezleal/CAOS_RESEARCH/actions/runs/36373913886)
and the
[Pages deployment](https://github.com/fsantibanezleal/CAOS_RESEARCH/actions/runs/36373914102).
The [live verification](live-verification.json) byte-matched the root, the
hashed JS and CSS assets, all KaTeX fonts, and the four replay and registry data
files against the exact-main build. The live browser matrix could not run
because the sandbox Chromium did not trust the egress TLS-inspection CA. The
live payload is byte-identical to the candidate, and the candidate matrix passed.
Tag `v0.74.000` is still to be created on the main commit: the cloud session's
git proxy refuses tag pushes.
