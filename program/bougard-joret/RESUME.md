# Bougard-Joret: session handoff

Updated: 2026-09-05.

## 1. State in one screen

[D] EXP-003 proves $T(d,d+1)=d^2+d+2$ for every integer $d\ge7$, where $T$ is the maximum triangle-free edge count under degree and matching bounds. The fixed-order bound at $2d+3$ is also sharp. The new contribution is the uniform upper bound; the attaining BET construction and finite values through $d=12$ are prior work. In particular, $T(13,14)=184$, closing BET's 184-to-185 interval. The full AEY conjecture remains open.

[D] Secondary result: $d^2+4d+1\le f(2d+3,2,d+2)\le d^2+4d+2$, $d\ge7$. The exact endpoint remains undetermined. The lower bound exceeds the degree-sum prediction by $\lfloor d/2\rfloor-2$. The raw BET extremizer's complement has connectivity $d+1$, so it cannot attain the required Bougard-Joret connectivity $d+2$.

[MV] EXP-003 certificates PASS: 48 graphs over $d=7,\ldots,30$, 24 rejected raw-complement cuts, and no survivors among 287,564 five-type candidates. The separate NetworkX audit checks all 48 matching numbers, complement independence numbers, and complement connectivities. Independent reasoning audit passed. The separate next-matching manuscript v0.01 and Zenodo publication remain pending; first-shell v0.02 is preserved.

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
| $T(d,m)$ | Maximum edges of a triangle-free graph with $\Delta\le d$, $\nu\le m$; distinct from Bougard-Joret $f$ |
| Next matching level | $T(d,d+1)=d^2+d+2$, all $d\ge7$; EXP-003 proof |
| $Q_d$ | Known BET attaining graph; its complement has connectivity $d+1$ |
| Bougard bracket | $d^2+4d+1\le f(2d+3,2,d+2)\le d^2+4d+2$; exact endpoint open |
| Matching certificate | EXP-003 certificate and separate NetworkX receipt; finite checks support the proof |

## 3. Experiment index

| Experiment | Question | Verdict | Load-bearing result |
|---|---|---|---|
| EXP-001-tree-strip | Adjacent diagonal value and all extremals | CONFIRMED | Uniform proof plus independently checked finite constructions |
| EXP-002-next-shell | Full first-shell value; all alpha-two extremals | CONFIRMED | Complete proof audited; independent exact certificates pass |
| EXP-003-triangle-free-next-matching | Exact next matching level for every $d\ge7$ | Proof and independent audits PASS | Uniform upper bound; known BET construction; separate manuscript and Zenodo pending |

## 4. In flight

Current round: EXP-003's committed preflight is `f3fdda6`. Its proof and independent audits pass. The separate manuscript is planned at `manuscripts/bougard-joret/next-matching/`, version 0.01, with Zenodo publication and public-byte verification pending. No DOI is assigned in this handoff. Scoped integration remains part of the current delivery work. Read the [next-matching source review](../../problems/combinatorics/bougard-joret/context/2026-09-05-next-matching-review.md) and [current plan](plan-2026-09-05-triangle-free.md).

Previous completed round: manuscript v0.02 is PUBLISHED at version DOI [10.5281/zenodo.22341644](https://doi.org/10.5281/zenodo.22341644), concept DOI 10.5281/zenodo.22315251. All 343,535 bytes matched a fresh unauthenticated download at publication; SHA-256 `faed3c5a760390a89bc77945e99837c85a55b09f6923570dcde50f289439d4b7`. API latest-version check and all ten PDF pages passed. After incorporating concurrent develop changes, all 100 repository tests passed. Research PR #251 passed current-head CI and merged at `8055fec`; private mirror PR #611 merged at `a6d642fd`. That research/publication round is complete, and its manuscript is preserved.

The paragraph below records the completed September 4 baseline.

Manuscript v0.01 remains frozen at version DOI `10.5281/zenodo.22315252`. At its publication, a fresh download matched all 319,548 PDF bytes, SHA-256 `a804014fddf8d47ae0dc3988c7b1e6a0d3619daf0a423b398724321095bbb323`, and the API confirmed it was then concept-latest. Research PR #248 merged to develop at `2507925`, and management PR #608 merged at `f09d60ee`. No serialized global release is claimed by this round.

## 5. Next actions

1. Read the [EXP-003 proof](../../problems/combinatorics/bougard-joret/experiments/EXP-003-triangle-free-next-matching/proof.md), certificate, independent audit, and the next-matching source review. The experiment verdict owns final evidence status.
2. Complete the separate next-matching manuscript v0.01, full checks, all-page PDF inspection, Zenodo publication, and fresh public-byte verification. Preserve the tree-strip manuscript v0.02.
3. Complete scoped commits, push, develop integration and final remote-state verification for this round; record its actual DOI and receipts when available.
4. EXP-001 and EXP-002 remain replayable from their own experiment directories. Their proofs and published manuscript are completed baselines, not pending new work.
5. Further research may address remaining triangle-free matching levels, the exact Bougard bracket endpoint, other shell extremizers, or $n=\alpha+k+2$. Require a new committed hypothesis before further computation. Both general conjectures remain open.

## 6. Where everything lives

- Operational state: `program/bougard-joret/`.
- Sources and portfolio audit: `problems/combinatorics/bougard-joret/context/`.
- Proof, code and certificate: `problems/combinatorics/bougard-joret/experiments/EXP-001-tree-strip/`.
- Full-shell proof, code and certificate: `problems/combinatorics/bougard-joret/experiments/EXP-002-next-shell/`.
- Next-matching proof and certificates: `problems/combinatorics/bougard-joret/experiments/EXP-003-triangle-free-next-matching/`.
- Narrative: `problems/combinatorics/bougard-joret/wiki/`.
- Preserved published manuscript: `manuscripts/bougard-joret/tree-strip/`, v0.02.
- New manuscript: `manuscripts/bougard-joret/next-matching/`, planned v0.01, Zenodo pending.
- Private mirror: `plans/caos-research/bougard-joret/` in the management repository.

## 7. Gotchas

- $T(d,m)$ is a maximum under degree/matching constraints; $f(n,\alpha,k)$ is a minimum under independence/connectivity constraints. Keep them distinct.
- BET owns the attaining construction and known finite values. The new claim is the uniform upper bound, with $T(13,14)=184$.
- Complementing the matching extremizer yields connectivity $d+1$, not the required $d+2$. Only the one-edge Bougard bracket is proved.
- The $d=6$ five-cycle blowup has 45 edges, not the formula's 44; it is deliberately outside the theorem range.
- Exactly two surviving tree vertices require the double-star case; the shared-neighbor argument alone is incomplete.
- Nonstar is necessary: a star yields independence number $k$.
- Tree representations do not automatically count unmarked isomorphism classes.
- The local finite controls do not establish the universal quantifier; the written proof does.
- Existing worktrees and management media edits were preserved. Shared releases remain serialized; no global bake or version bump belongs to this problem round.

Lenses ledger: degree sum and residual cyclomatic number yield the tree strip; missing-neighbor fibers and cyclic gaps yield the first shell; shortest-odd-cycle deficits and five neighborhood types yield the next matching upper bound; Tutte-Berge controls arbitrary order; adversarial complement cuts limit the Bougard translation.
