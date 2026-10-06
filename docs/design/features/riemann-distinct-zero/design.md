# Design and preimplementation review

2026-10-03, reviewed against committed EXP-020/025 verdicts, exact transfer and
independent audit receipts, wiki/20-distinct-zero-certificates.md and the frozen
manuscript. Existing short-interval content remains a separate counting lane.

The existing `riemann-replay-v9` contract receives an optional, explicitly versioned
`distinct_zero` object (`riemann-distinct-zero-v1`). This additive change preserves
the v9 helpers and older deployments; it does not silently reinterpret old fields.
The object contains the two completed exact fractions, fixed parameters, selected
recorded receipts, source attribution and the verified publication. Its provenance
uses the exporter's existing committed-byte reader. Every required receipt is
validated before any result is exported. Incomplete EXP-019/023 records enter the
experiment viewer only; they cannot enter this result object.

The new offline validator checks full-cover count and tree accounting, matching
packet/table/report bindings, native full-cell completion, rejected corruption
controls, exact transfer fraction and pressure accounting, licensed external source
hash and archived attestation, rational scalar controls, and all published-file
matches. These checks validate recorded evidence, not rerun interval arithmetic or
external Lean. Physical runtime CRLF bytes are reproduced by the published archive;
Git provenance describes normalized committed bytes independently.

The typed browser gate requires the new contract and all recorded acceptance flags.
It performs no scientific recomputation. A separate bilingual component transcribes
the general vector-pressure formula, parameters, proof dependencies and limitations.
Its selectable proof stages use theme-aware SVG and source citations. Summary,
context, references, strategy, results and open questions receive the corresponding
current content inside the existing shell; no additional sibling tabs are added.
Experiment names/statuses are translated for all new records.

Release owner: this chat, branch
`work/riemann-hypothesis/distinct-zero-release-20261003`, full checkout
the separate `caos-riemann-release` integration checkout. Frozen compute checkout remains untouched. Proposed
capability version 0.75.000 / package metadata 0.75.0. GitHub Pages remains appropriate
for the existing public, static baked workbench; no online heavy computation.

Review verdict: design accepted for implementation. Source-dependent claims are
visible, fail-closed controls are required, and each requirement names a measurable
gate. Product scaffolding is unchanged; this is a feature SDD under ADR-0075.

## Direct-entry review, 2026-10-04

R8 is accepted before implementation. After the existing production build, copy
its root `index.html` to `dist/problems/riemann-hypothesis/index.html`. The build
already uses root-relative asset/data URLs and React Router accepts a trailing
slash, so this supplies an actual Pages entry without duplicating application
logic. The existing fallback shim remains available for other routes. Verify
the copied HTML bytes and final direct-route HTTP/browser behavior. This is a
release defect correction within the authorized Riemann scope; no scientific
input or admitted bound changes.
