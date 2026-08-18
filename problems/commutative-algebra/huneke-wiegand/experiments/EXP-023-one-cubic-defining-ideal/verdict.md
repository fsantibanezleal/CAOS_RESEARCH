# EXP-023 verdict - one-cubic presentation CONFIRMED

Status: **CONFIRMED** on 2026-08-18 by an exact all-parameter Presburger proof, an exact bounded
campaign, and an independently encoded audit.

## Result

For every integer `p>=4`, the defining ideal of the conductor special fiber is

```text
J_p=((J_p)_2, X_0^2 X_(3p)-X_p^3).
```

Its complete first Betti row is

```text
beta_(1,2)=50p^2-17p,
beta_(1,3)=1,
beta_(1,j)=0 for every j>=4.
```

Thus the relation type is three and

```text
mu(J_p)=50p^2-17p+1.
```

Together with EXP-021, this gives an infinite family of one-dimensional Cohen--Macaulay special
fiber rings that are not Koszul. The result is about the explicit conductor family only; it does
not classify defining ideals of arbitrary conductor ideals or fiber cones.

## Why the conclusion is complete

The proof in `proof.md` identifies minimal equations in degrees three through five with component
defects in exact offset-state graphs. For all integers `p>=4` it proves:

- degree three has one component per nonzero offset, except exactly two at total `3p`;
- the two exceptional components are joined by the displayed cubic;
- degrees four and five have one component per nonzero offset and no surviving invalid component.

EXP-017 gives reduction number four and EXP-021 gives Cohen--Macaulayness. The construction in
Abdolmaleki--Kumashiro, Theorem 2.8, therefore bounds the complete defining set to degrees at most
five. There is no untested higher-degree tail.

## Exact evidence

The scalable campaign completed `p=4,...,23` in 249.611 seconds. Every row has the predicted
profile. Its aggregate is

```text
d23792c47a2e07785a27ebc71e99619705f7aa53a38ebe7f66ffa03b0518ce83.
```

The separately encoded total-by-total audit rehashed all 20 campaign rows and rebuilt
`p=4,13,23` in 19.867 seconds. Its aggregate is

```text
a27b3b13fde197b1f011bf07dc2c321d84ab7c895c9aa02d7c2a073e48f18038.
```

The bounded Presburger certificate covers all integer `p>=4`. It closed 133 terminal negated
queries as UNSAT, after four adaptive cell splits, with no SAT or unresolved result. Its query
aggregate is

```text
832c8421fe66359b8c246e3465e27de6ea7829215f892ab815e72b1f44787194.
```

Canonical artifact hashes are:

| artifact | SHA-256 |
|---|---|
| `artifacts/results.json` | `e91a4e6acd9bbc243642c028eaba755b3cebf1a647f162634e579e6598944f44` |
| `artifacts/audit.json` | `30deabe2aceb1791f2fe8458c7c78ffa2db6da3c87586cf1932545d7cae62180` |
| `artifacts/symbolic-certificate.json` | `c2dd364126eb059f22c9356d4b99d0b4ae8a2c54db5e1dbff1d0ebfc43a48a6d` |
| `artifacts/attempt-1-budget-checkpoint.json` | `94010d659afebdff99cd66e337d36d28bedbbca9e6b467f837ac1c6d19fca486` |

The original `p=4,...,24` request completed its `p=24` row but crossed the declared 300-second
budget at 314.865 seconds. Its checkpoint remains `INCONCLUSIVE_BUDGET`. The successful formal
campaign was narrowed before rerunning and does not overwrite that attempt.

## Predictions

- P1 PASS: the full defining ideal is the quadratic kernel plus the displayed cubic.
- P2 PASS: the complete first Betti row is exactly the declared row.
- P3 PASS: the relation type and minimal-equation count follow.
- P4 PASS: the fiber cone is Cohen--Macaulay by EXP-021 and non-Koszul by the necessary cubic.

Verdict: **CONFIRMED**.

## Adversarial validation

- The independent auditor uses total-fiber graphs instead of the campaign's global disjoint-set
  construction.
- The `p=4,5,6` calibration reproduces EXP-022's full monomial enumeration exactly.
- Omitting the cubic, adding a false second cubic, perturbing the quadratic count, and declaring
  the ring Koszul are rejected by the stored controls.
- Invalid totals are tested for zero connectivity rather than discarded from the dimension count.
- Solver `sat` would stop as a refutation, and a terminal `unknown` would force
  `INCONCLUSIVE`; neither occurred.

## How could this be wrong?

The main residual trust boundary is the exact symbolic implementation and Z3's soundness. The Z3
UNSAT results do not carry a separately checked proof object. This risk is reduced, but not erased,
by the explicit interval reduction in `proof.md`, the independent graph implementation, the
EXP-022 monomial calibration, hashed artifacts, and the finite stress range. A future
proof-producing Presburger backend or a fully expanded hand proof of every affine cell would
further reduce this boundary.

The non-Koszul conclusion uses only the standard necessary condition that a standard graded Koszul
algebra has a quadratic defining ideal. No claim is made about its full resolution, Groebner
bases, or other homological invariants.

## Publication consequence

This is a new uniform minimal-presentation theorem, not only computational evidence. It triggers
a substantive manuscript revision and a new Zenodo version under the repository publication rule.
