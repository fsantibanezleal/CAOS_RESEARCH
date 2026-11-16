# bougard-joret / next-matching

<!-- current:start -->
- **Current version**: v0.05, published 2026-11-14
- **Title**: The next matching level for triangle-free graphs with bounded degree and an exact Bougard-Joret value
- **Version DOI**: [10.5281/zenodo.24232146](https://doi.org/10.5281/zenodo.24232146)
- **Concept DOI (always latest)**: [10.5281/zenodo.22343021](https://doi.org/10.5281/zenodo.22343021)
<!-- current:end -->

## Scope

Let T(d, m) be the maximum number of edges of a triangle-free graph with maximum degree at most d and matching number at most m. The paper proves T(d, d + 1) = d^2 + d + 2 for every integer d >= 7 (the attaining construction is due to Banak, Ekim and Taskin; the contribution is the uniform upper bound, which settles 184 <= T(13, 14) <= 185 in favor of 184) and, as a consequence, the exact Bougard-Joret value f(2d + 3, 2, d + 2) = d^2 + 4d + 2 for every d >= 7 (EXP-004). The full Ahanjideh-Ekim-Yildiz conjecture remains open. Source of the scope: `zenodo.json` (description, version notes). Preprint, not peer reviewed.

## Sources and build

- Evidence: `problems/combinatorics/bougard-joret/experiments/EXP-003-triangle-free-next-matching/` and `EXP-004-bracket-endpoint/` (proofs, certificates, the independent audit, the configuration-split satisfiability runs).
- `main.tex` is the paper; `main.pdf` is its build (28 pages, 774,952 bytes, SHA-256 `9216fc30312a6cd9055481212c8e5cf78e9379e20c31e4238ba6f78b000137db` per `publication-gate.json`).
- `make_tables_figures.py` generates `numbers.tex`, `tables/*.tex` and `figures/*.pdf` from the EXP-003 and EXP-004 artifacts.
- Release records: `publication-gate.json` (v0.05) and `publication-verification.json` (the v0.01 receipt).

## Version history

- v0.01 = [10.5281/zenodo.22343022](https://doi.org/10.5281/zenodo.22343022), 2026-09-05: the uniform next-matching theorem, the fixed-order theorem and the one-edge Bougard bracket.
- v0.04 = [10.5281/zenodo.23965193](https://doi.org/10.5281/zenodo.23965193), 2026-11-04: the exact value f(2d + 3, 2, d + 2) = d^2 + 4d + 2 and the shared-neighbourhood theorem (EXP-004).
- v0.05 = [10.5281/zenodo.24232146](https://doi.org/10.5281/zenodo.24232146), 2026-11-14: the threshold Z(d), algorithms with commands and hashes, generated tables and figures, ablation, limitations; proofs unchanged in substance.
- v0.02 and v0.03: their DOIs are not recorded in the files read (UNVERIFIED).

Next-version trigger (from `metadata.md`): a wider uniform matching range (backlog BJB-015), a classification of the attaining graphs, or a correction. A finite rerun alone is not a trigger. Published bytes are immutable.
