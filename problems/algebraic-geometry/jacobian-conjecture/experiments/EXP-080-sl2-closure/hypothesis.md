# EXP-080 - Does the staircase carry an sl2 (or larger) weight structure?

- **Question.** Do the graded window operators close into an sl2 triple
  (e, f, h) with h the (v,1-u) weight? If so the corrector ladder is a weight
  module and termination = finite-dimensionality.
- **Motivation (dossier section 3).** The (v,1-u) grading is a torus weight;
  the T_i shift weight by fixed amounts; Lambda0 is a weight-lowest vector. An
  sl2 (or Virasoro/W) structure would make 'which degree closes' a
  representation-theoretic DECOMPOSITION and PREDICT obstruction locations
  (primitive vectors) instead of finding them by sweep.
- **Predictions.** 1. [MV] Assemble the weight operator h (grading) and the
  natural raising/lowering candidates from the T_i by weight sign. 2. [MV]
  Test [e, f] = h (up to scalars) and [h, e] = 2e, [h, f] = -2f on the window
  basis. 3. [D] If sl2 closes: the ladder module decomposes; if only a larger
  algebra closes, identify it; if nothing closes, record the honest null and
  the obstruction to a Lie structure.
- **Method.** Import the EXP-071 window operators; exact bracket computations;
  small and fast.
- **Success.** The closure question decided either way.
- **Failure.** none beyond an honest null.

Declared 2026-07-24 before the run.

## 2026-07-25 pre-run amendment (methodology/12)

The question is unchanged, but the original declaration did not distinguish the
raw monomial grading from the gauge-dependent pinned operators. The invariant
gate below must pass before any commutator assembly.

- **P1, source-complete.** The 2026-07-25 primary-source pass read Shaska,
  arXiv:2607.20210v1, in full. It classifies graded planar Keller maps but contains
  no `sl2`, corrector-ladder, or weight-module construction. The source does not
  decide this experiment.
- **P2, tooling smoke.** Stage A is a deterministic exact-integer support
  computation expected to finish in under one second and to print every result.
  No checkpoint is needed below five minutes. Stage B is forbidden unless Stage A
  identifies a canonical common grading.
- **P3, premise dependencies.**
  1. Raw brackets with a monomial perturbation have a fixed weight shift; this
     follows directly from the exponent formula and is checked in Stage A.
  2. The pinned maps \(A_i=\sigma T_i\) exist (EXP-064), but their grading
     homogeneity is a **hypothesis**, not a prior result: \(\sigma\) has a
     165-dimensional gauge freedom and EXP-064 only fixes one pivot gauge.
  3. The pinned ladder does not terminate (EXP-064), so termination or a finite
     degree bound may not be assumed (EXP-078).
  4. Solvability is automatic by the dual annihilation identity (EXP-068); it does
     not supply raising/lowering operators.
- **P4, one-sidedness.** A Stage-A PASS proves only that the declared \(h,e,f\)
  candidates are well-defined enough for the exact commutator test; a subsequent
  bracket PASS would establish an `sl2` representation for this pinned gauge only.
  A Stage-A FAIL proves that the declared "natural" triple is underdetermined or
  nonhomogeneous and stops the run. A bracket FAIL refutes only this candidate
  triple, not every Lie structure, every right-inverse gauge, or \(JC(2)\).
- **P5, invariant-first.** Before matrices, test (i) whether one nonzero monomial
  weight makes the full forced polynomial
  \(P_T=y^8(xy-1)^8+x\) homogeneous, (ii) whether the phrase "\(h\) the
  \((v,1-u)\) weight" selects a unique pair on its nine-monomial top edge, and
  (iii) how many distinct raw operator shifts occur. Multiple \(M_0\) degrees or
  multiple proposed raising degrees block the standard relations before any
  matrix bracket is meaningful.
- **P6, budget and kill.** Expected runtime under one second; hard budget one
  minute. If Stage A has not completed by then, stop with no structural claim.
  Stage B, if unlocked, gets a separate five-minute smoke budget before any
  widening.
