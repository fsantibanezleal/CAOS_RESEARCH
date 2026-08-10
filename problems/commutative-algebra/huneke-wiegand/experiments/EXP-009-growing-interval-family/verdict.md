# EXP-009 verdict - infinite growing-interval family CONFIRMED

Run date: 2026-08-10. Exact arithmetic, CPU only.

## Result

The construction in `hypothesis.md` is an infinite family. For every integer `p>=4`, the displayed
`Gamma_p` is a symmetric numerical semigroup with

```text
s = 6p,
multiplicity = 4s,
Frobenius number = 13s-1,
conductor = 13s,
embedding dimension = 11p,
```

and the nonprincipal ideal `I_p=(t^(4s),t^(5s))` is rigid. The full proof is in `proof.md`.

This produces infinitely many counterexamples in the same two-generated monomial-ideal class as
the public seed. Son Pham retains priority for the first public counterexample; the parametric
construction is the CAOS extension.

## Computational and adversarial record

- The exact campaign evaluated `p=2,...,300` in 2.45 seconds.
- `p=2,3` fail, while all 297 parameters `p=4,...,300` satisfy the affine residue identities.
- The original standard-library symmetry, closure, generation, minimal-generator and rigidity
  checks pass at `p=4,5,10,25,50`; boundary values `p=2,3` fail as predicted.
- A separate auditor reconstructed all 299 membership hashes and freshly ran standard checks at
  `p=2,3,4,5,10,25,50,75`.
- The `p=4` and `p=5` masks reproduce the independently audited Route K models at `s=24` and
  `s=30` byte-for-byte.
- Clearing the multiplicity endpoint and filling the omitted reflected selector are both rejected.
- Every family member is deductively outside the generalized-arithmetic-sequence positive class.

## Predictions

- P1 PASS: exact boundary failures and all declared positive parameters agree.
- P2 PASS: all seven affine sumset identities hold, and `proof.md` derives them for every `p>=4`.
- P3 PASS after the pre-run erratum: the lower blocks generate the semigroup and the embedding
  dimension is `11p`.
- P4 PASS: the interval-layer calculation proves `D=E+E` for all `p>=4`.
- P5 PASS: `4s+1`, the later member `4s+3p`, and the intervening gap `4s+p+1` give the exclusion.
- P6 PASS: both Route K hashes and both adversarial corruptions behave as predicted.

Verdict: **CONFIRMED**.

## Scope and publication consequence

The result is an infinite family theorem inside numerical semigroup rings and two-generated
monomial ideals. It does not classify counterexamples, arbitrary modules, or arbitrary
one-dimensional Gorenstein domains. It is nevertheless a material theorem beyond preprint v0.02,
so it triggers a manuscript revision and a new Zenodo version after the manuscript claim audit.

## How could this be wrong?

The main residual risk is expository: a hidden mistake in translating the exact residue identities
to the ring-theoretic rigidity statement. EXP-001 through EXP-003 independently support that
dictionary, and the finite full-window checker agrees at all audited checkpoints. The theorem does
not assert that every Route K model lies in this family or that the threshold `p=4` is globally
minimal outside the stated formula.
