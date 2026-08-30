# Claim audit - manuscript v0.23

Date: 2026-08-30. Publication status: reserved Zenodo new-version draft `22181972`, DOI
`10.5281/zenodo.22181972`; claim, build, render, metadata, extraction, and authorship gates pass.
Upload, publication, concept-latest, and fresh-download gates remain pending.

## Claim-to-evidence matrix

| claim or boundary | primary evidence | audit status |
|---|---|---|
| discovery priority | Pham public repository and recorded Huneke verification | PASS; CAOS does not claim discovery of the original counterexample |
| imported two-layer and connecting structure | EXP-033--035 proofs and frozen premise hashes | PASS; EXP-036 reproduces the complete `(4,2)` basis hashes and field ranks before larger cells |
| complete finite targets | EXP-036 canonical exact-sum artifacts | PASS for the complete `p<=6` triangle and targeted `(7,2)`, `(8,2)`, `(9,2)` cells; no selected submatrix is used |
| characteristic dependence | exact ranks over GF(2) and GF(3) | PASS in eight of nine displayed cells; GF(1000003) agrees with GF(3), but no theorem for every odd characteristic is claimed |
| two mechanisms | kernel, source, and combined block ranks | PASS; kernel rank defects occur at `(4,2)`, `(5,3)`, `(6,3)`, while tested `t=2` cells with `5<=p<=9` acquire dependence only in the connecting quotient |
| compact integral localization | exact unimodular cancellation and Smith form at `(4,2)` | PASS; 74 unit pivots leave a `5` by `45` residual with four zero rows and two entries `-2` |
| projective-plane recognition | traced active basis support | NOT ESTABLISHED; this deterministic reduction uses seven low variables, not the predicted six, and no universal impossibility is claimed |
| square excess formula | exact `(7,2)` target | REFUTED; `(p-3)^2` predicts 16 and the exact excess is 18 |
| quadratic excess formula | exact `(9,2)` target | REFUTED; `2p^2-17p+39` predicts 48 and the exact excess is 49 |
| cubic transfer to `C_p` | EXP-033 minimal cone plus EXP-036 offset inequality | PASS for every `p>=4`, `2<=t<=p-2`; the positive gap is at least `3(p-1)^2` |
| independent validation | semigroup bases, dynamic exact sums, reverse pivots, GF(5) control | PASS for all eight cells through `(8,2)`; the `(9,2)` route is an explicit 47.5-GB inconclusive resource stop and contributes no evidence |
| scope | EXP-036 verdict and manuscript theorem | PASS; finite characteristic dependence and all-parameter cubic absence are separated; no complete lower strand or infinite multiplicity formula is claimed |
| manuscript split decision | EXP-036 hypothesis/verdict and programme plan | PASS; this extends the existing lower-strand narrative, while a separate paper remains gated on an infinite connecting theorem or complete strand |
| publication identity | reserved Zenodo draft and manuscript page-one block | PASS at reservation; version 0.23, DOI, concept DOI, date, sole author, and sole ORCID agree |

## Evidence identities

- canonical complete triangle through `p=6`:
  `7c30e32740b27f8b41343246b7ea9da7e7270f35485cd0ec623778ea081fe365`;
- targeted `(7,2)` and `(8,2)`:
  `4773020bc77ff92777f067368c3169a80ef2c693b05d7f7e6693d3271716711f`;
- targeted `(9,2)`:
  `a59286a01def0b9314e79c70218efb8eb29b1aad586d2b7b8df1792df9509009`;
- independent `p<=6` and `p=7,8` audits:
  `36c8c8b62fa81aa465fef63c9e10ba5bb8b74764c9790f4612eaf16565f47672` and
  `99b1089fb1edcd770d2e90ed746b841768dbfb9fde6dde63b0819c0271690381`;
- compact localization:
  `8906751aaa2df6014c127808bf667aae81d6daccbf7a484526af01c77480109b`, with transform certificate
  `1cd41f70abb13e79eb6cb3687134ddcdf4ddd0f69129803d799f7653710ece36`;
- symbolic and cross-artifact certificate:
  `79f3156ee542a7c224fe0bf5e47fab6dcb1ce5bb4b09a2e002d156aebfd7e7b7`.

## Proof boundary

The cubic-source absence is deductive for the entire declared family. The complete-target ranks
are exact only for the nine displayed cells. Agreement between GF(3) and GF(1000003) is an
adversarial control, not proof of equality in every odd characteristic. The failed square and
quadratic formulas remain explicit negative controls.

The canonical `(9,2)` calculation is complete and exact over all three declared fields. Its
independent dynamic-sum route was stopped before any rank after crossing the resource boundary;
the preserved stop is not used to support the theorem. Independent basis/hash/rank agreement is
complete through `(8,2)`.

## Publication gates

- claim-to-evidence, attribution, split, and scope audit: PASS;
- two consecutive stable LaTeX builds: PASS; retained passes 3 and 4 contain no LaTeX/package
  warnings, unresolved references, overfull boxes, or underfull boxes;
- PDF metadata, extraction, page count, hashes, and all-page rendered inspection: PASS; all 53
  pages were rendered at 150 DPI and inspected, with full-size inspection of page one and pages
  46--51; 824,114 bytes, MD5 `6bcacfa265e840f40e89dcdb87b75f7b`, SHA-256
  `c77b08a3724db90b14039c2c88e98325403ef4f656f52137057a27eb6fa5072d`;
- sole-author and sole-ORCID audit: PASS; PDF metadata names only Felipe Santibanez-Leal, and the
  source/PDF author block contains only ORCID `0000-0002-0150-3246`; no machine authorship or
  coauthorship appears;
- repository tests, pipeline, and artifact consistency: PASS; `python -m ruff check data-pipeline
  tests`, `python -m pytest -q` (60 passed), `python -m researchlab.pipeline all`, and the artifact,
  template-residue, content-standards, and research-structure validators all passed on the exact
  candidate;
- exact Zenodo metadata and one-file upload validation: PENDING;
- publication, concept-latest check, and fresh unauthenticated download: PENDING.

The v0.23 manuscript may be published only after the repository, upload, and publication gates
are replaced by verified evidence.
