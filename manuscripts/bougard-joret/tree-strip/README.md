# bougard-joret / tree-strip

<!-- current:start -->
- **Current version**: v0.05, published 2026-11-14
- **Title**: Exact minimum size on the first interior shell of the Bougard-Joret problem, with the extremal graphs at independence numbers two and k-1
- **Version DOI**: [10.5281/zenodo.24232301](https://doi.org/10.5281/zenodo.24232301)
- **Concept DOI (always latest)**: [10.5281/zenodo.22315251](https://doi.org/10.5281/zenodo.22315251)
- **Record**: <https://zenodo.org/records/24232301> (file `bougard-joret-tree-strip-v0.05.pdf`)
<!-- current:end -->

## Scope

Let f(n, alpha, k) be the minimum number of edges of a k-connected graph with n vertices and independence number alpha (the Bougard-Joret function). The paper determines f on the whole first interior shell n = alpha + k + 1, f(alpha + k + 1, alpha, k) = ceil(k(alpha + k + 1) / 2) for every k >= 3 and 2 <= alpha <= k + 1, and classifies the extremal graphs at alpha = 2 (complements of disjoint unions of cycles of length at least five) and at the adjacent strip alpha = k - 1 (graphs built on a nonstar tree with prescribed fibers, f(2k, k-1, k) = k^2). Source of the scope: `zenodo.json` (description, version notes). The universal statements rest on the proofs of EXP-001 and EXP-002; the finite computations test them and do not replace them. The paper is a preprint, not peer reviewed.

## Sources and build

- Evidence: `problems/combinatorics/bougard-joret/experiments/EXP-001-tree-strip/` and `EXP-002-next-shell/` (proofs, certificates, the independent NetworkX audit).
- `main.tex` is the paper; `main.pdf` is its build (30 pages, 699,507 bytes, SHA-256 `b20e124c0fef963a5f8d1820958b9cea5486c31e616c1012ffc41fe33b7ecd78` per `publication-gate.json`).
- `make_tables.py` generates the tables, figure fragments and quoted numbers (`numbers.tex`, `table-*.tex`, `fig-*.tex`) from the experiment certificates; `make_zenodo_json.py` rewrites the version-dependent fields of `zenodo.json` from `main.tex`.
- Release records: `publication-gate.json` (v0.05), `publication-verification.json` and `publication-verification-v0.01.json` (earlier receipts).

## Version history

- v0.01 = [10.5281/zenodo.22315252](https://doi.org/10.5281/zenodo.22315252), 2026-09-04: adjacent tree strip and the nonstar-tree classification.
- v0.02 = [10.5281/zenodo.22341644](https://doi.org/10.5281/zenodo.22341644), 2026-09-05: the full shell n = alpha + k + 1 and the alpha = 2 classification.
- v0.03 = [10.5281/zenodo.22823417](https://doi.org/10.5281/zenodo.22823417), 2026-09-18: scientific-voice revision.
- v0.04 = [10.5281/zenodo.22835072](https://doi.org/10.5281/zenodo.22835072), 2026-09-18: author name printed as on the ORCID record.
- v0.05 = [10.5281/zenodo.24232301](https://doi.org/10.5281/zenodo.24232301), 2026-11-14: related work, algorithms with run times, generated tables and figures, ablation, limitations, title re-derived.

Next-version trigger (from `metadata.md`): a proved extension beyond n = alpha + k + 1, a further extremal classification or a representation-uniqueness theorem (backlog BJB-006, BJB-009), or a correction. A finite rerun alone is not a trigger. Published bytes are immutable.
