# EXP-037 hypothesis - connecting-parity quasipolynomial

Date: 2026-08-30. CPU only. All decisive arithmetic is integral or over explicitly declared
prime fields.

## Question

For the EXP-035 family at `t=2`, let

```text
e_p=dim_GF(2) A_(p,2)-dim_GF(3) A_(p,2).
```

Does the characteristic-two excess have the period-six cubic generating function

```text
sum_(p>=4) e_p x^(p-4)
  =(1+2x+x^2+x^3)/((1-x)^2(1-x^2)(1-x^3))?                   (P1)
```

More strongly, can the full connecting presentation be reduced by integral unit matchings to a
factor-two core indexed by the lattice points counted by this series?                    `(P2)`

## Falsifiable predictions

With `n=p-4`, P1 is equivalent to

```text
e_p=floor((10n^3+63n^2+126n+89)/72).
```

The first new exact predictions are

```text
e_10=73,   e_11=104.
```

P2 predicts that, after deterministic signed unit cancellation, the factor-two unmatched cells
admit a reproducible indexing by tuples `(r,a,b,c)` with numerator weights `1,2,1,1` and
`a+2b+3c=n-r`.

## Method

1. Verify the frozen EXP-036 premise hashes and reconstruct the six stored excesses.
2. Derive the coefficients of the rational generating function independently by finite sums and
   by the closed floor formula.
3. Implement a separately encoded `GF(2)` bitset rank and reversed sparse odd-prime rank, then
   reproduce `(4,2)` and `(5,2)` before attempting `(10,2)`.
4. Build the complete `(10,2)` target, never a selected submatrix, and checkpoint every completed
   basis and field rank.
5. Attempt integral sparse unit cancellation on the complete block presentation for the feasible
   small cells. Record the residual entries and labels even if the proposed lattice recognition
   fails.
6. Run `(11,2)` only if `(10,2)` passes and remains within the declared resource budget.

## What PASS and FAIL prove

- Exact `e_10=73` and `e_11=104` extend the finite agreement and reject the previous square and
  quadratic models more sharply. They do not prove P1 for all `p`.
- Any exact mismatch at `p=10` or `p=11` refutes P1.
- P2 passes only with an explicit all-parameter signed matching, a bijection to the declared
  lattice set, and independent reconstruction. Finite residual agreement alone is not P2.
- A structural mismatch refutes the proposed recognition without weakening any exact field rank.
- A budget stop is inconclusive and is not evidence for or against P1 or P2.

## Premise dependencies

- EXP-033: exact sequence and block-rank interpretation.
- EXP-034: integral two-layer incidence differential.
- EXP-035: zero-row family and first target.
- EXP-036: complete targets through `(9,2)`, field-rank controls, and all-parameter cubic-source
  absence.

The exact premise hashes are frozen in the EXP-037 preflight. Formula P1 is a new hypothesis, not
a premise.

## Invariant-first note

The exact `GF(2)` versus `GF(3)` rank difference at `(10,2)` is the cheapest decisive invariant.
Total Betti numbers, Hilbert numerators, kernel Smith data, and interpolation cannot decide the
connecting quotient. The rational generating function matters only because it yields a new value
before computation and a concrete lattice index for a possible proof.

## Compute budget and kill criterion

- regression and formula certificate: 30 seconds;
- small-cell sparse reduction: 180 seconds per cell;
- `(10,2)`: 1,800 seconds and 24 GB private memory;
- conditional `(11,2)`: 3,600 seconds and 40 GB private memory;
- checkpoint after each stage and stop at the first boundary.

No result is inferred from an incomplete rank.

