# Riemann hypothesis state

Updated: 2026-09-26. Latest completed public application release:
**0.73.000**, live-verified from main commit
`e6f905f8509adbb9be7e9470b88b5071a4a08d9e`. EXP-010 is confirmed on its work
branch after two referee passes, merged to `develop` and promoted to `main`; its
manuscript `short-interval-levinson` v0.01 is published at
[10.5281/zenodo.22984155](https://doi.org/10.5281/zenodo.22984155). The public
workbench does not yet show it.

The Riemann hypothesis remains open.

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

## Current strongest global result

EXP-009 proves the sharp auxiliary theorem

$$
R(\alpha,\beta)\le \sqrt 2\qquad (\alpha,\beta\ge0),
$$

with equality exactly at $(0,1)$ and $(1,0)$. With
$\alpha=\sinh u$, $\beta=\sinh v$, the proof reduces to a one-variable
endpoint and then to $(X^2-2)^2\ge0$.

Under the global framework attributed to Wang, arXiv:2609.24167v1, this gives

```text
d_dagger = 0.283165430808537327...
simple-critical proportion >= 0.6725007995946757558283550562963947865...
distinct-critical proportion >= 0.8362503997973378779141775281481973932...
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
