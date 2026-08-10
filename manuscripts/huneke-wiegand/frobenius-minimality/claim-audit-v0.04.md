# Claim audit - manuscript v0.04

Audited: 2026-08-10. Final result: PASS.

This audit treats symbolic proofs and exact experiment artifacts as the evidence sources. Finite
campaigns validate implementations and boundary behavior; they are not used as proofs of the
infinite statements.

| manuscript claim | evidence | audit result |
|---|---|---|
| public seed and discovery priority | source dossier; EXP-001; public candidate record | PASS; Son Pham is credited with the first public counterexample |
| independent seed reproduction and exact overring anatomy | EXP-001 and EXP-002 verdicts | PASS; described as reproduction and analysis, not discovery |
| complete `F<69` reproduction | EXP-004 verdict and manifest | PASS |
| Frobenius minimum `181` in the stated class | EXP-005 verdict and checked lower certificates | PASS; no claim about arbitrary modules or domains |
| unique normalized pair at `F=181` | EXP-007 verdict and terminal proof audit | PASS; explicitly limited to the minimum layer |
| first fixed-width interval ray fails uniformly | EXP-008 verdict and residue-7 proof | PASS |
| counterexample family for every integer `p>=4` | EXP-009 `proof.md`, verdict, and independent audit | PASS; theorem follows from interval identities and a layer/tail proof |
| family invariants `m=24p`, `F=78p-1`, conductor `78p`, embedding dimension `11p` | EXP-009 symbolic proof and generation audit | PASS |
| uniform formula `Lambda_p = Gamma_p union (7s+Q_p) union {13s-1}` | EXP-011 `proof.md` and verdict | PASS; derived from the exact valuation-block intersection `V_k intersect V_(k+1)` |
| overring invariants `m=24p`, `F=54p-1`, conductor `54p`, genus `38p-1`, embedding dimension `12p` | EXP-011 symbolic block counts and minimal-generator proof | PASS |
| `Lambda_p` is nonsymmetric and its semigroup ring is non-Gorenstein | EXP-011 genus calculation | PASS; `38p-1` differs from the symmetric value `27p` |
| uniform Ext, reflexivity, and Tor obstructions | EXP-011 proof; Dey-Lyle Proposition 4.1(2) and Theorems 4.2-4.4 | PASS; hypotheses and contrapositives are stated explicitly |
| EXP-011 finite sweep `p=4..300` | `results.json` | PASS; 297 rows, aggregate `e21926a689178a6c70b3b6e8319053edd0fd13f164ced9565d3b976e6159c0b0` |
| independent EXP-011 reconstruction and negative controls | `audit.py` and `audit.json` | PASS; aggregate `2ed711045ad83a3b47fb3e71d4c75ae9bfa9be1a5dd9a8c4072d5f170510343b` |
| current primary-source check | archived Dey-Lyle arXiv v2 PDF | PASS; SHA-256 `2f1521f79510ef50fb81d5f029935d5a2c9b7e4c030bc698b7e4f5caacf56fad`; cited results reread directly |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is the sole author; no automated system is named |
| publication identity | public Zenodo v0.04 record and fresh download | PASS; concept `10.5281/zenodo.21763582`, version `10.5281/zenodo.21876338`; public SHA-256 matches Git |

## Narrative boundaries

- The broad Huneke-Wiegand conjecture is already false because of the public seed.
- CAOS proves minimality and uniqueness only in the normalized two-generated monomial-ideal search
  class, plus a separate explicit family in symmetric numerical semigroup rings.
- The new theorem classifies the endomorphism overrings of that explicit family; it does not
  classify all counterexamples, arbitrary modules, or arbitrary one-dimensional Gorenstein domains.
- The computational sweep is a reproducibility and regression layer for the symbolic proof.
- Professor Huneke's verification is external evidence, not peer review or authorship.

## Build and rendered-document gate

- two-pass MiKTeX `pdflatex`: PASS;
- LaTeX/package warnings, undefined references, overfull/underfull boxes: zero;
- complete 12-page PNG inspection at 150 DPI: PASS;
- title, sole author/ORCID, preprint label, CC BY 4.0, concept DOI, reserved version DOI, running
  headers, page numbers, equations, tables, references, and scope language: PASS;
- frozen PDF: 491757 bytes, MD5 `248297d0a833ba21dce27d738a50e92f`, SHA-256
  `025cea4c59c4301ff6925cfe43353c7ac1c6cd8b4fc56a8c6d648347f418e825`;
- public record status, concept latest, sole author/ORCID, licence, filename, bytes, MD5, SHA-256,
  and independent downloaded-file comparison: PASS.
