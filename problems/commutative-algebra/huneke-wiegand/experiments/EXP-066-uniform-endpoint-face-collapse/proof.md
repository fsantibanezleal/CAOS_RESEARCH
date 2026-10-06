# EXP-066 proof: uniform endpoint face collapse

## Theorem

Let `p>=8`, `r in {1,2}`, and

```text
L_p     = [1,p] union [3p,4p-2],
E_{p,r} = (L_p minus {p-r,3p,3p+r}) union {6p,10p},
s_{p,r} = [S,E_{p,r};p-2].
```

Let `Pi_58` retain the full original target rows with semantic atoms
`R1,R3,R4,R5`. Then

```text
Pi_58 d(s_{p,r}) = -x_(0,r,p-2-r).
```

In particular, both endpoint triangle rows vanish integrally in the full
mask-58 semantic row projection for every `p>=8`.

## Proof

The first low interval contributes `p-1` elements to `E_{p,r}`, the second
contributes `p-3`, and the two high generators contribute two. Hence
`|E_{p,r}|=2p-2`.

Write `a=p-2` for the source coefficient and take exterior signs in increasing
generator order.

### First low interval

For `v in [1,p]`, multiplication by `a` gives an A row precisely when

```text
v+a>p, equivalently v>=3.
```

The source omits `p-r`, which lies in `[3,p]`. Consequently exactly `p-3`
first-interval deletions survive. Their faces contain `p-2` first-low,
`p-3` second-low, one H0 and one H2 generator. Subtracting the two baseline
counts `p,p` gives

```text
(-2,-3,1,0,1,0,0,0,0,0),
```

so every such row is `R0`.

### Second low interval

For `v in [3p,4p-2]`, multiplication by `a` gives a B row precisely when

```text
v+a>=4p-1, equivalently v>=3p+1.
```

The source already omits `3p`; all its remaining `p-3` second-interval
generators therefore survive except the separately omitted `3p+r`. After one
deletion the normalized face counts are

```text
(-1,-4,1,0,1,0,0,0,0,0),
```

so every such row is `R2`.

### High generators

Deleting `6p` would have coefficient offset `6p+a=7p-2`. This lies in the H0
degree-one interval `[6p,8p-2]`, not in the degree-two target basis, and gives
no boundary row.

Deleting `10p` gives coefficient offset `11p-2`, the upper endpoint of C2.
The remaining face has normalized counts

```text
(-1,-3,1,0,0,0,0,0,0,0),
```

and hence atom `R5`. Since `10p` is the final entry of a `2p-2` element
exterior set, its zero-based position is `2p-3`, which is odd. Its sign is
therefore `-1`.

The exact face is

```text
(L_p minus {p-r,3p,3p+r}) union {6p},
```

with coefficient `11p-2`. By the triangle-row definition this is exactly
`x_(0,r,p-2-r)`.

The complete nonzero boundary thus contains `p-3` rows of type `R0`, `p-3`
of type `R2`, and one negative `R5` endpoint row. Mask 58 removes `R0,R2`
and retains `R5`, proving the identity.

## Locked holdout and independent computation

The hypothesis was committed before the `p=11` holdout was opened. In the
frozen signed component, the semantic boundary conditions select unique source
columns:

| endpoint | component column | component row | retained entry |
|---|---:|---:|---:|
| `(0,1,8)` | 210 | 12559 | `-1` |
| `(0,2,7)` | 308 | 12560 | `-1` |

The source is recovered exactly from its R5 face: add the unique H2 generator
`10p` to the endpoint exterior; the R5 coefficient `11p-2` then forces source
coefficient `p-2`. This avoids a memory-expensive reconstruction of millions of
unrelated global rows.

The producer checked both endpoints for every `p=8,...,300` (586 identities)
and rejected 2,930 source/projection perturbations. The independent auditor
reimplemented the interval and atom classifications, traversed parameters in
reverse order, and reproduced the holdout columns. Its artifact status is
`INDEPENDENT_AUDIT_PASS`.

## Resource failures preserved

The first legacy labelled-component reconstruction stopped at the frozen 2 GiB
cap before classifying the holdout. A first unoptimized sweep was stopped after
`p=250` when quadratic face recounting exceeded the 120-second cap. Both partial
records are preserved. Replacing repeated recounting by a constant-time deletion
update completed the same frozen sweep in 5.5 seconds without changing the
formula.

## What could be wrong?

The theorem concerns the full original semantic row projection `Pi_58`. It does
not prove that the persistent isolated component is reconstructed uniformly for
all `p`, that projection commutes with every contraction outside the checked
parameters, or that the remaining triangle classes are independent or exhaustive
in the projected cokernel. The finite `p=11` carrier agreement closes the locked
holdout, not those all-parameter comparison obligations.
