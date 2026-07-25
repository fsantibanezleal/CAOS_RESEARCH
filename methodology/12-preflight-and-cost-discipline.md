# 12 - Preflight and cost discipline

Adopted 2026-07-24, derived from a measured waste audit of the Jacobian programme,
not from principle. The audit found that essentially none of the wasted effort was
computational error: the computations were correct. The waste came from decisions
about WHAT to compute, taken before cheap checks were done. The rules below are the
specific preventions, each tied to the failure that motivates it.

Every rule here is CHEAP (seconds to minutes) and guards something EXPENSIVE
(hours to days, or a wrong publication).

## The preflight checklist (run BEFORE any experiment gets machine time)

### P1. Source-complete before compute
Finish mining the primary sources bearing on the case, including the closing
remarks, final sections and bibliographic notes of papers already in our dossiers.
Only then does the case get machine time.
- COST THAT MOTIVATES IT: the C13 frontier case was derived by machine (about an
  hour plus a full delegated-agent session) and was ALREADY EXCLUDED in the
  published literature. The exclusion sat in the closing remark of a paper we had
  already cited in our own dossier. One more paragraph of reading would have
  saved the entire effort.
- CHECK: "Has any source I already cite settled this case? Did I read that source
  to the end, or only the section I needed at the time?"

### P2. Tooling smoke test before any long run
Any run expected to exceed roughly five minutes must first prove, on a tiny
instance, that it (a) emits flushed progress output and (b) writes a resumable
checkpoint. No exceptions for "it is the same code as last time".
- COST THAT MOTIVATES IT: an EXP-064 run consumed over TWENTY HOURS and produced
  ZERO output (block-buffered stdout plus a heavy symbolic backend). The identical
  mathematics, re-staged on an exact-Fraction backend with flushed staged prints,
  decided the question in 88 SECONDS. A ratio of roughly 800x, entirely from
  tooling choices.
- CHECK: run with a trivially small parameter first; confirm a progress line
  appears within seconds; confirm the resume index is written.

### P3. Declare the premise dependencies, and check them against our own record
State explicitly what the experiment's conclusion DEPENDS ON, then verify each
dependency against existing verdicts BEFORE running. Contradictions are usually
already in our own record.
- COST THAT MOTIVATES IT: the finite-ceiling claim presupposed that the pinned
  corrector ladder terminates. EXP-064 had ALREADY MEASURED that it does not. The
  contradiction was sitting in our own verdict file while the claim was written,
  published twice, and only then withdrawn.
- CHECK: list the premises; for each, name the verdict that supports it. A premise
  with no supporting verdict is a hypothesis, and must be labelled as such.

### P4. State what a PASS proves and what a FAIL proves (the one-sidedness field)
Every hypothesis.md must contain both. Many of our tests are one-sided: they can
refute but never confirm. Writing this down prevents mis-prioritising a search
that cannot deliver the answer being sought.
- COST THAT MOTIVATES IT: the degree-3 quadruple sweep consumed about FOURTEEN
  HOURS across three launches under the belief that exhausting it would decide the
  degree. It cannot: support-restricted sweeps test necessary conditions only, so
  every support passing proves nothing. Recognising this at declaration time would
  have demoted the run to a background lottery from the start.
- CHECK: "If every check passes, what have I established?" If the answer is
  "nothing positive", the run is a lottery: background priority only, and the
  positive route must be identified separately.

### P5. Invariant-first
Before committing to a heavy sweep, ask whether ONE invariant (units, class group,
weights, a degree count, a divisibility) decides the case. See methodology/10
lens 4. This has repeatedly produced one-line results where sweeps produced hours.
- CHECK: name the candidate invariants and why each does or does not apply, in the
  hypothesis, before running.

### P6. Declare the compute budget and the kill criterion
State up front: expected runtime, the budget at which the run is stopped, and what
is concluded if the budget is hit. A run stopped at budget with no result is a
recorded outcome, not a failure.
- CHECK: budget, checkpoint interval, and "if stopped early, we conclude X".

## Post-result rules

### R1. Retraction sweep covers NARRATIVE, not just headlines
When an experiment is retracted, grep the manuscripts, wiki, RESUME and mirror for
every statement that DEPENDS ON its reading, not only for its headline result.
- COST THAT MOTIVATES IT: after EXP-070 was retracted, its headline was corrected
  everywhere, but the narrative sentence it had licensed ("the obstruction MOVES
  with the degree") survived in the manuscript through three published versions,
  and the sound result says the opposite (the obstruction PERSISTS). A second
  correction pass was needed.
- CHECK: search for the retracted experiment's ID AND for the phrases its result
  motivated.

### R2. A claim enters a manuscript only if traced to a verdict line
Narrative sentences are claims. "The obstruction moves", "the campaign is a
decision procedure", "this is strong evidence" each need a verdict citation, or
they do not go in. Adjectives and framings outrun evidence more easily than
numbers do.

### R3. Publish deliberately, not reflexively
Publication is cheap to execute and permanent in the record. Before minting a new
version, re-read the changed passages against the verdicts once. Four DOI versions
in a single day, two of them correcting our own overclaims, is a signal that the
publish step ran ahead of the audit step.

## What this discipline is NOT for
It is not for slowing work down. Every rule above costs seconds to minutes. The
audit that produced them measured roughly 35 hours of avoidable compute plus two
published overclaims, all preventable by checks in this file. Speed comes from not
having to undo things.
