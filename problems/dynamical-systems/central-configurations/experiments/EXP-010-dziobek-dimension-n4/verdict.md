# EXP-010 - Verdict: EMPTINESS PROBES CONFIRMED IN SECONDS, CENSUS PROBES REFUTED BY CAP (2026-08-01; dim <= 3 gains probabilistic-exact support at trivial cost; the lane keeps cheap upper bounds and loses msolve censuses at this size)

Hypothesis: `hypothesis.md` (declared and committed before any run).
Runner: `run.py` (smoke + four msolve probes), `p3_dim.py` (deterministic rung).
Artifacts: `artifacts/` (drawn sections verbatim in draws.json, all msolve inputs,
both P2 raw outputs, run log, results.json).

## Outcomes against the declared predictions

| Prediction | Outcome | Facts |
|---|---|---|
| Smoke gate (three-way discrimination) | PASS in 1 s | square: all three stripped Dziobek differences AND Cayley-Menger vanish (exact polynomial reduction modulo 8A^3 = 4 + S2, S2^2 = 2, no radical heuristics); unit tetrahedron: Dziobek differences vanish, CM = 4 (nonzero, exact); 3-4-5 rectangle: CM = 0, Dziobek differences nonzero |
| P1 (two 3-section censuses, nonempty + degree, 900 s caps) | REFUTED BY CAP (the declared kill criterion fired) | both draws produced no msolve output at the inner 900 s timeout (952 s and 958 s wall including WSL overhead) |
| P2 (two 4-section emptiness probes, 900 s caps) | CONFIRMED, in 1 s each | msolve returned `[-1]:` (the empty-variety output, dimension -1) for both independent draws |
| P3 (deterministic grevlex staircase dimension = 3, 1800 s cap) | INCONCLUSIVE-CAP | the sympy Groebner computation did not finish inside its subprocess cap |
| P4 (degree agreement across the P1 draws) | UNTESTED | no degrees were produced |

## What is now supported, and how strongly

- **dim D4 <= 3 (upper bound), probabilistic-exact.** Two INDEPENDENT random
  codimension-4 affine-linear sections (integer coefficients drawn uniformly
  from [-10^6, 10^6] by the seeded generator declared in the hypothesis, draws
  recorded verbatim) meet the Dziobek variety in NO complex point, each decided
  exactly by msolve in one second. Any component of dimension >= 4 would meet a
  generic codimension-4 section; missing two independent ones is the evidence.
  Honesty about the bound: the hypothesis planned an a-posteriori failure bound
  from the measured degree, and no degree was measured (P1 capped), so only a
  crude a-priori ceiling is available (Bezout with the stripped degrees
  9 * 9 * 6 = 486 for two independent Dziobek differences plus Cayley-Menger),
  giving a failure estimate of order 10^-3 per draw with this coefficient range.
  This is evidence, not proof, and the verdict claims nothing stronger.
- **dim D4 >= 0** is exact and unconditional (the EXP-001 square lies on D4 by
  the smoke certificate). NO lower-bound evidence beyond 0 was obtained: the
  nonempty-census half of the instrument is exactly the half that walled.
- **The asymmetry is the discovery.** Emptiness (a Groebner basis collapsing to
  1) costs seconds; describing solutions (RUR over a large-degree eliminant)
  walls at this size, consistently with EXP-009. Upper bounds are cheap, and
  upper bounds are precisely what generic-finiteness arguments consume (what
  must be excluded is EXCESS dimension). The lane survives with its cheap half.

## Instrument consequences (per the declared consequence ladder)

1. The ENGINE-REFUTED branch fires for the census half: msolve 3-section
   censuses of D4 are closed at 900 s scale; CCB-034 (witness sets,
   HomotopyContinuation.jl with certification) is PROMOTED as the lower-bound
   and degree-data instrument.
2. The emptiness half is VALIDATED and stays: recorded random codim-(d+1)
   sections deciding empty in seconds is a general cheap upper-bound probe.
3. CCB-037 (the Dias-Pan Lemma 7.5 partial-Groebner device, read in full this
   morning: union of leading monomials of tractable subideals bounds the
   dimension DETERMINISTICALLY) is pulled forward as the deterministic
   companion for the same upper-bound direction, replacing the capped P3 full
   staircase.
4. Composite plan for EXP-011 (n = 5 spatial Dziobek, expected dim 4): cheap
   emptiness probes at codim 5 (probabilistic upper bound) + partial-GB leading
   terms (deterministic upper bound) + a witness point with an exact Jacobian
   rank certificate (lower bound at the witness), which is exactly the Dias-Pan
   proof shape executed with our exact instruments.

## Limitation stated up front (from the session exploration note, verbatim in substance)

Random linear sections of codimension d see only components of dimension >= d;
components of smaller dimension are invisible, and the staircase rung also
reports only the maximum. EXP-010's claims are therefore about the MAXIMUM
dimension of D4. That is the right one-sided direction for generic finiteness,
but nothing here describes the component structure below the top dimension; if
that ever becomes the question, witness sets (CCB-034) are the instrument.

## Adversarial validation record (methodology/03)

- Could `[-1]:` mean an error rather than emptiness? No: msolve exited OK (the
  runner checks the sentinel), `[-1]:` is msolve's documented empty output
  (dimension -1), and the P2 inputs differ from the 900-second P1 inputs by
  exactly one additional random hyperplane, so a malformed-input explanation
  would have broken P1 identically and instantly instead of running to cap.
- Could the P2 emptiness be an artifact of a DEGENERATE draw (sections
  intersecting in a special position)? Two independent draws from a 2 * 10^6
  value range behaving identically makes that the ~10^-3-order event bounded
  above; and a degenerate draw would generically produce MORE intersection,
  not less.
- The P1 caps were enforced by the inner `timeout 900`; the wall overshoot
  (952/958 s) is WSL startup plus file transfer, not budget creep.
- The smoke acceptance is polynomial-reduction arithmetic over QQ (reduced()
  against a two-element Groebner basis with coprime leading terms), not
  simplify/equals heuristics.

## Records

- results.json in artifacts holds the per-cell outcomes; the raw msolve outputs
  for both P2 draws are archived (`p2-draw1.out`, `p2-draw2.out`, both `[-1]:`).
- The parse fields "dim=None complex-count=None" in the run log reflect a
  runner-side parser that did not recognize the comma-free `[-1]:` form; the
  raw outputs are unambiguous and quoted here directly. The parser gap is
  recorded as a code note for the next runner, not rerun (outputs archived).
