# EXP-004 verdict: the frontier value, and a null result with teeth

Run 2026-07-25 with the repo `.venv` (Python 3.13.0), CPU only, exact rational arithmetic,
no floats, no randomness, no network. Total sweep time about 160 s.
Artifacts: `artifacts/run-log.txt`. Reproduce from the repository root:

```
.venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-004-frontier-value/run.py
```

## Verdict: CONFIRMED in its instrument predictions, with F4 REFUTED as a null result

F1, F2, F3, F5 and F6 hold. **F4 is refuted**, which the hypothesis explicitly allowed and
named as the likely outcome: no member of the swept family forces more violation than the
published instance. The null result is sharper than expected and is the main finding.

## The frontier instrument

For a fixed $(G, d, x)$ the FRONTIER VALUE is
$\alpha_{\max} = \max_{c \ge 0} \min\{\alpha(y) : c^{\mathsf T} y \le c^{\mathsf T} x\}$: the
largest violation, in units of $d_{\max}$, that any pricing of the arcs can force on a
cost-preserving rounding. Computed exactly as the largest threshold $A$ for which the
separation LP restricted to $\{y : \alpha(y) < A\}$ has positive optimum. An instance is a
counterexample to Goemans' conjecture exactly when $\alpha_{\max} > 1$, so EXP-003's
separation LP is the special case of this at the threshold just above 1.

**F2**: on V1-V5, $\alpha_{\max} \in \{0, 1/2\}$, all at most 1, consistent with EXP-003.

**F3, the 2026 instance**: $\alpha_{\max} = 16/15$ exactly, witnessed by the same normalised
cost vector $\tfrac17(2, 3, 0, 2, 0, 0, 0, 0, 0)$ that EXP-003 found optimal for the cost gap.
The routing budgets are $\{1/3, 2/5, 2/3, 2/3, 16/15, 16/15, 16/15, 26/15\}$ and the ceiling
(the budget of the all-free routing, which is always cost-good) is $26/15$.

So the published cost vector is optimal in BOTH senses: it maximises the cost gap (EXP-003)
and it maximises the violation forced (here). The larger value $26/15$ carried by the
all-free routing is NOT attainable by any pricing, because no nonnegative cost vector can
make all seven cheaper-budget routings simultaneously more expensive than $x$. [MV]

## F4: the null result, and why it is interesting

The spine family, which contains the 2026 counterexample as one parameter point (F1,
verified arc for arc under the explicit spine relabelling $v_1, v_2, v_3 \to u, v, w$),
was swept over a bounded integer box:

| Sweep | Structures | Demand sets | Split fractions | Points | Counterexamples |
|---|---|---|---|---|---|
| $k = 3$, $m = 3$ | 10 | 10 | 6 per terminal | 2448 | **1** |
| $k = 4$, $m = 4$ | 4 | 4 | 5 per terminal | 1008 | **0** |

The single counterexample found in 3456 parameter points is the 2026 instance itself, at
exactly its published parameters: $d = (15, 10, 15)$, $e = (2, 3, 3)$, $f = (0, 0, 1)$,
$\rho = (1/3, 2/5, 1/3)$. Nothing else in the box breaks the conjecture at all, and nothing
beats $16/15$. [MV]

Read carefully, that is a stronger statement than "we failed to improve the bound". Within
the natural family that contains it and over this box, the counterexample is **isolated and
extremal**: about one parameter point in 2448 at $k = 3$, and none at all at $k = 4$ in the
structures tried. The mechanism is simple to state, but its parameter window is extremely
narrow, which is a plausible part of why the conjecture stood for a quarter century while
the field proved it in class after class. [D, from the sweep]

It also sets a boundary on cheap optimism: pushing $\alpha^\star$ meaningfully above 1 will
not come from tuning this family's parameters. It needs a different conflict structure
(longer odd cycles, or conflicts mediated by more than one terminal), which is UFB-020 and
UFB-021 and is now the evidenced next step rather than a guess.

## The mid-experiment tooling failure, and what was done about it

Recorded in full because the LP layer now carries verdicts.

The sweep's first attempt CRASHED: sympy's rational simplex raised "Oscillating system led
to invalid solution" on a degenerate family member. That is exactly the single-point-of-
failure risk EXP-003's verdict flagged as UFB-033 ("sympy's rational simplex is currently a
single point of failure"), and it materialised one round later.

Response: we wrote our own exact simplex with **Bland's rule** (`ufclib/simplex.py`), which
cannot cycle, and moved the frontier instrument onto it. Then, as validation added AFTER
the hypothesis was committed and labelled as such in the code and here (check X1), the two
independent implementations were cross-checked on the six instances where sympy succeeds:
the 2026 instance ($2/7$ from both) and V1-V5 ($0$ from both). They agree exactly.

This closes UFB-033: the frontier and separation numbers now rest on two independent LP
implementations rather than one, and the primary one is anti-cycling by construction.

## Adversarial validation

- **Cross-implementation agreement** on all six decidable cases (X1), between a
  tableau simplex we wrote and sympy's, sharing no code.
- **The instrument reproduces EXP-002 and EXP-003** on the 2026 instance: same
  counterexample verdict, same witness, same $16/15$, same $2/7$ separation optimum.
- **Negative controls**: V1-V5 return $\alpha_{\max} \le 1$, so the instrument does not
  manufacture counterexamples.
- **The ceiling check (F5)**: every reported $\alpha_{\max}$ is at most the budget of the
  all-cheapest routing, which is a theorem from EXP-003, so a violation would indicate a bug.
- **A specification error caught and recorded**: F1's first run failed because the comparison
  was vertex-name sensitive (family spine $v_1, v_2, v_3$ versus published $u, v, w$). The
  family reproduced the instance exactly; only the check was wrong. It was fixed by passing
  an EXPLICIT relabelling rather than by loosening the comparison, so the test still
  distinguishes a genuinely different graph.

## How could this be wrong?

1. **The null result is about one family and one box.** The spine family has a single linear
   spine with one free and one expensive choice per terminal. Conflict structures that are
   not realisable on a linear spine (a genuine odd cycle of length 5, or conflicts requiring
   two mediating terminals) are entirely outside the sweep. F4's refutation says nothing
   about them, and the verdict does not pretend otherwise.
2. **The box is coarse in the split fractions.** Six values of $\rho$ per terminal at $k = 3$.
   A counterexample needing $\rho = 7/17$ would be invisible. The sweep is exact per point,
   not exhaustive over the continuum, and a finer or LP-driven parameter search (choosing
   $\rho$ to maximise the forced violation rather than sampling it) is the obvious upgrade,
   now UFB-036.
3. **`ufclib/simplex.py` is new code carrying verdicts.** It is validated against sympy on
   six cases and against textbook LPs in its smoke test, and Bland's rule guarantees
   termination, but it has not been fuzzed against a third implementation.
4. **$\alpha_{\max}$ is defined per instance, not per family.** Nothing here bounds
   $\alpha^\star$ from above; the only upper bound in the literature remains 2 for planar
   graphs, and none is known in general.

## Consequences for the strategy

- UFB-030 is DONE for this family: its maximum frontier value over the box is $16/15$,
  attained only by the published instance.
- UFB-033 is DONE: the independent exact LP route exists and both implementations agree.
- UFB-035 is partially answered: the distribution of frontier values in the family is
  degenerate, with one point above 1 and every other point at or below it.
- New rows: UFB-036 (optimise $\rho$ by LP instead of sampling it), UFB-037 (conflict
  structures not realisable on a linear spine, which is the only route left to a larger
  forced violation inside this programme).
- The evidenced next step for UF-P3 is no longer parameter tuning; it is a new structure.
