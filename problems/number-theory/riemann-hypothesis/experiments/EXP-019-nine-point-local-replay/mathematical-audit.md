# EXP-019 mathematical and replay audit

Status: preflight complete; full cover not yet established.

## Exact input and enclosure audit

The packet is immutable EXP-018 input, SHA-256
`9f113eb52fba9c3a1fd7d5f2714e925ef19d3104b8fdaa982661fa96794d0c0d`.
The 36 ordered pairs, nonnegative rational weights and all eight exact
span capacities are checked before computation. The source revision is
`1610b97b7895ff34982260f8dcaf04a0f7b82cf7`. MIT notices and byte-identical
kernel/verifier source files are retained in `code/rh019_vendor/`.

The compound pressure operation has no generic directed-rounding proof
from a single final `nextafter`. For this packet, however, exact Fraction
comparison checks every integer index 0 through 60844 against
`n/(2500*4000)`, including all one-body indices and all unpruned prefix
sums. None exceeds the exact pressure lower bound. Weight lower/upper and
target upper comparisons are checked exactly too. No arithmetic repair
is required for these pinned constants; this conclusion is not extended
to other pressures or grids.

The exact pressure cutoff is ceil(target*grid/pressure)+1. Outside it,
pressure alone exceeds the target. One-body exclusion uses a subset of
nonnegative terms; every surviving coordinate cell is grouped into
contiguous components. The Cartesian product is partitioned by its
deterministic enumeration index modulo 96. Splitting divides a closed
cell union at a grid boundary, covering the parent with disjoint interiors.
Shared boundaries do not compromise a universal lower bound.

The kernel is the exact Fourier integral of the cosine window. The sinc
derivative series use an explicit twice-first-omitted-term bound on
|z| <= 3/4; successive absolute term ratios are below 1/2 for the omitted
indices (starting at 24). Radius conversion is rounded upward. Outside
this region division occurs away from zero. Intersection only tightens
valid enclosing intervals. K(0) must exclude zero. Lower w cells follow
from an absolute-value lower bound and downward squared conversion.
Second-derivative cells round the Arb lower endpoint downward.

The interval box bound sums individually downward products and sums.
The tangent pruner constructs a pointwise Hessian lower matrix from the
signed cell minima. Negative second-derivative coefficients use weight
upper bounds. Float LDL is a rejection heuristic only; an Arb LDL check
of exact dyadic coefficients must prove every pivot positive. Convexity
then gives a supporting tangent lower bound, with exact rational centers
and radii and Arb value/gradient enclosures. An unresolved terminal cell
raises an error, producing no proof receipt.

## Instrumentation and controls

`checkpoint_general.py` copies the licensed verifier. Changes add only
deterministic initial-cover hashing, node-boundary state callbacks and
state restoration. Mathematical pruning, split order, table construction,
precision and grid are unchanged. Frozen `verify_general.py` remains the
reference. A synthetic conservative two-gap table forces subdivision;
an interrupted run is atomically saved and resumed, and all final counters
and details agree with the frozen original. This is tooling smoke only.

Checksums, packet/source/runtime/table bindings, tree accounting, box bounds,
initial-cover digests and completion flags reject malformed resume state.
Controls include corrupt checksums, wrong bindings/shards, false completion,
invalid counters/boxes/cover, incomplete coverage, table mismatch and an
unresolved terminal cell. Checksums detect accidental corruption; they do
not constitute a cryptographic proof of an execution against an adversary
who rewrites checkpoints and their checksums. The trust base includes the
executed Python/FLINT/Arb code and reproducibility of the complete traversal.

Per-shard progress is flushed at least every 30 seconds at callback
boundaries, checkpoints every 60 seconds, and the parent reports stage
completion. Full results require all 96 shards and an independent final
coverage review. Partial checkpoints do not establish the local inequality.

## Remaining obligations

Run all shards, inspect completion independently, reconcile source tables,
review the analytic energy input separately, and reassess the exact EXP-018
distinct-strip consequence and manuscript value. This experiment is a
local interval proof replay, not an RH proof or external peer review.
