# EXP-013: optimize the fixed mixed-Gram counting assembly

Declared 2026-10-03. Device: CPU. Exact rational arithmetic. Baseline:
public develop `0c0db89df62efb92b20744a9aa1426bca1036eae`.
This declaration is committed before any runner, canonical artifact or
numerical parameter search exists.

## Question and motivation

For the fixed local inputs of arXiv:2609.33043v1, can clipping and block
size improve the distinct-zero bound, and where does that tuning stop?
See [preflight](../../context/2026-10-03-update-and-dual-family-preflight.md),
sections 1 and 3. The entire six-page source and its trust exclusions were
read; the source theorem is not counted as a CAOS invention.

## Frozen definitions and predictions

`delta=891/200000`, `p=1/2736`, `H0=3362285207/5000000000`.
For integer `m>=7`, `a=delta(m-6)/m`, `beta=6p(m-6)/m` and
`q(m)=(1+H0-beta)/(2-a)`. Admissibility requires
`delta(m-6)<=tau^2`, `tau>=0`,
`c>=max(1+tau,2+tau/2)`, `rh=6c-7-c^2>=a` and
`rk=4c-2-c^2>=2a`.

A. Reproduce the source's bound exactly at `(m,tau,c)=(1298,12/5,17/5)`:
`q=16260119298029/19426831050000`.

B. `(1310,2411/1000,3411/1000)` satisfies all constraints and gives
`q(1310)>q(1298)`.

C. No integer `m>=1311` satisfies the constraints. An exact inequality
at `m=1311` and monotonicity, not a finite census, must prove this.
`q(m)` is strictly increasing, so `m=1310` is optimal within exactly
this fixed-input, scalar-clipping assembly.

## PASS and FAIL

PASS proves the rational parameter improvement and its cap, conditional
on the source's analytic and local inputs for the zero-count consequence.
It does not independently validate that certificate, establish a world
record, prove RH, move the 0.534 onset, or optimize other kernels or proofs.
FAIL is refuted or inconclusive as appropriate; frozen inputs stay fixed.

## Premises and invariant-first check

The matrix and counting formulas are imported from arXiv:2609.33043v1
Theorem 2 and equations (1)-(2); their variational argument will be
re-derived in the proof note. The local certificate and energy input are
attributed. EXP-009 supplies the earlier comparison only. EXP-010 is not
a premise for the global distinct count. All count definitions are explicit.
The single deciding invariant is compatibility of the clipping lower
bound with the off-line-pair residual. It permits algebraic elimination
of the real parameters without a grid search.

## Adversarial validation and budget

Use a second symbolic derivation of the boundary polynomial; independently
recompute the constants; test rejection of oversized blocks and weakened
residual constraints. Decimal output is display only. Persist exact fractions,
source/declaration hashes, and a deterministic audit. CPU budget 30 seconds
per entry point, no GPU or long-run checkpoint needed. A budget stop is
inconclusive. Disposition: research-record, parameter tuning of an attributed
theorem, no standalone manuscript trigger.
