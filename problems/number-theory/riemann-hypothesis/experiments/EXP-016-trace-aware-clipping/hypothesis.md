# EXP-016: retain trace-zero energy in the clipping dichotomy

Declared 2026-10-03 before implementation and computation. Baseline:
develop c0167840 (EXP-013--015). CPU, exact rational and symbolic arithmetic.

## Question and invariant

The source's block Gram matrix has diagonal one, so sum(lambda_i-1)=0.
Its clipped function is psi_tau(x)=x^2 for x<=tau and
2 tau x-tau^2 for x>tau, tau>=0. If one eigenvalue displacement s>=tau,
Jensen on the other m-1 displacements gives a previously discarded
s^2/(m-1). Can this improve the bound with the same analytic/local inputs?

## Frozen predictions

A. For m>=2, tau>0 and sum x_i=0, if max x_i>=tau then
sum psi_tau(x_i)>=tau^2 m/(m-1). Prove it uniformly and exhibit equality
in a positive-semidefinite unit-diagonal matrix for 0<tau<=m-1.
The elementary zero-sum variance/Jensen mechanism is not a new matrix
method; classical trace/variance bounds are prior art.

B. The source block dichotomy remains valid under the weaker requirement
delta(m-6)<=tau^2 m/(m-1), with delta=891/200000, pressure=1/2736,
energy gain=3362285207/5000000000. The counting formula and the
mixed-multiplicity threshold/residual constraints are unchanged.
Test the fixed rational choice m=1311,tau=2411/1000,c=3411/1000;
it should strictly exceed EXP-013's fixed original-assembly optimum.

C. No m>=1312 is admissible in the new scalar-clipping assembly.
Prove exclusion through the necessary condition
delta(m-6)(m-1)/m <= (1+sqrt(2-2a(m)))^2,
then a signed rational square test at 1312 and monotonicity.
This is a uniform cap, not a finite search.

## Controls and scope

Independent SymPy differentiation/substitution and exact equicorrelation
controls. A control without the trace-zero condition must violate the
stronger bound. Reject a changed multiplicity factor, oversized block,
source constant or reported fraction. Replay must be byte identical with
declaration, proof and code/source bindings. Budget 30 seconds per entry
point, no GPU. A budget failure is inconclusive.

The source's analytic energy and seven-point interval certificate remain
attributed; no independent full replay, Lean extension, world-record or
new short-window onset is asserted. EXP-013 stays correct for its explicitly
original dichotomy; this experiment changes that proof estimate.
Disposition: supporting research record. No standalone manuscript trigger
from a standard Jensen bound and a small source-based consequence.
