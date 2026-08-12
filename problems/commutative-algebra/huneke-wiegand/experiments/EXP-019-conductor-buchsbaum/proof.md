# EXP-019 - symbolic proof

Fix `p>=4`, put `s=6p`, and retain the EXP-013--018 notation. In particular,

```text
H={2p-1,4p-1} union [4p+1,5p-2],  |H|=p,
G=gr_T(R),
M=(m/T) direct-sum G_+.
```

All ideals below are monomial ideals in the numerical-semigroup ring, so their value sets give
monomial bases for the finite quotients and membership in a colon can be checked term by term.

## 1. Zeroth local cohomology as a colon saturation

Let `a+T^(n+1)` be homogeneous of degree `n` in `G`. It is killed by `G_+^k` exactly when

```text
aT^k subset T^(n+k+1).
```

Consequently

```text
H^0_(G_+)(G)_n
 = union_(k>=1) (((T^(n+k+1):T^k) intersect T^n)/T^(n+1)).
```

The degree-zero maximal ideal `m/T` of the Artinian ring `G_0=R/T` is nilpotent. Hence an element
is killed by a power of `G_+` if and only if it is killed by a power of the full homogeneous
maximal ideal `M`. Thus `H^0_M(G)=H^0_(G_+)(G)`.

EXP-017 proves

```text
v(T^k)=[4ks,infinity) for every k>=4.
```

For any `k>=4`, the monomial `t^v` therefore satisfies

```text
t^vT^k subset T^(n+k+1)
  iff v+4ks >= 4(n+k+1)s
  iff v >= 4(n+1)s.
```

If a class is killed for some smaller power, multiplying the containment by a further power of
`T` makes it killed for a power at least four. Conversely, the threshold itself gives a killing
power. Therefore the union of colons is exactly the stable-tail threshold `v>=4(n+1)s`.

## 2. The complete torsion module

The exact EXP-013 profiles show

```text
v(R) minus v(T) = {0} union (5s+H).
```

The threshold in degree zero is `4s`, so it deletes the unit class and retains exactly `5s+H`.
Thus

```text
H^0_M(G)_0 = span_k{t^(5s+h)+T : h in H} isomorphic to k^p.
```

There is no torsion in positive degree. Indeed:

- `v(T)` and `v(T^2)` agree from `8s` onward;
- `v(T^2)` and `v(T^3)` agree from `12s` onward;
- `v(T^3)` and `v(T^4)` agree from `16s` onward;
- `T^(n+1)=t^(4s)T^n` for every `n>=4`, so `v(T^n)` and `v(T^(n+1))` agree from
  `4(n+1)s` onward.

These are exactly the thresholds in degrees `1,2,3`, and `n>=4`. Hence

```text
H^0_M(G)=H^0_M(G)_0 isomorphic to k^p.
```

The EXP-018 Valabrega--Valla kernel is therefore not merely contained in the graded torsion: it is
the complete torsion module.

## 3. The full homogeneous maximal ideal annihilates the torsion

Take `r=5s+h` with `h in H`. Every positive value in `R` is at least `4s`, so every product of
`t^r` with `m` or `T` has value at least `9s`. Both `T` and `T^2` contain every value from `9s`
onward except `13s-1`.

That exceptional value cannot occur in either product. If `r+a=13s-1`, then

```text
a=8s-1-h,
```

which lies strictly between `7s` and `8s`; the exact ring profile has no values in that level.
Therefore

```text
t^r m subset T,
t^r T subset T^2.
```

The first containment says that the degree-zero part `m/T` kills the class of `t^r`; the second
says that `G_+` kills it. Thus

```text
M H^0_M(G)=0.
```

This checks the complete homogeneous maximal ideal, not only the positive graded part.

## 4. Buchsbaumness, invariant, and Cohen--Macaulay quotient

A one-dimensional Noetherian graded-local ring is Buchsbaum exactly when its homogeneous maximal
ideal annihilates its zeroth local cohomology. This is the dimension-one local-cohomology
criterion used in M. D'Anna, M. Mezzasalma, and V. Micale, *On the Buchsbaumness of the Associated
Graded Ring of a One-Dimensional Local Ring*, Communications in Algebra 37 (2009), 1594--1603,
`https://doi.org/10.1080/00927870802116521`; see also M. D'Anna, V. Micale, and A. Sammartano,
*On the associated graded ring of a semigroup ring*, Journal of Commutative Algebra 3 (2011),
147--168, `https://doi.org/10.1216/JCA-2011-3-2-147`.

Section 3 proves the criterion here. Therefore `G` is Buchsbaum. EXP-018 already proves
`depth(G)=0`, so it is not Cohen--Macaulay. In dimension one the Buchsbaum invariant is

```text
I(G)=length(H^0_M(G))=p.
```

It is unbounded across the family.

Finally, quotienting by the complete zeroth local cohomology leaves a one-dimensional ring with
positive depth, hence a Cohen--Macaulay ring. EXP-018 gives

```text
H_G(z)=((p+1)+(9p-1)z+12p z^2+(2p-1)z^3+z^4)/(1-z).
```

The torsion has Hilbert series `p` in degree zero. Subtraction yields

```text
H_(G/H^0_M(G))(z)
 = (1+(10p-1)z+12p z^2+(2p-1)z^3+z^4)/(1-z).
```

The proof is deductive for every `p>=4`. The finite campaign and independent audit support the
value-set implementation; they do not replace the infinite-family argument.
