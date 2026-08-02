# Selector-CNF correctness argument

This note records the mathematical contract of `build_selector_rigidity_cnf(F)`. It is independent
of CaDiCaL's search and DRAT-trim's proof checking.

## Proposition

For positive odd `F`, the selector CNF is satisfiable if and only if there are a symmetric
numerical semigroup `H` with Frobenius number `F` and a gap `s` in `[1,F]` for which

```text
E_s = {n >= 0 : n,n+s are in H}
D_s = {n >= 0 : n,n+s,n+2s are in H}
D_s = E_s + E_s.
```

## Semigroup variables

`h_n` records membership for `0<=n<=F`; membership above `F` is the constant true and membership
below zero is false. Unit clauses impose `h_0` and `not h_F`. For each reflected pair the two
clauses

```text
h_n or h_(F-n)
not h_n or not h_(F-n)
```

impose exact complementary membership. Closure clauses impose
`h_a and h_b -> h_(a+b)` whenever `a+b<=F`. Consequently every model's `h` vector is exactly a
symmetric numerical semigroup with Frobenius number `F`. Conversely, every such semigroup
satisfies these clauses.

## Unique shift and guarded definitions

The selector clause contains all `q_s`, every pair has an at-most-one clause, and
`q_s -> not h_s`. Hence exactly one selected `s` exists and it is a gap.

For every `n` and every `s`, guarded equivalence clauses impose, when `q_s` is true,

```text
E_n iff h_n and h_(n+s),
D_n iff h_n and h_(n+s) and h_(n+2s).
```

Because exactly one guard is true, all `E_n` and `D_n` are fixed to the definitions for the
selected shift. Guards for unselected shifts impose nothing and therefore cannot conflict.

## Sumset direction encoded in CNF

For every `n<=2F+1` and every unordered decomposition `n=a+b`, the Tseitin variable `P_(n,a,b)`
is equivalent to `E_a and E_b`. The clause

```text
not D_n or P_(n,0,n) or P_(n,1,n-1) or ...
```

is therefore exactly `D_n -> n in E+E`. This is the nonautomatic direction.

## Reverse inclusion is a theorem, not an omitted assumption

Suppose `a,b` are in `E`. Then `a,a+s,b,b+s` are in `H`. Closure gives

```text
a+b       in H,
a+b+s     = a+(b+s) in H,
a+b+2s    = (a+s)+(b+s) in H.
```

Thus `a+b` is in `D`, proving `E+E` is a subset of `D` for every numerical semigroup and every
shift. It need not be duplicated in the CNF. The solver-independent checker nevertheless tests
both directions and rejects any extracted model with a reverse failure.

## Why the finite window is complete

All integers at least `F+1` lie in `H`, so they also lie in `E` and `D`. Let `m=min(E)`; it exists
and `m<=F+1`. For every

```text
n >= m+F+1,
```

both `m` and `n-m` belong to `E`, hence `n` belongs to `E+E`. Since
`m+F+1<=2F+2`, every `n>=2F+2` satisfies the nonautomatic inclusion automatically. Checking
`0<=n<=2F+1` is therefore sufficient for equality on all nonnegative integers.

## Equisatisfiability

- From a CNF model, the preceding clauses decode a symmetric `H`, a unique gap `s`, and exact
  finite `E,D`. The sum clauses and tail argument give `D=E+E` globally.
- From any such rigid pair `(H,s)`, assign `h` and `q` from the pair, assign `E,D` by their
  definitions, and assign each `P` by its conjunction. Every clause is then true.

This proves the proposition. It does not prove that any particular CNF is SAT or UNSAT; those
claims require the decoded-model checks or accepted DRAT certificates specified in EXP-005.
