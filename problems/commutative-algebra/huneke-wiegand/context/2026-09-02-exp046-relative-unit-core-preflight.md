# EXP-046 preflight - relative unit cores and arithmetic deletion-contraction

Date: 2026-09-02. Status: source-complete for the declared finite gate.

## Primary-source pass

Fink and Moci, *Matroids over a ring*, arXiv:1209.6571v6,
<https://arxiv.org/abs/1209.6571>, assign a module to every subset of an integral vector
configuration and retain deletion, contraction, base change, and torsion data. Their framework
justifies treating the EXP-045 row-subset table as an integral deletion-contraction object. It does
not identify the CAOS modules or prove a uniform carrier theorem.

Pagaria and Paolini, *Representations of torsion-free arithmetic matroids*, arXiv:1908.04137,
<https://arxiv.org/abs/1908.04137>, use reduction and signed Hermite normal form to classify
representations. This supports signed normal-form exploration, but their torsion-free hypotheses
do not cover the CAOS factor-two cokernels.

Jollenbeck and Welker, *Resolution of the residue class field via algebraic discrete Morse theory*,
arXiv:math/0501179, <https://arxiv.org/abs/math/0501179>, extend discrete Morse cancellation to
complexes of free modules over a ring. EXP-046 uses only the elementary unit-leaf case, whose
integral splitting is re-derived in the hypothesis and checked directly.

Autry, Graves, Loucks, O'Neill, Ponomarenko, and Yih, *Squarefree divisor complexes of certain
numerical semigroup elements*, arXiv:1804.06632, <https://arxiv.org/abs/1804.06632>, confirm that
squarefree divisor complexes encode multigraded Betti information for numerical semigroup rings.
That remains a structural fallback after a finite signed core is exposed.

No source found in the existing dossier or fresh sweep proves the EXP-009 connecting quotient,
the carrier masks, or their parameter transition. The all-parameter problem remains open.

## Premise ledger

1. EXP-042 supplies frozen signed isolated matrices and exact first-Bockstein ranks `3,4,5,7`.
2. EXP-043 proves their rational ranks and complete isolated 2-primary cokernels.
3. EXP-045 exhausts the six-row-atom lattice. Minimal full carriers are `59` and `62`; their
   intersection `58` has Bockstein ranks `1,2,3,5`; mask `56` first becomes nonzero at `p=11`.
4. Exact linear algebra applied to the stored EXP-045 ranks gives the finite contraction table

   ```text
   58 -> 59: delta_Q = 2p-3,  delta_2 = 2p-5,
   58 -> 62: delta_Q = 4p-10, delta_2 = 4p-12
   ```

   for `p=8,9,10,11`. These are four-point identities, not yet formulas for all `p`.

## Invariant-first decision

The cheapest integral invariant is the unit-leaf two-core. A row or column of degree one contains
a unit `+1` or `-1`; elementary integral operations split that row-column pair and preserve all
torsion. Repeating this before Hermite or Smith computation can expose a bounded critical block or
falsify that expectation without fill-in.

Raw determinant products, another coefficient, and a full Smith form were rejected as first
actions. They do not explain the stable alternative completion and cost more than the unit-core
test.

## One-sidedness, cost, and kill gate

A PASS can prove only the declared finite unit-core decomposition. A FAIL disproves its proposed
component structure and identifies the residual carrier that must replace it. Neither outcome
proves a parameter-uniform matching.

The `p=8` smoke is capped at 300 seconds and 8 GB. The full `p=8,...,11` campaign is capped at
1,200 seconds and 16 GB, checkpointed after every parameter. If the budget is hit, the verdict is
inconclusive beyond the last complete checkpoint.
