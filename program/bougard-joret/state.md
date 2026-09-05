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
