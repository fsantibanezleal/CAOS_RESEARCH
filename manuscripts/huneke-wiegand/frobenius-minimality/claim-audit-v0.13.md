# Claim audit - manuscript v0.13

Audited: 2026-08-18. Final publication result: PASS.

Version 0.13 retains all v0.12 claims and adds only the homological edge results closed by
EXP-024. It corrects the stale v0.12 suggestion that presentation-ring regularity was open, while
leaving the interior Betti table, explicit Groebner bases, and primary decomposition open.

| manuscript claim | evidence | audit result |
|---|---|---|
| prior minimality, uniqueness, family, endomorphism, type, trace, stability, reduction, tangent-cone, Buchsbaum, Noether-normalization, special-fiber, and defining-ideal results | claim audits v0.05--v0.12; EXP-001--023 | PASS; scope, attribution, and EXP-023 solver boundary unchanged |
| `pd_(P_p)(F_p)=10p-1` | EXP-021 Cohen--Macaulay dimension one; `P_p` has `10p` variables; Auslander--Buchsbaum | PASS |
| `reg_(P_p)(F_p)=4` | EXP-021 exact degree-four h-polynomial and Cohen--Macaulayness; intrinsic/presentation-ring regularity identity | PASS; removed from open questions |
| alternating Betti polynomial `(1-z)^(10p-1)h_p(z)` | Hilbert series of the minimal graded `P_p`-resolution | PASS; explicitly does not identify all individual interior Betti numbers |
| `beta_(2,3)=2p(500p^2-330p+31)/3` | coefficient of `z^3` plus EXP-023 `beta_(1,3)=1`; independent degree-three dimension count | PASS; two symbolic derivations agree |
| complete last row `beta_(c,c+2)=10p`, `beta_(c,c+4)=1` | regular linear reduction to EXP-021 Artinian algebra; top Koszul homology equals socle | PASS; all other last-row entries vanish |
| `beta_(c-1,c+3)=8p` | regularity-four vanishing, zero degree-three socle, and coefficient of `z^(c+3)` | PASS |
| canonical-module generators: `10p` in degree `-1`, one in degree `-3` | graded dual of the last free module in `Ext^c(-,P_p(-10p))` | PASS |
| computational support | EXP-024 `results.json`, checkpoint, and `audit.json` | PASS; campaign `p=4,...,300`, every row independently rebuilt, selected source artifacts reconstructed |
| imported premise identity | frozen hashes of EXP-021/023 results, audits, proofs, and symbolic certificate | PASS; corrupted hash control rejected |
| adversarial scope | EXP-024 controls | PASS; false regularity/projective dimension/Betti entries and full-table overclaim rejected |
| manuscript split decision | EXP-024 preflight and verdict | PASS; same manuscript is coherent; split deferred to a standalone Groebner/full-resolution/primary-decomposition theorem |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system named |
| publication identity | public Zenodo record `21995498`, page-one block, and fresh download | PASS; version `0.13`, DOI `10.5281/zenodo.21995498`, concept DOI, date, CC-BY-4.0 licence, sole author/ORCID, filename, size, MD5, and SHA-256 agree |

## Scope boundaries

- EXP-024 concerns only the conductor special fibers in the explicit EXP-009 family.
- It determines homological edges, not the full resolution or an explicit Groebner basis.
- Its proof is deductive from EXP-021/023; a defect in those premises would propagate.
- EXP-023's exact Z3 UNSAT leaves still lack separately checked proof objects.
- The broad conjecture was already disproved by the public seed; Son Pham retains discovery
  priority.

## Build and rendered-document gate

- stable two-pass `pdflatex`: PASS; a repeated source-identical build retained 29 pages and the
  same rendered layout (container bytes vary with the build timestamp);
- warnings, undefined references, overfull boxes, and underfull boxes: PASS; none in the final
  log;
- complete 150-DPI rendered inspection: PASS; all 29 pages inspected in five contact sheets, with
  full-resolution checks of the title/DOI block, theorem pages 25--26, and trust/scope page 27;
- visual defects: none; formulas, long hashes, table rules, links, headers, footers, and page
  numbers are legible with no clipping, overlap, or stranded heading;
- sole-authorship, ORCID, version, DOI, concept DOI, and licence: PASS before build;
- frozen candidate PDF: 635,617 bytes, MD5 `d6ce72589100d1f57986da000501fdc7`, SHA-256
  `cc9e721c3f0155181b963095a0b0efcc37e023546b32c6dd61b772a3d30ec7ed`;
- Zenodo publication: PASS; record `21995498` is public and concept latest, with the sole human
  author and ORCID, CC-BY-4.0 licence, exact filename, and 635,617-byte file.
- Fresh unauthenticated download: PASS; MD5 `d6ce72589100d1f57986da000501fdc7` and SHA-256
  `cc9e721c3f0155181b963095a0b0efcc37e023546b32c6dd61b772a3d30ec7ed` exactly match Git.
