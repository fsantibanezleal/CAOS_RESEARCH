# Attempt 001 - ambient four-variable determinant

Status: **STOPPED AT DECLARED SINGLE-BLOCK GATE**.

The worker rebuilt the original 302-by-125 matrix, loaded the accepted
EXP-124 section, and computed the exact normalized joint dependency graph for
the `A`, `B`, `C`, and `(2,8)` directions. Its largest cyclic component has
size 33, confirming the first cost prediction.

Direct `domain-ge` expansion of that 33-by-33 block over
`QQ[A,B,C,T]` did not complete within the canonical 240-second single-block
gate. Only the component checkpoint was produced. No determinant coefficient,
graph divisibility, `T`-inertness, or coverage statement follows.

The route is retired because it computes the ambient four-variable
determinant before using the known graph equation. Attempt 002 will reduce to
the rational graph first, keep the excluded `A*S=0` fibres explicit, and
compute the smaller quotient-field determinant in `A,B,T`.
