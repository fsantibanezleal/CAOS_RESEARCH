# Version 0.01 publication validation

Reviewed 2026-09-05. Scope and dependencies are mapped in
[claim-audit-v0.01.md](claim-audit-v0.01.md); exact release bytes are frozen in
[publication-gate.json](publication-gate.json).

## Mathematical and computational gates

EXP-060--062 contain complete uniform proofs, independently reviewed against
the full original source and target. The result is the quadratic direct summand,
not the complete cokernel. The splitting is an existence argument, not an
explicit global D-row formula. The manuscript states the imported
family-to-presentation premise and disclaims discovery priority; the Zenodo
description explicitly credits Son Pham for the original public counterexample.

The integrated suite passes 213 tests. EXP-062 contributes 39 producer/auditor
tests; its independent audit reconstructs all 70 frozen signed triangle sources
and five eta transfers, and certifies 364 triangle-sector pairings on 65 distinct
sectors with 23,695 distinct original S sources. Repeated incidence counts are
explicitly distinguished from unique columns in the paper. The independent
certificate replays byte-identically with portable LF output. Research structure,
content, template, artifact-contract and Ruff gates pass. The scoped publisher
has 25 passing offline tests for identity, hashes, authorship, API-state safety,
atomic receipts, concurrency detection and unauthenticated verification.

## Build and rendered review

Two final stabilized LaTeX passes completed successfully. The final log has zero
warnings, overfull boxes or underfull boxes. The PDF is 18 pages and 503,686 bytes.
PDF text extraction succeeds; cross-references have no missing or duplicate
labels. Sole human author, ORCID, title, version DOI, concept DOI and CC BY 4.0
are present and agree with the mirrored metadata.

Every page was rendered with Poppler at 120 dpi and visually inspected: pages
1--18 PASS. The nine adjacent-page spreads were checked for clipped equations,
overlapping text, table boundaries, missing glyphs, header/footer collisions,
unexpected blanks, evidence links and reference layout. None were found. The
longest source and parity formulas fit the margins. Working renders are in
`E:/_Temp/caos-hw-quadratic-v001-qa/`; they are QA intermediates, not publication
payloads. The frozen source/PDF/metadata hashes, rather than those temporary
paths, identify the reviewed release.

## External delivery gate

This record approves only the exact frozen PDF for the already reserved draft
22342976. It does not itself assert publication. The publisher must check the
draft identity, metadata, sole file, byte size and checksum before publishing;
then verify public/latest metadata and a fresh unauthenticated PDF download.
The resulting `public-verification-v0.01.json` owns that later delivery claim.
Existing main v0.23 and curvilinear v0.02 PDFs remain untouched.
