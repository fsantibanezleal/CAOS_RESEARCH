# 02 - Experiment standard (EXP-NNN)

Each experiment is a folder `problems/<area>/<slug>/experiments/EXP-NNN-<short-slug>/`.
Numbering is per-problem, sequential, immutable. A superseded experiment is never edited; a new
EXP-NNN supersedes it and links back.

## Required files

| File | Content |
|---|---|
| `hypothesis.md` | Question; motivation (link to the context dossier section); the falsifiable prediction; method; success and failure criteria. **Written and committed BEFORE the run.** |
| `run.py` (or `run/`) | Deterministic, headless entry point run with the repo `.venv`. Seeds fixed. CPU/GPU declared at the top. Exits nonzero on check failure. |
| `artifacts/` | Raw outputs: logs, JSON, baked data, figures. Heavy artifacts (> a few MB) go to `E:\_Datos\caos-research\<slug>\EXP-NNN\` and are represented here by a manifest with SHA-256 hashes. |
| `verdict.md` | What happened; exact-arithmetic status; the adversarial-validation record (which refutation route was attempted, with output); verdict: `confirmed / refuted / null / inconclusive`; consequences for the strategy; a "how could this be wrong?" section. |

## Rules

- The hypothesis states, before any code runs, what outcome would count as failure. No moving the
  goalposts after the fact; a changed question is a NEW experiment.
- Every quantitative claim in `verdict.md` must be reproducible by re-running `run.py` from the
  repo root, with output identical up to declared nondeterminism (which must be none unless the
  experiment explicitly involves stochastic search; then seeds and tolerances are declared).
- Experiments that certify mathematical claims use exact arithmetic (see 04); an experiment whose
  point is float exploration says so in `hypothesis.md` and cannot yield a `confirmed` verdict on
  a mathematical identity by itself.
- Each experiment is referenced from the problem `history/` log entry of the day it ran, and from
  any wiki page that uses its result.
