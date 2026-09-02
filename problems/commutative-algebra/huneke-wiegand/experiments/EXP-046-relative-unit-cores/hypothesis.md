# EXP-046 hypothesis - relative unit cores of the stable carriers

Date: 2026-09-02. CPU only. Exact integer and finite-field arithmetic.

## Question

Let `M_p(S)` be the EXP-045 row projection with atom mask `S`. The stable minimal full carriers
`59` and `62` share mask `58`; at `p=11`, mask `56` carries the first smaller nonzero class.
EXP-046 asks whether degree-one integral cancellations split these presentations into a common
torsion core plus a bounded two-class completion.

The tested masks are `56`, `58`, `59`, and `62` for `p=8,9,10,11`. A unit-leaf cancellation
removes a row-column pair when either endpoint has degree one. Because every nonzero entry is
`+1` or `-1`, elementary operations split an identity summand. The cokernel becomes the cokernel
of the remaining matrix plus free zero-row summands, so its torsion and first Bockstein are
preserved.

## Predictions

### P1. Nontrivial exact compression

Every tested projection admits at least one unit cancellation. After peeling, recomposed ranks
must satisfy

```text
rank_q(M) = cancellations + sum rank_q(component)
```

for `q=2,3,5`, and component Bockstein ranks must sum to the stored EXP-045 value. Forward and
reverse deterministic peeling orders must give identical component dimension/rank/defect
multisets.

### P2. Separated constant-two completion

For both minimal full carriers, the residual defect partition consists of the mask-58 defect plus
two defect-one components. After replacing completion alias `R0` or `R2` by a common alias `RX`,
the two completion-component semantic signatures agree between masks `59` and `62` at each `p`.

A connected defect-two block, a merger with the mask-58 defect, or differing completion
signatures refutes this proposed splitting while still locating the correct residual block.

### P3. Isolated threshold component

For mask `56`, every residual component has defect zero at `p=8,9,10`, while `p=11` has exactly
one defect-one component. Its semantic atom-set signature already occurs at an earlier parameter,
so the threshold is predicted to be a sign/rank event inside persistent support rather than the
appearance of a new atom type.

## Independent audit and claim boundary

The runner verifies the exact EXP-042 matrices and EXP-045 result hash. It records every cancelled
pair count, free row, residual component, signed hash, field rank, Bockstein rank, and semantic
signature. An independent auditor must use the opposite queue priority, reconstruct every
projection, and recompute all component invariants without calling the runner's peeling routine.

A pass is a finite integral unit-core theorem only. Row masks are grouped deletions, not yet an
all-parameter matroid-over-rings representation. No recurrence, functorial `p -> p+1` map, full
lower strand, manuscript, or Zenodo update is claimed from this gate alone.
