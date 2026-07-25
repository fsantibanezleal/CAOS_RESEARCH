# EXP-009: the n = 4 equal-mass planar census IN THE TORUS

Declared: 2026-07-25, BEFORE any run. Route: R1 calibration (the CC-P1 entry rung).
Follows EXP-006, whose third prediction was refuted as posed: the AFFINE enriched
system has dimension 1, so it has no isolated census. This experiment asks the
corrected question on the correct object.

## Question

In the torus (all mutual distances invertible), does the equal-mass planar 4-body
system have a finite solution set whose positive realizable points reproduce the
published counts: 50 labeled solutions and 4 classes modulo relabeling?

## The two routes (run both; they are independent formulations)

- **Route A, saturation.** The enriched planar system (symmetric + asymmetric
  Albouy-Chenciner + energy-inertia + Cayley-Menger) together with the Rabinowitsch
  equation `t * r12 r13 r14 r23 r24 r34 - 1 = 0`, which forces every distance to be
  invertible. Solved with msolve.
- **Route B, the Hampton-Moeckel z-system.** Their equation (13): the five linear
  relations `sum_i m_i z_i = 0` and `f_j = sum_{i != j} m_i z_i r_ij^2 + k = 0`,
  together with `S_ij = z_i z_j` where `S_ij = r_ij^{-3} - 1`, cleared of
  denominators. This is a SQUARE system (11 equations, 11 unknowns: four z, k, six
  distances) and it is the object to which they apply BKK; the map (r, z) -> r is
  2:1 onto the Albouy-Chenciner plus Dziobek solutions, which is exactly why their
  mixed-volume bound 25380 divides down to 8460 noncollinear.

## Ground truth (from primary sources already read)

- 4 classes modulo rotation, reflection and permutation, for four equal masses
  (Moczurad-Zgliczynski 2019, appendix counts, PDF read; also Albouy's
  classification, quoted as a theorem by Hampton-Moeckel).
- 50 classes modulo rotation only (Simo 1978, quoted by Moczurad-Zgliczynski and by
  Hampton-Moeckel). Since every equal-mass central configuration with n <= 7 has a
  reflection symmetry (Moczurad-Zgliczynski, Theorem 1), each rotation class is
  achiral, so the 50 rotation classes correspond to 50 distinct LABELED distance
  vectors, which is what a census in distance coordinates counts.
- The square must appear with the exact side of EXP-001: minimal polynomial
  32x^6 - 32x^3 + 7.

## Falsifiable predictions

- **P1 (finiteness in the torus).** Both routes yield ZERO-dimensional systems
  (msolve reports dimension 0), in contrast with the affine system of EXP-006 which
  reported dimension 1.
- **P2 (the labeled count).** Route A's positive real solutions that are
  REALIZABLE in the plane number exactly 50. Realizability is tested exactly: the
  bordered Cayley-Menger determinant vanishes (already imposed) AND the three
  leading principal Cayley-Menger minors have the signs of a genuine planar
  configuration, checked in exact arithmetic on each solution.
- **P3 (the class count).** Those 50 solutions fall into exactly 4 orbits under the
  action of the symmetric group on the four bodies (relabeling permutes the six
  distances), and one orbit contains the square with a satisfying
  32a^6 - 32a^3 + 7 = 0.
- **P4 (cross-formulation agreement).** Route B returns the same set of distance
  vectors as Route A, after projecting away z and k and identifying the 2:1 fiber.

## Preflight (methodology/12)

- **P1 source-complete.** Hampton-Moeckel read in full (their Sections 2.2 and 6.2
  give the z-system, the 2:1 map and the counts); Moczurad-Zgliczynski read
  (appendix counts, symmetry theorem); no unread source bears on the equal-mass
  n = 4 count.
- **P2 tooling smoke test.** msolve is validated by EXP-006 on four n = 3 censuses
  with exact cross-verification; before the full runs, each route is smoke-tested by
  substituting the known square into the built system and checking every equation
  vanishes exactly.
- **P3 premise dependencies.** (a) The census belongs in the torus: established by
  EXP-006's dimension-1 finding plus the diagnostic excluding vanishing-distance
  loci. (b) The enriched system captures the planar CCs: EXP-002 P3. (c) The 2:1
  structure of Route B: Hampton-Moeckel Section 6.2 (primary, read). (d) The 50/4
  ground truth: primary sources above, both read.
- **P4 one-sidedness.** P2 and P3 are two-sided: a wrong count refutes either our
  pipeline or the equivalence reduction, and the artifacts distinguish which (a
  missing known configuration versus an extra solution). P1 is two-sided. P4 is a
  consistency check whose failure would indicate a bug in one route.
- **P5 invariant-first.** Classes are separated by cheap exact invariants before any
  geometric reconstruction: the sorted multiset of the six distances, plus the
  scale-free J = U I^(1/2) / M^(5/2) recorded per solution.
- **P6 budget and kill criterion.** 3600 s per route, 2.5 hours total. If a route
  hits its cap it is recorded inconclusive-cap and the other route's result stands
  on its own; no silent retries at larger budgets.

## Success / failure criteria

SUCCESS: P1 through P4 hold. FAILURE: any count differing from the published one is
recorded as a refutation with the machine output, and the follow-up question (which
side is wrong, ours or the transcription of the ground truth) becomes a new
experiment rather than an edit of this one.

## Method / environment

`run.py`: builds both systems with cclib, writes msolve inputs, runs them in WSL
under the caps, parses the boxes, applies the exact realizability test and the exact
class-orbit reduction, and re-verifies every accepted solution by exact residual
substitution. Deterministic; artifacts and hashes persisted.
