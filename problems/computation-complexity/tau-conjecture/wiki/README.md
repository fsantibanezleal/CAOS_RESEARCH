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
| 01 statement and history | Model, the conjecture, Smale's list, the BSS route | planned (source: 2026-08-01 dossier) |
| 02 the implication ladder | SS95, Koiran 2004, Buergisser 2009, factoring, 2026 state | planned (source: 2026-08-01 dossier) |
| 03 the census | Exact $z_{\max}(\tau)$ ladder and the integer $\tau'(n!)$ tables | started by EXP-001: $z_{\max}(1..4) = 1,2,3,3$ |
| 04 mechanisms | Anatomy of extremal witnesses; family rate results | planned |
| 05 experiments index | One line per EXP-NNN with verdicts | started |

## Experiments index

| EXP | Question | Verdict |
|---|---|---|
| [EXP-001](../experiments/EXP-001-small-tau-census/) | Exact $z_{\max}(\tau)$ for $\tau \le 4$ + Markstroem regression gate | CONFIRMED: gate 14/14; $z_{\max}(4) = 3$ |
