# Claim audit - manuscript v0.16

Audited: 2026-08-20. Final publication result: PASS.

Version 0.16 retains all claims through v0.15 and adds only the colon-Koszul degree-five diagonal
closed by EXP-029. The result is an all-parameter theorem for the conductor special fibers in the
explicit EXP-009 family. Finite campaigns and solver checks validate the implementation but do
not replace the integral normal form.

| manuscript claim | evidence | audit result |
|---|---|---|
| all results through the complete second Betti row | claim audits v0.05--v0.15; EXP-001--028 | PASS; attribution and inherited trust boundaries unchanged |
| exact high cubic colon | EXP-027 `proof.md`, equation `(Q_p:f_p)_1=span{X_a:a in H_p}` | PASS; `H_p={a in G_p:a>=6p}` and `|H_p|=8p` |
| complete degree-five third-syzygy profile | EXP-029 integral normal form and `proof.md` | PASS; `beta_(3,(5,b))` is the unordered distinct pair-sum count shifted by `3p` |
| characteristic independence | unit integral cancellations and primitive pair basis | PASS; relative `H_2` is free abelian in every offset |
| total `beta_(3,5)` | sum of the complete pair basis | PASS; `binom(8p,2)=4p(8p-1)` |
| exact offset support | block pair-sum coverage and unique gap | PASS; `[15p+1,39p-3] minus {33p-1}` with `24p-4` supported offsets |
| adjacent `beta_(4,5)` | EXP-024 Hilbert numerator, EXP-028 `beta_(2,5)`, and EXP-029 `beta_(3,5)` | PASS; `2p(5p-1)(10p-3)(100p^2-110p+13)/3` |
| complete internal-degree-five diagonal | minimal-shift bound plus the preceding three entries | PASS; nonzero only in homological degrees two, three, and four |
| exact computational support | EXP-029 `results.json`, `audit.json`, and `symbolic-certificate.json` | PASS; 297 formula rows, exact small profiles, two-field control, independent boundary ranks, and arithmetic/Z3 endpoint checks |
| failed-attempt handling | `attempt-1-symbolic-budget.json` and verdict | PASS; first materialized-support implementation is `INCONCLUSIVE_BUDGET` and explicitly non-evidence |
| manuscript split decision | EXP-029 verdict | PASS; second full diagonal belongs in the existing narrative; a separate sequel remains deferred |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system is named |
| reserved publication identity | Zenodo draft `22029468` and page-one block | PASS before upload; version `0.16`, DOI `10.5281/zenodo.22029468`, concept DOI, date, CC-BY-4.0 licence, and sole author/ORCID agree |

## Scope boundaries

- EXP-029 concerns only the conductor special fibers in the explicit EXP-009 family.
- It completes internal degree five, not the third homological row, full Betti table, full minimal
  resolution, or a classification of Huneke--Wiegand counterexamples.
- The integral normal form proves the all-parameter and characteristic-free claim. Finite-field
  computations are controls.
- The arithmetic and Z3 checks certify support-chain and coefficient identities, not the relative
  matching itself.
- EXP-023 retains its disclosed solver trust boundary; EXP-029 freezes that premise rather than
  removing it.
- The broad conjecture was already disproved by the public seed; Son Pham retains discovery
  priority.

## Computational validation gate

- canonical EXP-029 campaign: PASS; 297 rows for `p=4,...,300` and complete exact relative `H_2`
  profiles for `p=4,5,6`;
- explicit totals: PASS; `496`, `780`, and `1128`;
- complete `p=4` profile over `GF(2)` and `GF(1000003)`: PASS;
- independent rational ranks at offsets `60` and `61`: PASS; `0` and `1`;
- first symbolic attempt: `INCONCLUSIVE_BUDGET`; preserved and excluded from evidence;
- optimized symbolic/arithmetic certificate: PASS; 11 affine interval-chain obligations and the
  coefficient identity through `p=10000`;
- campaign aggregate: `7564f15534e8a29f875a367d3a324b95041e8eef836d15deac3e35130e1ad37d`;
- audit aggregate: `337854eef5d773c84cdd79c7734e63b295fa0337c5a1852e652559c334949b04`;
- symbolic aggregate: `605733497d6fb0ead97bfd25e26daaa66d546c297751960e1c427f29ff69f279`.

## Build, render, and publication gate

- Zenodo reservation: PASS; empty draft `22029468` reserves DOI
  `10.5281/zenodo.22029468` under concept DOI `10.5281/zenodo.21763582`;
- stable two-pass DOI-bearing build: PASS; 36 pages and stable cross-references;
- warnings, undefined references, overfull boxes, and underfull boxes: PASS; none in the final log;
- complete rendered inspection: PASS; all 36 pages inspected at 120 DPI in six contact sheets, with
  full-resolution checks of the title/DOI block and theorem/proof/reproducibility pages 31--34; no
  clipping, overlap, unreadable formulas, broken tables, or missing running headers;
- exact PDF identity: PASS; 691,569 bytes, MD5
  `ad69991f41c4f35da3c03f2c1ce343e9`, and SHA-256
  `4c2a49ae6e1a959afb8df4a365feb4c815d408f3746b5ef1df14ee5746abd554`;
- authenticated post-upload metadata, sole-authorship, and one-file gate: PASS; exactly one PDF,
  exact filename, 691,569 bytes, MD5, version, title, sole creator, ORCID, CC-BY-4.0 licence, and
  the v0.15/v0.16 description addendum matched before publication;
- Zenodo publication and concept-latest gate: PASS; record `22029468` is public and concept-latest
  with version `0.16` and DOI `10.5281/zenodo.22029468`;
- fresh unauthenticated download/hash verification: PASS; MD5
  `ad69991f41c4f35da3c03f2c1ce343e9` and SHA-256
  `4c2a49ae6e1a959afb8df4a365feb4c815d408f3746b5ef1df14ee5746abd554` exactly match Git.
