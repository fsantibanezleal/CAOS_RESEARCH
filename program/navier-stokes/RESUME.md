# navier-stokes: RESUME (zero-loss handoff)

Updated 2026-09-11 (opening round, research only, no experiment run). First read for any fresh
session, per methodology 07. Derived view: on conflict, the context dossiers win.

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

Our opening round did research only, and produced three things.

- **A statement audit.** The OpenAI Lean certificate states Fefferman (C) and (D) faithfully, checked
  clause by clause. 2,659 files, 641,332 lines, zero `sorry` outside the comparator reference stubs,
  zero added axioms, three standard axioms permitted. The strongest fact: the reference statement is
  adapted from DeepMind's Formal Conjectures, so the definitions that decide whether it is the right
  theorem were written by a third party before the claim existed. The **unforced Euler** certificate
  has NOT been audited and has no third-party reference to inherit, so it needs one more.
- **An exact transcription** of the Alpoge-Buckmaster modulation system, with the growth rate settled
  by computation rather than by reading the PDF.
- **A derived obstruction**, the one candidate for something of our own.

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

None run. EXP-001 to EXP-003 are specified in `backlog.md` as NS-003, NS-006 and NS-007, each with a
declared budget and kill criterion. The only code that exists is the preflight smoke test
`problems/analysis-pde/navier-stokes/code/modulation_smoke.py`, which is not an experiment.

## 4. In flight

Nothing is running. The plan is written and is **awaiting Felipe's validation**, per the mandatory
build sequence step 3. No machine time until then.

## 5. Next actions

1. NS-001 and NS-002: close the primary-source gap. Sections 3 to 10 of the Alpoge-Buckmaster
   Boussinesq paper, and the two Cordoba-Martinez-Zoroa sources the program rests on. If the
   dissipative analysis is already published there, rewrite the plan rather than execute it.
2. NS-004: audit the unforced Euler formal statement.
3. NS-003: replay the Lean build, the only verification available today.
4. Then Phase 2 and Phase 3 of `plan.md`, in that order, one heavy job at a time.

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
- **The recursion has no time axis.** Finite-time blowup also needs the stage times to sum. Escape of
  the gradient is necessary, not sufficient. Adding the time budget is the first task of EXP-003.
- **Dissipation does not rest during holding intervals.** The construction steers the laboratory
  component to zero so the next layer grows undisturbed, but the damping term does not vanish there.
  This is the largest missing piece and it pushes the threshold down.
- **Novelty is UNVERIFIED.** Alpoge and Buckmaster have an unreleased hypo-dissipative Navier-Stokes
  paper and have had it since before 2026-09-07. Expect to be second; say so.
- **Attribution is a gate.** Cordoba and Martinez-Zoroa originated the program. Never present the
  layer or pulse mechanism as ours.
- The OpenAI announcement and the Buckmaster statement disagree about the history. The source dossier
  records both without taking a position; keep it that way.
