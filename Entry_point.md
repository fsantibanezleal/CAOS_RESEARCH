# CAOS Research session entry point

This file is the first read for every CAOS Research working session. It routes the session to the
right problem record, preserves per-problem isolation, and makes the repository, rather than chat
history, the durable memory.

## 1. Authority and evidence order

Apply these sources in order:

1. The user's current request.
2. The private CAOS management entry point at `<CAOS_MANAGE>/Entry_point.md`, including security,
   quality, GitHub, diffusion, manuscript, Zenodo, release, and parallel-session rules.
3. This file and the binding documents under [`methodology/`](methodology/).
4. The selected problem's operational record under `program/<slug>/`.
5. The selected problem's primary evidence under `problems/<area>/<slug>/`.

For mathematical claims, the evidence order is more specific:

1. Experiment artifacts and `verdict.md`.
2. Primary-source dossiers in `context/`.
3. The append-only problem history.
4. `RESUME.md`, `state.md`, the wiki, manuscripts, and management mirrors, which are derived views
   and must be corrected if they disagree with primary evidence.

Never infer current state from a prior chat. Never silently resolve a conflict between records.
Identify it, use the primary evidence, correct every affected derived view, and record the correction.

## 2. Mandatory session start

Before any write:

1. Pull `develop` in both `CAOS_RESEARCH` and `CAOS_MANAGE`. Use an explicit remote and branch when
   local tracking is absent:

   ```powershell
   git pull --ff-only origin develop
   ```

2. Inspect `git status --short` in both repositories. Preserve existing work. If unrelated changes
   exist, do not overwrite them and do not mix them into a problem round without reviewing them.
3. Read [`program/portfolio.yaml`](program/portfolio.yaml) and resolve the requested name to one
   exact `<area>/<slug>`.
4. Create or resume a short-lived `work/<slug>/<topic>` branch from the updated `develop` branch.
   Parallel local sessions use separate git worktrees; never switch the branch beneath another
   active session.
5. Claim one problem scope for the session:
   `problems/<area>/<slug>/`, `program/<slug>/`, and
   `<CAOS_MANAGE>/plans/caos-research/<slug>/`.
6. Read, in order:
   - `program/<slug>/RESUME.md`
   - `program/<slug>/state.md`
   - `program/<slug>/backlog.md`
   - `program/<slug>/plan.md`
   - any strategy, route, lens, or research-line files named by `RESUME.md`
   - the latest entries in `problems/<area>/<slug>/history/log.md`
   - the hypotheses and verdicts for the in-flight and immediately preceding experiments
7. Read the methodology router in section 4 below before acting.
8. Give a short opening report: resolved problem and scope, current evidence-backed state, in-flight
   work, dirty files that must be preserved, the next proposed action, and whether any external or
   serialized action would require a separate gate.

If the requested name is ambiguous, inspect the portfolio and program folders first. Ask the user
only if more than one plausible target remains.

## 3. Continue an existing problem

For a request such as:

> Read the entry point at the CAOS Research repository and continue working with problem XXX.

Do the mandatory start, then:

1. Treat `RESUME.md` as the navigation page, not as proof.
2. Reconcile its in-flight and next-action claims against `state.md`, `backlog.md`, the latest
   history entry, and the relevant experiment verdicts.
3. Check whether a run is already active or an artifact is still changing before launching,
   editing, or committing related files.
4. Continue the highest-priority unblocked action. Do not start a different problem or a global
   release as a side effect.
5. Declare a new `EXP-NNN` hypothesis before any experimental run. Complete every preflight field
   required by methodology 02 and 12.
6. Persist results vertically in the same round: artifacts, verdict, code and tests when applicable,
   wiki transcription, manuscript update when triggered, history, backlog, state, `RESUME.md`, and
   the per-problem management mirror.
7. Close the round with focused commits, push the problem branch, and promote it to `develop` through
   a pull request. Do not bump the global version, bake cross-problem data, tag, or open the
   `develop` to `main` release PR unless the session explicitly owns the serialized release step.

## 4. Methodology router

Read [`methodology/README.md`](methodology/README.md) for the complete index. At minimum:

| Work being done | Required reads |
|---|---|
| Any problem work | 01 lifecycle, 07 handoff, 08 parallel sessions, 10 lenses, 11 exploration cadence |
| Declaring or running an experiment | 02 experiment standard, 03 adversarial validation, 04 code standards, 12 preflight and cost discipline |
| Writing dossiers, wiki, or mathematical narrative | 03 adversarial validation, 05 writing standards |
| Updating the web app | 06 web publication plus the applicable management ADRs and product-quality rules |
| Creating or expanding a manuscript | 05 writing standards and 09 manuscripts and publication |
| Publishing, Zenodo, versioning, baking, tagging, or PR work | 08 parallel sessions, 09 manuscripts and publication, and the management entry point |

The systematic exclusion or adjudication spine stays active, together with at least two complementary
research lenses. Every round includes and records an exploration moment. Before expensive compute,
use a single distinguishing invariant if one can decide the question.

## 5. Incorporate and open a new problem from a reference

For a request such as:

> Read the entry point at the CAOS Research repository, incorporate and start working with problem
> YYY based on reference ZZZ.

Use the following lifecycle. A reference is an input to verify, not an authority to copy.

### A. Resolve and preserve the reference

1. Identify the exact work: authors, title, date/version, DOI or arXiv identifier, official URL, and
   any accompanying code or data.
2. Prefer the primary source. Record provenance, access date, license, and verification status.
3. Read the entire source sections bearing on the proposed work, including conclusions, appendices,
   closing remarks, and cited prior exclusions.
4. Store heavy source files outside git under `E:\_Datos\caos-research\<slug>\`; persist an in-repo
   manifest with SHA-256 hashes and stable source links.
5. Mark claims `[V]`, `[MV]`, `[D]`, `[C]`, or `[U]` according to the local writing convention.
   Unverified claims cannot support a conclusion or compute campaign.

### B. Propose and scope

1. Choose a stable lowercase kebab-case `<slug>` and an area already declared in
   `program/portfolio.yaml`, or explicitly define and justify a new area.
2. Check that the slug does not collide with an existing portfolio row, `program/` folder, problem
   tree, manuscript tree, frontend page, or management mirror.
3. Add or update the portfolio row as `proposed` or `scoped`.
4. Persist a scoping sheet under `program/<slug>/` with:
   - precise problem statement and current verified status;
   - why the supplied reference matters;
   - feasibility class and exact versus numeric surface;
   - known examples, counterexamples, and closest prior work;
   - candidate invariants and at least three applicable lenses;
   - compute needs, likely costs, and stop conditions;
   - novelty risks, publication risks, and explicit non-claims.
5. Do not open the problem or spend machine time until the primary-source pass is source-complete.

### C. Open the durable problem record

When the `opened` lifecycle gate is satisfied, create:

```text
program/<slug>/
  RESUME.md
  plan.md
  state.md
  backlog.md

problems/<area>/<slug>/
  context/references.md
  history/log.md
  code/
  experiments/
  wiki/README.md

<CAOS_MANAGE>/plans/caos-research/<slug>/
  status.md
  findings.md
  history.md
```

Add `scripts/`, `wiki/assets/`, and `manuscripts/<slug>/` when the problem needs them. Use the
required seven-section `RESUME.md` contract from methodology 07. The plan must name the systematic
spine, at least two complementary lenses, the invariant-first probe, adversarial validation routes,
the exploration cadence, and the first bounded experiment.

Update the shared portfolio and program indexes only after pulling again immediately before those
shared-file writes. Transition to `exploring` only after `EXP-001` has a committed hypothesis,
deterministic entry point, artifacts, and verdict.

### D. Start the first round

1. Turn the smallest decision-bearing question into `EXP-001`.
2. Complete source mining and all methodology 12 preflight fields first.
3. Write and commit `hypothesis.md` before running the experiment.
4. Smoke-test progress and checkpoint behavior before any run expected to exceed five minutes.
5. Run within the declared budget and preserve raw output.
6. Write the verdict exactly as the evidence supports, including null or inconclusive outcomes.
7. Perform the full close-out in section 6.

## 6. Mandatory round close and handoff

Before ending a working session, reconcile and persist:

- the experiment hypothesis, code, raw artifacts, and verdict;
- reusable code and tests;
- the problem wiki and manuscript if their gates were triggered;
- `problems/<area>/<slug>/history/log.md`;
- `program/<slug>/backlog.md`;
- `program/<slug>/state.md`;
- `program/<slug>/RESUME.md`, including formulas, objects, experiment index, exact run state, ordered
  commands, path map, gotchas, and the lenses ledger;
- the per-problem management mirror: `status.md`, `findings.md`, and `history.md`.

Then:

1. Run focused tests and applicable structural/content guards.
2. Inspect the complete diff, including pre-existing changes requested for inclusion.
3. Confirm no secret, heavy artifact, machine-specific repository path, environment, dependency tree, or
   temporary output is staged.
4. Commit coherently under Felipe Santibanez-Leal's configured Git identity, without an LLM author
   or co-author trailer, and push the current working branch frequently.
5. Promote changes to `develop` and then `main` through proper pull requests. Do not direct-push
   protected integration branches when a PR is required.
6. Report the commits, pull requests, tests, remaining dirty files, active processes, and exact next
   action.

## 7. Shared and external actions

- Experiment rounds are per-problem and may run in parallel.
- Version changes, `CHANGELOG.md`, cross-problem data bakes, frontend builds that regenerate shared
  data, tags, and the `develop` to `main` release PR are one serialized release step owned by one
  session at a time.
- Do not edit another problem's files.
- Follow methodology 09 for manuscript and Zenodo triggers. If a problem record imposes a stricter
  public-action gate, that stricter gate controls until the user explicitly changes it.
- Credentials and operational details remain in the private management repository. Never copy them
  into this public repository or into chat.
- LLMs and automated assistants are tools, never authors or co-authors in commits, pull requests,
  manuscripts, software metadata, Zenodo records, or diffusion materials.

## 8. Fast prompt recipes

Continue:

> Read the entry point at `D:\path\to\CAOS_RESEARCH\Entry_point.md` and continue working with problem
> `<problem name or slug>`.

Incorporate a new reference-led problem:

> Read the entry point at `D:\path\to\CAOS_RESEARCH\Entry_point.md`, incorporate and start working
> with problem `<problem name>` based on `<DOI, arXiv URL, paper, repository, or attached source>`.

Resume a precise round:

> Read the entry point at `D:\path\to\CAOS_RESEARCH\Entry_point.md`, resume
> `<problem slug>` from its persisted state, and continue `<EXP-NNN or backlog id>`.

Own a release:

> Read the entry point at `D:\path\to\CAOS_RESEARCH\Entry_point.md`, inspect all landed problem
> rounds since the last release, and perform the serialized CAOS Research release step.

The absolute path in the user's prompt locates the repository. All tracked documentation and
evidence inside the repository use repo-relative paths so the public record stays portable.
