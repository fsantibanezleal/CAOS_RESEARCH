# EXP-068 verdict: CONFIRMED

Date: 2026-10-30. Hypothesis frozen at `ae0eacc7` before any code was written; proof written before
the run was read.

## Result

For every gluing `Gamma = a1*Gamma1 + a2*Gamma2` and relative ideals `A_i` of `Gamma_i`, the extension
`A = a1*A1 + a2*A2` satisfies `I_A = I_(A1) (x)_(k[y]) I_(A2)` and

`I_A (x)_R I_(A*) = T1 (x)_(k[y]) T2`, with `T_i = I_(A_i) (x) I_(A_i*)`,

so that `l(tau(T)) = a1*l(tau(T1)) + a2*l(tau(T2)) + sum_(j>=1) b1(j)*b2(j)`, `mu(A) = mu(A1)*mu(A2)`, and
`A` is Huneke-Wiegand iff `A1` or `A2` is a non-principal Huneke-Wiegand ideal ([proof](proof.md)).
The case García-Sánchez and Leamer (2012) Proposition 9 leaves open, both factors non-principal and
not Huneke-Wiegand, gives a counterexample. Two explicit four-generated counterexamples over
symmetric semigroups:

| instance | gluing | Frobenius | minimal generators of `A` | Huneke-Wiegand |
|---|---|---|---|---|
| Pham x Pham | `56*Gamma_P + 57*Gamma_P`, `A1 = A2 = (0,14)` | 23645 | `0, 784, 798, 1582` | no |
| Pham x EXP-009 (`p=4`) | `96*Gamma_P + 89*C_4`, `A1 = (0,14)`, `A2 = (0,24)` | 53599 | `0, 1344, 2136, 3480` | no |

## Prediction table

| prediction | outcome | evidence |
|---|---|---|
| P1 torsion-length law (direct tensor computation against the law from the factors) | PASS, 200 of 200 seeded cases; 33 cases with torsion in both factors, so the cross term is exercised | `artifacts/results.json`, `cases[*].p1` |
| P2 characterization and `mu(A) = mu(A1)*mu(A2)` (partition criterion against the factor rule and the torsion sign) | PASS, 200 of 200 | `cases[*].p2` |
| Invariant: Hilbert series `H_A(z) = H_A1(z^a1) H_A2(z^a2)(1-z^(a1*a2))` | PASS, 200 of 200 | `cases[*].hilbert_identity` |
| P3 four-generated counterexamples | PASS, both instances symmetric, Frobenius equal to `a1*F1 + a2*F2 + a1*a2`, four minimal generators, not Huneke-Wiegand; factors `(0,14)` and `(0,24)` not Huneke-Wiegand | `summary.p3_instances` |
| P4 controls | PASS: replacing `(0,14)` by the Huneke-Wiegand ideal `(0,1)` makes the extension Huneke-Wiegand; 30 of 30 pairs with `a1` not in `Gamma2` break the Hilbert identity; the extension test accepts the true ideal and rejects the perturbed `(0,784,798,1583)` (which is Huneke-Wiegand) | `summary.p4` |

Seed 20261030; 66 seconds of commodity CPU, inside the 20-minute budget.

## Independent audit

`audit.py` shares no code with `hwcert.gluing`: plain integer sets and breadth-first search. It
re-derives the Pham x Pham instance (Frobenius 23645, symmetric, minimal generators
`0, 784, 798, 1582`, not Huneke-Wiegand by the partition criterion) and recomputes the direct torsion
length on every eighth producer case: 25 of 25 agree with both producer routes
(`artifacts/audit.json`, `audit_pass: true`). A first auditor run stopped on an auditor defect (the
search for the least element of `A*` was bounded at 0); it was fixed before the recorded run.

## Scope and novelty boundary

- Proposition 9 and Proposition 10 of García-Sánchez and Leamer (arXiv:1211.4554v1) are re-proved as
  special cases; their credit is retained. EXP-067 is the case `Gamma2 = N`, `A2 = N`, and is a
  corollary of their Lemma 8(8) and Proposition 10.
- Sources searched for the factorization, the length law and the open case of Proposition 9:
  arXiv:1211.4554, arXiv:1305.4238, arXiv:1211.2896, arXiv:1808.06600; none states them. This is not a
  novelty proof.
- The characterization covers extension ideals. Ideals of the gluing that are not extensions are not
  covered, so the third Future Work question of García-Sánchez and Leamer remains open for them.
- Claims concern monomial (relative) ideals; a version for arbitrary modules would need `Hom` to
  factor over `k[y]` and is not claimed.

## How could this be wrong?

- The tensor isomorphism of Proposition 2 is standard multilinear algebra; the risk is in
  Proposition 1, which P1 and the Hilbert identity test case by case, and which the non-gluing control
  shows is sensitive to the gluing hypothesis.
- The direct tensor route truncates at `maxgen(A) + c(Gamma) + c(A*)`; the bound is proved in the
  docstring of `tensor_torsion` (anchors join through `w = maxgen + c(Gamma)`).
- Both computational routes rest on the definition of the tensor product and on Leamer's Theorem 1.4
  respectively; they agree on all 200 cases and on the published Pham counterexample.

## Consequence

Disposition `companion-manuscript`: the focused paper `gluing-extensions` v0.01 owns this theorem,
with EXP-067 as a credited corollary.
