# EXP-005 verdict: CONFIRMED on the load-bearing claim; a 2-cycle series discovered where predicted uncertain

Run 2026-08-01 (round 5), 3.4 s after the root-finder fix (below), repo
venv, exact arithmetic. Raw output: `artifacts/family.json`.

## Tooling incident (recorded)

The first launch hit the large-constant trap our own EXP-003 verdict had
flagged: divisor-based root counting on tower constant terms (~$c^{2^k}$,
up to $10^{18}$) is infeasible; the 10-minute budget killed it. Fix: the
escape lemma (monic stall theorem, Lemma 1, proved independently of this
experiment) bounds every integer root of an $h_c$-tower shape by
$|r| \le c + 1$, so exact root-finding is direct evaluation over that
window. The fixed finder is cross-checked against the divisor method on
all shapes with $j \le 2$, $c \le 10$ (exact agreement asserted in-run).

## Results ($1 \le c \le 200$, shapes: fixed-point $h^{\circ k} - x$ and
DOS $h^{\circ i\,2} - h^{\circ j\,2}$, $i < j \le 4$)

- **Family maximum: 5, attained ONLY at $c = 2$** (the Chebyshev case,
  root set $\{0,\pm1,\pm2\}$). Prediction 3, the load-bearing claim, is
  CONFIRMED on the measured range: the parameterized-family loophole is
  EMPTY here; yield does not grow with $c$ while $\tau(c)$ does (exact
  $\tau(c)$ from the depth-7 anchored integer BFS tabulated per $c$).
- Series 1 (predicted): $c = m(m+1)$, yield 4 via fixed/anti-fixed
  points, roots $\{\pm m, \pm(m+1)\}$: CONFIRMED for all $m \ge 2$ in
  range.
- **Series 2 (DISCOVERED; prediction 1's flagged caveat refuted):
  $c = m^2 + m + 1$ also yields 4**, via genuine integer 2-CYCLES:
  $h_c(m) = -m-1$, $h_c(-m-1) = m$, harvested by the $x^2 - h^{\circ2}(x)^2$
  shape with roots $\{\pm m, \pm(m+1)\}$ (14 such $c$ in range, plus
  $c = 1$ giving $\{-1, 0, 1\}$ from the cycle $0 \leftrightarrow -1$).
  Derivation re-audit: our discriminant analysis covered only
  period-1 signed points; period 2 exists on this second series.

## The classical frame that explains the ceiling [D proof + MV attribution]

For ANY $f \in \mathbb{Z}[x]$ and any cycle $a_0 \to a_1 \to \dots \to
a_r = a_0$ of integers, $a_{i+1} - a_i$ divides $f(a_{i+1}) - f(a_i) =
a_{i+2} - a_{i+1}$ cyclically, so all differences share one absolute
value $d$; summing $\pm d$ around the cycle to zero with $r \le 2$
sign-patterns forces $r \le 2$. (Classical; systematically developed in
Narkiewicz's polynomial-cycles literature [MV: attribution to verify at
read time]. The 5-line proof is [D], self-contained.) Hence over
$\mathbb{Z}$ the ONLY harvestable periodic structure of any polynomial
map is: fixed points, anti-fixed points, and 2-cycles: exactly what the
two series realize. Combined with the stall theorem's preimage-core
finiteness, single-map towers over $x^2 - c$ can never exceed
constant yield, now with the mechanism inventory COMPLETE (period 1,
signed period 1, period 2: nothing else exists to find).

## Prediction scorecard

1. Zero yield off $c = m(m+1)$: REFUTED as stated (the flagged
   falsifiable clause): the 2-cycle series and $c = 1$ are nonzero.
2. Yield 4 on $c = m(m+1)$, $m \ge 2$; 5 only at $c = 2$: CONFIRMED.
3. Family loophole empty (sup yield 5 at $c = 2$; yield-per-gate
   decreasing): CONFIRMED on the range, now EXPLAINED by the cycle-length
   bound.

## How could this be wrong?

The escape-bound window could miss roots if Lemma 1's constant were
wrong for some shape: hedged by the divisor-method cross-check at small
$c$ and by the lemma's 3-line proof; the shape list is finite and
explicit ($k \le 4$): longer towers only shrink root sets (preimage
cores stabilize), argued in the stall theorem, not re-measured here.

## Consequences

- RL-9 resolves for the quadratic family: the loophole is empty, and the
  reason is structural (integer cycle length $\le 2$). The remaining
  open flank for a superlinear factory is MULTI-map products with built
  constants: exactly the census's regime.
- The arithmetic-dynamics view (V8) is upgraded from analogy to working
  tool: the classical cycle bound did in one line what sweeps cannot.
  Next import candidate: uniform preperiodic bounds for non-monic /
  higher-degree families (Doyle-Poonen reading, TCB queue).
- New wiki-04 rows: series 2 mechanism; the cycle-length ceiling.
