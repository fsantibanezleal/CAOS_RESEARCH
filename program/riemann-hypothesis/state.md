# Riemann hypothesis state

Updated: 2026-10-03. Latest public application release: **0.74.000**
(replay v9, EXP-010 to EXP-012 in the workbench), promoted to main commit
`a464bdb52d88ed22582668d9c94ebbe25262b5b4`; live bytes match the exact-main build
([record](release-0.74.000/live-verification.json)). Previous: 0.73.000 from
`e6f905f8509adbb9be7e9470b88b5071a4a08d9e`. EXP-010 is confirmed on its work
branch after two referee passes, merged to `develop` and promoted to `main`; its
manuscript `short-interval-levinson` v0.01 is published at
[10.5281/zenodo.22984155](https://doi.org/10.5281/zenodo.22984155). The public
workbench shows it since release 0.74.000.

The Riemann hypothesis remains open.

Strategic review 2026-10-03: a new distinct-zero paper improves the
strip-wide EXP-009 companion, and EXP-013 improves its fixed-input assembly
slightly. Upstream also lists a higher simple-critical candidate; neither
changes the short-window onset. The active focus remains RH-F4 after a
recorded stop/review decision; RH-F6 is closed. See the
[current dossier](../../problems/number-theory/riemann-hypothesis/context/2026-10-03-update-and-dual-family-preflight.md),
[plan](plan.md) and [governance](research-governance.json).

## Current strongest short-interval result

EXP-010 localizes Levinson's method with Conrey's general operator polynomial
`Q` to `(T,T+T^theta]`. For mollifier exponents `nu<theta-1/2` the mollified
second moment is `c(P,Q,R,nu) w-hat(0)+O(H/L)` (Young's short proof with a
window weight), and for every `Q` with `Q(x)+Q(1-x)` constant the method
counts distinct sign changes of `Z`:

```text
liminf O(T,T^theta)/N(T,T^theta) >= kappa = 1 - log(c(P,Q,R,nu))/R
```

Degree-201 detectors certify `kappa>0.7170 nu`, against the rank-six Selberg
slope `0.140`. Through the EXP-006 product:

```text
every fixed theta in [0.534,1): positive proportion of simple critical zeros
theta=0.534   h > 1.4806994e-5     theta=0.5459  h > 0.0177638490
theta=0.535   h > 0.0015246940     theta=0.55    h > 0.0237708528
theta=0.54    h > 0.0090231376
```

The previous onset was `0.5458838` (EXP-008). At `theta=0.5459` the new bound
is about 1000 times the EXP-008 value. Above about `theta=0.567` Wang's
`c(theta)` remains the largest term. The moment and counting theorems are
internal; the onset uses Wang's arXiv:2609.07918v1 pair theorem through the
EXP-006 product.

| Evidence | SHA-256 |
|---|---|
| EXP-010 canonical result | `74ed14a925bdd10f27d09d6fb23a8e43f9474f8e0e5280fceafac33e06f49464` |
| EXP-010 independent audit | `b3a5fa0ae2ea54bcd1c4f323acfae3c81c87202780018ea8c29e798c674a4df1` |
| EXP-010 counting-lemma controls | `6ecab20fcd1c90632d2d4c20c9fe41ae51e40e05eee0e1540c82e9934aea375c` |

## EXP-009 global simple-critical result

EXP-009 proves the sharp auxiliary theorem

$$
R(\alpha,\beta)\le \sqrt 2\qquad (\alpha,\beta\ge0),
$$

with equality exactly at $(0,1)$ and $(1,0)$. With
$\alpha=\sinh u$, $\beta=\sinh v$, the proof reduces to a one-variable
endpoint and then to $(X^2-2)^2\ge0$.

Under the global framework attributed to Wang, arXiv:2609.24167v1, whose own
printed bound is `C_0+delta_0=0.6725007703...`, this gives a value about
`2.9e-8` higher:

```text
d_dagger = 0.283165430808537327...
simple-critical proportion >= 0.6725007995946757558283550562963947865...
distinct zeros anywhere in strip proportion >= 0.8362503997973378779141775281481973932...
```

The gain over the source baseline exceeds `9.5915e-8`. The independently
reproduced Wang correction lies between `6.66624e-8` and `6.66625e-8`.
The global transfer is attributed to a recent unreviewed preprint; it is not an
independent reproof of that framework.

## Short-interval companion

The same sharp kernel transfers through the existing Hilbert-parity product.
At `theta=0.5459`, its positive gain over EXP-008 is certified between
`3.0867809983334187e-31` and `6.1735619966669657e-31`. It does not move the
rank-six positivity onset. The pair-correlation and rank-six inputs remain
attributed.

## Portable evidence

| Evidence | Current portable SHA-256 |
|---|---|
| EXP-009 canonical result | `0cea78e847d1bcec62eb8cd809b704ceaebd58f78f1c405f13ec40838fbb5a66` |
| EXP-009 execution receipt | `86e6c02c7469d7635400057cc9fed484ecef60365dd2b7d3a07d2d5b36e66136` |
| Sharp-kernel manuscript PDF | `a60e2c21ebe3237d867ca94b682f86bb24a9cec868393e7d6a9e6eb31b510d82` |

Replay v8 reads committed bytes, binds both source reviews, validates source,
execution, proof-review, and publication hashes, and fails closed on weakened
claims. The exact certificate used CPU rational and interval arithmetic; a GPU
was not useful for this low-dimensional proof.

## Publication and release

The sharp-kernel preprint is published at
[10.5281/zenodo.22940291](https://doi.org/10.5281/zenodo.22940291). The reviewed
seven-page repository PDF matches a fresh unauthenticated public download byte
for byte. Publication is not peer acceptance.

Release 0.73.000 exposes all nine experiments in the bilingual
workbench. The scoped Python suite passed 64 tests and the frontend passed 24
tests plus TypeScript and production build. The exact-candidate browser matrix
passed eight desktop/phone EN/ES light/dark scenarios, 48 research-tab visits,
and 1,586 screenshots with no failures. PRs #337 and #338 are merged; exact-main
CI, Pages, eleven public byte comparisons, and eight live browser scenarios
also passed. Tag `v0.73.000` points to the verified main commit.

The result is asymptotic, has no effective starting height, and does not prove
RH or universal simplicity. Imported 2026 preprints remain attributed. No
finite census, DOI, passing build, or successful deployment proves RH.

## October source and experiment update

The attributed global distinct-zero bound from arXiv:2609.33043v1 is
0.83699288145242...; EXP-013's exact parameter improvement gives
62359683640669/74504434380000 = 0.83699291404068... and proves the
fixed-input integer cap. This counts distinct zeros anywhere in the strip.
The upstream trmdy README also lists a 0.673312742272... simple-critical
candidate, outside this replay; EXP-009 is therefore not presented as
the current worldwide global record. Those recent claims are attributed.

EXP-014/015 establish the uniform pointwise phase obstruction at
nu=theta-1/2, including squarefree twists with nonzero basic mollifier
coefficients. They do not preclude cancellation in the signed sum.
Canonical hashes: EXP-013 `c250ac76df06e8f66aaed2c720e292bf17e82923137a01ce56d9ced29d4f094b`;
EXP-014 `fb0f0d4a0d165d524a86285c8bae163297959aa9819a5181e1a89b46e3567c2f`; EXP-015 `871de5a7719bec0a077e1bda88729000d3988e20cee2940f3ef3dd6d55aa3ef8`.
No new onset or RH result. No new manuscript or Zenodo version.

Tag v0.74.000 and its GitHub release are now verified at the original
release commit; the [additive reconciliation](release-0.74.000/tag-reconciliation-20261003.json)
supersedes only the old pending-tag status. Replay v9 and the live workbench
still contain twelve experiments. EXP-013--015 are repository research
records and await a later serialized replay/UI release.

## Trace-aware follow-up, same review date

EXP-016 strengthens the block dichotomy using trace zero, and updates the
latest attributed distinct-strip bound to
69341429073721/82845897125000 = 0.83699291672944... . Its revised
scalar assembly has optimal integer block m=1311. The earlier EXP-013
cap concerns its original condition and remains correct.
Canonical SHA-256 `7b0346f7e5122efc2a5d48dc6ceb6c28f0e8341cc8a5cf57be6863a16d1c2d74`. Eleven new tests and the previous twenty
focused controls pass; the separate symbolic/matrix auditor passes.
RH-F7 closes. The short-window onset, RH status, manuscript/Zenodo
state and live replay v9 remain unchanged. RH-042 also covers EXP-016.

## Full-energy envelope follow-up

EXP-017 confirms the sharp retained-energy envelope and pressure transfer,
with the tau=1 formula attributed to upstream prior work. The exact
source-based distinct-strip candidate improves to 0.83699292567522... .
RH-F8 closes as supporting research-record; no onset/manuscript/release
change. Issue #354 tracks validation and promotion.

## Nine-point conditional follow-up

EXP-018 gives the independently checked conditional implication
Nd/N >= 3997934614153/4775549550000 = 0.83716744477146... from the
explicit pinned nine-point local inequality and source energy premise.
The local input has a candidate/log provenance discrepancy; it has not
been independently replayed here. Keep this separate from EXP-017's
seven-point attributed bound. RH-F9 closes, RH-046 / issue #356 remains
open for packet-bound replay and a later manuscript decision. No global
release, onset change, new manuscript or Zenodo version is claimed.

## Composite arithmetic layer, ongoing certificate run

EXP-021 confirms the classical shifted composite character decomposition
with complete gcd classes and primitive conductor factors. Exact controls
pass in 4.17 seconds; the proof and source are bound in its receipt.
RH-038 / issue #360 remains open for the uniform analytic reduction and
signed-family estimate. No longer mollifier, new onset or manuscript follows.
EXP-020 is still running; partial coverage does not upgrade EXP-018's premise.

EXP-022 independently confirms a fixed-window/weight pressure-family
ceiling 0.837421287797... for the counting assembly, not the actual zeros.
The candidate at p=1/1250 would imply 0.837385561059... after a new complete
universal local certificate. Issue #361 / RH-047 owns the audit. No new
lower theorem or manuscript has yet landed; the user objective remains open.

## Continued verification and signed-interface review

EXP-024 closes the exact shifted Gaussian and fixed smooth compact-window
representation step, with explicitly controlled remainders. Its main signed
moment remains open. The signed-character interface retains both frequency
signs, gcd/conductor factors and the distinction between its two Mellin
weights. The late source review rejects an incorrect displayed exponent
minimum as an imported premise and excludes the withdrawn January 2026
Kloosterman improvement. Short-support and non-abelian approaches now have
explicit conversion obligations; no new cancellation is asserted.

EXP-023's revised full cover resumed at 20:48:12 UTC on 2026-10-03 with
four workers and a six-hour operational supervisor. At 21:52 UTC 95/96
shards are complete, with no complete-certificate verdict. The earlier
EXP-020 has reached 91/96. Actual complete-output corruption checks and
an exact-byte archive builder are prepared and refuse partial output.
Draft PR #363 is pushed and unmerged. Only CI on 098c0476 is currently
verified successful; later GitHub API requests encountered network errors.
No new manuscript, DOI, release or deployment is claimed from these gates.

At 22:31 UTC both EXP-020 and EXP-023 have 95/96 completed shards.
EXP-023's additional native input audit passed all 52,240 closed cells of
both tables using hypergeometric midpoint jets and whole-cell Taylor bounds,
in 148.04 seconds. The earlier inconclusive variants remain archived.
This verified input audit does not replace the last multidimensional shard,
actual completed-output controls or exact transfer. The research goal remains
active; none of these supporting milestones is its stopping condition.
