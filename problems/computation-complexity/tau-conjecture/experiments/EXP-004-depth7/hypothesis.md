# EXP-004: $z_{\max}(7)$: does the bottom law $z = \tau - 1$ break?

Declared 2026-08-01 (round 4), before the run.

## Question

Exact value of $z_{\max}(7)$, deciding the bottom-law question (view V6,
round-4 addendum): does $z_{\max}(\tau) = \tau - 1$ continue at
$\tau = 7$ (value 6), or break (value 5)?

## Method (engineering only; NO unproved pruning)

Two stages, both exact, one optimized implementation (interned
polynomials as integer ids, op-result memo cache, states as sorted id
tuples):

1. Build the depth-6 frontier by expanding the exhausted depth-5 frontier
   (778,087 states). Internal regression gates: the expansion must
   re-yield exactly 134,494 new depth-6 polynomials and $z_{\max}(6) = 5$
   with the same 4 records (EXP-003 anchors), and the depth 1-5 state
   counts must match (9/98/1462/29506/778087). Estimated depth-6 frontier
   ~15-25M states, ~3-6 GB (machine verified this round: 48 GB, 24
   cores).
2. Last-gate scan over the depth-6 frontier (the EXP-003 lemma, applied
   one level up): decides $z_{\max}(7)$ exactly without storing the
   depth-7 frontier.

## Falsifiable predictions (committed before the run)

1. **$z_{\max}(7) = 5$: the bottom law BREAKS at 7.** Reasoning committed
   with the prediction: the depth-6 record states carry only the constant
   $-2$; a 6th root beyond the stable core $\{0, \pm1, \pm2\}$ requires a
   built constant ($\pm 3$-shifts or new factor roots), and every hand
   construction found costs $\ge 2$ extra gates (e.g. 6-rooters
   $q(q-2)(q-6)$ with $q = x^2-x$ at 9 gates; $\pm x(x^2-1)(x^2-4)(x-3)$
   at 9). EXP-003 refuted our previous such judgment, so confidence is
   explicitly moderate; either outcome is a decision-grade result.
2. The depth-7 new-polynomial count is on the order of $10^6$
   (extrapolating the ~9-12x growth: 1249, 11377, 134494).

## One-sidedness

The scan is decision-complete for depth 7 given the last-gate lemma and
an exhausted depth-6 frontier: exact $z_{\max}(7)$ either way; nothing
asymptotic follows. Prediction 1's refutation would extend the bottom
law and expose a constant-free 6-rooter mechanism (recorded in full, as
in EXP-003).

## Premise dependencies (P3)

- Last-gate lemma (EXP-003 hypothesis, [D]).
- EXP-001/002/003 verdicts as anchors (14/14 Markstroem; state counts;
  134,494; $z_{\max}(6) = 5$).
- tclib suite green (now 8 tests, incl. tower + monic-stall checks).
- The interned reimplementation is gated by the EXP-003 anchors INSIDE
  this run (stage-1 gates above) before stage 2 is trusted.

## Invariant-first note (P5)

The stall theorem (this round) excludes all single-inner-map towers from
ever beating a constant, so no invariant decides depth 7; the census
scan is the cheapest known decider. Justified.

## Compute budget and kill criterion (P6)

- Smoke (P2): the interned engine must reproduce depths 1-5 + the
  EXP-003 scan numbers (11,377 at depth 5 base) within a minute, with
  flushed progress and a written checkpoint.
- Budget: 3 hours wall, single process, CPU only; memory guard 30M
  states (abort stage 1 above it).
- Kill: if stage 1 exceeds 100 min or the guard trips: checkpoint state
  counts, report depth 7 INCONCLUSIVE (bounds $5 \le z_{\max}(7) \le
  z_{\max}(8)$ trivial side), and route to the multiprocess backend next
  round. If stage 2 exceeds the remaining budget: same, with
  states-scanned recorded.
- Expected: stage 1 ~10-30 min; stage 2 ~20-60 min.

## Success and failure criteria

- CONFIRMED: both stages complete; $z_{\max}(7)$ exact; predictions
  scored (the CENSUS is confirmed regardless of which way prediction 1
  goes; the prediction verdict is reported separately).
- REFUTED (tooling): any internal gate mismatch.
- INCONCLUSIVE: kill criterion.
