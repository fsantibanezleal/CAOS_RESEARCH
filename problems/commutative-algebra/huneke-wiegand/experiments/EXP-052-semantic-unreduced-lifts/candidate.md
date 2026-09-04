# EXP-052 frozen candidate from training only

Date frozen: 2026-09-03. Training parameters: `p=8,9,10`. Holdout: `p=11`, not semantically
reconstructed before this candidate is committed.

Every row below has high selected variables `{6p,10p}`. Write `A(a,b;j)` for the `D:A` row
missing `a,b` from `L0`, missing `3p,3p+j` from `L1`, and with the displayed product. Write
`B(a;j,w)` analogously for the `D:B` row missing `a` from `L0` and `3p,3p+j,w` from `L1`.

## Candidate for `58->59`

The exact divided boundary is the following signed sum; an empty index interval contributes zero.

```text
sum_(r=0)^2 (-1)^(r+1) A(p-3,p-r;2),              product 2p-3-r
+ sum_(r=0)^2 sum_(a=r+1)^(p-4)
    (-1)^(p+a+r-1) A(a,p-r;2),                    product a+p-r
+ sum_(a=4)^(p-4) 2(-1)^(p+a) A(a,p-3;2),         product a+p-3

-2 A(p-2,p;1) +2 A(p-2,p-1;1)
+2 A(p-3,p;1) -2 A(p-3,p-1;1),                    product a+b-1
+ sum_(a=4)^(p-4) 2(-1)^(p+a) A(a,p-2;1),         product a+p-3
+ sum_(a=5)^(p-4) 2(-1)^(p+a+1) A(a,p-3;1),       product a+p-4.
```

The six families contain exactly `6p-30` distinct rows.

## Candidate for `58->62`

```text
sum_(w=3p+2)^(4p-2)
    2(-1)^(w-(3p+2)) B(p-2;1,w),                  product w+p-3
+ sum_(w=3p+3)^(4p-2)
    -(-1)^(w-(3p+3)) B(p-3;2,w),                  product w+p-3
+ sum_(w=3p+3)^(4p-2)
    2(-1)^(w-(3p+3)) B(p-3;1,w),                  product w+p-4
+ sum_(a=1)^(p-4) sum_(w=4p-a-1)^(4p-2)
    -(-1)^(w-(4p-a-1)) B(a;2,w),                  product w+a.
```

The four families contain exactly `binom(p,2)-5` distinct rows.

`candidate.py` is the executable statement. The training checker requires exact equality of the
complete coefficient-token multisets, not only equality of row counts. No all-parameter claim is
made before a symbolic incidence proof.
