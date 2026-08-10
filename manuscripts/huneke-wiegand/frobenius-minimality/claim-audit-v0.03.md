# Claim audit - manuscript v0.03

Audited: 2026-08-10. Result: PASS.

This audit treats experiment verdicts and their committed artifacts as the evidence sources. The
finite campaign supports, but does not prove, the infinite statement.

| manuscript claim | evidence | audit result |
|---|---|---|
| public seed and discovery priority | source dossier; EXP-001; public candidate record | PASS; Son Pham is credited with the first public counterexample |
| independent colon reproduction | EXP-001 verdict | PASS; described as reproduction, not discovery |
| exact endomorphism-overring anatomy | EXP-002 verdict | PASS |
| complete `F<69` reproduction | EXP-004 verdict and manifest | PASS |
| Frobenius minimum `181` in the stated class | EXP-005 verdict and checked lower certificates | PASS; no claim about arbitrary modules or domains |
| unique normalized pair at `F=181` | EXP-007 verdict and terminal proof audit | PASS; explicitly limited to the minimum layer |
| Route K has two certified negative and eleven non-seed positive parameters | EXP-006 overall verdict and Route K audit | PASS; no recurrence inferred from finite SAT models |
| first fixed-width interval ray fails uniformly | EXP-008 verdict and residue-7 proof | PASS |
| family formula for every integer `p>=4` | EXP-009 hypothesis, `proof.md`, verdict, and independent audit | PASS; theorem is derived from interval identities and layer/tail proof |
| invariants `m=24p`, `F=78p-1`, conductor `78p`, embedding dimension `11p` | EXP-009 symbolic proof and generation audit | PASS |
| ideal `(t^(24p),t^(30p))` is nonprincipal and rigid | EXP-009 symbolic `D=E+E` proof and full-window/tail checks | PASS |
| finite sweep through `p=300` and boundary failures | EXP-009 `results.json` | PASS; aggregate `81d5a8eb6cf2e848807323e3b0bdba58c464779d25cdc788cef027585540dce2` |
| independently reconstructed positive hashes and semantic samples | EXP-009 `audit.py` and `audit.json` | PASS; aggregate `eb2aaf17650ed99f4e220a43c53bdd8835c82688a37567bb154c30a1ae520ce9` |
| generalized-arithmetic positive family does not contain the seed or EXP-009 family | manuscript derivations; EXP-009 proof | PASS; stated as exclusion from one positive class, not all variants |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is the sole author; no automated system is named |
| publication identity | public Zenodo v0.03 record and downloaded file | PASS; concept `10.5281/zenodo.21763582`, version `10.5281/zenodo.21873911`; public SHA-256 matches Git |

## Narrative boundaries

- The original conjecture is already false because of the public seed.
- CAOS claims a separate infinite family only in symmetric numerical semigroup rings with
  two-generated monomial ideals.
- The paper does not classify all counterexamples, arbitrary modules, arbitrary one-dimensional
  Gorenstein domains, all Route K models, or global minima for multiplicity/embedding dimension.
- Professor Huneke's verification is external evidence, not peer review or authorship.
- EXP-010 is not cited as evidence because it was superseded without a run.

## Build and rendered-document gate

- two-pass MiKTeX `pdflatex`: PASS;
- LaTeX/package warnings, undefined references, overfull/underfull boxes: zero;
- complete 11-page PNG inspection at 150 DPI: PASS;
- title, author/ORCID, preprint label, CC BY 4.0, concept DOI, version DOI, headers,
  page numbers, equations, tables, references, and scope language: PASS.
- public record status, concept latest, author/ORCID, licence, filename, bytes, MD5, SHA-256, and
  downloaded-file comparison: PASS.
