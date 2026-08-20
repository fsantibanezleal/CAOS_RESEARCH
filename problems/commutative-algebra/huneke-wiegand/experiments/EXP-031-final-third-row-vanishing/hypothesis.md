# EXP-031 hypothesis - final third-row vanishing

Status at declaration: **ACTIVE, NO RESULT CLAIMED**.

## Falsifiable prediction

For every integer `p>=4`, every field `k`, and every offset `b`, the total-degree-seven relative
homology group is zero:

```text
H_2(Delta_(p,(7,b));k)=0.
```

Equivalently,

```text
beta_(3,(7,b))(C_p)=0 for all b,
beta_(3,7)(C_p)=0.
```

Together with EXP-027, EXP-029, EXP-030, regularity four, and the minimal-shift bound, this would
complete the third homological row.

## Predicted integral contraction

Use the relative-cell predicate

```text
F is a cell iff b-sum(F) is in E_(p,7-|F|).
```

Because `E_(p,4)=E_(p,5)=[0,24p-1]` and
`E_(p,3)=[0,24p-1] minus {6p-1}`, Boolean matching on vertex `0` leaves precisely the triangles
`F` not containing `0` with residual `6p-1`.

For each unmatched triangle, let `x(F)` be the least member of

```text
([1,p] union [3p,4p-2]) minus F.
```

The prediction is that `F union {x(F)}` is an unmatched tetrahedron whose reduced boundary has
coefficient `+1` or `-1` on `F` and zero on every other unmatched triangle. Distinct unmatched
triangles receive distinct fillers. Hence the reduced boundary onto unmatched triangles is a
signed identity block and integral `H_2` vanishes.

Any missing filler, duplicate filler, second unmatched face, nonunit coefficient, nonzero exact
rank, or characteristic discrepancy refutes the relevant prediction.

## Canonical route

- Freeze and verify the four premise hashes in the preflight.
- Check the cumulative offset identities for all `p=4,...,300`.
- At `p=4`, construct complete degree-seven edge, triangle, and tetrahedron groups at every offset
  and compute `H_2` over `GF(2)` and `GF(1000003)`.
- At `p=5`, compute the complete profile over `GF(2)` within the declared budget.
- Independently enumerate all critical triangles and verify the unit filler map at the finite
  campaign parameters.

## Independent route

Rebuild `G_p`, the residual sets, critical triangles, and the least-low filler assignment from the
block formulas. Do not import the canonical module. Check all offsets for `p=4,...,12` and the
symbolic endpoint obligations through `p=300`.

## Compute and budget

- CPU only; repository Python 3.13 virtualenv; exact integer and finite-field arithmetic; no
  randomness.
- Smoke: `p=4`, two fields, 180-second budget, checkpoint every 25 offsets.
- Canonical: `p=4,5`, 900-second budget. If the full `p=5` rank route exceeds budget, preserve it
  as `INCONCLUSIVE_BUDGET`; the unit-filler certificate remains a separate route.
- Independent audit: 180 seconds.
- Generated artifacts must contain status, elapsed time, premise hashes, complete profiles or
  declared checkpoints, and canonical hashes.

## Success and claim gates

1. This declaration commit predates implementation and generated artifacts.
2. The complete `p=4` two-field profile is identically zero.
3. The canonical unit-filler checker passes all declared parameters and rejects perturbed holes,
   filler zero, and a deliberately reused filler.
4. The independent implementation agrees without importing canonical code.
5. A written all-parameter proof gives the acyclic matching and signed unit block.
6. Only after all gates pass may EXP-031 be marked CONFIRMED and manuscript v0.18 be opened.

A finite PASS alone validates code; it does not prove the all-parameter or every-field theorem.
