# Navier-Stokes: result and manuscript map

Updated 2026-11-19. This map separates mathematical evidence, strategic value, manuscript coverage and external novelty
(methodology 13). Experiment verdicts remain the authority for every finite result. The programme is dormant (portfolio
reviews of 2026-10-30 and 2026-11-19; reopening conditions in `state.md`).

## Status boundary

The Clay Millennium problem is open and this programme does not attempt it. The 2026 blowup results are not ours:
Alpoge and Buckmaster (forced blowup for IPM, 2D inviscid Boussinesq and 3D Euler, 2026-09-07, with Lean formalizations;
a hypodissipative Navier-Stokes result stated as believed and unreleased at the last check), the OpenAI announcement of
2026-09-08 (forced blowup for 3D Navier-Stokes for every positive viscosity and unforced 3D Euler blowup, with Lean
certificates; neither community-verified) and the programme of Cordoba and Martinez-Zoroa, who originated the layer
mechanism and hold the credit for it. The hypodissipative threshold (22 - 8 sqrt 7)/9 with rough forcing is Cordoba,
Martinez-Zoroa and Zheng's (arXiv:2407.06776). The report that the Lean proof does not correspond to the written blowup
proof is Bastounis, Circelli and Hansen's (arXiv:2610.08144). The announcement and Buckmaster's statement disagree about
the history; the records keep both and take no position.

The CAOS contributions are: the clause-by-clause statement audits of the Lean certificates and their full build and kernel
replay; the validation of a reduced modulation model against the 2D Boussinesq equations, with every criterion reported,
met or not; the derived class ceiling of layer cascades (neither growth law reaches classical viscosity); the exact
reconstruction of the published threshold from its own exponent budget; and the exponent content of the force estimates of
the published designs. Nothing here proves blowup for any equation or verifies the mathematics of either announced proof.

Internal validation and Zenodo persistence do not establish peer review or worldwide novelty. No source states the class
ceiling in the external review of 2026-10-30 [U], which is not a proof of novelty. At the 2026-11-19 refresh the new items
(Zheng, arXiv:2610.02509 and arXiv:2610.06544) were rated minor, as citations for the dormant audit paper. Every claim of
another author recorded here is theirs and not re-checked by CAOS beyond the statement, build and kernel checks named
below.

## Result blocks

| block | experiments | result status | value | manuscript home |
|---|---|---|---|---|
| Replay of the OpenAI Lean build: 11,424 jobs, zero sorryAx, the four theorems (C, D and both Euler) on three standard axioms | EXP-001 | confirmed; the statements of (C), (D) and the Euler theorem audited as faithful (NS-004) | a verification of build and statement, not of the mathematics | `blowup-claims-audit` |
| Kernel replay by leanchecker from an empty environment (NavierStokes 2,972 s, Euler 1,588 s, exit 0) | EXP-006 | confirmed | the kernel, not only the elaborator, accepts the certificate | `blowup-claims-audit` |
| Reduced modulation model against the 2D Boussinesq equations: peak rate to 4e-05 relative, frequency independence to 2.7e-04, dissipative term to 2.6e-04 absolute, three negative controls failing | EXP-002 | confirmed; one criterion not met (window maximum of the single-layer rate 2.47 percent against 2) | an instrument | `blowup-claims-audit` |
| Cascade model and the threshold sweep: alpha_c = 1/(4p) to 2.59e-06; the headline p = 11/4 + sqrt 7 at the published threshold is tautological and was downgraded | EXP-003 | confirmed; headline downgraded to a consistency relation | the class ceiling for the model | `blowup-claims-audit`, Theorem 3.1 |
| Multi-layer handoff on a frozen two-scale background: correlation 0.999 with the total gradient against 0.21 with the base | EXP-004 | pattern confirmed; the slope sub-gate not met (1.36 times the prediction); the dynamical companion without steering inconclusive | supports the premise of EXP-003 | research record, reported in `blowup-claims-audit` |
| Steered growth, hold and handoff cycle in the PDE: steering gain to 3.06e-06, landing 3.67e-04, hold decay 0.97 percent; layer 2 follows the total gradient at 0.808 against 0.392 | EXP-005 | decided in part: gates A, B, C pass; the committed parameters are refuted by the background's own instability; the 0.9 correlation gate is not met | the limit is the background's Rayleigh-Taylor instability and the reading instrument | research record, reported in `blowup-claims-audit` |
| Localization against the damping law: cost 3.6 alpha/(ell lambda), slope -0.9863 | EXP-007 | confirmed; negligible at the construction's separations | localization cannot set a hypodissipative threshold | `blowup-claims-audit` |
| Growth-law ceiling: critical exponent gamma/(2p) for the pendulum and the stretching law | EXP-008 | confirmed (pendulum to 1.1e-07, stretching to 1.8e-09, factor two exact; finite-horizon factor corrected 2026-11-14) | the class ceiling for both growth laws | `blowup-claims-audit`, Theorem 3.1 |
| Design bounds from the full force budgets of the smooth-forcing Boussinesq design and of the Euler design; reconstruction of (22 - 8 sqrt 7)/9 from its exponent budget | derivations NS-013, NS-016, NS-019, NS-021 (no experiment) | derived and machine checked in `nslib`; transcribed from archived sources with pages and equations | the published estimates certify far below the proved rough-force threshold | `blowup-claims-audit`, Theorems 4.1 and 4.2 |

## Manuscripts

| slug | version | version DOI | concept DOI | central question |
|---|---|---|---|---|
| `blowup-claims-audit` | v0.10 | [10.5281/zenodo.24231927](https://doi.org/10.5281/zenodo.24231927) | [10.5281/zenodo.22820520](https://doi.org/10.5281/zenodo.22820520) | how much dissipation can a multiscale layer cascade carry, and what do the published constructions certify |

Split decision: none. The paper is one coherent question; the audit of the announced certificates is its scope section.

## Focus record

- Closed: NS-F0, statement audit and Lean replay of the announced certificates (EXP-001, EXP-006); NS-F1, the reduced
  model against the Boussinesq equations and the dissipative extension (EXP-002, EXP-004, EXP-005, EXP-007); NS-F2, the
  class ceiling and the exponent content of the published designs (EXP-003, EXP-008, NS-013, NS-016, NS-017, NS-019,
  NS-021).
- Current: **NS-F3**, the audit paper at its published version with the scoping revisions (success gate met 2026-11-14:
  v0.09 scoped against arXiv:2610.08144, v0.10 with every criterion reported; 10.5281/zenodo.24231927).
- Proposed: NS-F4, reopening on a condition of `state.md` (a corrected formalization, a refutation of the forced blowup or
  a dissipative construction above the class ceiling), with the check of the NS-017 prediction against the unreleased
  Alpoge-Buckmaster hypodissipative paper first.

## Open obligations

- NS-010: re-read the Alpoge-Buckmaster hypodissipative paper the day it appears, compare its exponent with the recorded
  prediction and record the outcome either way (blocked until they post; not posted at the check of 2026-09-17).
- Seven validation criteria are reported as not met and one run as inconclusive in the paper; none is planned for repair
  while the programme is dormant.
- The many-layer steered dynamical cascade (EXP-005 follow-on) is an open build and is not planned.
- Attribution is a gate: the layer or pulse mechanism is never presented as ours.
