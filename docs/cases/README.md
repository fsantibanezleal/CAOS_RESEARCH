# Cases: the baked registry artifacts

This repository's "cases" are the three registry artifacts the export pipeline bakes for the
web app (CONTRACT 2), one manifest each under `data/derived/manifests/`:

| Case | Content | Source of truth |
|---|---|---|
| `portfolio` | The program board: areas, problems, lifecycle states, feasibility, GPU relevance. | `program/portfolio.yaml` |
| `experiments` | The experiment log: id, title, verdict and date per EXP-NNN record. | `problems/<area>/<slug>/experiments/EXP-*/{hypothesis,verdict}.md` |
| `jacobian` | The Jacobian problem payload: the announced map, the family table, the degree laws, the escape wall and census, the landscape survey. | Transcribed from the exact verdicts (EXP-004/007/008/011/012). |

Every value is traceable to a persisted experiment artifact; the bake is deterministic and the
artifact guard (`scripts/check_artifacts.py`) verifies bytes against the manifests in CI.
