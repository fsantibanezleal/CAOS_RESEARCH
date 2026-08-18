# EXP-025 - curvilinear and primary structure

Declared: 2026-08-18, before implementation or artifact generation. Backlog: HWB-031.

Fix an integer `p>=4`, put `q=24p`, and retain the frozen notation

```text
C_p=P_p/J_p,
P_p=k[X_a : a in G_p],
X_a maps to the degree-one class with offset a,
G_p=E_1.
```

EXP-021 proves that `C_p` is one-dimensional Cohen--Macaulay and free of rank `q` over
`k[X_0]`. EXP-023 proves that degree-`n` monomials agree exactly by total offset, and vanish
exactly when that offset is absent from `E_n`.

## Predictions

- P1: with degree one assigned to every generator `x y^a`, there is a graded isomorphism

  ```text
  C_p isomorphic to k[x y^a : a in G_p] inside k[x,y]/(y^q),
  X_a maps to x y^a.
  ```

- P2: dehomogenization at the reduction variable is the curvilinear algebra

  ```text
  C_p/(X_0-1) isomorphic to k[y]/(y^q),
  X_a maps to y^a.
  ```

- P3: if `L_p=(X_a : a>0)`, then

  ```text
  radical(J_p)=L_p,
  J_p is L_p-primary.
  ```

  Thus this is a complete primary decomposition with one component.

- P4: the nilradical `N_p=L_p/J_p` has sharp nilpotency index `q`:

  ```text
  N_p^q=0 but N_p^(q-1) is nonzero,
  ```

  with `X_1^(q-1)` as the sharp witness.

- P5: `J_p` is saturated for the irrelevant ideal and `Proj(C_p)` is a length-`q`
  curvilinear fat point supported at `[1:0:...:0]`, with one-dimensional Zariski tangent space.

- P6: that projective scheme is locally Gorenstein, while its homogeneous coordinate ring is
  neither level nor Gorenstein and has Cohen--Macaulay type `10p+1`.

## Deductive route

1. Compare every graded piece with the offset basis `E_n` to prove P1.
2. Use `0,1 in G_p` and the relations `X_0^(a-1)X_a=X_1^a` to obtain P2; use the frozen rank
   `q` to prove injectivity.
3. Identify the nilradical from P1 and prove the sharp exponent from the minimum positive offset
   `1`.
4. Use one-dimensional Cohen--Macaulayness: there are no embedded associated primes. The unique
   minimal prime therefore makes zero primary in `C_p`, proving P3.
5. Use positive depth to prove saturation; then dehomogenize on the unique support chart to prove
   P5 and P6.

## Exact campaign and audit

- Mandatory smoke at `p=4` after implementation.
- Full exact campaign at every `p=4,...,300` using integer/set arithmetic only.
- Route A reconstructs `G_p`, all relevant sumsets, dimensions, dehomogenization relations,
  nilpotence witnesses, and the unique coordinate radical from the disjoint Artinian layers.
- Independent Route B starts from the closed affine blocks, does not import Route A, rebuilds
  `p=4,5,17,73,151,300`, and rehashes every campaign row.
- Premise files are accepted only at the hashes frozen in the preflight.

## Adversarial controls

The implementation must reject all of the following:

- deletion of offset `1`, which destroys the asserted curvilinear generator;
- truncation exponents `q-1` and `q+1`;
- a corrupted degree-three hole or degree-four completeness claim;
- a proposed radical omitting one positive-offset coordinate;
- nilpotency exponents `q-1` and `q+1`;
- the false assertion that `C_p` itself is Gorenstein; and
- the invalid inference "unique minimal prime implies primary" when the Cohen--Macaulay/no-
  embedded-primes premise is removed.

## PASS, FAIL, and trust boundary

- A finite PASS validates the implementations only. The theorem for every `p>=4` requires the
  written symbolic argument from the frozen EXP-021/023 premises.
- Any smoke or campaign mismatch refutes the affected prediction and stops the campaign.
- A premise-hash mismatch or budget exhaustion yields `INCONCLUSIVE`, never a negative theorem.
- `CONFIRMED` requires the symbolic proof, mandatory smoke, full campaign, independent audit,
  all adversarial controls, and explicit separation of local from arithmetic Gorensteinness.

## Budget

CPU only, no randomness. Campaign budget: 60 seconds. Independent audit budget: 60 seconds.
Rows are checkpointed atomically. A hard wrapper may stop either process at 120 seconds.

