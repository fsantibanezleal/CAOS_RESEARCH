# Petersen coloring counterexamples: program plan

Opened 2026-09-03 from the scouting round (`program/scouting-2026-09/`), the scoping sheet
(`scoping-2026-09-03.md`), and the source dossier under
`problems/combinatorics/petersen-coloring/context/`. Feasibility A; GPU no (proof-carrying SAT
and exact enumeration on CPU).

## 1. The problem

Jaeger (1988) conjectured that every bridgeless cubic graph `G` admits a Petersen coloring, a map
`E(G) -> E(P)` into the edges of the Petersen graph `P` sending the three edges at every vertex
of `G` onto the three edges at some vertex of `P`. Jaeger (1985) proved this is equivalent to
`G` having a normal 5-edge-coloring (proper, every edge poor or rich). The conjecture implies
the Berge-Fulkerson conjecture and the 5-cycle double cover conjecture. In August 2026 it was
refuted: Putman gave two nonisomorphic 112-vertex counterexamples with DRAT-certified SAT
proofs; Jooken gave a human-checkable proof; Goedgebeur, Jooken, Macajova, Mattiolo and
Mazzuoccolo gave a 52-vertex cyclically 4-edge-connected girth-5 counterexample and infinite
cyclically 4-edge-connected families, and pinned the smallest counterexample order to `[38, 52]`.

## 2. What an offline exact-computation program can genuinely contribute

1. **Independent certification with a second encoding** of every retrievable counterexample
   (112 main, 112 D3, 52): our own CNFs, CaDiCaL proofs checked by drat-trim, positive controls,
   corrupted controls. Replication labeled as replication.
2. **The consequence audit**, unclaimed as of 2026-09-03: for each counterexample, decide by
   exact SAT with certificates whether it has a Berge-Fulkerson cover, a Berge cover with five
   perfect matchings (the perfect matching index), three perfect matchings with empty
   intersection (Fan-Raspaud), a 5-cycle double cover, a nowhere-zero 5-flow, a normal
   6-edge-coloring and a strong normal 6-edge-coloring; compute oddness and resistance exactly.
   These graphs are the first bridgeless cubic graphs outside the Petersen-colorable class, so
   they are the sharpest known test cases for every conjecture the Petersen coloring conjecture
   used to imply.
3. **Exact defect measures**: the normal-5 defect (minimum number of edges that are neither
   poor nor rich over all proper 5-edge-colorings) and the P-defect (minimum number of vertices
   at which the star condition fails over all edge maps into `E(P)`), each with a DRAT lower
   bound and an explicit witness upper bound. Nobody has quantified how far the counterexamples
   are from being colorable.
4. **Anatomy through the P-coloring-set calculus**: exact `P-Col` sets of the 4-poles `F`, `C`,
   `L` and of the 52-graph's connector, reproduced independently; used for a bounded,
   grammar-restricted minimality question (compositions of copies of `F` with small connectors
   on fewer than 52 vertices) and for the two-sided reading of every failed composition.
5. **Honest exposition**: the implication ladder, the census frontier `[38, 52]`, and the audit
   results as a wiki, a manuscript on Zenodo, and a web page at release time.

Non-claims: no new counterexample is promised; no minimality theorem beyond the declared
grammar; solver output without a checked proof object is never a theorem.

## 3. Lenses (methodology 10; spine plus at least two others)

- **Spine, lens 1 (exclusion)**: DRAT-certified non-existence (of colorings, covers, low-defect
  maps) on fixed graphs.
- **Lens 4 (invariant-first)**: the Berge-Fulkerson cover of the 112-vertex graph is one SAT
  call and decides the highest-stakes question first; oddness, perfect matching index and the
  defects are single invariants.
- **Lens 2 (anatomy)**: the `P-Col` calculus of the gadgets; why `F` composes into failure.
- **Lens 3 (recognition)**: which classical cover conjectures survive on the counterexamples.
- **Lens 6 (two-sided reading)**: each colorable composition in the grammar search is a datum
  about `P-Col` closure, feeding the next composition.
- **Lens 11 (external dialogue)**: Goedgebeur et al.'s forthcoming version; every borrowed
  claim re-derived in-repo before use.
- **Lens 10 (adversarial)**: hypotheses before runs; controls on both sides; corrupted inputs
  must fail; verdicts honor machine results.

## 4. Phases and exit gates

| phase | question | exit gate |
|---|---|---|
| PC-P0 | Are sources, priority and scope pinned? | context dossier, durable records, EXP-001 declared |
| PC-P1 | Do our own encodings certify the three counterexamples and accept the controls? | EXP-001 CONFIRMED with checked proofs and passing controls |
| PC-P2 | Do the counterexamples satisfy Berge-Fulkerson, Berge, Fan-Raspaud? | EXP-002 verdict with explicit covers or checked proofs |
| PC-P3 | Do they have 5-cycle double covers and nowhere-zero 5-flows; what are oddness and resistance? | EXP-003 verdict |
| PC-P4 | Normal 6 and strong normal 6 on all three; exact normal-5 defect and P-defect | EXP-004/005 verdicts |
| PC-P5 | Manuscript and Zenodo | preprint v0.01 transcribed from verdicts, published, hash-verified |
| PC-P6 | Anatomy and grammar minimality below 52 | `P-Col` sets reproduced; bounded search decided or budget recorded |
| PC-P7 | Cyclically 5-edge-connected counterexamples (their Problem 5) | declared only if PC-P6 yields a route |

## 5. Compute discipline

- Every SAT call: DIMACS written by our encoder, CaDiCaL in WSL with binary DRAT output,
  drat-trim check, SHA-256 of CNF, proof and logs recorded in the artifact manifest.
- Per-instance wall cap 30 minutes; beyond it the row is INCONCLUSIVE, never "probably".
- Positive answers are decoded and re-verified by a standard-library checker that never reads
  the CNF.
- Heavy artifacts under `E:/_Datos/caos-research/petersen-coloring/`; manifests in the repo.

## 6. Deployment axis

No separate web deployment is created for this problem in this round; the problem page joins
the shared static site at the next serialized release (methodology 06). The manuscript is
deployed to Zenodo (source-only class for the research record itself).
