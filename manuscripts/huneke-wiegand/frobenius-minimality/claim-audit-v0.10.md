# Claim audit - manuscript v0.10

Audited: 2026-08-12. Final result: PASS.

Version 0.10 retains all v0.09 claims and adds only the theorem-level consequences of the
committed EXP-020 symbolic proof. Exact campaigns support the proof and do not replace it.

| manuscript claim | evidence | audit result |
|---|---|---|
| prior minimality, uniqueness, family, endomorphism, type, trace, stability, reduction, tangent-cone, and Buchsbaum results | claim audits v0.05--v0.09; EXP-001--019 | PASS; scope and attribution unchanged |
| complete graded `F_p=k[x_p]`-module decomposition of `G_p=gr_(T_p)(R_p)` | EXP-020 recursive Apery-column proof plus the EXP-017--019 power, Hilbert, and torsion theorems | PASS; free shifts and exactly `p` copies of `F_p/(x_p)` in degree zero |
| minimal graded free resolution and Betti data | structure theorem for finitely generated graded modules over the PID `k[x_p]`, applied to the explicit decomposition | PASS; `beta_(0,0)=p+1`, `beta_(0,1)=10p-1`, `beta_(0,2)=12p`, `beta_(0,3)=2p-1`, `beta_(0,4)=1`, and `beta_(1,1)=p`, with no other Betti numbers |
| projective dimension one and regularity four | direct calculation from the minimal resolution | PASS |
| top-local-cohomology `a`-invariant three | the free summand `F_p(-4)` gives the largest top-local-cohomology end degree | PASS; convention is stated explicitly and finite-length `H^0` is excluded from this `a`-invariant |
| `length(G_p/x_pG_p)=25p=e0(T_p)+I(G_p)` | reduction of every free and exponent-one torsion summand modulo `x_p`, together with EXP-017 `e0=24p` and EXP-019 `I=p` | PASS |
| computational support through `p=300` | EXP-020 `results.json`, `audit.json`, reconstruction and independently implemented closed-form routes | PASS; 297/297 parameters pass; campaign `02cf6f62...aed`, audit `c439f7e4...eac` |
| selected artifact reconstruction | EXP-020 audit at `p=4,5,17,73,151,300` | PASS; every selected row is independently reconstructed and rehashed |
| literature viewpoint | Cortadellas--Zarzuela, arXiv `0906.0911`, and J. Algebra DOI `10.1016/j.jalgebra.2007.02.044` | PASS; only the Noether-normalization module viewpoint is used; maximal-ideal-specific formulas are not imported |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system named |
| publication identity | public Zenodo record, page-one block, and fresh download | PASS; version DOI `10.5281/zenodo.21909127`, concept DOI `10.5281/zenodo.21763582`, sole author/ORCID, and public SHA-256 match Git |

## Scope boundaries

- EXP-020 concerns only the conductor filtration in the explicit EXP-009 family.
- It does not classify graded modules or tangent cones of arbitrary ideals, modules, or
  one-dimensional Gorenstein domains.
- The module decomposition is a theorem from family-specific semigroup identities plus the
  graded PID structure theorem; the finite campaign is reproducibility evidence.
- The broad Huneke--Wiegand conjecture was already disproved by the public seed; discovery priority
  remains Son Pham's.

## Build and rendered-document gate

- final stable two-pass MiKTeX `pdflatex`: PASS;
- warning, reference, and box audit: PASS; zero warnings, undefined references, overfull boxes, or
  underfull boxes in the stable pass;
- complete 22-page rendered inspection at 150 DPI: PASS; all pages were inspected, with full-size
  checks of the title page, the transition into the new section, the theorem/proof pages, the
  reproducibility and scope page, and the bibliography; formulas, hashes, references, running
  headers, and page numbers are legible without clipping or overlap;
- frozen candidate PDF: 578949 bytes, MD5 `830ae1fd2e2fbf923a86cbf575e9a841`, SHA-256
  `00a78fd8101f106724877b3fdbc933c51024a872a2b9a4f05692358b4d1a9d03`;
- public record status, concept latest, sole author/ORCID, CC-BY-4.0 licence, filename, hashes, and
  fresh downloaded-file equality: PASS.
