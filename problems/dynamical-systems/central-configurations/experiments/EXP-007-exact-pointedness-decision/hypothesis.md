# EXP-007: exact decision of pointedness for every comet (closing EXP-004's undecided cases)

Declared: 2026-07-24, BEFORE any run. Route: R2/tropical lane (instrument
hardening). Backlog: CCB-032. Follows EXP-004, whose analyzer left exactly one
UNDECIDED comet in each failing control and therefore reported "no certificate"
rather than "not pointed".

## Question

Is every comet of every EXP-004 prevariety DECIDED exactly, and in particular are
the undecided comets of the failing controls genuinely UNPOINTED?

## The instrument

A cone is pointed exactly when the only nonnegative solution of
sum_i lambda_i g_i = 0 is lambda = 0. That is one linear feasibility question,
decided here by a phase-I simplex in exact `Fraction` arithmetic with Bland's rule
(`code/cclib/exact_lp.py`): FEASIBLE returns an explicit nonnegative zero
combination (certificate of unpointedness, verified by exact substitution);
INFEASIBLE returns a separating vector with strictly negative pairings against
every generator (certificate of pointedness, also verified exactly). The system has
one row per ambient coordinate plus a normalization row (11 or 12 rows), so the
cost grows with the generator count, not with a big matrix.

## Falsifiable predictions

- **P1 (total decidability).** Every comet of every EXP-004 output is decided:
  zero UNDECIDED remain, across all 16 cells.
- **P2 (the failing controls are genuinely unpointed).** The single undecided comet
  of each failing control (n = 5 arithmetic (0,1,2,3,4) with 71 generators; n = 5
  repeated (1,1,9,27,81) with 95; n = 4 equal (0,0,0,0) with 49) is UNPOINTED, with
  an explicit nonnegative zero combination. This upgrades EXP-004's negative half
  from "no certificate found" to a proof, and independently confirms the failure
  Jensen-Leykin report for arithmetic valuations at n = 5.
- **P3 (agreement on the positives).** Every comet that EXP-004's heuristic
  certified as pointed is confirmed pointed by the exact decider: no positive
  flips. A flip would be a serious instrument alarm and would invalidate EXP-004's
  positive half.

## Preflight (methodology/12)

- **P1 source-complete.** The mathematical criterion is standard (a cone is pointed
  iff its lineality space is trivial iff no nontrivial nonnegative zero
  combination exists); Jensen-Leykin use pointedness of recession cones in exactly
  this sense, and their paper is read in full. No unread source bears on it.
- **P2 tooling smoke test.** DONE before declaring: the decider was exercised on
  four hand cases including one unpointed cone with no antipodal pair (it returned
  lambda = (1/2, 1/4, 1/4), verified exactly).
- **P3 premise dependencies.** (a) The comet decomposition is correct: validated in
  EXP-004 by reproducing Jensen-Leykin's published 257-component count. (b) The
  recession generators are the unbounded rays of each comet: gfan's documented
  semantics under `--usevaluation`, consistent with the ray counts.
- **P4 one-sidedness.** Two-sided throughout: the decider always returns a
  certificate, and both kinds are verified by exact substitution, so every outcome
  is a proof rather than a search failure.
- **P5 invariant-first.** The cheap invariant (an antipodal generator pair) already
  runs inside the old analyzer and did not decide these comets; that is precisely
  why the LP is needed.
- **P6 budget and kill criterion.** 1800 s per output file, 2 hours total. If a
  cell hits its cap it is recorded inconclusive-cap, and the affected comets stay
  UNDECIDED in the record, with EXP-004's conclusions unchanged.

## Success / failure criteria

SUCCESS: P1, P2, P3 hold. FAILURE: any positive flip (P3) stops the tropical lane
until resolved; a decided-pointed outcome for a control comet (P2 refuted) would
mean the controls do not fail the way the literature says, which is itself a
finding and would be reported as such.

## Method / environment

`run.py`: re-parses each EXP-004 prevariety output (from `E:\_Datos\...\EXP-004\`),
rebuilds the comets with the corrected slice semantics, and decides each recession
cone with `cclib.exact_lp.decide_pointed`. Deterministic; exact throughout;
certificates persisted per comet.
