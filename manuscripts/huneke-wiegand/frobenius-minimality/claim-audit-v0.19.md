# Claim audit - manuscript v0.19

Date: 2026-08-20. Publication status: published and fresh-download verified at DOI
`10.5281/zenodo.22031481`.

## Claim-to-evidence matrix

| claim or boundary | primary evidence | audit status |
|---|---|---|
| discovery priority | Pham public repository and recorded Huneke verification | PASS; CAOS does not claim discovery of the original counterexample |
| imported canonical idealization | EXP-030 proof, verdict, and corrected audit | PASS; `D_p` is the stated canonical idealization with h-vector `(1,2p-2,1)` |
| low resolution shape | Cohen--Macaulay Gorenstein self-duality, regularity two, no linear equations | PASS; only the linear strand and terminal `beta_(c,c+2)=1` can occur |
| linear-strand ranks | alternating Hilbert numerator `(1+cz+z^2)(1-z)^c` | PASS; coefficient extraction gives `lambda_(c,a)=c binom(c,a)-binom(c,a+1)-binom(c,a-1)` |
| positivity and symmetry | factored lambda formula and Gorenstein duality | PASS for every `1<=a<=c-1` |
| full presentation-ring table | minimal tensor product with the Koszul complex on `m=8p` disjoint killed variables | PASS; the Betti polynomial is multiplied by `(1+xz)^m` over every field |
| projective dimension and regularity | endpoints of the product polynomial | PASS; `pd=10p-2`, `reg=2`, and final shift `10p` |
| total free-module rank | endpoint-separated binomial sum and evaluation at `(x,z)=(1,1)` | PASS; low total `(c-2)2^c+4`, full total `2^m((c-2)2^c+4)` |
| finite validation | EXP-032 canonical, independent, and symbolic artifacts | PASS; all 297 parameters `p=4,...,300` agree and complete tables are stored at `p=4,5,6` |
| rejected attempts | two budget artifacts plus recorded Hilbert, serialization, and CAS defects | PASS; each is retained or disclosed as non-evidence and excluded from the final aggregates |
| scope | EXP-032 verdict and manuscript scope section | PASS; free-module ranks and shifts are complete, but differential matrices and the full resolution of `C_p` remain open |
| manuscript split decision | EXP-032 preflight and verdict | PASS; this theorem completes the existing cubic-colon narrative and belongs in the main manuscript rather than a third paper |
| reserved publication identity | Zenodo draft `22031481`, metadata JSON, and page-one block | PASS; version, DOI, concept DOI, date, CC BY 4.0, sole author, and sole ORCID agree |

## Evidence identities

- canonical aggregate:
  `907438b249b98ca9ffef689b7edb9574cdb0044cc3dd4cb52de523129f7d37ee`;
- independent-audit aggregate:
  `43635c8497dfe57904997326e983c7477e7320809cb2fee661c7933041f47b09`;
- symbolic aggregate:
  `f696390447a3ce20397d937aa73baebf23a3c5ae249d4ad1215ff48cb710a2ae`;
- exact coefficient/table coverage: every `p=4,...,300`, with complete stored tables at
  `p=4,5,6`;
- canonical implementation SHA-256:
  `274c40e9e3b1f5182a16de075bf540ece926d5433d04ef828cac631378e40a5c`;
- independent implementation SHA-256:
  `0f91ab102bde540efb347fc0c0492f79585e3f4f64db516686dc05fc5eadb209`;
- symbolic implementation SHA-256:
  `5f067ffff47b6ae08bf345f13887bb97fb11d42c96f2b44f374dba03f9c2efec`.

## Proof boundary

The all-parameter result is deductive. The finite campaigns validate the coefficient
implementations, arithmetic identities, and adversarial controls; they do not replace the proof.
The proof imports the EXP-030 canonical-idealization theorem, then uses standard graded
Gorenstein self-duality, the Hilbert numerator, and a minimal Koszul tensor product on disjoint
variables. It introduces no new solver dependency.

The result is the complete ordinary graded Betti polynomial of the cubic-colon quotient
`D_p=P_p/(Q_p:f_p)`. It determines every free-module rank and degree shift, not explicit
differential matrices and not the full minimal resolution of the conductor special fiber `C_p`.

## Prepublication gates

- claim-to-evidence and scope audit: PASS;
- two consecutive stable LaTeX builds: PASS; no LaTeX/package warnings, unresolved references,
  overfull boxes, or underfull boxes in either retained v0.19 log;
- PDF metadata, extraction, page count, and hashes: PASS; 43 pages and 741,461 bytes, MD5
  `0ddc07fc56b07490e66a9b1967c6a0d0`, SHA-256
  `ebd4d3294cf1dd6fdeccf8902e93399a6617d661dd7421d9dd260278670f3a15`;
- all-page rendered visual inspection: PASS; all 43 pages inspected at 150 DPI, with full-size
  inspection of page one and pages 38--43 containing the new theorem, proof, trust boundary,
  scope, and references;
- sole-author and ORCID audit: PASS; Felipe Santibanez-Leal is the sole author and
  `0000-0002-0150-3246` is the sole ORCID; no machine authorship or coauthorship appears;
- source standards, repository structure, Ruff, tests, full pipeline, and artifact audit: PASS;
  all guards, Ruff, 60 tests, pipeline regeneration, and manifest/artifact consistency pass;
- exact Zenodo draft metadata and one-file upload validation: PASS; draft `22031481` is still a
  draft with version `0.19`, the expected title, one creator and ORCID, CC BY 4.0, open access,
  and exactly one completed file named `huneke-wiegand-frobenius-minimality-v0.19.pdf`, with
  741,461 bytes and MD5 `0ddc07fc56b07490e66a9b1967c6a0d0`;
- publication, concept-latest check, and fresh unauthenticated download: PASS; record `22031481`
  is public and concept-latest at version `0.19`, and a new unauthenticated download matches the
  committed 741,461-byte PDF by MD5 and SHA-256.

The first attempted insertion of the v0.19 theorem lost LaTeX command backslashes during patch
transport and failed before producing a candidate PDF. The source block was replaced, and only
the subsequently stable two-pass build and rendered PDF are admitted as publication evidence.
The first file-registration request was rejected because PowerShell collapsed a one-element JSON
array; the corrected registration then exposed a local PowerShell web-client null reference before
body transfer. The registered slot remained empty until the same committed PDF was transferred
and committed through a separate HTTP client. Only the final server-reported file and checksum
gate is admitted as upload evidence.

All publication gates pass. The immutable v0.19 artifact determines the complete ordinary graded
Betti polynomial and free-module rank/shift shape of the cubic-colon quotient. It does not claim
explicit differential matrices or the full conductor-special-fiber resolution.
