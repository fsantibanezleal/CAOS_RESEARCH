# EXP-028 - complete second Betti row

Declared: 2026-08-19, before implementation or committed artifact generation. Backlog: HWB-035.

Fix `p>=4`, put `q=24p`, and retain the notation and integral relative offset-Koszul
identification of EXP-027 for

```text
C_p=P_p/J_p,
P_p=k[X_a : a in G_p].
```

## Predictions

- P1: for every field `k`,

  ```text
  beta_(2,5)(C_p)=p(2p-3).
  ```

- P2: the complete offset support of `beta_(2,5)` is

  ```text
  A_p=[3p+2,5p-2],
  B_p=[6p+1,8p-3],
  C_p=[9p,11p-4].
  ```

  Each block has `2p-3` offsets, and there is no degree-five first homology outside their union.

- P3: writing `r=0,...,2p-4`, the offset multiplicities are

  ```text
  beta_(2,(5,3p+2+r))  = m_out(r),
  beta_(2,(5,6p+1+r))  = m_mid(r),
  beta_(2,(5,9p+r))    = m_out(2p-4-r),

  m_out(r)=min(floor(r/2)+1, floor((2p-4-r)/2)+1),
  m_mid(r)=min(r+1, 2p-3-r, p-2).
  ```

- P4: for every field `k`,

  ```text
  beta_(2,6)(C_p)=0.
  ```

- P5: the relevant integral first homology is free abelian in total degree five and zero in total
  degree six. Hence P1--P4 have no hidden characteristic exception.

- P6: together with the confirmed results of EXP-024 and EXP-027, the complete second Betti row
  is

  ```text
  beta_(2,3)=2p(500p^2-330p+31)/3,
  beta_(2,4)=8p,
  beta_(2,5)=p(2p-3),
  beta_(2,6)=0,
  beta_(2,j)=0 for j outside {3,4,5,6}.
  ```

## Exact campaign

- Mandatory post-implementation smoke at `p=4`.
- Route A constructs every relevant offset block in total degrees five and six, computes signed
  relative boundary ranks over `GF(2)` and `GF(1000003)` at `p=4`, and extends the degree-five
  `GF(2)` profile through `p=5,6`.
- Route B independently constructs signed integral boundary matrices at selected smallest offsets
  and checks Smith-normal-form or rational ranks without importing Route A rank code.
- Route C certifies the all-parameter interval classification: critical edge families, surviving
  Morse relations, degree-six filling, support endpoints, reflection, and multiplicity sums.
- Closed formulas and endpoint identities run for every `p=4,...,300` with deterministic hashes.
- Computation alone does not prove P1--P6; confirmation requires the integral case classification
  in `proof.md`.

## Adversarial controls

The implementation must reject:

- filling the unique hole `6p-1` in `E_3`;
- shifting, deleting, or merging one of the three support blocks;
- replacing `m_out` or `m_mid` by a nearby endpoint or plateau formula;
- treating a critical edge as a homology class before applying the Morse boundary;
- accepting the third block without its nonzero critical-triangle cancellations;
- inferring characteristic independence from one finite field;
- inferring `beta_(2,6)=0` from regularity alone;
- treating a mapping-cone colon count as the complete degree-five answer; or
- continuing after a frozen-premise mismatch or budget exhaustion.

## PASS, FAIL, and trust boundary

- A finite campaign PASS validates the implementation, formula, and checked chain ranks only.
- Premise mismatch, budget exhaustion, unresolved Morse differential, or unresolved integral
  torsion is `INCONCLUSIVE`, never a theorem or counterexample.
- Any support, multiplicity, rank, reflection, or endpoint mismatch refutes the affected
  prediction and stops the campaign.
- `CONFIRMED` requires an all-parameter integral matching proof, mandatory smoke, bounded
  campaign, independent audit, frozen premises, and all adversarial controls.

## Budget

CPU only and deterministic. Route A: 180 seconds. Route B: 120 seconds. Route C: 120 seconds.
Atomic checkpoints are mandatory; a hard wrapper may stop a route at twice its declared budget.
