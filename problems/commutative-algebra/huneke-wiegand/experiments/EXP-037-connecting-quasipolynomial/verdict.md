# EXP-037 verdict

Status: **REFUTED**.

The complete `(p,t)=(10,2)` target gives

```text
dim_GF(2) A_(10,2)=4240,
dim_GF(3) A_(10,2)=dim_GF(5) A_(10,2)=4168,
e_10=72.
```

The declared period-six candidate predicted `e_10=73`, so P1 fails at the first out-of-sample
cell. P2 also fails as stated because its proposed lattice set has cardinality 73, not 72.

The refutation is exact and independently audited: low-degree and canonical residual orders give
the same `GF(2)` ranks, and `GF(3)` agrees with `GF(5)`. The kernel cokernel has dimension 8,314
and the connecting boundary has rank 725,343 in all three fields; the characteristic dependence
is entirely in the connecting-image quotient. EXP-036 transfers the exact `A_10` values to
`C_10`.

This closes only the proposed generating function and lattice indexing. It does not prove an
infinite parity theorem, complete either lower strand, or resolve the Huneke-Wiegand conjecture.
The finite result alone does not trigger manuscript v0.24 or a Zenodo update.
