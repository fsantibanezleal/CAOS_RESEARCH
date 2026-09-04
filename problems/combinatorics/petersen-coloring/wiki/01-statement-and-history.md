# 01 - Statement and history

Sources: `context/2026-09-03-source-dossier.md` (marks as there).

## The conjecture

Let $P$ be the Petersen graph. For a cubic graph $G$, a Petersen coloring is a map
$\sigma : E(G) \to E(P)$ such that for every vertex $v$ of $G$ there is a vertex $w$ of $P$ with

$$\sigma(\partial_G(v)) = \partial_P(w),$$

that is, the three edges at $v$ go bijectively onto the three edges at some vertex of $P$.

**Conjecture (Jaeger 1988).** Every bridgeless cubic graph has a Petersen coloring. [V via the
2026 papers]

**Equivalence (Jaeger 1985).** $G$ has a Petersen coloring iff $G$ has a normal 5-edge-coloring:
a proper 5-edge-coloring in which every edge $uv$ is poor ($|c(\partial u)\cup c(\partial v)|=3$)
or rich ($=5$). [V, Putman Proposition 2.1]

## Why it mattered

The conjecture implies the Berge-Fulkerson conjecture (six perfect matchings covering every edge
exactly twice) and the 5-cycle double cover conjecture [V, Jooken introduction; Mazzuoccolo-
Mkrtchyan abstract]. Berge's conjecture (perfect matching index at most 5) and the Fan-Raspaud
conjecture (three perfect matchings with empty intersection) follow from Berge-Fulkerson [D].
Every 3-edge-colorable cubic graph is Petersen colorable, so only snarks matter [V, Open Problem
Garden].

## Verification frontier before 2026

All snarks on at most 36 vertices (Brinkmann-Goedgebeur-Hagglund-Markstrom 2013) and all weak
snarks of girth 4 on 36 vertices (Goedgebeur-Macajova-Skoviera 2019) are Petersen colorable; a
smallest counterexample must be a weak snark, so every counterexample has at least 38 vertices
[V, GJMMM Section 5].

## The disproof (August 2026)

| date | who | what |
|---|---|---|
| 2026-08-06 | Putman | two nonisomorphic 112-vertex counterexamples, girth 5, connectivity 3; SAT plus DRAT certificates; AI-assisted discovery |
| 2026-08-14 | Jooken | human-checkable proof via the P-coloring sets of the 4-poles $F$ and $L$ and a 4-clique obstruction in the line graph of $P$ |
| 2026-08-14 | Goedgebeur, Jooken, Macajova, Mattiolo, Mazzuoccolo | 52-vertex cyclically 4-edge-connected girth-5 counterexample; infinite cyclically 4-edge-connected families; smallest order in $[38, 52]$ |
| 2026-08 | anonymous X account | a 68-vertex counterexample (not retrievable) [U] |

Open after these papers: the smallest counterexample (Problem 7), cyclically 5-edge-connected
counterexamples (Problem 5), and the normal 6-edge-coloring conjecture (Conjecture 6).

## What this record does

CAOS does not compete for minimality. It certifies the public graphs independently (EXP-001) and
audits what survives of the implication ladder on the first counterexamples: perfect matching
covers (EXP-002), cycle double covers and flows (EXP-003), normal 6-edge-colorings and exact
defects (later experiments).
