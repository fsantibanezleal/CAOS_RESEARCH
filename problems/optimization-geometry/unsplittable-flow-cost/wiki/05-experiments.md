# 05 - Experiments

One line per experiment; the folders hold hypothesis, run, artifacts and the long-form
verdict. Verdicts are reported verbatim, never upgraded in language (methodology/06).

| EXP | Question | Verdict | The single load-bearing output |
|---|---|---|---|
| [EXP-001](../experiments/EXP-001-exact-instance-checker/) | Does our own exact checker decide SSUF instances correctly on hand-built cases with known answers? | CONFIRMED (2026-07-24) | `ufclib` adopted as ground truth: predictions P1-P8 hold on V1-V5 (parallel arcs, cyclic digraph, tight boundary, corrupted-flow rejection, exact rationals); 14 pytest regression tests |
| [EXP-002](../experiments/EXP-002-adjudicate-2026-claim/) | Is the 2026 claimed counterexample valid, and what exactly does it force? | CONFIRMED (2026-07-24) | Goemans' Conjecture 1.2 is FALSE: $c^T x = 58$, all 8 routings enumerated, the 4 congestion-good ones cost 90, 60, 60, 60; and $\alpha_{\mathrm{inst}} = 16/15$, so the refutation is by exactly one unit |
| [EXP-003](../experiments/EXP-003-separation-lp/) | Can we decide, without searching over cost vectors, whether an instance admits ANY counterexample cost vector? | CONFIRMED (2026-07-24) | The exact rational separation LP; its optimum on the 2026 instance is $2/7$, attained by the published cost vector normalised, so that vector is an OPTIMAL separator for that graph and flow; plus the $k = 1$ theorem and the corrected $k = 2$ statement |
| [EXP-004](../experiments/EXP-004-frontier-value/) | How much violation can an instance force, maximised over all cost vectors, and can any relative of the 2026 instance force more? | CONFIRMED instruments, F4 REFUTED as a null result (2026-07-25) | The frontier value $\alpha_{\max}$; it equals $16/15$ for the 2026 instance, and over 3456 parameter points of the family containing it the ONLY counterexample is that instance at exactly its published parameters |

## What EXP-002 established beyond the announcement

- $\alpha_{\mathrm{inst}} = 16/15$ exactly (the announcement stated only 58 versus 60).
- The instance is acyclic, so Morell-Skutella Conjecture 1.4 and the convex-combination
  form fall as corollaries, with the hypothesis machine-checked rather than assumed.
- Conjecture 1.3, Conjecture 1.5, the DGG theorem, Skutella's multiples case, the
  series-parallel theorem and the planar theorem were each tested against the instance and
  verified to survive.
- A $K_4$ subdivision on $\{s, u, v, w\}$ places the instance exactly one structure outside
  the class where the conjecture is proved; planarity pins the planar constant strictly
  between 1 and 2.
- An independent structural derivation (conflict triangle, independence number 1) reaches
  the bound 60 without enumerating costs, and agrees with the enumeration.

## What EXP-003 added

- The separation LP removes the cost vector from every future search: one exact rational LP
  per instance decides whether ANY nonnegative cost vector makes it a counterexample.
- On the 2026 instance the optimum is exactly $2/7$ and is attained by the published cost
  vector, so those prices are optimal for that graph and flow: the 58-versus-60 gap is the
  best that instance can produce, not one lucky choice among many. [MV]
- Minimality, rung 1: **no single-terminal instance is a counterexample**, for any cost
  vector. Every routing is congestion-good (the load on the chosen path is $d \le x_a + d$),
  and the cheapest-path routing is cost-good by flow decomposition. [D, machine-checked]
- Minimality, rung 2 (corrected): a claim recorded in round 1, that no counterexample exists
  with at most two terminals, was RETRACTED as invalid. What holds: the all-cheapest routing
  is always cost-good, and at $k = 2$ it is congestion-good exactly when every arc on both
  cheapest paths carries $x_a \ge \min(d_1, d_2)$; so a two-terminal counterexample needs a
  shared arc below that threshold. A 184-instance sweep found none, which is evidence and
  not a proof. [D and MV; the $k = 2$ question is OPEN]

## What EXP-004 added

- **The frontier value** $\alpha_{\max} = \max_{c \ge 0} \min\{\alpha(y) : y \text{ cost-good}\}$,
  the largest violation any pricing can force. An instance is a counterexample exactly when
  $\alpha_{\max} > 1$, so the separation LP is its special case at the threshold just above 1.
- For the 2026 instance $\alpha_{\max} = 16/15$: the published cost vector is optimal both
  for the cost gap and for the violation forced, and the $26/15$ of the all-free routing is
  unattainable by any pricing. [MV]
- **A sharp null result.** Over 3456 parameter points of the spine family that contains it
  (10 structures times 10 demand sets times 6 split fractions at $k = 3$; 4 times 4 times 5
  at $k = 4$), the only counterexample is the published instance at exactly its published
  parameters: one point in 2448 at three terminals, none at all at four. The instance is
  isolated and extremal in its own family, so a larger forced violation needs a different
  conflict structure, not parameter tuning. [MV]
- **A tooling failure and its fix.** sympy's rational simplex cycled on a degenerate family
  member, exactly the single-point-of-failure risk EXP-003 had flagged. We wrote an exact
  Bland-rule simplex; the two implementations now agree on all six decidable cases.

## Declared and not yet run

Nothing is in flight. Next: conflict structures not realisable on a linear spine (UFB-037),
which is the only route left inside this programme to a larger forced violation; an LP-driven
choice of the split fractions instead of sampling them (UFB-036); and the canonical form
(UFB-011) paired with constraint generation (UFB-034), which together open the minimality
exhaustion (UFB-012).
