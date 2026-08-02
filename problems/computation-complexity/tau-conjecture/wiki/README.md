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

## Manuscript

The census paper (v0.01, 2026-08-01, CC-BY-4.0) is published on Zenodo:
version DOI [10.5281/zenodo.21753439](https://doi.org/10.5281/zenodo.21753439),
concept DOI [10.5281/zenodo.21753438](https://doi.org/10.5281/zenodo.21753438)
(always the latest version). Source: `../../../../manuscripts/tau-conjecture/census/`.

## Pages

| Page | Content | Status |
|---|---|---|
| [01 statement and history](01-statement-and-history.md) | Model, the conjecture, sharpness, the real-side failure, history ladder | transcribed 2026-08-01 |
| [02 the implication ladder](02-implication-ladder.md) | SS95, Koiran 2004, Buergisser 2009, factoring, Rojas reduction, 2026 state | transcribed 2026-08-01 |
| [03 the census](03-census.md) | Exact $z_{\max}(\tau)$ ladder, record gallery, the tower obstruction | transcribed 2026-08-01 (EXP-003 row pending its verdict) |
| [04 mechanisms](04-mechanisms.md) | Move inventory, the two stall theorems, dual $T(S)$ table | transcribed 2026-08-01 (round 4) |
| 05 experiments index | One line per EXP-NNN with verdicts | current |

## Experiments index

| EXP | Question | Verdict |
|---|---|---|
| [EXP-001](../experiments/EXP-001-small-tau-census/) | Exact $z_{\max}(\tau)$ for $\tau \le 4$ + Markstroem regression gate | CONFIRMED: gate 14/14; $z_{\max}(4) = 3$ |
| [EXP-002](../experiments/EXP-002-census-depth5/) | $z_{\max}(5)$; minimal $\tau$ for 4 roots; valuation spectra | CONFIRMED: $z_{\max}(5) = 4$; minimal $\tau$ = 5; DOS mechanism |
| [EXP-003](../experiments/EXP-003-last-gate-depth6/) | $z_{\max}(6)$ via the last-gate scan | census CONFIRMED: $z_{\max}(6) = 5$ (min $\tau$ for 5 roots = 6); our "=4" prediction REFUTED |
| [EXP-004](../experiments/EXP-004-depth7/) | $z_{\max}(7)$: does the bottom law continue? | CONFIRMED: $z_{\max}(7) = 5$; the law BREAKS (second plateau); min $\tau$ for 6 roots in $[8,9]$ |
| [EXP-005](../experiments/EXP-005-family-towers/) | Family towers $x^2 - c$: is the parameterized loophole real? | CONFIRMED (empty; max 5 only at $c=2$); DISCOVERED the 2-cycle series $c = m^2{+}m{+}1$; cycle-length ceiling |
