# EXP-134 hypothesis - exact `(2,8)` lift of the EXP-124 graph section

Declared: 2026-08-01, before the verdict-bearing characteristic-zero run.

## Question

Is the EXP-124 alternative maximal minor exactly independent of the new
coefficient `T = epsilon_(2,8)` after restriction to the EXP-123 rational
graph

`G(A,B,C) = R(A^3,B) + A^2 C S(A^3,B) = 0`?

EXP-133 observed transverse degree zero at four modular graph controls, but
that observation is not a characteristic-zero identity. This experiment
tests the identity directly.

## Exact method

1. Rebuild the original 302-by-125 augmented matrix and the `(2,8)`
   direction from the bracket equations.
2. Reuse the accepted EXP-124 125-row section and exact anchor.
3. Normalize over `QQ` at that anchor and decompose the joint dependency
   graph for the `A`, `B`, `C`, and `T` directions.
4. Compute the exact determinant ratio blockwise over `QQ[A,B,C,T]`.
5. Reproduce the accepted EXP-124 determinant ratio at `T=0` exactly.
6. Divide every positive-`T` coefficient by `G` over `QQ[A,B,C]` and require
   an exactly zero remainder.

This is a quotient-ring/Fitting calculation. It avoids substituting
`C=-R/(A^2S)` and therefore introduces no denominator or missing fibre.

## Falsifiable predictions

1. The joint exact cyclic core has size at most 35.
2. The `T=0` determinant ratio equals the persisted EXP-124 ratio.
3. Every coefficient of `T^k`, `k>0`, lies in the principal ideal `(G)`.
4. At least one positive-`T` coefficient is nonzero in the ambient ring; if
   all vanish, the stronger ambient `T`-inertness will be recorded instead.

Prediction 3 is the verdict gate. Modular agreement cannot substitute for
exact polynomial division.

## Budget and stop rule

- CPU and exact rational arithmetic only.
- Target: 180 seconds; hard gate: 300 seconds.
- Persist the component ledger before determinant expansion and checkpoint
  after every exact block.
- If the largest block reaches the hard gate, retain the checkpoint and
  report `INCONCLUSIVE AT DECLARED GATE`; do not infer `T`-inertness.

## Interpretation boundary

A pass proves only that this one EXP-124 minor restricts to its old value on
the complete rational graph after adjoining `(2,8)`. Combined with the old
graph atlas it preserves a dense-open chart, but it does not cover the
`F3*F6*F7` residual, the finite base locus, the transverse `d=0` quotient, or
the complete five-coefficient restriction. It says nothing new about the
24-parameter core, the 51-parameter family, `(72,108)`, the planar degree
floor, or JC(2).
