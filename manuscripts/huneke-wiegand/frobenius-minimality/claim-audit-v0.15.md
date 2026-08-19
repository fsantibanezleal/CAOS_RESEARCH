# Claim audit - manuscript v0.15

Audited: 2026-08-19. Final publication result: PASS.

Version 0.15 retains all claims through v0.14 and adds only the complete second Betti row closed by
EXP-028. The result is an all-parameter theorem for the explicit EXP-009 family; finite campaigns
are validation controls and do not replace the integral argument.

| manuscript claim | evidence | audit result |
|---|---|---|
| all results through the first interior strand | claim audits v0.05--v0.14; EXP-001--027 | PASS; attribution and inherited trust boundaries unchanged |
| degree-five support | EXP-028 relative-chain analysis and `proof.md` | PASS; exactly `[3p+2,5p-2]`, `[6p+1,8p-3]`, and `[9p,11p-4]` |
| outer multiplicity profile | integral lexicographic matching and pair-sum count | PASS; `min(floor(r/2)+1,floor((2p-4-r)/2)+1)` |
| middle multiplicity profile | two adjacent pair-sum diagonals after integral cancellation | PASS; `min(r+1,2p-3-r,p-2)` |
| `beta_(2,5)=p(2p-3)` | sums of the two outer profiles and the middle profile | PASS; `binom(p,2)+p(p-2)+binom(p,2)` |
| `beta_(2,6)=0` | degree-six integral interval matching | PASS; every edge receives a distinct unit-pivot triangle |
| complete second Betti row | EXP-013/027 inherited entries plus EXP-028 tail | PASS; `beta_(2,3)=2p(500p^2-330p+31)/3`, `beta_(2,4)=8p`, `beta_(2,5)=p(2p-3)`, `beta_(2,6)=0`, and zero otherwise |
| characteristic independence | integral matching and unit Smith normal forms | PASS; integral first homology is free in degree five and zero in degree six |
| exact computational support | EXP-028 `results.json`, `audit.json`, and `symbolic_certificate.json` | PASS; 297 formula rows, complete small profiles, two-field controls, independent rational/Smith audit, and arithmetic/Z3 certificate |
| manuscript split decision | EXP-028 hypothesis and verdict | PASS; completing one row is integrated into the existing paper; a separate sequel is deferred until a higher-row theorem gives a distinct narrative |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system is named |
| publication identity | reserved Zenodo draft `22016550` and page-one block | PASS before upload; version `0.15`, DOI `10.5281/zenodo.22016550`, concept DOI, date, CC-BY-4.0 licence, and sole author/ORCID agree |

## Scope boundaries

- EXP-028 concerns only the conductor special fibers in the explicit EXP-009 family.
- It completes the second Betti row, not the full Betti table, the full minimal resolution, or a
  classification of Huneke--Wiegand counterexamples.
- The integral matching and Smith-form argument are the characteristic-free proof; finite-field
  computations are controls.
- The arithmetic and Z3 checks test endpoint and counting identities. They are not substitutes for
  the all-parameter interval proof.
- The broad conjecture was already disproved by the public seed; Son Pham retains discovery
  priority.

## Computational validation gate

- canonical EXP-028 campaign: PASS; 297 rows for `p=4,...,300`, complete degree-five profiles for
  `p=4,5,6`, degree-six all-offset validation at `p=4`, and GF(2)/GF(1000003) agreement;
- explicit degree-five totals: PASS; `20`, `35`, and `54` at `p=4,5,6`;
- independent SymPy rational-rank and Smith route: PASS;
- symbolic/arithmetic certificate: PASS; five Z3 obligations and direct identities through
  `p=10000`;
- campaign aggregate: `45f08e6a15e321512629fa4b6ab07161ddcc766ddf56e1d9579175f3444ec32f`.

## Build, render, and publication gate

- pre-reservation candidate: PASS; 34 pages, 673,957 bytes, MD5
  `de2187791c9a9de43bcf59842891d128`, SHA-256
  `e2a69d80392071ef2ff199dac9b90e23fc49292a8b0cb8476d22f54ad3775f61`;
- Zenodo reservation: PASS; empty draft `22016550` reserves DOI
  `10.5281/zenodo.22016550` under concept DOI `10.5281/zenodo.21763582`;
- DOI-bearing stable two-pass build: PASS; 34 pages, 674,169 bytes, MD5
  `204eb3575d1bebcd95eb25f48bae58cb`, and SHA-256
  `e7d3fb747f01b6c44c84ca9c2cf25a746cd2d05eb0996163f4a18e9e3cea1be9`;
- warnings, undefined references, overfull boxes, and underfull boxes: PASS; none in the final log;
- complete rendered inspection: PASS; all 34 pages inspected at 120 DPI in six contact sheets, with
  full-resolution checks of the title/DOI block, theorem and proof pages 29--31, and bibliography
  page 34; no clipping, overlap, unreadable formulas, or stranded headings;
- authenticated post-upload draft gate: PASS; exactly one committed PDF, exact filename, 674,169
  bytes, MD5, version, title, sole creator, ORCID, and v0.15 description addendum matched before
  publication;
- Zenodo publication and concept-latest gate: PASS; record `22016550` is public and concept-latest,
  with v0.15, sole human author/ORCID, CC-BY-4.0 licence, and exact filename, size, and MD5;
- fresh unauthenticated download/hash verification: PASS; MD5
  `204eb3575d1bebcd95eb25f48bae58cb` and SHA-256
  `e7d3fb747f01b6c44c84ca9c2cf25a746cd2d05eb0996163f4a18e9e3cea1be9` exactly match Git.
