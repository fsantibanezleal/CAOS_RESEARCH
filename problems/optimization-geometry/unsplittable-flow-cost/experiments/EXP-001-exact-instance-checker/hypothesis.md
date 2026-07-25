# EXP-001: the exact SSUF instance checker (calibration and toolchain shakedown)

Declared 2026-07-24, BEFORE any code was written or run (methodology/02).
Phase UF-P0. Backlog UFB-001.

## Question

Can we decide, exactly and by our own code, whether a given finite SSUF instance admits an
unsplittable routing that is simultaneously congestion-good and cost-good; and does that
decision procedure return the known answer on instances whose answer is fixed by
inspection?

## Motivation

Everything this programme will ever claim is judged against this checker (plan.md, UF-P0).
It is the ground truth for the adjudication of the 2026 claimed counterexample (EXP-002),
for the minimality exhaustion (UF-P2) and for the frontier measurements (UF-P3). A checker
that is subtly wrong would corrupt every downstream verdict, and the specific way such
checkers are historically wrong in this problem is documented: INCOMPLETE PATH
ENUMERATION (context/2026-07-24-claimed-counterexample-dossier.md, section 6).

## Definitions used (fixed here so the run cannot drift)

Instance $(G, s, T, d, x, c)$ with $G$ a digraph that MAY have parallel arcs, all of
$d, x, c$ exact rationals, $c \ge 0$, $x \ge 0$, and $x$ a feasible fractional flow:
divergence $\sum_{a \in \delta^+(v)} x_a - \sum_{a \in \delta^-(v)} x_a$ equals
$\sum_t d_t$ at $s$, $-d_t$ at each terminal $t$, and $0$ elsewhere. Capacities are $x$
itself (the convention of the entire literature; see the literature dossier section 1).
$d_{\max} = \max_t d_t$.

An unsplittable routing assigns to each terminal $t$ one simple $s$-$t$ path $P^t$ (no
repeated vertex), with load $y_a = \sum_{t: a \in P^t} d_t$. Congestion-good:
$y_a \le x_a + d_{\max}$ for every arc (inclusive inequality). Cost-good:
$c^T y \le c^T x$ (inclusive).

Restriction to SIMPLE paths is without loss of generality for our purposes and the
argument is recorded here rather than assumed: appending a cycle to a walk can only add
load on arcs and, since $c \ge 0$, can only add cost, so a non-simple routing is never
congestion-better nor cost-better than the simple routing obtained by deleting the cycles.
This is a derivation [D], and P7 below turns it into a machine check on a concrete case.

## Falsifiable predictions

Each is a machine assertion in `run.py`; the run exits nonzero on any failure.

- **P1 (enumeration completeness).** On each validation instance, the number of simple
  $s$-$t_i$ paths found by our own depth-first search equals the number obtained by hand,
  which is recorded per instance in the table below BEFORE the run.
- **P2 (routing count).** The number of unsplittable routings equals the product over
  terminals of the per-terminal path counts.
- **P3 (feasibility).** Each validation instance's fractional flow passes the conservation
  and nonnegativity checks; and a deliberately corrupted copy of V1 (one arc's $x$ value
  changed by $+1$) FAILS them. A checker that accepts everything checks nothing.
- **P4 (the DGG floor).** On every validation instance, at least one congestion-good
  routing exists. This is forced by the Dinitz-Garg-Goemans theorem, so a violation means
  either our instance data or our code is wrong, never that the theorem is.
- **P5 (the known answers).** On every validation instance V1-V5 a routing exists that is
  BOTH congestion-good and cost-good, with the specific witnessing routing and the exact
  minimum cost as recorded in the table below.
- **P6 (boundary inclusivity).** On V4, the routing that loads an arc to exactly
  $x_a + d_{\max}$ is classified as congestion-good, i.e. the inequality is inclusive and
  there is no off-by-one at the boundary.
- **P7 (cycles).** On V5, whose digraph contains a directed cycle, the path enumeration
  terminates and returns exactly the same path count as the acyclic V1; and the acyclicity
  test reports False for V5 and True for V1-V4.
- **P8 (exactness).** Every reported quantity is an exact rational; V3 uses fractional flow
  values $1/2$ and the reported costs are exact rationals, never floats. A grep of the
  experiment code for float literals and float-producing operations finds none.

## Method

1. Write `problems/optimization-geometry/unsplittable-flow-cost/code/ufclib/` with the
   instance model (arc-indexed, so parallel arcs are representable), the feasibility check,
   the simple-path enumerator, the routing enumerator, and the exact decision functions
   (congestion-good, cost-good, per-arc violation, $\alpha_{\mathrm{inst}}$).
2. Write the five validation instances from the table below as code, not as data files, so
   they are reviewable next to their expected answers.
3. `run.py` asserts P1-P8 and tees a full report to `artifacts/`.
4. pytest tests in `code/ufclib/tests/` covering the same properties, so CI keeps them.

Arithmetic: `fractions.Fraction` only. No floats anywhere, per methodology/04 and the
problem's standing policy. No dependency on the proposer's verifier, which is archived but
is never imported or executed.

## The validation set, with answers fixed by inspection BEFORE the run

| id | instance | paths per terminal | expected |
|---|---|---|---|
| V1 | one terminal $t$, $d = 2$; arcs $s \to t$ ($x = 1$, $c = 5$), $s \to a$ ($x = 1$, $c = 0$), $a \to t$ ($x = 1$, $c = 0$); $c^T x = 5$ | 2 | 2 routings, both congestion-good ($d_{\max} = 2$, every bound is $x_a + 2 \ge 2$); the detour has cost 0, the direct one 10; a good routing EXISTS, minimum congestion-good cost $= 0$ |
| V2 | one terminal $t$, $d = 2$; TWO PARALLEL arcs $s \to t$ with $x = 1$ each, costs 0 and 7; $c^T x = 7$ | 2 | parallel arcs must produce 2 distinct paths (a checker keyed on (tail, head) would find 1 and is wrong); good routing exists, minimum cost 0 |
| V3 | one terminal $t$, $d = 1$; $s \to a$ ($x = 1/2$, $c = 1$), $a \to t$ ($x = 1/2$), $s \to b$ ($x = 1/2$, $c = 3$), $b \to t$ ($x = 1/2$); $c^T x = 2$ | 2 | congestion never binds ($d_{\max} = 1 > $ every load difference); cheapest routing costs 1, which is $\le 2$; good routing exists; all quantities exact rationals |
| V4 | two terminals $t_1, t_2$, $d = (1, 1)$; $s \to u$ ($x = 2$), $u \to t_1$ ($x = 1$), $u \to t_2$ ($x = 1$), $u \to m$ ($x = 0$), $m \to t_1$ ($x = 0$); all costs 0 | $t_1$: 2, $t_2$: 1 | 2 routings; the one through $m$ loads $u \to m$ to exactly $0 + 1 = x + d_{\max}$, which is congestion-good BY THE INCLUSIVE INEQUALITY; both routings cost 0, so good routings exist |
| V5 | V1 plus a directed cycle on two fresh vertices $p, q$ ($p \to q$, $q \to p$, both $x = 0$, cost 0), and arcs $a \to p$, $q \to t$ ($x = 0$) | 3 | the enumerator must terminate; paths are $s t$, $s a t$, and $s a p q t$; acyclicity reports False; a good routing still exists |

Note on V5: adding the cycle creates a third genuine simple path, so the prediction in P7
is stated as "terminates and the acyclicity test reports False", and the path count is
predicted to be 3 rather than 2. This correction was made while writing the table, before
the run, and is recorded rather than silently applied.

## Success and failure criteria

- **Confirmed** if P1-P8 all hold. The checker is then adopted as the programme's ground
  truth and EXP-002 may use it.
- **Refuted** if any prediction fails and the failure is in the checker: the checker is
  fixed and a NEW experiment (EXP-001b) re-runs the full set, since editing a hypothesis
  after a run is not permitted.
- **Instructive failure** if a prediction fails because the hand-computed expectation in
  the table above was wrong. That is recorded as such in the verdict, with the corrected
  value and what the mistake teaches, and it does NOT count as a checker success unless the
  machine's value is then independently confirmed by hand.
