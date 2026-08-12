# Claim audit - manuscript v0.06

Audited: 2026-08-12. Prepublication result: PASS. Public-artifact verification: PENDING.

The symbolic proofs carry the infinite statements. Exact campaigns validate implementations and
boundaries; they do not substitute for the proofs. Version 0.06 corrects the novelty description
of the balanced colength in immutable v0.05 and adds the exact conductor-stability theorem.

| manuscript claim | evidence | audit result |
|---|---|---|
| public seed and discovery priority | source dossier; EXP-001; public candidate record | PASS; Son Pham is credited with the first public counterexample |
| Frobenius minimum `181` and minimum-layer uniqueness in the stated class | EXP-005 and EXP-007 verdicts and checked certificates | PASS; no arbitrary-module claim |
| counterexample family for every `p>=4` | EXP-009 proof and verdict | PASS; deductive interval identities are load-bearing |
| exact `Lambda_p`, type and reduced type `10p` | EXP-011/012 proofs and verdicts | PASS |
| common formula `tr_R(J_p)=R_p:E_p=tr_R(E_p)` and value `p+1` | EXP-013 proof and verdict | PASS; exact ideal and evaluated colength are family-specific |
| equality `length(R/(R:E))=length(E/R)` | Herzog--Kumashiro Proposition 3.1, Claim 1 | PASS; manuscript now identifies this as general one-dimensional Gorenstein local duality, not new family-specific structure |
| conductor `T_p` is nonstable | EXP-014; Dey Corollary 3.7; EXP-012 type `10p` | PASS; finite birational, one-dimensional Gorenstein hypotheses are matched; a direct value witness is also recorded |
| exact square and defect `length(T_p^2/t^(4s)T_p)=14p` | EXP-016 symbolic proof, verdict, campaigns and audit | PASS; five residue identities and six disjoint defect blocks are load-bearing |
| original square-tail prediction was refuted | EXP-015 hypothesis and verdict; EXP-016 correction | PASS; `13s-1` failure at the first `p=4` smoke gate is disclosed and no failed campaign artifact was manufactured |
| EXP-014/016 campaigns through `p=300` | committed results and independent audit artifacts | PASS; symbolic proofs remain load-bearing |
| source identity | archived Herzog--Kumashiro and Dey PDFs | PASS; SHA-256 `4bc99c1d2054cb9eda10c25eafd94ebbac39bbbb3d27f282f0e05d45619663f9` and `0b02dc69d94d129e68235cdf4366775fc54f025d52fbf47dd918bd290c62a1c1` |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system named |
| publication identity | reserved Zenodo record and page-one block | PENDING; DOI `10.5281/zenodo.21907943` is reserved, but no public record is claimed before upload, publication, and fresh-download verification |

## Scope boundaries

- The broad conjecture is already false due to the public seed.
- Minimality and uniqueness concern the normalized two-generated monomial-ideal class.
- The family results concern only the explicit `Gamma_p,J_p,E_p,T_p` construction.
- The colength balance is general duality; only the exact common ideal and its value `p+1` are
  family-specific calculations.
- Nonstability and defect `14p` do not classify conductors of arbitrary birational extensions.
- No classification of arbitrary modules, rings, counterexamples, or nearby Kunz faces is claimed.

## Build and rendered-document gate

- two-pass MiKTeX `pdflatex`: PASS;
- warning, reference, and box audit: PASS; zero warnings, undefined references, overfull boxes, or
  underfull boxes in the final pass;
- complete 17-page rendered inspection at 150 DPI: PASS after correcting the section-13 heading;
  title block, equations, hashes, tables, references, running headers, and page numbers are legible
  with no clipping or overlap;
- frozen candidate PDF: 526699 bytes, MD5 `4ff26288ef70a875ebf3f17cb726ff16`, SHA-256
  `10cc2bd31026cfe6a921c4cf54832a7df018b0f0b0f38ee196bc597954255dd4`;
- public record status, concept latest, sole author/ORCID, CC-BY-4.0 licence, filename, hashes, and
  fresh downloaded-file equality: PENDING.
