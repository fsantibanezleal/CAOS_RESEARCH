# EXP-002 verdict (2026-07-24)

Hypothesis: `hypothesis.md` (declared and committed 2026-07-24 BEFORE any run, commit
1c6cb16). Runner: `run.py` (staged, capped; census instrument v2 in `code/cclib`).
Artifacts: `artifacts/`. Recorded run: 2026-07-24 03:32:45 to 04:11:29 (2324 s), sympy
1.14, Python 3.13, CPU only, deterministic.

## Verdict: confirmed on every decided prediction; P2 inconclusive at caps (2 of 4 samples)

| Prediction | Outcome | Machine result |
|---|---|---|
| P1 enrichment kills the lines | CONFIRMED | the enriched ideal (F + G + e_IU) is ZERO-DIMENSIONAL DIRECTLY for all four mass samples, grevlex GB of size 24 in 0.7-0.8 s each, NO saturation; the EXP-001 line {r13 = r23 = 0} fails the G-equations identically in symbolic masses |
| P2 classical n = 3 census | INCONCLUSIVE-CAP (no failure) | decided samples (1,1,1) and (1,1,2): EXACTLY 4 positive points each: the equilateral + one collinear point per ordering; zero non-realizable, zero non-classical, zero duplicates. Samples (1,2,3) and (2,3,5): the sympy census exceeded the 900 s cap (see the engine note) |
| P3 planar rhombus census | CONFIRMED | with e_CM adjoined, EXACTLY ONE positive solution: the square, b^2 = 2a^2, a = CRootOf(32x^6 - 32x^3 + 7, 1) (the EXP-001 value); clean eliminants x(32x^6 - 32x^3 + 7) and x(4x^6 - 4x^3 - 7); the tetrahedron satisfies the no-CM stratum equations and violates e_CM (= 4): the Dziobek sanity check |
| P4 invariant baseline | CONFIRMED | U = M I exactly at both anchors; J(square) = 1/16 + sqrt(2)/8, J(tetrahedron) = 3 sqrt(6)/32 (exact; the cross-paper matching baseline) |

## What this round establishes

1. **The enriched system (F + G + e_IU, + e_CM for planarity) is the program's
   default object**: it eliminates, at zero cost, both pathologies EXP-001 found in
   the bare symmetric system (coordinate-line components; hours-long saturations).
   This is the n = 3 instance of a pattern now triple-sourced: HM06 could not run
   their method on bare AC and needed Dziobek; HJ11 added G "to generate a more
   refined set of cones"; Jensen-Leykin explicitly call for "different versions of
   the Albouy-Chenciner equations" at n = 6. Quantifying enrichment at PREVARIETY
   level is our minted frontier experiment (CCB-031).
2. **The census instrument v2 is validated at calibration scale**: one grevlex GB,
   Stickelberger multiplication-matrix eliminants (charpoly over QQ via DomainMatrix),
   squarefree dedup, CRootOf isolation, certified-numeric pre-filter, exact residual
   acceptance. Regression tests (4) green on the EXP-001 exact anchors.
3. **The engine limit is measured, not guessed**: for integer-separated masses like
   (1,2,3), the qdim-100 charpoly/acceptance arithmetic blows past 900 s (a probe ran
   2.4 h without finishing). Decision recorded (lenses addendum, self-questioning):
   sympy remains the specification + independent-verification layer; msolve
   (RUR + certified boxes) becomes the computation layer (CCB-025). P2's completion
   on the capped samples re-runs under that engine as a follow-up experiment.

## Adversarial-validation record (methodology/03)

- Independent routes: the P3 square value re-confirmed against EXP-001 (different
  system: enriched + CM vs bare cores) and against the hand Cartesian derivation;
  the P2 decided censuses agree with EXP-001's P3 collinear values (chart route vs
  full-system route) and with the classical Euler-Lagrange count.
- First-run instrument catch (recorded, fixed, regression-gated): Poly.real_roots
  returns roots WITH multiplicity; the un-deduplicated census emitted 8 copies of the
  equilateral point. Caught by inspecting the first recorded run's classes; fixed via
  squarefree parts; a second catch in the same pass: Matrix.charpoly returns a
  PurePoly over its OWN Dummy generator (wrapping its expression in a fresh symbol
  yields a silent degree-0 polynomial). Both are now regression-tested.
- Engine honesty: the capped samples are reported inconclusive, not extrapolated;
  the decided samples' acceptance used exact residuals (equals(0) is True) on every
  equation.

## How could this be wrong?

- P2's decided-sample completeness rests on the Stickelberger argument (every
  coordinate value of V(I) is an eigenvalue of the multiplication matrix) plus exact
  acceptance; an implementation error in the staircase/normal-form matrix would
  break completeness. Mitigations: the eliminants factor into exactly the classical
  values; the regression suite pins the known anchors; quotient dims match between
  runs. Residual risk: low, but a cross-engine check (msolve RUR) is queued and will
  either agree or expose it.
- The certified-numeric pre-filter rejects at |value| > 1e-20 at 40 digits; sympy's
  evalf precision tracking is trusted there. A silent evalf precision failure could
  wrongly reject a true solution; the exact-acceptance layer cannot catch a wrongly
  REJECTED candidate. Mitigation: all expected classical solutions were found on
  every decided sample; the msolve cross-check covers this too.
- P1's zero-dimensionality certificate (pure-power criterion) is standard; it was
  independently exercised in EXP-001 (where it correctly FAILED on the bare system).

## Consequences for the strategy

- EXP-003 candidates: (a) msolve-engine P2 completion on (1,2,3), (2,3,5) + n = 4
  equal-mass planar census against the 4-classes ground truth (CC-P1 entry rung);
  (b) CCB-029 gfan reproduction of the Jensen-Leykin n = 5 prevariety (the tropical
  lane opener). Both hypothesis-first.
- cclib gains nothing new before EXP-003; the enriched builders and census v2 are
  the stable base.
