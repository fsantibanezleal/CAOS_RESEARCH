# EXP-011 - uniform endomorphism overring of the infinite family

Declared 2026-08-10 before implementation or execution. Phase HW-P5, anatomy/invariant route.
Premise and source audit: `context/2026-08-10-exp011-endomorphism-family-preflight.md`.

## Question

Does the EXP-002 endomorphism-overring escape mechanism admit an exact formula for every member of
the EXP-009 family?

For every integer `p>=4`, retain the EXP-009 notation

```text
s=6p,
R_p=k[t^Gamma_p] localized at the positive-degree maximal ideal,
J_p=(1,t^s)R_p,
V_p=Gamma_p union (s+Gamma_p).
```

Let `Lambda_p=v(End_(R_p)(J_p))` and put

```text
Q_p = [p+1,2p-2] union {2p,4p}.
```

## Predictions

- P1: for every `p>=4`,
  `Lambda_p=Gamma_p union (7s+Q_p) union {13s-1}`.
- P2: `Lambda_p` has multiplicity `24p`, Frobenius number `54p-1`, conductor `54p`, genus
  `38p-1`, and exactly `p+1` values outside `Gamma_p`.
- P3: the minimal generators are precisely the `11p` EXP-009 lower generators together with
  `7s+Q_p`; hence the embedding dimension is `12p`.
- P4: `Lambda_p` is nonsymmetric for every `p>=4`, so its localized semigroup ring is not
  Gorenstein. The symmetry genus would be `27p`, whereas the predicted genus is `38p-1`.
- P5: the Dey-Lyle map applies uniformly: `J_p` remains rigid over its commutative endomorphism
  ring but is not reflexive there, and the same adjacent `Ext` and `Tor` groups identified in
  EXP-002 are forced nonzero.
- P6: direct block intersection and an independent generated-semigroup/Apéry route agree exactly
  through `p=300`; deleting one member of `Q_p` and shifting the terminal singleton are rejected.

## What PASS and FAIL prove

- A PASS of P1-P4 and P6 proves the exact finite instances in the declared campaign and validates
  the implementation. It does not by itself prove the formulas for all `p`.
- An exact symbolic block proof is required for the infinite statement and P5.
- Any mismatch for `p>=4` refutes the corresponding formula and stops the experiment. A failed
  corruption control invalidates the checker, not the theorem.

## Premise dependencies

- EXP-009 CONFIRMED: exact family blocks, generation, symmetry, nonprincipality, and rigidity.
- EXP-002 CONFIRMED: endomorphism-value dictionary and audited Dey-Lyle dependency map.
- Dey-Lyle arXiv:2510.02210v2: external theorem dependency, source version rechecked in the
  preflight dossier.

## Method and adversarial validation

1. Route A constructs `Gamma_p` and `V_p` from the closed block formulas, then computes adjacent
   intersections directly.
2. Route B starts only from the predicted minimal generators, constructs `Gamma_p` by exact
   additive closure, computes its Apéry set, and rebuilds `Lambda_p` semantically.
3. Both routes independently compute the difference, conductor, genus, minimal generators, and
   symmetry status for every `p=4,...,300`.
4. A separate audit rebuilds selected cases `p=4,5,17,73,151,300`, hashes every campaign row, and
   runs the two corrupted-formula controls.
5. A readable proof must derive the block formula, generation, invariants, nonsymmetry, and the
   uniform theorem consequences without relying on the finite sweep.

## Invariant-first note

No SAT search is justified. The single deciding invariant is adjacent membership in `V_p`: the
endomorphism block is `V_k intersect V_(k+1)`. Cardinality and the last incomplete block then give
all predicted numerical invariants.

## Compute budget and stop rule

- CPU only, exact integer arithmetic, no randomness or new dependency.
- Smoke cases `p=4,5`: under ten seconds. Full `p=4,...,300` campaign: under two minutes.
- Progress must flush at least every 25 parameters. Artifacts are written atomically at completion.
- Stop at the first exact mismatch. If the two-minute budget is reached, record `INCONCLUSIVE` and
  retain completed rows; no infinite claim follows.

## Exploration moment

The prior programme used anatomy only on the public seed. Applying the same lens to the proved
family turns the visible empty level 7 into a new overring layer `B intersect C`. This is a uniform
structural route, not another counterexample search, and directly addresses the surviving-variant
question: the endomorphism criteria fail by the same mechanism throughout the family.
