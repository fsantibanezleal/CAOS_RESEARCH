# Frontier source and proof audit

Access date: 2026-08-02. Scope: HW-P3, before EXP-004 computation.

## Published frontier

García-Sánchez and Leamer, *Huneke-Wiegand Conjecture for Complete Intersection
Numerical Semigroup Rings*, arXiv:1211.4554v1, Example 23, states that NumericalSgps was used to
check every two-generated ideal of every symmetric numerical semigroup with Frobenius number
less than 69. The paper does not provide the enumerated semigroups, executable code, counts, or
machine certificates for that finite claim. The same example then closes the class under iterated
gluings. Section 4 asks broader ring and module questions, but does not extend the finite frontier.

Primary source: `https://arxiv.org/abs/1211.4554`.

## Independent enumeration theorem

Blanco and Rosales, *The Tree of Irreducible Numerical Semigroups with Fixed Frobenius Number*,
Forum Mathematicum 25 (2013), 1249-1261, DOI `10.1515/form.2011.151`, arXiv:1105.2147,
Theorem 9, gives a complete rooted tree for irreducible numerical semigroups of fixed Frobenius
number `F`. For odd `F`, irreducible is equivalent to symmetric. The root is

```text
C(F) = {0,(F+1)/2,(F+1)/2+1,...} minus {F}.
```

The children of a node `S` replace `x` by `F-x`, where `x` is a minimal generator satisfying

```text
F/2 < x < F,
2x-F not in S,
3x != 2F,
4x != 3F,
F-x < multiplicity(S).
```

The theorem proves completeness and uniqueness of the path to the root. Example 10 independently
lists the six nodes for `F=11`, which supplies a small exact regression target.

Primary sources: `https://arxiv.org/abs/1105.2147` and `https://doi.org/10.1515/form.2011.151`.

## Proof-carrying SAT route

CaDiCaL accepts DIMACS CNF and emits a proof as its second positional output. DRAT-trim checks
whether a DRAT proof derives the empty clause from the original CNF. The solver and checker are
separate implementations. The official documentation defines the formats and validation rule.

Primary tooling sources:

- `https://github.com/arminbiere/cadical`
- `https://github.com/marijnheule/drat-trim`
- CaDiCaL 2.0 tool paper: `https://doi.org/10.1007/978-3-031-37703-7`
- DRAT-trim paper: `https://doi.org/10.1007/978-3-319-09284-3_31`

## Archived-source integrity

External source root: `E:/_Datos/caos-research/huneke-wiegand/sources/`.

| object | SHA-256 |
|---|---|
| `1105.2147.tar` | `55996ab608ff8dbaf9c44040f7bd6def67843246088425b200e5deab0b0da01e` |
| `1105.2147.pdf` | `26423cf1da402b00f183a9fd67cb2470d9d3364bded26240bd90d0ca72fb0492` |
| `1211.4554.tar` | `b9e6421057d9892181f15c5df648036585b5e7420f442d6e234f308583d23d54` |

## Exploration and self-questioning

The earlier plan treated certified SAT as the frontier spine. The source audit exposes a stronger
two-sided design: theorem-complete enumeration supplies transparent mathematical objects and
witnesses, while DRAT supplies proof-carrying obstruction. Either route can expose an encoding or
enumeration defect in the other. The cheap invariant is parity: a symmetric numerical semigroup
has odd Frobenius number and genus `(F+1)/2`, so only odd `F` and exactly half-membership vectors
need consideration.

No current primary source found in the fresh 2026-08-02 sweep reports a frontier beyond 69 or a
classification of the new public candidate. The candidate repository's latest pushed commit remains
`a7e26159916b` from 2026-08-01 and adds attribution for Professor Huneke's verification, not a
minimality result.
