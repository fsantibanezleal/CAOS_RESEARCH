# Claim audit - manuscript v0.05

Audited: 2026-08-12. Final result: PASS.

The symbolic proofs carry the infinite statements. Exact campaigns validate implementations and
boundaries; they do not substitute for the proofs.

| manuscript claim | evidence | audit result |
|---|---|---|
| public seed and discovery priority | source dossier; EXP-001; public candidate record | PASS; Son Pham is credited with the first public counterexample |
| Frobenius minimum `181` in the stated class | EXP-005 verdict and checked lower certificates | PASS; no arbitrary-module claim |
| unique normalized pair at `F=181` | EXP-007 verdict and terminal proof audit | PASS; minimum layer only |
| counterexample family for every `p>=4` | EXP-009 proof and verdict | PASS; deductive interval identities are load-bearing |
| exact `Lambda_p` and its invariants | EXP-011 proof and verdict | PASS |
| uniform Ext/reflexivity/Tor conclusions | EXP-011; Dey-Lyle Proposition 4.1(2), Theorems 4.2-4.4 | PASS; hypotheses and contrapositives explicit |
| `PF(Lambda_p)` formula, type and reduced type `10p` | EXP-012 proof and verdict; Maitra-Mukundan Theorem 2.13 and Proposition 3.7 | PASS |
| maximal reduced type and non-almost-Gorenstein completion | EXP-012 block proof and almost-symmetric identity | PASS |
| common formula `tr_R(J_p)=R_p:E_p=tr_R(E_p)` | EXP-013 proof and verdict | PASS; value-set products and conductor stability explicit |
| balanced defect `length(R/T)=length(E/R)=p+1` | EXP-013 reflected-block proof plus EXP-011 extension count | PASS |
| original trace tail prediction was refuted | EXP-013 hypothesis, preflight, history, and verdict | PASS; `13s-1` correction disclosed in text |
| EXP-012/013 campaigns through `p=300` | committed `results.json` and audits | PASS; symbolic proofs remain load-bearing |
| current trace source | Lindo-Maitra-Zhang version of record, DOI `10.1007/s13348-026-00515-0` | PASS; Corollary 5.6 and Gorenstein scope checked directly |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system named |
| publication identity | public Zenodo record, page-one block, and fresh download | PASS; version DOI `10.5281/zenodo.21907297`, concept DOI `10.5281/zenodo.21763582`; public SHA-256 matches Git |

## Scope boundaries

- The broad conjecture is already false due to the public seed.
- Minimality and uniqueness concern the normalized two-generated monomial-ideal class.
- The family results concern the explicit `Gamma_p,J_p,E_p` construction only.
- No classification of arbitrary modules, rings, counterexamples, or nearby Kunz faces is claimed.
- The v0.05 record is public only after build, render, upload, publication, and fresh-public-download
  verification all passed.

## Build and rendered-document gate

- two-pass MiKTeX `pdflatex`: PASS;
- warning, reference, and box audit: PASS; zero warnings, undefined references, overfull boxes, or
  underfull boxes in the final two passes;
- complete 15-page rendered inspection at 150 DPI: PASS; title block, equations, hashes, tables,
  references, running headers, and page numbers are legible with no clipping or overlap;
- frozen candidate PDF: 515650 bytes, MD5 `75a1102cc9dab8785ee00ba7f93012e7`, SHA-256
  `4bd2cfd7351cb6cec1b3fa006c7eb3018732c283b5bb5a1e5c86015435275276`;
- public record status, concept latest, sole author/ORCID, CC-BY-4.0 licence, filename, bytes, MD5,
  SHA-256, and fresh downloaded-file equality: PASS.
