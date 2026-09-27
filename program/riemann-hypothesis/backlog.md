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
| RH-026 | Export replay v9, integrate EXP-010 into the public workbench, and complete a serialized release with rendered QA | open | P1 |
| RH-027 | Prove a general-`Q`, uniform-shift short-window mollified moment for `nu<min{(3theta-1)/4,3/8}`. Re-scoped 2026-09-27: Steuding proves the `T^(1/3+eps)M^(4/3)` error only for degree-one `Q`, fixed shifts, `nu<3/8`, orders at most two; `(3theta-1)/4` is inferred, not stated. A new theorem, gated on RH-030 and RH-031; engines Ishikawa-Matsumoto or Tang arXiv:2608.14852 | open, gated | P1 |
| RH-028 | Localized two-piece (Feng-type) mollifier to raise `kappa/nu` above `0.7173`. Narrowed 2026-09-27: a same-length piece should inherit the localized Young off-diagonal, so the gain is main-term only. Decide first by benchmarking the `0.7170` slope against the variational construction of arXiv:2508.11108; close if the gain is below 1% | open, benchmark first | P2 |
| RH-029 | Proof hygiene: record in EXP-005/008 that the rectangle-sign detour defect is paid by the discarded Littlewood contribution of on-line detector zeros | open | P2 |
| RH-030 | Primary-source gate for the 2026-09-27 sweep: quote with versions Wang 2609.07918 (curve, threshold, support), the Steuding 2002 statement, Tang 2608.14852 admissible range, the small-`nu` slope of 2508.11108, the attribution passage of Lamzouri 2609.02882v2, and current versions of the tracked preprints. No `[S]` input enters a declaration before this | open; arXiv and Springer unreachable from the 2026-09-27 cloud session, sources must be added to `context/source-cache/` | P0 |
| RH-031 | Value of information for RH-027: minimal degree of `Q` and resulting proportion at `theta` in `{0.505,0.51,0.52,0.534}` at `nu=min{(3theta-1)/4,3/8}`. Invariant first: reproduce Steuding's `0.552` and `0.591` with `Q(x)=1-x`; if that fails, suspend RH-027 | planned | P1 |
| RH-032 | Cohn-Elkies admissibility without RH: can the Lamzouri/Weil-form framework absorb kernels with `r-hat<=0` beyond the support, i.e. an unconditional substitute for `F>=0` there? Invariant first: reproduce `0.67250`, `0.6727`, `0.6792` at support 1 and the `0.55019` threshold, and resolve the Cheer-Goldston discrepancy. Global stake about `+0.0067`; onset stake about `0.0015` | planned | P1 |
| RH-033 | Wang's spectral term `Delta_K` inside EXP-010: show that the program's stability refinement dominates it, or add it. Invariant first: reproduce `delta_0=6.66624e-8` at support 1 | planned | P2 |
| RH-034 | Moment LP over multiplicity distributions containing the EXP-006 product as its Cauchy-Schwarz instance; price the short-window `sum m^2` or three-level input needed for onset `0.52`. Invariant first: reproduce `0.5458838` | planned | P3 |
| RH-035 | Written closure of the Karatsuba/Selberg route below `theta=1/2`: `simple>=(c-(Q-1)/6)N` needs an odd-order critical proportion above about 17-19% | planned | P4 |
| RH-036 | Replay Zhu arXiv:2608.24827 (`lambda_min(0.8)`) in interval arithmetic, then test a Landau-Widom degrees-of-freedom barrier for Gram-type detectors near `theta=1/2` | planned | P4 |
| RH-037 | Records hygiene before RH-026: reference item 28 title (done 2026-09-27); `frontend/src/data/citations.ts` still carries the old title; describe EXP-009's constant as `2.9e-8` above Wang's printed `C_0+delta_0`; record the Yang density-one retraction beside the 79.62% quarantine; journal metadata for 2511.20059 | open | P1 |

The 2026-09-27 literature and representation sweep
([dossier](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-literature-and-representation-sweep.md))
found no external result above the EXP-009 constant or the EXP-010 onset. It
re-scoped RH-027 and RH-028 and added RH-030 to RH-037. Dispatch order:
RH-030, then the invariant-first computations RH-031 and RH-032; RH-027 is
attempted only if RH-031 shows that a partial extension would move the onset.
