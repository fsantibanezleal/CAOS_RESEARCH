# EXP-007 - Verdict: CONFIRMED on all three predictions (2026-07-24; every comet decided exactly, the failing controls are provably unpointed)

Hypothesis: `hypothesis.md` (declared and committed BEFORE the run, commit c4ab69a).
Instrument: `code/cclib/exact_lp.py` (phase-I simplex over `Fraction`, Bland's rule).
Runner: `run.py`. Artifacts: `artifacts/summary.json`, per-cell unpointedness
certificates, `run-log.txt`. Recorded run: 2026-07-24 06:49:21 to 06:49:54, 33
seconds for all sixteen cells.

## Verdict

| Prediction | Outcome | Machine result |
|---|---|---|
| P1 total decidability | CONFIRMED | all 16 cells fully decided; ZERO undecided comets; zero certificate-verification failures |
| P2 the failing controls are genuinely unpointed | CONFIRMED | n = 4 equal valuations (0,0,0,0): the single comet is UNPOINTED; n = 5 arithmetic (0,1,2,3,4): 180 pointed + 1 UNPOINTED; n = 5 repeated (1,1,9,27,81): 210 pointed + 1 UNPOINTED; every S2 cell: exactly one UNPOINTED comet. Each carries an explicit nonnegative zero combination, re-verified by exact substitution independently of the decider |
| P3 no positive flips | CONFIRMED | every comet EXP-004 certified pointed is confirmed pointed: 281/281 (pow3), 257/257 (squares), 266/266 (pow2), 250/250 (primes) at n = 5, and 10/10, 10/10, 9/9 at n = 4 |

## What this changes

EXP-004's negative half was operational ("no certificate found"). It is now a
PROOF: the recession cone of the offending comet contains a line, exhibited as an
explicit nonnegative combination of its generators that sums to zero. Consequences:

1. Our data now independently CONFIRMS, rather than merely being consistent with,
   Jensen-Leykin's report that arithmetic valuations (0,1,2,3,4) fail at n = 5, and
   it localizes the failure to exactly one comet out of 181.
2. The n = 4 equal-valuation case (0,0,0,0) is provably unpointed, which is the
   sharp form of their observation that this specialization is as hard as the
   original Hampton-Moeckel computation.
3. Every S2 cell (symmetric equations removed) is provably unpointed, so EXP-004's
   headline finding, that the algebraically redundant symmetric equations are
   tropically load-bearing, now rests on proofs on both sides: certificates where
   they are kept, refutations where they are dropped.
4. The instrument is cheap: 33 seconds for all sixteen cells, versus a heuristic
   that could not decide these cases at all. It becomes the default decision
   procedure for the lane, including the n = 6 outputs when they land.

## Adversarial-validation record (methodology/03)

- Every certificate is re-verified in `run.py` INDEPENDENTLY of the decider that
  produced it: for pointedness, all generators pair strictly negatively with the
  separating vector; for unpointedness, the nonnegative multipliers sum to a
  strictly positive total and annihilate every coordinate exactly. Zero failures.
- The decider was smoke-tested before declaration on four hand cases, including an
  unpointed cone with NO antipodal generator pair (the case the old heuristic
  structurally could not catch), where it returned lambda = (1/2, 1/4, 1/4).
- Cross-check against the previous instrument: the 1361 comets the heuristic had
  certified are all confirmed, and the 6 it could not decide are now decided; the
  two instruments disagree nowhere.

## How could this be wrong?

- The decision assumes the recession generators of a comet are exactly the unbounded
  rays gfan lists for its cones. That reading was validated in EXP-004 by
  reproducing the published 257-component count; it remains the load-bearing
  convention.
- Exact arithmetic removes numerical doubt, but a bug in the tableau update would
  produce a wrong certificate. That is why every certificate is re-verified outside
  the decider, by direct substitution: a wrong certificate cannot pass that check.
- Pointedness of every comet is JL25's sufficient condition for dimension zero.
  Unpointedness of one comet does NOT prove the variety is positive-dimensional:
  the prevariety only over-approximates the tropical variety. Our negative results
  are therefore about the CERTIFICATE, not about finiteness itself, and the verdict
  states them that way.

## Consequences for the strategy

1. CCB-032 closed. The exact decider replaces the heuristic everywhere.
2. EXP-004's verdict is amended by reference (its negative half is upgraded here);
   the manuscript's screening section is updated to state proofs rather than
   absences.
3. For n = 6 (EXP-005, running): whatever the prevariety turns out to be, its
   comets will be decided exactly by this instrument, so the outcome will be a
   certificate either way.
