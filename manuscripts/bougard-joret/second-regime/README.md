# bougard-joret / second-regime

<!-- current:start -->
- **Current version**: v0.04, published 2026-11-14
- **Title**: The second Bougard-Joret line to order 24: an exhaustive check, the extremal graphs at 35 triples, and a construction without a clique partition for every odd alpha
- **Version DOI**: [10.5281/zenodo.24231735](https://doi.org/10.5281/zenodo.24231735)
- **Concept DOI (always latest)**: [10.5281/zenodo.24044537](https://doi.org/10.5281/zenodo.24044537)
- **Record**: <https://zenodo.org/records/24231735> (file `bougard-joret-second-regime-v0.04.pdf`)
<!-- current:end -->

## Scope

Bougard and Joret conjectured f(n, alpha, k) = t(n, alpha) + ceil(k alpha / 2) for n > k alpha, where t(n, alpha) counts the edges of alpha disjoint balanced cliques. Didin has announced a proof of the lower bound (Zenodo preprint 10.5281/zenodo.22831382, under review; not audited by this programme). The paper is an independent exhaustive check: at all 53 triples with alpha >= 3, k >= 3 and n <= 24 outside the range settled by Bougard and Joret's Proposition 8, f equals the conjectured value (seven pairs (alpha, k) are settled for every n); a validation suite; the 246 extremal graphs at 35 triples, 40 of which have no partition into alpha cliques (all at k = 3 with alpha odd); a construction without a clique partition for every odd alpha; and, for alpha >= 3 and conditional on Didin's Theorem 3, a characterisation of the extremal graphs without such a partition. Source of the scope: `zenodo.json` (description, version notes). Preprint, not peer reviewed.

## Sources and build

- Evidence: `problems/combinatorics/bougard-joret/experiments/EXP-005-second-regime-small/` to `EXP-014-block-uniqueness/`.
- `main.tex` is the paper with its section files (`*.tex`); `main.pdf` is its build (37 pages, 809,752 bytes, SHA-256 `17167eb8af5ab3d89d942587e9aab7c51072d2b62298ee143c836e9f3c2da17a` per `publication-gate.json`).
- `make_tables.py` (argument `--exp`, the experiments folder) generates every table, figure input and quoted number (`numbers.tex`, `table.tex`, `window.tex`, `percount.tex`, `structure.tex`, `validation.tex`, `graphs.tex`, `growth-*.dat`) from the experiment records.
- Release record: `publication-gate.json` (v0.04).

## Version history

- v0.01 = [10.5281/zenodo.24044538](https://doi.org/10.5281/zenodo.24044538), 2026-11-07: the 39 open triples with n <= 22.
- v0.02 = [10.5281/zenodo.24059677](https://doi.org/10.5281/zenodo.24059677), 2026-11-08: order 23 (47 triples).
- v0.03 = [10.5281/zenodo.24229265](https://doi.org/10.5281/zenodo.24229265), 2026-11-14: full rewrite (order 24, validation, extremal graphs, odd-alpha construction).
- v0.04 = [10.5281/zenodo.24231735](https://doi.org/10.5281/zenodo.24231735), 2026-11-14: the characterisation of the extremal graphs without a clique partition (EXP-014), experimental design, ablation and limitations.
