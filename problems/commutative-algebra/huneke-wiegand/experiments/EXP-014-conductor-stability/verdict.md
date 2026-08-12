# EXP-014 verdict - duality correction and conductor nonstability CONFIRMED

Run date: 2026-08-12. Exact integer and bitset arithmetic, CPU only.

## Result

Two all-parameter conclusions are confirmed.

First, the EXP-013 balance

```text
length(R_p/(R_p:E_p))=length(E_p/R_p)
```

is a specialization of one-dimensional Gorenstein local duality, explicitly present as
Herzog-Kumashiro Proposition 3.1 Claim 1. It is not family-specific novelty. The exact conductor
formula and its common trace interpretation remain the family-specific EXP-013 result.

Second, for every integer `p>=4`, the common conductor/trace ideal `T_p` is not stable. Dey
Corollary 3.7 proves this from `type(E_p)=10p>1`, while the independent explicit witness is

```text
8s+p+1 in v(T_p^2) minus v(t^(4s)T_p).
```

## Computational and adversarial record

- The exact campaign checked every `p=4,...,300` in under four seconds.
- The proved tail bound reduces the complete quotient to values below `17s`.
- Every parameter rejected stability and contained the declared witness.
- A separate implementation rehashed all 297 rows and reconstructed
  `p=4,5,17,73,151,300` without importing experiment code.
- Campaign aggregate:
  `b965a77a1a7c572f1ef01451439acae072a7db2f9c5c4e25c3d42717f7bc3339`.
- Audit aggregate:
  `22f7ddca76fbabc62d5cb90dd6e2a71ffc342bf7ecd102eef81c146a3365d768`.
- `results.json` SHA-256:
  `ef1694e15bdd9bd7520b69a26b9579e79b66caed5fbd097921163eed1ab53080`.
- `audit.json` SHA-256:
  `2848ab9c83ec97c231c9a0d0c52a0b60ba0b720f907148f8f714351a0927f37d`.
- The false-stability control was rejected at every parameter.

## New pattern, not yet an all-parameter claim

All 297 exact rows exhibit defect length `14p`, distributed at levels
`8,9,10,11,12,16` as

```text
2p, p, 3p, 6p, 2p-1, 1.
```

The exact residue blocks are stable across the campaign. EXP-014 does not promote this fitted
pattern to an infinite theorem. It triggers a separately declared symbolic EXP-015.

## Prediction ledger

- P1 PASS with correction: the length balance is general local duality, not new family structure.
- P2 PASS: `T_p` is nonstable for every `p>=4` by Dey's criterion.
- P3 PASS: the explicit monomial witness proves nonstability independently.
- P4 PASS as finite evidence: the complete tested defect sets were determined and expose a
  theorem candidate.

Verdict: **CONFIRMED**.

## Consequence and scope

The manuscript requires a new version because its current sentence calls the balanced defect new
data. The corrected statement must credit general local duality and distinguish it from the exact
family formula. The nonstability theorem and any proved exact defect formula are possible new
material, but publication waits for EXP-015 and the full claim audit.

This does not classify arbitrary rigid ideals, arbitrary finite birational extensions, or the
nearby Kunz face.

## How could this be wrong?

The deductive conclusion depends on the exact EXP-009, EXP-011, EXP-012, and EXP-013 premises and
on applying the cited local theorems with the rings in the correct order. The explicit witness
removes dependence on Dey's theorem for nonstability. The `14p` defect pattern remains only finite
evidence until EXP-015 supplies an all-parameter sumset proof.
