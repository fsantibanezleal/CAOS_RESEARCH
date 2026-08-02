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

## Interpretation and publication

A failed fixed-offset lift is still useful if it identifies the load-bearing residue constraint.
A finite list of SAT instances is experimental evidence, not an infinite family. Only a proved
parametric construction triggers a family manuscript claim; it must preserve Son Pham's discovery
priority for the seed and distinguish CAOS's extension.
