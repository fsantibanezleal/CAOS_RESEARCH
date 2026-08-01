# EXP-004 verdict: CONFIRMED: $z_{\max}(7) = 5$: the bottom law breaks at 7

Run 2026-08-01 (rounds 4-5), `run.py` (tclib suite green; smoke replicated
EXP-003 in full: 134,494 / $z_{\max}(6)=5$ / 4 records, 3x faster), repo
venv Python 3.13.0, single process, exact arithmetic; 86.5 min wall total
(stage 1 ~17 min, scan ~69 min; budget 170 min, kill never approached).
Raw output: `artifacts/scan7.json`.

## Results (decision-complete at depth 7 via the last-gate lemma)

| $\tau$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| $z_{\max}$ | 1 | 2 | 3 | 3 | 4 | 5 | **5** |

- Stage 1: depth-6 frontier built EXACTLY: 25,844,905 reached-set states;
  internal gates all passed (state counts 9/98/1462/29506/778087; new-poly
  counts up to 134,494 at depth 6; $z_{\max}(6) = 5$ recomputed).
- Stage 2: complete scan of all 25,844,905 states: 2,013,706 distinct
  depth-7 polynomials; z histogram: 742,635 rootless; 904,421 with one;
  299,488 with two; 63,903 with three; 3,196 with four; 63 with five;
  ZERO with six or more.
- **Prediction 1 CONFIRMED: $z_{\max}(7) = 5$.** The growth sequence is
  $1, 2, 3, 3, 4, 5, 5$: a second plateau. The minimal $\tau$ for 6
  distinct integer roots is at least 8 (and at most 9: witness
  $q(q-2)(q-6)$ with $q = x^2 - x$, 9 gates, committed in the EXP-004
  hypothesis; an 8-gate construction is not known to us).
- Prediction 2 CONFIRMED (new-poly count $2.0 \times 10^6$, order $10^6$).

## Reading (two-sided, honest)

The bottom of the ladder now shows plateaus at $\tau = 4$ and $\tau = 7$:
one extra gate is NOT always convertible into an extra root; conversion
succeeds when a cheap structural move is available (the multiply-by-$x$
move at 6) and fails when the next root needs a BUILT constant (beyond
the free $\{0, \pm1, \pm2\}$ world, roots need constants like 3 or 6,
whose construction costs 2-3 gates). Combined with this round's family
results (EXP-005: cycle-length ceiling; stall theorems), the measured
picture is coherent: root acquisition is gated by constant-building, and
every known mechanism pays roughly constant gates per root: the
linear-rate world, comfortably inside the conjecture. No superlinear
mechanism through depth 7, now with the mechanism inventory
theorem-bounded (periods $\le 2$) on the iteration side.

## Adversarial validation record

- The interned engine is a REIMPLEMENTATION of the census core, gated
  in-run against every prior anchor (EXP-001/002/003 values) before
  stage 2 was trusted; smoke = full EXP-003 replication.
- Root counts on the 63 five-rooters: certified by the divisor argument;
  spot replay of records was already covered at depth 6 (the depth-7
  five-rooters are new polynomials but none is a RECORD, so no witness
  reconstruction was required by the hypothesis; the record set of the
  census remains the depth-6 one).
- Memory guard and deadline honored; cache stabilized at 15.1M entries
  (under the 40M cap).

## How could this be wrong?

Same soundness surface as EXP-003 (last-gate lemma + normalization
lemmas), exercised here at 33x scale with all gates green. The single
shared-blind-spot risk (tclib arithmetic) remains hedged by the sympy
cross-check (284/284, round 3) and the EXP-005 escape-bound cross-check.

## Consequences for the strategy

- The census spine has decided depths 1-7 with two plateaus; depth 8 by
  this method would need the ~25.8M-state frontier EXPANDED (~700M-1B
  states): out of single-machine naive reach; the declared routes are
  TCB-005 proved canonicalization, a compiled/parallel backend, or the
  RL-7 SAT lane for targeted $T(S)$ decisions (does a 8-gate 6-rooter
  exist? is now a crisp SAT-shaped question).
- The minimal-$\tau$(6 roots) window is $[8, 9]$: closing it is the next
  decision-bearing question and a natural first SAT-lane target.
- The bottom law is FALSIFIED as a law; the honest summary for the wiki:
  $z_{\max}$ grows, but with constant-building friction visible as
  plateaus: the first measured structure in the growth function.
