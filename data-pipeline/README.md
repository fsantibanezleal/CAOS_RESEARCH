# data-pipeline/, the offline engine (`researchlab`)

Rename `researchlab` → `<slug>lab` per product. The **single source of physics/algorithm truth**; `frontend/` and
`app/` consume it, never re-implement it. Its own venv: **`.venv-pipeline`** (heavy SOTA engines, local-only).

## Layout (the package lives directly under `data-pipeline/`)
- `researchlab/pipeline.py`, orchestrator + CLI (`python -m researchlab.pipeline [all|<case>] [--seed N]`)
- `researchlab/registry.py`, cases grouped by CATEGORY · `researchlab/live.py`, Pyodide live entrypoint
- `researchlab/io/`, `contract.py` (**CONTRACT 1**) · `formats.py` (standard readers/writers) · `schema.py` (types)
- `researchlab/core/`, `rng.py` (seeded determinism) · `trace.py` · `manifest.py` (**CONTRACT 2**) · `gate.py`
- `researchlab/model/`, the shared pure-Python core (Pyodide-safe); EXAMPLE = SIR
- `researchlab/stages/`, `preprocess → feature_extraction → train → infer → evaluate → export`
- `researchlab/cases/`, documented cases

Setup + run: `scripts/setup.{sh,ps1}` then `scripts/precompute.{sh,ps1}`. See
[../docs/architecture/05_precompute-pipeline.md](../docs/architecture/05_precompute-pipeline.md).
