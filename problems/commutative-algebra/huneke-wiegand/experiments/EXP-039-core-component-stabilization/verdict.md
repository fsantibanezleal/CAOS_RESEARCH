# EXP-039 verdict

Status: **REFUTED**, with a relevant structural redirect.

P1 fails at `p=6`: the defect partition is `4+2+2+1`, not nine defect-one components, and the
largest component has 5,264 vertices.  At `p=9`, only two components carry the full partition
`45+4`, with a 354,085-vertex component.  P2's bounded recurring-component model is therefore
also refuted.

The negative result exposes a more useful pattern.  For `p=6,7,8`, the four defect sectors have
dimensions

```text
binom(p-2,3), p-4, p-4, p-5.
```

At `p=9`, the first three merge in unsigned support but preserve their combined defect
`35+5+5=45`; the fourth remains of dimension four.  Their free total extends to 73 at `p=10`,
exactly one above the exact EXP-037 value 72.  This makes a first relation among four signed
sectors the strongest current explanation of the `-x^6` correction.

Every defective block is orientation-sensitive: sign erasure changes its odd rank, and one sign
flip raises that rank by one.  The next route must therefore preserve signed chain data and cannot
work only with the support graph.

The component partitions are exact and aggregate to the independently audited ranks, but the
latent sector identification remains finite and unproved.  EXP-039 does not prove the recurrence,
complete a lower strand, or resolve Huneke--Wiegand.  No manuscript or Zenodo update is opened.
