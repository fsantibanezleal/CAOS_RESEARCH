# Claim audit - manuscript v0.11

Audited: 2026-08-12. Final result: PASS.

Version 0.11 retains all v0.10 claims and adds only the theorem-level consequences of the
committed EXP-021 symbolic proof. Exact campaigns support the proof and do not replace it.

| manuscript claim | evidence | audit result |
|---|---|---|
| prior minimality, uniqueness, family, endomorphism, type, trace, stability, reduction, tangent-cone, Buchsbaum, and Noether-normalization results | claim audits v0.05--v0.10; EXP-001--020 | PASS; scope and attribution unchanged |
| `T_p^2=m_pT_p` and all higher identities | EXP-021 block proof using EXP-009/013/016 exact value profiles | PASS; monomial value sets agree and associativity gives every `n>=1` |
| natural graded-algebra isomorphism `G_p/H^0 isomorphic to F(T_p)` | degree-zero kernel `m_p/T_p=H^0` from EXP-019; positive-degree kernels vanish by the square identity | PASS; this is a natural ring quotient, not only equality of Hilbert series |
| Cohen--Macaulay special fiber and exact free shifts | EXP-019 quotient Cohen--Macaulayness plus EXP-020 free module, transported through the natural isomorphism | PASS; confined to the explicit conductor family |
| Artinian h-vector and socle vector `(0,0,10p,0,1)` | EXP-021 closed offset blocks and multiplication witnesses | PASS; type is `10p+1`, with socle in two degrees |
| neither level nor Gorenstein | socle occurs in degrees two and four and has dimension greater than one | PASS |
| computational support through `p=300` | EXP-021 `results.json`, `audit.json`, direct value-product route and closed-form route | PASS; 297/297 optimized rows pass; campaign `38578775...a95b`, audit `17794070...0a9c` |
| preserved first budget attempt | EXP-021 `attempt-1-budget.txt` and verdict | PASS; reported as `INCONCLUSIVE`, not mathematical failure |
| selected artifact reconstruction | independent EXP-021 audit at `p=4,5,17,73,151,300` | PASS; all selected invariants rebuilt and all 297 campaign rows rehashed |
| literature boundary | Cortadellas--Zarzuela, J. Algebra DOI `10.1016/j.jalgebra.2007.02.044` | PASS; general analytic-spread-one fiber-cone framework cited; family-specific square, quotient, and socle are proved directly |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system named |
| publication identity | public Zenodo record, page-one block, and fresh download | PASS; version DOI `10.5281/zenodo.21909961`, concept DOI `10.5281/zenodo.21763582`, sole author/ORCID, and public SHA-256 match Git |

## Scope boundaries

- EXP-021 concerns only the conductor ideals in the explicit EXP-009 family.
- It does not classify arbitrary conductors, fiber cones, analytic-spread-one ideals, modules, or
  one-dimensional Gorenstein domains.
- The finite campaign validates reproducibility; the infinite theorem rests on the symbolic block,
  natural-kernel, and socle proofs.
- The broad Huneke--Wiegand conjecture was already disproved by the public seed; discovery priority
  remains Son Pham's.
- A defining ideal for the fiber cone remains open and is not implied by the module decomposition.

## Build and rendered-document gate

- final stable two-pass MiKTeX `pdflatex`: PASS;
- stable-pass warning/reference/box audit: PASS; zero warnings, undefined references, overfull
  boxes, or underfull boxes;
- complete 25-page render at 150 DPI: PASS; every page was inspected in five contact sheets, with
  full-resolution checks of the title/DOI block, preceding module theorem, new fiber-cone theorem
  and proof, experiment aggregates, scope/open-question page, and bibliography;
- visual defects: none; formulas, hashes, references, headers, and page numbers are legible with
  no clipping or overlap;
- frozen candidate PDF: 589,535 bytes, MD5 `1ad22a6a87c0c6a5a80f8a913d06ca95`, SHA-256
  `0b3a9131e3c419c0a89cb064ea6beb7c696006171fe18bec578e7ba963a520ce`;
- public record status, concept latest, sole author/ORCID, CC-BY-4.0 licence, filename, hashes, and
  fresh downloaded-file equality: PASS.
