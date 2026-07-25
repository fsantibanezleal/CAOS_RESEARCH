# 08 - Parallel sessions and per-problem isolation

Adopted 2026-07-24 (Felipe's directive). Multiple Claude sessions may drive
different problems of this repo in parallel. These rules keep them isolated;
they BIND every session and override ad-hoc habits.

## What is already isolated (write freely, per problem)

- `problems/<area>/<slug>/`: experiments, wiki, history/log.md, context
  dossiers. Experiment rounds live entirely here.
- `program/<slug>/`: RESUME.md (the zero-loss handoff), plan, backlog, state,
  routes, strategy files.
- The frontend page component of the problem.
- The mirror: `_CAOS_MANAGE/plans/caos-research/<slug>/` (status.md +
  findings.md + history.md are PER PROBLEM).

## The shared surfaces and their ownership rules

1. **Version + CHANGELOG + tags are GLOBAL.** An experiment round therefore
   closes WITHOUT a version bump: verdict + wiki + log + RESUME + mirror,
   committed and pushed on its problem branch, then promoted to `develop` by
   pull request. The RELEASE STEP (version bump in the 3
   places, CHANGELOG entry naming every problem's landed rounds, data bake,
   frontend build, tag, PR `develop` to `main` merged) is performed by ONE session
   at a time and folds in everything since the last release. Never bump from
   two sessions concurrently; when in doubt, skip the release and keep
   committing rounds: the next release picks them up.
2. **The data bake regenerates cross-problem files** (data/derived/research/*):
   it runs ONLY inside the release step.
3. **Branch and PR discipline.** `develop` is the integration branch, not a
   parallel-session workspace. Each problem round uses or resumes a short-lived
   `work/<problem>/<topic>` branch, commits small, and pushes often. Promote the
   round to `develop` through a pull request. Parallel local sessions use separate
   git worktrees so one session never switches the branch beneath another. Pull
   BOTH repos before any write (the session-start ritual). The serialized release
   owner promotes `develop` to `main` through a separate pull request.
4. **Wiki 05 / experiment indexes are per problem** (each problem's wiki
   folder): no cross-problem index edits outside a release.
5. **Human authorship only.** Commits, pull requests, manuscripts, repository
   metadata, Zenodo records, and diffusion materials use Felipe's human identity.
   An LLM or automated assistant is never named as author or co-author.

## Session start ritual (every session, every problem)

1. Pull the current integration state in CAOS_RESEARCH and CAOS_MANAGE.
2. Create or resume the problem work branch and verify its base against `develop`.
3. Read program/<slug>/RESUME.md (the handoff) and the strategy files it names.
4. Work the rounds (hypothesis BEFORE run; verdicts honor machine results).
5. Close rounds per rule 1; release only when you own the release step.
