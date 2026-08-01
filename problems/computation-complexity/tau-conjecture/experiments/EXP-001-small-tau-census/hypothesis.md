# EXP-001: exact census of z_max(tau) for small tau, with an integer regression gate

Declared 2026-08-01, before any run. Opening experiment of the tau-conjecture
program (TC-P0 in `program/tau-conjecture/plan.md`).

## Question

For the constant-free SLP model of the Shub-Smale tau conjecture (inputs
$\{-1, 1, x\}$; gates $+,-,\times$ of fan-in 2; length = number of operation
gates), what is the EXACT value of

$$z_{\max}(\tau) := \max\{\, z(f) : f \ne 0,\ \tau(f) \le \tau \,\}$$

(distinct integer roots) for $\tau \le 4$, and which polynomials attain it?

## Motivation

Dossier section 5 (`context/2026-08-01-deep-research-dossier.md`): the
literature pass found no published census of $z_{\max}$; the growth data and
extremal mechanisms are the experimental image of the conjecture's claim
$z \le (1+\tau)^c$. Markstroem 2014 (read in full) provides the method
pattern (normalized enumeration, set-dedup, targeted pruning) and, on the
integer restriction, published EXACT anchors we can regress against.

## Model lemmas (declared, [D], proved in-place here)

1. **Free 0 is redundant given free $-1$**: any optimal program using the
   constant 0 as an operand can be rewritten at equal length without it
   ($a+0, a-0$ are duplicates; $a \times 0 = 0$; $0-a = (-1) \times a$, same
   single-gate cost). Hence inputs $\{-1,1,x\}$ give the same $\tau$ as the
   survey's $\{-1,0,1,x\}$.
2. **Normalization**: an optimal program never computes a value equal to an
   input or to an earlier value (delete the step, shorten the program), and
   never computes 0 (a computed 0 is only usable as the redundant constant
   of lemma 1). Enumerating only such programs preserves exactness.
3. **Reached-set sufficiency**: the future of a program depends only on the
   SET of values computed so far (order is irrelevant); BFS over reached
   sets with set-level dedup visits every reachable set of each depth
   exactly once. (This is the polynomial analogue of Markstroem's
   range-isomorphism reduction, which he states for the integer case.)

No other pruning is used in this experiment (in particular, no sign-symmetry
pruning: soundness of that reduction is TCB-005, future work).

## Method

`run.py`, deterministic, headless, pure Python 3.13 standard library, exact
integer arithmetic on dense coefficient tuples (degree cap $2^4 = 16$ at
depth 4 is tiny).

- Stage A (regression gate): integer restriction, inputs $\{1\}$, positive
  normalized values (Markstroem's exact setting), BFS over reached sets to
  depth 7. PASS iff reached-set sizes equal his Figure 1 column "Size of
  reached set" (k=1..7: 2, 4, 9, 26, 102, 562, 4363) and initial intervals
  (k=1..7: 2, 4, 6, 12, 40, 112, 310). (Interpretation fixed in advance:
  "reached at k" = computable by a program of length at most k, with 1
  reached at k=0; sizes count reached values including 1.)
- Stage B (the census): polynomial model, BFS by depth to $\tau = 4$; per
  depth record: number of distinct reached sets, number of distinct
  polynomials, $z_{\max}$, and ALL witnesses attaining it (SLP listing,
  polynomial, root list). Integer roots counted exactly: strip $x^m$ (root
  0 if $m > 0$), then test divisors of the trailing coefficient.
- Root counting is independently cross-checked on every witness by a second
  route (evaluate $f$ at each claimed root from its SLP replay; and confirm
  no further roots by the divisor argument).

## Falsifiable predictions (committed before the run)

1. Stage A reproduces Markstroem's seven values exactly. (If not, the
   experiment FAILS and nothing downstream is trusted; we then debug
   against his printed witness programs.)
2. $z_{\max}(1) = 1$, $z_{\max}(2) = 2$ (witness $x^2 - 1$),
   $z_{\max}(3) = 3$ (witness $x^3 - x$). [D: constructions in hand; the
   census must confirm no better exists.]
3. $z_{\max}(4) \in \{3, 4\}$: we know no length-4 construction with 4
   distinct integer roots; the census decides.

## One-sidedness (what a PASS proves, what a FAIL proves)

- For each completed depth, the census is DECISION-COMPLETE: it proves the
  exact value of $z_{\max}(\tau)$ (both the record and its unbeatability).
  This is a theorem about the bottom of the ladder.
- It proves NOTHING about the conjecture asymptotically, in either
  direction. Growth data at $\tau \le 4$ cannot distinguish polynomial from
  superpolynomial growth. The census's value is structural (mechanisms) and
  foundational (trusted tooling for the frontier pushes).
- A Stage A mismatch refutes OUR TOOLING (or, far less likely, Markstroem's
  table): it does not bear on the conjecture.

## Premise dependencies (methodology 12, P3)

- Markstroem's Figure 1 values: [V] read directly in arXiv:1306.3091v4.
- Model equivalence to the survey definition: lemmas 1-2 above, [D],
  self-contained.
- No other external premise is load-bearing.

## Invariant-first note (P5)

Considered cheap deciders: the degree cap ($z \le \deg \le 2^\tau$) gives
$z_{\max}(\tau) \le 2^\tau$, far above the observed candidates, so it
decides nothing at these depths; no divisibility/height invariant known to
us decides $z_{\max}(4)$ without search. Enumeration is therefore justified
at this scale.

## Compute budget and kill criterion (P6)

- Smoke test first (P2): depth-2 run must print progress lines and write
  the checkpoint file within seconds.
- Budget: 30 minutes wall total on the local machine (repo venv, CPU only).
- Kill criterion: if Stage B depth 4 is not complete at 20 minutes, save
  the checkpoint, report depths $\le 3$ as decided and depth 4 as
  INCONCLUSIVE (partial), and stop. If the budget is hit, we conclude that
  depth-4 exhaustion needs the TCB-005 canonicalization work, and the
  verdict says so.
- Expected runtime: seconds for Stage A to depth 6; depth 7 possibly
  minutes; Stage B minutes at depth 4 (state count estimated $10^5$-$10^6$).

## Success and failure criteria

- CONFIRMED: Stage A passes AND Stage B completes depth 4, yielding exact
  $z_{\max}(\tau \le 4)$ with verified witnesses.
- PARTIAL/INCONCLUSIVE: Stage A passes, Stage B stops at the kill
  criterion with depth 4 incomplete.
- REFUTED (of the tooling): Stage A mismatch.
