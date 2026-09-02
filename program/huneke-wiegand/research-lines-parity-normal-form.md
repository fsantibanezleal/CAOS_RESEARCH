# Parity-normal-form research lines

Updated: 2026-09-02. Scope: unresolved all-parameter characteristic-two connecting quotient in
the EXP-009 family. The broad Huneke--Wiegand conjecture is already false and is not the target.

## Solvability assessment

The CAOS target is not solved. It is now materially more tractable than it was after EXP-038:
EXP-041 replaces an apparently changing component decomposition by one isolated family with a
fixed normalized twelve-atom alphabet through `p=8,...,11`. This makes a uniform signed-chain
description plausible. It does not yet supply the parameter maps needed for an infinite theorem,
so solvability should be described as **plausible but unproved**, not imminent or guaranteed.

The proof bottleneck is precise: construct an integral normal form, chain equivalence, or
functorial transition map for the persistent component and prove that it controls the whole
characteristic-sensitive quotient for every `p`. A recurrence fitted to dimensions cannot replace
that step.

## Ranked routes

### 1. Bockstein plus signed matched-block normal form - active

For the isolated integer matrix `M_p`, compute a canonical basis of `ker(M_p mod 2)`. Every lift
`z` has even boundary, so `(M_p z)/2 mod 2` defines the first Bockstein class in
`coker(M_p mod 2)`. Its rank detects order-exactly-two directions without a full Smith form.

Immediate actions:

1. reproduce the frozen support hashes and ranks for `p=8,...,11`;
2. extract only the isolated twelve-atom component with signed entries;
3. compute the Bockstein rank with forward and reverse canonical reductions;
4. classify nonzero witnesses by normalized atom support; and
5. use integral unit or matched-block cancellations to shrink the component before any Smith
   computation.

This route is strongest because it acts directly on the observed characteristic gap and may turn
the finite defects `3,4,5,7` into explicit torsion witnesses.

EXP-042 completes the first finite gate: independently audited Bockstein ranks are exactly
`3,4,5,7`, proving that many valuation-one Smith factors. The next action is a Hadamard modular
rank certificate. If it proves that the odd-field rank is the rational rank, the tested isolated
2-primary cokernels are completely elementary. The atom chosen to represent a Bockstein image is
pivot dependent (`D:B` for high pivots and `K:C0` for low pivots), so a canonical one-atom
localization is refuted.

EXP-043 closes the rational-rank gap with exact modular Hadamard certificates. The complete finite
isolated 2-primary types at `p=8,9,10,11` are `(Z/2)^3,(Z/2)^4,(Z/2)^5,(Z/2)^7`. The active proof
bottleneck is no longer finite Smith arithmetic; it is a uniform integral reduction of the
`D:B <-> K:C0` bridge and a compatible parameter transition.

EXP-044 is the declared localization diagnostic. Deleting either row family tests necessity;
retaining only their union tests sufficiency. The experiment can refute or sharpen the proposed
bridge, but projection is not a unimodular equivalence and therefore cannot itself prove the
desired normal form.

The result refutes the two-atom carrier while preserving a sharper clue: deleting either marked
atom kills the Bockstein, but their union also has Bockstein zero. The active object is therefore
a larger signed circuit. The next finite action is exhaustive rather than speculative: enumerate
all 64 subsets of the six row atoms and extract the inclusion-minimal full-Bockstein carriers
shared by all four parameters.

EXP-045 declares that exhaustive lattice before computation. Its strong prediction is that the
full six-atom set is the unique nonzero carrier. A refutation remains decisive because the stored
minimal-carrier antichains will specify the exact smaller circuit that replaces it.

The exhaustive result refutes that prediction and supplies the replacement. Minimal full
carriers are stably `59` and `62`; their intersection `58` carries ranks `1,2,3,5`, and either
completion adds exactly two. The `p=11` minimal nonzero carrier drops to `56`, exposing a separate
threshold class. The highest-value action is now an integral relative comparison of the two
alternative completions, not another global rank or coefficient sweep.

### Arithmetic deletion-contraction refinement - completed leaf gate

Fink and Moci's matroids-over-rings framework records quotient modules, torsion, deletion,
contraction, and base change for integral vector configurations. The CAOS row masks are grouped
row families rather than a proved instance of the desired uniform object, so the framework is a
dictionary and invariant ledger, not a theorem transfer.

Applied to the finite carrier table, the contraction-rank increments are

```text
58 -> 59: (delta_Q,delta_2)=(2p-3,2p-5),
58 -> 62: (delta_Q,delta_2)=(4p-10,4p-12)
```

at every tested parameter. Both expose the same defect-two completion despite different ambient
ranks. EXP-046 tests the cheapest integral explanation: unit-leaf cancellation followed by
component decomposition.

That explanation is now refuted. All sixteen tested projections leave one connected nonzero core;
masks `59` and `62` have zero unit-leaf cancellations, so their defect-two increments cannot be
peeled off as separate blocks. Mask `56` changes from defect zero to one at `p=11` without changing
its semantic atom-set support. The active route must therefore create fill through certified
integer operations rather than search for existing leaves.

### Fill-producing relative presentation - active

For a row inclusion `S subset T`, use the exact cokernel sequence induced by
`M_p(S) -> M_p(T)` to present the relative quotient after eliminating free directions. The finite
rank increments are different for `R0` and `R2`, but both parity increments are two. The immediate
test is whether fraction-free signed Hermite elimination produces a bounded parity presentation
with equivalent mod-two and Bockstein data for `58->59` and `58->62`.

The certificate must record every integral pivot and permutation, preserve the source hashes, and
recompose ranks over at least three fields. If the residual parity matrix grows with `p`, the next
fallback is a filtered relative squarefree-divisor complex with explicit chain maps. A field-only
Schur complement is diagnostic and cannot establish the integral claim.

EXP-047 declares the exact finite gate. For `M_T=[A;B]`, it computes
`Z^(T-S)/B(ker_Z A)` from a transformed Hermite basis and then reads its compact Smith form. The
predictions are `(Z/2)^2` after free stabilization for both alternative completions and
`(Z/2)^(p-7)` for `56->58`. These finite Smith forms can validate the relative-module target but
cannot replace the later uniform basis and parameter maps.

### 2. Relative squarefree-divisor homology - structural fallback

Multigraded Betti numbers of numerical semigroup rings can be represented by reduced homology of
squarefree divisor complexes. Recast the twelve atom families as a filtered relative complex and
compute the connecting differential between simple interval pieces. This is attractive if the
Bockstein witnesses have stable face descriptions, but premature if the filtration cannot be
proved to be a subcomplex.

### 3. OI/FI finite generation and representation stability - theorem framework

OI/FI methods can turn compatible families of resolutions into stabilization statements, and
Gröbner methods for combinatorial categories can imply rational Hilbert series. They become useful
only after explicit order-preserving injections send the `p` complex to the `p+1` complex and
commute with the signed differential. The repeated atom skeleton is evidence for looking for such
maps; it is not itself an OI-module proof.

### 4. Algebraic discrete Morse compression - companion technique

Algebraic discrete Morse theory preserves homology when cancellations form an acyclic matching
with invertible coefficients. The existing leaf peeling is the first elementary instance. A
parameterized matching on the twelve-atom block could leave a bounded critical complex and would
pair naturally with the Bockstein calculation. A rank-only elimination with field-dependent
pivots is not an integral Morse proof.

### 5. Toric gluing or splitting - conditional and demoted

Gluing can factor resolutions after an actual ideal or semigroup splitting. No such splitting has
been proved for the connecting component. Do not infer one from disconnected support, semantic
tags, or matching dimension formulas.

### 6. Additional coefficients - low priority

Do not spend on `p=13` or new full component ranks while the persistent block lacks a structural
classifier. A new coefficient is justified only by a declared out-of-sample prediction from a
proved or explicitly conjectured transition law.

## Literature anchors and limits

- Jollenbeck and Welker construct homology-preserving smaller free complexes from acyclic
  algebraic Morse matchings: <https://arxiv.org/abs/math/0501179>.
- Autry et al. use squarefree divisor complexes for multigraded Betti numbers of numerical
  semigroup rings: <https://arxiv.org/abs/1804.06632>.
- Nagel and Romer prove noetherianity and finite Gröbner bases for suitable OI-modules and explain
  how finite generation can stabilize syzygies in fixed homological degree:
  <https://arxiv.org/abs/1710.09247>.
- Sam and Snowden give Gröbner/noetherianity and Hilbert-series criteria for representations of
  combinatorial categories: <https://arxiv.org/abs/1409.1670>.
- Raicu proves representation stability for homology of packing complexes and corresponding
  syzygies, an analogy rather than a theorem about the CAOS family:
  <https://arxiv.org/abs/1209.1183>.
- Dalili and Kummini connect characteristic-dependent Betti numbers with simplicial homology and
  discrete Morse constructions: <https://arxiv.org/abs/1009.4243>.
- Fink and Moci organize quotient modules, torsion, base change, deletion, and contraction for
  matroids over a commutative ring: <https://arxiv.org/abs/1209.6571>.
- Pagaria and Paolini use reduction and signed Hermite normal form for representations of
  torsion-free arithmetic matroids; their torsion-free hypothesis prevents a direct theorem
  transfer here: <https://arxiv.org/abs/1908.04137>.

None of these sources supplies the missing chain maps or the CAOS recurrence. They justify the
route vocabulary and proof obligations only.

## Manuscript split gate

Do not update v0.23 or Zenodo for another finite rank/profile table. Open a complementary
lower-strand manuscript only after at least one of these occurs:

- an all-parameter parity/torsion theorem for the connecting quotient;
- a uniform signed normal form or acyclic matching with a proved finite critical complex;
- a proved OI/FI or relative-homology model that forces a recurrence or rational series; or
- another independently transferable theorem of comparable strength.

A finite Bockstein certificate is an experiment milestone and a route-selection result, not by
itself a publication trigger.
