# Claim audit - manuscript v0.17

Audited: 2026-08-20. Release status: PRE-PUBLICATION QA.

Version 0.17 retains all claims through v0.16 and adds only the complete cubic-colon and
degree-six third-syzygy theorem closed by EXP-030. The result is an all-parameter theorem for the
conductor special fibers in the explicit EXP-009 family. Finite campaigns validate the
implementations but do not replace the canonical-idealization and integral normal-form proofs.

| manuscript claim | evidence | audit result |
|---|---|---|
| all results through internal degree five | claim audits v0.05--v0.16; EXP-001--029 | PASS; attribution and inherited trust boundaries unchanged |
| complete cubic colon | EXP-030 `proof.md` and the EXP-027 linear-colon premise | PASS; `Q_p:f_p=Q_p+(X_h:h in H_p)` and `|H_p|=8p` |
| canonical idealization | EXP-030 normal forms | PASS; `P_p/(Q_p:f_p)` is `V_p semidirect omega_(V_p)` |
| Hilbert series and Gorenstein property | canonical idealization and degree-by-degree normal forms | PASS; `(1+(2p-2)z+z^2)/(1-z)^2` and dimension two |
| complete degree-six third-syzygy profile | multigraded Hilbert numerator and EXP-030 integral relative normal form | PASS; coefficient formula `s_p+eta_p r_p` |
| characteristic independence | unit integral cancellations and primitive unmatched labels | PASS; relative `H_2` is free abelian in every offset |
| total `beta_(3,6)` | exact coefficient sum | PASS; `8p(7p^2-12p+2)/3` |
| exact offset support | symbolic interval expansion | PASS; `[3p+4,29p-5] minus ([6p-3,6p+1] union [9p-3,9p])` |
| exact computational support | EXP-030 `results.json`, `audit.json`, and `symbolic-certificate.json` | PASS; 297 formula rows, exact small profiles, two-field control, independent coefficients/ranks, and symbolic identities |
| failed-attempt handling | `attempt-1-audit-encoding.json` and verdict | PASS; the implementation that inserted offset `8p-1` is `INVALID_IMPLEMENTATION` and explicitly non-evidence |
| manuscript split decision | EXP-030 verdict | PASS; this adjacent strand belongs in the existing homological narrative; a separate sequel remains deferred |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system is named |
| reserved publication identity | Zenodo draft `22030167` and page-one block | PASS before upload; version `0.17`, DOI `10.5281/zenodo.22030167`, concept DOI, date, CC-BY-4.0 licence, and sole author/ORCID agree |

## Scope boundaries

- EXP-030 concerns only the conductor special fibers in the explicit EXP-009 family.
- It determines `beta_(3,6)`, not `beta_(3,7)`, the complete third homological row, the full Betti
  table, the full minimal resolution, or a classification of Huneke--Wiegand counterexamples.
- The integral normal form proves the all-parameter and characteristic-free claim. Finite-field
  computations are controls.
- The symbolic certificate checks scalar and support identities, not the relative matching itself.
- EXP-023 retains its disclosed solver trust boundary; EXP-030 freezes that premise rather than
  removing it.
- The broad conjecture was already disproved by the public seed; Son Pham retains discovery
  priority.

## Computational validation gate

- canonical EXP-030 campaign: PASS; 297 formula rows for `p=4,...,300` and complete exact relative
  `H_2` profiles for `p=4,5,6`;
- explicit totals: PASS; `704`, `1560`, and `2912`;
- complete `p=4` profile over `GF(2)` and `GF(1000003)`: PASS;
- corrected independent idealization-Hilbert audit: PASS; all coefficients for `p=4,5,6` and
  rational ranks at the selected `p=4` offsets agree;
- first independent audit: `INVALID_IMPLEMENTATION`; preserved and excluded from evidence because
  it incorrectly inserted the forbidden offset `8p-1`;
- symbolic certificate: PASS; exact scalar/support identities for `p=4,...,25,50,100,300`;
- campaign aggregate: `de439ff5cf0784b332fcf811b17217579221afca42510f755963c81ff8beaa4d`;
- audit aggregate: `bf5034efc37ec23edbd60d87c1eca36d437a9f9fc1e9d38f59816d8a7d3a7a16`;
- symbolic aggregate: `c519356b98ea0c76ec3d49d5f04e3512f711e601fa6491a8bf28dd337454968c`.

## Build, render, and publication gate

- Zenodo reservation: PASS; the explicit PID-reservation response for draft `22030167` returned DOI
  `10.5281/zenodo.22030167` under concept DOI `10.5281/zenodo.21763582` at
  `2026-08-20T13:41:08Z`;
- stable two-pass DOI-bearing build: PASS; 40 pages and stable cross-references;
- warnings, undefined references, overfull boxes, and underfull boxes: PASS; none in the final log;
- complete rendered inspection: PASS; all 40 pages inspected at 120 DPI in five contact sheets,
  with full-resolution checks of the title/DOI block and theorem/proof/reproducibility pages
  34--38; an absorbed-spacing-command defect found on the first theorem render was corrected and
  pages 34--36 were rebuilt and rechecked at 150 DPI; no clipping, overlap, unreadable formulas,
  broken tables, or missing running headers remain;
- exact PDF identity: PASS; 714,021 bytes, MD5 `4c7daffba7539f37ea4ecb6d52fad9d9`, and
  SHA-256 `480f135b9ecf8dbcec0fb91e85491f8fcf11e1e3c7417f6415ebeda366b5d640`;
- sole-human-authorship gate: PASS; the PDF title page and metadata name only Felipe
  Santibanez-Leal, and the ORCID is `0000-0002-0150-3246`;
- authenticated upload and exact draft validation: PENDING;
- Zenodo publication, concept-latest, and fresh unauthenticated download verification: PENDING.
