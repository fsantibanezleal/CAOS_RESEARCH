# Bougard-Joret: session handoff

Updated: 2026-09-04.

## 1. State in one screen

[D] EXP-001 proves $f(2k,k-1,k)=k^2$ for every $k\ge3$. Every extremal graph is built from a nonstar tree $T$ on $k+1$ vertices and an independent $(k-1)$-set partitioned into fibers $|S_t|=\deg_T(t)-1$; each fiber misses only its indexing tree vertex. The numerical extension starts at $k=4$; $k=3$ was known. The full Bougard-Joret problem is not solved.

[MV] 86 nonstar tree controls passed; six stars rejected; independent cut/flow and independence checks agree; all 32,768 labeled order-six graphs audited. See the EXP-001 verdict and certificate for exact counts.

## 2. The objects table

| Object | Definition / authority |
|---|---|
| $f(n,\alpha,k)$ | Minimum edges of a $k$-connected graph with order $n$ and independence $\alpha$ |
| $T$ | Nonstar tree of order $k+1$, EXP-001 |
| $S_t$ | Missing-neighbor fiber, cardinality $\deg_T(t)-1$ |
| $G(T,(S_t))$ | Tree plus all cross edges except the fiber nonedges |
| Certificate | EXP-001 `artifacts/certificate.json`, exact finite controls |

## 3. Experiment index

| Experiment | Question | Verdict | Load-bearing result |
|---|---|---|---|
| EXP-001-tree-strip | Adjacent diagonal value and all extremals | CONFIRMED | Uniform proof plus independently checked finite constructions |

## 4. In flight

No mathematical computation remains active. Manuscript v0.01 is compiled/publication work in progress; reserved version DOI `10.5281/zenodo.22315252`, concept record `22315251` checked from the API. A reservation is not publication. Final publication and PR verification are recorded in the closing state entry.

## 5. Next actions

1. Replay: `python problems/combinatorics/bougard-joret/experiments/EXP-001-tree-strip/run.py --output tmp/bougard-replay.json`.
2. Regression: `python -m pytest tests/test_bougard_joret_tree_strip.py`.
3. Read `problems/combinatorics/bougard-joret/context/report-source.md` before selecting another target; it records all 20 portfolio rows and important unsplittable-flow updates.
4. If extending, declare EXP-002 for $n=\alpha+k+1$ with $k-\alpha\ne1$; prove a residual connectivity/independence criterion before broad enumeration. Do not claim the whole shell is solved.

## 6. Where everything lives

- Operational state: `program/bougard-joret/`.
- Sources and portfolio audit: `problems/combinatorics/bougard-joret/context/`.
- Proof, code and certificate: `problems/combinatorics/bougard-joret/experiments/EXP-001-tree-strip/`.
- Narrative: `problems/combinatorics/bougard-joret/wiki/`.
- Manuscript: `manuscripts/bougard-joret/tree-strip/`.
- Private mirror: `plans/caos-research/bougard-joret/` in the management repository.

## 7. Gotchas

- Exactly two surviving tree vertices require the double-star case; the shared-neighbor argument alone is incomplete.
- Nonstar is necessary: a star yields independence number $k$.
- Tree representations do not automatically count unmarked isomorphism classes.
- The local finite controls do not establish the universal quantifier; the written proof does.
- Existing worktrees and management media edits were preserved. Shared releases remain serialized; no global bake or version bump belongs to this problem round.

Lenses ledger: exclusion/degree sum forces regularity; invariant/residual cyclomatic number forces a tree; anatomy supplies missing-neighbor fibers; adversarial review repairs the two-vertex case; the portfolio comparison identifies a future residual-graph generalization.
