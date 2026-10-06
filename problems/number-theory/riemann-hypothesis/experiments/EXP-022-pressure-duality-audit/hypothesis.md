# EXP-022: pressure duality for the distinct-strip objective

Declared 2026-10-03 before pressure search or witness arithmetic. This is
a bounded adjunct to RH-F4, with EXP-020 continuing independently and all
its runtime sources frozen. The new source will only read the pinned
window and pair weights; it must not alter the in-flight certificate.

## Target and reason to investigate

The nine-point packet optimized a simple-zero objective at pressure
`p=1/2500`. Its position weights and perturbed cosine window can instead
be tested against the distinct-strip objective

    q(p,delta,m) = (1+H0-8*p*t)/(2-delta*t), t=(m-8)/m.

Here delta must be a universal lower bound for E(g)+p*S(g), not an observed
minimum. For fixed weights, delta_max(p)=inf_g(E(g)+p*S(g)) is concave,
and every actual gap configuration supplies an affine upper bound. This
is a convex-duality/ergodic-optimization perspective, with classical
mathematics and no new-method priority asserted.

Two decisions are sought. First, can this family support a substantial
distinct-strip target `q>=419/500=0.838`? Second, does a changed pressure
offer a candidate at least 0.0001 above EXP-020's proposed transfer, large
enough to justify a separately declared full certificate? A finite search
can suggest the second decision only; it cannot prove a new proportion.
An exact witness envelope may decide the first uniformly for all p>=0
and every admissible m, without an exhaustive pressure grid.

## Invariant and proof before computation

For any valid gap vector, write E>=0 and S=sum(g). Necessarily delta<=E+p*S.
If a transfer with positive denominator attains q0, then

    q0*delta*t-8*p*t >= 2*q0-1-H0 = C.

For this target C>0. Since 0<t<1, this implies

    q0*E+p*(q0*S-8) >= C

for every chosen gap witness. Thus a finite collection with
`sup_(p>=0) min_i(q0*E_i+p*(q0*S_i-8)) < C` proves impossibility for this
fixed window/weight pressure family, even before spectral admissibility
constraints are imposed. Use rigorous upper enclosures for each E_i and
an independently certified upper H0; this direction makes the barrier
conservative. The maximum of the concave piecewise-affine envelope is
determined by zero and nonnegative line intersections, provided a negative
slope bounds the high-pressure tail. Retain degenerate/equal-slope cases.

## Controls, computation and scope

Read the full pinned packet and its refined-deduction/campaign notes first.
Use one CPU process with deterministic starts and analytic floating
gradients for exploration at pressures 1/3000, 1/2500, 1/2000, 1/1600,
1/1250, 1/1000, 1/800, 1/600 and 1/400. Include the source minimizing
configuration, equal gaps, and reproducible asymmetric starts. Preserve
all local outcomes; rationalize selected nonnegative gaps at denominator
10^6, then recompute E with 192-bit Arb from the frozen kernel. No floating
quantity can close the universal barrier. Expected under two minutes,
ten-minute CPU budget; stop search at five minutes and preserve partial
progress before exact witness checks. Emit progress between pressures.

Controls: reproduce the packet's floating objective, finite-difference
check analytic gradients, compare rational witness energy to its floating
evaluation, check capacities and source hashes, and distinguish a reversed
witness inequality. Evaluate an independent envelope implementation by
exact rational intersections. Candidate block arithmetic must check both
mixed-multiplicity residuals and the attributed clipping/block condition.

PASS for a barrier requires exact witness energies, the written uniform
argument and independent rational envelope audit. PASS for a new zeta
bound requires a new universal local certificate and analytic transfer;
that computation is outside this exploratory declaration. No pressure
barrier refutes other windows, weights, signed analytic approaches or RH.
No separate manuscript/Zenodo trigger arises from a classical duality
observation or an unproved candidate. This round alone is not the user's
research stopping condition.
