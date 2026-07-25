# EXP-006 - Verdict: P1 AND P2 CONFIRMED, P3 REFUTED AS POSED (2026-07-24; the capped censuses are completed and cross-verified, the n = 4 affine system is positive-dimensional)

Hypothesis: `hypothesis.md` (declared and committed BEFORE any run, commits a29b5b5
and the runner in the same round). Engines: msolve 0.10.1 (WSL, SHA-256
be6ea2289f0fab9847bf7dec1ef4e89cb66f83da064a7b4b0749876a3d18d8ff) computing, sympy
1.14 verifying. Artifacts: `artifacts/` (msolve inputs and outputs, per-sample
verification JSON, log). Recorded run: 2026-07-24 06:45:02 to 07:14:13.

## Verdict

| Prediction | Outcome | Machine result |
|---|---|---|
| P1 agreement where both engines decide | CONFIRMED | masses (1,1,1) and (1,1,2): msolve returns exactly 4 positive real boxes each; all four of our exact points fall inside distinct boxes; zero unexplained boxes |
| P2 completion of the capped samples | CONFIRMED | masses (1,2,3) and (2,3,5), which exceeded the sympy census cap in EXP-002, are DECIDED by msolve in under a second each: exactly 4 positive boxes, containing exactly our four exact points (equilateral plus one collinear per ordering), zero unexplained boxes |
| P3 the n = 4 equal-mass planar census | **REFUTED AS POSED** | msolve returns `[1, 6, -1, []]`: the affine system (symmetric + asymmetric AC + energy-inertia + Cayley-Menger, six distance variables) has DIMENSION 1, so it has no isolated-solution census to report. The predicted class count could not be tested on this object |

## What P3's refutation teaches

The prediction assumed the enriched planar system is zero-dimensional at n = 4, by
analogy with n = 3 where enrichment sufficed (EXP-002). It is not. Diagnostics run
in the same session:

- The obvious suspects are excluded: the loci r12 = 0, r12 = r34 = 0 and
  r12 = r13 = r23 = 0 do NOT lie in the variety (15, 20 and 3 of the equations
  respectively fail to vanish there), so the extra dimension is not the
  vanishing-distance pathology that EXP-001 found at n = 3.
- The remaining explanation is the one the literature already acts on: the census
  must be taken in the TORUS, where every mutual distance is invertible. This is
  exactly why Hampton-Moeckel work with the torus and BKK rather than with the
  affine variety, and why saturation was needed at n = 3 before enrichment replaced
  it. The saturated system (Rabinowitsch variable on the product of all six
  distances) was submitted to msolve as a diagnostic and had not returned within
  the session's budget, so the corrected census is a NEW experiment, not a rescue
  of this one.

The counts themselves therefore remain untested against the published ground truth
(4 classes modulo rotation, reflection and permutation; 50 modulo rotation only).
The verdict records that honestly rather than quoting the literature as if we had
reproduced it.

## What the confirmed half establishes

1. The two censuses that our own engine could not finish are now COMPLETE, and they
   agree exactly with the classical answer: for four different positive mass
   vectors, the n = 3 positive census is precisely the equilateral point plus one
   collinear point per ordering.
2. The cross-engine agreement is exact, not numerical: msolve's rational isolating
   boxes are tested for containment of our independently computed algebraic points,
   and the counts match with no unexplained boxes. Two independent implementations
   (Groebner + RUR + certified isolation, versus Stickelberger eliminants + exact
   residual acceptance) agree on every decided instance, which is the
   cross-implementation rung of methodology/03.
3. The engine split now has measured justification: msolve decides in about a second
   what saturated our sympy path for 40 minutes, while sympy remains the layer that
   verifies msolve's output exactly.

## How could this be wrong?

- Containment of an exact algebraic point in a rational box is decided exactly, so a
  false match is impossible; a false MISS would show up as an unmatched exact point,
  and none occurred.
- msolve's box list is trusted for COMPLETENESS (that it found every real solution).
  If it silently dropped one, our test would not catch it, since we only verify that
  our known points are present and that no extra boxes remain. At n = 3 the expected
  count is classical and matched exactly, which is the available check.
- The dimension report `[1, 6, -1, []]` is msolve's, not independently confirmed by
  us; the diagnostic evidence above supports it, and the saturated rerun will settle
  it in the follow-up experiment.

## Consequences for the strategy

1. EXP-002's inconclusive-at-cap cells are now closed as CONFIRMED classical.
2. The n = 4 planar census moves to a new experiment on the TORUS (saturated
   system), with a longer budget and the option of the HM06 z-variable formulation
   (their equation (13), a square 10 x 10 system to which BKK applies directly).
3. Standing rule reinforced: the affine variety and the torus variety are different
   objects, and every census statement must name which one it is about.
