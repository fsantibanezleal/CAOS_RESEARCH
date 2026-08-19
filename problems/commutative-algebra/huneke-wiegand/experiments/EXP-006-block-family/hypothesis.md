# EXP-006 - block/Kunz family search

Declared 2026-08-02 before implementation or parameter sweeps. Phase HW-P4. Backlog HWB-006.
Execution is gated on EXP-005's selector calibration at `F=181`; the minimality search itself keeps
priority.

## Question

Does the public rigid pair belong to an infinite or recurrent family organized by the relations

```text
multiplicity m = 4s,
Frobenius F = 13s-1,
```

and by short membership blocks between `4s` and `7s`?

## Exact seed decomposition

At `s=14`, the displayed minimal generators are exactly

```text
4s + A,       A = {0,1,2,7,8},
5s + [0,s-1],
6s + B,       B = {3,5,6,9,11,12,13}.
```

The seed also has `F=13s-1`. This numerical identity is an observation to explain, not evidence
that the same fixed offsets work for another parameter.

## Routes

- G, fixed-offset falsification: generate the numerical semigroup from the displayed template for
  even `s>=14`, then check conductor, Frobenius, symmetry, minimal generators and exact rigidity at
  shift `s`. Retain the first failed invariant and witness.
- K, constrained block SAT: if Route G fails, keep `m=4s` and `F=13s-1` but make level-4 and
  level-6 residue membership Boolean. Impose closure, symmetry and rigidity, minimizing departure
  from the seed's block densities. Decode with the independent exact checker.
- A, algebraic extraction: only after at least three non-seed exact instances, infer residue rules
  and prove closure, symmetry and `D=E+E` by interval/residue arguments. Computational recurrence
  alone is not an infinite family.

## Committed predictions

- P1: Route G at `s=14` reconstructs the public semigroup exactly, including its 26 minimal
  generators, `F=181`, symmetry and rigidity.
- P2: the naive fixed-offset template is not accepted as a family merely from the seed; either it
  fails by `s=28` with an explicit first invariant witness, or every even `s=14,...,28` passes all
  exact checks and becomes a stronger recurrence target.
- P3: every Route K SAT model passes the standard-library semigroup and full-window/tail rigidity
  checks; corrupted block membership is rejected.
- P4: no family claim is made without at least three non-seed instances and a symbolic proof. If
  fewer exist in the declared range, the result is an isolation/obstruction map.
- P5: every proposed instance is tested against generalized-arithmetic-sequence membership and
  current positive classes; excluded hypotheses are recorded explicitly.
- P6: deterministic parameter order, hashes, checkpoints and negative witnesses make both a
  positive recurrence and a failed ansatz reproducible.

## Budgets and stop rules

- Route G: even `s=14,...,100`, under ten minutes total.
- Route K: even `s=16,...,40`, 20 minutes per parameter and four hours total.
- Route A: no compute cap, but it begins only after the recurrence gate in P4.
- Stop a parameter at the first exact semantic failure; do not tune the template after seeing a
  result without declaring a new versioned hypothesis.

## Binding Route K execution refinement (2026-08-10, before Route K code or runs)

Route K asks the following broad existence question for each even `s=16,18,...,40`, in ascending
order. Set `F=13s-1`. Does there exist a symmetric numerical semigroup `Gamma` such that

```text
multiplicity(Gamma) = 4s,
[5s,6s-1] is contained in Gamma,
s is a gap, and
I = (1,t^s) is rigid, equivalently D=E+E?
```

No cardinality or fixed-offset restriction is imposed on the variable level-4 and level-6
membership blocks in this primary decision layer. This makes an UNSAT result stronger than a
density-restricted search and prevents an arbitrary optimization convention from hiding a model.
If a parameter is SAT, a secondary deterministic density-ranking layer may select a model closest
to the seed densities for structural comparison; that ranking is descriptive and is not needed for
the existence decision.

### Invariant-first deductions

These deductions precede computation and become independent decoded-model checks.

1. Since `F=13s-1` must be odd for a symmetric numerical semigroup, `s` must be even. This is why
   the declared sweep has no odd parameters.
2. Multiplicity `4s` and symmetry force `[9s,13s-2]` to be members and force `9s-1` to be a gap.
3. Full membership of `[5s,6s-1]` and symmetry force `[7s,8s-1]` to be gaps.
4. If `B={r:6s+r in Gamma, 0<=r<s}`, symmetry gives exactly one of `r` and `s-1-r`
   in `B`. Hence `|B|=s/2`; the seed's level-6 density is forced, not an optimization target.
5. If `A={r:4s+r in Gamma, 0<=r<s}`, then every `4s+r` with `r in A` lies in `E` because
   the level-5 block is full. The least element of `E` is `4s`, so `E+E` has no value below
   `8s`. Rigidity therefore forbids `4s+r` from lying in `D`; equivalently `A` and `B` are
   disjoint.

None of these invariants alone decides existence. They materially reduce the plausible block
geometry and provide cheap witnesses against malformed solver models.

### One-sidedness and premise dependencies

- A checked SAT model proves existence only at that finite parameter. Three non-seed models open
  Route A but do not prove an infinite family.
- A checked UNSAT certificate proves nonexistence only inside the stated `m=4s`, `F=13s-1`, full
  level-5 scaffold. It does not rule out other Frobenius laws, multiplicities, or block shapes.
- The exact `D=E+E` encoding and decoder are supported by EXP-003 calibration, EXP-004 proof
  reproduction, EXP-005 minimum search, and EXP-007 minimum-layer classification.
- The public seed and its exact block decomposition are supported by EXP-001 and Route G's `s=14`
  reconstruction.
- The fixed-offset failure that triggers Route K is supported by `route-g-verdict.md`.

### Adversarial and operational gates

- Calibrate the complete Route K formula at `s=14`; it must decode to the public semigroup, which
  EXP-007 proves is the only possible global model at `F=181`.
- Decode every SAT result with the standard-library semigroup and full-window/tail rigidity
  checker, then check all five invariant deductions above.
- Reject a deliberately corrupted forced block fact through a separate constraint checker.
- For every UNSAT result, retain the solver proof and require acceptance by the pinned independent
  proof checker. A timeout is `UNKNOWN`, never UNSAT.
- Emit flushed progress and an atomic checkpoint in the `s=14` smoke test before the declared
  range runs. Heavy CNF, proof, and solver-output files live outside Git and are hash-manifested.
- Retain the original 20-minute per-parameter and four-hour total caps. On a cap, persist the exact
  last completed parameter and conclude only that the remaining declared cases are unresolved.

### Source-complete and exploration record

The 2026-08-10 refresh found no newer commit, issue, pull request, public family, or certified
extension in the candidate repository or current primary-source search. The candidate repository's
latest commit remains the 2026-08-01 attribution of Professor Huneke's independent verification.
The March 2026 revision of Landeros et al. still gives a positive theorem for generalized
arithmetic sequences, a class already excluded for the seed. The useful new viewpoint this round
is that Route K is not a free two-block search: symmetry fixes the level-6 density and rigidity
couples the two free blocks by disjointness.

## Interpretation and publication

A failed fixed-offset lift is still useful if it identifies the load-bearing residue constraint.
A finite list of SAT instances is experimental evidence, not an infinite family. Only a proved
parametric construction triggers a family manuscript claim; it must preserve Son Pham's discovery
priority for the seed and distinguish CAOS's extension.
