# EXP-065 hypothesis: dual-guided integral endpoint decoder

Date: 2026-09-20. This hypothesis is frozen before implementation or execution.

## Question

Can the integral vanishing of the two mask-58 endpoint triangles be upgraded
from EXP-064's finite existence theorem to explicit, semantically labelled source
witnesses without computing a transformed HNF of the complete carrier matrix?

For `p=8,9,10`, the targets are the literal mask-58 rows associated with

```text
T1(p) = (0,1,p-3),
T2(p) = (0,2,p-4).
```

The `p=11` matrices are excluded from this training experiment. Any formula
suggested by the training results must be frozen in a later EXP before a `p=11`
holdout run.

## Motivation and new viewpoint

EXP-064 proves that each target lies in the integral image, but its argument uses
the complete elementary 2-primary type and does not exhibit a source. EXP-058's
escaping-column lemma says that an annihilating dual on a partial source set
identifies a necessary omitted column direction.

Read the matrix as an exact decoding problem. A source column is a move, the
endpoint row is a syndrome, and an annihilating dual is a parity check. Starting
from the columns incident to the target, repeatedly add every omitted column with
nonzero pairing against the current exact dual. This is also column generation:
the dual supplies the pricing rule for columns capable of removing the current
obstruction.

The primary-source and cross-disciplinary assessment is recorded in
`context/2026-09-20-post-exp064-online-route-review.md`.

## Premise dependencies

1. EXP-042 supplies frozen signed carrier matrices for `p=8,...,11`.
2. EXP-048 supplies the exact six-atom mask semantics and labelled component
   reconstruction.
3. EXP-053 supplies a unique reconstruction of component columns in the original
   presentation for the training parameters.
4. EXP-063 identifies both endpoint triangle targets as literal surviving `R5`
   coordinates.
5. EXP-064 proves that both endpoint targets lie in the integral image of mask 58
   for every tested parameter.
6. The escaping-column lemma in EXP-058 proves the correctness of the dual-guided
   expansion rule. It does not prove that few iterations suffice.

## Falsifiable predictions

### P1: bounded exact decoding

For both targets and every training parameter `p=8,9,10`, dual-guided column
generation finds an integer source witness in at most six expansion rounds, using
at most 900 carrier columns and 8 GiB private memory per parameter.

### P2: semantic compression

After mapping the nonzero source coefficients back to original column labels and
normalizing all interval positions by endpoint distance:

- each coefficient has absolute value at most four;
- each witness has support at most `40p`; and
- the union of normalized label skeletons across the six witnesses has size at
  most 80.

These bounds are deliberately loose. Passing them makes a finite-state rewrite
or interval-family formula plausible; failing them redirects to the relative
divisor-complex route.

### P3: exact provenance and controls

Direct multiplication in the complete projected matrix must reproduce one unit
target coordinate and zero on every other selected row. Reversing the column
order must preserve membership and the independently reconstructed target. A
target-row mutation and a witness-coefficient mutation must both be rejected.

## Method

1. Verify every frozen premise hash before loading a matrix.
2. Reconstruct the mask-58 selected rows and exact endpoint row labels without
   reading EXP-064's conclusion artifact as a solver input.
3. Reconstruct original semantic labels for all surviving component columns.
4. Initialize the active source set with every column incident to the target.
5. Use exact rational, unit-first sparse elimination with original-column
   provenance.
6. If inconsistent, persist an integer annihilating dual and add all omitted
   columns with nonzero dual pairing. Repeat within the declared cap.
7. If the rational section is integral, verify it directly. If it is rational but
   nonintegral, use an exact local transformed HNF only on the active submatrix.
8. Normalize the final nonzero semantic labels and write checkpoints after every
   expansion.

No floating arithmetic, stochastic search, global Smith form or full transformed
HNF is permitted.

## What PASS and FAIL prove

- P1 PASS proves explicit finite integral witnesses for all six training targets
  and validates dual-guided decoding as an exact extraction method. It does not
  prove a uniform formula.
- P1 FAIL at the round/column/time cap refutes only the declared bounded decoder.
  It does not refute existence, which is already known from EXP-064.
- P2 PASS gives a bounded semantic vocabulary from which a separate symbolic
  hypothesis can be frozen. It does not prove that the vocabulary persists.
- P2 FAIL is evidence against the finite-state source route and raises the
  priority of the relative-complex filtration.
- P3 FAIL invalidates the affected witness and forces a refuted verdict regardless
  of P1/P2.

## Invariant-first note

Rank, mod-two quotient dimension and first Bockstein already decide existence and
exponent, but cannot recover source coefficients. The cheapest remaining
decision-bearing invariant is the annihilator of the active column span: its
support pairing identifies exactly which omitted columns can change consistency.
This is used before any lattice normal form.

## Adversarial validation

The auditor will rebuild the selected rows, targets and semantic column map in a
separate order; multiply every retained witness from scratch; recompute rational
membership with reverse column order; and run the two mutations. Any formula
recognition is explicitly deferred to a later frozen experiment.

## Compute budget and kill criteria

- CPU only, one process.
- Smoke: `p=8`, one target, two expansion rounds, 120 seconds, 4 GiB.
- Training: `p=8,9,10`, both targets, at most 900 seconds and 8 GiB per parameter.
- At most six dual expansions and 900 active columns per target.
- Flush progress and atomically checkpoint after every round and target.
- A time, memory, round or column cap produces `INCONCLUSIVE_RESOURCE` for the
  unfinished target; completed witnesses remain finite results.

## Publication gate

Finite witnesses alone do not update Zenodo. A later all-parameter formula with
an independent symbolic proof would trigger expansion of the existing integral
connecting manuscript. A separate manuscript requires a general finite-state
Morse/decoding theorem or a complete complementary-cokernel theorem.

