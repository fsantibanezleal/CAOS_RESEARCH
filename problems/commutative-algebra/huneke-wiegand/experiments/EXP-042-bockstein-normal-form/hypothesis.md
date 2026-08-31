# EXP-042 hypothesis - Bockstein normal form of the persistent isolated sector

Date: 2026-08-31. CPU only. Exact signed integer extraction plus bit-packed mod-two reduction.

## Question and predictions

Let `M_p` be the exact signed matrix of the isolated normalized twelve-atom component identified
by EXP-041 for `p=8,...,11`.

### P1. Frozen extraction

An independent extractor must reproduce the frozen component support hash, signed hash, row and
column counts, nonzero count, and ranks over `GF(2)`, `GF(3)`, and `GF(5)` at every parameter.
Failure is an implementation failure and no Bockstein output is evidence.

### P2. The observed rank gap is visible in the first Bockstein

For a canonical basis of `ker(M_p mod 2)`, form

```text
beta_p(z) = (M_p z)/2 mod (2, im(M_p mod 2)).
```

The predicted Bockstein ranks are exactly the frozen odd-minus-two defects:

```text
p=8,9,10,11 -> rank(beta_p)=3,4,5,7.
```

A pass produces that many independent order-exactly-two elementary-divisor directions in each
finite isolated component. It does not prove that these are all integral torsion factors unless a
separate rational-rank upper bound is supplied.

### P3. Order and basis independence

Forward and reversed column orders must produce the same kernel dimension, matrix rank, and
Bockstein rank. A separately implemented auditor must verify every stored kernel equation over
`GF(2)`, every even lift, every quotient reduction, and the final ranks from compact witness
certificates.

## Method

1. Reconstruct the EXP-039/041 signed support and exact two-sided leaf peeling.
2. Select the unique defective component with the frozen EXP-041 coefficient-tag support and
   normalized twelve-atom skeleton.
3. Store its signed sparse columns, semantic atom labels, and frozen hashes.
4. Reduce bit-packed row vectors over `GF(2)` while tracking kernel combinations.
5. Lift every kernel basis vector with coefficients in `{0,1}`, compute the even integer boundary,
   divide by two, and reduce the result modulo the mod-two column image.
6. Reduce the resulting quotient classes to compute `rank(beta_p)` and retain independent compact
   witness hashes.
7. Repeat with reversed column order and audit independently.

## Evidence boundary and resource gate

The `p=8` smoke is capped at 600 seconds and 20 GB. The primary `p=8,...,11` campaign is capped at
2,400 seconds and 36 GB with atomic per-parameter output. A resource stop is inconclusive. Exact
finite Bockstein ranks do not prove an all-parameter recurrence, an OI/FI structure, the full
lower strand, or a new Huneke--Wiegand theorem. No manuscript or Zenodo update is authorized by a
finite pass alone.
