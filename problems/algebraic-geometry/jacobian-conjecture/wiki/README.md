# Jacobian conjecture - wiki

Curated exposition of the problem and of this program's results. Every claim here traces to a
numbered experiment (`../experiments/`) or a primary source (`../context/`). State: exploring.

| Page | Content |
|---|---|
| [01-statement-and-history.md](01-statement-and-history.md) | The conjecture, Kraus 1884 to Keller 1939 to Smale 16, the classical results ladder, the 2026 refutation for N >= 3. |
| [02-mechanism.md](02-mechanism.md) | Why the counterexample works: weighted skew-product structure, the reduced two-variable Keller identity, the fiber cubic, non-properness. |
| [03-seed-family.md](03-seed-family.md) | Our constructor v2: the general seed family, det and fiber-degree laws, new explicit counterexamples with rational collision certificates. |
| [04-two-dimensional-frontier.md](04-two-dimensional-frontier.md) | The still-open N = 2 case: the exact obstruction to the mechanism, our null results and conjectures, the honest map of what remains. |
| [05-experiments.md](05-experiments.md) | Index of experiments with verdicts. |

## The picture in five lines

The Jacobian conjecture asked whether a polynomial map $F : \mathbb{C}^N \to \mathbb{C}^N$ with
constant nonzero Jacobian determinant must be invertible. On 2026-07-19 Levent Alpöge (with the
LLM Claude Fable 5) announced a degree-(7, 6, 4) map on $\mathbb{C}^3$ with $\det JF = -2$ and a
three-point fiber: the conjecture is FALSE for $N \ge 3$ (we validated this exactly, EXP-001).
This program reverse-engineered the structure (EXP-002), generalized it to an infinite
constructor family with new explicit counterexamples (EXP-004), and localized exactly why the
mechanism cannot touch the still-open case $N = 2$ (EXP-005).
