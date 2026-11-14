# navier-stokes: history log

## 2026-09-11, opening round (research only)

- Problem opened. The portfolio row moved `proposed` to `scoped` to `opened` in one round, on the
  strength of the deep-research pass persisted the same day.
- First problem on disk in the `analysis-pde` area, which until now was an area name with no folder.
- Sources: the OpenAI Navier-Stokes and Euler manuscripts, the three Alpoge-Buckmaster papers,
  Buckmaster's priority statement, Fefferman's official Clay text, and eleven background references,
  all downloaded, hashed and recorded in `context/references.md`. Third-party PDFs are not
  redistributed here; the mirror is outside git.
- Lean statement audit of `openai/NavierStokesAndEuler` completed for alternatives (C) and (D):
  faithful, clause by clause, with the reference statement inherited from a third party. The unforced
  Euler certificate was NOT audited and is queued as NS-004.
- The Alpoge-Buckmaster modulation system transcribed exactly, with the growth rate settled by
  computing the matrix rather than by reading the mangled PDF extraction.
- Derived here: the dissipative extension of that system, the frequency cap, and an upper bound of
  1/4 on the cascade dissipation exponent.
- A stronger reading of that bound (a clean critical exponent) was refuted by our own smoke test
  inside the same session. The weaker surviving statement is recorded, together with the two known
  omissions that push the real threshold down. Preserved in `program/navier-stokes/state.md`.
- No experiment run. The plan is written and awaiting validation before any machine time.
- Commit `3f8d76d` carries the dossiers and the smoke test.

## 2026-09-12, EXP-002: the reduced model against the Boussinesq equations (CONFIRMED)

- Question: does the Alpoge-Buckmaster modulation system, with the dissipative extension derived in this
  problem, predict the full nonlinear 2D Boussinesq equations for one layer? Hypothesis and three pass
  criteria (rate within 2 percent where the background is flattest, band structure, frequency independence
  within 2 percent) committed in the runner docstring before the run; three corrupted models had to fail.
- Verdict CONFIRMED (`experiments/EXP-002-reduction-control/verdict.md`): peak rate 1.999828 against 2 at
  phi = pi/2 and 1.414271 against 1.414214 at phi = pi/4 (rates 4e-05 relative at the peak in the verdict
  text; the result files give 8.6e-05 and 4.1e-05); band structure present (unstable band amplified 3.32,
  stable band ends at 0.57); peak rate spread 2.7e-04 across lambda = 20 to 160; damping term within 2.6e-04
  absolute across six (alpha, nu) cases.
- The first corrupted-model control ran at phi = pi/2, where zeta_1 = 1, and could not discriminate; it was
  rerun at phi = pi/4 and all three failed as required. Validity boundary stated: scale separation at least
  20, small amplitudes, one layer, short horizon.
- Reproduction added 2026-09-17: `code/reproduce_all.py` reran the stored settings after the library
  refactors, every numeric leaf identical.

## 2026-09-12, EXP-003: the cascade model against the published threshold (CONFIRMED, headline downgraded)

- Question: does the repaired cascade model, with the time budget and the hold-interval damping restored,
  predict `alpha_c = 1/(4p)` and the published threshold? Three predictions committed in the runner docstring
  (horizon-corrected threshold within 1 percent, C2 and C4 give the same exponent, `p = 11/4 + sqrt 7`).
- Verdict CONFIRMED (`experiments/EXP-003-threshold-sweep/verdict.md`): relative error 2.59e-06 against the
  horizon-corrected prediction, the gap to `1/(4p)` halving as the horizon doubles (0.009618, 0.004803,
  0.002400 at 400, 800, 1600 stages); C3 not binding, C4 binding while C2 holds in 0 of 2,304 schedules;
  `p = 11/4 + sqrt 7` to 6.2e-15; 1,000,000 schedules (174,600 close), zero violations, 1.46 s.
- An off-by-one (Q stages against Q-1) was found and fixed: 47 apparent violations and a residual of 2.56e-04
  became zero violations and 2.59e-06.
- The headline was stated as a consistency relation; it was corrected on 2026-09-14 to tautological, since the
  construction saturates its dissipation constraint at every alpha. The published threshold is set by a
  force-regularity constraint the model lacks (`context/2026-09-14-threshold-reconstruction.md`).

## 2026-09-12, EXP-004: the layer-to-layer handoff in the nonlinear equations (pattern CONFIRMED, slope not met)

- Question: does the growth rate of a layer follow the total accumulated low-frequency gradient and not the
  base stratification? Hypothesis committed in the runner docstring: H1 correlation above 0.9 with slope
  within 15 percent of 1, and the base-only control H2 worse on both.
- Part A (dynamical, no steering) INCONCLUSIVE: correlation 0.27 against 0.22 for the control, which did not
  discriminate; the setup lacked the steering that freezes the previous layer.
- Part B (frozen two-scale background, exact steady state, drift 1.45e-15) correlation 0.99945 against 0.212
  for the base alone. The committed slope sub-gate was NOT met (1.358, all_pass false) and is reported so; the
  slope is already 1.35 at A_1 = 0 and falls to 1.29 and 1.24 as the mask tightens, so it is a measurement
  systematic of the estimator (`experiments/EXP-004-multilayer-handoff/verdict.md`).
- A wave above the 2/3 dealiasing limit is annihilated silently (the first attempt, lambda_2 = 256 at
  N = 512); the runner now refuses that configuration.

## 2026-09-15, EXP-005: the steered growth, hold and handoff cycle (DECIDED IN PART)

- Question: does the transcribed steering control of Alpoge-Buckmaster Lemmas 3.7 and 3.8, run in a
  co-rotating frame, reproduce the reduced model in the PDE, does dissipation factorize as `e^(-dt)`, and does a
  steered layer carry the next one? Hypothesis with gates A to D committed before any code ran
  (`experiments/EXP-005-steered-cycle/hypothesis.md`, commit e636748).
- Gate A passed (every assertion of Lemma 3.7; `mu* = 0.66321`). Gates B and C passed on the repaired
  configuration (k = (15, 26)), flattened background: landing 3.67e-04, steering gain 3.06e-06, hold drift
  0.36 percent, 7 of 7 gates; sine background 4 of 7. Dissipation: hold decays at `d` within 0.97 percent.
- The run at the committed parameters (k = (4, 31), sin s = 0.128) is REFUTED: amplitude grows 726-fold in the
  hold. The background is Rayleigh-Taylor unstable at `sqrt(A) = 2.0` while the layer grows at 0.256, so
  favourable modes gain about 72 e-folds; recorded as gate B5, raw output preserved.
- Gate D: pattern reproduced with the control discriminating, correlation 0.808 at best (lambda_2 = 360)
  against 0.392, but D1 (above 0.9) NOT met. A separation of 17 (lambda_2 = 512, N = 2048, 22 minutes) added
  on 2026-09-17 gave 0.509 and settled the attribution to the measurement, since window and separation both
  have an interior optimum.

## 2026-09-16, EXP-006: the Lean kernel replay of the certificate (CONFIRMED)

- Question: does the Lean kernel, and not only the elaborator, accept `openai/NavierStokesAndEuler`? Hypothesis
  and gates E1 to E4 committed 2026-09-15 (commit b3dd0a2); budget 6 h for the module replay, 4 h for the
  fresh replay.
- First strategy (replay all 2,659 modules) abandoned after 80 minutes: 144 s of CPU, 11.6 GB resident, no
  module finished, because each task loads its own import closure. Replaced by `leanchecker --fresh` on the two
  root modules, pinned toolchain v4.34.0-rc2.
- Verdict CONFIRMED (`experiments/EXP-006-kernel-replay/verdict.md`): NavierStokes closure in 2,972 s and Euler
  in 1,588 s from an empty environment, exit 0 for both. The tool's own scope is kept: it detects environment
  hacking and is not an external verifier. Nothing is established about the statements or the mathematics.

## 2026-09-17, EXP-007: localization against the damping law (CONFIRMED)

- Question: does the spatial localization of every layer break the dissipative reduction, which rests on the
  fractional Laplacian being diagonal on a plane wave? Hypotheses H1 to H4 committed before the run
  (`experiments/EXP-007-localized-dissipation/hypothesis.md`), no time stepping, N = 4096.
- Verdict CONFIRMED, all three gates: slope -0.9863 in `log(ell lambda)` (criterion -1 within 0.1); coefficient
  0.180 to 3.606, exactly linear in alpha, so the error is `3.6 alpha / (ell lambda)`; control at
  `ell lambda = 1.4` has error 1.90.
- The error depends on the bandwidth ratio alone (1.7182e-02, 1.7179e-02, 1.7179e-02 at lambda = 64, 128, 256 for
  `ell lambda = 102.4`). At the construction's separations (`Q_q >= 201`) it is `lambda_{q-1}^(3 - Q_q)`.
  Scope: the damping term only, one envelope shape; the inviscid residual of a localized ansatz is untouched.

## 2026-09-17, EXP-008: the growth-law ceiling (CONFIRMED)

- Question: does the critical exponent of the cascade follow `gamma / (2p)` for both growth laws, as the paper's
  Theorem 3.1 (published as v0.04 before the run) predicts? The pendulum case had been measured by EXP-003; the
  stretching case `gamma = 1` had not.
- Verdict CONFIRMED (`experiments/EXP-008-growth-law-ceiling/verdict.md`): relative error 1.11e-07 for the
  pendulum law and 1.84e-09 for the stretching law at p = 1.5, 2, 3, 5, against the horizon-corrected
  prediction; the ratio of the two laws at equal p is exactly 2. The experiment measures the cascade
  bookkeeping and not the partial differential equations.

## 2026-10-30 - portfolio review: external status

External status: the Clay problem is open; the OpenAI forced blowup (2026-09-08) is unrefereed [V2]. New: Bastounis, Circelli, Hansen arXiv:2610.08144 (2026-10-06): the Lean proof does not correspond to the natural-language blowup proof [V, re-checked]. Our Lean audit checked the statements, which remains consistent with a proof-correspondence gap. No source states our class ceiling [U]; the nearest quantitative value is the hypodissipative threshold (22-8*sqrt(7))/9 of arXiv:2407.06776 [V2].
Plan change (assessment): one citation and scope revision (v0.09), the bounded comparison of that threshold with the class ceiling, then dormant. New rows NS-020 and NS-021.

Source: [portfolio review](../../../../program/portfolio-review-2026-10-30.md).

## 2026-11-02 - v0.09 published; dormant

- Status section scoped against arXiv:2610.08144 (Lean proof does not follow the written proof; the written
  argument is not claimed false). Published as v0.09, 10.5281/zenodo.23890775.
- NS-021 closed by reference to Section 5 (exponent budget behind the published threshold).
- Held dormant: no open backlog item; reopening conditions in state.md.
