# EXP-035 hypothesis - zero-row classification and consecutive survival family

Status at declaration: **ACTIVE, NO RESULT CLAIMED**. Final status: **P1/P2 CONFIRMED; P3'S
COORDINATEWISE MECHANISM REFUTED; STRONGER CHARACTERISTIC-DEPENDENT TARGET CONFIRMED**. See
`proof.md` and `verdict.md`.

## Question

Can the EXP-034 isolated incidence coordinate be upgraded to a canonical family of primitive
kernel classes, and do the lowest new cells survive the connecting map into
`A_p=P_p/Q_p` for every `p>=4`?

## Definitions

Let `n=10p-1`, let `G_p^+=G_p minus {0}`, and retain the EXP-034 sets

```text
H_p={g in G_p:g>=6p},
B_p=[6p,24p-1] minus H_p,
R_b={g in G_p^+:b-g in H_p}.
```

For `F subset G_p^+`, `|F|=i`, write `[b,F]` for the codomain coordinate
`e_F tensor v_b` of `delta_(i+1)`.

## Falsifiable predictions

### P1. Complete zero-row classification

The row `[b,F]` is identically zero over the integers if and only if

```text
R_b subset F.                                                (1)
```

Consequently the regularity-two cokernel of `K_p` contains a canonical primitive free summand
whose rank in homological degree `i` is

```text
z_(p,i)=sum_(b in B_p, |R_b|<=i) binom(n-|R_b|,i-|R_b|),     (2)
```

and hence `beta_(i,i+2)(K_p)>=z_(p,i)` over every field. A single row violating either direction
of (1), or torsion in the declared coordinate summand, refutes P1.

### P2. The next low-cardinality block

For every integer `t` with `2<=t<=p-2`, put

```text
b_(p,t)=10p+t,
F_(p,t)=[3p,4p-2] union {t} union [t+2,p],
r_(p,t)=2p-t-1,
tau_(p,t)=4p^2+6p-t(t-1)/2.
```

The prediction is

```text
R_(b_(p,t))=F_(p,t),                                        (3)
```

so `[b_(p,t),F_(p,t)]` is a primitive integral cokernel coordinate in total offset
`tau_(p,t)`. This gives one `K_p` class in every homological degree
`p+1,...,2p-3`, in addition to the EXP-034 class at degree `p`.

### P3. Consecutive survival in `A_p` and `C_p`

The stronger prediction is that no cycle of the corresponding multigraded `D_p` source can
carry a nonzero coefficient on a lifted chain `e_(F_(p,t)) tensor X_l`, `l in F_(p,t)`.
Equivalently, exact low-complex boundary pivots kill every possible connecting coefficient. Since

```text
r_(p,t)<2p-2,
```

the row-two strand of `D_p` is absent at the target homological degree. The predicted consequence
is

```text
beta_(r,(r+2,tau))(A_p)>=1,
beta_(r,(r+2,tau))(C_p)>=1                                 (4)
```

for `(r,tau)=(r_(p,t),tau_(p,t))` and every allowed `(p,t)`. Thus

```text
beta_(i,i+2)(A_p)>=1 and beta_(i,i+2)(C_p)>=1
for every p<=i<=2p-3.                                      (5)
```

An exact source cycle that hits one declared coordinate refutes P3 for that parameter cell. It
does not refute P1 or P2.

## Premise dependencies

Every canonical run must verify:

```text
EXP-032 proof    4dc37605c012b7f6a70ec5d383897c45a34e1dd5d5e4bb32a0582b7a6d651d1c
EXP-033 proof    e27cd386ad47da7ad5282e88a095d82f2b1156f76546e934b287e911da2c7b1c
EXP-034 proof    0d0a87b0a5fd4e3bbb5570e3e664eb59fcf8d07222abd62c48bdae9d20d61b4a
EXP-034 verdict  ebbf52a0b2d85b0bb5c71ca6fb48846d17b1d91644e48e69dbc3a5e8a5f81304
```

EXP-032 owns the complete `D_p` Betti polynomial. EXP-033 owns the exact sequence, regular
reduction, and minimal cubic cone. EXP-034 owns the two-layer incidence differential and the first
surviving class. No conclusion is allowed after a premise mismatch.

## Validation routes

### Canonical route

- derive `G_p`, `H_p`, `B_p`, and every `R_b` from the frozen block formulas;
- verify (1) directly and record the complete histogram of `|R_b|` for `p=4,...,300`;
- verify (2), (3), the degree and offset formulas, and the row-two threshold;
- build only the declared multigraded low-source complexes for a smoke range, checking exact
  ranks over `GF(2)` and `GF(1000003)` and preserving the first failed pivot or cycle.

### Independent route

Reconstruct the two Artinian layers from numerical-semigroup ideal powers, without importing the
canonical block or representation functions. Rebuild the selected source complexes by literal
low multiplication over `QQ`, compare representation sets and ranks, and reject filled-gap,
deleted-variable, wrong-block, and wrong-threshold controls.

### Symbolic route

Prove (1) directly from the signed incidence formula. Prove (3) by an exhaustive interval
partition of `G_p^+`. If P3 survives the smoke gate, derive an all-parameter unit-pivot or
triangular matching for every `l in F_(p,t)`. Finite ranks alone cannot establish P3.

## What PASS and FAIL prove

- **Full PASS** proves P1, P2, and P3 with canonical, independent, and written all-parameter
  support. It establishes the consecutive nonvanishing interval (5), not either complete Betti
  strand.
- **Partial PASS** proves the zero-row direct summand and the explicit `K_p` family but finds or
  leaves unresolved a connecting-map cancellation. The precise failed cell and source cycle are
  persisted.
- **FAIL** means a certified counterexample to the two-layer premises, (1), or (3).
- Hitting the budget yields `INCONCLUSIVE_BUDGET`; it proves neither survival nor cancellation.

## Invariant-first note

The set-containment invariant `R_b subset F` decides zero-row status without matrix construction.
The cardinality threshold `|R_b|<2p-2` removes the target `D_p` row-two term but does not decide the
connecting map. Hilbert series, ordinary Betti counts, and maximal-rank heuristics cannot decide
the selected multigraded survival cells.

## Compute budget and kill criterion

- Canonical classification through `p=300`: 120 seconds.
- Small exact connecting complexes: 300 seconds total, with a smoke gate at `p=4` that must emit
  progress within seconds.
- Independent reconstruction: 240 seconds.
- Symbolic certificate: 240 seconds.
- Stop P3 at the first certified source cycle that hits a selected coordinate. Do not replace the
  target with a weaker one inside this experiment.

## Publication gate

P1 alone is a reusable structural theorem and a relevant result, but does not automatically
trigger a Zenodo version. The all-parameter consecutive survival theorem (5) materially changes
the lower-strand boundary and opens in-place manuscript v0.22. A separate manuscript remains
deferred unless the zero-row method yields a transferable theorem beyond this family or a
complete strand.
