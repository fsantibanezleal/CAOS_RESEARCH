# Jacobian conjecture - problem backlog

| id | title | phase | status | updated | notes |
|---|---|---|---|---|---|
| JCB-001 | EXP-001 exact validation of the announced counterexample | P0 | done | 2026-07-20 | confirmed |
| JCB-002 | EXP-002 structure reverse-engineering (symmetry, z-linearity, invariant reduction, fiber identity) | P1 | done | 2026-07-20 | confirmed, exact, independent of secondary sources |
| JCB-003 | EXP-003 (v1 constructor, partially refuted) + EXP-004 constructor v2 (confirmed: general family, new counterexamples P3/P4/P5 with rational collisions) | P1 | done | 2026-07-20 | the generalization core; det = -k p(1)^2, fiber degree d+1 |
| JCB-004 | EXP-005 2D obstruction: equivariant reduction proved; one-invariant collapse proposition; no Keller slices | P5 | done | 2026-07-20 | caveats recorded; injectivity scan vacuous -> JCB-014 |
| JCB-014 | EXP-006 branch-symbolic 2D enumeration | P5 | done | 2026-07-20 | non-vacuous: 216 instances, all LINEAR + injective; EXP-010 widening queued |
| JCB-015 | EXP-007 asymptotic variety of F and P3, exact | P2 | done | 2026-07-20 | escape = multiple fiber root; explicit surface; end-to-end escape demo |
| JCB-016 | EXP-010 2D rigidity all weights | P5 | done | 2026-07-21 | THEOREM: every Gm-equivariant Keller map of C^2 is linear |
| JCB-017 | EXP-011 real fiber census | P2 | done | 2026-07-21 | 1-or-3 census, wall = discriminant, real surjectivity; viz data model ready |
| JCB-018 | Optional: Lean formalization of the rigidity theorem | P5 | todo | 2026-07-21 | hardening |
| JCB-019 | EXP-012 done (landscape; uniqueness of the m=2 mechanism); widening: (1,-2,-m) systems, m=4 lattice scan, higher-degree seeds | P3/P5 | doing | 2026-07-21 | parity law refuted; uniqueness is the finding |
| JCB-005 | Asymptotic variety / non-properness locus, exact | P2 | done | 2026-07-20 | EXP-007: A(F) = {C=0} union discriminant surface; escape = multiple fiber root |
| JCB-006 | Real-slice topology + GPU fiber-sampling viz artifacts | P2 | todo | 2026-07-20 | |
| JCB-007 | Minimality: family-internal DONE (EXP-008: degree law, F minimal, fiber floor 3, new d=5 instance); global search degrees 3..6 pending (GPU) | P3 | doing | 2026-07-20 | |
| JCB-008 | BCW/Druzkowski explicit cubic push-through | P4 | todo | 2026-07-20 | |
| JCB-009 | Consequence cascade verification from primary sources (Mathieu SU(3), GMC, Zhao, Image, Dixmier care) | P4 | todo | 2026-07-20 | |
| JCB-010 | JC(2) primary-literature deep pass (Moh, Abhyankar, Newton polygon, properness results) | P5 | todo | 2026-07-20 | |
| JCB-011 | Small-degree 2D Keller-map search (exact, then GPU-widened) | P5 | todo | 2026-07-20 | |
| JCB-012 | Novel-approach pool: other weight lattices, unipotent flows, several-t invariant rings; char-p behavior DONE (EXP-009: explicit F_ell certificates, degree < ell) | P5+ | doing | 2026-07-20 | promoted when active experiments run dry |
| JCB-013 | Wiki + SVGs + web page + manuscript chapter | P6 | doing | 2026-07-21 | web LIVE; SVG pass pending |
| JCB-020 | EXP-013 leading-form cascade (done: ray-sweep bridge certified; (2,2) exhaustive) | P5 | done | 2026-07-21 | continuation = JCB-021 |
| JCB-021 | JC(2) machine: (2,3) THEOREM (EXP-020: explicit inverse); (2,4) same consistency ideal; staged (3,4) elimination queued | P5 | doing | 2026-07-21 | the machine loop validated end to end |
| JCB-025 | The uniform (2,n) theorem | P5 | done | 2026-07-21 | EXP-021: min degree <= 2 closed uniformly with one inverse formula |
| JCB-026 | Quasi-triangular at (3,3) cube case: DONE (EXP-022: alignment forced; closure for any f; descent inverter runs) | P5 | done | 2026-07-21 | remaining (3,n) strata folded into JCB-027 |
| JCB-027 | Primitive stratum first contact: DONE (EXP-023: (4, <= 6) window empty on the sampled slice, +8 by one descent step; controls non-vacuous) | P5 | done | 2026-07-21 | ladder continues as JCB-028 |
| JCB-028 | (4,6) staged certificates: 63 slices (up to 3 lower coeffs) ALL certified empty (EXP-025); pure-slice windows <= 18 empty; E-locus closed. Remaining: 4+ coeff slices / full 8-param; closed-form all-degree certificate [C] | P5 | in-progress | 2026-07-21 | (4,*) ladder literature-covered (gcd 2); machine value = replication |
| JCB-030 | Composite-gcd frontier: FIRST CONTACT DONE (EXP-026: (18, <= 27) certified empty for all a != 0 at h = x^4 y^5; h-sweep empty; gcd-12 probe empty). gcd-12 certificate DONE (EXP-027); polygon strategy VALIDATED (EXP-028: sieve exact, (18, <= 36) certified past the divisible rung, all-degree statement [D]) | P5 | in-progress | 2026-07-21 | successor instrument: JCB-032 |
| JCB-032 | DONE (EXP-029): the closed form is the weight-class banded system; THEOREM: x + a x^u y^v (u >= 2, v >= 1, a != 0) is never a Keller component at any degree; beyond-floor certified at degree 135 | P5 | done | 2026-07-21 | retires the pure-slice window program |
| JCB-033 | Theorems 2-3 tail step: the annihilation lemma in closed form [D] (one derivation now closes both) | P4 | in-progress | 2026-07-22 | the single remaining derived gap |
| JCB-034 | Same-edge frontier: DONE (EXP-032, THEOREM 3: every x-anchored edge falls, any coefficient pattern) | P5 | done | 2026-07-22 | subsumes Theorems 1-2 leading forms |
| JCB-035 | The sharp frontier: classify completions with Y-ANCHORED tops (quasi-triangular type and conjugates): the only place components can live; JC(2) = nothing else does. Start: normalize y-anchored edges, run the mirrored class analysis, map which phi admit completions (expect: exactly the compositional/triangular family) | P5 | todo | 2026-07-22 | the endgame frame |
| JCB-031 | Sources: Abhyankar similarity + Moh 1983 + the 108-floor preprint (arXiv:2204.14178) now cited (EXP-028); REMAINING: full-text hypotheses of similarity (coordinate case, N^0 convention), Moh's six-shapes detail, rigidity novelty full pass | P3 | in-progress | 2026-07-21 | hardens the [D] all-degree statement |
| JCB-029 | Primary sources verified: Magnus 1954 (gcd 1; year corrected), Appelgate-Onishi 1985 + Nagata (gcd prime; {1,8} u P u 2P); wiki 04 + manuscript unhedged; full-text pass optional | P3 | done | 2026-07-21 | EXP-025 part 5 |
| JCB-022 | EXP-014 Puiseux escape obstructions for planar Keller maps | P5 | todo | 2026-07-21 | hypothesis design ready in log |
| JCB-023 | EXP-015 checker + bridge extractor | P5 | done | 2026-07-21 | shipped, pytest/CI-permanent |
| JCB-024 | EXP-016 done: cascade verified from primary sources; NEW: extract an explicit failing Hessian-nilpotent quartic | P4 | doing | 2026-07-21 | flags lifted |
