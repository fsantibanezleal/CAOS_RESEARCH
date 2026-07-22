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
| JCB-021 | DONE (EXP-039): (3,4) top forced to a perfect cube (elimination + GL2 orbits), cube stratum inverts 4/4; (3,n) column classically covered (gcd in {1,3}); staged elimination replaced by the top-force argument | P5 | done | 2026-07-22 | the machine loop validated at (2,3)..(2,5), (3,3), (3,4) |
| JCB-025 | The uniform (2,n) theorem | P5 | done | 2026-07-21 | EXP-021: min degree <= 2 closed uniformly with one inverse formula |
| JCB-026 | Quasi-triangular at (3,3) cube case: DONE (EXP-022: alignment forced; closure for any f; descent inverter runs) | P5 | done | 2026-07-21 | remaining (3,n) strata folded into JCB-027 |
| JCB-027 | Primitive stratum first contact: DONE (EXP-023: (4, <= 6) window empty on the sampled slice, +8 by one descent step; controls non-vacuous) | P5 | done | 2026-07-21 | ladder continues as JCB-028 |
| JCB-028 | DONE (EXP-040): pure slice = Theorem 1 corollary; below-weight slices = Theorem 2 corollaries; 4-subset sweep clean (105 solves); above-weight residue owned by JCB-038 | P5 | done | 2026-07-22 | closed by subsumption |
| JCB-030 | CLOSED-RECALIBRATED (EXP-040 + literature dossier): gcd 9/12/18 certificates are replications INSIDE the verified floor (gcd <= 8 interval, B >= 16 Heitmann, B = 16 or B > 20 GGV); superseded by JCB-040 | P5 | done | 2026-07-22 | honest relabel |
| JCB-032 | DONE (EXP-029): the closed form is the weight-class banded system; THEOREM: x + a x^u y^v (u >= 2, v >= 1, a != 0) is never a Keller component at any degree; beyond-floor certified at degree 135 | P5 | done | 2026-07-21 | retires the pure-slice window program |
| JCB-033 | DONE (EXP-036): annihilation in closed form (sources = L(P^{k-1} m) live in the image; the covector kills the image; window criterion retrodicts the old artifacts). Theorems 2-4 UNCONDITIONAL | P4 | done | 2026-07-22 | the derived gap is closed |
| JCB-034 | Same-edge frontier: DONE (EXP-032, THEOREM 3: every x-anchored edge falls, any coefficient pattern) | P5 | done | 2026-07-22 | subsumes Theorems 1-2 leading forms |
| JCB-035 | Opening moves DONE (EXP-033: k = 0 and m = 0 edges fall; THEOREM 4 vertex dichotomy: vertex-x components are EXACTLY x + f(y)) | P5 | done | 2026-07-22 | the dichotomy stands |
| JCB-036 | Rotate-descent IMPLEMENTED and validated (EXP-034: whole library linearizes, 0-6 steps); the induction's limit stated: mixed-corner tops are the hard-shape stop | P5 | done | 2026-07-22 | the induction is mechanized for linear-base tops |
| JCB-037 | Corner structure DONE (EXP-035): the corner operator is diagonal, kernel = powers of B, a pure corner cannot carry the constant. The core moved to the staircase | P5 | done | 2026-07-22 | the corner is clean |
| JCB-038 | Staircase transport: instrument (EXP-037) + THEOREM 5 WINDOW FORM (EXP-042: cleared all-parameter certificates, monomial pairings, window law -c_N a^N; annihilation transfers). REMAINING: the transport chain closed form = Theorem 5 all-degree (route N1) | P5 | doing | 2026-07-22 | one step left |
| JCB-039 | DONE (EXP-038): matched-pair law exact; NO added obstruction depth; halves window unknowns: kept as an instrument for wide scans | P4 | done | 2026-07-22 | tool, not a route |
| JCB-031 | Literature pass DONE (context/2026-07-22-literature-pass-dossier.md): Moh six configurations transcribed; similarity exact form (vdE 10.2.1); floor = max >= 125 or (72,108); novelty verdicts T1/T2/rigidity NOT FOUND, T3/T4 partial; six UNVERIFIED items carried in the dossier | P3 | done | 2026-07-22 | UNVERIFIED items listed in the dossier |
| JCB-029 | Primary sources verified: Magnus 1954 (gcd 1; year corrected), Appelgate-Onishi 1985 + Nagata (gcd prime; {1,8} u P u 2P); wiki 04 + manuscript unhedged; full-text pass optional | P3 | done | 2026-07-21 | EXP-025 part 5 |
| JCB-022 | DONE first contact (EXP-014): exact properness certificates (8/8 library); JC(2) <=> empty Jelonek set recorded; full Jelonek-set computation optional later | P5 | done | 2026-07-22 | instrument is CI-reusable |
| JCB-023 | EXP-015 checker + bridge extractor | P5 | done | 2026-07-21 | shipped, pytest/CI-permanent |
| JCB-024 | DONE (EXP-041): THE DIM-48 WITNESS: HC(48) false explicitly; f_H homogeneous HN quartic (382 Q(i) monomials); exact 2-point collision; P_star falsifies Zhao's VC explicitly; Thompson input verified in-house (index corrected 17 -> 18) | P4 | done | 2026-07-22 | first explicit witness per the verified sweep |
| JCB-040 | LIVE FRONTIER: first contact DONE (EXP-043: x^m edge operator NEW; B = 16 core = staircase transport; Theorem 4 kills the pure m = 1 shape; scoping blocks 13/22). NEXT (route N2): the (48,64) validation sweep, then open B = 16 (max > 150), then (72,108) | P5 | doing | 2026-07-22 | block-cheap per scoping |
| JCB-041 | Integration: manuscript half DONE via the session-23 SPLIT (A v0.07 / B v0.01 NEW planar / C v0.02 witness; all compile; replication labels + Magnus/Zoladek hygiene in B). REMAINING: web bake + screenshot pass (nine unbaked records); wiki 04 rewrite; FELIPE: novelty phrasing before submission | P6 | doing | 2026-07-22 | manuscript debt cleared |
| JCB-042 | Outreach (Felipe's call): report the nilpotency-index correction (17 -> 18) to the Thompson repo with our exact chain as evidence | P6 | todo | 2026-07-22 | courtesy + record |
| JCB-043 | Route M1 (NEW): import literature shape restrictions as machine window FILTERS (GGV subrectangular; GGHV lower-left chains Props 4.1-4.2; Makar-Limanov polytopes; Lee-Li vertex regions); value test = measured unknown-count reduction on the (48,64) system | P5 | todo | 2026-07-22 | routes addendum M1 |
