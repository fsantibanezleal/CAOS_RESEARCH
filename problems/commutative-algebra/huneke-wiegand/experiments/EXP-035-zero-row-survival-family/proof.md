# EXP-035 proof - zero-row summands and a characteristic-dependent lower Betti cell

## Theorem

Retain the EXP-034 notation over an arbitrary field. Let

```text
G_p^+=G_p minus {0},          n=|G_p^+|=10p-1,
R_b={g in G_p^+:b-g in H_p}, b in B_p.
```

For `F subset G_p^+`, write `[b,F]=e_F tensor v_b` for the corresponding codomain coordinate of
the two-layer incidence map. Then:

1. `[b,F]` is an integral zero row if and only if `R_b subset F`. These coordinates split off a
   primitive free summand of the regularity-two cokernel of `K_p`, of rank

   ```text
   z_(p,i)=sum_(b in B_p, |R_b|<=i) binom(10p-1-|R_b|,i-|R_b|)    (1)
   ```

   in homological degree `i`.

2. For every `2<=t<=p-2`, put

   ```text
   b_(p,t)=10p+t,
   F_(p,t)=[3p,4p-2] union {t} union [t+2,p].                    (2)
   ```

   Then

   ```text
   R_(b_(p,t))=F_(p,t),
   |F_(p,t)|=2p-t-1,
   b_(p,t)+sum F_(p,t)=4p^2+6p-t(t-1)/2.                       (3)
   ```

   Hence `K_p` has a primitive zero-coordinate class in each homological degree
   `p+1,...,2p-3`, in addition to the EXP-034 class at degree `p`. This is a direct-summand lower
   bound, not a complete cokernel calculation.

3. At the first new cell, `(p,t)=(4,2)`, put

   ```text
   b=42, F={2,4,12,13,14}, i=5, tau=87.                         (4)
   ```

   The exact multigraded Betti numbers are

   ```text
   beta_(5,(7,87))(K_4)=5 over GF(2),  4 over GF(3),
   beta_(5,(7,87))(A_4)=4 over GF(2),  3 over GF(3),
   beta_(5,(7,87))(C_4)=4 over GF(2),  3 over GF(3).            (5)
   ```

   Thus the lower multigraded Betti tables of `K_4`, `A_4`, and `C_4` depend on the
   characteristic. Integrally, the selected cokernel of `K_4` is

   ```text
   Z^4 direct-sum Z/2Z.                                        (6)
   ```

The theorem does not determine either complete lower strand, and it does not assert that every
cell in (2) survives the connecting map.

## 1. Complete zero-row classification

The EXP-034 differential is

```text
delta_(i+1)(e_E tensor u_h)
 =sum_(g in E, h+g in B_p) (-1)^pos e_(E minus {g}) tensor v_(h+g).  (7)
```

An entry can reach `[b,F]` only from

```text
E=F union {g}, h=b-g,
```

where `g notin F` and `g in R_b`. Therefore the row is zero exactly when
`R_b minus F` is empty. If that set is nonempty, any `g` in it supplies an entry with coefficient
`+1` or `-1`, so the converse is also integral.

Let `Z_i` be the free coordinate submodule spanned by all `[b,F]` with `|F|=i` and
`R_b subset F`. Equation (7) has zero projection onto `Z_i`. Thus, after splitting the codomain
into `Z_i` and its complementary coordinate module, the image of `delta_(i+1)` lies entirely in
the complement. The cokernel consequently contains `Z_i` as a primitive free direct summand.
For fixed `b`, the number of size-`i` supersets of `R_b` is

```text
binom(n-|R_b|,i-|R_b|).
```

Summing over `b` proves (1) over the integers and hence over every field.

## 2. The explicit consecutive kernel family

Fix `2<=t<=p-2` and `b=10p+t`. Partition `G_p^+` into its two low blocks and the high part.

For `1<=g<=p`:

- `g<t` gives `10p<b-g<11p-1`, which is a gap between high blocks;
- `g=t` gives `b-g=10p`, the high singleton;
- `g=t+1` gives the missing offset `10p-1`;
- `t+2<=g<=p` gives `8p<=b-g<=10p-2`, inside the second high interval.

For `3p<=g<=4p-2`, the complement satisfies

```text
6p+t+2<=b-g<=7p+t<=8p-2,
```

so the entire second low block lies in `R_b`. Finally, `g>=6p` gives
`b-g<=4p+t<6p`, so no high variable lies in `R_b`. This proves the set equality in (3).

The set has `(p-1)+1+(p-t-1)=2p-t-1` elements. Its sum is

```text
(p-1)(7p-2)/2 + t + p(p+1)/2-(t+1)(t+2)/2,
```

and adding `10p+t` gives the offset formula in (3). As `t` decreases from `p-2` to `2`, the
homological degrees run from `p+1` through `2p-3`. Section 1 proves the primitive classes.

## 3. Why the proposed coordinatewise survival fails

For `(p,t)=(4,2)`, the selected low chain is

```text
e_(2,4,12,13,14) tensor X_2.
```

It is not a coloop in the low source boundary. With a fixed high exterior factor `e_40`, the
following ten-term integral combination is a cycle; each pair denotes
`coefficient * (e_E tensor X_l)`:

```text
+ ([1,2,3,13,14],14)
- ([1,2,4,13,14],13)
- ([1,3,4,12,13],14)
+ ([1,3,4,12,14],13)
+ ([1,3,12,13,14],4)
- ([1,4,12,13,14],3)
+ ([2,3,4,12,13],13)
- ([2,3,4,12,14],12)
- ([2,3,12,13,14],3)
+ ([2,4,12,13,14],2).                                      (8)
```

Its low Koszul boundary is zero over the integers. Removing the high factor from the last term
gives the selected coordinate `[42,F]` with coefficient one. Hence the unit-pivot survival
mechanism of EXP-034 does not extend to this cell. This refutes the coordinatewise part of P3 but
does not decide the dimension of the full target quotient.

## 4. Complete target quotient and the rank identity

The complete target component has `79` kernel codomain rows and `119` kernel boundary columns.
Let `d_D` be the low boundary on the `710` degree-one source chains, let `J` be the connecting
chain map, and let `delta_K` be the kernel incidence boundary. No choice of a cycle basis is
needed. The image of

```text
M = [[d_D,0],[J,delta_K]]                                    (9)
```

projects onto `im(d_D)`, and the kernel of that projection is
`im(delta_K)+J(ker d_D)`. Therefore

```text
dim coker(delta_K)=79-rank(delta_K),
dim coker(Tor(D)->coker(delta_K))=79+rank(d_D)-rank(M).       (10)
```

Exact sparse elimination gives

| field | `rank(delta_K)` | `dim coker(delta_K)` | `rank(d_D)` | `rank(M)` | connecting rank | surviving dimension |
|---|---:|---:|---:|---:|---:|---:|
| `GF(2)` | 74 | 5 | 513 | 588 | 1 | 4 |
| `GF(3)` | 75 | 4 | 513 | 589 | 1 | 3 |
| `GF(5)` | 75 | 4 | 513 | 589 | 1 | 3 |
| `GF(1000003)` | 75 | 4 | 513 | 589 | 1 | 3 |

The Smith normal form of the integral `79` by `119` matrix `delta_K` has rank `75`, four free
cokernel factors, and exactly one nonunit invariant factor, equal to `2`. This proves (6) and the
first line of (5). Equation (10) proves the second line over `GF(2)` and `GF(3)`.

Finally, the minimal EXP-033 cubic cone could add to the `C_4` component only from the shifted
diagonal group at homological degree four and offset `87-3p=75`. The four smallest high offsets
sum to

```text
24+25+26+27=102>75.
```

That source component is zero, so the `C_4` values equal the `A_4` values, proving (5).

## 5. Validation and trust boundary

- The canonical representation classifier covers every `p=4,...,300`; its complete aggregate is
  `cc98154e60bdc00fe1f503020aa7d5c66b53ff0cc4ce2158f199d03c2a5fda8b`.
- The first failed pivot is preserved in the smoke artifact as the integral cycle (8).
- The complete target calculation uses all `79`, `119`, and `710` basis elements, not a selected
  submatrix. Its artifact SHA-256 is
  `4072a9fb7844d07763fae1b08e99da3d94d38cf3a40f980316c38f0931091276`.
- An independent route reconstructs both Artinian layers from numerical-semigroup ideal powers,
  uses a reversed column and pivot order, matches every basis hash and rank, and has artifact
  SHA-256 `b92e787bc120b5fa12aac1fc4a10792883e699ed7315055958f3916e8d10b60b`.
- Nine symbolic interval negations are UNSAT, the offset identity is exact, the Smith and cubic
  boundaries are rechecked, and the symbolic artifact SHA-256 is
  `b1bfc105f3e9ace368f181ccf10f367fe1f4d23199e49c14275bd8e9b941569e`.

The all-parameter claims are the deductive zero-row and interval arguments in Sections 1 and 2.
The characteristic-dependent statement is exact for `p=4`; no extrapolation to all `p` is made.

