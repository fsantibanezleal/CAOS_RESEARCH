# EXP-005 - minimal Frobenius search beyond the published frontier

Declared 2026-08-02 before implementation or any computation with the selector encoding. Phase
HW-P3. Backlog HWB-005. Execution is gated on a conclusive EXP-004 verdict.

## Question

What is the least odd Frobenius number `F >= 69` for which a symmetric numerical semigroup
`Gamma` and a gap `s` give a rigid nonprincipal two-generated monomial ideal `(0,s)`? In
particular, is the public `(F,s)=(181,14)` example minimal by Frobenius number?

## Change of viewpoint

EXP-004 asks one SAT question for every fixed pair `(F,s)`. That is appropriate for an auditable
reproduction but duplicates the semigroup constraints `F` times. EXP-005 instead introduces
one-hot selector variables `q_s` and asks a single existential question per `F`:

```text
there exist Gamma and exactly one s in [1,F]
such that Gamma is symmetric, s is a gap, and D_s = E_s + E_s.
```

Guarded Tseitin variables encode `q_s and Gamma(n+s)` and
`q_s and Gamma(n+s) and Gamma(n+2s)`. Their disjunctions define `E(n)` and `D(n)` exactly. A SAT
model therefore identifies both the semigroup and the selected shift. An UNSAT proof rules out all
shifts for that `F` at once.

## Independent routes

- Route S: direct selector-DIMACS, CaDiCaL, and DRAT-trim. Every SAT model is decoded and checked
  with the solver-independent exact semigroup/rigidity implementation. Every UNSAT result must
  have a DRAT proof accepted against the exact CNF.
- Route T: Blanco--Rosales complete-tree enumeration for the initial extension values, continued
  only while its measured growth remains within the declared wall budget. Every gap is checked.
- Fixed-pair adversary: any selector SAT model is regenerated as the EXP-004 fixed `(F,s)` CNF and
  must be SAT with an independently valid decoded model.

## Committed predictions

- P1: selector formulas at every odd `F<=67` are UNSAT, and every proof is accepted by DRAT-trim.
- P2: the selector formula at `F=181` is SAT and returns a semantically valid rigid pair. The model
  need not equal the public candidate; if it differs, both models are retained.
- P3: selector and fixed-pair encodings agree at the known `(181,14)` calibration and at every
  selector-discovered SAT frontier value.
- P4: Route T and Route S agree for every fully completed odd `F>=69` in the tree budget.
- P5: the search scans odd `F` in strictly increasing order and stops at the first validated SAT
  value. All smaller values have checked UNSAT proofs, not only solver status codes.
- P6: checkpoints, exact formula/proof/model hashes, pinned tool identities, elapsed time, and the
  honest completed frontier survive interruption and resume without changing prior hashes.

## Interpretation

If the first validated SAT value is `F0`, the accepted proofs for all odd `F<F0`, symmetry's odd
Frobenius constraint, and the independently checked model at `F0` establish Frobenius minimality
within the two-generated monomial-ideal problem. If `F0=181`, this proves minimality of the public
Frobenius value but not uniqueness of its semigroup or shift.

If the run reaches a declared cap without SAT, only the completed checked interval is claimed. A
timeout, rejected proof, invalid decoded model, route mismatch, or hash mismatch is INCONCLUSIVE
for that value and blocks every larger minimality claim.

## Compute budget and stages

1. Regression: selector `F<=11`, under five minutes total.
2. Calibration: selector `F=181` and fixed `(181,14)`, under ten minutes each.
3. Published frontier: one checked proof per odd `F<=67`, under 60 minutes total.
4. Novel frontier: odd `F=69,71,...,181`, six hours wall cap, 600 seconds per `F`; stop at the
   first independently validated SAT model.
5. Tree cross-check: start at `F=69`; stop before the next `F` when an individual enumeration
   exceeds 30 minutes or projected memory exceeds 8 GiB. A budget stop is not a failed prediction.

No GPU is required. Heavy CNFs and proofs live outside Git under
`E:/_Datos/caos-research/huneke-wiegand/EXP-005-minimal-frobenius-search/`; Git retains code,
compact results, hashes, and verdicts.

## Publication gate

A certified extension beyond 69 is novel computational evidence and triggers a manuscript update
assessment. A proof of the least Frobenius value is stronger and triggers manuscript plus Zenodo
review. Neither upload nor release occurs until the result, attribution, certificate manifest,
claim language, and repository state pass the publication methodology.
