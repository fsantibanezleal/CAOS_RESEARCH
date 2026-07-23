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
   committed and pushed to develop. The RELEASE STEP (version bump in the 3
   places, CHANGELOG entry naming every problem's landed rounds, data bake,
   frontend build, tag, PR develop->main merged) is performed by ONE session
   at a time and folds in everything since the last release. Never bump from
   two sessions concurrently; when in doubt, skip the release and keep
   committing rounds: the next release picks them up.
2. **The data bake regenerates cross-problem files** (data/derived/research/*):
   it runs ONLY inside the release step.
3. **develop is the shared branch** (no task branches): git pull BOTH repos
   before any write (the session-start ritual), commit small, push often.
4. **Wiki 05 / experiment indexes are per problem** (each problem's wiki
   folder): no cross-problem index edits outside a release.

## Session start ritual (every session, every problem)

1. git pull in CAOS_RESEARCH and _CAOS_MANAGE.
2. Read program/<slug>/RESUME.md (the handoff) and the strategy files it names.
3. Work the rounds (hypothesis BEFORE run; verdicts honor machine results).
4. Close rounds per rule 1; release only when you own the release step.
