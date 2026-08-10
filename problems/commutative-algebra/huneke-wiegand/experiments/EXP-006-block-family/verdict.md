# EXP-006 verdict - scaffold supports an infinite family

Closed: 2026-08-10. Route G is REFUTED; Route K is CONFIRMED; Route A is completed by EXP-009.

## Result

The seed's fixed residue offsets do not extend, but the broader scaffold

```text
multiplicity m=4s,
Frobenius F=13s-1,
[5s,6s-1] contained in Gamma,
I=(1,t^s) rigid
```

does support infinitely many counterexamples. EXP-006 itself establishes the finite existence
map and opens the predeclared extraction gate. EXP-009 supplies the symbolic family proof.

## Route K classification

- The `s=14` calibration reproduces the public seed exactly, with membership SHA-256
  `8bf4cd6f17f12068a5755533a6852f2c36fbe9cb704c17a778a94789745fd80b`.
- `s=16,18` are UNSAT inside the declared scaffold, with accepted proof certificates.
- Every even `s=20,22,...,40` is SAT and independently validated: eleven non-seed models.
- The campaign used 44.98 solver seconds and completed without an UNKNOWN.
- The independent audit checked 27 load-bearing queries, freshly accepted 12 UNSAT proofs,
  validated 15 SAT models, and rehashed 80 external files totaling 354,465,653 bytes.
- External manifest aggregate:
  `8c4c82415b79f0d1f27e43a60e276c8d67d54170df09cf1a9ef4099f86fb5006`.
- Independent audit aggregate:
  `e483b0f66d9b65118b77d758df051b8c9eaea83b15c828720804ad1c29d5a39e`.

## Interpretation

The negative values `s=16,18` show that the scaffold is not universally feasible. The positive
finite values alone do not prove a family. Route A therefore proceeded through explicit block
recognition: EXP-008 refuted a fixed-width interval ray and exposed the missing layer-9 coverage;
EXP-009 widened the relevant interval with the parameter and proved an infinite subfamily at
`s=6p` for every `p>=4`.

The conclusion is restricted to symmetric numerical semigroups and two-generated monomial ideals.
It neither classifies all Route K models nor settles variants of the conjecture for arbitrary
modules or one-dimensional Gorenstein domains.
