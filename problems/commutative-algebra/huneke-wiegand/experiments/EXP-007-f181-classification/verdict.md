# EXP-007 verdict - CONFIRMED

Run date: 2026-08-02. Phase HW-P3. Backlog HWB-010.

## Main result

At the least possible Frobenius number `F=181`, there is exactly one normalized rigid pair
`(Gamma,s)` in the symmetric numerical-semigroup, nonprincipal two-generated monomial-ideal
class. It is Son Pham's public semigroup at shift `s=14`:

```text
Gamma = <56,57,58,63,64,70,71,72,73,74,75,76,77,78,79,80,81,82,83,
         87,89,90,93,95,96,97>.
```

Thus the public pair is not only Frobenius-minimal, it is the unique normalized pair attaining
that minimum in the stated class.

## Completeness chain

1. The selector formula at `F=181` first returned the exact public model at shift 14.
2. Adding `not q_14` made the selector formula UNSAT. CaDiCaL emitted a 45,867,741-byte DRAT
   proof, and DRAT-trim accepted it against the exact formula. Therefore 14 is the complete
   feasible-shift set.
3. The fixed `(181,14)` formula returned the exact public membership vector.
4. A projected clause containing one signed literal for every `h[0..181]` blocked that vector,
   independent of auxiliary assignments. The resulting formula was UNSAT. Its 1,608,691-byte
   proof was accepted by DRAT-trim. Therefore no second semigroup occurs at shift 14.
5. The independent auditor rebuilt all four formulas byte-for-byte, decoded both SAT logs,
   reran closure, symmetry, generator and rigidity checks, reproduced every compact aggregate,
   and accounted for all 12 external artifacts.
6. The auditor freshly reran both proof checks. Both passed in 232.88 seconds total.

The projected-blocking proof is recorded in `encoding-proof.md`. It excludes exactly one complete
mathematical projection and cannot overcount alternative Tseitin assignments.

## Prediction table

| prediction | result | decisive evidence |
|---|---|---|
| P1 | PASS | support is exactly `[14]`; terminal support proof accepted |
| P2 | PASS | fixed `s=14` class contains the exact public vector |
| P3 | PASS | no additional shift or membership vector exists after checked terminal proofs |
| P4 | PASS | selector support and the nonempty fixed classes both equal `{14}` |
| P5 | PASS | every completeness boundary has a persisted and freshly rechecked DRAT proof |
| P6 | PASS | deterministic reconstruction reproduces all CNF and aggregate hashes after resume-safe checkpoints |

## Evidence summary

```text
feasible shifts:                    1  ({14})
normalized rigid pairs:             1
distinct semigroups:                1
support SAT solve:             164.44 seconds
support terminal solve:        520.61 seconds
support initial proof check:   375.96 seconds
fixed-model solve:               2.86 seconds
fixed terminal solve:            9.17 seconds
fixed initial proof check:       10.74 seconds
fresh audit proof rechecks:     232.88 seconds
external files:                     12
external bytes:             63,609,504
external manifest SHA-256:  02d1265b75e886bc6ec693e60b367b661476170c755e38a220342396564ef5d3
classification SHA-256:     b37d9410fa07c00f22ccc0f83796644db3b44f0dd654c06933aa5d22cb1ed788
```

The regression at `F=11` independently ends with zero feasible shifts and an accepted proof.

## Exact equivalence and scope

Translation of a two-generated monomial ideal and interchange of its generators reduce it to one
positive normalized shift `(0,s)`. The classification is exact in those normalized coordinates.
It does not assert an additional unproved quotient by abstract ring isomorphism.

This result does not classify higher Frobenius values, arbitrary modules, arbitrary one-dimensional
Gorenstein local domains, minimum multiplicity or embedding dimension across all counterexamples,
or an infinite family. Son Pham retains discovery priority for the counterexample. CAOS contributes
the certified minimality and minimum-layer classification.

## Publication decision

The complete classification is a scope strengthening of preprint v0.01. Under the binding
publication methodology it triggers a manuscript expansion and a Zenodo new version. The frozen
v0.01 file and DOI must remain unchanged.
