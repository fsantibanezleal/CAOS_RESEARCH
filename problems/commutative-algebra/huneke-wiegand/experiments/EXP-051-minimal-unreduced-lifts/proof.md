# EXP-051 proof record - sparse exact representatives before quotient normalization

Date: 2026-09-03. Status: **REFUTED overall**, with P1 and P2 confirmed finitely. CPU-only
exact integer and binary arithmetic.

## Exact construction

For each compact relative presentation `R`, EXP-051 enumerates the binary cycles in two
deterministic kernel bases. Every such cycle `z` has even integral boundary, so

```text
Rz=2b
```

for an integral vector `b`. Its parity is reduced modulo `im(R mod 2)` only to identify the
Bockstein quotient class; `b` itself is never changed by quotient normalization. The runner keeps
one low-complexity representative of every nonzero class and selects two independent classes.
The selected quotient span agrees with the two EXP-049 formula classes.

## Declared predictions

P1 passes finitely for both stable completions and every `p=8,...,11`. Across the primary route,
the sixteen divided boundaries have supports

```text
15,18, 19,23; 14,24, 21,31; 27,30, 34,40; 21,36, 29,50,
```

where each semicolon separates consecutive values of `p`. Every coefficient has absolute value
at most two. The independent high-pivot/reversed-order route also passes: its supports range from
11 to 37 and its coefficients again have absolute value at most two.

P2 passes finitely. The primary binary cycles have support only `1`, `2`, or `6`; in particular,
one selected class is represented by a two-column cycle for every inclusion and every parameter.
The alternate cycles have support exactly `2p-8`, still within the declared `4p` bound. Both
routes span the same intrinsic rank-two quotient at every finite case.

P3 is refuted. After sorting the primary pair by boundary support, one `58->59` boundary series is
the affine law `6p-30` and one cycle series is constantly two, but the remaining series are not
affine on the complete window. The alternating one/six-column choices and non-affine support
counts show that raw elimination indices are not the correct parameter coordinates.

## Independent audit

The separate auditor passes 409 of 409 checks. Directly from every frozen EXP-047 sparse integer
matrix, it reconstructs all 32 primary and alternate cycle boundaries, verifies evenness and
`Rz=2b`, rebuilds every stored hash and complexity statistic, independently reduces the boundary
parities modulo the binary image, proves quotient rank two and route-subspace agreement, and
recomputes all three declared verdicts.

The runner SHA-256 is
`4e0debc35c7aa286cfcc73dcbe6c6d4e1d15cfcc5e7d184db7e81e45f5e8b98a`. The result SHA-256 is
`f1acaa6b769ec04b7d87a1ac416c184ffac2f5007d18a04efb397c8013ec8b1f`, with internal artifact
hash `ff6784398e1c00931e0b6cbc20f482dfa24780774081a5f4ec6fb4a368c45364`. The audit certificate
has internal hash `38653b72caa24c642000c47a83af93af728fafc5fe9d6c30b88b6bc62523fbd0` and external SHA-256
`aa1cddf1d40ca280d9c2bb3e7eaaed2039a204727e39e883eef1ddd1f59df6b4`.

## What could make this wrong?

- Every conclusion is exact only for `p=8,...,11`; no finite support bound is an all-parameter
  theorem.
- The search minimizes within deterministic kernel bases, not over the full binary kernel.
- Cycle column numbers are elimination coordinates. Their alternating patterns cannot be promoted
  until the columns are pulled back to the original labelled source complex.
- The rank-two lower bound still needs symbolic dual identities, and the upper bound still needs a
  uniform free complement or relative-Morse matching.

## Consequence and route change

EXP-050's large corrections are quotient-section artifacts, not evidence that exact torsion
representatives are intrinsically large. The new exact representatives have binary witnesses of
support at most six in the primary route and integral boundary height at most two. This makes
semantic pullback of the selected source columns the strongest primal next step.

The proof programme now has three separate obligations: prove the bounded EXP-049 dual formulas
for a uniform lower bound; derive parameter formulas for these sparse unreduced source cycles; and
construct a free complement for the upper bound. Support-count extrapolation is demoted.

No manuscript or Zenodo update is triggered.
