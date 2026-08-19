# EXP-027 - relative offset-Koszul Betti strand

Declared: 2026-08-19, before implementation or committed artifact generation. Backlog: HWB-035.

Fix `p>=4`, set `q=24p`, and write

```text
P_p=k[X_a : a in G_p],
C_p=P_p/J_p,
X_a maps to x y^a in k[x,y]/(y^q).
```

For `u=(j,b)`, let `(Delta_u,Gamma_u)` be the relative squarefree divisor pair defined in the
preflight. Its relative chain group in dimension `r-1` has basis

```text
{F subset G_p : |F|=r and b-sum(F) is in E_(j-r)}.
```

The signed deletion boundary is exactly the offset-`u` Koszul differential.

## Predictions

- P1: for every field `k`,

  ```text
  beta_(2,4)(C_p)=8p.
  ```

- P2: the multigraded support of that entry is multiplicity-free and equals

  ```text
  {3p+a : a in G_p and a>=6p}
  = [9p,11p-2]
    union [11p,13p-2]
    union {13p}
    union [14p-1,15p-1]
    union [16p+1,17p-2]
    union [17p,18p-1]
    union {19p}
    union [20p-1,21p-1].
  ```

- P3: for every field `k`,

  ```text
  beta_(3,4)(C_p)=p(5p-1)(500p^2-440p+47)/2.
  ```

- P4: under the EXP-023 presentation `J_p=(Q_p,f_p)`,

  ```text
  f_p=X_0^2X_(3p)-X_p^3,
  (Q_p:f_p)_1=span_k{X_a : a in G_p and a>=6p}.
  ```

- P5: the degree-four relative first homology is torsion-free over `Z`; therefore P1--P3 have no
  hidden characteristic exception.

## Exact campaign

- Mandatory post-implementation smoke at `p=4`.
- Route A constructs every offset block in total degree four, computes signed relative boundary
  ranks over at least two unrelated finite fields, classifies the nonzero first-homology support,
  and checks the formulas for selected explicit cases. At least one smallest case must also be
  checked by exact integer or rational reduction.
- Route B independently constructs the quadratic-fiber graph of `Q_p`, tests whether `X_a f_p`
  reduces to zero for every `a in G_p`, and verifies the closed colon support for all
  `p=4,...,300`.
- A symbolic interval certificate must prove the support count and all endpoint identities for
  arbitrary `p>=4`. Computation alone does not prove P1--P5.
- The campaign uses atomic checkpoints and deterministic row hashes.

## Adversarial controls

The implementation must reject:

- replacing `E_3=[0,24p-1]\{6p-1}` by the full interval;
- lowering the truncation threshold from `24p` to `24p-1`;
- deleting any singleton or shifting any interval endpoint in the predicted support;
- treating the two monomials of `f_p` as connected in a quadratic fiber when they are not;
- declaring a low variable `a<6p` to lie in `(Q_p:f_p)_1`;
- declaring a high variable `a>=6p` outside that colon;
- using the Hilbert coefficient identity as if it determined both Betti entries independently;
- accepting rank agreement over only one characteristic; or
- continuing after a frozen-premise hash mismatch.

## PASS, FAIL, and trust boundary

- A finite campaign PASS validates the implementation and formula search only.
- A premise-hash mismatch, budget exhaustion, or unresolved integral torsion question is
  `INCONCLUSIVE`, never a negative theorem.
- A support, rank, colon, endpoint, or Hilbert-coefficient mismatch refutes the affected
  prediction and stops the campaign.
- `CONFIRMED` requires the direct relative-Koszul derivation, an all-parameter support proof with
  integral unit-coefficient control, mandatory smoke, bounded campaign, independent colon audit,
  frozen premise hashes, and all adversarial controls.

## Budget

CPU only, no randomness. Route A: 180 seconds. Route B campaign: 120 seconds. Symbolic
certificate: 120 seconds. Atomic checkpoints are mandatory; a hard wrapper may stop any route at
twice its declared budget.
