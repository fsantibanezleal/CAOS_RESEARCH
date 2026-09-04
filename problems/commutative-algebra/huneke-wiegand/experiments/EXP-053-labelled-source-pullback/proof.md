# EXP-053 proof record - HNF pullback obstruction and common source class

Date: 2026-09-04. Status: **REFUTED on P2; P1 INCONCLUSIVE BY RESOURCE GATE**.

## Exact completed checkpoints

The training extractor independently reconstructed exact row and column labels for the frozen
component at `p=8,9`. Every one of the 1,094 and parameter-expanded frozen columns was matched
uniquely to its original source or kernel-domain label, with no ambiguous signed-incidence key.
The transformed HNF was then rebuilt and its kernel hash matched the EXP-047 relative artifact.

For both stable completions, summing the two EXP-051 kernel coordinates gives an original source
chain that vanishes on every mask-58 row and whose added-row boundary equals the stored relative
boundary. The direct identities pass at both completed parameters.

## New common-source observation

The two completions use exactly the same HNF coordinates and the same labelled source chain:

```text
p=8: kernel coordinates {9,52}, labelled support 125
p=9: kernel coordinates {12,70}, labelled support 178
```

At each parameter, the complete coefficient-label multiset hash agrees between `58->59` and
`58->62`. Thus the two EXP-052 divided-boundary formulas are restrictions of one common source
cycle to the two complementary added-row blocks. A future labelled identity can target the union
`58->63` once, rather than construct the first class independently in the two completions.

## Refutation and resource boundary

P2 is refuted on the completed checkpoints. Although every source coefficient has absolute value
at most four, the pullback has 75 coefficient-sensitive semantic skeletons in each completion,
far above the declared limit twelve. The HNF pullback is therefore not the compact semantic proof
object exposed by EXP-052.

The `p=10` labelled component scan completed, but its transformed-HNF operation did not return at
the declared safe-stage wall-time gate. The process was interrupted after preserving `p=8,9`.
P1 is consequently `INCONCLUSIVE_RESOURCE`; no `p=10` chain is claimed. Labelled source data at
`p=11` remained unopened, so P3 was not evaluated.

The audit hash-locks the extractor and artifact, rechecks internal hashes, label normalization,
support and coefficient statistics, common-source equality, and all persisted identity flags. It
passes 45/45 checks. This is an integrity and cross-completion audit, not a second HNF
reconstruction.

The training artifact has SHA-256
`c415521c477b715ecea71cb1e983279b26f44baed78e54995674fa430167dc31` and internal hash
`be6fa11e45e53f9c65d42c09116f37342965312f48ada39bf09387ef6acad634`. The audit certificate has
SHA-256 `8d90589fdb4b5eaf359f2e7d5eebc6077afbf05a98631430eae7088c91a57fc3` and internal hash
`9207360a92a404444550f68e6d7b6d18306a42a0ab3357784d242f24f874ee71`.

## Redirect

Do not continue generic HNF pullback to `p=10,11`. Construct a labelled source chain directly
against the union of the frozen `58->59` and `58->62` boundary formulas. The desired identity is
one simultaneous telescoping equation on mask `63`; its two projections recover the first
nonzero class in each completion. The second independent class and the upper bound remain
separate obligations.

No manuscript or Zenodo update is triggered.
