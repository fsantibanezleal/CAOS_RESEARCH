# EXP-058 verdict

Date: 2026-09-05. Status: **REFUTED** on P1 at `p=8`. P2 is
**NOT APPLICABLE: NO INTEGRAL WITNESS**.

The complete declared radius-two original source span does not contain `2eta_8`, even over the
rationals. The run stopped at this first refutation. Parameters `p=9,10` were not evaluated.

## Exact result

| Radius | Source columns | Complete boundary rows | Nonzero incidences | Separating dual support |
|---:|---:|---:|---:|---:|
| 1 | 47 | 240 | 306 | 14 |
| 2 | 330 | 1803 | 2669 | 40 |

Both neighborhoods completed inside the declared caps. For each one, an explicit integer dual
satisfies `lambda M_local=0` on every selected original source column and
`lambda(2eta_8)=4`. This independently checkable contradiction proves rational inconsistency
without relying on a rank computation. The radius-two dual has 35 `D` rows and five `K` rows,
with every nonzero coefficient equal to `+1` or `-1`.

This refutes the prescribed local search prediction, not the existence of a source in the full
original domain. No statement for every parameter is inferred from the `p=8` obstruction.

## Independent audit and tests

The independent coefficient-first inverse-incidence enumeration reconstructs both complete
neighborhoods and agrees with every stored source label and every full boundary coefficient.
The independent right-to-left differential also verifies both original-coordinate residuals and
both annihilating integer duals, including their nonzero target pairing. A deliberate increment
of a nonzero dual coefficient is rejected in each case.

The audit status is `INDEPENDENT_AUDIT_PASS`, but its P2 status is
`NOT_APPLICABLE_NO_INTEGRAL_WITNESS`; zero integral parameters were verified. No independent
rank computation or successful source-coefficient mutation test is claimed. The focused producer
suite passes 12 tests, including exact rational-section classification, dual certificates,
inverse-face verification, cap behavior, and canonical artifact integrity. Ruff passes for
the producer, auditor, and focused test file.

The primary [results.json](artifacts/results.json) has SHA-256
`710029d2460e4a6b7fc319161bb337740bcb35b2ec961bec532db0b4e99127cd` and internal hash
`d6abcd05b24a42f7b5b066e2b308cee6034d2fe938f55bd756c1e1e44ee2d3ff`.
The independent [audit-results.json](artifacts/audit-results.json) has SHA-256
`7be205d2e6c86a128a5f5047531e9b488e534ce0defa9be8bf7cd64b2bbd9661` and internal hash
`c6fa6f017aa590d80fb1cd18a820c54a522c1fc86674e04e5ddd5da98cc50fe5`.

The producer and auditor SHA-256 hashes are respectively
`10c812fff961c2dca780986726b8f9be254f2a05472877cde925db5b56972037` and
`7d9cbce1a47603923b832e47d82c858bafabd76e14f7772870952dc425f7b024`.

## How could this be wrong?

- Both implementations import the original algebraic coefficient-module model; the audit does
  not independently prove that model from the semigroup definition.
- The local enumeration must include all columns incident to each declared frontier and all
  their boundary rows. Independent reverse-direction enumeration and coefficient comparison
  address this exact failure mode.
- The dual annihilates the selected columns only. Extending it by zero to other original rows
  does not make it a functional on the full cokernel.
- The nonzero integer pairing is not a proof of the intended characteristic-two torsion class,
  and no all-parameter dual formula is established.

## Consequence and next gate

The [escaping-column lemma](proof.md) gives a sharper next action: any full source for
`2eta_8` must use a column outside the radius-two set with nonzero pairing against the stored
dual. Prioritize such columns in a separately declared search, or construct an explicit mixed
source family symbolically. No radius-three search or escaping-column enumeration was run here.

The two uniform endpoint identities remain intact. Nonzero class, uniform order two, a second
class, and an upper bound remain open. This finite local refutation does not trigger a manuscript
or Zenodo version on its own.
