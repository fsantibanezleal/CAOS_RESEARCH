# EXP-070 verdict: CONFIRMED

Date: 2026-11-14. Hypothesis frozen at `a1974bc0` before any code was written. Every number below is read from
`artifacts/results.json` and `artifacts/run-log.txt`; `run.py` reproduces them from the repository root (exact
integer arithmetic, no random choice; only the times vary). The run took 668 s with at most 10 worker processes,
inside the three-hour budget; B4 was run because B1 to B3 finished far inside two hours.

## Result

On all 48 gluings `Gamma = a1*Gamma_B + a2*S` (B1 to B3: 36 cases; B4: 12 cases), the torsion-length law of EXP-068
holds by the producer's direct tensor computation and agrees with an independent auditor that shares no code with
it; the Huneke-Wiegand predicate follows the factor rule; `mu(A) = mu(A_B)*mu(A_S)`; and the Hilbert identity holds.
36 of the 48 have a factor that is a counterexample (Pham `(0,14)`, `C_4` with `(0,24)`, `C_5` with `(0,30)`),
including the 18 cases with the principal partner ideal, in which the extension is itself a counterexample
(non-principal, torsion length 0).

## Prediction table

| prediction | outcome | evidence |
|---|---|---|
| P1 torsion-length law (direct on the glued semigroup against the law from the factors) | PASS, 48 of 48; for the 36 counterexample-factor cases the law is `a2*l(tau(T_S))` as predicted; 30 cases have nonzero torsion, 6 (B3 with partner ideal `(0,1)`) have torsion in both factors so the cross term is exercised | `artifacts/results.json`, `cases[*].producer.p1`, `torsion_law`, `torsion_direct` |
| P2 characterization (predicate equals the factor rule, agrees with `l(tau(T)) > 0`, `mu = mu*mu`; counterexample factor with principal partner ideal gives a counterexample; non-principal Huneke-Wiegand partner ideal gives Huneke-Wiegand) | PASS, 48 of 48, including `p2_special_rule` on every case: 18 of 18 counterexample-factor cases with principal partner are non-principal with torsion 0 (`summary.extension_is_itself_counterexample = 18`); every case with a Huneke-Wiegand partner ideal is Huneke-Wiegand | `cases[*].producer.p2`, `p2_special_rule`, `summary` |
| P3 independent route (EXP-068 `audit.py`: torsion length, predicate; here also `mu` and Frobenius) | PASS, 48 of 48 completed within 900 s (slowest 70 s), all agree; none listed as not completed | `cases[*].audit`, `audit_agrees`, `summary.cases_audit_not_completed = []` |
| P4 Hilbert identity | PASS, 48 of 48; the Frobenius number measured on the glued semigroup equals `a1*F1 + a2*F2 + a1*a2` on all 48 | `cases[*].producer.hilbert_identity`, `frobenius_matches` |
| C1 not a gluing | PASS: for B1 and B2 with `<2,3>`, replacing `a1 = 2` by the gap 1 (coprime to `a2` = 57 and 97) was not refused by the constructor and the Hilbert identity broke in both | `controls.c1` |
| C2 not an extension | PASS: B1 with `<2,3>` and the principal partner ideal, minimal generators `0, 28`; the true ideal is an extension, the perturbed `(0, 29)` is not; the perturbed ideal is Huneke-Wiegand (reported, not assumed) with 2 generators | `controls.c2` |

Premises recomputed in the run (`summary.premises`): Pham `(0,14)` is not Huneke-Wiegand with factor torsion length 0
(Frobenius 181, multiplicity 56); `C_4` with `(0,24)` the same (Frobenius 311, multiplicity 96); Pham `(0,1)` is
Huneke-Wiegand with factor torsion length 14. B4 (`C_5`, Frobenius 389, multiplicity 120) had the same status
(`cases[*].spec_factors.b`). Partner ideals: `(0)` is principal on all six partners and `(0,1)` is
Huneke-Wiegand on all six (computed by the producer and, independently, by the auditor, `audit.factor_hw`).

Cost model: the pairs scanned by the direct torsion computation range from 158,379 (B3 x `<2,3>`) to 3,470,379
(B4 x `<3,5>`), with windows from `[-11, 1996]` to `[-249, 6514]` (`cases[*].producer.pairs_scanned`, `window`).
These gluings have Frobenius number below 3,000, so the cost stays small; the instances with two counterexample
factors (Frobenius 23,645 and 53,599) are not computed, as declared in the hypothesis.

## Adversarial-validation record

- "The producer and auditor agree only because they share code." The auditor `auditor.py` imports only the standard
  library and EXP-068 `audit.py`; a unit test checks that neither file imports `hwcert` or the producer module. The
  auditor rebuilds the glued generators, the extension generators, the minimal generators and the Frobenius number
  from the declared inputs, not from the producer; it agrees on torsion length, predicate, `mu` and Frobenius number
  in 48 of 48.
- "The law holds only on factors without counterexamples." 36 of the 48 cases have a counterexample factor, and the
  law, the characterization and the audit pass on all of them.
- "The checks cannot fail." C1 and C2 each broke the property they test, and the first shows the Hilbert check
  rejects a non-gluing; the unit test `test_producer_and_auditor_agree_on_a_case_with_torsion_from_the_partner`
  exercises a case with torsion.
- The cost model (`pair_count`) is checked against a brute-force enumeration of the loops of `tensor_torsion` in a
  unit test.

## Consequences for the papers

The gluing paper (`gluing-extensions`, Corollary 5.2) can cite this experiment for the case it is about: gluings in
which a factor is a counterexample, with the extension itself a counterexample when the partner ideal is principal,
by two routes that share no code. It can say that the law was checked on 36 gluings with a counterexample factor and
12 with the Huneke-Wiegand control (up to Frobenius number below 3,000), and that the two-counterexample instances
(Examples 5.4 and 5.5) remain consequences of the proved theorem and of the partition criterion, not of a direct
torsion computation. The curvilinear paper is not affected.

## How could this be wrong?

- Producer and auditor take the same inputs (generators of both factors, declared ideals, `a1`, `a2`, chosen by the
  hypothesis rule); a mistake in the rule would affect both. The rule satisfies the gluing conditions (`a1` in `S`,
  `a2` in `Gamma_B`, gcd 1), and C1 shows a violation is detected.
- All 48 partner choices are small semigroups; the partner torsion is at most 4 blocks, so the cross term is
  exercised only in the six cases with `Gamma_P` and `(0,1)`.
- Both routes enumerate degrees up to a bound derived from the same cost argument (EXP-068, `tensor_torsion`
  docstring); the auditor's bound is its own (`audit.direct_torsion`), but a shared flaw in the argument would not be
  caught by agreement.
- A pass on 48 cases is evidence, not a proof; the proof is EXP-068's.
