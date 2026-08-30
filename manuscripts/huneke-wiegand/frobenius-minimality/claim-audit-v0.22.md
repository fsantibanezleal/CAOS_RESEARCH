# Claim audit - manuscript v0.22

Date: 2026-08-30. Publication status: published and fresh-download verified at DOI
`10.5281/zenodo.22177072`.

## Claim-to-evidence matrix

| claim or boundary | primary evidence | audit status |
|---|---|---|
| discovery priority | Pham public repository and recorded Huneke verification | PASS; CAOS does not claim discovery of the original counterexample |
| imported incidence structure | EXP-033/034 exact sequence, Artinian bases, and signed two-layer boundary | PASS; the EXP-035 theorem uses the frozen displayed incidence map |
| complete primitive zero-row criterion | EXP-035 proof and representation sets `R_b` | PASS; `e_F tensor v_b` is an integral zero row exactly when `R_b subset F` |
| free-summand count | direct coordinate projection and binomial superset count | PASS; every zero coordinate splits primitively and the displayed `z_(p,i)` formula counts all of them |
| consecutive kernel family | exact interval partition for `b=10p+t` | PASS for every `p>=4` and `2<=t<=p-2`; homological degrees are `p+1,...,2p-3` |
| proposed P3 mechanism | persisted ten-term integral low Koszul cycle | REFUTED as declared; the selected coordinate is reached by the connecting image |
| complete first target | all 79 kernel rows, 119 boundary columns, and 710 source columns | PASS; no selected submatrix or coordinate quotient is substituted |
| characteristic dependence in `K_4` | exact finite-field ranks and integral Smith form | PASS; dimensions are five over `GF(2)` and four over `GF(3)`, with cokernel `Z^4 direct-sum Z/2Z` |
| characteristic dependence in `A_4` | block-matrix rank identity and complete connecting image | PASS; `beta_(5,(7,87))(A_4)` is four over `GF(2)` and three over `GF(3)` |
| transfer to `C_4` | EXP-033 minimal cubic cone and shifted-offset exclusion | PASS; the smallest four-high-variable source offset is 102, above the required 75 |
| independent validation | semigroup-derived reconstruction, reversed pivots, four fields, and symbolic exclusions | PASS; bases, ranks, Smith profile, and nine interval obligations agree |
| scope | EXP-035 verdict and manuscript scope section | PASS; one characteristic-dependent cell is proved, not complete lower strands or all-parameter torsion |
| manuscript split decision | EXP-035 preflight and verdict | PASS; the theorem directly extends the lower-strand narrative of v0.21 and remains coherent in the main paper |
| publication identity | Zenodo record `22177072`, metadata JSON, and page-one block | PASS; version, DOI, concept DOI, date, CC BY 4.0, sole author, and sole ORCID agree |

## Evidence identities

- zero-row classification aggregate:
  `cc98154e60bdc00fe1f503020aa7d5c66b53ff0cc4ce2158f199d03c2a5fda8b`;
- complete-target artifact SHA-256:
  `4072a9fb7844d07763fae1b08e99da3d94d38cf3a40f980316c38f0931091276`;
- independent artifact SHA-256:
  `b92e787bc120b5fa12aac1fc4a10792883e699ed7315055958f3916e8d10b60b`;
- symbolic artifact SHA-256:
  `b1bfc105f3e9ace368f181ccf10f367fe1f4d23199e49c14275bd8e9b941569e`.

## Proof boundary

The zero-row classification and explicit consecutive family are deductive for every `p>=4`.
Finite computation validates bases, interval partitions, controls, and implementation but is not
extrapolated into the proof. The declared coordinatewise P3 mechanism is explicitly refuted.

The characteristic-dependent theorem is an exact complete calculation in the single target
`(p,t)=(4,2)`. The canonical route includes every row and column, the independent route rebuilds
the Artinian bases from numerical-semigroup ideal powers and reverses elimination order, and
integral Smith form identifies the factor two. No extension of this torsion statement to `p>4`,
no complete lower strand, and no full special-fiber resolution is claimed.

## Publication gates

- claim-to-evidence, attribution, split, and scope audit: PASS;
- two consecutive stable LaTeX builds: PASS; no LaTeX/package warnings, unresolved references,
  overfull boxes, or underfull boxes in either retained v0.22 log;
- PDF metadata, extraction, page count, hashes, and all-page rendered inspection: PASS; all 51
  pages inspected at 150 DPI, with full-size inspection of page one and theorem pages 45--46;
  810,905 bytes, MD5 `5ed2409d6688b30147963a7293598440`, SHA-256
  `3868f511a047073c9d7bedf25e026f1aaf3a5ab2c05c45d03614675ef6bdf5c2`;
- sole-author and sole-ORCID audit: PASS; Felipe Santibanez-Leal is the sole author and
  `0000-0002-0150-3246` is the sole ORCID; no machine authorship or coauthorship appears;
- repository tests, pipeline, and artifact consistency: PASS; template, content, research
  structure, and local-path guards pass, Ruff passes the CI scope, all 60 tests pass, the full
  registry pipeline completes, and all manifest/artifact pairs are consistent;
- exact Zenodo metadata and one-file upload validation: PASS; before publication, draft
  `22177072` was at version `0.22` with the expected title and date, sole creator and ORCID,
  CC BY 4.0, and exactly one completed file named
  `huneke-wiegand-frobenius-minimality-v0.22.pdf`, with 810,905 bytes and MD5
  `5ed2409d6688b30147963a7293598440`;
- publication, concept-latest check, and fresh unauthenticated download: PASS; record `22177072`
  is public and concept-latest at version `0.22`; its title, DOI, concept DOI, date, sole creator
  and ORCID, CC BY 4.0 license, filename, bytes, and MD5 agree, and a fresh unauthenticated
  download matches the committed PDF by MD5 and SHA-256.

All manuscript publication gates pass. The immutable v0.22 artifact proves the all-parameter
primitive zero-row theorem and one characteristic-dependent multigraded cell at `p=4`. It does
not claim complete lower strands, explicit differential matrices, all-parameter torsion, or the
full special-fiber resolution.
