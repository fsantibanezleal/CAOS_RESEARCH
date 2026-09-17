# navier-stokes: state (heartbeat)

| Date | From | To | Evidence |
|---|---|---|---|
| 2026-09-11 | proposed | scoped | Scoping decided by the two 2026-09-05 portfolio reviews plus the deep-research pass of 2026-09-11; primary sources read and hashed |
| 2026-09-11 | scoped | opened | Context dossiers persisted at `3f8d76d`; `plan.md`, `state.md`, `backlog.md`, `RESUME.md` written; strategy chosen and scope limits declared |
| 2026-09-12 | opened | exploring | Plan validated by Felipe; Phase 0 gate closed; EXP-002 and EXP-003 both CONFIRMED with controls; wiki authored |

- **State:** exploring (since 2026-09-12; heartbeat 2026-09-14). Plan validated by Felipe on
  2026-09-12 with the instruction to execute all of it. EXP-001 to EXP-004 closed with verdicts;
  round 2 derived the published threshold and opened EXP-005 (steered cascade).
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
(Corrected 2026-09-14: tautological along the published family; see the 2026-09-14 section.)

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
`Quot.sound`. On 2026-09-13 the FULL build completed too (11,424 jobs, zero `sorryAx`, zero errors),
adding both unforced-Euler theorems (`euler_breakdown_R3`, `exists_compact_smooth_euler_singularity`)
on the same three axioms. So the ENTIRE certificate type-checks with no gaps. The Euler half needed a
two-part cache repair: `unpack!` to overwrite oleans the external disk-deletion storm had corrupted,
then an incremental convergence loop (5 passes, read errors 34 to 22 to 11 to 9 to 5 to 0) to ride out
Windows read-contention from heavy build parallelism. The certificate was never at fault: every
failure was a file-read error or process crash, never a mathematical one.

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

All four experiments are closed with verdicts and EXP-001 confirmed both certificate halves. The
remaining items are next-round scope:

1. The fully dynamical multi-layer test WITH steering, so each grown layer is held frozen while the
   next grows. EXP-004 confirmed the physics on a frozen surrogate; the steered dynamical cascade is
   the larger open build.
2. (Done 2026-09-14, see below.) The published threshold is derived from the construction's own
   exponent budget; the round-1 calibration is withdrawn as tautological.

## Done, 2026-09-14 (round 2, part 1): the published threshold, derived

Reading Cordoba-Martinez-Zoroa-Zheng Sections 1.2.4 and 4 in full, the threshold
`(22 - 8 sqrt 7)/9` is derived exactly from the construction's own exponent bookkeeping, with no fitted
constants: with dissipation (4.3.5) and self-interaction (4.3.2) saturated, the binding constraint is
the outer velocity acting on the inner layer (4.3.4), `4s < 2 + 3 alpha - 7 alpha R - 2/R`; its optimum
over the frequency ratio is exactly the paper's `alpha R^2 = 2/7`, and `s = 0` there is exactly
`alpha_0`. Localization (4.3.3) is slack by `(sqrt(2 alpha/7) - alpha)/2`. The paper's heuristic binds on
localization instead and gives `5 - 2 sqrt 6`, so the heuristic-to-proof gap is exactly a swap of the
binding constraint. Code `nslib/cmz_budget.py` (30 tests), exact sympy guard in CI
(`tests/test_navier_stokes_threshold.py`), dossier `context/2026-09-14-threshold-reconstruction.md`.

**Correction recorded in place** in EXP-003's verdict, `cascade.py`, wiki page 4, the experiments
index, RESUME and test docstrings: the round-1 calibration `p = 11/4 + sqrt 7` is tautological, because
the construction saturates the dissipation constraint at every alpha, and its clean form is automatic
in `Q(sqrt 7)`. Both reasons previously given for it being non-empty are withdrawn.


## Done, 2026-09-15 (round 2, part 2): the steering cycle, and a kernel replay

**EXP-005, DECIDED IN PART.** The control that returns a grown layer to rest is transcribed from
Alpoge-Buckmaster Lemmas 3.7 and 3.8 (`nslib/steering.py`, kept free of torch so CI guards it) and
realized in the PDE in a co-rotating frame, where the construction's common rotation becomes a
rotating gravity direction on the torus and a low-frequency force holds the base
(`nslib/corotating.py`). Gate A passes every assertion of Lemma 3.7. On a background flattened so its
gradient is affine to fourth order, the whole growth, steering and hold cycle matches the reduced
model to 3.06e-06 in the steering gain, lands the vorticity at 3.67e-04 of its peak, holds it there
(0.36 percent drift), and reproduces the endpoint map at all three trial pulses to 4.7e-04; both
negative controls fail as required. The dissipative cycle factorizes exactly as derived: reusing the
INVISCID pulse still lands at 4.1e-04, the hold decays at `nu lambda^(2 alpha)` to 0.97 percent, and
`e^(d t)` times the viscous run reproduces the inviscid one to 0.24 percent.

**The committed-parameter run is refuted, and the reason is the finding.** The background is
Rayleigh-Taylor unstable at `sqrt(A)` while the steered layer grows at `sqrt(A) sin s`, so at the
committed insertion angle every parasite gained `1/sin s` times as many e-folds as the layer, about 72
over the schedule, and the run was destroyed by its own background. Preserved with a note, plus a new
parasite gate so this can never be reported as the layer's growth.

**The dynamical handoff EXP-004 could not do.** Layer 1 grown, steered to rest, deposit 0.92 of the
base gradient, then layer 2 grown on it: the local rate follows the TOTAL gradient at correlation
0.808 against 0.392 for the base-only control. The committed 0.9 gate is NOT met and is reported as
not met; the limit is measured (a reading window with an interior optimum, and separation 6 to 12
moving 0.755 to 0.808).

**EXP-006 CONFIRMED.** `leanchecker` ships with the toolchain since Lean v4.28.0 and the certificate
pins v4.34.0-rc2, so the kernel can re-check the certificate independently of the elaborator. Both
halves replay CLEAN from an EMPTY environment, every constant in the closure and mathlib included:
NavierStokes 2,972 s, Euler 1,588 s, exit 0, at most 6.4 GB resident. A per-module sweep was tried
first and abandoned for a measured reason (80 minutes wall for 144 seconds of CPU, I/O bound, nothing
finished), and the swap is recorded in the verdict.

**Derived from the same budget, and new:** the admissible frequency ratios form an interval whose
discriminant is exactly the polynomial whose root is `alpha_0`, so it closes to a single point at the
threshold, and that point is the paper's own `R = sqrt(2/(7 alpha))`. Its lower end exceeds 1 at every
positive alpha, with margin exactly `-alpha` at `R = 1`: a GEOMETRIC cascade, which is what our own
model uses, is inadmissible at any viscosity. Super-geometric frequency growth is forced, not
preferred.

**A gate added after a near miss.** Writing wiki page 6 through a shell heredoc turned every `\alpha`
into a BEL byte; the page still rendered. `scripts/check_content_standards.py` now flags stray control
characters in tracked text, verified against a planted corruption.

Wiki pages 6 (where the published threshold comes from) and 7 (steering, and what a holding interval
costs) authored with the results.


## Done, 2026-09-16 (round 3): the model's cap is unreachable, and a dated prediction

**NS-016, half closed.** Generalizing our cascade to any schedule `log lambda_{q+1} = R log lambda_q`
moves only C1, which becomes `R < p`; the threshold `alpha_c = 1/(4p)` stands. Importing nothing but
the admissible-ratio interval from the published force budget then caps it at `1/(4 R_-(alpha))`, and
above the published threshold no ratio is admissible at all. So EXP-003's cap of `1/4` is correct for
the model and vacuous as a bound on the real problem: the schedules that approach it are excluded
before dissipation ever binds. What is still missing is stated precisely (a localization scale, the
residual of the ansatz, a norm) rather than guessed.

**NS-017, a prediction, dated and falsifiable.** Applying our dissipative extension to the
Alpoge-Buckmaster schedule as published: their (3.8) gives a layer stopping at `lambda^(-7/8)`, so the
amplitude margin is `delta = 1/8`, and their `120 k_q <= Q_q` ties the smoothness of the force to the
frequency ratio. Our growth condition is then `alpha < delta/(4 Q_q)`, tighter by `Q_{q-1}` with their
own insertion angle. Since `Q_q = Q* + q` is unbounded, no positive alpha survives every stage: the
first stage already fails above `1.55e-04`, and at the exponent where hypodissipative blowup is
already proved with a rough force this schedule could not control even one derivative. The trade-off
is `alpha < delta/(4 Q)`, with our own cap of `1/4` sitting in the corner `delta -> 1`, `Q -> 1`.
Recorded with its falsification criterion before their hypodissipative paper appeared; NS-010 checks
it. Wiki page 8, 13 numeric tests plus a CI guard.

**Round 2 merged** to develop as PR #278 with CI green.


## Done, 2026-09-17: reproduction pass, and EXP-007

**Reproduction.** EXP-002, EXP-003 and EXP-004 rerun at the settings stored in their own result files,
after two rounds of refactoring underneath them: 13, 21 and 18 numeric leaves, zero mismatches. The
defect found was in the RECORD, not the code: the verdicts named the runner but not its settings, and
the recorded EXP-004 run used `measure2 = 0.08`, `settle = 2.0` against defaults of 0.25 and 1.0, so
rerunning from the documented command gave 0.9920 instead of 0.9995. Each verdict now carries a
command rebuilt from its own args block, and `code/reproduce_all.py` reads its command line from the
record.

**EXP-005 part D, the one unmet gate, rerun at separation 17:** correlation 0.509, down from 0.808 at
separation 12. The trend does not continue, and both measurement knobs now show an interior optimum,
which locates the limit in the instrument rather than in the handoff. D1 stays reported as not met.

**EXP-007 CONFIRMED.** Localization costs the damping law a relative error of
`3.6 alpha / (ell lambda)`: first order in the bandwidth ratio (slope -0.9863), dependent on that
ratio alone (cases splitting it differently agree to four digits), and exactly linear in alpha. At the
construction's separations, `ell_q lambda_q = lambda_{q-1}^(Q_q - 3)` with `Q_q >= 201`, the error is
negligible, so localization cannot set a hypodissipative threshold. This answers, for the dissipative
term, one of the three objects NS-016 listed as missing from our model.

**NS-010 checked 2026-09-17:** the Alpoge-Buckmaster hypodissipative paper is still not posted.
