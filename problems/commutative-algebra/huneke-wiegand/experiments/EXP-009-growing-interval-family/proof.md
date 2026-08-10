# EXP-009 symbolic proof

## The theorem

For every integer `p>=4`, put `s=6p` and define

```text
A = [0,p] union [3p,4p-2],
B = ([p+1,3p-1] minus {2p-1}) union {4p} union [5p-1,6p-1],
C = [0,2p] union [3p,5p-2].
```

Let `Gamma_p` contain zero, the blocks `4s+A`, `[5s,6s-1]`, `6s+B`, `8s+C`,
`[9s,13s-2]`, and every integer at least `13s`, with no other nonnegative members.
Then `Gamma_p` is a symmetric numerical semigroup with multiplicity `4s`, Frobenius number
`13s-1`, conductor `13s`, and embedding dimension `11p`. The ideal

```text
I_p = (t^(4s),t^(5s))
```

over the localization of `k[t^Gamma_p]` at its positive-degree maximal ideal is nonprincipal and
rigid. Consequently these pairs form an infinite family of counterexamples in the two-generated
monomial-ideal class.

## Residue identities

For subsets of `[0,s-1]`, write `low(X+Y)` for sums below `s` and `carry(X+Y)` for sums at least
`s`, reduced by `s`. Direct addition of the displayed intervals gives

| sum | low residues | carried residues |
|---|---|---|
| `A+A` | `C` | `[0,2p-4]` |
| `A+B` | `[p+1,6p-1]` | `[0,4p-3]` |
| `B+B` | `[2p+2,6p-2]` | `[0,6p-2]` |
| `A+C` | `[0,6p-2]` | not needed |

The point removed from the middle interval of `B` is paired with the singleton `4p`; the adjacent
interval sums overlap because `p>=4`. In particular,

```text
[0,2p-4] union [p+1,6p-1] = [0,6p-1],
[0,4p-3] union [2p+2,6p-2] = [0,6p-2].
```

The first equality is the threshold-bearing one: it is false at `p=2,3` and true for every
`p>=4`. The experiment checks the seven equalities as literal finite set identities through
`p=300`; the proof here uses only their affine endpoints.

## Semigroup, Frobenius number and symmetry

The only sums of positive members that can remain below the conductor have level pairs among
`4,5,6,8`. The table handles `4+4`, `4+6`, `6+6`, and `4+8`; every other such sum lands in one of
the full blocks. The exact exclusions of residue `s-1` in `low(B+B)` and `low(A+C)` prevent the
Frobenius gap from being produced. Thus the displayed set is closed.

The lower blocks generate the entire displayed set. The `A+A` identity produces `8s+C`; sums of
the level-4 and full level-5 generators produce level 9; two level-5 generators produce level 10
and residues `0,...,s-2` of level 11; level-5 plus level-6 generators fill the remaining residue
of level 11 and level 12 through `13s-2`. Adding the generator `4s` to `[9s,13s-2]` produces
`[13s,17s-2]`, and `5s+(12s-1)` produces `17s-1`. This gives `4s` consecutive generated values
from `13s`, so the conductor tail follows.

Every displayed lower generator is below twice the multiplicity, hence cannot be a sum of two
positive members. Their number is

```text
|A| + s + |B| = 2p + 6p + 3p = 11p.
```

Symmetry is blockwise. The gaps below `4s` reflect to `[9s,13s-2]`; the full level-5 block reflects
to the empty level-7 block; `C` is the complement of the reflected `A`; and `B` contains exactly
one residue from each pair `{r,s-1-r}`. Finally zero reflects to `13s-1`. Therefore `Gamma_p` is
symmetric and its semigroup ring is Gorenstein.

## Rigidity

Normalize `I_p` to `(1,t^s)` and write

```text
E = {z : z,z+s are in Gamma_p},
D = {z : z,z+s,z+2s are in Gamma_p}.
```

The block descriptions above give

```text
E: 4s+A, 5s+B, 8s+C,
   full levels 9 and 10,
   residues [0,s-2] in levels 11 and 12,
   and the full tail from level 13;

D: 8s+C, full level 9,
   residues [0,s-2] in levels 10, 11 and 12,
   and the full tail from level 13.
```

There is no lower block of `D` because `A` and `B` are disjoint. The residue table now computes
`E+E` layer by layer:

```text
level 8:  low(A+A)                         = C,
level 9:  carry(A+A) union low(A+B)        = [0,s-1],
level 10: carry(A+B) union low(B+B)        = [0,s-2],
level 11: carry(B+B)                       = [0,s-2],
level 12: low(A+C)                         = [0,s-2].
```

At and above level 13, `E` contains `4s`, `4s+1`, and the high intervals with only the two
boundary holes forced by the Frobenius gap. Translating by `4s` and `4s+1` fills both holes and
all subsequent values. Hence `D=E+E` everywhere, including the conductor tail. This is the exact
rigidity criterion for the normalized two-generated monomial ideal.

The shift `s` is a gap, so the ideal is not principal. Over the local domain it is therefore not
free. The equality `D=E+E` says its tensor product with its dual is torsion-free, producing the
claimed counterexample.

## Positive-family exclusion

Membership of `4s+1` in `Gamma_p` forces `h=1,d=1` in any generalized-arithmetic presentation
`<4s,4sh+d,...>`. The later member `4s+3p` would then force every intervening value, including
`4s+p+1`, but that value is a gap. Thus no `Gamma_p` belongs to the generalized-arithmetic-sequence
positive family.
