# Attempt 001 - direct graph normalization is structurally singular

The first implementation required every persisted section to be invertible at
the same EXP-123 graph controls. The premise is false: the EXP-123 shared
section defines that graph, so its determinant must vanish there at `T=0`.
The run stopped at the declared premise gate before determinant
reconstruction.

This is not evidence against the transverse lift. It refutes only direct
normalization on the singular fibre. The corrected computation normalizes at
`C+1` and evaluates the graph pencil

`det(I - K_C + T K_(2,8))`

on the joint SCCs of the normalized `C` and `(2,8)` operators. This avoids
division by the graph-defining minor and preserves exact fibre information.
