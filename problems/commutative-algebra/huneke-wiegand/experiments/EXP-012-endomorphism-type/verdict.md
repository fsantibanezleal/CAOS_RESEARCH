# EXP-012 verdict - pseudo-Frobenius anatomy CONFIRMED

Run date: 2026-08-12. Exact integer and bitset arithmetic, CPU only.

## Result

Every prediction passes. For every integer `p>=4`, the EXP-011 endomorphism semigroup has

```text
PF(Lambda_p) = (6s+B^c) union (7s+Q^c) union (8s+C^c),
type(Lambda_p) = reduced_type(Lambda_p) = 10p.
```

There are no lower pseudo-Frobenius numbers. The associated semigroup ring therefore has maximal
reduced type. Since `2g-(F+type)=12p-1`, the semigroup is never almost symmetric and its completed
semigroup ring is never almost Gorenstein.

This strengthens EXP-011's nonsymmetry statement: the failure of the Gorenstein center condition is
not sporadic or bounded. Its Cohen-Macaulay type grows linearly and without bound across the family.

## Symbolic proof

The proof in `proof.md` is load-bearing. Every gap in the final multiplicity window is automatically
pseudo-Frobenius. Explicit level-5 or level-4 minimal-generator witnesses exclude every gap below
that window. Exact block complements then give sizes `3p`, `5p`, and `2p`.

## Computational and adversarial record

- Two exact routes agree for all 297 parameters `p=4,...,300`.
- Route A tests all gaps against the complete minimal-generator set with bitset intersections.
- Route B reconstructs the Apéry set modulo `4s` and extracts its semigroup-order maxima.
- Campaign aggregate:
  `9bed38fb1c786c3740e000dde7ea7d79a7e7c83fa584ff12fc2c4623b5d503ec`.
- A separate implementation rehashes all rows and reconstructs full semantics at
  `p=4,5,17,73,151,300`.
- Audit aggregate:
  `0315c4c22c41e0d2b8a5abb27f717a4d4a6f7356ef30ca388206d739e0de2c37`.
- `results.json` SHA-256:
  `2bf8dff459ca98780738bedc4c026967b46e249e720704657818c5c7644d29ac`.
- `audit.json` SHA-256:
  `477cf8c20e18d27f7d77d328b2efdffce3fd09aa664c3cc80b2292bee7584b53`.
- Both artifacts reproduce byte-for-byte on a second run.
- Deleting a predicted PF value and injecting the lower gap `5s-1` are rejected.

## Prediction ledger

- P1 PASS: the complete PF block formula is proved and both routes agree.
- P2 PASS: type and reduced type are exactly `10p`.
- P3 PASS: every family member has maximal reduced type.
- P4 PASS: every family member is not almost symmetric and its completion is not almost Gorenstein.
- P5 PASS: the independent reconstruction and both corruptions pass.

Verdict: **CONFIRMED**.

## Consequence and scope

EXP-012 closes another exact row of HW-P5. It quantifies the endomorphism-center obstruction for the
entire explicit family but does not classify arbitrary counterexamples, arbitrary rigid modules, or
nearby Kunz faces. Son Pham retains priority for the first public counterexample.

The result is theorem-level manuscript material, but publication is not automatic. Methodology 12
requires deliberate consolidation rather than reflexive version minting. The next strongest route is
the trace/endomorphism equality suggested by Lindo-Maitra-Zhang Corollary 5.6.

## How could this be wrong?

The finite campaign cannot prove the formula for all `p`; that role belongs to the explicit witness
proof. The ring-theoretic conclusions use the standard numerical-semigroup dictionaries for type,
reduced type, and almost Gorenstein completions. The result has not been journal peer reviewed or
formalized in a proof assistant.
