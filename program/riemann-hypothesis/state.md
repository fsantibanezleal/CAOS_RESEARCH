# Riemann hypothesis state

Updated: 2026-09-20. Public release: **0.71.000**, released and live-verified
from main commit `8302be35cb96280692ad1333d690a63cb220f8b2` (tag
`v0.71.000`). Current research round: **EXP-007 declared; spectral-defect
parity coupling is under proof review and has not been computed**.

EXP-006 proves the sharp finite product

$$
(Q-S)(N-O)\ge2(N-S)^2,
$$

where `N` counts copies in a conjugation-invariant finite multiset, `S` counts
simple real support points, `O` counts distinct odd-multiplicity real support,
and `Q` is Lamzouri's squared-kernel pair sum. The proof attributes the known
arbitrary-parameter Hilbert estimate, retains its simple-real term, and combines
the first-subspace dimension with parity.

With Wang's fixed-test short-interval pair theorem and the confirmed EXP-005
odd-support curve, the theorem gives

$$
\liminf S/N\ge\max\left\{0,c(\theta),
\frac{c(\theta)+2k_3(\theta)}3,
h_3(\theta)\right\},
$$

$$
h_3(\theta)=\frac{3+k_3(\theta)-
\sqrt{(1-k_3(\theta))(9-k_3(\theta)-8c(\theta))}}4.
$$

The exact certificate proves a unique positivity root in
`(0.545884,0.545885)`. At theta=0.5459 the earlier linear term is negative,
while `h3` exceeds `0.0000168381638551244569880374399`. The canonical result
SHA-256 is `82c4761b5c97011ff86cdd379d647ad0f94643a7eb8324a4a09aa37f58848bbf`.
It was executed from clean commit
`0d736fa22ce7e833200381a32e8cc89f77c660e8` after the strengthening was
committed. The 18,479-profile census, exact directed intervals, scalar barrier
witness, and independent 100-digit replay passed.

The declaration commit is
`b1febcf8a6d5830218e1df386af1e8a92c3037be`. The original broad-bracket and
weaker-transfer runs remain preserved. The proof, audit, verdict and source
bindings merged through research PR #316 into `develop`. Replay v5 is baked
and tested. Release 0.71.000 passed 428 Linux tests, 107 scoped
Riemann tests, 18 frontend tests, and 20 rendered browser scenarios with zero
failures. Manuscript v0.06 is published at
[10.5281/zenodo.22852479](https://doi.org/10.5281/zenodo.22852479); its reviewed
PDF matches a fresh public download. Main promotion, Pages, ten live byte
comparisons, and eight live browser scenarios passed.

EXP-005 remains the analytic seed: for every fixed `1/2<theta<1`, it gives odd
critical support density at least `(theta-1/2)/(4eC3)`. EXP-004 provides the
linear parity transfer, EXP-003 the pressure improvement at theta=3/4, and
EXP-002 the original compact stability certificate. The detailed history and
immutable prior artifacts remain in their experiment and release directories.

The latest completed public release is recorded in
[release-0.71.000](release-0.71.000/README.md). It includes manuscript v0.06 at
[10.5281/zenodo.22852479](https://doi.org/10.5281/zenodo.22852479), merged
research PR #316, release PR #317, promotion PR #318, successful CI and Pages,
ten byte-matched live files, and eight live EN/ES light/dark desktop/phone
scenarios. Release 0.70.000 and its receipts remain immutable.

The result is asymptotic for each fixed exponent and has no effective starting
height. The imported 2026 preprints have been source-audited, but the work has
not received external peer review or an end-to-end formal proof. The Riemann
hypothesis remains open.
