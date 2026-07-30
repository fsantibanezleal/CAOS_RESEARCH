# EXP-116 - Verdict: quotienting \(P\) preserves the rank gap but exposes a 51-column core

Verdict: **mixed, exact quotient gate**. The kernel quotient is valid and the
inconsistency gap survives every exact control. The compact-core prediction
is refuted.

## Result

Removing the \(y^8\) column is globally valid on \(d=0\) because its
coefficient in the EXP-115 kernel
\[
P=a y+b y^5+y^8(1-xy)^8
\]
is the fixed unit \(1\). The complete quotient augmented matrix has shape
302 by 124: 123 coefficient columns and the target column.

The first proposed anchor \((a,b)=(0,0)\) is not generic. Its exact rank
profile is
\[
\operatorname{rank}M_{\mathrm{quot}}=112,\qquad
\operatorname{rank}[M_{\mathrm{quot}}\mid b]=113.
\]
Thus the origin prediction is refuted, but the inconsistency gap remains.

At the exact anchor \((a,b)=(0,1)\), the quotient profile is
\[
123/124.
\]
The same exact \(123/124\) profile is reproduced at EXP-115's three boundary
controls:
\[
(0,1),\qquad (1,0),\qquad (-9,12/5).
\]

## Exact quotient graph

Normalizing at \((0,1)\) gives strongly connected component sizes
\[
51,11,10,9,8,7,1,\ldots,1.
\]
There are six nontrivial cyclic blocks and sixteen one-dimensional loop
blocks. Twelve further singleton components are acyclic.

The largest cyclic block has size 51, refuting the predicted bound 24 and
exceeding the declared determinant gate 36. The corrected run therefore
stops before symbolic determinant computation and persists the exact graph,
row basis, rank profiles, and graph digest.

## Execution correction

The first implementation checked the size gate after entering the determinant
loop. It spent about 210 seconds computing the 51-block determinant and then
failed the gate. That determinant output was not persisted or promoted.
The implementation was corrected so the final recorded run enforces the
36-column gate before determinant computation and completes in 0.55 seconds.

Any 51-block determinant claim requires a separately declared experiment.

## What this proves

- The EXP-115 \(P\)-kernel can be quotiented globally on the complete
  \(d=0\) \(T_B\) plane.
- The quotient preserves an exact one-rank inconsistency gap at the origin
  and at representatives of all three boundary components.
- The origin is a deeper rank stratum \(112/113\), not a failure of the
  inconsistency mechanism.
- The first generic quotient chart is controlled by a 51-column cyclic block,
  not a block of size at most 24.

## What this does not prove

- Sample rank gaps do not prove the gap uniformly over the \(a,b\)-plane.
- No quotient determinant or alternative quotient chart is promoted by this
  experiment.
- The 51-block concerns only the \(d=0\) \(T_B\) restriction.
- The 24-parameter core, full \((72,108)\), degree floor, and JC(2) remain
  open.

## Adversarial validation

- The EXP-115 polynomial kernel identity was rechecked coefficientwise before
  deleting \(y^8\).
- The removed column was resolved by label, not a hard-coded semantic
  assumption; it is effective column 7 and monomial \(y^8\).
- Exact nullspace calculations give \(112/113\) at the origin and \(123/124\)
  at all three nonzero boundary controls.
- The graph is computed over \(\mathbb Q\). Its artifact records the row
  basis, direction nonzero counts, edge count, SCCs, and SHA-256 digest.

## Strategy consequence

Declare EXP-117 specifically for the 51-column quotient block, with a
five-minute determinant budget now justified by the measured exploratory
runtime. Factor its exact determinant in shifted coordinates
\[
a,\qquad s=b-1.
\]
Then:

1. test the factorization against direct exact determinants;
2. determine whether the origin's deeper rank drop appears as an explicit
   factor intersection;
3. use the smaller 11/10/9/8/7 blocks and singleton loops as independent
   factors;
4. select alternative 124-column charts only on the resulting residual.

The quotient-boundary route remains first priority.
