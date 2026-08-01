# EXP-005: the parameterized-tower loophole for $h_c = x^2 - c$: empty or real?

Declared 2026-08-01 (round 5), before the run. Actions RL-9 (view V8,
arithmetic-dynamics context note): the monic stall theorem bounds each
SINGLE map's tower yield by a map-dependent constant $Z(h)$; a refuter
could try to grow $Z(h_c)$ with $c$ faster than the cost $\tau(c)$ of
building $c$. This experiment measures the actual yields exactly across
the family.

## Questions

For $h_c = x^2 - c$, $1 \le c \le 200$, and tower levels
$B^2 - A^2$ with $B = h_c^{\circ i}$, $A = h_c^{\circ j}$,
$0 \le i < j \le 4$ (the DOS shapes; $h^{\circ 0} = x$), plus the
fixed-point shapes $h_c^{\circ k}(x) - x$, $k \le 4$:

1. The exact maximum integer-root yield $Z_{\text{meas}}(c)$ over these
   shapes, per $c$.
2. The yield-per-gate ratio against the exact $\tau(c)$ (computed by the
   anchored integer BFS to depth 7, which covers all $c \le 200$) plus
   the tower gate cost $2j + 3 + \tau(c)$-type ledger.
3. Whether any $(c, \text{shape})$ beats the geometric-progression
   linear-rate benchmark or even the single-map record.

## Committed derivation and predictions ([D], written before the run)

The discriminant computation: $h_c(y) = \pm y$ both have discriminant
$1 + 4c$, so integer fixed/anti-fixed points exist iff $1 + 4c$ is an
odd square, i.e. $c = m(m+1)$: then $A$-set $= \{m+1, -m\}$ (fixed),
$\{m, -m-1\}$ (anti-fixed). Preimages: $h_c^{-1}(m+1) = \{\pm(m+1)\}$
(since $c + m + 1 = (m+1)^2$), $h_c^{-1}(-m) = \{\pm m\}$ (since
$c - m = m^2$), while $h_c^{-1}(m)$ needs $m(m+2)$ square (only $m=0$)
and $h_c^{-1}(-m-1)$ needs $m^2 - 1$ square (only $m = 1$, giving 0).
Hence the stable core is $\{\pm m, \pm(m+1)\}$ for $m \ge 2$ (size 4),
and $\{0, \pm 1, \pm 2\}$ exactly for $m = 1$ ($c = 2$, the Chebyshev
case, size 5).

PREDICTIONS:
1. $Z_{\text{meas}}(c) = 0$ for every $c$ NOT of the form $m(m+1)$ (no
   integer fixed/anti-fixed points, and DOS-shape roots require
   $h^{\circ(j-1)}$-values landing in those sets; for the general
   $i < j$ shapes, roots require $h^{\circ i}(x)$ to be a signed
   $(j-i)$-periodic point, and we predict no NEW integer signed-periodic
   points beyond the $r = 1$ sets in this range: to be checked by the
   run, this is the falsifiable part).
2. $Z_{\text{meas}}(c) = 4$ for $c = m(m+1)$, $m \ge 2$; $= 5$ only at
   $c = 2$; $\le 2$ at $c = 0$-degenerate cases excluded ($c \ge 1$).
3. Consequently the family loophole is EMPTY: $\sup_c$ yield $= 5$,
   attained at the single map $c = 2$ already covered by the census;
   yield-per-gate is maximized at $c = 2$ and DECREASES in $c$ (cost
   $\tau(c)$ grows, yield does not).

## One-sidedness

The run decides the predictions exactly on the measured range
($c \le 200$, shapes $j \le 4$). A violation (an unexpected signed-
periodic integer point creating yield $> 5$, or nonzero yield off the
$m(m+1)$ sequence) would be a DISCOVERY contradicting our derivation
(then the derivation is re-audited first). Confirmation on the range
plus the derivation's general argument upgrades the family stall to a
stated lemma for all $c$ (the derivation covers all $c$ for the $r = 1$
shapes; the $r \ge 2$ shapes are proved only by the measured range plus
the core-boundedness argument, and the lemma will say so honestly).

## Premise dependencies (P3)

- Monic stall theorem (this round, [D]) for the core-boundedness frame.
- tclib exact arithmetic (anchored EXP-001..003; suite 8 tests green).
- Exact $\tau(c)$ for $c \le 200$: integer BFS to depth 7 anchored to
  Markstroem 14/14 (EXP-001).

## Invariant-first note (P5)

The discriminant $1 + 4c$ IS the invariant that decides fixed-point
existence in one line: the run's role is only to check the $r \ge 2$
shapes and tabulate exact yields/costs. This is invariant-first working
as intended: the heavy part was decided on paper.

## Compute budget and kill criterion (P6)

- Pure tclib tuple arithmetic; degrees $\le 2^5 = 32$; $c \le 200$,
  shapes $\le 15$ per $c$: ~3000 polynomials plus one depth-7 integer
  BFS. Expected: under 2 minutes total. Budget: 10 minutes; kill:
  abort and report partial if exceeded (would indicate a tooling bug).
- Smoke: $c = 2$ must reproduce the Chebyshev note values (roots
  $\{\pm1,\pm2\}$ at $G_1$, $\{0,\pm1,\pm2\}$ at $G_2$).

## Success and failure criteria

- CONFIRMED: predictions 1-3 hold on the full measured range.
- REFUTED: any counterexample row (recorded in full; derivation
  re-audit becomes the next action).
- INCONCLUSIVE: budget kill (tooling investigation).
