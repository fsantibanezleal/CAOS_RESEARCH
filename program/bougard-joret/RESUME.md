# Bougard-Joret: session handoff

Updated: 2026-09-05.

## 1. State in one screen

[D] EXP-002 extends the result to the full first interior shell: for every $k\ge3$, $2\le\alpha\le k+1$, $f(\alpha+k+1,\alpha,k)=\lceil k(\alpha+k+1)/2\rceil$. For $\alpha=2$, every extremal graph is the complement of disjoint cycles of lengths at least five. The proof owns these universal statements; the experiment verdict owns final audit status. General shell extremizers are not classified beyond this case and the original tree strip.

[MV] EXP-002 certificate PASS: 75 graphs, 45 independent direct checks, 36 Harary cases, 15 odd-degree-sum cases, 75 damaged-edge controls, eight complement-cycle controls, and the complete order-six census of 32,768 graphs with 60 extremals.

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
| First interior shell | $n=\alpha+k+1$, $k\ge3$, $2\le\alpha\le k+1$; EXP-002 proof |
| Shell certificate | EXP-002 `artifacts/certificate.json`; finite PASS is not a universal proof |

## 3. Experiment index

| Experiment | Question | Verdict | Load-bearing result |
|---|---|---|---|
| EXP-001-tree-strip | Adjacent diagonal value and all extremals | CONFIRMED | Uniform proof plus independently checked finite constructions |
| EXP-002-next-shell | Full first-shell value; all alpha-two extremals | CONFIRMED | Complete proof audited; independent exact certificates pass |

## 4. In flight

Current round: manuscript v0.02 is PUBLISHED at version DOI [10.5281/zenodo.22341644](https://doi.org/10.5281/zenodo.22341644), concept DOI 10.5281/zenodo.22315251. All 343,535 bytes match a fresh unauthenticated download; SHA-256 `faed3c5a760390a89bc77945e99837c85a55b09f6923570dcde50f289439d4b7`. API latest-version check and all ten PDF pages pass. After incorporating concurrent develop changes, all 100 repository tests pass. Research PR #251 passed current-head CI and merged at `8055fec`; private mirror PR #611 merged at `a6d642fd`. This research/publication round is complete. No mathematical run remains active.

The paragraph below records the completed September 4 baseline.

Manuscript v0.01 remains frozen at version DOI `10.5281/zenodo.22315252`. At its publication, a fresh download matched all 319,548 PDF bytes, SHA-256 `a804014fddf8d47ae0dc3988c7b1e6a0d3619daf0a423b398724321095bbb323`, and the API confirmed it was then concept-latest. Research PR #248 merged to develop at `2507925`, and management PR #608 merged at `f09d60ee`. No serialized global release is claimed by this round.

## 5. Next actions

1. Replay: `python problems/combinatorics/bougard-joret/experiments/EXP-001-tree-strip/run.py --output tmp/bougard-replay.json`.
2. Regression: `python -m pytest tests/test_bougard_joret_tree_strip.py`.
3. Read `problems/combinatorics/bougard-joret/context/report-source.md` before selecting another target; it records all 20 portfolio rows and important unsplittable-flow updates.
4. Read EXP-002 `proof.md`, `verdict.md`, and the September 5 portfolio refresh; replay `python problems/combinatorics/bougard-joret/experiments/EXP-002-next-shell/run.py --output tmp/bougard-shell-replay.json`.
5. The September 5 proof, publication and scoped integration are complete. See [the closed plan](plan-2026-09-05.md); further research requires a new committed hypothesis.
6. Further research: classify remaining shell extremizers or declare a new hypothesis for $n=\alpha+k+2$. The general problem remains open.

## 6. Where everything lives

- Operational state: `program/bougard-joret/`.
- Sources and portfolio audit: `problems/combinatorics/bougard-joret/context/`.
- Proof, code and certificate: `problems/combinatorics/bougard-joret/experiments/EXP-001-tree-strip/`.
- Full-shell proof, code and certificate: `problems/combinatorics/bougard-joret/experiments/EXP-002-next-shell/`.
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
