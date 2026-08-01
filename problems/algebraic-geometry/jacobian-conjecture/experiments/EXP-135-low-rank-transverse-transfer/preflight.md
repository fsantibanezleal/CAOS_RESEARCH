# EXP-135 preflight - exact square-zero transfer controls

Status: **CONFIRMED EXACT RATIONAL-CONTROL PREFLIGHT**. The global function-
field identity remains open.

## Exact result

The EXP-124 transverse core was rebuilt and factored exactly as
`K_T = U V^T`, with `U` having seven columns. Entry-by-entry multiplication
reproduces the complete 33-by-33 transverse core.

At the four rational points on the EXP-123 graph
`(A,B) = (1,0), (1,1), (2,0), (2,1)`, the old core `H_0` is invertible. For
`L = V^T H_0^-1 U`, exact rational arithmetic gives the same stronger
profile at every control:

- `rank(L)=3`;
- `L^2=0` (nilpotency index two);
- `det(I_7+T L)=1` exactly.

The accepted preflight completed in under ten seconds. Artifact SHA-256:
`D322A3041F10289A60640CB658640180C0B506AD8F84F450BFB8AA8CD8A403EA`.

## Strategic consequence

The next exact predicate is not a determinant. Solve the seven graph-
quotient right-hand sides and test the 49 entries of
`(V^T H_0^-1 U)^2`. If they vanish in `QQ(A,B)`, the transfer determinant is
automatically one. The observed rank-three collapse may permit an additional
factorization, but it is not assumed globally. Every solve denominator
remains part of the proof ledger.

## Strict scope

Four rational controls do not prove the square-zero identity in the graph
function field. Lucky controls or rank jumps remain possible. Thus EXP-135
does not yet prove graph `T`-inertness, retain the old residual divisor as a
transverse theorem, cover a new stratum, close the five-coefficient
restriction, or affect `(72,108)`, the planar floor, or JC(2).
