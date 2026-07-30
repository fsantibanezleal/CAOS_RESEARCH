# EXP-116 - Quotient the \(d=0\) boundary kernel

## Question

After quotienting the explicit \(P\)-kernel found by EXP-115, does the
complete \(d=0\) \(T_B\) system retain the inconsistency rank gap
\[
\operatorname{rank}M=123,\qquad
\operatorname{rank}[M\mid b]=124
\]
uniformly in \(a,b\)?

## Structural input

On
\[
d=1+\varepsilon_{(1,0)}=0,
\]
EXP-115 proves the exact polynomial kernel
\[
P(a,b)=a y+b y^5+y^8(1-xy)^8
\]
inside the retained \(Q\)-space. The coefficient of \(y^8\) is the fixed
unit \(1\). Therefore the \(y^8\) column can be removed globally: the kernel
identity expresses it as a polynomial combination of the remaining
columns.

The quotient augmented matrix has 124 columns:

- 123 \(Q\)-columns after removing \(y^8\);
- one appended target column.

A nonzero 124-by-124 quotient minor proves
\(\operatorname{rank}[M\mid b]=124\). Since the quotient coefficient block
has only 123 columns, this gives the desired inconsistency immediately.

## Premise dependencies

- [MV] EXP-111 supplies the complete 302-row effective augmented matrix.
- [MV] EXP-115 proves the coefficientwise \(P\)-kernel and its fixed nonzero
  \(y^8\) coordinate.
- [D] Removing the \(y^8\) column preserves the augmented column space on
  the full \(d=0\) plane.
- [D] Any nonzero quotient augmented minor certifies inconsistency because
  the quotient coefficient block has at most rank 123.

## Predictions

1. [D] The quotient matrix has shape 302 by 124 and exact rank 124 at
   \(a=b=0\).
2. [C] Normalization at \(a=b=0\) produces a dependency graph with a largest
   strongly connected component strictly smaller than 124.
3. [C] The normalized determinant is constant, or factors through a compact
   cyclic core of size at most 24.
4. [C] If the first quotient chart vanishes, alternative complete-row charts
   reduce the residual to a finite or explicitly factored set.

## Method

1. Reconstruct the complete 302-by-125 augmented system and specialize
   \(d=0\).
2. Delete the \(y^8\) column using EXP-115's fixed kernel coordinate.
3. Select a deterministic exact 124-row basis at \(a=b=0\).
4. Normalize the two direction matrices by that basis.
5. Compute the exact union dependency graph, strongly connected components,
   and cyclic parameter support.
6. Factor the determinant into its cyclic diagonal blocks. If the largest
   block is within budget, compute its exact polynomial in \(a,b\).
7. Verify the result at five direct exact rational points.

## One-sidedness

- A constant nonzero quotient determinant closes the entire \(d=0\)
  \(T_B\) plane.
- A nonconstant factorization names the exact residual for alternative
  124-column charts; it does not close that residual.
- This quotient result concerns only \(T_B\), not the 24-parameter core or
  the full 51-parameter family.

## Adversarial validation

- Recheck the EXP-115 kernel identity before deleting the column.
- The removed column must be the \(y^8\) monomial with fixed kernel
  coefficient \(1\).
- Direct exact determinants at five points must match the block
  factorization.
- The exact rank profile \(123/124\) at EXP-115's three boundary controls
  must be reproduced.

## Compute budget and kill criterion

CPU-only, five-minute budget. Stop before a symbolic determinant of any cyclic
block larger than 36. Persist the graph and block decomposition even if the
determinant step is stopped. Do not infer uniform rank from samples.

Declared 2026-07-29 before implementation or run.
