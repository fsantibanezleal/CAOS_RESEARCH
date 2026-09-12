# Riemann hypothesis state

Updated: 2026-09-12. Current public release: **0.64.000**, deployed and live-verified.
Current research round: **EXP-003 confirmed; broader alternatives in source preflight**.

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
[PR #266](https://github.com/fsantibanezleal/CAOS_RESEARCH/pull/266) is a draft;
publication of a v0.02 expansion and its public replay release are not complete.
The sole published preprint remains v0.01, DOI 10.5281/zenodo.22727389.

The user's latest direction broadens the investigation beyond constant tuning.
Three independent source-led reviews examine classical odd/critical zero counts and
multiplicity, spectral negative-mass/optimization witnesses, and alternative RH
reformulations such as Nyman-Beurling approximation and positivity criteria. No
new experiment in those families has run. Their claims remain proposals until the
source-complete gate, declaration commit, proof, and adversarial validation pass.

The established result does not lower the positivity exponent or solve RH. A possible
multiplicity/parity transfer is being investigated precisely because it may change
the interval range; this state does not prematurely adopt that proposed consequence.

The first release closure is recorded in [its live receipt](release-0.64.000/live-verification.json):
public PRs #263/#264 merged, main 08660dc, tag v0.64.000, successful Pages run
34706614866, 13 exact live-file comparisons and eight passing live UI scenarios.
Private coordination PRs #631/#632 are also merged; its develop/main heads were
verified at 2bde950d. Unrelated original worktrees remain preserved.
