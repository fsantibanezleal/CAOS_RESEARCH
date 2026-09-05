# EXP-061 proof: a twelve-row functional and a nonzero order-two class

Date: 2026-09-05. This is an all-parameter argument in the original integral
presentation of EXP-036/054. Its finite computational audit is a separate
verification gate, recorded in the verdict. No finite rank pattern is used to
infer any assertion below.

## 1. Original presentation and the claim

Fix an integer `p>=8`. Put

```text
L_A=[1,p], L_B=[3p,4p-2], L=L_A union L_B,
H=[6p,8p-2] union [8p,10p-2] union {10p}
  union [11p-1,12p-1] union [13p+1,14p-2]
  union [14p,15p-1] union {16p} union [17p-1,18p-1],
Q=[6p,24p-1] minus H,
tau=sum(L)+10p-2=4p^2+6p-1.
```

An original source label consists of an exterior subset of `L union H` of
cardinality `2p-2` and a coefficient offset making its total offset `tau`.
S sources have coefficient in `L`; K sources have coefficient in `H`. K target
labels have exterior cardinality `2p-3`, coefficient in `Q`, and the same total
offset. The remaining target labels are the D rows described by low products.

For completeness, the original multiplication rules used here are:

- A first-low coefficient times a first-low exterior variable gives a D:A row
  exactly when their sum exceeds `p`.
- A mixed first/second-low product gives a D:B row exactly when its sum is at
  least `4p-1`.
- A second-low times second-low product is zero.
- A product involving a high coefficient or high exterior variable gives a
  K row exactly when its sum belongs to `Q`.

The differential deletes one exterior variable, with its usual increasing
exterior sign. Over `F_2` these signs disappear. Write the full original map as

```text
M(s,t)=(d_D s, d_K^S s+d_K^K t),
```

where `s` is an S chain and `t` a K-source chain. In particular, K sources
have no D component. We shall construct a functional `lambda_K` on the entire
K target over `F_2` satisfying

```text
lambda_K(eta)=1,
lambda_K d_K^K=0,
lambda_K d_K^S(s)=0 whenever d_D s=0.
```

These statements suffice to prove eta is not in the image of the full map
over `F_2`; no explicit functional on all D rows is required.

## 2. The functional, its twelve rows, and reflection

Index first-low variables by `p-r`, `0<=r<=p-1`, and second-low variables
by `3p+u`, `0<=u<=p-2`. Put `k=p-4`. For any integer indices define

```text
z_uv=1 if the unordered multiset {u,v,p-2-u-v} is {0,2,k},
z_uv=0 otherwise.
```

Thus an invalid second index or a diagonal has value zero. This convention
extends the formula by zero outside the second-index range. The multiset has
three distinct elements for `p>=8`, and directly gives

```text
z_uv=z_vu,       z_uv=z_u,p-2-u-v.
```

Recall the signed integral K row convention of EXP-060:

```text
e(r;u,v)=(-1)^(p+r+u+v)
 [K,(L minus {p-r,3p+u,3p+v}) union {6p};11p-2+u+v-r],
u<v.
```

Its sign is immaterial over `F_2`. Put `S=u+v`. Give this row value `z_uv`
when `r=S` or `r=S+1`, and zero otherwise. The nonzero instances are exactly
the following six C2 rows:

| Second pair | First endpoints | Coefficient offsets |
|---|---|---|
| `(0,2)` | `2,3` | `11p-2,11p-3` |
| `(0,k)` | `p-4,p-3` | `11p-2,11p-3` |
| `(2,k)` | `p-2,p-1` | `11p-2,11p-3` |

A C0 row here means

```text
[K,(L minus {p-r,p-s,3p+u}) union {6p};8p-1],
r<s, r+s=p+u-1.
```

Give it value

```text
d_u(r)=z_u,r-u+z_u,r-u-1.
```

This is independent of which of `r,s` is used. Indeed set
`n=p-1-u` and `t=r-u`; then `s-u=n-t`, and the reflection identity for z
exchanges the two summands of `d_u(r)` and `d_u(s)`. If `r=s`, the two
summands coincide, so `d_u(r)=0`. Thus no nonexistent repeated exterior
variable is represented by a fixed reflection point.

The nonzero C0 rows are exactly

```text
(r,s;u)=(2,p-3;0), (3,p-4;0),
        (2,p-1;2), (3,p-2;2),
        (p-4,p-1;k), (p-3,p-2;k).
```

Set the functional to zero on every other original K row. All twelve listed
rows are valid and distinct: their first indices lie in `0,...,p-1`, their
second indices in `0,...,p-2`, and the six C0 pairs satisfy `r<s` even at
`p=8`. Their coefficient offsets belong to `Q`. The C0 omitted-low sum is
`4p+1`, which proves the target grading; the C2 labels have grading by their
displayed formula. Rows of the two types have different coefficient offsets.

The four-row integral target of EXP-057 is, in this notation,

```text
eta=-2e(3;0,2)-e(2;0,2)-2e(2;0,1)-2e(3;0,1).
```

Hence modulo two it is precisely `e(2;0,2)`, and
`lambda_K(eta)=z_02=1`.

## 3. Every original K-source boundary is annihilated

Classify a K source by its number of exterior high variables. With no high
variable, every face still has no high variable and is invisible. With two
or more high variables, a low face retains at least two highs; a high face
has coefficient at least `6p+6p=12p`. Neither can meet the support of
`lambda_K`, whose rows have one exterior high and coefficient at most
`11p-2`. With exactly one high different from `6p`, low faces retain the
wrong high and the high face has none. These cases are all invisible.

It remains to consider exterior high set `{6p}`. Its low exterior is `L`
minus two elements. If their sum is `m`, grading forces coefficient
`c=4p-2+m`. There are three exhaustive omitted-low types.

### 3.1 Two omitted first-low variables

For omitted endpoints `r<s`, the coefficient is `6p-2-r-s<6p`. It is not
in `H`, so no such original K source exists.

### 3.2 One omitted first-low and one omitted second-low variable

The source is

```text
X(r,u)=[K,(L minus {p-r,3p+u}) union {6p};8p-2+u-r].
```

Its coefficient ranges from `7p-1` to `9p-4`; the only gap in `H` within
this interval is `8p-1`. It is therefore admissible exactly when `r>=u`
or `r<=u-2`.

If `r<=u-2`, no supported C2 face can occur, because such a face would
require `r=u+v` or `u+v+1` with `v>=0`. No C0 face occurs either: its
other first endpoint would exceed `p-1`.

If `r>=u`, a C0 face has other first endpoint `s=p+u-1-r`, which lies
in `[u,p-1]`. When `s!=r` its functional value is `d_u(r)`. When `s=r`
the corresponding variable is absent from the exterior, but `d_u(r)=0`
by the fixed-point observation of Section 2.

The supported C2 faces remove second-low indices `v=r-u` or `r-u-1`.
Invalid indices and the already omitted index `v=u` contribute zero by the
definition of z. Their total functional value is again `d_u(r)`. The
high face has no high variable and is invisible. Thus the total pairing is
`d_u(r)+d_u(r)=0` in every admissible case.

### 3.3 Two omitted second-low variables

For indices `u<v`, put `S=u+v`. The forced coefficient is `10p-2+S`,
with `1<=S<=2p-5`. It belongs to `H` precisely when `S=2` or
`S>=p+1`. In the first case, the possible supported first-low faces have
endpoints `2` and `3`, are both present, and both have value `z_uv`; their
sum is zero. In the second case, neither endpoint `S` nor `S+1` is in
`0,...,p-1`, so the pairing is zero. Second-low faces and the high face
are invisible.

This exhausts every original K source and proves `lambda_K d_K^K=0`.

## 4. All potentially visible S sectors

An S source can reach the support of `lambda_K` only by deleting a high
variable. Its exterior high set must consequently be exactly `{6p,h}`,
with low coefficient `c`, and the removed high must satisfy `h=b-c` for
one of the supported coefficient offsets b. Direct intersection with `H`
gives the complete list:

| Target coefficient b | Coefficient c in `L_A` | Coefficient c in `L_B` |
|---|---|---|
| `8p-1` | `h in [7p-1,8p-2]` | no admissible high |
| `11p-2` | `h in {10p-2,10p}` | `h in [7p,8p-2]` |
| `11p-3` | `h in {10p-3,10p-2,10p}` | `h in [7p-1,8p-3]` |

The union is `[7p-1,8p-2] union {10p-3,10p-2,10p}`. In particular,
`10p-3` cannot be dropped: it reaches coefficient `11p-3` with first-low
coefficient `p`. It was added during independent paper preflight, before the
committed declaration and any numerical evaluation.

The D differential removes only low variables, so it preserves the complete
exterior-high set. Consequently its kernel is the direct sum of its kernels
in individual high-set sectors. Every other sector has zero K pairing term
by term. It remains to annihilate the complete D kernel in each listed sector.

## 5. The complete D kernel for h=8p-d, 2<=d<=p+1

This section proves completeness over `F_2`, not merely that a proposed
subfamily consists of cycles. It includes potentials excluded from the
restricted source construction of EXP-060.

### 5.1 Exhaustive source classification and D equations

The low exterior is `L` minus three variables. If their sum is m, the
coefficient is `m-4p+d-2`. Three omitted first-low variables give at most
`d-p-5<=-4`, so cannot occur. Three omitted second-low variables give at
least `5p+d+1>4p-2`, and cannot occur either. The other two cases are:

| Name | Omitted lows | Coefficient | Admissible indices |
|---|---|---|---|
| alpha | `p-r,p-s,3p+u`, `r<s` | `p+d-2+u-r-s` | `u+d-2<=r+s<=p+u+d-3` |
| beta | `p-r,3p+u,3p+v`, `u<v`, `S=u+v` | `3p+d-2+S-r` | `max(0,S+d-p)<=r<=min(p-1,S+d-2)` |

In the alpha type the coefficient is always below `3p`, even before imposing
admissibility, so a valid coefficient is first-low. In the beta type it is
always above p, so a valid coefficient is second-low. Thus the table exhausts
all original S sources in this high sector.

The complete D:A equations are

```text
alpha_u(r,s)+alpha_u(r,t)+alpha_u(s,t)=0,
r<s<t, u+d-2<=r+s+t<=p+u+d-3.
```

Their product offset is `2p+d-2+u-r-s-t`. The complete D:B equations are

```text
alpha_u(r,s)+alpha_v(r,s)+beta_r(u,v)+beta_s(u,v)=0,
r<s, u<v, max(0,S+d-p)<=r+s<=S+d-1.
```

Their product offset is `4p+d-2+S-r-s`. These ranges follow directly from
the first-low and mixed multiplication thresholds of Section 1. Missing or
inadmissible source terms in an equation are zero. No other D type occurs:
second-low times second-low vanishes, and the two remaining low-face types
give exactly the equations above.

### 5.2 A-vertex-zero reconstruction and its converse

For each u put `t_u=u+d-2`. Set `f_u(0)=0`; for `r>0` define
`f_u(r)=alpha_u(0,r)` if `r>=t_u`, and set it to zero otherwise.
The upper bound for the pair `(0,r)` is at least `p-1`, so this precisely
describes all such source coordinates. In particular,

```text
f_u(r)=0 for r<t_u,   f_u(0)=0.
```

For every admissible pair `0<r<s`, the A equation on endpoints `{0,r,s}`
is present and forces

```text
alpha_u(r,s)=f_u(r)+f_u(s).
```

Pairs containing zero have the same formula by definition. Conversely, every
potential collection with the displayed vanishing solves all A equations:
the potential terms cancel in pairs. A source pair below its lower bound has
both endpoints below `t_u` and thus both potentials zero; a pair above its
upper bound cannot occur inside an A equation whose triple sum obeys that
upper bound. This checks every truncated term.

At `d=2`, `t_u=u`. Hence `f_u(u)` is a genuine free coordinate for every
`u>=1`; only `f_0(0)` is removed by the vertex-zero convention. Setting all
these coordinates to zero would lose part of the complete kernel and is not
permitted in this argument.

### 5.3 B-star reconstruction, including empty intervals

Fix `u<v`, put `S=u+v` and `F=f_u+f_v`. The B upper bound satisfies
`S+d-1<=p+u+d-3` because `v<=p-2`. Thus both alpha terms may be replaced
by their potential differences, including their zero lower truncations. Every
B equation reduces to

```text
beta_r+F(r)=beta_s+F(s).
```

There are two exhaustive cases.

If `S<=p-d`, the beta interval is `0,...,b` with `b=S+d-2<=p-2`.
The B equation on `{0,b+1}` is present, while beta at `b+1` is absent.
It forces `beta_0=F(b+1)`. The equations on `{0,r}`, `1<=r<=b`, then
force uniquely

```text
beta_r=F(r)+F(S+d-1).
```

This formula also extends as zero to `r=b+1`. No endpoint of a B equation
exceeds `b+1`, so all remaining equations hold, including the boundary one.

If `S>=p-d+1`, put `a=S+d-p>=1`. The beta interval is `a,...,p-1`
if `a<=p-1`, and is empty otherwise. One has `a<=u+d-2=t_u`, so both
potentials vanish strictly below a. For each `r>=a`, the B-star equation
on `{0,r}` is present and has beta at zero absent. It forces uniquely

```text
beta_r=F(r).
```

This extends by zero below a. If `a>p-1`, both potentials are zero at every
available index and the empty beta interval satisfies all equations as well.
These observations also prove the converse for every B equation.

Every complete D cycle is therefore given uniquely by the stated free
potentials and these alpha/beta formulas. Reconstruction reads original
coordinates and uses no rank inference or division. The same formulas produce
a D cycle for every allowed potential collection. In particular, no extra
second-low-coefficient-only kernel has been overlooked.

## 6. Pairing every generalized potential cycle

Only the h face can pair nontrivially with the functional. The `6p` face is
zero in the original product module since `6p+L` is contained in `H`;
in any event it would retain h rather than the required exterior high `6p`.

A supported C0 face has coefficient `h+c=8p-1`, hence `c=d-1` and
`r+s=p+u-1`. This coefficient is first-low for every `2<=d<=p+1`.
For a reflected pair the contribution is `(f_u(r)+f_u(s))d_u(r)`.
Reflection gives the same d value at both endpoints. Every potentially
nonzero `f_u(r)` has `r>=t_u>=u`, so its reflected endpoint also lies in
`[u,p-1]`. Fixed points contribute zero. Summing over the distinct pairs
therefore gives the full C0 pairing

```text
sum_{u,r} f_u(r)d_u(r)
 = sum_{u<v} z_uv (F(u+v)+F(u+v+1)).                 (1)
```

The expansion is legitimate at all endpoints: on the support of z the sums
S are `2,p-4,p-2`, so both S and `S+1` lie in `0,...,p-1`.

For supported C2 faces, only beta endpoints `r=S` and `r=S+1` matter.
Their source coefficients are respectively `3p+d-2` and `3p+d-3`.
The three possible cases are as follows.

- If `d=2`, only `r=S` is admissible. On z's support `S<=p-2=p-d`,
  so its beta value is `F(S)+F(S+1)`.
- If `3<=d<=p`, both endpoints are admissible. Their beta constants, when
  present, cancel; if absent, the same conclusion holds directly. Their sum
  is `F(S)+F(S+1)`.
- If `d=p+1`, only `r=S+1` is admissible, with beta value `F(S+1)`.
  The only possible nonzero potential is `f_0(p-1)`. Since all supported
  S satisfy `S<=p-2`, one has `F(S)=0`, giving the same expression.

Thus the C2 pairing is also (1). The two contributions cancel over `F_2`.
All other original K faces have functional value zero by definition; no
assertion that those faces themselves vanish is required. This proves
`lambda_K d_K^S=0` on the complete D kernel of every sector
`h=8p-d`, `2<=d<=p+1`.

## 7. The three remaining high sectors

Take `h=10p-3,10p-2,10p`. Three omitted first-low variables or two omitted
first-low plus one second-low variable cannot give an admissible coefficient.
For the latter type even its largest omitted sum is `6p-3`, giving
coefficient at most `-2` at the smallest of these h values. The only sources
with a first-low coefficient therefore omit one first-low and two second-low
variables. Sources omitting three second-low variables, when admissible, have
second-low coefficients and make no D:A contribution.

Fix an omitted second pair `u<v`, with `S=u+v`, and call the coefficients
of the first-low source family `a_r`. The forced coefficient offsets and
their lower bounds are:

| High h | Coefficient offset | Lower endpoint bound |
|---|---|---|
| `10p-3` | `p+1+S-r` | `r>=S+1` |
| `10p-2` | `p+S-r` | `r>=S` |
| `10p` | `p-2+S-r` | `r>=max(0,S-2)` |

Whenever `a_r` exists with `r>0`, the exterior first-low variable p is
present. Its product with the first-low coefficient lies in `[p+1,2p]`
and gives a D:A row with first endpoints `{0,r}`. The only possible other
source contributing to this row is `a_0`; no second-low coefficient can
contribute to a D:A row.

For `h=10p-3` and `10p-2`, the endpoint-zero source is absent because
`S>=1`. Thus every `a_r` in these families is forced to zero by its A-star
equation. This includes the supported `r=S+1` face for `10p-3` and both
possible supported faces for `10p-2`.

For `h=10p`, the same argument forces all `a_r` to zero when `S>=3`.
Only z-supported second sums need further consideration: they are
`2,p-4,p-2`. The latter two are at least four for `p>=8`. For `S=2`,
the coefficient is `p-r`, and every `r=0,...,p-1` is admissible. The
D:A row on endpoints `{2,3}` has coefficient offset `2p-5>p` and forces

```text
a_2+a_3=0.
```

These are exactly the two possible supported C2 contributions in this case.
There is no C0 contribution in these large-high sectors. Consequently every
complete D cycle has zero pairing in all three sectors. Other source families
may enter D:B equations, but cannot alter any of the A constraints just used.

Together with Sections 4-6, this proves the required annihilation on every
original S chain with `d_D s=0`, not merely on a selected local span.

## 8. Nonvanishing in the full quotient and exact integral order

Suppose, for contradiction, that eta were an original boundary over `F_2`:

```text
eta=M(s,t).
```

Eta has zero D component, so `d_D s=0`. Section 3 gives
`lambda_K d_K^K t=0`; Sections 4-7 give `lambda_K d_K^S s=0`. Applying
the functional therefore yields

```text
1=lambda_K(eta)=lambda_K(d_K^S s+d_K^K t)=0,
```

a contradiction. Thus eta is nonzero in the cokernel of the full original
map over `F_2`. This relative-functional argument does not need an explicit
extension to D rows or any global matrix basis.

An integral source for eta would reduce to one over `F_2`, so its integral
cokernel class is nonzero. EXP-060 supplies the independently proved integral
identity `M V_p=2eta_p`. Combining nonvanishing and annihilation proves:

```text
For every integer p>=8, [eta_p] has exact order two in coker_Z(M).
```

EXP-057's corrected original identity is `M(s+q)=b_A+b_B+eta`. Hence
`[b_A+b_B]=-[eta]` in the same integral cokernel, and this tracked class
also has exact order two for every `p>=8`.

## 9. Scope and independent verification

The all-parameter proof rests on the explicit original presentation,
exhaustive source classification, complete potential reconstruction, and
relative-functional contradiction. The finite audit must challenge these
formulas using independently enumerated original columns and D kernels; it
does not substitute rank samples for the completeness proof.

This establishes one nonzero order-two class. It does not prove a second
independent class, characterize the whole cokernel or connecting quotient,
bound that quotient from above, or prove a recurrence. Nor does it reopen
priority for the already-disproved broad Huneke-Wiegand statement or resolve
a Jacobian-conjecture question. The original coefficient model remains an
explicit imported premise, rather than something proved by agreement among
implementations of its differential.
