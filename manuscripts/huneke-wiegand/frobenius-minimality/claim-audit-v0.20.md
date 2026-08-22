# Claim audit - manuscript v0.20

Date: 2026-08-22. Publication status: published and fresh-download verified at DOI
`10.5281/zenodo.22062161`.

## Claim-to-evidence matrix

| claim or boundary | primary evidence | audit status |
|---|---|---|
| discovery priority | Pham public repository and recorded Huneke verification | PASS; CAOS does not claim discovery of the original counterexample |
| imported colon quotient | EXP-030/032 proof, verdicts, and frozen hashes | PASS; `D_p` is two-dimensional Cohen--Macaulay of regularity two with the complete stated Betti polynomial |
| colon intersection | EXP-033 proof, using regularity of `f_p` on `D_p` | PASS; `Q_p=(Q_p,f_p) intersect (Q_p:f_p)` |
| pullback and kernel Hilbert series | EXP-033 exact sequences plus EXP-024/032 Hilbert series | PASS; `H_(K_p)=(8p z+10p z^2)/(1-z)` |
| kernel regularity | EXP-026 regular element and EXP-033 Artinian reduction | PASS; `K_p` is one-dimensional Cohen--Macaulay with regularity two |
| quadratic quotient invariants | depth lemma, regularity inequality, Auslander--Buchsbaum, and terminal Hilbert coefficient | PASS; `depth(A_p)=1`, `pd(A_p)=10p-1`, `reg(A_p)=2` |
| mapping-cone minimality | strict source/target grading gap | PASS; every comparison entry has positive degree and every induced Tor map vanishes |
| complete upper strands | minimal cone plus EXP-032 colon polynomial | PASS; the regularity-three and regularity-four formulas, supports, and totals hold over every field |
| finite validation | EXP-033 canonical, independent, structural, and symbolic artifacts | PASS; all 297 parameters `p=4,...,300` agree, with stored complete strands at `p=4,5,6` |
| rejected attempts | three exact budget-stop artifacts | PASS; stops at `p=102,209,267` are retained as inconclusive non-evidence |
| scope | EXP-033 verdict and manuscript scope section | PASS; comparison-rank ambiguity is removed, but the two lower `A_p` strands and full special-fiber resolution remain open |
| manuscript split decision | EXP-033 preflight and verdict | PASS; the theorem directly continues the v0.19 cubic-colon narrative and belongs in the main manuscript |
| publication identity | Zenodo record `22062161`, metadata JSON, and page-one block | PASS; version, DOI, concept DOI, date, CC BY 4.0, sole author, and sole ORCID agree |

## Evidence identities

- canonical aggregate:
  `67bff9217c89f212916220e858ef5168abe2d64cdbd789488e0ce5f49204092a`;
- independent-audit aggregate:
  `6593291efaf092333bc42972c2f05712a151efb46f3f52ed9d28afd329585a4c`;
- symbolic aggregate:
  `58ab24887c79c3c075fdefea1f38ff2e1c1ef539490f7f52359149ed2bb1a4c8`;
- exact coefficient coverage: every `p=4,...,300`, with complete stored upper strands at
  `p=4,5,6`;
- canonical implementation SHA-256:
  `5ea4a6068aac1d22d814362b8db8ad22a39145c72d104072fb80106f418e01db`;
- independent implementation SHA-256:
  `f6f00f16b997e72d7fbdfc3b329faccc8e67350b7c2b0854332241faea4842eb`;
- symbolic implementation SHA-256:
  `0da790c2e52d1cd8542922c5a4e9badfaf628f6b4ed5909a7acded355650c820`.

## Proof boundary

The result is deductive. The finite campaigns validate the arithmetic identities, implementations,
frozen premise boundary, and adversarial controls; they do not replace the proof. The proof imports
the EXP-023/024/026/030/032 colon, Hilbert-series, regular-element, and Betti-polynomial theorems.
Within that boundary it uses ideal arithmetic, a pullback, a regular linear element, the depth and
regularity lemmas, Auslander--Buchsbaum, and graded minimality. It introduces no solver or
floating-point dependency.

The result removes every comparison-rank ambiguity from the cubic mapping cone and determines the
complete two upper regularity strands. It does not determine the two lower strands of `A_p`,
explicit differential matrices, or the full minimal resolution of the conductor special fiber.

## Publication gates

- claim-to-evidence, attribution, and scope audit: PASS;
- two consecutive stable LaTeX builds: PASS; no LaTeX/package warnings, unresolved references,
  overfull boxes, or underfull boxes in either retained v0.20 log;
- PDF metadata, extraction, page count, hashes, and all-page rendered inspection: PASS; all 45 pages
  inspected at 150 DPI, with full-size inspection of page one and pages 40--45 containing the new
  theorem, proof, trust boundary, scope, and references; 774,246 bytes, MD5
  `69f45597e879afc8fd91ca4157fb2cf3`, SHA-256
  `163a3a2fc6a5d61b6ff97e3ed1089dc3b6e9b320aa9c68ed67d2f1155362d743`;
- sole-author and sole-ORCID audit: PASS; Felipe Santibanez-Leal is the sole author and
  `0000-0002-0150-3246` is the sole ORCID; no machine authorship or coauthorship appears;
- repository tests, pipeline, and artifact consistency: PASS; template, content, and research
  structure guards pass, Ruff passes the CI scope and EXP-033 scripts, all 60 tests pass, the full
  registry pipeline completes, and all three manifest/artifact pairs are consistent;
- exact Zenodo metadata and one-file upload validation: PASS; draft `22062161` is unsubmitted at
  version `0.20`, with the expected title, one creator and ORCID, CC BY 4.0, open access, and exactly
  one completed file named `huneke-wiegand-frobenius-minimality-v0.20.pdf`, with 774,246 bytes and
  MD5 `69f45597e879afc8fd91ca4157fb2cf3`;
- publication, concept-latest check, and fresh unauthenticated download: PASS; record `22062161` is
  public and concept-latest at version `0.20`; its public title, DOI, concept DOI, sole creator and
  ORCID, CC BY 4.0 license, filename, bytes, and MD5 agree, and a fresh unauthenticated download
  matches the committed PDF by MD5 and SHA-256.

All manuscript publication gates pass. The immutable v0.20 artifact proves minimality of the cubic
mapping cone and determines both upper special-fiber Betti strands. It does not claim the two lower
quadratic-quotient strands, explicit differential matrices, or the full special-fiber resolution.
