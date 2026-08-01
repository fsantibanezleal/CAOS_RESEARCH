# EXP-133 verdict - bounded principal-open transverse lift selected

Status: **CONFIRMED MODULAR PREFLIGHT**. This selects the next exact worker; it
is not a graph-cover theorem.

## Result

EXP-133 reuses five accepted 125-row sections from EXP-123, EXP-124, EXP-129,
and EXP-130. At a graph point the EXP-123 section is structurally singular, so
direct normalization there is invalid. The corrected computation normalizes
each section at `C+1` and evaluates

`det(I - K_C + T K_(2,8))`

on the joint strongly connected components of the normalized `C` and `(2,8)`
operators.

At primes 1009 and 1153 and graph controls `(A,B)=(1,0),(1,1)`, the transverse
degree ledger is identical:

| section | degree in `T` | cyclic support |
|---|---:|---:|
| EXP-123 shared | 1 | 7 or 9 |
| EXP-124 graph | 0 | 0 or 7 |
| EXP-129 atlas 1 | 1 | 9 or 10 |
| EXP-129 atlas 2 | 0 | 2 or 8 |
| EXP-130 structural | 2 | 10 |

Thus two accepted sections are `T`-inert on every control, two are affine,
and the finite-base structural section is quadratic. No joint cyclic support
exceeds 10, far below the declared cutoff 45. The EXP-123/EXP-124 determinant
polynomials have unit gcd in `F_p[T]` at all four controls.

The strongest insight is methodological and geometric: the first transverse
lift is a low-degree deformation of the existing atlas after restriction to
the rational graph. New row selection is not the next move. Exact SCC block
reconstruction is.

## Predictions

1. **Confirmed on all declared controls:** every section has the same degree
   at both primes and both graph points.
2. **Confirmed more strongly:** two accepted sections are `T`-inert and two
   are affine.
3. **Confirmed more strongly:** maximum cyclic support is 10, not merely at
   most 45.
4. **Confirmed on all declared controls:** the graph-defining EXP-123 section
   and the EXP-124 cover section have unit `T` gcd.

## Refuted implementation premise

Attempt 001 required all sections to be invertible on the graph. This is
impossible for EXP-123 because its determinant defines the graph. The run
stopped at the premise gate. Normalization at `C+1`, followed by the joint
`(C,T)` pencil, removes the invalid division and retains the singular fibre.

## Adversarial scope

The degree statements are modular observations at four controls. They do not
prove that a displayed degree is global, that `T`-inertness holds identically
in characteristic zero, or that the pairwise unit gcd persists on every graph
or residual point. Lucky controls, exceptional characteristic-zero factors,
or degree jumps on the factor curves remain possible.

Therefore EXP-133 does not close the rational graph, its finite base locus,
the complete `A!=0,d=1` sector, the transverse `d=0` quotient, or the
five-coefficient restriction. It says nothing new about the 24-parameter
core, the full 51-parameter family, `(72,108)`, the planar floor, or JC(2).

## Next exact worker

1. Reconstruct the EXP-124 graph section over characteristic zero on the
   quotient `R+YS=0` and decide whether its `T` coefficient is identically
   zero. Its observed joint SCC has size at most 7.
2. If inertness is exact, retain the unchanged `F3*F6*F7` residual ledger and
   reconstruct EXP-129 atlas 1 (affine in `T`) and atlas 2 (`T`-inert) on the
   five squarefree field blocks.
3. Treat the EXP-130 base-locus section only after the graph residual: its
   observed transverse degree is two with cyclic support 10.

Accepted artifact SHA-256:
`35E18A6477312B81F0CDB18C8165539A72129C1D81B16F79AC89EFB948BEBA73`.

The accepted run completed in 10.21 seconds.
