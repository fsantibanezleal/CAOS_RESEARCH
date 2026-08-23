# tau-conjecture: problem backlog

| id | title | status | priority | notes |
|---|---|---|---|---|
| TCB-001 | EXP-001: polynomial census z_max(tau) for small tau + integer regression gate vs Markstroem | done | P0 | 2026-08-01 CONFIRMED: gate 14/14; z_max(1..4) = 1,2,3,3 |
| TCB-015 | EXP-002: census at tau = 5; decide minimal tau with z_max = 4 | done | P0 | 2026-08-01 CONFIRMED: z_max(5) = 4; minimal tau = 5; DOS/Chebyshev-shadow mechanism found |
| TCB-016 | RL-4 first lemma: iterated x^2 - 2 factory over Z | done | P1 | 2026-08-01 PROVED: periodic points {2,-1}; towers stall at {0,+-1,+-2}; context derivation note + tclib tests |
| TCB-017 | N_2 valuation-spectrum record hunt (RL-2) | todo | P2 | Digit ladders (V9) now measured through tau=7 (EXP-007); spectrum-record hunt still open |
| TCB-018 | Dual set-function T(S) structure lemmas (RL-3) | done | P2 | 2026-08-19 note: anti-monotonicity, union+1, translation+1, reflection+1 PROVED; scaling recorded OPEN (TCB-031); exact T table through size 6 |
| TCB-002 | Read Shub-Smale 1995 (Duke) in full; transcribe the exact theorem statements and proof route | blocked | P1 | 2026-08-01 access attempt failed (Project Euclid paywall; author page TLS broken); statement triply confirmed (Rojas Def 1 + survey + Koiran); needs a library credential |
| TCB-003 | Read Rojas math/0304100 in full; pin the two weak versions + the 2-adic bound constants | done | P1 | 2026-08-01 read in full (round 2); constants pinned in references.md; feeds TC-P3 co-census |
| TCB-004 | Read Cheng 2004 + Cheng 2003 + Strassen 1976/77; pin the upper-bound ladder for tau'(n!) | todo | P1 | Upper bounds quoted via Markstroem |
| TCB-005 | Depth-8 backend | done | P0 | 2026-08-20 EXP-011: out-of-core pipeline (validate/build7/scan8, all known-answer-gated); depth-7 frontier built in full (1,048,460,912); z_max(8) = 6 |
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
| TCB-024 | Doyle-Poonen read (V8 import gate) | done | P2 | 2026-08-20 abstract read: function-field strong uniform boundedness for z^d+c; over number fields only for bounded eventual period. VERDICT: no unconditional constant for our tower question, so no import; our stall theorems remain self-contained. |
| TCB-027 | Mod-p instrumentation: root counts of census records over F_p vs the Frobenius ceiling (V10) | todo | P2 | Cheap add-on to the census catalog; pairs with the V9 digit ladders |
| TCB-028 | Paper v0.03 | done | P1 | 2026-08-20 PUBLISHED with the z_max(8) resolution: DOI 10.5281/zenodo.22035884 (concept unchanged) |
| TCB-029 | The final-pm 8-gate residual | subsumed | P0 | 2026-08-20: EXP-010 (QF_BV) also engine-bound at known-answer scale: the solver lane is CLOSED (both backends, semantics proven, search intractable); the residual is decided by EXP-011 scan8 (all-gate, unconditional) |
| TCB-030 | Evaluation-matrix instrumentation (V11): entry-growth measurements on record matrices; Mahler/height trade-off lemma target | todo | P2 | Context note 2026-08-03 |
| TCB-031 | The scaling gap: bounds for T(2S) vs T(S) (no elementary substitution exists) | todo | P2 | Minted by the RL-3 note; concrete first case: T({0,+-2,+-4}) |
| TCB-032 | The {9,10} window for 7 roots: construction hunt (corrected cost model), then depth-9 feasibility memo | todo | P1 | Depth-9 build needs ~1 TB scratch |
| TCB-033 | Digit + mod-p ladders at depth 8, replayed from the stored frontier asset | todo | P2 | Frontier at E:/_Datos/caos-research/tau-conjecture/ |
