# EXP-011 verdict - uniform endomorphism family CONFIRMED

Run date: 2026-08-10. Exact integer and bitset arithmetic, CPU only.

## Result

All six predictions pass. For every integer `p>=4`, with `s=6p`, the EXP-009 ideal
`J_p=(1,t^s)` has endomorphism value semigroup

```text
Lambda_p = Gamma_p union (7s+Q_p) union {13s-1},
Q_p = [p+1,2p-2] union {2p,4p}.
```

The symbolic derivation in `proof.md` proves

```text
multiplicity = 24p,
Frobenius = 54p-1,
conductor = 54p,
genus = 38p-1,
embedding dimension = 12p.
```

The semigroup is nonsymmetric. The endomorphism ring is therefore not Gorenstein, is strictly
larger than `R_p`, and exhibits the same nonreflexive Ext/Tor escape mechanism as the public seed
for every member of the infinite family.

## Computational and adversarial record

- The exact campaign checked all 297 parameters `p=4,...,300` in under five seconds.
- Direct adjacent-block intersection agreed exactly with additive generation from the predicted
  minimal generators at every parameter.
- Every row passed the formula, difference-set, conductor, genus, generator-count, and
  nonsymmetry checks.
- The campaign aggregate is
  `e21926a689178a6c70b3b6e8319053edd0fd13f164ced9565d3b976e6159c0b0`.
- A separate implementation rehashed all 297 rows and reconstructed full semantic windows at
  `p=4,5,17,73,151,300`.
- The independent audit aggregate is
  `2ed711045ad83a3b47fb3e71d4c75ae9bfa9be1a5dd9a8c4072d5f170510343b`.
- Removing the first required `Q_p` value and omitting the terminal singleton were both rejected.
- The initial smoke run exposed a one-shift truncation in the new checker at the end of its finite
  window. No campaign artifact had been written. Extending the source membership window by the
  required shift fixed the implementation without changing the declared formula or predictions.

## Prediction ledger

- P1 PASS: the exact block formula is proved and all finite instances agree.
- P2 PASS: the five numerical formulas follow from the last incomplete block and exact gap count.
- P3 PASS: the `p` new level-7 values are minimal and the old Frobenius is generated.
- P4 PASS: genus `38p-1` differs from the symmetric value `27p` for every `p>=4`.
- P5 PASS: the current Dey-Lyle source was reread and its hypotheses hold uniformly.
- P6 PASS: both exact routes, all row hashes, six reconstructions, and two corruptions agree.

Verdict: **CONFIRMED**.

## Consequence and scope

EXP-011 closes a substantive part of HW-P5: the seed-only endomorphism anatomy from EXP-002 is now
a theorem for the full EXP-009 family. It does not classify every rigid ideal, every Route K model,
or every nearby Kunz face. Son Pham retains priority for the first public counterexample.

This is new theorem-level material beyond manuscript v0.03. It triggers a manuscript v0.04 claim
audit and a Zenodo new version under methodology 09; publication must not occur until the revised
manuscript is built, rendered, and checked against this verdict.

## How could this be wrong?

The finite computation cannot prove the formulas for all `p`; that role belongs to `proof.md`.
The remaining risk is a mistaken theorem-hypothesis translation in the Dey-Lyle consequences.
That risk is reduced by direct rereading of Proposition 4.1(2) and Theorems 4.2 through 4.4 and by
the already independent EXP-002 dependency audit. Journal peer review and proof-assistant
formalization remain absent.
