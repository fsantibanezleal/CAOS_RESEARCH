# EXP-003 verdict: the separation LP, and the first minimality rungs

Run 2026-07-24 with the repo `.venv` (Python 3.13.0, sympy 1.14.0), CPU only, exact
rational arithmetic throughout (sympy's rational simplex), no floats, no randomness, no
network. Artifacts: `artifacts/run-log.txt`. Reproduce from the repository root:

```
.venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-003-separation-lp/run.py
.venv/Scripts/python.exe -m pytest problems/optimization-geometry/unsplittable-flow-cost/code/ufclib/tests/ -q
```

## Verdict: CONFIRMED

All seven predictions G1-G7 hold. The separation LP is adopted as the programme's second
instrument, and two minimality results land: one theorem at $k = 1$ and a sharp necessary
condition plus a bounded sweep at $k = 2$.

## G2, G4: the 2026 instance, and a fact that was not predicted

$(\mathrm{SEP})$ optimum on the 2026 counterexample: **exactly $2/7$**, with witness

$$c = \left(\tfrac{2}{7}, \tfrac{3}{7}, 0, \tfrac{2}{7}, 0, 0, 0, 0, 0\right),$$

which is exactly the published cost vector $(2, 3, 0, 2, 0, 0, 0, 0, 0)$ divided by its
coordinate sum 7. The prediction was only that the optimum is at least $2/7$; the machine
returned equality. [MV]

**Consequence, stated carefully.** The optimum of $(\mathrm{SEP})$ is the largest
normalised cost gap any nonnegative cost vector can force on this
$(G, s, T, d, x)$. Since it is attained by the published vector, that cost vector is
OPTIMAL for this graph and this fractional flow: no reweighting of the arcs separates the
fractional flow from the congestion-good routings by more. The announced 58-versus-60 gap
is therefore not one lucky choice of prices among many; it is the best this instance can
do. [MV for the optimum and the witness; [D] for the reading]

The round trip (G4) closes the loop: under the witness costs, `ufclib` independently reports
$c^T x = 58/7$, minimum congestion-good cost $60/7$, and a counterexample verdict, with the
gap $2/7$ matching the LP optimum exactly. The LP and the enumerator agree.

## G3: the validation set

On V1-V5 the optimum is exactly 0 in every case, so no nonnegative cost vector turns any of
them into a counterexample. [MV] This is strictly stronger than what EXP-001 established,
which concerned only the one cost vector each instance carried.

The optima are 0 rather than negative, which is worth recording: on these instances one can
always choose prices so that the best congestion-good routing exactly TIES the fractional
cost, but never beats it by a positive margin. The conjecture holds on them with no slack to
spare, which is a reminder that "obeys the conjecture" and "obeys it comfortably" are
different properties. A future frontier experiment should look at the DISTRIBUTION of
$(\mathrm{SEP})$ optima, not just its sign.

## G5: minimality rung 1, a theorem at $k = 1$

**Claim [D, machine-checked on a family].** No single-terminal instance is a counterexample,
for any nonnegative cost vector.

Proof. Let $T = \{t\}$ with demand $d$, so $d_{\max} = d$. (i) EVERY routing is
congestion-good: the routing puts load $d$ on the arcs of its chosen path and 0 elsewhere,
and $d \le x_a + d$ holds for every arc because $x_a \ge 0$. (ii) Routing on a cheapest
$s$-$t$ path is cost-good: $x$ is a flow of value $d$ from $s$ to $t$, so it decomposes into
$s$-$t$ paths carrying weights summing to $d$ (plus possibly circulations, which have
nonnegative cost and can only increase $c^T x$); each path costs at least the cheapest path
cost $\gamma$, so $c^T x \ge d \gamma$, which is the cost of the chosen routing. Hence the
cheapest-path routing is both congestion-good and cost-good. $\square$

Machine check: on six single-terminal instances built to look adversarial (bottlenecks,
zero-flow arcs, a long cheap detour against a short expensive arc, demands 1, 3, 7), every
routing was congestion-good and $(\mathrm{SEP})$ returned optimum $\le 0$ in each. [MV]

## G6: the CORRECTION, and what is actually true at $k = 2$

**What was wrong.** The RESUME after round 1 recorded, as a derivation, that no
counterexample exists with at most two terminals, on the grounds that "a conflict graph on
at most two nodes has no odd cycle". That argument does not survive contact with the
definitions. A terminal may have many path choices, so the conflict graph is not a two-node
graph; and even when it is, the step from an integral stable-set polytope to the absence of
a separating nonnegative cost vector was asserted, not proved. The claim was declared
suspect in this experiment's hypothesis BEFORE the run, and it is withdrawn here. Only the
$k = 1$ case above is a theorem.

**What replaces it [D, machine-checked on 184 instances].** At $k = 2$:

1. The all-cheapest routing (each terminal on a cheapest path) is ALWAYS cost-good. This
   holds for every $k$, by the same per-terminal decomposition argument as in G5 applied to
   the decomposition $x = \sum_i x^i$ into per-terminal flows.
2. The all-cheapest routing is congestion-good IF AND ONLY IF every arc lying on BOTH
   cheapest paths carries $x_a \ge \min(d_1, d_2)$. (On an arc used by one path the load is
   at most $d_{\max} \le x_a + d_{\max}$; on a shared arc the load is $d_1 + d_2$, and
   $d_1 + d_2 \le x_a + \max(d_1, d_2)$ is exactly $x_a \ge \min(d_1, d_2)$.)
3. Therefore any two-terminal counterexample MUST contain an arc on both cheapest paths with
   $x_a < \min(d_1, d_2)$. That is a sharp necessary condition, and it tells a future
   exhaustion exactly where to look.

The characterisation held on all 184 instances of the swept family, and the all-cheapest
routing was cost-good on all of them. [MV]

**The sweep.** 184 two-terminal instances with a shared spine and two choices per terminal,
sweeping demands $(2,3), (3,5), (4,5), (5,7)$, every integer split of each demand between
its two choices, and four cost pairs. None admits ANY nonnegative cost vector making it a
counterexample. [MV]

## G7: honest scope, pre-committed and honoured

The $k = 2$ result is EVIDENCE over a bounded parameter box, not a proof. The family is one
shape (a single shared spine arc); it does not cover two-terminal instances with several
shared arcs, longer detours, parallel arcs, or non-integer splits. "None found in this box"
is not "none exists", and this verdict does not claim otherwise. The open question stands:
is there a two-terminal counterexample at all? The necessary condition in G6.3 is the handle.

## Adversarial validation

- **Cross-instrument agreement (rung 3).** The LP and the enumerator are independent code
  paths, one polyhedral and one combinatorial, and they agree on the 2026 instance both in
  verdict and in the exact value of the gap ($2/7$). Neither shares the other's arithmetic.
- **The derivation was committed before the run** (hypothesis, both directions of the
  equivalence), so the reduction imported from the proposer's transcript is now ours and is
  no longer [CLAIMED]. The transcript's version is superseded by our own statement and proof.
- **A negative control set** (V1-V5, six single-terminal instances, 184 two-terminal
  instances) exercises the LP on cases that must NOT be counterexamples; an instrument that
  only ever says yes would be useless.
- **The failed claim was retracted in writing** rather than quietly dropped, per
  methodology/03.

## How could this be wrong?

1. **The LP layer is exact but not independently re-implemented.** sympy's rational simplex
   is a single implementation; a bug there would corrupt every optimum. Mitigations in place:
   the round trip through `ufclib` (G4) checks the optimum against an independent
   combinatorial computation on the one instance that matters, and G3/G5/G6 check the sign on
   192 instances where the answer is known by argument. A second exact LP route (a
   Fraction-based simplex of our own, or a dual certificate check) is queued as UFB-033.
2. **$(\mathrm{SEP})$ requires enumerating all congestion-good routings**, which is
   exponential in the number of terminals. It is fine at these sizes and will NOT be fine for
   the full minimality exhaustion; the canonical-form work (UFB-011) must be paired with a
   smarter constraint generation, or the exhaustion will stall.
3. **The optimality reading in G2 is about this $(G, s, T, d, x)$ only.** It says the
   published cost vector is the best separator for THAT graph and flow. It says nothing about
   whether another graph or flow of the same size does better, which is exactly what UF-P3
   asks.
4. **The $k = 2$ family is one shape.** See G7.

## Consequences for the strategy

- UFB-010 is DONE: the separation LP exists, is exact, is validated, and is in the library
  with tests.
- UFB-025 is CORRECTED and partially done: $k = 1$ is a theorem; $k = 2$ has a necessary
  condition and a bounded sweep, and remains open.
- New rows: UFB-033 (an independent exact LP route or dual certificate), UFB-034 (constraint
  generation so the LP scales past tiny instances), UFB-035 (the distribution of
  $(\mathrm{SEP})$ optima, not just the sign, as the natural frontier statistic).
- The next rung, UFB-011 canonical forms, is now the only thing between us and a real
  minimality exhaustion.
