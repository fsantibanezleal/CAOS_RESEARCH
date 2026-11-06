# EXP-001 verdict: no counterexample to Hoa's conjecture through order 11; A185306(11) = 67

Date: 2026-11-06. Status: **CONFIRMED [MV]** (prediction held on the computed range). The hypothesis was committed
before any computation.

## Result

Every maximal non-Hamiltonian graph of order $n\le 11$, up to isomorphism, was found, and every vertex set of
every longest cycle of each was examined.

| n | connected graphs generated | MNH graphs | circumferences (graphs) | Hoa holds | Q2 witness | Q3 witness | max residual components |
|---|---:|---:|---|---|---|---|---:|
| 3 | 2 | 1 | 0 (1: the path $P_3$) | vacuous | none | none | 0 |
| 4 | 6 | 1 | 3 (1) | yes | none | none | 1 |
| 5 | 21 | 3 | 3 (1), 4 (2) | yes | none | none | 1 |
| 6 | 112 | 3 | 4 (1), 5 (2) | yes | none | none | 1 |
| 7 | 853 | 7 | 4, 5, 6 (1, 1, 5) | yes | none | none | 1 |
| 8 | 11,117 | 9 | 5, 6, 7 (1, 2, 6) | yes | none | none | 1 |
| 9 | 261,080 | 18 | 5, 6, 7, 8 (1, 1, 2, 14) | yes | none | none | 1 |
| 10 | 11,716,571 | 31 | 6, 7, 8, 9 (1, 1, 4, 25) | yes | none | none | 1 |
| 11 | 1,006,700,565 | **67** | 6, 7, 8, 9, 10 (1, 1, 2, 6, 57) | yes | none | none | 1 |

Consequences:

1. **Hoa's conjecture holds for every MNH graph of order at most 11**, for every longest cycle. With Zhan's
   counterexamples, the least counterexample order $n_0$ satisfies $12\le n_0\le 56$ (it was $8\le n_0\le 56$).
2. **OEIS A185306 is extended by one term: $a(11)=67$** (the sequence stopped at $a(10)=31$ since 2013).
3. Zhan's Question 2 and Question 3 have no witness through order 11, and his $f(n)$ (Question 4) equals 1 for
   $4\le n\le 11$: every residual of every longest cycle is a single complete graph.

The connected-graph counts equal OEIS A001349 at every order, so the generation is complete.

## Validation

- **Gate 1, known answer:** A185306 for $n=3,\dots,10$ reproduced exactly (1, 1, 3, 3, 7, 9, 18, 31).
- **Gate 2, generator:** geng counts equal A001349 for every order computed, including $n=11$
  ($1{,}006{,}700{,}565$).
- **Gate 3, independent re-check** (`verify.py`, depth-first backtracking, no shared code with `mnh.c`): all 139
  MNH graphs of orders 4 to 11 confirmed non-Hamiltonian with every nonadjacent pair joined by a Hamilton path,
  and their circumference, number of longest-cycle vertex sets and residual flags agree (0 disagreements).
- **Soundness of the prune:** the degree-sum condition used to skip graphs (every nonadjacent pair has
  $d(u)+d(v)\le n-1$) holds in every MNH graph by the Bondy-Chvatal closure argument; graphs failing it are not
  MNH. A geng build that applies the same condition inside generation (`prune_degsum.c`) reproduces 18 and 31 at
  orders 9 and 10.

## Stop condition

The hypothesis runs order 12 only if order 11 extrapolates to under 12 hours on 24 cores. Order 11 took 636 s on 28
processes; order 12 has 164,059,830,476 connected graphs (163 times more), about 29 hours, and the in-generation
prune barely shortens it (46 s against 52 s at order 10). Order 12 is not run in this experiment; faster routes
(the universal-vertex split $K_1\vee H$ with $H$ maximal nontraceable, and maximum degree at most $n-4$ otherwise,
by Goedgebeur-Neyt-Zamfirescu Corollary 12) are recorded as backlog.

## Reproduction

In WSL: build nauty 2.8.9; `gcc -O2 -march=native -o mnh mnh.c`; `geng -cq <n> <res>/<mod> | mnh`; then
`python verify.py <n>` on Windows or Linux. Lists of all MNH graphs with their residual flags:
`artifacts/mnh-n<n>.txt`.
