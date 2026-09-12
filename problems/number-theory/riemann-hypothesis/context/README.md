# Source audit and local archive

Review cutoff: 2026-09-12. The archive contains 21 primary-source documents and four
licensed code snapshots. The original supplied Anthropic PDF is distinct from its revision.
The original-proof acquisition subset comprises 16 PDFs and 559 pages; review depth is
reported honestly in the dossiers and was concentrated on theorem dependencies and proofs.

| Record | Scope |
|---|---|
| [Source manifest](source-manifest.json) | Original URLs, versions, licenses, exact byte counts and SHA-256 |
| [Original and successor review](2026-09-12-original-and-successor-review.md) | Historical record, original argument, later candidates and objections |
| [Lamzouri analysis](2026-09-12-lamzouri-analysis.md) | Finite Hilbert framework, constants and prior-art barriers |
| [Formalization audit](2026-09-12-formalization-audit.md) | Pinned Lean sources, explicit assumptions and current CI coverage |
| [Wang transfer audit](2026-09-12-wang-transfer-audit.md) | Short-interval theorem, deweighting, error estimates and smoothing |

Full text whose public redistribution permission was not identified is retained locally in
`source-cache/`. The public record contains provenance and independently authored analysis.
Four permissively licensed code ZIPs in `source-snapshots/` retain upstream licenses.
No third-party source is relabeled as CAOS authorship.

From the repository root, restore or verify the archive with:

```text
python problems/number-theory/riemann-hypothesis/code/restore_sources.py
python problems/number-theory/riemann-hypothesis/code/restore_sources.py --verify-only
```

Restoration checks exact size and SHA-256, failing closed if an upstream URL changes.
Derived mathematical claims belong to the experiment verdicts and their adversarial audits.
