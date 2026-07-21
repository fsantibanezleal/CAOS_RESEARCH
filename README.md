<!--
[![CI](https://img.shields.io/github/actions/workflow/status/fsantibanezleal/CAOS_RESEARCH/ci.yml?branch=main&label=CI)](https://github.com/fsantibanezleal/CAOS_RESEARCH/actions)
-->
[![License](https://img.shields.io/github/license/fsantibanezleal/CAOS_RESEARCH)](LICENSE)
[![Version](https://img.shields.io/github/v/tag/fsantibanezleal/CAOS_RESEARCH?label=version&sort=semver)](https://github.com/fsantibanezleal/CAOS_RESEARCH/tags)

# CAOS Research - an experiment-history repository for open problems

Methodical, offline, adversarially validated experimentation on open mathematical and physical
problems (Smale problems, Millennium problems, and adjacent). The repository IS the record: every
problem carries its own context dossiers, investigation history, code, numbered experiments with
declared hypotheses and verdicts, and a curated wiki. A static web app showcases, per problem:
summary, context, references and alternative approaches, the current strategy, and our results.

All computation runs offline (local CPU/GPU); the web app only replays persisted artifacts.
Findings are consolidated into a LaTeX manuscript (`manuscript/`).

## Layout

| Folder | What it holds |
|---|---|
| [`methodology/`](methodology/) | The research operating system: problem lifecycle, experiment standard (EXP-NNN), adversarial validation ladder, code and writing standards, web publication gates. |
| [`program/`](program/) | The status section: portfolio board (`portfolio.yaml` + README), and per-problem plan / state / backlog. The plan of each problem lives here, inside the repo. |
| [`problems/<area>/<slug>/`](problems/) | One self-contained folder per problem: `context/` (dossiers, references), `history/` (append-only log), `code/` (tested per-problem package), `scripts/`, `experiments/EXP-NNN-*/`, `wiki/`. |
| [`manuscript/`](manuscript/) | LaTeX manuscript mapping all findings and approaches (built PDF committed per release). |
| `data-pipeline/`, `frontend/`, `docs/`, `scripts/` | CAOS product-repo base (ADR-0057): offline pipeline that bakes problem/experiment artifacts for the web app, the shared-shell SPA, the repo wiki, and the CI guards. |

## Problems

| Area | Problem | State |
|---|---|---|
| Algebraic geometry | [Jacobian conjecture](problems/algebraic-geometry/jacobian-conjecture/) | exploring (opened 2026-07-20) |

The Jacobian conjecture was refuted for N >= 3 on 2026-07-19 (Levent Alpöge, with Claude Fable 5).
This program independently validated the counterexample in exact arithmetic, studies why it works
and how it generalizes, and pursues what transfers to the still-open N = 2 case. See the problem
wiki for the current picture and `program/jacobian-conjecture/state.md` for the heartbeat.

## Running

```powershell
# one-time setup (Windows; .sh twins exist for bash)
.\scripts\setup.ps1

# run a problem experiment (each EXP folder documents its exact entry point), e.g.:
.\.venv\Scripts\python.exe problems\algebraic-geometry\jacobian-conjecture\experiments\EXP-001-validate-counterexample\run.py
```

Every experiment is deterministic, headless, and exact where the claim requires it (rational or
certified arithmetic; floats are exploration-only). See `methodology/02-experiment-standard.md`.

## Versioning

`X.XX.XXX` display form, tags per release, `CHANGELOG.md` (Keep a Changelog). Pre-1.0 while the
first problem has not reached the `published` gate.

## License

MIT (c) 2026 Felipe Santibañez-Leal
