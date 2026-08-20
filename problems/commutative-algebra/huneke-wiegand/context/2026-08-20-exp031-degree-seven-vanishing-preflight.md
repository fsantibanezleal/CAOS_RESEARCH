# EXP-031 preflight - final third-row vanishing

Date: 2026-08-20. Scope: HWB-035 and HWB-045.

## Question and claim boundary

Determine the last regularity-allowed entry in the third homological row of the conductor special
fiber `C_p`, namely `beta_(3,7)`, for every integer `p>=4` and every field. A confirmation would
complete the third row only. It would not determine the remaining higher rows, the full Betti
table, the full minimal resolution, or any new statement about the already-false broad
Huneke--Wiegand conjecture.

## Why the route changes

The EXP-029 pre-declaration probe found `beta_(3,7)=0` at `p=4,5`, but no theorem was claimed.
EXP-030 then identified the complete cubic-colon quotient. Its next resolution strand contributes
no degree-four second syzygy when the low codimension is `2p-2>=6`, but that observation alone
does not exclude a contribution from `P_p/Q_p`.

The stronger route works directly in the total-degree-seven relative complex. The cumulative
offset sets simplify to

```text
E_(p,5)=E_(p,4)=[0,24p-1],
E_(p,3)=[0,24p-1] minus {6p-1}.
```

Match a cell not containing the distinguished vertex `0` with the cell obtained by adjoining
`0`, whenever the latter exists. In homological dimension two, every triangle is matched except a
triangle `F` with

```text
b-sum(F)=6p-1.
```

For each such triangle, choose the least positive low generator

```text
x in ([1,p] union [3p,4p-2]) minus F.
```

There are `2p-1>=7` positive low generators, so this set is nonempty. The tetrahedron `F union
{x}` has residual `6p-1-x` in `E_(p,3)`. It has `F` as its only unmatched triangle face because a
different deleted vertex cannot reproduce the residual hole. This predicts a unit diagonal from
unmatched tetrahedra onto all unmatched triangles.

This is a candidate integral contraction, not a result until its signs, cell predicates,
acyclicity, uniqueness, and exact finite profiles pass the declared gates.

## Frozen premises

| premise | SHA-256 | use |
|---|---|---|
| EXP-024 `proof.md` | `b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088` | regularity and minimal-shift boundary |
| EXP-027 `proof.md` | `355ff5c7e4bbc74fc8a1e346aac041d77b3fbc758051dbc729836db6a259e0bc` | relative-complex dictionary and exact offset sets |
| EXP-030 `proof.md` | `1822095a7d16207b7d04261b7a6645f7ca51b01f490ba9d212a84ab7ca5bc729` | complete cubic colon and degree-six calibration |
| EXP-030 `verdict.md` | `7f8d2fe3c61a0fc1f864452ca98d05d04e154496a2d45d2c8d8a7b32644de4d9` | confirmed scope boundary |

Any mismatch stops the canonical run as `INCONCLUSIVE_PREMISE`.

## Required routes

1. Canonical chain checker: enumerate the degree-seven relative complex at the smoke parameters,
   compute exact `H_2` ranks, and separately validate every distinguished-vertex match and unit
   filler.
2. Independent audit: rebuild the cell predicates and filler assignment without importing the
   canonical implementation; check uniqueness and direct signed boundary coefficients.
3. Symbolic proof: establish the all-parameter residual identities, availability of a positive low
   filler, acyclicity of the zero-vertex matching, and the one-critical-face property.
4. Integral gate: the reduced block must have unit diagonal. Finite-field agreement is a control,
   not the source of characteristic independence.

## Manuscript decision

If confirmed, this completes the third homological row and is material enough for an in-place
v0.18 revision of the existing homological manuscript. A separate manuscript remains deferred
until a genuinely distinct higher-row mechanism or a complete resolution appears.
