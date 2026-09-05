# EXP-059 proof: an integral potential basis and a seven-row connecting image

Date: 2026-09-05. Scope: every integer `p>=8`, and only the original S-source sector
whose exterior high set is exactly `{6p,8p-4}`. The following is a symbolic derivation;
its finite independent checks are recorded separately in the artifact and verdict.

## 1. Exhaustion of original source labels

Write `L=[1,p] union [3p,4p-2]`, `N=|L|=2p-1`, and `h=8p-4`.
The original source has exterior cardinality `2p-2=N-1` and total offset
`4p^2+6p-1=sum(L)+10p-2`. With the two fixed high variables, its low exterior is
`L` minus three elements. If their sum is `m`, the coefficient offset is

```text
c=m-4p+2.
```

Index first-low variables by `p-r`, `0<=r<=p-1`, and second-low variables by
`3p+u`, `0<=u<=p-2`. Three omitted first-low variables give `c<1`; three omitted
second-low variables give `c>4p-2`. Neither is an original S source. The remaining
possibilities are precisely:

| Missing low variables | Coefficient offset | Admissibility |
|---|---|---|
| `p-r,p-s,3p+u`, `r<s` | `p+2+u-r-s` | `u+2<=r+s<=p+u+1` |
| `p-r,3p+u,3p+v`, `u<v` | `3p+2+u+v-r` | `max(0,u+v-p+4)<=r<=min(p-1,u+v+2)` |

In the first row the coefficient cannot be second-low; in the second it cannot be
first-low. These inequalities therefore exhaust, rather than select from, the sector.
Every displayed label automatically has the original exterior degree and total offset.

## 2. Orientation and the complete D equations

Use increasing endpoint order on the first-low indices, followed by increasing
second-low indices. This reverses the order of the actual first-low variables.
For a low exterior set `E`, send its increasing wedge to its omitted-variable wedge
with the sign of the permutation `(E,L minus E)`. Then reorder the omitted first-low
variables into endpoint order. For a missing triple the resulting source sign is

```text
(-1)^(p+r+s+u) for the first row of the table,
(-1)^(p+r+u+v) for the second row of the table.
```

Indeed the unreordered complement sign for a missing `k`-subset with zero-based
positions `d_i` is `(-1)^(k(N-1)-sum(d_i)-k(k-1)/2)`. Substitution for `k=3`,
including the transposition of two omitted first-low variables where applicable,
gives the two formulas above. Complementing contraction gives wedge insertion,
with common sign `(-1)^(|E|-1)=-1` here. Thus write `alpha_u(r,s)` and
`beta_r(u,v)` for the signed, normalized source coefficients in the two rows.

The complete A equations, for omitted first endpoints `r<s<t` and second endpoint
`u`, are, up to a common unit sign,

```text
alpha_u(r,s)-alpha_u(r,t)+alpha_u(s,t)=0.
```

They occur when `u+2<=r+s+t<=p+u+1`. Coefficients for inadmissible source pairs
are interpreted as zero. The complete B equations, for omitted first endpoints
`r<s` and second endpoints `u<v`, are

```text
alpha_u(r,s)-alpha_v(r,s)+beta_r(u,v)-beta_s(u,v)=0.
```

They occur when `max(0,u+v-p+4)<=r+s<=u+v+3`. These are all possible low
faces: first-low coefficients times first-low variables produce A; the two mixed
products produce B; second-low times second-low vanishes. In particular, there are
no additional D equations with three omitted second-low variables.

## 3. Integral reconstruction from vertex zero

Fix `u`. Put `f_u(0)=0`, set `f_u(r)=0` for `r<=u+1`, and for `r>=u+2`
define `f_u(r)=alpha_u(0,r)`. For every admissible pair `0<r<s`, the A equation
on `{0,r,s}` is present and gives

```text
alpha_u(r,s)=f_u(s)-f_u(r).
```

The same formula holds for pairs containing zero. If an omitted pair has sum below
`u+2`, both potentials are zero. If its sum exceeds `p+u+1`, that pair does not
occur in any A equation. It follows that every A-kernel element has this form and,
conversely, every such potential solves all A equations. No division is used.

Now fix `u<v`, put `R=u+v` and `F=f_u-f_v`. In a B equation its upper bound
`r+s<=R+3` implies `r+s<=p+u+1` because `v<=p-2`; hence the alpha terms are
exactly their potential differences, with zero below their lower admissibility
bound. The B equation reduces to

```text
beta_r-F(r)=beta_s-F(s).
```

There are two cases.

* If `R<=p-4`, the beta indices are `0,...,R+2`. The equation on endpoints
  `{0,R+3}` has beta at `R+3` absent, so it forces `beta_0=-F(R+3)`.
  The equations on `{0,r}` then give `beta_r=F(r)-F(R+3)` throughout the
  admissible interval. Every remaining equation is the difference of two such
  identities.
* If `R>=p-3`, put `a=R-p+4>=1`. The beta indices are `a,...,p-1`.
  Since `a<=u+2`, both potentials vanish below `a`. The equations on `{0,r}`,
  for every `r>=a`, give `beta_r=F(r)`. The other equations hold because this
  formula also extends by zero below `a`.

Thus beta is uniquely determined over the integers by the frozen formula. In
particular, when all alpha coefficients vanish, all beta coefficients vanish;
the second-low-coefficient-only D map is injective in this entire fixed-high
sector, not merely on a selected endpoint subset.

The free potentials are exactly `(u,r)` with `0<=u<=p-3` and `u+2<=r<=p-1`.
Their number is `sum_{u=0}^{p-3}(p-u-2)=binom(p-1,2)`. The unit potentials
therefore form an integral basis of the full D kernel in this sector. The inverse
map reads the distinguished alpha coordinate `(0,r,u)`, so the reconstruction is
integral and unique, with an identity coordinate minor. A rational-rank equality
or a finite scan is not being used to infer this lattice statement.

## 4. Height and support of one basis chain

For a unit potential at `(u0,r0)`, alpha is nonzero only for `u=u0` and pairs
containing `r0`; there are at most `p-1` such pairs. Each nonzero alpha is a unit.
Beta is nonzero only on second pairs containing `u0`. Usually it has at most one
nonzero index, namely `r0`. There is at most one exceptional second partner,
specified by `u+v=r0-3`, for which beta is a constant unit on `0,...,r0-1`.
There are `p-2` possible partners and at most `p-1` terms in that exceptional
interval. Consequently beta has at most `(p-3)+(p-1)=2p-4` terms, and the full
source has height one and support at most `3p-5`. The alpha and beta source
families are disjoint, so no unaccounted coefficient addition occurs.

## 5. Complete original K boundary

The two high variables follow `2p-4` low variables. Removing `6p` has positive
sign and removing `h=8p-4` has negative sign. Every `6p` face vanishes:

```text
6p+[1,p] lies in H0,
6p+[3p,4p-2] lies in H1.
```

For an alpha source the other product is `8p-4+c`, with `1<=c<=p`.
Only `c=3` survives, giving the C0 offset `8p-1`; `c=1,2` lies in H0 and
`4<=c<=p` lies in H1. For a beta source the other product is `11p-4+t`,
where its coefficient is `3p+t`, `0<=t<=p-2`. Only `t=0,1,2` survives,
giving the C2 offsets `11p-4,11p-3,11p-2`; the remaining offsets lie in H3.
Every surviving K coefficient is the negative of its actual source coefficient.
This proves the complete original-map formula in P3, including the absence of
any extra high-free or different-high rows.

For a unit potential, an alpha face survives only when its partner is
`s=p+u0-1-r0`, giving at most one C0 row. A non-exceptional beta face survives
only for second partners `r0-u0`, `r0-u0-1`, or `r0-u0-2`, giving at most
one row each. The exceptional partner `r0-u0-3` gives at most three rows,
at first endpoints `u+v,u+v+1,u+v+2`. Invalid, repeated, or out-of-range
partners are simply absent. Hence the full original boundary has at most seven
distinct rows: one C0 and six C2.

## 6. Scope and remaining gates

This supplies an exact, all-parameter D-cycle basis and a sparse connecting image
for one specified high pair. It does not prove that this sector controls the full
original presentation. In particular, neither `2eta` being a boundary nor eta
being nonzero in the integral cokernel follows from this parametrization. The
second class and a uniform upper bound are still separate obligations.

The independent artifact must attack signs, grading, all original faces, recovery
coordinates, and deliberate mutations. Such finite checks do not replace the
reconstruction proof above. Residual risks include an incorrect imported original
coefficient module or a mistake in the written exhaustion or orientation argument.
The stronger manuscript and Zenodo theorem gate is not bypassed by the reduced
support size alone.
