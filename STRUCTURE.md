# CAOS Research repository structure

This is the authoritative map of the research repository. The generic product archetype still
governs the offline pipeline, static frontend, documentation, CI, and deployment layers, but the
research record adds a stricter per-problem persistence model.

Start every working session at [`Entry_point.md`](Entry_point.md).

## 1. The five record planes

| Plane | Canonical location | Purpose | Authority |
|---|---|---|---|
| Portfolio registry | `program/portfolio.yaml` | Every candidate problem, area, lifecycle state, feasibility, and compute profile | Canonical for membership and routing |
| Operational state | `program/<slug>/` | Resume handoff, plan, heartbeat, backlog, routes, strategies, and lenses | Canonical for what to do next |
| Primary research evidence | `problems/<area>/<slug>/` | Sources, derivations, code, experiment hypotheses, raw artifacts, verdicts, history, and wiki | Canonical for mathematical claims |
| Publication record | `manuscripts/<slug>/`, `data/derived/`, `frontend/` | Manuscripts and public replay views transcribed from validated evidence | Derived, never allowed to outrun verdicts |
| Private management mirror | `<CAOS_MANAGE>/plans/caos-research/<slug>/` | Portfolio axes, numbered findings, management history, credentials, release and publication operations | Derived mirror plus private operations |

The repository is the memory. Chat is never a record plane.

## 2. Source-of-truth rules

1. A mathematical claim is owned by an experiment verdict and its persisted artifacts, or by a
   primary-source dossier with an explicit verification label.
2. `RESUME.md` is the fastest navigation document, but it is derived. On conflict, correct it from
   the primary evidence.
3. `state.md` is the problem heartbeat. `backlog.md` owns actionable work and status. `plan.md` owns
   the durable strategy.
4. `history/log.md` is append-only. It records decisions, dead ends, corrections, and experiment
   links.
5. The wiki, manuscripts, frontend, and management mirror are transcriptions. Every claim they
   surface must remain traceable to primary evidence.
6. `program/portfolio.yaml` is the only machine-readable registry. Human problem tables are useful
   views and must be kept synchronized.

## 3. Repository tree

```text
CAOS_RESEARCH/
|-- Entry_point.md                 # session bootstrap and workflow router
|-- README.md                      # public repository landing page
|-- STRUCTURE.md                   # this authoritative map
|-- methodology/                   # binding research operating system, documents 01 to 12
|-- program/
|   |-- portfolio.yaml             # canonical portfolio registry
|   |-- README.md                  # human-readable portfolio view
|   `-- <slug>/
|       |-- RESUME.md              # required seven-section zero-loss handoff
|       |-- plan.md                # strategy, phases, lenses, validation routes
|       |-- state.md               # lifecycle heartbeat and immediate frontier
|       |-- backlog.md             # identified work with explicit statuses
|       `-- *.md                   # routes, research lines, checklists, strategy notes
|-- problems/
|   `-- <area>/<slug>/
|       |-- context/               # primary-source dossiers, references, scoping evidence
|       |-- history/log.md         # append-only problem history
|       |-- code/                  # reusable tested per-problem packages
|       |-- scripts/               # optional thin problem entry points
|       |-- experiments/
|       |   `-- EXP-NNN-<slug>/
|       |       |-- hypothesis.md  # committed before the run
|       |       |-- run.py         # or a deterministic run/ entry point
|       |       |-- artifacts/     # raw outputs or hashed heavy-artifact manifests
|       |       `-- verdict.md     # evidence, adversarial check, limitations, disposition
|       `-- wiki/
|           |-- README.md
|           |-- 01-*.md ...        # deep, numbered exposition
|           `-- assets/            # hand-authored theme-aware SVGs
|-- manuscripts/<slug>/<paper>/    # LaTeX source, PDF, and per-paper Zenodo metadata
|-- data-pipeline/researchlab/      # cross-problem offline export engine
|-- data/
|   |-- raw/                        # local and ignored
|   `-- derived/                    # compact committed replay artifacts
|-- manifests/                      # artifact contracts
|-- frontend/                       # shared-shell static web app
|-- docs/                           # repository-level public documentation
|-- app/                            # optional dormant API lane
|-- deploy/                         # deployment configuration
|-- scripts/                        # setup, precompute, smoke, and structural guards
|-- tests/                          # cross-problem pipeline and contract tests
`-- .github/workflows/              # CI and serialized deployment automation
```

## 4. Per-problem durable record

Every problem at `opened` or a later lifecycle state must have:

```text
program/<slug>/
  RESUME.md
  plan.md
  state.md
  backlog.md

problems/<area>/<slug>/
  context/
  history/log.md
  code/
  experiments/
  wiki/README.md
```

The root guard `scripts/check_research_structure.py` enforces this contract against
`program/portfolio.yaml`.

### RESUME contract

`RESUME.md` contains, in order:

1. State in one screen, including load-bearing formulas and evidence labels.
2. The named objects table.
3. The experiment index and load-bearing output of each experiment.
4. In-flight mathematics and exact partial-run state.
5. Ordered next actions with commands and decision points.
6. A path map for every relevant record and artifact.
7. Gotchas, runtime facts, environment constraints, and solver workarounds.

It also carries the current lenses ledger required by methodology 10 and 11.

### Experiment contract

An experiment folder is immutable after closure except for explicit factual correction. A changed
question gets a new sequential experiment number. Every experiment persists:

- a falsifiable hypothesis committed before execution;
- source completeness, premise dependencies, one-sidedness, invariant-first reasoning, compute
  budget, checkpoint interval, and kill criterion;
- a deterministic entry point;
- raw artifacts or a hash manifest for external heavy artifacts;
- a verdict with the validation route, residual failure modes, and consequences.

## 5. Lifecycle and intake

The lifecycle is:

```text
proposed -> scoped -> opened -> exploring -> consolidating -> published
                                      \-> dormant | closed
```

- `proposed` and `scoped` candidates need portfolio and scoping records, but not a full problem tree.
- `opened` requires the source-complete context pass, operational files, durable problem tree, a
  selected strategy, and a declared multi-lens approach.
- `exploring` requires a completed `EXP-001`.
- `consolidating` requires adversarial records for every claim moving toward publication.
- `published` requires the wiki, manuscript or explicit manuscript disposition, web gate, and
  traceable replay artifacts to be complete.
- `dormant` and `closed` retain the entire record and state what would reopen the problem.

Multiple problems can be active simultaneously. Each session owns one problem scope. Shared releases
remain serialized.

## 6. Isolation and shared surfaces

Freely writable inside one problem session:

- `problems/<area>/<slug>/`
- `program/<slug>/`
- the selected problem's frontend page component
- `<CAOS_MANAGE>/plans/caos-research/<slug>/`

Serialized shared surfaces:

- global version sources and `CHANGELOG.md`;
- tags and the release pull request;
- cross-problem artifact bake and shared derived data;
- shared portfolio indexes when concurrent edits could collide;
- shared frontend registries and navigation.

Pull both repositories before any write and again immediately before editing a shared surface.
Experiment rounds commit and push frequently without a version bump. Promotion to integration and
release branches uses proper pull requests. LLMs and automated assistants are never authors or
co-authors.

## 7. Offline pipeline and web replay

The public web application never performs research computation. The data flow is:

```text
problem evidence
  -> offline data-pipeline stages
  -> compact artifacts plus manifests
  -> static frontend replay
```

The pipeline keeps explicit ingestion and artifact contracts. Tests never overwrite canonical
artifacts. Cross-problem baking is part of the serialized release step because it rewrites shared
derived files.

The optional `app/` backend remains dormant unless an applicable architecture decision activates it.
Heavy research dependencies belong only in the offline lane. The frontend and live lane must not
import them.

## 8. Heavy data, credentials, and portability

- Heavy data and source archives live under `E:\_Datos\caos-research\<slug>\` with SHA-256 manifests
  in the problem record.
- Temporary compute uses `E:\_Temp`.
- Secrets, credentials, tokens, operational publication tooling, and private infrastructure details
  remain in `CAOS_MANAGE`.
- Public tracked files use repo-relative paths. Local machine repository paths are never committed.
- Dependency trees, virtual environments, caches, raw heavy arrays, temporary screenshots, and
  active-run logs are not repository source.

## 9. Validation

At minimum, structural documentation changes run:

```powershell
python scripts/check_research_structure.py
python scripts/check_content_standards.py
python scripts/check_template_residue.py
```

Code, pipeline, frontend, manuscript, and release changes add the checks required by their respective
methodology and management gates. A green test does not override contradictory mathematical evidence;
the experiment record remains authoritative.
