# Riemann hypothesis state

Updated: 2026-09-19. Release: **0.65.000**, released and live-verified from release commit `24a2cb250e44fa59c9f6a56c86eefdf009258e70` (tag `v0.65.000`).
Current research round: **EXP-005 confirmed; explicit local Selberg transfer and threshold below 0.546**.

EXP-005 responds to Pearce-Crump arXiv:2609.15329v1, which appeared after the
prior source cutoff. Its coefficient-uniform arbitrary-subinterval estimate
localizes the sign-preserving Selberg detector to every fixed exponent above one
half. The confirmed theorem gives odd-critical liminf at least
$(\theta-1/2)/(4eC_3)$. Combined with EXP-004, exact controls place the new
simple-critical positivity threshold in $(0.5459,0.546)$. At theta=0.546, a
fixed legal mollifier proves simple-critical proportion above
$0.00009762394133453968$. The canonical result hash is
`3f0ca476c0e2fe688e4e4f43fc11861d9491b3066d067e46bf88d1a441c696a5`.

EXP-004 has a separate confirmed verdict and proof-review record. It proves a
qualitative extension of the simple-critical positivity range below Wang's
cosine root: for one fixed classical density constant $\kappa>0$, a fixed
$\theta_1<\theta_0$ has $\liminf S/N\ge\kappa/3$ for every fixed
$\theta\in[\theta_1,1)$. A distinct-count inequality gives an analogous
above-one-half consequence below the root. No numerical $\kappa$, $\theta_1$,
effective height, or new decimal exponent is claimed.

[D+MV] [EXP-003](../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/verdict.md) confirms a stronger odd-frame theorem throughout
the complete positive short-interval cosine curve and a new pressure certificate.
At theta=3/4, its bound is 0.419087888170111727959091183775, with distinct companion
0.709543944085055863979545591887. The Wang baseline is 0.419075012975424333734553610698;
the first published EXP-002 example is 0.419076828425303996736665787527.

The new certificate has 16,797 nodes, 8,351 energy-plus-pressure leaves, 48 pressure
leaves and zero unresolved cells. Construction at 160 bits and complete sinc-Taylor
replay at 256 bits passed. Stage A also replayed all 48,761 earlier nodes and checked
328 incidence/boundary cases. The full repository suite passed **288 tests** after
the new committed-source export gates. Shared Arb/geometry and external analytic
premises remain explicit; this is not end-to-end Lean verification or peer review.

The theorem, separate-stage verdict, source audit, scientific code, candidates and
canonical results are committed and pushed in the pressure work branch. Research
[PR #266](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/266) merged to develop
at `65980d33f40c291c86a384420afa888b53abbea0`; release PR [#267](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/267), develop synchronization [#268](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/268), live receipt [#269](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/269), and main promotion [#270](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/270) are merged.
the EXP-005 manuscript is published as v0.05 at [10.5281/zenodo.22851518](https://doi.org/10.5281/zenodo.22851518)
the public replay release is live-verified in
[release-0.65.000](release-0.65.000/README.md). The v0.01 record remains immutable
at DOI 10.5281/zenodo.22727389. The v0.05 public download matches the reviewed
24-page PDF at SHA-256 `bcfefac4b138d2b41c5fe232c64590e3b6f0c309455d40e01451d9251c1e8acc`.

The user's latest direction broadened the investigation beyond constant tuning.
Three primary-source dossiers now cover classical odd/critical zero counts and
multiplicity, spectral negative-mass/optimization witnesses, and alternative RH
reformulations. Commit be5aac4 preserves the cross-area review and verified archive.
EXP-004 was declared and pushed in e03413b before implementation or computation.
Its finite parity certificates, source conventions, seed packing and legal support
limits, complete proof, exact runner, final proof review and verdict are confirmed.
EXP-005 is confirmed in `5132beed` after a source-bound exact certificate and
term-by-term analytic audit. No further computational family is declared.

EXP-003 does not lower the positivity exponent or solve RH. EXP-004 confirms a
qualitative extension below the zero of Wang's cosine curve. EXP-005 replaces
the unspecified density for $\theta>1/2$ by an explicit curve and proves the
decimal threshold bracket above. The result has no effective onset height.
General RH remains open.

The first release closure is recorded in [its live receipt](release-0.64.000/live-verification.json):
public PRs #263/#264 merged, main 08660dc, tag v0.64.000, successful Pages run
34706614866, 13 exact live-file comparisons and eight passing live UI scenarios.
The expanded release closure is recorded in [the v0.65 live receipt](release-0.65.000/live-verification.json): CI and Pages runs 34718338752, 34718338730, 34719132932, and 34719132914 passed; deployed assets and data hashes matched; eight EN/ES light/dark desktop/phone scenarios visited all six research tabs, with 48 tab visits, 288 screenshots, and zero failures. Private coordination PRs #631/#632/#635/#636 are merged; private main/develop now contain the synchronized v0.65 records. Unrelated original worktrees remain preserved.
