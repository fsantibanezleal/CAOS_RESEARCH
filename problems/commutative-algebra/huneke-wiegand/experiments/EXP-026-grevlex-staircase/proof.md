# EXP-026 proof - the explicit grevlex staircase

## Theorem

Fix `p>=4`, put `q=24p`, and retain the EXP-025 presentation

```text
C_p=P_p/J_p,
P_p=k[X_a : a in G_p],
X_a maps to x y^a in k[x,y]/(y^q).
```

Use graded reverse lexicographic order with `X_a>X_b` if and only if `a>b`, so `X_0` is the
last variable. Then the reduced Groebner basis of `J_p` has degree profile

```text
degree 2: 50p^2-17p,
degree 3: 5p-1,
degree 4: p-2,
degree >=5: 0.
```

Its total size is `50p^2-11p-3`. No minimal leading monomial is divisible by `X_0`.

The quadratic part consists of every noncanonical quadratic monomial `M`, with reduced relation

```text
M-N_(2,s)  if s=sum(M)<q,
M          if s>=q,
```

where `N_(2,s)` is the grevlex-smallest quadratic factorization of `s`. Of the quadratic basis
elements,

```text
(77p^2-49p+2)/2
```

are binomials and `(23p^2+15p-2)/2` are monomial zero-relations.

The nonquadratic elements are exactly the families declared in `hypothesis.md`. In compact form,
their leading monomials are

| degree | leading monomial | range |
|---:|---|---|
| 3 | `X_i X_p X_(12p-1)` | `1<=i<=p` |
| 3 | `X_i X_p X_(15p-1)` | `1<=i<=p` |
| 3 | `X_i X_p X_(18p-1)` | `1<=i<=p` |
| 3 | `X_i X_(4p-2) X_(16p)` | `1<=i<=p-2` |
| 3 | `X_i X_(4p-2) X_(18p-1)` | `1<=i<=p` |
| 3 | `X_p^3` | one element |
| 4 | `X_i X_p^2 X_(4p-2)` | `2<=i<=p-1` |

The corresponding reduced tails are the twelve endpoint/interior formulas in the declaration;
the quartic tail is `X_0^3 X_(6p+i-2)`.

## 1. Canonical standard monomials

EXP-025 proves that the image of a degree-`n` monomial is determined by the pair

```text
(n,total offset)
```

when the total offset is below `q`, and is zero otherwise. Thus each surviving fiber contains
exactly one standard monomial: its grevlex-smallest member. Because the variables are ordered by
decreasing offset, grevlex-smallest is equivalent, for a fixed degree, to lexicographically
smallest after listing the factors in nondecreasing offset order.

Write that representative as `N_(n,s)`. Therefore

```text
in(J_p) = (all monomials other than the N_(n,s)).
```

A monomial is a minimal generator of `in(J_p)` exactly when it is not canonical and every
one-variable divisor is canonical. This boundary criterion reduces the Groebner problem to a
finite factorization problem.

## 2. Quadratic boundary

There are `10p` variables, hence `binom(10p+1,2)=50p^2+5p` quadratic monomials. EXP-025 gives
`|E_2|=22p`, and every surviving offset contributes one canonical quadratic. Consequently the
number of noncanonical quadratics is

```text
50p^2+5p-22p=50p^2-17p.
```

Split the ordered offset set `G_p` into the eleven closed blocks in the premise formula. Directly
summing, block by block, the unordered pairs `a<=b` satisfying `a+b>=24p` gives

```text
Z_p=(23p^2+15p-2)/2.
```

These are precisely the monomial zero-relations. Subtracting `Z_p` and the `22p` canonical pairs
from all quadratic monomials gives

```text
B_p=(77p^2-49p+2)/2
```

binomial quadratic relations. Both expressions are integers because their numerators are even.

## 3. Cubic and quartic boundary

The all-parameter certificate formalizes the preceding boundary criterion in Presburger
arithmetic. Its generator predicate is exactly the eleven-block formula for `G_p`. A sorted tuple
is declared standard exactly when it has total offset below `24p` and no lexicographically smaller
sorted factorization with the same total exists.

For all integers `p>=4`, the certificate closes the following counterexample formulas as UNSAT:

1. a minimal cubic boundary outside the six declared families;
2. a declared cubic that is not minimal boundary;
3. a minimal quartic boundary outside the declared family;
4. a declared quartic that is not minimal boundary; and
5. for each of twelve endpoint/interior cases, a tail that is nonstandard, has unequal offset, or
   is not grevlex-smaller than its lead.

Each proof obligation runs in a fresh Z3 process to remove solver-allocation order as a hidden
input. All 16 queries are UNSAT. Their aggregate is

```text
10c66bbcaa56108f6bdb423bda7c37d35818c4066ef57970a4e29e046f9dd5fa.
```

The five cubic groups contain `p,p,p,p-2,p` elements, and the isolated cubic contributes one, so
the cubic count is `5p-1`. The quartic range has `p-2` elements.

## 4. Stabilization and absence of later generators

EXP-025 gives `E_4=[0,q-1]` and `E_n=[0,q-1]` for every `n>=4`. Because `X_0` is the last
variable, adding an `X_0` factor makes a fixed-offset factorization lexicographically smaller than
any factorization with fewer `X_0` factors. Hence, for every `n>=4` and `0<=s<q`,

```text
N_(n,s)=X_0^(n-4) N_(4,s).
```

The standard staircase therefore stabilizes at degree four. If a minimal initial generator had
degree at least five, all of its one-variable divisors would be standard; the displayed formula
would then force the monomial itself to be the corresponding `X_0`-multiple and hence standard,
a contradiction. There are no minimal generators in degree at least five.

This deterministic stabilization argument is the trust anchor for the infinite tail. Exploratory
quantified degree-five queries did close as UNSAT in isolated runs but had unstable runtimes, so
they are deliberately not used in the final certificate.

## 5. Consequences

The displayed binomials are monic, have pairwise distinct minimal leading monomials, and have
canonical tails. They are therefore the reduced Groebner basis.

No leading generator contains `X_0`. Thus `X_0` is regular on the monomial degeneration, and the
standard monomials not divisible by `X_0` have degree counts

```text
(1,10p-1,12p,2p-1,1).
```

This gives a flat Cohen--Macaulay monomial degeneration with the same Hilbert series as `C_p`.
It also separates two complexities that need not agree: `J_p` has relation type three by
EXP-023, while this natural reduced Groebner basis necessarily reaches degree four.

## Trust boundary

- The standard-monomial and stabilization arguments are deductive consequences of frozen
  EXP-025.
- The family classification uses Z3 4.16.0 over quantifier-bearing Presburger formulas. The
  solver returned UNSAT, but no separately checked proof objects were emitted.
- The finite campaign and independent clique audit test implementations and catch formula/order
  errors; they do not replace the all-parameter argument.
- No assertion is made about the unresolved interior Betti table.

