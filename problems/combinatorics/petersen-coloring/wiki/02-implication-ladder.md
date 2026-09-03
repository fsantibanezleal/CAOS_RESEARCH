# 02 - The implication ladder, before and after the disproof

Sources: `context/2026-09-03-source-dossier.md` section 2; EXP-002, EXP-003 verdicts.

## Before August 2026

$$
\text{Petersen coloring conjecture}
\;\Longrightarrow\;
\begin{cases}
\text{Berge-Fulkerson} \Longrightarrow \text{Berge (index} \le 5) \Longrightarrow \text{Fan-Raspaud},\\[2pt]
\text{5-cycle double cover} \Longrightarrow \text{cycle double cover}.
\end{cases}
$$

- Petersen coloring iff normal 5-edge-coloring (Jaeger 1985) [V via Putman Prop. 2.1].
- Petersen coloring implies Berge-Fulkerson and the 5-cycle double cover conjecture (Jaeger
  1988) [V via Jooken, Mazzuoccolo-Mkrtchyan].
- Berge-Fulkerson implies Berge: five of the six matchings already cover every edge; implies
  Fan-Raspaud: any three of the six meet in no edge because every edge lies in exactly two [D].
- 3-edge-colorable cubic graphs have Petersen colorings [V, Open Problem Garden], so the whole
  ladder is about snarks.

## After the disproof

The top of the ladder is false (Putman 2026; Jooken 2026; Goedgebeur-Jooken-Macajova-Mattiolo-
Mazzuoccolo 2026). Every implication below the top is still a theorem, but the conjectures
below the top lose their strongest known sufficient condition, and the counterexamples become
their sharpest test cases: they are the only known bridgeless cubic graphs for which the
Petersen route to a Berge-Fulkerson cover or a 5-cycle double cover is closed.

## What survives on the counterexamples (this record)

| conjecture | `G112` | `H112` | `G52` | evidence |
|---|---|---|---|---|
| Berge-Fulkerson | holds | holds | holds | explicit six perfect matchings, EXP-002 |
| Berge (index $\le 5$) | holds, index 4 | holds, index 4 | holds, index 4 | explicit four perfect matchings, EXP-002 |
| Fan-Raspaud | holds | holds | holds | explicit triple, EXP-002 |
| 5-cycle double cover | holds | holds | holds | explicit five even subgraphs, EXP-003 |
| Tutte 5-flow | holds | holds | holds | explicit nowhere-zero $\mathbb{Z}_5$ flow, EXP-003 |
| normal 6-edge-coloring (Conjecture 6 of GJMMM) | EXP-004 | EXP-004 | EXP-004 | pending |

None of these is evidence for the general conjectures beyond the three graphs; the record only
says that the first three counterexamples do not carry any of them down with the Petersen
coloring conjecture.
