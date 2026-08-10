# EXP-004 - certified reproduction of the F<69 frontier

Declared 2026-08-02 before installing CaDiCaL or DRAT-trim, before implementation, and before any
frontier run. Phase HW-P3. Backlog HWB-004.

## Question

Can CAOS independently reproduce the published statement that every two-generated monomial ideal
over every symmetric numerical semigroup with Frobenius number below 69 satisfies the
Huneke-Wiegand property, with complete enumeration and independently checked UNSAT certificates?

For a symmetric semigroup `Gamma` and a gap `s`, define

```text
E(n) = Gamma(n) and Gamma(n+s)
D(n) = Gamma(n) and Gamma(n+s) and Gamma(n+2s).
```

The ideal `(0,s)` is a counterexample exactly when `D=E+E`. EXP-003 proves that checking through
`2F+1` plus the conductor tail is complete.

## Premise dependencies

- EXP-001 confirms the candidate equality and a known-positive control by independent algebraic
  and finite routes.
- EXP-003 confirms the finite `D=E+E` encoding, exact tail, model extraction, and corrupted-model
  rejection. It does not supply a lower bound.
- García-Sánchez--Leamer Example 23 is the published `F<69` target, not evidence for this run.
- Blanco--Rosales Theorem 9 is the primary completeness theorem for Route A.
- The mathematical correctness of the custom CNF translation is a hypothesis to be attacked by
  Route A, small brute-force controls, and the known candidate.

## Invariant-first reduction

Symmetry forces `F` odd and genus `(F+1)/2`. Therefore the complete range is
`F in {1,3,...,67}`. Values above `F` are automatically in Gamma, and every relevant shift is a
gap `1 <= s <= F`. No cheaper invariant decides the rigidity equality itself.

## Route A: theorem-complete enumeration

Implement Blanco--Rosales Theorem 9 directly with Python standard-library integer sets. Starting
from `C(F)`, enumerate every tree node exactly once. Independently validate every node for
Frobenius number, symmetry, genus, closure, minimal generators, and unique parent. Test every gap
with the EXP-003 finite equality checker and retain an explicit missing-`D` witness for every
positive case. Do not call NumericalSgps or upstream candidate code.

## Route B: proof-carrying CNF

Generate DIMACS CNF independently of Z3 for every pair `(F,s)`. Use Tseitin equivalences for
`E(n)`, `D(n)`, and each decomposition pair, closure and symmetry clauses, and the complete
`0..2F+1` rigidity window. CaDiCaL must return UNSAT and emit a DRAT proof. DRAT-trim must accept
every proof against the exact CNF. Store heavy CNFs/proofs outside Git under
`E:/_Datos/caos-research/huneke-wiegand/EXP-004-certified-f69-frontier/`; commit a manifest with
sizes and SHA-256 hashes.

## Committed predictions

- P1: Route A enumerates exactly six symmetric semigroups at `F=11`, matching Blanco--Rosales
  Example 10, and finds no counterexample for any of their gaps.
- P2: Route A exhausts every odd `F<69` and finds zero counterexamples; every tested positive case
  carries an explicit first value in `D` missing from `E+E`.
- P3: a deliberately invalid `F=11` tree mutation obtained by replacing 10 with 1 in the root is
  rejected by the semantic validator before it can enter the frontier.
- P4: Route B is SAT for the unpinned `(181,14)` formula; its extracted model passes the
  solver-independent EXP-003 checker.
- P5: Route B is UNSAT for every `(F,s)` with odd `F<69` and `1<=s<=F`; every result has a DRAT
  proof accepted by DRAT-trim.
- P6: Routes A and B agree on the complete frontier, tool versions and formula/proof hashes are
  recorded, and interrupted suites resume from an atomic checkpoint without changing prior hashes.

## One-sidedness

A PASS of P1-P6 proves, conditional only on the cited enumeration theorem and independently
checked CNF certificates, that no symmetric numerical semigroup with `F<69` has a rigid
nonprincipal two-generated monomial ideal. It reproduces the published frontier but does not
extend it.

A valid model below 69, accepted by both semantic routes, would refute the published finite claim.
A route mismatch, rejected proof, timeout, incomplete manifest, or invalid checkpoint makes the
experiment INCONCLUSIVE as an instrument and blocks any frontier statement.

## Compute budget and kill criteria

- Smoke gate: `F<=11`, flushed progress within five seconds, checkpoint written, total under two
  minutes.
- Route A full gate: 30 minutes wall time, checkpoint after each `F`.
- Route B full gate: 90 minutes total, 300 seconds per query, checkpoint after every checked proof.
- Any query hitting its cap is recorded as UNKNOWN; the suite stops without a mathematical PASS.
- No GPU. Exact integer and Boolean arithmetic only. Deterministic ordering and seeds.

## Publication scope

Successful reproduction alone does not trigger a manuscript or Zenodo version. A separately
declared extension beyond 69 or a new structural theorem is required for the novelty gate.
