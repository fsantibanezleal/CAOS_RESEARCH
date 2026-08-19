# Claim audit - manuscript v0.14

Audited: 2026-08-19. Pre-publication result: PASS; Zenodo identity pending.

Version 0.14 retains all v0.13 claims and adds only the first interior Betti strand closed by
EXP-027. It corrects the stale v0.13 statement that the entire interior table was open while
explicitly leaving every other unresolved interior entry open.

| manuscript claim | evidence | audit result |
|---|---|---|
| all results through the homological edges | claim audits v0.05--v0.13; EXP-001--024 | PASS; attribution and inherited trust boundaries unchanged |
| relative-chain formula for `beta_(i,b)` | direct multigraded Koszul-chain identification; Bruns--Herzog squarefree-divisor-complex framework | PASS; derived over the integers before base change |
| integral upper bound and support | EXP-027 lexicographic unit matching on the relative chain complex | PASS; one unmatched integral cycle exactly on each stated offset |
| exact colon `(Q_p:f_p)_1` | EXP-027 semigroup-difference test, explicit high quadratic paths, and low parity obstruction | PASS; high variables and only high variables occur |
| minimal mapping-cone lower bound | cubic generator outside `Q_p` and the exact linear colon | PASS; entries have positive degree, hence no cancellation |
| `beta_(2,4)=8p` with complete multiplicity-free support | matching upper bound plus mapping-cone lower bound | PASS; support is the eight stated intervals/singletons |
| characteristic independence | integral chain matching and primitive unmatched generators | PASS; relative `H_1` is free of rank one on support and zero elsewhere |
| `beta_(3,4)=p(5p-1)(500p^2-440p+47)/2` | degree-four coefficient of the Hilbert numerator using the now-known adjacent entries | PASS; integer-valued for every integer `p` |
| quadratic ideal linearly presented through the first nonlinear position | `beta_(2,4)(P_p/Q_p)=0` from the relative matching | PASS; no claim is made about later strands |
| exact computational support | EXP-027 `results.json`, `symbolic_certificate.json`, and independently encoded `audit.json` | PASS; 297 parameters, all offsets for `p=4,5,6`, two fields at `p=4`, and six symbolic UNSAT obligations |
| manuscript split decision | EXP-027 hypothesis and verdict | PASS; this strand directly extends v0.13, while a standalone manuscript remains deferred until a substantial part of the remaining table is determined |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system is named |
| publication identity | version 0.14 title block and Zenodo draft | PENDING; version DOI will be inserted before upload and publication |

## Scope boundaries

- EXP-027 concerns only the conductor special fibers in the explicit EXP-009 family.
- It determines the first interior strand, not the full Betti table or full minimal resolution.
- The integral matching is the characteristic-free proof; finite-field computations are controls.
- The six symbolic UNSAT results have no separately checked solver proof objects and are not used
  as substitutes for the deductive interval arguments.
- The broad conjecture was already disproved by the public seed; Son Pham retains discovery
  priority.

## Build and rendered-document gate

- stable two-pass `pdflatex`: PASS; 31 pages;
- warnings, undefined references, overfull boxes, and underfull boxes: PASS; none in the final log;
- complete 120-DPI rendered inspection: PASS; all 31 pages inspected in six contact sheets, with
  focused checks of the title block, theorem pages 27--29, and bibliography page 31;
- visual defects: none; formulas, interval display, matching table, links, headers, footers, and
  page numbers are legible with no clipping, overlap, or stranded heading;
- sole-authorship, ORCID, candidate version, concept DOI, and licence: PASS;
- pre-reservation candidate PDF: 31 pages, SHA-256
  `fe35b5360faf23d345d1771838c8ef81f584a46b64abd736d090d1139b51296e`;
- Zenodo reservation, DOI-bearing final build, upload, publication, and fresh public-download
  verification: PENDING.
