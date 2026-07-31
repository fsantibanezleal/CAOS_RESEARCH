# EXP-113 - Verdict: three directions generate the full 36-core graph, but SCC compression is exhausted

Verdict: **mixed, exact**. The proposed second SCC split is refuted, while the
small-support prediction is confirmed.

## Result

The exact run completed in 4.1 seconds.

Removing the forced direction \((1,0)\) does not split the 36-core. The other
23 active directions still make all 36 vertices strongly connected. Therefore
the forced-axis factor is not the source of the core's global coupling.

Each single \(x\)-degree group has a proper SCC decomposition, but mixed groups
reconnect the core. Deterministic deletion produces two different
deletion-minimal full-connectivity supports:
\[
T_A=\{(0,1),(0,7),(2,9)\},
\]
and, in reverse deletion order,
\[
T_B=\{(0,1),(0,5),(1,0)\}.
\]
Each triple alone makes all 36 core vertices strongly connected. Removing any
one member from the corresponding deletion-minimal support destroys that
property.

The known EXP-100 pair
\[
\{(0,1),(1,7)\}
\]
is cyclic but does not make the full core strongly connected, as required by
the positive and negative controls.

## Trace-interaction result

The undirected graph defined by nonzero exact pair traces
\[
\operatorname{tr}(N_iN_j)
\]
has component sizes
\[
4,4,4,2,1,1,1,1,1,1,1,1,1,1.
\]
Thus quadratic trace interactions are highly fragmented even though the union
dependency graph is fully connected. The full coupling is carried partly by
higher-order directed cycles.

## What this proves

- No further SCC compression exists on the pinned 36-core merely by factoring
  out the forced direction.
- Full graph complexity is already present on explicit three-parameter
  supports.
- The 24-variable determinant cannot be understood from pair traces alone.
- The two triples are rigorous minimal controls for determinant
  reconnaissance. They are selected by exact connectivity, not by blind slice
  enumeration.

## What this does not prove

- Strong connectivity does not prove that the determinant depends on every
  selected parameter. Directed-cycle contributions may cancel algebraically.
- Deletion-minimal does not mean minimum cardinality across all subsets,
  although both deterministic orders reached cardinality three.
- Results on \(T_A\) or \(T_B\) do not close the 24-parameter core.

## Adversarial validation

- Every matrix entry, trace, and graph edge was exact over \(\mathbb Q\).
- Forward and reverse deletion orders produced different full-connectivity
  triples, reducing dependence on one ordering artifact.
- The EXP-100 pair passed both its cycle-positive and
  full-connectivity-negative controls.

## How could this be wrong?

- The graph is tied to EXP-112's selected pinned basis.
- Graph connectivity can overestimate actual determinant dependence through
  cancellation. EXP-114 is required before promoting either triple as an
  algebraic model.
- Alternative augmented charts can have different cores.

## Strategy consequence

Run exact symbolic determinants on \(T_A\) and \(T_B\). If graph connectivity
survives algebraically as compact factors, use those factors to select
alternative charts. If a direction cancels entirely, replace graph support by
actual determinant support as the next invariant.
