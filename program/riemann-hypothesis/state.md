# Riemann hypothesis state

Updated: 2026-09-20. Latest completed public application release:
**0.71.000**, live-verified from main commit
`8302be35cb96280692ad1333d690a63cb220f8b2`. Current research round:
**EXP-007 and EXP-008 confirmed, manuscript v0.07 published, release 0.72.000
candidate validation in progress**.

The Riemann hypothesis remains open.

## Current strongest result

EXP-008 proves that the local Selberg detector transfer works for every fixed
finite rank $q$:

$$
\liminf_{T\to\infty}\frac{O(T,T^\theta)}{N(T,T^\theta)}
\ge k_q(\theta)=\frac{\theta-1/2}{4eC_q}.
$$

Using Pearce-Crump's stated source-certified rank-six interval in the EXP-006
Hilbert-parity product gives

$$
0.5458837<\theta_6<0.5458838
<0.5458846<\theta_3<0.5458847.
$$

At theta=0.545884, the rank-six term exceeds
`2.5541123454645702e-7` while the rank-three term remains negative. At
theta=0.5459, the rank-six lower bound exceeds
`0.0000177645181613023236390595079` and its pointwise gain over rank three
exceeds `9.263543061777356e-7`.

The source prints the certified $C_6$ interval but not the coefficient matrix.
The result is therefore confirmed relative to that attributed input. CAOS has
not independently reconstructed $C_6$.

## Spectral companion

EXP-007 proves

$$
(Q-S-D(G))(N-O)\ge2(N-S)^2.
$$

It strictly improves every positive point of the scalar curve. With the
rank-six input and optimized fixed radius `rho=11/5`, the gain at theta=0.5459
exceeds `1.7766622541125682e-68`. This does not move the onset.

## Portable evidence

| Evidence | Current portable canonical SHA-256 |
|---|---|
| EXP-007 result | `98094f267a78b88b8a976de6b6d816fbb25231869a6ad5dc8c941411bfa45947` |
| EXP-008 result | `1ccfa56face643fb96148856c4608577b3afa75947383cf738423ce13eeb5781` |
| Manuscript v0.07 PDF | `c7bda5f1acc0b34ac33b6a071e66586b4032ae6e385d93f7fdd2d197411dbf81` |

The runners write explicit UTF-8/LF bytes. The historical Windows byte streams
cited by manuscript v0.07 remain preserved under
`artifacts/windows-canonical-v1/`. Replay v7 reads committed bytes, validates
execution receipts and proof-review hashes, and fails closed on weakened claims
or stale evidence.

## Publication and release

Manuscript v0.07 is published at
[10.5281/zenodo.22860012](https://doi.org/10.5281/zenodo.22860012). The reviewed
30-page PDF matches a fresh unauthenticated public download byte for byte.
Publication is not peer acceptance.

Release candidate 0.72.000 exposes EXP-007 and EXP-008 in the bilingual
workbench. It still requires rendered browser QA, scoped promotion, and live
deployment verification. Until those gates pass, 0.71.000 remains the latest
completed application release.

The result is asymptotic for each fixed exponent and has no effective starting
height. Imported 2026 preprints remain attributed. No finite census, exact
certificate, DOI, or passing build proves RH.
