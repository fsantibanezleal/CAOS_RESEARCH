# EXP-049 proof record - literal-chain obstruction and parity duals

Date: 2026-09-03. Status: **REFUTED overall**, with P3 confirmed finitely and a uniform
`58->62` dual candidate retained. CPU-only exact integer and binary arithmetic.

## Exact question and result

Let `R` be either compact relative matrix from EXP-047, and let `a_1,a_2` be the two zero-one
`alpha` or `beta` chains displayed by EXP-048. EXP-049 tests the literal lattice equations

```text
R y_j = 2 a_j.
```

All sixteen equations fail, two chains in each of two inclusions for every `p=8,...,11`.
Therefore the zero-one support formulas are valid representatives of the relative Bockstein
classes, but are not themselves integral order-two representatives. Each actual integral torsion
chain has the form

```text
b_j = a_j + 2 c_j,       R y_j = 2 b_j,
```

with a nonzero even correction `2c_j`. This distinction was not decided by EXP-048.

The primary membership test reduces `2a_j` against a transformed row Hermite basis of `R^T`.
The audit reverses the relation-column order, recomputes the canonical row HNF independently, and
again obtains nonmembership in all sixteen cases.

## Dual parity certificates

P3 passes throughout the finite range. For each inclusion, exact binary functionals
`ell_1,ell_2` satisfy

```text
ell_i R = 0,
ell_i(a_j) = delta_(i,j).
```

Low-pivot and high-pivot solvers independently produce valid certificates. Every functional from
both routes has support at most four. Thus the four named Bockstein classes are nonzero and pairwise
independent in every tested relative cokernel even though their literal zero-one lifts are not
torsion vectors.

For `58->59`, the low-pivot support sizes by `p=8,9,10,11` are

```text
(2,2), (2,2), (1,2), (1,1).
```

The alternate high-pivot sizes are `(2,2),(2,2),(4,2),(2,4)`. These bounded certificates do not
yet expose one stable row formula.

For `58->62`, both solvers have support sizes `(2,4)` at every parameter. More strongly, the
low-pivot functionals have one exact formula on all four tested values. Write
`epsilon_B(u;V;q)` for the coordinate functional of the `R2` row
`rho_B(u;V;q)`, and put

```text
V_1={3p,3p+1,4p-2},     V_2={3p,3p+2,4p-2}.
```

Then the observed duals are

```text
lambda_(p,1)
 = epsilon_B(p-1;V_1;5p-4)
 + epsilon_B(p-2;V_1;5p-5),

lambda_(p,2)
 = epsilon_B(p-1;V_1;5p-4)
 + epsilon_B(p-2;V_2;5p-4)
 + epsilon_B(p-2;V_1;5p-5)
 + epsilon_B(p-3;V_2;5p-5).
```

The independent audit reconstructs these eight support sets directly and verifies their
annihilation and identity pairing. They are exact finite classifications and all-parameter
candidate formulas, not yet a symbolic proof.

## Declared predictions

- P1 is refuted: none of the sixteen literal equations `Ry=2a` has an integer solution.
- P2 is refuted because P1 supplies no source-domain realization of the literal chains.
- P3 passes finitely: both independent dual solvers certify annihilation and identity pairing in
  all sixteen functional-chain pairs.

## Independent audit

The separate auditor passes 98 of 98 checks. It verifies source and relative hashes, recomputes
all sixteen nonmembership decisions using reversed relation order, directly checks both dual
systems against the sparse matrices, enforces the support-four bound, and reconstructs the two
displayed `58->62` dual formulas.

The primary result SHA-256 is
`567f554abaa1456133a4c0cd475d1848dad92a36dd8b9412381fe2fab9fc39b7`. Its internal artifact hash
is `4d4a92ca428a7cf59733d00342c895b9c09fde276fa8d03f0d151b872892648f`. The audit certificate has
internal hash `df2663ed0c81d4db9f24a205667a44868b152a9107177aac52ce4306978eb997` and external SHA-256
`fd74e83350c35a6e4e4f6a4778766c9b59e9c30347dc00104b428a904e0e6ca6`.

## What could make this wrong?

- The nonmembership and dual results are exact only for `p=8,...,11`. They do not prove an
  all-parameter obstruction or formula.
- The literal-chain failure does not contradict the relative `(Z/2)^2`. It proves that the chosen
  zero-one lift of each mod-two class has a free or lattice component that must be corrected.
- The `58->62` dual formulas were recognized after the run. They require a symbolic incidence
  calculation before they can be asserted for every `p`.
- Bounded duals prove a lower bound of two torsion directions. A uniform upper bound still needs a
  relative-Morse reduction, a parameter-compatible Smith complement, or an equivalent theorem.

## Consequence and next proof gate

HWB-075 remains the strongest route, but the primal target changes. The next experiment must carry
exact Bockstein provenance through quotient reduction to construct `b_j=a_j+2c_j` and `y_j` with
`Ry_j=2b_j`, then classify the corrections and source cycles semantically. In parallel, the two
displayed `58->62` dual formulas should be checked symbolically against generic relation families.

The upper-bound obligation is now explicit and separate: after two torsion classes are constructed
and detected, reduce the remaining relative complex to a free cokernel. The nonuniform `56->58`
threshold remains on the relative-Morse route.

No manuscript or Zenodo update is triggered by this finite refutation and candidate formula.
