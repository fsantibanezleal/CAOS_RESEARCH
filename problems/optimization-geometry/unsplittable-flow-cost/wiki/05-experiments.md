# 05 - Experiments

One line per experiment; the folders hold hypothesis, run, artifacts and the long-form
verdict. Verdicts are reported verbatim, never upgraded in language (methodology/06).

| EXP | Question | Verdict | The single load-bearing output |
|---|---|---|---|
| [EXP-001](../experiments/EXP-001-exact-instance-checker/) | Does our own exact checker decide SSUF instances correctly on hand-built cases with known answers? | CONFIRMED (2026-07-24) | `ufclib` adopted as ground truth: predictions P1-P8 hold on V1-V5 (parallel arcs, cyclic digraph, tight boundary, corrupted-flow rejection, exact rationals); 14 pytest regression tests |
| [EXP-002](../experiments/EXP-002-adjudicate-2026-claim/) | Is the 2026 claimed counterexample valid, and what exactly does it force? | CONFIRMED (2026-07-24) | Goemans' Conjecture 1.2 is FALSE: $c^T x = 58$, all 8 routings enumerated, the 4 congestion-good ones cost 90, 60, 60, 60; and $\alpha_{\mathrm{inst}} = 16/15$, so the refutation is by exactly one unit |

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

## Declared and not yet run

Nothing is in flight. The next declarations, in order, are the exact rational separation LP
(UFB-010) and the canonical form (UFB-011), which together open the minimality exhaustion
(UFB-012); then the conflict-family constructions for the frontier constant (UFB-020,
UFB-021, UFB-030).
