# EXP-008 - parametric interval block family

Declared 2026-08-10 before implementation or evaluation of the proposed formula. Phase HW-P4,
Route A. Trigger: EXP-006 Route K produced eleven non-seed models at every even shift from 20
through 40 and passed the three-instance gate.

## Question

Does the Route K recurrence contain an explicit infinite family of symmetric numerical semigroups
whose two-generated monomial ideals are rigid?

## Proposed construction

For every integer `q>=6`, set

```text
s = 4q+2,
F = 13s-1,
m = 4s.
```

Define residue sets in `[0,s-1]=[0,4q+1]` by

```text
A_q = [0,q-2] union [2q+1,2q+4],

B_q = [q-1,q+1]
      union [q+3,2q]
      union {3q-1}
      union [3q+3,4q+1].
```

The proposed semigroup has the finite membership pattern

```text
{0},
4s + A_q,
[5s,6s-1],
6s + B_q,
no members in [7s,8s-1],
8s + C_q, where C_q = [0,s-1] minus (s-1-A_q),
the gap 9s-1,
[9s,13s-2],
the Frobenius gap 13s-1,
and the full conductor tail from 13s onward.
```

Equivalently, the lower three nonzero blocks should generate exactly this membership pattern.
The normalized ideal is `I_q=(1,t^s)` over the associated localized semigroup ring.

## Why this formula was selected

The `s=30` (`q=7`) and `s=34` (`q=8`) density-optimal Route K models have exactly these interval
sets. The formula is therefore inferred after EXP-006 and is not retroactively part of that
experiment. The threshold `q>=6` is declared because at `q=5` the proposed sets meet at residue
`14`, violating the Route K deduction `A intersect B` is empty.

## Predictions

- P1: for every `q=6,...,100`, the formula defines a closed symmetric numerical semigroup with
  multiplicity `4s`, Frobenius `13s-1`, conductor `13s` and the displayed lower-block generators.
- P2: `I_q` is nonprincipal and rigid for every tested `q`, with exact equality `D=E+E` through
  `2F+1` and the standard proved tail.
- P3: the construction is outside the generalized-arithmetic-sequence positive family for every
  tested `q`.
- P4: `q=5` is rejected by the declared block-overlap obstruction; no lower threshold is claimed.
- P5: a theorem claim requires a symbolic interval proof of closure, symmetry and every layer of
  `D=E+E` for all `q>=6`. A finite sweep alone cannot confirm the family.
- P6: the exact implementation independently regenerates the two source models at `q=7,8` and
  rejects at least one corrupted interval endpoint.

## One-sidedness

- A failed exact instance refutes the proposed family formula and records the first invariant and
  witness.
- Passing the finite sweep establishes only those finite instances.
- Passing the symbolic interval verifier, together with a readable derivation of its affine
  endpoint obligations, proves the construction for all integers `q>=6` within the same monomial
  ideal class as EXP-005 and EXP-007.
- This experiment does not resolve the original Huneke-Wiegand conjecture for arbitrary modules or
  rings. It produces further counterexamples inside the already disproved general conjecture.

## Premise dependencies

- The finite `D=E+E` dictionary and conductor tail are supported by EXP-001 through EXP-003.
- The exact SAT encoding and independent proof loop are supported by EXP-004, EXP-005 and EXP-007.
- The Route K block deductions and finite recurrence are supported by EXP-006 and its independent
  audit.
- Priority for the first public counterexample remains with Son Pham. This proposed family is a
  CAOS extension, not a rediscovery of the seed.

## Method and adversarial validation

1. Construct the proposed finite mask directly from the affine interval formula.
2. Independently generate the semigroup from the lower blocks and compare masks through the
   conductor.
3. Apply the standard-library symmetry, closure, minimal-generator and rigidity checkers.
4. Record normalized `A`, `B`, `C`, generator counts, membership hashes and first failures.
5. Build a separate affine-interval proof checker. It must reduce each closure and `D=E+E` layer
   to explicit interval inclusions whose endpoint inequalities are proved for `q>=6`.
6. Corrupt one endpoint in `A` and one selector pair in `B`; both must be rejected.
7. Run an exact generalized-arithmetic presentation search on the finite regression instances and
   give a parameter-level exclusion proof before a theorem claim.

## Budget and stop rules

- Finite sweep: `q=5,...,100`, under five minutes total.
- Symbolic interval proof: under thirty minutes; no SMT result without extracted endpoint
  obligations counts as a proof.
- CPU only, exact integer and Boolean arithmetic, deterministic order, no random seeds.
- Stop at the first failed predicted instance and write a refutation verdict before changing any
  interval. A modified formula is a new experiment.

## Exploration moment

The new viewpoint is to quotient out the large forced membership blocks and treat rigidity as a
small additive-basis identity on residue intervals. The construction is designed so symmetry fixes
`C_q` and half of `B_q`, while the remaining proof burden becomes finitely many affine interval
sums. This is the recognition lens applied to the Kunz/block face exposed by Route K.
