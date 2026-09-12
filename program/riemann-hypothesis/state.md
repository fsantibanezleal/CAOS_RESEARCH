# Riemann hypothesis state

Updated: 2026-09-12. Release candidate: **0.65.000**, locally validated; main deployment and live verification are pending.
Current research round: **EXP-003 and EXP-004 confirmed; v0.02 published on Zenodo and replay integrated**.

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
at `65980d33f40c291c86a384420afa888b53abbea0`;
the expanded preprint is published at [10.5281/zenodo.22728744](https://doi.org/10.5281/zenodo.22728744)
the public replay release candidate is validated in
[release-0.65.000](release-0.65.000/README.md). The v0.01 record remains immutable
at DOI 10.5281/zenodo.22727389.

The user's latest direction broadened the investigation beyond constant tuning.
Three primary-source dossiers now cover classical odd/critical zero counts and
multiplicity, spectral negative-mass/optimization witnesses, and alternative RH
reformulations. Commit be5aac4 preserves the cross-area review and verified archive.
EXP-004 was declared and pushed in e03413b before implementation or computation.
Its finite parity certificates, source conventions, seed packing and legal support
limits, complete proof, exact runner, final proof review and verdict are confirmed.
No further computational family is declared.

EXP-003 does not lower the positivity exponent or solve RH. EXP-004 confirms a
qualitative extension below the zero of Wang's cosine curve. Its imported classical
density is positive but unspecified; no new decimal exponent is claimed. General
RH remains open.

The first release closure is recorded in [its live receipt](release-0.64.000/live-verification.json):
public PRs #263/#264 merged, main 08660dc, tag v0.64.000, successful Pages run
34706614866, 13 exact live-file comparisons and eight passing live UI scenarios.
Private coordination PRs #631/#632 are also merged; its develop/main heads were
verified at 2bde950d. Unrelated original worktrees remain preserved.
