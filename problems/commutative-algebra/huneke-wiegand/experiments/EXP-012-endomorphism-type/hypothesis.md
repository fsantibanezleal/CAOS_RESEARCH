# EXP-012 - pseudo-Frobenius anatomy and reduced type

Declared: 2026-08-12, before implementation or execution. Phase HW-P5. Backlog HWB-007 and
HWB-013.

## Question and prediction

For every integer `p>=4`, put `s=6p` and retain the EXP-011 semigroup `Lambda_p`. Define

```text
B^c = [0,p] union {2p-1} union [3p,4p-1] union [4p+1,5p-2],
Q^c = [0,p] union {2p-1} union [2p+1,4p-1] union [4p+1,6p-1],
C^c = [2p+1,3p-1] union [5p-1,6p-1].
```

The falsifiable prediction is

```text
PF(Lambda_p) = (6s+B^c) union (7s+Q^c) union (8s+C^c).
```

Consequently:

1. `type(Lambda_p)=10p`;
2. its reduced type is also `10p`, so its semigroup ring has maximal reduced type;
3. `Lambda_p` is not almost symmetric, hence its semigroup ring is not almost Gorenstein;
4. there are no pseudo-Frobenius numbers below `5s`.

## Premise dependencies

- EXP-009 proves the exact family semigroup and its minimal generators.
- EXP-011 proves the exact `Lambda_p` blocks, conductor `9s`, multiplicity `4s`, genus `38p-1`,
  and minimal generators in levels 4 through 7.
- Maitra-Mukundan Theorem 2.13 and Proposition 3.7 support the reduced-type interpretation.
- The numerical-semigroup dictionary identifies type with `|PF|` and almost Gorenstein with almost
  symmetry. The almost-symmetric genus identity is used only after its hypotheses are checked.

No premise claims the predicted PF formula; that is the new hypothesis.

## Method

1. Derive the PF formula symbolically from the exact level blocks.
2. Route A: enumerate all gaps and test `f+g in Lambda_p` for every minimal generator `g`.
3. Route B: reconstruct the Apéry set modulo `4s`; its order-maximal elements minus `4s` must give
   the same PF set.
4. Check every `p=4,...,300` exactly, with deterministic row and campaign hashes.
5. An independent auditor will reconstruct selected semantic windows, rehash every row, and reject
   a deleted predicted PF number and an injected lower gap.

## What PASS and FAIL prove

- A computational PASS shows two exact finite implementations agree with the prediction through
  `p=300`; it supports but does not prove the all-`p` theorem. The symbolic block proof is
  load-bearing for confirmation.
- Any mismatch is a decisive refutation of the displayed formula at that parameter. An additional
  lower PF number refutes maximal reduced type; a missing displayed value refutes the count.
- A completed symbolic proof plus successful adversarial checks confirms the theorem for every
  `p>=4`.

## Invariant-first note

The last multiplicity window `[5s,9s-1]` contains exactly `10p` gaps, giving a lower bound on type
without computation. The experiment tests whether lower PF numbers exist. This single invariant
can decide maximal reduced type and almost symmetry, so no SAT or Groebner computation is warranted.

## Compute budget and kill criterion

CPU only, exact integer and bitset arithmetic, no randomness. Smoke budget: 10 seconds at `p=4,5`.
Full budget: two minutes for `p=4,...,300`. Because the expected run is below five minutes, no
checkpoint is required. Abort on the first semantic mismatch or at two minutes; a budget hit is
`INCONCLUSIVE`, not evidence for or against the formula.

## Success and failure criteria

Success requires the symbolic proof, Route A/Route B equality for all 297 parameters, stable hashes,
an independent audit, and both corruptions rejected. Any formula, count, type, reduced-type, or
almost-symmetry mismatch is failure and is preserved in the verdict.
