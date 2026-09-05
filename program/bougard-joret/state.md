# Bougard-Joret state

| Date | From | To | Evidence |
|---|---|---|---|
| 2026-09-04 | proposed | opened | Primary source pass, scope, plan and committed EXP-001 hypothesis at 0c14bf1 |
| 2026-09-04 | opened | exploring | Deterministic exact checker and full controls run |
| 2026-09-04 | exploring | consolidating | EXP-001 uniform theorem and equality characterization survived adversarial audit; manuscript v0.01 prepared |

The broader extremal problem is open. The September 4 process closure below describes that completed round; current work is recorded in the September 5 section.

## 2026-09-04 publication

Manuscript v0.01 is public at [version DOI 10.5281/zenodo.22315252](https://doi.org/10.5281/zenodo.22315252), concept DOI 10.5281/zenodo.22315251. All 319,548 bytes match an unauthenticated fresh download; API concept-latest check passed. SHA-256: `a804014fddf8d47ae0dc3988c7b1e6a0d3619daf0a423b398724321095bbb323`. The five-page PDF was inspected on every page, with no final LaTeX warnings. All 61 tests pass. Research PR #248 is the integration gate. Global release, version and cross-problem bake remain outside this scoped round.

## 2026-09-04 integration close

Research PR #248 passed both CI jobs on head `287e4ad` and merged to develop at `25079250b2e8b3acebbdb2fb9d3865a6b4778d5b`. Management PR #608 merged at `f09d60eeafe64f2e4d1c507a23aedf0be23913ff`. BJB-004 is complete. The next research action is BJB-005, with a new committed hypothesis before computation. No detached process or pending mathematical run remains.

## 2026-09-05 full-shell continuation

EXP-002 preflight was committed at `d15f240` before implementation. The proof establishes $f(\alpha+k+1,\alpha,k)=\lceil k(\alpha+k+1)/2\rceil$ for all $k\ge3$, $2\le\alpha\le k+1$, and characterizes alpha-two extremizers as complements of unions of cycles of lengths at least five. EXP-001 remains unchanged. Refer to EXP-002's verdict for the final independent-audit disposition.

The exact certificate is PASS: 75 graphs, 45 direct checks, 36 Harary cases, 15 odd-degree-sum cases, 75 damaged-edge controls, eight cycle controls, and 32,768 order-six graphs yielding 60 extremals. These finite checks support the written universal proof.

Lifecycle remains consolidating. Manuscript v0.02 is published at DOI `10.5281/zenodo.22341644`; concept-latest and public-byte verification pass for all 343,535 bytes. All ten pages were inspected, final LaTeX warnings are absent, and the combined repository suite has 100 passing tests after integrating concurrent develop. Both complete-proof and manuscript-transcription audits pass. No global release is asserted. Navigation: [September 5 plan](plan-2026-09-05.md).

## 2026-09-05 integration close

Research PR #251 passed both CI jobs on head `be25aa4` and merged to develop at `8055fecfe0dffa30ec087a73199d7ba627fed1e7`. Private mirror PR #611 merged at `a6d642fd3457e3b8453f10e7fd336dd4b4a71e20`. BJB-005 and BJB-008 are complete. No mathematical process or publication gate remains; general conjecture work and serialized global release remain separate.

## 2026-09-05 next-matching continuation

This subsequent round follows the completed first-shell publication above. The [new source review](../../problems/combinatorics/bougard-joret/context/2026-09-05-next-matching-review.md) revisits 13 unstarted and seven active rows and selects a published triangle-free matching slice. EXP-003 preflight was committed and pushed at `f3fdda6` before computation.

[D] The [proof](../../problems/combinatorics/bougard-joret/experiments/EXP-003-triangle-free-next-matching/proof.md) establishes $T(d,d+1)=d^2+d+2$ for all integer $d\ge7$, including the sharp fixed-order bound at $2d+3$. The known attaining construction is credited to BET. The uniform upper bound settles $T(13,14)=184$, rather than 185. Direct Tutte-Berge and published AEY component-reduction arguments independently connect the fixed-order bound to arbitrary order.

[D] The secondary result is $d^2+4d+1\le f(2d+3,2,d+2)\le d^2+4d+2$. The exact endpoint is open; the raw matching extremizer has a complement cut of size $d+1$ and cannot supply the required connectivity $d+2$.

[MV] The exact and independent certificates pass: 48 graphs for $d=7,\ldots,30$, 24 rejected complement cuts, and zero survivors among 287,564 five-type candidates. The separate NetworkX audit checks matching, complement independence and full connectivity for all 48 graphs. Independent reasoning audit passed. Finite evidence supports the written universal proof.

Lifecycle: consolidating. A separate manuscript v0.01 is planned in `manuscripts/bougard-joret/next-matching/`; Zenodo publication, DOI assignment, public-byte verification and scoped integration remain pending. The published first-shell v0.02 and EXP-001/002 are preserved. The full AEY conjecture and general Bougard-Joret determination remain open. Navigation: [current plan](plan-2026-09-05-triangle-free.md).
