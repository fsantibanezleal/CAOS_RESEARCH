# EXP-047 preflight - relative kernel images and Smith forms

Date: 2026-09-02. Scope: exact finite relative modules for the stable row-carrier inclusions.

## Algebraic reduction

Write a row inclusion as

```text
M_T = [A; B] : Z^C -> Z^S direct-sum Z^(T-S),
A=M_S.
```

Projection onto the first row block induces the exact sequence

```text
0 -> Z^(T-S) / B(ker_Z A) -> coker(M_T) -> coker(M_S) -> 0.
```

Indeed, a class in the kernel can be represented by `(0,d)`, and changing the lift in the source
changes `d` by `Bz` for `z in ker_Z A`. Thus the missing object after EXP-046 is not another
connected-component statistic: it is the integer matrix of `B` on a saturated lattice basis of
`ker_Z A`.

## Exact engine and trust boundary

FLINT supplies row Hermite normal form with a transformation matrix and integer Smith normal form.
For `H=U*A^T`, the zero rows of `H` and corresponding rows of unimodular `U` give a saturated
integer basis of `ker_Z A`. Multiplying those basis vectors by `B` produces the relative
presentation. The implementation pins `python-flint==0.9.0`, freezes every source hash, verifies
`A*K=0`, and recomposes the field-rank increments before reading the Smith diagonals.

Primary engine references:

- FLINT integer-matrix documentation: <https://flintlib.org/doc/fmpz_mat.html>.
- python-flint integer-matrix API: <https://python-flint.readthedocs.io/en/latest/fmpz_mat.html>.

The library's exact algorithms are part of the trust boundary. An independent audit must
reconstruct the source blocks, verify every stored relative relation, recompute modular ranks by
an unrelated sparse implementation, and recompute the compact Smith forms independently where
resource-feasible.

## Prior finite constraints

The EXP-045 ranks force the following relative cokernel dimensions if the exact sequence is
implemented correctly:

```text
58 -> 59: dim_odd = binom(p-2,2), dim_2 = dim_odd + 2
58 -> 62: dim_odd = p^2-4p-3, dim_2 = dim_odd + 2
56 -> 58: dim_2 - dim_odd = p-7
```

These identities count even invariant factors but do not distinguish `2` from `4`, `8`, and so
on. EXP-047 uses integral Smith forms to make that distinction. No result below was inspected
before the hypothesis was declared.
