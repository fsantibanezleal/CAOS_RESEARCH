# central-configurations / tropical-replication

LaTeX source of the preprint "Exact replication and screening of tropical finiteness certificates for central
configurations" (source version 0.12, 14 November 2026). The release and the publication gate are separate steps.

Files:

- `main.tex`: the manuscript. The tables, the figure data and the hash table lie between
  `% BEGIN GENERATED <name>` and `% END GENERATED <name>` markers and are written by `gen_tables.py`.
- `gen_tables.py`: reads the stored artifacts of `problems/dynamical-systems/central-configurations/experiments/`
  (EXP-004 `screening-table.txt` and `hashes.txt`, EXP-007 `summary.json`, EXP-008 `table.json` and the twelve
  stored `gfan` outputs) and rewrites the generated regions. The twelve enrichment cells are decided again from
  the stored outputs with the EXP-004 comet extraction and the exact decider of `code/cclib/exact_lp.py`; no
  `gfan` run is started. `python gen_tables.py --check` exits 1 when `main.tex` differs from the artifacts.
- `zenodo.json`: deposit metadata.

Build, from this folder: `pdflatex main.tex` twice. Voice check, from the repository root:
`python scripts/check_manuscript_voice.py manuscripts/central-configurations/tropical-replication`.
