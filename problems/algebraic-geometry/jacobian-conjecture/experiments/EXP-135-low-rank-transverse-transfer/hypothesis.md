# EXP-135 hypothesis - rank-seven transverse transfer determinant

Declared: 2026-08-01, after EXP-134 reached its exact determinant gates.

## Question

Can the exact `(2,8)` dependence of the EXP-124 graph section be decided by
the rank-seven matrix determinant lemma rather than by expanding its
33-by-33 cyclic block?

On the rational graph let

`H(A,B) = H_0(A,B) + T K_T`,

where `K_T` has exact rank seven by EXP-134. Choose an exact rank
factorization `K_T=U V^T`. Wherever `H_0` is invertible,

`det(H)/det(H_0) = det(I_7 + T V^T H_0^{-1} U)`.

Equality in the graph function field decides the polynomial identity; every
denominator factor must still be classified before a coverage statement.

## Falsifiable predictions

1. Exact pivot factorization reconstructs `K_T=U V^T` with seven columns.
2. The seven solves `H_0 W=U` complete inside the gate when performed on the
   old EXP-124 block decomposition rather than a new generic inverse.
3. The 7-by-7 transfer determinant is exactly one in `QQ(A,B)[T]`, matching
   EXP-133's degree-zero controls. A nonconstant result refutes graph
   `T`-inertness and becomes the exact residual coefficient.
4. Every solve denominator factors through the declared graph chart
   denominators `A`, `S(A^3,B)`, and the old section divisor
   `N=F3*F6*F7`; any additional factor is split as a new exceptional fibre.

Prediction 3 is the identity gate. Prediction 4 prevents fraction-field
cancellation from hiding a boundary.

## Exact method

1. Hash-check EXP-123, EXP-124, EXP-133, and the terminal EXP-134 checkpoint.
2. Rebuild the accepted section and reproduce the unique size-33 core and
   transverse rank seven.
3. Compute a deterministic exact pivot-column factorization of `K_T` and
   verify its product entry by entry.
4. Restrict `H_0` to the rational graph. Reuse the old `T=0` component
   decomposition and solve only the seven required right-hand sides.
5. Form and factor the 7-by-7 transfer determinant over `QQ(A,B)[T]`.
6. Verify at four exact rational graph controls and two independent primes.
7. Persist all denominator factors and classify their fibres before any
   graph-cover conclusion.

## Budget and stop rule

- Smoke/rank factorization: 30 seconds.
- Seven exact solves: target 180 seconds, hard gate 300 seconds.
- Transfer determinant and denominator audit: target 60 seconds.
- Total hard gate: 420 seconds, with a checkpoint after each solve.
- If the solves gate, redirect to modular reconstruction of the 49 transfer
  entries with a proved multidegree bound; do not return to a 33-by-33
  determinant expansion.

## Interpretation boundary

Even an exact unit transfer determinant preserves only the EXP-124 section
on the rational graph. The EXP-129 transverse residual sections and EXP-130
finite-base lift remain necessary, as does the separate transverse `d=0`
quotient. No outcome here settles the complete five-coefficient restriction,
the 24-parameter core, `(72,108)`, the degree floor, or JC(2).
