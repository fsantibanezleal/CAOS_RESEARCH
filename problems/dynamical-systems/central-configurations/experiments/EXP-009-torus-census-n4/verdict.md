# EXP-009 - Verdict: INCONCLUSIVE-CAP ON BOTH ROUTES (2026-08-01; the n = 4 torus census exceeds our direct-solve budget; the bounding and incidence-dimension routes become the way in)

Hypothesis: `hypothesis.md` (declared and committed BEFORE any run, commit bb2902e).
Runner: `run.py` (smoke test + route A), `finish.sh` (detached budget enforcement),
`analyze.py` (exact census analyzer, unused this round: nothing to analyze).
Artifacts: `artifacts/` (both msolve inputs, finish log, run log).

## What happened, honestly

| Item | Outcome |
|---|---|
| Smoke test | PASS: the exact square of EXP-001 (side minimal polynomial 32x^6 - 32x^3 + 7) satisfies every equation of the built route-A system exactly |
| Route A (enriched planar system + Rabinowitsch saturation; 7 unknowns) | INCONCLUSIVE-CAP: msolve produced no output within the declared 3600 s; the cap was enforced (the first run was killed at exactly 3600 s by the detached finisher after the controlling shell died) |
| Route B (the Hampton-Moeckel z-system, 12 equations, 12 unknowns, saturated) | INCONCLUSIVE-CAP: two attempts; the first was killed by a WSL virtual-machine idle shutdown (infrastructure, not budget: recorded, fix deployed), the second ran its full 3600 s cap and produced no output |
| P1 (dimension 0 in the torus) | UNDECIDED: neither route returned a dimension |
| P2 (50 realizable labeled solutions), P3 (4 classes with the exact square), P4 (cross-route agreement) | UNTESTED: no solution sets were produced |

Per the declared kill criterion (methodology/12 P6): both cells are recorded
inconclusive-cap, no silent retries at larger budgets, and the published counts
(50 and 4) remain UNTESTED BY US, exactly as EXP-006's verdict already stated.

## Reading the result (what a double cap actually says)

This is informative, not merely disappointing, for three reasons.

1. **It matches the literature's own behavior.** Hampton-Moeckel did not solve this
   system either. They proved finiteness and then BOUNDED the count with a mixed
   volume (25380 for their z-system, giving at most 8460 noncollinear solutions);
   the only exact equal-mass counts in the record come from Albouy's classification
   by hand-plus-computer case analysis and from interval listings
   (Moczurad-Zgliczynski), not from a direct algebraic solve. Our double cap is
   consistent with the direct solve being genuinely out of practical reach for
   Groebner-based engines at this size, which is presumably why nobody in the
   literature reports one.
2. **The gap between n = 3 and n = 4 is now measured on our own hardware**: under
   one second per census at n = 3 (EXP-006) against more than an hour without an
   answer at n = 4 (both formulations). That calibrates what "one n more" costs in
   the census lane and disciplines any thought of a direct n = 5 census.
3. **It forces the strategically correct routes**, which the approaches evaluation
   (program/central-configurations/approaches-evaluation-2026-07-25.md) had already
   ranked: for COUNTS, bounding (BKK mixed volume) rather than solving; for
   FINITENESS, the incidence-dimension lane (CCB-033), which needs a dimension
   rather than a solution list. EXP-010 (declared next) opens that lane with a
   calibration at n = 4 and n = 5 against known answers.

## Adversarial-validation record (methodology/03)

- The declared budgets were enforced mechanically (a detached WSL script killed
  route A at exactly 3600 s; route B's second attempt ran under `timeout 3600`),
  so the caps are facts, not judgment calls.
- The infrastructure failure that killed route B's first attempt is documented with
  its root cause (WSL vmIdleTimeout) and its permanent fix; it is not counted as
  evidence about the mathematics.
- The smoke test passed before any solver time was spent, so the caps are about
  solver difficulty, not about a malformed system.

## How could this be wrong?

- A cap proves nothing about the system's true difficulty beyond this engine and
  budget; msolve with different options (elimination order, RUR on a better
  variable), a larger budget, or another engine (magma, FGb) might decide it. The
  verdict claims only what was measured: OUR declared budgets do not suffice.
- Route B's system was rebuilt after the interruption from the same generator; the
  repo artifact and the file actually consumed on WSL agree byte-for-byte
  (SHA-256 77bfea6e9b81c8a36286b214559bcdf12a21e2448a19f8255c82f64ffdd23dc4;
  route A: 526ec58a6d7357644efe921f97cb176b32f69718448e07249ce92a3dbbc6eb1b).
  The route-B file is small (347 bytes) because the z-system is genuinely sparse:
  the whole system is the moment condition, four linear-in-z equations, six
  product equations encoding S_ij = z_i z_j, and one Rabinowitsch equation.

## Consequences for the strategy

1. The n = 4 exact census by direct solve is CLOSED as a lane at current budgets;
   the ground-truth comparison moves to (a) the BKK bounding rung (reproduce
   HM06's 25380 with our own mixed-volume computation, which bounds without
   solving) and (b) interval listing a la Moczurad-Zgliczynski if a census is ever
   truly needed.
2. EXP-010 (incidence-dimension calibration, CCB-033) is the next declaration: it
   asks for dimensions, not solution lists, which is exactly the quantity the
   double cap shows we should not brute-force.
3. The manuscript's census section gains one sentence stating the double cap and
   the redirect, keeping the record honest about what was not achieved.
