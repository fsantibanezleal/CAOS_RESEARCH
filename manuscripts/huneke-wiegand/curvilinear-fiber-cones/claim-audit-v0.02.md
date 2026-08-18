# Claim audit - curvilinear conductor fiber cones v0.02

Audit date: 2026-08-18. Prepublication decision: **PASS - exact candidate frozen for DOI
reservation**.

Version 0.02 retains every v0.01 primary-structure result and adds only the explicit canonical
grevlex degeneration established by EXP-026. The version DOI is intentionally absent from this
candidate: it will be inserted only after Zenodo reserves the new-version record, followed by a
fresh complete build, render, metadata, upload, and public-download audit.

## Claim map

| manuscript claim | evidence owner | audit result |
|---|---|---|
| truncated standard-graded parametrization, complete one-component primary decomposition, sharp nilpotence, curvilinear projective geometry, local/arithmetic Gorenstein contrast, and characteristic-sensitive differentials | EXP-025 and claim audit v0.01 | PASS; unchanged |
| canonical standard monomial in every surviving degree/offset fiber | EXP-026 Lemma 7.1 and `proof.md` | PASS |
| reduced grevlex basis profile `(50p^2-17p,5p-1,p-2)` in degrees two through four | EXP-026 Theorem 7.2, full campaign, clique audit, and symbolic certificate | PASS |
| quadratic split into `(77p^2-49p+2)/2` binomials and `(23p^2+15p-2)/2` monomial zero-relations | EXP-026 exact pair count and independent campaign reconstruction | PASS |
| six displayed cubic groups of total size `5p-1`, one quartic family of size `p-2`, and all reduced tails | EXP-026 explicit boundary classification and 16 all-parameter obligations | PASS |
| no reduced-basis elements in degree at least five | EXP-026 degree-four interval saturation and last-variable stabilization argument | PASS; deductive infinite tail closure |
| no minimal leading monomial contains `X_0` | EXP-026 boundary classification | PASS |
| flat Cohen--Macaulay monomial degeneration and Artinian Hilbert function `(1,10p-1,12p,2p-1,1)` | regularity of `X_0` on standard monomials plus frozen Hilbert layers | PASS |
| natural reduced grevlex degree four although minimal relation type is three | EXP-023 minimal presentation and EXP-026 quartic family | PASS |

The finite campaign covers every `p=4,...,300`; the independently encoded clique audit covers
`p=4,5,6,17,73,151,300`; and the Presburger certificate closes 16 all-integer obligations for
`p>=4`. The manuscript states their trust boundaries: finite agreement is not an infinite proof,
the solver emits no independently checked UNSAT proof objects, and the standard-monomial and
degree-stabilization arguments remain separate deductive steps.

## Source and novelty boundary

- Bhardwaj--Chau--Javadekar and Saha--Sengupta--Srivastava supply context for projective monomial
  curves, numerical semigroups, and associated graded semigroup algebras.
- The manuscript does not transfer results from those sources; the exact staircase and formulas
  are proved for the present truncated conductor family.
- The result strengthens the structural analysis of the published CAOS Huneke--Wiegand
  counterexample family. It neither solves a still-open general Huneke--Wiegand problem nor claims
  corresponding bases for arbitrary fiber cones, semigroup rings, or modules.
- The remaining interior Betti-table problem is stated explicitly. A separate manuscript is
  deferred unless that problem yields a theorem large enough to stand independently.

## Experiment and adversarial QA

- EXP-026 mandatory `p=4` smoke: PASS;
- optimized 297-row campaign: PASS, aggregate
  `63af8f734afc8c057751d7633f63eec6d1df83472d494dbad6ada19e4365a218`;
- independent seven-parameter clique audit: PASS, aggregate
  `401c4807cc0a29a67a42c0d84ca8f235c86a271fe93bf1a2d2df586766e41373`;
- all-parameter symbolic certificate: 16/16 negated obligations UNSAT, aggregate
  `10c66bbcaa56108f6bdb423bda7c37d35818c4066ef57970a4e29e046f9dd5fa`;
- eight adversarial controls: PASS in every campaign row;
- original capped implementation: honestly retained as `INCONCLUSIVE_BUDGET` through `p=144`;
  it is not presented as negative mathematical evidence.

## Build, extraction, and render QA

- clean two-pass pdfLaTeX build;
- no LaTeX/package warnings, undefined references, overfull boxes, or underfull boxes;
- PDF metadata has the intended title, subject, keywords, and Felipe as sole author;
- PDF has eight letter-size pages, no encryption, form fields, or JavaScript;
- text extraction confirms version 0.02, the theorem profile, absence of later basis elements, the
  remaining Betti-table question, and absence of placeholder or automated-authorship text;
- all eight pages rendered at 150 DPI and individually inspected after the final source change;
- no clipping, overlap, broken equation, stray TeX command, unreadable glyph, table overflow,
  bibliography defect, or stranded heading.

Frozen pre-DOI candidate:

```text
file    = main.pdf
pages   = 8
bytes   = 453450
MD5     = 2c293dd26bd8c34498539f0c7e9b609e
SHA-256 = 036490d25dbb886d3e3351a2c33f94a31a0bef068ef87e4ca016e32d3175af88
```

## Identity, attribution, and metadata QA

- sole author and sole Zenodo creator: Felipe Santibañez-Leal;
- ORCID: `0000-0002-0150-3246`;
- Son Pham's discovery priority and Craig Huneke's independent verification remain external
  provenance, not authorship or endorsement;
- no LLM, AI system, tool, or model is named as author or co-author;
- version `0.02`, English language, CC BY 4.0, subject, keywords, and related identifiers agree
  across `main.tex`, `README.md`, and valid `zenodo.json`;
- concept DOI `10.5281/zenodo.21997377` is retained; the new version DOI remains pending by design.

## Publication gate

Prepublication QA is complete. Publication remains pending until the new-version DOI is reserved,
inserted into the manuscript, and the DOI-bearing artifact passes the same full build and visual
inspection. Only that final file may be uploaded. After publication, public metadata and a fresh
unauthenticated download must match the committed byte count, MD5, and SHA-256 before this audit is
closed as a published PASS.
