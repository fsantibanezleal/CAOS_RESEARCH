# EXP-112 - Complete augmented dependency graph and cyclic-core gate

## Question

After removing the structural constant \(Q\)-column, does the complete
51-parameter augmented matrix admit a common acyclic flag on the exact pinned
chart, or at least decompose into smaller strongly connected blocks?

## Motivation

EXP-111 proves that generic rank is already understood and that the unresolved
object is the common zero locus of augmented \(125\)-minors. EXP-099 tested a
historical pinned minor against only 26 directions and refuted a common strict
flag. It did not compute the exact strongly connected decomposition for all 51
directions.

The complete row union also contains 13 equations absent at the pinned forced
point. Their coefficient rows vanish at \(\varepsilon=0\), so they cannot enter
an invertible pinned minor. They remain available for later exceptional-stratum
charts. The immediate invariant-first question is therefore the exact graph of
the full 51-direction perturbation on the strongest existing pinned chart.

## Premise dependencies

- [MV] EXP-111 supplies the complete 302-row union, the structural constant
  column, and the exact generic-rank correction.
- [MV] EXP-059 supplies an exact nonzero augmented pinned minor.
- [MV] EXP-099 supplies the common-flag method and refutes acyclicity for its
  historical 26-direction subset.
- [D] If every normalized direction is strictly triangular in one common
  ordering, the pinned determinant is constant and nonzero for all parameters.
- [D] More generally, strongly connected components of the exact union graph
  give a simultaneous block-triangular decomposition. The selected determinant
  factors through its diagonal cyclic blocks.

## Predictions

1. [MV] The effective augmented coefficient system has 302 rows and 125
   columns: 124 nonconstant \(Q\)-columns plus the target.
2. [MV] None of the 13 recovered rows can enter an invertible pinned minor
   because its constant coefficient row is zero.
3. [MV] The exact pinned minor reconstructs and is invertible.
4. [MV] The full 51-direction graph is cyclic, reproducing EXP-099's negative
   common-flag control.
5. [C] The largest exact strongly connected block is smaller than 125, so the
   determinant problem compresses to a proper cyclic core.

## Method

- Import the canonical EXP-071 polygon and bracket construction.
- Build constant and direction coefficient matrices on the complete 302-row
  union.
- Remove the constant \(Q\)-column and append the target column.
- Select the deterministic exact pinned row basis by rational row reduction.
- Normalize every one of the 51 direction matrices by the exact pinned inverse.
- Construct the union dependency graph, compute its strongly connected
  components, condensation order, self-loops, and the directions supporting
  each cyclic block.
- Persist the exact zero pattern, selected rows, component sizes, and hashes.

## One-sidedness

- If the graph is acyclic, PASS proves the selected augmented determinant is
  the exact nonzero pinned constant for all 51 parameters and closes this
  reduced family.
- If the graph is cyclic but splits into smaller components, PASS proves an
  exact block factorization of this selected determinant and restricts further
  chart algebra to the cyclic diagonal blocks. It does not close their common
  zero loci.
- If the graph is one 125-vertex strongly connected component, FAIL refutes
  compression on this pinned basis only. It does not rule out another row
  basis, multiple charts, or use of the recovered rows after specialization.

## Adversarial validation

- Exact rational arithmetic determines every graph edge.
- The historical 26-direction subset is evaluated as a regression control.
- Direct determinant evaluations at three mixed integer points test the graph
  reading but are not used as proof.
- The 13 recovered rows are checked to be zero at the pinned point and nonzero
  in at least one direction matrix.

## Invariant-first note

Strong connectivity is the distinguishing invariant. It decides whether the
selected determinant is constant, factorizable into smaller parameter cores,
or irreducible by this graph method before any symbolic determinant expansion.

## Compute budget and kill criterion

CPU-only exact run. Expected runtime is under five minutes; stop at ten minutes.
If the exact inverse or normalization exceeds the budget, persist timing and
declare the experiment inconclusive. Do not fall back to a modular graph for a
mathematical claim.

Declared 2026-07-29 before implementation or run.
