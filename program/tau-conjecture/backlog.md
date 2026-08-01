# tau-conjecture: problem backlog

| id | title | status | priority | notes |
|---|---|---|---|---|
| TCB-001 | EXP-001: polynomial census z_max(tau) for small tau + integer regression gate vs Markstroem | done | P0 | 2026-08-01 CONFIRMED: gate 14/14; z_max(1..4) = 1,2,3,3 |
| TCB-015 | EXP-002: census at tau = 5; decide minimal tau with z_max = 4 | done | P0 | 2026-08-01 CONFIRMED: z_max(5) = 4; minimal tau = 5; DOS/Chebyshev-shadow mechanism found |
| TCB-016 | RL-4 first lemma: iterated x^2 - 2 factory over Z (how many iterations keep all roots integral; gate cost per doubling) | todo | P1 | Concrete question minted by EXP-002's mechanism discovery |
| TCB-017 | N_2 valuation-spectrum record hunt (RL-2): measured growth vs Rojas' [s, s(s+1)/2] window | todo | P2 | First observation: depth-5 records all have spectra {0,1} |
| TCB-018 | Dual set-function T(S) structure lemmas (RL-3): union/translation/scaling/reflection costs; T table from census data | todo | P2 | |
| TCB-002 | Read Shub-Smale 1995 (Duke) in full; transcribe the exact theorem statements and proof route | todo | P0 | The origin paper; currently cited via Buergisser 2024 survey |
| TCB-003 | Read Rojas math/0304100 in full; pin the two weak versions + the 2-adic bound constants | todo | P1 | Feeds the additive-complexity co-census (TC-P3) |
| TCB-004 | Read Cheng 2004 + Cheng 2003 + Strassen 1976/77; pin the upper-bound ladder for tau'(n!) | todo | P1 | Upper bounds quoted via Markstroem |
| TCB-005 | Canonicalization lemmas for polynomial SLP enumeration (normalization, sign symmetry, value-multiset dedup soundness) + sympy cross-check of the poly layer | todo | P0 | Now the DECLARED PREREQUISITE for the depth-6 census (EXP-002 verdict); naive depth 6 ~25M state-ops |
| TCB-006 | Integer census extension past Markstroem length 11 (checkpointed DFS; then GPU/multiprocess) | todo | P2 | Includes monotonicity probe for his Problem 2.1 |
| TCB-007 | Witness anatomy: classify record mechanisms per tau; candidate infinite families + per-family rate lemmas | todo | P2 | Anatomy lens; two-sided reading of the census |
| TCB-008 | Read KPT15 + Hrubes 2013 + Dutta 2021; real/SoS variant bounds transcription | todo | P2 | Reformulation lens |
| TCB-009 | Read Lipton 1994 + Shamir 1979; factoring bridge page for the wiki | todo | P2 | Also the division-model contrast |
| TCB-010 | PosSLP adjacency survey (Allender et al. 2009; arXiv:2307.08008, 2403.00115) | todo | P3 | Dictionary lens; decision-side twin |
| TCB-011 | Wiki pages 01-05 (statement/history; implication ladder; census; mechanisms; open questions) | todo | P2 | Vertical: each page lands with the round that produces its content |
| TCB-012 | Manuscript (replication-first: census + Markstroem extension) per methodology 09 | todo | P3 | Gate: enough validated + novel material |
| TCB-013 | Web problem page + baked census artifacts | todo | P3 | Publication gate (methodology 06) at release |
| TCB-014 | ECCC TR19-142 (IPS / tau) read; proof-complexity bridge note | todo | P3 | |
