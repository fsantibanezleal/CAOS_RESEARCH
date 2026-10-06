# EXP-023: a new-pressure universal certificate and distinct-strip consequence

Declared 2026-10-03 before implementation, rounding audit or interval pilot.
EXP-022 justifies this bounded new-input round: it proposed a conditional
gain about 0.00021 above EXP-020, exceeding the predeclared 0.0001 value
gate, and proved that further pressure tuning of this fixed packet cannot
exceed 0.837421287797... . RH-F4 remains the active analytic focus; this is
a bounded adjunct. EXP-020 continues with its runtime source frozen.

## New input and exact target

Keep the pinned nine-point packet SHA-256
9f113eb52fba9c3a1fd7d5f2714e925ef19d3104b8fdaa982661fa96794d0c0d,
its perturbed window, all 36 pair positions and exact weight capacities.
OVERRIDE the source pressure and lower target explicitly:

    p=1/1250, delta=52231/5000000, r=8, grid=4000, precision=128.

Prove, for every g_i>=0, p*sum g_i+sum a_ij*K(sum_(i<=k<j)g_k)^2>=delta,
where K is the normalized overlap from the pinned packet. No new lower
input follows from EXP-022's observed floating minima, or from EXP-020's
partial run at a different pressure.

At m=562, tau=1203/500 and c=1703/500 the attributed elementary block
dichotomy suffices if D=delta*(m-8)<=tau^2. The exact transfer would give

    Nd/N >= (1+3362285207/5000000000-8*p*(m-8)/m)
             /(2-delta*(m-8)/m)
          = 2340938143167/2795532013000 = 0.8373855610599298... .

Check c>=1+tau, c>=2+tau/2, 6c-7-c^2>=a, 4c-2-c^2>=2a and 2-a>0,
a=delta*(m-8)/m. This is a distinct-zero bound in the whole critical
strip, not a simple-critical proportion, short-window onset or RH claim.

## Implementation and controls

Reuse the already reviewed and tested immutable quadratic verifier,
certified LDL helper and source kernel; do not edit any of those files.
Build separately bound runner/checkpoint wrappers for the new pressure.
The kernel tables depend on window/grid/precision, not pressure or target.
Check the baseline tables' complete hashes and source binding before
copying their prefix of the exact new cutoff+8 cells. No table generation
or new numerical enclosure method is needed. Independently audit directed
pressure/target rounding over every cutoff index and exact pair capacities.
Reconstruct all coordinate exclusions, Cartesian initial boxes and the
96-way partition in a separate stdlib auditor. Require every report,
empty complete checkpoint, identity/counter invariant and binding. The
auditor must reject partial coverage. Do not reinterpret the different-
pressure result as proving the original EXP-018 local premise.

## Cost and decision gate

Run one actual shard-0 pilot with one CPU process alongside EXP-020. Pilot
planning budget: 20 minutes wall clock after prepared-table launch;
checkpoint every 60 seconds and print every 30 seconds at full node
boundaries. A budget hit preserves incomplete state, not FAIL or theorem.
If the first shard finishes, record its actual cost and domain size before
authorizing a full cover; one shard alone is not a reliable worst-case ETA.
An optional second diversity pilot must be priced before it starts.

A new full cover may use at most four additional workers while EXP-020's
24 continue, keeping total workers below 32 logical processors. Its own
cost review must be persisted before launch. Any change of priority or
stopping of EXP-020 must preserve and validate its snapshots first. CPU
interval arithmetic determines every proof decision; no GPU floating
decision can certify an enclosure. The new wrappers freeze at launch.

PASS requires the complete universal cover, independent audit and exact
mixed-multiplicity transfer with attributed analytic premises explicit.
FAIL requires an actual unresolved terminal cell or invalid bound, whose
state is retained. A finite search, partial pilot or runtime success is
inconclusive for the universal input. A completed stronger distinct-strip
theorem plus EXP-022's method-output ceiling triggers a focused companion
manuscript coherence/novelty review; no extra unrelated paper is planned.
The user research stopping condition remains unmet before those gates.
