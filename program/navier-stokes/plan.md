# navier-stokes: plan

Written 2026-09-11 from the dossiers in `problems/analysis-pde/navier-stokes/context/`, not from
memory or from chat. **Status: VALIDATED by Felipe 2026-09-12, with the instruction to execute all of it. Phase 0 ran the
same day and reframed the target; see the Phase 0 gate dossier.**

## What we are not doing

We are not attacking the Clay Millennium problem. The 2026-09-05 portfolio reviews scored this row
feasibility B and concluded that numerical regularity cannot replace the required existence or
breakdown argument. That verdict stands. Global regularity of three-dimensional Navier-Stokes is out
of our reach and nothing in the September 2026 results changes that.

We are also not going to reproduce a published mechanism and present it as a finding. The simplified
model that exhibits the blowup behaviour is already in print as Subsection 1.2 and Lemma 3.1 of the
Alpoge-Buckmaster Boussinesq paper. Writing it down is a control, not a result.

## What changed on 2026-09-07 and 2026-09-08

Two independent groups posted finite-time blowup constructions, both extending the multiscale program
of Diego Cordoba and Luis Martinez-Zoroa.

- Alpoge and Buckmaster: forced blowup for IPM, 2D inviscid Boussinesq and 3D incompressible Euler,
  each with a Lean formalization. They state they also believe they have hypo-dissipative
  Navier-Stokes, unreleased.
- OpenAI: forced blowup for 3D Navier-Stokes for every positive viscosity, claimed to establish
  Fefferman alternatives (C) and (D), plus **unforced** 3D Euler blowup from smooth compactly
  supported data. Both with Lean certificates checked against a third-party reference statement.

Neither has been verified by the community. The Clay Institute has not commented.

This created a finite, checkable surface where there was none: an exact four-dimensional reduction of
a real blowup mechanism, published days ago, extensible to dissipation in three lines.

## The objective

One target, two controls around it.

**Target (reframed 2026-09-12 by the Phase 0 gate; see**
`problems/analysis-pde/navier-stokes/context/2026-09-12-phase0-gate.md`**).** The bare threshold
question is NOT ours: Cordoba, Martinez-Zoroa and Zheng published finite-time blowup for
hypodissipative Navier-Stokes for every `alpha < alpha_0 = (22 - 8 sqrt 7)/9` in 2024, in ARMA in
2026, with rough forcing. Our derived cap of `1/4` (our convention) is consistent with their
`0.0463` (same convention) and loose by a factor of 5.40.

What that hands us is better than an open question: a published exact number to calibrate against.
The target is now a single falsifiable question. **Does the reduced modulation model, with the time
budget and the hold-interval damping put back in, predict `alpha_0`?** If it does, the reduction has
demonstrated predictive power and can be aimed at what is actually open, such as the exponent cost of
smooth forcing. If it does not, the layer bookkeeping is not what sets `alpha_0`, which is a
publishable negative result inside the problem record.

**Superseded target.** Locate the dissipation threshold of the layer-cascade ansatz. The dossier derives the
dissipative modulation system and a frequency cap
$\lambda_q\lesssim A_q^{1/(4\alpha)}\nu^{-1/(2\alpha)}$, giving an upper bound of $\alpha\le 1/4$ on
the exponent for which the cascade can close. That bound has two known omissions: no time budget
$\sum_q T_q<\infty$, and no damping charged during the holding intervals. Both push the real threshold
down. The objective is to repair both and find where the transition actually sits, as a function of
$\nu$ and of how the summable amplitude budget is spent.

**Control 1.** Independent reproduction of the inviscid modulation system, validated against a direct
2D Boussinesq simulation through a full growth, steering and holding cycle. A reduced model never
checked against the equation it reduces is a picture, not an instrument. This control also tells us
where the reduction stops tracking, which is the honest boundary of every statement we make with it.

**Control 2.** Independent replay of the OpenAI Lean build, and a statement audit of the unforced
Euler certificate. The Navier-Stokes statement audit is already done and is clean; the Euler one is
missing and matters more, because it has no third-party reference statement to inherit.

## Why this is worth doing

The frequency cap explains four independent published facts that it was not derived from: every result
in the program is inviscid or Darcy; Alpoge and Buckmaster reach hypo-dissipative and stop; Tao judges
the route extendable but not yet extended; and OpenAI, reaching for the viscous case, abandoned the
cascade for a self-similar core with $\mathrm{Re}_r=O(1)$. A heuristic that accounts for the shape of
a literature it did not use is worth machine time.

## Deliberate scope limits

- The threshold is a statement about a **model system**, not about Navier-Stokes. It will be written
  that way everywhere.
- Novelty is UNVERIFIED. The unreleased Alpoge-Buckmaster hypo-dissipative paper is the obvious place
  this already exists, and Sections 3 to 10 of their Boussinesq paper have not been read. We expect to
  be second and will say so. The first backlog item is closing that reading gap.
- Credit: the mechanism belongs to Cordoba and Martinez-Zoroa. Every surface we produce says so.

## Phases

**Phase 0, preflight (no heavy compute).** Close the primary-source gap: read Sections 3 to 10 of the
Alpoge-Buckmaster Boussinesq paper and obtain the two Cordoba-Martinez-Zoroa sources the program rests
on. If the dissipative analysis is already there, the target changes and this plan is rewritten rather
than executed. Declare the compute budget and kill criterion for each experiment below.

**Phase 1, EXP-001, Lean replay.** Build `openai/NavierStokesAndEuler` and run the two Comparator
challenges. Budget and kill criterion in `backlog.md`. Runs on E: with output redirected to files, one
heavy job at a time. Outcome is a verdict on the only verification anyone can do today.

**Phase 2, EXP-002, the reduction control.** Implement the inviscid modulation system and a 2D
pseudo-spectral Boussinesq solver on the GPU. Positive control: the reduced system must predict the
PDE through a growth, steering and holding cycle. Negative control: a deliberately corrupted
modulation coefficient must fail the comparison. Deliverable is the tracking error as a function of
$\lambda$ and of stage index, and the point where the reduction breaks.

**Phase 3, EXP-003, the threshold sweep.** Add the time budget and hold-time damping to the recursion,
then sweep $(\alpha,\nu,\lambda_q,\varphi_q,\Theta_q$ schedule$)$ as a batched GPU ensemble of $10^5$
to $10^7$ trajectories. Commit the hypothesis before the run, per methodology 02. Deliverable is the
transition surface and its dependence on $\nu$ and the budget.

**Phase 4, consolidation.** Only if Phase 3 produces a stable number: write it up as a statement about
the model system, with the Cordoba-Martinez-Zoroa attribution and the honest novelty caveat. A
manuscript is not automatic and is not promised here.

## Deployment

`none` for now. This problem has no web surface until it has a result worth publishing; the research
web app already has a problem-page pattern and this row would join it at Phase 4, not before. Stated
per the entry point's requirement to pick the deploy target deliberately.

## GPU sizing

RTX 4070 Laptop, 8 GB, compute capability 8.9, driver 560.94. Torch is not installed and will go in a
project `.venv`, never globally. The ensemble sweep is batched ODE integration and fits comfortably.
The 2D pseudo-spectral solver is the binding constraint: 8 GB sets the achievable resolution and
therefore how many cascade stages the control can resolve. That is a sizing question for Phase 2, not
a blocker.

## What would make us stop

- Phase 0 finds the dissipative analysis already published: rewrite the plan, keep the audit work.
- Phase 2's control shows the reduced system does not track the PDE: the threshold question is
  meaningless as posed and the plan is rewritten around the PDE instead.
- Phase 3 finds no stable transition: record the negative result and close the round. A null result
  here is a legitimate outcome and will be published as one in the problem's history.
