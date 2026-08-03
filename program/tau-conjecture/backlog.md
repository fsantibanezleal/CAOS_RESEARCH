# tau-conjecture: problem backlog

| id | title | status | priority | notes |
|---|---|---|---|---|
| TCB-001 | EXP-001: polynomial census z_max(tau) for small tau + integer regression gate vs Markstroem | done | P0 | 2026-08-01 CONFIRMED: gate 14/14; z_max(1..4) = 1,2,3,3 |
| TCB-015 | EXP-002: census at tau = 5; decide minimal tau with z_max = 4 | done | P0 | 2026-08-01 CONFIRMED: z_max(5) = 4; minimal tau = 5; DOS/Chebyshev-shadow mechanism found |
| TCB-016 | RL-4 first lemma: iterated x^2 - 2 factory over Z | done | P1 | 2026-08-01 PROVED: periodic points {2,-1}; towers stall at {0,+-1,+-2}; context derivation note + tclib tests |
| TCB-017 | N_2 valuation-spectrum record hunt (RL-2) | todo | P2 | Digit ladders (V9) now measured through tau=7 (EXP-007); spectrum-record hunt still open |
| TCB-018 | Dual set-function T(S) structure lemmas (RL-3): union/translation/scaling/reflection costs; T table from census data | todo | P2 | |
| TCB-002 | Read Shub-Smale 1995 (Duke) in full; transcribe the exact theorem statements and proof route | blocked | P1 | 2026-08-01 access attempt failed (Project Euclid paywall; author page TLS broken); statement triply confirmed (Rojas Def 1 + survey + Koiran); needs a library credential |
| TCB-003 | Read Rojas math/0304100 in full; pin the two weak versions + the 2-adic bound constants | done | P1 | 2026-08-01 read in full (round 2); constants pinned in references.md; feeds TC-P3 co-census |
| TCB-004 | Read Cheng 2004 + Cheng 2003 + Strassen 1976/77; pin the upper-bound ladder for tau'(n!) | todo | P1 | Upper bounds quoted via Markstroem |
| TCB-005 | Canonicalization lemmas (sign/reflection orbit quotient, dominated-state pruning; proofs first) or compiled backend | todo | P0 | Depth 6 was decided WITHOUT it (last-gate scan); now the blocker for depth 7 (depth-6 frontier ~20M states). sympy cross-check DONE 2026-08-01 (284/284) |
| TCB-006 | Integer census extension past Markstroem length 11 (checkpointed DFS; then GPU/multiprocess) | todo | P2 | Includes monotonicity probe for his Problem 2.1 |
| TCB-007 | Witness anatomy: classify record mechanisms per tau; candidate infinite families + per-family rate lemmas | todo | P2 | Anatomy lens; two-sided reading of the census |
| TCB-008 | Read KPT15 + Hrubes 2013 + Dutta 2021; real/SoS variant bounds transcription | todo | P2 | Reformulation lens |
| TCB-009 | Read Lipton 1994 + Shamir 1979; factoring bridge page for the wiki | todo | P2 | Also the division-model contrast |
| TCB-010 | PosSLP adjacency survey (Allender et al. 2009; arXiv:2307.08008, 2403.00115) | todo | P3 | Dictionary lens; decision-side twin |
| TCB-011 | Wiki pages 01-05 (statement/history; implication ladder; census; mechanisms; open questions) | todo | P2 | Vertical: each page lands with the round that produces its content |
| TCB-012 | Manuscript (replication-first) | done | P3 | Superseded by TCB-022: census paper published 2026-08-01 |
| TCB-013 | Web problem page + baked census artifacts | todo | P3 | Publication gate (methodology 06) at release |
| TCB-014 | ECCC TR19-142 (IPS / tau) read; proof-complexity bridge note | todo | P3 | |
| TCB-019 | EXP-004: z_max(7) | done | P0 | 2026-08-01 CONFIRMED: z_max(7) = 5, bottom law breaks; frontier 25,844,905 states exact; done WITHOUT canonicalization (interned engine + last-gate scan) |
| TCB-020 | Generalize the stall lemma to monic inner maps | done | P2 | 2026-08-01 PROVED (monic stall theorem note + spot-check); EXP-005 measured the x^2-c family: loophole empty |
| TCB-021 | Close the [8,9] window for 6 roots | done | P0 | 2026-08-02 EXP-006: min tau(6 roots) = 8 EXACTLY (408 witnesses, 3 replay-verified); our emptiness prediction refuted; shipped as paper v0.02 (DOI 10.5281/zenodo.21763182) |
| TCB-025 | Re-scan with full hit retention | done | P1 | 2026-08-02 EXP-007: max union = 6: NO 8-gate 7-rooter via final x; 408 anchor reproduced |
| TCB-026 | Anatomy pass: punctured five-rooters | done | P2 | 2026-08-02 EXP-007: two-center DOS products x^2(x^2-1)(x-2)(x-4); the hole is the second center |
| TCB-022 | Manuscript gate assessment + paper | done | P1 | 2026-08-01 PUBLISHED: census paper v0.01, DOI 10.5281/zenodo.21753439 (concept .21753438) |
| TCB-023 | Narkiewicz read: pin the classical cycle-length <= 2 attribution | todo | P2 | Cited [MV] in EXP-005 verdict with our own [D] proof |
| TCB-024 | Doyle-Poonen read (V8 import gate) | todo | P2 | Before any uniform-boundedness import |
| TCB-027 | Mod-p instrumentation: root counts of census records over F_p vs the Frobenius ceiling (V10) | todo | P2 | Cheap add-on to the census catalog; pairs with the V9 digit ladders |
| TCB-028 | Paper v0.03 (deliberate): seven-rooter exclusion + digit ladders + punctured anatomy + V10 narrative; ship WITH the z_max(8) resolution | todo | P1 | R3 discipline: no reflexive publish |
| TCB-029 | SAT lane EXP: the final-pm 8-gate case (z_max(8) = 6? 7-rooter at 8?) per the 2026-08-02 design note | todo | P0 | The single remaining unknown at depth 8 |
| TCB-030 | Evaluation-matrix instrumentation (V11): entry-growth measurements on record matrices; Mahler/height trade-off lemma target | todo | P2 | Context note 2026-08-03 |
