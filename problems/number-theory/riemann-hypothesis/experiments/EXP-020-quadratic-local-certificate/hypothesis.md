# EXP-020: second-order certified local lower bound

Declared 2026-10-03 before implementing or testing the new pruning path.
EXP-019's source-identical complete replay continues with immutable bindings.

## Uniform mathematical target

If F is twice continuously differentiable on a convex box B, x0 belongs
to B, and Hessian(F)(x)>=L for every x in B with L positive definite,
then for every x in B,

    F(x)>=F(x0)+grad(F)(x0).(x-x0)+1/2*(x-x0)^T L (x-x0)
         >=F(x0)-1/2*grad(F)(x0)^T L^(-1) grad(F)(x0).

Test this exact second-order replacement for the source's first-order
tangent pruner. Preserve every signed interval Hessian coefficient and the
Arb positive-pivot LDL proof. Reuse that LDL factorization for an Arb
triangular solve; no float eigenvalue or inverse certifies a decision.
The unconstrained minimum is a lower bound even outside the box; no
assertion about the stationary point belonging to B is needed.

## Candidate and value

Use the exact EXP-018 packet, window, pressure and weights, but declare the
stronger proposed universal local target delta=3051/500000 (0.006102),
compared with EXP-019's 15211/2500000 (0.0060844). The source's numerical
minimum 0.006102730481... motivates but does not prove this target.
At grid 4000, fresh exact cutoff and tables must cover the new target.
Every shard must verify. A success strengthens an input mathematically,
beyond merely replaying the published local target, and can raise the
distinct-strip consequence through the already proved general transfer.

## Invariant first and premises

The quadratic inequality is standard convex analysis, not claimed as a new
general optimization theorem. Prove it by integrating the Hessian along
a line segment; independently derive the LDL solve by completing squares.
Validate on exact positive-definite rational quadratics and deliberately
indefinite controls before computing any actual gap candidates. Test
agreement with direct exact inversion, precision perturbation and legacy
tangent bounds. The window input is independently certified in EXP-019;
the analytic energy theorem remains an explicit attributed dependency.

## Budgets, failures and manuscript route

Initially one worker, at most ten CPU minutes for invariant and local
smoke, and one CPU hour for the first complete-cover cost assessment.
Progress and atomic resumable checkpoints remain mandatory. Any failed
positive pivot rejects this pruning path for that box; other valid pruning
paths may continue. Any invalid enclosure, binding or terminal cell stops
certification and is retained. A budget hit is incomplete, not a refutation.

PASS requires a uniform lemma, independently validated exact solve, full
packet-bound local coverage and an exact stronger compatible transfer.
FAIL disproves the implementation or proposed target, not RH. No finite
minimization result counts as certification. Reassess a focused distinct-zero
companion manuscript only after complete coverage and prior-art review.
This is a bounded secondary target; RH-F4 remains the only active focus.
