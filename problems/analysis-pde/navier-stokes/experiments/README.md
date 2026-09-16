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
| [EXP-005](EXP-005-steered-cycle/) | Does the growth, steering and hold cycle work in the PDE, and does a steered layer carry the next one? | **DECIDED IN PART** (A, B, C pass; the committed parameters are refuted by the background's own instability; D confirms the pattern at 0.81, below its 0.9 gate) |
| [EXP-006](EXP-006-kernel-replay/) | Does the Lean KERNEL accept the certificate, not just the elaborator? | **CONFIRMED**, both halves replayed from an empty environment |

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

The result was stated as a consistency relation. Corrected 2026-09-14: it is tautological, since the construction saturates the dissipation constraint at every alpha. The published threshold is derived exactly from a different constraint (the outer velocity acting on the inner layer); see `context/2026-09-14-threshold-reconstruction.md`.

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

## EXP-005, the steered cycle

The control the construction uses to return a grown layer to rest, transcribed from Alpoge-Buckmaster
Lemmas 3.7 and 3.8 and run against the PDE in a co-rotating frame, where the common rotation of the
background becomes a rotating gravity direction on the torus. On a background flattened so its
gradient is affine to fourth order, the cycle matches the reduced model to 3e-06 in the steering gain
and lands the vorticity amplitude at 3.7e-04 of its peak, with both negative controls failing as
required. The dissipative cycle factorizes exactly as derived: the inviscid pulse still lands, and a
holding interval decays at `nu lambda^(2 alpha)` to within one percent.

The run at the parameters committed in the hypothesis is refuted, and the reason is worth more than
the run: the background is Rayleigh-Taylor unstable at `sqrt(A)` while the steered layer grows at
`sqrt(A) sin s`, so a small insertion angle gives every parasite `1/sin s` times as many e-folds as
the layer gets. The cascade always runs against a faster instability of its own background, and what
saves the real construction is localization, not speed.

## EXP-006, the kernel replay

`leanchecker` ships with the Lean toolchain since v4.28.0, and the certificate pins v4.34.0-rc2, so
the certificate can be re-checked by the kernel alone rather than trusted from a successful build.
Both halves replay clean from an EMPTY environment: NavierStokes in 2,972 s and Euler in 1,588 s,
exit 0 for both, at most 6.4 GB resident. That closes the gap EXP-001 left open, since a build and an
axiom report both read the environment the elaborator produced. The tool's own scope statement is
kept rather than inflated: it detects environment hacking, it is not an external verifier.

## What still remains open

EXP-005 closed the dynamical two-layer handoff WITH steering, at 0.81 correlation against a control
at 0.39. What remains open is a cascade of MANY layers, where the time compression that fits
infinitely many stages into finite time starts to matter, and a model-side force-regularity budget,
which is the constraint that actually sets the published threshold (wiki page 6).
