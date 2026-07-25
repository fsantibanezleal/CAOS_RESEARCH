# EXP-008 - Verdict: P1 AND P2 REFUTED, P3 CONFIRMED (2026-07-24; Dziobek is tropically active but does not rescue the hard case, and the f-vector is the wrong monotone invariant)

Hypothesis: `hypothesis.md` (declared and committed BEFORE any run, commit 6b9ca06).
Runner: `run.py`. Instrument: the EXP-007 exact decider on every comet. Artifacts:
`artifacts/table.json`, `run-log.txt`, inputs and outputs per cell.
Environment: gfan 0.7, WSL2, 8 threads, `--bits 0` (arbitrary precision).

## The grid (n = 4; every comet decided exactly, no heuristics)

| Valuations | System | f-vector | comets | pointed | unpointed |
|---|---|---|---|---|---|
| equal (0,0,0,0) | A1 baseline | 1 49 66 18 | 1 | 0 | **1** |
| equal | A2 = A1 + e_IU | 1 49 66 18 | 1 | 0 | **1** |
| equal | A3 = A1 + Dziobek | 1 37 48 12 | 1 | 0 | **1** |
| equal | A4 = A1 + both | 1 37 48 12 | 1 | 0 | **1** |
| powers of 2 (1,2,4,8) | A1 | 63 119 82 19 | 10 | 10 | 0 |
| powers of 2 | A2 | 63 119 82 19 | 10 | 10 | 0 |
| powers of 2 | A3 | 64 131 101 27 | **7** | 7 | 0 |
| powers of 2 | A4 | 64 131 101 27 | **7** | 7 | 0 |
| arithmetic (0,1,2,3) | A1 | 83 164 108 23 | 9 | 9 | 0 |
| arithmetic | A2 | 82 162 107 23 | 9 | 9 | 0 |
| arithmetic | A3 | 86 183 135 34 | **6** | 6 | 0 |
| arithmetic | A4 | 85 181 134 34 | **6** | 6 | 0 |

## Predictions

- **P1 (monotone f-vector shrinking): REFUTED, with a structural correction.**
  Adding Dziobek's equations GROWS f-vector entries at the powers-of-2 and
  arithmetic valuations (119 -> 131, 82 -> 101, 19 -> 27 at powers of 2) while
  SHRINKING them by about 25 percent at equal valuations (49 -> 37, 66 -> 48,
  18 -> 12). The prediction conflated two different things: the prevariety as a SET
  and the polyhedral subdivision that represents it. Adding valid equations
  intersects more tropical hypersurfaces, which can only shrink the set but REFINES
  the subdivision, so cone counts may rise. The correct monotone invariant is the
  COMET COUNT, and in our data it decreases monotonically everywhere:
  10 -> 7 (powers of 2), 9 -> 6 (arithmetic), 1 -> 1 (equal). The refutation is
  therefore about our choice of invariant, not about the mathematics, and it is
  exactly the kind of confusion the declaration-before-run discipline surfaces.
- **P2 (Dziobek rescues the hard equal-valuation case): REFUTED.** With Dziobek
  adjoined the equal-valuation prevariety shrinks by a quarter, yet its single comet
  remains UNPOINTED, now with an exact nonnegative zero combination certifying it.
  Consequence, and the informative content of this experiment: the enrichment that
  rescued the ALGEBRAIC proof of Hampton-Moeckel (who state they could not run their
  method on the Albouy-Chenciner equations alone) does NOT rescue the TROPICAL
  certificate at the same specialization. The two roles of Dziobek's equations come
  apart: they are tropically active (they cut the prevariety and merge comets) but
  not tropically decisive at the hard case.
- **P3 (no positive flips): CONFIRMED.** Every valuation that certified under the
  baseline still certifies under all three enrichments: 10, 10, 7, 7 comets at
  powers of 2 and 9, 9, 6, 6 at arithmetic, all pointed.

## Additional findings

1. **The energy-inertia relation is tropically inert.** A2 reproduces A1's f-vector
   exactly at equal and powers-of-2 valuations, and shrinks it by one cone at
   arithmetic. Consistent with it being an algebraic consequence of the AC
   equations: it adds no new initial-form conditions. Contrast with the dependent
   SYMMETRIC equations, whose removal was catastrophic in EXP-004: dependence in the
   ideal does not predict tropical relevance in either direction, which is the
   sharper form of EXP-004's lesson.
2. **A reproducible gfan bug, with a free workaround.** Under `--bits 0`, gfan 0.7
   fails to parse an input mixing `t^0` with positive t-powers ("Unknown
   variable:1"), while the byte-identical file parses under `--bits 64`. Since every
   polynomial of the system is homogeneous in the masses (AC linear, e_IU quadratic,
   Cayley-Menger and Dziobek mass-free), shifting all valuations by a constant
   multiplies each polynomial by a unit and leaves the tropical prevariety
   unchanged; shifting to avoid zero valuations sidesteps the bug at no
   mathematical cost. Recorded in the runner and reusable by the lane.

## Adversarial-validation record (methodology/03)

- Every comet verdict here is an exact certificate from the EXP-007 decider, not a
  heuristic, and the baseline A1 cells reproduce EXP-004's numbers exactly
  (equal: 1 49 66 18; powers of 2: 63 119 82 19; arithmetic: 83 164 108 23), which
  cross-validates the new input-construction path against the previous one.
- The Dziobek generator was unit-tested before use: the exact square of EXP-001
  (side minimal polynomial 32x^6 - 32x^3 + 7) satisfies all three equations exactly.
- The valuation-shift workaround was validated by construction (unit multiples) and
  empirically: the shifted arithmetic baseline reproduces the unshifted EXP-004
  f-vector 83 164 108 23 digit for digit.

## How could this be wrong?

- Dziobek's equations hold on the planar NONCOLLINEAR stratum. A certificate
  obtained with them therefore covers that stratum; the 12 collinear classes are
  classical (Moulton). The A3/A4 cells must be read with that scope, and the
  positive cells here are not claimed as full generic-finiteness certificates: the
  A1 cells already provide those.
- Unpointedness of the equal-valuation comet does not prove that finiteness fails at
  equal valuations; the prevariety over-approximates the tropical variety. It proves
  only that this certificate route does not close at that specialization.

## Consequences for the strategy

1. Track the COMET COUNT, not the f-vector, as the shrinkage measure in the lane.
2. Dziobek enrichment is worth carrying at n = 4 (a third of the comets disappear)
   but it is not a rescue mechanism for hard valuations; at n = 5 and n = 6 planar
   it is unavailable anyway, since the Dziobek stratum there has dimension n - 2 > 2.
3. e_IU can be dropped from tropical runs with no loss, which is a small but free
   saving for the expensive n = 6 attempts.
4. The valuation-shift trick is now standard for `--bits 0` runs.
