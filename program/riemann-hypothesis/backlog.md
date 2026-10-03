# Riemann hypothesis backlog

| ID | Work | Status | Priority |
|---|---|---|---|
| RH-001 | Version-pin and archive supplied and successor primary sources with licenses and hashes | done | P0 |
| RH-002 | Audit exact theorem scope, formal assumptions, and known method barriers | done | P0 |
| RH-003 | EXP-001: independently certify baseline constants and normalization audit | done | P0 |
| RH-004 | EXP-002: prove or refute a short-interval stability gain and certify a concrete instance | done | P0 |
| RH-005 | Audit later numerical candidates and higher-moment claims without adopting their headlines | done | P1 |
| RH-006 | Complete source-backed wiki, history, reproducibility tests, and handoff | done | P0 |
| RH-007 | Manuscript and Zenodo publication if validated novelty triggers methodology 09 | done | P0 |
| RH-008 | Scoped PR promotion and serialized public replay release with rendered QA | done | P0 |
| RH-009 | EXP-003: audit odd-frame amplification, then test a bounded two-variable pressure certificate | done | P0 |

The aggregate Hilbert multiplicity-defect bound and the Montgomery-Taylor kernel optimum
are already implied by inspected prior work. Repackaging them is not a new theorem claim.

RH-008 closure: PRs #263 and #264 merged, main `08660dc`, tag `v0.64.000`, successful
Pages run 34706614866, and [live verification](release-0.64.000/live-verification.json)
of 13 byte-matched public files plus eight passing scenarios and 224 screenshots.
RH-009 is confirmed in separate Stage A/B verdicts and committed result abfa001.
The new bound is 0.419087888170111727959091183775 at theta=3/4.

| ID | Next work | Status | Priority |
|---|---|---|---|
| RH-010 | Source-complete alternative methods, including parity/multiplicity, spectral witnesses and approximation criteria | done for declared scope; dossiers and verified archive committed | P0 |
| RH-011 | Declare and adversarially test the strongest relevant alternative | done; EXP-004 confirmed in fbc4f9f with proof-review binding | P0 |
| RH-012 | Consolidate the expanded manuscript, public replay, publication and release evidence | done; v0.65.000 released and live-verified | P0 |
| RH-013 | EXP-005: localize the optimized Selberg detector and test an explicit simple-critical bound at theta=0.546 | done; theorem, exact certificate, audit and proof-review binding confirmed | P0 |
| RH-014 | Expand and publish the manuscript with EXP-005, then integrate the public replay and serialized release | done; v0.05 published and release 0.70.000 live-verified | P0 |
| RH-015 | EXP-006: test Hilbert dimension and parity compression below theta=0.5459 | done; strengthened theorem, exact certificate, audit and proof-review binding confirmed | P0 |
| RH-016 | Publish manuscript v0.06 and integrate replay v5 into the next serialized release | done; v0.06 published and release 0.71.000 live-verified | P0 |
| RH-017 | EXP-007: retain the spectral Gram defect through Hilbert-dimension parity compression and test the strict short-interval gain | done; theorem, correlated exact gain, audit and proof-review binding confirmed | P0 |
| RH-018 | Integrate EXP-007 into manuscript v0.07 and publish after rendered review | done; v0.07 published and public bytes verified | P0 |
| RH-019 | EXP-008: prove fixed-rank localization and test the source-certified rank-six onset | done; theorem, exact certificate, audit and attributed-input review confirmed | P0 |
| RH-020 | Export replay v7, integrate EXP-007/008 into the public workbench, and complete serialized release QA | done; release 0.72.000 live-verified from exact main | P0 |
| RH-021 | Independently reconstruct the rank-six coefficient matrix or obtain a source artifact that permits exact C6 replay | open | P1 |
| RH-022 | EXP-009: audit Wang's global refinement, sharpen its three-point kernel constant, and transfer the result through the parity product | done; sharp ratio theorem, exact global gain, proof review, and Zenodo preprint confirmed | P0 |
| RH-023 | Export replay v8, integrate EXP-009 into the public workbench, and complete release 0.73.000 QA | done; release 0.73.000 live-verified from exact main | P0 |
| RH-024 | EXP-010: localize Levinson's method with general `Q`, prove the distinct sign-change count, certify degree-201 detectors and move the parity onset | done; canonical certificate, independent audit, controls and two referee passes confirmed; Prediction A scope corrected to `Q(0)=1` | P0 |
| RH-025 | Deposit the `short-interval-levinson` manuscript v0.01 on Zenodo through the vault tooling and record the receipt | done; DOI 10.5281/zenodo.22984155, public bytes verified | P0 |
| RH-026 | Export replay v9, integrate EXP-010 into the public workbench, and complete a serialized release with rendered QA | done 2026-09-28: release 0.74.000 promoted (PRs #346, #347), live bytes match the exact-main build; tag and GitHub release verified 2026-10-03 at a464bdb5 (additive reconciliation receipt) | P1 |
| RH-027 | Short-window moment beyond `nu<theta-1/2` | EXP-012 inconclusive 2026-09-28: Tang's dual moment is about `sqrt(h)sqrt(T)` per pair; trivial bound gives `nu<(2/3)(theta-1/2)`, hybrid large sieve gives `theta-1/2`; target A' withdrawn. Continues as RH-038 | P1 |
| RH-028 | Second mollifier piece at short length | closed 2026-09-27: Bui-Conrey-Young piece gains below `1e-9` at `nu=0.068,0.15` ([route preflights](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-route-preflights.md)); Feng pieces not computed | P2 |
| RH-029 | Proof hygiene: record in EXP-005/008 that the rectangle-sign detour defect is paid by the discarded Littlewood contribution of on-line detector zeros | open | P2 |
| RH-030 | Primary-source gate for the 2026-09-27 sweep | done 2026-09-27: Wang 2609.07918, Steuding 1999, Tang 2608.14852, arXiv:2508.11108 and Lamzouri v2 read in full; versions current; sources pinned in `context/source-manifest-rh030.json`; see dossier section 6 | P0 |
| RH-031 | Value of information for RH-027 | done 2026-09-27: invariants reproduced (0.53396, 0.590, 0.552); Tang-type onset 0.5257, Steuding-type positive for every `theta>1/2` ([route preflights](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-route-preflights.md)) | P1 |
| RH-032 | Cohn-Elkies admissibility without RH | closed 2026-09-27: the unconditional framework sees the pair sum only as a norm with compactly supported `eta`; no sign for `F` beyond the support ([route preflights](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-route-preflights.md)) | P3 |
| RH-033 | Wang's `Delta_K` inside EXP-010 | closed 2026-09-27: vanishes with the simple count, cannot move any onset; global version dominated by EXP-009 ([route preflights](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-route-preflights.md)) | P2 |
| RH-034 | Linear Hilbert-parity refinement | closed 2026-09-28 by EXP-011 (confirmed): `Q>=2N+3O-4S` is false for the Montgomery-Taylor window (certified slack `-0.0582`), and no refinement with `beta>=2.365` holds (certified lattice ratio `2.3589`); with the EXP-010 detectors such refinements cannot reach `theta=0.532` | P1 |
| RH-035 | Route below `theta=1/2` | closed 2026-09-27: needs an explicit odd density of 8% to 36% ([route preflights](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-route-preflights.md)) | P4 |
| RH-036 | Zhu window replay | closed 2026-09-27: Galerkin upper bound `2.047e-17` at `N=20`, inside Zhu's window; no proportion channel ([route preflights](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-route-preflights.md)) | P4 |
| RH-037 | Records hygiene before RH-026 | done 2026-09-27: reference 28 and frontend citation titles, 2511.20059 journal metadata, retraction note, EXP-009 comparison wording | P1 |

The 2026-09-27 literature and representation sweep
([dossier](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-literature-and-representation-sweep.md))
found no external result above the EXP-009 constant or the EXP-010 onset. It
re-scoped RH-027 and RH-028 and added RH-030 to RH-037.
All routes RH-028 to RH-037 were worked on 2026-09-27 ([route preflights](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-route-preflights.md)).
EXP-011 closed RH-034 and EXP-012 stopped the Tang route with standard bounds
(2026-09-28). RH-026 released as 0.74.000 on 2026-09-28. Next: RH-038 (asymptotic large sieve
for the dual family).
| RH-038 | Asymptotic evaluation of the dual family for moduli `h<=T^nu` and `t`-ranges of length `T/H`, to beat `nu<theta-1/2` | preflight 2026-09-28: CIS arXiv:1808.02879 Theorem 1 covers twists up to `Q^vartheta`, `vartheta<1`, at the central point only; the dual family sits at `vartheta=1` with an extra `t`-average. Needs a hybrid (modulus and `t`) asymptotic large sieve with shifts; none located | open, research-level | P1 |

## Current continuation review 2026-10-03

The historical September sweep above is superseded for external standing
by the October dossier. RH-038 remains open, but its immediate obligation
is a complete shifted, composite-twist, signed reduction; direct use of
CIS 1808.02879 fails at the twist endpoint, while CIS 1105.1177 allows
only logarithmic heights. EXP-014/015 close uniform pointwise phase repairs,
not summed cancellation. RH-021 and RH-029 remain open integrity tasks.

| ID | Work | Status | Priority |
|---|---|---|---|
| RH-039 | Archive and audit October primary sources and external standing | done; source-manifest-20261003 and dated dossier | P0 |
| RH-040 | Optimize and cap fixed mixed-Gram parameters | done; EXP-013 confirmed, RH-F6 closed | P1 |
| RH-041 | Prove the phase-resolution obstruction and check nonzero Mobius support | done; EXP-014/015 confirmed | P1 |
| RH-042 | Integrate EXP-013--015 into a later serialized replay/workbench release | open; research records are not in live replay v9 | P2 |

## Trace-aware follow-up

| ID | Work | Status | Priority |
|---|---|---|---|
| RH-043 | Retain trace-zero energy in the clipped-block dichotomy | done; EXP-016 confirmed with a revised cap, RH-F7 closed | P1 |

RH-042 includes EXP-016 as well as EXP-013--015. The sharper block estimate
does not change RH-038's analytic target or the onset. Larger searches on
these fixed inputs are not admitted without a new uniform theorem and a
value-of-information check.

| RH-044 | Sharp retained-energy envelope and pressure transfer | declared EXP-017; issue #354; bounded secondary focus RH-F8 | P1 |
