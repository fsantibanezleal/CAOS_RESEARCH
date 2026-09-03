# Environment and tooling facts for the new problem (verified 2026-09-02)

Recorded so the plan and the first experiments are written against what actually exists on the
machine, not against what a paper assumes.

| item | fact | how verified |
|---|---|---|
| Windows Python | repo `.venv`, CPython 3.13.14, numpy 2.5.1, sympy 1.14.0; pytest and ruff pinned in `requirements-dev.txt` | `.venv/Scripts/python.exe --version`, `pip list` |
| LaTeX | MiKTeX `pdflatex` on PATH (`C:/Users/fsant/AppData/Local/Programs/MiKTeX/miktex/bin/x64/`) | `command -v pdflatex` |
| WSL | Ubuntu 24.04, 30 logical CPUs visible, 25 GB RAM | `wsl -l -v`, `nproc`, `free -g` |
| Exact algebra in WSL | `/usr/bin/Singular`, `/usr/bin/4ti2-groebner` | `command -v` inside WSL |
| SAT in WSL | `/usr/bin/cadical`; DRAT-trim binary at `/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim/drat-trim` (shared checker binary, not problem data) | HW EXP-004 `route_b.py` constants |
| Missing everywhere | Macaulay2, GAP, nauty (`geng`), kissat, Sage, Magma, Julia | `command -v` on both sides |
| Invocation pattern | Windows runner calls `wsl.exe -e <tool>` with `wslpath -a` translated paths; flushed stage prints; per-stage wall caps | HW EXP-001 and EXP-004 runners |
| Heavy data | `E:/_Datos/caos-research/<slug>/` with in-repo SHA-256 manifests | methodology 04 |
| Temp | `E:/_Temp/` only; this session's worktree is `E:/_Temp/caos-research-newproblem` on branch `work/new-problem/scouting` (renamed to `work/<slug>/open` once the slug is fixed) | `git worktree list` |
| GitHub auth | `gh auth status` fails in this session; use the vault PAT with `GH_TOKEN` for `gh` and a token URL with `-c credential.helper=` for pushes | memory note, verified failure |
| Zenodo | prereserve flow: `reserve_doi.py <product> <slug>` (needs `manuscripts/<product>/<slug>/zenodo.json` in the vault), rebuild PDF with the DOIs printed, `attach_pdf.py`, `publish_manuscripts.py`; ledger `manuscripts/<product>/deposits.json`; the header block standard is `conventions/manuscript-header-standard.md` | vault `tools/zenodo/` read |

Installable on demand inside WSL (apt): `nauty` (provides `geng`, `labelg`, `countg`), `macaulay2`
(via the Macaulay2 PPA), `gap`. Each install must be pinned in the problem's RESUME gotchas with
the exact version once used.
