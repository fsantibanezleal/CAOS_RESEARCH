# EXP-037 - Verdict: CONFIRMED 1, 2, 5; prediction 3 REFUTED as declared; 4 mapped (2026-07-22)

Artifacts: `artifacts/output-AB-2026-07-22.txt`, `artifacts/output-CD-2026-07-22.txt`,
`artifacts/output-E-2026-07-22.txt`.

## The formalization stands: the staircase IS a triangular transport system

1. **Block triangularity [MV] (prediction 1).** Under the x-edge grading w = (v, 1-u), every
   nonzero entry of the window matrix sits at a class offset s - sigma for a P-class s, and
   for pure above-weight staircases the diagonal offset u - 1 is minimal (4 samples,
   offsets == allowed exactly). The RESUME's step (a) is not an analogy: the Keller window
   literally block-triangulates along the staircase classes.
2. **Classwise elimination is exact and complete [MV] (prediction 2).** The transport sweep
   (solve the diagonal Theorem-1 block per class, inject kernel parameters, emit cokernel
   obstructions) reproduces the monolithic verdict on every sample (5 staircase shapes:
   EMPTY == EMPTY) and on the positive control x + (x + y)^2, which stays CONSISTENT with 5
   kernel parameters. One structural discovery en route: genuine components carry P-classes
   BELOW the x-class (their tops are y-anchored), so the diagonal block must be the MINIMAL
   P-class; with that choice the sweep is triangular for every P with linear part x. The
   instrument is general, not staircase-specific.
3. **Localization [MV, prediction 3 REFUTED as declared].** The declared prediction said the
   first inconsistent transport equation would sit at the vertex-matching (second-edge)
   classes. The machine says otherwise, 8/8 on the (u, v, d) grid: the first failure is at
   the CONSTANT'S class (row-class 0), below every interference class. The hand-off between
   edges does not break locally; it transports the contradiction all the way down to the
   constant's row, exactly as in the single-edge theorems. This is good news recorded as a
   refutation: the obstruction has ONE canonical location, the constant.
4. **The chain pattern [C -> nearly D] (prediction 4).** The symbolic (generic) transport
   equations are startlingly clean: for P = x + a x^u y^v + b x^d the constant-class
   equation reduces to -2a = 0 (u = 2 cases; three shapes), with further equations
   -2b = 0, -12b^3 = 0, -8b^4 = 0 at higher classes. The entire window collapses, after
   elimination, to "the staircase coefficients must vanish": the exact analog of Theorem 1's
   positive chain. CAVEAT, recorded: part E's eliminations run over QQ(a, b)
   (fraction-field steps), so the symbolic statement is GENERIC; soundness for every
   parameter value stays with the numeric runs (parts B/C) and needs cleared certificates
   (EXP-024 style) before any Theorem 5 is declared.
5. **Territory [MV] (prediction 5).** All JCB-028 residue shapes (pure slice + above-weight
   coefficients x^2, x^2 y, x^3, and pairs) and richer 3-vertex staircases have EMPTY
   windows at N = 8 (7 shapes). The JCB-028 residue is now inside the staircase program's
   mapped territory.

## What this changes

- JCB-038 step (a) and step (b) are DONE as instruments: the staircase is formalized (class
  grading + minimal-class diagonal) and the transport recursion is executable code emitting
  the reduced system on kernel parameters.
- Step (c) has its first empirical answer: the reduced system is over-determined on every
  sample, and its failing equation is the constant's, with closed generic form -2a = 0 on
  the minimal family. The Theorem 5 candidate is now concrete: prove the constant-class
  transport equation equals (nonzero constant) * a for the family x + a x^u y^v + R_above,
  by clearing the generic elimination into an all-parameter certificate.
- The refuted localization prediction sharpens the proof target: no vertex-matching
  argument is needed; the single constant-class equation carries everything.

## How could this be wrong?

- Part E is generic-only (declared); a parameter locus where the elimination degenerates
  could in principle behave differently: the cleared-certificate pass (queued as the
  JCB-038 continuation) is the closure.
- Windows are finite (N = 7..8); the all-degree statement needs the annihilation lemma
  (EXP-036) re-instantiated for the staircase certificates, same as Theorems 2-4.
