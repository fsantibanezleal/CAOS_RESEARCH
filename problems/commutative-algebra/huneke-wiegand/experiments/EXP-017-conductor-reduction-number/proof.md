# EXP-017 - symbolic proof

Put `D=[0,s-1]`, `D^-=[0,s-2]`, and retain the residue blocks `A_p,B_p,C_p`.
EXP-013 and EXP-016 give

```text
v(T_p)   = (4s+A) union (5s+(A union B)) union (6s+B) union (8s+C)
           union [9s,13s-2] union [13s,infinity),

v(T_p^2) = (8s+C) union [9s,13s-2] union [13s,infinity).
```

Let `Q_p=t^(4s)R_p`.

## 1. The remaining powers

The level-eight block of `T_p^2` added to the least block `4s+A` gives

```text
12s + low(C+A) = 12s+D^-.
```

This is the same residue identity `low(A+C)=D^-` used in the family theorem. All other products
of a finite block of `T_p` with `[9s,13s-2]`, or with the tail from `13s`, fill the tail from
`13s`; no value can fill `13s-1` because that value is not in the base semigroup. Hence

```text
v(T_p^3) = [12s,13s-2] union [13s,infinity).
```

Now `0 in A`. Adding `4s+A` to `[12s,13s-2]` fills `[16s,17s-2]`, while adding it to the tail
fills from `17s`; the endpoint `17s-1=(4s+1)+(13s-2)` is also present because `1 in A`.
Therefore

```text
v(T_p^4) = [16s,infinity).
```

Adding the least value `4s` gives `[20s,infinity)`, and no smaller sum is possible, so

```text
v(T_p^5) = [20s,infinity) = v(Q_p T_p^4).
```

Multiplying this equality by `T_p` inductively proves
`T_p^(n+1)=Q_p T_p^n` for every `n>=4`.

## 2. Exact Sally quotients

Direct subtraction of the displayed profiles gives

```text
v(T_p^3) minus v(Q_p T_p^2)
  = 12s + ([2p+1,3p-1] union [5p-1,6p-2]) union {17s-1},

v(T_p^4) minus v(Q_p T_p^3) = {17s-1}.
```

The first set has `(p-1)+p+1=2p` elements; the second has one. EXP-016 already proves that the
preceding quotient has length `14p`.

For the initial quotient, subtract `v(Q_p)=4s+Gamma_p` from the EXP-013 formula. The surviving
disjoint blocks are

```text
4s+(A minus {0}),
5s+(A union B),
6s+B,
8s+(C minus A),
10s+(D minus B),
11s+D,
12s+(D^- minus C),
{17s-1}.
```

Their cardinalities are respectively

```text
2p-1, 5p, 3p, 2p, 3p, 6p, 2p-1, 1,
```

whose sum is `23p-1`. Thus the successive lengths, starting at `T_p/Q_p`, are exactly

```text
23p-1, 14p, 2p, 1, 0, 0, ... .
```

In particular the first three nonzero quotients rule out reduction numbers below four, while
`T_p^5=Q_pT_p^4` proves reduction number four. Since `T_p` is primary to the maximal ideal in a
one-dimensional local domain, its analytic spread is one; the one-generated reduction `Q_p` is
minimal.

## 3. Hilbert coefficients

The parameter ideal `Q_p=(t^(4s))` has colength `4s=24p`, the size of the Apéry set modulo the
multiplicity. Thus `e_0(T_p)=24p`.

For each `i`, multiplication by the nonzerodivisor `t^(4s)` gives the exact length identity

```text
length(T_p^i/T_p^(i+1))
 = length(R_p/Q_p) - length(T_p^(i+1)/Q_pT_p^i).
```

Summing from `i=0` to `n-1` yields

```text
length(R_p/T_p^n)
 = 24pn - sum_(i=0)^(n-1) length(T_p^(i+1)/Q_pT_p^i).
```

For every `n>=4`, the sum is

```text
(23p-1)+14p+2p+1 = 39p.
```

Hence the exact eventual Hilbert function is `length(R_p/T_p^n)=24pn-39p`, and

```text
e_0(T_p)=24p,  e_1(T_p)=39p.
```

This proof uses only the exact block formulas and cardinalities; the finite campaign is supporting
implementation evidence.

