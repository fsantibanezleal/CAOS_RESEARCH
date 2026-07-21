# 04 - Code standards

## Environments

- One repo `.venv` (Python 3.13), pinned `requirements-dev.txt` (+ per-lane files of the ADR-0057
  base). Never a global environment. New dependency = pin + install + commit in the same change.
- GPU work (torch/CuPy) is declared per experiment and isolated to experiments that need it; the
  repo must remain fully runnable CPU-only (GPU experiments then skip with a clear message).
- Temp on `E:\_Temp`; heavy data on `E:\_Datos\caos-research\<problem>\` with in-repo manifests
  (SHA-256) pointing to it. Nothing heavy is committed.

## Exact vs float policy

- Mathematical identities, counterexample validity, fiber counts, determinants: **exact only**
  (sympy over QQ, exact Groebner/resultants, integer arithmetic). The script asserts and exits
  nonzero on failure; CI re-runs the cheap certificates permanently.
- Search and exploration may use floats/GPU, but anything a verdict depends on is re-checked
  exactly on the candidate set the search produced.

## Structure

- Reusable per-problem logic is promoted from `experiments/` into `problems/.../code/<pkg>/` with
  pytest tests; `scripts/` are thin entry points. Cross-problem utilities go to
  `data-pipeline/researchlab/` (the repo engine) with the same test discipline.
- Tests never write canonical artifacts (hard rule): all test writes go to tmp paths; CI asserts
  artifact content, not just existence.

## CI

- Guards from the base template stay wired: content standards (English-only, no em-dash/emoji),
  template residue, artifact integrity, pytest.
- Flagship exact certificates (seconds-cheap) run on every CI build, e.g. the Jacobian EXP-001
  validation; a regression there fails the build.
