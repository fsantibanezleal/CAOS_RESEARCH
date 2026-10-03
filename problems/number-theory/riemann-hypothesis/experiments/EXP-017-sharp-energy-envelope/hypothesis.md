# EXP-017: sharp retained-energy envelope and pressure transfer

Declared 2026-10-03 before runner implementation and computation, on
develop 5ba579a2. See context/2026-10-03-energy-envelope-preflight.md.

## Predictions and method

A. For m>=2, tau>0, real x_i with sum x_i=0 and E=sum x_i^2,
sum psi_tau(x_i)>=F_m(E), where psi_tau(x)=x^2 for x<=tau and
2*tau*x-tau^2 otherwise. F_m(E)=E when E<=tau^2*m/(m-1), otherwise
E/m+2*tau*sqrt((m-1)*E/m)-tau^2. Prove sharpness at every E via
one positive displacement and m-1 equal negative ones, and PSD unit
diagonal realization for E<=m*(m-1). Uniform analytic proof is essential;
a finite stress family cannot establish this prediction on its own.

B. F is increasing, concave, and 1-Lipschitz on E>=0. For p,W,D>=0,
E+p*W>=D implies sum psi_tau(x_i)+p*W>=F_m(D). Applying the pinned
source block and counting inputs replaces a=delta*(m-6)/m by
a_eff=F_m(delta*(m-6))/m, leaving beta=6*p*(1-6/m) unchanged.
The unchanged threshold and residual constraints must still be checked.

C. A feasible rational m,tau,c and rational lower certificate for F(D)
can improve EXP-016's q=69341429073721/82845897125000. Search at most
51 integers m=1300..1350, and tau in [2.410,2.413] with denominator
10^6, c=1+tau. A floating approximation may locate a candidate, but
all accepted slacks and q use rational square-root brackets. This is
a finite candidate certificate, NOT a global optimality claim.

## Preflight and one-sidedness

Dependencies: EXP-016 confirms the zero-sum trace and clipping model;
EXP-013 binds delta=891/200000, p=1/2736 and
H0=3362285207/5000000000. The source's analytic energy, smoothing,
pinching and seven-point certificate remain attributed and unreplayed
here. The candidate full envelope and pressure transfer are hypotheses.
Invariant first: zero sum controls both the maximum and total positive
energy; extremal equicorrelation realizes equality. No heavy grid needed.

PASS with the proof and independent symbolic derivation confirms the
universal envelope and exact candidate consequence within those inputs.
Finite samples alone prove neither. FAIL refutes the proposed envelope,
transfer or candidate, not RH. A failed analytic source premise invalidates
the attributed consequence, not the stand-alone vector inequality.

Adversarial routes: independent completion-of-squares scalar minorant;
PSD equality cases below, at and above clipping; tau=0/invalid dimensions
rejected; missing trace control; pressure endpoint cases; rational vectors
with multiple clipped entries; certificate corruption and byte replay.
CPU budget 60 seconds per entry point; deterministic grid/seed; checkpoint
not required for a sub-minute run. Budget hit means inconclusive. No GPU.

Manuscript decision is made after proof and prior-art comparison. A standard
variance bound and a tiny attributed constant gain stay supporting records;
no RH, simple-critical improvement, new onset, or worldwide record claim.
