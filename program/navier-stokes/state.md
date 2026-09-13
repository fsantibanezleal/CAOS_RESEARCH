# navier-stokes: state (heartbeat)

| Date | From | To | Evidence |
|---|---|---|---|
| 2026-09-11 | proposed | scoped | Scoping decided by the two 2026-09-05 portfolio reviews plus the deep-research pass of 2026-09-11; primary sources read and hashed |
| 2026-09-11 | scoped | opened | Context dossiers persisted at `3f8d76d`; `plan.md`, `state.md`, `backlog.md`, `RESUME.md` written; strategy chosen and scope limits declared |
| 2026-09-12 | opened | exploring | Plan validated by Felipe; Phase 0 gate closed; EXP-002 and EXP-003 both CONFIRMED with controls; wiki authored |

- **State:** exploring (2026-09-12). Plan validated by Felipe on 2026-09-12 with the instruction to
  execute all of it. Two experiments closed with verdicts; EXP-001 (Lean replay) is running.
- **Area:** analysis-pde. This is the first problem opened in that area; it was previously an area
  name with nothing on disk.
- **Feasibility:** the portfolio row stays B. The Clay problem is not our target and the 2026-09-05
  verdict that numerical regularity cannot replace the breakdown argument still holds. The restricted
  question we opened (dissipation threshold of the layer-cascade ansatz) has a class A surface, and
  that distinction is recorded in `plan.md` rather than by inflating the row.

## Done, 2026-09-11 (opening round, research only)

Deep-research pass persisted before any plan. Primary sources downloaded, hashed and read to the depth
recorded in `problems/analysis-pde/navier-stokes/context/references.md`: the OpenAI Navier-Stokes and
Euler manuscripts, the three Alpoge-Buckmaster papers, Buckmaster's priority statement, Fefferman's
official Clay text, and eleven background references.

Findings recorded:

- OpenAI Theorem 1.1 matches Fefferman alternative (C) clause by clause, and is stronger than (C)
  requires in two respects: compactly supported force rather than merely rapidly decaying, and zero
  initial velocity.
- Their companion Euler theorem is **unforced**, which is the stronger mathematical claim and the one
  with no Clay reference statement to be audited against.
- Lean statement audit: `openai/NavierStokesAndEuler` states (C) and (D) faithfully. 2,659 files,
  641,332 lines, zero `sorry` outside the comparator reference stubs, zero added axioms, and the
  reference statement is adapted from DeepMind's Formal Conjectures, so it was authored by a third
  party before the claim existed. The Euler certificate has not been audited.
- The Alpoge-Buckmaster modulation system transcribed exactly. The growth rate is
  `sqrt(A) sin(phi)`, settled by computing the matrix rather than by reading mangled PDF glyphs, and
  it carries no dependence on the wave frequency.
- Derived here: the dissipative modulation system, the frequency cap
  `lambda <= A^(1/(4 alpha)) nu^(-1/(2 alpha))`, and an upper bound of `1/4` on the cascade
  dissipation exponent.

## Refuted inside the same session, and preserved

The first draft of the evaluation read the recursion coefficient crossing as a clean critical exponent
`alpha_c = 1/4`. The smoke test in `problems/analysis-pde/navier-stokes/code/modulation_smoke.py`
refuted that reading: over 4,000 stages, two legal amplitude budgets and four viscosities, escape below
`1/4` is not automatic (at `alpha = 0.24` it happens in 4 of 8 settings), so the transition depends on
`nu` and on how the budget is spent. The surviving statement is the weaker one, that `1/4` is an upper
bound and no escape was observed above it. Two omissions are recorded and both push the real threshold
down: the recursion has no time axis, and dissipation is not charged during the holding intervals.

The part that survives untouched, and the reason the line is worth pursuing: classical viscosity is
`alpha = 1`, four times the bound, and the failure there is not marginal in any parameter setting
tried. The naive layer cascade does not reach classical Navier-Stokes.

## Next

Phase 0 of `plan.md`: close the primary-source gap on Sections 3 to 10 of the Alpoge-Buckmaster
Boussinesq paper and on the two Cordoba-Martinez-Zoroa sources. If the dissipative analysis is already
published there, the plan is rewritten rather than executed.


## Done, 2026-09-12 (execution round)

**Phase 0 gate, NS-001 and NS-002.** A keyword census over the full extracted text of all four
September 2026 manuscripts shows the three Alpoge-Buckmaster papers are dissipation-free (zero hits
for viscosity and diffusion in the Boussinesq paper; the only dissipation mentions are in the
AI-statement section and refer to their own unreleased writeup). But the hypodissipative result is
already published by the originators: Cordoba, Martinez-Zoroa and Zheng, ARMA 250 (2026) article 38,
arXiv:2407.06776v2 from 2024, blowup for every `|grad|^alpha` exponent below `(22 - 8 sqrt 7)/9`, with
rough forcing. In our convention that is 0.0463 against our derived cap of 0.25: consistent, so the
cap is not refuted, and loose by a factor 5.40. The bare threshold question is therefore withdrawn as
a novelty target and replaced by a calibration question with a known answer.

**EXP-002 CONFIRMED.** The reduced modulation model predicts the full nonlinear 2D Boussinesq
equations: peak rate to 4e-05 relative at two angles, the predicted band structure present, frequency
independence to 2.7e-04 across an eightfold range of `lambda`, and the derived dissipative term
tracking the measured rate to 2.6e-04 absolute across `alpha` in {0.25, 0.5, 1} and `nu` in
{1e-5, 1e-4}. Three negative controls all fail as required, after the first attempt was found vacuous
at `phi = pi/2` where `zeta_1 = 1`.

**EXP-003 CONFIRMED.** `alpha_c = 1/(4p)`, measured to 2.59e-06 against the horizon-corrected
prediction, with the gap to the asymptotic form halving exactly as the horizon doubles. Both omissions
the repair was built to fix turn out NOT to move the exponent: the time budget is not binding, and
hold-interval damping gives the same exponent as growth positivity because the remaining time shrinks
at exactly the rate the growth rate rises. Inverting at the published threshold gives
`p = 11/4 + sqrt 7` exactly, to 6.2e-15. Stated as a consistency relation, not a derivation.

**NS-004.** The unforced Euler certificate audited and found faithful, with maximality pinning the
lifespan in both directions, local regularity before the endpoint, nonzero compactly supported data,
and both standard blowup criteria diverging. The 2026-09-11 audit's claim that it lacked third-party
provenance was wrong and is corrected in place.

**NS-008, NS-009.** Project `.venv` with torch 2.6.0+cu124 on the RTX 4070; wiki authored, five pages
plus a theme-aware figure.

## Errors found and fixed rather than shipped

Of the same family (a check that cannot see what it claims to test), across the whole build:

- a negative control at a degenerate angle where the corruption changed nothing;
- a log-slope fit in a region where the amplitude crosses zero;
- a stage horizon too short to observe the stall it was testing for;
- an off-by-one in the horizon bound (the binding stage is `Q-1`, not `Q`), which left 47 apparent
  violations in a million-schedule ensemble and a hundredfold worse residual;
- (EXP-004) a wave placed above the 2/3 dealiasing limit, annihilated silently and fitting garbage
  near rate 970, now a loud guard;
- (EXP-004) an injection transient read as an inflated rate, now removed by a settling interval;
- (EXP-001) a stale run-1 build log misread as the current run's output, and a naive grep for "error"
  matching module NAMES (`ErrorHarmonics`); the real checks are `sorryAx` count and the axiom lines.

## Done, 2026-09-12/13 (continuation)

**EXP-001, Navier-Stokes CONFIRMED.** `NavierStokes.ComparatorSolution`, which transitively pulls the
whole Navier-Stokes development, built cleanly three separate times: 9,371 jobs, zero `sorryAx`, and
both headline theorems (Fefferman C and D) depending on exactly `propext`, `Classical.choice`,
`Quot.sound`. The proof of the Millennium claim type-checks under the kernel on an independent machine
with no gaps. The Euler build (the mathematically stronger unforced claim) is a larger, separate build
blocked by mathlib-cache corruption from an external multi-hundred-GB disk deletion that happened
during the first attempt; the certificate is not at fault (zero mathematical errors, only olean read
failures and process crashes). A forced cache re-fetch and rebuild is in progress.

**EXP-004, the multi-layer handoff, CONFIRMED on pattern.** On a frozen two-scale vertical background
(an exact steady state, drift 1.45e-15), the local growth rate of a fine wave follows the TOTAL
two-scale gradient at correlation 0.99945 and the base stratification alone at 0.212. This is the
load-bearing premise of EXP-003: a layer responds to the total accumulated low-frequency gradient. The
absolute slope carries a ~1.36 measurement-geometry systematic (present at one scale, shrinking toward
flat regions, absolute rate already pinned by EXP-002), so the pre-committed slope sub-gate was not
met and is reported as not met. The naive dynamical companion (no steering) is inconclusive by
construction and recorded as such.

**NS-002 fully closed.** Both Cordoba-Martinez-Zoroa sources the program rests on are now read in the
primary source: the IPM paper (arXiv:2410.22920, reference [6], whose title I had mislabelled) and the
multi-layer degenerate-pendula Boussinesq paper (arXiv:2505.20988, Adv. Math. 480, reference [5]). 16
source PDFs archived.

## Next

1. Record the Euler build outcome when the repair rebuild lands.
2. The fully dynamical multi-layer test WITH steering, so each grown layer is held frozen while the
   next grows. EXP-004 confirmed the physics on a frozen surrogate; the steered dynamical cascade is
   the larger open build.
3. Derive `p = 11/4 + sqrt 7` from the construction's own localization and correction requirements,
   which would turn the consistency relation into a theorem about the model.
