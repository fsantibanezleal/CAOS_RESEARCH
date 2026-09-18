# navier-stokes: RESUME (zero-loss handoff)

Updated 2026-09-18 (manuscript v0.07, 10.5281/zenodo.22830171: Theorem 4.2, the Euler design is
pendulum-class and its force estimates certify at most 3.8e-3 ours; NS-016 and NS-019 closed). First read for any fresh session, per methodology 07. Derived
view: on conflict, the context dossiers win.

Manuscript v0.08 (10.5281/zenodo.22835133, 2026-09-18) is v0.07 with the author name printed as
Santibáñez-Leal (the manuscripts campaign; the publish tool now refuses any other spelling on page 1).
Its content equals v0.07, so the next content revision is v0.09.

## 1. State in one screen

The problem row. `navier-stokes`, area `analysis-pde`, portfolio feasibility B, opened 2026-09-11.
Previously `proposed` since the portfolio was created, and reviewed twice on 2026-09-05 with the
verdict that numerical regularity cannot replace the required existence or breakdown argument.

What we are NOT doing: the Clay Millennium problem. That verdict still stands.

What happened. On 2026-09-07 Alpoge and Buckmaster posted forced finite-time blowup for IPM, 2D
inviscid Boussinesq and 3D incompressible Euler, with Lean formalizations. On 2026-09-08 OpenAI
announced forced blowup for 3D Navier-Stokes for every positive viscosity, claiming Fefferman
alternatives (C) and (D), plus **unforced** 3D Euler blowup, with Lean certificates. Both extend the
multiscale program of Diego Cordoba and Luis Martinez-Zoroa, who hold the intellectual credit and whom
both parties credit explicitly. Neither proof is community-verified; Clay has not commented.

The opening round (2026-09-11) did research only; the execution round (2026-09-12) closed two
experiments. What we hold:

- **A statement audit.** The OpenAI Lean certificate states Fefferman (C) and (D) faithfully, checked
  clause by clause. 2,659 files, 641,332 lines, zero `sorry` outside the comparator reference stubs,
  zero added axioms, three standard axioms permitted. The strongest fact: the reference statement is
  adapted from DeepMind's Formal Conjectures, so the definitions that decide whether it is the right
  theorem were written by a third party before the claim existed. The **unforced Euler** certificate
  was audited on 2026-09-12 and is faithful too, and it inherits the SAME third-party reference (the
  2026-09-11 dossier claimed otherwise and is corrected in place).
- **An exact transcription** of the Alpoge-Buckmaster modulation system, with the growth rate settled
  by computation rather than by reading the PDF, now verified against a full nonlinear PDE simulation.
- **A derived obstruction and its calibration**: `alpha_c = 1/(4p)`, and the published hypodissipative
  threshold corresponds to `p = 11/4 + sqrt 7` exactly. CORRECTED 2026-09-14: that identity is
  tautological (it holds at every alpha along the published family). The published threshold is
  now DERIVED exactly from the construction's outer-velocity constraint (their 4.3.4), with the
  paper's own frequency ratio as the optimum; see `context/2026-09-14-threshold-reconstruction.md`.
- **The class ceiling (Theorem 3.1).** A layer cascade with `lambda = A^p` and growth rate
  `A^gamma` carries dissipation only up to `alpha <= gamma/(2p) < gamma/2`: 1/4 for the pendulum
  mechanism, 1/2 for stretching (`(-Laplacian)^alpha`; 1/2 and 1 in `|grad|^alpha`). Neither reaches
  classical viscosity. Code `code/nslib/class_ceiling.py`; confirmed numerically by EXP-008.
- **The design ceiling (Theorem 4.1 of v0.05).** Transcribed from the full force budget of the
  smooth-forcing construction: its estimates certify at most `alpha = 2.65e-4` ours at the published
  choices (175 times below the proved threshold), `2.22e-3` with every free choice released, and
  `4.48e-3` under the most favourable structural reading (10 times below). Code
  `code/nslib/ab_force_budget.py`; dossier `context/2026-09-17-force-estimates-exponent-content.md`.
  v0.04 had published `1.08e-3` (theirs) from a misread inequality; `ab_ceiling.py` keeps that record.
- **The manuscript.** `manuscripts/navier-stokes/blowup-claims-audit/`, v0.07 on Zenodo
  (version 10.5281/zenodo.22830171, concept 10.5281/zenodo.22820520). It is about the problem only;
  no process narration belongs in it.

## 2. The objects table

| object | meaning | where |
|---|---|---|
| `Theta, Omega` | signed amplitudes of the temperature and vorticity waves | dossier Section 4 |
| `zeta(t)` | wavevector direction; the physical wavevector is `lambda zeta` | same |
| `lambda` | fixed frequency parameter of one layer; increases stage to stage | same |
| `D(t), G(t)` | background velocity gradient (trace free) and temperature gradient | same |
| `A_q` | background temperature-gradient magnitude at stage `q` | evaluation dossier |
| `alpha` | dissipation order in `(-Laplacian)^alpha`; classical viscosity is `alpha = 1` | evaluation dossier |
| `tau = 1 - t` | time remaining, OpenAI self-similar core | source dossier Section 2 |
| `h` | OpenAI core anisotropy exponent, between 0 and 1/100 | same |

The inviscid modulation system, exact where the envelope is one and the profile is linear:

```
zeta_dot  = -D^T zeta
Theta_dot = -(J zeta . G) / (lambda |zeta|^2) * Omega
Omega_dot = lambda * zeta_1 * Theta
```

Frozen growth rate `sqrt(A) sin(phi)`, eigenline `Omega = (lambda r / sqrt(A)) Theta`.

**The one fact that drives everything:** the growth rate carries no `lambda`. Frequency buys gradient,
not growth, because the `lambda` in `Omega_dot` cancels the `1/lambda` in `Theta_dot`.

Dissipative extension, derived here and verified numerically:

```
Theta_dot = ... - nu (lambda |zeta|)^(2 alpha) Theta
Omega_dot = ... - nu (lambda |zeta|)^(2 alpha) Omega
```

giving eigenvalues `-nu (lambda r)^(2 alpha) +/- sqrt(A) sin(phi)` and the frequency cap
`lambda_q <= A_q^(1/(4 alpha)) nu^(-1/(2 alpha))`.

## 3. Experiment index

| id | subject | verdict |
|---|---|---|
| EXP-001 | replay the OpenAI Lean build | **CONFIRMED**, both halves: 11,424 jobs, 0 sorryAx, all four theorems (C, D, and both Euler) on standard axioms |
| EXP-002 | does the reduced model predict the Boussinesq PDE? | **CONFIRMED** |
| EXP-003 | does the repaired cascade model predict the published threshold? | **CONFIRMED** |
| EXP-004 | does the multi-layer handoff survive in the PDE? | pattern **CONFIRMED** (frozen two-scale, corr 0.999 vs base 0.21); slope systematic characterized; dynamical companion inconclusive |
| EXP-005 | does the growth, steering and hold cycle work in the PDE? | **DECIDED IN PART**: A, B, C pass (gain to 3e-06, landing 3.7e-04, hold decay to 0.97 percent); committed parameters REFUTED by the background's own instability; D confirms the handoff pattern at 0.808 against a 0.392 control, below its 0.9 gate |
| EXP-006 | does the Lean KERNEL accept the certificate, not just the elaborator? | **CONFIRMED**: both halves replayed from an EMPTY environment (NavierStokes 2,972 s, Euler 1,588 s, exit 0) |
| EXP-007 | does localization break the dissipative reduction? | **CONFIRMED**: the cost is `3.6 alpha / (ell lambda)`, slope -0.9863, negligible at the construction's separations |
| EXP-008 | does the critical exponent follow `gamma/(2p)` for BOTH growth laws? | **CONFIRMED**: pendulum to 1.1e-07, stretching to 1.8e-09, factor two exact; prediction published before the run |

Every experiment reproduces from the `args` block of its own result file: `code/reproduce_all.py`.

EXP-002: peak rate to 4e-05 relative, band structure present, frequency independence to 2.7e-04 across
`lambda` in [20, 160], derived dissipative term to 2.6e-04 absolute, three negative controls all
failing at a non-degenerate angle.

EXP-003: `alpha_c = 1/(4p)` to 2.59e-06 against the horizon-corrected prediction; both repaired
omissions non-binding; 1,000,000 schedules with zero violations. Its H3 (`p = 11/4 + sqrt 7` at the
published threshold) is arithmetically true but tautological, corrected 2026-09-14 in its verdict.

## 4. In flight

Nothing running. EXP-008 closed on 2026-09-17 (CPU, seconds). EXP-006 closed on 2026-09-16: both halves replayed clean
(`E:/_Temp/exp006-fresh.sh`, logs and exit codes in `E:/_Temp/exp006/`, runner archived in
`code/exp006-fresh.sh`).

EXP-001 closed on 2026-09-13: the whole certificate BUILDS clean (11,424 jobs, 0 sorryAx). The Euler
build needed a two-part cache repair (unpack! to fix disk-storm corruption, then an incremental
convergence loop to ride out Windows read-contention, 5 passes 34->22->11->9->5->0). Logs:
`E:/_Temp/lean-build/build-pass*.log`, loop `E:/_Temp/lean-build-loop.sh`.

## 5. Next actions

1. DONE 2026-09-15 by EXP-005 part D: layer 1 grown, STEERED to rest, deposit 0.92 of the base
   gradient, layer 2 then following the total gradient at 0.808 against a 0.392 control. What is still
   open is MANY layers, where the time compression starts to matter, and the correlation gate of 0.9
   that this run did not reach.
2. DONE 2026-09-14, in corrected form: the published threshold is derived from the construction's
   own exponent budget (binding constraint: outer velocity on the inner layer, 4.3.4). Our cascade
   model lacks that constraint; adding a force-regularity budget to it is the model-side follow-up.
3. NS-016 (half done): give our cascade model a force-regularity budget of its own. Round 2 showed why this matters more
   than it looked: the published budget excludes `R = 1` outright, and our model's schedule IS
   geometric, so a rigorous version of it would have to move to `M_{n+1} = M_n^R` first.
4. NS-010: compare exponents the day the Alpoge-Buckmaster hypodissipative paper appears; the class
   ceiling predicts it cannot exceed 1/2 ours for a stretching mechanism, 1/4 for a pendulum one.
5. DONE 2026-09-18 (NS-019): the Euler design is pendulum-class and its force estimates certify at
   most 3.64e-3 ours (7.27e-3 theirs) under any retuning; `ab_euler_budget.py`,
   `context/2026-09-18-euler-force-budget.md`, manuscript v0.07 Theorem 4.2. NS-010 prediction
   sharpened: a hypodissipative NS on this architecture should stay below about 7.5e-3 (theirs).

Eight experiments are closed with verdicts. The open items above are
next-round scope, not blockers.

## 6. Where everything lives

| what | path |
|---|---|
| source dossier, theorems transcribed | `problems/analysis-pde/navier-stokes/context/2026-09-11-source-dossier.md` |
| Lean statement audit | `problems/analysis-pde/navier-stokes/context/2026-09-11-lean-statement-audit.md` |
| the evaluation and the obstruction | `problems/analysis-pde/navier-stokes/context/2026-09-11-simplified-model-and-beyond.md` |
| reference library with hashes | `problems/analysis-pde/navier-stokes/context/references.md` |
| preflight smoke test | `problems/analysis-pde/navier-stokes/code/modulation_smoke.py` |
| plan, state, backlog | `program/navier-stokes/` |
| management mirror | CAOS_MANAGE `plans/caos-research/navier-stokes/` |
| manuscript source and gate | `manuscripts/navier-stokes/blowup-claims-audit/` |
| reproduction harness | `problems/analysis-pde/navier-stokes/code/reproduce_all.py` |
| local PDF mirror, NOT in git | `E:/_Temp/ns-research/pdfs/` |
| OpenAI Lean clone, NOT in git | `E:/_Temp/lean-ns/` |

## 7. Gotchas

- **The PDF text extraction mangles radicals.** `pdftotext` floats the radical sign onto its own line,
  so `sqrt(A) sin(phi)` and `sqrt(A sin(phi))` are indistinguishable in the extracted text. They differ
  numerically by a lot (1.28 versus 2.13 at one sampled parameter). Settle any transcribed formula by
  computing it, never by reading the extraction. Same class of error as the LaTeX heredoc corruption
  already in our record.
- **A clean threshold was refuted inside the opening session.** The first draft read the recursion
  coefficient crossing as a critical exponent of 1/4. The smoke test showed the transition moves with
  `nu` and with the amplitude budget. The surviving claim is only that 1/4 is an **upper bound**, with
  no escape observed above it. Do not restore the stronger wording.
- **Both first-pass omissions turned out NOT to move the exponent** (EXP-003, and this was not the
  expected outcome). The time budget is not binding because stage times decay geometrically. Damping
  during the holds gives the SAME exponent as growth positivity, because the remaining time shrinks
  like `1/sqrt(A_q)`, exactly the rate at which the growth rate rises. Do not reintroduce either as an
  open worry.
- **The multi-layer handoff is now checked on a frozen surrogate (EXP-004).** The rate of a fine wave
  follows the TOTAL two-scale gradient (corr 0.999), not the base alone (0.21), confirming EXP-003's
  premise. Still open: the fully dynamical cascade WITH steering, so each grown layer is held frozen
  while the next grows. The naive dynamical run without steering is inconclusive by construction.
- **EXP-004 carries a ~1.36 slope systematic**, present already at one scale and shrinking toward flat
  regions: it is a measurement-geometry effect, not a handoff failure, and the absolute rate was
  pinned by EXP-002. Do not read it as the rate being 1.36x too big.
- **The bare threshold question is NOT ours.** Cordoba, Martinez-Zoroa and Zheng published it in 2024
  (ARMA 2026): blowup for every `|grad|^alpha` exponent below `(22 - 8 sqrt 7)/9`, with rough forcing.
  Our cap is consistent with it and loose by 5.40. The round-1 "calibration relation" was
  tautological (withdrawn 2026-09-14). What we hold instead is the exact reconstruction of their
  constant from their own exponent budget (`nslib/cmz_budget.py`): the outer-velocity constraint
  binds, localization is slack. Do not revive the calibration as evidence of anything. Alpoge and
  Buckmaster additionally have an unreleased hypodissipative paper, presumably the smooth-forcing
  upgrade.
- **A finite horizon cannot see a late stall.** A bisection truncated at `Q` stages overreports the
  threshold by `1 + 2 log(1/nu) / (g (Q-1))`; at `nu = 1e-10`, `Q = 400` that is 11.5 percent. The
  binding stage is `Q-1`, not `Q`, and the difference is not cosmetic.
- **Attribution is a gate.** Cordoba and Martinez-Zoroa originated the program. Never present the
  layer or pulse mechanism as ours.
- The OpenAI announcement and the Buckmaster statement disagree about the history. The source dossier
  records both without taking a position; keep it that way.


- **The cascade runs against a faster instability of its own background** (EXP-005). The background is
  Rayleigh-Taylor unstable at `sqrt(A)`; a layer inserted at angle `s` grows at `sqrt(A) sin s`. Any
  realization in a plain periodic box must keep the total time short enough that round-off-seeded
  parasites stay below the layer, or the run is destroyed by its own background rather than by the
  mechanism. The real construction is protected by localization and forcing, not by speed.
- **A demodulation window has to fit under the 2/3 dealiasing limit**, not just the wave. A wave at
  0.94 of the limit passes a naive check while its window is clipped, and the only symptom is
  systematically low rates.

- **Our cap of 1/4 is unreachable, and that is now the headline about our own model.** It comes from
  the dissipation constraint alone; the schedules that approach it need a frequency ratio the
  published force budget excludes. Do not quote 1/4 as a bound on the real problem.
- **The trade-off to quote instead is `alpha < delta/(4 Q)`**, amplitude margin against frequency
  ratio. The smooth-forcing design spends both on smoothness (`delta = 1/8`, `Q >= 200`); our cap is
  the opposite corner.
- **There is a dated prediction on the record** (NS-017, wiki page 8) about the unreleased
  Alpoge-Buckmaster hypodissipative paper. When it appears, check it before anything else, and record
  the outcome either way.

- **Every experiment reproduces from its own record** (`code/reproduce_all.py`, report
  `experiments/reproduction-2026-09-17.json`). Rerun from the record, never from a command retyped
  into prose: EXP-004's recorded run used non-default `measure2` and `settle`, and rerunning with the
  defaults looks exactly like a regression.
