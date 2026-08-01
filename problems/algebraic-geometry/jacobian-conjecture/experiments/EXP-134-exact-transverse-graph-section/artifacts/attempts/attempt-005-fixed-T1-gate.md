# Attempt 005 - first new fixed value reached the gate

The optimized rank/root worker loaded the persisted exact EXP-124
`T=0` determinant, divided out the unchanged singleton factors, and verified
that exact baseline identity. It then attempted the first genuinely new core
determinant at `T=1`.

After substituting the exact rational graph, the size-33 determinant over
`QQ(A,B)` did not complete within the declared 240-second single-value gate.
The checkpoint contains the exact rank-seven bound and the accepted `T=0`
baseline record, but no `T=1` determinant. Therefore the eight-root
certificate is computationally retired and proves no graph-quotient or
ambient inertness.

The retained rank-seven structure selects a lower-dimensional exact route:
factor the transverse core as `U*V^T` and use the matrix determinant lemma to
replace the 33-by-33 transverse determinant by the 7-by-7 transfer determinant
`det(I_7 + T V^T H_0^{-1} U)`.
