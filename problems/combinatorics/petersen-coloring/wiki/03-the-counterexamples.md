# 03 - The counterexamples and their independent certification

Sources: EXP-001 verdict; `context/2026-09-03-source-dossier.md`.

## The three retrievable graphs

| name | order | size | girth | edge connectivity | cyclic edge connectivity | digest (Putman convention) | origin |
|---|---|---|---|---|---|---|---|
| `G112` | 112 | 168 | 5 | 3 | 4 [MV] | `dc16cc18600cf77c8661b7baf89c7019f265299308541961ff884ea7187b4e8b` | Putman main graph, $G = 3L + C$, $L = 4F + C$ |
| `H112` | 112 | 168 | 5 | 3 | 4 [MV] | `0f2d8858110c6f012de7ddffa92fdbc709d7da630f199b0e3c81bb56eb6b35c7` | Putman $D_3$-symmetric graph |
| `G52` | 52 | 78 | 5 | 3 | 4 [MV] | `27db5d3b680441cf...` (our 0-based transcription) | Goedgebeur-Jooken-Macajova-Mattiolo-Mazzuoccolo appendix |

Here $F$ is the Petersen graph minus the endpoints of one edge (an 8-vertex 4-pole), $C$ a claw
six-pole, and $L$ a 36-vertex 4-pole; all three counterexamples contain $F$ as a submultipole.
Cyclic edge connectivity 4 is certified by an exhaustive search over all edge sets of size at
most 3 (no cycle-separating cut) and an explicit cycle-separating 4-cut ($\{2,6,9,12\}$ in the
112-vertex graphs, $\{2,3,8,14\}$ in `G52`, edge indices of the sorted edge lists).

## The mechanism (Jooken)

With $Q$ the line graph of $P$ and $i_1, i_2, o_1, o_2$ the semi-edges of $F$: every
P-coloring of $F$ has $\mathrm{dist}_Q(\sigma(i_1), \sigma(i_2)) \le 2$ and the outputs are
determined by the inputs (equal at distance 0; copied at distance 1; copied or both replaced by
their "starred" neighbours at distance 2). For $L$ the outputs are equal at distance 0, copied at
distance 1, and swapped at distance 2 or 3. Three copies of $L$ around a claw then force four
edges of $P$ pairwise adjacent in $Q$, a 4-clique impossible in the line graph of a triangle-free
cubic graph. [V, Jooken Lemmas 2.1, 2.2, Theorem 2.3]

## Independent certification (EXP-001, CONFIRMED)

Our encodings share no variable scheme with the public ones: Petersen colorings use edge-image
variables $y_{e,f}$ ($f \in E(P)$) with pairwise adjacency clauses (valid because $P$ is
triangle-free, so three pairwise adjacent distinct edges form a star); normal colorings use
edge-color variables, side-presence variables $p_{e,c}, q_{e,c}$ and a rich indicator $r_e$.

| instance | solve (s) | proof (bytes) | drat-trim (s) |
|---|---|---|---|
| `G112` Petersen | 65.6 | 98,426,474 | 43.7 |
| `G112` normal-5 | 1,216.8 | 786,818,036 | 900.5 |
| `H112` Petersen | 29.5 | 95,632,373 | 24.5 |
| `H112` normal-5 | 977.2 | 868,156,862 | 1,293.5 |
| `G52` Petersen | 1.8 | 4,094,201 | 1.2 |
| `G52` normal-5 | 178.8 | 226,490,830 | 231.8 |

All six UNSAT with `s VERIFIED`; the same holds with symmetry breaking removed. Five colorable
controls (Petersen, $K_4$, prism, $J_5$, $J_7$) are SAT with checker-validated witnesses. Putman's
four public proofs verify under our drat-trim binary (third route). [MV]
