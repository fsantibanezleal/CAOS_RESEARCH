# Attempt 003 - fraction-field graph determinant

Status: **STOPPED AT DECLARED SINGLE-BLOCK GATE**.

The worker proved exactly that the `(2,8)` operator restricted to the unique
33-vertex joint cyclic core has rank seven. It then substituted the rational
graph and formed the determinant over the exact univariate coefficient ring
`QQ(A,B)[T]`.

The 33-by-33 coefficient-field determinant did not complete within 240
seconds. No determinant coefficient and no graph identity were produced.
The rank-seven result is retained because it independently proves a global
degree bound `deg_T <= 7` for the core determinant; all other cyclic blocks
are singleton blocks with zero transverse diagonal.

The next route is the exact rank/root certificate: compute the ambient core
determinant separately at `T=0,...,7`. Equality at all eight values proves
constancy by the degree bound, while the first mismatch exactly refutes
ambient `T`-inertness without prejudging graph-quotient inertness.
