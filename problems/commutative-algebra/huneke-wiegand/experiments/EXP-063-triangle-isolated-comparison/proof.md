# EXP-063 proof and certificate interpretation

Date: 2026-09-20. Scope: exact finite computation for `p=8,9,10,11`.

## 1. The target comparison is literal

EXP-048 replays the two unit-leaf cancellation stages used to obtain the
persistent component. A unit row-leaf block and a unit column-leaf block have
the respective forms

```text
[e 0]       [e a]
[b C]       [0 C],                 e in {+1,-1}.
```

In the first case, target contraction sends `(y0,y)` to
`y-b e^(-1)y0`; in the second it sends `(y0,y)` to `y`. Therefore a target
vector supported only on rows surviving every cancellation is carried to the
same coordinate vector in the reduced target. This elementary calculation is
the only algebraic-Morse input needed here.

For every triangle `T=(i,j,k)`, the EXP-062 row label is reconstructed without
calling its producer:

```text
x_T = [K,(L_p minus {p-i-j,3p+i,3p+j}) union {6p};11p-2].
```

All 19 labels over the four parameters occur uniquely among the final
component rows. Every one has semantic atom `R5`. Hence no chosen triangle row
was a pivot, and the contraction sends each `x_T` to its literal surviving
coordinate. The frozen signed-component hashes are checked before this
identification.

EXP-062 supplies an original integral source whose boundary is `+/-2x_T` in
the unsigned exact-row convention. Thus every image class still has order
dividing two after contraction and any row projection.

## 2. Exact binary quotient calculation

For mask `m`, write `R_m` for the frozen signed component matrix restricted to
the rows selected by `m`, and let `X_m` contain the corresponding unit vectors
for the triangle rows. The computed invariant is

```text
dim_F2 ((im(R_m mod 2)+span(X_m))/im(R_m mod 2)).
```

Both low-pivot and high-pivot elimination give the same relation subspace.
The ranks are:

| `p` | triangles | mask 56 | mask 58 | mask 59 | mask 62 |
|---:|---:|---:|---:|---:|---:|
| 8 | 3 | 0 | 1 | 3 | 3 |
| 9 | 4 | 0 | 2 | 4 | 4 |
| 10 | 5 | 0 | 3 | 5 | 5 |
| 11 | 7 | 1 | 5 | 7 | 7 |

These equal the independently frozen Bockstein ranks of the four carriers.
For masks 59 and 62 there is no relation among the triangle vectors. For mask
58, in lexicographic triangle order, the complete relation space is the
constant two-dimensional span

```text
(0,1,p-3),   (0,2,p-4).
```

Equivalently, exactly the remaining `q(p)-2` triangle coordinates are
independent in the mod-two quotient at all four tested parameters. The mask-56
relation space is all triangles for `p=8,9,10`; at `p=11` its only surviving
direction is `(2,3,4)`. No uniform mask-56 formula is inferred from that
threshold.

## 3. Independent audit

The auditor regenerates the triangle enumeration and exact labels in separate
code, replays the labelled component reconstruction, and reads the frozen
signed columns rather than a producer-emitted matrix. For each of 16
parameter/mask pairs, it enumerates every one of the at most `2^7` triangle
combinations and tests image membership with high-pivot reduction. The resulting
kernel basis agrees exactly with the producer's low-pivot basis.

It also verifies that the 19 labels are exactly those appearing in the frozen
EXP-062 `+/-2x_T` boundaries. Twelve adversarial controls check that duplicating
a triangle lowers the full-carrier rank, a nontriangle `R5` row is rejected by
the exact-label set, and a signed-entry mutation changes the frozen matrix
hash. The first audit attempt incorrectly required coefficient `+2` at odd
`p`; that pre-reconstruction failure is preserved, and the corrected audit
checks absolute coefficient two plus exact label.

## 4. What follows and what does not

The computation proves a finite labelled target bridge and exact mod-two
relation spaces. In particular, masks 59 and 62 carry `q` independent
order-two triangle images for the tested parameters, and these map to the full
isolated component's complete `(Z/2)^q` subgroup.

Vanishing in `coker(R_m mod 2)` does not by itself prove integral vanishing in
`coker_Z(R_m)`: an order-two element could be twice an order-four element.
Therefore the two mask-58 endpoint relations are candidates for the exact
relative kernel, not yet an integral kernel theorem. Nor does this finite
calculation prove survival for every `p`, exclude additional carrier torsion,
classify the complementary full cokernel, or establish a recurrence. The next
proof must construct uniform integral relative witnesses and transformed duals
for the two named endpoint triangles.
