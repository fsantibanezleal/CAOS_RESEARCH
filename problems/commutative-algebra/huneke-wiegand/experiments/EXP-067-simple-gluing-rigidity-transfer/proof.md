# EXP-067 proof: simple gluing preserves two-generated rigidity

## Theorem

Let `Gamma` be a numerical semigroup of multiplicity `m`, let `s>0` be a gap,
and let `a` satisfy `a,a+s in Gamma`. Suppose the two-generated monomial ideal

```text
I = (t^a,t^(a+s))
```

is rigid in the localized numerical semigroup ring. For any integer `q>=1`
with `gcd(q,m)=1`, define the simple gluing

```text
Delta = m*N + q*Gamma.
```

Then:

1. `Delta` is a numerical semigroup of multiplicity `m`, and its Apery set
   with respect to `m` is `q*Ap(Gamma,m)`, with residues permuted by
   multiplication by `q`;
2. if `Gamma` is symmetric with Frobenius number `F`, then `Delta` is symmetric
   with Frobenius number `q(F+m)-m`;
3. `q*s` is a gap of `Delta`; and
4. if `Gamma` is symmetric, `(t^(qa),t^(q(a+s)))` is a nonprincipal rigid
   ideal in the localized semigroup ring of `Delta`.

Thus every symmetric two-generated monomial counterexample has infinitely many
simple-gluing descendants.

## 1. Apery set and symmetry

Write the Apery set of `Gamma` with respect to `m` as
`{w_0,...,w_(m-1)}`, where `w_i` is the least element congruent to `i` modulo
`m`. Since `q` is invertible modulo `m`, the values `q*w_i` occupy all residue
classes modulo `m`.

Each `q*w_i` belongs to `Delta`. Conversely, an element of `Delta` in residue
`q*i` has the form `m*b+q*gamma`, with `b>=0` and `gamma in Gamma`. Its
congruence implies `gamma=i mod m`, so `gamma>=w_i` and the element is at least
`q*w_i`. Hence

```text
Ap(Delta,m) = {q*w_i : 0<=i<m},
```

with the stated residue permutation. Every positive generator other than `m`
is at least `q*m`, so the multiplicity remains `m`.

The maximum Apery value of `Gamma` is `F+m`; therefore

```text
F(Delta) = q(F+m)-m.
```

The Apery genus formula gives

```text
g(Delta)
 = q*g(Gamma) + (q-1)(m-1)/2.
```

If `Gamma` is symmetric, `2g(Gamma)=F+1`, and consequently

```text
2g(Delta)
 = q(F+1)+(q-1)(m-1)
 = q(F+m)-m+1
 = F(Delta)+1.
```

The numerical semigroup `Delta` is therefore symmetric.

If `q*s` belonged to `Delta`, then `q*s=m*b+q*gamma` for some `b>=0` and
`gamma in Gamma`. Coprimality gives `b=q*h` and `s=gamma+m*h` for an integer
`h>=0`, contradicting that `s` is a gap. Thus `q*s` is a gap.

## 2. Simultaneous representation alignment

For `r>=0`, define

```text
C_r(Gamma,s) = {x>=0 : x+j*s in Gamma for every 0<=j<=r}.
```

We claim

```text
C_r(Delta,q*s) = m*N + q*C_r(Gamma,s).                 (2.1)
```

The right-to-left inclusion follows immediately from semigroup closure.

For the converse, take `n in C_r(Delta,q*s)`. For each `j`, choose
`b_j>=0` and `gamma_j in Gamma` such that

```text
n+q*j*s = m*b_j+q*gamma_j.
```

Comparing with `j=0` and using `gcd(q,m)=1`, there is an integer `ell_j` with

```text
gamma_j = gamma_0+j*s+m*ell_j,
b_j     = b_0-q*ell_j.
```

Set `L=max_j ell_j` and choose `j_0` attaining that maximum. Then
`b_0-qL=b_(j_0)>=0`. Moreover, for every `j`,

```text
gamma_0+mL+j*s = gamma_j+m(L-ell_j) in Gamma.
```

Thus `gamma_0+mL` belongs to `C_r(Gamma,s)`, and

```text
n = m(b_0-qL)+q(gamma_0+mL),
```

which proves the other inclusion in (2.1).

## 3. Rigidity transfer

Use the exponent sets

```text
E = C_1(Gamma,s),
D = C_2(Gamma,s).
```

For a two-generated monomial ideal over a one-dimensional Gorenstein numerical
semigroup ring, the established colon criterion identifies rigidity with
`D=E+E`. Assume `Gamma` is symmetric. Then `Delta` is symmetric by item 2, so
the criterion applies in both semigroup rings. Applying (2.1) for `r=1,2` gives

```text
E_Delta = m*N+q*E,
D_Delta = m*N+q*D.
```

Since `N+N=N`,

```text
E_Delta+E_Delta
 = m*N+q(E+E)
 = m*N+q*D
 = D_Delta.
```

The scaled ideal is rigid. Both exponents `q*a` and `q(a+s)` belong to
`q*Gamma` and hence to `Delta`. Its normalized shift `q*s` is a gap, so it is
not principal.

## 4. Two-parameter CAOS family

For EXP-009, `m=24p`, `s=6p`, `a=m`, `F=78p-1`, and the embedding dimension is
`11p`. The theorem therefore gives, for every `p>=4` and every `q>=1` coprime
to `24p`,

```text
Gamma_(p,q) = 24p*N + q*Gamma_p,
F_(p,q)     = q(102p-1)-24p,
I_(p,q)     = (t^(24pq),t^(30pq)).
```

The minimal generators are `24p` together with `q` times the original minimal
generators other than `24p`. If one of those scaled generators were redundant,
coprimality would divide the coefficient of `24p` by `q` and produce a
redundancy among the original generators. Thus the embedding dimension remains
`11p`.

The case `q=1` is EXP-009. For every fixed `p`, infinitely many integers are
coprime to `24p`, so this is a genuine two-parameter counterexample family.

## 5. Exact supporting checks

The producer and independent auditor test the same 72 cases: `p=4,...,12` and
the first eight admissible `q` values for each `p`. Both reconstruct Apery sets,
by two different algorithms, and check the Apery transfer, the Frobenius and
symmetry formulas, the gap `q*s`, and the rigidity sumset through `2F+1`. Only
the producer compares the complete `E` and `D` transfer sets with (2.1) and runs
the adverse controls. The `<4,5>` nonrigid control remains nonrigid for
`q=1,3,5,7`. The five noncoprime controls record `gcd(24p,q)>1` for pairs chosen
with that property; they document the P4 premise but exercise no rejection path.

These checks validate the implementations. The all-parameter conclusion is the
deductive argument above.
