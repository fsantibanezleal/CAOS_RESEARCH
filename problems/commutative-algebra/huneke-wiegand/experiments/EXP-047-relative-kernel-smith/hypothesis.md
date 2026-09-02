# EXP-047 hypothesis - Smith forms of the relative carrier modules

Date: 2026-09-02. CPU only. Exact integer arithmetic through `python-flint==0.9.0`.

## Question

For each row inclusion `S subset T`, let

```text
Q_p(S,T) = Z^(T-S) / B(ker_Z M_p(S)),
```

where `B` is the added-row block. EXP-047 computes `Q_p(58,59)`, `Q_p(58,62)`, and
`Q_p(56,58)` for `p=8,9,10,11`. This is the exact kernel of
`coker M_p(T) -> coker M_p(S)`.

## Predictions

### P1. Two-class stable completions

The two stable completions have exact relative modules

```text
Q_p(58,59) = Z^binom(p-2,2) direct-sum (Z/2Z)^2,
Q_p(58,62) = Z^(p^2-4p-3) direct-sum (Z/2Z)^2.
```

Equivalently, after unit factors are removed, both relative Smith forms contain exactly two
nonunit entries and both are `2`. Any factor divisible by four, additional torsion prime, or
failure of the free-rank formula refutes P1.

### P2. Relative equivalence after free stabilization

After discarding unit relations and the predicted free summands, the two completion modules have
the identical Smith presentation `diag(2,2)` at every tested parameter. This is stable module
equivalence only; it does not predict a canonical chain map between the `R0` and `R2` blocks.

### P3. Linear threshold quotient

The threshold comparison has

```text
Q_p(56,58) = Z^f_p direct-sum (Z/2Z)^(p-7),
f_p = rows(R1) - (3p-7).
```

Thus its torsion ranks are `1,2,3,4`. Together with the mask-56 ranks `0,0,0,1`, this recomposes
the mask-58 sequence `1,2,3,5`. A higher 2-power or odd torsion factor refutes P3.

## Gates and claim boundary

The `p=8` smoke must finish before the full range. Each row must record source hashes, HNF rank,
kernel nullity, annihilation checks, compact relative matrix hash, modular ranks, Smith diagonal,
and exact recomposition. Time and memory budgets are explicit. An independent auditor must not
call the runner.

A pass is a finite exact theorem about three relative cokernel modules. It does not prove the
formulas for all `p`, produce the required uniform chain equivalence, or settle the full
connecting-parity problem. A manuscript or Zenodo update remains closed unless a uniform proof or
another transferable theorem is obtained.
