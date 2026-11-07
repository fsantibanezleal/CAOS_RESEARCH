# Bougard-Joret backlog

| ID | Status | Work / decision |
|---|---|---|
| BJB-001 | done | Review all 20 portfolio rows and choose a precise novelty target |
| BJB-002 | done | Prove adjacent exceptional strip and characterize every extremal, EXP-001 |
| BJB-003 | done | Independent proof audit and exact finite certificate with negative controls |
| BJB-004 | done | Five-page v0.01 published and byte-verified; 61 tests pass; research PR #248 and management PR #608 merged to develop |
| BJB-005 | done | Full first interior shell value, all alpha-two extremizers, 75 exact constructions and complete order-six control census; integrated with BJB-008 |
| BJB-006 | open | Determine when different maximum independent sets yield different tree representations |
| BJB-007 | recorded handoff | Owning unsplittable-flow round should reconcile August two-sided disproof and external lower bounds from the portfolio audit |
| BJB-008 | done | Ten-page v0.02 published and byte-verified at DOI 10.5281/zenodo.22341644; 100 tests and current-head CI pass; research PR #251 merged at 8055fec, private PR #611 at a6d642fd |
| BJB-009 | open | Classify all first-shell extremizers beyond alpha two and the tree strip |
| BJB-010 | deferred after source comparison | Initial second-shell search selected the stronger published next-matching target in EXP-003; the general second shell remains open |
| BJB-011 | done | Extend the same-day portfolio review; verify AEY final sources, BET construction and Table 3, including the unresolved 184-to-185 interval at $(13,14)$ |
| BJB-012 | done | EXP-003 proves $T(d,d+1)=d^2+d+2$ for all $d\ge7$; new uniform upper bound, known BET construction; $T(13,14)=184$; independent audits PASS |
| BJB-013 | done | Seven-page next-matching v0.01 published at DOI 10.5281/zenodo.22343022; 352,871 bytes and latest version verified, all-page QA/no LaTeX warnings, 101 tests passed; scoped PR integration complete through research PR #255 and private mirror PR #613; first-shell v0.02 preserved |
| BJB-014 | done | EXP-004: $f(2d+3,2,d+2)=d^2+4d+2$ for every $d\ge7$; every fixed-order maximizer has a $K_{2,d}$; independent audit PASS; next-matching v0.04 published (10.5281/zenodo.23965193) |
| BJB-015 | open | Extend the triangle-free matching upper bound beyond the solved $m=d+1$ level; no full AEY conjecture claim |
| BJB-016 | done | EXP-005 (2026-11-06): the second-regime formula t(n,alpha)+ceil(k*alpha/2) holds exactly at the seven smallest open triples (10,3,3)=17, (11,3,3)=20, (13,4,3)=21, (14,4,3)=24, (15,4,3)=27, (13,3,4)=28, (14,3,4)=32, by complete enumeration (nauty geng + exact filter); open window beyond them (alpha=3,k=5; alpha=4,k=4; alpha=5,k=3) not computed |
| BJB-017 | done | EXP-006 and EXP-007 (2026-11-07): the second-regime formula t(n,alpha)+ceil(k*alpha/2) holds at all 39 triples of the open window with n <= 22 (EXP-005: 7, EXP-006: 4, EXP-007: 28), by complete enumeration with an independence-pruned generator; note `second-regime` v0.01 |
| BJB-018 | todo | Extend the open-window computation past order 22 (EXP-007 pipeline; the per-edge-count cost grows fastest for large k, (22,3,7) at E = 80 took 1,331 s) |

Neither the tree strip, the full first shell nor the EXP-003 bracket resolves the general revised Bougard-Joret problem. The next-matching theorem settles one full level of the AEY conjecture; the full conjecture remains open. The [new review](../../problems/combinatorics/bougard-joret/context/2026-09-05-next-matching-review.md) extends the September 5 portfolio refresh covering all 13 unstarted and seven active rows. The [proof](../../problems/combinatorics/bougard-joret/experiments/EXP-003-triangle-free-next-matching/proof.md) and exact receipts own the research claims. The separate manuscript is [published](https://doi.org/10.5281/zenodo.22343022), with [public-byte verification complete](../../manuscripts/bougard-joret/next-matching/publication-verification.json); scoped integration is complete through research PR #255 and private mirror PR #613.
