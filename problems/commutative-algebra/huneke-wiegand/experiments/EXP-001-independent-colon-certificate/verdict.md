# EXP-001 verdict - CONFIRMED ON P1-P6

Date: 2026-08-01. Hypothesis committed before code/run at `8dae63c`. Final runner commit:
`f470df2` plus the current artifacts.

## Result

The candidate is independently reproduced without importing or executing upstream verifier code.

| prediction | outcome | evidence |
|---|---|---|
| P1 | PASS | finite route: F=181, conductor=182, genus=91, symmetric; Singular toric quotient dimension 1 |
| P2 | PASS | colon minima are B and B+14 exactly |
| P3 | PASS | Singular intersection modulo product and product modulo intersection both simplify to zero |
| P4 | PASS | `<4,5>` control has unequal ideals; residues `x5^3`, `x4^4` |
| P5 | PASS | standard-library finite route agrees and finds the 49 minimal exponents on each side |
| P6 | PASS | mutated expected colon set is rejected |

Singular/4ti2 produced a 322-generator standard basis for the toric ideal and completed in about
11 seconds. The finite checker completed immediately. The control completed in under one second.

## Instrumentation incidents

1. Attempt 1: Debian's Singular helper directory was absent from PATH, so `toric_ideal` was not
   invoked. The runner now treats any Singular `?` diagnostic as fatal.
2. Attempt 2: the DU backend returned a dimension-zero ideal and was rejected by P1. BLR, justified
   by the positive grading row, returned dimension one.
3. Attempt 3: both reduced differences consisted entirely of zero slots, but scalar ideal equality
   misclassified the representation. Simplifying zero generators before testing fixed the gate.

All failed raw outputs are preserved under `artifacts/attempt-*`. None was accepted as evidence.

## Scope

This independently confirms the finite colon certificate and, together with the published
Huneke-Iyengar-Wiegand theorem chain, validates the public counterexample at replication strength.
It does not establish discovery priority, minimality, a family, or peer review.
