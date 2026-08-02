# EXP-005 verdict - CONFIRMED

Run date: 2026-08-02. Phase HW-P3. Backlog HWB-005.

## Main result

The least Frobenius number of a symmetric numerical semigroup admitting a rigid nonprincipal
two-generated monomial ideal is

```text
F_min = 181.
```

The first validated pair occurs at shift `s=14`, and the decoded semigroup is exactly Son Pham's
public candidate. Thus the public example is Frobenius-minimal within this numerical-semigroup,
two-generated-monomial-ideal class.

## Proof chain

1. A symmetric numerical semigroup has odd Frobenius number.
2. EXP-004 independently proves nonexistence for every odd `F<=67` by both complete theorem-tree
   enumeration and checked fixed-pair DRAT proofs.
3. EXP-005's selector formula is equisatisfiable with existence of a symmetric semigroup and a gap
   `s` satisfying `D_s=E_s+E_s`; `encoding-proof.md` records both directions and the finite tail.
4. For every odd `F=69,71,...,179`, CaDiCaL returned UNSAT and DRAT-trim accepted the proof
   against the exact selector CNF.
5. At `F=181`, the selector CNF returned SAT with `s=14`. The standard-library checker validated
   semigroup closure, symmetry and the full rigidity window/tail. A separately generated fixed-pair
   CNF returned the same semigroup, which also equals the public candidate vector.

These steps cover every possible positive Frobenius number below 181 and exhibit a valid example
at 181.

## Prediction table

| prediction | result | decisive evidence |
|---|---|---|
| P1 | PASS | all 34 selector formulas at odd `F<=67` have accepted UNSAT proofs; 136-file audit passes |
| P2 | PASS | selector `F=181` is SAT at `s=14`; exact semantics pass and the public vector is recovered |
| P3 | PASS | selector and independently generated fixed-pair formulas return the same valid `(181,14)` model |
| P4 | PASS | theorem-tree and selector routes agree at `F=69,71,73,75` |
| P5 | PASS | strict increasing scan has 56 accepted UNSAT proofs for `69<=F<=179`, then validated SAT at 181 |
| P6 | PASS | all checkpoints, tool identities, hashes, model checks and three independent audits pass |

## Selector search evidence

```text
requested odd values:       57  (69 through 181)
UNSAT_VERIFIED:             56  (69 through 179)
SAT_VALIDATED:               1  (181, shift 14)
UNKNOWN:                     0
wall time:            4,303.86 seconds
CNF bytes:             169,745,433
DRAT proof bytes:      586,785,257
aggregate SHA-256:     0f580de2707a00fdd52e1b3c04e7767b97ce7b0a826593b119e9a49ae04da743
results SHA-256:       08e552a002644c747a9a474b11b9938f1c4c41f9687216b143e68d4d3f9c6e1f
```

The slowest solver query was `F=175` at 218.83 seconds, below the 600-second cap. The full search
auditor rehashed 228 expected external files totaling 760,081,739 bytes: zero missing files, zero
hash mismatches, zero bad status markers and zero semantic failures. It independently reproduced
the aggregate and strict minimality order.

The selector-frontier calibration separately rehashed 136 files for all odd `F<=67`, and the
standalone `F=181` calibration rehashed four files and recovered the public vector. Both audits
pass.

## Independent theorem-tree cross-check beyond 69

The Blanco--Rosales route was continued without using SAT models:

| F | symmetric semigroups | gap cases | rigid cases | seconds |
|---:|---:|---:|---:|---:|
| 69 | 11,276 | 394,660 | 0 | 137.00 |
| 71 | 19,812 | 713,232 | 0 | 235.37 |
| 73 | 25,405 | 939,985 | 0 | 333.21 |
| 75 | 23,297 | 885,286 | 0 | 330.10 |

This adds 79,790 explicitly enumerated semigroups and 2,933,163 explicit gap checks beyond the
published boundary, all agreeing with the selector proofs. The tree route was stopped after the
declared initial cross-check interval because proof-carrying SAT already certifies the full lower
range and further enumeration would duplicate it at rapidly increasing cost.

## Attribution and exact scope

Son Pham retains discovery priority for the counterexample and public candidate. Professor Craig
Huneke's verification remains independent external evidence. CAOS's result is the certified
Frobenius-minimality extension and its reproducible proof suite; it must never be presented as
discovery of the counterexample itself.

The result does **not** prove uniqueness at `F=181`, minimal multiplicity, minimal embedding
dimension, minimal ideal shift, or minimality among arbitrary Gorenstein domains and modules. It
does not repair the disproved conjecture. Those are separate questions.

## Publication decision

Unlike EXP-004, EXP-005 supplies validated novel mathematics: a complete certified lower range and
the exact least Frobenius value. The manuscript and Zenodo gate is triggered. Publication must
include the attribution boundary, equisatisfiability proof, toolchain identities, compact manifests,
external proof archive hashes and instructions for independent verification.
