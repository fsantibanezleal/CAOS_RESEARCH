# Riemann hypothesis state

Updated: 2026-09-26. Latest completed public application release:
**0.73.000**, live-verified from main commit
`e6f905f8509adbb9be7e9470b88b5071a4a08d9e`. EXP-009 is confirmed,
manuscript v0.01 is published, and replay v8 is deployed and live-verified.

The Riemann hypothesis remains open.

## Current strongest result

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
