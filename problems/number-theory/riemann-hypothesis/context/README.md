# Source audit and local archive

Review cutoff: 2026-09-19. The archive contains 64 source documents/pages and seven
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
| [Classical density and multiplicity](2026-09-12-critical-mass-and-multiplicity-route.md) | Exact odd-zero count, seed packing, parity mechanism and mollifier interfaces |
| [Independent parity audit](2026-09-12-parity-transfer-adversarial-audit.md) | Source conventions, excess accounting, quantifiers and novelty search |
| [Spectral and optimization alternatives](2026-09-12-spectral-optimization-alternatives.md) | Negative spectrum, witnesses, conditioning and missing higher moments |
| [Alternative RH reformulations](2026-09-12-alternative-rh-reformulations.md) | Approximation, positivity, spectral and heat-flow criteria with obstructions |
| [Pressure-frame prior art](2026-09-12-pressure-frame-prior-art.md) | Multi-point pressure, mixed certificates, global capacity methods and the next short-interval question |
| [Local optimized Selberg transfer](2026-09-19-local-selberg-transfer.md) | Pearce-Crump's explicit detector, the Axiom unconditional-formalization update, and the now-confirmed EXP-005 short-interval localization |
| [Hilbert dimension and parity compression](2026-09-20-hilbert-parity-compression.md) | EXP-006 preflight for retaining Lamzouri's first-subspace dimension in the odd-multiplicity transfer |

Full text whose public redistribution permission was not identified is retained locally in
`source-cache/`. The public record contains provenance and independently authored analysis.
Seven permissively licensed code ZIPs in `source-snapshots/` retain upstream licenses.
No third-party source is relabeled as CAOS authorship.

From the repository root, restore or verify the archive with:

```text
python problems/number-theory/riemann-hypothesis/code/restore_sources.py
python problems/number-theory/riemann-hypothesis/code/restore_sources.py --verify-only
```

Restoration checks exact size and SHA-256, failing closed if an upstream URL changes.
Derived mathematical claims belong to the experiment verdicts and their adversarial audits.
