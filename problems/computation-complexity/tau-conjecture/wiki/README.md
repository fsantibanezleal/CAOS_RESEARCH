# Shub-Smale tau conjecture (Smale problem 4): wiki

Curated exposition of the problem and of our verified results. Pages are
written vertically: each lands in the same round as the experiments whose
content it transcribes (from `../context/` dossiers and `../experiments/`
verdicts, never from memory).

## The problem in one paragraph

For $f \in \mathbb{Z}[x]$ computed by a constant-free straight-line program
(gates $+,-,\times$; free constants $-1,0,1$; input $x$) of length
$\tau(f)$, Shub and Smale conjectured (1995) that the number $z(f)$ of
distinct integer roots satisfies $z(f) \le (1+\tau(f))^c$ for a universal
constant $c$. True, it implies $P_{\mathbb{C}} \ne NP_{\mathbb{C}}$ in the
Blum-Shub-Smale model and $VP^0 \ne VNP^0$ in constant-free Valiant theory;
it is open, the real-zeros analogue is false, and no nontrivial lower bound
on $\tau(n!)$ is known.

## Pages

| Page | Content | Status |
|---|---|---|
| [01 statement and history](01-statement-and-history.md) | Model, the conjecture, sharpness, the real-side failure, history ladder | transcribed 2026-08-01 |
| 02 the implication ladder | SS95, Koiran 2004, Buergisser 2009, factoring, Rojas reduction, 2026 state | planned (source: 2026-08-01 dossier + approaches evaluation) |
| 03 the census | Exact $z_{\max}(\tau)$ ladder, record gallery, witness programs | data ready: $z_{\max}(1..5) = 1,2,3,3,4$ (EXP-001/002) |
| 04 mechanisms | DOS/Chebyshev-shadow factory, shifted products, family rate results | seeded by EXP-002 verdict |
| 05 experiments index | One line per EXP-NNN with verdicts | current |

## Experiments index

| EXP | Question | Verdict |
|---|---|---|
| [EXP-001](../experiments/EXP-001-small-tau-census/) | Exact $z_{\max}(\tau)$ for $\tau \le 4$ + Markstroem regression gate | CONFIRMED: gate 14/14; $z_{\max}(4) = 3$ |
| [EXP-002](../experiments/EXP-002-census-depth5/) | $z_{\max}(5)$; minimal $\tau$ for 4 roots; valuation spectra | CONFIRMED: $z_{\max}(5) = 4$; minimal $\tau$ = 5; DOS mechanism |
