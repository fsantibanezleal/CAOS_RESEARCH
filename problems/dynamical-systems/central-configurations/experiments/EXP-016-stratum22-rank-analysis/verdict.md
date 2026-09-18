# EXP-016 - Verdict: GENERIC RANK 4 CONFIRMED AT TWO EXACT WITNESSES, COMPONENT DECOMPOSITION CAPPED (2026-08-01; stage (ii)'s foundation is set; the case chain can avoid irreducibility entirely)

Hypothesis: `hypothesis.md` (declared before any run). Runner: `run.py`.
Artifacts: `artifacts/` (results, run log, the minAss script and its output
through the cap).

## Outcomes

| Prediction | Outcome | Facts |
|---|---|---|
| Smoke (pairing identities at W1) | PASS, and it carries extra weight | all six partner equations evaluate to exact negatives of the block equations at the witness: the computational cross-check of the dossier's symmetry proof, replacing the confirmation the killed derivation script never delivered |
| P1 (rank at W1 = (3, -1, 2, 1, 1, -2)) | CONFIRMED: rank 4 | exact radical arithmetic, one second |
| P2 (rank at W2 = (2, -2, 1, 2, 3, -1)) | CONFIRMED: rank 4 | exact radical arithmetic, one second |
| P3 (minAssGTZ of the gauged shape ideal, 300 s) | INCONCLUSIVE-CAP | primary decomposition is much heavier than the one-second std of the same ideal; capped honestly |

## What is established

The 6 x 4 mass-coefficient matrix of the reduced block has FULL RANK 4 at two
independent exact geometries on the stratum. The rank-deficient locus being
Zariski closed, rank 4 is the generic rank on every component of the shape
variety containing either witness; in the fiber inequality
dim_P(fiber) <= 4 - rank, generic fibers over such components are
zero-dimensional. This is the exact analogue of the Dias-Pan Lemma 7.7
computation, obtained here by pure radical arithmetic with no truncation or
mean-value error budgets (their method needed both).

## The route around the capped rung

P3 sought the Dias-Pan "E irreducible" analogue. The cap does not block the
chain: the Lemma 7.3 case argument needs, for each k, that components with
k-dimensional shape projection do not sit inside the rank-<k determinantal
locus Delta_k. That follows from DIMENSION bounds alone: if
dim(shape variety intersect Delta_k pushed to distance form) < k, no such
component fits inside. So EXP-017's declared shape is: push the 3 x 3 and
4 x 4 minors of the mass matrix to distance-only polynomials (the Delta
areas factor as widths times height differences, whose squares are
r-expressible; the s-factors clear as inverse-cube differences exactly as in
Dias-Pan's D_l), then bound dim(shape + minors) per k with Singular and the
partial-GB union pattern where full bases wall. Irreducibility is never
needed. The genuine CC witness (EXP-018) then anchors the top case.

## Soundness notes

- The rank decisions are minor-by-minor exact arithmetic in a real radical
  extension; no floating point anywhere.
- The two geometries were fixed in the hypothesis before any computation.
- The capped minAss run is archived; its partial output was not used.
