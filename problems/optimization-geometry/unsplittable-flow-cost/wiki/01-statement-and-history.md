# 01 - Statement and history

## The setting

A single source $s$ in a digraph $G = (V, A)$ must serve terminals $t \in T$ with demands
$d_t$. A FRACTIONAL (splittable) flow $x \in \mathbb{Q}^A_{\ge 0}$ may split a terminal's
demand across several paths; an UNSPLITTABLE flow $\mathcal{P} = \{P^t\}_{t \in T}$ must
send each terminal's entire demand along a SINGLE $s$-$t$ path, with resulting arc load

$$f^{\mathcal{P}}(a) = \sum_{t \in T:\, a \in P^t} d_t .$$

Write $d_{\max} = \max_t d_t$. Throughout this literature the capacity of an arc is taken
to BE $x(a)$, the fractional load: violation is measured against the flow you are rounding,
which is the worst case. Reading any statement below with a separate capacity vector in
mind silently changes it. [VERIFIED: arXiv:2308.02651, "this can be interpreted as a
worst-case assumption where the capacity $u(a)$ of an arc $a$ is equal to $x(a)$"]

Deciding whether an unsplittable flow respecting capacities exists at all is NP-hard, even
on a two-vertex graph (Bin Packing and Subset Sum reduce to it), which is why the field
studies rounding WITH a bounded violation instead. [VERIFIED: arXiv:2308.02651]

## The theorem (Dinitz, Garg, Goemans 1999)

Given any SSUF instance, one can compute in polynomial time an unsplittable flow with

$$f^{\mathcal{P}}(a) \le x(a) + d_{\max} \qquad \text{for every arc } a .$$

Call such a routing CONGESTION-GOOD. The additive $d_{\max}$ is the best constant one can
hope for. [VERIFIED as a statement in three independent primary sources; the Combinatorica
original, 19(1) 1999, 17-41, remains unread here and is backlog UFB-002]

## The conjecture (Goemans, shortly after)

Add nonnegative arc costs $c$. Call a routing COST-GOOD if $c^T f^{\mathcal{P}} \le c^T x$.
Goemans conjectured that one can always have BOTH at once: a routing that is
congestion-good and cost-good simultaneously.

Each condition alone is easy or known. Congestion-goodness alone is the theorem above.
Cost-goodness alone is trivial: route every terminal on a cheapest $s$-$t$ path, ignoring
capacities entirely. The whole content of the conjecture is the word SIMULTANEOUSLY.

An equivalent form, used throughout the literature: $x$ can be written as a CONVEX
COMBINATION of congestion-good unsplittable flows. One direction is immediate (if
$x = \sum_i \lambda_i y_i$ then $\min_i c^T y_i \le c^T x$ for every $c \ge 0$); the
converse is attributed to Martens, Salazar and Skutella. [VERIFIED as a statement:
arXiv:2412.05182 footnote 1; the converse's proof is unread here, backlog UFB-003]

## The arc, 1998 to 2026

| Year | Event |
|---|---|
| 1998/99 | Dinitz, Garg, Goemans prove the congestion theorem (FOCS 1998, Combinatorica 1999). Goemans conjectures the cost version shortly after. |
| 2002 | Skutella proves the conjecture when all demands are multiples of one another. |
| 2022 | Morell and Skutella state two stronger conjectures adding arc-wise LOWER bounds, and prove the lower-bound half alone. |
| 2023/24 | Traub, Vargas Koch and Zenklusen prove a cost statement for PLANAR graphs at twice the violation, $2 d_{\max}$, via a structured discrepancy problem. Their paper records: "This intriguing conjecture remains open. More so, there are arguably no non-trivial graph classes for which it is known to hold." |
| 2024/25 | Majthoub Almoghrabi, Skutella and Warode prove the conjecture for SERIES-PARALLEL digraphs, in the stronger convex-combination form and with STRICT deviation $< d_{\max}$: the first non-trivial class. |
| 2025-10 | Swamy, Traub, Vargas Koch and Zenklusen show the cost-free two-sided conjecture implies a $2 d_{\max}$ cost statement, and record that whether Goemans' conjecture holds even with $O(d_{\max})$ violation "remains wide open". |
| 2026-07-22/23 | A counterexample is announced publicly, outside peer review: a 7-vertex planar instance produced with a large language model. No preprint; no expert confirmation found at the time of writing. |
| 2026-07-24 | This programme verifies that instance independently, by exact enumeration (EXP-002). The conjecture is FALSE. [MV] |

## What the refutation does and does not mean

FALSE: the conjecture as stated, with the constant 1; the Morell-Skutella conjecture with
costs (the counterexample is acyclic); the convex-combination form. [MV for the instance,
[D] for the two corollaries]

STILL TRUE or STILL OPEN: the Dinitz-Garg-Goemans theorem itself (it has no cost clause);
the cost-free two-sided conjecture; the $2 d_{\max}$ cost statement; the series-parallel and
planar theorems; and the question the primary literature calls the breakthrough target,
whether a cost-good routing always exists with violation $O(d_{\max})$. The counterexample
forces the violation constant above 1 by exactly $1/15$, so the gap between what is refuted
(1) and what is proved for planar graphs (2) remains almost entirely open. [MV for the
constant, see 03]
