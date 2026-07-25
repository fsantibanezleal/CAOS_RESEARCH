# EXP-004: the frontier value of an instance, and a search for a larger forced violation

Declared 2026-07-25, BEFORE the run and before any of its code was written
(methodology/02). Phase UF-P3. Backlog UFB-030, UFB-020, UFB-035.

## Question

The 2026 counterexample forces a violation of $16/15\,\dmax$ UNDER ITS PUBLISHED COST
VECTOR. Two questions follow, and neither is answered by the refutation:

1. For a fixed graph, demands and fractional flow $(G, d, x)$, what is the LARGEST violation
   any nonnegative cost vector can force? Call it the instance's FRONTIER VALUE
   $\alpha_{\max}(G, d, x)$.
2. Over a family of structurally similar instances, how large can the frontier value get?
   Every unit above 1 is a lower bound on the global constant $\alpha^\star$, whose only
   known upper bound is 2, for planar graphs (TVZ24), with nothing known in general.

## The instrument (derived here, before implementation)

Fix $(G, d, x)$. Each unsplittable routing $y$ has an exact
$\alpha(y) = \max_a (y_a - x_a)^+/\dmax$, the budget it consumes. For a cost vector $c$,
$\alpha_{\mathrm{inst}}(c) = \min\{\alpha(y) : c^{\mathsf T} y \le c^{\mathsf T} x\}$, and we
want $\alpha_{\max} = \max_{c \ge 0} \alpha_{\mathrm{inst}}(c)$.

The set of achievable values is finite (there are finitely many routings), so for a
candidate threshold $A$ let $S_A = \{y : \alpha(y) < A\}$. Then some $c \ge 0$ forces
$\alpha_{\mathrm{inst}}(c) \ge A$ if and only if some $c \ge 0$ makes every $y \in S_A$
strictly more expensive than $x$, which is exactly the separation LP of EXP-003 with its
constraint set restricted to $S_A$:

$$\max\ \delta \ \ \text{s.t.}\ \ c^{\mathsf T}(y - x) \ge \delta \ \forall y \in S_A,
\quad \textstyle\sum_a c_a = 1, \quad c \ge 0 ,$$

feasible with $\delta > 0$. So $\alpha_{\max}$ is the largest candidate $A$ whose LP has
positive optimum (with $S_A = \emptyset$ counted as feasible, since then no routing at all
sits below $A$). This makes EXP-003's separation LP the special case $A = \min\{\alpha(y) :
\alpha(y) > 1\}$: an instance is a counterexample exactly when $\alpha_{\max} > 1$.

Note the ceiling: routing every terminal on a cheapest path is always cost-good (EXP-003),
so $\alpha_{\max} \le \alpha(\text{all-cheapest routing})$ always.

## The family (the 2026 instance is a member, verified as prediction F1)

Spine $s = v_0 \to v_1 \to \cdots \to v_m$ with zero costs. Terminal $i$ has demand $d_i$, a
free choice leaving the spine at $v_{e_i}$ (arc $v_{e_i} \to t_i$, cost 0) carrying a
fraction $\rho_i$ of its demand, and an expensive choice leaving at $v_{f_i}$ with
$f_i < e_i$ (arc $v_{f_i} \to t_i$, cost $c_i > 0$) carrying $1 - \rho_i$. Spine arc $r$
carries $\sum_{i : e_i \ge r} \rho_i d_i + \sum_{i : f_i \ge r} (1 - \rho_i) d_i$.

The 2026 counterexample is exactly this family at $m = 3$, $k = 3$, demands $(15, 10, 15)$,
$e = (2, 3, 3)$, $f = (0, 0, 1)$, $\rho = (1/3, 2/5, 1/3)$, expensive costs $(2, 3, 2)$.
The mediated third conflict (choices 1 and 2 clash on the first spine arc because terminal 3
traverses it whichever path it takes) is the $f_3 = 1$ parameter.

## Falsifiable predictions

- **F1 (the family contains the counterexample).** Instantiating the family at the
  parameters above reproduces the 2026 instance arc for arc, and our checker returns the
  same verdict, $c^{\mathsf T}x = 58$ and $\alpha_{\mathrm{inst}} = 16/15$.
- **F2 (the instrument is sound on known cases).** On the EXP-001 validation instances
  V1-V5, $\alpha_{\max} \le 1$: no cost vector forces a violation beyond $\dmax$, consistent
  with EXP-003 finding their separation optimum at most 0.
- **F3 (the 2026 instance's frontier value).** $\alpha_{\max} = 16/15$ for the 2026 instance.
  That is, the published cost vector is optimal not only for the cost gap (EXP-003) but also
  for the violation it forces, and the larger value $26/15$ carried by the all-free routing
  is NOT attainable by any cost vector. Confidence: moderate. A refutation here (i.e.
  $\alpha_{\max} = 26/15$) would be a strictly better lower bound on $\alpha^\star$ from the
  same instance and would be more interesting than the prediction holding.
- **F4 (the sweep finds something better).** Over a bounded integer parameter box of the
  family with $k \le 4$ terminals and spine length $m \le 4$, at least one instance has
  frontier value strictly greater than $16/15$. Confidence: low to moderate. This is the
  prediction the experiment exists to test, and it is the one most likely to fail.
- **F5 (the ceiling).** Every instance in the sweep satisfies
  $\alpha_{\max} \le \alpha(\text{all-cheapest routing})$, and no instance in the sweep
  reaches $\alpha_{\max} \ge 2$, which would contradict the planar theorem for any planar
  member of the family.
- **F6 (honest scope, pre-committed).** Whatever the maximum found, the verdict states it as
  a lower bound on $\alpha^\star$ obtained over a bounded box of ONE structural family, never
  as an estimate of $\alpha^\star$, and never as evidence about the $O(\dmax)$ question.

## Method

Implement `ufclib.frontier.frontier_value` per the derivation above (exact rationals,
sympy rational simplex, reusing the EXP-003 LP builder). Generate the family
deterministically over an integer box; decide each instance with the separation LP as a
filter, then compute the frontier value of those that are counterexamples. No randomness.

## Success and failure criteria

- **Confirmed** if F1, F2, F3, F5 hold and F4 is decided either way with its outcome stated
  plainly.
- **Refuted** if the instrument disagrees with EXP-002 or EXP-003 anywhere (F1, F2), which
  would invalidate the frontier numbers.
- A failure of F4 (no family member beats $16/15$) is a legitimate NULL result and is
  reported as such: it would say the published instance is already extremal in this family,
  which is itself worth recording.
