# EXP-018 - The genuine witness: the regular hexagon as a stratum central configuration with full-rank mass matrix

Declared: 2026-08-01, BEFORE any run. Campaign: CCB-036 stage 3 (the Dias-Pan
Prop 5.2 + 7.8 anchor for k = 2, p = 2). Declared out of order (before
EXP-017's loci bounds) because it is small, decisive, and independent.

## The candidate

The regular hexagon with six equal masses is a classical planar central
configuration (equal masses on a regular polygon). With the reflection axis
through two opposite vertices it lies in OUR stratum: bodies 1, 2 on the axis
at (0, 1), (0, -1); pair A at (+-sqrt(3)/2, 1/2); pair B at
(+-sqrt(3)/2, -1/2). All mutual distances lie in Q(sqrt(3)) (sides 1,
short diagonals sqrt(3), long diagonals 2 at circumradius 1), so every check
below is exact radical arithmetic. Note q != v, so the configuration sits in
the campaign's declared scope (away from the equal-heights sub-stratum), and
equal masses are consistent with the pair-equality lemma.

## Predictions

- P1 (stratum CC verification): the six reduced Laura-Andoyer equations
  {L13, L15, L23, L25, L35, L36} vanish EXACTLY at the hexagon with all
  masses equal (the Laura-Andoyer equations are lambda-free, so no scale
  normalization is needed). This re-derives a classical fact inside our
  framework; failure would be a pipeline bug, not a finding.
- P2 (the anchor question, genuinely two-branched): the 6 x 4
  mass-coefficient matrix J at the hexagon has rank 4, OR it has rank < 4
  because the hexagon's extra symmetry (dihedral beyond our reflection)
  degenerates it. BOTH branches are declared: rank 4 makes the hexagon the
  Dias-Pan Prop 7.8 anchor (a genuine CC off Delta_4) in one shot; rank < 4
  is a real structural datum (symmetric points often degenerate) and the
  witness hunt continues at less symmetric stratum CCs via the census
  machinery (a follow-up declaration, not this experiment).

## Preflight (methodology/12)

- Source-complete: the hexagon CC fact is classical (regular polygons of
  equal masses; Moeckel's notes among others) and is INDEPENDENTLY VERIFIED
  here by P1's exact computation, so no [U] tag is consumed; the L-machinery
  is the dossier's, already exercised by EXP-016's smoke.
- Smoke: P1 IS the gate (a nonzero value stops everything as a bug).
- One-sidedness: P2 is explicitly two-branched; P1 failure is declared a bug
  because the hexagon's CC property is classical AND re-checked exactly.
- Invariant: the rank value at a genuine CC point.
- Budget: exact radical arithmetic only; minutes; no engine caps needed.

## Consequence ladder

- P2 = rank 4: the top-case anchor of the Lemma 7.3 chain exists; combined
  with EXP-016 (generic rank 4) the remaining gap to the stratum theorem is
  EXACTLY the low-rank loci analysis (EXP-017: Delta_2/Delta_3 exclusions
  and the Delta_4 dimension bound). No statement is claimed yet.
- P2 = rank < 4: recorded as a symmetry-degeneracy finding; EXP-018b hunts a
  less symmetric witness (census machinery on the stratum system at generic
  rational pair-equal masses).
