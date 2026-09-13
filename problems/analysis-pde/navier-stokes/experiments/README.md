# navier-stokes experiments

Each experiment gets its own directory holding, per methodology 02: the hypothesis committed **before**
the run, the exact command and environment, the raw outputs, the controls (at least one positive and
one deliberately corrupted negative), and the verdict. A verdict is CONFIRMED, REFUTED, INCONCLUSIVE or
DECIDED-IN-PART, and a refuted prediction is preserved rather than edited away.

| id | question | verdict |
|---|---|---|
| [EXP-001](EXP-001-lean-replay/) | Does the OpenAI Lean certificate build? | **CONFIRMED** (both Navier-Stokes and Euler; 11,424 jobs, 0 sorryAx, standard axioms) |
| [EXP-002](EXP-002-reduction-control/) | Does the reduced modulation model predict the Boussinesq PDE? | **CONFIRMED** |
| [EXP-003](EXP-003-threshold-sweep/) | Does the repaired cascade model predict the published threshold? | **CONFIRMED** |
| [EXP-004](EXP-004-multilayer-handoff/) | Does the layer-to-layer handoff survive in the full nonlinear PDE? | pattern **CONFIRMED** (frozen), slope systematic characterized |

## EXP-001, the Lean replay

The only verification of the September 2026 claims mechanically available to a third party. Its
[hypothesis](EXP-001-lean-replay/hypothesis.md) was committed before the result and states the
asymmetry plainly: a green build is weak positive evidence, and a red build is in the first instance
evidence about our machine rather than about the artifact.

## EXP-002, the reduction control

A reduced model never checked against the equation it reduces is a picture, not an instrument. This
runs the full nonlinear 2D Boussinesq system on the GPU and asks whether the modulation system
predicts it. Peak growth rate to 4e-05 relative, band structure present, frequency independence to
2.7e-04 across an eightfold range of `lambda`, and the dissipative term derived in this problem
tracking the measured rate to 2.6e-04 absolute.

Its stated validity boundary matters as much as its result: scale separation at least 20, small
amplitudes, **a single layer**, and a short horizon. Nothing in it licenses a claim about many
interacting layers.

## EXP-003, the threshold sweep

`alpha_c = 1/(4p)`, measured over 1,000,000 schedules with zero violations, and the published
threshold `(22 - 8 sqrt 7)/9` corresponding to `p = 11/4 + sqrt 7` exactly. Both omissions the model
was repaired to fix turn out not to move the exponent, which was not the expected outcome.

The result is deliberately stated as a consistency relation rather than a derivation.

## The preflight that is not an experiment

[`../code/modulation_smoke.py`](../code/modulation_smoke.py) is the tooling smoke test methodology 12
requires before machine time. It has already done its job once, by refuting the first reading of the
threshold inside the session that produced it.

## EXP-004, the multi-layer handoff

The gap EXP-002 and EXP-003 named: does a layer respond to the TOTAL accumulated low-frequency
gradient, not just the base stratification? Tested on a frozen two-scale background (an exact steady
state, drift 1.5e-15). The local rate of a fine wave follows the total two-scale gradient at
correlation 0.99945 and the base alone at 0.212, confirming the load-bearing premise. The absolute
slope carries a measurement-geometry systematic (a factor ~1.36, present already at one scale,
shrinking toward flat regions), so the pre-committed slope sub-gate was not met and is reported as
not met. The dynamical companion run is inconclusive by construction, because it does not implement
the steering that freezes the previous layer; that is recorded honestly.

## What still remains open

A fully dynamical multi-layer confirmation WITH steering implemented, so each grown layer is held
frozen while the next grows. EXP-004 Part B establishes the essential physics on a frozen surrogate;
the dynamical cascade with steering is a larger build and the natural next step.
