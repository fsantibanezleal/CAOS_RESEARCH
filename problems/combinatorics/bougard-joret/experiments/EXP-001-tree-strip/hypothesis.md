# EXP-001: tree classification one vertex above the exceptional boundary

Declared 2026-09-04, before computation. CPU, deterministic exact integer combinatorics.

## Question and prediction

For every integer $k\ge3$, predict $f(2k,k-1,k)=k^2$. Predict the following complete equality characterization. Take a nonstar tree $T$ on $k+1$ vertices and an independent set $S$ of size $k-1$. Partition $S$ into labeled fibers $S_t$ of sizes $\deg_T(t)-1$. Join $s\in S_t$ to every vertex of $T$ except $t$. Every resulting graph is extremal, and every extremal graph has this representation relative to every maximum independent set.

Motivation: [primary dossier](../../context/references.md). Das-Gupta solve the preceding order boundary. Degree-sum equality at the new order forces $k$-regularity; the residual graph must then have $k$ edges and be connected.

## Proposed proof and adversarial issue

Necessity: delete a maximum independent set $S$; $T$ is connected, each $s$ misses exactly one of the $k+1$ residual vertices, and $\deg_T(t)=1+|S_t|$. Thus $T$ is a tree. A star would have $k$ independent leaves, contradicting $\alpha=k-1$.

Sufficiency: all degrees are $k$. An independent set contained in a nonstar tree has size at most $k-1$; a mixed independent set consists of a single residual vertex $t$ and some of $S_t$, hence has size at most $\deg_T(t)\le k-1$.

Connectivity needs a separate proof, not a degree argument. Delete fewer than $k$ vertices. If all $S$ disappear, the tree remains intact. If at least three tree vertices survive, every pair of surviving $S$ vertices shares a tree neighbor. The resulting common component omits at most one residual vertex $t$, and disconnecting it would require deleting its tree neighbors plus all $S\setminus S_t$, at least $k$ vertices. The exceptional case of exactly two surviving tree vertices forces all $S$ to survive and the two vertices to carry all positive fibers; the tree must then be a double star with an edge between its two internal vertices, reconnecting the components. Explicitly validate this exceptional case.

## Method and success/failure

Write the full all-parameter argument, audit it independently, then enumerate nonisomorphic trees on 4 through 9 vertices using a deterministic construction and canonical deduplication, including stars as negative controls. For $k=3,4,5$, enumerate missing-neighbor assignments and residual graphs satisfying degree equality independently of the tree generator. Exhaustively verify independence by subsets and connectivity by vertex cuts for the small range; compare a separate flow-based connectivity checker if available. Enumerate all labeled simple graphs through order 6 to check the base extremal class independently. Persist witnesses and aggregate counts.

A PASS of finite tests proves only the enumerated statements. The universal conclusion requires the written combinatorial proof and its audit. A counterexample refutes the corresponding prediction; an incorrect proof step requires repair and explicit recording, never concealment. Reaching the budget is inconclusive for missing controls and does not weaken the theorem's proof obligation.

## Premises, invariants and cost

No previous local experiment is a premise. Definitions, the handshaking lemma and elementary tree facts are rederived as needed. Das-Gupta's boundary theorem motivates the target but is not needed for its proof.

Invariant-first: $2e=2k^2$ with minimum degree $k$ forces all degrees equal; residual connectedness and $e(T)=|T|-1$ force a tree. This avoids an unrestricted graph search.

Five-minute cap per stage; checkpoint after every tree order / parameter. Expected seconds to a few minutes. Stop with a saved partial record at budget. Small smoke stage before any larger run. Negative controls: star input must fail the independence target; remove an edge from a valid graph and reject the $k$-regular certificate; residual disconnected equality models must fail connectivity. No solver UNSAT claim is used as proof.
