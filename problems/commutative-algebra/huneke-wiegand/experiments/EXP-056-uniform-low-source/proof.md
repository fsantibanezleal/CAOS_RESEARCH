# EXP-056 proof record: a uniform low-source identity

Date: 2026-09-04. Scope: every integer `p>=8`. This record proves the algebraic identities in
P1 and P2 from the original coefficient module and signed differential. P3 is the separate
adversarial check recorded in [verdict.md](verdict.md) and `artifacts/results.json`.

## 1. Objects, grading, and the claimed identity

Put

$$L_p=[1,p]\mathbin{\cup}[3p,4p-2],\qquad
H_p=\{g\in G_p:g\ge6p\},\qquad
B_p=[6p,24p-1]\setminus H_p.$$

The interval description of `H_p` and the original differential are those of
[EXP-036](../EXP-036-factor-two-torsion-anatomy/run.py) and
[EXP-037](../EXP-037-connecting-quasipolynomial/run.py). In particular, low-low products are

$$u\cdot v=\begin{cases}
A_{u+v},&u,v\in[1,p],\ u+v>p,\\
B_{u+v},&\text{exactly one of }u,v\text{ is in }[3p,4p-2],\ u+v\ge4p-1,\\
0,&\text{otherwise}.
\end{cases}$$

Here `A` and `B` denote the two coefficient types in the `D` target, while `B_p` is the set
of degree-two offsets in the `K` target. A high-low or high-high product contributes to a `K`
row exactly when its offset sum lies in `B_p`. Removing the variable in zero-based position
`r` from an increasing exterior set has coefficient `(-1)^r`.

Define

$$T_p(a,j)=[S,(L_p\setminus\{a,3p,3p+j\})\cup\{6p,10p\};a+j-2].$$

Only the following weights are nonzero:

| `j` | `a` | `w_j(a)` |
|---:|---|---|
| 2 | `1<=a<=p-4` | `(-1)^(a+1)` |
| 2 | `a=p-3` | `(-1)^(p+1)` |
| 1 | `a=p-2` | `2(-1)^(p+1)` |
| 1 | `a=p-3` | `2(-1)^p` |

Let

$$s_p=\sum_{j=1}^2\sum_{a=1}^p w_j(a)T_p(a,j).$$

Every coefficient offset `a+j-2` in this sum lies in `[1,p-3]`, so every term is an admissible
low-source label. There are exactly `(p-4)+3=p-1` distinct terms, with coefficients of
absolute value at most two.

The exterior cardinality is `2p-2`. Since

$$\sum_{u\in L_p}u=4p^2-4p+1,$$

each source term has total offset

$$\sum_{u\in L_p}u-(a+6p+j)+16p+(a+j-2)=4p^2+6p-1.$$

Thus `s_p` belongs to the original `(p,2)` source block: its exterior degree is `i+1=2p-2`,
its coefficient has internal degree one, and its total internal degree is `2p-1`. All boundary
terms have exterior degree `i=2p-3`, coefficient degree two, and the same total offset.

Write `b_p^A` and `b_p^B` for the two disjoint `D`-row formulas frozen by
[EXP-052](../EXP-052-semantic-unreduced-lifts/candidate.md). The claim is

$$M_ps_p=b_p^A+b_p^B+\gamma_p,$$

where

$$\gamma_p=-\sum_{j=1}^2\sum_{a=1}^p w_j(a)
[K,(L_p\setminus\{a,3p,3p+j\})\cup\{6p\};10p+a+j-2].$$

The proof below collects every possible original boundary row. It does not identify a frozen
coordinate projection with an original-chain inclusion.

## 2. Complete `A`-row calculation

For `a<b`, denote the row

$$\mathsf A(a,b;j)=
[D,(L_p\setminus\{a,b,3p,3p+j\})\cup\{6p,10p\};A,a+b+j-2].$$

It can receive a contribution from precisely `T_p(a,j)` and `T_p(b,j)`. In the first exterior
set, `b` has position `b-2`; in the second, `a` has position `a-1`. Therefore its collected
coefficient is

$$C_j(a,b)=(-1)^b w_j(a)+(-1)^{a-1}w_j(b),$$

provided `a+b+j-2>p`; if this strict inequality fails, the product is zero.

For `j=2`, two ordinary indices `a<b<=p-4` cancel because

$$(-1)^b(-1)^{a+1}+(-1)^{a-1}(-1)^{b+1}=0.$$

The exceptional weight at `p-3` instead produces

$$C_2(a,p-3)=2(-1)^{p+a}\quad(1\le a\le p-4).$$

Its product survives exactly when `a>=4`. The last three indices have zero source weights,
so they contribute only through the other endpoint. These observations give the complete
nonzero `j=2` list in the first three rows of the following table.

For `j=1`, only `p-3` and `p-2` carry weights. Their mutual pair cancels. Pairing either with
an earlier index gives the lower cutoffs `a>=5` and `a>=4`, respectively. Pairing with `p-1`
or `p` gives the four endpoint entries. The resulting complete list is:

| Family | Index range | Row coefficient | Why the product survives |
|---|---|---|---|
| `A(p-3,p-r;2)` | `r=0,1,2` | `(-1)^(r+1)` | `2p-r-3>p` |
| `A(a,p-r;2)` | `r=0,1,2`, `r+1<=a<=p-4` | `(-1)^(p+a+r-1)` | `a>r` |
| `A(a,p-3;2)` | `4<=a<=p-4` | `2(-1)^(p+a)` | `a>3` |
| `A(p-2,p;1)` | one row | `-2` | `2p-3>p` |
| `A(p-2,p-1;1)` | one row | `2` | `2p-4>p` |
| `A(p-3,p;1)` | one row | `2` | `2p-4>p` |
| `A(p-3,p-1;1)` | one row | `-2` | `2p-5>p` |
| `A(a,p-2;1)` | `4<=a<=p-4` | `2(-1)^(p+a)` | `a>3` |
| `A(a,p-3;1)` | `5<=a<=p-4` | `2(-1)^(p+a+1)` | `a>4` |

Empty ranges contribute nothing, including the last range at `p=8`. Every pair omitted from
the table either has both weights zero, has the cancellation just exhibited, or fails the
product inequality. This is exactly the six-family `b_p^A` formula of EXP-052, with its finite
endpoint families displayed separately. Its disjoint nonzero rows number

$$3+(3p-15)+(p-7)+4+(p-7)+(p-8)=6p-30.$$

## 3. Complete `B`-row calculation

Let `v` be a second-low variable present in `T_p(a,j)`, and denote the resulting row by

$$\mathsf B(a;j,v)=
[D,(L_p\setminus\{a,3p,3p+j,v\})\cup\{6p,10p\};B,v+a+j-2].$$

There are `p-1` first-low variables before `v`. Among the second-low variables below it,
`3p` is omitted and `3p+j` is omitted precisely when `v>3p+j`. The zero-based position of `v`
is consequently

$$v-2p-2-\mathbf1_{v>3p+j}.$$

For `v>3p+j` its sign is `(-1)^(v+1)`. The only possible present variable below `3p+j`
occurs when `j=2` and `v=3p+1`. Its product is always zero: the source coefficient is at most
`p-3`, so its total offset is at most `4p-2`, below the `B` threshold `4p-1`.

Thus every surviving contribution has coefficient `(-1)^(v+1)w_j(a)` and satisfies
`v+a+j-2>=4p-1`. Substitution gives precisely the following four families:

| Family | Index range | Product offset | Row coefficient |
|---|---|---|---|
| `B(p-2;1,v)` | `3p+2<=v<=4p-2` | `v+p-3` | `2(-1)^(v-(3p+2))` |
| `B(p-3;2,v)` | `3p+3<=v<=4p-2` | `v+p-3` | `-(-1)^(v-(3p+3))` |
| `B(p-3;1,v)` | `3p+3<=v<=4p-2` | `v+p-4` | `2(-1)^(v-(3p+3))` |
| `B(a;2,v)` | `1<=a<=p-4`, `4p-a-1<=v<=4p-2` | `v+a` | `-(-1)^(v-(4p-a-1))` |

For the second row, the threshold permits `v=3p+2`, but this is the omitted variable and
therefore not a face. The other lower bounds follow directly from the threshold. The possible
overlap between `j=1` and `j=2` faces would require the already excluded `j=2, v=3p+1` face,
so the displayed nonzero rows are distinct. These are exactly the four families of `b_p^B`.
Their total support is

$$ (p-3)+(p-4)+(p-4)+\sum_{a=1}^{p-4}a
=\binom p2-5.$$

All low faces have now been accounted for. Therefore the `D` component of `M_ps_p` is
`b_p^A+b_p^B`, proving P1 for every `p>=8`.

## 4. The signed `K` residual

The exterior set of each `T_p(a,j)` contains exactly two high variables, `6p` and `10p`,
after `2p-4` low variables. Removing `6p` has positive sign, but its product offset satisfies

$$6p+(a+j-2)\in[6p+1,7p-3]\subset H_p,$$

so it is zero in the degree-two layer `B_p`. Removing `10p` has position `2p-3` and sign
minus. Its product offset satisfies

$$10p+(a+j-2)\in[10p+1,11p-3]\subset B_p.$$

It therefore contributes exactly the corresponding term in `gamma_p`. There are no other high
faces, proving P2. These `p-1` `K` rows are distinct, so `gamma_p` has support exactly `p-1`,
again with coefficients of absolute value at most two.

The total offset of each such row is explicitly

$$\sum_{u\in L_p}u-(a+6p+j)+6p+(10p+a+j-2)=4p^2+6p-1,$$

which also checks the grading without appealing to the source identity.

## 5. Integral cokernel transfer and the remaining problem

The identity is over the integers, in the full original presentation. Consequently,

$$[b_p^A+b_p^B]=-[\gamma_p]\quad\text{in }\operatorname{coker}_{\mathbb Z}M_p.$$

No division or field reduction is used in this conclusion. It replaces a quadratic-size
displayed representative by an explicitly defined `p-1`-row representative of the same class,
up to sign.

Conditionally, suppose an exact source `z_p^{corr}` is known to satisfy
`M_p z_p^{corr}=2(b_p^A+b_p^B)`. Then

$$M_p(2s_p-z_p^{corr})=2\gamma_p.$$

Equivalently, `z_p^{corr}-2s_p` has boundary `-2gamma_p`. This subtraction is valid for any
parameter where the premise is established. A finite source witness from EXP-055 does not make
that premise uniform. The displayed source `s_p` is not itself asserted to be a cycle; its
nonzero `D` boundary is essential to the transfer.

The new all-parameter target is therefore concrete: prove that `gamma_p` is nonzero in the full
cokernel and construct an original source with boundary `2gamma_p`. A second independent class
and a torsion upper bound are further, separate obligations. None is implied by the identity
proved here. In particular, this record does not claim an all-parameter order-two class, a
completed connecting quotient, or a solution of the lower-strand problem.

## 6. Validation boundary and publication decision

The proof uses the full coefficient and sign rules, not a projected HNF basis. Every possible
low and high face is covered by the tables and interval exclusions above. P3 is reserved for
comparison against the saved training sources, independent exact arithmetic at new parameters,
and intentional sign-corruption controls. Those results are recorded in the artifact and
verdict, rather than being assumed by the symbolic proof.

The standard signed-chain viewpoint is compatible with the explicit chain-map discipline in
[Skoldberg, Sections 2-3](https://arxiv.org/html/1311.5803v1). The specific identity in this record
is derived directly; no result from that source supplies the missing nonzero class or torsion
upper bound.

A possible failure would be an error in the imported original coefficient module or in the
exhaustive sign and truncation calculation. The independent P3 audit is designed to attack the
latter. Finite tests cannot replace the all-parameter calculation, and successful tests cannot
extend the claim beyond the identity and cokernel transfer. Publication remains subject to the
problem's stronger manuscript split gate; this identity alone does not automatically open a
new manuscript or Zenodo version.
