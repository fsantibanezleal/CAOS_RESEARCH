# Riemann distinct-zero replay requirements

Reviewed before implementation, 2026-10-03. Scope: the existing research workbench,
the completed EXP-020/025 results and their published companion. Existing program
authorization covers research, publication and release. RH remains open.

| ID | EARS requirement | Verification gate |
|---|---|---|
| R1 | THE exporter SHALL read only committed evidence and bind every new input to its Git revision and SHA-256. | `tests/test_riemann_distinct_export.py`: committed-source and provenance cases |
| R2 | IF any required cover, input, transfer, publication or source-binding receipt fails, THEN THE exporter SHALL reject the distinct-zero payload. | `tests/test_riemann_distinct_export.py`: actual-receipt corruption matrix |
| R3 | THE replay SHALL distinguish whole-strip distinct points from simple critical-line zeros, retain exact fractions, and state the external local theorem and arithmetic trust bases. | `frontend/src/test/riemannDistinct.test.ts`; `scripts/verify_riemann_ui.mjs` distinct section assertions |
| R4 | WHILE EXP-019/023 lack completed verdicts, THE workbench SHALL show their incomplete status without presenting their candidate bounds as confirmed results. | exporter exclusion test; browser experiment-record checks |
| R5 | WHEN a user changes language, theme or proof stage, THE existing six-tab workbench SHALL preserve readable equations, source citations, evidence inspection and concept-DOI access on phone and desktop. | pointer browser matrix in `scripts/verify_riemann_ui.mjs`; rendered screenshots review |
| R6 | IF the new optional evidence is absent or inconsistent, THEN THE browser SHALL withhold the new bound and preserve the older replay. | `frontend/src/test/riemannDistinct.test.ts`: missing/corrupt payload controls |
| R7 | THE release SHALL preserve the frozen published bytes, serialize baking/version changes, and verify source integration, CI, Pages and live artifact hashes separately. | feature `convergence.md`; release receipts and public download/hash checks |

No browser optimizer, certificate traversal, live zeta computation or learned model
is introduced. Publication and machine checks are not mathematical peer acceptance.
