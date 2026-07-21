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
| JCB-025 | The uniform (2,n) theorem attempt: one symbolic pass over all completion degrees n (same discriminant variety; family-shaped inverse) | P5 | todo | 2026-07-21 | would close the whole (2,n) column at once |
| JCB-022 | EXP-014 Puiseux escape obstructions for planar Keller maps | P5 | todo | 2026-07-21 | hypothesis design ready in log |
| JCB-023 | EXP-015 checker + bridge extractor | P5 | done | 2026-07-21 | shipped, pytest/CI-permanent |
| JCB-024 | EXP-016 done: cascade verified from primary sources; NEW: extract an explicit failing Hessian-nilpotent quartic | P4 | doing | 2026-07-21 | flags lifted |
