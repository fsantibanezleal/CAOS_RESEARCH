# EXP-053 proof record - HNF pullback obstruction and common source class

Date: 2026-09-04. Status: **REFUTED on P2; P1 PASSES FINITELY WITH A RESOURCE OVERRUN**.

## Exact completed checkpoints

The training extractor independently reconstructed exact row and column labels for the frozen
component at `p=8,9,10`. Every frozen column was matched uniquely to its original source or
kernel-domain label, with no ambiguous signed-incidence key.
The transformed HNF was then rebuilt and its kernel hash matched the EXP-047 relative artifact.

For both stable completions, summing the two EXP-051 kernel coordinates gives an original source
chain that vanishes on every mask-58 row and whose added-row boundary equals the stored relative
boundary. The direct identities pass at all three training parameters.

## New common-source observation

The two completions use exactly the same HNF coordinates and the same labelled source chain:

```text
p=8: kernel coordinates {9,52}, labelled support 125
p=9: kernel coordinates {12,70}, labelled support 178
p=10: kernel coordinates {15,88}, labelled support 238
```

At each parameter, the complete coefficient-label multiset hash agrees between `58->59` and
`58->62`. Thus the two EXP-052 divided-boundary formulas are restrictions of one common source
cycle to the two complementary added-row blocks. A future labelled identity can target the union
`58->63` once, rather than construct the first class independently in the two completions.

## Refutation and resource boundary

P2 is refuted on the completed checkpoints. Although every source coefficient has absolute value
at most four, the pullback has 78 coefficient-sensitive semantic skeletons in each completion,
far above the declared limit twelve. The HNF pullback is therefore not the compact semantic proof
object exposed by EXP-052.

The `p=10` transformed-HNF operation exceeded the 600-second safe-stage gate. Its parent terminal
was interrupted, but the exact process continued and later wrote a complete checkpoint. That
checkpoint passes the same mapping, kernel-hash, and direct-identity checks, so P1 passes finitely
with a documented resource overrun. Labelled source data at `p=11` remained unopened, so P3 was
not evaluated.

The audit hash-locks the extractor and artifact, rechecks internal hashes, label normalization,
support and coefficient statistics, common-source equality, and all persisted identity flags. It
passes 62/62 checks. This is an integrity and cross-completion audit, not a second HNF
reconstruction.

The training artifact has SHA-256
`0d6bb8b885d965ed91a94d06a072d8baacca56df65903e10e1c91382f649edfe` and internal hash
`51abddcec492659908769aafa0451c7ca43cbab72befb6ddee04673f0c80899d`. The audit certificate has
SHA-256 `4f283e79434d312c6de06a063b6784c17f6e0b422a4c97054c3a63c4dc822127` and internal hash
`3c94a9abb2a481eb45dd15664ff44fecf2af146f13b1ae18aeeb95823833a9bc`.

## Redirect

Do not continue generic HNF pullback to `p=11`. Construct a labelled source chain directly
against the union of the frozen `58->59` and `58->62` boundary formulas. The desired identity is
one simultaneous telescoping equation on mask `63`; its two projections recover the first
nonzero class in each completion. The second independent class and the upper bound remain
separate obligations.

No manuscript or Zenodo update is triggered.
