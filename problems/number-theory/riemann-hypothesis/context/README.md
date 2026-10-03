# Source audit and local archive

Review cutoff: 2026-09-19. The archive contains 64 source documents/pages and seven
licensed code snapshots. The original supplied Anthropic PDF is distinct from its revision.
The original-proof acquisition subset comprises 16 PDFs and 559 pages; review depth is
reported honestly in the dossiers and was concentrated on theorem dependencies and proofs.

| Record | Scope |
|---|---|
| [Source manifest](source-manifest.json) | Original URLs, versions, licenses, exact byte counts and SHA-256 |
| [EXP-007 source manifest extension](source-manifest-exp007.json) | Additive post-release source records without changing the manifest pinned by earlier experiments |
| [EXP-010 source manifest extension](source-manifest-exp010.json) | Additive records for Young, CFKL and Bui-Conrey-Young, the arXiv sources of the localized Levinson detector |
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
| [Rank-six local transfer](2026-09-20-rank-six-local-transfer.md) | EXP-008 source boundary, fixed-rank localization, onset comparison, and interdisciplinary next routes |
| [Interdisciplinary update and defect-parity seam](2026-09-20-interdisciplinary-update-and-defect-parity.md) | Post-cutoff sources, cross-area route evaluation, and the EXP-007 spectral-defect parity preflight |
| [Localized Levinson-Conrey preflight](2026-09-26-levinson-localization-preflight.md) | EXP-010 sources and gates: short-interval shifted moment, distinct sign-change counting, certified detector constants, route decision |
| [Literature and representation sweep](2026-09-27-literature-and-representation-sweep.md) | Post-EXP-010 external standing, the RH-027 source correction, kernel versus second-order levers, cross-field representations ranked by proportion channel |

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

## Additive October archive

[Source manifest 20261003](source-manifest-20261003.json) pins five PDF and
five source bundles: Knausgard 2609.33043v1, CIS 1808.02879v1 and
1105.1177v1, Tang 2608.14852v1, CLMR 2409.01457v1.
The [dated review](2026-10-03-update-and-dual-family-preflight.md) records
the actual reading scope, formalization exclusions and method gaps.
Its cache_path entries follow the context/source-cache restoration contract;
the same path after the source-cache prefix identifies the external archive.
Papers remain externally cached. Earlier manifests stay frozen.

[Trace preflight](2026-10-03-trace-clipping-preflight.md) and
[source-manifest-exp016](source-manifest-exp016.json) add the author-hosted
Wolkowicz-Styan 1980 paper. Reading scope: printed pages 472-474,
the trace/variance setup and Theorem 2.1. The 36-page PDF is archived
externally, not claimed to have been reviewed completely.

[Late source eligibility review](2026-10-03-late-source-eligibility.md)
and its [manifest](source-manifest-20261003-late-review.json) preserve the
Qi--Qiao spectral paper, Das--Pujahari derivative paper and Cicada Lean
port. The review records an exact discrepancy in a displayed exponent
minimum, spectral-family applicability gaps and explicit formal analytic
hypotheses. It does not infer a theorem refutation or new zero bound.
