# EXP-040 hypothesis - a degree-six relation in the merged parity sector

Date: 2026-08-30. CPU only. Exact arithmetic over declared prime fields.

## Claims

Let the four latent EXP-039 defect sectors have free dimensions

```text
T_p=binom(p-2,3),  L_p=p-4,  L'_p=p-4,  R_p=p-5.
```

At `p=9`, the first three lie in one connected support component with defect
`35+5+5=45`, while `R_9=4` stays separate.

### P1. First relation at `p=10`

The complete unit-peeled `(10,2)` core has exactly two characteristic-dependent connected
components, with odd-minus-two rank defects

```text
(T_10+L_10+L'_10)-1=67,  R_10=5.
```

Thus the exact total `72` localizes its one-unit correction entirely inside the merged sector.

### P2. First translates at `p=11`

Conditional on P1, the `(11,2)` defects are

```text
(T_11+L_11+L'_11)-2=96,  R_11=6.
```

The two-unit correction is compatible with two degree-one translates of one degree-six relation.

### P3. Signed bridge certificate

After transporting the four sector tags from `p=6,7,8`, a signed set of cross-sector columns can
be isolated whose removal restores the free merged defects `68` and `98`; reinstating the columns
reduces them by exactly one and two.  P3 requires explicit signed column hashes and tag maps.  P1
and P2 alone do not establish it.

## Premise dependencies

- EXP-039 is **REFUTED** for bounded defect-one components but exactly certifies the partitions
  through `p=9` and their orientation sensitivity.
- EXP-037 exactly and independently audits the aggregate `p=10` ranks and value 72.
- EXP-038 exactly and independently audits the aggregate `p=11` ranks and value 102, but remains
  inconclusive for the all-parameter relation.

Frozen EXP-039 SHA-256 hashes are

```text
proof       43071ff8b6a3c23acc319798aab3fdac78610665ec95506e32ff2e5053fb28da
verdict     61376ab683151239c7c6f446f2d0cf55afe76e00b2fcad32fa69baf27621042e
run.py      8ab5678829094a2b314a23889201b06f555aafc5af176500ef62a5eb30e4a352
result      831a4300cac10bf44753050a686a7993fabef09bf28b4332c6bb1fb9881c9e2c
audit       55e3159dd01f9c412ad56a5808eda1f428672341b57ce5dd6eb4e2f266051534
```

## Method and controls

1. Import the frozen EXP-039 decomposition and add only the already audited aggregate rank gates
   for `p=10,11`.
2. Rank every residual component over `GF(2)`, `GF(3)`, and `GF(5)`.
3. Require exact componentwise agreement between the two odd fields and agreement of component
   sums with the frozen complete ranks.
4. Preserve the sign-erased and one-sign-flipped controls on every defective component.
5. Stop after `p=10` if its partition is not `67+5`; otherwise checkpoint before `p=11`.
6. Attempt P3 only after both numerical partitions pass.

## What PASS and FAIL prove

- **P1 PASS** finitely localizes the first correction to the merged sector; it does not prove the
  relation.
- **P1 FAIL** refutes the four-sector placement and stops P2/P3.
- **P2 PASS** gives a second, independently declared multiplicity check compatible with translated
  relations; it still does not prove an all-parameter module.
- **P2 FAIL** refutes the simple translation count.
- **P3 PASS** supplies a finite signed relation mechanism.  An all-parameter translation theorem
  remains mandatory before EXP-038 can be confirmed.

## Invariant-first and compute budget

Component rank partitions are the cheapest invariant capable of locating the correction.  P1 has
a 900-second, 30-GB cap.  Conditional P2 raises the combined cap to 2,400 seconds and 36 GB.  Each
completed parameter is checkpointed.  Resource stop means **INCONCLUSIVE**.  No finite-only pass
opens a manuscript or Zenodo gate.
