# EXP-063: exact triangle-to-isolated comparison

Declared 2026-09-20 before computation. Status: **DECLARED, NOT RUN**.
CPU-only exact integer reconstruction and bit-packed `GF(2)` linear algebra.

## Frozen question

For `p=8,9,10,11`, reconstruct the exact labelled persistent component of
EXP-042 by replaying the integral unit cancellations. For every increasing
triple `T=(i,j,k)` with `i+j+k=p-2`, let `x_T=x_ij` be the exact K-row chosen
in EXP-062.

Let `R_m` be the signed component matrix projected to the row atoms selected
by mask `m` in `{56,58,59,62}`. Let `X_m` be the matrix of those surviving
triangle coordinate vectors after the same row projection. The operational
triangle-span rank is

    rank_F2([R_m mod 2 | X_m]) - rank_F2(R_m mod 2).

Because EXP-062 supplies an exact integral source with boundary `2x_T`, every
nonzero quotient class measured this way has integral order exactly two in the
full presentation; EXP-043 supplies the independent finite torsion ceilings
for masks `59` and `62`.

## Predictions fixed before computation

- **P1 (labelled survival):** every exact `x_T` survives both unit-cancellation
  stages, belongs to the unique frozen isolated component, has semantic atom
  `R5`, and is carried to the literal same surviving target coordinate. No
  triangle row is a pivot or lies outside the selected component.
- **P2 (complete finite isolated basis):** for masks `59` and `62`, the
  triangle-span rank is exactly `q=3,4,5,7`, respectively. Thus the triangle
  classes account for the entire finite two-primary torsion certified in
  EXP-043 for each of the four parameters.
- **P3 (relative losses):** the triangle-span ranks for mask `58` are
  `1,2,3,5`, and for mask `56` are `0,0,0,1`. Equivalently, projection from
  either full carrier to `58` has a two-dimensional kernel on the triangle
  span, while projection `58 -> 56` loses `p-7` dimensions. Preserve a
  deterministic basis of each kernel as explicit combinations of named
  triangles and compare the two completion masks.

## Method and certificates

1. Verify SHA-256 pins for EXP-036/037/042/043/047/048/062 premises and all
   frozen `p=8,...,11` matrix artifacts.
2. Replay the original labelled basis construction and both exact unit-leaf
   cancellation stages. Select the unique component by the frozen support and
   signed hashes; record surviving row labels and a cancellation-transcript
   digest.
3. Independently regenerate every EXP-062 triangle and its exact selected K
   label. Reject duplicates, missing labels, pivoted labels, non-`R5` atoms,
   or any mismatch between rebuilt and frozen signed matrices.
4. For each mask, compute the two ranks above in both low-pivot and high-pivot
   orders. Emit deterministic quotient residuals and relation-kernel bases in
   lexicographic triangle order.
5. The auditor must reconstruct labels through the prior independently pinned
   route, read the frozen signed matrices rather than producer matrices,
   recompute all ranks with the opposite pivot convention, and exercise three
   controls: duplicate one triangle, replace one with a nontriangle `R5` row,
   and flip one signed matrix entry before hash validation.

## Interpretation boundary

A pass proves only a finite labelled comparison at `p=8,...,11`. It does not
prove the same cancellation survival or spanning statement for all `p`, does
not classify the complementary full cokernel, and does not establish the
lower-strand recurrence. A failure is still decisive for the proposed literal
comparison and must redirect the next symbolic route to a corrected chain map.

## Resources and stopping rules

- Smoke: `p=8`, at most 180 seconds and 4 GiB private memory.
- Full producer: `p=8,...,11`, at most 900 seconds and 12 GiB.
- Independent audit: at most 900 seconds and 12 GiB.
- One CPU process per stage; atomic artifact writes and a checkpoint after each
  parameter. Stop on the first premise/hash/label/rank disagreement or resource
  cap. Preserve partial and failure artifacts. Do not enlarge the parameter
  range or perform a new HNF/SNF campaign in this experiment.

No manuscript or Zenodo update is authorized by this declaration alone. A
uniform theorem or comparably strong structural advance is required.
