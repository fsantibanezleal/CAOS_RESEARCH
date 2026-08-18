# EXP-026 verdict - explicit grevlex staircase

Status: **CONFIRMED** on 2026-08-18.

## Result

For every integer `p>=4`, grevlex with variables ordered by decreasing offset and `X_0` last has a
reduced Groebner basis of degree profile

```text
(50p^2-17p, 5p-1, p-2)
```

in degrees two, three, and four. There are no later elements. Its total size is
`50p^2-11p-3`, and no minimal leading monomial is divisible by `X_0`.

The quadratic part is the canonical set-comprehension basis from `proof.md`. It splits into

```text
binomial quadrics: (77p^2-49p+2)/2,
monomial zero quadrics: (23p^2+15p-2)/2.
```

The `5p-1` cubics are exactly six uniform families, including the EXP-023 isolated cubic, and the
`p-2` quartics form one uniform family. Every reduced tail is explicit.

## Validation record

- Mandatory `p=4` smoke: PASS; profile `(732,19,2,0,0)` through degree six.
- Full exact campaign: PASS at all 297 values `p=4,...,300` in 8.474 seconds; aggregate
  `63af8f734afc8c057751d7633f63eec6d1df83472d494dbad6ada19e4365a218`.
- Independent clique audit: PASS at `p=4,5,6,17,73,151,300` in 0.598 seconds; it enumerates
  canonical pairs directly, reconstructs higher clique boundaries without Route A state, rehashes
  every campaign row, and has aggregate
  `401c4807cc0a29a67a42c0d84ca8f235c86a271fe93bf1a2d2df586766e41373`.
- All-parameter symbolic certificate: PASS. All 16 cubic/quartic completeness, soundness, and tail
  obligations are UNSAT in 62.505 seconds; query aggregate
  `10c66bbcaa56108f6bdb423bda7c37d35818c4066ef57970a4e29e046f9dd5fa`.
- All eight adversarial controls pass in every campaign row.

The first complete campaign attempt is preserved as `INCONCLUSIVE_BUDGET`: it checked 141 rows
through `p=144` before the declared 120-second cap. Profiling showed repeated recursive canonical
searches dominated runtime. Replacing them with a cached quadratic oracle plus exact boundary
divisibility checks preserved the earlier row hashes and completed the campaign. The budget stop
is evidence about implementation cost only, not a mathematical failure.

## Consequences and scope

- `C_p` has a flat Cohen--Macaulay monomial degeneration whose Artinian reduction has Hilbert
  function `(1,10p-1,12p,2p-1,1)`.
- The natural reduced Groebner degree is four although the minimal relation type is three.
- The explicit Groebner half of HWB-029 is closed.
- The interior Betti table is not computed and is moved to a separate backlog item.

## Manuscript decision

The trigger is crossed: this is a new theorem with an exact basis, all-parameter classification,
and independent validation. It concerns exactly the algebra of the focused
`curvilinear-fiber-cones` companion, so that manuscript must expand to v0.02 and publish as a new
Zenodo version. A third manuscript would fragment one coherent object. A later complete interior
Betti table may justify a split.

## Trust boundary

The solver classification uses quantifier-bearing Presburger formulas and emits no independently
checked UNSAT proof objects. The deductive standard-monomial principle and `X_0`-stabilization
argument are separately written, while the clique audit is independently encoded but finite.
The result does not solve the Huneke--Wiegand conjecture in general; it strengthens the structural
analysis of the already known CAOS counterexample family.

