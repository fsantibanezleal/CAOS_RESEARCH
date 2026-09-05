# EXP-062 proof: a quadratic family of independent two-torsion classes

Date: 2026-09-05. Scope: the full original integral presentation `M_p` of
EXP-036/054, for every integer `p>=8`. The family-to-presentation premise is
imported. The source and functional arguments below are symbolic; finite
audits are separate implementation and premise checks.

## 1. Notation and the theorem

Use the original low/high sets, multiplication rules, grading, and block map
of [EXP-061, Section 1](../EXP-061-uniform-parity-functional/proof.md):

```text
M(s,t)=(d_D s, d_K^S s+d_K^K t),
L=[1,p] union [3p,4p-2],
tau=sum(L)+10p-2.
```

All target and source labels below are original labels, not coordinates of a
reduced or isolated subpresentation. Put `n=p-2` and

```text
T_p={(i,j,k):0<=i<j<k, i+j+k=n}.
```

The signed integral target notation is

```text
e(r;u,v)=(-1)^(p+r+u+v)
 [K,(L minus {p-r,3p+u,3p+v}) union {6p};11p-2+u+v-r],
x_uv=e(u+v;u,v),  u<v.
```

For `T=(i,j,k)` choose `x_T=x_ij`. Its coefficient offset is `11p-2`,
and its first endpoint is `i+j<=p-2`. All these rows have the required
exterior cardinality and total offset.

We prove that the map

```text
(Z/2)^(q(p)) -> coker_Z(M_p),   basis_T -> [x_T],
q(p)=floor(((p-2)^2+3)/12),
```

is injective. Section 8 gives a further, nonconstructive splitting corollary;
neither conclusion describes the complete cokernel.

## 2. Explicit signed original sources for 2x_T

Use EXP-060's signed source operator `P` with exterior high set
`{6p,8p-2}`. To fix every sign, for potentials vanishing at `r<=u` it
has alpha source coefficient

```text
(-1)^(p+r+s+u)(f_u(s)-f_u(r)),
missing lows {p-r,p-s,3p+u},
coefficient offset p+u-r-s,
r<s, u<=r+s<=p+u-1,
```

and beta source coefficient

```text
(-1)^(p+r+u+v) beta_r,
missing lows {p-r,3p+u,3p+v}, coefficient offset 3p+u+v-r,
max(0,u+v-p+2)<=r<=min(p-1,u+v),
beta_r=F(r)-F(u+v+1) if u+v<=p-2, otherwise F(r),
F=f_u-f_v.
```

For distinct `u,a,b` with `a<b` and `u+a+b=n`, define the interval
potential `T_u(a,b)` by

```text
f_u(r)=1 on [u+a+1,u+b], all other values zero.
```

The interval is nonempty, is strictly above u, and ends at
`u+b=n-a<=p-2`. Its endpoints sum to `p+u-1`, so it is invariant under
`r -> p+u-1-r`. The complete face calculation of EXP-060 applies without
requiring any of `u,a,b` to be zero:

- Every D face cancels by the signed potential equations.
- Every `6p` face vanishes in the original coefficient module.
- A C0 face occurs only at a reflected pair and has coefficient proportional
  to `f_u(s)-f_u(r)`, hence vanishes.
- The remaining K boundary is the diagonal C2 difference
  `f_u(u+v+1)-f_u(u+v)`, with the oriented edge convention
  `y_uv=x_uv`, `y_vu=-x_uv` for `u<v`.

An interval has exactly two endpoint differences, so the exact full original
identity is

```text
M P(T_u(a,b))=y_ua-y_ub.
```

For `T=(i,j,k)` put

```text
F_T=T_i(j,k)-T_j(i,k)-T_k(i,j),
W_T=P(F_T).
```

Every source label is admissible by the operator bounds above. Linearity and
the displayed orientations give

```text
M W_T=(x_ij-x_ik)-(-x_ij-x_jk)-(-x_ik+x_jk)=2x_ij.
```

This proves P1 for every triangle and every `p>=8`, including triangles with
positive smallest entry. It is an integral identity with every original face
retained, not merely a mod-two cycle calculation.

## 3. Generic relative parity functionals and adjacency endpoints

Fix `T=(i,j,k)` and define over `F_2`

```text
z^T_uv=1 exactly when the unordered multiset {u,v,n-u-v} is T,
z^T_uv=0 otherwise.
```

Invalid indices and diagonals are zero. The only supported unordered pairs
are the three edges of T. Consequently

```text
z^T_uv=z^T_vu,       z^T_uv=z^T_u,n-u-v.
```

Define `lambda_T` on the whole original K target by assigning value `z^T_uv`
to `e(S;u,v)` and `e(S+1;u,v)`, where `S=u+v`. It is zero on other
rows of that C2 type. On a C0 row of coefficient `8p-1`, omitted lows
`{p-r,p-s,3p+u}`, and `r+s=p+u-1`, assign

```text
d^T_u(r)=z^T_u,r-u+z^T_u,r-u-1.
```

Set it to zero on all other target rows. Reflection gives
`d^T_u(r)=d^T_u(s)`, and at a reflected fixed point this value is zero.

For explicit support, each `u in T` has two other entries `v<w`. Its C0
pairs are

```text
(r,s;u)=(u+v,u+w+1;u),
        (u+v+1,u+w;u),
```

except that the second pair is omitted when `w=v+1`: it is a fixed point,
and its two contributions cancel in `F_2`. Each endpoint lies in
`0,...,p-1` because every pair sum is at most `n=p-2`. The first pair
always has distinct endpoints; the second does precisely when `w>=v+2`.
Rows arising from different u have different omitted second-low variables.

There are always six C2 support rows. Hence the complete functional support
has size

```text
12 - 1_{j=i+1} - 1_{k=j+1},
```

which ranges from ten to twelve. At `p=8`, triangle `(1,2,3)` has ten
rows. Treating every triangle as having twelve rows would be incorrect.
This formula also proves validity and distinctness, with no numerical count
assumption.

## 4. Every original K source is annihilated

The source classification of EXP-061, Section 3, depends on the original
presentation, not the selected triangle. For transparency, the functional
calculation in each case is reproduced here.

Sources with no exterior high, a sole high different from `6p`, or at least
two highs are invisible: low faces retain the wrong high set, while a K
high face has coefficient at least `12p`, above all supported offsets.
Only sources with exterior high `{6p}` remain; their low exterior omits two
elements.

- Two omitted first lows force coefficient below `6p`, so no original K
  source of this type exists.
- One omitted first endpoint r and second endpoint u gives
  `X(r,u)` with coefficient `8p-2+u-r`. Its admissible ranges are `r>=u`
  or `r<=u-2`. The latter range has no supported face. In the former,
  the C0 pairing is `d^T_u(r)` and the two possible C2 faces sum to the
  same value. A reflected fixed point is absent as an exterior face and
  has d value zero. Thus the total pairing vanishes.
- Two omitted second indices with sum S give coefficient `10p-2+S`,
  admissible only at `S=2` or `S>=p+1`. At `S=2`, the two supported
  first endpoints `2,3` have equal value `z^T_uv`, whether that value is
  zero or one. At `S>=p+1`, both endpoints are outside the first-index
  range. The total is again zero.

Thus `lambda_T d_K^K=0` for every triangle. Nothing in this calculation
requires an edge incident to second index zero.

## 5. Every complete D-cycle connecting image is annihilated

### 5.1 Exhaustive sectors and the unchanged complete-kernel theorem

The supported coefficient offsets remain exactly among
`8p-1,11p-2,11p-3`, so the full reachability calculation of EXP-061,
Section 4, applies. An S source can meet the functional only in exterior-high
sectors `{6p,h}` with

```text
h in [7p-1,8p-2] union {10p-3,10p-2,10p}.
```

In particular, `10p-3` remains included. The D differential preserves its
entire exterior-high set, so its complete kernel splits over these sectors;
all other sectors pair to zero term by term.

For `h=8p-d`, `2<=d<=p+1`, EXP-061, Section 5, proves the complete
kernel parametrization over `F_2`:

```text
alpha_u(r,s)=f_u(r)+f_u(s),
u+d-2<=r+s<=p+u+d-3,
f_u(r)=0 for r<u+d-2, f_u(0)=0;

beta_r(u,v)=F(r)+F(S+d-1) if S<=p-d, otherwise F(r),
F=f_u+f_v, S=u+v,
max(0,S+d-p)<=r<=min(p-1,S+d-2).
```

The proof exhausts all original source types, reconstructs alpha from the
A equations through first endpoint zero, and then uniquely reconstructs beta
from the B-star equations, including empty intervals and absent endpoints.
At `d=2`, `f_u(u)` is free for every `u>=1`. This completeness theorem
does not involve z or T and therefore applies unchanged.

The reconstruction's first-low endpoint zero must not be confused with a
second index in T. It is an available endpoint of the complete original
presentation even when `i>0`. No triangle-zero assumption enters the
complete-kernel theorem.

### 5.2 Generic C0/C2 cancellation

For an arbitrary potential collection in that complete kernel, reflection
and the fixed-point cancellation give C0 pairing

```text
sum_{u,r} f_u(r)d^T_u(r)
 = sum_{u<v} z^T_uv (F(S)+F(S+1)).                 (1)
```

Every supported pair has `S<=p-2`, since its third vertex is nonnegative.
Thus S and `S+1` are valid first indices. The C2 calculation is exactly:

- At `d=2`, only `r=S` is an admissible supported beta face, with value
  `F(S)+F(S+1)`.
- At `3<=d<=p`, both supported endpoints are admissible, and their beta
  constants cancel, giving `F(S)+F(S+1)`.
- At `d=p+1`, only `r=S+1` is admissible. The sole possible nonzero
  potential is `f_0(p-1)`, so `F(S)=0` on the supported pair sums. Its
  beta value `F(S+1)` is therefore the same required expression.

Consequently C2 pairing is also (1) and cancels C0 over `F_2`. This uses
only symmetry, reflection, and the pair-sum bound; it does not use any
particular vertex value. Unsupported original faces need not vanish, but
their functional values are zero.

### 5.3 The three large-high sectors, including S=1

For `h=10p-3` or `10p-2`, the relevant first-low-coefficient sources omit
one first endpoint r and two second endpoints of sum S. Their coefficient
offsets are `p+1+S-r` or `p+S-r`, respectively, forcing `r>=S+1` or
`r>=S`. Their endpoint-zero source is absent. The D:A star on `{0,r}`
therefore forces each coefficient to zero. Other admissible source families
have second-low coefficients and cannot contribute to a D:A row.

For `h=10p`, the first-low coefficient is `p-2+S-r`. When `S>=3`,
endpoint zero is again absent and the same star argument applies. It remains
to consider sums `S=1` and `S=2`, which can occur for a general triangle.
The relevant supported endpoints are S and `S+1`. Their D:A equation has
product offset

```text
2p-S-3,
```

which is strictly greater than p for both sums when `p>=8`. The equation
therefore forces the two source coefficients to sum to zero. Both sources
are admissible, and no second-low-coefficient source can enter this D:A row.
There is no supported C0 face in these large-high sectors.

This proves `lambda_T d_K^S(s)=0` for every complete original D cycle s.
The `S=1` argument is necessary for this generalization; the special
triangle of EXP-061 only required the `S=2` exception.

## 6. Diagonal detection and integral independence

An unordered edge `{a,b}` can belong to only one triangle of sum n: its
third vertex must be `n-a-b`. Hence distinct triangles have disjoint
unordered edge sets. For their chosen target classes,

```text
lambda_T(x_U)=delta_TU.
```

Suppose an integral combination `sum_U m_U x_U` were in the image of the
full original map. Reducing the source equation modulo two, its zero D
component places its S chain in the complete D kernel. Sections 4-5 then
show that each relative functional must evaluate to zero. The diagonal
pairing forces `m_T=0 mod 2` for every T.

Conversely, every even coefficient vector is an integral relation, because
Section 2 supplies `M W_T=2x_T`. The relation lattice among these chosen
classes is therefore exactly `2Z^{T_p}`. This proves the asserted injection
of `(Z/2)^{|T_p|}` into the full integral cokernel.

This is not a dimension inference from finite pairings: the disjoint-edge
argument and the complete relative-functional proof establish every pairing
and relation statement for all p.

## 7. Exact count and quadratic growth

Let q(n) count strictly increasing nonnegative triples of sum n. For `n>=6`,
triples whose smallest entry is at least two correspond bijectively to triples
of sum `n-6`, by subtracting two from every entry. Those with smallest entry
zero number `floor((n-1)/2)`. Those with smallest entry one number
`floor((n-2)/2)-1`. Their sum is `n-3`. Hence

```text
q(n)-q(n-6)=n-3.
```

The initial counts for `n=0,...,5` are `0,0,0,1,1,2`. The function
`floor((n^2+3)/12)` has exactly these initial values and the same recurrence,
because its unrounded arguments differ by the integer `n-3`. Therefore

```text
|T_p|=q(p-2)=floor(((p-2)^2+3)/12).
```

Thus the number of independent detected integral two-torsion classes is
quadratically unbounded. For example, the theorem gives 3, 4, 5, and 7 classes
at `p=8,9,10,11`, respectively. Agreement with earlier finite isolated ranks
does not identify that isolated object with this full cokernel or supply an
upper bound.

## 8. Deductive splitting corollary, without an explicit global retraction

The injection proved above in fact splits as a homomorphism of abelian groups.
This is a consequence of the established relative functionals, not an added
numerical prediction or a computed Smith normal form.

For each T define a functional on `im(d_D)` over `F_2` by

```text
mu_T(d_D s)=lambda_T(d_K^S s).
```

It is well-defined: two choices of s differ by a complete D cycle, annihilated
by Section 5. Extend this linear functional from the subspace `im(d_D)` to
the whole D target; finite-dimensional vector spaces admit such extensions.
The functional `(mu_T,lambda_T)` then annihilates the full original map,
because the two S contributions are equal and cancel over `F_2`, while
the K contribution is zero by Section 4.

Reduction modulo two followed by these extended functionals defines a group
map from the integral cokernel to `(Z/2)^{T_p}`. Its composition with the
injection of Section 6 is the identity, by the diagonal pairings. Hence the
detected subgroup is a direct summand. No explicit extension on every D row
or global retraction certificate is constructed here; the splitting assertion
is an existence corollary. It still does not count all torsion factors.

## 9. The original tracked class and the remaining boundary

EXP-060 gives exact target-vector identities

```text
eta=x_02+2x_01-2 M B-2 M D,
M P(F_1)=2x_01,
B=P(delta_03)-Q_3, D=P(delta_02)+Q_2.
```

Consequently the explicit source

```text
C=P(F_1-2delta_03-2delta_02)+2Q_3-2Q_2
```

satisfies `M C=eta-x_02`. Thus eta is integrally congruent to the class
chosen for triangle `{0,2,p-4}`. This is a quotient equality, not an
equality of original target vectors. EXP-057 transfers it, up to sign, to
`b_A+b_B`.

The theorem is a lower bound and the splitting corollary is a partial
decomposition. Neither gives the full cokernel, its free rank or odd torsion,
an identification with an isolated subpresentation or relative completion
quotient, or the lower-strand recurrence. The original coefficient model
remains an imported premise. All conclusions require the full-source and
complete-kernel proof above, not only a local dual or a finite matrix rank.
