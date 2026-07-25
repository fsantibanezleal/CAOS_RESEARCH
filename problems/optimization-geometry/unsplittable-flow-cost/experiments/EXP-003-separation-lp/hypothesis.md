# EXP-003: the separation LP, and the first minimality rungs

Declared 2026-07-24, BEFORE the run and before any of its code was written
(methodology/02). Phase UF-P2. Backlog UFB-010, and it also takes up UFB-025, whose claim
as recorded in the RESUME was too strong (see G6).

## Question

Can we decide, exactly, whether a given instance $(G, s, T, d, x)$ admits ANY nonnegative
cost vector making it a counterexample, without searching over cost vectors; and what do
the first rungs of the minimality ladder look like once we can?

## Motivation

Every later rung needs the cost vector out of the search space. An exhaustive hunt over
(digraph, demands, fractional flow, cost vector) is hopeless; over
(digraph, demands, fractional flow) with one exact LP per instance it is finite and
honest. The reduction was sketched in the proposer's transcript and is recorded as
[CLAIMED] in the counterexample dossier section 5; this experiment re-derives it in our own
words and implements it exactly, which is the condition for using it at all.

## The derivation (ours, to be committed before the run)

Fix $(G, s, T, d, x)$ and let $\mathcal{U}(x)$ be the set of load vectors of
congestion-good unsplittable routings. It is finite, and nonempty by the
Dinitz-Garg-Goemans theorem. Note that $\mathcal{U}(x)$ does NOT depend on $c$: that is the
whole reason the reduction works.

The instance admits a counterexample cost vector exactly when there is $c \ge 0$, $c \ne 0$,
with $c^T y > c^T x$ for every $y \in \mathcal{U}(x)$. The condition is invariant under
scaling $c$ by a positive number, so we may normalise $\sum_a c_a = 1$ and consider

$$\mathrm{(SEP)} \qquad \max\ \delta \quad \text{s.t.} \quad c^T(y - x) \ge \delta \ \ \forall y \in \mathcal{U}(x), \qquad \sum_a c_a = 1, \qquad c \ge 0 .$$

Claim: the instance admits a counterexample cost vector if and only if the optimum of (SEP)
is strictly positive.

If the optimum is $\delta^\* > 0$ with witness $c$, then every congestion-good routing has
$c^T y \ge c^T x + \delta^\* > c^T x$, and $c \ge 0$, so $(G, s, T, d, x, c)$ is a
counterexample. Conversely, if some $c \ge 0$, $c \ne 0$ witnesses a counterexample, then
$\min_{y \in \mathcal{U}(x)} c^T (y - x) > 0$ because the minimum is over a finite nonempty
set; rescaling $c$ by $1/\sum_a c_a > 0$ preserves that strict inequality and gives a
feasible point of (SEP) with positive objective. (SEP) is feasible (any normalised $c \ge 0$
gives some, possibly negative, $\delta$) and bounded (the objective is at most
$\max_{y} \max_a |y_a - x_a|$).

## Falsifiable predictions

- **G1 (the instrument works).** (SEP) is feasible and bounded on every instance below, and
  is solved in EXACT rational arithmetic (sympy's rational simplex; no floats), returning a
  rational optimum and a rational witness $c$.
- **G2 (the 2026 instance).** The optimum is strictly positive. Moreover it is at least
  $2/7$, since the published cost vector $(2, 3, 0, 2, 0, 0, 0, 0, 0)$ has coordinate sum 7
  and gives $\min_y c^T(y - x) = 60 - 58 = 2$, hence $\delta = 2/7$ after normalisation. The
  exact optimum is NOT predicted (a better cost vector may exist) and is reported by the
  machine.
- **G3 (the validation set).** On V1-V5 from EXP-001, the optimum is at most 0: no
  nonnegative cost vector can turn any of them into a counterexample. This is a strictly
  stronger statement than what EXP-001 checked, which was only that the ONE given cost
  vector admits a good routing.
- **G4 (round trip).** Feeding the LP's witness $c$ from G2 back into `ufclib` reproduces the
  counterexample verdict: no routing both congestion-good and cost-good. The two instruments
  must agree.
- **G5 (minimality rung 1, $k = 1$).** With a single terminal, EVERY routing is
  congestion-good, because $y_a = d_1 \le x_a + d_1 = x_a + d_{\max}$ on the chosen path and
  $y_a = 0$ elsewhere; and routing on a cheapest $s$-$t_1$ path is cost-good, because $x$
  decomposes into $s$-$t_1$ paths of total weight $d_1$, each of cost at least the cheapest,
  so $c^T x \ge d_1 \cdot (\text{cheapest path cost})$. Hence NO single-terminal instance is
  a counterexample, for any cost vector. Prediction: (SEP) returns optimum at most 0 on
  every single-terminal instance tested, including ones built to look adversarial.
- **G6 (CORRECTION of an overreach, $k = 2$).** The RESUME recorded, as a derivation, that
  no counterexample exists with at most two terminals, via "a conflict graph on at most two
  nodes has no odd cycle". That argument is NOT valid as stated: a terminal may have many
  path choices, so the conflict graph is not a two-node graph, and the step from an integral
  stable-set polytope to the absence of a separating nonnegative cost vector was asserted
  rather than proved. What IS provable at $k = 2$, and is declared here as the replacement
  prediction: routing both terminals on their cheapest paths is always cost-good, and it is
  congestion-good if and only if every arc lying on BOTH cheapest paths carries
  $x_a \ge \min(d_1, d_2)$. Consequently any two-terminal counterexample must have a shared
  arc on the two cheapest paths with $x_a < \min(d_1, d_2)$. Prediction: this
  characterisation holds on every two-terminal instance tested, and a targeted family of
  two-terminal instances built to violate that necessary condition (shared bottleneck, two
  choices per terminal, parameters swept over a bounded integer box) yields NO counterexample
  under (SEP).
- **G7 (honest scope).** G6's family sweep is EVIDENCE, not a proof: the verdict must say so
  explicitly and must not upgrade "none found in a bounded box" into "none exists".

## Method

`run.py` builds (SEP) from `ufclib`'s enumeration of congestion-good routings, solves it
with `sympy.solvers.simplex.linprog` over the rationals, and asserts G1-G7. The two-terminal
family is generated deterministically over an integer parameter box; no randomness anywhere.

## Success and failure criteria

- **Confirmed** if G1-G6 hold and G7 is honoured in the verdict's language.
- **Refuted** if the LP disagrees with `ufclib` anywhere (G4), or if a two-terminal
  counterexample IS found, which would be a genuinely new result and would immediately
  become its own experiment with the full validation ladder before any claim.
- **Instructive** if the $k = 2$ characterisation in G6 is wrong: the corrected statement,
  and what the error teaches, go in the verdict.
